import pytest
from fhircraft.fhir.mapper.engine.abstract import FHIRMappingEngineComponent
from fhircraft.fhir.mapper.engine.scope import MappingScope
from fhircraft.fhir.path.engine import Invocation, Element, Index


@pytest.fixture
def component():
    class MockComponent(FHIRMappingEngineComponent):
        def process(self, scope: MappingScope):
            pass

    return MockComponent()


@pytest.fixture
def context():
    return MappingScope(
        name="TestScope",
        variables={
            "var1": Invocation(Element("A"), Element("B")),
            "var2": Invocation(Element("C"), Element("D")),
        },
    )


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("var1", "A.B"),
        ("var1.C", "A.B.C"),
        ("var1.C.var1", "A.B.C.var1"),
        ("var1.Cvar1", "A.B.Cvar1"),
        (
            "var1.replace(var1.C, 'John')",
            "A.B.replace(A.B.C, 'John')",
        ),
        ("var2", "C.D"),
        ("var2.code", "C.D.code"),
        ("var2.value", "C.D.value"),
        (
            "var2.where(valueString = var1.C)",
            "C.D.where(valueString = A.B.C)",
        ),
    ],
)
def test_resolve_fhirpath_within_context(component, context, expression, expected):
    assert (
        str(component.resolve_fhirpath_within_context(expression, context)) == expected
    )
