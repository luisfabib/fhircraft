from unittest import TestCase

import pytest

from fhircraft.fhir.path.engine.core import (
    Element,
    FHIRPathCollectionItem,
    Invocation,
    Literal,
    FHIRPathError,
    This,
)
from fhircraft.fhir.path.engine.strings import Upper

from fhircraft.fhir.resources.datatypes.R4.resources.patient import Patient

from dataclasses import dataclass
from typing import List, Optional
from unittest import TestCase

import pytest

from fhircraft.fhir.path.engine.core import Element, Invocation, RootElement
from fhircraft.fhir.path.exceptions import FHIRPathRuntimeError

env = dict()

class TestRoot(TestCase):

    def test_evaluate_returns_collection_unchanged(self):
        # Root().evaluate should return the collection unchanged
        items = [
            FHIRPathCollectionItem(value=MockPatient()),
            FHIRPathCollectionItem(value=MockPatient()),
            FHIRPathCollectionItem(value=MockPatient()),
        ]
        result = RootElement('Patient').evaluate(items, env)
        assert result == items
        assert all(isinstance(item, FHIRPathCollectionItem) for item in result)

    def test_evaluate_empty_collection_returns_empty_list(self):
        # Root().evaluate([]) should return []
        result = RootElement('Patient').evaluate([], env)
        assert result == []

    def test_raises_error_for_wrong_type(self):
        item = FHIRPathCollectionItem(value=MockPatient())
        with pytest.raises(FHIRPathError):
            RootElement('Condition').evaluate([item], env)


    def test_root_string_representation(self):
        expression = RootElement('Patient')
        assert str(expression) == "Patient"


# class TestParent(TestCase):
#     class DummyValue:
#         pass

#     def _make_item_with_parent(self, parent_value=None):
#         parent_item = FHIRPathCollectionItem(value=parent_value or self.DummyValue())
#         child_item = FHIRPathCollectionItem(value=self.DummyValue(), parent=parent_item)
#         return child_item, parent_item

#     def test_evaluate_returns_parents_when_present(self):
#         child1, parent1 = self._make_item_with_parent()
#         child2, parent2 = self._make_item_with_parent()
#         collection = [child1, child2]
#         result = Parent().evaluate(collection, env)
#         assert result == [parent1, parent2]
#         assert all(isinstance(item, FHIRPathCollectionItem) for item in result)

#     def test_evaluate_skips_items_without_parent(self):
#         item_without_parent = FHIRPathCollectionItem(value=self.DummyValue())
#         child, parent = self._make_item_with_parent()
#         collection = [item_without_parent, child]
#         result = Parent().evaluate(collection, env)
#         assert result == [parent]
#         assert parent in result
#         assert item_without_parent not in result

#     def test_evaluate_empty_collection_returns_empty_list(self):
#         result = Parent().evaluate([], env)
#         assert result == []

#     def test_evaluate_all_items_without_parent_returns_empty_list(self):
#         items = [FHIRPathCollectionItem(value=self.DummyValue()) for _ in range(3)]
#         result = Parent().evaluate(items, env)
#         assert result == []

#     def test_parent_string_representation(self):
#         expression = Parent()
#         assert str(expression) == "$"


class TestThis(TestCase):
    class DummyValue:
        pass

    def setUp(self):
        self.value1 = self.DummyValue()
        self.value2 = self.DummyValue()
        self.items = [
            FHIRPathCollectionItem(value=self.value1),
            FHIRPathCollectionItem(value=self.value2),
        ]

    def test_evaluate_returns_same_collection(self):
        # This().evaluate should return the collection unchanged
        result = This().evaluate(self.items, env)
        assert result == self.items
        assert all(isinstance(item, FHIRPathCollectionItem) for item in result)

    def test_evaluate_empty_collection_returns_empty_list(self):
        result = This().evaluate([], env)
        assert result == []

    def test_evaluate_with_single_item(self):
        item = FHIRPathCollectionItem(value=self.value1)
        result = This().evaluate([item], env)
        assert result == [item]

    def test_evaluate_with_none_value(self):
        item = FHIRPathCollectionItem(value=None)
        result = This().evaluate([item], env)
        assert result == [item]
        assert result[0].value is None

    def test_this_string_representation(self):
        expression = This()
        assert str(expression) == ""

