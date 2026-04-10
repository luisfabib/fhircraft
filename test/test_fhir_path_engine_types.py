from collections import namedtuple

import pytest

from fhircraft.fhir.path.engine.core import (
    Element,
    This,
    FHIRPathCollectionItem,
    TypeSpecifier,
)
from fhircraft.fhir.path.engine.literals import Date, Quantity
from fhircraft.fhir.path.engine.types import Is, As, LegacyIs, LegacyAs
from fhircraft.fhir.resources.datatypes.R4.primitive import (
    Code,
    String as FHIRString,
    Integer as FHIRInteger,
    Boolean as FHIRBoolean,
    Decimal as FHIRDecimal,
    Date as FHIRDate,
    DateTime as FHIRDateTime,
    Time as FHIRTime,
    Instant as FHIRInstant,
    Uri as FHIRUri,
    Canonical as FHIRCanonical,
    PositiveInt as FHIRPositiveInt,
    UnsignedInt as FHIRUnsignedInt,
)
from fhircraft.fhir.resources.datatypes.R4.core.observation import Observation
from fhircraft.fhir.resources.datatypes.R4.core.practitioner import Practitioner

env = {"%fhirRelease": "R4"}

# -------------
# Is
# -------------

test_cases = (
    # FHIR String type checking
    ("ABC", "FHIR.string", True),
    ("123", "FHIR.string", True),
    ("", "FHIR.string", True),
    (123, "FHIR.string", False),
    # FHIR Integer type checking
    (12, "FHIR.integer", True),
    (-12, "FHIR.integer", True),
    (0, "FHIR.integer", True),
    ("12", "FHIR.integer", True),
    ("-12", "FHIR.integer", True),
    # FHIR UnsignedInt type checking
    (12, "FHIR.unsignedInt", True),
    ("12", "FHIR.unsignedInt", True),
    (0, "FHIR.unsignedInt", True),
    (-12, "FHIR.unsignedInt", False),
    ("-12", "FHIR.unsignedInt", False),
    # FHIR PositiveInt type checking
    (12, "FHIR.positiveInt", True),
    ("12", "FHIR.positiveInt", True),
    (0, "FHIR.positiveInt", False),
    (-12, "FHIR.positiveInt", False),
    ("-12", "FHIR.positiveInt", False),
    # System Integer type checking
    (12, "System.Integer", True),
    ("12", "System.Integer", False),
    (0, "System.Integer", True),
    (-12, "System.Integer", True),
    ("-12", "System.Integer", False),
    # FHIR Decimal type checking
    (23, "FHIR.decimal", True),
    (23.32, "FHIR.decimal", True),
    ("23.32", "FHIR.decimal", True),
    ("23", "FHIR.decimal", True),
    # System Decimal type checking
    (23, "System.Decimal", False),
    (23.32, "System.Decimal", True),
    ("23.32", "System.Decimal", False),
    ("23", "System.Decimal", False),
    # FHIR Boolean type checking
    (True, "FHIR.boolean", True),
    ("true", "FHIR.boolean", True),
    (False, "FHIR.boolean", True),
    ("false", "FHIR.boolean", True),
    ("invalid", "FHIR.boolean", False),
    # System Boolean type checking
    (True, "System.Boolean", True),
    ("true", "System.Boolean", False),
    (False, "System.Boolean", True),
    ("false", "System.Boolean", False),
    ("invalid", "System.Boolean", False),
    # FHIR Complex type checking
    (Date("@2024"), "FHIR.date", True),
    (Quantity(12, "g"), "FHIR.Quantity", True),
    (Practitioner(gender="example"), "FHIR.Practitioner", True),
    (Observation(status="example"), "FHIR.Observation", True),
    # System Complex type checking
    (Date("@2024"), "System.Date", True),
    (Quantity(12, "g"), "System.Quantity", True),
    (Practitioner(gender="example"), "System.Quantity", False),
    (Observation(status="example"), "System.Quantity", False),
    # FHIR primitive class instances — type checking via is/as
    (FHIRString(value="ABC"), "FHIR.string", True),
    (FHIRInteger(value=12), "FHIR.integer", True),
    (FHIRBoolean(value=True), "FHIR.boolean", True),
    (FHIRDecimal(value=23.32), "FHIR.decimal", True),
    (FHIRDate(value="2024-01-01"), "FHIR.date", True),
    (FHIRDateTime(value="2024-01-01T10:30:00"), "FHIR.dateTime", True),
    (FHIRTime(value="10:30:00"), "FHIR.time", True),
    (FHIRInstant(value="2024-01-15T10:30:00Z"), "FHIR.instant", True),
    (FHIRUri(value="http://example.com"), "FHIR.uri", True),
    (
        FHIRCanonical(value="http://hl7.org/fhir/ValueSet/example"),
        "FHIR.canonical",
        True,
    ),
    (FHIRPositiveInt(value=5), "FHIR.positiveInt", True),
    (FHIRUnsignedInt(value=5), "FHIR.unsignedInt", True),
    # Cross-type checks — primitive instance against wrong type specifier
    (FHIRString(value="ABC"), "FHIR.integer", False),
    (FHIRInteger(value=12), "FHIR.string", False),
)


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
@pytest.mark.parametrize("left, type_specifier, expected", test_cases)
def test_is_returns_correct_boolean(left, type_specifier, expected):
    resource = namedtuple("Resource", ["left"])(left=left)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Is(Element("left"), TypeSpecifier(type_specifier)).evaluate(
        collection, env
    )
    assert result[0].value == expected


