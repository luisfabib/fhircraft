from abc import ABC
import re
from sys import path
from typing import TYPE_CHECKING, Any, Sequence, Tuple, Type
from fhircraft.fhir.mapper.engine.abstract import FHIRMappingEngineComponent
from fhircraft.fhir.path import engine as fp, fhirpath as fhirpath_parser
from fhircraft.fhir.mapper.engine.exceptions import MappingError
import uuid

from fhircraft.fhir.path.engine.core import FHIRPath

if TYPE_CHECKING:
    from fhircraft.fhir.mapper.engine.scope import MappingScope
    from fhircraft.fhir.resources.datatypes.R4.core.structure_map import (
        StructureMapGroupRuleTargetParameter as R4_StructureMapParameter,
    )
    from fhircraft.fhir.resources.datatypes.R4B.core.structure_map import (
        StructureMapGroupRuleTargetParameter as R4B_StructureMapParameter,
    )
    from fhircraft.fhir.resources.datatypes.R5.core.structure_map import (
        StructureMapGroupRuleTargetParameter as R5_StructureMapParameter,
    )


class MappingTransform(FHIRMappingEngineComponent, ABC):
    pass


class Copy(MappingTransform):
    """Implements the 'copy' transform, which copies the source value to the target."""

    source: str | None = None
    literal: Any | None = None

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) != 1:
            raise ValueError("Copy transform requires exactly one parameter")
        parameter = parameters[0]
        if parameter.valueId:
            self.source = str(parameter.valueId)
        else:
            self.literal = parameter.value

    def process(self, scope: "MappingScope") -> Any:
        """
        Copies a value from the source or uses a provided literal.

        This function attempts to copy a value from the specified `source` using FHIRPath resolution within the given `scope`.
        If `source` is not provided, it returns the given `literal` value instead.

        Args:
            scope (MappingScope): The mapping scope containing context and instances for FHIRPath resolution.

        Returns:
            Any: The copied value from the source or the provided literal.

        """
        # Just copy the source value or use the literal
        if self.source:
            source_fhirpath = scope.resolve_fhirpath(self.source)
            return source_fhirpath.single(scope.get_instances())
        elif self.literal:
            return self.literal

        def __repr__(self):
            if hasattr(self, "source"):
                return f"CopyTransform(source={self.source})"
            else:
                return f"CopyTransform(literal={self.literal})"


class Create(MappingTransform):
    """Implements the 'create' transform, which creates a new instance of the specified type."""

    type_specifier: str

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) != 1:
            raise ValueError("Create transform requires exactly one parameter")
        self.type_specifier = parameters[0].value

    def process(self, scope: "MappingScope") -> Any:
        """
        Creates and returns a new instance of a model of the specified type using the provided mapping scope.

        Args:
            scope (MappingScope): The mapping scope containing type definitions and model constructors.

        Returns:
            BaseModel: A newly constructed instance of the specified model type.
        """
        return scope.get_type(self.type_specifier).model_construct()


class Truncate(MappingTransform):
    """Implements the 'truncate' transform, which truncates a string to a specified length."""

    source: str
    length: int

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) != 2:
            raise ValueError("Truncate transform requires exactly two parameters")
        self.source = parameters[0].value
        self.length = int(str(parameters[1].value))

    def process(self, scope: "MappingScope") -> Any:
        """
        Truncates the value obtained from a FHIRPath expression to a specified length.

        Args:
            scope (MappingScope): The current mapping scope containing context and data.

        Returns:
            str: The truncated string result from the FHIRPath expression.
        """
        source_fhirpath = scope.resolve_fhirpath(self.source)
        return source_fhirpath._invoke(fp.Substring(0, int(self.length))).single(
            scope.get_instances()
        )


