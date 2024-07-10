from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.boolean import *
from fhircraft.fhir.path.engine.additional import GetValue
from collections import namedtuple
import pytest 



#-------------
# And
#-------------

and_boolean_logic_cases = (
    (True, True, True),
    (True, False, False),
    (True, [], []),
    (False, True, False),
    (False, False, False),
    (False, [], False),
    ([], True, []),
    ([], False, False),
    ([], [], []),
)
@pytest.mark.parametrize("left, right, expected", and_boolean_logic_cases)
def test_and_returns_correct_logic_boolean(left, right, expected):    
    resource = namedtuple('Resource', ['left', 'right'])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = And(Invocation(Element('left'),GetValue()), Invocation(Element('right'), GetValue())).evaluate(collection)
    assert result == expected


#-------------
# Or
#-------------

or_boolean_logic_cases = (
    (True, True, True),
    (True, False, True),
    (True, [], True),
    (False, True, True),
    (False, False, False),
    (False, [], []),
    ([], True, True),
    ([], False, []),
    ([], [], []),
)
@pytest.mark.parametrize("left, right, expected", or_boolean_logic_cases)
def test_or_returns_correct_logic_boolean(left, right, expected):    
    resource = namedtuple('Resource', ['left', 'right'])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Or(Invocation(Element('left'),GetValue()), Invocation(Element('right'), GetValue())).evaluate(collection)
    assert result == expected

#-------------
# Xor
#-------------

xor_boolean_logic_cases = (
    (True, True, False),
    (True, False, True),
    (True, [], []),
    (False, True, True),
    (False, False, False),
    (False, [], []),
    ([], True, []),
    ([], False, []),
    ([], [], []),
)
@pytest.mark.parametrize("left, right, expected", xor_boolean_logic_cases)
def test_xor_returns_correct_logic_boolean(left, right, expected):    
    resource = namedtuple('Resource', ['left', 'right'])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Xor(Invocation(Element('left'),GetValue()), Invocation(Element('right'), GetValue())).evaluate(collection)
    assert result == expected

#-------------
# Implies
#-------------

implies_boolean_logic_cases = (
    (True, True, True),
    (True, False, False),
    (True, [], []),
    (False, True, True),
    (False, False, True),
    (False, [], True),
    ([], True, True),
    ([], False, []),
    ([], [], []),
)
@pytest.mark.parametrize("left, right, expected", implies_boolean_logic_cases)
def test_implies_returns_correct_logic_boolean(left, right, expected):    
    resource = namedtuple('Resource', ['left', 'right'])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Implies(Invocation(Element('left'),GetValue()), Invocation(Element('right'), GetValue())).evaluate(collection)
    assert result == expected

