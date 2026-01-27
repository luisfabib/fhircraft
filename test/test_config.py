import warnings
from contextlib import contextmanager

import pytest

from fhircraft.config import (
    FhircraftConfig,
    ValidationConfig,
    configure,
    disable_constraint,
    enable_constraint,
    get_config,
    load_config_from_env,
    reset_config,
    set_config,
    with_config,
)


@pytest.fixture(autouse=True)
def reset_config_after_test():
    """Reset configuration after each test to ensure isolation."""
    yield
    reset_config()


class TestValidationConfig:
    """Tests for ValidationConfig dataclass."""

    def test_default_validation_config(self):
        """Test default ValidationConfig values."""
        config = ValidationConfig()
        assert config.disable_warnings is False
        assert config.disabled_constraints == set()
        assert config.disable_warning_severity is False
        assert config.disable_errors is False
        assert config.mode == "strict"

    def test_validation_config_with_values(self):
        """Test ValidationConfig with custom values."""
        config = ValidationConfig(
            disable_warnings=True,
            disabled_constraints={"dom-6", "sdf-0"},
            mode="lenient",
        )
        assert config.disable_warnings is True
        assert config.disabled_constraints == {"dom-6", "sdf-0"}
        assert config.mode == "lenient"


class TestFHIRCraftConfig:
    """Tests for FhircraftConfig dataclass."""

    def test_default_fhircraft_config(self):
        """Test default FhircraftConfig values."""
        config = FhircraftConfig()
        assert isinstance(config.validation, ValidationConfig)
        assert config.validation.mode == "strict"

    def test_fhircraft_config_with_validation(self):
        """Test FhircraftConfig with custom ValidationConfig."""
        validation = ValidationConfig(disable_warnings=True)
        config = FhircraftConfig(validation=validation)
        assert config.validation.disable_warnings is True

    def test_fhircraft_config_with_dict(self):
        """Test FhircraftConfig converts dict to ValidationConfig."""
        config = FhircraftConfig(
            validation={"disable_warnings": True, "mode": "lenient"}
        )
        assert isinstance(config.validation, ValidationConfig)
        assert config.validation.disable_warnings is True
        assert config.validation.mode == "lenient"


class TestConfigAccess:
    """Tests for get_config and set_config functions."""

    def test_get_default_config(self):
        """Test getting default configuration."""
        config = get_config()
        assert isinstance(config, FhircraftConfig)
        assert config.validation.mode == "strict"

    def test_set_config(self):
        """Test setting global configuration."""
        new_config = FhircraftConfig(validation=ValidationConfig(disable_warnings=True))
        set_config(new_config)

        config = get_config()
        assert config.validation.disable_warnings is True

    def test_config_persistence(self):
        """Test that set_config persists across multiple get_config calls."""
        configure(disable_validation_warnings=True)

        assert get_config().validation.disable_warnings is True
        assert get_config().validation.disable_warnings is True


class TestConfigureFunction:
    """Tests for the configure() convenience function."""

    def test_configure_disable_warnings(self):
        """Test configuring to disable warnings."""
        configure(disable_validation_warnings=True)

        config = get_config()
        assert config.validation.disable_warnings is True

    def test_configure_validation_mode(self):
        """Test configuring validation mode."""
        configure(validation_mode="lenient")

        config = get_config()
        assert config.validation.mode == "lenient"

    def test_configure_disabled_constraints(self):
        """Test configuring disabled constraints."""
        configure(disabled_constraints={"dom-6", "sdf-0"})

        config = get_config()
        assert config.validation.disabled_constraints == {"dom-6", "sdf-0"}

    def test_configure_multiple_options(self):
        """Test configuring multiple options at once."""
        configure(
            disable_validation_warnings=True,
            validation_mode="lenient",
            disabled_constraints={"dom-6"},
        )

        config = get_config()
        assert config.validation.disable_warnings is True
        assert config.validation.mode == "lenient"
        assert config.validation.disabled_constraints == {"dom-6"}

    def test_configure_disable_errors(self):
        """Test configuring to disable errors."""
        configure(disable_validation_errors=True)

        config = get_config()
        assert config.validation.disable_errors is True

    def test_configure_disable_warning_severity(self):
        """Test configuring to disable warning severity only."""
        configure(disable_warning_severity=True)

        config = get_config()
        assert config.validation.disable_warning_severity is True


