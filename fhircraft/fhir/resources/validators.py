import traceback
import warnings

from typing import TYPE_CHECKING, Any, List, TypeVar, Union, Sequence

__all__ = [
    "validate_element_constraint",
    "validate_model_constraint",
    "validate_FHIR_element_pattern",
    "validate_FHIR_model_pattern",
    "validate_FHIR_element_fixed_value",
    "validate_FHIR_model_fixed_value",
    "validate_type_choice_element",
    "validate_slicing_cardinalities",
    "get_type_choice_value_by_base",
]

from pydantic import BaseModel
from pydantic_core import PydanticCustomError
from fhircraft.config import get_config
from fhircraft.exceptions import FhirValidationWarning, FHIRPathWarning
from fhircraft.fhir.resources.base import FHIRPrimitiveModel
from fhircraft.utils import (
    capitalize,
    ensure_list,
    get_all_models_from_field,
    is_dict_subset,
)

if TYPE_CHECKING:
    from fhircraft.fhir.resources.base import FHIRBaseModel, FHIRSliceModel

T = TypeVar("T", bound=BaseModel)


def _validate_FHIR_element_constraint(
    value: Any,
    instance: Any,
    expression: str,
    human: str,
    key: str,
    severity: str,
    element: str | None = None,
):
    """
    Validate FHIR element constraint against a FHIRPath expression.

    Args:
        value (Any): The value to validate.
        instance (Any): The instance containing the value.
        expression (str): The FHIRPath expression to evaluate.
        human (str): A human-readable description of the constraint.
        key (str): The key associated with the constraint.
        severity (str): The severity level of the constraint.

    Returns:
        Any: The validated value.

    Raises:
        PydanticCustomError: If the validation fails and severity is not 'warning'.
        Warning: If the validation fails and severity is 'warning'.
    """
    from fhircraft.config import get_config
    from fhircraft.fhir.path import parse_fhirpath
    from fhircraft.exceptions import (
        FHIRPathLexingError,
        FHIRPathParsingError,
        FHIRPathWarning,
    )

    # Check configuration for validation control
    config = get_config()

    # Skip validation if mode is 'skip'
    if config.validation_mode == "skip":
        return value

    # Skip if this specific constraint is disabled
    if key in config.disabled_fhir_constraints:
        return value

    # Skip if all warnings are disabled and this is a warning
    if severity == "warning" and (
        config.disable_validation_warnings or config.disable_fhir_warnings
    ):
        return value

    # Skip if all errors are disabled and this is an error
    if severity == "error" and config.disable_fhir_errors:
        return value

    # In lenient mode, convert errors to warnings
    effective_severity = severity
    if config.validation_mode == "lenient" and severity == "error":
        effective_severity = "warning"

    if value is None:
        return value

    environment = (
        {"%fhirRelease": release}
        if (release := getattr(instance, "_fhir_release", None))
        else {}
    )
    for item in ensure_list(value):
        try:
            valid = parse_fhirpath(expression).single(
                item, default=True, environment=environment
            )
        except (
            ValueError,
            FHIRPathLexingError,
            FHIRPathParsingError,
            AttributeError,
            NotImplementedError,
        ) as e:
            warnings.warn(
                f"Warning: FHIRPath raised {e.__class__.__name__} for expression: [{key}] -> {expression}. {traceback.format_exc()}",
                FHIRPathWarning,
                stacklevel=2,
            )
            return value
        error_message = f"[{key}] {human} -> {expression}"
        if element:
            error_message = f"{element}\n\t{error_message}"
        if effective_severity == "warning" and not valid:
            warnings.warn(error_message, FhirValidationWarning, stacklevel=2)
        else:
            if not valid:
                raise PydanticCustomError("fhir_invariant_violation", error_message)  # type: ignore
    return value


