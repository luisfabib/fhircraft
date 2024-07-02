
from pydantic import BaseModel, create_model, Field
import fhircraft.fhir.profiling.primitive_types as fhir_types
import datetime
import pytest 

# Format: (string, expected_object)
fhir_types_test_cases = (
    ('boolean', True, True),
    ('boolean', 'true', True),
    ('boolean', 'false', False),
    ('integer', 1234, 1234),
    ('integer', '1234', 1234),
    ('string', 'stringTest', 'stringTest'),
    ('decimal', 12, 12),
    ('decimal', '12', 12),
    ('decimal', 12.52, 12.52),
    ('decimal', '12.52', 12.52),
    ('uri', 'foo://example.com:8042/over/there?name=ferret#nose', 'foo://example.com:8042/over/there?name=ferret#nose'),
    ('url', 'http://www.example.com/index.html', 'http://www.example.com/index.html'),
    ('canonical', 'example.com/resources/1234', 'example.com/resources/1234'),
    ('base64Binary', 'aGVsbG8gd29yaw==', 'aGVsbG8gd29yaw=='),
    ('instant', '2015-02-07T13:28:17.239', datetime.datetime(2015, 2, 7, 13, 28, 17, 239000)),
    ('instant', datetime.datetime(2015, 2, 7, 13, 28, 17, 239000), datetime.datetime(2015, 2, 7, 13, 28, 17, 239000)),
    ('date', '2015-02-07', datetime.date(2015, 2, 7)),
    ('date', '2015-02', datetime.date(2015, 2, 1)),
    ('date', '2015', datetime.date(2015,1 , 1)),
    ('date', datetime.date(2015, 2, 7), datetime.date(2015, 2, 7)),
    ('datetime', '2015-02-07T13:28:17.239', datetime.datetime(2015, 2, 7, 13, 28, 17, 239000)),
    ('datetime', '2015-02-07', datetime.datetime(2015, 2, 7)),
    ('datetime', '2015-02', datetime.datetime(2015, 2, 1)),
    ('datetime', '2015', datetime.datetime(2015, 1 , 1)),
    ('datetime', datetime.datetime(2015, 2, 7, 13, 28, 17, 239000), datetime.datetime(2015, 2, 7, 13, 28, 17, 239000)),
    ('time', '12:54', datetime.time(12, 54)),
    ('time', '12:54:32', datetime.time(12, 54, 32)),
    ('time', datetime.time(12, 54, 32), datetime.time(12, 54, 32)),
    ('code', 'code1234', 'code1234'),    
    ('oid', 'urn:oid:1.2.3.4.5', 'urn:oid:1.2.3.4.5'),
    ('id', 'ID.A.B.3.4.5', 'ID.A.B.3.4.5'),
    ('markdown', 'test string text', 'test string text'),
    ('unsignedInt', '12345', 12345),
    ('unsignedInt', 12345, 12345),
    ('positiveInt', '12345', 12345),
    ('positiveInt', 12345, 12345),
    ('uuid', 'urn:uuid:c757873d-ec9a-4326-a141-556f43239520', 'urn:uuid:c757873d-ec9a-4326-a141-556f43239520'),
)
@pytest.mark.parametrize("fieldType, inputValue, expectedValue", fhir_types_test_cases)
def test_parser(fieldType, inputValue, expectedValue):
    fhir_type = getattr(fhir_types, fieldType)        
    testModel = create_model('testModel', field=(fhir_type, Field()))
    instance = testModel(field = inputValue)
    assert instance.field == expectedValue
    