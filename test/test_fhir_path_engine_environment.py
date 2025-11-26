import pytest

from fhircraft.fhir.path.engine.environment import *
from fhircraft.fhir.path.exceptions import FHIRPathError
from fhircraft.fhir.resources.datatypes.R4 import (
    Patient,
    Observation,
    Patient,
    Reference,
)


# -------------
# Environment variables
# -------------


def test_env_variable_returns_value():
    value = 42
    collection = [FHIRPathCollectionItem(value="another-value")]
    result = EnvironmentVariable("%variable").evaluate(collection, {"%variable": value})
    result = result[0].value if len(result) == 1 else result
    assert result == value


def test_env_variable_raises_error_out_of_context():
    collection = [FHIRPathCollectionItem(value="another-value")]
    with pytest.raises(FHIRPathError):
        EnvironmentVariable("%variable").evaluate(collection, dict())


def test_env_variable_string_representation():
    assert str(EnvironmentVariable("%variable")) == "%variable"


def test_default_context_variable_is_set():
    reference = Reference(reference="patient-1")
    observation = Observation(subject=reference, meta=None)
    patient = Patient(id="patient-1", contained=[observation])  # type: ignore
    assert EnvironmentVariable("%context").single(patient) == patient
    assert EnvironmentVariable("%context").single(observation) == observation
    assert EnvironmentVariable("%context").single(reference) == reference


def test_default_resource_variable_is_set():
    reference = Reference(reference="patient-1")
    observation = Observation(subject=reference, meta=None)
    patient = Patient(id="patient-1", contained=[observation])  # type: ignore
    assert EnvironmentVariable("%resource").single(patient) == patient
    assert EnvironmentVariable("%resource").single(observation) == observation
    assert EnvironmentVariable("%resource").single(reference) == observation


def test_default_root_resource_variable_is_set():
    reference = Reference(reference="patient-1")
    observation = Observation(subject=reference, meta=None)
    patient = Patient(id="patient-1", contained=[observation])  # type: ignore
    assert EnvironmentVariable("%rootResource").single(patient) == patient
    assert EnvironmentVariable("%rootResource").single(observation) == patient
    assert EnvironmentVariable("%rootResource").single(reference) == patient


def test_default_ucum_variable_is_set():
    value = 42
    assert EnvironmentVariable("%ucum").single(value) == "http://unitsofmeasure.org"


# -------------
# $this
# -------------


def test_contextual_this_returns_value():
    value = 42
    collection = [FHIRPathCollectionItem(value="another-value")]
    result = ContextualThis().evaluate(collection, {"$this": value})
    result = result[0].value if len(result) == 1 else result
    assert result == value


def test_contextual_this_fallback_value():
    collection = [FHIRPathCollectionItem(value="another-value")]
    result = ContextualThis().evaluate(collection, dict())
    assert result == collection


def test_contextual_this_string_representation():
    assert str(ContextualThis()) == "$this"


# -------------
# $index
# -------------


def test_contextual_index_returns_value():
    value = 1
    collection = [FHIRPathCollectionItem(value="another-value")]
    result = ContextualIndex().evaluate(collection, {"$index": value})
    result = result[0].value if len(result) == 1 else result
    assert result == value


def test_contextual_index_raises_error_out_of_context():
    collection = [FHIRPathCollectionItem(value="another-value")]
    with pytest.raises(FHIRPathError):
        ContextualIndex().evaluate(collection, dict())


def test_contextual_index_string_representation():
    assert str(ContextualIndex()) == "$index"


# -------------
# $total
# -------------


def test_contextual_total_returns_value():
    value = 1
    collection = [FHIRPathCollectionItem(value="another-value")]
    result = ContextualTotal().evaluate(collection, {"$total": value})
    result = result[0].value if len(result) == 1 else result
    assert result == value


def test_contextual_total_raises_error_out_of_context():
    collection = [FHIRPathCollectionItem(value="another-value")]
    with pytest.raises(FHIRPathError):
        ContextualTotal().evaluate(collection, dict())


def test_contextual_total_string_representation():
    assert str(ContextualTotal()) == "$total"
