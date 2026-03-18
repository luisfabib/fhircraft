"""Unit tests for the TypeRegistry and public module functions.

Each public function that performs a lookup has a single parametrized test that
covers every primitive type plus a representative selection of complex types and
resources across all three supported FHIR releases.
"""

from __future__ import annotations

from typing_extensions import TypeAliasType  # primitives use typing_extensions
from unittest.mock import patch

import pytest

from fhircraft.fhir.resources.datatypes.registry import (
    TypeRegistry,
    _registry_cache,
    get_fhir_type,
    get_fhir_type_by_url,
    get_registry,
)
from fhircraft.fhir.resources.datatypes import primitives


# ---------------------------------------------------------------------------
# Parametrize data
# ---------------------------------------------------------------------------

# Every primitive exported by primitives.py (PascalCase names).
_PRIMITIVES = [
    "Base64Binary",
    "Boolean",
    "Canonical",
    "Code",
    "Date",
    "DateTime",
    "Decimal",
    "Id",
    "Instant",
    "Integer",
    "Integer64",
    "Markdown",
    "Oid",
    "PositiveInt",
    "String",
    "Time",
    "UnsignedInt",
    "Uri",
    "Url",
    "Uuid",
]

# Primitive camelCase aliases (as stored in FHIR manifests).
_PRIMITIVE_CAMEL = [
    "base64Binary",
    "boolean",
    "canonical",
    "code",
    "date",
    "dateTime",
    "decimal",
    "id",
    "instant",
    "integer",
    "markdown",
    "oid",
    "positiveInt",
    "string",
    "time",
    "unsignedInt",
    "uri",
    "url",
    "uuid",
]

# (name, release) pairs for complex types.
_COMPLEX_CASES = [
    ("CodeableConcept", "R4"),
    ("CodeableConcept", "R4B"),
    ("CodeableConcept", "R5"),
    ("HumanName", "R4"),
    ("HumanName", "R4B"),
    ("HumanName", "R5"),
    ("Address", "R4B"),
    ("Quantity", "R4B"),
    ("Period", "R4B"),
    ("Reference", "R4B"),
    ("Identifier", "R4B"),
    ("ContactPoint", "R4B"),
]

# (name, release) pairs for resource types.
_RESOURCE_CASES = [
    ("Observation", "R4"),
    ("Observation", "R4B"),
    ("Observation", "R5"),
    ("Patient", "R4B"),
    ("Condition", "R4B"),
    ("Encounter", "R4B"),
]

# Canonical URLs for get_fhir_type_by_url — exact casing from the FHIR manifest.
_PRIMITIVE_URLS = [
    (f"http://hl7.org/fhir/StructureDefinition/{name}", "R4B")
    for name in [
        "boolean",
        "string",
        "integer",
        "decimal",
        "uri",
        "url",
        "canonical",
        "base64Binary",
        "instant",
        "date",
        "dateTime",
        "time",
        "code",
        "oid",
        "id",
        "markdown",
        "unsignedInt",
        "positiveInt",
        "uuid",
    ]
]

# Canonical URLs for complex and resource types.
_COMPLEX_URLS = [
    ("http://hl7.org/fhir/StructureDefinition/CodeableConcept", "R4B"),
    ("http://hl7.org/fhir/StructureDefinition/HumanName", "R4B"),
    ("http://hl7.org/fhir/StructureDefinition/Address", "R4B"),
    ("http://hl7.org/fhir/StructureDefinition/Quantity", "R4B"),
    ("http://hl7.org/fhir/StructureDefinition/Period", "R4B"),
    ("http://hl7.org/fhir/StructureDefinition/Reference", "R4B"),
    ("http://hl7.org/fhir/StructureDefinition/Identifier", "R4B"),
    ("http://hl7.org/fhir/StructureDefinition/CodeableConcept", "R4"),
    ("http://hl7.org/fhir/StructureDefinition/CodeableConcept", "R5"),
]

_RESOURCE_URLS = [
    ("http://hl7.org/fhir/StructureDefinition/Observation", "R4B"),
    ("http://hl7.org/fhir/StructureDefinition/Patient", "R4B"),
    ("http://hl7.org/fhir/StructureDefinition/Condition", "R4B"),
    ("http://hl7.org/fhir/StructureDefinition/Encounter", "R4B"),
    ("http://hl7.org/fhir/StructureDefinition/Observation", "R4"),
    ("http://hl7.org/fhir/StructureDefinition/Observation", "R5"),
]


