import inspect
from typing import TYPE_CHECKING, Any, Callable, List, Literal, Optional

from abc import ABC, abstractmethod
from functools import partial
import keyword

from dataclasses import dataclass, field as dc_field
from typing_extensions import Annotated

from pydantic import Field, field_validator, model_validator
from pydantic.aliases import AliasChoices
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from fhircraft.fhir.resources.datatypes.utils import (
    get_fhir_type,
    get_complex_FHIR_type,
)
from fhircraft.fhir.resources.base import FHIRBaseModel

from fhircraft.fhir.resources.factory.context import BuildContext
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.factory.exceptions import (
    BuilderError,
    TypeResolutionError,
)
from fhircraft.fhir.resources.validators import (
    validate_FHIR_element_fixed_value,
    validate_FHIR_element_pattern,
    validate_element_constraint,
    validate_model_constraint,
)
from fhircraft.utils import capitalize, ensure_list

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4.complex.element_definition import (
        ElementDefinitionType as R4_ElementDefinitionType,
        ElementDefinitionConstraint as R4_ElementDefinitionConstraint,
    )
    from fhircraft.fhir.resources.datatypes.R4B.complex.element_definition import (
        ElementDefinitionType as R4B_ElementDefinitionType,
        ElementDefinitionConstraint as R4B_ElementDefinitionConstraint,
    )
    from fhircraft.fhir.resources.datatypes.R5.complex.element_definition import (
        ElementDefinitionType as R5_ElementDefinitionType,
        ElementDefinitionConstraint as R5_ElementDefinitionConstraint,
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
    """

    type: type
    """The resolved Python type. """

    kind: str
    """The kind of FHIR type (e.g., "primitive", "complex", "resource"). """

    requires_primitive_extension: bool = False
    """Whether this type requires a corresponding primitive extension field. """


@dataclass
class ValidatorInformation:
    """
    Resolved validator information for a Pydantic validator.
    """

    name: str
    """The name of the validator. """

    kind: Literal["field", "model"]
    """The kind of validator (field-level or model-level). """

    function: Callable
    """The actual validator function. """

    arguments: dict[str, Any] = dc_field(default_factory=dict)
    """The arguments for the validator function."""

    field: str | None = None
    """The fields this validator applies to (for field validators). """

    def as_pydantic_definition(self):

        if self.kind == "field":
            if not self.field:
                raise ValueError(
                    "Field validators must specify the field they apply to."
                )
            validator_decorator = field_validator(self.field, mode="after")
        elif self.kind == "model":
            validator_decorator = model_validator(mode="after")
        else:
            raise ValueError(f"Invalid validator kind: {self.kind}")
        return validator_decorator(partial(self.function, **self.arguments))


@dataclass
class FieldInformation:

    name: str
    """ The name of the field. """

    annotation: Any
    """ The type annotation for the field. """

    default: Any = _Unset
    """ The default value for the field. """

    alias: str | None = None
    """ The alias for the field. """

    validation_alias: AliasChoices | None = None
    """ The validation alias for the field. """

    description: str | None = None
    """ The description of the field. """

    min_length: int | None = None
    """ The minimum length of the field. """

    max_length: int | None = None
    """ The maximum length of the field. """
    min_value: int | None = None
    """ The minimum value of the field. """

    max_value: int | None = None
    """ The maximum value of the field. """

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
                ge=self.min_value,
                le=self.max_value,
            ),
        )


@dataclass
class Build:
    """The result of a Builder's build() method, containing the field and validator information needed to construct a Pydantic model."""

    fields: List[FieldInformation] = dc_field(default_factory=list)
    """ The list of fields to include in the model. """

    validators: List[ValidatorInformation] = dc_field(default_factory=list)
    """ The list of validators to include in the model. """

    properties: dict[str, Callable] = dc_field(default_factory=dict)
    """ The dictionary of properties to include in the model. """


class Builder(ABC):

    def __init__(self, context: BuildContext):
        self.context = context

    @abstractmethod
    def can_handle(self, node: ElementNode, index: DefinitionIndex) -> bool:
        raise NotImplementedError(
            "Builder subclasses must implement the can_handle() method."
        )

    @abstractmethod
    def build(self, node: ElementNode, index: DefinitionIndex) -> Build:
        raise NotImplementedError(
            "Builder subclasses must implement the build() method."
        )

    @staticmethod
    def handle_python_keyword(field_name: str) -> tuple[str, AliasChoices | None]:
        """
        Handle Python keywords and reserved class keywords by creating safe aliases.

        This function checks if a field name is a Python keyword or a reserved class keyword.
        If it is, the function creates a safe alternative by appending an underscore and returns
        both the safe name and an AliasChoices object mapping the original name to the safe name.

        Args:
            field_name (str): The name of the field to check.

        Returns:
            tuple[str, AliasChoices | None]: A tuple containing:
                - str: The safe field name (with underscore appended if it's a keyword, otherwise unchanged)
                - AliasChoices | None: An AliasChoices object mapping original to safe name if a conflict exists,
                                        None otherwise.

        Example:
            >>> handle_python_keyword("class")
            ("class_", AliasChoices("class", "class_"))
            >>> handle_python_keyword("my_field")
            ("my_field", None)
        """
        if keyword.iskeyword(field_name) or field_name in CLASS_RESERVED_KEYWORDS:
            safe = f"{field_name}_"
            alias = AliasChoices(field_name, safe)
            return safe, alias
        return field_name, None

    @staticmethod
    def build_field_information(
        name: str,
        node: ElementNode,
        type: type | Annotated,
        alias: str | None = None,
        validation_alias: AliasChoices | None = None,
        description: str | None = None,
    ) -> FieldInformation:
        """
        Build field information for a FHIR resource field.

        Args:
            name: The name of the field.
            node: The ElementNode containing field metadata and constraints.
            type: The base type annotation for the field (type or Annotated).
            alias: Optional alias for the field during serialization.
            validation_alias: Optional validation alias choices for the field.
            description: Optional description of the field. If not provided, uses node.documentation.

        Returns:
            FieldInformation: A FieldInformation object containing the field's name, annotation,
                default value, alias, validation alias, description, and constraints (min/max
                length and min/max value).

        Notes:
            - Default value priority: node.default_value > node.fixed > node.pattern > None
            - If the field is an array and a default is set, it is converted to a list.
            - Arrays are annotated as List[type].
            - All fields are made Optional to enforce optionality.
            - Min/max cardinality constraints only apply to array fields.
        """

        if node.default_value is not None:
            default = node.default_value
        elif node.fixed is not None:
            default = node.fixed
        elif node.pattern is not None:
            default = node.pattern
        else:
            default = None

        if node.is_array and default is not None:
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
            description=description or node.documentation,
            min_length=node.min_cardinality if node.is_array else None,
            max_length=node.max_length
            or (node.max_cardinality if node.is_array else None),
            min_value=node.min_value,
            max_value=node.max_value,
        )

    @staticmethod
    def build_invariant_constraint(
        field_name: str,
        constraint: "R4_ElementDefinitionConstraint | R4B_ElementDefinitionConstraint | R5_ElementDefinitionConstraint",
        kind: Literal["field", "model"] = "field",
    ) -> ValidatorInformation:
        """
        Build validator information for a FHIR invariant constraint.
        This function creates a ValidatorInformation object that encapsulates the details
        of a FHIR invariant constraint, which can be used to validate elements against
        user-defined constraints expressed in FHIRPath expressions.

        Args:
            field_name: The name of the field/element to apply the constraint to.
            constraint: An ElementDefinitionConstraint object (from FHIR R4, R4B, or R5)
                       containing the constraint definition with required attributes:
                       key, expression, human, and severity.
            kind: The kind of validator to create, either "field" for field-level validation or "model" for model-level validation. Defaults to "field".

        Returns:
            ValidatorInformation: An object containing the name, kind, function, and arguments for the constraint validator.

        Raises:
            BuilderError: If the constraint is missing any required attributes
        """

        if not (
            constraint.key
            and constraint.expression
            and constraint.human
            and constraint.severity
        ):
            raise BuilderError(
                "Invalid constraint definition: missing required attributes."
            )

        constraint_name = constraint.key.replace("-", "_")
        validator_name = f"FHIR_{constraint_name}_constraint_validator"

        if kind == "field":
            return ValidatorInformation(
                name=validator_name,
                kind="field",
                function=validate_element_constraint,
                arguments={
                    "elements": field_name,
                    "expression": constraint.expression,
                    "human": constraint.human,
                    "key": constraint.key,
                    "severity": constraint.severity,
                },
            )
        elif kind == "model":
            return ValidatorInformation(
                name=validator_name,
                kind="model",
                function=validate_model_constraint,
                arguments={
                    "expression": constraint.expression,
                    "human": constraint.human,
                    "key": constraint.key,
                    "severity": constraint.severity,
                },
            )

    def resolve_type(
        self,
        type: "R4_ElementDefinitionType | R4B_ElementDefinitionType | R5_ElementDefinitionType",
    ) -> TypeInformation:
        """
        Resolve a FHIR type definition to its corresponding type information.
        This method processes FHIR ElementDefinitionType objects and returns TypeInformation
        containing the resolved type, its kind, and whether it requires primitive extensions.

        Args:
            type: An ElementDefinitionType from FHIR R4, R4B, or R5 release that specifies
                a type code, optional profile URL, and other type metadata.

        Returns:
            TypeInformation: An object containing the resolved Python type, its kind (primitive, complex, resource), and whether it requires a primitive extension field.

        Raises:
            TypeResolutionError: If the type definition has no code attribute, making it
                impossible to resolve the type for the given FHIR release.
        """

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

    def build_primitive_extension_placeholder(
        self,
        node: ElementNode,
    ) -> FieldInformation:
        """
        Build a placeholder field information for primitive type extensions.
        Creates a FieldInformation object representing an extension placeholder for a primitive FHIR element.
        The placeholder field allows storing extension data associated with primitive values.

        Args:
            node: ElementNode representing the primitive FHIR element for which to create an extension placeholder.

        Returns:
            FieldInformation: Field information for the extension placeholder
        """

        # Process the name for the placeholder field
        original_name = f"_{node.name}"
        placeholder_name = f"{node.name}_ext"
        safe_placeholder_name, ext_alias = self.handle_python_keyword(placeholder_name)

        # Get the appropriate Element type for the placeholder field
        placeholder_type = get_complex_FHIR_type("Element", self.context.fhir_release)

        info = self.build_field_information(
            safe_placeholder_name,
            node,
            placeholder_type,
            alias=original_name,
            validation_alias=ext_alias,
            description=f"Placeholder element for {node.name} extensions",
        )
        return info

    def build_field_validators(
        self, node: ElementNode, safe_name: str
    ) -> List[ValidatorInformation]:
        validators = []
        # Build the field validators for this element
        if node.fixed is not None:
            validators.append(
                ValidatorInformation(
                    name=f"FHIR_{safe_name}_fixed_value_constraint",
                    kind="field",
                    field=safe_name,
                    function=partial(
                        validate_FHIR_element_fixed_value,
                    ),
                    arguments={"constant": node.fixed},
                )
            )

        # Build the field validators for this element
        if node.pattern is not None:
            validators.append(
                ValidatorInformation(
                    name=f"FHIR_{safe_name}_pattern_constraint",
                    kind="field",
                    field=safe_name,
                    function=partial(
                        validate_FHIR_element_pattern, pattern=node.pattern
                    ),
                )
            )

        for constraint in node.definition.constraint or []:
            validators.append(
                self.build_invariant_constraint(safe_name, constraint, kind="field")
            )

        return validators
