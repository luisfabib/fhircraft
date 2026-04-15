"""
Builders for handling polymorphic type-choice elements, which can have multiple types defined in FHIR (e.g., value[x]).
"""

from functools import partial
from fhircraft.fhir.resources.factory.builders.base import (
    Build,
    Builder,
    ValidatorInformation,
)
from fhircraft.fhir.resources.factory.builders.simple import SimpleFieldBuilder
from fhircraft.fhir.resources.factory.context import BuildContext
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.exceptions import TypeResolutionError
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.validators import (
    validate_type_choice_element,
    get_type_choice_value_by_base,
)
from fhircraft.utils import capitalize


class TypeChoiceFieldBuilder(Builder):

    def can_handle(self, node: ElementNode, index: DefinitionIndex) -> bool:
        return node.is_polymorphic_type

    def build(self, node: ElementNode, index: DefinitionIndex) -> Build:
        from fhircraft.fhir.resources.factory.assembler import ModelAssembler

        build = Build()
        base_name = node.name
        field_type_infos = [self.resolve_type(type) for type in node.types]

        if not field_type_infos:
            raise TypeResolutionError(
                f"Element '{node.path}' is a type choice but has none of its types could be resolved"
            )

        sub_models: dict[str, type] = {}
        children = index.get_children(node.id)
        if isinstance(children, list) and children:
            subtree = index.get_subtree(node.id)
            for field_type_info in field_type_infos:
                original_type = field_type_info.type
                type_name = (
                    original_type
                    if isinstance(original_type, str)
                    else original_type.__name__
                )
                sub_model_name = (
                    f"{self.context.resource_name}{capitalize(base_name)}{type_name}"
                )
                assembler = ModelAssembler(
                    index=subtree,
                    ctx=self.context,
                    resource_name=sub_model_name,
                )
                sub_models[type_name] = assembler.assemble(
                    sub_model_name, base=(original_type,)
                )

        for field_type_info in field_type_infos:
            original_type = field_type_info.type
            type_name = (
                original_type
                if isinstance(original_type, str)
                else original_type.__name__
            )
            # Use the sub-model as the actual field type when children are present;
            # the field name always uses the original (base) type name so that the
            # type-choice validator keeps working.
            field_type = sub_models.get(type_name, original_type)

            typed_name = f"{base_name}{type_name}"
            safe_name, validation_alias = self.handle_python_keyword(typed_name)

            build.fields.append(
                self.build_field_information(
                    safe_name,
                    node,
                    field_type,
                    validation_alias=validation_alias,
                )
            )

            build.validators = self.build_field_validators(node, safe_name)

        # Type-choice validator & property go on the first FieldBuild
        if build:
            build.validators.append(
                ValidatorInformation(
                    name=f"{base_name}_type_choice_validator",
                    kind="model",
                    function=validate_type_choice_element,
                    arguments={
                        "field_types": [info.type for info in field_type_infos],
                        "field_name_base": base_name,
                        "required": node.is_required,
                    },
                )
            )
            build.properties[base_name] = partial(
                get_type_choice_value_by_base, base=base_name
            )

        return build
