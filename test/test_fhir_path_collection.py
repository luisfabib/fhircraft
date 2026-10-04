"""Unit tests for ``fhircraft.fhir.path.collection"""

from __future__ import annotations

from typing import ClassVar, Optional

import pytest
from pydantic import BaseModel, ConfigDict, Field

from fhircraft.exceptions import FHIRPathEvaluationError
from fhircraft.fhir.path.collection import (
    FHIRPathCollection,
    FHIRPathCollectionItem,
)
from fhircraft.fhir.path.engine.core import Element
from fhircraft.fhir.path.engine.subsetting import Index

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


ENV = {"%fhirRelease": "R5"}


def select(resource, *names) -> FHIRPathCollection:
    collection = FHIRPathCollection([FHIRPathCollectionItem(resource)])
    for name in names:
        collection = Element(name).evaluate(collection, ENV)
    return collection


# =========================================================================== #
# FHIRPathCollectionItem
# =========================================================================== #


def test_wrap__wraps_plain_value_as_accessorless_item():
    item = FHIRPathCollectionItem.wrap("hello")
    assert item.value == "hello"
    assert item.accessor is None


def test_wrap__passes_through_existing_item_unchanged():
    original = FHIRPathCollectionItem.wrap("hello")
    assert FHIRPathCollectionItem.wrap(original) is original


def test_wrap_all__scalar_list_and_none():
    assert [i.value for i in FHIRPathCollectionItem.wrap_all("a")] == ["a"]
    assert [i.value for i in FHIRPathCollectionItem.wrap_all(["a", "b"])] == ["a", "b"]
    assert FHIRPathCollectionItem.wrap_all(None) == []


def test_canonical_path__uses_accessor(named_patient):
    (item,) = select(named_patient, "name")[1:2]
    assert item.canonical_path.endswith("name[1]")


def test_canonical_path__nests_multiple_levels(named_patient):
    item = select(named_patient, "name", "family")[0]
    assert item.canonical_path.endswith("name[0].family")


def test_has_element__declared_unknown_and_open(patient, open_patient):
    assert FHIRPathCollectionItem(patient).has_element("gender")
    assert not FHIRPathCollectionItem(patient).has_element("bogus")
    assert FHIRPathCollectionItem(open_patient).has_element("anything")


def test_eq__compares_by_value():
    assert FHIRPathCollectionItem("a") == "a"
    assert FHIRPathCollectionItem("a") == FHIRPathCollectionItem("a")
    assert FHIRPathCollectionItem("a") != FHIRPathCollectionItem("b")


def test_hash__unhashable_value_does_not_raise():
    hash(FHIRPathCollectionItem({"a": 1}))


def test_repr__includes_value(patient):
    assert "p1" in repr(select(patient, "id")[0])


# =========================================================================== #
# FHIRPathCollection: targets
# =========================================================================== #


def test_targets__follow_items(named_patient):
    result = select(named_patient, "name")
    assert len(result.targets) == 1
    assert len(result.accessors) == 2


def test_targets__survive_empty_result(patient):
    result = select(patient, "gender")
    assert len(result) == 0
    assert len(result.targets) == 1


def test_targets__none_for_literals():
    collection = FHIRPathCollection([FHIRPathCollectionItem("a")])
    assert collection.targets == ()


def test_slice__returns_collection(named_patient):
    result = select(named_patient, "name")[1:]
    assert isinstance(result, FHIRPathCollection)
    assert result.targets[0].index == 1


def test_slicing_keeps_accessors(named_patient):
    tail = select(named_patient, "name")[1:]
    assert tail[0].accessor.index == 1


# =========================================================================== #
# FHIRPathCollection: patch API
# =========================================================================== #


def test_set__scalar_on_existing(patient):
    select(patient, "gender").set("female")
    assert patient.gender == "female"


def test_set__on_missing_value_through_empty_collection(patient):
    result = select(patient, "gender")
    assert patient.gender is None
    result.set("male")
    assert patient.gender == "male"


def test_set__materialises_missing_parents(patient):
    select(patient, "name", "family").set("Doe")
    assert patient.name[0].family == "Doe"


def test_set__on_dict_materialises_nested_path():
    data: dict = {}
    select(data, "name", "family").set("Doe")
    assert data == {"name": {"family": "Doe"}} or data == {"name": [{"family": "Doe"}]}


def test_set__raises_without_targets():
    with pytest.raises(FHIRPathEvaluationError):
        FHIRPathCollection([FHIRPathCollectionItem("a")]).set("b")


def test_add__appends_to_list_field(named_patient):
    select(named_patient, "telecom").add("555")
    assert named_patient.telecom == ["555"]
    select(named_patient, "telecom").add("556")
    assert named_patient.telecom == ["555", "556"]


def test_add__assigns_scalar_field(patient):
    select(patient, "gender").add("male")
    assert patient.gender == "male"


def test_insert__at_position(patient):
    patient.telecom = ["a", "c"]
    select(patient, "telecom").insert("b", 1)
    assert patient.telecom == ["a", "b", "c"]


def test_insert__raises_for_scalar_field(patient):
    with pytest.raises(FHIRPathEvaluationError):
        select(patient, "gender").insert("x", 0)


def test_delete__removes_selected_list_entries(named_patient):
    select(named_patient, "name")[1:].delete()
    assert len(named_patient.name) == 1


def test_delete__removes_all_in_reverse_safely(named_patient):
    select(named_patient, "name").delete()
    assert not named_patient.name


def test_delete__raises_without_targets():
    with pytest.raises(FHIRPathEvaluationError):
        FHIRPathCollection().delete()


def test_delete__raises_for_required_field(patient):
    with pytest.raises(FHIRPathEvaluationError):
        select(patient, "birthDate").delete()


def test_move__reorders_list(patient):
    patient.telecom = ["a", "b", "c"]
    select(patient, "telecom").move(0, 2)
    assert patient.telecom == ["b", "c", "a"]


def test_snapshot_restore__reverts_changes(named_patient):
    result = select(named_patient, "name")
    snap = result.snapshot()
    result.delete()
    assert not named_patient.name
    result.restore(snap)
    assert [n.family for n in named_patient.name] == ["Smith", "Smith"]


# =========================================================================== #
# Virtual accessors / Index
# =========================================================================== #


def test_virtual__deep_path_on_empty_resource(patient):
    result = select(patient, "name", "given")
    assert len(result) == 0
    assert patient.name == []
    result.add("John")
    assert patient.name[0].given == ["John"]


def test_index__out_of_range_has_target_and_no_mutation(patient):
    result = Index(1).evaluate(select(patient, "telecom"), ENV)
    assert len(result) == 0
    assert len(result.targets) == 1
    assert patient.telecom == []
    result.set("x")
    assert patient.telecom[-1] == "x" or "x" in patient.telecom
