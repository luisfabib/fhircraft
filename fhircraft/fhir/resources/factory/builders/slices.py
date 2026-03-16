from fhircraft.fhir.resources.factory.builders.base import (
    Build,
    Builder,
    ValidatorInformation,
)
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.base import FHIRSliceModel
from typing import Union, Annotated
from pydantic import Field
import warnings
from fhircraft.fhir.resources.validators import (
    validate_slicing_cardinalities,
)
from fhircraft.utils import capitalize


class SlicedFieldBuilder(Builder):

    def can_handle(self, node: ElementNode, index: DefinitionIndex) -> bool:
        return node.is_slice_entry

    def build(self, node: ElementNode, index: DefinitionIndex) -> Build:
        from fhircraft.fhir.resources.factory.assembler import ModelAssembler

        build = Build()
        safe_name, val_alias = self.handle_python_keyword(node.name)

        slice_entry_field_types = [self.resolve_type(type) for type in node.types]

        # Build a slice model for each named slice
        slice_models: list[type] = []
        for slice_node in index.get_slices(node.id):

            slice_name: str = slice_node.slice_name  # type: ignore[union-attr]
            slice_index = index.get_subtree(slice_node.id)

            if len(slice_node.types) > 1:
                warnings.warn(
                    f"Slice '{slice_name}' on element '{node.path}' has multiple types; "
                    f"only the first will be used for slice model base class resolution."
                )
            slice_base_type = self.resolve_type(slice_node.types[0]).type
            slice_model_name = (
                f"{self.context.resource_name}{self._capitalise_slice_name(slice_name)}"
            )

            if slice_base_type is FHIRSliceModel or issubclass(
                slice_base_type, FHIRSliceModel
            ):
                slice_bases = (slice_base_type,)
            else:
                slice_bases = (slice_base_type, FHIRSliceModel)

            assembler = ModelAssembler(
                index=slice_index,
                ctx=self.context,
                resource_name=slice_model_name,
            )
            slice_model = assembler.assemble(slice_model_name, base=slice_bases)
            # Set the slice cardinality on the model for later validation use
            assert isinstance(slice_model, type) and issubclass(
                slice_model, FHIRSliceModel
            ), f"Built slice model '{slice_model_name}' does not inherit from FHIRSliceModel"
            slice_model.min_cardinality = slice_node.min_cardinality
            slice_model.max_cardinality = slice_node.max_cardinality

            if slice_model is None:
                raise TypeError(
                    f"Failed to build slice model with fields for slice '{slice_name}'"
                )

            slice_models.append(slice_model)

        union_types = [*slice_models, *[t.type for t in slice_entry_field_types]]
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
                alias=node.name,
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