class TestElement(TestCase):

    def setUp(self):
        class DummyResource:
            def __init__(self):
                self.status = "active"
                self.valueString = None
                self.identifier = [
                    type("Identifier", (), {"value": "id1"})(),
                    type("Identifier", (), {"value": "id2"})(),
                ]

        self.resource = DummyResource()
        self.collection = [FHIRPathCollectionItem(self.resource, path=This())]

    def test_element_string_representation(self):
        expression = Element("elementName")
        assert str(expression) == "elementName"

    def test_evaluate_returns_field_value(self):
        # Should return the value of the field as a FHIRPathCollectionItem
        result = Element("status").evaluate(self.collection, env, create=False)
        assert len(result) == 1
        assert result[0].value == "active"

    def test_evaluate_returns_empty_when_field_missing_and_create_false(self):
        # Should return empty list if field does not exist and create is False
        result = Element("missingField").evaluate(self.collection, env, create=False)
        assert result == []

    def test_evaluate_creates_missing_primitive_field(self):
        # Should create the field if missing and create is True
        class Dummy:
            pass

        dummy = Dummy()
        collection = [FHIRPathCollectionItem(dummy, path=This())]
        result = Element("newField").evaluate(collection, env, create=True)
        assert len(result) == 1
        assert hasattr(dummy, "newField")
        assert getattr(dummy, "newField") is None

    def test_evaluate_handles_list_fields(self):
        # Should return all items in a list field as FHIRPathCollectionItems
        result = Element("identifier").evaluate(self.collection, env, create=False)
        assert len(result) == 2
        assert result[0].value.value == "id1"
        assert result[1].value.value == "id2"

    def test_evaluate_with_empty_collection(self):
        # Should return empty list if input collection is empty
        result = Element("status").evaluate([], env, create=False)
        assert result == []

    def test_evaluate_with_multiple_items(self):
        # Should evaluate each item in the input collection
        class Dummy:
            def __init__(self, val):
                self.status = val

        items = [FHIRPathCollectionItem(Dummy("a")), FHIRPathCollectionItem(Dummy("b"))]
        result = Element("status").evaluate(items, env, create=False)
        assert [item.value for item in result] == ["a", "b"]

    def test_evaluate_returns_parent_link(self):
        # Should set parent on returned FHIRPathCollectionItem
        result = Element("status").evaluate(self.collection, env, create=False)
        assert result[0].parent == self.collection[0]

def test_children_returns_correct_primitive_extension():
    ext = dict(extension=[dict(url="http://example.com/ext", value="Extension Value")])
    resource = dict(fieldA=1, fieldB_ext=ext)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Element('fieldB').evaluate(collection, env)
    assert result[0].value == ext

class TestInvocation(TestCase):

    def setUp(self):
        class DummyResource:
            def __init__(self):
                self.status = "active"

        self.resource = DummyResource()
        self.collection = [FHIRPathCollectionItem(self.resource, path=This())]

    def test_evaluate_invokes_method_on_each_item(self):
        result = Invocation(Element("status"), Upper()).evaluate(self.collection, env)
        assert result[0].value == "ACTIVE"

    def test_evaluate_empty_collection_returns_empty_list(self):
        result = Invocation(Element("status"), Upper()).evaluate([], env)
        assert result == []
    
    def test_invocation_string_representation(self):
        expression = Invocation(Element("left"), Element("right"))
        assert str(expression) == "left.right"


class TestLiteral(TestCase):
    
    def test_evaluate_returns_single_value_for_multiple_collection_items(self):
        items = [
            FHIRPathCollectionItem(value="a"),
            FHIRPathCollectionItem(value="b"),
        ]
        literal = Literal(42)
        result = literal.evaluate(items, env)
        assert len(result) == 1
        assert all(item.value == 42 for item in result)

    def test_evaluate_with_empty_collection_returns_nonempty_list(self):
        literal = Literal("test")
        result = literal.evaluate([], env)
        assert result == [FHIRPathCollectionItem(value="test")]

    def test_evaluate_with_single_item(self):
        item = FHIRPathCollectionItem(value="x")
        literal = Literal(True)
        result = literal.evaluate([item], env)
        assert len(result) == 1
        assert result[0].value is True

    def test_evaluate_with_none_literal(self):
        items = [FHIRPathCollectionItem(value="a")]
        literal = Literal(None)
        result = literal.evaluate(items, env)
        assert len(result) == 1
        assert result[0].value is None
    
    def test_literal_string_representation(self):
        assert str(Literal("foo")) == "\'foo\'"
        assert str(Literal(120)) == "120"
        assert str(Literal(True)) == "true"


