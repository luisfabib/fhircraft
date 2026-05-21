"""
FHIR Resource Factory — public API package.
"""

from __future__ import annotations

from fhircraft.fhir.resources.datatypes.registry import TypeRegistry
from fhircraft.fhir.resources.factory.assembler import ModelAssembler

from fhircraft.fhir.resources.factory.context import BuildContext
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.exceptions import (
    DefinitionIndexError,
    DefinitionResolutionError,
)
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.factory.core import FHIRModelFactory
from fhircraft.fhir.resources.factory.resolver import SnapshotResolver

__all__ = [
    # Core factory
    "FHIRModelFactory",
    # Pipeline internals (public access)
    "ModelAssembler",
    "SnapshotResolver",
    "DefinitionIndex",
    "ElementNode",
    "BuildContext",
    "TypeRegistry",
    # Exceptions
    "DefinitionIndexError",
    "DefinitionResolutionError",
]
