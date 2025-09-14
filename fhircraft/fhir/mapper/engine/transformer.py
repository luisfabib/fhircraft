import re
import uuid
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, List

from pydantic import BaseModel

import fhircraft.fhir.path.engine as fhirpath
from fhircraft.fhir.mapper.structures.StructureMap import StructureMapParameter
from fhircraft.fhir.path import fhirpath as fhirpath_parser
from fhircraft.fhir.resources.datatypes.R4B.complex_types import (
    CodeableConcept,
    Coding,
    ContactPoint,
    Identifier,
    Quantity,
)

from .exceptions import MappingError, RuleProcessingError
from .scope import MappingScope


@dataclass
class TransformParameter:
    name: str
    type: str
    is_optional: bool = False


def validate_transform_parameters(
    *signatures: list[TransformParameter],
) -> Callable:
    """
    Decorator to validate transform parameters.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(
            scope: MappingScope, parameters: List[StructureMapParameter]
        ) -> Any:
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
                    print(transform_arguments)
                    # All parameters match this signature
                    return func(scope, **transform_arguments)
            raise RuleProcessingError(
                f"Parameters did not match any valid signature for {func.__name__}. {error}"
            )

        return wrapper

    return decorator


class MappingTransformer:

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

    def execute(self, name: str, scope, parameters):
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
        return scope.get_type(type).model_construct()

    @staticmethod
    @validate_transform_parameters(
        [
            TransformParameter("source", "Id"),
            TransformParameter("length", "Integer"),
        ],
    )
    def _truncate_transform(scope: MappingScope, source: str, length: int) -> str:
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
        source_fhirpath = scope.resolve_fhirpath(source)
        resource_type = source_fhirpath._invoke(
            fhirpath.Element("resourceType")
        ).single(scope.get_instances())
        resource_id = source_fhirpath._invoke(fhirpath.Element("id")).single(
            scope.get_instances()
        )
        return f"{resource_type}/{resource_id}"

    @staticmethod
    @validate_transform_parameters()
    def _uuid_transform(scope: MappingScope) -> str:
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
        source_code = scope.resolve_fhirpath(source).single(scope.get_instances())
        concept_map = scope.get_concept_map(map_name.lstrip("#"))
        if concept_map.group is None:
            raise MappingError(f"Concept map '{map_name}' has no groups defined.")
        for group in concept_map.group:
            for element in group.element:
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
        if value and not system:
            raise NotImplementedError(
                "Implicit system detection for the 'cp' transform is not yet supported. Please specify the system explicitly."
            )
        return ContactPoint(
            system=system,
            value=value,
        )