class TestWithConfigContextManager:
    """Tests for the with_config() context manager."""

    def test_with_config_temporary_change(self):
        """Test that with_config changes are temporary."""
        # Initial state
        assert get_config().validation.disable_warnings is False

        # Inside context
        with with_config(disable_validation_warnings=True):
            assert get_config().validation.disable_warnings is True

        # After context
        assert get_config().validation.disable_warnings is False

    def test_with_config_nested(self):
        """Test nested with_config contexts."""
        with with_config(validation_mode="lenient"):
            assert get_config().validation.mode == "lenient"

            with with_config(validation_mode="skip"):
                assert get_config().validation.mode == "skip"

            assert get_config().validation.mode == "lenient"

        assert get_config().validation.mode == "strict"

    def test_with_config_exception_handling(self):
        """Test that config is restored even if exception occurs."""
        assert get_config().validation.mode == "strict"

        try:
            with with_config(validation_mode="skip"):
                assert get_config().validation.mode == "skip"
                raise ValueError("Test exception")
        except ValueError:
            pass

        # Config should be restored
        assert get_config().validation.mode == "strict"

    def test_with_config_returns_config(self):
        """Test that with_config yields the new configuration."""
        with with_config(disable_validation_warnings=True) as config:
            assert isinstance(config, FhircraftConfig)
            assert config.validation.disable_warnings is True


class TestConstraintFunctions:
    """Tests for disable_constraint and enable_constraint functions."""

    def test_disable_single_constraint(self):
        """Test disabling a single constraint."""
        disable_constraint("dom-6")

        config = get_config()
        assert "dom-6" in config.validation.disabled_constraints

    def test_disable_multiple_constraints(self):
        """Test disabling multiple constraints at once."""
        disable_constraint("dom-6", "sdf-0", "ele-1")

        config = get_config()
        assert "dom-6" in config.validation.disabled_constraints
        assert "sdf-0" in config.validation.disabled_constraints
        assert "ele-1" in config.validation.disabled_constraints

    def test_enable_constraint(self):
        """Test enabling a previously disabled constraint."""
        disable_constraint("dom-6")
        assert "dom-6" in get_config().validation.disabled_constraints

        enable_constraint("dom-6")
        assert "dom-6" not in get_config().validation.disabled_constraints

    def test_enable_multiple_constraints(self):
        """Test enabling multiple constraints."""
        disable_constraint("dom-6", "sdf-0", "ele-1")
        enable_constraint("dom-6", "ele-1")

        config = get_config()
        assert "dom-6" not in config.validation.disabled_constraints
        assert "sdf-0" in config.validation.disabled_constraints
        assert "ele-1" not in config.validation.disabled_constraints

    def test_enable_nonexistent_constraint(self):
        """Test that enabling a nonexistent constraint doesn't raise error."""
        enable_constraint("nonexistent")
        # Should not raise any error


class TestResetConfig:
    """Tests for reset_config function."""

    def test_reset_config(self):
        """Test that reset_config returns to defaults."""
        configure(
            disable_validation_warnings=True,
            validation_mode="skip",
            disabled_constraints={"dom-6"},
        )

        reset_config()

        config = get_config()
        assert config.validation.disable_warnings is False
        assert config.validation.mode == "strict"
        assert config.validation.disabled_constraints == set()


class TestLoadConfigFromEnv:
    """Tests for load_config_from_env function."""

    def test_load_disable_warnings_from_env(self, monkeypatch):
        """Test loading FHIRCRAFT_DISABLE_WARNINGS from environment."""
        monkeypatch.setenv("FHIRCRAFT_DISABLE_WARNINGS", "true")

        load_config_from_env()

        assert get_config().validation.disable_warnings is True

    def test_load_validation_mode_from_env(self, monkeypatch):
        """Test loading FHIRCRAFT_VALIDATION_MODE from environment."""
        monkeypatch.setenv("FHIRCRAFT_VALIDATION_MODE", "lenient")

        load_config_from_env()

        assert get_config().validation.mode == "lenient"

    def test_load_disabled_constraints_from_env(self, monkeypatch):
        """Test loading FHIRCRAFT_DISABLED_CONSTRAINTS from environment."""
        monkeypatch.setenv("FHIRCRAFT_DISABLED_CONSTRAINTS", "dom-6,sdf-0,ele-1")

        load_config_from_env()

        config = get_config()
        assert "dom-6" in config.validation.disabled_constraints
        assert "sdf-0" in config.validation.disabled_constraints
        assert "ele-1" in config.validation.disabled_constraints

    def test_load_all_from_env(self, monkeypatch):
        """Test loading all environment variables."""
        monkeypatch.setenv("FHIRCRAFT_DISABLE_WARNINGS", "true")
        monkeypatch.setenv("FHIRCRAFT_VALIDATION_MODE", "skip")
        monkeypatch.setenv("FHIRCRAFT_DISABLED_CONSTRAINTS", "dom-6")

        load_config_from_env()

        config = get_config()
        assert config.validation.disable_warnings is True
        assert config.validation.mode == "skip"
        assert "dom-6" in config.validation.disabled_constraints

    def test_load_invalid_validation_mode(self, monkeypatch):
        """Test that invalid validation mode is ignored."""
        monkeypatch.setenv("FHIRCRAFT_VALIDATION_MODE", "invalid")

        load_config_from_env()

        # Should remain default
        assert get_config().validation.mode == "strict"

    def test_load_with_no_env_vars(self):
        """Test that load_config_from_env works with no variables set."""
        # Should not raise any errors
        load_config_from_env()
        assert get_config().validation.mode == "strict"


