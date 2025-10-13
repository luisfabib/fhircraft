"""
Type checking and conversion utilities for FHIR primitive types.

This module provides convenient functions to check if values conform to FHIR primitive types
and to convert between different types. The core conversion logic is implemented here,
and FHIRPath conversion functions use these utilities.
"""

import importlib
import re
from datetime import date, datetime, time
from typing import TYPE_CHECKING, Any, Type, Union

from pydantic import BaseModel, Field, ValidationError, create_model
from typing_extensions import TypeAliasType

import fhircraft.fhir.resources.datatypes.primitives as primitives
import fhircraft.fhir.resources.datatypes.R4.complex_types as r4_complex_types
import fhircraft.fhir.resources.datatypes.R4B.complex_types as r4b_complex_types
import fhircraft.fhir.resources.datatypes.R5.complex_types as r5_complex_types
from fhircraft.utils import get_FHIR_release_from_version

if TYPE_CHECKING:
    from fhircraft.fhir.resources.base import FHIRBaseModel


class FHIRTypeError(Exception):
    """Raised when type checking or conversion fails."""

    pass


__complex_types_relases__ = {
    "R4": r4_complex_types,
    "R4B": r4b_complex_types,
    "R5": r5_complex_types,
}


def get_fhir_primitive_type(type_str: str) -> type | None:
    return getattr(primitives, type_str, None)


def get_complex_FHIR_type(type_str: str, release="R4B") -> type:
    complex_FHIR_types = __complex_types_relases__.get(release)
    if not complex_FHIR_types:
        raise ValueError(f"Unsupported FHIR release: {release}")
    return getattr(complex_FHIR_types, type_str)


def get_fhir_resource_type(type_str: str, release="R4B") -> type:
    # Convert CamelCase to snake_case for module lookup
    type_str_snake = re.sub(r"(?<!^)(?=[A-Z])", "_", type_str).lower()
    resource_module = importlib.import_module(
        f"fhircraft.fhir.resources.datatypes.{release}.resources.{type_str_snake}"
    )

    resource = getattr(resource_module, type_str, None)
    if not resource:
        # Try to get from factory cache using lazy import to avoid circular dependency
        try:
            from fhircraft.fhir.resources import factory

            resource = next(
                (
                    model
                    for model in factory.factory.construction_cache.values()
                    if model.__name__ == type_str
                    and release
                    == get_FHIR_release_from_version(getattr(model, "fhirVersion", ""))
                ),
                None,
            )
        except ImportError:
            # Factory not available, which is fine - we'll just fail gracefully
            pass

        if not resource:
            raise AttributeError(f"Unknown {release} FHIR resource type: {type_str}")
    return resource


# Type checking functions
def is_fhir_primitive_type(
    value: Any, fhir_type: Type | TypeAliasType | str, raise_on_error: bool = True
) -> bool:
    """
    Check if a value conforms to a FHIR primitive type.

    Args:
        value: The value to check
        fhir_type: The FHIR type to check against (class, TypeAliasType, or string name)
        raise_on_error: Whether to raise FHIRTypeError on unknown type (default: True)

    Returns:
        bool: `True` if the value conforms to the type, `False` otherwise

    Raises:
        FHIRTypeError: If the fhir_type is a string and does not correspond to a known type

    Examples:
        >>> is_fhir_primitive_type("123", primitives.Integer)
        True
        >>> is_fhir_primitive_type("true", primitives.Boolean)
        True
        >>> is_fhir_primitive_type("invalid-date", primitives.Date)
        False
        >>> is_fhir_primitive_type(42, "UnsignedInt")
        True
    """
    # Handle string type names
    if isinstance(fhir_type, str):
        if hasattr(primitives, fhir_type):
            fhir_type = getattr(primitives, fhir_type)
        else:
            if raise_on_error:
                raise FHIRTypeError(f"Unknown FHIR type: {fhir_type}")
            return False

    # For TypeAliasType, use Pydantic validation
    if isinstance(fhir_type, TypeAliasType):
        try:
            # Create a temporary model with the field type
            TestModel = create_model("TestModel", field=(fhir_type, Field()))
            TestModel(field=value)
            return True
        except ValidationError:
            return False

    # For complex types, try instantiation
    try:
        if hasattr(fhir_type, "model_validate"):
            if isinstance(value, dict):
                fhir_type.model_validate(value)  # type: ignore
            else:
                fhir_type(value)  # type: ignore
            return True
    except (ValidationError, TypeError):
        return False

    return False


