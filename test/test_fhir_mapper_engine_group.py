"""
Comprehensive test suite for the Group class.

This module contains unit tests for the Group class and all its methods,
using both real FHIR objects and mocking where appropriate for testing
various scenarios including error conditions.
"""

import pytest
from unittest.mock import Mock, patch
from pydantic import BaseModel

from fhircraft.fhir.mapper.engine.group import Group
from fhircraft.fhir.mapper.engine.scope import MappingScope
from fhircraft.fhir.mapper.engine.exceptions import (
    MappingDigestionError,
    MappingError,
)
from fhircraft.fhir.path.engine import Exists
from fhircraft.fhir.resources.datatypes.R4B.core.structure_map import (
    StructureMapGroup,
    StructureMapGroupInput,
    StructureMapGroupRule,
)


# ============================================================================
# TEST MODELS
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


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def minimal_group_definition():
    """Minimal group definition with just a name and input."""
    input_def = StructureMapGroupInput(name="src", type="Person", mode="source")
    return StructureMapGroup(name="test-group", input=[input_def], rule=None)


@pytest.fixture
def group_definition_with_multiple_inputs():
    """Group definition with multiple input configurations."""
    input1 = StructureMapGroupInput(name="src", type="Person", mode="source")
    input2 = StructureMapGroupInput(name="tgt", type="Patient", mode="target")
    return StructureMapGroup(
        name="multi-input-group", input=[input1, input2], rule=None
    )


@pytest.fixture
def group_definition_with_rules():
    """Group definition with rule configurations."""
    input_def = StructureMapGroupInput(name="src", type="Person", mode="source")
    rule = StructureMapGroupRule(
        name="test-rule", source=None, target=None, rule=None, dependent=None
    )
    return StructureMapGroup(name="group-with-rules", input=[input_def], rule=[rule])


@pytest.fixture
def group_definition_without_inputs():
    """Group definition missing inputs (for error testing)."""
    return StructureMapGroup(name="no-inputs-group", input=None, rule=None)


@pytest.fixture
def group_definition_input_without_name():
    """Group definition with input missing name."""
    input_def = StructureMapGroupInput(name=None, type="Person", mode="source")
    return StructureMapGroup(name="invalid-input-group", input=[input_def], rule=None)


@pytest.fixture
def group_definition_target_input_without_type():
    """Group definition with target input missing type."""
    input_def = StructureMapGroupInput(name="tgt", type=None, mode="target")
    return StructureMapGroup(name="target-no-type-group", input=[input_def], rule=None)


@pytest.fixture
def mock_parent_group():
    """Mock parent group for testing."""
    return Mock()


@pytest.fixture
def mapping_scope():
    """Real mapping scope with patient and person types."""
    return MappingScope(
        name="test-scope",
        types={"Patient": PatientModel, "Person": PersonModel},
        source_instances={"src": PersonModel(firstName="John", lastName="Doe")},
        target_instances={"Patient": PatientModel()},
    )


@pytest.fixture
def sample_fhirpath():
    """Sample FHIRPath for testing."""
    return Exists()


@pytest.fixture
def mock_rule_with_first_target():
    """Mock rule with 'first' target list mode."""
    rule = Mock()
    rule.has_first_target = True
    rule.has_last_target = False
    rule.process = Mock()
    return rule


@pytest.fixture
def mock_rule_with_last_target():
    """Mock rule with 'last' target list mode."""
    rule = Mock()
    rule.has_first_target = False
    rule.has_last_target = True
    rule.process = Mock()
    return rule


@pytest.fixture
def mock_regular_rule():
    """Mock rule without special list modes."""
    rule = Mock()
    rule.has_first_target = False
    rule.has_last_target = False
    rule.process = Mock()
    return rule


# ============================================================================
# Group.__init__() Tests
# ============================================================================


def test_init_minimal_group(minimal_group_definition, mock_parent_group):
    """Test initialization with minimal group definition."""
    group = Group(minimal_group_definition, mock_parent_group)

    assert group.definition == minimal_group_definition
    assert group.name == "test-group"
    assert group.parent_group == mock_parent_group
    assert len(group.rules) == 0
    assert len(group.inputs) == 1
    assert group.inputs[0].name == "src"


def test_init_group_without_name(mock_parent_group):
    """Test initialization generates name when none provided."""
    input_def = StructureMapGroupInput(name="src", type="Person", mode="source")
    definition = StructureMapGroup(name=None, input=[input_def], rule=None)
    group = Group(definition, mock_parent_group)

    assert group.name.startswith("group-")
    assert group.definition == definition


def test_init_with_multiple_inputs(
    group_definition_with_multiple_inputs, mock_parent_group
):
    """Test initialization with multiple input definitions."""
    group = Group(group_definition_with_multiple_inputs, mock_parent_group)

    assert len(group.inputs) == 2
    assert group.inputs[0].name == "src"
    assert group.inputs[0].mode == "source"
    assert group.inputs[1].name == "tgt"
    assert group.inputs[1].mode == "target"


