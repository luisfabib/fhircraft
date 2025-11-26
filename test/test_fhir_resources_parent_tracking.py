"""
Unit tests for parent tracking functionality in FHIRBaseModel.

Tests the implementation of _parent and _root_resource tracking across
all construction patterns and edge cases identified in the analysis.
"""

from __future__ import annotations
from copy import deepcopy
from typing import Optional, Union

from fhircraft.fhir.resources.base import FHIRBaseModel, FHIRList


class MockPatient(FHIRBaseModel):
    """Minimal Patient model for testing."""

    resourceType: str = "Patient"
    id: Optional[str] = None
    name: Optional[str] = None
    contained: Optional[list[Union[MockPractitioner, MockObservation]]] = None


class MockPractitioner(FHIRBaseModel):
    """Minimal Practitioner model for testing."""

    resourceType: str = "Practitioner"
    id: Optional[str] = None
    name: Optional[str] = None


class MockObservation(FHIRBaseModel):
    """Minimal Observation model for testing."""

    resourceType: str = "Observation"
    id: Optional[str] = None
    subject: Optional[MockReference] = None
    performer: Optional[list[MockReference]] = None


class MockReference(FHIRBaseModel):
    """Minimal Reference model for testing."""

    reference: Optional[str] = None


class TestParentTracking:
    """Test parent tracking implementation."""

    def test_direct_instantiation(self):
        """Test parent tracking with direct instantiation."""
        patient = MockPatient(
            id="p1",
            name="John",
            contained=[MockPractitioner(id="pract1", name="Dr. Smith")],
        )

        # Root has no parent
        assert patient._parent is None
        assert patient._root_resource is patient

        # Contained resource has parent
        assert patient.contained
        practitioner = patient.contained[0]
        assert practitioner._parent is patient
        assert practitioner._root_resource is patient

    def test_model_validate_dict(self):
        """Test parent tracking with model_validate(dict)."""
        data = {
            "id": "p1",
            "name": "John",
            "contained": [{"id": "pract1", "name": "Dr. Smith"}],
        }
        patient = MockPatient.model_validate(data)

        assert patient._parent is None
        assert patient._root_resource is patient

        assert patient.contained
        practitioner = patient.contained[0]
        assert practitioner._parent is patient
        assert practitioner._root_resource is patient

    def test_model_validate_json(self):
        """Test parent tracking with model_validate_json."""
        json_str = '{"id": "p1", "name": "John", "contained": [{"id": "pract1", "name": "Dr. Smith"}]}'
        patient = MockPatient.model_validate_json(json_str)

        assert patient._parent is None
        assert patient._root_resource is patient

        assert patient.contained
        practitioner = patient.contained[0]
        assert practitioner._parent is patient
        assert practitioner._root_resource is patient

    def test_model_construct(self):
        """Test parent tracking with model_construct."""
        patient = MockPatient.model_construct(
            id="p1",
            name="John",
            contained=[MockPractitioner.model_construct(id="pract1", name="Dr. Smith")],
        )

        assert patient._parent is None
        assert patient._root_resource is patient

        assert patient.contained
        practitioner = patient.contained[0]
        assert practitioner._parent is patient
        assert practitioner._root_resource is patient

    def test_incremental_field_assignment(self):
        """Test parent tracking with incremental field assignment (CRITICAL fix)."""
        patient = MockPatient(id="p1", name="John")

        # Assign contained field after construction
        patient.contained = [MockPractitioner(id="pract1", name="Dr. Smith")]

        # Context should be propagated via __setattr__
        practitioner = patient.contained[0]
        assert (
            practitioner._parent is patient
        ), "Context LOST after incremental assignment!"
        assert practitioner._root_resource is patient

    def test_list_mutation_append(self):
        """Test parent tracking with list.append() (CRITICAL fix)."""
        patient = MockPatient(
            id="p1",
            name="John",
            contained=[MockPractitioner(id="pract1", name="Dr. Smith")],
        )

        # Verify FHIRList is being used
        assert isinstance(patient.contained, FHIRList)

        # Append new practitioner
        new_pract = MockPractitioner(id="pract2", name="Dr. Jones")
        patient.contained.append(new_pract)

        # Original item should still have context
        assert patient.contained[0]._parent is patient
        assert patient.contained[0]._root_resource is patient

        # Newly appended item should have context
        assert (
            patient.contained[1]._parent is patient
        ), "Context LOST after list.append()!"
        assert patient.contained[1]._root_resource is patient

    def test_list_mutation_extend(self):
        """Test parent tracking with list.extend()."""
        patient = MockPatient(
            id="p1", name="John", contained=[MockPractitioner(id="pract1")]
        )

        # Extend with multiple practitioners
        new_practs = [MockPractitioner(id="pract2"), MockPractitioner(id="pract3")]
        assert patient.contained
        patient.contained.extend(new_practs)

        # All items should have context
        assert patient.contained
        for pract in patient.contained:
            assert pract._parent is patient
            assert pract._root_resource is patient

    def test_list_mutation_insert(self):
        """Test parent tracking with list.insert()."""
        patient = MockPatient(
            id="p1",
            name="John",
            contained=[MockPractitioner(id="pract1"), MockPractitioner(id="pract3")],
        )
        assert patient.contained
        # Insert in the middle
        new_pract = MockPractitioner(id="pract2")
        patient.contained.insert(1, new_pract)

        # Inserted item should have context
        assert patient.contained[1]._parent is patient
        assert patient.contained[1]._root_resource is patient
        assert patient.contained[1].id == "pract2"

    def test_model_copy(self):
        """Test parent tracking with model_copy()."""
        original = MockPatient(
            id="p1", name="John", contained=[MockPractitioner(id="pract1")]
        )

        # Copy the patient
        copied = original.model_copy()

        # Copied instance should have its own context (not point to original)
        assert copied._parent is None
        assert copied._root_resource is copied, "Copied instance has stale reference!"

        # Nested items should point to copied instance
        assert copied.contained
        assert copied.contained[0]._parent is copied
        assert copied.contained[0]._root_resource is copied

    def test_deepcopy(self):
        """Test parent tracking with deepcopy()."""
        original = MockPatient(
            id="p1", name="John", contained=[MockPractitioner(id="pract1")]
        )

        # Deep copy the patient
        cloned = deepcopy(original)

        # Cloned instance should have its own context
        assert cloned._parent is None
        assert cloned._root_resource is cloned

        # Nested items should point to cloned instance
        assert cloned.contained and original.contained
        assert cloned.contained[0]._parent is cloned
        assert cloned.contained[0]._root_resource is cloned

        # Verify it's truly a deep copy (not sharing data)
        assert cloned.contained[0] is not original.contained[0]

    def test_serialization_roundtrip(self):
        """Test parent tracking after serialization roundtrip."""
        original = MockPatient(
            id="p1", name="John", contained=[MockPractitioner(id="pract1")]
        )

        # Serialize to dict and back
        data = original.model_dump()
        restored = MockPatient.model_validate(data)

        # Context should be re-established
        assert restored._parent is None
        assert restored._root_resource is restored
        assert restored.contained
        assert restored.contained[0]._parent is restored
        assert restored.contained[0]._root_resource is restored

    def test_deeply_nested_resources(self):
        """Test parent tracking with deeply nested resources."""
        # Create a patient with a nested observation-like structure
        # (using Practitioner since Patient.contained only accepts Practitioner)
        inner_pract = MockPractitioner(id="pract1", name="Dr. Smith")

        patient = MockPatient(id="patient1", name="John", contained=[inner_pract])

        # Verify context chain
        assert patient._parent is None
        assert patient._root_resource is patient

        # Practitioner is contained in patient
        assert patient.contained
        pract = patient.contained[0]
        assert pract._parent is patient
        assert pract._root_resource is patient

        # Test with a model that has nested structure
        observation = MockObservation(
            id="obs1", subject=MockReference(reference="#patient1")
        )

        # Verify nested reference tracking
        assert observation._parent is None
        assert observation._root_resource is observation

        ref = observation.subject
        assert ref
        assert ref._parent is observation
        assert ref._root_resource is observation  # Root is observation, not patient

    def test_context_preserved_across_field_access(self):
        """Test that context is preserved when accessing fields."""
        patient = MockPatient(
            id="p1", name="John", contained=[MockPractitioner(id="pract1")]
        )

        # Access contained multiple times
        assert patient.contained
        pract1 = patient.contained[0]
        pract2 = patient.contained[0]

        # Both references should have context
        assert pract1._parent is patient
        assert pract1._root_resource is patient
        assert pract2._parent is patient
        assert pract2._root_resource is patient

    def test_empty_list_handling(self):
        """Test that empty lists are handled correctly."""
        patient = MockPatient(id="p1", name="John", contained=[])

        # Empty list should be FHIRList
        assert isinstance(patient.contained, FHIRList)

        # Adding items should work
        patient.contained.append(MockPractitioner(id="pract1"))
        assert patient.contained[0]._parent is patient
        assert patient.contained[0]._root_resource is patient

    def test_none_list_handling(self):
        """Test that None lists are handled correctly."""
        patient = MockPatient(id="p1", name="John")

        # contained is None initially
        assert patient.contained is None

        # Setting to a list should work
        patient.contained = [MockPractitioner(id="pract1")]

        # Should be converted to FHIRList with context
        assert isinstance(patient.contained, FHIRList)
        assert patient.contained[0]._parent is patient
        assert patient.contained[0]._root_resource is patient

    def test_single_nested_model(self):
        """Test parent tracking with single nested model (not a list)."""
        observation = MockObservation(
            id="obs1", subject=MockReference(reference="#patient1")
        )

        # Single nested model should have context
        assert observation._parent is None
        assert observation._root_resource is observation

        ref = observation.subject
        assert ref
        assert ref._parent is observation
        assert ref._root_resource is observation

    def test_updating_single_nested_model(self):
        """Test updating a single nested model field."""
        observation = MockObservation(id="obs1")

        # Add reference after construction
        observation.subject = MockReference(reference="#patient1")

        # Context should be propagated
        assert observation.subject._parent is observation
        assert observation.subject._root_resource is observation

    def test_fhir_list_context_update(self):
        """Test that FHIRList updates context when parent changes."""
        patient1 = MockPatient(id="p1", contained=[MockPractitioner(id="pract1")])
        patient2 = MockPatient(id="p2")

        # Move contained list from patient1 to patient2
        patient2.contained = patient1.contained

        # Context should update to patient2
        assert patient2.contained
        assert patient2.contained[0]._parent is patient2
        assert patient2.contained[0]._root_resource is patient2


