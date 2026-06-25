from pydantic import BaseModel, TypeAdapter, create_model, Field
from fhircraft.fhir.resources.base import FHIRBaseModel
import fhircraft.fhir.resources.datatypes.R4.primitive as R4_primitives
import fhircraft.fhir.resources.datatypes.R4B.primitive as R4B_primitives
import fhircraft.fhir.resources.datatypes.R5.primitive as R5_primitives

from datetime import date, time, datetime
import pytest

modules = {
    "R4": R4_primitives,
    "R4B": R4B_primitives,
    "R5": R5_primitives,
}

FHIR_RELEASES = [
    "release",
    ["R4", "R4B", "R5"],
]

# ==========================================
# String
# ==========================================

STRING_TEST_CASES = [
    "value, expected",
    [
        ("test", "test"),
        ("Test", "Test"),
        ("Test with spaces", "Test with spaces"),
        (
            "Test with characters !@#$%^&*()_+-=[]{}|;':,.<>/?`~",
            "Test with characters !@#$%^&*()_+-=[]{}|;':,.<>/?`~",
        ),
    ],
]


@pytest.mark.parametrize(*STRING_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__string_deserialization(release, value, expected):
    instance = modules[release].String(value)
    assert instance == expected


@pytest.mark.parametrize(*STRING_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__string_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].string)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].String(value))
    assert instance == expected


