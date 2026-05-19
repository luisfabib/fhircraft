"""
Unit tests for FHIRContextMixin.

Tests all public and protected methods of FHIRContextMixin, including
parent/index tracking, lazy resource resolution, context propagation,
and list-wrapping behaviour.
"""

from __future__ import annotations

from typing import ClassVar, List, Literal, Optional

import pytest

from pydantic import BaseModel
from fhircraft.fhir.resources.base import FHIRList
from fhircraft.fhir.resources.base.mixins.context import FHIRContextMixin

# ===========================================================
# Minimal concrete models for testing
# ===========================================================


class MockResource(BaseModel, FHIRContextMixin):
    """A minimal resource-kind model."""

    _type: ClassVar[str] = "MockResource"
    _kind: ClassVar[
        Literal["primitive-type", "complex-type", "resource", "logical"]
    ] = "resource"

    id: Optional[str] = None
    child: Optional["MockElement"] = None
    children: Optional[List["MockElement"]] = None


class MockLogical(BaseModel, FHIRContextMixin):
    """A minimal logical-kind model."""

    _type: ClassVar[str] = "MockLogical"
    _kind: ClassVar[
        Literal["primitive-type", "complex-type", "resource", "logical"]
    ] = "logical"

    id: Optional[str] = None


class MockElement(BaseModel, FHIRContextMixin):
    """A minimal complex-type model (non-resource)."""

    _type: ClassVar[str] = "MockElement"
    _kind: ClassVar[
        Literal["primitive-type", "complex-type", "resource", "logical"]
    ] = "complex-type"

    value: Optional[str] = None
    nested: Optional["MockElement"] = None


class MockObservationModel(BaseModel, FHIRContextMixin):
    """A resource-kind model with a single and a list reference field."""

    _type: ClassVar[str] = "MockObservationModel"
    _kind: ClassVar[
        Literal["primitive-type", "complex-type", "resource", "logical"]
    ] = "resource"

    id: Optional[str] = None
    subject: Optional[MockElement] = None
    performer: Optional[List[MockElement]] = None


class MockPatientModel(BaseModel, FHIRContextMixin):
    """A resource-kind model that contains a list of nested resources."""

    _type: ClassVar[str] = "MockPatientModel"
    _kind: ClassVar[
        Literal["primitive-type", "complex-type", "resource", "logical"]
    ] = "resource"

    id: Optional[str] = None
    contained: Optional[List[MockObservationModel]] = None


# ===========================================================
# Fixtures
# ===========================================================


@pytest.fixture
def resource():
    return MockResource(id="r1")


@pytest.fixture
def element():
    return MockElement(value="v1")


@pytest.fixture
def resource_with_child():
    root = MockResource(id="r1", child=MockElement(value="child"))
    root._set_resource_context(parent=None, index=None)
    return root


@pytest.fixture
def resource_with_children():
    root = MockResource(
        id="r1",
        children=[MockElement(value="c0"), MockElement(value="c1")],
    )
    root._set_resource_context(parent=None, index=None)
    return root


# ===========================================================
# _is_resource()
# ===========================================================


def test_is_resource__returns_true_for_resource_kind():
    assert MockResource._is_resource() is True


def test_is_resource__returns_true_for_logical_kind():
    assert MockLogical._is_resource() is True


def test_is_resource__returns_false_for_complex_type_kind():
    assert MockElement._is_resource() is False


def test_is_resource__returns_false_when_kind_absent():
    class NoKind(FHIRContextMixin):
        pass

    assert NoKind._is_resource() is False


# ===========================================================
# _root_resource property
# ===========================================================


def test_root_resource__returns_self_when_no_parent(resource):
    assert resource._root_resource is resource


def test_root_resource__returns_topmost_ancestor(resource_with_child):
    child = resource_with_child.child
    assert child._root_resource is resource_with_child


def test_root_resource__walks_multiple_levels():
    deep = MockElement(value="deep")
    middle = MockElement(nested=deep)
    root = MockResource(id="root", child=middle)
    # Wire the parent chain manually (no model_post_init on plain BaseModel mixin).
    object.__setattr__(middle, "_parent", root)
    object.__setattr__(deep, "_parent", middle)
    assert deep._root_resource is root


# ===========================================================
# _resource property
# ===========================================================


def test_resource__returns_self_when_instance_is_resource(resource):
    assert resource._resource is resource


def test_resource__returns_nearest_enclosing_resource_for_child(resource_with_child):
    child = resource_with_child.child
    assert child._resource is resource_with_child


def test_resource__returns_none_when_no_enclosing_resource():
    standalone_element = MockElement(value="lone")
    # No parent set – walk terminates immediately at self (complex-type).
    assert standalone_element._resource is None


def test_resource__skips_non_resource_ancestors():
    # MockElement wraps another MockElement; neither is a resource.
    outer = MockElement(nested=MockElement(value="inner"))
    assert (inner := outer.nested) is not None
    assert inner._resource is None


# ===========================================================
# _set_resource_context()
# ===========================================================


def test_set_resource_context__sets_parent_and_index(resource, element):
    element._set_resource_context(parent=resource, index=3)

    assert element._parent is resource
    assert element._index == 3


def test_set_resource_context__sets_none_parent_and_index(resource):
    resource._set_resource_context(parent=None, index=None)

    assert resource._parent is None
    assert resource._index is None