class TestFHIRListBehavior:
    """Test FHIRList specific behavior."""

    def test_fhir_list_initialization(self):
        """Test FHIRList initialization."""
        parent = MockPatient(id="p1")
        items = [MockPractitioner(id="pract1"), MockPractitioner(id="pract2")]

        fhir_list = FHIRList(items, parent=parent, root=parent)

        # All items should have context
        for item in fhir_list:
            assert item._parent is parent
            assert item._root_resource is parent

    def test_fhir_list_behaves_like_list(self):
        """Test that FHIRList behaves like a regular list."""
        fhir_list = FHIRList([MockPractitioner(id="pract1")])

        # Should support standard list operations
        assert len(fhir_list) == 1
        assert fhir_list[0].id == "pract1"

        # Iteration
        for item in fhir_list:
            assert isinstance(item, MockPractitioner)

        # Slicing
        subset = fhir_list[0:1]
        assert len(subset) == 1

    def test_fhir_list_setitem(self):
        """Test FHIRList __setitem__ for context propagation."""
        parent = MockPatient(id="p1")
        fhir_list = FHIRList(
            [MockPractitioner(id="pract1")], parent=parent, root=parent
        )

        # Replace item
        new_pract = MockPractitioner(id="pract2")
        fhir_list[0] = new_pract

        # New item should have context
        assert fhir_list[0]._parent is parent
        assert fhir_list[0]._root_resource is parent
        assert fhir_list[0].id == "pract2"