def is_fhir_complex_type(
    value: Any, fhir_type: "FHIRBaseModel | type | str", raise_on_error: bool = True
) -> bool:
    """
    Check if a value conforms to a complex FHIR type.

    Args:
        value: The value to check
        fhir_type: The complex FHIR type (or name thereof) to check against
        raise_on_error: Whether to raise FHIRTypeError on unknown type (default: True)

    Returns:
        bool: `True` if the value conforms to the type, `False` otherwise

    Raises:
        FHIRTypeError: If the fhir_type is a string and does not correspond to a known complex type
    """
    if isinstance(fhir_type, str):
        try:
            fhir_type = get_complex_FHIR_type(fhir_type)
        except AttributeError:
            if raise_on_error:
                raise FHIRTypeError(f"Unknown complex FHIR type: {fhir_type}")
            else:
                return False
    try:
        if hasattr(fhir_type, "model_validate"):
            fhir_type.model_validate(value)  # type: ignore
        return True
    except ValidationError as e:
        return False


def is_fhir_resource_type(
    value: Any, fhir_type: "FHIRBaseModel | type | str", raise_on_error: bool = True
) -> bool:
    """
    Check if a value conforms to a FHIR resource.

    Args:
        value: The value to check
        fhir_type: The complex FHIR type (or name thereof) to check against
        raise_on_error: Whether to raise FHIRTypeError on unknown type (default: True)

    Returns:
        bool: `True` if the value conforms to the type, `False` otherwise

    Raises:
        FHIRTypeError: If the fhir_type is a string and does not correspond to a known resource type
    """
    if isinstance(fhir_type, str):
        try:
            resource = get_fhir_resource_type(fhir_type)
        except AttributeError as e:
            if raise_on_error:
                raise e
            else:
                return False
        fhir_type = resource

    try:
        if hasattr(fhir_type, "model_validate"):
            fhir_type.model_validate(value)  # type: ignore
        return True
    except ValidationError as e:
        return False


def is_boolean(value: Any) -> bool:
    """Check if value is a valid FHIR Boolean."""
    return is_fhir_primitive_type(value, primitives.Boolean)


def is_integer(value: Any) -> bool:
    """Check if value is a valid FHIR Integer."""
    return is_fhir_primitive_type(value, primitives.Integer)


def is_integer64(value: Any) -> bool:
    """Check if value is a valid FHIR Integer64."""
    return is_fhir_primitive_type(value, primitives.Integer64)


def is_decimal(value: Any) -> bool:
    """Check if value is a valid FHIR Decimal."""
    return is_fhir_primitive_type(value, primitives.Decimal)


def is_string(value: Any) -> bool:
    """Check if value is a valid FHIR String."""
    return is_fhir_primitive_type(value, primitives.String)


def is_uri(value: Any) -> bool:
    """Check if value is a valid FHIR Uri."""
    return is_fhir_primitive_type(value, primitives.Uri)


def is_url(value: Any) -> bool:
    """Check if value is a valid FHIR Url."""
    return is_fhir_primitive_type(value, primitives.Url)


def is_canonical(value: Any) -> bool:
    """Check if value is a valid FHIR Canonical."""
    return is_fhir_primitive_type(value, primitives.Canonical)


def is_base64binary(value: Any) -> bool:
    """Check if value is a valid FHIR Base64Binary."""
    return is_fhir_primitive_type(value, primitives.Base64Binary)


def is_instant(value: Any) -> bool:
    """Check if value is a valid FHIR Instant."""
    return (
        is_fhir_primitive_type(value, primitives.Instant)
        if isinstance(value, str)
        else isinstance(value, datetime)
    )


def is_date(value: Any) -> bool:
    """Check if value is a valid FHIR Date."""
    return (
        is_fhir_primitive_type(value, primitives.Date)
        if isinstance(value, str)
        else isinstance(value, date) and not is_datetime(value)
    )


def is_datetime(value: Any) -> bool:
    """Check if value is a valid FHIR DateTime."""
    return (
        is_fhir_primitive_type(value, primitives.DateTime)
        if isinstance(value, str)
        else isinstance(value, datetime) and not is_date(value)
    )


