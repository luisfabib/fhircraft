"""
DefinitionIndex — flat, dict-based index of :class:`ElementNode` objects.

Replaces the ``StructureNode`` tree.  All navigation is performed through
string-key lookups and filtering rather than pointer traversal.
"""

from __future__ import annotations

from typing import Any, Iterator, List

from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.exceptions import DefinitionIndexError


class DefinitionIndex:
    """
    Indexed collection of :class:`ElementNode` objects keyed by ``element.id`` and ``element.path``.
    """

    def __init__(self, nodes: list[ElementNode]) -> None:
        self._nodes_by_id: dict[str, ElementNode] = {node.id: node for node in nodes}
        self._nodes_by_path: dict[str, List[ElementNode]] = {}
        for node in nodes:
            self._nodes_by_path.setdefault(node.path, []).append(node)

    @classmethod
    def from_elements(cls, elements: list[Any]) -> DefinitionIndex:
        """Wrap each *ElementDefinition* in an :class:`ElementNode` and build the index.

        Args:
            elements: List of raw FHIR ``ElementDefinition`` objects (any version).

        Returns:
            A fully populated :class:`DefinitionIndex`.
        """
        return cls([ElementNode(definition=element) for element in elements])

    # ------------------------------------------------------------------
    # Basic access
    # ------------------------------------------------------------------

    @property
    def nodes(self) -> list[ElementNode]:
        """List of all nodes in this index."""
        return list(self._nodes_by_id.values())

    def get(self, id: str) -> ElementNode:
        """
        Get element node by id
        """
        if id not in self._nodes_by_id:
            raise DefinitionIndexError(f"Element id {id!r} not found in index.")
        return self._nodes_by_id[id]

    def get_by_path(self, path: str) -> List[ElementNode]:
        """
        Get element node by path, can return multiple matches
        """
        if path not in self._nodes_by_path:
            raise DefinitionIndexError(f"Element path {path!r} not found in index.")
        return self._nodes_by_path[path]

    def __contains__(self, element_id: str) -> bool:
        return element_id in self._nodes_by_id

    def __iter__(self) -> Iterator[ElementNode]:
        return iter(self._nodes_by_id.values())

    def __len__(self) -> int:
        return len(self._nodes_by_id)

    def ids(self) -> list[str]:
        """Sorted list of all element ids in this index."""
        return sorted(self._nodes_by_id.keys())

    def paths(self) -> set[str]:
        """Set of all element paths in this index."""
        return set(self._nodes_by_path.keys())

    # ------------------------------------------------------------------
    # Root detection
    # ------------------------------------------------------------------

    def root(self) -> ElementNode:
        """
        Return the single root element of this index.
        """
        root_node = [n for n in self.nodes if n.is_root]
        if not root_node:
            raise DefinitionIndexError("DefinitionIndex has no root element.")
        if len(root_node) > 1:
            raise DefinitionIndexError(
                f"DefinitionIndex has multiple root candidates: {[n.id for n in root_node]}"
            )
        return root_node[0]

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def get_parent(self, id: str) -> ElementNode:
        """
        Return the parent of the element with *id*.
        """
        if parent_id := self.get(id).parent_id:
            return self.get(parent_id)
        else:
            raise DefinitionIndexError(
                f"Element {id!r} has no parent (it is a root element)."
            )

    def get_children(self, id: str) -> list[ElementNode]:
        """
        Return immediate non-slice children of *id*.
        """
        return [n for n in self.nodes if n.parent_id == id and not n.is_slice]

    def get_slices(self, id: str) -> list[ElementNode]:
        """
        Return the named slices defined under *id*.
        """
        node = self.get(id)
        if not node.is_slice_entry:
            raise DefinitionIndexError(
                f"Element {id!r} is not a slicing entry and cannot have slices."
            )
        return [n for n in self.nodes if n.is_slice and n.id.startswith(node.id + ":")]

    def get_slice_children(self, slice_id: str) -> list[ElementNode]:
        """
        Convenience alias for :meth:`children` when navigating inside a slice.

        Returns immediate non-slice elements whose ``parent_id == slice_id``.
        """
        return self.get_children(slice_id)

    def get_subtree(self, id: str) -> DefinitionIndex:
        """
        Return a new :class:`DefinitionIndex` scoped to *id* and all of
        its descendants (children, slices, and their sub-elements).
        """
        prefix_dot = id + "."
        prefix_colon = id + ":"
        subtree_nodes = [
            node
            for node in self.nodes
            if (
                node.id == id
                or node.id.startswith(prefix_dot)
                or node.id.startswith(prefix_colon)
            )
        ]
        return DefinitionIndex(subtree_nodes)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        try:
            r = self.root()
            return f"DefinitionIndex(root={r.id!r}, size={len(self)})"
        except DefinitionIndexError:
            return f"DefinitionIndex(size={len(self)})"
