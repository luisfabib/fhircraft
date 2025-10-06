from collections import namedtuple
from unittest import TestCase

import pytest

from fhircraft.fhir.path.engine.core import (
    Element,
    FHIRPathCollectionItem,
    FHIRPathError,
    Invocation,
)
from fhircraft.fhir.path.engine.core import This
from fhircraft.fhir.path.engine.subsetting import *
from fhircraft.fhir.resources.datatypes import get_complex_FHIR_type

Coding = get_complex_FHIR_type("Coding")
CodeableConcept = get_complex_FHIR_type("CodeableConcept")


env = dict()

# -------------
# Indexing
# -------------


def test_indexing_returns_empty_for_empty_collection():
    collection = []
    result = Index(1).evaluate(collection, env, create=False)
    assert result == []


def test_indexing_returns_empty_for_out_of_bounds_index():
    collection = [FHIRPathCollectionItem(value="item1")]
    result = Index(1).evaluate(collection, env, create=False)
    assert result == []


def test_indexing_returns_correct_item_from_collection():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Index(1).evaluate(collection, env, create=False)
    assert result == [collection[1]]


def test_indexing_returns_last_with_negative_index():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Index(-1).evaluate(collection, env, create=False)
    assert result == [collection[2]]

def test_index_string_representation():
    expression = Index(2)
    assert str(expression) == "[2]"

class TestIndexPrimitive(TestCase):

    def setUp(self):
        TestResource = namedtuple("TestResource", "field")
        self.resource = TestResource(field=[1, 2, 3])
        parent = FHIRPathCollectionItem(self.resource, path=This())
        self.collection = Element("field").evaluate([parent], env)

    def test_index_evaluates_correctly(self):
        result = Index(2).evaluate(self.collection, env, create=False)
        assert len(result) == 1
        assert result[0].value == 3
        assert len(self.resource.field) == 3

    def test_index_creates_missing_elements(self):
        result = Index(5).evaluate(self.collection, env, create=True)
        assert len(result) == 1
        assert result[0].value is None
        assert len(self.resource.field) == 6

    def test_index_does_not_modify_collection_out_of_bounds(self):
        result = Index(10).evaluate(self.collection, env, create=False)
        assert len(result) == 0
        assert len(self.resource.field) == 3

    def test_index_updates_value(self):
        Index(2).update_values(self.collection, value="value")
        assert len(self.resource.field) == 3
        assert self.resource.field[2] == "value"

    def test_index_updates_and_creates_value(self):
        Index(10).update_values(self.collection, value="value")
        assert len(self.resource.field) == 11
        assert self.resource.field[10] == "value"

    def test_index_handles_negative_indices(self):
        result = Index(-1).evaluate(self.collection, env, create=False)
        assert len(result) == 1
        assert result[0].value == 3
        assert len(self.resource.field) == 3

    def test_index_handles_non_integer_indices(self):
        with pytest.raises(FHIRPathError):
            Index("a")  # type: ignore


class TestIndexResources(TestCase):

    def setUp(self):
        self.resource = CodeableConcept(
            coding=[
                Coding(code="code-1", system="system-1"),
                Coding(code="code-2", system="system-2"),
                Coding(code="code-3", system="system-3"),
            ]
        )
        parent = FHIRPathCollectionItem(self.resource, path=This())
        self.collection = Element("coding").evaluate([parent], env)

    def test_index_evaluates_correctly(self):
        result = Index(2).evaluate(self.collection, env, create=False)
        assert len(result) == 1
        assert result[0].value == Coding(code="code-3", system="system-3")
        assert len(self.resource.coding) == 3

    def test_index_creates_missing_elements(self):
        result = Index(5).evaluate(self.collection, env, create=True)
        assert len(result) == 1
        assert result[0].value == Coding.model_construct()
        assert len(self.resource.coding) == 6

    def test_index_does_not_modify_collection_out_of_bounds(self):
        result = Index(10).evaluate(self.collection, env, create=False)
        assert len(result) == 0
        assert len(self.resource.coding) == 3

    def test_index_updates_value(self):
        Index(2).update_values(
            self.collection, value=Coding(code="code-5", system="system-5")
        )
        assert len(self.resource.coding) == 3
        assert self.resource.coding[2] == Coding(code="code-5", system="system-5")

    def test_index_updates_and_creates_value(self):
        Index(10).update_values(
            self.collection, value=Coding(code="code-5", system="system-5")
        )
        assert len(self.resource.coding) == 11
        assert self.resource.coding[10] == Coding(code="code-5", system="system-5")

    def test_index_creates_with_empty_list(self):
        resource = CodeableConcept(coding=[])
        parent = FHIRPathCollectionItem(resource, path=This())
        collection = Element("coding").evaluate([parent], env, create=True)
        Index(0).evaluate(collection, env, create=True)
        assert len(resource.coding) == 1
        assert resource.coding == [Coding.model_construct()]


