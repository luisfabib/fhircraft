from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, Invocation, Element
from fhircraft.fhir.path.engine.additional import GetValue
from fhircraft.fhir.path.engine.collection import *
from collections import namedtuple 

#-------------
# Union
#-------------

def test_union_returns_combined_collection_without_duplicates():    
    resource = namedtuple('Resource', ['left', 'right'])(left='A', right='B')
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Union(Invocation(Element('left'),GetValue()), Invocation(Element('right'), GetValue())).evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="A"), FHIRPathCollectionItem(value="B")]



#-------------
# In
#-------------

def test_in_returns_empty_if_left_empty():    
    resource = namedtuple('Resource', ['left', 'right'])(left='A', right=['A','B','C'])
    collection = [FHIRPathCollectionItem(value=resource)]
    result = In([], Element('right')).evaluate(collection)
    assert result == []

def test_in_returns_false_if_right_empty():    
    resource = namedtuple('Resource', ['left', 'right'])(left='A', right=['A','B','C'])
    collection = [FHIRPathCollectionItem(value=resource)]
    result = In('B', []).evaluate(collection)
    assert result == False

def test_in_checks_membership_correctly():    
    resource = namedtuple('Resource', ['left', 'right'])(left='A', right=['A','B','C'])
    collection = [FHIRPathCollectionItem(value=resource)]
    result = In('B', Element('right')).evaluate(collection)
    assert result == True



#-------------
# Contains
#-------------

def test_contains_returns_empty_if_right_empty():    
    resource = namedtuple('Resource', ['left', 'right'])(left='A', right=['A','B','C'])
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Contains(Element('right'), []).evaluate(collection)
    assert result == []

def test_contains_returns_false_if_left_empty():    
    resource = namedtuple('Resource', ['left', 'right'])(left='A', right=['A','B','C'])
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Contains([], 'B').evaluate(collection)
    assert result == False

def test_contains_checks_containership_correctly():    
    resource = namedtuple('Resource', ['left', 'right'])(left='A', right=['A','B','C'])
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Contains(Element('right'), 'B', ).evaluate(collection)
    assert result == True