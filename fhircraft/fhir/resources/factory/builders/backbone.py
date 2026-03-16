from fhircraft.fhir.resources.factory.builders.base import Build, Builder
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.base import FHIRBaseModel

from pydantic import BaseModel
from typing import get_args as _get_args
from fhircraft.utils import capitalize


class BackboneFieldBuilder(Builder):

    def can_handle(self, node: ElementNode, index: DefinitionIndex) -> bool:
        has_children = bool(index.get_children(node.id))
        return has_children

    def build(self, node: ElementNode, index: DefinitionIndex) -> Build:
        from fhircraft.fhir.resources.factory.assembler import ModelAssembler

        build = Build()
        safe_name, val_alias = self.handle_python_keyword(node.name)

        # Determine the base class for the backbone model:
        backbone_base: type | None = None
        if self.context.base is not None:
            # First try to resolve the backbone base type from the base model's field annotation
            backbone_base = self.resolve_type_from_base_model(safe_name)
        if backbone_base is None:
            # Fallback: use the FHIR type resolved from the element definition
            ft = self.resolve_type(node.types[0])
            backbone_base = (
                ft
                if isinstance(ft, type)
                else (
                    self.resolve_type(node.types[0]).type
                    if node.types
                    else FHIRBaseModel
                )
            )

        # Build the backbone model name from the element path
        path_parts = node.path.split(".")[1:]  # strip resource prefix
        backbone_name = self.context.resource_name + "".join(
            capitalize(part.replace("[x]", "")) for part in path_parts
        )

        assembler = ModelAssembler(
            index=index.get_subtree(node.id),
            ctx=self.context,
            resource_name=backbone_name,
        )
        backbone_model = assembler.assemble(backbone_name, base=(backbone_base,))

        if not backbone_model:
            raise TypeError(
                f"Failed to build backbone model with fields for element '{node.path}'"
            )

        build.fields.append(
            self.build_field_information(
                safe_name,
                node,
                backbone_model,
                validation_alias=val_alias,
            )
        )

        build.validators = self.build_field_validators(node, safe_name)

        return build