# -------------
# Single
# -------------


def test_single_returns_empty_for_empty_collection():
    collection = []
    result = Single().evaluate(collection, env, create=False)
    assert result == []


def test_single_returns_item_for_single_item_collection():
    collection = [FHIRPathCollectionItem(value="item1")]
    result = Single().evaluate(collection, env, create=False)
    assert result == collection


def test_single_raises_error_for_multiple_item_collection():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
    ]
    with pytest.raises(FHIRPathError):
        Single().evaluate(collection, env, create=False)

def test_single_string_representation():
    expression = Single()
    assert str(expression) == "single()"

# -------------
# First
# -------------


def test_first_returns_empty_for_empty_collection():
    collection = []
    result = First().evaluate(collection, env, create=False)
    assert result == []


def test_first_returns_first_item_in_collection():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = First().evaluate(collection, env, create=False)
    assert result == [collection[0]]

def test_first_string_representation():
    expression = First()
    assert str(expression) == "first()"

# -------------
# Last
# -------------


def test_last_returns_empty_for_empty_collection():
    collection = []
    result = Last().evaluate(collection, env, create=False)
    assert result == []


def test_last_returns_last_item_in_collection():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Last().evaluate(collection, env, create=False)
    assert result == [collection[-1]]

def test_last_string_representation():
    expression = Last()
    assert str(expression) == "last()"

# -------------
# Tail
# -------------


def test_tail_returns_empty_for_empty_collection():
    collection = []
    result = Tail().evaluate(collection, env, create=False)
    assert result == []


def test_tail_returns_expected_collection():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Tail().evaluate(collection, env, create=False)
    assert result == collection[1:]

def test_tail_string_representation():
    expression = Tail()
    assert str(expression) == "tail()"

# -------------
# Skip
# -------------


def test_skip_returns_empty_for_empty_collection():
    collection = []
    result = Skip(2).evaluate(collection, env, create=False)
    assert result == []


def test_skip_returns_original_if_num_is_zero_or_less():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Skip(-1).evaluate(collection, env, create=False)
    assert result == []
    result = Skip(0).evaluate(collection, env, create=False)
    assert result == []


def test_skip_returns_empty_if_num_larger_than_list():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Skip(5).evaluate(collection, env, create=False)
    assert result == []


def test_skip_returns_expected_collection():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Skip(2).evaluate(collection, env, create=False)
    assert result == [collection[-1]]

def test_skip_string_representation():
    expression = Skip(2)
    assert str(expression) == "skip(2)"

# -------------
# Take
# -------------


def test_take_returns_empty_for_empty_collection():
    collection = []
    result = Take(2).evaluate(collection, env, create=False)
    assert result == []


def test_take_returns_original_if_num_is_zero_or_less():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Take(-1).evaluate(collection, env, create=False)
    assert result == []
    result = Take(0).evaluate(collection, env, create=False)
    assert result == []


def test_take_returns_full_collection_if_num_larger():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Take(5).evaluate(collection, env, create=False)
    assert result == collection


def test_take_returns_expected_collection():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Take(2).evaluate(collection, env, create=False)
    assert result == collection[:2]

def test_take_string_representation():
    expression = Take(2)
    assert str(expression) == "take(2)"

# ---------------
# Intersection
# ---------------


def test_intersection_returns_common_items_without_duplicates():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    other_collection = [
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Intersect(other_collection).evaluate(collection, env, create=False)
    assert result == [
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]

def test_intersection_string_representation():
    expression = Intersect(Element("other"))
    assert str(expression) == "intersect(other)"

# ---------------
# Exclude
# ---------------


def test_exclude_returns_common_items_without_duplicates():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item3"),
    ]
    other_collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item3"),
    ]
    result = Exclude(other_collection).evaluate(collection, env, create=False)
    assert result == [
        FHIRPathCollectionItem(value="item2"),
        FHIRPathCollectionItem(value="item2"),
    ]
