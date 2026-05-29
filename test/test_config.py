import warnings
import pytest

from fhircraft.config import (
    FhircraftConfig,
    configure,
    disable_constraint,
    enable_constraint,
    get_config,
    load_config_from_env,
    reset_config,
    override_config,
)
from fhircraft.fhir.resources.validators import (
    _validate_FHIR_element_constraint,
)
from fhircraft.fhir.terminology import TerminologyService


class _StubTerminologyService:
    """Minimal structural implementation of TerminologyService for config tests."""

    def codesystem_lookup(self, *, code, system=None, version=None):
        return None

    def validate_valueset_code(
        self, *, url=None, code=None, system=None, version=None, display=None
    ):
        return False

    def validate_codesystem_code(
        self, *, url=None, code=None, version=None, display=None
    ):
        return False

    def codesystem_subsumes(self, codeA, codeB, system=None, version=None):
        return None


@pytest.fixture(autouse=True)
def reset_config_after_test():
    """Reset configuration after each test to ensure isolation."""
    yield
    reset_config()


# =========================================================================
# FhircraftConfig dataclass
# =========================================================================


def test_default_config_values():
    config = FhircraftConfig()
    assert config.disable_validation_warnings is False
    assert config.disabled_fhir_constraints == frozenset()
    assert config.disable_fhir_warnings is False
    assert config.disable_fhir_errors is False
    assert config.mode == "strict"


def test_config_with_custom_values():
    config = FhircraftConfig(
        disable_validation_warnings=True,
        disabled_fhir_constraints={"dom-6", "sdf-0"},  # type: ignore
        mode="lenient",
    )
    assert config.disable_validation_warnings is True
    assert config.disabled_fhir_constraints == frozenset({"dom-6", "sdf-0"})
    assert config.mode == "lenient"


def test_default_fhircraft_config():
    config = FhircraftConfig()
    assert isinstance(config, FhircraftConfig)
    assert config.mode == "strict"


def test_fhircraft_config_with_custom_field():
    config = FhircraftConfig(disable_validation_warnings=True)
    assert config.disable_validation_warnings is True


def test_fhircraft_config_invalid_mode():
    with pytest.raises(ValueError, match="Invalid validation mode"):
        FhircraftConfig(mode="invalid")  # type: ignore


# =========================================================================
# get_config()
# =========================================================================


def test_get_config__get_default_config():
    config = get_config()
    assert isinstance(config, FhircraftConfig)
    assert config.mode == "strict"


def test_get_config__config_persistence():
    configure(disable_validation_warnings=True)

    assert get_config().disable_validation_warnings is True
    assert get_config().disable_validation_warnings is True


# =========================================================================
# configure()
# =========================================================================


def test_configure__disable_warnings():
    configure(disable_validation_warnings=True)

    config = get_config()
    assert config.disable_validation_warnings is True


def test_configure__validation_mode():
    configure(validation_mode="lenient")

    config = get_config()
    assert config.mode == "lenient"


def test_configure__disabled_constraints():
    configure(disabled_fhir_constraints={"dom-6", "sdf-0"})

    config = get_config()
    assert config.disabled_fhir_constraints == frozenset({"dom-6", "sdf-0"})


def test_configure__multiple_options():
    configure(
        disable_validation_warnings=True,
        validation_mode="lenient",
        disabled_fhir_constraints={"dom-6"},
    )

    config = get_config()
    assert config.disable_validation_warnings is True
    assert config.mode == "lenient"
    assert config.disabled_fhir_constraints == frozenset({"dom-6"})


def test_configure__disable_fhir_errors():
    configure(disable_fhir_errors=True)

    config = get_config()
    assert config.disable_fhir_errors is True


def test_configure__disable_fhir_warnings():
    configure(disable_fhir_warnings=True)

    config = get_config()
    assert config.disable_fhir_warnings is True


# =========================================================================
# override_config()
# =========================================================================


def test_override_config__temporary_change():
    # Initial state
    assert get_config().disable_validation_warnings is False

    # Inside context
    with override_config(disable_validation_warnings=True):
        assert get_config().disable_validation_warnings is True

    # After context
    assert get_config().disable_validation_warnings is False


def test_override_config__nested():
    with override_config(validation_mode="lenient"):
        assert get_config().mode == "lenient"

        with override_config(validation_mode="skip"):
            assert get_config().mode == "skip"

        assert get_config().mode == "lenient"

    assert get_config().mode == "strict"


def test_override_config__exception_handling():
    assert get_config().mode == "strict"

    try:
        with override_config(validation_mode="skip"):
            assert get_config().mode == "skip"
            raise ValueError("Test exception")
    except ValueError:
        pass

    # Config should be restored
    assert get_config().mode == "strict"


def test_override_config__returns_config():
    with override_config(disable_validation_warnings=True) as config:
        assert isinstance(config, FhircraftConfig)
        assert config.disable_validation_warnings is True


# =========================================================================
# disable_constraint()
# =========================================================================


def test_disable_single_constraint():
    disable_constraint("dom-6")
    config = get_config()
    assert "dom-6" in config.disabled_fhir_constraints


def test_disable_multiple_constraints():
    disable_constraint("dom-6", "sdf-0", "ele-1")
    config = get_config()
    assert "dom-6" in config.disabled_fhir_constraints
    assert "sdf-0" in config.disabled_fhir_constraints
    assert "ele-1" in config.disabled_fhir_constraints


def test_enable_constraint():
    disable_constraint("dom-6")
    assert "dom-6" in get_config().disabled_fhir_constraints

    enable_constraint("dom-6")
    assert "dom-6" not in get_config().disabled_fhir_constraints


