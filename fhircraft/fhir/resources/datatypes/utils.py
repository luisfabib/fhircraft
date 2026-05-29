"""
Type checking and conversion utilities for FHIR primitive types.

This module provides convenient functions to check if values conform to FHIR primitive types
and to convert between different types. The core conversion logic is implemented here,
and FHIRPath conversion functions use these utilities.
"""

import re
from datetime import date, datetime, time
from typing import TYPE_CHECKING, Any, Union
from typing_extensions import TypeAliasType

from pydantic import TypeAdapter, BaseModel, ValidationError

from fhircraft.exceptions import FhirTypeError
import fhircraft.fhir.resources.datatypes as constants
from fhircraft.fhir.resources.datatypes.registry import get_fhir_type

if TYPE_CHECKING:
    from fhircraft.fhir.resources.base import FHIRBaseModel


# Cache for TypeAdapter instances to avoid repeated creation
_type_adapter_cache: dict[int, TypeAdapter] = {}


# Type checking functions
def is_fhir_primitive_type(
    value: Any,
    fhir_type: "type[FHIRBaseModel] | type | TypeAliasType | str",
    release: str | None = None,
) -> bool:
    """
    Check if a value conforms to a primitive FHIR type.

    Args:
        value: The value to check
        fhir_type: The primitive FHIR type (or name thereof) to check against

    Returns:
        bool: `True` if the value conforms to the type, `False` otherwise

    Raises:
        FhirTypeError: If the fhir_type is a string and does not correspond to a known primitive type
    """
    if isinstance(fhir_type, str):
        if not release:
            raise FhirTypeError(
                f"Release must be specified when fhir_type is given as a string: '{fhir_type}'"
            )
        fhir_type = get_fhir_type(fhir_type, release)  # type: ignore

    if isinstance(fhir_type, type) and issubclass(fhir_type, BaseModel):
        if getattr(fhir_type, "_kind", None) != "primitive-type":
            return False
        elif isinstance(value, fhir_type):
            return True
        else:
            try:
                fhir_type.model_validate(value)
                return True
            except ValidationError as e:
                return False
    else:
        return False


def is_fhir_complex_type(
    value: Any,
    fhir_type: "type[FHIRBaseModel] | type | TypeAliasType | str",
    release: str | None = None,
) -> bool:
    """
    Check if a value conforms to a complex FHIR type.

    Args:
        value: The value to check
        fhir_type: The complex FHIR type (or name thereof) to check against

    Returns:
        bool: `True` if the value conforms to the type, `False` otherwise

    Raises:
        FhirTypeError: If the fhir_type is a string and does not correspond to a known complex type
    """
    if isinstance(fhir_type, str):
        if not release:
            raise FhirTypeError(
                f"Release must be specified when fhir_type is given as a string: '{fhir_type}'"
            )
        fhir_type = get_fhir_type(fhir_type, release)  # type: ignore

    if isinstance(fhir_type, type) and issubclass(fhir_type, BaseModel):
        if getattr(fhir_type, "_kind", None) != "complex-type":
            return False
        elif isinstance(value, fhir_type):
            return True
        else:
            try:
                fhir_type.model_validate(value)
                return True
            except ValidationError as e:
                return False
    else:
        return False


def is_fhir_resource_type(
    value: Any,
    fhir_type: "type[FHIRBaseModel] | type | TypeAliasType | str",
    release: str | None = None,
) -> bool:
    """
    Check if a value conforms to a FHIR resource.

    Args:
        value: The value to check
        fhir_type: The complex FHIR type (or name thereof) to check against
        release: The FHIR release to use when resolving fhir_type if it is given as a string (e.g., "4.0.1", "4.3.0", "5.0.0"). Required if fhir_type is a string.

    Returns:
        bool: `True` if the value conforms to the type, `False` otherwise

    Raises:
        FhirTypeError: If the fhir_type is a string and does not correspond to a known resource type
    """
    if isinstance(fhir_type, str):
        if not release:
            raise FhirTypeError(
                f"Release must be specified when fhir_type is given as a string: '{fhir_type}'"
            )
        fhir_type = get_fhir_type(fhir_type, release)  # type: ignore

    if isinstance(fhir_type, type) and issubclass(fhir_type, BaseModel):
        if getattr(fhir_type, "_kind", None) != "resource":
            return False
        elif isinstance(value, fhir_type):
            return True
        else:
            try:
                fhir_type.model_validate(value)
                return True
            except ValidationError as e:
                return False
    else:
        return False


