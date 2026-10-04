"""Tests for the public FHIRPathMixin interface: ``model.evaluate`` and ``model.patch``."""

import pytest

from fhircraft.exceptions import FHIRPathEvaluationError
from fhircraft.fhir.path.patch import FHIRPatch
from fhircraft.fhir.resources.datatypes import get_fhir_type

Patient = get_fhir_type("Patient", "R5")


@pytest.fixture
def patient():
    return Patient(
        gender="male",
        name=[
            {"use": "official", "family": "Doe", "given": ["John"]},
            {"use": "nickname", "family": "Smith"},
        ],
        telecom=[
            {"system": "phone", "value": "555-0100"},
            {"system": "fax", "value": "555-0199"},
        ],
    )


# --------------------------------------------------------------------------- #
# evaluate
# --------------------------------------------------------------------------- #


def test_evaluate__returns_list_of_values(patient):
    assert patient.evaluate("Patient.name.family") == ["Doe", "Smith"]


def test_evaluate__returns_empty_list_when_nothing_matches(patient):
    assert patient.evaluate("Patient.birthDate") == []


def test_evaluate__supports_functions_and_filters(patient):
    assert patient.evaluate("Patient.telecom.where(system='phone').value") == [
        "555-0100"
    ]
    assert patient.evaluate("Patient.name.count()") == [2]
    assert patient.evaluate("Patient.name.first().use") == ["official"]
    assert patient.evaluate("Patient.birthDate.exists()") == [False]


def test_evaluate__accepts_environment_variables(patient):
    from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem

    result = patient.evaluate(
        "Patient.name.where(use = %use).family",
        {"%use": FHIRPathCollectionItem.wrap("nickname")},
    )
    assert result == ["Smith"]


def test_evaluate__does_not_mutate_model(patient):
    before = patient.model_dump()
    patient.evaluate("Patient.address.line[3]")
    assert patient.model_dump() == before


# --------------------------------------------------------------------------- #
# patch
# --------------------------------------------------------------------------- #


def test_patch__is_fhir_patch_bound_to_model(patient):
    assert isinstance(patient.patch, FHIRPatch)


def test_patch_add__appends_to_repeating_element_and_coerces_dicts(patient):
    patient.patch.add("Patient.name", {"family": "Roe"})
    assert patient.evaluate("Patient.name.family") == ["Doe", "Smith", "Roe"]
    assert type(patient.name[2]) is type(patient.name[0])


def test_patch_add__creates_missing_parents(patient):
    patient.patch.add("Patient.address[0].line", "1 Main St")
    assert patient.evaluate("Patient.address.line") == ["1 Main St"]


def test_patch_add__assigns_single_valued_element():
    patient = Patient()
    patient.patch.add("Patient.birthDate", "1990-05-15")
    assert patient.evaluate("Patient.birthDate") == ["1990-05-15"]


def test_patch_insert__at_index(patient):
    patient.patch.insert("Patient.name", {"family": "Mid"}, 1)
    assert patient.evaluate("Patient.name.family") == ["Doe", "Mid", "Smith"]


def test_patch_insert__rejects_single_valued_element(patient):
    with pytest.raises(FHIRPathEvaluationError):
        patient.patch.insert("Patient.gender", "female", 0)


def test_patch_replace__overwrites_every_match(patient):
    patient.patch.replace("Patient.name.family", "Roe")
    assert patient.evaluate("Patient.name.family") == ["Roe", "Roe"]


def test_patch_replace__raises_when_nothing_matches(patient):
    with pytest.raises(FHIRPathEvaluationError):
        patient.patch.replace("Patient.birthDate", "1990-05-15")


def test_patch_delete__removes_matched_elements(patient):
    patient.patch.delete("Patient.telecom.where(system='fax')")
    assert patient.evaluate("Patient.telecom.system") == ["phone"]


def test_patch_delete__removing_last_entry_unsets_field(patient):
    patient.patch.delete("Patient.telecom")
    assert patient.telecom in (None, [])


def test_patch_delete__raises_when_nothing_matches(patient):
    with pytest.raises(FHIRPathEvaluationError):
        patient.patch.delete("Patient.birthDate")


def test_patch_move__reorders_repeating_element(patient):
    patient.patch.move("Patient.name", 0, 1)
    assert patient.evaluate("Patient.name.family") == ["Smith", "Doe"]


def test_patch_move__out_of_range_raises_and_leaves_model_intact(patient):
    with pytest.raises(FHIRPathEvaluationError):
        patient.patch.move("Patient.name", 0, 5)
    assert patient.evaluate("Patient.name.family") == ["Doe", "Smith"]


def test_patch__failed_operation_is_rolled_back(patient):
    before = patient.model_dump()
    with pytest.raises(FHIRPathEvaluationError):
        patient.patch.insert("Patient.name", {"family": "X"}, 9)
    assert patient.model_dump() == before