# ===========================================================================
# get_fhir_type
# ===========================================================================


@pytest.mark.parametrize(
    "type_str, release",
    # Every primitive by PascalCase name across all three releases
    [(name, release) for name in _PRIMITIVES for release in ("R4", "R4B", "R5")]
    # camelCase aliases (manifest style) for R4B
    + [(name, "R4B") for name in _PRIMITIVE_CAMEL]
    # Complex types
    + [(name, release) for name, release in _COMPLEX_CASES]
    # Resources
    + [(name, release) for name, release in _RESOURCE_CASES],
)
def test_get_fhir_type__returns_non_none_type(type_str: str, release: str) -> None:
    result = get_fhir_type(type_str, release, fail_if_not_found=True)
    assert result is not None


@pytest.mark.parametrize(
    "type_str, release",
    [(name, "R4B") for name in _PRIMITIVES],
)
def test_get_fhir_type__primitive_is_type_alias(type_str: str, release: str) -> None:
    result = get_fhir_type(type_str, release)
    assert isinstance(result, TypeAliasType)


@pytest.mark.parametrize(
    "type_str, release",
    [(name, release) for name, release in _COMPLEX_CASES]
    + [(name, release) for name, release in _RESOURCE_CASES],
)
def test_get_fhir_type__complex_and_resource_is_type(
    type_str: str, release: str
) -> None:
    result = get_fhir_type(type_str, release)
    assert isinstance(result, type)


def test_get_fhir_type__raises_attribute_error_for_unknown_name() -> None:
    with pytest.raises(AttributeError):
        get_fhir_type("NoSuchTypeThatExists", "R4B", fail_if_not_found=True)


def test_get_fhir_type__returns_none_for_unknown_name_when_not_fail() -> None:
    result = get_fhir_type("NoSuchTypeThatExists", "R4B", fail_if_not_found=False)
    assert result is None


# ===========================================================================
# get_fhir_type_by_url
# ===========================================================================


@pytest.mark.parametrize(
    "url, release",
    _PRIMITIVE_URLS + _COMPLEX_URLS + _RESOURCE_URLS,
)
def test_get_fhir_type_by_url__returns_non_none_type(url: str, release: str) -> None:
    result = get_fhir_type_by_url(url, release, fail_if_not_found=True)
    assert result is not None


@pytest.mark.parametrize("url, release", _PRIMITIVE_URLS)
def test_get_fhir_type_by_url__primitive_url_returns_type_alias(
    url: str, release: str
) -> None:
    result = get_fhir_type_by_url(url, release)
    assert isinstance(result, TypeAliasType)


@pytest.mark.parametrize("url, release", _COMPLEX_URLS + _RESOURCE_URLS)
def test_get_fhir_type_by_url__complex_and_resource_url_returns_type(
    url: str, release: str
) -> None:
    result = get_fhir_type_by_url(url, release)
    assert isinstance(result, type)


def test_get_fhir_type_by_url__raises_attribute_error_for_unknown_url() -> None:
    with pytest.raises(AttributeError):
        get_fhir_type_by_url(
            "http://example.org/no-such-type", "R4B", fail_if_not_found=True
        )


def test_get_fhir_type_by_url__returns_none_for_unknown_url_when_not_fail() -> None:
    result = get_fhir_type_by_url(
        "http://example.org/no-such-type", "R4B", fail_if_not_found=False
    )
    assert result is None


# ===========================================================================
# get_registry
# ===========================================================================


def test_get_registry__returns_type_registry_instance() -> None:
    assert isinstance(get_registry("R4B"), TypeRegistry)


@pytest.mark.parametrize("release", ["R4", "R4B", "R5"])
def test_get_registry__each_release_loads(release: str) -> None:
    reg = get_registry(release)
    assert reg.release == release


def test_get_registry__returns_same_object_on_repeated_calls() -> None:
    a = get_registry("R4B")
    b = get_registry("R4B")
    assert a is b