def test_init_with_rules(group_definition_with_rules, mock_parent_group):
    """Test initialization creates Rule objects from rule definitions."""
    group = Group(group_definition_with_rules, mock_parent_group)

    assert len(group.rules) == 1
    assert group.rules[0].name == "test-rule"
    assert group.rules[0].parent_group == group


def test_init_without_inputs_raises_error(
    group_definition_without_inputs, mock_parent_group
):
    """Test initialization fails when group lacks input definitions."""
    with pytest.raises(
        MappingDigestionError, match="Group 'no-inputs-group' has no input definitions"
    ):
        Group(group_definition_without_inputs, mock_parent_group)


# ============================================================================
# Group._organize_rules() Tests
# ============================================================================


def test_organize_rules_empty_list(minimal_group_definition, mock_parent_group):
    """Test organizing rules when no rules are present."""
    group = Group(minimal_group_definition, mock_parent_group)

    # Should not raise error and rules should be empty
    assert len(group.rules) == 0


def test_organize_rules_regular_rules_only(mock_parent_group):
    """Test organizing rules with only regular rules."""
    input_def = StructureMapGroupInput(name="src", type="Person", mode="source")
    definition = StructureMapGroup(name="test-group", input=[input_def], rule=None)
    group = Group(definition, mock_parent_group)

    # Add mock regular rules
    rule1 = Mock()
    rule1.has_first_target = False
    rule1.has_last_target = False
    rule2 = Mock()
    rule2.has_first_target = False
    rule2.has_last_target = False
    group.rules = [rule1, rule2]

    group._organize_rules()

    # Order should remain the same
    assert group.rules == [rule1, rule2]


def test_organize_rules_with_first_and_last(mock_parent_group):
    """Test organizing rules with first, regular, and last rules."""
    input_def = StructureMapGroupInput(name="src", type="Person", mode="source")
    definition = StructureMapGroup(name="test-group", input=[input_def], rule=None)
    group = Group(definition, mock_parent_group)

    # Create rules in mixed order
    regular_rule = Mock()
    regular_rule.has_first_target = False
    regular_rule.has_last_target = False

    first_rule = Mock()
    first_rule.has_first_target = True
    first_rule.has_last_target = False

    last_rule = Mock()
    last_rule.has_first_target = False
    last_rule.has_last_target = True

    # Add in random order
    group.rules = [regular_rule, last_rule, first_rule]

    group._organize_rules()

    # Should be reordered: first, regular, last
    assert group.rules == [first_rule, regular_rule, last_rule]


def test_organize_rules_multiple_first_rules_raises_error(mock_parent_group):
    """Test error when multiple rules have 'first' target list mode."""
    input_def = StructureMapGroupInput(name="src", type="Person", mode="source")
    definition = StructureMapGroup(name="test-group", input=[input_def], rule=None)
    group = Group(definition, mock_parent_group)

    first_rule1 = Mock()
    first_rule1.has_first_target = True
    first_rule1.has_last_target = False

    first_rule2 = Mock()
    first_rule2.has_first_target = True
    first_rule2.has_last_target = False

    group.rules = [first_rule1, first_rule2]

    with pytest.raises(
        MappingDigestionError,
        match="Only one rule with 'first' target list mode allowed",
    ):
        group._organize_rules()


def test_organize_rules_multiple_last_rules_raises_error(mock_parent_group):
    """Test error when multiple rules have 'last' target list mode."""
    input_def = StructureMapGroupInput(name="src", type="Person", mode="source")
    definition = StructureMapGroup(name="test-group", input=[input_def], rule=None)
    group = Group(definition, mock_parent_group)

    last_rule1 = Mock()
    last_rule1.has_first_target = False
    last_rule1.has_last_target = True

    last_rule2 = Mock()
    last_rule2.has_first_target = False
    last_rule2.has_last_target = True

    group.rules = [last_rule1, last_rule2]

    with pytest.raises(
        MappingDigestionError,
        match="Only one rule with 'last' target list mode allowed",
    ):
        group._organize_rules()


# ============================================================================
# Group.bind_parameters() Tests
# ============================================================================


def test_bind_parameters_success(
    minimal_group_definition, mapping_scope, sample_fhirpath
):
    """Test successful parameter binding."""
    group = Group(minimal_group_definition, None)

    group.bind_parameters(mapping_scope, [sample_fhirpath], is_dependent=False)

    # Should define variable in scope
    assert "src" in mapping_scope.variables
    assert mapping_scope.variables["src"] == sample_fhirpath


def test_bind_parameters_parameter_count_mismatch(
    minimal_group_definition, mapping_scope, sample_fhirpath
):
    """Test error when parameter count doesn't match input count."""
    group = Group(minimal_group_definition, None)

    with pytest.raises(MappingError, match="Expected 1 parameters, got 2"):
        group.bind_parameters(
            mapping_scope, [sample_fhirpath, sample_fhirpath], is_dependent=False
        )


