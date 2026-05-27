"""
Builders for handling sliced elements and their associated slice models.
"""

from fhircraft.fhir.resources.factory.builders.base import (
    Build,
    Builder,
    ValidatorInformation,
)
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.base import FHIRSliceModel
from pydantic import Field
import warnings
from typing import Annotated, Union
from fhircraft.fhir.resources.validators import (
    validate_slicing_cardinalities,
)
from fhircraft.utils import _get_deepest_args, capitalize


class SlicedFieldBuilder(Builder):

    def can_handle(self, node: ElementNode, index: DefinitionIndex) -> bool:
        return node.is_slice_entry

    def build(self, node: ElementNode, index: DefinitionIndex) -> Build:
        from fhircraft.fhir.resources.factory.assembler import ModelAssembler

        build = Build()
        safe_name, val_alias = self.handle_python_keyword(node.name)

        # Determine the base class for the slice models
        slice_entry_base: type | None = None
        inherited_slices: list[type] = []
        if self.context.base is not None:
            if base_field := self.context.base.model_fields.get(safe_name):
                # First try to resolve the slice base type from the base model's field annotation
                slice_entry_base = next(
                    (
                        model
                        for model in _get_deepest_args(base_field.annotation)
                        if isinstance(model, type)
                        and not issubclass(model, FHIRSliceModel)
                        and not model is type(None)
                    ),
                    None,
                )
                inherited_slices = [
                    slice
                    for slice in _get_deepest_args(base_field.annotation)
                    if isinstance(slice, type) and issubclass(slice, FHIRSliceModel)
                ]
        if not slice_entry_base and len(node.types) == 1:
            # If that fails, fall back to the FHIR type resolved from the element definition
            slice_entry_base = self.resolve_type(node.types[0]).type

        # Build a slice model for each named slice
        slice_models: list[type] = []
        slice_base = None
        for slice_node in index.get_slices(node.id):
            slice_name: str = slice_node.slice_name  # type: ignore[union-attr]
            slice_model_name = (
                f"{self.context.resource_name}{self._capitalise_slice_name(slice_name)}"
            )
            slice_index = index.get_subtree(slice_node.id)
            if len(slice_node.types) > 1:
                warnings.warn(
                    f"Slice '{slice_name}' on element '{node.path}' has multiple types; "
                    f"only the first will be used for slice model base class resolution."
                )

            if slice_node.profile_urls:
                slice_base = self.resolve_type(slice_node.types[0]).type
            elif not slice_entry_base and len(slice_node.types):
                slice_base = self.resolve_type(slice_node.types[0]).type
            else:
                slice_base = slice_entry_base

            if not isinstance(
                slice_base, type
            ):
                raise TypeError(f"Resolved slice base for slice '{node.id}' is not a type")

            # Ensure the slice base is a subclass of FHIRSliceModel, as all slice models must inherit from it for validation purposes
            if slice_base is FHIRSliceModel or (
                isinstance(slice_base, type) and issubclass(slice_base, FHIRSliceModel)
            ):
                slice_bases = (slice_base,)
            else:
                slice_bases = (slice_base, FHIRSliceModel)

            assembler = ModelAssembler(
                index=slice_index,
                ctx=self.context,
                resource_name=slice_model_name,
            )
            slice_model = assembler.assemble(slice_model_name, base=slice_bases)
            # Set the slice cardinality on the model for later validation use
            if not (isinstance(slice_model, type) and issubclass(slice_model, FHIRSliceModel)):
                raise TypeError(f"Built slice model '{slice_model_name}' does not inherit from FHIRSliceModel")
            slice_model.min_cardinality = slice_node.min_cardinality
            slice_model.max_cardinality = slice_node.max_cardinality

            if slice_model is None:
                raise TypeError(
                    f"Failed to build slice model with fields for slice '{slice_name}'"
                )

            slice_models.append(slice_model)

        union_types = [*inherited_slices, *slice_models]
        # If the slicing rules are not 'closed', include the base type (either from the slice entry or the slice definition) in the union to allow for unsliced entries
        if not node.slicing_rules == "closed":
            union_types += [slice_entry_base or slice_base]
        if len(union_types) == 1:
            annotation = union_types[0]
        else:
            annotation = Annotated[
                Union[tuple(union_types)],
                Field(union_mode="left_to_right"),
            ]

        build.fields.append(
            self.build_field_information(
                safe_name,
                node,
                annotation,
                alias=node.name if safe_name != node.name else None,
                validation_alias=val_alias,
                description=getattr(node.definition, "short", None),
            )
        )

        # Slicing cardinality validator
        build.validators.append(
            ValidatorInformation(
                name=f"{safe_name}_slicing_cardinality_validator",
                kind="field",
                function=validate_slicing_cardinalities,
                arguments={"field_name": safe_name},
                field=safe_name,
            )
        )

        return build

    @staticmethod
    def _capitalise_slice_name(name: str) -> str:
        return "".join(capitalize(part) for part in name.split("-"))
