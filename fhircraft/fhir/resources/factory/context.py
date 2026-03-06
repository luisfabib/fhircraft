"""
BuildContext and TypeRegistry — immutable configuration passed through the
factory pipeline.

``TypeRegistry`` resolves FHIR type codes and canonical URLs to Python types.
``BuildContext`` is the frozen context container passed to every builder,
assembler, and validator collector.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from fhircraft.fhir.resources.factory.profile_factory import FHIRStructureFactory
    from fhircraft.fhir.resources.repository import (
        CompositeStructureDefinitionRepository,
    )


@dataclass(frozen=True)
class BuildContext:
    """
    Immutable context container passed through the entire factory pipeline.

    Attributes:
        fhir_release: FHIR release short-name (``"R4"``, ``"R4B"``, ``"R5"``).
        fhir_version: Full FHIR version string (e.g. ``"4.3.0"``).
        registry: The :class:`TypeRegistry` for this build session.
        repository: The ``StructureDefinition`` repository for resolving
            references and looking up base definitions.
    """

    fhir_release: str
    fhir_version: str
    base: type
    factory: FHIRStructureFactory
    repository: "CompositeStructureDefinitionRepository"
