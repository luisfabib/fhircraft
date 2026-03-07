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
    from fhircraft.fhir.resources.factory.core import FHIRStructureFactory
    from fhircraft.fhir.resources.definitions.registry import (
        StructureDefinitionRegistry,
    )


@dataclass(frozen=True)
class BuildContext:
    """
    Immutable context container passed through the entire factory pipeline.
    """

    fhir_release: str
    """ FHIR release version (e.g. 'R4', 'STU3', 'R5'). """

    fhir_version: str
    """ Full FHIR version string (e.g. '4.3.0'). """

    base: type
    """ The base model class for this build session. """

    resource_name: str
    """ The resource name for this build session. """

    factory: FHIRStructureFactory
    """ The FHIR structure factory for this build session. """

    registry: "StructureDefinitionRegistry"
    """ The structure definition registry for resolving references and looking up base definitions. """
