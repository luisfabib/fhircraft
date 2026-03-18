"""
Module defining the BuildContext dataclass, which serves as an immutable container for contextual information during the FHIR structure building process in the factory pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from fhircraft.fhir.resources.factory.core import FHIRModelFactory
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

    factory: FHIRModelFactory
    """ The FHIR structure factory for this build session. """

    registry: "StructureDefinitionRegistry"
    """ The structure definition registry for resolving references and looking up base definitions. """
