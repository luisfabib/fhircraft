from fhircraft.fhir.path.collection import FHIRPathCollection
from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, Element
from fhircraft.fhir.path.engine.combining import *
from dataclasses import dataclass


@dataclass
class ComplexItem:
    id: str
    value: str

    def __hash__(self):
        return hash((self.id, self.value))


env = dict()

# -------------
# Union
# -------------


def test_union_returns_combined_collection_without_duplicates():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item1"),
    ]
    other_collection = [FHIRPathCollectionItem(value="item2")]
    result = Union(FHIRPathCollection(other_collection)).evaluate(
        FHIRPathCollection(collection), env
    )
    assert set(result) == {
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
    }


def test_union_returns_combined_collection_with_complex_items():
    collection = [FHIRPathCollectionItem(value=ComplexItem(id="item1", value="value1"))]
    other_collection = [
        FHIRPathCollectionItem(value=ComplexItem(id="item2", value="value2"))
    ]
    result = Union(FHIRPathCollection(other_collection)).evaluate(
        FHIRPathCollection(collection), env
    )
    assert sorted(result, key=lambda item: item.id) == [
        ComplexItem(id="item1", value="value1"),
        ComplexItem(id="item2", value="value2"),
    ]


def test_union_string_representation():
    expression = Union(Element("other"))
    assert str(expression) == "union(other)"


# -------------
# Combine
# -------------


def test_combine_returns_combined_collection_with_duplicates():
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item1"),
    ]
    other_collection = [FHIRPathCollectionItem(value="item2")]
    result = Combine(FHIRPathCollection(other_collection)).evaluate(
        FHIRPathCollection(collection), env
    )
    assert set(result) == {
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
    }


def test_combine_returns_combined_collection_with_complex_items():
    collection = [FHIRPathCollectionItem(value=ComplexItem(id="item1", value="value1"))]
    other_collection = [
        FHIRPathCollectionItem(value=ComplexItem(id="item2", value="value2"))
    ]
    result = Combine(FHIRPathCollection(other_collection)).evaluate(
        FHIRPathCollection(collection), env
    )
    assert result == [
        ComplexItem(id="item1", value="value1"),
        ComplexItem(id="item2", value="value2"),
    ]


def test_combine_string_representation():
    expression = Combine(Element("other"))
    assert str(expression) == "combine(other)"
