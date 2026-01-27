# Fhircraft modules
import traceback
import warnings

# Standard modules
from typing import TYPE_CHECKING, Any, List, TypeVar, Union, Sequence

from pydantic import BaseModel

if TYPE_CHECKING:
    from fhircraft.fhir.resources.base import FHIRBaseModel, FHIRSliceModel

from fhircraft.fhir.path.engine import environment
from fhircraft.utils import ensure_list, get_all_models_from_field, merge_dicts

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
        AssertionError: If the validation fails and severity is not 'warning'.
        Warning: If the validation fails and severity is 'warning'.
    """
    from fhircraft.config import get_config
    from fhircraft.fhir.path.exceptions import (
        FhirPathLexerError,
        FhirPathParserError,
        FhirPathWarning,
    )
    from fhircraft.fhir.path.parser import fhirpath

    # Check configuration for validation control
    config = get_config()
    validation_config = config.validation

    # Skip validation if mode is 'skip'
    if validation_config.mode == "skip":
        return value

    # Skip if this specific constraint is disabled
    if key in validation_config.disabled_constraints:
        return value

    # Skip if all warnings are disabled and this is a warning
    if severity == "warning" and (
        validation_config.disable_warnings or validation_config.disable_warning_severity
    ):
        return value

    # Skip if all errors are disabled and this is an error
    if severity == "error" and validation_config.disable_errors:
        return value

    # In lenient mode, convert errors to warnings
    effective_severity = severity
    if validation_config.mode == "lenient" and severity == "error":
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
            valid = fhirpath.parse(expression).single(
                item, default=True, environment=environment
            )
            error_message = f"[{key}] {human}. -> {expression}"
            if element:
                error_message = f"{element}\n\t{error_message}"
            if effective_severity == "warning" and not valid:
                warnings.warn(error_message, FhirPathWarning)
            else:
                assert valid, error_message
        except (
            ValueError,
            FhirPathLexerError,
            FhirPathParserError,
            AttributeError,
            NotImplementedError,
        ) as e:
            warnings.warn(
                f"Warning: FHIRPath raised {e.__class__.__name__} for expression: [{key}] -> {expression}. {traceback.format_exc()}"
            )
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
        AssertionError: If the validation fails and severity is not `warning`.
        Warning: If the validation fails and severity is `warning`.
    """
    for element in elements:
        value = getattr(instance, element)
        if not value:
            continue
        _validate_FHIR_element_constraint(
            value, instance, expression, human, key, severity
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
        AssertionError: If the validation fails and severity is not `warning`.
        Warning: If the validation fails and severity is `warning`.
    """
    return _validate_FHIR_element_constraint(
        instance, instance, expression, human, key, severity
    )


def validate_FHIR_element_pattern(
    cls: Any,
    element: Union["FHIRBaseModel", List["FHIRBaseModel"]],
    pattern: Union["FHIRBaseModel", List["FHIRBaseModel"], Any],
) -> Union["FHIRBaseModel", List["FHIRBaseModel"], Any]:
    """
    Validate the FHIR element against a specified pattern and return the element if it fulfills the pattern.

    Args:
        cls (Any): Placeholder for an argument that is not used in the function.
        element (Union[FHIRBaseModel, List[FHIRBaseModel]]): The FHIR element to validate against the pattern.
        pattern (Union[FHIRBaseModel, List[FHIRBaseModel]]): The pattern to validate the element against.

    Returns:
        Union[FHIRBaseModel, List[FHIRBaseModel]]: The validated FHIR element.

    Raises:
        AssertionError: If the element does not fulfill the specified pattern.
    """
    from fhircraft.fhir.resources.base import FHIRBaseModel

    if isinstance(pattern, list):
        pattern = pattern[0]
    _element = element[0] if isinstance(element, list) else element
    if isinstance(_element, FHIRBaseModel):
        assert (
            merge_dicts(_element.model_dump(), pattern.model_dump())
            == _element.model_dump()
        ), f"Value does not fulfill pattern:\n{pattern.model_dump_json(indent=2)}"
    elif isinstance(_element, dict) and isinstance(pattern, dict):
        assert (
            merge_dicts(_element, pattern) == _element
        ), f"Value does not fulfill pattern: {pattern}"
    else:
        assert _element == pattern, f"Value does not fulfill pattern: {pattern}"
    return element


def validate_type_choice_element(
    instance: T,
    field_types: List[Any],
    field_name_base: str,
    required: bool = False,
    non_allowed_types: List[Any] | None = None,
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
        AssertionError: If more than one value is set for the type choice element or if a non-allowed type is set.
    """
    types_set_count = sum(
        (
            getattr(
                instance,
                (
                    field_name_base
                    + (
                        field_type
                        if isinstance(field_type, str)
                        else field_type.__name__
                    )
                ),
                None,
            )
        )
        is not None
        for field_type in field_types
    )
    assert (
        types_set_count <= 1
    ), f"Type choice element {field_name_base}[x] can only have one value set."
    assert not required or (
        required and types_set_count > 0
    ), f"Type choice element {field_name_base}[x] must have one value set. Got {types_set_count}."

    # Check that non-allowed types are not set
    if non_allowed_types:
        for non_allowed_type in non_allowed_types:
            field_name = field_name_base + (
                non_allowed_type
                if isinstance(non_allowed_type, str)
                else non_allowed_type.__name__
            )
            value = getattr(instance, field_name, None)
            assert (
                value is None
            ), f"Type choice element {field_name_base}[x] cannot use non-allowed type '{non_allowed_type}'. "

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
    from fhircraft.fhir.resources.base import FHIRSliceModel

    if values is None:
        return values
    slices = get_all_models_from_field(
        cls.model_fields[field_name], issubclass_of=FHIRSliceModel
    )
    for slice in slices:
        slice_instances_count = sum([isinstance(value, slice) for value in values])
        assert (
            slice_instances_count >= slice.min_cardinality
        ), f"Slice '{slice.__name__}' for field '{field_name}' violates its min. cardinality. \
                Requires min. cardinality of {slice.min_cardinality}, but got {slice_instances_count}"
        assert (
            slice_instances_count <= slice.max_cardinality
        ), f"Slice '{slice.__name__}' for field '{field_name}' violates its max. cardinality. \
                Requires max. cardinality of {slice.max_cardinality}, but got {slice_instances_count}"
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
