from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.navigation import *
from fhircraft.fhir.resources.complex_types import Extension as ExtensionType
from pydantic import BaseModel
from collections import namedtuple
import pytest 
from unittest import TestCase


#-------------
# Children
#-------------

def test_children_returns_empty_for_empty_collection():
    collection = []
    result = Children().evaluate(collection)
    assert result == []

def test_children_returns_correct_elements():
    class Resource(BaseModel):
        fieldA: int 
        fieldB: int 
        fieldC: int 

    resource = Resource(
        fieldA=1, fieldB=2, fieldC=3
    )
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Children().evaluate(collection)
    assert result[0].value == 1
    assert result[1].value == 2
    assert result[2].value == 3




#-------------
# Descendants
#-------------

def test_decendants_returns_empty_for_empty_collection():
    collection = []
    result = Descendants().evaluate(collection)
    assert result == []

def test_descendants_returns_correct_elements():
    class Resource(BaseModel):
        fieldA: int 
        fieldB: int 
        fieldC: int 
        subfield: "Resource" = None

    resource = Resource(
        fieldA=1, fieldB=2, fieldC=3, subfield=Resource(
            fieldA=4, fieldB=5, fieldC=6
        )
    )
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Descendants().evaluate(collection)
    assert result[0].value == 1
    assert result[1].value == 2
    assert result[2].value == 3
    assert result[3].value == resource.subfield
    assert result[4].value == 4
    assert result[5].value == 5
    assert result[6].value == 6
