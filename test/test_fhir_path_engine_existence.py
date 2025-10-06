
from fhircraft.fhir.path.engine.comparison import *
from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.existence import *

env = dict()

# -------------
# Empty
# -------------


def test_empty_returns_true_for_empty_collection():
    collection = []
    result = Empty().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_empty_returns_false_for_non_empty_collection():
    collection = [FHIRPathCollectionItem(value="item1")]
    result = Empty().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]

def test_empty_string_representation():
    expression = Empty()
    assert str(expression) == "empty()"

# -------------
# Exists
# -------------


def test_exists_returns_false_for_empty_collection():
    collection = []
    result = Exists().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_exists_returns_true_for_non_empty_collection():
    collection = [
        FHIRPathCollectionItem(value=[FHIRPathCollectionItem.wrap(1)]),
        FHIRPathCollectionItem(value=2),
    ]
    result = Exists().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_exists_applies_criteria_correctly_and_returns_true_if_filtered_collection_has_elements():
    criteria = Where(GreaterThan(This(), [FHIRPathCollectionItem.wrap(1)]))
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = Exists(criteria).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_exists_applies_criteria_correctly_and_returns_false_if_filtered_collection_is_empty():
    criteria = Where(GreaterThan(This(), [FHIRPathCollectionItem.wrap(9999)]))
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = Exists(criteria).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_exists_string_representation():
    expression = Exists()
    assert str(expression) == "exists()"

# -------------
# All
# -------------


def test_all_returns_true_for_empty_collection():
    collection = []
    result = All([FHIRPathCollectionItem.wrap(None)]).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_all_returns_true_for_criteria_applying_to_all():
    criteria = GreaterThan(This(), [FHIRPathCollectionItem.wrap(1)])
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = All(criteria).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_all_returns_false_for_criteria_not_applying_to_all():
    criteria = GreaterThan(This(), [FHIRPathCollectionItem.wrap(0)])
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = All(criteria).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_all_string_representation():
    expression = All(Element("criteria"))
    assert str(expression) == "all(criteria)"


# -------------
# AllTrue
# -------------


def test_allTrue_returns_true_for_empty_collection():
    collection = []
    result = AllTrue().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_allTrue_returns_true_if_all_items_are_true():
    collection = [
        FHIRPathCollectionItem(value=True),
        FHIRPathCollectionItem(value=True),
    ]
    result = AllTrue().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_allTrue_returns_false_if_any_item_is_false():
    collection = [
        FHIRPathCollectionItem(value=True),
        FHIRPathCollectionItem(value=False),
    ]
    result = AllTrue().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_alltrue_string_representation():
    expression = AllTrue()
    assert str(expression) == "allTrue()"

# -------------
# AnyTrue
# -------------


def test_anyTrue_returns_false_for_empty_collection():
    collection = []
    result = AnyTrue().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_anyTrue_returns_false_if_all_items_are_false():
    collection = [
        FHIRPathCollectionItem(value=False),
        FHIRPathCollectionItem(value=False),
    ]
    result = AnyTrue().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_anyTrue_returns_true_if_any_item_is_true():
    collection = [
        FHIRPathCollectionItem(value=True),
        FHIRPathCollectionItem(value=False),
    ]
    result = AnyTrue().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_anytrue_string_representation():
    expression = AnyTrue()
    assert str(expression) == "anyTrue()"

# -------------
# AllFalse
# -------------


def test_allFalse_returns_true_for_empty_collection():
    collection = []
    result = AllFalse().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_allFalse_returns_true_if_all_items_are_false():
    collection = [
        FHIRPathCollectionItem(value=False),
        FHIRPathCollectionItem(value=False),
    ]
    result = AllFalse().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_allFalse_returns_false_if_any_item_is_true():
    collection = [
        FHIRPathCollectionItem(value=True),
        FHIRPathCollectionItem(value=False),
    ]
    result = AllFalse().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_allfalse_string_representation():
    expression = AllFalse()
    assert str(expression) == "allFalse()"