class Cast(MappingTransform):
    """Implements the 'cast' transform, which casts a value to a specified type."""

    source: str
    type_specifier: str | None
    type_conversion_function: Type[fp.FHIRPath] | None

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) not in [1, 2]:
            raise ValueError("Cast transform requires one or two parameters")
        self.source = parameters[0].value
        if len(parameters) == 2:
            self.type_specifier = (
                parameters[1].value[0].upper() + parameters[1].value[1:]
            )
            self.type_conversion_function = getattr(fp, f"To{self.type_specifier}", None)  # type: ignore
            if not self.type_conversion_function:
                raise ValueError(f"Unsupported type for cast: {self.type_specifier}")
        else:
            self.type_specifier = None
            self.type_conversion_function = None

    def process(self, scope: "MappingScope") -> Any:
        """
        Casts the value of a FHIRPath expression to a specified target type.

        Args:
            scope (MappingScope): The current mapping scope containing context and instance data.

        Returns:
            Any: The value of the source FHIRPath expression cast to the specified type.
        """
        source_fhirpath = scope.resolve_fhirpath(self.source)
        # Explicit casting
        if self.type_conversion_function:
            return source_fhirpath._invoke(self.type_conversion_function()).single(
                scope.get_instances()
            )
        else:
            is_decimal = source_fhirpath._invoke(
                fp.LegacyIs(fp.TypeSpecifier("Decimal"))
            ).single(scope.get_instances())
            is_date = source_fhirpath._invoke(
                fp.LegacyIs(fp.TypeSpecifier("Date"))
            ).single(scope.get_instances())
            if is_decimal:
                return source_fhirpath._invoke(fp.ToDecimal()).single(
                    scope.get_instances()
                )
            elif is_date:
                return source_fhirpath._invoke(fp.ToDate()).single(
                    scope.get_instances()
                )
            else:
                raise NotImplementedError(
                    "Implicit casting is only supported for Decimal and Date types, please specify a target type explicitly."
                )


class Append(MappingTransform):
    """Implements the 'append' transform, which appends string representations of parameters."""

    elements: Sequence[Tuple[bool, str]]

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        """
        Processes a list of `StructureMapParameter` objects, extracting their `valueId` or `valueString` attributes.
        For each parameter:
        - If `valueId` is present, it resolves the FHIRPath and appends its string value.
        - If `valueString` is present, it appends the string directly.
        - If neither is present, it raises a `RuleProcessingError`.

        Args:
            parameters: A sequence of StructureMapParameter objects to process.

        Raises:
            RuleProcessingError: If no parameters are provided, or if a parameter does not have a valid type (`valueId` or `valueString`).
        """
        if len(parameters) < 1:
            raise ValueError("Append transform requires at least one parameter")
        self.elements = []
        for parameter in parameters:
            if not (parameter.valueId or parameter.valueString):
                raise ValueError(
                    "Append transform parameters must be of type Id or String"
                )
            is_literal = parameter.valueId is None
            self.elements.append(
                (is_literal, str(parameter.valueId or parameter.valueString))
            )

    def process(self, scope: "MappingScope") -> Any:
        """
        Appends the string representations of the provided parameters.

        Args:
            scope: The current mapping scope used to resolve FHIRPath expressions.

        Returns:
            str: The concatenated string of all parameter values.

        Raises:
            RuleProcessingError: If no parameters are provided, or if a parameter does not have a valid type (`valueId` or `valueString`).
        """
        strings = []
        for is_literal, value in self.elements:
            if is_literal:
                strings.append(value)
            else:
                source_fhirpath = scope.resolve_fhirpath(value)
                strings.append(str(source_fhirpath.single(scope.get_instances())))
        return "".join(strings)


class Reference(MappingTransform):
    """Implements the 'reference' transform, which creates a FHIR reference from a given source."""

    source: str

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) != 1:
            raise ValueError("Reference transform requires exactly one parameter")
        if param := parameters[0].valueId:
            self.source = str(param)
        else:
            raise ValueError("Reference transform parameter must be of type Id")

    def process(self, scope: "MappingScope") -> str:
        """
        Transforms a FHIR resource reference by extracting its resource type and ID from the given source.

        Args:
            scope (MappingScope): The current mapping scope containing context and instances.

        Returns:
            str: A string in the format "ResourceType/ResourceId" representing the FHIR reference.
        """
        source_fhirpath = scope.resolve_fhirpath(self.source)
        resource_type = (
            source_fhirpath._invoke(fp.Element("resourceType")).single(
                scope.get_instances()
            )
            or source_fhirpath.single(scope.get_instances()).__class__.__name__
        )
        resource_id = source_fhirpath._invoke(fp.Element("id")).single(
            scope.get_instances()
        )
        return f"{resource_type}/{resource_id}"


class UUID(MappingTransform):
    """Implements the 'uuid' transform, which generates a UUID string."""

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) != 0:
            raise ValueError("UUID transform does not take any parameters")

    def process(self, scope: "MappingScope") -> Any:
        """
        Generates a new UUID string.

        Args:
            scope (MappingScope): The current mapping scope (unused in this function).

        Returns:
            str: A newly generated UUID as a string.
        """
        return str(uuid.uuid4())


