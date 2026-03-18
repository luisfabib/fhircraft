"""
Module responsible for assembling Pydantic models from the internal definition index using a chain of builders.
"""

import warnings

from functools import partial
from typing import Any, Sequence

from pydantic import BaseModel, create_model
from fhircraft.fhir.resources.base import FHIRBaseModel

from fhircraft.fhir.resources.factory.builders.base import Builder, ValidatorInformation
from fhircraft.fhir.resources.factory.context import BuildContext
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.factory.exceptions import AssemblerError
from fhircraft.fhir.resources.factory.builders import (
    TypeChoiceFieldBuilder,
    SlicedFieldBuilder,
    BackboneFieldBuilder,
    SimpleFieldBuilder,
)
from fhircraft.fhir.resources.validators import (
    validate_FHIR_model_fixed_value,
    validate_FHIR_model_pattern,
)

BUILDER_CHAIN: list[type[Builder]] = [
    TypeChoiceFieldBuilder,
    SlicedFieldBuilder,
    BackboneFieldBuilder,
    SimpleFieldBuilder,
]


class ModelAssembler:

    index: DefinitionIndex
    """ The definition index to assemble from. """

    ctx: BuildContext
    """ The build context. """

    resource_name: str
    """ The name of the resource being assembled (for error messages). """

    builder_chain: Sequence[Builder]
    """ The chain of builders to use for assembling fields.  Initialized from :attr:`BUILDER_CHAIN`. """

    def __init__(
        self,
        index: DefinitionIndex,
        ctx: BuildContext,
        resource_name: str = "Unknown",
    ) -> None:
        self.index = index
        self.ctx = ctx
        self.resource_name = resource_name
        self.builder_chain = [builder(ctx) for builder in BUILDER_CHAIN]

    def assemble(
        self,
        name: str,
        base: type | tuple[type, ...] | None = None,
    ) -> type:
        """
        Dynamically assembles and returns a Pydantic model class based on the provided name, base classes,
        and the structure defined in the internal index.
        Args:
            name (str): The name of the model to be created.
            base (type or tuple[type, ...], optional): The base class(es) for the model. If None, uses the default base from context or FHIRBaseModel.
        Returns:
            type: The dynamically created Pydantic model class.
        Raises:
            ValueError: If a child element in the index lacks a definition.
            AssemblerError: If a builder fails to construct a field or validator.
        Notes:
            - Resolves base classes and iterates over child elements to build fields, validators, and properties.
            - Handles model-level constraints, including fixed values and patterns.
            - Attaches properties and sets constraint defaults as needed.
            - Issues a warning if no fields are built and no fields are inherited from base classes.
        """

        # Resolve base classes
        if base is None:
            base_classes: tuple[type, ...] = (self.ctx.base or FHIRBaseModel,)
        elif isinstance(base, tuple):
            base_classes = base
        else:
            base_classes = (base,)

        # ------------------------------------------------------------------
        # Iterate children (direct non-slice elements of the root)
        # ------------------------------------------------------------------
        root = self.index.root()
        fields = {}
        field_validators = {}
        properties = {}

        for child_node in self.index.get_children(root.id):
            if not child_node.definition:
                raise ValueError(
                    f"Element '{child_node.id}' has no definition in the index."
                )

            # ----------------------------------------------------------
            # Dispatch through builder chain
            # ----------------------------------------------------------
            builder = self._find_builder(child_node)

            try:
                build = builder.build(
                    child_node,
                    self.index,
                )
            except Exception as exc:
                raise AssemblerError(
                    f"Builder failed for element '{child_node.id}': {exc}"
                ) from exc

            # ----------------------------------------------------------
            # Accumulate results
            # ----------------------------------------------------------
            fields.update(
                {info.name: info.as_pydantic_definition() for info in build.fields}
            )
            field_validators.update(
                {info.name: info.as_pydantic_definition() for info in build.validators}
            )
            properties.update(build.properties)

        model_validators = {
            info.name: info.as_pydantic_definition()
            for constraint in (root.definition.constraint or [])
            if (
                info := Builder.build_invariant_constraint(
                    root.path, constraint, kind="model"
                )
            )
        }
        # Handle fixed value and pattern constraints on the model itself (e.g. for slices)
        if root.fixed is not None:
            fixed_validator = self.build_model_fixed_value_constraint(root)
            model_validators[fixed_validator.name] = (
                fixed_validator.as_pydantic_definition()
            )

        if root.pattern is not None:
            pattern_validator = self.build_model_pattern_constraint(root)
            model_validators[pattern_validator.name] = (
                pattern_validator.as_pydantic_definition()
            )

        has_inherited_fields = any(
            len(getattr(base, "model_fields", [])) for base in base_classes
        )
        if not fields and not has_inherited_fields:
            warnings.warn(
                f"No fields built for model '{name}' and no fields defined on base class(es) {base_classes}."
            )

        # ------------------------------------------------------------------
        # Build the Pydantic model
        # ------------------------------------------------------------------

        model = create_model(
            name,
            **fields,  # type: ignore[arg-type]
            __base__=base_classes,
            __validators__={**field_validators, **model_validators},  # type: ignore[arg-type]
            __doc__=root.documentation,
            __module__=self.ctx.factory.__module__,
        )

        if root.fixed or root.pattern:
            # If the slice entry has a fixed value or pattern, set it as default on the field and register a validator
            self._set_constraint_default_values(model, root)

        # Attach properties
        for attr_name, property_getter in properties.items():
            setattr(model, attr_name, property(property_getter))

        return model

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_builder(self, node: Any) -> Builder:
        for builder in self.builder_chain:
            if builder.can_handle(node, self.index):
                return builder
        raise AssemblerError(f"No suitable builder found for node '{node.id}'.")

    @staticmethod
    def _set_constraint_default_values(
        model: type,
        node: Any,
    ) -> None:
        """Override slice model field defaults with pattern values and register validator."""
        constrain_value = node.fixed or node.pattern

        if not isinstance(constrain_value, BaseModel):
            raise TypeError(
                f"Expected fixed or pattern value for a slice to be a Pydantic model instance, got {type(constrain_value)}"
            )

        for constraint_field in constrain_value.__class__.model_fields:
            if constraint_field not in model.model_fields:
                raise ValueError(
                    f"Constraint field '{constraint_field}' not found in slice model fields: {list(model.model_fields.keys())}"
                )
            val = getattr(constrain_value, constraint_field, None)
            if val is not None:
                # Update default on the field
                model.model_fields[constraint_field].default = val

    @staticmethod
    def build_model_fixed_value_constraint(node: ElementNode) -> ValidatorInformation:
        """
        Constructs a ValidatorInformation object for enforcing a fixed value constraint on a FHIR model element.
        Args:
            node (ElementNode): The element node containing the fixed value to be validated.
        Returns:
            ValidatorInformation: An object encapsulating the validator's name, kind, function, and arguments for the fixed value constraint.
        """

        return ValidatorInformation(
            name=f"FHIR_{node.name}_fixed_value_constraint",
            kind="model",
            function=partial(validate_FHIR_model_fixed_value, constant=node.fixed),
            arguments={"constant": node.fixed},
        )

    @staticmethod
    def build_model_pattern_constraint(node: ElementNode) -> ValidatorInformation:
        """
        Constructs a ValidatorInformation object for enforcing a pattern constraint on a FHIR model element.
        Args:
            node (ElementNode): The element node containing the pattern to be validated.
        Returns:
            ValidatorInformation: An object containing the validator's name, kind, and a partial function
            for pattern validation specific to the provided node.
        """

        return ValidatorInformation(
            name=f"FHIR_{node.name}_pattern_constraint",
            kind="model",
            function=partial(validate_FHIR_model_pattern, pattern=node.pattern),
        )
