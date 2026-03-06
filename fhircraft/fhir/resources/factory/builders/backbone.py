from fhircraft.fhir.resources.factory.builders.base import Build, Builder
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.index import DefinitionIndex

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

            if issubclass(self.context.base, BaseModel):
                fi = self.context.base.model_fields.get(safe_name)
                if fi:
                    # Dig through Optional[List[...]] to find the inner type
                    inner = fi.annotation
                    while inner:
                        args = _get_args(inner)
                        if not args:
                            break
                        # Filter out NoneType
                        non_none = [a for a in args if a is not type(None)]
                        if not non_none:
                            break
                        inner = non_none[0]

                    if isinstance(inner, type) and issubclass(inner, BaseModel):
                        backbone_base = inner

        if backbone_base is None:
            # Fallback: use the FHIR type resolved from the element definition
            ft = self.resolve_type(node.types[0])
            backbone_base = ft if isinstance(ft, type) else None

        if backbone_base is None:
            from fhircraft.fhir.resources.base import FHIRBaseModel

            backbone_base = FHIRBaseModel

        # Build the backbone model name from the element path
        path_parts = node.path.split(".")[1:]  # strip resource prefix
        backbone_name = backbone_base.__name__ + "".join(
            capitalize(part.replace("[x]", "")) for part in path_parts
        )

        assembler = ModelAssembler(
            index=index.get_subtree(node.id),
            ctx=self.context,
            base_model=backbone_base,
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
