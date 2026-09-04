import pytest
from unittest.mock import Mock, patch
from pydantic import BaseModel

from fhircraft.fhir.mapper.engine.rule import Rule
from fhircraft.fhir.mapper.engine.scope import MappingScope
from fhircraft.exceptions import (
    MapperRuleProcessingError,
    MapperExecutionError,
    MapperDigestionError,
)
from fhircraft.fhir.resources.datatypes.R5.core.structure_map import (
    StructureMapGroupRule,
    StructureMapGroupRuleDependentParameter,
    StructureMapGroupRuleSource,
    StructureMapGroupRuleTarget,
    StructureMapGroupRuleDependent,
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
def minimal_rule_definition():
    """Minimal rule definition with just a name."""
    return StructureMapGroupRule(
        name="test-rule",
        source=[
            StructureMapGroupRuleSource(context="src", variable="a", element=None),
        ],
        target=None,
        rule=None,
        dependent=None,
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
        source=[
            StructureMapGroupRuleSource(
                context="Patient", variable="src", element=None
            ),
        ],
        target=[target1, target2],
        rule=None,
        dependent=None,
    )


@pytest.fixture
def rule_definition_with_nested_rules():
    """Rule definition with nested rule configurations."""
    nested_rule = StructureMapGroupRule(
        name="nested-rule",
        source=[
            StructureMapGroupRuleSource(
                context="Patient", variable="src", element=None
            ),
        ],
        target=None,
        rule=None,
        dependent=None,
    )
    return StructureMapGroupRule(
        name="parent-rule",
        source=[
            StructureMapGroupRuleSource(
                context="Patient", variable="src", element=None
            ),
        ],
        target=None,
        rule=[nested_rule],
        dependent=None,
    )


@pytest.fixture
def rule_definition_with_dependents():
    """Rule definition with dependent configurations."""
    dependent = StructureMapGroupRuleDependent(
        name="dependent-group",
        parameter=[StructureMapGroupRuleDependentParameter(valueId="testVar")],
    )
    return StructureMapGroupRule(
        name="rule-with-dependents",
        source=[
            StructureMapGroupRuleSource(
                context="Patient", variable="src", element=None
            ),
        ],
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


# ============================================================================
# Rule.__init__()
# ============================================================================


def test_init__minimal(minimal_rule_definition, mock_parent_group):
    """Test initialization with minimal rule definition."""
    rule = Rule(minimal_rule_definition, mock_parent_group)

    assert rule.definition == minimal_rule_definition
    assert rule.name == "test-rule"
    assert rule.parent_group == mock_parent_group
    assert len(rule.targets) == 0
    assert len(rule.nested_rules) == 0
    assert len(rule.dependents) == 0


def test_init__creates_sources(rule_definition_with_sources, mock_parent_group):
    rule = Rule(rule_definition_with_sources, mock_parent_group)

    assert len(rule.sources) == 2

    # Check sources were initialized with correct parameters
    assert rule.sources[0].definition == rule_definition_with_sources.source[0]
    assert rule.sources[0].parent_rule == rule
    assert rule.sources[1].definition == rule_definition_with_sources.source[1]
    assert rule.sources[1].parent_rule == rule


def test_init__creates_targets(rule_definition_with_targets, mock_parent_group):
    rule = Rule(rule_definition_with_targets, mock_parent_group)

    assert len(rule.targets) == 2

    # Check targets were initialized with correct parameters
    assert rule.targets[0].definition == rule_definition_with_targets.target[0]
    assert rule.targets[0].parent_rule == rule
    assert rule.targets[1].definition == rule_definition_with_targets.target[1]
    assert rule.targets[1].parent_rule == rule


def test_init__creates_nested_rules(
    rule_definition_with_nested_rules, mock_parent_group
):
    rule = Rule(rule_definition_with_nested_rules, mock_parent_group)

    assert len(rule.nested_rules) == 1
    assert isinstance(rule.nested_rules[0], Rule)
    assert rule.nested_rules[0].name == "nested-rule"
    assert rule.nested_rules[0].parent_group == mock_parent_group


def test_init__creates_dependents(rule_definition_with_dependents, mock_parent_group):
    rule = Rule(rule_definition_with_dependents, mock_parent_group)

    assert len(rule.dependents) == 1
    assert rule.dependents[0] == rule_definition_with_dependents.dependent[0]


def test_init__raises_error_for_dependent_without_name(mock_parent_group):
    dependent = StructureMapGroupRuleDependent.model_construct(
        name=None, variable=["var1"]
    )
    rule_def = StructureMapGroupRule.model_construct(
        name="rule-invalid-dependent",
        source=None,
        target=None,
        rule=None,
        dependent=[dependent],
    )

    with pytest.raises(
        MapperDigestionError, match="Dependent rule or group must have a name"
    ):
        Rule(rule_def, mock_parent_group)


# ============================================================================
# Rule.process()
# ============================================================================


def test_process__iterates_over_source_collections(
    rule_definition_with_sources,
    mapping_scope,
    sample_fhirpath,
):
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

    rule.process(mapping_scope)

    # Should process target for each iteration
    assert mock_target.process.call_count == 3
    assert mock_source.process.called


def test_process__propagates_errors_from_sources(
    rule_definition_with_sources, mapping_scope
):
    """Test that MapperRuleProcessingError from sources is propagated."""
    rule = Rule(rule_definition_with_sources, None)

    # Mock source to raise MapperRuleProcessingError
    mock_source = Mock()
    mock_source.variable = "patient"
    mock_source.process.side_effect = MapperRuleProcessingError("Test assertion error")
    rule.sources = [mock_source]

    with pytest.raises(
        MapperRuleProcessingError,
        match="Source assertion failed for rule rules-with-sources",
    ):
        rule.process(mapping_scope)


def test_process__raises_error_for_source_variable_not_in_scope(
    rule_definition_with_sources, mapping_scope
):
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
        MapperRuleProcessingError, match="Source variable missing-var not found"
    ):
        rule.process(mapping_scope)


def test_process__with_dependent_groups(
    rule_definition_with_dependents, mapping_scope, sample_fhirpath
):
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


def test_process__with_nested_rules(
    rule_definition_with_nested_rules, mapping_scope, sample_fhirpath
):
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


# ============================================================================
# Rule._process_dependent_group()
# ============================================================================


def test_process_dependent_group__raises_error_if_not_found(
    minimal_rule_definition, mapping_scope
):
    """Test error when dependent group is not found."""
    rule = Rule(minimal_rule_definition, None)

    dependent = Mock()
    dependent.name = "missing-group"

    mapping_scope.resolve_symbol = Mock(return_value=None)

    with pytest.raises(
        MapperRuleProcessingError,
        match="Dependent group or rule 'missing-group' not found",
    ):
        rule._process_dependent_group(dependent, mapping_scope)


def test_process_dependent_group__with_r4_legacy_variables(
    minimal_rule_definition, mapping_scope
):
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
# Rule.has_first_target/has_last_target
# ============================================================================


def test_has_first_target__true(minimal_rule_definition, target_with_first_list_mode):
    rule = Rule(minimal_rule_definition, None)
    rule.targets = [target_with_first_list_mode]

    assert rule.has_first_target is True


def test_has_first_target__false(minimal_rule_definition, target_without_list_modes):
    rule = Rule(minimal_rule_definition, None)
    rule.targets = [target_without_list_modes]

    assert rule.has_first_target is False


def test_has_last_target__true(minimal_rule_definition, target_with_last_list_mode):
    rule = Rule(minimal_rule_definition, None)
    rule.targets = [target_with_last_list_mode]

    assert rule.has_last_target is True


def test_has_last_target__false(minimal_rule_definition, target_without_list_modes):
    rule = Rule(minimal_rule_definition, None)
    rule.targets = [target_without_list_modes]

    assert rule.has_last_target is False


def test_has_last_first_target__mixed_list_modes(
    minimal_rule_definition,
    target_with_first_list_mode,
    target_with_last_list_mode,
    target_without_list_modes,
):
    rule = Rule(minimal_rule_definition, None)
    rule.targets = [
        target_without_list_modes,
        target_with_first_list_mode,
        target_with_last_list_mode,
    ]

    assert rule.has_first_target is True
    assert rule.has_last_target is True


def test_has_last_first_target__no_targets(minimal_rule_definition):
    rule = Rule(minimal_rule_definition, None)
    rule.targets = []

    assert rule.has_first_target is False
    assert rule.has_last_target is False
