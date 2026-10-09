from fhircraft.fhir.path.collection import FHIRPathCollection
from typing import Union

from pydantic import BaseModel

from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.navigation import *
from fhircraft.fhir.resources.datatypes.R4.complex import Element as El, Extension

env = dict()

# -------------
# Children
# -------------


def test_children_returns_empty_for_empty_collection():
    collection = []
    result = Children().evaluate(FHIRPathCollection(collection), env)
    assert result == []


def test_children_returns_correct_elements_model():
    class Resource(BaseModel):
        fieldA: int
        fieldB: int
        fieldC: int

    resource = Resource(fieldA=1, fieldB=2, fieldC=3)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Children().evaluate(FHIRPathCollection(collection), env)
    assert result[0] == 1
    assert result[1] == 2
    assert result[2] == 3


def test_children_returns_correct_elements_dict():
    class Resource(BaseModel):
        fieldA: int
        fieldB: int
        fieldC: int

    resource = Resource(fieldA=1, fieldB=2, fieldC=3).model_dump()
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Children().evaluate(FHIRPathCollection(collection), env)
    assert result[0] == 1
    assert result[1] == 2
    assert result[2] == 3


def test_children_string_representation():
    expression = Children()
    assert str(expression) == "children()"


# -------------
# Descendants
# -------------


def test_decendants_returns_empty_for_empty_collection():
    collection = []
    result = Descendants().evaluate(FHIRPathCollection(collection), env)
    assert result == []


def test_descendants_returns_correct_elements():
    class Resource(BaseModel):
        fieldA: int
        fieldB: int
        fieldC: int
        subfield: Union["Resource", None] = None

    resource = Resource(
        fieldA=1, fieldB=2, fieldC=3, subfield=Resource(fieldA=4, fieldB=5, fieldC=6)
    )
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Descendants().evaluate(FHIRPathCollection(collection), env)
    assert result[0] == 1
    assert result[1] == 2
    assert result[2] == 3
    assert result[3] == resource.subfield
    assert result[4] == 4
    assert result[5] == 5
    assert result[6] == 6
    assert result[5] == 5
    assert result[6] == 6


def test_descendants_string_representation():
    expression = Descendants()
    assert str(expression) == "descendants()"