def test_enable_multiple_constraints():
    disable_constraint("dom-6", "sdf-0", "ele-1")
    enable_constraint("dom-6", "ele-1")
    config = get_config()
    assert "dom-6" not in config.disabled_fhir_constraints
    assert "sdf-0" in config.disabled_fhir_constraints
    assert "ele-1" not in config.disabled_fhir_constraints


# =========================================================================
# enable_constraint()
# =========================================================================


def test_enable_nonexistent_constraint():
    enable_constraint("nonexistent")


# =========================================================================
# reset_config()
# =========================================================================


def test_reset_config():
    configure(
        disable_validation_warnings=True,
        validation_mode="skip",
        disabled_fhir_constraints={"dom-6"},  # type: ignore
    )
    reset_config()
    config = get_config()
    assert config.disable_validation_warnings is False
    assert config.mode == "strict"
    assert config.disabled_fhir_constraints == frozenset()


# =========================================================================
# load_config_from_env()
# =========================================================================


def test_load_disable_warnings_from_env(monkeypatch):
    monkeypatch.setenv("FHIRCRAFT_DISABLE_WARNINGS", "true")

    load_config_from_env()

    assert get_config().disable_validation_warnings is True


def test_load_validation_mode_from_env(monkeypatch):
    monkeypatch.setenv("FHIRCRAFT_VALIDATION_MODE", "lenient")

    load_config_from_env()

    assert get_config().mode == "lenient"


def test_load_disabled_constraints_from_env(monkeypatch):
    monkeypatch.setenv("FHIRCRAFT_DISABLED_CONSTRAINTS", "dom-6,sdf-0,ele-1")

    load_config_from_env()

    config = get_config()
    assert "dom-6" in config.disabled_fhir_constraints
    assert "sdf-0" in config.disabled_fhir_constraints
    assert "ele-1" in config.disabled_fhir_constraints


def test_load_all_from_env(monkeypatch):
    monkeypatch.setenv("FHIRCRAFT_DISABLE_WARNINGS", "true")
    monkeypatch.setenv("FHIRCRAFT_VALIDATION_MODE", "skip")
    monkeypatch.setenv("FHIRCRAFT_DISABLED_CONSTRAINTS", "dom-6")

    load_config_from_env()

    config = get_config()
    assert config.disable_validation_warnings is True
    assert config.mode == "skip"
    assert "dom-6" in config.disabled_fhir_constraints


def test_load_invalid_validation_mode(monkeypatch):
    monkeypatch.setenv("FHIRCRAFT_VALIDATION_MODE", "invalid")

    load_config_from_env()

    # Should remain default
    assert get_config().mode == "strict"


def test_load_with_no_env_vars():
    # Should not raise any errors
    load_config_from_env()
    assert get_config().mode == "strict"


# =========================================================================
# Terminology_service configuration
# =========================================================================


def test_default_config_terminology_service_is_none():
    assert get_config().terminology_service is None


def test_configure__sets_terminology_service():
    stub = _StubTerminologyService()
    configure(terminology_service=stub)
    assert get_config().terminology_service is stub


def test_configure__clears_terminology_service_with_none():
    stub = _StubTerminologyService()
    configure(terminology_service=stub)
    assert get_config().terminology_service is stub

    configure(terminology_service=None)
    assert get_config().terminology_service is None


def test_configure__omitting_terminology_service_preserves_existing():
    stub = _StubTerminologyService()
    configure(terminology_service=stub)

    # Call configure() for an unrelated setting — service must survive
    configure(disable_validation_warnings=True)

    assert get_config().terminology_service is stub


def test_override_config__terminology_service_restored():
    stub = _StubTerminologyService()

    with override_config(terminology_service=stub):
        assert get_config().terminology_service is stub

    assert get_config().terminology_service is None


def test_override_config__clears_terminology_service_within_context():
    stub = _StubTerminologyService()
    configure(terminology_service=stub)

    with override_config(terminology_service=None):
        assert get_config().terminology_service is None

    # Restored after context
    assert get_config().terminology_service is stub


def test_override_config__omitting_terminology_service_preserves_existing():
    stub = _StubTerminologyService()
    configure(terminology_service=stub)

    with override_config(disable_validation_warnings=True):
        assert get_config().terminology_service is stub

    assert get_config().terminology_service is stub


def test_terminology_service_isinstance_check():
    # TerminologyService is @runtime_checkable; structural implementations must pass
    stub = _StubTerminologyService()
    assert isinstance(stub, TerminologyService)


# =========================================================================
# Validation integration and thread safety tests
# =========================================================================


def test_validation_skips_invariants():
    from fhircraft.fhir.resources.datatypes.R4.complex import Quantity

    with override_config(validation_mode="skip"):
        qty = Quantity.model_validate(
            {"code": "mg"}
        )  # This would normally raise an error due to missing system
        assert qty.code == "mg"


def test_validation_respects_disabled_warnings():

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
            len([warning for warning in w if "Test constraint" in str(warning.message)])
            == 0
        )


def test_validation_respects_disabled_constraints():
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
            len([warning for warning in w if "Test constraint" in str(warning.message)])
            == 0
        )


def test_validation_mode_skip():

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


def test_validation_lenient_mode():
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


def test_validation_with_context_manager():

    # Default: warnings enabled
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # Temporarily disable warnings
        with override_config(disable_validation_warnings=True):
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


def test_context_isolation():
    from contextvars import copy_context

    configure(validation_mode="strict")

    def check_config_in_context():
        return get_config().mode

    # Create a new context with different config
    ctx = copy_context()

    # Modify config in new context
    with override_config(validation_mode="lenient"):
        result_in_context = check_config_in_context()

    # Main context should be unchanged
    assert get_config().mode == "strict"