class TestResourceAndIndexTracking:
    """Test _resource and _index tracking implementation."""

    def test_resource_tracking_on_resource_types(self):
        """Test that _resource points to self for resource types."""
        patient = MockPatient(id="p1", name="John")

        # Patient is a resource type, so _resource should point to itself
        assert hasattr(patient, "resourceType")
        assert patient._resource is patient
        assert patient._root_resource is patient

    def test_resource_tracking_on_nested_non_resource(self):
        """Test that _resource inherits from parent for non-resource types."""
        patient = MockPatient(
            id="p1",
            contained=[
                MockObservation(
                    id="obs1", subject=MockReference(reference="Patient/p1")
                )
            ],
        )

        # Observation is a resource, so its _resource should be itself
        assert patient.contained
        observation = patient.contained[0]
        assert isinstance(observation, MockObservation)
        assert observation._resource is observation
        assert observation._root_resource is patient

        # Reference is NOT a resource, so its _resource should be Observation
        reference = observation.subject
        assert reference
        assert not hasattr(reference, "resourceType")
        assert reference._resource is observation  # Points to containing Observation
        assert reference._root_resource is patient  # Root is still Patient

    def test_resource_vs_parent_distinction(self):
        """Test distinction between _parent (immediate parent) and _resource (containing resource)."""
        patient = MockPatient(
            id="p1",
            contained=[
                MockObservation(
                    id="obs1", subject=MockReference(reference="Patient/p1")
                )
            ],
        )

        assert patient.contained
        observation = patient.contained[0]
        assert isinstance(observation, MockObservation)
        reference = observation.subject
        assert reference

        # Reference's _parent is the Observation (immediate parent)
        assert reference._parent is observation

        # Reference's _resource is also Observation (containing resource)
        assert reference._resource is observation

        # But Observation's _parent is Patient
        assert observation._parent is patient

        # And Observation's _resource is itself (it's a resource type)
        assert observation._resource is observation

    def test_index_tracking_in_lists(self):
        """Test that _index is correctly set for items in lists."""
        patient = MockPatient(
            id="p1",
            contained=[
                MockObservation(id="obs1"),
                MockObservation(id="obs2"),
                MockObservation(id="obs3"),
            ],
        )

        # Check indices
        assert patient.contained
        assert patient.contained[0]._index == 0
        assert patient.contained[1]._index == 1
        assert patient.contained[2]._index == 2

    def test_index_tracking_on_append(self):
        """Test that _index is set correctly when appending to list."""
        patient = MockPatient(id="p1", contained=[])

        obs1 = MockObservation(id="obs1")
        assert patient.contained is not None
        patient.contained.append(obs1)
        assert obs1._index == 0

        obs2 = MockObservation(id="obs2")
        assert patient.contained
        patient.contained.append(obs2)
        assert obs2._index == 1

    def test_index_tracking_on_insert(self):
        """Test that _index is updated correctly when inserting into list."""
        patient = MockPatient(
            id="p1",
            contained=[
                MockObservation(id="obs1"),
                MockObservation(id="obs3"),
            ],
        )

        # Insert in the middle
        obs2 = MockObservation(id="obs2")
        assert patient.contained
        patient.contained.insert(1, obs2)

        # Check all indices are correct
        assert patient.contained
        assert patient.contained[0]._index == 0
        assert patient.contained[1]._index == 1
        assert patient.contained[2]._index == 2

    def test_index_tracking_on_extend(self):
        """Test that _index is set correctly when extending list."""
        patient = MockPatient(id="p1", contained=[MockObservation(id="obs1")])

        new_obs = [MockObservation(id="obs2"), MockObservation(id="obs3")]
        assert patient.contained
        patient.contained.extend(new_obs)

        assert patient.contained[0]._index == 0
        assert patient.contained[1]._index == 1
        assert patient.contained[2]._index == 2

    def test_index_none_for_non_list_items(self):
        """Test that _index is None for items not in lists."""
        patient = MockPatient(id="p1")

        # Patient itself is not in a list
        assert patient._index is None

    def test_contained_scenario(self):
        """Test the Patient.contained.select(Observation).subject scenario."""
        # Create a Patient with contained Observations
        patient = MockPatient(
            id="p1",
            contained=[
                MockObservation(
                    id="obs1",
                    subject=MockReference(reference="Patient/p1"),
                    performer=[MockReference(reference="Practitioner/pract1")],
                ),
                MockObservation(
                    id="obs2",
                    subject=MockReference(reference="Patient/p1"),
                ),
            ],
        )

        # Get first observation
        assert patient.contained
        obs1 = patient.contained[0]

        # Observation should have:
        # - _root_resource = Patient
        # - _resource = Observation (itself, since it has resourceType)
        # - _parent = Patient
        assert obs1._root_resource is patient
        assert obs1._resource is obs1
        assert obs1._parent is patient

        # Get subject reference from observation
        assert isinstance(obs1, MockObservation)
        subject_ref = obs1.subject

        # Subject reference should have:
        # - _root_resource = Patient (top-level resource)
        # - _resource = Observation (containing resource)
        # - _parent = Observation (immediate parent)
        assert subject_ref
        assert subject_ref._root_resource is patient
        assert subject_ref._resource is obs1
        assert subject_ref._parent is obs1

        # Get performer reference
        assert obs1.performer
        performer_ref = obs1.performer[0]

        # Performer reference should also track correctly
        assert performer_ref._root_resource is patient
        assert performer_ref._resource is obs1
        assert performer_ref._parent is obs1
        assert performer_ref._index == 0  # It's in a list