class Translate(MappingTransform):
    """Implements the 'translate' transform, which translates a code using a concept map."""

    source: str
    concept_map_name: str
    output_type: str = "code"

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) not in [2, 3]:
            raise ValueError(
                "Translate transform requires exactly two or three parameters"
            )
        self.source = parameters[0].value
        self.concept_map_name = parameters[1].value
        if len(parameters) == 3:
            self.output_type = parameters[2].value
            if self.output_type != "code":
                raise NotImplementedError(
                    f"Output mode '{self.output_type}' for translate operation is not yet supported."
                )

    def process(self, scope: "MappingScope") -> Any:
        """
        Translates a source code using a specified FHIR ConceptMap.

        Args:
            scope (MappingScope): The current mapping scope, providing access to FHIRPath resolution and ConceptMaps.

        Returns:
            str: The translated target code from the ConceptMap.

        Raises:
            MappingError: If the ConceptMap has no groups, if a target code is not defined for the source code,
                          or if the source code cannot be mapped using the ConceptMap.
        """
        source_code = scope.resolve_fhirpath(self.source).single(scope.get_instances())
        concept_map = scope.get_concept_map(self.concept_map_name.lstrip("#"))
        if concept_map.group is None:
            raise MappingError(
                f"Concept map '{self.concept_map_name}' has no groups defined."
            )
        for group in concept_map.group:
            for element in group.element or []:
                if element.target is None:
                    continue
                for element_target in element.target:
                    if element.code == source_code:
                        if self.output_type == "code":
                            if element_target.code is None:
                                raise MappingError(
                                    f"Concept map '{self.concept_map_name}' does not define a target code for source code '{source_code}'."
                                )
                            return element_target.code
        else:
            raise MappingError(
                f"Could not map source code '{source_code}' using concept map '{self.concept_map_name}'."
            )


class Evaluate(MappingTransform):
    """Implements the 'evaluate' transform, which evaluates a FHIRPath expression."""

    source: str | None = None
    expression: str

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) not in [1, 2]:
            raise ValueError(
                "Evaluate transform requires exactly one or two parameters"
            )
        if len(parameters) == 2:
            self.source = str(parameters[0].value)
        self.expression = str(parameters[-1].value)

    def process(self, scope: "MappingScope") -> Any:
        """
        Evaluates a FHIRPath expression against a specified source within the given mapping scope.

        Args:
            scope: The current mapping scope containing context and instances.

        Returns:
            Any: The result of evaluating the FHIRPath expression against the source context.
        """
        if self.source:
            context = scope.resolve_fhirpath(self.source).single(scope.get_instances())
        else:
            context = scope.get_instances()
        expression = self.resolve_fhirpath_within_context(self.expression, scope)
        transformed_values = expression.values(context)
        if len(transformed_values) == 1:
            return transformed_values[0]
        elif len(transformed_values) > 1:
            return transformed_values
        else:
            return None


class CodeableConcept(MappingTransform):
    """Implements the 'cc' transform, which creates a CodeableConcept from parameters."""

    text: fp.FHIRPath | str | None = None
    code: fp.FHIRPath | str | None = None
    system: fp.FHIRPath | str | None = None
    display: fp.FHIRPath | str | None = None

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) not in [1, 2, 3]:
            raise ValueError(
                "CodeableConcept transform requires one, two, or three parameters"
            )
        if len(parameters) == 1:
            self.text = (
                fp.Literal(text.value)
                if not (text := parameters[0]).valueId
                else str(text.valueId)
            )
        else:
            self.code = (
                fp.Literal(code.value)
                if not (code := parameters[0]).valueId
                else str(code.valueId)
            )
            self.system = (
                fp.Literal(system.value)
                if not (system := parameters[1]).valueId
                else str(system.valueId)
            )
            if len(parameters) == 3:
                self.display = (
                    fp.Literal(display.value)
                    if not (display := parameters[2]).valueId
                    else str(display.valueId)
                )

    def process(self, scope: "MappingScope") -> Any:
        """
        Creates a CodeableConcept instance from the provided Coding parameters.

        Args:
            scope: The current mapping scope (unused in this function).

        Returns:
            CodeableConcept: A codeableConcept dictionary containing the specified Codings.
        """
        if self.text:
            text = (
                scope.resolve_fhirpath(self.text)
                if isinstance(self.text, str)
                else self.text
            ).single(scope.get_instances())
            return {"text": str(text)}
        elif self.code and self.system:
            code = (
                scope.resolve_fhirpath(self.code)
                if isinstance(self.code, str)
                else self.code
            ).single(scope.get_instances())
            system = (
                scope.resolve_fhirpath(self.system)
                if isinstance(self.system, str)
                else self.system
            ).single(scope.get_instances())
            display = None
            if self.display:
                display = (
                    scope.resolve_fhirpath(self.display)
                    if isinstance(self.display, str)
                    else self.display
                ).single(scope.get_instances())
            return {
                "coding": [
                    {
                        "code": str(code) if code else None,
                        "system": str(system) if system else None,
                        "display": str(display) if display else None,
                    }
                ]
            }
        else:
            raise ValueError(
                "CodeableConcept transform requires either a text parameter or code and system parameters"
            )


