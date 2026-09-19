"""Read/write access to a single element slot of a single container."""

from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from collections.abc import Mapping, MutableMapping
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic.fields import FieldInfo

from fhircraft.exceptions import FHIRPathEvaluationError
from fhircraft.utils import contains_list_type, ensure_list, get_fhir_model_from_field

if TYPE_CHECKING:  # pragma: no cover
    from fhircraft.fhir.path.collection import FHIRPathCollectionItem

__all__ = [
    "ElementAccessor",
    "ModelAccessor",
    "DictAccessor",
    "resolve_field",
    "Cardinality",
]


# --------------------------------------------------------------------------- #
# Field-name resolution
# --------------------------------------------------------------------------- #

#: Suffixes tried, in order, when mapping a FHIRPath element name onto an actual
#: model attribute.  Mirrors the fallback chain in ``Element.evaluate``:
#: ``value`` -> ``value_`` (shadowed builtins / reserved words) -> ``value_ext``
#: (primitive extensions, the ``_value`` sibling in the JSON representation).
FIELD_PREFIXES: tuple[str, ...] = ("", "_")


def resolve_field(container: Any, element: str) -> str | None:
    """Map a FHIRPath element name onto a concrete attribute/key on *container*.

    Returns ``None`` when the container has no such element.  Models that
    declare ``extra='allow'`` accept any name and therefore always resolve.
    """
    if container is None:
        return None

    if isinstance(container, Mapping):
        for prefix in FIELD_PREFIXES:
            candidate = f"{prefix}{element}"
            if candidate in container:
                return candidate
        # A mapping is open by construction: an absent key is still writable.
        return element

    model_fields = getattr(type(container), "model_fields", None)
    if model_fields is None:
        for prefix in FIELD_PREFIXES:
            candidate = f"{prefix}{element}"
            if hasattr(container, candidate):
                return candidate
        return None

    for prefix in FIELD_PREFIXES:
        candidate = f"{prefix}{element}"
        if candidate in model_fields:
            return candidate

    # Check for properties defined on the model class itself
    for prefix in FIELD_PREFIXES:
        candidate = f"{prefix}{element}"
        if hasattr(type(container), candidate):
            return candidate

    # Aliases (FHIR JSON names that are not valid Python identifiers).
    for name, info in model_fields.items():
        if info.alias == element or info.serialization_alias == element:
            return name

    if _allows_extra(type(container)):
        return element

    return None


def _allows_extra(model_cls: type) -> bool:
    config = getattr(model_cls, "model_config", None)
    if config is None:
        return False
    extra = (
        config.get("extra")
        if isinstance(config, dict)
        else getattr(config, "extra", None)
    )
    return extra == "allow"


# --------------------------------------------------------------------------- #
# Cardinality
# --------------------------------------------------------------------------- #


class Cardinality(tuple):
    """``(min, max)`` where ``max`` is ``None`` for ``*``.

    A tuple subclass so it compares and unpacks like one, but prints as FHIR
    cardinality notation in error messages.
    """

    __slots__ = ()

    def __new__(cls, minimum: int, maximum: int | None) -> "Cardinality":
        return super().__new__(cls, (minimum, maximum))

    @property
    def min(self) -> int:
        """Minimum cardinality."""
        return self[0]

    @property
    def max(self) -> int | None:
        """Maximum cardinality, or ``None`` for unbounded."""
        return self[1]

    @property
    def is_collection(self) -> bool:
        """Whether this element represents a collection (maximum cardinality > 1 or unbounded)."""
        return self.max is None or self.max > 1

    @property
    def is_required(self) -> bool:
        """Whether this element is required (minimum cardinality > 0)."""
        return self.min > 0

    def __str__(self) -> str:
        return f"{self.min}..{'*' if self.max is None else self.max}"

    def __repr__(self) -> str:
        return f"Cardinality({self.min}, {self.max})"


# --------------------------------------------------------------------------- #
# Accessors
# --------------------------------------------------------------------------- #


