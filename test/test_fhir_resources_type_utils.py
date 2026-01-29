"""
Test file demonstrating FHIR type checking and conversion utilities.
"""

import pytest
from pydantic import ValidationError

import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.resources.datatypes.R4.complex import Coding
from fhircraft.fhir.resources.datatypes.R4.complex.element_definition import (
    ElementDefinitionSlicingDiscriminator,
)
from fhircraft.fhir.resources.datatypes.utils import ( 
    get_primitive_type_by_name,
    get_primitive_type_name,
    is_boolean,
    is_date,
    is_datetime,
    is_decimal,
    is_fhir_primitive,
    is_fhir_primitive_type,
    is_fhir_complex_type,
    is_fhir_resource_type,
    is_integer,
    is_integer64,
    is_positive_int,
    is_string,
    is_time,
    is_code,
    is_unsigned_int,
    is_uri,
    is_url,
    is_canonical,
    is_base64binary,
    is_oid,
    is_uuid,
    is_id,
    is_markdown,
    list_primitive_types,
    to_boolean,
    to_date,
    to_datetime,
    to_decimal,
    to_integer,
    to_time,
)


@pytest.mark.parametrize(
    "value, expected",
    (
        (True, True),
        (False, True),
        ("True", True),
        ("False", True),
        ("true", True),
        ("false", True),
        ("1", True),
        ("0", True),
        ("Atrue", False),
        ("Afalse", False),
        ("trueB", False),
        ("falseB", False),
        (123, False),
        (1, True),
        ("invalid", False),
    ),
)
def test_is_boolean(value, expected):
    assert is_boolean(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (123, True),
        ("123", True),
        ("-456", True),
        ("12.34", False),
        ("abc", False),
        ("A123", False),
        ("123B", False),
        ("urn:ietf:rfc:3986", False),
        (0, True), 
        ("0", True),
        (-2147483648, True),  
        ("-2147483648", True),
        (2147483647, True), 
        ("2147483647", True),
        (-2147483649, False),
        ("-2147483649", False),  
        (2147483648, False), 
        ("2147483648", False),
    ],
)
def test_is_integer(value, expected):
    assert is_integer(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (123, True),
        ("123", True),
        ("-456", True),
        ("12.34", False),
        ("abc", False),
        ("A123", False),
        ("123B", False),
        ("urn:ietf:rfc:3986", False),
        (0, True), 
        ("0", True),
        (-9223372036854775808, True),  
        ("-9223372036854775808", True),
        (9223372036854775807, True), 
        ("9223372036854775807", True),
        (-9223372036854775809, False),
        ("-9223372036854775809", False),  
        (9223372036854775808, False), 
        ("9223372036854775808", False),
    ],
)
def test_is_integer64(value, expected):
    assert is_integer64(value) == expected

@pytest.mark.parametrize(
    "value,expected",
    [
        (12.34, True),
        ("12.34", True),
        ("12", True),
        ("invalid", False),
        ("A123.12", False),
        ("123.12B", False),
    ],
)
def test_is_decimal(value, expected):
    assert is_decimal(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("hello", True),
        ("", True),  # Edge case: empty string
        (123, False),
    ],
)
def test_is_string(value, expected):
    assert is_string(value) == expected




@pytest.mark.parametrize(
    "value,expected",
    [
        ("http://helloworld.com/", True),
        ("foo+://example.com:8042/over/there?name=ferret#nose", True),
        ("foo+://andrewj:myPassword:mySecondPassword@example.com:8042/over/there?name=ferret#nose", True),
        ("urn:example:animal:ferret:nose", True),
        ("http://10.15.20.73/", True),
        ("http://user.@com/", True),
        ("mailto:John.Doe@example.com", True),
        ("news:comp.infosystems.www.servers.unix", True),
        ("tel:+1-816-555-1212", True),
        ("telnet://192.0.2.16:80/", True),
        ("urn:oasis:names:specification:docbook:dtd:xml:4.1.2", True),
        ("urn:uuid:53fefa32-fcbb-4ff8-8a92-55ee120877b7", True),
        (123, False),
        (True, False),
    ],
)
def test_is_uri(value, expected):
    assert is_uri(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("http://helloworld.com/", True),
        ("http://222.helloworld.com/", True),
        ("http://www.helloworld.com/", True),
        ("foo+://example.com:8042/over/there?name=ferret#nose", True),
        ("foo+://andrewj:myPassword:mySecondPassword@example.com:8042/over/there?name=ferret#nose", True),
        ("urn:example:animal:ferret:nose", True),
        ("http://10.15.20.73/", True),
        ("http://user.@com/", True),
        ("mailto:John.Doe@example.com", True),
        ("news:comp.infosystems.www.servers.unix", True),
        ("tel:+1-816-555-1212", True),
        ("telnet://192.0.2.16:80/", True),
        ("urn:oasis:names:specification:docbook:dtd:xml:4.1.2", True),
        ("urn:uuid:53fefa32-fcbb-4ff8-8a92-55ee120877b7", True),
        (123, False),
        (True, False),
    ],
)
def test_is_url(value, expected):
    assert is_url(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Zg==", True),
        ("Zm8=", True),
        ("Zm9v", True),
        ("Zm9vYg==", True),
        ("Zm9vYmE=", True),
        ("Zm9vYmFy", True),
        ("SGVsbG8gV29ybGQh", True),
        ("YW55IGNhcm5hbCBwbGVhcw==", True),
        ("TWFu", True),
        ("U29tZSByYW5kb20gYnl0ZXM=", True),
        ("AAECAwQFBgcICQ==", True),
        ("////", True),
        ("QUJDREVGR0hJSg==", True),
        ("Zg=", False),
        ("Z===", False),
        ("Zm=9v", False),
        ("Zm9v===", False),
        ("Zm9v=", False),
        ("SGVsbG8gV29ybGQh==", False),
        ("SGVsbG8gV29ybGQh=", False),
        ("Zm9v*", False),
        ("Zm9v-", False),
        ("Zm9v_", False),
        ("Zm9v$", False),
        ("Zm 9v", False),
        ("Zm9v\t", False),
        ("Z", False),
        ("Zm9", False),
        ("====", False),
        ("==Zm9v==", False),
        (123, False),
        (True, False),
    ],
)
def test_is_base64binary(value, expected):
    assert is_base64binary(value) == expected



