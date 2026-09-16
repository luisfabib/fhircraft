"""Unit tests for ``fhircraft.fhir.path.collection"""

from __future__ import annotations

from typing import ClassVar, Optional

import pytest
from pydantic import BaseModel, ConfigDict, Field

from fhircraft.exceptions import FHIRPathEvaluationError
from fhircraft.fhir.path.accessors import ElementAccessor
from fhircraft.fhir.path.collection import FHIRPathCollectionItem

# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #


class HumanName(BaseModel):
    _type: ClassVar[str] = "HumanName"

    family: Optional[str] = None
    given: list[str] = Field(default_factory=list)


class ClosedPatient(BaseModel):
    _type: ClassVar[str] = "Patient"
    model_config = ConfigDict(extra="forbid")

    id: Optional[str] = None
    gender: Optional[str] = None
    birthDate: str = Field(...)
    name: list[HumanName] = Field(default_factory=list)
    telecom: list[str] = Field(default_factory=list)


class OpenPatient(BaseModel):
    """Accepts arbitrary extra fields -- exercises the extra='allow' path."""

    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None


def make_patient(**overrides) -> ClosedPatient:
    defaults = dict(id="p1", birthDate="1990-05-15")
    defaults.update(overrides)
    return ClosedPatient(**defaults)  # type: ignore


@pytest.fixture
def patient() -> ClosedPatient:
    return make_patient()


@pytest.fixture
def named_patient() -> ClosedPatient:
    return make_patient(
        name=[
            HumanName(family="Smith", given=["John"]),
            HumanName(family="Smith", given=["Johnny"]),
        ]
    )


@pytest.fixture
def open_patient() -> OpenPatient:
    return OpenPatient(id="p1")


# =========================================================================== #
# FHIRPathCollectionItem.wrap()
# =========================================================================== #


def test_wrap__wraps_plain_value_as_parentless_item():
    item = FHIRPathCollectionItem.wrap("hello")
    assert item.value == "hello"
    assert item.parent is None


def test_wrap__passes_through_existing_item_unchanged():
    original = FHIRPathCollectionItem.wrap("hello")
    assert FHIRPathCollectionItem.wrap(original) is original


# =========================================================================== #
# FHIRPathCollectionItem.wrap_all()
# =========================================================================== #


def test_wrap_all__wraps_scalar_value_as_single_item_list():
    items = FHIRPathCollectionItem.wrap_all("hello")
    assert [item.value for item in items] == ["hello"]


def test_wrap_all__wraps_list_value_as_one_item_per_element():
    items = FHIRPathCollectionItem.wrap_all(["a", "b"])
    assert [item.value for item in items] == ["a", "b"]


def test_wrap_all__returns_empty_list_for_none():
    assert FHIRPathCollectionItem.wrap_all(None) == []


# =========================================================================== #
# FHIRPathCollectionItem.child()
# =========================================================================== #