class ElementAccessor(ABC):
    """Read/write handle onto one element slot of one container.

    Subclasses implement only the four raw primitives -- ``_read_field``,
    ``_write_field``, ``_remove_field``, ``_field_info`` -- and inherit the
    list/scalar bookkeeping, which is identical for models and mappings.
    """

    __slots__ = ("container", "element", "field", "index", "_is_list")

    #: Human-readable kind, used in error messages.
    kind: ClassVar[str] = "element"

    def __init__(
        self,
        container: Any,
        element: str,
        field: str,
        index: int | None = None,
        is_list: bool | None = None,
    ) -> None:
        self.container = container
        self.element = element
        self.field = field
        self.index = index
        self._is_list = is_list

    # -- construction ------------------------------------------------------ #

    @classmethod
    def for_item(cls, item: "FHIRPathCollectionItem") -> "ElementAccessor | None":
        """Build the accessor for *item*, or ``None`` if it is not writable.

        Literals, environment variables and root items have no parent container
        and therefore no accessor.
        """
        if item.parent is None or item.element is None:
            return None

        container = item.parent.value
        if container is None:
            return None
        if isinstance(container, list):
            # A parent collection item should never hold a bare list -- the
            # engine unwraps lists into sibling items.  Guard rather than
            # silently writing to element zero.
            raise FHIRPathEvaluationError(
                f"Cannot resolve a writable location for '{item.element}': "
                "its parent is an unwrapped list"
            )

        field = resolve_field(container, item.element)
        if field is None:
            return None

        if isinstance(container, Mapping):
            return DictAccessor(container, item.element, field, item.index)
        # `resolve_field` already proved `field` is reachable via `hasattr` for
        # containers without `model_fields`/`__dict__` (e.g. namedtuples).
        if (
            hasattr(type(container), "model_fields")
            or hasattr(container, "__dict__")
            or hasattr(container, field)
        ):
            return ModelAccessor(container, item.element, field, item.index)
        return None

    # -- raw primitives (subclass responsibility) -------------------------- #

    @abstractmethod
    def _read_field(self) -> Any:
        """Return the whole field value (the list itself, for list fields)."""

    @abstractmethod
    def _write_field(self, value: Any) -> None:
        """Replace the whole field value."""

    @abstractmethod
    def _remove_field(self) -> None:
        """Unset the field entirely."""

    @abstractmethod
    def _field_info(self) -> FieldInfo | None:
        """Pydantic field metadata, or ``None`` for untyped containers."""

    @property
    def field_info(self) -> FieldInfo | None:
        return self._field_info()

    @property
    def is_list(self) -> bool:
        """Whether the *field* is list-valued (independent of its current value)."""
        if self._is_list is None:
            info = self.field_info
            if info is not None:
                self._is_list = contains_list_type(info.annotation)
            else:
                self._is_list = isinstance(self._read_field(), list)
        return self._is_list

    @property
    def cardinality(self) -> Cardinality:
        """Best-effort cardinality from a Pydantic ``FieldInfo``."""

        if self.field_info is None:
            return Cardinality(0, None if self.is_list else 1)

        minimum = 1 if self.field_info.is_required() else 0
        maximum: int | None = None if self.is_list else 1

        for constraint in self.field_info.metadata or ():
            min_len = getattr(constraint, "min_length", None)
            max_len = getattr(constraint, "max_length", None)
            if min_len is not None:
                minimum = max(minimum, int(min_len))
            if max_len is not None:
                maximum = (
                    int(max_len) if maximum is None else min(maximum, int(max_len))
                )

        return Cardinality(minimum, maximum)

    @property
    def fhir_type(self) -> str | None:
        """FHIR type name the slot expects, e.g. ``'HumanName'`` or ``'string'``."""
        info = self.field_info
        if info is None:
            return None
        model = get_fhir_model_from_field(info)
        return getattr(model, "_type", None) if model is not None else None

    def exists(self) -> bool:
        """Whether the slot currently holds a value."""
        current = self._read_field()
        if self.index is None:
            return current is not None
        return isinstance(current, list) and 0 <= self.index < len(current)

    def construct(self) -> Any:
        """Instantiate the empty model this slot expects (the ``create=True`` path).

        Returns ``None`` for primitive slots, which need no container object.
        """
        info = self.field_info
        if info is None:
            return None
        model = get_fhir_model_from_field(info)
        if model is None:
            return None
        return model.model_construct()

    # -- read -------------------------------------------------------------- #

    def get(self) -> Any:
        """Return the value at this slot."""
        current = self._read_field()
        if self.index is None:
            return current
        if not isinstance(current, list):
            return current if self.index == 0 else None
        if 0 <= self.index < len(current):
            return current[self.index]
        return None

    def snapshot(self) -> Any:
        """Deep copy of the whole field, for transactional rollback."""
        return copy.deepcopy(self._read_field())

    def restore(self, snapshot: Any) -> None:
        """Undo every mutation since *snapshot* was taken."""
        self._write_field(snapshot)

    # -- write ------------------------------------------------------------- #

    def set(self, value: Any) -> None:
        """Assign *value* to this slot.

        Scalar slot, list value: accepted only when the list has at most one
        element -- silently dropping the rest would hide a cardinality bug.
        List field addressed without an index: replaces the whole list.
        """
        current = self._read_field()

        if self.index is None:
            if not self.is_list and isinstance(value, list):
                if len(value) > 1:
                    raise FHIRPathEvaluationError(
                        f"Cannot assign {len(value)} values to single-valued "
                        f"element '{self.element}' (cardinality {self.cardinality})"
                    )
                value = value[0] if value else None
            elif self.is_list and value is not None and not isinstance(value, list):
                value = [value]
            self._write_field(value)
            return

        if not isinstance(current, list):
            # Indexed write into a slot that is not yet a list.
            if self.is_list:
                self._write_field(_pad(list(), self.index, value))
            elif self.index == 0:
                self._write_field(value)
            else:
                raise FHIRPathEvaluationError(
                    f"Cannot write index [{self.index}] of single-valued "
                    f"element '{self.element}'"
                )
            return

        if self.index < len(current):
            current[self.index] = value
        else:
            _pad(current, self.index, value)

    def delete(self) -> None:
        """Remove the value at this slot.

        Removing the last entry of a list unsets the field rather than leaving
        an empty array behind, which FHIR forbids in the JSON representation.
        """
        current = self._read_field()

        if self.index is None or not isinstance(current, list):
            self._remove_field()
            return

        if not 0 <= self.index < len(current):
            raise FHIRPathEvaluationError(
                f"Cannot delete index [{self.index}] of '{self.element}': "
                f"list has {len(current)} entries"
            )
        del current[self.index]
        if not current:
            self._remove_field()

    def insert(self, value: Any, at: int) -> None:
        """Insert *value* into the list at position *at*.

        *at* may equal the current length (append).  Negative indices are
        rejected: FHIRPatch indices are absolute.
        """
        if not self.is_list:
            raise FHIRPathEvaluationError(
                f"Cannot insert into single-valued element '{self.element}' "
                f"(cardinality {self.cardinality})"
            )
        if at < 0:
            raise FHIRPathEvaluationError(
                f"Insert index must be non-negative, got {at}"
            )

        current = self._read_field()
        if not isinstance(current, list):
            current = ensure_list(current) if current is not None else []
            self._write_field(current)
            current = self._read_field()

        if at > len(current):
            raise FHIRPathEvaluationError(
                f"Cannot insert at index [{at}] of '{self.element}': "
                f"list has {len(current)} entries"
            )
        current.insert(at, value)

    def move(self, source: int, destination: int) -> None:
        """Move the entry at *source* to *destination*, shifting the rest.

        Indices are interpreted against the list *before* the move, matching
        the FHIRPatch ``move`` semantics.
        """
        if not self.is_list:
            raise FHIRPathEvaluationError(
                f"Cannot reorder single-valued element '{self.element}'"
            )
        current = self._read_field()
        if not isinstance(current, list):
            raise FHIRPathEvaluationError(
                f"Cannot reorder '{self.element}': no list present"
            )
        size = len(current)
        for name, idx in (("source", source), ("destination", destination)):
            if not 0 <= idx < size:
                raise FHIRPathEvaluationError(
                    f"Move {name} index [{idx}] is out of range for "
                    f"'{self.element}' ({size} entries)"
                )
        if source == destination:
            return
        current.insert(destination, current.pop(source))

    # -- dunders ----------------------------------------------------------- #

    def __repr__(self) -> str:
        suffix = "" if self.index is None else f"[{self.index}]"
        return (
            f"{type(self).__name__}("
            f"{type(self.container).__name__}.{self.field}{suffix})"
        )


