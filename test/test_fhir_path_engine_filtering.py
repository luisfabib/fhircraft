from collections import namedtuple

import pytest

from fhircraft.fhir.path.engine.comparison import *
from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.filtering import *
from fhircraft.fhir.path.engine.literals import Date, Quantity

env = dict()

# -------------
# Where
# -------------


def test_where_returns_empty_for_empty_collection():
    collection = []
    result = Where(LessThan(This(), [FHIRPathCollectionItem.wrap(1)])).evaluate(
        collection, env
    )
    assert result == []


def test_where_returns_valid_items_in_collection_where_true():
    collection = [FHIRPathCollectionItem(value=4), FHIRPathCollectionItem(value=1)]
    result = Where(LessThan(This(), [FHIRPathCollectionItem.wrap(3)])).evaluate(
        collection, env
    )
    assert result == [collection[1]]


def test_where_string_representation():
    expression = Where(LessThan(Element("field"), Literal(3)))
    assert str(expression) == "where(field < 3)"


# -------------
# Select
# -------------


def test_select_returns_empty_for_empty_collection():
    collection = []
    result = Select(Invocation(This(), Element("field"))).evaluate(collection, env)
    assert result == []


def test_select_returns_collection_of_projected_elements():
    Resource = namedtuple("Resource", "field")
    collection = [
        FHIRPathCollectionItem(value=Resource(field=123)),
        FHIRPathCollectionItem(value=Resource(field=456)),
    ]
    result = Select(Invocation(This(), Element("field"))).evaluate(collection, env)
    assert result[0].value == 123
    assert result[1].value == 456


def test_select_string_representation():
    expression = Select(Invocation(Element("field"), Element("subfield")))
    assert str(expression) == "select(field.subfield)"


# -------------
# Repeat
# -------------


def test_repeat_returns_empty_for_empty_collection():
    collection = []
    result = Repeat(Invocation(This(), Element("field"))).evaluate(collection, env)
    assert result == []


def test_repeat_returns_collection_of_nested_repeating_elements():
    Resource = namedtuple("Resource", ("label", "items"))
    collection = [
        FHIRPathCollectionItem(
            value=Resource(
                label="1",
                items=[
                    Resource(label="1.1", items=[]),
                    Resource(label="1.2", items=[Resource(label="1.2.1", items=[])]),
                    Resource(label="1.3", items=[Resource(label="1.3.1", items=[])]),
                ],
            )
        )
    ]
    result = Repeat(Invocation(This(), Element("items"))).evaluate(collection, env)
    assert [item.value.label for item in result] == [
        "1.1",
        "1.2",
        "1.3",
        "1.2.1",
        "1.3.1",
    ]


def test_repeat_string_representation():
    expression = Repeat(Invocation(Element("field"), Element("subfield")))
    assert str(expression) == "repeat(field.subfield)"


# -------------
# ofType
# -------------

ofType_cases = (
    ("ABC", "String"),
    (12, "Integer"),
    (12, "UnsignedInt"),
    (12, "PositiveInt"),
    (Date("@2024"), "Date"),
    (Quantity(12, "g"), "Quantity"),
)


@pytest.mark.parametrize("expected, type", ofType_cases)
def test_ofType_returns_filtered_collection_by_type(expected, type):
    collection = [
        FHIRPathCollectionItem(value="ABC"),
        FHIRPathCollectionItem(value=12),
        FHIRPathCollectionItem(value=Date("@2024")),
        FHIRPathCollectionItem(value=Quantity(12, "g")),
    ]
    result = OfType(type).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=expected)]


def test_ofType_returns_empty_for_empty_collection():
    collection = []
    result = OfType("String").evaluate(collection, env)
    assert result == []


def test_ofType_string_representation():
    expression = OfType("Patient")
    assert str(expression) == "ofType(Patient)"
