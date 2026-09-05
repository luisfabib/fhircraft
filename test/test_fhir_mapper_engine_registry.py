"""Unit tests for StructureMapRegistry (fhir/mapper/engine/registry.py)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from fhircraft.fhir.mapper.engine.registry import (
    MapperRegistryNotFoundError,
    StructureMapRegistry,
)
from fhircraft.utils import FHIRRelease

# ---------------------------------------------------------------------------
# Patch targets
# ---------------------------------------------------------------------------

_REQUESTS_GET = "fhircraft.fhir.mapper.engine.registry.requests.get"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FHIR_RELEASE = "R5"
SM_URL = "http://example.org/fhir/StructureMap/MyMap"
SM_URL_VERSIONED = f"{SM_URL}|1.0.0"


def make_group(name: str) -> MagicMock:
    group = MagicMock(name=f"mock-group-{name}")
    group.name = name
    return group


def make_sm(
    url: str = SM_URL,
    groups: list | None = None,
) -> MagicMock:
    sm = MagicMock(name="mock-structure-map")
    sm.url = url
    sm.group = groups or [make_group("default")]
    return sm


def make_registry(fhir_release: FHIRRelease = FHIR_RELEASE) -> StructureMapRegistry:
    return StructureMapRegistry(fhir_release=fhir_release)


# ===========================================================================
# StructureMapRegistry.__init__
# ===========================================================================


def test_init__stores_fhir_release():
    reg = make_registry()
    assert reg.fhir_release == FHIR_RELEASE


def test_init__starts_with_empty_manifest():
    reg = make_registry()
    assert reg.structure_maps_by_url == {}


def test_init__internet_access_disabled_by_default():
    reg = make_registry()
    assert reg._internet_access_enabled is False


def test_init__raises_for_unsupported_release():
    with pytest.raises(ValueError, match="Unsupported FHIR release"):
        StructureMapRegistry(fhir_release="R3")


def test_init__accepts_r4_release():
    reg = StructureMapRegistry(fhir_release="R4")
    assert reg.fhir_release == "R4"


def test_init__accepts_r4b_release():
    reg = StructureMapRegistry(fhir_release="R4B")
    assert reg.fhir_release == "R4B"


# ===========================================================================
# StructureMapRegistry.parse_canonical_url  (static, pure)
# ===========================================================================


def test_parse_canonical_url__plain_url_returns_no_version():
    base, version = StructureMapRegistry.parse_canonical_url(SM_URL)
    assert base == SM_URL
    assert version is None


def test_parse_canonical_url__url_with_version_splits_correctly():
    base, version = StructureMapRegistry.parse_canonical_url(SM_URL_VERSIONED)
    assert base == SM_URL
    assert version == "1.0.0"


def test_parse_canonical_url__strips_surrounding_whitespace():
    base, version = StructureMapRegistry.parse_canonical_url(f" {SM_URL} | 2.0 ")
    assert base == SM_URL
    assert version == "2.0"


# ===========================================================================
# StructureMapRegistry.enable_internet_access / disable_internet_access
# ===========================================================================


def test_enable_internet_access__sets_flag_true():
    reg = make_registry()
    reg.enable_internet_access()
    assert reg._internet_access_enabled is True


def test_disable_internet_access__sets_flag_false():
    reg = make_registry()
    reg.enable_internet_access()
    reg.disable_internet_access()
    assert reg._internet_access_enabled is False


# ===========================================================================
# StructureMapRegistry.__contains__
# ===========================================================================


def test_contains__returns_true_for_registered_url():
    reg = make_registry()
    sm = make_sm()
    reg.structure_maps_by_url[SM_URL] = sm
    assert SM_URL in reg


def test_contains__returns_true_for_versioned_url_when_base_registered():
    reg = make_registry()
    sm = make_sm()
    reg.structure_maps_by_url[SM_URL] = sm
    assert SM_URL_VERSIONED in reg


def test_contains__returns_false_for_unknown_url():
    reg = make_registry()
    assert "http://example.org/Unknown" not in reg


# ===========================================================================
# StructureMapRegistry.add
# ===========================================================================


def test_add__stores_sm_in_memory_manifest():
    reg = make_registry()
    sm = make_sm()
    reg.add(sm)
    assert SM_URL in reg.structure_maps_by_url


def test_add__strips_version_from_url():
    reg = make_registry()
    sm = make_sm(url=SM_URL_VERSIONED)
    reg.add(sm)
    assert SM_URL in reg.structure_maps_by_url
    assert SM_URL_VERSIONED not in reg.structure_maps_by_url


def test_add__raises_value_error_when_sm_has_no_url():
    reg = make_registry()
    sm = make_sm(url="")
    # Falsy URL should raise
    with pytest.raises(ValueError, match="url"):
        reg.add(sm)


def test_add__raises_value_error_on_duplicate_when_fail_if_exists():
    reg = make_registry()
    sm = make_sm()
    reg.add(sm)
    with pytest.raises(ValueError, match="already exists"):
        reg.add(sm, fail_if_exists=True)


def test_add__does_not_raise_on_duplicate_when_fail_if_exists_false():
    reg = make_registry()
    sm = make_sm()
    reg.add(sm)
    reg.add(sm, fail_if_exists=False)  # should not raise


def test_add__versioned_and_base_url_both_stored_under_base_key():
    reg = make_registry()
    sm_base = make_sm(url=SM_URL)
    sm_ver = make_sm(url=SM_URL_VERSIONED)
    reg.add(sm_base)
    reg.add(sm_ver)
    # Both resolve to the same base key; second overwrites first
    assert SM_URL in reg.structure_maps_by_url
    assert reg.structure_maps_by_url[SM_URL] is sm_ver


# ===========================================================================
# StructureMapRegistry.get
# ===========================================================================


def test_get__returns_sm_from_memory_manifest():
    reg = make_registry()
    sm = make_sm()
    reg.structure_maps_by_url[SM_URL] = sm
    result = reg.get(SM_URL)
    assert result is sm


def test_get__returns_sm_when_queried_with_versioned_url():
    reg = make_registry()
    sm = make_sm()
    reg.structure_maps_by_url[SM_URL] = sm
    result = reg.get(SM_URL_VERSIONED)
    assert result is sm


def test_get__raises_when_not_found_and_internet_disabled():
    reg = make_registry()
    with pytest.raises(MapperRegistryNotFoundError):
        reg.get(SM_URL)


def test_get__downloads_and_manifests_when_internet_enabled():
    reg = make_registry()
    reg.enable_internet_access()

    raw_sm: dict[str, Any] = {
        "resourceType": "StructureMap",
        "url": SM_URL,
        "name": "MyMap",
        "status": "active",
        "group": [
            {
                "name": "test-group",
                "input": [{"name": "test-input", "mode": "source"}],
            }
        ],
    }

    mock_response = MagicMock()
    mock_response.json.return_value = raw_sm
    mock_response.raise_for_status = MagicMock()

    with patch(_REQUESTS_GET, return_value=mock_response):
        result = reg.get(SM_URL)

    # Should now be manifestd
    assert SM_URL in reg.structure_maps_by_url
    assert result.url == SM_URL


def test_get__does_not_call_internet_when_disabled():
    reg = make_registry()
    with patch(_REQUESTS_GET) as mock_get:
        with pytest.raises(MapperRegistryNotFoundError):
            reg.get(SM_URL)
    mock_get.assert_not_called()


# ===========================================================================
# StructureMapRegistry.from_dict
# ===========================================================================


def test_from_dict__validates_and_registers_valid_sm():
    reg = make_registry()
    raw: dict[str, Any] = {
        "resourceType": "StructureMap",
        "url": SM_URL,
        "name": "MyMap",
        "status": "active",
        "group": [
            {
                "name": "test-group",
                "input": [{"name": "test-input", "mode": "source"}],
            }
        ],
    }
    result = reg.from_dict(raw)
    assert result.url == SM_URL
    assert SM_URL in reg.structure_maps_by_url


def test_from_dict__raises_on_invalid_data():
    reg = make_registry()
    with pytest.raises(ValueError, match="StructureMap"):
        reg.from_dict({"resourceType": "Patient", "url": SM_URL, "group": []})


def test_from_dict__respects_fail_if_exists():
    reg = make_registry()
    raw: dict[str, Any] = {
        "resourceType": "StructureMap",
        "url": SM_URL,
        "name": "MyMap",
        "status": "active",
        "group": [
            {
                "name": "test-group",
                "input": [{"name": "test-input", "mode": "source"}],
            }
        ],
    }
    reg.from_dict(raw)
    with pytest.raises(ValueError, match="already exists"):
        reg.from_dict(raw, fail_if_exists=True)


# ===========================================================================
# StructureMapRegistry.download_url
# ===========================================================================


def test_download_url__calls_requests_get_with_correct_url():
    mock_response = MagicMock()
    mock_response.json.return_value = {"resourceType": "StructureMap"}
    mock_response.raise_for_status = MagicMock()

    with patch(_REQUESTS_GET, return_value=mock_response) as mock_get:
        result = StructureMapRegistry.download_url(SM_URL)

    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert (
        call_args[0][0] == SM_URL
        or call_args[1].get("url") == SM_URL
        or SM_URL in str(call_args)
    )


def test_download_url__raises_on_http_error():
    import requests as req

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = req.HTTPError("404")

    with patch(_REQUESTS_GET, return_value=mock_response):
        with pytest.raises(req.HTTPError):
            StructureMapRegistry.download_url(SM_URL)
