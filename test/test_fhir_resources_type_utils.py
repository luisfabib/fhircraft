"""
Test file demonstrating FHIR type checking and conversion utilities.
"""

import pytest
from pydantic import ValidationError

import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.resources.datatypes.R4.complex_types import Coding
from fhircraft.fhir.resources.definitions.element_definition import ElementDefinitionDiscriminator
from fhircraft.fhir.resources.datatypes.utils import (  # Type checking functions; Type conversion functions; Complex type utilities; Utility functions
    FHIRTypeError,
    get_primitive_type_by_name,
    get_primitive_type_name,
    is_boolean,
    is_date,
    is_datetime,
    is_decimal,
    is_fhir_primitive_type,
    is_fhir_complex_type,
    is_fhir_resource_type,
    is_integer,
    is_positive_int,
    is_string,
    is_time,
    is_unsigned_int,
    is_uri,
    list_primitive_types,
    to_boolean,
    to_date,
    to_datetime,
    to_decimal,
    to_integer,
    to_time,
)



@pytest.mark.parametrize("value, expected", (
    (True, True),
    (False, True),
    ("true", True),
    ("false", True),
    ("1", True),
    ("0", True),
    (123, False),
    (1, True),
    ("invalid", False),
))
def test_is_boolean(value, expected):
    assert is_boolean(value) == expected

@pytest.mark.parametrize("value,expected", [
    (123, True),
    ("123", True),
    ("-456", True),
    ("12.34", False),
    ("abc", False),
    (0, True),  # Edge case: zero value
    (-2147483648, True),  # Edge case: min 32-bit int
    (2147483647, True),   # Edge case: max 32-bit int
])
def test_is_integer(value, expected):
    assert is_integer(value) == expected

@pytest.mark.parametrize("value,expected", [
    (12.34, True),
    ("12.34", True),
    ("12", True),
    ("invalid", False),
])
def test_is_decimal(value, expected):
    assert is_decimal(value) == expected

@pytest.mark.parametrize("value,expected", [
    ("hello", True),
    ("", True),  # Edge case: empty string
    (123, False),
])
def test_is_string(value, expected):
    assert is_string(value) == expected

@pytest.mark.parametrize("value,expected", [
    ("2023-12-25", True),
    ("2023-12", True),
    ("2023", True),
    ("invalid-date", False),
])
def test_is_date_param(value, expected):
    assert is_date(value) == expected

@pytest.mark.parametrize("value,expected", [
    ("2023-12-25T10:30:00+02:00", True),
    ("2023-12-25T10:30:00Z", True),
    ("2023-12-25T10:30:00", True),
    ("2023-12-25T10:30", True),
    ("2023-12-25T10", True),
    ("2023-12-25", True),
    ("2023-12", True),
    ("2023", True),
    ("invalid-datetime", False),
])
def test_is_datetime(value, expected):
    assert is_datetime(value) == expected

@pytest.mark.parametrize("value,expected", [
    ("10:30:00", True),
    ("23:59:59", True),
    ("00:00:00", True),
    ("10:30", True),
    ("invalid-time", False),
])
def test_is_time(value, expected):
    assert is_time(value) == expected

@pytest.mark.parametrize("value,expected", [
    (123, True),
    ("123", True),
    (0, True),
    (-123, False),
    ("-123", False),
])
def test_is_unsigned_int(value, expected):
    assert is_unsigned_int(value) == expected

@pytest.mark.parametrize("value,expected", [
    (123, True),
    ("123", True),
    (0, False),
    (-123, False),
])
def test_is_positive_int(value, expected):
    assert is_positive_int(value) == expected


@pytest.mark.parametrize("value,expected", [
    ("true", True),
    ("false", False),
    ("1", True),
    ("0", False),
    ("invalid", None),
])
def test_to_boolean(value, expected):
    assert to_boolean(value) == expected

@pytest.mark.parametrize("value,expected", [
    ("123", 123),
    ("-456", -456),
    (789, 789),
    ("invalid", None),
])
def test_to_integer(value, expected):
    assert to_integer(value) == expected

@pytest.mark.parametrize("value,expected", [
    ("12.34", 12.34),
    ("56", 56.0),
    (78.9, 78.9),
    ("invalid", None),
])
def test_to_decimal(value, expected):
    assert to_decimal(value) == expected

@pytest.mark.parametrize("value,expected", [
    ("2023-12-25", "2023-12-25"),
    ("2023-12-25T10:30:00", "2023-12-25"),
    ("invalid", None),
])
def test_to_date(value, expected):
    assert to_date(value) == expected

@pytest.mark.parametrize("value,expected", [
    ("10:30:00", "10:30:00"),
    ("23:59:59", "23:59:59"),
    ("00:00:00", "00:00:00"),
    ("10:30", "10:30"),
    ("invalid", None),
])
def test_to_time(value, expected):
    assert to_time(value) == expected

@pytest.mark.parametrize("value,expected", [
    ("2023-12-25T10:30:00+02:00", "2023-12-25T10:30:00+02:00"),
    ("2023-12-25T10:30:00Z", "2023-12-25T10:30:00Z"),
    ("2023-12-25T10:30:00", "2023-12-25T10:30:00"),
    ("2023-12-25T10:30", "2023-12-25T10:30"),
    ("2023-12-25T10", "2023-12-25T10"),
    ("2023-12-25", "2023-12-25"),
    ("2023-12", "2023-12"),
    ("2023", "2023"),
    ("invalid-datetime", None),
])
def test_to_datetime(value, expected):
    assert to_datetime(value) == expected


def test_utility_functions():
    """Test utility functions for working with types."""

    # Test getting type names
    assert get_primitive_type_name(primitives.Boolean) == "Boolean"
    assert get_primitive_type_name(primitives.Integer) == "Integer"

    # Test getting types by name
    boolean_type = get_primitive_type_by_name("Boolean")
    assert boolean_type == primitives.Boolean

    invalid_type = get_primitive_type_by_name("InvalidType")
    assert invalid_type is None

    # Test listing all types
    type_names = list_primitive_types()
    assert "Boolean" in type_names
    assert "Integer" in type_names
    assert "String" in type_names
    assert len(type_names) > 15  # Should have many primitive types


@pytest.mark.parametrize("value,fhir_type,expected", [
    ("true", "Boolean", True),
    ("123", "Integer", True),
    ("invalid", "Boolean", False),
    ("2023-12-25", "Date", True),
    ("not-a-date", "Date", False),
])
def test_is_fhir_primitive_type(value, fhir_type, expected):
    assert is_fhir_primitive_type(value, fhir_type) == expected

@pytest.mark.parametrize("value,fhir_type,expected", [
    (Coding(code='123', system='example.com'), Coding, True),
    ("not-coding", Coding, False),
])
def test_is_fhir_complex_type(value, fhir_type, expected):
    assert is_fhir_complex_type(value, fhir_type) == expected

@pytest.mark.parametrize("value,fhir_type,expected", [
    (ElementDefinitionDiscriminator(type='value', path='example'), ElementDefinitionDiscriminator, True),
    ("not-elementdefinition", ElementDefinitionDiscriminator, False),
])
def test_is_fhir_resource_type(value, fhir_type, expected):
    assert is_fhir_resource_type(value, fhir_type) == expected
