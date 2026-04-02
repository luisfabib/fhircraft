import pytest
from fhircraft.fhir.resources.base import FHIRPrimitiveModel, FHIRBaseModel
from fhircraft.fhir.resources.datatypes.registry import (
    TypeRegistry,
    get_fhir_type,
    get_fhir_type_by_url,
    get_registry,
)


# ---------------------------------------------------------------------------
# Parametrize data
# ---------------------------------------------------------------------------

URL_BASE = "http://hl7.org/fhir/StructureDefinition/"

FHIR_RELEASES = ["R4", "R4B", "R5"]

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
    "CodeableConcept",
    "Coding",
    "HumanName",
    "Address",
    "Quantity",
    "Period",
    "Reference",
    "Identifier",
    "ContactPoint",
    "Coding",
]

# (name, release) pairs for resource types.
_RESOURCE_CASES = [
    "Observation",
    "Patient",
    "Condition",
    "Encounter",
]

# Canonical URLs for get_fhir_type_by_url — exact casing from the FHIR manifest.
_PRIMITIVE_URLS = [
    f"{URL_BASE}{name}"
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
    f"{URL_BASE}{name}"
    for name in [
        "HumanName",
        "Address",
        "Quantity",
        "Period",
        "Reference",
        "Identifier",
        "CodeableConcept",
    ]
]

_RESOURCE_URLS = [
    f"{URL_BASE}{name}"
    for name in [
        "Observation",
        "Patient",
        "Condition",
        "Encounter",
        "Observation",
    ]
]


# ===========================================================================
# get_fhir_type
# ===========================================================================


@pytest.mark.parametrize(
    "type_str", _PRIMITIVES + _PRIMITIVE_CAMEL + _COMPLEX_CASES + _RESOURCE_CASES
)
@pytest.mark.parametrize("release", FHIR_RELEASES)
def test_get_fhir_type__returns_non_none_type(release: str, type_str: str):
    result = get_fhir_type(type_str, release, fail_if_not_found=True)
    assert result is not None


@pytest.mark.parametrize("type_str", _PRIMITIVES)
@pytest.mark.parametrize("release", FHIR_RELEASES)
def test_get_fhir_type__primitive_is_type_alias(release: str, type_str: str):
    result = get_fhir_type(type_str, release)
    assert isinstance(result, type)
    assert issubclass(result, FHIRPrimitiveModel)


@pytest.mark.parametrize("type_str", _COMPLEX_CASES + _RESOURCE_CASES)
@pytest.mark.parametrize("release", FHIR_RELEASES)
def test_get_fhir_type__complex_and_resource_is_type(release: str, type_str: str):
    result = get_fhir_type(type_str, release)
    assert isinstance(result, type)
    assert issubclass(result, FHIRBaseModel)


def test_get_fhir_type__raises_attribute_error_for_unknown_name():
    with pytest.raises(AttributeError):
        get_fhir_type("NoSuchTypeThatExists", "R4B", fail_if_not_found=True)


def test_get_fhir_type__returns_none_for_unknown_name_when_not_fail():
    result = get_fhir_type("NoSuchTypeThatExists", "R4B", fail_if_not_found=False)
    assert result is None


# ===========================================================================
# get_fhir_type_by_url
# ===========================================================================


@pytest.mark.parametrize("url", _PRIMITIVE_URLS + _COMPLEX_URLS + _RESOURCE_URLS)
@pytest.mark.parametrize("release", FHIR_RELEASES)
def test_get_fhir_type_by_url__returns_non_none_type(release: str, url: str):
    result = get_fhir_type_by_url(url, release, fail_if_not_found=True)
    assert result is not None


@pytest.mark.parametrize("url", _PRIMITIVE_URLS)
@pytest.mark.parametrize("release", FHIR_RELEASES)
def test_get_fhir_type_by_url__primitive_url_returns_type_alias(release: str, url: str):
    result = get_fhir_type_by_url(url, release)
    assert isinstance(result, type)
    assert issubclass(result, FHIRPrimitiveModel)


@pytest.mark.parametrize("url", _COMPLEX_URLS + _RESOURCE_URLS)
@pytest.mark.parametrize("release", FHIR_RELEASES)
def test_get_fhir_type_by_url__complex_and_resource_url_returns_type(
    release: str, url: str
):
    result = get_fhir_type_by_url(url, release)
    assert isinstance(result, type)
    assert issubclass(result, FHIRBaseModel)


def test_get_fhir_type_by_url__raises_attribute_error_for_unknown_url():
    with pytest.raises(AttributeError):
        get_fhir_type_by_url(
            "http://example.org/no-such-type", "R4B", fail_if_not_found=True
        )


def test_get_fhir_type_by_url__returns_none_for_unknown_url_when_not_fail():
    result = get_fhir_type_by_url(
        "http://example.org/no-such-type", "R4B", fail_if_not_found=False
    )
    assert result is None


# ===========================================================================
# get_registry
# ===========================================================================


@pytest.mark.parametrize("release", FHIR_RELEASES)
def test_get_registry__returns_type_registry_instance(release: str):
    assert isinstance(get_registry(release), TypeRegistry)


@pytest.mark.parametrize("release", FHIR_RELEASES)
def test_get_registry__each_release_loads(release: str):
    reg = get_registry(release)
    assert reg.release == release


@pytest.mark.parametrize("release", FHIR_RELEASES)
def test_get_registry__returns_same_object_on_repeated_calls(release: str):
    a = get_registry(release)
    b = get_registry(release)
    assert a is b
