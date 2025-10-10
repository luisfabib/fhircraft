
from pydantic import BaseModel, create_model, Field
import fhircraft.fhir.resources.datatypes.primitives as fhir_types
from datetime import date, time, datetime
import json 
import pytest 

fhir_types_test_cases = (
    ('Boolean', True, True),
    ('Boolean', 'true', True),
    ('Boolean', 'false', False),
    ('Boolean', False, False),
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
    ('Instant', '2015-02-07T13:28:17.239', '2015-02-07T13:28:17.239'),
    ('Instant', datetime(2015,2,7), '2015-02-07T00:00:00'),
    ('Instant', datetime(2015,2,7, 13,28,17), '2015-02-07T13:28:17'),
    ('Date', '2015-02-07', '2015-02-07'),
    ('Date', '2015-02', '2015-02'),
    ('Date', '2015', '2015'),
    ('Date', date(2015,2,7), '2015-02-07'),
    ('DateTime', '2015-02-07T13:28:17.239', '2015-02-07T13:28:17.239'),
    ('DateTime', '2015-02-07', '2015-02-07'),
    ('DateTime', '2015-02',  '2015-02'),
    ('DateTime', '2015', '2015'),
    ('DateTime', datetime(2015,2,7), '2015-02-07T00:00:00'),
    ('DateTime', datetime(2015,2,7, 13,28,17), '2015-02-07T13:28:17'),
    ('Time', '12:54', '12:54'),
    ('Time', '12:54:32', '12:54:32'),
    ('Time', time(12,54), '12:54:00'),
    ('Time', time(12,54,32), '12:54:32'),
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
def test_fhir_primitive_type_implicit_type_casting(fieldType, inputValue, expectedValue):
    fhir_type = getattr(fhir_types, fieldType)        
    testModel = create_model('testModel', field=(fhir_type, Field()))
    instance = testModel(field = inputValue)
    assert instance.field == expectedValue

fhir_types_serialization_test_cases = (
    ('Boolean', True, True),
    ('Boolean', False, False),
    ('Integer', 1234, 1234),
    ('String', 'stringTest', 'stringTest'),
    ('Decimal', 12, 12),
    ('Decimal', '12.0', 12.0),
    ('Decimal', 12.52, 12.52),
    ('Decimal', '12.52', 12.52),
    ('Uri', 'foo://example.com:8042/over/there?name=ferret#nose', 'foo://example.com:8042/over/there?name=ferret#nose'),
    ('Url', 'http://www.example.com/index.html', 'http://www.example.com/index.html'),
    ('Canonical', 'example.com/resources/1234', 'example.com/resources/1234'),
    ('Base64Binary', 'aGVsbG8gd29yaw==', 'aGVsbG8gd29yaw=='),
    ('Instant', '2015-02-07T13:28:17.239', '2015-02-07T13:28:17.239'),
    ('Date', '2015-02-07', '2015-02-07'),
    ('Date', '2015-02', '2015-02'),
    ('Date', '2015', '2015'),
    ('DateTime', '2015-02-07T13:28:17.239', '2015-02-07T13:28:17.239'),
    ('DateTime', '2015-02-07', '2015-02-07'),
    ('DateTime', '2015-02', '2015-02'),
    ('DateTime',  '2015', '2015'),
    ('Time', '12:54', '12:54'),
    ('Time', '12:54:32', '12:54:32'),
    ('Code', 'code1234', 'code1234'),    
    ('Oid', 'urn:oid:1.2.3.4.5', 'urn:oid:1.2.3.4.5'),
    ('Id', 'ID.A.B.3.4.5', 'ID.A.B.3.4.5'),
    ('Markdown', 'test string text', 'test string text'),
    ('UnsignedInt', 12345, 12345),
    ('PositiveInt', 12345, 12345),
    ('Uuid', 'urn:uuid:c757873d-ec9a-4326-a141-556f43239520', 'urn:uuid:c757873d-ec9a-4326-a141-556f43239520'),
)
@pytest.mark.parametrize("fieldType, inputValue, serializedValue", fhir_types_serialization_test_cases)
def test_fhir_primitive_type_serialization(fieldType, inputValue, serializedValue):
    fhir_type = getattr(fhir_types, fieldType)        
    testModel = create_model('testModel', field=(fhir_type, Field()))
    instance = testModel(field = inputValue)
    assert json.loads(instance.model_dump_json()) == {"field":serializedValue}
    