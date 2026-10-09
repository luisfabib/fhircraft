"""The currency of the FHIRPath engine: values, where they came from, and where they could go."""

from __future__ import annotations

import operator
from dataclasses import dataclass, field
from typing import Any, Iterable, Self, SupportsIndex

from fhircraft.exceptions import FHIRPathEvaluationError
from fhircraft.fhir.path.accessors import (
    ElementAccessor,
    _root_label,
    resolve_field,
)
from fhircraft.utils import ensure_list

__all__ = [
    "FHIRPathCollectionItem",
    "FHIRPathCollection",
    "Collection",
]

#: A plain collection of FHIRPath result values.
Collection = list


@dataclass(slots=True, eq=False)
class FHIRPathCollectionItem:
    """One item of a FHIRPath collection: a value plus a record of its origin.

    Attributes:
        value: The item's value.
        accessor: The location the value was read from, or ``None`` for
            literals, environment variables and other parentless values.  The
            item itself is read-only; mutate through the accessor or the
            enclosing `FHIRPathCollection`.
    """

    value: Any
    accessor: ElementAccessor | None = field(default=None, repr=False)

    @classmethod
    def wrap(cls, data: Any) -> "FHIRPathCollectionItem":
        """Wrap *data* as a parentless item, passing existing items through."""
        return data if isinstance(data, cls) else cls(data)

    @classmethod
    def wrap_all(cls, data: Any) -> list["FHIRPathCollectionItem"]:
        """Wrap *data* -- scalar or iterable -- as a collection."""
        return [cls.wrap(item) for item in ensure_list(data) if item is not None]

    @property
    def canonical_path(self) -> str:
        """Canonical, index-qualified FHIRPath to this item, e.g. ``'Patient.name[0].given[1]'``.

        Items without an accessor are labelled by their own resource/datatype name.
        """
        if self.accessor is not None:
            return self.accessor.canonical_path
        return _root_label(self.value)

    def has_element(self, name: str) -> bool:
        """Whether this item's value declares the FHIRPath element *name*."""
        return resolve_field(self.value, name) is not None

    def __eq__(self, other: Any) -> bool:
        """Compare by value.

        Items compare equal to bare values so that FHIRPath's own equality
        operators can work on collections without unwrapping first.
        """
        if isinstance(other, FHIRPathCollectionItem):
            return self.value == other.value
        return self.value == other

    def __hash__(self) -> int:
        try:
            return hash(self.value)
        except TypeError:
            return hash(repr(self.value))

    def __repr__(self) -> str:
        return f"<CollectionItem {self.canonical_path} = {self.value!r}>"


