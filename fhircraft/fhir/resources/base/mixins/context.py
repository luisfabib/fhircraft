"""
Parent-context tracking mixin for FHIRBaseModel.

Provides the _parent / _index attributes and the lazy properties that
walk up the parent chain to locate containing resources.
"""

from typing import Any, Union


class FHIRContextMixin:
    """
    Mixin that provides hierarchical parent-context tracking.

    Every FHIR model instance stores a reference to its direct parent
    (_parent) and its position within a list (_index).  The root resource
    and nearest enclosing resource are resolved lazily by walking the
    parent chain, avoiding the need to store and update those references.
    """

    _parent: "Union[FHIRContextMixin, None]" = None
    _index: "Union[int, None]" = None

    @property
    def _root_resource(self) -> "FHIRContextMixin":
        """Walk up the _parent chain and return the topmost node."""
        node = self
        while node._parent is not None:
            node = node._parent
        return node  # type: ignore[return-value]

    @property
    def _resource(self) -> "Union[FHIRContextMixin, None]":
        """Walk up the _parent chain and return the nearest enclosing resource/logical node."""
        node: Any = self
        while node is not None:
            if node._is_resource():
                return node
            node = node._parent
        return None

    @classmethod
    def _is_resource(cls) -> bool:
        """Return True if this class represents a FHIR resource or logical model."""
        kind = getattr(cls, "_kind", None)
        if kind is None:
            return False
        kind_value = kind.value if hasattr(kind, "value") else str(kind)
        return kind_value in ("resource", "logical")

    def _set_resource_context(
        self,
        parent: "Union[FHIRContextMixin, None]" = None,
        index: Union[int, None] = None,
    ) -> None:
        """
        Set parent and index context for this instance, then propagate to direct children.

        Only _parent and _index are stored; _root_resource and _resource are
        resolved lazily by walking _parent.

        Args:
            parent: The parent FHIRContextMixin instance (if this is a nested field).
            index:  The position of this instance within a parent list (if applicable).
        """
        object.__setattr__(self, "_parent", parent)
        object.__setattr__(self, "_index", index)

        for field_name in type(self).model_fields:  # type: ignore[arg-type]
            value = getattr(self, field_name, None)
            if value is not None:
                self._propagate_context_to_value(value)

    def _propagate_context_to_value(self, value: Any) -> None:
        """
        Propagate parent context to a direct child field value.

        Wraps plain lists in FHIRList so future mutations are also tracked.
        Only _parent and _index are written; deeper descendants resolve their
        own context lazily once their own _parent is set.

        Args:
            value: The field value (FHIRBaseModel, list, or other).
        """
        from fhircraft.fhir.resources.base import FHIRList

        if isinstance(value, FHIRContextMixin):
            object.__setattr__(value, "_parent", self)
            object.__setattr__(value, "_index", None)
        elif isinstance(value, list):
            if not isinstance(value, FHIRList):
                # Wrap plain list in FHIRList to track future mutations.
                fhir_list = FHIRList(value, parent=self)
                for field_name in type(self).model_fields:  # type: ignore[arg-type]
                    if getattr(self, field_name, None) is value:
                        object.__setattr__(self, field_name, fhir_list)
                        break
            else:
                # Re-point existing FHIRList at the current parent.
                value._parent = self
                value._propagate_context()
