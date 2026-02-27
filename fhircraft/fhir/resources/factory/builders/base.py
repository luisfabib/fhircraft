import inspect
from typing import TYPE_CHECKING, Any, Callable, List, Optional

from abc import ABC, abstractmethod
import keyword

from dataclasses import dataclass, field as dc_field

from pydantic import Field
from pydantic.aliases import AliasChoices
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from fhircraft.fhir.resources.factory.context import BuildContext
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.index import DefinitionIndex


from fhircraft.fhir.resources.datatypes.utils import get_fhir_type
from fhircraft.fhir.resources.base import FHIRBaseModel
from fhircraft.fhir.resources.factory.exceptions import TypeResolutionError
from fhircraft.utils import capitalize

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4.complex.element_definition import (
        ElementDefinitionType as R4_ElementDefinitionType,
    )
    from fhircraft.fhir.resources.datatypes.R4B.complex.element_definition import (
        ElementDefinitionType as R4B_ElementDefinitionType,
    )
    from fhircraft.fhir.resources.datatypes.R5.complex.element_definition import (
        ElementDefinitionType as R5_ElementDefinitionType,
    )

# Class-level attribute names that collide with Pydantic's metaclass machinery
CLASS_RESERVED_KEYWORDS: frozenset[str] = frozenset(
    {"property", "classmethod", "field_validator", "model_validator"}
)
FHIR_SD_PREFIX = "http://hl7.org/fhir/StructureDefinition/"
FHIRPATH_TYPE_PREFIX = "http://hl7.org/fhirpath/System."

_Unset: Any = PydanticUndefined


@dataclass
class TypeInformation:
    """
    Resolved type information for an ElementDefinitionType.

    Attributes:
        type: The resolved Python type.
        kind: The kind of FHIR type (e.g., "primitive", "complex", "resource").
        requires_primitive_extension: Whether this type requires a corresponding primitive extension field.
    """

    type: type
    kind: str
    requires_primitive_extension: bool = False


@dataclass
class FieldInformation:

    name: str
    annotation: Any
    default: Any = _Unset
    alias: str | None = None
    validation_alias: AliasChoices | None = None
    description: str | None = None
    min_length: int | None = None
    max_length: int | None = None

    def as_pydantic_definition(self) -> tuple[Any, FieldInfo]:
        return (
            self.annotation,
            Field(
                self.default,
                alias=self.alias,
                validation_alias=self.validation_alias,
                description=self.description,
                min_length=self.min_length,
                max_length=self.max_length,
            ),
        )


@dataclass
class Build:

    fields: dict[str, Any] = dc_field(default_factory=dict)
    validators: dict[str, Any] = dc_field(default_factory=dict)
    properties: dict[str, Callable] = dc_field(default_factory=dict)


class Builder(ABC):

    def __init__(self, context: BuildContext):
        self.context = context

    @abstractmethod
    def can_handle(self, node: ElementNode, index: DefinitionIndex) -> bool:
        raise NotImplementedError(
            "Builder subclasses must implement the can_handle() method."
        )

    @abstractmethod
    def build(
        self,
        name: str,
        node: ElementNode,
        index: DefinitionIndex,
        base_model: type | None = None,
        resource_name: str = "Unknown",
        visited_paths: set[str] | None = None,
    ) -> list[Build]:
        raise NotImplementedError(
            "Builder subclasses must implement the build() method."
        )

    @staticmethod
    def handle_python_keyword(field_name: str) -> tuple[str, AliasChoices | None]:
        if keyword.iskeyword(field_name) or field_name in CLASS_RESERVED_KEYWORDS:
            safe = f"{field_name}_"
            alias = AliasChoices(field_name, safe)
            return safe, alias
        return field_name, None

    @staticmethod
    def build_field_information(
        name: str,
        node: ElementNode,
        type: type,
        default: Any = _Unset,
        alias: str | None = None,
        validation_alias: AliasChoices | None = None,
    ) -> FieldInformation:
        from fhircraft.utils import ensure_list

        if default is _Unset:
            default = None
        elif node.is_array and default is not None:
            default = ensure_list(default)

        annotation = type
        if node.is_array:
            annotation = List[annotation]

        # Enforce optionality for all fields
        annotation = Optional[annotation]

        return FieldInformation(
            name=name,
            annotation=annotation,
            default=default,
            alias=alias,
            validation_alias=validation_alias,
            description=node.documentation,
            min_length=node.min_cardinality if node.is_array else None,
            max_length=node.max_cardinality if node.is_array else None,
        )

    def resolve_type(
        self,
        type: "R4_ElementDefinitionType | R4B_ElementDefinitionType | R5_ElementDefinitionType",
    ) -> TypeInformation:
        fhir_release = type._fhir_release
        # Normalise the identifier: strip well-known URL prefixes
        if not type.code:
            raise TypeResolutionError(
                f"Cannot resolve FHIR type with no code for release '{fhir_release}'."
            )

        type_code = str(type.code)
        is_fhirpath_system_type = type_code.startswith(FHIRPATH_TYPE_PREFIX)

        # Handle the special case of FHIRPath system types, which are identified by a URL but do not have a profile and are not valid FHIR type names
        if is_fhirpath_system_type:
            if not type.profile:
                # Fallback to the raw code if no profile is provided
                type_code = type_code.removeprefix(FHIRPATH_TYPE_PREFIX)
            else:
                # For FHIRPath system types, the profile URL contains the actual FHIR type name
                type_code = type.profile[0]

        # This is a rare case, only logical models and FHIRPath system types should use this
        if type_code.startswith(FHIR_SD_PREFIX):
            type_code = type_code.removeprefix(FHIR_SD_PREFIX)

        type_code = capitalize(type_code)
        # Get the Fhircraft type
        fhir_type = get_fhir_type(type_code, fhir_release)

        # If a profile is specified and it's not a FHIRPath system type, resolve and build the profile to get the actual type to use
        if type.profile and not is_fhirpath_system_type:
            fhir_type = self.context.factory.build(canonical_url=type.profile[0])

        kind = (
            fhir_type._kind
            if inspect.isclass(fhir_type) and issubclass(fhir_type, FHIRBaseModel)
            else "primitive"
        )
        return TypeInformation(
            type=fhir_type,
            kind=kind,
            requires_primitive_extension=(
                not is_fhirpath_system_type and kind == "primitive"
            ),
        )
