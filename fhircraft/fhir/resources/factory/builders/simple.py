"""
Builders for handling simple fields, which are the most common type of element in FHIR resources.
"""

from typing import Any, Union, Union
from typing import Any


from fhircraft.fhir.resources.factory.builders.base import (
    Build,
    Builder,
)
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.exceptions import TypeResolutionError
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.factory.builders.base import Builder


class SimpleFieldBuilder(Builder):
    """
    Fallback builder for all other elements.

    Produces a plain typed field, and — for FHIR primitive types — also
    appends a ``_{name}`` extension placeholder field.
    """

    def can_handle(self, _: ElementNode, __: DefinitionIndex) -> bool:
        return True  # always handles as fallback

    def build(self, node: ElementNode, _: DefinitionIndex) -> Build:

        build = Build()

        safe_name, val_alias = self.handle_python_keyword(node.name)
        field_types = [self.resolve_type(type) for type in node.types]

        if not field_types:
            raise TypeResolutionError(
                f"Element '{node.path}' has no types that could be resolved"
            )

        # Union when multiple types
        field_type: Any = (
            Union[tuple([subtype.type for subtype in field_types])]
            if len(field_types) > 1
            else field_types[0].type
        )

        # Build the field information
        build.fields.append(
            self.build_field_information(
                safe_name,
                node,
                field_type,
                validation_alias=val_alias,
            )
        )

        build.validators = self.build_field_validators(node, safe_name)

        if any(subtype.requires_primitive_extension for subtype in field_types):
            placeholder = self.build_primitive_extension_placeholder(node)
            build.fields.append(placeholder)
        return build