def validate_element_constraint(
    instance: T,
    elements: Sequence[str],
    expression: str,
    human: str,
    key: str,
    severity: str,
) -> T:
    """
    Validates a FHIR element constraint based on a FHIRPath expression.

    Args:
        instance (T): The instance to be validated.
        elements (Sequence[str]): The elements to be validated.
        expression (str): The FHIRPath expression to evaluate.
        human (str): A human-readable description of the constraint.
        key (str): The key associated with the constraint.
        severity (str): The severity level of the constraint ('warning' or 'error').

    Returns:
        Any: The validated value.

    Raises:
        PydanticCustomError: If the validation fails and severity is not `warning`.
        Warning: If the validation fails and severity is `warning`.
    """

    config = get_config()
    if config.validation_mode == "skip":
        return instance

    values = {}

    def _get_path_value(obj: Any, element_path: str, current_path: str = "") -> None:
        """
        Recursively extract values from nested object paths, handling lists correctly.

        Args:
            obj: Current object to traverse
            element_path: Remaining path to traverse (dot-separated)
            current_path: Path traversed so far (for error reporting)
        """
        if not element_path:
            # We've reached the end of the path
            values[current_path] = obj
            return

        parts = element_path.split(".", 1)
        current_attr = parts[0]
        remaining_path = parts[1] if len(parts) > 1 else ""

        # Build the new current path
        new_current_path = (
            f"{current_path}.{current_attr}" if current_path else current_attr
        )

        # Get the attribute value
        current_value = getattr(obj, current_attr, None) if obj is not None else None

        if current_value is None:
            # Attribute doesn't exist or is None
            values[
                (
                    new_current_path
                    if not remaining_path
                    else f"{new_current_path}.{remaining_path}"
                )
            ] = None
            return

        if isinstance(current_value, list):
            if not remaining_path:
                # We want the list itself
                values[new_current_path] = current_value
            else:
                # We need to traverse into each item in the list
                for idx, item in enumerate(current_value):
                    item_path = f"{new_current_path}[{idx}]"
                    _get_path_value(item, remaining_path, item_path)
        else:
            if not remaining_path:
                # We want this value
                values[new_current_path] = current_value
            else:
                # Continue traversing
                _get_path_value(current_value, remaining_path, new_current_path)

    for element_path in elements:
        _get_path_value(instance, element_path)

    for path, value in values.items():
        _validate_FHIR_element_constraint(
            value, instance, expression, human, key, severity, element=path
        )
    return instance


def validate_model_constraint(
    instance: T, expression: str, human: str, key: str, severity: str
) -> T:
    """
    Validates a FHIR model constraint based on a FHIRPath expression.

    Args:
        instance (T): Instance of the model to be validated.
        expression (str): The FHIRPath expression to evaluate.
        human (str): A human-readable description of the constraint.
        key (str): The key associated with the constraint.
        severity (str): The severity level of the constraint ('warning' or 'error').

    Returns:
        instance (type[T]): The validated model instance.

    Raises:
        PydanticCustomError: If the validation fails and severity is not `warning`.
        Warning: If the validation fails and severity is `warning`.
    """
    config = get_config()
    if config.validation_mode == "skip":
        return instance
    return _validate_FHIR_element_constraint(
        instance, instance, expression, human, key, severity
    )


def validate_FHIR_element_pattern(
    cls: Any,
    element: Union["FHIRBaseModel", List["FHIRBaseModel"], Any],
    pattern: Union["FHIRBaseModel", List["FHIRBaseModel"], Any],
) -> Any:
    """
    Validate the FHIR element against a specified pattern and return the element if it fulfills the pattern.

    Args:
        cls (Any): Placeholder for an argument that is not used in the function.
        element (Union[FHIRBaseModel, List[FHIRBaseModel]]): The FHIR element to validate against the pattern.
        pattern (Union[FHIRBaseModel, List[FHIRBaseModel]]): The pattern to validate the element against.

    Returns:
        Union[FHIRBaseModel, List[FHIRBaseModel]]: The validated FHIR element.

    Raises:
        PydanticCustomError: If the element does not fulfill the specified pattern.
    """
    from fhircraft.fhir.resources.base import FHIRBaseModel

    config = get_config()
    if config.validation_mode == "skip":
        return element

    if isinstance(pattern, list):
        pattern = pattern[0]
    _element = element[0] if isinstance(element, list) else element
    _element = (
        _element.model_dump() if isinstance(_element, FHIRBaseModel) else _element
    )
    _pattern = pattern.model_dump() if isinstance(pattern, FHIRBaseModel) else pattern
    if (isinstance(_pattern, dict) and not is_dict_subset(_pattern, _element)) or (
        not isinstance(_pattern, dict) and _element != _pattern
    ):
        error = f"Value does not fulfill pattern:\n{_pattern if not isinstance(pattern, FHIRBaseModel) else pattern.model_dump_json(indent=2)}"
        if config.validation_mode == "lenient":
            warnings.warn(str(error), FhirValidationWarning, stacklevel=2)
        else:
            raise PydanticCustomError("fhir_pattern_violation", str(error))  # type: ignore
    return element


