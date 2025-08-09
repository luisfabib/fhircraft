from unittest import TestCase

import pytest

from fhircraft.fhir.path.engine.core import (
    Element,
    FHIRPathCollectionItem,
    Invocation,
    Literal,
    Parent,
    Root,
    This,
)
from fhircraft.fhir.path.engine.strings import Upper


class TestRoot(TestCase):

    def test_evaluate_returns_collection_unchanged(self):
        # Root().evaluate should return the collection unchanged
        items = [
            FHIRPathCollectionItem(value="a"),
            FHIRPathCollectionItem(value="b"),
            FHIRPathCollectionItem(value="c"),
        ]
        result = Root().evaluate(items)
        assert result == items
        assert all(isinstance(item, FHIRPathCollectionItem) for item in result)

    def test_evaluate_empty_collection_returns_empty_list(self):
        # Root().evaluate([]) should return []
        result = Root().evaluate([])
        assert result == []

    def test_evaluate_with_single_item(self):
        item = FHIRPathCollectionItem(value="single")
        result = Root().evaluate([item])
        assert result == [item]


class TestParent(TestCase):
    class DummyValue:
        pass

    def _make_item_with_parent(self, parent_value=None):
        parent_item = FHIRPathCollectionItem(value=parent_value or self.DummyValue())
        child_item = FHIRPathCollectionItem(value=self.DummyValue(), parent=parent_item)
        return child_item, parent_item

    def test_evaluate_returns_parents_when_present(self):
        child1, parent1 = self._make_item_with_parent()
        child2, parent2 = self._make_item_with_parent()
        collection = [child1, child2]
        result = Parent().evaluate(collection)
        assert result == [parent1, parent2]
        assert all(isinstance(item, FHIRPathCollectionItem) for item in result)

    def test_evaluate_skips_items_without_parent(self):
        item_without_parent = FHIRPathCollectionItem(value=self.DummyValue())
        child, parent = self._make_item_with_parent()
        collection = [item_without_parent, child]
        result = Parent().evaluate(collection)
        assert result == [parent]
        assert parent in result
        assert item_without_parent not in result

    def test_evaluate_empty_collection_returns_empty_list(self):
        result = Parent().evaluate([])
        assert result == []

    def test_evaluate_all_items_without_parent_returns_empty_list(self):
        items = [FHIRPathCollectionItem(value=self.DummyValue()) for _ in range(3)]
        result = Parent().evaluate(items)
        assert result == []


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
        result = This().evaluate(self.items)
        assert result == self.items
        assert all(isinstance(item, FHIRPathCollectionItem) for item in result)

    def test_evaluate_empty_collection_returns_empty_list(self):
        result = This().evaluate([])
        assert result == []

    def test_evaluate_with_single_item(self):
        item = FHIRPathCollectionItem(value=self.value1)
        result = This().evaluate([item])
        assert result == [item]

    def test_evaluate_with_none_value(self):
        item = FHIRPathCollectionItem(value=None)
        result = This().evaluate([item])
        assert result == [item]
        assert result[0].value is None


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
        self.collection = [FHIRPathCollectionItem(self.resource, path=Root())]

    def test_evaluate_returns_field_value(self):
        # Should return the value of the field as a FHIRPathCollectionItem
        result = Element("status").evaluate(self.collection, create=False)
        assert len(result) == 1
        assert result[0].value == "active"

    def test_evaluate_returns_empty_when_field_missing_and_create_false(self):
        # Should return empty list if field does not exist and create is False
        result = Element("missingField").evaluate(self.collection, create=False)
        assert result == []

    def test_evaluate_creates_missing_primitive_field(self):
        # Should create the field if missing and create is True
        class Dummy:
            pass

        dummy = Dummy()
        collection = [FHIRPathCollectionItem(dummy, path=Root())]
        result = Element("newField").evaluate(collection, create=True)
        assert len(result) == 1
        assert hasattr(dummy, "newField")
        assert getattr(dummy, "newField") is None

    def test_evaluate_handles_list_fields(self):
        # Should return all items in a list field as FHIRPathCollectionItems
        result = Element("identifier").evaluate(self.collection, create=False)
        assert len(result) == 2
        assert result[0].value.value == "id1"
        assert result[1].value.value == "id2"

    def test_evaluate_with_empty_collection(self):
        # Should return empty list if input collection is empty
        result = Element("status").evaluate([], create=False)
        assert result == []

    def test_evaluate_with_multiple_items(self):
        # Should evaluate each item in the input collection
        class Dummy:
            def __init__(self, val):
                self.status = val

        items = [FHIRPathCollectionItem(Dummy("a")), FHIRPathCollectionItem(Dummy("b"))]
        result = Element("status").evaluate(items, create=False)
        assert [item.value for item in result] == ["a", "b"]

    def test_evaluate_returns_parent_link(self):
        # Should set parent on returned FHIRPathCollectionItem
        result = Element("status").evaluate(self.collection, create=False)
        assert result[0].parent == self.collection[0]