# -------------
# AnyFalse
# -------------


def test_anyFalse_returns_false_for_empty_collection():
    collection = []
    result = AnyFalse().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_anyFalse_returns_false_if_all_items_are_true():
    collection = [
        FHIRPathCollectionItem(value=True),
        FHIRPathCollectionItem(value=True),
    ]
    result = AnyFalse().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_anyFalse_returns_true_if_any_item_is_false():
    collection = [
        FHIRPathCollectionItem(value=True),
        FHIRPathCollectionItem(value=False),
    ]
    result = AnyFalse().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_anyfalse_string_representation():
    expression = AnyFalse()
    assert str(expression) == "anyFalse()"

# -------------
# Count
# -------------


def test_count_empty_collection():
    collection = []
    result = Count().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(0)]


def test_count_nonempty_collection():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = Count().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(2)]


def test_count_string_representation():
    expression = Count()
    assert str(expression) == "count()"


# -------------
# SubsetOf
# -------------


def test_subsetOf_returns_false_when_other_collection_is_empty():
    other_collection = []
    collection = [FHIRPathCollectionItem(value=1)]
    result = SubsetOf(other=other_collection).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_subsetOf_returns_true_when_all_items_in_input_collection_are_in_other_collection():
    other_collection = [
        FHIRPathCollectionItem(value=1),
        FHIRPathCollectionItem(value=2),
    ]
    collection = [FHIRPathCollectionItem(value=1)]
    result = SubsetOf(other=other_collection).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_subsetOf_returns_false_when_not_all_items_in_input_collection_are_in_other_collection():
    other_collection = [
        FHIRPathCollectionItem(value=1),
        FHIRPathCollectionItem(value=2),
    ]
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=3)]
    result = SubsetOf(other=other_collection).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_subsetof_string_representation():
    expression = SubsetOf(Element('other'))
    assert str(expression) == "subsetOf(other)"

# -------------
# SupersetOf
# -------------


def test_supersetOf_returns_false_when_other_collection_is_empty():
    other_collection = []
    collection = [FHIRPathCollectionItem(value=1)]
    result = SupersetOf(other=other_collection).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_supersetOf_returns_true_when_all_items_in_other_collection_are_in_ipnut_collection():
    other_collection = [FHIRPathCollectionItem(value=1)]
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = SupersetOf(other=other_collection).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_supersetOf_returns_false_when_not_all_items_in_other_collection_are_in_input_collection():
    other_collection = [
        FHIRPathCollectionItem(value=1),
        FHIRPathCollectionItem(value=2),
    ]
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=3)]
    result = SupersetOf(other=other_collection).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_supersetof_string_representation():
    expression = SupersetOf(Element('other'))
    assert str(expression) == "supersetOf(other)"

# -------------
# Distinct
# -------------


def test_disctinct_empty_collection():
    collection = []
    result = Distinct().evaluate(collection, env)
    assert result == []


def test_disctinct_no_repeatition():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = Distinct().evaluate(collection, env)
    assert sorted(result, key=lambda item: item.value) == sorted(
        collection, key=lambda item: item.value
    )


def test_disctinct_with_repeatition():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    new_collection = collection + collection
    result = Distinct().evaluate(new_collection, env)
    assert sorted(result, key=lambda item: item.value) == sorted(
        collection, key=lambda item: item.value
    )


def test_distinct_string_representation():
    expression = Distinct()
    assert str(expression) == "distinct()"

# -------------
# IsDistinct
# -------------


def test_isDisctinct_empty_collection():
    collection = []
    result = IsDistinct().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_isDisctinct_no_repeatition():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = IsDistinct().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_isDisctinct_with_repetition():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    new_collection = collection + collection
    result = IsDistinct().evaluate(new_collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_isdistinct_string_representation():
    expression = IsDistinct()
    assert str(expression) == "isDistinct()"