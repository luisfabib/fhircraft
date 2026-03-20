import pytest
from pydantic import BaseModel

from fhircraft.fhir.mapper.engine.target import RuleTarget
from fhircraft.fhir.mapper.engine.scope import MappingScope
from fhircraft.fhir.mapper.engine.exceptions import (
    MappingDigestionError,
    SourceProcessingError,
)
from fhircraft.fhir.path.engine.core import Element
from fhircraft.fhir.resources.datatypes.R4B.core.structure_map import (
    StructureMapGroupRuleTarget,
    StructureMapGroupRuleTargetParameter,
)


# ============================================================================
# Helpers & Fixtures
# ============================================================================


class PatientModel(BaseModel):
    """Simple patient model for testing."""

    id: str = "patient-1"
    name: list[str] = []
    active: bool = True


class PersonModel(BaseModel):
    """Simple person model for testing."""

    id: str = "person-1"
    firstName: str = ""
    lastName: str = ""


@pytest.fixture
def basic_target_definition():
    """Basic target definition with minimal required fields."""
    return StructureMapGroupRuleTarget(
        context="Patient",
        variable=None,
        element=None,
        transform=None,
        parameter=None,
    )


@pytest.fixture
def target_with_variable():
    """Target definition with custom variable."""
    return StructureMapGroupRuleTarget(
        context="Patient",
        variable="patient-var",
        element=None,
        transform=None,
        parameter=None,
    )


@pytest.fixture
def target_with_element():
    """Target definition with element path."""
    return StructureMapGroupRuleTarget(
        context="Patient",
        variable="patient",
        element="name",
        transform=None,
        parameter=None,
    )


@pytest.fixture
def target_with_copy_transform():
    """Target definition with copy transform and parameters."""
    return StructureMapGroupRuleTarget(
        context="Patient",
        variable="patient",
        element="name",
        transform="copy",
        parameter=[StructureMapGroupRuleTargetParameter(valueString="John Doe")],
    )


@pytest.fixture
def mock_rule():
    """Mock parent rule with minimal implementation."""

    class MockRule:
        def __init__(self):
            self.name = "test_rule"

    return MockRule()


@pytest.fixture
def mapping_scope():
    """Real mapping scope with patient and person types."""
    return MappingScope(
        name="test_scope",
        types={"Patient": PatientModel, "Person": PersonModel},
        source_instances={"src": PersonModel(firstName="John", lastName="Doe")},
        target_instances={"Patient": PatientModel()},
    )


# ============================================================================
# RuleTarget.__init__()
# ============================================================================


def test_init__with_minimal_required(basic_target_definition, mock_rule):
    target = RuleTarget(basic_target_definition, mock_rule)

    assert target.definition == basic_target_definition
    assert target.parent_rule == mock_rule
    assert target.variable.startswith("target-")  # Note: typo in original code
    assert target.resolved_path is None
    assert target.transform is None


def test_init__with_custom_variable_name(target_with_variable, mock_rule):
    target = RuleTarget(target_with_variable, mock_rule)

    assert target.variable == "patient-var"


def test_init__with_copy_transform(target_with_copy_transform, mock_rule):
    """Test initialization with copy transform."""
    target = RuleTarget(target_with_copy_transform, mock_rule)

    assert target.variable == "patient"
    assert target.transform is not None
    assert target.definition.transform == "copy"


def test_init__auto_generates_variable_name_if_missing(
    basic_target_definition, mock_rule
):
    target = RuleTarget(basic_target_definition, mock_rule)

    assert target.variable.startswith("target-")
    assert str(id(basic_target_definition)) in target.variable


def test_init__raises_error_for_missing_context(mock_rule):
    target_def = StructureMapGroupRuleTarget(context=None)

    with pytest.raises(MappingDigestionError, match="Source context is required"):
        RuleTarget(target_def, mock_rule)


def test_init__raises_error_for_unsupported_transform(mock_rule):
    """Test error for unsupported transform types."""
    target_def = StructureMapGroupRuleTarget(
        context="Patient", transform="invalid_transform"
    )

    with pytest.raises(
        SourceProcessingError, match="Unsupported transform: invalid_transform"
    ):
        RuleTarget(target_def, mock_rule)


