"""
Comprehensive test suite for the RuleSource class.

This module contains unit tests for the RuleSource class and all its methods,
including edge cases, error conditions, and various scenarios.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch

from fhircraft.fhir.mapper.engine.source import RuleSource
from fhircraft.fhir.mapper.engine.exceptions import (
    SourceAssertionError,
    SourceProcessingError,
    SourceConditionError,
    SourceTypeError,
)
from fhircraft.fhir.path import engine as fp
from fhircraft.fhir.path.engine.core import FHIRPath


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_source_definition():
    """Base mock source definition with common defaults."""
    source = Mock()
    source.context = "Patient"
    source.variable = "patient"
    source.element = None
    source.condition = None
    source.check = None
    source.type = None
    source.listMode = None
    source.min = None
    source.max = None
    return source


@pytest.fixture
def mock_rule():
    """Mock parent rule."""
    return Mock()


@pytest.fixture
def mock_scope():
    """Mock mapping scope with common setup."""
    scope = Mock()
    scope.get_instances.return_value = {}
    return scope


@pytest.fixture
def mock_fhirpath():
    """Mock FHIRPath object with common methods."""
    path = Mock(spec=FHIRPath)
    path.count.return_value = 1
    path._invoke.return_value = path  # Default to returning self
    path.single.return_value = True
    return path


@pytest.fixture
def rule_source_factory():
    """Factory for creating RuleSource instances with mocked dependencies."""

    def _create_rule_source(source_mock, rule_mock, patch_literals=True):
        if patch_literals:
            with patch("fhircraft.fhir.path.engine.Literal"):
                return RuleSource(source_mock, rule_mock)
        else:
            return RuleSource(source_mock, rule_mock)

    return _create_rule_source


@pytest.fixture
def processed_rule_source(
    rule_source_factory, mock_source_definition, mock_rule, mock_scope, mock_fhirpath
):
    """Rule source that has been successfully processed."""
    mock_scope.resolve_fhirpath.return_value = mock_fhirpath
    rule_source = rule_source_factory(mock_source_definition, mock_rule)

    # Mock all condition checks to pass
    with (
        patch.object(rule_source, "_apply_list_mode"),
        patch.object(rule_source, "_check_type_condition", return_value=True),
        patch.object(rule_source, "_check_where_condition", return_value=True),
        patch.object(rule_source, "_check_assertion_condition", return_value=True),
        patch.object(rule_source, "_validate_cardinality", return_value=True),
    ):

        rule_source.process(mock_scope)

    return rule_source


# ============================================================================
# PROCESS METHOD TESTS
# ============================================================================


class TestRuleSourceProcess:
    """Tests for the main process method."""

    def test_process_success_basic(
        self,
        mock_source_definition,
        mock_rule,
        mock_scope,
        mock_fhirpath,
        rule_source_factory,
    ):
        """Test basic successful processing."""
        mock_scope.resolve_fhirpath.return_value = mock_fhirpath
        rule_source = rule_source_factory(mock_source_definition, mock_rule)

        with (
            patch.object(rule_source, "_apply_list_mode"),
            patch.object(rule_source, "_check_type_condition", return_value=True),
            patch.object(rule_source, "_check_where_condition", return_value=True),
            patch.object(rule_source, "_check_assertion_condition", return_value=True),
            patch.object(rule_source, "_validate_cardinality", return_value=True),
        ):

            rule_source.process(mock_scope)

            mock_scope.resolve_fhirpath.assert_called_once_with("Patient")
            mock_scope.define_variable.assert_called_once_with("patient", mock_fhirpath)
            assert rule_source.resolved_path == mock_fhirpath
            assert rule_source.iteration_count == 1

    def test_process_with_element_path(
        self,
        mock_source_definition,
        mock_rule,
        mock_scope,
        mock_fhirpath,
        rule_source_factory,
    ):
        """Test processing with element path."""
        mock_source_definition.element = "name"
        mock_element_path = Mock(spec=FHIRPath)
        mock_element_path.count.return_value = 2
        mock_fhirpath._invoke.return_value = mock_element_path
        mock_scope.resolve_fhirpath.return_value = mock_fhirpath

        rule_source = rule_source_factory(mock_source_definition, mock_rule)

        with (
            patch.object(rule_source, "_apply_list_mode"),
            patch.object(rule_source, "_check_type_condition", return_value=True),
            patch.object(rule_source, "_check_where_condition", return_value=True),
            patch.object(rule_source, "_check_assertion_condition", return_value=True),
            patch.object(rule_source, "_validate_cardinality", return_value=True),
        ):

            rule_source.process(mock_scope)

            mock_fhirpath._invoke.assert_called_once()
            assert rule_source.resolved_path == mock_element_path
            assert rule_source.iteration_count == 2

    @pytest.mark.parametrize(
        "condition_method,exception_class,error_pattern",
        [
            ("_check_type_condition", SourceTypeError, "Source type condition not met"),
            (
                "_check_where_condition",
                SourceConditionError,
                "Source condition not met",
            ),
            (
                "_check_assertion_condition",
                SourceAssertionError,
                "Source assertion failed",
            ),
            (
                "_validate_cardinality",
                SourceProcessingError,
                "Cardinality constraints violated",
            ),
        ],
    )
    def test_process_condition_failures(
        self,
        mock_source_definition,
        mock_rule,
        mock_scope,
        mock_fhirpath,
        rule_source_factory,
        condition_method,
        exception_class,
        error_pattern,
    ):
        """Test processing failures for various condition checks."""
        mock_scope.resolve_fhirpath.return_value = mock_fhirpath
        rule_source = rule_source_factory(mock_source_definition, mock_rule)

        # Mock all conditions to pass except the one being tested
        condition_patches = {
            "_apply_list_mode": Mock(),
            "_check_type_condition": Mock(return_value=True),
            "_check_where_condition": Mock(return_value=True),
            "_check_assertion_condition": Mock(return_value=True),
            "_validate_cardinality": Mock(return_value=True),
        }
        condition_patches[condition_method] = Mock(return_value=False)

        with patch.multiple(rule_source, **condition_patches):
            with pytest.raises(exception_class, match=error_pattern):
                rule_source.process(mock_scope)

    def test_process_fails_when_context_not_found(
        self, mock_source_definition, mock_rule, mock_scope, rule_source_factory
    ):
        """Test processing fails when context cannot be resolved."""
        mock_scope.resolve_fhirpath.return_value = None
        rule_source = rule_source_factory(mock_source_definition, mock_rule)

        with pytest.raises(
            SourceProcessingError, match="Source context Patient not found"
        ):
            rule_source.process(mock_scope)

    @pytest.mark.parametrize("count_return", [None, 0])
    def test_process_handles_zero_iteration_count(
        self,
        mock_source_definition,
        mock_rule,
        mock_scope,
        mock_fhirpath,
        rule_source_factory,
        count_return,
    ):
        """Test processing handles zero/None iteration count properly."""
        mock_fhirpath.count.return_value = count_return
        mock_scope.resolve_fhirpath.return_value = mock_fhirpath
        rule_source = rule_source_factory(mock_source_definition, mock_rule)

        with (
            patch.object(rule_source, "_apply_list_mode"),
            patch.object(rule_source, "_check_type_condition", return_value=True),
            patch.object(rule_source, "_check_where_condition", return_value=True),
            patch.object(rule_source, "_check_assertion_condition", return_value=True),
            patch.object(rule_source, "_validate_cardinality", return_value=True),
        ):

            rule_source.process(mock_scope)

            assert rule_source.iteration_count == 0


# ============================================================================
# _check_type_condition() Tests
# ============================================================================


@pytest.mark.parametrize(
    "type_name,value,expected",
    [
        ("string", "string-value", True),
        ("string", 123, False),
        ("integer", "123", True),
        ("integer", "string", False),
        ("boolean", "true", True),
        ("boolean", 123, False),
    ],
)
def test_check_type_condition_various_types(
    processed_rule_source, type_name, value, expected
):
    """Test type condition check with various types."""
    processed_rule_source.definition.type = type_name
    processed_rule_source.resolved_path = fp.Element("value")

    scope = MagicMock()
    scope.get_instances.return_value = {"value": value}
    assert processed_rule_source._check_type_condition(scope) == expected


def test_check_type_condition_no_type(processed_rule_source, mock_scope):
    """Test type condition check when no type is specified."""
    processed_rule_source.definition.type = None
    assert processed_rule_source._check_type_condition(mock_scope) == True


# ============================================================================
# _validate_cardinality() Tests
# ============================================================================


@pytest.mark.parametrize(
    "min_card,max_card,iteration_count,expected",
    [
        (None, None, 5, True),
        (2, None, 3, True),
        (5, None, 3, False),
        (None, "5", 3, True),
        (None, "2", 5, False),
        (None, "*", 1000, True),
        (2, "5", 3, True),
        (5, "10", 3, False),
        (1, "3", 5, False),
    ],
)
def test_validate_cardinality(
    rule_source_factory,
    mock_source_definition,
    mock_rule,
    min_card,
    max_card,
    iteration_count,
    expected,
):
    """Test cardinality validation when no constraints are specified."""
    mock_source_definition.min = min_card
    mock_source_definition.max = max_card
    source = rule_source_factory(mock_source_definition, mock_rule)
    source.iteration_count = iteration_count
    assert source._validate_cardinality() is expected


# ============================================================================
# _apply_list_mode() Tests
# ============================================================================


@pytest.mark.parametrize(
    "list_mode,resolved_fhirpath,expected_fhirpath",
    [
        ("first", fp.Element("A"), fp.Invocation(fp.Element("A"), fp.First())),
        ("last", fp.Element("A"), fp.Invocation(fp.Element("A"), fp.Last())),
        ("not_first", fp.Element("A"), fp.Invocation(fp.Element("A"), fp.Tail())),
        ("only_one", fp.Element("A"), fp.Invocation(fp.Element("A"), fp.Single())),
        (
            "not_last",
            fp.Element("A"),
            fp.Invocation(
                fp.Element("A"), fp.Exclude(fp.Invocation(fp.Element("A"), fp.Last()))
            ),
        ),
    ],
)
def test_apply_simple_mode(
    mock_source_definition,
    rule_source_factory,
    mock_rule,
    list_mode,
    resolved_fhirpath,
    expected_fhirpath,
):
    """Test application of simple list modes."""
    mock_source_definition.listMode = list_mode
    rule_source = rule_source_factory(mock_source_definition, mock_rule)
    rule_source.resolved_path = resolved_fhirpath

    rule_source._apply_list_mode()

    assert str(rule_source.resolved_path) == str(expected_fhirpath)


def test_apply_list_mode_unsupported(
    mock_source_definition, mock_rule, rule_source_factory
):
    """Test unsupported list mode raises error."""
    mock_source_definition.listMode = "unsupported_mode"
    rule_source = rule_source_factory(mock_source_definition, mock_rule)
    rule_source.resolved_path = fp.Element("A")

    with pytest.raises(SourceProcessingError):
        rule_source._apply_list_mode()