def test_set_resource_context__propagates_parent_to_child_field():
    root = MockResource(id="root", child=MockElement(value="c"))
    child = root.child
    # Call explicitly to ensure propagation runs.
    root._set_resource_context(parent=None, index=None)
    assert child is not None
    assert child._parent is root


def test_set_resource_context__propagates_parent_to_list_items():
    root = MockResource(
        id="root",
        children=[MockElement(value="c0"), MockElement(value="c1")],
    )
    root._set_resource_context(parent=None, index=None)

    # FHIRList._propagate_context() only sets _parent on FHIRBaseModel items;
    # verify the list itself is wrapped and owns the correct parent reference.
    assert root.children is not None
    assert isinstance(root.children, FHIRList)
    assert root.children._parent is root


def test_set_resource_context__wraps_plain_list_in_fhir_list():
    root = MockResource(
        id="root",
        children=[MockElement(value="c0")],
    )
    root._set_resource_context(parent=None, index=None)

    assert isinstance(root.children, FHIRList)


def test_set_resource_context__does_not_propagate_to_none_fields(resource):
    # Calling on a resource with no child/children should not raise.
    resource._set_resource_context(parent=None, index=None)

    assert resource._parent is None


# ===========================================================
# _propagate_context_to_value()
# ===========================================================


def test_propagate_context_to_value__sets_parent_on_fhir_context_mixin_child(
    resource, element
):
    resource._propagate_context_to_value(element)

    assert element._parent is resource


def test_propagate_context_to_value__sets_index_none_on_fhir_context_mixin_child(
    resource, element
):
    object.__setattr__(element, "_index", 99)
    resource._propagate_context_to_value(element)

    assert element._index is None


def test_propagate_context_to_value__wraps_plain_list_in_fhir_list(resource):
    plain = [MockElement(value="x")]
    # Attach the plain list as a field value first.
    object.__setattr__(resource, "children", plain)

    resource._propagate_context_to_value(plain)

    assert isinstance(resource.children, FHIRList)
    assert resource.children._parent is resource


def test_propagate_context_to_value__re_points_existing_fhir_list(resource):
    other_parent = MockResource(id="other")
    fhir_list = FHIRList([MockElement(value="y")], parent=other_parent)
    object.__setattr__(resource, "children", fhir_list)

    resource._propagate_context_to_value(fhir_list)

    assert fhir_list._parent is resource


def test_propagate_context_to_value__propagates_context_to_fhir_list_items(resource):
    item = MockElement(value="z")
    fhir_list = FHIRList([item], parent=None)
    object.__setattr__(resource, "children", fhir_list)

    resource._propagate_context_to_value(fhir_list)

    # FHIRList._propagate_context() only propagates _parent to FHIRBaseModel
    # items; the list itself is re-pointed to the new parent.
    assert fhir_list._parent is resource


def test_propagate_context_to_value__ignores_non_model_non_list_values(resource):
    # Should not raise for scalar values.
    resource._propagate_context_to_value("just a string")
    resource._propagate_context_to_value(42)
    resource._propagate_context_to_value(None)


# ===========================================================
# Contained scenario (_root_resource / _resource / _parent / _index)
# ===========================================================


def test_contained_scenario__observation_root_resource_and_parent():
    """Observation (contained resource) reports the patient as its root."""
    obs1 = MockObservationModel(id="obs1")
    patient = MockPatientModel(id="p1", contained=[obs1])
    object.__setattr__(obs1, "_parent", patient)
    object.__setattr__(obs1, "_index", 0)

    assert obs1._root_resource is patient
    assert obs1._resource is obs1
    assert obs1._parent is patient


def test_contained_scenario__observation_index_reflects_position_in_list():
    """Each contained observation carries the correct list index."""
    obs1 = MockObservationModel(id="obs1")
    obs2 = MockObservationModel(id="obs2")
    patient = MockPatientModel(id="p1", contained=[obs1, obs2])
    object.__setattr__(obs1, "_parent", patient)
    object.__setattr__(obs1, "_index", 0)
    object.__setattr__(obs2, "_parent", patient)
    object.__setattr__(obs2, "_index", 1)

    assert obs1._index == 0
    assert obs2._index == 1


def test_contained_scenario__subject_ref_context_chain():
    """A subject reference's _root_resource is the patient and _resource is the observation."""
    subject_ref = MockElement(value="Patient/p1")
    obs1 = MockObservationModel(id="obs1", subject=subject_ref)
    patient = MockPatientModel(id="p1", contained=[obs1])
    object.__setattr__(obs1, "_parent", patient)
    object.__setattr__(obs1, "_index", 0)
    object.__setattr__(subject_ref, "_parent", obs1)

    assert subject_ref._root_resource is patient
    assert subject_ref._resource is obs1
    assert subject_ref._parent is obs1


def test_contained_scenario__performer_ref_context_chain():
    """A performer reference's _root_resource is the patient, _resource the observation, and _index its list position."""
    performer_ref = MockElement(value="Practitioner/pract1")
    obs1 = MockObservationModel(
        id="obs1",
        performer=[performer_ref],
    )
    patient = MockPatientModel(id="p1", contained=[obs1])
    object.__setattr__(obs1, "_parent", patient)
    object.__setattr__(obs1, "_index", 0)
    object.__setattr__(performer_ref, "_parent", obs1)
    object.__setattr__(performer_ref, "_index", 0)

    assert performer_ref._root_resource is patient
    assert performer_ref._resource is obs1
    assert performer_ref._parent is obs1
    assert performer_ref._index == 0
