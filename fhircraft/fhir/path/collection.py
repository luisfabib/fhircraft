"""The currency of the FHIRPath engine: a value plus where it came from."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Iterator

from fhircraft.exceptions import FHIRPathEvaluationError
from fhircraft.fhir.path.accessors import (
    Cardinality,
    ElementAccessor,
    resolve_field,
)
from fhircraft.utils import ensure_list

if TYPE_CHECKING:  # pragma: no cover
    from pydantic.fields import FieldInfo

__all__ = ["FHIRPathCollectionItem", "Collection"]

#: A FHIRPath collection is just an ordered list of items.
Collection = list


_UNSET = object()


@dataclass(slots=True, eq=False)
class FHIRPathCollectionItem:
    """One item of a FHIRPath collection, aware of its origin.

    Attributes:
        value: The item's value.
        parent: The item whose value contains this one, or ``None`` for roots, literals and environment variables.
        element: The logical FHIRPath element name under the parent, e.g. ``'given'`` or ``None`` when there is no parent.
        index: Position within the parent's list, or ``None`` for single-valued elements.
    """

    value: Any
    parent: "FHIRPathCollectionItem | None" = None
    element: str | None = None
    index: int | None = None

    # Lazily built; never part of equality or repr.
    _accessor: Any = field(default=_UNSET, repr=False, compare=False, kw_only=True)

    @classmethod
    def wrap(cls, data: Any) -> "FHIRPathCollectionItem":
        """Wrap *data* as a parentless item, passing existing items through."""
        return data if isinstance(data, cls) else cls(data)

    @classmethod
    def wrap_all(cls, data: Any) -> list["FHIRPathCollectionItem"]:
        """Wrap *data* -- scalar or iterable -- as a collection."""
        return [cls.wrap(item) for item in ensure_list(data) if item is not None]

    def child(
        self,
        value: Any,
        element: str,
        *,
        index: int | None = None,
    ) -> "FHIRPathCollectionItem":
        """Build a child item rooted at this one.

        This is what ``Element._evaluate`` calls instead of constructing an
        item and then bolting a ``partial`` onto it.
        """
        return FHIRPathCollectionItem(
            value=value,
            parent=self,
            element=element,
            index=index,
        )

    @property
    def accessor(self) -> ElementAccessor | None:
        """The write handle for this item, or ``None`` if it is not writable."""
        if self._accessor is _UNSET:
            self._accessor = ElementAccessor.for_item(self)
        return self._accessor

    @property
    def is_writable(self) -> bool:
        """Whether this item denotes a writable location in a container."""
        return self.accessor is not None

    @property
    def canonical_path(self) -> str:
        """Canonical, index-qualified FHIRPath to this item.

        ``'Patient.name[0].given[1]'``.  Round-trippable: re-evaluating the
        returned expression against the same root yields this item.  Indices
        are emitted only for list-valued elements, so scalar navigation stays
        readable.
        """
        segment = self._segment()
        if self.parent is None:
            return segment
        parent_location = self.parent.canonical_path
        if not parent_location:
            return segment
        return f"{parent_location}.{segment}" if segment else parent_location

    def _segment(self) -> str:
        if self.element is None:
            return _root_label(self.value)
        return self.element if self.index is None else f"{self.element}[{self.index}]"

    @property
    def root(self) -> "FHIRPathCollectionItem":
        """The outermost ancestor -- the resource the expression was run against."""
        item = self
        while item.parent is not None:
            item = item.parent
        return item

    @property
    def ancestors(self) -> Iterator["FHIRPathCollectionItem"]:
        """Yield parent contexts from nearest to farthest."""
        item = self.parent
        while item is not None:
            yield item
            item = item.parent

    @property
    def depth(self) -> int:
        """Number of parent contexts."""
        return sum(1 for _ in self.ancestors)

    # ------------------------------------------------------------------ #
    # Typing
    # ------------------------------------------------------------------ #

    def _require_accessor(self) -> ElementAccessor:
        accessor = self.accessor
        if accessor is None:
            raise FHIRPathEvaluationError(
                f"'{self.canonical_path}' is not a writable location: literals, "
                "environment variables and root resources cannot be modified"
            )
        return accessor

    def has_element(self, name: str) -> bool:
        """Whether this item's value declares the FHIRPath element *name*."""
        return resolve_field(self.value, name) is not None

    # ------------------------------------------------------------------ #
    # Patch interface
    # ------------------------------------------------------------------ #

    def set(self, value: Any) -> None:
        """Assign *value* at this location."""
        self._require_accessor().set(value)
        self.value = value

    def delete(self) -> None:
        """Remove the value at this location.

        The item is left in place with ``value = None``; it is a record of a
        location, and the location still exists after its content is removed.
        Sibling items holding stale indices are invalidated by the caller --
        the patch engine re-resolves between operations for exactly this
        reason.
        """
        self._require_accessor().delete()
        self.value = None

    def insert(self, value: Any, at: int) -> None:
        """Insert *value* into this item's list at position *at*."""
        self._require_accessor().insert(value, at)

    def move(self, source: int, destination: int) -> None:
        """Reorder this item's list, moving *source* to *destination*."""
        self._require_accessor().move(source, destination)

    def snapshot(self) -> Any:
        """Deep copy of the enclosing field, for rollback."""
        return self._require_accessor().snapshot()

    def restore(self, snapshot: Any) -> None:
        """Undo every mutation made since *snapshot*."""
        self._require_accessor().restore(snapshot)

    # ------------------------------------------------------------------ #
    # Dunders
    # ------------------------------------------------------------------ #

    def __eq__(self, other: Any) -> bool:
        """Compare by value.

        Items compare equal to bare values so that FHIRPath's own equality
        operators can work on collections without unwrapping first; two items
        additionally have to agree on where they came from.
        """
        if isinstance(other, FHIRPathCollectionItem):
            return (
                self.value == other.value
                and self.element == other.element
                and self.index == other.index
            )
        return self.value == other

    def __hash__(self) -> int:
        try:
            value_hash = hash(self.value)
        except TypeError:
            value_hash = hash(repr(self.value))
        return hash((self.element, self.index, value_hash))

    def __repr__(self) -> str:
        return f"<CollectionItem {self.canonical_path} = {self.value!r}>"


def _root_label(value: Any) -> str:
    """The leading segment of a location: the resource or datatype name."""
    if isinstance(value, Mapping):
        return str(value.get("resourceType", ""))
    declared = getattr(type(value), "_type", None) or getattr(value, "_type", None)
    if isinstance(declared, str):
        return declared
    return ""
