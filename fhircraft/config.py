"""
FHIRcraft Global Configuration
"""

import dataclasses
import os
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Container


_VALID_MODES = ("strict", "lenient", "skip")


@dataclass(frozen=True)
class FhircraftConfig:
    """Global configuration for FHIRcraft.

    Attributes:
        disable_validation_warnings: Disable all validation warnings globally.
        disable_fhir_warnings: Disable only FHIR warning-severity issues, keep errors.
        disable_fhir_errors: Disable error-level constraints (use with extreme caution).
        disabled_fhir_constraints: Set of constraint keys to disable (e.g., 'dom-6').
        mode: Validation mode - 'strict', 'lenient', or 'skip'.
            - strict: All validations enabled (default)
            - lenient: Convert errors to warnings
            - skip: Disable all validations
    """

    disable_validation_warnings: bool = False
    disable_fhir_warnings: bool = False
    disable_fhir_errors: bool = False
    disabled_fhir_constraints: FrozenSet[str] = field(default_factory=frozenset)
    mode: Literal["strict", "lenient", "skip"] = "strict"

    def __post_init__(self) -> None:
        # Coerce mutable set to frozenset so the type contract is always satisfied
        if isinstance(self.disabled_fhir_constraints, set):
            object.__setattr__(
                self,
                "disabled_fhir_constraints",
                frozenset(self.disabled_fhir_constraints),
            )
        if self.mode not in _VALID_MODES:
            raise ValueError(
                f"Invalid validation mode {self.mode!r}. "
                f"Must be one of: {', '.join(_VALID_MODES)}"
            )


# Thread-safe context variable for configuration.
# Uses None as default to avoid sharing a single instance across all contexts
# that have never called set_config().
_config_context: ContextVar[FhircraftConfig | None] = ContextVar(
    "fhircraft_config", default=None
)


def get_config() -> FhircraftConfig:
    """Get the current FHIRcraft configuration.

    Returns:
        FhircraftConfig: The current configuration instance.
    """
    config = _config_context.get()
    if config is None:
        return FhircraftConfig()
    return config


def configure(
    *,
    disable_validation_warnings: bool | None = None,
    disable_fhir_warnings: bool | None = None,
    disable_fhir_errors: bool | None = None,
    disabled_fhir_constraints: Container[str] | None = None,
    validation_mode: Literal["strict", "lenient", "skip"] | None = None,
) -> None:
    """Configure FHIRcraft settings.

    All parameters are optional; only the ones provided will be changed.
    Unspecified parameters retain their current values.

    Args:
        disable_validation_warnings: Disable all validation warnings globally.
        disable_fhir_warnings: Disable only FHIR warning-severity issues, keep errors.
        disable_fhir_errors: Disable error-level constraints (use with extreme caution).
        disabled_fhir_constraints: Set of constraint keys to disable (e.g., {'dom-6'}).
        validation_mode: Validation mode - 'strict', 'lenient', or 'skip'.
    """
    current = get_config()
    _config_context.set(
        dataclasses.replace(
            current,
            **{
                k: v
                for k, v in {
                    "disable_validation_warnings": disable_validation_warnings,
                    "disable_fhir_warnings": disable_fhir_warnings,
                    "disable_fhir_errors": disable_fhir_errors,
                    "disabled_fhir_constraints": disabled_fhir_constraints,
                    "mode": validation_mode,
                }.items()
                if v is not None
            },
        )
    )


@contextmanager
def context_config(
    *,
    disable_validation_warnings: bool | None = None,
    disable_fhir_warnings: bool | None = None,
    disable_fhir_errors: bool | None = None,
    disabled_fhir_constraints: Container[str] | None = None,
    validation_mode: Literal["strict", "lenient", "skip"] | None = None,
):
    """Context manager for temporary configuration changes.

    All parameters are optional; only the ones provided will be changed within
    the context block. Previous configuration is automatically restored on exit,
    even if an exception occurs.

    Args:
        disable_validation_warnings: Disable all validation warnings globally.
        disable_fhir_warnings: Disable only FHIR warning-severity issues, keep errors.
        disable_fhir_errors: Disable error-level constraints (use with extreme caution).
        disabled_fhir_constraints: Set of constraint keys to disable (e.g., {'dom-6'}).
        validation_mode: Validation mode - 'strict', 'lenient', or 'skip'.

    Yields:
        FhircraftConfig: The temporary configuration.
    """
    old_config = get_config()
    new_config = dataclasses.replace(
        old_config,
        **{
            k: v
            for k, v in {
                "disable_validation_warnings": disable_validation_warnings,
                "disable_fhir_warnings": disable_fhir_warnings,
                "disable_fhir_errors": disable_fhir_errors,
                "disabled_fhir_constraints": disabled_fhir_constraints,
                "mode": validation_mode,
            }.items()
            if v is not None
        },
    )
    token = _config_context.set(new_config)
    try:
        yield new_config
    finally:
        _config_context.reset(token)


def disable_constraint(*constraint_keys: str) -> None:
    """Disable specific validation constraints by their keys.

    Creates a new configuration with the given keys added to
    `disabled_fhir_constraints`; the change is visible to the current context
    only and does not escape a surrounding `context_config` block.

    Args:
        *constraint_keys: One or more constraint keys to disable (e.g., 'dom-6').
    """
    config = get_config()
    _config_context.set(
        dataclasses.replace(
            config,
            disabled_fhir_constraints=config.disabled_fhir_constraints
            | frozenset(constraint_keys),
        )
    )


def enable_constraint(*constraint_keys: str) -> None:
    """Re-enable specific validation constraints by their keys.

    Args:
        *constraint_keys: One or more constraint keys to re-enable.
    """
    config = get_config()
    _config_context.set(
        dataclasses.replace(
            config,
            disabled_fhir_constraints=config.disabled_fhir_constraints
            - frozenset(constraint_keys),
        )
    )


def reset_config() -> None:
    """Reset configuration to default values.

    This is useful for testing or when you want to clear all
    configuration changes.
    """
    _config_context.set(None)


def load_config_from_env() -> None:
    """Load configuration from environment variables.

    Supported environment variables:
        - FHIRCRAFT_DISABLE_WARNINGS: 'true' to disable all validation warnings
        - FHIRCRAFT_VALIDATION_MODE: 'strict', 'lenient', or 'skip'
        - FHIRCRAFT_DISABLED_CONSTRAINTS: Comma-separated constraint keys
    """
    kwargs: dict = {}

    if os.getenv("FHIRCRAFT_DISABLE_WARNINGS", "").lower() == "true":
        kwargs["disable_validation_warnings"] = True

    validation_mode = os.getenv("FHIRCRAFT_VALIDATION_MODE", "").lower()
    if validation_mode in _VALID_MODES:
        kwargs["validation_mode"] = validation_mode

    disabled_constraints = os.getenv("FHIRCRAFT_DISABLED_CONSTRAINTS", "")
    if disabled_constraints:
        kwargs["disabled_fhir_constraints"] = frozenset(
            key.strip() for key in disabled_constraints.split(",")
        )

    if kwargs:
        configure(**kwargs)


__all__ = [
    "FhircraftConfig",
    "get_config",
    "configure",
    "context_config",
    "disable_constraint",
    "enable_constraint",
    "reset_config",
    "load_config_from_env",
]
