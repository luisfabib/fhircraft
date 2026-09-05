"""
FHIRcraft: FHIR Resource Modeling and Processing Toolkit

Two-tier public API
-------------------
**Top-level** (``from fhircraft import ...``)
    Common-task imports covering the vast majority of use cases:
    resource access, model building, data transformation, and configuration.

**Subpackage** (``from fhircraft.fhir.path import ...``, etc.)
    Specialized or path-heavy workflows that are cleaner under their own namespace:

    - ``fhircraft.fhir.path``  — ``FHIRPath``, ``FHIRPathMixin``, ``parse_fhirpath``
    - ``fhircraft.fhir.resources`` — ``StructureDefinitionRegistry``, ``get_fhir_type_by_url``,
      ``FHIRSliceModel``, ``FHIRModelKind``
    - ``fhircraft.exceptions``  — full exception/warning hierarchy
"""

__version__ = "0.8.3"

from typing import Final, Literal

# ---  Supported FHIR releases  ---
SUPPORTED_FHIR_RELEASES: Final = ("R4", "R4B", "R5")

# --- Model building ---
from fhircraft.fhir.resources.factory import FHIRModelFactory
from fhircraft.fhir.resources.base import FHIRBaseModel
from fhircraft.fhir.resources.datatypes import R4, R4B, R5

# --- Data transformation ---
from fhircraft.fhir.mapper import FHIRStructureMapper

# --- Configuration ---
from fhircraft.config import (
    get_config,
    configure,
    override_config,
    disable_constraint,
    enable_constraint,
    reset_config,
    load_config_from_env,
)

# --- Utilities ---
from fhircraft.utils import get_FHIR_release_from_version

__all__ = [
    # Resource access
    "R4",
    "R4B",
    "R5",
    # Model building
    "FHIRModelFactory",
    "FHIRBaseModel",
    # Data transformation
    "FHIRStructureMapper",
    # Configuration
    "configure",
    "get_config",
    "override_config",
    "reset_config",
    "disable_constraint",
    "enable_constraint",
    "load_config_from_env",
    # Utilities
    "get_FHIR_release_from_version",
    "SUPPORTED_FHIR_RELEASES",
]
