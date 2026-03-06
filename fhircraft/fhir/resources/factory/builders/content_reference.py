from fhircraft.fhir.resources.factory.builders.backbone import BackboneFieldBuilder
from fhircraft.fhir.resources.factory.builders.base import (
    Build,
    Builder,
)
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.index import DefinitionIndex


class ContentReferenceBuilder(Builder):
    """
    Handles elements where ``contentReference`` points to another element in
    the same (or an external) StructureDefinition.

    The referenced sub-tree is located and — if no cycle is detected — the
    element is built as a backbone field using the referenced children.  On
    cycle detection the referenced type code is used directly instead.
    """

    def can_handle(self, node: ElementNode, _: DefinitionIndex) -> bool:
        return node.is_content_reference

    def build(self, node: ElementNode, index: DefinitionIndex) -> Build:

        ref: str = node.definition.contentReference  # type: ignore[union-attr]
        resource_url, ref_path = ref.split("#") if "#" in ref else ("", ref)

        # Locate the referenced sub-tree
        if resource_url:
            # External reference — load from registry
            ref_sd = self.context.registry.get(resource_url)
            if not ref_sd or not ref_sd.snapshot or not ref_sd.snapshot.element:
                raise ValueError(
                    f"Cannot resolve contentReference '{ref}' — resource not found."
                )
            ref_index = DefinitionIndex.from_elements(ref_sd.snapshot.element)
        else:
            ref_index = index

        # Navigate to the referenced element
        ref_node = ref_index.get(ref_path)
        if ref_node is None:
            # Try relative path (strip resource prefix)
            parts = ref_path.split(".", 1)
            ref_node = (
                ref_index.get(ref_path) if len(parts) < 2 else ref_index.get(ref_path)
            )

        if ref_node is None:
            raise ValueError(f"Cannot navigate to contentReference path '{ref_path}'.")

        ref_subtree = ref_index.get_subtree(ref_path)

        # Build using BackboneFieldBuilder with the referenced sub-tree
        return BackboneFieldBuilder(context=self.context).build(
            node,
            ref_subtree,
        )