def test_init__raises_error_for_transform_with_invalid_parameters(mock_rule):
    target_def = StructureMapGroupRuleTarget(
        context="Patient",
        transform="copy",
        parameter=[
            StructureMapGroupRuleTargetParameter(valueString="value1"),
            StructureMapGroupRuleTargetParameter(valueString="value2"),
        ],
    )

    with pytest.raises(ValueError):
        RuleTarget(target_def, mock_rule)


# ============================================================================
# RuleTarget.process()
# ============================================================================


def test_process__without_transform(basic_target_definition, mock_rule, mapping_scope):
    """Test basic successful processing without transform."""
    target = RuleTarget(basic_target_definition, mock_rule)

    # Mock resolve_fhirpath to return an Element
    original_resolve = mapping_scope.resolve_fhirpath
    mapping_scope.resolve_fhirpath = lambda ctx: Element(ctx)

    target.process(mapping_scope)

    # Restore original method
    mapping_scope.resolve_fhirpath = original_resolve

    # Check that processing completed
    assert target.resolved_path is not None
    assert target.variable in mapping_scope.variables


def test_process__with_element(target_with_element, mock_rule, mapping_scope):
    target = RuleTarget(target_with_element, mock_rule)

    # Mock resolve_fhirpath to return an Element
    original_resolve = mapping_scope.resolve_fhirpath
    mapping_scope.resolve_fhirpath = lambda ctx: Element(ctx)

    target.process(mapping_scope)

    # Restore original method
    mapping_scope.resolve_fhirpath = original_resolve

    # Check that processing completed with element
    assert target.resolved_path is not None
    assert target.variable == "patient"
    assert target.variable in mapping_scope.variables


def test_process__with_copy_transform(
    target_with_copy_transform, mock_rule, mapping_scope
):
    target = RuleTarget(target_with_copy_transform, mock_rule)

    # Mock resolve_fhirpath to return an Element
    original_resolve = mapping_scope.resolve_fhirpath
    mapping_scope.resolve_fhirpath = lambda ctx: Element(ctx)

    target.process(mapping_scope)

    # Restore original method
    mapping_scope.resolve_fhirpath = original_resolve

    # Check that processing completed with transform
    assert target.resolved_path is not None
    assert target.transform is not None
    assert target.variable in mapping_scope.variables


# ============================================================================
# RuleTarget._resolve_transform()
# ============================================================================


@pytest.mark.parametrize(
    "transform_name",
    [
        "copy",
        "create",
        "cast",
        "append",
        "cc",
        "cp",
        "qty",
        "evaluate",
    ],
)
def test_resolve_transform__supported_transform(transform_name, mock_rule):
    # Create target definition with transform
    target_def = StructureMapGroupRuleTarget(
        context="Patient",
        transform=transform_name,
        parameter=[StructureMapGroupRuleTargetParameter(valueString="test")],
    )

    target = RuleTarget(target_def, mock_rule)
    result = target._resolve_transform(transform_name, target_def.parameter)

    # Should return a transform instance
    assert result is not None


def test_resolve_transform__none_returns_none(basic_target_definition, mock_rule):
    target = RuleTarget(basic_target_definition, mock_rule)
    result = target._resolve_transform(None, [])

    assert result is None


def test_resolve_transform__raises_error_for_unsupported_transform(
    basic_target_definition, mock_rule
):
    target = RuleTarget(basic_target_definition, mock_rule)

    with pytest.raises(
        SourceProcessingError, match="Unsupported transform: unsupported_transform"
    ):
        target._resolve_transform("unsupported_transform", [])


def test_resolve_transform__copy_transform_with_string_parameter(mock_rule):
    target_def = StructureMapGroupRuleTarget(
        context="Patient",
        transform="copy",
        parameter=[StructureMapGroupRuleTargetParameter(valueString="test_value")],
    )

    target = RuleTarget(target_def, mock_rule)
    transform = target._resolve_transform("copy", target_def.parameter)

    assert transform is not None
    # The transform should be able to process
    from fhircraft.fhir.mapper.engine.scope import MappingScope

    scope = MappingScope(name="test")
    result = transform.process(scope)
    assert result == "test_value"
