import pytest
from unittest.mock import Mock, patch
from pydantic import BaseModel

from fhircraft.fhir.mapper.engine.rule import Rule
from fhircraft.fhir.mapper.engine.scope import MappingScope
from fhircraft.fhir.mapper.engine.exceptions import (
    RuleProcessingError,
    SourceAssertionError,
    MappingDigestionError,
)
from fhircraft.fhir.resources.datatypes.R4B.core.structure_map import (
    StructureMapGroupRule,
    StructureMapGroupRuleSource,
    StructureMapGroupRuleTarget,
    StructureMapGroupRuleDependent,
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
def minimal_rule_definition():
    """Minimal rule definition with just a name."""
    return StructureMapGroupRule(
        name="test-rule", source=None, target=None, rule=None, dependent=None
    )


@pytest.fixture
def rule_definition_with_sources():
    """Rule definition with source configurations."""
    source1 = StructureMapGroupRuleSource(
        context="Patient", variable="patient", element=None
    )
    source2 = StructureMapGroupRuleSource(
        context="Person", variable="person", element=None
    )
    return StructureMapGroupRule(
        name="rules-with-sources",
        source=[source1, source2],
        target=None,
        rule=None,
        dependent=None,
    )


@pytest.fixture
def rule_definition_with_targets():
    """Rule definition with target configurations."""
    target1 = StructureMapGroupRuleTarget(
        context="Patient", variable="patient", element=None
    )
    target2 = StructureMapGroupRuleTarget(
        context="Person", variable="person", element=None
    )
    return StructureMapGroupRule(
        name="rule-with-targets",
        source=None,
        target=[target1, target2],
        rule=None,
        dependent=None,
    )


@pytest.fixture
def rule_definition_with_nested_rules():
    """Rule definition with nested rule configurations."""
    nested_rule = StructureMapGroupRule(
        name="nested-rule", source=None, target=None, rule=None, dependent=None
    )
    return StructureMapGroupRule(
        name="parent-rule", source=None, target=None, rule=[nested_rule], dependent=None
    )


@pytest.fixture
def rule_definition_with_dependents():
    """Rule definition with dependent configurations."""
    dependent = StructureMapGroupRuleDependent(
        name="dependent-group", variable=["test_var"]
    )
    return StructureMapGroupRule(
        name="rule-with-dependents",
        source=None,
        target=None,
        rule=None,
        dependent=[dependent],
    )


@pytest.fixture
def mock_parent_group():
    """Mock parent group for rule."""
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
    from fhircraft.fhir.path.engine import Exists

    return Exists()


# ============================================================================
# Rule.__init__() Tests
# ============================================================================


def test_init_minimal_rule(minimal_rule_definition, mock_parent_group):
    """Test initialization with minimal rule definition."""
    rule = Rule(minimal_rule_definition, mock_parent_group)

    assert rule.definition == minimal_rule_definition
    assert rule.name == "test-rule"
    assert rule.parent_group == mock_parent_group
    assert len(rule.sources) == 0
    assert len(rule.targets) == 0
    assert len(rule.nested_rules) == 0
    assert len(rule.dependents) == 0


def test_init_rule_without_name(mock_parent_group):
    """Test initialization generates name when none provided."""
    definition = StructureMapGroupRule(
        name=None, source=None, target=None, rule=None, dependent=None
    )
    rule = Rule(definition, mock_parent_group)

    assert rule.name.startswith("rule-")
    assert rule.definition == definition


def test_init_with_sources(rule_definition_with_sources, mock_parent_group):
    """Test initialization creates RuleSource objects from source definitions."""
    rule = Rule(rule_definition_with_sources, mock_parent_group)

    assert len(rule.sources) == 2

    # Check sources were initialized with correct parameters
    assert rule.sources[0].definition == rule_definition_with_sources.source[0]
    assert rule.sources[0].parent_rule == rule
    assert rule.sources[1].definition == rule_definition_with_sources.source[1]
    assert rule.sources[1].parent_rule == rule


def test_init_with_targets(rule_definition_with_targets, mock_parent_group):
    """Test initialization creates RuleTarget objects from target definitions."""
    rule = Rule(rule_definition_with_targets, mock_parent_group)

    assert len(rule.targets) == 2

    # Check targets were initialized with correct parameters
    assert rule.targets[0].definition == rule_definition_with_targets.target[0]
    assert rule.targets[0].parent_rule == rule
    assert rule.targets[1].definition == rule_definition_with_targets.target[1]
    assert rule.targets[1].parent_rule == rule


def test_init_with_nested_rules(rule_definition_with_nested_rules, mock_parent_group):
    """Test initialization creates nested Rule objects."""
    rule = Rule(rule_definition_with_nested_rules, mock_parent_group)

    assert len(rule.nested_rules) == 1
    assert isinstance(rule.nested_rules[0], Rule)
    assert rule.nested_rules[0].name == "nested-rule"
    assert rule.nested_rules[0].parent_group == mock_parent_group


def test_init_with_dependents(rule_definition_with_dependents, mock_parent_group):
    """Test initialization extracts dependent information."""
    rule = Rule(rule_definition_with_dependents, mock_parent_group)

    assert len(rule.dependents) == 1
    assert rule.dependents[0] == rule_definition_with_dependents.dependent[0]


# ============================================================================
# Rule.process() Tests
# ============================================================================


def test_init_dependent_without_name_raises_error(mock_parent_group):
    """Test initialization fails when dependent lacks name."""
    dependent = StructureMapGroupRuleDependent(name=None, variable=["var1"])
    rule_def = StructureMapGroupRule(
        name="rule-invalid-dependent",
        source=None,
        target=None,
        rule=None,
        dependent=[dependent],
    )

    with pytest.raises(
        MappingDigestionError, match="Dependent rule or group must have a name"
    ):
        Rule(rule_def, mock_parent_group)


def test_process_source_assertion_error_propagates(
    rule_definition_with_sources, mapping_scope
):
    """Test that SourceAssertionError from sources is propagated."""
    rule = Rule(rule_definition_with_sources, None)

    # Mock source to raise SourceAssertionError
    mock_source = Mock()
    mock_source.variable = "patient"
    mock_source.process.side_effect = SourceAssertionError("Test assertion error")
    rule.sources = [mock_source]

    with pytest.raises(
        SourceAssertionError,
        match="Source assertion failed for rule rules-with-sources",
    ):
        rule.process(mapping_scope)


def test_process_iterates_over_source_collections(
    rule_definition_with_sources,
    mapping_scope,
    sample_fhirpath,
):
    """Test that rule processes iterations based on source collection sizes."""
    rule = Rule(rule_definition_with_sources, None)

    # Mock source with iteration count
    mock_source = Mock()
    mock_source.variable = "patient"
    mock_source.iteration_count = 3  # 3 iterations
    mock_source.process = Mock()
    rule.sources = [mock_source]

    # Mock target
    mock_target = Mock()
    rule.targets = [mock_target]

    # Mock scope methods
    mapping_scope.resolve_fhirpath = Mock(return_value=sample_fhirpath)

    result_scope = rule.process(mapping_scope)

    # Should process target for each iteration
    assert mock_target.process.call_count == 3
    assert mock_source.process.called


def test_process_missing_source_variable_raises_error(
    rule_definition_with_sources, mapping_scope
):
    """Test that missing source variable in scope raises RuleProcessingError."""
    rule = Rule(rule_definition_with_sources, None)

    # Mock source
    mock_source = Mock()
    mock_source.variable = "missing-var"
    mock_source.iteration_count = 1
    mock_source.process = Mock()
    rule.sources = [mock_source]

    # Mock scope to return None for missing variable
    mapping_scope.resolve_fhirpath = Mock(return_value=None)

    with pytest.raises(
        RuleProcessingError, match="Source variable missing-var not found"
    ):
        rule.process(mapping_scope)


def test_process_with_dependents(
    rule_definition_with_dependents, mapping_scope, sample_fhirpath
):
    """Test that dependent groups are processed during iteration."""
    rule = Rule(rule_definition_with_dependents, None)

    # Mock source for iteration
    mock_source = Mock()
    mock_source.variable = "patient"
    mock_source.iteration_count = 1
    mock_source.process = Mock()
    rule.sources = [mock_source]

    # Mock the _process_dependent_group method
    with patch.object(rule, "_process_dependent_group") as mock_process_dependent:
        mapping_scope.resolve_fhirpath = Mock(return_value=sample_fhirpath)

        rule.process(mapping_scope)

        # Should call dependent processing
        mock_process_dependent.assert_called_once()


def test_process_with_nested_rules(
    rule_definition_with_nested_rules, mapping_scope, sample_fhirpath
):
    """Test that nested rules are processed during iteration."""
    rule = Rule(rule_definition_with_nested_rules, None)

    # Mock source for iteration
    mock_source = Mock()
    mock_source.variable = "patient"
    mock_source.iteration_count = 1
    mock_source.process = Mock()
    rule.sources = [mock_source]

    # Mock nested rule process method
    rule.nested_rules[0].process = Mock(return_value=mapping_scope)

    mapping_scope.resolve_fhirpath = Mock(return_value=sample_fhirpath)

    rule.process(mapping_scope)

    # Should call nested rule processing
    rule.nested_rules[0].process.assert_called_once()


def test_process_finishes_processing_rule_in_scope(
    minimal_rule_definition, mapping_scope
):
    """Test that rule processing is properly finished in scope."""
    rule = Rule(minimal_rule_definition, None)

    with patch.object(mapping_scope, "finish_processing_rule") as mock_finish:
        rule.process(mapping_scope)
        mock_finish.assert_called_once_with("test-rule")


# ============================================================================
# Rule._process_dependent_group() Tests
# ============================================================================


def test_process_dependent_group_not_found_raises_error(
    minimal_rule_definition, mapping_scope
):
    """Test error when dependent group is not found."""
    rule = Rule(minimal_rule_definition, None)

    dependent = Mock()
    dependent.name = "missing-group"

    mapping_scope.resolve_symbol = Mock(return_value=None)

    with pytest.raises(
        RuleProcessingError,
        match="Dependent group or rule 'missing-group' not found",
    ):
        rule._process_dependent_group(dependent, mapping_scope)


def test_process_dependent_group_r4_variables(minimal_rule_definition, mapping_scope):
    """Test processing dependent group with R4/R4B-style variables."""
    from fhircraft.fhir.mapper.engine.group import Group

    rule = Rule(minimal_rule_definition, None)

    # Create dependent with variable attribute (R4/R4B style)
    dependent = Mock()
    dependent.name = "test_group"
    dependent.parameter = None  # No parameter attribute for R4/R4B
    dependent.variable = ["var1", "var2"]

    # Mock group and scope
    mock_group = Mock(spec=Group)
    mapping_scope.resolve_symbol = Mock(return_value=mock_group)
    mapping_scope.resolve_fhirpath = Mock(side_effect=lambda x: f"resolved_{x}")

    rule._process_dependent_group(dependent, mapping_scope)

    # Should call group.process with resolved variables
    mock_group.process.assert_called_once_with(
        mapping_scope, ["resolved_var1", "resolved_var2"], is_dependent=True
    )


# ============================================================================
# Rule Properties Tests
# ============================================================================


@pytest.fixture
def target_with_first_list_mode():
    """Target with 'first' list mode."""
    target = Mock()
    target.has_list_mode = Mock(return_value=False)
    target.has_list_mode.side_effect = lambda mode: mode == "first"
    return target


@pytest.fixture
def target_with_last_list_mode():
    """Target with 'last' list mode."""
    target = Mock()
    target.has_list_mode = Mock(return_value=False)
    target.has_list_mode.side_effect = lambda mode: mode == "last"
    return target


@pytest.fixture
def target_without_list_modes():
    """Target without special list modes."""
    target = Mock()
    target.has_list_mode = Mock(return_value=False)
    return target


def test_has_first_target_true(minimal_rule_definition, target_with_first_list_mode):
    """Test has_first_target returns True when rule has target with 'first' list mode."""
    rule = Rule(minimal_rule_definition, None)
    rule.targets = [target_with_first_list_mode]

    assert rule.has_first_target is True

    def test_has_first_target_false(
        self, minimal_rule_definition, target_without_list_modes
    ):
        """Test has_first_target returns False when rule has no targets with 'first' list mode."""
        rule = Rule(minimal_rule_definition, None)
        rule.targets = [target_without_list_modes]

        assert rule.has_first_target is False


def test_has_last_target_true(minimal_rule_definition, target_with_last_list_mode):
    """Test has_last_target returns True when rule has target with 'last' list mode."""
    rule = Rule(minimal_rule_definition, None)
    rule.targets = [target_with_last_list_mode]

    assert rule.has_last_target is True


def test_has_last_target_false(minimal_rule_definition, target_without_list_modes):
    """Test has_last_target returns False when rule has no targets with 'last' list mode."""
    rule = Rule(minimal_rule_definition, None)
    rule.targets = [target_without_list_modes]

    assert rule.has_last_target is False


def test_multiple_targets_mixed_list_modes(
    minimal_rule_definition,
    target_with_first_list_mode,
    target_with_last_list_mode,
    target_without_list_modes,
):
    """Test properties work correctly with multiple targets having different list modes."""
    rule = Rule(minimal_rule_definition, None)
    rule.targets = [
        target_without_list_modes,
        target_with_first_list_mode,
        target_with_last_list_mode,
    ]

    assert rule.has_first_target is True
    assert rule.has_last_target is True


def test_no_targets(minimal_rule_definition):
    """Test properties return False when rule has no targets."""
    rule = Rule(minimal_rule_definition, None)
    rule.targets = []

    assert rule.has_first_target is False
    assert rule.has_last_target is False
