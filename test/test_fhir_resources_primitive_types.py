
from pydantic import BaseModel, create_model, Field
import fhircraft.fhir.profiling.primitive_types as fhir_types
import datetime
import pytest 

# Format: (string, expected_object)
fhir_types_test_cases = (
    ('Boolean', True, True),
    ('Boolean', 'true', True),
    ('Boolean', 'false', False),
    ('Integer', 1234, 1234),
    ('Integer', '1234', 1234),
    ('String', 'stringTest', 'stringTest'),
    ('Decimal', 12, 12),
    ('Decimal', '12', 12),
    ('Decimal', 12.52, 12.52),
    ('Decimal', '12.52', 12.52),
    ('Uri', 'foo://example.com:8042/over/there?name=ferret#nose', 'foo://example.com:8042/over/there?name=ferret#nose'),
    ('Url', 'http://www.example.com/index.html', 'http://www.example.com/index.html'),
    ('Canonical', 'example.com/resources/1234', 'example.com/resources/1234'),
    ('Base64Binary', 'aGVsbG8gd29yaw==', 'aGVsbG8gd29yaw=='),
    ('Instant', '2015-02-07T13:28:17.239', datetime.datetime(2015, 2, 7, 13, 28, 17, 239000)),
    ('Instant', datetime.datetime(2015, 2, 7, 13, 28, 17, 239000), datetime.datetime(2015, 2, 7, 13, 28, 17, 239000)),
    ('Date', '2015-02-07', datetime.date(2015, 2, 7)),
    ('Date', '2015-02', datetime.date(2015, 2, 1)),
    ('Date', '2015', datetime.date(2015,1 , 1)),
    ('Date', datetime.date(2015, 2, 7), datetime.date(2015, 2, 7)),
    ('DateTime', '2015-02-07T13:28:17.239', datetime.datetime(2015, 2, 7, 13, 28, 17, 239000)),
    ('DateTime', '2015-02-07', datetime.datetime(2015, 2, 7)),
    ('DateTime', '2015-02', datetime.datetime(2015, 2, 1)),
    ('DateTime', '2015', datetime.datetime(2015, 1 , 1)),
    ('DateTime', datetime.datetime(2015, 2, 7, 13, 28, 17, 239000), datetime.datetime(2015, 2, 7, 13, 28, 17, 239000)),
    ('Time', '12:54', datetime.time(12, 54)),
    ('Time', '12:54:32', datetime.time(12, 54, 32)),
    ('Time', datetime.time(12, 54, 32), datetime.time(12, 54, 32)),
    ('Code', 'code1234', 'code1234'),    
    ('Oid', 'urn:oid:1.2.3.4.5', 'urn:oid:1.2.3.4.5'),
    ('Id', 'ID.A.B.3.4.5', 'ID.A.B.3.4.5'),
    ('Markdown', 'test string text', 'test string text'),
    ('UnsignedInt', '12345', 12345),
    ('UnsignedInt', 12345, 12345),
    ('PositiveInt', '12345', 12345),
    ('PositiveInt', 12345, 12345),
    ('Uuid', 'urn:uuid:c757873d-ec9a-4326-a141-556f43239520', 'urn:uuid:c757873d-ec9a-4326-a141-556f43239520'),
)
@pytest.mark.parametrize("fieldType, inputValue, expectedValue", fhir_types_test_cases)
def test_parser(fieldType, inputValue, expectedValue):
    fhir_type = getattr(fhir_types, fieldType)        
    testModel = create_model('testModel', field=(fhir_type, Field()))
    instance = testModel(field = inputValue)
    assert instance.field == expectedValue
    