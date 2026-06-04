"""
FHIR Mapper Module

Provides FHIR StructureMap-based data transformation via FHIRStructureMapper.

Recommended import::

    from fhircraft.fhir.mapper import FHIRStructureMapper
"""

from .interface import FHIRStructureMapper

__all__ = [
    "FHIRStructureMapper",
]