def test_bind_parameters_target_input_missing_type_non_dependent(mock_parent_group):
    """Test error when target input lacks type for non-dependent call."""
    input_def = StructureMapGroupInput(name="tgt", type=None, mode="target")
    definition = StructureMapGroup(name="test-group", input=[input_def], rule=None)
    group = Group(definition, mock_parent_group)

    mapping_scope = MappingScope(name="test")
    sample_fhirpath = Exists()

    with pytest.raises(
        MappingError,
        match="Target input 'tgt' in group 'test-group' must have a type specified",
    ):
        group.bind_parameters(mapping_scope, [sample_fhirpath], is_dependent=False)


def test_bind_parameters_target_input_no_type_dependent_allowed(mock_parent_group):
    """Test that target input without type is allowed for dependent calls."""
    input_def = StructureMapGroupInput(name="tgt", type=None, mode="target")
    definition = StructureMapGroup(name="test-group", input=[input_def], rule=None)
    group = Group(definition, mock_parent_group)

    mapping_scope = MappingScope(name="test")
    sample_fhirpath = Exists()

    # Should not raise error when is_dependent=True
    group.bind_parameters(mapping_scope, [sample_fhirpath], is_dependent=True)
    assert "tgt" in mapping_scope.variables


def test_bind_parameters_unknown_input_type(mock_parent_group):
    """Test error when input has unknown type."""
    input_def = StructureMapGroupInput(name="src", type="UnknownType", mode="source")
    definition = StructureMapGroup(name="test-group", input=[input_def], rule=None)
    group = Group(definition, mock_parent_group)

    mapping_scope = MappingScope(name="test")
    sample_fhirpath = Exists()

    with pytest.raises(
        MappingError,
        match="Input 'src' in group 'test-group' has unknown type 'UnknownType'",
    ):
        group.bind_parameters(mapping_scope, [sample_fhirpath], is_dependent=False)


# ============================================================================
# Group.process() Tests
# ============================================================================


def test_process_success_minimal(
    minimal_group_definition, mapping_scope, sample_fhirpath
):
    """Test successful processing with minimal configuration."""
    group = Group(minimal_group_definition, None)

    # Should complete without error
    group.process(mapping_scope, [sample_fhirpath], is_dependent=False)


def test_process_creates_group_scope(
    minimal_group_definition, mapping_scope, sample_fhirpath
):
    """Test that process creates a group scope with correct parent."""
    group = Group(minimal_group_definition, None)

    with patch("fhircraft.fhir.mapper.engine.group.MappingScope") as mock_scope_class:
        mock_scope = Mock()
        mock_scope_class.return_value = mock_scope

        group.process(mapping_scope, [sample_fhirpath], is_dependent=False)

        # Should create group scope with correct parameters
        mock_scope_class.assert_called_once_with(
            name="test-group", parent=mapping_scope
        )


def test_process_calls_bind_parameters(
    minimal_group_definition, mapping_scope, sample_fhirpath
):
    """Test that process calls bind_parameters with correct arguments."""
    group = Group(minimal_group_definition, None)

    with patch.object(group, "bind_parameters") as mock_bind:
        group.process(mapping_scope, [sample_fhirpath], is_dependent=True)

        mock_bind.assert_called_once()
        # Check that is_dependent flag was passed correctly
        assert mock_bind.call_args[0][2] == True  # is_dependent parameter


def test_process_executes_all_rules(
    group_definition_with_rules, mapping_scope, sample_fhirpath
):
    """Test that process executes all rules in the group."""
    group = Group(group_definition_with_rules, None)

    # Mock the rule's process method
    group.rules[0].process = Mock()

    group.process(mapping_scope, [sample_fhirpath], is_dependent=False)

    # Should call process on each rule
    group.rules[0].process.assert_called_once()


def test_process_with_multiple_rules_execution_order(mock_parent_group):
    """Test that rules are executed in the correct order."""
    input_def = StructureMapGroupInput(name="src", type="Person", mode="source")
    definition = StructureMapGroup(name="test-group", input=[input_def], rule=None)
    group = Group(definition, mock_parent_group)

    # Create mock rules in order: regular, first, last
    regular_rule = Mock()
    regular_rule.has_first_target = False
    regular_rule.has_last_target = False
    regular_rule.process = Mock()

    first_rule = Mock()
    first_rule.has_first_target = True
    first_rule.has_last_target = False
    first_rule.process = Mock()

    last_rule = Mock()
    last_rule.has_first_target = False
    last_rule.has_last_target = True
    last_rule.process = Mock()

    # Add rules and organize them
    group.rules = [regular_rule, last_rule, first_rule]
    group._organize_rules()

    mapping_scope = MappingScope(name="test", types={"Person": PersonModel})
    sample_fhirpath = Exists()

    group.process(mapping_scope, [sample_fhirpath], is_dependent=False)

    # All rules should be called
    first_rule.process.assert_called_once()
    regular_rule.process.assert_called_once()
    last_rule.process.assert_called_once()

    # Verify order by checking that rules are in expected sequence
    assert group.rules == [first_rule, regular_rule, last_rule]
