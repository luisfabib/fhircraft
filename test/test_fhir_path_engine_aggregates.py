from collections import namedtuple

import pytest

from fhircraft.fhir.path.engine.aggregates import Aggregate
from fhircraft.fhir.path.engine.boolean import *
from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.math import *
from fhircraft.fhir.path.engine.environment import *

env = dict()

# -------------
# Aggregate
# -------------

aggregate_cases = (
    ([1,2,3,4], 0, 10),
    ([1,2,3,4], 5, 15),
)


@pytest.mark.parametrize("values, init, expected", aggregate_cases)
def test_aggregate_returns_correct_sum(values, init, expected):
    collection = [FHIRPathCollectionItem(value=val) for val in values]
    result = Aggregate(Addition(ContextualThis(), ContextualTotal()), Literal(init)).evaluate(collection, env)
    result = result[0].value if len(result) == 1 else result
    assert result == expected

def test_aggregate_string_representation():
    expression = Aggregate(Addition(ContextualThis(), ContextualTotal()), Literal(0))
    assert str(expression) == "aggregate($this + $total, 0)"

def test_aggregate_short_string_representation():
    expression = Aggregate(Addition(ContextualThis(), ContextualTotal()))
    assert str(expression) == "aggregate($this + $total)"