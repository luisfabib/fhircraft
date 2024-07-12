from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.types import *
from fhircraft.fhir.path.engine.literals import Quantity
from fhircraft.fhir.path.engine.additional import GetValue
from collections import namedtuple
import pytest 



#-------------
# Is
#-------------

addition_cases = (
    ('ABC', 'String', True),
    (12, 'Integer', True),
    (23.32, 'Decimal', True),
    (True, 'Boolean', True),
    (Date('@2024'), 'Date', True),
    (Quantity(12,'g'), 'Quantity', True),
    (12, 'String', False),
    ('12', 'Integer', False),
)
@pytest.mark.parametrize("left, type_specifier, expected", addition_cases)
def test_is_returns_correct_boolean(left, type_specifier, expected):    
    resource = namedtuple('Resource', ['left'])(left=left)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Is(Invocation(Element('left'),GetValue()), type_specifier).evaluate(collection)
    assert result == expected

@pytest.mark.parametrize("left, type_specifier, expected", addition_cases)
def test_legacy_is_returns_correct_boolean(left, type_specifier, expected):    
    collection = [FHIRPathCollectionItem(value=left)]
    result = LegacyIs(type_specifier).evaluate(collection)
    assert result == expected


#-------------
# Is
#-------------

addition_cases = (
    ('String', 'ABC'),
    ('Integer', 123),
    ('Decimal', True),
    ('Boolean', True),
    ('Date', Date('@2024')),
)
@pytest.mark.parametrize("type_specifier, expected", addition_cases)
def test_as_returns_correct_boolean(type_specifier, expected):    
    collection = [FHIRPathCollectionItem(value=expected)]
    result = As(This(), type_specifier).evaluate(collection)
    assert result == expected

@pytest.mark.parametrize("type_specifier, expected", addition_cases)
def test_legacy_as_returns_correct_boolean(type_specifier, expected):    
    collection = [FHIRPathCollectionItem(value=expected)]
    result = LegacyAs(type_specifier).evaluate(collection)
    assert result == expected
