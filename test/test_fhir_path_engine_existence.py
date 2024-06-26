from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.existence import *
import operator 

import pytest 
from unittest import TestCase


#-------------
# Empty
#-------------

def test_empty_returns_true_for_empty_collection():
    collection = []
    result = Empty().evaluate(collection)
    assert result is True

def test_empty_returns_false_for_non_empty_collection():
    collection = [FHIRPathCollectionItem(value="item1")]
    result = Empty().evaluate(collection)
    assert result is False


#-------------
# Exists
#-------------

def test_exists_returns_false_for_empty_collection():
    collection = []
    result =  Exists().evaluate(collection)
    assert result is False
    
def test_exists_returns_true_for_non_empty_collection():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = Exists().evaluate(collection)
    assert result is True

def test_exists_applies_criteria_correctly_and_returns_true_if_filtered_collection_has_elements():
    criteria = Where(Operation(This(), operator.gt,1))
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = Exists(criteria).evaluate(collection)
    assert result is True

def test_exists_applies_criteria_correctly_and_returns_false_if_filtered_collection_is_empty():
    criteria = Where(Operation(This(), operator.gt,9999))
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = Exists(criteria).evaluate(collection)
    assert result is False

#-------------
# All
#-------------

def test_all_returns_true_for_empty_collection():
    collection = []
    result = All(None).evaluate(collection)
    assert result is True
    
def test_all_returns_true_for_criteria_applying_to_all():
    criteria = Operation(This(), operator.gt,0)
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = All(criteria).evaluate(collection)
    assert result is True
    
def test_all_returns_false_for_criteria_not_applying_to_all():
    criteria = Operation(This(), operator.gt,0)
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = All(criteria).evaluate(collection)
    assert result is True

#-------------
# AllTrue
#-------------

def test_allTrue_returns_true_for_empty_collection():
    collection = []
    result = AllTrue().evaluate(collection)
    assert result is True
    
def test_allTrue_returns_true_if_all_items_are_true():
    collection = [FHIRPathCollectionItem(value=True), FHIRPathCollectionItem(value=True)]
    result = AllTrue().evaluate(collection)
    assert result is True
    
def test_allTrue_returns_false_if_any_item_is_false():
    collection = [FHIRPathCollectionItem(value=True), FHIRPathCollectionItem(value=False)]
    result = AllTrue().evaluate(collection)
    assert result is False


#-------------
# AnyTrue
#-------------

def test_anyTrue_returns_false_for_empty_collection():
    collection = []
    result = AnyTrue().evaluate(collection)
    assert result is False
    
def test_anyTrue_returns_false_if_all_items_are_false():
    collection = [FHIRPathCollectionItem(value=False), FHIRPathCollectionItem(value=False)]
    result = AnyTrue().evaluate(collection)
    assert result is False
    
def test_anyTrue_returns_true_if_any_item_is_true():
    collection = [FHIRPathCollectionItem(value=True), FHIRPathCollectionItem(value=False)]
    result = AnyTrue().evaluate(collection)
    assert result is True

    
#-------------
# AllFalse
#-------------

def test_allFalse_returns_true_for_empty_collection():
    collection = []
    result = AllFalse().evaluate(collection)
    assert result is True
    
def test_allFalse_returns_true_if_all_items_are_false():
    collection = [FHIRPathCollectionItem(value=False), FHIRPathCollectionItem(value=False)]
    result = AllFalse().evaluate(collection)
    assert result is True
    
def test_allFalse_returns_false_if_any_item_is_true():
    collection = [FHIRPathCollectionItem(value=True), FHIRPathCollectionItem(value=False)]
    result = AllFalse().evaluate(collection)
    assert result is False
    

#-------------
# AnyFalse
#-------------

def test_anyFalse_returns_false_for_empty_collection():
    collection = []
    result = AnyFalse().evaluate(collection)
    assert result is False
    
def test_anyFalse_returns_false_if_all_items_are_true():
    collection = [FHIRPathCollectionItem(value=True), FHIRPathCollectionItem(value=True)]
    result = AnyFalse().evaluate(collection)
    assert result is False
    
def test_anyFalse_returns_true_if_any_item_is_false():
    collection = [FHIRPathCollectionItem(value=True), FHIRPathCollectionItem(value=False)]
    result = AnyFalse().evaluate(collection)
    assert result is True



#-------------
# Count
#-------------

def test_count_empty_collection():
    collection = []
    result = Count().evaluate(collection)
    assert result == 0

def test_count_empty_collection():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = Count().evaluate(collection)
    assert result == 2
    


#-------------
# SubsetOf
#-------------

def test_subsetOf_returns_false_when_other_collection_is_empty():
    other_collection = []
    collection = [FHIRPathCollectionItem(value=1)]
    result = SubsetOf(other=other_collection).evaluate(collection)
    assert result is False

def test_subsetOf_returns_true_when_all_items_in_input_collection_are_in_other_collection():
    other_collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    collection = [FHIRPathCollectionItem(value=1)]
    result = SubsetOf(other=other_collection).evaluate(collection)
    assert result is True

def test_subsetOf_returns_false_when_not_all_items_in_input_collection_are_in_other_collection():
    other_collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    collection = [FHIRPathCollectionItem(value=1),FHIRPathCollectionItem(value=3)]
    result = SubsetOf(other=other_collection).evaluate(collection)
    assert result is False



#-------------
# SupersetOf
#-------------

def test_supersetOf_returns_false_when_other_collection_is_empty():
    other_collection = []
    collection = [FHIRPathCollectionItem(value=1)]
    result = SupersetOf(other=other_collection).evaluate(collection)
    assert result is True

def test_supersetOf_returns_true_when_all_items_in_other_collection_are_in_ipnut_collection():
    other_collection = [FHIRPathCollectionItem(value=1)]
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = SupersetOf(other=other_collection).evaluate(collection)
    assert result is True

def test_supersetOf_returns_false_when_not_all_items_in_other_collection_are_in_input_collection():
    other_collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    collection = [FHIRPathCollectionItem(value=1),FHIRPathCollectionItem(value=3)]
    result = SupersetOf(other=other_collection).evaluate(collection)
    assert result is False



#-------------
# Distinct
#-------------

def test_disctinct_empty_collection():
    collection = []
    result = Distinct().evaluate(collection)
    assert result == []
    
def test_disctinct_no_repeatition():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = Distinct().evaluate(collection)
    assert sorted(result, key=lambda item: item.value) == sorted(collection, key=lambda item: item.value)
    
def test_disctinct_with_repeatition():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    new_collection = collection + collection
    result = Distinct().evaluate(new_collection)
    assert sorted(result, key=lambda item: item.value) == sorted(collection, key=lambda item: item.value)
    


#-------------
# IsDistinct
#-------------

def test_isDisctinct_empty_collection():
    collection = []
    result = IsDistinct().evaluate(collection)
    assert result == True
    
def test_isDisctinct_no_repeatition():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = IsDistinct().evaluate(collection)
    assert result == True
    
def test_isDisctinct_with_repeatition():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    new_collection = collection + collection
    result = IsDistinct().evaluate(new_collection)
    assert result == False
    