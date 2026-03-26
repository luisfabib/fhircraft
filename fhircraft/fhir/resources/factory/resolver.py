"""
SnapshotResolver — turns any StructureDefinition into a complete
:class:`~fhircraft.fhir.resources.factory.index.DefinitionIndex`.
"""

from typing import Sequence, Literal, TYPE_CHECKING

from fhircraft.fhir.resources.definitions.registry import StructureDefinitionRegistry
from fhircraft.fhir.resources.factory.element_node import (
    ElementNode,
    FHIRPATH_TYPE_PREFIX,
    FHIR_TYPE_PREFIX,
)
from fhircraft.fhir.resources.factory.exceptions import (
    DefinitionResolutionError,
)
from fhircraft.fhir.resources.factory.index import DefinitionIndex

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4.complex import (
        ElementDefinition as R4_ElementDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R4B.complex import (
        ElementDefinition as R4B_ElementDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R5.complex import (
        ElementDefinition as R5_ElementDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R4.core import (
        StructureDefinition as R4_StructureDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R4B.core import (
        StructureDefinition as R4B_StructureDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R5.core import (
        StructureDefinition as R5_StructureDefinition,
    )

_BASE_MERGE_FIELDS = {"min", "max", "type", "short", "definition", "comment"}


class SnapshotResolver:
    """
    Resolves a FHIR ``StructureDefinition`` into a complete :class:`DefinitionIndex`.
    """

    def __init__(self, registry: StructureDefinitionRegistry) -> None:
        self._registry = registry

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def resolve(
        self,
        sd: "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition",
        mode: Literal["auto", "snapshot", "differential"] = "auto",
    ) -> DefinitionIndex:
        """
        Resolve a StructureDefinition into a DefinitionIndex.
        This method resolves either the snapshot or differential representation of a
        StructureDefinition into a normalized DefinitionIndex. When mode is set to "auto",
        the method automatically selects the differential mode if available, otherwise uses
        snapshot mode.

        Args:
            sd: A FHIR StructureDefinition resource (R4, R4B, or R5 version).
            mode: Resolution mode to use. Defaults to "auto". Options are:
                  - "auto": Automatically selects "differential" if available, else "snapshot"
                  - "snapshot": Uses the snapshot representation directly
                  - "differential": Merges the differential over the base_index

        Returns:
            DefinitionIndex: A resolved index of FHIR elements.

        Raises:
            AssertionError: If the selected mode's required elements are missing or contain None values.
            DefinitionResolutionError: If neither snapshot nor differential elements are available.
        """

        if mode == "auto":
            mode = (
                "differential"
                if sd.baseDefinition
                and sd.differential
                and len(sd.differential.element or []) > 1
                else "snapshot"
            )
        if mode == "snapshot":
            # Type check assertions
            assert (
                sd.snapshot
            ), f"StructureDefinition {sd.name or sd.url} snapshot is None"
            assert (
                sd.snapshot.element
            ), f"StructureDefinition {sd.name or sd.url} snapshot.element is None"
            assert all(
                [e is not None for e in sd.snapshot.element]
            ), f"StructureDefinition {sd.name or sd.url} snapshot.element contains None"
            # Fast path: wrap snapshot elements directly without merging
            elements = sd.snapshot.element
            resolved_index = DefinitionIndex.from_elements(elements)

        elif mode == "differential":
            # Type check assertions
            assert (
                sd.differential
            ), f"StructureDefinition {sd.name or sd.url} differential is None"
            assert (
                sd.differential.element
            ), f"StructureDefinition {sd.name or sd.url} differential.element is None"
            assert all(
                [e is not None for e in sd.differential.element]
            ), f"StructureDefinition {sd.name or sd.url} differential.element contains None"

            if not (base_canonical := sd.baseDefinition):
                raise DefinitionResolutionError(
                    f"StructureDefinition '{getattr(sd, 'name', '?')}' has no baseDefinition, which is required for differential resolution."
                )
            # Obtain the base snapshot for differential resolution
            base_definition = self._registry.get(base_canonical)
            partial_base_index = self.resolve(base_definition, mode="auto")
            if base_definition.snapshot and base_definition.snapshot.element:
                base_index = DefinitionIndex.from_elements(
                    base_definition.snapshot.element
                )
                base_index.update(partial_base_index.nodes, replace=True)
            else:
                base_index = partial_base_index
            # Merge differential over base snapshot to produce a synthetic snapshot
            resolved_index = self._resolve_differential(
                sd.differential.element, base_index
            )
        else:
            raise DefinitionResolutionError(
                f"StructureDefinition '{getattr(sd, 'name', '?')}' has neither a "
                "snapshot nor a differential element list."
            )

        # Finally, resolve any contentReferences in the resulting index
        resolved_index = self._resolve_content_references(resolved_index)

        return resolved_index

    # ------------------------------------------------------------------
    # Differential resolution
    # ------------------------------------------------------------------

    def _resolve_differential(
        self,
        diff_elements: "Sequence[R4_ElementDefinition] | Sequence[R4B_ElementDefinition] | Sequence[R5_ElementDefinition]",
        base_index: DefinitionIndex,
    ) -> DefinitionIndex:
        """
        Resolve differential elements by merging them with base elements from a snapshot.
        This method takes a sequence of differential elements and merges each one with
        its corresponding base element to produce a complete definition index. It handles
        building intermediate nodes as needed to support the element hierarchy.

        Args:
            diff_elements: A sequence of differential element definitions to resolve.
                           Can be R4, R4B, or R5 ElementDefinition objects.
            base_index: A DefinitionIndex containing the base snapshot elements to merge against.

        Returns:
            DefinitionIndex: A new DefinitionIndex containing the merged result, with keys
                             representing full element ids of the profile being resolved.

        Raises:
            DefinitionResolutionError: If a differential element is missing an id,
                                       or if the resolution produces an empty element list.
        """

        nodes = [ElementNode(definition=e) for e in diff_elements]

        # The merged result; keys are full element ids of the profile being resolved
        merged_nodes: dict[str, ElementNode] = {}

        # Iterate over all differential elements, merging each one (and any missing
        for node in nodes:
            if not node.id:
                raise DefinitionResolutionError(
                    "Differential element with missing id cannot be resolved."
                )

            # Build intermediate segments from base snapshot as needed to support this node's id
            for id in node.id_ancestry:
                if id not in merged_nodes:
                    intermediate_node = self._build_intermediate_node(id, base_index)
                    if intermediate_node is not None and id != node.id:
                        merged_nodes[id] = intermediate_node

            if node.is_root:
                # Root element of the differential; must match the base snapshot root
                base_node = base_index.root()
            else:
                # Look up the base node for this element
                if base_index.contains(id=node.id, ignore_root=True):
                    base_node = base_index.get(node.id, ignore_root=True)
                elif base_index.contains(path=node.path, ignore_root=True):
                    base_node = base_index.get_single_by_path(
                        node.path, ignore_root=True, ignore_slices=True
                    )
                else:
                    base_node = None

            if base_node is None:
                merged_nodes[node.id] = node
            else:
                # Now, merge the actual differential node
                merged_nodes[node.id] = self._merge_node_with_base(node, base_node)

        if not merged_nodes:
            raise DefinitionResolutionError(
                "Differential resolution produced an empty element list."
            )

        return DefinitionIndex(list(merged_nodes.values()))

    def _build_intermediate_node(
        self, id: str, base_index: DefinitionIndex
    ) -> ElementNode | None:
        """
        Build an intermediate ElementNode from a base definition.

        This is used to fill in missing segments of the element hierarchy
        that are not explicitly defined in the differential but are needed
        to support the full element ids used by the differential nodes.

        It first checks if the exact node id exists in the base index. If not
        defined in the base, it attempts to build the intermediate node by looking up
        its parent node in the base index and expanding its types. If neither of these
        approaches succeed, an error is raised.
        """
        root_name = id.rsplit(".", 1)[0] if "." in id else ""
        path = ".".join([seg.split(":")[0] for seg in id.split(".")])
        if not "." in id:
            base_node = base_index.root()
        elif base_index.contains(id=id, ignore_root=True):
            base_node = base_index.get(id, ignore_root=True)
        elif base_index.contains(path=path, ignore_root=True):
            base_node = base_index.get_single_by_path(
                path, ignore_root=True, ignore_slices=True
            )
        elif (parent_path := path.rsplit(".", 1)[0]) and base_index.contains(
            path=parent_path, ignore_root=True
        ):
            parent_base_node = base_index.get_single_by_path(
                parent_path, ignore_root=True, ignore_slices=True
            )
            node = self._build_type_node(parent_base_node.type_codes, id, base_index)
            base_index.add(node)
            return node
        else:
            return None
        new_path = (
            ".".join(filter(None, [root_name, *base_node.path_segments[1:]]))
            if root_name
            else base_node.path
        )
        merge_fields = base_node.definition.model_dump(include=set(_BASE_MERGE_FIELDS))
        # For type-choice type-slices (e.g. value[x]:valueQuantity) narrow the
        # inherited type list to the single concrete type indicated by the suffix.
        candidate = ElementNode(
            definition=base_node.definition.__class__(
                id=id, path=new_path, **merge_fields
            )
        )
        if candidate.is_type_choice_slice and base_node.types:
            concrete_suffix = id.rsplit(":", 1)[1].lower()
            matched_type = next(
                (
                    t
                    for t in base_node.types
                    if t.code and concrete_suffix.endswith(str(t.code).lower())
                ),
                None,
            )
            if matched_type is not None:
                merge_fields["type"] = [matched_type]
        new_definition = base_node.definition.__class__(
            id=id,
            path=new_path,
            **merge_fields,
        )
        return ElementNode(definition=new_definition)

    def _build_type_node(
        self,
        datatypes: Sequence[str],
        id: str,
        base_index: DefinitionIndex,
    ) -> ElementNode:
        """
        Build a type node by resolving and expanding a complex FHIR type.
        This method constructs an ElementNode for a given FHIR datatype by retrieving
        the corresponding StructureDefinition from the repository and extracting the
        matching element definition from its snapshot.

        Args:
            datatypes: A sequence of datatype names to expand. When multiple types are
                       provided (e.g. for a polymorphic ``value[x]`` element), each type
                       is tried in order and the first one that contains a matching
                       sub-element is used.
            id: The unique identifier for the element node to be created.
            base_index: A DefinitionIndex used to check for existing elements.

        Returns:
            ElementNode: A newly constructed ElementNode with the expanded type definition.

        Raises:
            DefinitionResolutionError

        Notes:
            - This method is used during differential StructureDefinition resolution.
            - Only complex types are supported for expansion; primitive and FHIRPath types
              are skipped when iterating over multiple candidates.
            - The generated element id is checked against the base index to prevent conflicts.
        """
        if not self._registry:
            raise DefinitionResolutionError(
                "Repository is required for type expansion during differential resolution."
            )

        if not datatypes:
            raise DefinitionResolutionError(
                f"Type expansion failed for element '{id}'. No type codes provided."
            )

        local_id = id.rsplit(".", 1)[-1]
        id_path = ".".join([seg.split(":")[0] for seg in id.split(".")])
        if id in base_index:
            raise DefinitionResolutionError(
                f"Type expansion failed: generated intermediate node id '{id}' already exists in base index."
            )

        for datatype in datatypes:
            if datatype.startswith(FHIRPATH_TYPE_PREFIX):
                continue
            try:
                type_structure_definition = self._registry.get(
                    f"{FHIR_TYPE_PREFIX}{datatype}"
                )
            except FileNotFoundError:
                continue
            if type_structure_definition.kind != "complex-type":
                continue
            snapshot = type_structure_definition.snapshot
            if not snapshot or not snapshot.element:
                continue
            matching_node = next(
                (
                    n
                    for e in snapshot.element
                    if (n := ElementNode(e)).local_id == local_id
                ),
                None,
            )
            if matching_node is None:
                continue
            # Determine unsliced path for newly synthesised element
            return ElementNode(
                definition=matching_node.definition.__class__(
                    id=id,
                    path=id_path,
                    **matching_node.definition.model_dump(
                        include=set(_BASE_MERGE_FIELDS)
                    ),
                )
            )

        raise DefinitionResolutionError(
            f"Type expansion failed for element '{id}'. No matching element with local id "
            f"'{local_id}' found in any of the provided types: {list(datatypes)}."
        )

    def _merge_node_with_base(
        self, node: ElementNode, base_node: ElementNode
    ) -> ElementNode:
        """
        Merge a node with its base node to create a new ElementNode with combined definitions.
        This method combines the definition attributes from both the given node and its base node,
        with the given node's attributes taking precedence. The merged definition retains the
        node's id and path, or uses the base node's path if the node's path is not defined.

        Args:
            node: The node to merge, whose definition attributes take precedence.
            base_node: The base node providing default definition attributes.

        Returns:
            ElementNode: A new ElementNode containing the merged definition from both nodes.
        """
        merged_definition = base_node.definition.__class__(
            id=node.id,
            path=node.path or base_node.path,
            **{
                **base_node.definition.model_dump(
                    exclude_none=True, exclude={"id", "path", "contentReference"}
                ),
                **node.definition.model_dump(
                    exclude_none=True, exclude={"id", "path", "contentReference"}
                ),
            },
        )
        return ElementNode(definition=merged_definition)

    def _resolve_content_references(self, index: DefinitionIndex) -> DefinitionIndex:
        """
        Resolve contentReferences in the given DefinitionIndex by replacing them with the
        referenced element definitions.

        This method iterates through all elements in the provided DefinitionIndex and identifies
        any elements that contain a contentReference. For each contentReference found, it locates
        the referenced element definition within the same index (or an external StructureDefinition if specified)
        and replaces the original element's definition with a new definition based on the referenced one.

        Args:
            index: The DefinitionIndex to process for contentReference resolution.

        Returns:
            DefinitionIndex: A new DefinitionIndex with all contentReferences resolved to their actual definitions.
        """
        resolved_nodes = []
        for node in index.nodes:
            if not node.is_content_reference:
                resolved_nodes.append(node)
                continue

            reference: str = node.definition.contentReference  # type: ignore[union-attr]
            resource_url, ref_path = (
                reference.split("#") if "#" in reference else ("", reference)
            )

            # Locate the referenced sub-tree
            if resource_url:
                # External reference — load from registry
                ref_sd = self._registry.get(resource_url)
                if not ref_sd or not ref_sd.snapshot or not ref_sd.snapshot.element:
                    raise ValueError(
                        f"Cannot resolve contentReference '{reference}' — resource not found."
                    )
                ref_index = DefinitionIndex.from_elements(ref_sd.snapshot.element)
            else:
                ref_index = index

            # Navigate to the referenced element
            ref_node = ref_index.get(ref_path)
            resolved_nodes.append(
                self._merge_node_with_base(
                    node,
                    ref_node,
                )
            )
        return DefinitionIndex(nodes=resolved_nodes)
