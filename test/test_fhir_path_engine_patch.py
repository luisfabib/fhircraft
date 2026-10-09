"""End-to-end tests of accessor targets and patch operations on FHIRPath results."""

from typing import Optional

import pytest
from pydantic import BaseModel, Field

from fhircraft.exceptions import FHIRPathEvaluationError
from fhircraft.fhir.path.collection import FHIRPathCollection, FHIRPathCollectionItem
from fhircraft.fhir.path.engine.core import Element
from fhircraft.fhir.path.engine.filtering import Where
from fhircraft.fhir.path.engine.subsetting import First, Index, Tail
from fhircraft.fhir.path.parser import FHIRPathParser

env = {"%fhirRelease": "R5"}
parser = FHIRPathParser()


class Name(BaseModel):
    family: Optional[str] = None
    given: list[str] = Field(default_factory=list)


class Patient(BaseModel):
    gender: Optional[str] = None
    name: list[Name] = Field(default_factory=list)


def wrap(value) -> FHIRPathCollection:
    return FHIRPathCollection([FHIRPathCollectionItem(value)])


def run(expression: str, resource) -> FHIRPathCollection:
    return parser.parse(expression)._evaluate_wrapped(resource)


# --------------------------------------------------------------------------- #
# Targets
# --------------------------------------------------------------------------- #


def test_targets__element_on_existing_value():
    patient = Patient(gender="male")
    result = Element("gender").evaluate(wrap(patient), env)
    assert list(result) == ["male"]
    assert len(result.targets) == 1
    assert result.targets[0].get() == "male"


def test_targets__element_on_absent_value_keeps_target():
    result = Element("gender").evaluate(wrap(Patient()), env)
    assert len(result) == 0
    assert len(result.targets) == 1
    assert result.targets[0].get() is None


def test_targets__chain_through_absent_parent():
    result = Element("given").evaluate(
        Element("name").evaluate(wrap(Patient()), env), env
    )
    assert len(result) == 0
    assert len(result.targets) == 1
    assert result.targets[0].canonical_path.endswith("name[0].given")


def test_targets__index_beyond_end_addresses_next_slot():
    patient = Patient(name=[Name(family="A")])
    result = Index(1).evaluate(Element("name").evaluate(wrap(patient), env), env)
    assert len(result) == 0
    assert result.targets[0].canonical_path.endswith("name[1]")
    assert len(patient.name) == 1


def test_targets__evaluation_never_mutates_resource():
    patient = Patient()
    run("name[0].given[2]", patient)
    assert patient == Patient()


def test_targets__items_keep_accessor_through_subsetting():
    patient = Patient(name=[Name(family="A"), Name(family="B"), Name(family="C")])
    names = Element("name").evaluate(wrap(patient), env)
    tail = Tail().evaluate(names, env)
    assert [
        item.canonical_path.endswith(f"name[{n}]")
        for n, item in enumerate(tail._items, 1)
    ] == [
        True,
        True,
    ]
    first = First().evaluate(names, env)
    assert first._items[0].accessor is not None
    assert first._items[0].accessor.index == 0


def test_targets__items_keep_accessor_through_where():
    patient = Patient(name=[Name(family="A"), Name(family="B")])
    names = Element("name").evaluate(wrap(patient), env)
    result = Where(parser.parse("family = 'B'")).evaluate(names, env)
    assert len(result) == 1
    assert result._items[0].accessor is not None
    assert result._items[0].accessor.index == 1


def test_targets__literal_has_none():
    assert parser.parse("'abc'")._evaluate_wrapped(Patient()).targets == ()


# --------------------------------------------------------------------------- #
# Patch operations
# --------------------------------------------------------------------------- #


def test_patch__set_on_absent_nested_path():
    patient = Patient()
    run("name[0].family", patient).set("Doe")
    assert patient.name[0].family == "Doe"


def test_patch__set_overwrites_existing_value():
    patient = Patient(gender="male")
    run("gender", patient).set("female")
    assert patient.gender == "female"


def test_patch__add_appends_to_list():
    patient = Patient(name=[Name(family="A")])
    run("name", patient).add(Name(family="B"))
    assert [n.family for n in patient.name] == ["A", "B"]


def test_patch__add_to_nested_list_on_empty_resource():
    patient = Patient()
    run("name[0].given", patient).add("John")
    assert patient.name[0].given == ["John"]


def test_patch__insert_at_position():
    patient = Patient(name=[Name(family="A"), Name(family="C")])
    run("name", patient).insert_at(Name(family="B"), 1)
    assert [n.family for n in patient.name] == ["A", "B", "C"]


def test_patch__delete_filtered_items():
    patient = Patient(name=[Name(family="A"), Name(family="B"), Name(family="C")])
    run("name.where(family != 'B')", patient).delete()
    assert [n.family for n in patient.name] == ["B"]


def test_patch__delete_single_indexed_item():
    patient = Patient(name=[Name(family="A"), Name(family="B")])
    run("name[0]", patient).delete()
    assert [n.family for n in patient.name] == ["B"]


def test_patch__move_reorders_list():
    patient = Patient(name=[Name(family="A"), Name(family="B"), Name(family="C")])
    run("name", patient).move(0, 2)
    assert [n.family for n in patient.name] == ["B", "C", "A"]


def test_patch__snapshot_and_restore_roll_back():
    patient = Patient(name=[Name(family="A"), Name(family="B")])
    result = run("name", patient)
    snapshot = result.snapshot()
    result.delete()
    assert not patient.name
    result.restore(snapshot)
    assert [n.family for n in patient.name] == ["A", "B"]


def test_patch__set_on_dict_resource():
    data: dict = {}
    run("name.family", data).set("Doe")
    assert "Doe" in str(data)


def test_patch__literal_cannot_be_patched():
    with pytest.raises(FHIRPathEvaluationError):
        run("'abc'", Patient()).set("x")