class Coding(MappingTransform):
    """Implements the 'c' transform, which creates a Coding from parameters."""

    code: fp.FHIRPath | str | None = None
    system: fp.FHIRPath | str | None = None
    display: fp.FHIRPath | str | None = None

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) not in [2, 3]:
            raise ValueError("Coding transform requires two or three parameters")
        self.code = (
            fp.Literal(code.value)
            if not (code := parameters[0]).valueId
            else str(code.valueId)
        )
        self.system = (
            fp.Literal(system.value)
            if not (system := parameters[1]).valueId
            else str(system.valueId)
        )
        if len(parameters) == 3:
            self.display = (
                fp.Literal(display.value)
                if not (display := parameters[2]).valueId
                else str(display.valueId)
            )

    def process(self, scope: "MappingScope") -> Any:
        """
        Creates a CodeableConcept instance from the provided Coding parameters.

        Args:
            scope: The current mapping scope (unused in this function).

        Returns:
            Coding: A coding dictionary containing the specified Codings.
        """
        if self.code and self.system:
            code = (
                scope.resolve_fhirpath(self.code)
                if isinstance(self.code, str)
                else self.code
            ).single(scope.get_instances())
            system = (
                scope.resolve_fhirpath(self.system)
                if isinstance(self.system, str)
                else self.system
            ).single(scope.get_instances())
            display = None
            if self.display:
                display = (
                    scope.resolve_fhirpath(self.display)
                    if isinstance(self.display, str)
                    else self.display
                ).single(scope.get_instances())
            return {
                "code": str(code) if code else None,
                "system": str(system) if system else None,
                "display": str(display) if display else None,
            }
        else:
            raise ValueError(
                "CodeableConcept transform requires either a text parameter or code and system parameters"
            )


class Quantity(MappingTransform):
    """Implements the 'qty' transform, which creates a Quantity"""

    text: fp.FHIRPath | str | None = None
    value: fp.FHIRPath | str | None = None
    unit: fp.FHIRPath | str | None = None
    system: fp.FHIRPath | str | None = None
    code: fp.FHIRPath | str | None = None

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) not in [1, 2, 4]:
            raise ValueError("Quantity transform requires one, two, or four parameters")
        if len(parameters) == 1:
            self.text = (
                fp.Literal(text.value)
                if not (text := parameters[0]).valueId
                else str(text.valueId)
            )
        else:
            self.value = (
                fp.Literal(value.value)
                if not (value := parameters[0]).valueId
                else str(value.valueId)
            )
            self.unit = (
                fp.Literal(unit.value)
                if not (unit := parameters[1]).valueId
                else str(unit.valueId)
            )
            if len(parameters) == 4:
                self.system = (
                    fp.Literal(system.value)
                    if not (system := parameters[2]).valueId
                    else str(system.valueId)
                )
                self.code = (
                    fp.Literal(code.value)
                    if not (code := parameters[3]).valueId
                    else str(code.valueId)
                )

    def process(self, scope: "MappingScope") -> Any:
        """
        Transforms quantity-related input parameters into a FHIR Quantity object.

        This function supports two modes of operation:
        1. Parsing a single `text` parameter of the form '[<|<=|>=|>|ad]<number> <unit>', extracting the comparator, value, and unit.
        2. Using explicit `value` and `unit` parameters (with optional `system` and `code`).

        Args:
            scope (MappingScope): The mapping scope context (not used in this function).

        Returns:
            Quantity: A FHIR Quantity object constructed from the provided parameters.

        Raises:
            RuleProcessingError: If the `text` parameter does not match the expected format.
            AssertionError: If neither `text` nor both `value` and `unit` are provided.
        """
        if self.text:
            text = (
                scope.resolve_fhirpath(self.text)
                if isinstance(self.text, str)
                else self.text
            ).single(scope.get_instances())
            matches = re.search(r"(<|<=|>=|>|ad)?(\d+((\.|\,)\d+)?) (.*)", str(text))
            if not matches:
                raise MappingError(
                    "The 'qty' transform single parameter must be of the form '[<|<=|>=|>|ad]<number> <unit>'"
                )

            return dict(
                comparator=matches.group(1) if matches.group(1) else None,
                value=float(matches.group(2).replace(",", ".")),
                unit=str(matches.group(5)) if matches.group(5) else None,
                system=None,
                code=None,
            )
        else:
            assert self.value and self.unit
            value = (
                scope.resolve_fhirpath(self.value)
                if isinstance(self.value, str)
                else self.value
            ).single(scope.get_instances())
            unit = (
                scope.resolve_fhirpath(self.unit)
                if isinstance(self.unit, str)
                else self.unit
            ).single(scope.get_instances())
            system = (
                (
                    scope.resolve_fhirpath(self.system)
                    if isinstance(self.system, str)
                    else self.system
                ).single(scope.get_instances())
                if self.system
                else None
            )
            code = (
                (
                    scope.resolve_fhirpath(self.code)
                    if isinstance(self.code, str)
                    else self.code
                ).single(scope.get_instances())
                if self.code
                else None
            )
            return dict(
                value=float(str(value)) if value is not None else None,
                unit=str(unit) if unit else None,
                system=str(system) if system else None,
                code=str(code) if code else None,
            )


