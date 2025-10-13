import re
import uuid
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, List

from pydantic import BaseModel

import fhircraft.fhir.path.engine as fhirpath
from fhircraft.fhir.path.parser import fhirpath as fhirpath_parser
from fhircraft.fhir.resources.datatypes.R4B.complex_types import (
    CodeableConcept,
    Coding,
    ContactPoint,
    Identifier,
    Quantity,
)
from fhircraft.fhir.resources.datatypes.R5.resources.structure_map import (
    StructureMapGroupRuleTargetParameter as StructureMapParameter,
)

from .exceptions import MappingError, RuleProcessingError
from .scope import MappingScope


@dataclass
class TransformParameter:
    """
    Represents a parameter used in a transformation process.
    """

    name: str
    """The name of the parameter."""

    type: str
    """The data type of the parameter."""

    is_optional: bool = False
    """Indicates whether the parameter is optional. Defaults to False."""


def validate_transform_parameters(
    *signatures: list[TransformParameter],
) -> Callable:
    """
    A decorator to validate the parameters passed to a transformation function against one or more expected signatures.

    Each signature is a list of `TransformParameter` objects that define the expected parameter names, types, and whether they are optional.
    The decorator checks if the provided parameters match any of the given signatures in terms of count and type.
    If a match is found, the decorated function is called with the validated and unpacked parameters.
    If no signature matches, a `RuleProcessingError` is raised.

    Args:
        *signatures (list[TransformParameter]): One or more lists of `TransformParameter` objects representing valid parameter signatures.

    Returns:
        Callable: A decorator that wraps the target function with parameter validation logic.

    Raises:
        RuleProcessingError: If the provided parameters do not match any of the given signatures.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(
            scope: MappingScope, parameters: List[StructureMapParameter]
        ) -> Any:
            error = ""
            if not signatures:
                # No validation required
                return func(scope)
            # Try all signatures; only raise if none match
            for signature in signatures:
                min_count = sum(1 for param in signature if not param.is_optional)
                max_count = len(signature)
                if len(parameters) < min_count or len(parameters) > max_count:
                    error = f"{func.__name__} requires between {min_count} and {max_count} parameters, but got {len(parameters)}."
                    continue
                transform_arguments = {}
                for param, expected in zip(parameters, signature):
                    if (value := getattr(param, f"value{expected.type}", None)) is None:
                        error = f"Parameter '{expected.name}' expected type '{expected.type}', but got '{type(param)}'."
                        break
                    transform_arguments[expected.name] = value
                else:
                    # All parameters match this signature
                    return func(scope, **transform_arguments)
            # No signature matched
            raise RuleProcessingError(
                f"Parameters did not match any valid signature for {func.__name__}. {error}"
            )

        return wrapper

    return decorator


class MappingTransformer:
    """
    MappingTransformer is responsible for executing various FHIR Mapping Language transforms
    within a mapping scope. It provides implementations for a set of standard transforms
    (such as copy, create, truncate, cast, append, reference, uuid, translate, evaluate, etc.)
    used in FHIR StructureMap-based data transformations.

    Attributes:
        _transforms (dict): A mapping of transform names to their corresponding handler methods.

    Raises:
        MappingError: If an invalid or unsupported transform is requested.
        NotImplementedError: If a requested transform or feature is not implemented.
        RuleProcessingError: For invalid parameters or processing errors in transforms.
    """

    def __init__(self):
        self._transforms = {
            "copy": self._copy_transform,
            "create": self._create_transform,
            "truncate": self._truncate_transform,
            "escape": None,  # Not implemented yet
            "cast": self._cast_transform,
            "append": self._append_transform,
            "reference": self._reference_transform,
            "dateOp": None,  # Not implemented yet
            "uuid": self._uuid_transform,
            "pointer": None,  # Not implemented yet
            "translate": self._translate_transform,
            "evaluate": self._evaluate_transform,
            "cc": self._cc_transform,
            "c": self._c_transform,
            "qty": self._qty_transform,
            "id": self._id_transform,
            "cp": self._cp_transform,
        }

    def execute(
        self, name: str, scope: MappingScope, parameters: List[StructureMapParameter]
    ) -> Any:
        """
        Executes a registered FHIR Mapping Language transform by name.

        Args:
            name: The name of the transform to execute.
            scope: The current execution scope or context for the transform.
            parameters: Parameters to be passed to the transform function.

        Returns:
            result (Any): The result of the executed transform function.

        Raises:
            MappingError: If the specified transform name is not registered.
            NotImplementedError: If the transform is registered but not implemented.
        """
        if name not in self._transforms:
            raise MappingError(f"Invalid FHIR Mapping Language transform: {name}")
        if not (transform := self._transforms[name]):
            raise NotImplementedError(f"Transform '{name}' is not implemented.")
        return transform(scope, parameters)

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("source", "Id"),
        ],
        [
            TransformParameter("literal", ""),
        ],
    )
    def _copy_transform(
        scope: MappingScope, source: str | None = None, literal: str | None = None
    ) -> Any:
        """
        Copies a value from the source or uses a provided literal.

        This function attempts to copy a value from the specified `source` using FHIRPath resolution within the given `scope`.
        If `source` is not provided, it returns the given `literal` value instead.

        Args:
            scope (MappingScope): The mapping scope containing context and instances for FHIRPath resolution.
            source (str | None, optional): The FHIRPath expression or key to resolve and copy the value from. Defaults to None.
            literal (str | None, optional): A literal value to use if `source` is not provided. Defaults to None.

        Returns:
            Any: The copied value from the source or the provided literal.

        """
        # Just copy the source value or use the literal
        if source:
            source_fhirpath = scope.resolve_fhirpath(source)
            # Just copy the source value
            return source_fhirpath.single(scope.get_instances())
        elif literal:
            # Just use the literal value
            return literal

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("type", ""),
        ],
    )
    def _create_transform(scope: MappingScope, type: str) -> BaseModel:
        """
        Creates and returns a new instance of a model of the specified type using the provided mapping scope.

        Args:
            scope (MappingScope): The mapping scope containing type definitions and model constructors.
            type (str): The name of the type for which to create a new model instance.

        Returns:
            BaseModel: A newly constructed instance of the specified model type.
        """
        return scope.get_type(type).model_construct()

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("source", "Id"),
            TransformParameter("length", "Integer"),
        ],
    )
    def _truncate_transform(scope: MappingScope, source: str, length: int) -> str:
        """
        Truncates the value obtained from a FHIRPath expression to a specified length.

        Args:
            scope (MappingScope): The current mapping scope containing context and data.
            source (str): The FHIRPath expression or field name to resolve and truncate.
            length (int): The maximum number of characters to retain from the source value.

        Returns:
            str: The truncated string result from the FHIRPath expression.

        Raises:
            Any exceptions raised by `scope.resolve_fhirpath` or FHIRPath evaluation.
        """
        source_fhirpath = scope.resolve_fhirpath(source)
        return source_fhirpath._invoke(fhirpath.Substring(0, int(length))).single(
            scope.get_instances()
        )

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("source", "Id"),
            TransformParameter("to_type", "String"),
        ],
    )
    def _cast_transform(
        scope: MappingScope, source: str, to_type: str | None = None
    ) -> Any:
        """
        Casts the value of a FHIRPath expression to a specified target type.

        Args:
            scope (MappingScope): The current mapping scope containing context and instance data.
            source (str): The FHIRPath expression or field name to be cast.
            to_type (str | None, optional): The target type to cast the value to. Must be explicitly specified.

        Returns:
            Any: The value of the source FHIRPath expression cast to the specified type.

        Raises:
            NotImplementedError: If the target type (`to_type`) is not specified.

        Notes:
            Implicit type casting is not supported; the target type must be provided.
        """
        if not to_type:
            raise NotImplementedError(
                "Implicit type casting if not yet supported for the 'cast' transform. Please specify the target type explicitly."
            )
        source_fhirpath = scope.resolve_fhirpath(source)
        return source_fhirpath._invoke(
            getattr(fhirpath, f"To{to_type.title()}")()
        ).single(scope.get_instances())

    @staticmethod
    def _append_transform(
        scope: MappingScope, parameters: List[StructureMapParameter]
    ) -> str:
        """
        Appends the string representations of the provided parameters.

        This method processes a list of `StructureMapParameter` objects, extracting their `valueId` or `valueString` attributes.
        For each parameter:
        - If `valueId` is present, it resolves the FHIRPath and appends its string value.
        - If `valueString` is present, it appends the string directly.
        - If neither is present, it raises a `RuleProcessingError`.

        Args:
            scope (MappingScope): The current mapping scope used to resolve FHIRPath expressions.
            parameters (List[StructureMapParameter]): A list of parameters to be appended. Each parameter must have either a `valueId` or `valueString`.

        Returns:
            str: The concatenated string of all parameter values.

        Raises:
            RuleProcessingError: If no parameters are provided, or if a parameter does not have a valid type (`valueId` or `valueString`).
        """
        if not parameters or len(parameters) < 1:
            raise RuleProcessingError(
                "The 'append' transform requires at least one parameter of type Id and String"
            )
        strings = []
        for parameter in parameters:
            if parameter.valueId:
                source_fhirpath = scope.resolve_fhirpath(parameter.valueId)
                strings.append(str(source_fhirpath.single(scope.get_instances())))
            elif parameter.valueString:
                strings.append(parameter.valueString)
            else:
                raise RuleProcessingError(
                    "Invalid parameter type for 'append' transform"
                )
        return "".join(strings)

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("source", "Id"),
        ],
    )
    def _reference_transform(scope: MappingScope, source: str) -> str:
        """
        Transforms a FHIR resource reference by extracting its resource type and ID from the given source.

        Args:
            scope (MappingScope): The current mapping scope containing context and instances.
            source (str): The FHIRPath expression or reference to the source resource.

        Returns:
            str: A string in the format "ResourceType/ResourceId" representing the FHIR reference.

        Raises:
            Any exception raised by `scope.resolve_fhirpath` or the FHIRPath evaluation methods if the resource type or ID cannot be resolved.
        """
        source_fhirpath = scope.resolve_fhirpath(source)
        resource_type = (
            source_fhirpath._invoke(fhirpath.Element("resourceType")).single(
                scope.get_instances()
            )
            or source_fhirpath.single(scope.get_instances()).__class__.__name__
        )
        resource_id = source_fhirpath._invoke(fhirpath.Element("id")).single(
            scope.get_instances()
        )
        return f"{resource_type}/{resource_id}"

    @staticmethod
    @validate_transform_parameters()
    def _uuid_transform(scope: MappingScope) -> str:
        """
        Generates a new UUID string.

        Args:
            scope (MappingScope): The current mapping scope (unused in this function).

        Returns:
            str: A newly generated UUID as a string.
        """
        return str(uuid.uuid4())

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("source", "Id"),
            TransformParameter("map_name", "String"),
            TransformParameter("output", "String", is_optional=True),
        ],
    )
    def _translate_transform(
        scope: MappingScope, source: str, map_name: str, output: str = "code"
    ) -> str:
        """
        Translates a source code using a specified FHIR ConceptMap.

        Args:
            scope (MappingScope): The current mapping scope, providing access to FHIRPath resolution and ConceptMaps.
            source (str): The FHIRPath expression or identifier for the source code to be translated.
            map_name (str): The name (optionally prefixed with '#') of the ConceptMap to use for translation.
            output (str, optional): The desired output type. Currently, only "code" is supported. Defaults to "code".

        Returns:
            str: The translated target code from the ConceptMap.

        Raises:
            MappingError: If the ConceptMap has no groups, if a target code is not defined for the source code,
                          or if the source code cannot be mapped using the ConceptMap.
            NotImplementedError: If an unsupported output mode is requested.
        """
        source_code = scope.resolve_fhirpath(source).single(scope.get_instances())
        concept_map = scope.get_concept_map(map_name.lstrip("#"))
        if concept_map.group is None:
            raise MappingError(f"Concept map '{map_name}' has no groups defined.")
        for group in concept_map.group:
            for element in group.element or []:
                if element.target is None:
                    continue
                for element_target in element.target:
                    if element.code == source_code:
                        if output == "code":
                            if element_target.code is None:
                                raise MappingError(
                                    f"Concept map '{map_name}' does not define a target code for source code '{source_code}'."
                                )
                            return element_target.code
                        else:
                            raise NotImplementedError(
                                f"Output mode '{output}' for translate operation is not yet implemented."
                            )
        else:
            raise MappingError(
                f"Could not map source code '{source_code}' using concept map '{map_name}'."
            )

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("source", "Id"),
            TransformParameter("evaluate_fhirpath", "String"),
        ],
        [
            TransformParameter("evaluate_fhirpath", "String"),
        ],
    )
    def _evaluate_transform(
        scope: MappingScope,
        evaluate_fhirpath: str,
        source: str | None = None,
    ) -> Any:
        """
        Evaluates a FHIRPath expression against a specified source within the given mapping scope.

        Args:
            scope (MappingScope): The current mapping scope containing context and instances.
            evaluate_fhirpath (str): The FHIRPath expression to evaluate.
            source (str | None, optional): The source FHIRPath context to resolve. Must be provided.

        Returns:
            Any: The single value resulting from the FHIRPath evaluation, or None if no value is found.

        Raises:
            NotImplementedError: If the source is not provided (implicit FHIRPath context is not supported).
            MappingError: If the FHIRPath expression yields more than one value.
        """
        if not source:
            raise NotImplementedError(
                "The evaluate transforms with implicit FHIRPath context is not supported."
            )
        context = scope.resolve_fhirpath(source).single(scope.get_instances())
        transformed_values = fhirpath_parser.parse(evaluate_fhirpath).values(context)
        if transformed_values and len(transformed_values) > 1:
            raise MappingError(
                f"Currently, the evaluate transform only supports FHIRPath expressions that yield a single value. It returned {len(transformed_values)}"
            )
        return transformed_values[0] if transformed_values else None

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("text", "String"),
        ],
        [
            TransformParameter("code", "String"),
            TransformParameter("system", "String"),
            TransformParameter("display", "String", is_optional=True),
        ],
    )
    def _cc_transform(
        scope: MappingScope,
        text: str | None = None,
        code: str | None = None,
        system: str | None = None,
        display: str | None = None,
    ) -> CodeableConcept:
        """
        Transforms the provided code, system, display, and text values into a CodeableConcept instance.

        If only `text` is provided (and `code`, `system`, and `display` are all None), returns a CodeableConcept with the text set.
        Otherwise, returns a CodeableConcept with a single Coding element constructed from the provided `code`, `system`, and `display`.

        Args:
            scope (MappingScope): The current mapping scope (not used in this function).
            text (str | None, optional): The text representation of the concept.
            code (str | None, optional): The code value for the Coding.
            system (str | None, optional): The system URI for the Coding.
            display (str | None, optional): The display text for the Coding.

        Returns:
            CodeableConcept: The constructed CodeableConcept instance.
        """
        if text and not code and not system and not display:
            return CodeableConcept(text=text)
        else:
            return CodeableConcept(
                coding=[
                    Coding(
                        code=code,
                        system=system,
                        display=display,
                    )
                ]
            )

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("code", "String"),
            TransformParameter("system", "String"),
            TransformParameter("display", "String", is_optional=True),
        ],
    )
    def _c_transform(
        scope: MappingScope,
        code: str | None = None,
        system: str | None = None,
        display: str | None = None,
    ) -> Coding:
        """
        Creates a FHIR Coding object with the provided code, system, and display values.

        Args:
            scope (MappingScope): The current mapping scope, providing context for the transformation.
            code (str | None, optional): The code value for the Coding. Defaults to None.
            system (str | None, optional): The system URI for the Coding. Defaults to None.
            display (str | None, optional): The display text for the Coding. Defaults to None.

        Returns:
            Coding: A FHIR Coding object populated with the specified code, system, and display.
        """
        return Coding(
            code=code,
            system=system,
            display=display,
        )

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("text", "String"),
        ],
        [
            TransformParameter("value", "String"),
            TransformParameter("unit", "String"),
        ],
        [
            TransformParameter("value", "String"),
            TransformParameter("unit", "String"),
            TransformParameter("system", "String"),
            TransformParameter("code", "String"),
        ],
    )
    def _qty_transform(
        scope: MappingScope,
        text: str | None = None,
        value: str | None = None,
        unit: str | None = None,
        system: str | None = None,
        code: str | None = None,
    ) -> Quantity:
        """
        Transforms quantity-related input parameters into a FHIR Quantity object.

        This function supports two modes of operation:
        1. Parsing a single `text` parameter of the form '[<|<=|>=|>|ad]<number> <unit>', extracting the comparator, value, and unit.
        2. Using explicit `value` and `unit` parameters (with optional `system` and `code`).

        Args:
            scope (MappingScope): The mapping scope context (not used in this function).
            text (str | None, optional): A string representing the quantity, possibly with a comparator and unit.
            value (str | None, optional): The numeric value of the quantity, as a string.
            unit (str | None, optional): The unit of the quantity.
            system (str | None, optional): The system that identifies the coded unit (optional).
            code (str | None, optional): The code that identifies the unit (optional).

        Returns:
            Quantity: A FHIR Quantity object constructed from the provided parameters.

        Raises:
            RuleProcessingError: If the `text` parameter does not match the expected format.
            AssertionError: If neither `text` nor both `value` and `unit` are provided.
        """
        if text:
            matches = re.search(r"(<|<=|>=|>|ad)?(\d+((\.|\,)\d+)?) (.*)", text)
            if not matches:
                raise RuleProcessingError(
                    "The 'qty' transform single parameter must be of the form '[<|<=|>=|>|ad]<number> <unit>'"
                )

            return Quantity(
                comparator=matches.group(1) if matches.group(1) else None,
                value=float(matches.group(2).replace(",", ".")),
                unit=matches.group(5),
                system=None,
                code=None,
            )
        else:
            assert value and unit
            return Quantity(
                value=float(value),
                unit=unit,
                system=system,
                code=code,
            )

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("system", "String"),
            TransformParameter("value", "String"),
            TransformParameter("type", "String", is_optional=True),
        ],
    )
    def _id_transform(
        scope: MappingScope, system: str, value: str, type: str | None = None
    ) -> Identifier:
        """
        Transforms the given system, value, and optional type into a FHIR Identifier object.

        Args:
            scope (MappingScope): The current mapping scope (context for the transformation).
            system (str): The identifier system URI.
            value (str): The identifier value.
            type (str | None, optional): The code representing the type of identifier. If provided, a CodeableConcept is created for the type.

        Returns:
            Identifier: A FHIR Identifier object constructed from the provided parameters.
        """
        return Identifier(
            system=system,
            value=value,
            type=(
                CodeableConcept(
                    coding=[
                        Coding(
                            code=type,
                            system="http://hl7.org/fhir/ValueSet/identifier-type",
                        )
                    ]
                )
                if type
                else None
            ),
        )

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("value", "String"),
        ],
        [
            TransformParameter("system", "String"),
            TransformParameter("value", "String"),
        ],
    )
    def _cp_transform(
        scope: MappingScope,
        value: str | None = None,
        system: str | None = None,
    ) -> ContactPoint:
        """
        Transforms the given value and system into a ContactPoint instance.

        Args:
            scope (MappingScope): The current mapping scope (not used in this implementation).
            value (str | None, optional): The contact point value (e.g., phone number, email address). Defaults to None.
            system (str | None, optional): The contact point system (e.g., 'phone', 'email'). If not provided, raises NotImplementedError. Defaults to None.

        Returns:
            ContactPoint: A ContactPoint instance with the specified system and value.

        Raises:
            NotImplementedError: If value is provided but system is not specified, as implicit system detection is not supported.
        """
        if value and not system:
            raise NotImplementedError(
                "Implicit system detection for the 'cp' transform is not yet supported. Please specify the system explicitly."
            )
        return ContactPoint(
            system=system,
            value=value,
        )
