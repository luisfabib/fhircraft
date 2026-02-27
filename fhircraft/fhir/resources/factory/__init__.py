"""
FHIR Resource Factory — public API package.

New API (clean break)
---------------------

``ProfileFactory``  — the new factory class.
``factory``         — module-level singleton for convenience.

Compatibility shims for existing callers
-----------------------------------------

``ResourceFactory``         → ``ProfileFactory`` (alias)
``construct_resource_model`` → ``factory.build``

The old ``StructureNode``, ``ConstructionMode``, and
``ResourceFactoryValidators`` are no longer provided by this package.
Import them from :mod:`fhircraft.fhir.resources.factory_legacy` if still
needed during migration.
"""

from __future__ import annotations

from fhircraft.fhir.resources.factory.assembler import ModelAssembler

# from fhircraft.fhir.resources.factory.builders import (
#     # BUILDER_CHAIN,
#     # BuiltField,
#     # BackboneFieldBuilder,
#     # ContentReferenceFieldBuilder,
#     # FieldBuilder,
#     # SimpleFieldBuilder,
#     # SlicedFieldBuilder,
#     # TypeChoiceFieldBuilder,
#     # build_pydantic_field,
#     # handle_python_keyword,
# )
from fhircraft.fhir.resources.factory.context import BuildContext
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.exceptions import (
    DefinitionIndexError,
    DefinitionResolutionError,
)
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.factory.profile_factory import FHIRStructureFactory
from fhircraft.fhir.resources.factory.resolver import SnapshotResolver
from fhircraft.fhir.resources.factory.validators import ValidatorCollector

# ------------------------------------------------------------------
# Module-level singleton
# ------------------------------------------------------------------

#: Default :class:`ProfileFactory` instance used by the convenience function
#: :func:`construct_resource_model`.  Configures itself lazily.
factory = FHIRStructureFactory()

# ------------------------------------------------------------------
# Compatibility shims (legacy names)
# ------------------------------------------------------------------

#: Alias kept for backward compatibility.  New code should use
#: :class:`FHIRStructureFactory` directly.
ResourceFactory = FHIRStructureFactory

#: Convenience function; equivalent to ``factory.build(sd=...)``.
construct_resource_model = factory.build

__all__ = [
    # New API
    "FHIRStructureFactory",
    "ModelAssembler",
    "SnapshotResolver",
    "DefinitionIndex",
    "ElementNode",
    "BuildContext",
    "TypeRegistry",
    "ValidatorCollector",
    "BuiltField",
    "FieldBuilder",
    "BUILDER_CHAIN",
    "BackboneFieldBuilder",
    "ContentReferenceFieldBuilder",
    "SimpleFieldBuilder",
    "SlicedFieldBuilder",
    "TypeChoiceFieldBuilder",
    "build_pydantic_field",
    "handle_python_keyword",
    # Exceptions
    "DefinitionIndexError",
    "DefinitionResolutionError",
    "UnregisteredTypeError",
    # Singletons / convenience
    "factory",
    "construct_resource_model",
    # Compatibility shims
    "ResourceFactory",
]