class Identifier(MappingTransform):
    """Implements the 'id' transform, which creates an Identifier"""

    system: fp.FHIRPath | str
    value: fp.FHIRPath | str
    type: fp.FHIRPath | str

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) != 3:
            raise ValueError("Identifier transform requires three parameters")
        self.system = (
            fp.Literal(system.value)
            if not (system := parameters[0]).valueId
            else str(system.valueId)
        )
        self.value = (
            fp.Literal(value.value)
            if not (value := parameters[1]).valueId
            else str(value.valueId)
        )
        self.type = (
            fp.Literal(type_.value)
            if not (type_ := parameters[2]).valueId
            else str(type_.valueId)
        )

    def process(self, scope: "MappingScope") -> Any:
        """
        Creates an Identifier instance from the provided parameters.

        Args:
            scope: The current mapping scope (unused in this function).

        Returns:
            Identifier: An identifier dictionary containing the specified system, value, and code.
        """
        system = (
            scope.resolve_fhirpath(self.system)
            if isinstance(self.system, str)
            else self.system
        ).single(scope.get_instances())
        value = (
            scope.resolve_fhirpath(self.value)
            if isinstance(self.value, str)
            else self.value
        ).single(scope.get_instances())
        type_ = (
            scope.resolve_fhirpath(self.type)
            if isinstance(self.type, str)
            else self.type
        ).single(scope.get_instances())
        return {
            "system": str(system) if system else None,
            "value": str(value) if value else None,
            "type": {
                "coding": [
                    {
                        "code": str(type_) if type_ else None,
                        "system": "http://hl7.org/fhir/ValueSet/identifier-type",
                    }
                ]
            },
        }


class ContactPoint(MappingTransform):
    """Implements the 'cp' transform, which creates a ContactPoint"""

    system: fp.FHIRPath | str | None = None
    value: fp.FHIRPath | str

    def __init__(
        self,
        parameters: Sequence[
            "R4_StructureMapParameter | R4B_StructureMapParameter | R5_StructureMapParameter"
        ],
    ):
        if len(parameters) not in [1, 2]:
            raise ValueError("Identifier transform requires one or two parameters")
        if len(parameters) == 2:
            self.system = (
                fp.Literal(system.value)
                if not (system := parameters[0]).valueId
                else str(system.valueId)
            )
        self.value = (
            fp.Literal(value.value)
            if not (value := parameters[-1]).valueId
            else str(value.valueId)
        )

    def process(self, scope: "MappingScope") -> Any:
        """
        Creates an Identifier instance from the provided parameters.

        Args:
            scope: The current mapping scope (unused in this function).

        Returns:
            Identifier: An identifier dictionary containing the specified system, value, and code.
        """
        value = (
            scope.resolve_fhirpath(self.value)
            if isinstance(self.value, str)
            else self.value
        ).single(scope.get_instances())
        if self.system:
            system = (
                scope.resolve_fhirpath(self.system)
                if isinstance(self.system, str)
                else self.system
            ).single(scope.get_instances())
        else:
            # Determine through regex which system type to use
            if re.match(r"^[+]{1}(?:[0-9\-\$$\$$\/\.]\s?){6,15}[0-9]{1}$", str(value)):
                system = "phone"
            elif re.match(r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$", str(value)):
                system = "email"
            elif re.match(r"^\+1[2-9][0-9]{9}$", str(value)):
                system = "fax"
            elif re.match(
                r"^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$",
                str(value),
            ):
                system = "url"
            else:
                system = "other"
        return {
            "system": str(system),
            "value": str(value),
        }