@pytest.mark.parametrize(
    "value,expected",
    [
        ("http://helloworld.com/", True),
        ("http://helloworld.com|1.2.3", True),
        ("foo+://example.com:8042/over/there?name=ferret#nose", True),
        ("urn:example:animal:ferret:nose", True),
        ("urn:example:animal:ferret:nose|1.2.3", True),
        ("http://10.15.20.73/", True),
        ("http://10.15.20.73|1.2.3", True),
        ("http://user.@com/", True),
        ("http://user.@com|1.2.3", True),
        (123, False),
        (True, False),
    ],
)
def test_is_canonical(value, expected):
    assert is_canonical(value) == expected

@pytest.mark.parametrize(
    "value,expected",
    [
        ("2023-12-25", True),
        ("2023-12", True),
        ("2023", True),
        ("true", False),
        ("urn:ietf:rfc:3986", False),
        ("invalid-date", False),
    ],
)
def test_is_date_param(value, expected):
    assert is_date(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("2023-12-25T10:30:00+02:00", True),
        ("2023-12-25T10:30:00Z", True),
        ("2023-12-25T10:30:00", True),
        ("2023-12-25T10:30", True),
        ("2023-12-25T10", True),
        ("2023-12-25", True),
        ("2023-12", True),
        ("2023", True),
        ("urn:ietf:rfc:3986", False),
        ("invalid-datetime", False),
    ],
)
def test_is_datetime(value, expected):
    assert is_datetime(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("10:30:00", True),
        ("23:59:59", True),
        ("00:00:00", True),
        ("10:30", True),
        ("urn:ietf:rfc:3986", False),
        ("invalid-time", False),
    ],
)
def test_is_time(value, expected):
    assert is_time(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (123, True),
        ("123", True),
        (0, True),
        ("0", True),
        (-1, False),
        ("-1", False),
        (4294967295, True),
        ("4294967295", True),
        (4294967296, False),
        ("4294967296", False),
    ],
)
def test_is_unsigned_int(value, expected):
    assert is_unsigned_int(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (123, True),
        ("123", True),
        (0, False),
        ("0", False),
        (-123, False),
        ("-123", False),
        (2147483647, True),
        ("2147483647", True),
        (2147483648, False),
        ("2147483648", False),
    ],
)
def test_is_positive_int(value, expected):
    assert is_positive_int(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("ABC", True),
        ("ABC DEF", True),
        ("ABC DEF GHI", True),
        ("123", True),
        ("123 456", True),
        ("123 456 789", True),
        ("ABC ", False),
        (" ABC", False),
        (" ABC ", False),
        ("ABC  DEF", False),
        ("ABC   DEF", False),
        (" ABC DEF", False),
        ("ABC DEF ", False),
        (123, False),
        (True, False),
    ],
)
def test_is_code(value, expected):
    assert is_code(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("urn:oid:1.2.3.4.5", True),
        ("urn:oid:1.2.3.4.5.6", True),
        ("urn:oid:1.2.3.4.5urn:oid:1.2.3.4.5", False),
        ("urn:ntfl:1.2.3.4.5", False),
        ("urn:oid:12.12.32.32", False),
        (123, False),
        ('ABC', False),
    ],
)
def test_is_oid(value, expected):
    assert is_oid(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("urn:uuid:c757873d-ec9a-4326-a141-556f43239520", True),
        ("urn:uuid:53fefa32-fcbb-4ff8-8a92-55ee120877b7", True),
        ("urn:uuid:", False),
        ("urn:uuid:123e4567e89b12d3a456426614174000", False),
        ("urn:uuid:123e4567-e89b-12d3-a456-42661417400", False),
        ("urn:uuid:123e4567-e89b-12d3-a456-42661417400000", False),
        ("urn:uuid:123e4567-e89b-12d3-a4567-426614174000", False),
        ("urn:uuid:123e4567-e89b-12d3-a456-42661417400g", False),
        ("urn:uuid:gggggggg-gggg-gggg-gggg-gggggggggggg", False),
        ("urn:uuid:123e4567-e89b-12d3-a456-426614174000-extra", False),
        ("urn:uuid:123e4567-e89b-12d3-a456", False),
        ("urn:uuid:123e4567--e89b-12d3-a456-426614174000", False),
        ("urn:uuid:123e4567-e89b-12d3-a456426614174000", False),
        ("uuid:123e4567-e89b-12d3-a456-426614174000", False),
        ("urn:guid:123e4567-e89b-12d3-a456-426614174000", False),
        (123, False),
        ('ABC', False),
    ],
)
def test_is_uuid(value, expected):
    assert is_uuid(value) == expected

