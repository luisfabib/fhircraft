from pydantic import BaseModel, create_model, Field
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
def test_primitives__base64binary_serialization(release, value, expected):
    instance = modules[release].Base64Binary(value)
    assert instance.model_dump() == expected


# ==========================================
# Instant
# ==========================================

INSTANT_DESER_TEST_CASES = [
    "value, expected",
    [
        ("2015-02-07T13:28:17.239", datetime(2015, 2, 7, 13, 28, 17, 239000)),
        (datetime(2015, 2, 7), datetime(2015, 2, 7)),
        (datetime(2015, 2, 7, 13, 28, 17), datetime(2015, 2, 7, 13, 28, 17)),
    ],
]

INSTANT_SER_TEST_CASES = [
    "value, expected",
    [
        ("2015-02-07T13:28:17.239", "2015-02-07T13:28:17.239"),
        (datetime(2015, 2, 7), "2015-02-07T00:00:00"),
        (datetime(2015, 2, 7, 13, 28, 17), "2015-02-07T13:28:17"),
    ],
]


@pytest.mark.parametrize(*INSTANT_DESER_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__instant_deserialization(release, value, expected):
    instance = modules[release].Instant(value)
    assert instance == expected


@pytest.mark.parametrize(*INSTANT_SER_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__instant_serialization(release, value, expected):
    instance = modules[release].Instant(value)
    assert instance.model_dump() == expected


# ==========================================
# Date
# ==========================================

DATE_DESER_TEST_CASES = [
    "value, expected",
    [
        ("2015-02-07", date(2015, 2, 7)),
        ("2015-02", "2015-02"),
        ("2015", "2015"),
        (date(2015, 2, 7), date(2015, 2, 7)),
    ],
]

DATE_SER_TEST_CASES = [
    "value, expected",
    [
        ("2015-02-07", "2015-02-07"),
        ("2015-02", "2015-02"),
        ("2015", "2015"),
        (date(2015, 2, 7), "2015-02-07"),
    ],
]


@pytest.mark.parametrize(*DATE_DESER_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__date_deserialization(release, value, expected):
    instance = modules[release].Date(value)
    assert instance == expected


@pytest.mark.parametrize(*DATE_SER_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__date_serialization(release, value, expected):
    instance = modules[release].Date(value)
    assert instance.model_dump() == expected


# ==========================================
# DateTime
# ==========================================

DATETIME_DESER_TEST_CASES = [
    "value, expected",
    [
        ("2015-02-07T13:28:17.239", datetime(2015, 2, 7, 13, 28, 17, 239000)),
        ("2015-02-07", date(2015, 2, 7)),
        ("2015-02", "2015-02"),
        ("2015", "2015"),
        (datetime(2015, 2, 7), datetime(2015, 2, 7)),
        (datetime(2015, 2, 7, 13, 28, 17), datetime(2015, 2, 7, 13, 28, 17)),
    ],
]

DATETIME_SER_TEST_CASES = [
    "value, expected",
    [
        ("2015-02-07T13:28:17.239", "2015-02-07T13:28:17.239"),
        ("2015-02-07", "2015-02-07"),
        ("2015-02", "2015-02"),
        ("2015", "2015"),
        (datetime(2015, 2, 7), "2015-02-07T00:00:00"),
        (datetime(2015, 2, 7, 13, 28, 17), "2015-02-07T13:28:17"),
    ],
]


@pytest.mark.parametrize(*DATETIME_DESER_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__datetime_deserialization(release, value, expected):
    instance = modules[release].DateTime(value)
    assert instance == expected


@pytest.mark.parametrize(*DATETIME_SER_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__datetime_serialization(release, value, expected):
    instance = modules[release].DateTime(value)
    assert instance.model_dump() == expected


# ==========================================
# Time
# ==========================================

TIME_DESER_TEST_CASES = [
    "value, expected",
    [
        ("12:54", time(12, 54)),
        ("12:54:32", time(12, 54, 32)),
        (time(12, 54), time(12, 54)),
        (time(12, 54, 32), time(12, 54, 32)),
    ],
]

TIME_SER_TEST_CASES = [
    "value, expected",
    [
        ("12:54", "12:54:00"),
        ("12:54:32", "12:54:32"),
        (time(12, 54), "12:54:00"),
        (time(12, 54, 32), "12:54:32"),
    ],
]


@pytest.mark.parametrize(*TIME_DESER_TEST_CASES)
@pytest.mark.parametrize(*FHIR_RELEASES)
def test_primitives__time_deserialization(release, value, expected):
    instance = modules[release].Time(value)
    assert instance == expected


@pytest.mark.parametrize(*TIME_SER_TEST_CASES)
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
def test_primitives__xhtml_serialization(release, value, expected):
    instance = modules[release].Xhtml(value)
    assert instance.model_dump() == expected
