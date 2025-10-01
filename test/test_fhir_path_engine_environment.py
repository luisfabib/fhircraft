import pytest

from fhircraft.fhir.path.engine.environment import *
from fhircraft.fhir.path.exceptions import FHIRPathError

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
    value = 42
    assert EnvironmentVariable("%context").single(value) == value


def test_default_resource_variable_is_set():
    value = 42
    assert EnvironmentVariable("%resource").single(value) == value


def test_default_root_resource_variable_is_set():
    value = 42
    assert EnvironmentVariable("%rootResource").single(value) == value


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