def is_time(value: Any) -> bool:
    """Check if value is a valid FHIR Time."""
    return (
        is_fhir_primitive_type(value, primitives.Time)
        if isinstance(value, str)
        else isinstance(value, time)
    )


def is_code(value: Any) -> bool:
    """Check if value is a valid FHIR Code."""
    return is_fhir_primitive_type(value, primitives.Code)


def is_oid(value: Any) -> bool:
    """Check if value is a valid FHIR Oid."""
    return is_fhir_primitive_type(value, primitives.Oid)


def is_id(value: Any) -> bool:
    """Check if value is a valid FHIR Id."""
    return is_fhir_primitive_type(value, primitives.Id)


def is_markdown(value: Any) -> bool:
    """Check if value is a valid FHIR Markdown."""
    return is_fhir_primitive_type(value, primitives.Markdown)


def is_unsigned_int(value: Any) -> bool:
    """Check if value is a valid FHIR UnsignedInt."""
    return is_fhir_primitive_type(value, primitives.UnsignedInt)


def is_positive_int(value: Any) -> bool:
    """Check if value is a valid FHIR PositiveInt."""
    return is_fhir_primitive_type(value, primitives.PositiveInt)


def is_uuid(value: Any) -> bool:
    """Check if value is a valid FHIR Uuid."""
    return is_fhir_primitive_type(value, primitives.Uuid)


# Type conversion functions with core logic
def to_boolean(value: Any) -> Union[bool, None]:
    """
    Convert value to FHIR Boolean.

    Args:
        value: Value to convert

    Returns:
        bool or None: Converted boolean value or None if conversion fails

    Examples:
        >>> to_boolean("true")
        True
        >>> to_boolean("1")
        True
        >>> to_boolean("invalid")
        None
    """
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        lower_val = value.lower()
        if lower_val in ["true", "t", "yes", "y", "1", "1.0"]:
            return True
        elif lower_val in ["false", "f", "no", "n", "0", "0.0"]:
            return False
        else:
            return None
    elif isinstance(value, (int, float)):
        return bool(value)
    else:
        return None


def to_integer(value: Any) -> Union[int, None]:
    """
    Convert value to FHIR Integer.

    Args:
        value: Value to convert

    Returns:
        int or None: Converted integer value or None if conversion fails
    """
    if isinstance(value, int):
        return value
    elif isinstance(value, bool):
        return int(value)
    elif isinstance(value, str):
        if re.match(r"^[+-]?\d+$", value.strip()):
            try:
                return int(value)
            except ValueError:
                return None
        else:
            return None
    else:
        return None