@dataclass
class MockPatient:
    """Mock FHIR Patient resource for testing."""

    resourceType: str = "Patient"
    name: Optional[List[dict]] = None
    gender: Optional[str] = None
    birthDate: Optional[str] = None
    telecom: Optional[List[dict]] = None


class TestPublicFHIRPathInterface(TestCase):

    def setUp(self):
        """Set up test data."""
        self.patient = MockPatient(
            name=[
                {"family": "Doe", "given": ["John"]},
                {"family": "Smith", "given": ["Jane"]},
            ],
            gender="male",
            birthDate="1990-01-01",
            telecom=[
                {"system": "phone", "value": "555-1234"},
                {"system": "email", "value": "john@example.com"},
            ],
        )

        self.empty_patient = MockPatient()

    def test_get_values_returns_all_matches(self):
        """Test get_values() returns all matching values as a list."""
        # Test multiple values
        path = Element("name")
        values = path.values(self.patient)

        self.assertIsInstance(values, list)
        self.assertEqual(len(values), 2)
        self.assertEqual(values[0]["family"], "Doe")
        self.assertEqual(values[1]["family"], "Smith")

    def test_get_values_returns_empty_list_for_no_matches(self):
        """Test get_values() returns empty list when no matches found."""
        path = Element("nonexistent")
        values = path.values(self.patient)

        self.assertIsInstance(values, list)
        self.assertEqual(len(values), 0)

    def test_get_single_returns_single_match(self):
        """Test single() returns single value when exactly one match."""
        path = Element("gender")
        value = path.single(self.patient)

        self.assertEqual(value, "male")

    def test_get_single_returns_default_for_no_matches(self):
        """Test single() returns default when no matches."""
        path = Element("gender")
        value = path.single(self.empty_patient, default="unknown")

        self.assertEqual(value, "unknown")

    def test_get_single_raises_error_for_multiple_matches(self):
        """Test single() raises error when multiple matches found."""
        path = Element("name")

        with self.assertRaises(FHIRPathRuntimeError) as context:
            path.single(self.patient)

        self.assertIn(
            "Expected single value but found 2 values", str(context.exception)
        )

    def test_first_returns_first_match(self):
        """Test first() returns the first matching value."""
        path = Element("name")
        value = path.first(self.patient)

        self.assertEqual(value["family"], "Doe")

    def test_first_returns_default_for_no_matches(self):
        """Test first() returns default when no matches."""
        path = Element("name")
        value = path.first(self.empty_patient, default={"family": "Unknown"})

        self.assertEqual(value["family"], "Unknown")

    def test_last_returns_last_match(self):
        """Test last() returns the last matching value."""
        path = Element("name")
        value = path.last(self.patient)

        self.assertEqual(value["family"], "Smith")

    def test_last_returns_default_for_no_matches(self):
        """Test last() returns default when no matches."""
        path = Element("name")
        value = path.last(self.empty_patient, default={"family": "Unknown"})

        self.assertEqual(value["family"], "Unknown")

    def test_exists_returns_true_when_matches_found(self):
        """Test exists() returns True when matches are found."""
        path = Element("gender")

        self.assertTrue(path.exists(self.patient))

    def test_exists_returns_false_when_no_matches(self):
        """Test exists() returns False when no matches found."""
        path = Element("gender")

        self.assertFalse(path.exists(self.empty_patient))

    def test_count_returns_correct_number_of_matches(self):
        """Test count() returns the correct number of matches."""
        # Multiple matches
        path = Element("name")
        self.assertEqual(path.count(self.patient), 2)

        # Single match
        path = Element("gender")
        self.assertEqual(path.count(self.patient), 1)

        # No matches
        path = Element("nonexistent")
        self.assertEqual(path.count(self.patient), 0)

    def test_is_empty_returns_correct_boolean(self):
        """Test is_empty() returns the correct boolean value."""
        # Has matches
        path = Element("gender")
        self.assertFalse(path.is_empty(self.patient))

        # No matches
        path = Element("gender")
        self.assertTrue(path.is_empty(self.empty_patient))