def validate_FHIR_model_pattern(
    model: Union["FHIRBaseModel", List["FHIRBaseModel"], Any],
    pattern: Union["FHIRBaseModel", List["FHIRBaseModel"], Any],
) -> Any:
    """
    Validate the FHIR model against a specified pattern and return the model if it fulfills the pattern.

    Args:
        model (Union[FHIRBaseModel, List[FHIRBaseModel]]): The FHIR model to validate against the pattern.
        pattern (Union[FHIRBaseModel, List[FHIRBaseModel]]): The pattern to validate the model against.

    Returns:
        Union[FHIRBaseModel, List[FHIRBaseModel]]: The validated FHIR model.

    Raises:
        PydanticCustomError: If the model does not fulfill the specified pattern.
    """
    return validate_FHIR_element_pattern(cls=None, element=model, pattern=pattern)


def validate_FHIR_element_fixed_value(
    cls: Any,
    element: Union["FHIRBaseModel", List["FHIRBaseModel"], Any],
    constant: Union["FHIRBaseModel", List["FHIRBaseModel"], Any],
) -> Any:
    """
    Validate the FHIR element against a specified constant value and return the element if it fulfills the constant.

    Args:
        cls (Any): Placeholder for an argument that is not used in the function.
        element (Union[FHIRBaseModel, List[FHIRBaseModel]]): The FHIR element to validate against the constant.
        constant (Union[FHIRBaseModel, List[FHIRBaseModel]]): The constant value to validate the element against.

    Returns:
        Union[FHIRBaseModel, List[FHIRBaseModel]]: The validated FHIR element.

    Raises:
        PydanticCustomError: If the element does not fulfill the specified constant.
    """
    from fhircraft.fhir.resources.base import FHIRBaseModel

    config = get_config()
    if config.validation_mode == "skip":
        return element

    if isinstance(constant, list):
        constant = constant[0]
    _element = element[0] if isinstance(element, list) else element

    if isinstance(constant, FHIRBaseModel):
        constant = constant.model_dump()
    if isinstance(_element, FHIRBaseModel):
        _element = _element.model_dump()
    if constant != _element:
        error = f"Value does not fulfill constant:\n{constant.model_dump_json(indent=2) if isinstance(constant, FHIRBaseModel) else constant}"
        if config.validation_mode == "lenient":
            warnings.warn(error, FhirValidationWarning, stacklevel=2)
        else:
            raise PydanticCustomError("fhir_pattern_violation", str(error))  # type: ignore
    return element


def validate_FHIR_model_fixed_value(
    model: Union["FHIRBaseModel", List["FHIRBaseModel"], Any],
    constant: Union["FHIRBaseModel", List["FHIRBaseModel"], Any],
) -> Any:
    """
    Validate the FHIR model against a specified constant value and return the model if it fulfills the constant.

    Args:
        model (Union[FHIRBaseModel, List[FHIRBaseModel]]): The FHIR model to validate against the constant.
        constant (Union[FHIRBaseModel, List[FHIRBaseModel]]): The constant value to validate the model against.

    Returns:
        Union[FHIRBaseModel, List[FHIRBaseModel]]: The validated FHIR element.

    Raises:
        PydanticCustomError: If the element does not fulfill the specified constant.
    """
    return validate_FHIR_element_fixed_value(cls=None, element=model, constant=constant)