class TestValidationIntegration:
    """Tests for integration with validation system."""

    def test_validation_respects_disabled_warnings(self):
        """Test that validators respect disable_warnings config."""
        from fhircraft.fhir.resources.validators import (
            _validate_FHIR_element_constraint,
        )

        configure(disable_validation_warnings=True)

        # This would normally emit a warning, but should be suppressed
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = _validate_FHIR_element_constraint(
                value={"test": "value"},
                instance=None,
                expression="false",  # Always fails
                human="Test constraint",
                key="test-1",
                severity="warning",
            )
            # Should not have any warnings
            assert (
                len(
                    [
                        warning
                        for warning in w
                        if "Test constraint" in str(warning.message)
                    ]
                )
                == 0
            )

    def test_validation_respects_disabled_constraints(self):
        """Test that validators respect disabled_constraints config."""
        from fhircraft.fhir.resources.validators import (
            _validate_FHIR_element_constraint,
        )

        disable_constraint("test-1")

        # This constraint should be skipped
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = _validate_FHIR_element_constraint(
                value={"test": "value"},
                instance=None,
                expression="false",
                human="Test constraint",
                key="test-1",
                severity="warning",
            )
            assert (
                len(
                    [
                        warning
                        for warning in w
                        if "Test constraint" in str(warning.message)
                    ]
                )
                == 0
            )

    def test_validation_mode_skip(self):
        """Test that mode='skip' disables all validation."""
        from fhircraft.fhir.resources.validators import (
            _validate_FHIR_element_constraint,
        )

        configure(validation_mode="skip")

        # Should not raise assertion error even though expression fails
        result = _validate_FHIR_element_constraint(
            value={"test": "value"},
            instance=None,
            expression="false",
            human="Test constraint",
            key="test-1",
            severity="error",
        )
        # Should return value unchanged
        assert result == {"test": "value"}

    def test_validation_lenient_mode(self):
        """Test that lenient mode converts errors to warnings."""
        from fhircraft.fhir.resources.validators import (
            _validate_FHIR_element_constraint,
        )

        configure(validation_mode="lenient")

        # This would normally raise AssertionError, but should emit warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = _validate_FHIR_element_constraint(
                value={"test": "value"},
                instance=None,
                expression="false",
                human="Test constraint",
                key="test-1",
                severity="error",
            )
            # Should have emitted a warning instead of raising
            assert any("Test constraint" in str(warning.message) for warning in w)

    def test_validation_with_context_manager(self):
        """Test validation with temporary config via context manager."""
        from fhircraft.fhir.resources.validators import (
            _validate_FHIR_element_constraint,
        )

        # Default: warnings enabled
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Temporarily disable warnings
            with with_config(disable_validation_warnings=True):
                result = _validate_FHIR_element_constraint(
                    value={"test": "value"},
                    instance=None,
                    expression="false",
                    human="Test in context",
                    key="test-2",
                    severity="warning",
                )
                # No warnings in this context
                assert (
                    len(
                        [
                            warning
                            for warning in w
                            if "Test in context" in str(warning.message)
                        ]
                    )
                    == 0
                )


class TestThreadSafety:
    """Tests for thread safety using contextvars."""

    def test_context_isolation(self):
        """Test that context changes are isolated."""
        from contextvars import copy_context

        configure(validation_mode="strict")

        def check_config_in_context():
            return get_config().validation.mode

        # Create a new context with different config
        ctx = copy_context()

        # Modify config in new context
        with with_config(validation_mode="lenient"):
            result_in_context = check_config_in_context()

        # Main context should be unchanged
        assert get_config().validation.mode == "strict"
