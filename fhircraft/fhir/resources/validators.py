# Fhircraft modules
import traceback
import warnings

# Standard modules
from typing import Any, List, TypeVar, Union, TYPE_CHECKING

from pydantic import BaseModel, ValidationError

if TYPE_CHECKING:
    from fhircraft.fhir.resources.base import FHIRBaseModel, FHIRSliceModel

from fhircraft.utils import ensure_list, get_all_models_from_field, merge_dicts

T = TypeVar("T", bound=BaseModel)


def _validate_FHIR_element_constraint(
    value: Any, expression: str, human: str, key: str, severity: str
):
    """
    Validate FHIR element constraint against a FHIRPath expression.

    Args:
        value (Any): The value to validate.
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
    from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem
    from fhircraft.fhir.path.exceptions import (
        FhirPathLexerError,
        FhirPathParserError,
        FhirPathWarning,
    )
    from fhircraft.fhir.path.parser import fhirpath

    if value is None:
        return value
    for item in ensure_list(value):
        try:
            valid = fhirpath.parse(expression).single(item, default=True)
            error_message = f'{human}. [{key}] -> "{expression}"'
            if severity == "warning" and not valid:
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
                f"Warning: FHIRPath raised {e.__class__.__name__} for expression: {expression}. {traceback.format_exc()}"
            )
    return value


def validate_element_constraint(
    cls, value: Any, expression: str, human: str, key: str, severity: str
) -> Any:
    """
    Validates a FHIR element constraint based on a FHIRPath expression.

    Args:
        cls (Any): Placeholder for an argument that is not used in the function.
        value (Any): The value to be validated.
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
    return _validate_FHIR_element_constraint(value, expression, human, key, severity)


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
    return _validate_FHIR_element_constraint(instance, expression, human, key, severity)


def validate_FHIR_element_pattern(
    cls: Any,
    element: Union["FHIRBaseModel", List["FHIRBaseModel"]],
    pattern: Union["FHIRBaseModel", List["FHIRBaseModel"]],
) -> Union["FHIRBaseModel", List["FHIRBaseModel"]]:
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
    if isinstance(pattern, list):
        pattern = pattern[0]
    _element = element[0] if isinstance(element, list) else element
    assert (
        merge_dicts(_element.model_dump(), pattern.model_dump())
        == _element.model_dump()
    ), f"Value does not fulfill pattern:\n{pattern.model_dump_json(indent=2)}"
    return element


def validate_type_choice_element(
    instance: T, field_types: List[Any], field_name_base: str, required: bool = False
) -> T:
    """
    Validate the type choice element for a given instance.

    Args:
        instance (T): The instance to validate.
        field_types (List[Any]): List of field types to check.
        field_name_base (str): Base name of the field.

    Returns:
        T: The validated instance.

    Raises:
        AssertionError: If more than one value is set for the type choice element.
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
    return instance


def validate_slicing_cardinalities(
    cls: Any, values: List[Any], field_name: str
) -> List["FHIRSliceModel"]:
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


def validate_contained_resource(
    cls, resources: Any, release: str
) -> List["FHIRBaseModel"] | None:
    """
    Validate that a contained resource is a valid FHIR resource.

    Args:
        cls (Any): Placeholder for an argument that is not used in the function.
        resources (Any): The contained resource to validate.
        release (str): The FHIR release version to use for validation.

    Returns:
        FHIRBaseModel: The validated contained resource.

    Raises:
        TypeError: If the contained resource is not a FHIRBaseModel or a dict.
    """
    from fhircraft.fhir.resources.datatypes.utils import get_fhir_resource_type
    from fhircraft.fhir.resources.base import FHIRBaseModel
    
    if not resources:
        return None
    if not isinstance(resources, list):
        resources = [resources]
    validated_resources = []
    for i, resource in enumerate(resources):
        if isinstance(resource, FHIRBaseModel):
            validated_resources.append(resource)
        if isinstance(resource, dict) and "resourceType" in resource:
            resourceModel = get_fhir_resource_type(
                resource["resourceType"], release=release
            )
            validated_resources.append(resourceModel.model_validate(resource))
        else:
            raise ValidationError(
                "Contained resource must be a FHIRBaseModel or a dict, and must have a 'resourceType' property."
            )

    return validated_resources
