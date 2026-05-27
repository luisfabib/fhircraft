"""
DefinitionIndex — flat, dict-based index of :class:`ElementNode` objects.
"""

from __future__ import annotations

from typing import Any, Iterator, List, overload

from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.exceptions import FactoryDefinitionIndexError
from fhircraft.utils import capitalize


class DefinitionIndex:
    """
    Indexed collection of :class:`ElementNode` objects keyed by ``element.id`` and ``element.path``.
    """

    def __init__(self, nodes: list[ElementNode]) -> None:
        self._nodes_by_id: dict[str, ElementNode] = {}
        self._nodes_by_path: dict[str, List[ElementNode]] = {}
        self._synthetic_ids: set[str] = set()
        for node in nodes:
            self.add(node, replace=True)

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

    def add(self, node: ElementNode, replace: bool = False) -> None:
        """Add an :class:`ElementNode` to this index."""
        if node.id in self._nodes_by_id:
            if not replace:
                raise FactoryDefinitionIndexError(
                    f"Duplicate element id {node.id!r} cannot be added to index."
                )
            else:
                self._nodes_by_id[node.id] = node
        self._nodes_by_id[node.id] = node
        self._nodes_by_path.setdefault(node.path, []).append(node)
        if node.is_polymorphic_type and node.type_codes:
            # Add synthetic nodes for each type choice (e.g. Observation.valueString)
            for type_code in node.type_codes:
                type_node = ElementNode(
                    definition=node.definition.model_copy(
                        update={
                            "id": node.id.replace("[x]", capitalize(type_code)),
                            "path": node.path.replace("[x]", capitalize(type_code)),
                            "type": [node.definition.type[0].model_copy(update={"code": type_code})],  # type: ignore
                            "slicing": None,
                        }
                    )
                )
                if type_node.id not in self:
                    self._synthetic_ids.add(type_node.id)
                    self.add(type_node)

    def update(self, nodes: list[ElementNode], replace: bool = False) -> None:
        """Add multiple :class:`ElementNode` objects to this index."""
        for node in nodes:
            self.add(node, replace=replace)

    @overload
    def _get_without_root(self, *, id: str, path: None = ...) -> ElementNode | None: ...

    @overload
    def _get_without_root(
        self, *, id: None = ..., path: str
    ) -> List[ElementNode] | None: ...

    def _get_without_root(
        self, *, id: str | None = None, path: str | None = None
    ) -> ElementNode | List[ElementNode] | None:
        """Helper for get() that ignores the root element when matching by id or path."""
        if id is not None:
            return next(
                (
                    n
                    for n in self.nodes
                    if ".".join(n.id_segments[1:])
                    == (id.split(".", 1)[1] if "." in id else id)
                ),
                None,
            )
        if path is not None:
            return [
                n
                for n in self.nodes
                if ".".join(n.path_segments[1:])
                == (path.split(".", 1)[1] if "." in path else path)
            ]
        return None

    def contains(
        self,
        *,
        id: str | None = None,
        path: str | None = None,
        ignore_root: bool = False,
    ) -> bool:
        """
        Check if an element node exists by id or path.
        """
        if ignore_root:
            if id:
                node = self._get_without_root(id=id)
            elif path:
                node = self._get_without_root(path=path)
            else:
                return False
        else:
            if id:
                node = self._nodes_by_id.get(id)
            elif path:
                node = self._nodes_by_path.get(path, [])
            else:
                return False
        return bool(node)

    def get(self, id: str, ignore_root: bool = False) -> ElementNode:
        """
        Get element node by id
        """
        if ignore_root:
            node = self._get_without_root(id=id)
        else:
            node = self._nodes_by_id.get(id)
        if not node:
            raise FactoryDefinitionIndexError(f"Element id {id!r} not found in index.")
        return node

    def get_by_path(
        self, path: str, ignore_root: bool = False, ignore_slices: bool = False
    ) -> List[ElementNode]:
        """
        Get element node by path, can return multiple matches
        """
        if ignore_root:
            nodes = self._get_without_root(path=path)
        else:
            nodes = self._nodes_by_path.get(path, [])
        if nodes and ignore_slices:
            nodes = [n for n in nodes if not n.is_slice and not n.is_type_choice_slice]
            if len(nodes) > 1:
                non_slice_child_nodes = [n for n in nodes if not n.is_slice_child]
                if non_slice_child_nodes:
                    nodes = non_slice_child_nodes
        if not nodes:
            raise FactoryDefinitionIndexError(f"Element path {path!r} not found in index.")
        return nodes

    def get_single_by_path(
        self, path: str, ignore_root: bool = False, ignore_slices: bool = False
    ) -> ElementNode:
        """
        Get a single element node by path, raises an error if multiple matches are found.
        """
        nodes = self.get_by_path(
            path=path, ignore_root=ignore_root, ignore_slices=ignore_slices
        )
        if len(nodes) > 1:
            raise FactoryDefinitionIndexError(
                f"expected a single element node but found {len(nodes)} for path {path!r} in index. The following nodes were found: {[n.id for n in nodes]}"
            )
        return nodes[0]

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
            raise FactoryDefinitionIndexError("DefinitionIndex has no root element.")
        if len(root_node) > 1:
            raise FactoryDefinitionIndexError(
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
            raise FactoryDefinitionIndexError(
                f"Element {id!r} has no parent (it is a root element)."
            )

    def get_children(self, id: str) -> list[ElementNode]:
        """
        Return immediate non-slice children of *id*.

        Synthetic type-expansion nodes (e.g. ``Observation.valueQuantity``
        generated from ``Observation.value[x]``) are excluded — the
        :class:`TypeChoiceFieldBuilder` already handles the canonical
        ``value[x]`` element and emits one typed field per type.
        """
        return [
            n
            for n in self.nodes
            if n.parent_id == id
            and not n.is_slice
            and not n.is_type_choice_slice
            and n.id not in self._synthetic_ids
        ]

    def get_slices(self, id: str) -> list[ElementNode]:
        """
        Return the named slices defined under *id*.
        """
        node = self.get(id)
        if not node.is_slice_entry:
            raise FactoryDefinitionIndexError(
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

        The returned index is re-rooted: the matched element becomes the root
        with an id equal to its capitalised :attr:`~ElementNode.name`
        (e.g. ``Observation.component`` → ``Component``), and all descendant
        ids and paths are rewritten accordingly.
        """
        root_node = self.get(id)
        raw_name = root_node.name
        new_root_name = raw_name[0].upper() + raw_name[1:]

        # Original path prefix used for rewriting path fields (no slice names).
        original_path = root_node.path
        original_path_dot = original_path + "."

        prefix_dot = id + "."
        prefix_colon = id + ":"

        def _rewrite_id(original_id: str) -> str:
            if original_id == id:
                return new_root_name
            if original_id.startswith(prefix_dot):
                return new_root_name + "." + original_id[len(prefix_dot) :]
            if original_id.startswith(prefix_colon):
                return new_root_name + ":" + original_id[len(prefix_colon) :]
            return original_id

        def _rewrite_path(original_path_value: str) -> str:
            if original_path_value == original_path:
                return new_root_name
            if original_path_value.startswith(original_path_dot):
                return (
                    new_root_name + "." + original_path_value[len(original_path_dot) :]
                )
            return original_path_value

        subtree_nodes = []
        for node in self.nodes:
            node_id = node.id
            if node_id in self._synthetic_ids:
                continue
            if (
                node_id != id
                and not node_id.startswith(prefix_dot)
                and not node_id.startswith(prefix_colon)
            ):
                continue
            new_definition = node.definition.model_copy(
                update={
                    "id": _rewrite_id(node_id),
                    "path": _rewrite_path(node.path),
                }
            )
            subtree_nodes.append(ElementNode(definition=new_definition))

        return DefinitionIndex(subtree_nodes)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        try:
            r = self.root()
            return f"DefinitionIndex(root={r.id!r}, size={len(self)})"
        except FactoryDefinitionIndexError:
            return f"DefinitionIndex(size={len(self)})"