@pytest.mark.parametrize(
    "value,expected",
    [
        ("12345", True),
        ("ABC12345", True),
        ("ABC-123-45", True),
        ("ABC.123.45", True),
        ("ABC:123:45", False),
        ("12345"*60, False),
        (123, False),
        (0, False),
        (-123, False),
    ],
)
def test_is_id(value, expected):
    assert is_id(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("12345", True),
        ("ABC12345", True),
        ("ABC-123-45", True),
        ("ABC.123.45", True),
        ("ABC:123:45", True),
        ("12345"*60, True),
        (123, False),
        (0, False),
        (-123, False),
    ],
)
def test_is_markdown(value, expected):
    assert is_markdown(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("true", True),
        ("false", False),
        ("1", True),
        ("0", False),
        ("invalid", None),
    ],
)
def test_to_boolean(value, expected):
    assert to_boolean(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("123", 123),
        ("-456", -456),
        (789, 789),
        ("invalid", None),
    ],
)
def test_to_integer(value, expected):
    assert to_integer(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("12.34", 12.34),
        ("56", 56.0),
        (78.9, 78.9),
        ("invalid", None),
    ],
)
def test_to_decimal(value, expected):
    assert to_decimal(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("2023-12-25", "2023-12-25"),
        ("2023-12-25T10:30:00", "2023-12-25"),
        ("invalid", None),
    ],
)
def test_to_date(value, expected):
    assert to_date(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("10:30:00", "10:30:00"),
        ("23:59:59", "23:59:59"),
        ("00:00:00", "00:00:00"),
        ("10:30", "10:30"),
        ("invalid", None),
    ],
)
def test_to_time(value, expected):
    assert to_time(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("2023-12-25T10:30:00+02:00", "2023-12-25T10:30:00+02:00"),
        ("2023-12-25T10:30:00Z", "2023-12-25T10:30:00Z"),
        ("2023-12-25T10:30:00", "2023-12-25T10:30:00"),
        ("2023-12-25T10:30", "2023-12-25T10:30"),
        ("2023-12-25T10", "2023-12-25T10"),
        ("2023-12-25", "2023-12-25"),
        ("2023-12", "2023-12"),
        ("2023", "2023"),
        ("invalid-datetime", None),
    ],
)
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


@pytest.mark.parametrize(
    "value,fhir_type,expected",
    [
        ("true", "Boolean", True),
        ("123", "Integer", True),
        ("invalid", "Boolean", False),
        ("2023-12-25", "Date", True),
        ("not-a-date", "Date", False),
    ],
)
def test_is_fhir_primitive_type(value, fhir_type, expected):
    assert is_fhir_primitive_type(value, fhir_type) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("true", True),
        (123, True),
        ("2023-12-25", True),
        ("http://example.com", True),  # URI
        ("10:30:00", True),  # Time
        ("12.34", True),  # Decimal
        (Coding(code="123", system="http://example.com"), False),
    ],
)
def test_is_fhir_primitive(value, expected):
    assert is_fhir_primitive(value) == expected


@pytest.mark.parametrize(
    "value,fhir_type,expected",
    [
        (Coding(code="123", system="http://example.com"), Coding, True),
        ("not-coding", Coding, False),
    ],
)
def test_is_fhir_complex_type(value, fhir_type, expected):
    assert is_fhir_complex_type(value, fhir_type) == expected


@pytest.mark.parametrize(
    "value,fhir_type,expected",
    [
        (
            ElementDefinitionSlicingDiscriminator(type="value", path="example"),
            ElementDefinitionSlicingDiscriminator,
            True,
        ),
        ("not-elementdefinition", ElementDefinitionSlicingDiscriminator, False),
    ],
)
def test_is_fhir_resource_type(value, fhir_type, expected):
    assert is_fhir_resource_type(value, fhir_type) == expected
