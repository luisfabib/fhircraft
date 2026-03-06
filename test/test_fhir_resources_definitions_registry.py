"""Unit tests for StructureDefinitionRegistry (definitions/registry.py)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, mock_open, patch

import pytest

from fhircraft.fhir.resources.definitions.registry import (
    Manifest,
    ManifestEntry,
    StructureDefinitionNotFoundError,
    StructureDefinitionRegistry,
)

# Patch targets
_MANIFEST_LOAD = "fhircraft.fhir.resources.definitions.registry.Manifest.load"
_REQUESTS_GET = "fhircraft.fhir.resources.definitions.registry.requests.get"
_GET_FHIR_TYPE = "fhircraft.fhir.resources.definitions.registry.get_fhir_type"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FHIR_RELEASE = "R4B"
SD_URL = "http://hl7.org/fhir/StructureDefinition/MyProfile"


def make_manifest(
    by_url: dict | None = None,
    by_name: dict | None = None,
    definitions: dict | None = None,
) -> Manifest:
    m = Manifest()
    m.by_url = by_url or {}
    m.by_name = by_name or {}
    m.definitions = definitions or {}
    return m


def make_sd(url: str = SD_URL, resource_type: str = "StructureDefinition") -> MagicMock:
    sd = MagicMock(name="mock-sd")
    sd.url = url
    sd._resource_type = resource_type
    return sd


def make_registry(manifest: Manifest | None = None) -> StructureDefinitionRegistry:
    """Return a registry with a mocked (empty) manifest so no filesystem access occurs."""
    with patch(_MANIFEST_LOAD, return_value=manifest or make_manifest()):
        return StructureDefinitionRegistry(FHIR_RELEASE)


# ===========================================================================
# StructureDefinitionRegistry.__init__
# ===========================================================================


def test_init__stores_fhir_release():
    reg = make_registry()
    assert reg.fhir_release == FHIR_RELEASE


def test_init__starts_with_empty_sd_cache():
    reg = make_registry()
    assert reg.structure_definitions_by_url == {}


def test_init__internet_access_disabled_by_default():
    reg = make_registry()
    assert reg._internet_access_enabled is False


def test_init__loads_manifest():
    manifest = make_manifest(by_url={"http://example.org/X": "X.json"})
    with patch(_MANIFEST_LOAD, return_value=manifest) as mock_load:
        reg = StructureDefinitionRegistry(FHIR_RELEASE)
    mock_load.assert_called_once()
    assert reg.local_manifest is manifest


# ===========================================================================
# StructureDefinitionRegistry.parse_canonical_url  (static, pure)
# ===========================================================================


def test_parse_canonical_url__plain_url_returns_no_version():
    url, version = StructureDefinitionRegistry.parse_canonical_url(
        "http://example.org/X"
    )
    assert url == "http://example.org/X"
    assert version is None


def test_parse_canonical_url__url_with_version_splits_correctly():
    url, version = StructureDefinitionRegistry.parse_canonical_url(
        "http://example.org/X|1.0.0"
    )
    assert url == "http://example.org/X"
    assert version == "1.0.0"


def test_parse_canonical_url__strips_surrounding_whitespace():
    url, version = StructureDefinitionRegistry.parse_canonical_url(
        " http://example.org/X | 2.0 "
    )
    assert url == "http://example.org/X"
    assert version == "2.0"


# ===========================================================================
# StructureDefinitionRegistry.enable_internet_access / disable_internet_access
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
# StructureDefinitionRegistry.set_registry_base_url
# ===========================================================================


def test_set_registry_base_url__updates_package_client_base_url():
    reg = make_registry()
    reg.set_registry_base_url("https://my-registry.example.org")
    assert reg._package_client.base_url == "https://my-registry.example.org"


# ===========================================================================
# StructureDefinitionRegistry.__contains__
# ===========================================================================


def test_contains__returns_true_for_url_in_memory_cache():
    reg = make_registry()
    sd = make_sd()
    reg.structure_definitions_by_url[sd.url] = sd
    assert sd.url in reg


def test_contains__returns_true_for_url_in_local_manifest():
    manifest = make_manifest(by_url={SD_URL: "MyProfile.json"})
    reg = make_registry(manifest)
    assert SD_URL in reg


def test_contains__returns_false_for_unknown_url():
    reg = make_registry()
    assert "http://example.org/Unknown" not in reg


# ===========================================================================
# StructureDefinitionRegistry.add
# ===========================================================================


def test_add__stores_sd_in_memory_cache():
    reg = make_registry()
    sd = make_sd()
    reg.add(sd)
    assert SD_URL in reg.structure_definitions_by_url


def test_add__raises_value_error_when_sd_has_no_url():
    reg = make_registry()
    sd = make_sd(url="")
    with pytest.raises(ValueError):
        reg.add(sd)


def test_add__raises_value_error_on_duplicate_when_fail_if_exists():
    reg = make_registry()
    sd = make_sd()
    reg.add(sd)
    with pytest.raises(ValueError):
        reg.add(sd, fail_if_exists=True)


def test_add__does_not_raise_on_duplicate_when_fail_if_exists_false():
    reg = make_registry()
    sd = make_sd()
    reg.add(sd)
    reg.add(sd, fail_if_exists=False)  # should not raise


def test_add__strips_version_from_url():
    reg = make_registry()
    sd = make_sd(url="http://example.org/X|1.0.0")
    reg.add(sd)
    assert "http://example.org/X" in reg.structure_definitions_by_url


def test_add__versioned_and_base_url_stored_under_base_key():
    reg = make_registry()
    sd = make_sd(url="http://example.org/X|2.0")
    reg.add(sd)
    assert "http://example.org/X|2.0" not in reg.structure_definitions_by_url
    assert "http://example.org/X" in reg.structure_definitions_by_url


# ===========================================================================
# StructureDefinitionRegistry.get – in-memory cache lookup
# ===========================================================================


def test_get__returns_sd_from_memory_cache():
    reg = make_registry()
    sd = make_sd()
    reg.structure_definitions_by_url[SD_URL] = sd
    assert reg.get(SD_URL) is sd


def test_get__does_not_call_manifest_when_sd_is_in_cache():
    reg = make_registry()
    sd = make_sd()
    reg.structure_definitions_by_url[SD_URL] = sd
    reg.local_manifest.by_url = MagicMock()  # would raise if accessed via get
    result = reg.get(SD_URL)
    assert result is sd


# ===========================================================================
# StructureDefinitionRegistry.get – local manifest lookup
# ===========================================================================


def test_get__loads_sd_from_local_manifest_file():
    reg = StructureDefinitionRegistry(FHIR_RELEASE)
    result = reg.get("http://hl7.org/fhir/StructureDefinition/Patient")
    assert result is not None


def test_get__raises_file_not_found_when_manifest_entry_file_missing(tmp_path):
    manifest = make_manifest(by_url={SD_URL: "Missing.json"})
    with patch(_MANIFEST_LOAD, return_value=manifest):
        reg = StructureDefinitionRegistry(FHIR_RELEASE)

    with patch(
        "fhircraft.fhir.resources.definitions.registry.DEFINITIONS_DIR",
        tmp_path,  # entries/ sub-dir doesn't exist → file missing
    ):
        with pytest.raises(FileNotFoundError):
            reg.get(SD_URL)


# ===========================================================================
# StructureDefinitionRegistry.get – internet fallback
# ===========================================================================


def test_get__raises_not_found_when_internet_disabled_and_sd_unknown():
    reg = make_registry()
    with pytest.raises(StructureDefinitionNotFoundError):
        reg.get("http://example.org/Unknown")


def test_get__fetches_from_internet_when_enabled():
    reg = make_registry()
    reg.enable_internet_access()
    sd = make_sd()

    with (
        patch.object(reg, "download_url", return_value={"url": SD_URL}) as mock_dl,
        patch.object(reg, "_validate_structure_definition", return_value=sd),
    ):
        result = reg.get(SD_URL)

    mock_dl.assert_called_once_with(SD_URL)
    assert result is sd


def test_get__internet_lookup_stores_result_in_cache():
    reg = make_registry()
    reg.enable_internet_access()
    sd = make_sd()

    with (
        patch.object(reg, "download_url", return_value={"url": SD_URL}),
        patch.object(reg, "_validate_structure_definition", return_value=sd),
    ):
        reg.get(SD_URL)

    assert SD_URL in reg.structure_definitions_by_url


# ===========================================================================
# StructureDefinitionRegistry.download_url  (static)
# ===========================================================================


def test_download_url__calls_requests_get_with_url():
    mock_response = MagicMock()
    mock_response.json.return_value = {"resourceType": "StructureDefinition"}
    with (
        patch(_REQUESTS_GET, return_value=mock_response) as mock_get,
        patch(
            "fhircraft.fhir.resources.definitions.registry.load_env_variables",
            return_value={},
        ),
    ):
        StructureDefinitionRegistry.download_url("http://example.org/X")

    mock_get.assert_called_once()
    assert mock_get.call_args[0][0] == "http://example.org/X"


def test_download_url__returns_response_json():
    payload = {"resourceType": "StructureDefinition", "url": SD_URL}
    mock_response = MagicMock()
    mock_response.json.return_value = payload
    with (
        patch(_REQUESTS_GET, return_value=mock_response),
        patch(
            "fhircraft.fhir.resources.definitions.registry.load_env_variables",
            return_value={},
        ),
    ):
        result = StructureDefinitionRegistry.download_url("http://example.org/X")

    assert result == payload


def test_download_url__calls_raise_for_status():
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    with (
        patch(_REQUESTS_GET, return_value=mock_response),
        patch(
            "fhircraft.fhir.resources.definitions.registry.load_env_variables",
            return_value={},
        ),
    ):
        StructureDefinitionRegistry.download_url("http://example.org/X")

    mock_response.raise_for_status.assert_called_once()


# ===========================================================================
# StructureDefinitionRegistry.download_package
# ===========================================================================


def test_download_package__calls_load_resources_from_package():
    reg = make_registry()
    sd = make_sd()
    reg._package_client = MagicMock()
    reg._package_client.load_resources_from_package.return_value = [{"url": SD_URL}]

    with patch.object(reg, "_validate_structure_definition", return_value=sd):
        reg.download_package("hl7.fhir.r4b.core", "4.3.0")

    reg._package_client.load_resources_from_package.assert_called_once_with(
        "StructureDefinition", "hl7.fhir.r4b.core", "4.3.0"
    )


def test_download_package__adds_each_validated_sd():
    reg = make_registry()
    sd_a = make_sd(url="http://example.org/A")
    sd_b = make_sd(url="http://example.org/B")
    reg._package_client = MagicMock()
    reg._package_client.load_resources_from_package.return_value = [
        {"url": "http://example.org/A"},
        {"url": "http://example.org/B"},
    ]

    with patch.object(reg, "_validate_structure_definition", side_effect=[sd_a, sd_b]):
        reg.download_package("pkg", "1.0")

    assert "http://example.org/A" in reg.structure_definitions_by_url
    assert "http://example.org/B" in reg.structure_definitions_by_url


# ===========================================================================
# StructureDefinitionRegistry.from_dict
# ===========================================================================


def test_from_dict__validates_and_stores_sd():
    reg = make_registry()
    sd = make_sd()
    with patch.object(reg, "_validate_structure_definition", return_value=sd) as mock_v:
        result = reg.from_dict({"url": SD_URL})

    mock_v.assert_called_once_with({"url": SD_URL})
    assert result is sd
    assert SD_URL in reg.structure_definitions_by_url


def test_from_dict__returns_validated_sd():
    reg = make_registry()
    sd = make_sd()
    with patch.object(reg, "_validate_structure_definition", return_value=sd):
        result = reg.from_dict({"url": SD_URL})
    assert result is sd


# ===========================================================================
# Manifest helpers
# ===========================================================================


def test_manifest_contains__true_for_url_in_by_url():
    m = make_manifest(by_url={SD_URL: "X.json"})
    assert SD_URL in m


def test_manifest_contains__true_for_name_in_by_name():
    m = make_manifest(by_name={"MyProfile": [SD_URL]})
    assert "MyProfile" in m


def test_manifest_contains__false_for_unknown():
    m = make_manifest()
    assert "http://example.org/Unknown" not in m
