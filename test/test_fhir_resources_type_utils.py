"""
Test file demonstrating FHIR type checking and conversion utilities.
"""

import pytest
from pydantic import ValidationError

import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.resources.datatypes.utils import (  # Type checking functions; Type conversion functions; Complex type utilities; Utility functions
    FHIRTypeError,
    get_primitive_type_by_name,
    get_primitive_type_name,
    is_boolean,
    is_date,
    is_datetime,
    is_decimal,
    is_fhir_type,
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
    validate_fhir_type,
)


def test_type_checking_functions():
    """Test the is_* type checking functions."""

    # Boolean type checking
    assert is_boolean(True) == True
    assert is_boolean("true") == True
    assert is_boolean("false") == True
    assert is_boolean("invalid") == False
    assert is_boolean(123) == False

    # Integer type checking
    assert is_integer(123) == True
    assert is_integer("123") == True
    assert is_integer("-456") == True
    assert is_integer("12.34") == False
    assert is_integer("abc") == False

    # Decimal type checking
    assert is_decimal(12.34) == True
    assert is_decimal("12.34") == True
    assert is_decimal("12") == True
    assert is_decimal("invalid") == False

    # String type checking
    assert is_string("hello") == True
    assert is_string("") == True
    assert is_string(123) == False

    # Date type checking
    assert is_date("2023-12-25") == True
    assert is_date("2023-12") == True
    assert is_date("2023") == True
    assert is_date("invalid-date") == False

    # Datetime type checking
    assert is_datetime("2023-12-25T10:30:00+02:00") == True
    assert is_datetime("2023-12-25T10:30:00Z") == True
    assert is_datetime("2023-12-25T10:30:00") == True
    assert is_datetime("2023-12-25T10:30") == True
    assert is_datetime("2023-12-25T10") == True
    assert is_datetime("2023-12-25") == True
    assert is_datetime("2023-12") == True
    assert is_datetime("2023") == True
    assert is_datetime("invalid-datetime") == False

    # Time type checking
    assert is_time("10:30:00") == True
    assert is_time("23:59:59") == True
    assert is_time("00:00:00") == True
    assert is_time("10:30") == True
    assert is_time("invalid-time") == False

    # UnsignedInt type checking
    assert is_unsigned_int(123) == True
    assert is_unsigned_int("123") == True
    assert is_unsigned_int(0) == True
    assert is_unsigned_int(-123) == False
    assert is_unsigned_int("-123") == False

    # PositiveInt type checking
    assert is_positive_int(123) == True
    assert is_positive_int("123") == True
    assert is_positive_int(0) == False
    assert is_positive_int(-123) == False


def test_generic_type_checking():
    """Test the generic is_fhir_type function."""

    # Using TypeAliasType
    assert is_fhir_type("true", primitives.Boolean) == True
    assert is_fhir_type("123", primitives.Integer) == True
    assert is_fhir_type("invalid", primitives.Boolean) == False

    # Using string type names
    assert is_fhir_type("true", "Boolean") == True
    assert is_fhir_type("123", "Integer") == True
    assert is_fhir_type("invalid", "Boolean") == False

    # Invalid type name
    with pytest.raises(ValueError):
        is_fhir_type("value", "InvalidType")


def test_type_conversion_functions():
    """Test the to_* type conversion functions."""

    # Boolean conversion
    assert to_boolean("true") == True
    assert to_boolean("false") == False
    assert to_boolean("1") == True
    assert to_boolean("0") == False
    assert to_boolean("invalid") == None

    # Integer conversion
    assert to_integer("123") == 123
    assert to_integer("-456") == -456
    assert to_integer(789) == 789
    assert to_integer("invalid") == None

    # Decimal conversion
    assert to_decimal("12.34") == 12.34
    assert to_decimal("56") == 56.0
    assert to_decimal(78.9) == 78.9
    assert to_decimal("invalid") == None

    # Date conversion
    assert to_date("2023-12-25") == "2023-12-25"
    assert to_date("2023-12-25T10:30:00") == "2023-12-25"
    assert to_date("invalid") == None


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


def test_detailed_validation():
    """Test detailed validation with error handling."""

    # Valid case
    result = validate_fhir_type("true", primitives.Boolean, raise_on_error=False)
    assert result == True

    # Invalid case - should return False when raise_on_error=False
    result = validate_fhir_type("invalid", primitives.Boolean, raise_on_error=False)
    assert result == False

    # Invalid case - should raise when raise_on_error=True
    with pytest.raises((ValidationError, FHIRTypeError)):
        validate_fhir_type("invalid", primitives.Boolean, raise_on_error=True)

    # Unknown type name
    with pytest.raises((FHIRTypeError, AttributeError)):
        validate_fhir_type("value", "UnknownType", raise_on_error=True)


def test_edge_cases():
    """Test edge cases and boundary conditions."""

    # Empty strings
    assert is_string("") == True
    assert is_uri("") == True  # Empty URI is valid in FHIR

    # Zero values
    assert is_integer(0) == True
    assert is_unsigned_int(0) == True
    assert is_positive_int(0) == False  # Zero is not positive

    # Boundary values for integers
    assert is_integer(-2147483648) == True  # Min 32-bit int
    assert is_integer(2147483647) == True  # Max 32-bit int

    # Partial dates
    assert is_date("2023") == True
    assert is_date("2023-12") == True
    assert is_date("2023-12-25") == True