def _pad(target: list, index: int, value: Any) -> list:
    """Extend *target* with ``None`` up to *index*, then place *value* there."""
    target.extend([None] * (index - len(target)))
    target.append(value)
    return target


class ModelAccessor(ElementAccessor):
    """Accessor for Pydantic FHIR models."""

    __slots__ = ()
    kind = "field"

    def _read_field(self) -> Any:
        return getattr(self.container, self.field, None)

    def _write_field(self, value: Any) -> None:
        try:
            setattr(self.container, self.field, value)
        except Exception as exc:  # pydantic ValidationError, AttributeError, ...
            raise FHIRPathEvaluationError(
                f"Cannot assign to '{type(self.container).__name__}."
                f"{self.field}': {exc}"
            ) from exc

    def _remove_field(self) -> None:
        info = self._field_info()
        if (
            info is None
            and self.field in getattr(self.container, "__pydantic_extra__", {})
            or {}
        ):
            del self.container.__pydantic_extra__[self.field]
            return
        if info is not None and info.is_required():
            raise FHIRPathEvaluationError(
                f"Cannot delete required element '{self.element}' "
                f"(cardinality {self.cardinality})"
            )
        self._write_field(None)

    def _field_info(self) -> FieldInfo | None:
        return getattr(type(self.container), "model_fields", {}).get(self.field)


class DictAccessor(ElementAccessor):
    """Accessor for plain mappings -- raw JSON and non-FHIR data.

    Untyped, so ``is_list`` and ``cardinality`` are inferred from the value
    that happens to be present.
    """

    __slots__ = ()
    kind = "key"

    def _read_field(self) -> Any:
        return self.container.get(self.field)

    def _write_field(self, value: Any) -> None:
        if not isinstance(self.container, MutableMapping):
            raise FHIRPathEvaluationError(
                f"Cannot assign to key '{self.field}' of an immutable mapping"
            )
        self.container[self.field] = value

    def _remove_field(self) -> None:
        if not isinstance(self.container, MutableMapping):
            raise FHIRPathEvaluationError(
                f"Cannot delete key '{self.field}' of an immutable mapping"
            )
        self.container.pop(self.field, None)

    def _field_info(self) -> FieldInfo | None:
        return None
