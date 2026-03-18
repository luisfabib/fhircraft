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


class TypeChoiceFieldBuilder(Builder):

    def can_handle(self, node: ElementNode, _: DefinitionIndex) -> bool:
        return node.is_polymorphic_type

    def build(self, node: ElementNode, _: DefinitionIndex) -> Build:

        build = Build()
        base_name = node.name
        field_type_infos = [self.resolve_type(type) for type in node.types]

        if not field_type_infos:
            raise TypeResolutionError(
                f"Element '{node.path}' is a type choice but has none of its types could be resolved"
            )

        for field_type_info in field_type_infos:
            field_type = field_type_info.type

            typed_name = f"{base_name}{field_type if isinstance(field_type, str) else field_type.__name__}"
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

            # Add primitive extension field if applicable
            if field_type_info.requires_primitive_extension:
                placeholder = self.build_primitive_extension_placeholder(node)
                build.fields.append(placeholder)

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
