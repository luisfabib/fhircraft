"""
FHIR Resources Module
"""

from .base import FHIRBaseModel, FHIRModelKind, FHIRSliceModel, FHIRPrimitiveModel
from .factory import FHIRModelFactory
from .definitions import StructureDefinitionRegistry
from .datatypes import (
    get_fhir_type,
    get_fhir_type_by_url,
)
from .generator import CodeGenerator
from fhircraft.exceptions import (
    FhirTypeError,
    FhirValidationWarning,
    FactoryException,
    FactoryDefinitionIndexError,
    FactoryDefinitionResolutionError,
    FactoryBuilderError,
    FactoryTypeResolutionError,
    FactoryAssemblerError,
    FactoryWarning,
    DefinitionNotFoundError,
)

__all__ = [
    # Core model classes
    "FHIRBaseModel",
    "FHIRSliceModel",
    "FHIRModelKind",
    "FHIRPrimitiveModel",
    # Factory
    "FHIRModelFactory",
    # Registry
    "StructureDefinitionRegistry",
    # Type helpers
    "get_fhir_type",
    "get_fhir_type_by_url",
    # Code generation
    "CodeGenerator",
    # Exceptions (re-exported for convenience)
    "FhirTypeError",
    "FhirValidationWarning",
    "FactoryException",
    "FactoryDefinitionIndexError",
    "FactoryDefinitionResolutionError",
    "FactoryBuilderError",
    "FactoryTypeResolutionError",
    "FactoryAssemblerError",
    "FactoryWarning",
    "DefinitionNotFoundError",
]