def test_child__creates_item_with_parent_set(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    child = root.child(patient.gender, "gender")
    assert child.parent is root


def test_child__creates_item_with_given_element_and_index(named_patient):
    root = FHIRPathCollectionItem.wrap(named_patient)
    child = root.child(named_patient.name[1], "name", index=1)
    assert child.element == "name"
    assert child.index == 1


def test_child__defaults_index_to_none_when_not_given(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    child = root.child(patient.gender, "gender")
    assert child.index is None


# =========================================================================== #
# FHIRPathCollectionItem.accessor
# =========================================================================== #


def test_accessor__returns_none_for_item_without_parent(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    assert root.accessor is None


def test_accessor__returns_accessor_for_navigated_item(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(patient.gender, "gender")
    assert isinstance(item.accessor, ElementAccessor)


def test_accessor__returns_none_when_field_unresolvable_on_closed_model(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(None, "nickname")
    assert item.accessor is None


def test_accessor__is_cached_after_first_access(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(patient.gender, "gender")
    first = item.accessor
    second = item.accessor
    assert first is second


# =========================================================================== #
# FHIRPathCollectionItem.is_writable
# =========================================================================== #


def test_is_writable__true_for_item_with_resolvable_accessor(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(patient.gender, "gender")
    assert item.is_writable is True


def test_is_writable__false_for_item_without_parent(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    assert root.is_writable is False


def test_is_writable__false_when_field_unresolvable(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(None, "nickname")
    assert item.is_writable is False


# =========================================================================== #
# FHIRPathCollectionItem.canonical_path
# =========================================================================== #


def test_canonical_path__returns_root_label_for_resource_root(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    assert root.canonical_path == "Patient"


def test_canonical_path__returns_scalar_element_path(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(patient.gender, "gender")
    assert item.canonical_path == "Patient.gender"


def test_canonical_path__returns_indexed_element_path_for_list_field(named_patient):
    root = FHIRPathCollectionItem.wrap(named_patient)
    item = root.child(named_patient.name[0], "name", index=0)
    assert item.canonical_path == "Patient.name[0]"


def test_canonical_path__nests_multiple_levels(named_patient):
    root = FHIRPathCollectionItem.wrap(named_patient)
    name_item = root.child(named_patient.name[0], "name", index=0)
    given_item = name_item.child(named_patient.name[0].given[0], "given", index=0)
    assert given_item.canonical_path == "Patient.name[0].given[0]"


def test_canonical_path__falls_back_to_bare_segment_when_parent_label_is_empty():
    # A dict with no 'resourceType' key has no root label, so the child's
    # path shouldn't carry a leading dot for a label that doesn't exist.
    root = FHIRPathCollectionItem.wrap({"gender": "female"})
    assert root.canonical_path == ""
    child = root.child("female", "gender")
    assert child.canonical_path == "gender"


# =========================================================================== #
# FHIRPathCollectionItem.root
# =========================================================================== #


def test_root__returns_self_for_item_without_parent(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    assert root.root is root


def test_root__returns_outermost_ancestor_for_nested_item(named_patient):
    root = FHIRPathCollectionItem.wrap(named_patient)
    name_item = root.child(named_patient.name[0], "name", index=0)
    given_item = name_item.child(named_patient.name[0].given[0], "given", index=0)
    assert given_item.root is root


# =========================================================================== #
# FHIRPathCollectionItem.ancestors
# =========================================================================== #


def test_ancestors__yields_parents_nearest_first(named_patient):
    root = FHIRPathCollectionItem.wrap(named_patient)
    name_item = root.child(named_patient.name[0], "name", index=0)
    given_item = name_item.child(named_patient.name[0].given[0], "given", index=0)
    chain = list(given_item.ancestors)
    assert len(chain) == 2
    assert chain[0] is name_item
    assert chain[1] is root


def test_ancestors__yields_nothing_for_root_item(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    assert list(root.ancestors) == []


# =========================================================================== #
# FHIRPathCollectionItem.depth
# =========================================================================== #


def test_depth__zero_for_root_item(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    assert root.depth == 0


def test_depth__counts_levels_for_nested_item(named_patient):
    root = FHIRPathCollectionItem.wrap(named_patient)
    name_item = root.child(named_patient.name[0], "name", index=0)
    given_item = name_item.child(named_patient.name[0].given[0], "given", index=0)
    assert given_item.depth == 2


# =========================================================================== #
# FHIRPathCollectionItem.has_element()
# =========================================================================== #


def test_has_element__true_for_declared_field(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    assert root.has_element("gender") is True


def test_has_element__false_for_unknown_field_on_closed_model(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    assert root.has_element("nickname") is False


def test_has_element__true_for_arbitrary_field_on_open_model(open_patient):
    root = FHIRPathCollectionItem.wrap(open_patient)
    assert root.has_element("nickname") is True


def test_has_element__checks_the_items_own_value_not_the_parents(named_patient):
    root = FHIRPathCollectionItem.wrap(named_patient)
    name_item = root.child(named_patient.name[0], "name", index=0)
    # 'family' belongs to HumanName (this item's own value); 'gender'
    # belongs to Patient (the parent's value), not to this item.
    assert name_item.has_element("family") is True
    assert name_item.has_element("gender") is False


# =========================================================================== #
# FHIRPathCollectionItem.set()
# =========================================================================== #


def test_set__updates_own_value_after_writing_through_accessor(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(patient.gender, "gender")
    item.set("male")
    assert item.value == "male"
    assert patient.gender == "male"


def test_set__raises_for_item_without_parent(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    with pytest.raises(FHIRPathEvaluationError):
        root.set("x")


def test_set__raises_when_field_unresolvable(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(None, "nickname")
    with pytest.raises(FHIRPathEvaluationError):
        item.set("Ally")


# =========================================================================== #
# FHIRPathCollectionItem.delete()
# =========================================================================== #


def test_delete__sets_own_value_to_none(named_patient):
    root = FHIRPathCollectionItem.wrap(named_patient)
    item = root.child(named_patient.name[0], "name", index=0)
    item.delete()
    assert item.value is None


def test_delete__removes_the_underlying_list_entry(named_patient):
    remaining = named_patient.name[1]
    root = FHIRPathCollectionItem.wrap(named_patient)
    item = root.child(named_patient.name[0], "name", index=0)
    item.delete()
    assert named_patient.name == [remaining]


def test_delete__raises_for_item_without_parent(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    with pytest.raises(FHIRPathEvaluationError):
        root.delete()


def test_delete__propagates_required_field_error_from_accessor(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(patient.birthDate, "birthDate")
    with pytest.raises(FHIRPathEvaluationError):
        item.delete()


# =========================================================================== #
# FHIRPathCollectionItem.insert()
# =========================================================================== #


def test_insert__delegates_to_accessor_and_updates_container(patient):
    patient.telecom = ["555-0123"]
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(patient.telecom, "telecom")
    item.insert("555-0456", at=1)
    assert patient.telecom == ["555-0123", "555-0456"]


def test_insert__raises_for_item_without_parent(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    with pytest.raises(FHIRPathEvaluationError):
        root.insert("x", at=0)


def test_insert__propagates_scalar_field_error_from_accessor(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(patient.gender, "gender")
    with pytest.raises(FHIRPathEvaluationError):
        item.insert("male", at=0)


# =========================================================================== #
# FHIRPathCollectionItem.move()
# =========================================================================== #


def test_move__reorders_the_underlying_list(patient):
    patient.name = [HumanName(family="A"), HumanName(family="B"), HumanName(family="C")]
    a, b, c = patient.name
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child(patient.name, "name")
    item.move(0, 2)
    assert patient.name == [b, c, a]


def test_move__raises_for_item_without_parent(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    with pytest.raises(FHIRPathEvaluationError):
        root.move(0, 1)


# =========================================================================== #
# FHIRPathCollectionItem.snapshot() / FHIRPathCollectionItem.restore()
# =========================================================================== #


def test_snapshot__returns_a_deep_copy_of_the_enclosing_field(named_patient):
    root = FHIRPathCollectionItem.wrap(named_patient)
    item = root.child(named_patient.name, "name")
    snapshot = item.snapshot()
    named_patient.name[0].family = "Changed"
    assert snapshot[0].family == "Smith"


def test_snapshot__raises_for_item_without_parent(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    with pytest.raises(FHIRPathEvaluationError):
        root.snapshot()


def test_restore__reverts_mutations_made_since_the_snapshot(named_patient):
    root = FHIRPathCollectionItem.wrap(named_patient)
    item = root.child(named_patient.name, "name")
    snapshot = item.snapshot()
    item.delete()
    item.restore(snapshot)
    assert [entry.family for entry in named_patient.name] == ["Smith", "Smith"]


def test_restore__raises_for_item_without_parent(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    with pytest.raises(FHIRPathEvaluationError):
        root.restore([])


# =========================================================================== #
# FHIRPathCollectionItem.__eq__
# =========================================================================== #


def test_eq__compares_equal_to_a_matching_bare_value():
    item = FHIRPathCollectionItem.wrap("hello")
    assert item == "hello"


def test_eq__compares_unequal_to_a_non_matching_bare_value():
    item = FHIRPathCollectionItem.wrap("hello")
    assert item != "world"


def test_eq__compares_two_items_by_value_element_and_index(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    a = root.child("female", "gender")
    b = root.child("female", "gender")
    assert a == b


def test_eq__items_with_the_same_value_but_different_element_are_unequal(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    a = root.child("x", "gender")
    b = root.child("x", "maritalStatus")
    assert a != b


def test_eq__items_with_the_same_value_but_different_index_are_unequal(named_patient):
    root = FHIRPathCollectionItem.wrap(named_patient)
    a = root.child(named_patient.name[0], "name", index=0)
    b = root.child(named_patient.name[0], "name", index=1)
    assert a != b


# =========================================================================== #
# FHIRPathCollectionItem.__hash__
# =========================================================================== #


def test_hash__equal_items_hash_equal(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    a = root.child("female", "gender")
    b = root.child("female", "gender")
    assert hash(a) == hash(b)


def test_hash__item_with_unhashable_value_does_not_raise():
    item = FHIRPathCollectionItem.wrap({"a": 1})
    hash(item)  # a dict value would normally break hash(); this must not raise


# =========================================================================== #
# FHIRPathCollectionItem.__repr__
# =========================================================================== #


def test_repr__includes_canonical_path_and_value(patient):
    root = FHIRPathCollectionItem.wrap(patient)
    item = root.child("female", "gender")
    text = repr(item)
    assert "Patient.gender" in text
    assert "female" in text
