"""
ElementNode — a frozen, computed-property wrapper around a single FHIR ElementDefinition.

Every component of the factory pipeline receives ``ElementNode`` objects rather
than raw ``ElementDefinition`` objects.  All properties are derived purely from
the definition's own fields; no external state is required.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, Sequence

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4.complex.element_definition import (
        ElementDefinition as R4ElementDefinition,
        ElementDefinitionType as R4ElementDefinitionType,
    )
    from fhircraft.fhir.resources.datatypes.R4B.complex.element_definition import (
        ElementDefinition as R4BElementDefinition,
        ElementDefinitionType as R4BElementDefinitionType,
    )
    from fhircraft.fhir.resources.datatypes.R5.complex.element_definition import (
        ElementDefinition as R5ElementDefinition,
        ElementDefinitionType as R5ElementDefinitionType,
    )

POLYMORPHIC_PATH_SUFFIX = "[x]"
BACKBONE_CODES = frozenset({"BackboneElement", "Element"})

FHIR_TYPE_PREFIX = "http://hl7.org/fhir/StructureDefinition/"
FHIRPATH_TYPE_PREFIX = "http://hl7.org/fhirpath/System."


@dataclass(frozen=True, slots=True)
class ElementNode:
    """
    Immutable wrapper around a FHIR ElementDefinition that exposes a rich set
    of computed properties used throughout the factory pipeline.

    Attributes:
        definition: The raw FHIR ElementDefinition (R4, R4B, or R5 variant).
    """

    definition: "R4ElementDefinition | R4BElementDefinition | R5ElementDefinition"

    # ------------------------------------------------------------------
    # Identity & position
    # ------------------------------------------------------------------

    @property
    def id(self) -> str:
        """Full element id (dot-separated, slices encoded with colon)."""
        return self.definition.id or ""

    @property
    def id_segments(self) -> list[str]:
        """
        List of segments of `id`.
        """
        return re.split(r"[\.\:]", self.id) if self.id else []

    @property
    def id_ancestry(self) -> list[str]:
        """
        List of ancestor ids of `id`.
        """
        segments_with_separators = re.split(r"([\.\:])", self.id)
        return [
            "".join(segments_with_separators[: (2 * i + 1)])
            for i in range(0, len(self.id_segments))
        ]

    @property
    def path(self) -> str:
        """Element path (dot-separated, no slice names)."""
        return self.definition.path or ""

    @property
    def depth(self) -> int:
        """Number of '.' separators in the id (root = 0)."""
        return self.path.count(".")

    @property
    def path_segments(self) -> list[str]:
        """
        List of segments of `path`.
        """
        return self.path.split(".") if self.path else []

    @property
    def path_ancestry(self) -> list[str]:
        """
        List of ancestor segments of `path`.
        """
        return [".".join(self.path_segments[: i + 1]) for i in range(0, self.depth + 1)]

    @property
    def name(self) -> str:
        """
        Official element name
        """
        name = self.path_segments[-1]
        if self.is_polymorphic_type:
            # The "[x]" is not considered to be part of the official element name, though it may frequently appear in documentation that way.
            return name.rstrip(POLYMORPHIC_PATH_SUFFIX)
        else:
            return name

    @property
    def local_id(self) -> str:
        """Leaf segment of *id* (may include ``:sliceName``)."""
        return self.id.rsplit(".", 1)[-1]

    @property
    def parent_id(self) -> str | None:
        """
        *id* with the last ``.segment`` removed.  ``None`` for root-level elements.

        Note: for a top-level slice like ``Observation.component:systolic`` the
        parent_id is ``"Observation"`` (not ``"Observation.component"``).  This is
        intentional — slices are accessed via :meth:`DefinitionIndex.slices`, never
        via :meth:`DefinitionIndex.children`.
        """
        if "." not in self.id:
            return None
        return self.id.rsplit(".", 1)[0]

    # ------------------------------------------------------------------
    # Structural flags
    # ------------------------------------------------------------------

    @property
    def is_root(self) -> bool:
        """
        Whether this element is a root element (has no parent).
        """
        return self.depth == 0

    @property
    def is_slice(self) -> bool:
        """
        True when this element *is* a named slice definition.

        A named slice has a colon in its :attr:`local_id`, e.g.
        ``Observation.component:systolic`` → ``local_id = "component:systolic"``.
        """
        return ":" in self.local_id

    @property
    def is_slice_entry(self) -> bool:
        """
        The first element that declares slicing is considered to be the slicing entry
        """
        return self.definition.slicing is not None

    @property
    def is_slice_child(self) -> bool:
        """True when *any* ancestor segment of the id contains ``:`` — this element lives
        inside a slice sub-tree."""
        return any(":" in seg for seg in self.id.split("."))

    @property
    def is_content_reference(self) -> bool:
        """True when ``definition.contentReference`` is set."""
        return self.definition.contentReference is True

    # ------------------------------------------------------------------
    # Slice identity
    # ------------------------------------------------------------------

    @property
    def slice_name(self) -> str | None:
        """
        The slice name (part after ``:`` in :attr:`local_id`), or ``None`` if this
        element is not itself a named slice.
        """
        if not self.is_slice:
            raise ValueError("Only slices have slice names")
        return self.definition.sliceName or self.local_id.split(":", 1)[1]

    @property
    def is_slicing_ordered(self) -> bool:
        """
        If elements must be in same order as slices
        """
        if not self.is_slice_entry:
            raise ValueError("Only slice entry elements have slicing rules")
        if slicing := self.definition.slicing:
            return slicing.ordered is True
        return False

    @property
    def slicing_rules(self) -> Literal["openAtEnd", "open", "closed"]:
        """
        The slicing rules for this slice entry element, one of ``"openAtEnd"``, ``"open"``, or ``"closed"``.  Defaults to ``"open"`` when not specified.
        """
        if (slicing := self.definition.slicing) and (rules := slicing.rules):
            if rules not in (
                "open",
                "closed",
                "openAtEnd",
            ):
                raise ValueError("Invalid slicing rules: {}".format(slicing.rules))
            return rules
        return "open"

    @property
    def slice_ancestry(self) -> list[str]:
        """
        Names of all ancestor slices in outermost-first order.
        """
        names: list[str] = []
        for seg in self.id.split("."):
            if ":" in seg:
                names.append(seg.split(":", 1)[1])
        return names

    # ------------------------------------------------------------------
    # Cardinality
    # ------------------------------------------------------------------

    @property
    def min_cardinality(self) -> int:
        """
        Minimum cardinality (defaults to 0 when not specified).
        """
        if (val := self.definition.min) is None:
            raise ValueError(
                "ElementDefinition.min is required and must be an integer."
            )
        return int(val)

    @property
    def max_cardinality(self) -> int | None:
        """Maximum cardinality.  ``None`` means unbounded (``*``)."""
        if (val := getattr(self.definition, "max", None)) is None:
            raise ValueError(
                "ElementDefinition.max is required and must be an integer or valid string."
            )
        s = str(val)
        if s == "*":
            return None
        try:
            return int(s)
        except (ValueError, TypeError):
            raise ValueError("ElementDefinition.max must be an integer or '*'.")

    @property
    def is_required(self) -> bool:
        """True when ``min_cardinality >= 1``."""
        return self.min_cardinality >= 1

    @property
    def is_prohibited(self) -> bool:
        """True when ``max == "0"``."""
        return self.max_cardinality == 0

    @property
    def is_array(self) -> bool:
        """
        Whether this element is multi-valued and represented as a list (``max`` > 1 or ``*``).
        """
        return (self.max_cardinality is None) or (self.max_cardinality > 1)

    # ------------------------------------------------------------------
    # Type helpers
    # ------------------------------------------------------------------

    @property
    def types(
        self,
    ) -> "Sequence[R4ElementDefinitionType] | Sequence[R4BElementDefinitionType] | Sequence[R5ElementDefinitionType]":
        """List of FHIR type codes from ``definition.type``."""
        return self.definition.type or []

    @property
    def type_codes(self) -> list[str]:
        """List of FHIR type codes from ``definition.type``."""
        return [str(t.code) for t in self.types if t.code]

    @property
    def is_polymorphic_type(self) -> bool:
        """
        Whether the element is polymorphic (a.k.a type-choice).

        Note: If the element is polymorphic (has more than one datatype), then the end of the
        path for the element SHALL be "[x]" to designate that the name of the element may vary when serialized.
        """
        return self.path.endswith(POLYMORPHIC_PATH_SUFFIX) or len(self.type_codes) > 1

    @property
    def profile_urls(self) -> list[str]:
        """All profile canonical URLs collected from ``definition.type[*].profile``."""
        urls: list[str] = []
        for t in self.types:
            for p in getattr(t, "profile", None) or []:
                urls.append(str(p))
        return urls

    # ------------------------------------------------------------------
    # Documentation
    # ------------------------------------------------------------------

    @property
    def documentation(self) -> str:
        """
        Full combination of the elemments's `short`,  `definition`, and `comment` fields, in
        that order of preference.  Returns an empty string if none of those fields are set.
        """
        return "\n".join(
            filter(
                None,
                [
                    self.definition.short,
                    self.definition.definition,
                    self.definition.comment,
                ],
            )
        )

    # ------------------------------------------------------------------
    # Constraint values
    # ------------------------------------------------------------------

    @property
    def pattern(
        self,
    ):
        """
        The pattern[x] value for this element, if any.  Returns ``None`` if no pattern is specified.
        """
        return self.definition.pattern

    @property
    def fixed(
        self,
    ):
        """
        The fixed[x] value for this element, if any.  Returns ``None`` if no fixed is specified.
        """
        return self.definition.fixed

    @property
    def default_value(
        self,
    ):
        """
        The defaultValue[x] value for this element, if any.  Returns ``None`` if no default is specified.
        """
        return self.definition.defaultValue

    @property
    def min_value(
        self,
    ):
        """
        The minValue[x] value for this element, if any.  Returns ``None`` if no minValue is specified.
        """
        return self.definition.minValue

    @property
    def max_value(
        self,
    ):
        """
        The maxValue[x] value for this element, if any.  Returns ``None`` if no maxValue is specified.
        """
        return self.definition.maxValue

    @property
    def max_length(
        self,
    ):
        """
        The maxLength[x] value for this element, if any.  Returns ``None`` if no maxLength is specified.
        """
        return self.definition.maxLength

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"ElementNode(id={self.id!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ElementNode):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