class FHIRPathCollection(list[Any]):
    """A list of result values with private provenance and writable locations.

    Iteration and indexing expose values; ``_items`` keeps the corresponding
    accessor records for engine operations. ``targets`` outlive the values:
    ``Patient.name[0].given[2]`` on an empty resource can still carry the
    accessor where a value could be added.
    """

    def __init__(
        self,
        items: Iterable[Any] = (),
        *,
        targets: Iterable[ElementAccessor] | None = None,
    ) -> None:
        wrapped_items = tuple(FHIRPathCollectionItem.wrap(item) for item in items)
        super().__init__(item.value for item in wrapped_items)
        self._items = wrapped_items
        self._targets = None if targets is None else tuple(targets)

    # -------------------------------------------------
    # Collection Utilities
    # -------------------------------------------------

    def first(self) -> Any:
        """Return the first item in the collection, or None if the collection is empty."""
        return self[0] if self._items else None

    def last(self) -> Any:
        """Return the last item in the collection, or None if the collection is empty."""
        return self[-1] if self._items else None

    def single(self) -> Any:
        """Return the single item in the collection, or None if the collection is empty.

        Raises:
            ValueError: If the collection contains more than one item.
        """
        if not self._items:
            return None
        if len(self._items) > 1:
            raise ValueError("Collection contains more than one item")
        return self[0]

    @property
    def accessors(self) -> tuple[ElementAccessor, ...]:
        """Accessors of the existing items, in order."""
        return tuple(i.accessor for i in self._items if i.accessor is not None)

    @property
    def targets(self) -> tuple[ElementAccessor, ...]:
        """Writable locations addressed by the expression, whether or not they hold a value."""
        return self.accessors if self._targets is None else self._targets

    # -------------------------------------------------
    # List overrides
    # -------------------------------------------------

    def __getitem__(self, index) -> Any:
        if isinstance(index, slice):
            return type(self)(self._items[index], targets=self._targets)
        return list.__getitem__(self, index)

    def __setitem__(self, index, value) -> None:
        if isinstance(index, slice):
            values = tuple(FHIRPathCollectionItem.wrap(item) for item in value)
            old_items = self._items
            selected = range(*index.indices(len(old_items)))
            old_selected = tuple(old_items[item_index] for item_index in selected)
            list.__setitem__(self, index, [item.value for item in values])
            if len(old_selected) == len(values):
                values = tuple(
                    FHIRPathCollectionItem(item.value, old.accessor)
                    for old, item in zip(old_selected, values)
                )
            if index.step in (None, 1):
                start, stop, _ = index.indices(len(old_items))
                self._items = old_items[:start] + values + old_items[stop:]
            else:
                self._items = self._replace_sliced_items(index, values)
            return

        index = operator.index(index)
        item_index = index if index >= 0 else len(self._items) + index
        if not 0 <= item_index < len(self._items):
            raise IndexError("list assignment index out of range")
        items = list(self._items)
        old_item = items[item_index]
        item = FHIRPathCollectionItem.wrap(value)
        list.__setitem__(self, index, item.value)
        items[item_index] = FHIRPathCollectionItem(item.value, old_item.accessor)
        self._items = tuple(items)

    def _replace_sliced_items(
        self, index: slice, replacement: tuple[FHIRPathCollectionItem, ...]
    ) -> tuple[FHIRPathCollectionItem, ...]:
        items = list(self._items)
        selected = range(*index.indices(len(items)))
        for item_index, item in zip(selected, replacement):
            items[item_index] = item
        return tuple(items)

    def __delitem__(self, index) -> None:
        list.__delitem__(self, index)
        items = list(self._items)
        del items[index]
        self._items = tuple(items)

    def append(self, value: Any) -> None:
        item = FHIRPathCollectionItem.wrap(value)
        list.append(self, item.value)
        self._items += (item,)

    def extend(self, values: Iterable[Any]) -> None:
        if isinstance(values, FHIRPathCollection):
            self._targets = tuple(
                list(self._targets or [])
                + [target for target in (values._targets or [])]
            )
            values = [item.value for item in values._items]
        items = tuple(FHIRPathCollectionItem.wrap(value) for value in values)
        list.extend(self, (item.value for item in items))
        self._items += items

    def insert(self, index: SupportsIndex, value: Any) -> None:
        index = operator.index(index)
        item = FHIRPathCollectionItem.wrap(value)
        list.insert(self, index, item.value)
        items = list(self._items)
        items.insert(index, item)
        self._items = tuple(items)

    def pop(self, index: SupportsIndex = -1) -> Any:
        index = operator.index(index)
        value = list.pop(self, index)
        items = list(self._items)
        items.pop(index)
        self._items = tuple(items)
        return value

    def remove(self, value: Any) -> None:
        del self[self.index(value)]

    def clear(self) -> None:
        list.clear(self)
        self._items = ()

    def reverse(self) -> None:
        list.reverse(self)
        self._items = tuple(reversed(self._items))

    def sort(self, *, key=None, reverse: bool = False) -> None:
        sorted_items = sorted(
            zip(self, self._items),
            key=(
                (lambda pair: key(pair[0])) if key is not None else lambda pair: pair[0]
            ),
            reverse=reverse,
        )
        list.__setitem__(self, slice(None), [value for value, _ in sorted_items])
        self._items = tuple(item for _, item in sorted_items)

    def __iadd__(self, values: Iterable[Any]) -> Self:
        self.extend(values)
        return self

    def __imul__(self, count: SupportsIndex) -> Self:
        multiplier = operator.index(count)
        list.__imul__(self, multiplier)
        self._items *= max(0, multiplier)
        return self

    def __eq__(self, value: object) -> bool:
        if isinstance(value, list):
            return list(self) == list(value)
        return super().__eq__(value)

    # ------------------------------------------------------------------
    # Patch interface
    # ------------------------------------------------------------------

    def _require_targets(self) -> tuple[ElementAccessor, ...]:
        targets = self.targets
        if not targets:
            raise FHIRPathEvaluationError(
                "The expression does not address a writable location: literals, "
                "environment variables and root resources cannot be modified"
            )
        return targets

    def set(self, value: Any) -> None:
        """Assign *value* at every addressed location."""
        for target in self._require_targets():
            target.set(value)

    def add(self, value: Any) -> None:
        """Append *value* to the list element (or assign the single-valued one)."""
        for target in self._require_targets():
            target = target.at(None)
            if not target.is_list:
                target.set(value)
                continue
            current = target.get()
            target.insert(value, len(current) if isinstance(current, list) else 0)

    def insert_at(self, value: Any, at: Any) -> None:
        """Insert *value* at position *at* of the addressed FHIR list element."""
        for target in self._require_targets():
            target.at(None).insert(value, at)

    def delete(self) -> None:
        """Remove every item of the collection from its container."""
        self._require_targets()
        for accessor in reversed(self.accessors):
            accessor.delete()

    def move(self, source: int, destination: int) -> None:
        """Reorder the addressed list element, moving *source* to *destination*."""
        for target in self._require_targets():
            target.at(None).move(source, destination)

    def snapshot(self) -> list[tuple[ElementAccessor, Any]]:
        """Deep copy of the addressed fields, for rollback."""
        return [(t.at(None), t.at(None).snapshot()) for t in self._require_targets()]

    def restore(self, snapshot: list[tuple[ElementAccessor, Any]]) -> None:
        """Undo every mutation made since *snapshot*."""
        for accessor, saved in snapshot:
            accessor.restore(saved)

    def __repr__(self) -> str:
        return f"FHIRPathCollection({list(self._items)!r}, targets={len(self.targets)})"
