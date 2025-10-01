from collections import namedtuple

from fhircraft.fhir.path.engine.additional import GetValue
from fhircraft.fhir.path.engine.collection import *
from fhircraft.fhir.path.engine.core import Element, FHIRPathCollectionItem, Invocation

env = dict()

# -------------
# Union
# -------------


def test_union_returns_combined_collection_without_duplicates():
    resource = namedtuple("Resource", ["left", "right"])(left="A", right="B")
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Union(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert result == [
        FHIRPathCollectionItem(value="A"),
        FHIRPathCollectionItem(value="B"),
    ]

def test_union_string_representation():
    expression = Union(Element("left"), Element("right"))
    assert str(expression) == "left | right"

# -------------
# In
# -------------


def test_in_returns_empty_if_left_empty():
    resource = namedtuple("Resource", ["left", "right"])(
        left="A", right=["A", "B", "C"]
    )
    collection = [FHIRPathCollectionItem(value=resource)]
    result = In([], Element("right")).evaluate(collection, env)
    result = result[0].value if len(result) == 1 else result
    assert result == []

def test_in_returns_false_if_right_empty():
    resource = namedtuple("Resource", ["left", "right"])(
        left="A", right=["A", "B", "C"]
    )
    collection = [FHIRPathCollectionItem(value=resource)]
    result = In([FHIRPathCollectionItem(value="B")], []).evaluate(collection, env)
    result = result[0].value if len(result) == 1 else result
    assert result == False


def test_in_checks_membership_correctly():
    resource = namedtuple("Resource", ["left", "right"])(
        left="A", right=["A", "B", "C"]
    )
    collection = [FHIRPathCollectionItem(value=resource)]
    result = In([FHIRPathCollectionItem(value="B")], Element("right")).evaluate(
        collection, env
    )
    result = result[0].value if len(result) == 1 else result
    assert result == True

def test_in_string_representation():
    expression = In(Element("left"), Element("right"))
    assert str(expression) == "left in right"

# -------------
# Contains
# -------------


def test_contains_returns_empty_if_right_empty():
    resource = namedtuple("Resource", ["left", "right"])(
        left="A", right=["A", "B", "C"]
    )
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Contains(Element("right"), []).evaluate(collection, env)
    result = result[0].value if len(result) == 1 else result
    assert result == []


def test_contains_returns_false_if_left_empty():
    resource = namedtuple("Resource", ["left", "right"])(
        left="A", right=["A", "B", "C"]
    )
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Contains([], [FHIRPathCollectionItem(value="B")]).evaluate(collection, env)
    result = result[0].value if len(result) == 1 else result
    assert result == False


def test_contains_checks_containership_correctly():
    resource = namedtuple("Resource", ["left", "right"])(
        left="A", right=["A", "B", "C"]
    )
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Contains(Element("right"), [FHIRPathCollectionItem(value="B")]).evaluate(
        collection, env
    )
    result = result[0].value if len(result) == 1 else result
    assert result == True

def test_contains_string_representation():
    expression = Contains(Element("left"), Element("right"))
    assert str(expression) == "left contains right"
