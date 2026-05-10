from fhircraft.fhir.resources.base.model import FHIRBaseModel


class FHIRList(list):
    """
    Custom list wrapper that maintains parent context on mutations.

    This list automatically propagates _parent, _root_resource, _resource, and _index context
    to FHIRBaseModel items when they are added via append, extend, insert, or __setitem__.
    """

    def __init__(self, items=None, parent=None, root=None, resource=None):
        """Initialize FHIRList with items and context.

        ``root`` and ``resource`` are accepted for backwards-compatibility but
        are no longer stored; they are resolved lazily via ``_parent`` on items.
        """
        super().__init__(items or [])
        self._parent = parent
        self._propagate_context()

    def _propagate_context(self):
        """Set _parent and _index on all current FHIRBaseModel items."""
        if self._parent is None:
            return

        for index, item in enumerate(self):
            if isinstance(item, FHIRBaseModel):
                object.__setattr__(item, "_parent", self._parent)
                object.__setattr__(item, "_index", index)

    def append(self, item):
        """Append item and propagate context."""
        super().append(item)
        if isinstance(item, FHIRBaseModel):
            object.__setattr__(item, "_parent", self._parent)
            object.__setattr__(item, "_index", len(self) - 1)

    def extend(self, items):
        """Extend list and propagate context to new items."""
        start_index = len(self)
        super().extend(items)
        for offset, item in enumerate(items):
            if isinstance(item, FHIRBaseModel):
                object.__setattr__(item, "_parent", self._parent)
                object.__setattr__(item, "_index", start_index + offset)

    def insert(self, index, item):
        """Insert item and propagate context."""
        super().insert(index, item)
        if isinstance(item, FHIRBaseModel):
            object.__setattr__(item, "_parent", self._parent)
            object.__setattr__(item, "_index", index)
        # Re-index all items after insertion point
        for i in range(index + 1, len(self)):
            if isinstance(self[i], FHIRBaseModel):
                object.__setattr__(self[i], "_index", i)

    def __setitem__(self, index, item):
        """Set item and propagate context."""
        super().__setitem__(index, item)
        if isinstance(item, FHIRBaseModel):
            if isinstance(index, int):
                object.__setattr__(item, "_parent", self._parent)
                object.__setattr__(item, "_index", index)
            else:
                # Slice assignment – re-propagate to fix indices.
                self._propagate_context()
        elif isinstance(item, list):
            # Slice assignment with a plain list – re-propagate to fix indices.
            self._propagate_context()
