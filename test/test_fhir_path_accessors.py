"""Unit tests for ``fhircraft.fhir.path.accessors``"""

from __future__ import annotations

from types import MappingProxyType
from typing import ClassVar, Optional

import pytest
from pydantic import BaseModel, ConfigDict, Field

from fhircraft.exceptions import FHIRPathEvaluationError
from fhircraft.fhir.path.accessors import (
    Cardinality,
    DictAccessor,
    ElementAccessor,
    ModelAccessor,
    resolve_field,
)
from fhircraft.fhir.path.collection import FHIRPathCollectionItem

# --------------------------------------------------------------------------- #
# Domain fixtures
# --------------------------------------------------------------------------- #


class HumanName(BaseModel):
    _type: ClassVar[str] = "HumanName"

    family: Optional[str] = None
    given: list[str] = Field(default_factory=list)


class MockPatient(BaseModel):
    _type: ClassVar[str] = "Patient"
    model_config = ConfigDict(extra="forbid")

    id: Optional[str] = None
    gender: Optional[str] = None
    birthDate: str = Field(...)
    name: list[HumanName] = Field(default_factory=list, max_length=3)
    telecom: list[str] = Field(default_factory=list)
    note: Optional[list[str]] = None
    class_: Optional[str] = None
    value_ext: Optional[dict] = None
    resource_type: Optional[str] = Field(default=None, alias="resourceType")


class PlainObject:
    def __init__(self) -> None:
        self.value = "hello"


def make_patient(**overrides) -> MockPatient:
    defaults = dict(id="p1", birthDate="1990-05-15")
    defaults.update(overrides)
    return MockPatient(**defaults)  # type: ignore


@pytest.fixture
def patient() -> MockPatient:
    return make_patient()


@pytest.fixture
def named_patient() -> MockPatient:
    return make_patient(
        name=[
            HumanName(family="Smith", given=["John"]),
            HumanName(family="Smith", given=["Johnny"]),
        ]
    )


@pytest.fixture
def plain_object() -> PlainObject:
    return PlainObject()


def accessor_for(item: FHIRPathCollectionItem) -> ElementAccessor:
    result = ElementAccessor.for_item(item)
    assert result is not None, f"expected an accessor for {item!r}"
    return result


# =========================================================================== #
# resolve_field()
# =========================================================================== #


def test_resolve_field__returns_none_for_none_container():
    assert resolve_field(None, "gender") is None


def test_resolve_field__matches_direct_key_in_mapping():
    assert resolve_field({"gender": "female"}, "gender") == "gender"


def test_resolve_field__matches_underscore_suffixed_key_in_mapping():
    assert resolve_field({"value_": "x"}, "value") == "value_"


def test_resolve_field__matches_ext_suffixed_key_in_mapping():
    assert resolve_field({"value_ext": {"extension": []}}, "value") == "value_ext"


def test_resolve_field__falls_back_to_element_name_for_absent_mapping_key():
    # Mappings are open containers: an absent key is still a writable location.
    assert resolve_field({}, "nickname") == "nickname"


def test_resolve_field__matches_direct_field_on_model(patient):
    assert resolve_field(patient, "gender") == "gender"


def test_resolve_field__matches_underscore_suffixed_field_on_model(patient):
    assert resolve_field(patient, "class") == "class_"


def test_resolve_field__matches_ext_suffixed_field_on_model(patient):
    assert resolve_field(patient, "value") == "value_ext"


def test_resolve_field__matches_alias_on_model(patient):
    assert resolve_field(patient, "resourceType") == "resource_type"


def test_resolve_field__returns_none_for_unknown_field_on_closed_model(patient):
    assert resolve_field(patient, "nickname") is None


def test_resolve_field__returns_attribute_name_for_plain_object_with_existing_attribute(
    plain_object,
):
    assert resolve_field(plain_object, "value") == "value"


def test_resolve_field__returns_none_for_plain_object_without_attribute(plain_object):
    assert resolve_field(plain_object, "missing") is None


# =========================================================================== #
# Cardinality
# =========================================================================== #


def test_str__formats_bounded_cardinality():
    assert str(Cardinality(0, 1)) == "0..1"


def test_str__formats_unbounded_cardinality():
    assert str(Cardinality(0, None)) == "0..*"


def test_is_collection__true_when_max_is_none():
    assert Cardinality(0, None).is_collection is True