def is_fhir_primitive(value: Any) -> bool:
    """Check if a value is a FHIR primitive type."""
    from fhircraft.fhir.resources.base import FHIRPrimitiveModel

    if isinstance(value, FHIRPrimitiveModel) and value.value is not None:
        return True
    if isinstance(value, (str | int | float | bool | date | datetime | time)):
        return True
    else:
        return False


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
    from fhircraft.fhir.resources.base import FHIRPrimitiveModel

    if isinstance(value, FHIRPrimitiveModel):
        value = value.value
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
    from fhircraft.fhir.resources.base import FHIRPrimitiveModel

    if isinstance(value, FHIRPrimitiveModel):
        value = value.value
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
    from fhircraft.fhir.resources.base import FHIRPrimitiveModel

    if isinstance(value, FHIRPrimitiveModel):
        value = value.value
    elif isinstance(value, (int, float)):
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
    from fhircraft.fhir.resources.base import FHIRPrimitiveModel

    if isinstance(value, FHIRPrimitiveModel):
        value = value.value
    if isinstance(value, str):
        # Check if it's already a valid date
        date_pattern = rf"^{constants.YEAR_REGEX}(-{constants.MONTH_REGEX}(-{constants.DAY_REGEX})?)?$"
        if re.match(date_pattern, value):
            return value

        # Check if it's a datetime that we can extract date from
        datetime_pattern = rf"^({constants.YEAR_REGEX}(-{constants.MONTH_REGEX}(-{constants.DAY_REGEX})?)?)(T{constants.HOUR_REGEX}(:{constants.MINUTES_REGEX}(:{constants.SECONDS_REGEX}({constants.TIMEZONE_REGEX})?)?)?)?$"
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
    from fhircraft.fhir.resources.base import FHIRPrimitiveModel

    if isinstance(value, FHIRPrimitiveModel):
        value = value.value
    if isinstance(value, str):
        # Check if it's already a valid datetime
        datetime_pattern = rf"^{constants.YEAR_REGEX}(-{constants.MONTH_REGEX}(-{constants.DAY_REGEX})?)?(T{constants.HOUR_REGEX}(:{constants.MINUTES_REGEX}(:{constants.SECONDS_REGEX}({constants.TIMEZONE_REGEX})?)?)?)?$"
        if re.match(datetime_pattern, value):
            return value

        # Check if it's a date that we can convert to datetime
        date_pattern = rf"^{constants.YEAR_REGEX}(-{constants.MONTH_REGEX}(-{constants.DAY_REGEX})?)?$"
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
    from fhircraft.fhir.resources.base import FHIRPrimitiveModel

    if isinstance(value, FHIRPrimitiveModel):
        value = value.value
    if isinstance(value, str):
        # Check if it's already a valid time
        time_pattern = rf"^{constants.HOUR_REGEX}(:{constants.MINUTES_REGEX}(:{constants.SECONDS_REGEX}({constants.TIMEZONE_REGEX})?)?)?$"
        if re.match(time_pattern, value):
            return value

        # Check if it's a datetime/date that contains time info we can extract
        datetime_pattern = rf"^({constants.YEAR_REGEX}(-{constants.MONTH_REGEX}(-{constants.DAY_REGEX})?)?)(T({constants.HOUR_REGEX}(:{constants.MINUTES_REGEX}(:{constants.SECONDS_REGEX}({constants.TIMEZONE_REGEX})?)?)?))$"
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
    from fhircraft.fhir.resources.base import FHIRPrimitiveModel

    if isinstance(value, FHIRPrimitiveModel):
        value = value.value
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