def validate_type_choice_element(
    instance: T,
    field_types: List[Any],
    field_name_base: str,
    required: bool = False,
    non_allowed_types=[],
) -> T:
    """
    Validate the type choice element for a given instance.

    Args:
        instance (T): The instance to validate.
        field_types (List[Any]): List of field types to check.
        field_name_base (str): Base name of the field.
        required (bool): Whether the type choice element is required.
        non_allowed_types (List[Any] | None): List of types that are not allowed for this element (for negative checks).

    Returns:
        T: The validated instance.

    Raises:
        PydanticCustomError: If more than one value is set for the type choice element or if a non-allowed type is set.
    """

    config = get_config()
    if config.validation_mode == "skip":
        return instance

    _field_types: List[str] = [
        (
            capitalize(field_type)
            if isinstance(field_type, str)
            else capitalize(str(field_type.__name__))
        )
        for field_type in field_types
    ]
    types_set_count = sum(
        (
            element is not None
            if not isinstance(
                element := getattr(
                    instance,
                    (field_name_base + field_type),
                    None,
                ),
                FHIRPrimitiveModel,
            )
            else element.value is not None
        )
        for field_type in _field_types
    )

    def _assert(condition: bool, message: str) -> None:
        if not condition:
            if config.validation_mode == "lenient":
                warnings.warn(message, FhirValidationWarning, stacklevel=2)
            else:
                raise PydanticCustomError("fhir_type_choice_violation", message)  # type: ignore

    _assert(
        types_set_count <= 1,
        f"Type choice element {field_name_base}[x] can only have one value set.",
    )
    _assert(
        not required or types_set_count > 0,
        f"Type choice element {field_name_base}[x] must have one value set. Got {types_set_count}.",
    )
    all_types = [
        field.replace(field_name_base, "")
        for field in instance.__class__.model_fields
        if field.startswith(field_name_base)
    ]
    # Check that non-allowed types are not set
    non_allowed_types = non_allowed_types or [
        field_type for field_type in all_types if field_type not in _field_types
    ]
    if non_allowed_types:
        for non_allowed_type in non_allowed_types:
            field_name = field_name_base + (
                non_allowed_type
                if isinstance(non_allowed_type, str)
                else non_allowed_type.__name__
            )
            value = getattr(instance, field_name, None)
            _assert(
                value is None,
                f"Type choice element {field_name_base}[x] cannot use non-allowed type '{non_allowed_type}'. Only the following types are allowed: {', '.join(_field_types)}. Got non-allowed type '{non_allowed_type}' with value '{value}'.",
            )

    return instance


def validate_slicing_cardinalities(
    cls: Any, values: List[Any] | None, field_name: str
) -> List["FHIRSliceModel"] | None:
    """
    Validates the cardinalities of FHIR slices for a specific field within a FHIR resource.

    Args:
        cls (Any): The Pydantic FHIR model class.
        values (List[Any]): List of values for the field.
        field_name (str): The name of the field to validate.

    Returns:
        List[FHIRSliceModel]: The validated list of values.

    Raises:
        AssertionError: If cardinality constraints are violated for any slice.
    """
    from fhircraft.config import get_config
    from fhircraft.fhir.resources.base import FHIRSliceModel

    config = get_config()
    if config.validation_mode == "skip":
        return values

    if values is None:
        return values
    slices = get_all_models_from_field(
        cls.model_fields[field_name], issubclass_of=FHIRSliceModel
    )
    for slice in slices:
        slice_instances_count = sum([isinstance(value, slice) for value in values])
        # Only validate cardinalities if there are instances of the slice present
        if slice_instances_count > 0:
            if slice_instances_count < slice.min_cardinality:
                message = f"Slice '{slice.__name__}' for field '{field_name}' violates its min. cardinality. \
                        Requires min. cardinality of {slice.min_cardinality}, but got {slice_instances_count}"
                if config.validation_mode == "lenient":
                    warnings.warn(message, FhirValidationWarning, stacklevel=2)
                else:
                    raise PydanticCustomError("fhir_cardinality_violation", message)  # type: ignore
            if slice.max_cardinality is not None:
                if slice_instances_count > slice.max_cardinality:
                    message = f"Slice '{slice.__name__}' for field '{field_name}' violates its max. cardinality. \
                            Requires max. cardinality of {slice.max_cardinality}, but got {slice_instances_count}"
                    if config.validation_mode == "lenient":
                        warnings.warn(message, FhirValidationWarning, stacklevel=2)
                    else:
                        raise PydanticCustomError("fhir_cardinality_violation", message)  # type: ignore
    return values


def get_type_choice_value_by_base(instance: BaseModel, base: str) -> Any:
    """
    Retrieve the value of a type-choice field in an instance based on the field
    name starting with a specific base string.

    Args:
        instance (object): The instance object to retrieve the value from.
        base (str): The base string that the field name should start with.

    Returns:
        value (Any): The value of the first field found in the instance that starts with the specified base string,
                    or `None` if no such field exists or the value is `None`.
    """
    for field in instance.__class__.model_fields:
        if field.startswith(base):
            value = getattr(instance, field)
            if value is not None:
                return value