def to_decimal(value: Any) -> Union[float, None]:
    """
    Convert value to FHIR Decimal.

    Args:
        value: Value to convert

    Returns:
        float or None: Converted decimal value or None if conversion fails
    """
    if isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, bool):
        return float(value)
    elif isinstance(value, str):
        try:
            # Check if it matches decimal pattern
            if re.match(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$", value.strip()):
                return float(value)
            else:
                return None
        except ValueError:
            return None
    else:
        return None


def to_date(value: Any) -> Union[str, None]:
    """
    Convert value to FHIR Date.

    Args:
        value: Value to convert

    Returns:
        str or None: Converted date string or None if conversion fails
    """
    if isinstance(value, str):
        # Check if it's already a valid date
        date_pattern = rf"^{primitives.YEAR_REGEX}(-{primitives.MONTH_REGEX}(-{primitives.DAY_REGEX})?)?$"
        if re.match(date_pattern, value):
            return value

        # Check if it's a datetime that we can extract date from
        datetime_pattern = rf"^({primitives.YEAR_REGEX}(-{primitives.MONTH_REGEX}(-{primitives.DAY_REGEX})?)?)(T{primitives.HOUR_REGEX}(:{primitives.MINUTES_REGEX}(:{primitives.SECONDS_REGEX}({primitives.TIMEZONE_REGEX})?)?)?)?$"
        datetime_match = re.match(datetime_pattern, value)
        if datetime_match:
            return datetime_match.group(1)  # Extract date part

        return None
    else:
        return None


def to_datetime(value: Any) -> Union[str, None]:
    """
    Convert value to FHIR DateTime.

    Args:
        value: Value to convert

    Returns:
        str or None: Converted datetime string or None if conversion fails
    """
    if isinstance(value, str):
        # Check if it's already a valid datetime
        datetime_pattern = rf"^{primitives.YEAR_REGEX}(-{primitives.MONTH_REGEX}(-{primitives.DAY_REGEX})?)?(T{primitives.HOUR_REGEX}(:{primitives.MINUTES_REGEX}(:{primitives.SECONDS_REGEX}({primitives.TIMEZONE_REGEX})?)?)?)?$"
        if re.match(datetime_pattern, value):
            return value

        # Check if it's a date that we can convert to datetime
        date_pattern = rf"^{primitives.YEAR_REGEX}(-{primitives.MONTH_REGEX}(-{primitives.DAY_REGEX})?)?$"
        if re.match(date_pattern, value):
            return value  # Date is a valid partial datetime

        return None
    else:
        return None


def to_time(value: Any) -> Union[str, None]:
    """
    Convert value to FHIR Time.

    Args:
        value: Value to convert

    Returns:
        str or None: Converted time string or None if conversion fails
    """
    if isinstance(value, str):
        # Check if it's already a valid time
        time_pattern = rf"^{primitives.HOUR_REGEX}(:{primitives.MINUTES_REGEX}(:{primitives.SECONDS_REGEX}({primitives.TIMEZONE_REGEX})?)?)?$"
        if re.match(time_pattern, value):
            return value

        # Check if it's a datetime/date that contains time info we can extract
        datetime_pattern = rf"^({primitives.YEAR_REGEX}(-{primitives.MONTH_REGEX}(-{primitives.DAY_REGEX})?)?)(T({primitives.HOUR_REGEX}(:{primitives.MINUTES_REGEX}(:{primitives.SECONDS_REGEX}({primitives.TIMEZONE_REGEX})?)?)?))$"
        datetime_match = re.match(datetime_pattern, value)
        if datetime_match:
            return datetime_match.group(4)  # Extract time part

        return None
    else:
        return None


def to_string(value: Any) -> Union[str, None]:
    """
    Convert value to string representation.

    Args:
        value: Value to convert

    Returns:
        str or None: String representation or None if conversion fails
    """
    if isinstance(value, str):
        return value
    elif isinstance(value, (int, float, bool)):
        return str(value)
    elif hasattr(value, "__str__"):
        try:
            return str(value)
        except Exception:
            return None
    else:
        return None


def to_quantity(value: Any) -> Union[Any, None]:
    """
    Convert value to FHIR Quantity.

    Args:
        value: Value to convert

    Returns:
        Quantity or None: Converted Quantity object or None if conversion fails
    """
    try:
        # Import here to avoid circular imports
        Quantity = get_complex_FHIR_type("Quantity")

        if isinstance(value, str):
            # Try to parse "value unit" format like "10.5 mg"
            quantity_match = re.match(r"^(\d+(?:\.\d+)?)\s*([a-zA-Z]+)$", value.strip())
            if quantity_match:
                val, unit = quantity_match.groups()
                decimal_val = to_decimal(val)
                if decimal_val is not None:
                    return Quantity(value=decimal_val, unit=unit)
            return None
        elif isinstance(value, (int, float)):
            # Simple numeric value becomes quantity with unit "1"
            return Quantity(value=float(value), unit="1")
        elif isinstance(value, bool):
            # Boolean to quantity: True=1.0, False=0.0
            return Quantity(value=float(value), unit="1")
        else:
            return None
    except Exception:
        return None


# Utility functions for working with type aliases
def get_primitive_type_name(fhir_type: TypeAliasType) -> str:
    """Get the string name of a FHIR primitive type."""
    if hasattr(fhir_type, "__name__"):
        return fhir_type.__name__
    # Fallback: search primitives module
    for name in dir(primitives):
        if getattr(primitives, name) is fhir_type:
            return name
    return "Unknown"


def get_primitive_type_by_name(type_name: str) -> Union[TypeAliasType, None]:
    """Get a FHIR primitive type by its string name."""
    return getattr(primitives, type_name, None)


def list_primitive_types() -> list[str]:
    """List all available FHIR primitive type names."""
    return [
        name
        for name in dir(primitives)
        if not name.startswith("_")
        and isinstance(getattr(primitives, name), TypeAliasType)
    ]