def test_is_collection__true_when_max_greater_than_one():
    assert Cardinality(0, 3).is_collection is True


def test_is_collection__false_when_max_equals_one():
    assert Cardinality(0, 1).is_collection is False


def test_is_required__true_when_min_is_positive():
    assert Cardinality(1, 1).is_required is True


def test_is_required__false_when_min_is_zero():
    assert Cardinality(0, 1).is_required is False


def test_min__returns_first_tuple_element():
    assert Cardinality(2, 5).min == 2


def test_max__returns_second_tuple_element():
    assert Cardinality(2, 5).max == 5


def test_cardinality__unpacks_like_a_plain_tuple():
    minimum, maximum = Cardinality(1, 3)
    assert (minimum, maximum) == (1, 3)


# =========================================================================== #
# ElementAccessor.for_item()
# =========================================================================== #


def test_for_item__returns_none_for_item_without_parent(patient):
    root = FHIRPathCollectionItem(value=patient)
    assert ElementAccessor.for_item(root) is None


def test_for_item__returns_none_for_item_without_element(patient):
    root = FHIRPathCollectionItem(value=patient)
    item = FHIRPathCollectionItem(value=patient, parent=root, element=None)
    assert ElementAccessor.for_item(item) is None


def test_for_item__returns_none_when_parent_value_is_none(patient):
    root = FHIRPathCollectionItem(value=None)
    item = FHIRPathCollectionItem(value=None, parent=root, element="gender")
    assert ElementAccessor.for_item(item) is None


def test_for_item__returns_model_accessor_for_model_container(patient):
    root = FHIRPathCollectionItem(value=patient)
    item = FHIRPathCollectionItem(value=patient.gender, parent=root, element="gender")
    accessor = ElementAccessor.for_item(item)
    assert isinstance(accessor, ModelAccessor)


def test_for_item__returns_dict_accessor_for_mapping_container():
    data = {"gender": "female"}
    root = FHIRPathCollectionItem(value=data)
    item = FHIRPathCollectionItem(value="female", parent=root, element="gender")
    accessor = ElementAccessor.for_item(item)
    assert isinstance(accessor, DictAccessor)


def test_for_item__returns_model_accessor_for_plain_object_with_dict(plain_object):
    root = FHIRPathCollectionItem(value=plain_object)
    item = FHIRPathCollectionItem(
        value=plain_object.value, parent=root, element="value"
    )
    accessor = ElementAccessor.for_item(item)
    assert isinstance(accessor, ModelAccessor)


def test_for_item__raises_for_unwrapped_list_parent():
    list_parent = FHIRPathCollectionItem(value=[1, 2, 3])
    item = FHIRPathCollectionItem(value=1, parent=list_parent, element="x")
    with pytest.raises(FHIRPathEvaluationError):
        ElementAccessor.for_item(item)


def test_for_item__returns_none_when_field_unresolvable(patient):
    root = FHIRPathCollectionItem(value=patient)
    item = FHIRPathCollectionItem(value=None, parent=root, element="nickname")
    assert ElementAccessor.for_item(item) is None


# =========================================================================== #
# ModelAccessor.get()
# =========================================================================== #


def test_get__returns_scalar_field_value_from_model(patient):
    patient.gender = "female"
    accessor = ModelAccessor(patient, "gender", "gender", None)
    assert accessor.get() == "female"


def test_get__returns_scalar_value_when_index_zero_and_field_not_list(patient):
    patient.gender = "female"
    accessor = ModelAccessor(patient, "gender", "gender", 0)
    assert accessor.get() == "female"


def test_get__returns_indexed_item_from_model_list(named_patient):
    accessor = ModelAccessor(named_patient, "name", "name", 1)
    assert accessor.get() is named_patient.name[1]


def test_get__returns_none_for_out_of_range_index_on_model_list(named_patient):
    accessor = ModelAccessor(named_patient, "name", "name", 5)
    assert accessor.get() is None


# =========================================================================== #
# DictAccessor.get()
# =========================================================================== #


def test_get__returns_value_from_dict():
    data = {"family": "Smith"}
    accessor = DictAccessor(data, "family", "family", None)
    assert accessor.get() == "Smith"


def test_get__returns_none_for_missing_dict_key():
    accessor = DictAccessor({}, "family", "family", None)
    assert accessor.get() is None


# =========================================================================== #
# ModelAccessor.set()
# =========================================================================== #


