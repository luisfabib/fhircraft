from __future__ import annotations

from typing import Any, Sequence

from pydantic import create_model
from fhircraft.fhir.resources.base import FHIRBaseModel

from fhircraft.fhir.resources.factory.builders.base import Builder
from fhircraft.fhir.resources.factory.context import BuildContext
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.factory.exceptions import AssemblerError
from fhircraft.fhir.resources.factory.builders import (
    TypeChoiceFieldBuilder,
    SlicedFieldBuilder,
    BackboneFieldBuilder,
    SimpleFieldBuilder,
)

BUILDER_CHAIN: list[type[Builder]] = [
    TypeChoiceFieldBuilder,
    SlicedFieldBuilder,
    BackboneFieldBuilder,
    SimpleFieldBuilder,
]


class ModelAssembler:

    index: DefinitionIndex
    """   The definition index to assemble from. """

    ctx: BuildContext
    """   The build context. """

    resource_name: str
    """   The name of the resource being assembled (for error messages). """

    builder_chain: Sequence[Builder]
    """   The chain of builders to use for assembling fields.  Initialized from :attr:`BUILDER_CHAIN`. """

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
        Construct and return a Pydantic model class for this scope.

        Args:
            name: The Python class name for the resulting model.
            base: The base class(es) to inherit from.  If ``None``,
                :attr:`base_model` is used.  May be a single type or a tuple of
                types (for multiple inheritance, e.g. ``(Observation, FHIRSliceModel)``).

        Returns:
            The constructed Pydantic model class.
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

        has_inherited_fields = any(
            len(getattr(base, "model_fields", [])) for base in base_classes
        )
        if not fields and not has_inherited_fields:
            raise AssemblerError(
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
