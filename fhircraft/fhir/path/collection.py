"""The currency of the FHIRPath engine: values, where they came from, and where they could go."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from fhircraft.exceptions import FHIRPathEvaluationError
from fhircraft.fhir.path.accessors import (
    ElementAccessor,
    _root_label,
    resolve_field,
)
from fhircraft.utils import ensure_list

__all__ = ["FHIRPathCollectionItem", "FHIRPathCollection", "Collection"]

#: A FHIRPath collection is just an ordered list of items.
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


class FHIRPathCollection(list[FHIRPathCollectionItem]):
    """A list of items plus the writable locations the expression addressed.

    ``targets`` outlive the items: ``Patient.name[0].given[2]`` on an empty
    resource yields no items but still carries the accessor where a value
    could be added.  When not given explicitly, targets are the accessors of
    the items, so any plain list of items behaves like a collection.
    """

    def __init__(
        self,
        items: Iterable[FHIRPathCollectionItem] = (),
        *,
        targets: Iterable[ElementAccessor] | None = None,
    ) -> None:
        super().__init__(items)
        self._targets = None if targets is None else tuple(targets)

    @property
    def accessors(self) -> tuple[ElementAccessor, ...]:
        """Accessors of the existing items, in order."""
        return tuple(i.accessor for i in self if i.accessor is not None)

    @property
    def targets(self) -> tuple[ElementAccessor, ...]:
        """Writable locations addressed by the expression, whether or not they hold a value."""
        return self.accessors if self._targets is None else self._targets

    def __getitem__(self, index) -> Any:
        if isinstance(index, slice):
            return type(self)(list.__getitem__(self, index))
        return list.__getitem__(self, index)

    # ------------------------------------------------------------------ #
    # Patch interface
    # ------------------------------------------------------------------ #

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

    def insert(self, value: Any, at: Any) -> None:
        """Insert *value* at position *at* of the addressed list element."""
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
        return f"FHIRPathCollection({list(self)!r}, targets={len(self.targets)})"