def test_is_returns_empty_for_empty_collection():
    result = Is(Element("left"), TypeSpecifier("string")).evaluate([], env)
    assert result == []


def test_is_string_representation():
    expression = Is(Element("field"), TypeSpecifier("string"))
    assert str(expression) == "field is string"


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
@pytest.mark.parametrize("left, type_specifier, expected", test_cases)
def test_legacy_is_returns_correct_boolean(left, type_specifier, expected):
    collection = [FHIRPathCollectionItem(value=left)]
    result = LegacyIs(TypeSpecifier(type_specifier)).evaluate(collection, env)
    assert result[0].value == expected


def test_legacy_is_returns_empty_for_empty_collection():
    result = LegacyIs(TypeSpecifier("string")).evaluate([], env)
    assert result == []


def test_legacy_is_string_representation():
    expression = LegacyIs(TypeSpecifier("string"))
    assert str(expression) == "is(string)"


# -------------
# As
# -------------


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
@pytest.mark.parametrize("expected, type_specifier, equal", test_cases)
def test_as_returns_correct_boolean(expected, type_specifier, equal):
    collection = [FHIRPathCollectionItem(value=expected)]
    result = As(This(), TypeSpecifier(type_specifier)).evaluate(collection, env)
    assert result[0].value == expected if equal else result == []


def test_as_returns_empty_for_empty_collection():
    result = As(This(), TypeSpecifier("string")).evaluate([], env)
    assert result == []


def test_as_string_representation():
    expression = As(Element("field"), TypeSpecifier("string"))
    assert str(expression) == "field as string"


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
@pytest.mark.parametrize("expected, type_specifier, equal", test_cases)
def test_legacy_as_returns_correct_boolean(expected, type_specifier, equal):
    collection = [FHIRPathCollectionItem(value=expected)]
    result = LegacyAs(TypeSpecifier(type_specifier)).evaluate(collection, env)
    assert result[0].value == expected if equal else result == []


def test_legacy_as_returns_empty_for_empty_collection():
    result = LegacyAs(TypeSpecifier("string")).evaluate([], env)
    assert result == []


def test_legacy_as_string_representation():
    expression = LegacyAs(TypeSpecifier("string"))
    assert str(expression) == "as(string)"