class TestInvocation(TestCase):

    def setUp(self):
        class DummyResource:
            def __init__(self):
                self.status = "active"

        self.resource = DummyResource()
        self.collection = [FHIRPathCollectionItem(self.resource, path=Root())]

    def test_evaluate_invokes_method_on_each_item(self):
        result = Invocation(Element("status"), Upper()).evaluate(self.collection)
        assert result[0].value == "ACTIVE"

    def test_evaluate_empty_collection_returns_empty_list(self):
        result = Invocation(Element("status"), Upper()).evaluate([])
        assert result == []


class TestLiteral(TestCase):

    class TestLiteral(TestCase):

        def test_evaluate_returns_literal_value_for_each_item(self):
            # Should return a FHIRPathCollectionItem with the literal value for each input item
            items = [
                FHIRPathCollectionItem(value="a"),
                FHIRPathCollectionItem(value="b"),
            ]
            literal = Literal(42)
            result = literal.evaluate(items)
            assert len(result) == 2
            assert all(item.value == 42 for item in result)
            assert all(isinstance(item, FHIRPathCollectionItem) for item in result)

        def test_evaluate_with_empty_collection_returns_empty_list(self):
            literal = Literal("test")
            result = literal.evaluate([])
            assert result == []

        def test_evaluate_with_single_item(self):
            item = FHIRPathCollectionItem(value="x")
            literal = Literal(True)
            result = literal.evaluate([item])
            assert len(result) == 1
            assert result[0].value is True

        def test_evaluate_returns_parent_link(self):
            # Should set parent on returned FHIRPathCollectionItem
            item = FHIRPathCollectionItem(value="x")
            literal = Literal("foo")
            result = literal.evaluate([item])
            assert result[0].parent == item

        def test_evaluate_with_none_literal(self):
            items = [FHIRPathCollectionItem(value="a")]
            literal = Literal(None)
            result = literal.evaluate(items)
            assert len(result) == 1
            assert result[0].value is None


"""
Test file demonstrating the improved FHIRPath interface.

This file shows examples of using the enhanced public interface methods
for common FHIRPath operations.
"""

from dataclasses import dataclass
from typing import List, Optional
from unittest import TestCase

import pytest

from fhircraft.fhir.path.engine.core import Element, Invocation, This
from fhircraft.fhir.path.exceptions import FHIRPathRuntimeError


@dataclass
class MockPatient:
    """Mock FHIR Patient resource for testing."""

    name: Optional[List[dict]] = None
    gender: Optional[str] = None
    birthDate: Optional[str] = None
    telecom: Optional[List[dict]] = None


class TestImprovedFHIRPathInterface(TestCase):
    """Test cases demonstrating the improved FHIRPath interface."""

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

    def test_set_value_modifies_all_matches(self):
        """Test set_value() modifies all matching locations."""
        # This test would require a more complete implementation
        # with proper setter functionality
        pass

    def test_set_single_value_modifies_single_match(self):
        """Test set_single_value() modifies exactly one matching location."""
        # This test would require a more complete implementation
        # with proper setter functionality
        pass
