from fhircraft.fhir.resources.factory.builders.base import Build, Builder
from fhircraft.fhir.resources.factory.element_node import ElementNode, BACKBONE_CODES
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.base import FHIRBaseModel

from pydantic import BaseModel
from fhircraft.utils import _get_deepest_args, capitalize


class BackboneFieldBuilder(Builder):

    def can_handle(self, node: ElementNode, index: DefinitionIndex) -> bool:
        has_children = bool(index.get_children(node.id))
        if has_children:
            return True
        if node.type_codes and any(code in BACKBONE_CODES for code in node.type_codes):
            if self.context.base and node.name in self.context.base.model_fields:
                backbone_base = next(
                    (
                        m
                        for m in _get_deepest_args(
                            self.context.base.model_fields[node.name].annotation
                        )
                        if isinstance(m, type)
                        and issubclass(m, BaseModel)
                        and m is not type(None)
                    ),
                    None,
                )
                if backbone_base is not None:
                    return True
        return False

    def build(self, node: ElementNode, index: DefinitionIndex) -> Build:
        from fhircraft.fhir.resources.factory.assembler import ModelAssembler

        build = Build()
        safe_name, val_alias = self.handle_python_keyword(node.name)

        # Determine the base class for the backbone model:
        backbone_base: type | None = None
        if self.context.base and safe_name in self.context.base.model_fields:
            # First try to resolve the backbone base type from the base model's field annotation
            backbone_base = next(
                (
                    model
                    for model in _get_deepest_args(
                        self.context.base.model_fields.get(safe_name).annotation
                    )
                    if isinstance(model, type)
                    and issubclass(model, BaseModel)
                    and not model is type(None)
                ),
                None,
            )

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

        # When no child elements are constrained, use the resolved backbone type directly instead of creating an empty wrapper subclass.
        if not index.get_children(node.id):
            build.fields.append(
                self.build_field_information(
                    safe_name,
                    node,
                    backbone_base,
                    validation_alias=val_alias,
                )
            )
            build.validators = self.build_field_validators(node, safe_name)
            return build

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