@pytest.mark.parametrize(*STRING_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__string_serialization(release, value, expected):
    instance = modules[release].String(value)
    assert instance.model_dump() == expected


# ==========================================
# Id
# ==========================================

ID_TEST_CASES = [
    "value, expected",
    [
        ("ID.A.B.3.4.5", "ID.A.B.3.4.5"),
        ("Test-Id", "Test-Id"),
    ],
]


@pytest.mark.parametrize(*ID_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__id_deserialization(release, value, expected):
    instance = modules[release].Id(value)
    assert instance == expected


# @pytest.mark.parametrize(*ID_TEST_CASES)
# @pytest.mark.parametrize(*FHIR_RELEASES)
# def test_primitives__id_type_alias(release, value, expected):
#     adapter = TypeAdapter(modules[release].id)
#     # Native string deserialization
#     instance = adapter.validate_python(value)
#     assert instance == expected
#     # Class deserialization
#     instance = adapter.validate_python(modules[release].Id(value))
#     assert instance == expected
#     # Parent class deserialization
#     instance = adapter.validate_python(modules[release].String(value))
#     assert instance == expected


@pytest.mark.parametrize(*ID_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__id_serialization(release, value, expected):
    instance = modules[release].Id(value)
    assert instance.model_dump() == expected


# ==========================================
# Boolean
# ==========================================

BOOLEAN_TEST_CASES = [
    "value, expected",
    [
        (True, True),
        (False, False),
        ("true", True),
        ("false", False),
    ],
]


@pytest.mark.parametrize(*BOOLEAN_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__boolean_deserialization(release, value, expected):
    instance = modules[release].Boolean(value)
    assert instance == expected


@pytest.mark.parametrize(*BOOLEAN_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__boolean_serialization(release, value, expected):
    instance = modules[release].Boolean(value)
    assert instance.model_dump() == expected


# ==========================================
# Integer
# ==========================================

INTEGER_TEST_CASES = [
    "value, expected",
    [
        (1234, 1234),
        ("1234", 1234),
        (-1, -1),
        (0, 0),
    ],
]


@pytest.mark.parametrize(*INTEGER_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__integer_deserialization(release, value, expected):
    instance = modules[release].Integer(value)
    assert instance == expected


@pytest.mark.parametrize(*INTEGER_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__integer_serialization(release, value, expected):
    instance = modules[release].Integer(value)
    assert instance.model_dump() == expected


# ==========================================
# Integer64 (R5 only)
# ==========================================

INTEGER64_TEST_CASES = [
    "value, expected",
    [
        (9223372036854775807, 9223372036854775807),
        ("9223372036854775807", 9223372036854775807),
        (-9223372036854775808, -9223372036854775808),
        (0, 0),
    ],
]


@pytest.mark.parametrize(*INTEGER64_TEST_CASES)
def test_primitives__integer64_deserialization(value, expected):
    instance = modules["R5"].Integer64(value)
    assert instance == expected


@pytest.mark.parametrize(*INTEGER64_TEST_CASES)
def test_primitives__integer64_serialization(value, expected):
    instance = modules["R5"].Integer64(value)
    assert instance.model_dump() == expected


# ==========================================
# Decimal
# ==========================================

DECIMAL_TEST_CASES = [
    "value, expected",
    [
        (12, 12),
        (12.0, 12.0),
        (12.52, 12.52),
        ("12.52", 12.52),
        ("12", 12.0),
    ],
]


@pytest.mark.parametrize(*DECIMAL_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__decimal_deserialization(release, value, expected):
    instance = modules[release].Decimal(value)
    assert instance == expected


@pytest.mark.parametrize(*DECIMAL_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__decimal_serialization(release, value, expected):
    instance = modules[release].Decimal(value)
    assert instance.model_dump() == expected


# ==========================================
# Uri
# ==========================================

URI_TEST_CASES = [
    "value, expected",
    [
        ("http://example.org", "http://example.org"),
        (
            "foo://example.com:8042/over/there?name=ferret#nose",
            "foo://example.com:8042/over/there?name=ferret#nose",
        ),
        ("urn:isbn:0451450523", "urn:isbn:0451450523"),
    ],
]


@pytest.mark.parametrize(*URI_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__uri_deserialization(release, value, expected):
    instance = modules[release].Uri(value)
    assert instance == expected


@pytest.mark.parametrize(*URI_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__id_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].uri)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Uri(value))
    assert instance == expected
    # Parent class deserialization
    instance = adapter.validate_python(modules[release].String(value))
    assert instance == expected


@pytest.mark.parametrize(*URI_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__uri_serialization(release, value, expected):
    instance = modules[release].Uri(value)
    assert instance.model_dump() == expected


# ==========================================
# Url
# ==========================================

URL_TEST_CASES = [
    "value, expected",
    [
        ("http://www.example.com/index.html", "http://www.example.com/index.html"),
        ("https://example.com/path?q=1", "https://example.com/path?q=1"),
    ],
]


@pytest.mark.parametrize(*URL_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__url_deserialization(release, value, expected):
    instance = modules[release].Url(value)
    assert instance == expected


@pytest.mark.parametrize(*URL_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__url_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].url)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Url(value))
    assert instance == expected
    # Parent class deserialization
    instance = adapter.validate_python(modules[release].String(value))
    assert instance == expected


@pytest.mark.parametrize(*URL_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__url_serialization(release, value, expected):
    instance = modules[release].Url(value)
    assert instance.model_dump() == expected


# ==========================================
# Canonical
# ==========================================

CANONICAL_TEST_CASES = [
    "value, expected",
    [
        (
            "http://hl7.org/fhir/StructureDefinition/Patient",
            "http://hl7.org/fhir/StructureDefinition/Patient",
        ),
        ("example.com/resources/1234", "example.com/resources/1234"),
    ],
]


@pytest.mark.parametrize(*CANONICAL_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__canonical_deserialization(release, value, expected):
    instance = modules[release].Canonical(value)
    assert instance == expected


@pytest.mark.parametrize(*CANONICAL_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__canonical_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].canonical)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Canonical(value))
    assert instance == expected
    # Parent class deserialization
    instance = adapter.validate_python(modules[release].String(value))
    assert instance == expected


@pytest.mark.parametrize(*CANONICAL_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__canonical_serialization(release, value, expected):
    instance = modules[release].Canonical(value)
    assert instance.model_dump() == expected


# ==========================================
# Code
# ==========================================

CODE_TEST_CASES = [
    "value, expected",
    [
        ("active", "active"),
        ("code1234", "code1234"),
        ("two words", "two words"),
    ],
]


@pytest.mark.parametrize(*CODE_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__code_deserialization(release, value, expected):
    instance = modules[release].Code(value)
    assert instance == expected


@pytest.mark.parametrize(*CODE_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__code_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].code)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Code(value))
    assert instance == expected
    # Parent class deserialization
    instance = adapter.validate_python(modules[release].String(value))
    assert instance == expected


@pytest.mark.parametrize(*CODE_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__code_serialization(release, value, expected):
    instance = modules[release].Code(value)
    assert instance.model_dump() == expected


# ==========================================
# Markdown
# ==========================================

MARKDOWN_TEST_CASES = [
    "value, expected",
    [
        ("test string text", "test string text"),
        ("# Heading\n\nParagraph", "# Heading\n\nParagraph"),
    ],
]


@pytest.mark.parametrize(*MARKDOWN_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__markdown_deserialization(release, value, expected):
    instance = modules[release].Markdown(value)
    assert instance == expected


@pytest.mark.parametrize(*MARKDOWN_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__markdown_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].markdown)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Markdown(value))
    assert instance == expected
    # Parent class deserialization
    instance = adapter.validate_python(modules[release].String(value))
    assert instance == expected


@pytest.mark.parametrize(*MARKDOWN_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__markdown_serialization(release, value, expected):
    instance = modules[release].Markdown(value)
    assert instance.model_dump() == expected


# ==========================================
# Oid
# ==========================================

OID_TEST_CASES = [
    "value, expected",
    [
        ("urn:oid:1.2.3.4.5", "urn:oid:1.2.3.4.5"),
        ("urn:oid:2.16.840.1.113883.6.96", "urn:oid:2.16.840.1.113883.6.96"),
    ],
]


@pytest.mark.parametrize(*OID_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__oid_deserialization(release, value, expected):
    instance = modules[release].Oid(value)
    assert instance == expected


@pytest.mark.parametrize(*OID_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__oid_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].oid)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Oid(value))
    assert instance == expected
    # Parent class deserialization
    instance = adapter.validate_python(modules[release].String(value))
    assert instance == expected


@pytest.mark.parametrize(*OID_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__oid_serialization(release, value, expected):
    instance = modules[release].Oid(value)
    assert instance.model_dump() == expected


# ==========================================
# Uuid
# ==========================================

UUID_TEST_CASES = [
    "value, expected",
    [
        (
            "urn:uuid:c757873d-ec9a-4326-a141-556f43239520",
            "urn:uuid:c757873d-ec9a-4326-a141-556f43239520",
        ),
    ],
]


@pytest.mark.parametrize(*UUID_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__uuid_deserialization(release, value, expected):
    instance = modules[release].Uuid(value)
    assert instance == expected


@pytest.mark.parametrize(*UUID_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__uuid_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].uuid)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Uuid(value))
    assert instance == expected
    # Parent class deserialization
    instance = adapter.validate_python(modules[release].String(value))
    assert instance == expected


@pytest.mark.parametrize(*UUID_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__uuid_serialization(release, value, expected):
    instance = modules[release].Uuid(value)
    assert instance.model_dump() == expected


# ==========================================
# Base64Binary
# ==========================================

BASE64BINARY_TEST_CASES = [
    "value, expected",
    [
        ("aGVsbG8gd29yaw==", "aGVsbG8gd29yaw=="),
        ("dGVzdA==", "dGVzdA=="),
    ],
]


@pytest.mark.parametrize(*BASE64BINARY_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__base64binary_deserialization(release, value, expected):
    instance = modules[release].Base64Binary(value)
    assert instance == expected


@pytest.mark.parametrize(*BASE64BINARY_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__base64binary_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].base64Binary)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Base64Binary(value))
    assert instance == expected
    # Parent class deserialization
    instance = adapter.validate_python(modules[release].String(value))
    assert instance == expected


@pytest.mark.parametrize(*BASE64BINARY_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__base64binary_serialization(release, value, expected):
    instance = modules[release].Base64Binary(value)
    assert instance.model_dump() == expected


# ==========================================
# Instant
# ==========================================

INSTANT_TEST_CASES = [
    "value, expected",
    [
        ("2015-02-07T13:28:17.239", "2015-02-07T13:28:17.239"),
        (datetime(2015, 2, 7), "2015-02-07T00:00:00"),
        (datetime(2015, 2, 7, 13, 28, 17), "2015-02-07T13:28:17"),
    ],
]


@pytest.mark.parametrize(*INSTANT_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__instant_deserialization(release, value, expected):
    instance = modules[release].Instant(value)
    assert instance == expected


@pytest.mark.parametrize(*INSTANT_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__instant_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].instant)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Instant(value))
    assert instance == expected
    # Parent class deserialization
    if isinstance(value, str):
        instance = adapter.validate_python(modules[release].String(value))
    else:
        instance = adapter.validate_python(modules[release].DateTime(value))
    assert instance == expected


@pytest.mark.parametrize(*INSTANT_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__instant_serialization(release, value, expected):
    instance = modules[release].Instant(value)
    assert instance.model_dump() == expected


# ==========================================
# Date
# ==========================================

DATE_TEST_CASES = [
    "value, expected",
    [
        ("2015-02-07", "2015-02-07"),
        ("2015-02", "2015-02"),
        ("2015", "2015"),
        (date(2015, 2, 7), "2015-02-07"),
    ],
]


@pytest.mark.parametrize(*DATE_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__date_deserialization(release, value, expected):
    instance = modules[release].Date(value)
    assert instance == expected


@pytest.mark.parametrize(*DATE_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__date_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].date_)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Date(value))
    assert instance == expected
    # Parent class deserialization
    if isinstance(value, str):
        instance = adapter.validate_python(modules[release].String(value))
    else:
        instance = adapter.validate_python(modules[release].Date(value))
    assert instance == expected


@pytest.mark.parametrize(*DATE_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__date_serialization(release, value, expected):
    instance = modules[release].Date(value)
    assert instance.model_dump() == expected


# ==========================================
# DateTime
# ==========================================

DATETIME_TEST_CASES = [
    "value, expected",
    [
        ("2015-02-07T13:28:17.239", "2015-02-07T13:28:17.239"),
        ("2023-03-26T15:21:02.749+11:00", "2023-03-26T15:21:02.749+11:00"),
        ("2015-02-07", "2015-02-07"),
        ("2015-02", "2015-02"),
        ("2015", "2015"),
        (datetime(2015, 2, 7), "2015-02-07T00:00:00"),
        (datetime(2015, 2, 7, 13, 28, 17), "2015-02-07T13:28:17"),
    ],
]


@pytest.mark.parametrize(*DATETIME_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__datetime_deserialization(release, value, expected):
    instance = modules[release].DateTime(value)
    assert instance == expected


@pytest.mark.parametrize(*DATETIME_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__datetime_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].dateTime)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].DateTime(value))
    assert instance == expected
    # Parent class deserialization
    if isinstance(value, str):
        instance = adapter.validate_python(modules[release].String(value))
    else:
        instance = adapter.validate_python(modules[release].DateTime(value))
    assert instance == expected


@pytest.mark.parametrize(*DATETIME_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__datetime_serialization(release, value, expected):
    instance = modules[release].DateTime(value)
    assert instance.model_dump() == expected


# ==========================================
# Time
# ==========================================

TIME_TEST_CASES = [
    "value, expected",
    [
        ("12:54", "12:54"),
        ("12:54:32", "12:54:32"),
        (time(12, 54), "12:54:00"),
        (time(12, 54, 32), "12:54:32"),
    ],
]


@pytest.mark.parametrize(*TIME_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__time_deserialization(release, value, expected):
    instance = modules[release].Time(value)
    assert instance == expected


@pytest.mark.parametrize(*TIME_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__time_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].time_)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Time(value))
    assert instance == expected
    # Parent class deserialization
    if isinstance(value, str):
        instance = adapter.validate_python(modules[release].String(value))
    else:
        instance = adapter.validate_python(modules[release].Time(value))
    assert instance == expected


@pytest.mark.parametrize(*TIME_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__time_serialization(release, value, expected):
    instance = modules[release].Time(value)
    assert instance.model_dump() == expected


# ==========================================
# UnsignedInt
# ==========================================

UNSIGNED_INT_TEST_CASES = [
    "value, expected",
    [
        (12345, 12345),
        ("12345", 12345),
        (0, 0),
    ],
]


@pytest.mark.parametrize(*UNSIGNED_INT_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__unsignedint_deserialization(release, value, expected):
    instance = modules[release].UnsignedInt(value)
    assert instance == expected


@pytest.mark.parametrize(*UNSIGNED_INT_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__unsignedint_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].unsignedInt)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].UnsignedInt(value))
    assert instance == expected
    # Parent class deserialization
    if isinstance(value, str):
        instance = adapter.validate_python(modules[release].String(value))
    else:
        instance = adapter.validate_python(modules[release].Integer(value))
    assert instance == expected


@pytest.mark.parametrize(*UNSIGNED_INT_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__unsignedint_serialization(release, value, expected):
    instance = modules[release].UnsignedInt(value)
    assert instance.model_dump() == expected


# ==========================================
# PositiveInt
# ==========================================

POSITIVE_INT_TEST_CASES = [
    "value, expected",
    [
        (12345, 12345),
        ("12345", 12345),
        (1, 1),
    ],
]


@pytest.mark.parametrize(*POSITIVE_INT_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__positiveint_deserialization(release, value, expected):
    instance = modules[release].PositiveInt(value)
    assert instance == expected


@pytest.mark.parametrize(*POSITIVE_INT_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__positiveint_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].positiveInt)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].PositiveInt(value))
    assert instance == expected
    # Parent class deserialization
    if isinstance(value, str):
        instance = adapter.validate_python(modules[release].String(value))
    else:
        instance = adapter.validate_python(modules[release].Integer(value))
    assert instance == expected


@pytest.mark.parametrize(*POSITIVE_INT_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__positiveint_serialization(release, value, expected):
    instance = modules[release].PositiveInt(value)
    assert instance.model_dump() == expected


# ==========================================
# Xhtml
# ==========================================

XHTML_TEST_CASES = [
    "value, expected",
    [
        ("<div>Hello</div>", "<div>Hello</div>"),
        ("<p>test</p>", "<p>test</p>"),
    ],
]


@pytest.mark.parametrize(*XHTML_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__xhtml_deserialization(release, value, expected):
    instance = modules[release].Xhtml(value)
    assert instance == expected


@pytest.mark.parametrize(*XHTML_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__xhtml_type_alias(release, value, expected):
    adapter = TypeAdapter(modules[release].xhtml)
    # Native string deserialization
    instance = adapter.validate_python(value)
    assert instance == expected
    # Class deserialization
    instance = adapter.validate_python(modules[release].Xhtml(value))
    assert instance == expected
    # Parent class deserialization
    instance = adapter.validate_python(modules[release].String(value))
    assert instance == expected


@pytest.mark.parametrize(*XHTML_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__xhtml_serialization(release, value, expected):
    instance = modules[release].Xhtml(value)
    assert instance.model_dump() == expected


# ==========================================
# Primitive Operator Tests (FHIRPrimitiveModel)
# ==========================================


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__integer_addition(release):
    a = modules[release].Integer(5)
    b = modules[release].Integer(3)
    assert a + b == 8


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__integer_addition_with_native_int(release):
    a = modules[release].Integer(10)
    assert a + 5 == 15


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__integer_subtraction(release):
    a = modules[release].Integer(10)
    b = modules[release].Integer(4)
    assert a - b == 6


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__decimal_addition(release):
    a = modules[release].Decimal(2.5)
    b = modules[release].Decimal(1.5)
    assert a + b == pytest.approx(4.0)


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__decimal_addition_with_native_float(release):
    a = modules[release].Decimal(3.0)
    assert a + 1.5 == pytest.approx(4.5)


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__integer_multiplication(release):
    a = modules[release].Integer(6)
    b = modules[release].Integer(7)
    assert a * b == 42


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__string_concatenation(release):
    a = modules[release].String("hello")
    b = modules[release].String(" world")
    assert a + b == "hello world"


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__string_concatenation_with_native_str(release):
    a = modules[release].String("foo")
    assert a + " bar" == "foo bar"


# ==========================================
# Primitive Comparison Operator Tests
# ==========================================


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__integer_equality_with_class(release):
    a = modules[release].Integer(42)
    b = modules[release].Integer(42)
    assert a == b


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__integer_equality_with_native(release):
    a = modules[release].Integer(42)
    assert a == 42


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__integer_inequality(release):
    a = modules[release].Integer(1)
    b = modules[release].Integer(2)
    assert a != b
    assert a != 2


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__integer_less_than(release):
    a = modules[release].Integer(3)
    b = modules[release].Integer(5)
    assert a < b
    assert a < 5


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__integer_greater_than(release):
    a = modules[release].Integer(10)
    b = modules[release].Integer(4)
    assert a > b
    assert a > 4


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__string_equality_with_native(release):
    a = modules[release].String("hello")
    assert a == "hello"


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__string_inequality_with_native(release):
    a = modules[release].String("hello")
    assert a != "world"


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__boolean_equality(release):
    a = modules[release].Boolean(True)
    b = modules[release].Boolean(True)
    assert a == b
    assert a == True  # noqa: E712


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__boolean_inequality(release):
    a = modules[release].Boolean(True)
    b = modules[release].Boolean(False)
    assert a != b
    assert b == False  # noqa: E712


# ==========================================
# Mixed Native/Class Coercion in Model Fields
# ==========================================


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__model_field_accepts_native_and_class_string(release):
    """A model field typed as the string type-alias accepts both str and String."""
    from pydantic import create_model

    string_alias = modules[release].string

    Model = create_model("Model", name=(string_alias, ...))

    # Native str
    from_native = Model.model_validate({"name": "Alice"})
    assert from_native.name == "Alice"  # type: ignore

    # String class
    from_class = Model.model_validate({"name": modules[release].String("Bob")})
    assert from_class.name == "Bob"  # type: ignore


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__model_field_accepts_native_and_class_integer(release):
    """A model field typed as the integer type-alias accepts both int and Integer."""
    from pydantic import create_model

    integer_alias = modules[release].integer

    Model = create_model("Model", count=(integer_alias, ...))

    from_native = Model.model_validate({"count": 7})
    assert from_native.count == 7  # type: ignore

    from_class = Model.model_validate({"count": modules[release].Integer(13)})
    assert from_class.count == 13  # type: ignore


@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__none_value_with_extension_is_valid(release):
    """A FHIRPrimitiveModel with no value but with an extension satisfies ele-1."""
    import importlib

    datatypes = importlib.import_module(f"fhircraft.fhir.resources.datatypes.{release}")
    Extension = datatypes.Extension

    instance = modules[release].String(extension=[Extension(url="http://example.org/ext", valueString="note")])  # type: ignore
    assert instance.value is None
    assert instance.extension is not None
    assert len(instance.extension) == 1
