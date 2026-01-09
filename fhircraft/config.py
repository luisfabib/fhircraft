"""
FHIRcraft Global Configuration
"""

import os
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Literal, Set


@dataclass
class ValidationConfig:
    """Configuration for FHIR validation behavior.

    Attributes:
        disable_warnings: Disable all validation warnings globally.
        disabled_constraints: Set of constraint keys to disable (e.g., 'dom-6').
        disable_warning_severity: Disable only warnings, keep errors.
        disable_errors: Disable error-level constraints (use with extreme caution).
        mode: Validation mode - 'strict', 'lenient', or 'skip'.
            - strict: All validations enabled (default)
            - lenient: Convert errors to warnings
            - skip: Disable all validations
    """

    disable_warnings: bool = False
    disabled_constraints: Set[str] = field(default_factory=set)
    disable_warning_severity: bool = False
    disable_errors: bool = False
    mode: Literal["strict", "lenient", "skip"] = "strict"


@dataclass
class FhircraftConfig:
    """Global configuration for FHIRcraft.

    This configuration class is designed to be easily extendable for future
    features beyond validation.

    Attributes:
        validation: Validation-specific configuration.
    """

    validation: ValidationConfig = field(default_factory=ValidationConfig)

    def __post_init__(self):
        """Ensure validation is a ValidationConfig instance."""
        if isinstance(self.validation, dict):
            self.validation = ValidationConfig(**self.validation)


# Thread-safe context variable for configuration
_config_context: ContextVar[FhircraftConfig] = ContextVar(
    "fhircraft_config", default=FhircraftConfig()
)


def get_config() -> FhircraftConfig:
    """Get the current FHIRcraft configuration.

    Returns:
        FhircraftConfig: The current configuration instance.
    """
    return _config_context.get()


def set_config(config: FhircraftConfig) -> None:
    """Set the global FHIRcraft configuration.

    Args:
        config: The new configuration to apply globally.

    Warning:
        This sets the configuration globally and persists until changed.
        Consider using `with_config()` for temporary changes.
    """
    _config_context.set(config)


def configure(**kwargs) -> None:
    """Configure FHIRcraft settings using keyword arguments.

    This is a convenience function that allows setting configuration
    options without creating config objects explicitly.

    **kwargs: Configuration options. Can include:
        - disable_validation_warnings (bool)
        - validation_mode (str: 'strict', 'lenient', 'skip')
        - disable_validation_errors (bool)
        - disabled_constraints (Set[str])
    """
    current_config = get_config()

    # Map convenience kwargs to nested structure
    validation_kwargs = {}

    if "disable_validation_warnings" in kwargs:
        validation_kwargs["disable_warnings"] = kwargs["disable_validation_warnings"]
    if "validation_mode" in kwargs:
        validation_kwargs["mode"] = kwargs["validation_mode"]
    if "disable_validation_errors" in kwargs:
        validation_kwargs["disable_errors"] = kwargs["disable_validation_errors"]
    if "disabled_constraints" in kwargs:
        validation_kwargs["disabled_constraints"] = kwargs["disabled_constraints"]
    if "disable_warning_severity" in kwargs:
        validation_kwargs["disable_warning_severity"] = kwargs[
            "disable_warning_severity"
        ]

    # Create new validation config with updates
    validation_dict = {**current_config.validation.__dict__, **validation_kwargs}
    new_validation = ValidationConfig(**validation_dict)

    # Create new config
    new_config = FhircraftConfig(validation=new_validation)
    set_config(new_config)


@contextmanager
def with_config(**kwargs):
    """Context manager for temporary configuration changes.

    This allows you to temporarily modify configuration within a specific
    code block, with automatic restoration when exiting the block.

    Yields:
        (FhircraftConfig): The temporary configuration.
    """
    old_config = get_config()

    # Build new config from kwargs
    validation_kwargs = {}
    if "disable_validation_warnings" in kwargs:
        validation_kwargs["disable_warnings"] = kwargs["disable_validation_warnings"]
    if "validation_mode" in kwargs:
        validation_kwargs["mode"] = kwargs["validation_mode"]
    if "disable_validation_errors" in kwargs:
        validation_kwargs["disable_errors"] = kwargs["disable_validation_errors"]
    if "disabled_constraints" in kwargs:
        validation_kwargs["disabled_constraints"] = kwargs["disabled_constraints"]
    if "disable_warning_severity" in kwargs:
        validation_kwargs["disable_warning_severity"] = kwargs[
            "disable_warning_severity"
        ]

    # Merge with current config
    validation_dict = {**old_config.validation.__dict__, **validation_kwargs}
    new_validation = ValidationConfig(**validation_dict)
    new_config = FhircraftConfig(validation=new_validation)

    # Set new config and store token for reset
    token = _config_context.set(new_config)
    try:
        yield new_config
    finally:
        _config_context.reset(token)


def disable_constraint(*constraint_keys: str) -> None:
    """Disable specific validation constraints by their keys.

    Args:
        *constraint_keys: One or more constraint keys to disable (e.g., 'dom-6').
    """
    config = get_config()
    config.validation.disabled_constraints.update(constraint_keys)


def enable_constraint(*constraint_keys: str) -> None:
    """Re-enable specific validation constraints by their keys.

    Args:
        *constraint_keys: One or more constraint keys to re-enable.
    """
    config = get_config()
    for key in constraint_keys:
        config.validation.disabled_constraints.discard(key)


def reset_config() -> None:
    """Reset configuration to default values.

    This is useful for testing or when you want to clear all
    configuration changes.
    """
    set_config(FhircraftConfig())


def load_config_from_env() -> None:
    """Load configuration from environment variables.

    Supported environment variables:
        - FHIRCRAFT_DISABLE_WARNINGS: 'true' to disable validation warnings
        - FHIRCRAFT_VALIDATION_MODE: 'strict', 'lenient', or 'skip'
        - FHIRCRAFT_DISABLED_CONSTRAINTS: Comma-separated constraint keys
    """
    kwargs = {}

    if os.getenv("FHIRCRAFT_DISABLE_WARNINGS", "").lower() == "true":
        kwargs["disable_validation_warnings"] = True

    validation_mode = os.getenv("FHIRCRAFT_VALIDATION_MODE", "").lower()
    if validation_mode in ("strict", "lenient", "skip"):
        kwargs["validation_mode"] = validation_mode

    disabled_constraints = os.getenv("FHIRCRAFT_DISABLED_CONSTRAINTS", "")
    if disabled_constraints:
        kwargs["disabled_constraints"] = set(
            key.strip() for key in disabled_constraints.split(",")
        )

    if kwargs:
        configure(**kwargs)


__all__ = [
    "FhircraftConfig",
    "ValidationConfig",
    "get_config",
    "set_config",
    "configure",
    "with_config",
    "disable_constraint",
    "enable_constraint",
    "reset_config",
    "load_config_from_env",
]