def test_set__assigns_scalar_value_to_scalar_field(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    accessor.set("male")
    assert patient.gender == "male"


def test_set__unwraps_single_element_list_for_scalar_field(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    accessor.set(["male"])
    assert patient.gender == "male"


def test_set__unwraps_empty_list_to_none_for_scalar_field(patient):
    patient.gender = "male"
    accessor = ModelAccessor(patient, "gender", "gender", None)
    accessor.set([])
    assert patient.gender is None


def test_set__raises_for_multi_value_list_on_scalar_field(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.set(["male", "female"])


def test_set__wraps_scalar_value_into_list_for_list_field(patient):
    accessor = ModelAccessor(patient, "telecom", "telecom", None)
    accessor.set("555-0123")
    assert patient.telecom == ["555-0123"]


def test_set__replaces_whole_list_for_list_field_when_given_a_list(patient):
    patient.telecom = ["555-0123"]
    accessor = ModelAccessor(patient, "telecom", "telecom", None)
    accessor.set(["a", "b"])
    assert patient.telecom == ["a", "b"]


def test_set__writes_indexed_position_in_existing_list(named_patient):
    replacement = HumanName(family="Doe", given=["Jane"])
    accessor = ModelAccessor(named_patient, "name", "name", 0)
    accessor.set(replacement)
    assert named_patient.name[0] is replacement
    assert len(named_patient.name) == 2


def test_set__pads_list_with_none_when_index_beyond_current_length(named_patient):
    extra = HumanName(family="Extra", given=["X"])
    accessor = ModelAccessor(named_patient, "name", "name", 3)
    accessor.set(extra)
    assert named_patient.name[2] is None
    assert named_patient.name[3] is extra
    assert len(named_patient.name) == 4


def test_set__pads_currently_empty_list_when_indexed_write_used(patient):
    value = HumanName(family="X")
    accessor = ModelAccessor(patient, "name", "name", 2)
    accessor.set(value)
    assert patient.name == [None, None, value]


def test_set__initializes_list_from_none_when_indexed_write_used(patient):
    assert patient.note is None
    accessor = ModelAccessor(patient, "note", "note", 0)
    accessor.set("first note")
    assert patient.note == ["first note"]


def test_set__raises_for_nonzero_index_on_scalar_field_without_existing_list(patient):
    accessor = ModelAccessor(patient, "gender", "gender", 2)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.set("male")


def test_set__writes_scalar_field_via_index_zero_when_not_yet_a_list(patient):
    accessor = ModelAccessor(patient, "gender", "gender", 0)
    accessor.set("male")
    assert patient.gender == "male"


# =========================================================================== #
# DictAccessor.set()
# =========================================================================== #


def test_set__assigns_key_on_dict():
    data = {}
    accessor = DictAccessor(data, "gender", "gender", None)
    accessor.set("male")
    assert data == {"gender": "male"}


def test_set__raises_on_immutable_mapping():
    data = MappingProxyType({"gender": "female"})
    accessor = DictAccessor(data, "gender", "gender", None)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.set("male")


# =========================================================================== #
# ModelAccessor.delete()
# =========================================================================== #


def test_delete__unsets_scalar_field(patient):
    patient.gender = "male"
    accessor = ModelAccessor(patient, "gender", "gender", None)
    accessor.delete()
    assert patient.gender is None


def test_delete__raises_when_deleting_required_field(patient):
    accessor = ModelAccessor(patient, "birthDate", "birthDate", None)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.delete()


def test_delete__removes_indexed_entry_from_list(named_patient):
    remaining = named_patient.name[1]
    accessor = ModelAccessor(named_patient, "name", "name", 0)
    accessor.delete()
    assert named_patient.name == [remaining]


def test_delete__unsets_field_when_removing_last_list_entry(patient):
    patient.name = [HumanName(family="Solo")]
    accessor = ModelAccessor(patient, "name", "name", 0)
    accessor.delete()
    assert patient.name is None


def test_delete__raises_for_out_of_range_index(named_patient):
    accessor = ModelAccessor(named_patient, "name", "name", 5)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.delete()


# =========================================================================== #
# DictAccessor.delete()
# =========================================================================== #


def test_delete__removes_key_from_dict():
    data = {"gender": "female"}
    accessor = DictAccessor(data, "gender", "gender", None)
    accessor.delete()
    assert "gender" not in data


def test_delete__does_not_raise_for_missing_dict_key():
    data = {}
    accessor = DictAccessor(data, "gender", "gender", None)
    accessor.delete()  # should not raise
    assert "gender" not in data


def test_delete__raises_on_immutable_mapping():
    data = MappingProxyType({"gender": "female"})
    accessor = DictAccessor(data, "gender", "gender", None)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.delete()


# =========================================================================== #
# ModelAccessor.insert()
# =========================================================================== #


def test_insert__appends_value_to_list_field(patient):
    patient.telecom = ["555-0123"]
    accessor = ModelAccessor(patient, "telecom", "telecom", None)
    accessor.insert("555-0456", at=1)
    assert patient.telecom == ["555-0123", "555-0456"]


def test_insert__inserts_at_beginning_of_list(patient):
    patient.telecom = ["555-0456"]
    accessor = ModelAccessor(patient, "telecom", "telecom", None)
    accessor.insert("555-0123", at=0)
    assert patient.telecom == ["555-0123", "555-0456"]


def test_insert__raises_for_scalar_field(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.insert("male", at=0)


def test_insert__raises_for_negative_index(patient):
    accessor = ModelAccessor(patient, "telecom", "telecom", None)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.insert("555-0123", at=-1)


def test_insert__raises_for_index_beyond_current_length(patient):
    patient.telecom = ["555-0123"]
    accessor = ModelAccessor(patient, "telecom", "telecom", None)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.insert("555-0456", at=5)


def test_insert__initializes_list_when_field_currently_none(patient):
    assert patient.note is None
    accessor = ModelAccessor(patient, "note", "note", None)
    accessor.insert("first note", at=0)
    assert patient.note == ["first note"]


# =========================================================================== #
# DictAccessor.insert()
# =========================================================================== #


def test_insert__appends_value_into_dict_list():
    data = {"telecom": ["555-0123"]}
    accessor = DictAccessor(data, "telecom", "telecom", None)
    accessor.insert("555-0456", at=1)
    assert data["telecom"] == ["555-0123", "555-0456"]


# =========================================================================== #
# ModelAccessor.move()
# =========================================================================== #


def test_move__reorders_list_entries(patient):
    patient.name = [
        HumanName(family="A"),
        HumanName(family="B"),
        HumanName(family="C"),
    ]
    a, b, c = patient.name
    accessor = ModelAccessor(patient, "name", "name", None)
    accessor.move(0, 2)
    assert patient.name == [b, c, a]


def test_move__is_noop_when_source_equals_destination(named_patient):
    before = list(named_patient.name)
    accessor = ModelAccessor(named_patient, "name", "name", None)
    accessor.move(1, 1)
    assert named_patient.name == before


def test_move__raises_for_scalar_field(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.move(0, 1)


def test_move__raises_for_out_of_range_source(named_patient):
    accessor = ModelAccessor(named_patient, "name", "name", None)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.move(5, 0)


def test_move__raises_for_out_of_range_destination(named_patient):
    accessor = ModelAccessor(named_patient, "name", "name", None)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.move(0, 5)


def test_move__raises_when_field_has_no_list_present(patient):
    accessor = ModelAccessor(patient, "note", "note", None)
    with pytest.raises(FHIRPathEvaluationError):
        accessor.move(0, 1)


# =========================================================================== #
# ModelAccessor.exists()
# =========================================================================== #


def test_exists__true_for_present_scalar(patient):
    patient.gender = "female"
    accessor = ModelAccessor(patient, "gender", "gender", None)
    assert accessor.exists() is True


def test_exists__false_for_absent_scalar(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    assert accessor.exists() is False


def test_exists__true_for_valid_index(named_patient):
    accessor = ModelAccessor(named_patient, "name", "name", 1)
    assert accessor.exists() is True


def test_exists__false_for_out_of_range_index(named_patient):
    accessor = ModelAccessor(named_patient, "name", "name", 5)
    assert accessor.exists() is False


def test_exists__false_when_list_field_currently_none(patient):
    accessor = ModelAccessor(patient, "note", "note", 0)
    assert accessor.exists() is False


# =========================================================================== #
# ModelAccessor.construct()
# =========================================================================== #


def test_construct__returns_constructed_model_for_complex_field(patient):
    accessor = ModelAccessor(patient, "name", "name", None)
    constructed = accessor.construct()
    assert isinstance(constructed, HumanName)


def test_construct__returns_none_for_primitive_field(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    assert accessor.construct() is None


def test_construct__returns_none_for_dict_accessor():
    accessor = DictAccessor({}, "name", "name", None)
    assert accessor.construct() is None


# =========================================================================== #
# ModelAccessor.snapshot() / ModelAccessor.restore()
# =========================================================================== #


def test_snapshot__returns_deep_copy_independent_of_live_field(named_patient):
    accessor = ModelAccessor(named_patient, "name", "name", None)
    snapshot = accessor.snapshot()
    named_patient.name[0].family = "Changed"
    assert snapshot[0].family == "Smith"


def test_restore__reverts_field_to_snapshotted_state(named_patient):
    accessor = ModelAccessor(named_patient, "name", "name", None)
    snapshot = accessor.snapshot()
    accessor.delete()
    accessor.restore(snapshot)
    assert [n.family for n in named_patient.name] == ["Smith", "Smith"]


# =========================================================================== #
# ModelAccessor/DictAccessor properties
# =========================================================================== #


def test_cardinality__scalar_optional_field_reports_zero_one(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    assert accessor.cardinality == Cardinality(0, 1)


def test_cardinality__required_scalar_field_reports_one_one(patient):
    accessor = ModelAccessor(patient, "birthDate", "birthDate", None)
    assert accessor.cardinality == Cardinality(1, 1)


def test_cardinality__unconstrained_list_field_reports_zero_unbounded(patient):
    accessor = ModelAccessor(patient, "telecom", "telecom", None)
    assert accessor.cardinality == Cardinality(0, None)


def test_cardinality__list_field_with_max_length_reports_bounded_max(patient):
    accessor = ModelAccessor(patient, "name", "name", None)
    assert accessor.cardinality == Cardinality(0, 3)


def test_cardinality__untyped_dict_accessor_reports_zero_one():
    accessor = DictAccessor({}, "gender", "gender", None)
    assert accessor.cardinality == Cardinality(0, 1)


def test_is_list__true_for_list_annotated_model_field(patient):
    accessor = ModelAccessor(patient, "name", "name", None)
    assert accessor.is_list is True


def test_is_list__false_for_scalar_model_field(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    assert accessor.is_list is False


def test_is_list__infers_true_from_present_list_value_on_dict_accessor():
    accessor = DictAccessor({"telecom": ["555-0123"]}, "telecom", "telecom", None)
    assert accessor.is_list is True


def test_is_list__infers_false_from_scalar_value_on_dict_accessor():
    accessor = DictAccessor({"gender": "female"}, "gender", "gender", None)
    assert accessor.is_list is False


def test_is_list__caches_result_after_first_access(patient):
    accessor = ModelAccessor(patient, "name", "name", None)
    first = accessor.is_list
    patient.name = "not actually a list any more"  # bypasses validation on assignment
    assert accessor.is_list == first


def test_fhir_type__returns_complex_type_name_for_model_field(patient):
    accessor = ModelAccessor(patient, "name", "name", None)
    assert accessor.fhir_type == "HumanName"


def test_fhir_type__returns_none_for_primitive_field(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    assert accessor.fhir_type is None


def test_fhir_type__returns_none_for_dict_accessor():
    accessor = DictAccessor({}, "name", "name", None)
    assert accessor.fhir_type is None


def test_field_info__returns_field_info_for_model_accessor(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    assert accessor.field_info is not None
    assert accessor.field_info is type(patient).model_fields["gender"]


def test_field_info__returns_none_for_unknown_field_on_plain_object(plain_object):
    accessor = ModelAccessor(plain_object, "value", "value", None)
    assert accessor.field_info is None


def test_field_info__returns_none_for_dict_accessor():
    accessor = DictAccessor({}, "gender", "gender", None)
    assert accessor.field_info is None


# =========================================================================== #
# __repr__
# =========================================================================== #


def test_repr__includes_container_type_and_field_name(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    text = repr(accessor)
    assert "ModelAccessor" in text
    assert "MockPatient" in text
    assert "gender" in text


def test_repr__includes_index_when_present(named_patient):
    accessor = ModelAccessor(named_patient, "name", "name", 1)
    assert "[1]" in repr(accessor)


def test_repr__omits_index_brackets_when_absent(patient):
    accessor = ModelAccessor(patient, "gender", "gender", None)
    assert "[" not in repr(accessor)
