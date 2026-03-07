"""
ProfileFactory — the top-level façade for building Pydantic models from FHIR
``StructureDefinition`` objects.

This is the main public entry point; the rest of the pipeline (resolver,
assembler, builders, validators) is invoked from here.

Usage::

    factory = ProfileFactory(repository)
    factory.register_sd_dict(my_profile_dict)   # pre-register dependency
    model = factory.build(sd=my_profile_sd)
"""

from __future__ import annotations

import re
import keyword
import warnings
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Sequence, TYPE_CHECKING

from pydantic import BaseModel, Field, create_model

from fhircraft.fhir.resources.base import (
    FHIRBaseModel,
    FHIRSliceModel,
    FhirBaseModelKind,
)
from fhircraft.fhir.resources.factory.assembler import ModelAssembler
from fhircraft.fhir.resources.factory.context import BuildContext
from fhircraft.fhir.resources.factory.exceptions import (
    DefinitionResolutionError,
)
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.factory.resolver import SnapshotResolver
from fhircraft.fhir.resources.definitions.registry import StructureDefinitionRegistry
from fhircraft.fhir.resources.datatypes.registry import (
    get_fhir_type_by_url,
    get_fhir_type,
)
from fhircraft.utils import get_FHIR_release_from_version, capitalize

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4.core import (
        StructureDefinition as R4_StructureDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R4B.core import (
        StructureDefinition as R4B_StructureDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R5.core import (
        StructureDefinition as R5_StructureDefinition,
    )


class FHIRStructureFactory:

    def __init__(
        self, fhir_release: str, registry: StructureDefinitionRegistry | None = None
    ) -> None:

        self.fhir_release: str = fhir_release
        if registry and registry.fhir_release != fhir_release:
            raise ValueError(
                f"Provided registry FHIR release '{registry.fhir_release}' does not match factory FHIR release '{fhir_release}'."
            )
        self.definition_registry = registry or StructureDefinitionRegistry(fhir_release)
        # Global cache: canonical URL → built Pydantic model
        self.construction_cache: dict[str, type[BaseModel]] = {}

    # ------------------------------------------------------------------
    # Main entry points
    # ------------------------------------------------------------------

    def build(
        self,
        structure_definition: Any = None,
        *,
        canonical_url: str | None = None,
        mixins: Sequence[type] | None = None,
        mode: Literal["auto", "snapshot", "differential"] = "auto",
    ) -> type[BaseModel]:
        """
        Build and return a Pydantic model for the given ``StructureDefinition``.

        Args:
            structure_definition: The ``StructureDefinition`` to build from.  Accepted forms:

                * A parsed ``R4 / R4B / R5 StructureDefinition`` Pydantic object
                * A ``dict`` (will be validated as a ``StructureDefinition``)
                * A file path string (``*.json`` / ``*.yaml``)
                * A canonical URL string (fetched from the repository)
                * ``None`` — requires *canonical_url* to be set

            canonical_url: Canonical URL to look up when *sd* is ``None``.
            mixins: Optional extra base classes added to the constructed model
                (e.g. ``(FHIRSliceModel,)``).

        Returns:
            A Pydantic model class representing the FHIR resource / profile.

        Raises:
            ValueError: For invalid / missing inputs.
            DefinitionResolutionError: When the differential cannot be resolved.
            UnregisteredTypeError: When a required type is not in the registry.
        """

        if structure_definition:
            structure_definition = self._normalise_structure_definition(
                self.definition_registry, structure_definition
            )
        elif canonical_url:
            structure_definition = self.definition_registry.get(canonical_url)
        # Cache check
        if structure_definition.url in self.construction_cache:
            return self.construction_cache[structure_definition.url]

        return self._build(structure_definition, mixins=mixins, mode=mode)

    # ------------------------------------------------------------------
    # Internal build pipeline
    # ------------------------------------------------------------------

    def _build(
        self,
        structure_def: "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition",
        mixins: Sequence[type] | None = None,
        mode: Literal["auto", "snapshot", "differential"] = "auto",
    ) -> type[BaseModel]:

        sd_url = structure_def.url or ""
        sd_name = structure_def.name or ""
        fhir_version = structure_def.fhirVersion or ""

        if not sd_name:
            raise ValueError("StructureDefinition must have a valid 'name'.")
        if not fhir_version:
            raise ValueError(
                "StructureDefinition must specify 'fhirVersion'. "
                "Set it explicitly if building from a dict."
            )

        fhir_release = get_FHIR_release_from_version(fhir_version)
        sanitized_name = self._sanitize_name(sd_name)

        # ------------------------------------------------------------------
        # Resolve base definition
        # ------------------------------------------------------------------
        base_canonical = structure_def.baseDefinition
        base_model: type = FHIRBaseModel
        base_index = None
        if base_canonical:
            # Try directly from registry of built-in types first
            resolved = get_fhir_type_by_url(
                base_canonical, fhir_release, fail_if_not_found=False
            )
            if (
                resolved is not None
                and isinstance(resolved, type)
                and issubclass(resolved, FHIRBaseModel)
            ):
                base_model = resolved
            else:
                # Try to build from repository
                try:
                    base_model = self.build(canonical_url=base_canonical)
                except Exception as exc:
                    warnings.warn(
                        f"Could not resolve base definition '{base_canonical}' for "
                        f"'{sd_name}': {exc}.  Using FHIRBaseModel as fallback."
                    )
                    base_model = FHIRBaseModel

            # Obtain the base snapshot for differential resolution
            base_definition = self.definition_registry.get(base_canonical)
            if base_definition.snapshot and base_definition.snapshot.element:
                base_index = DefinitionIndex.from_elements(
                    base_definition.snapshot.element
                )
            else:
                raise DefinitionResolutionError(
                    f"Base definition '{base_canonical}' for '{sd_name}' has no snapshot or elements."
                )

        # ------------------------------------------------------------------
        # Produce the complete DefinitionIndex
        # ------------------------------------------------------------------
        resolver = SnapshotResolver(self.definition_registry)
        definition_index = resolver.resolve(structure_def, base_index, mode=mode)

        # ------------------------------------------------------------------
        # Assemble the Pydantic model
        # ------------------------------------------------------------------
        base_classes: tuple[type, ...] = (base_model,)
        if mixins:
            base_classes = (base_model, *mixins)

        assembler = ModelAssembler(
            index=definition_index,
            ctx=BuildContext(
                fhir_release=self.fhir_release,
                fhir_version=fhir_version,
                registry=self.definition_registry,
                resource_name=sanitized_name,
                factory=self,
                base=base_model,
            ),
            resource_name=sanitized_name,
        )
        model = assembler.assemble(sanitized_name, base=base_classes)

        # ------------------------------------------------------------------
        # Override / inject meta.profile default
        # ------------------------------------------------------------------
        if sd_url:
            has_meta = "meta" in model.model_fields or (
                issubclass(base_model, BaseModel) and "meta" in base_model.model_fields
            )
            if has_meta:
                try:
                    Meta = get_fhir_type("Meta", fhir_release)
                    meta_field: tuple = (
                        Optional[Meta],
                        Field(
                            title="Meta",
                            description="Metadata about the resource.",
                            default=Meta(profile=[sd_url]),
                        ),
                    )
                    model = create_model(
                        sanitized_name,
                        meta=meta_field,
                        __base__=model,
                    )
                except Exception:
                    pass  # non-fatal

        # ------------------------------------------------------------------
        # Attach structural class metadata
        # ------------------------------------------------------------------
        if issubclass(model, FHIRBaseModel):
            model._fhir_release = fhir_release
            model._canonical_url = structure_def.url
            model._kind = (
                FhirBaseModelKind(structure_def.kind)
                if structure_def.kind
                else FhirBaseModelKind.LOGICAL
            )
            model._type = structure_def.type or sd_name
            abstract = structure_def.abstract
            if abstract is not None:
                model._abstract = bool(abstract)
            elif issubclass(base_model, FHIRBaseModel) and hasattr(
                base_model, "_abstract"
            ):
                model._abstract = base_model._abstract
            else:
                model._abstract = False

        # ------------------------------------------------------------------
        # Cache and register
        # ------------------------------------------------------------------
        if sd_url:
            self.construction_cache[sd_url] = model
        return model

    # ------------------------------------------------------------------
    # Input normalisation
    # ------------------------------------------------------------------

    def _normalise_structure_definition(
        self,
        registry: StructureDefinitionRegistry,
        sd: Any,
    ) -> "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition":
        """
        Normalise *sd* (dict / str / Pydantic SD / ``None``) to a validated
        ``StructureDefinition`` Pydantic object, fetching from the repository
        when necessary.
        """

        if getattr(sd, "_resource_type", None) == "StructureDefinition":
            registry.add(sd)
            return sd

        elif isinstance(sd, dict):
            return registry.from_dict(sd)

        elif isinstance(sd, str):
            # Canonical URL
            return registry.get(sd)

        return sd

    # ------------------------------------------------------------------
    # Name sanitisation (carried over from legacy factory)
    # ------------------------------------------------------------------

    @staticmethod
    def _sanitize_name(name: str) -> str:
        """Produce a valid Python class name from a FHIR resource name."""
        sanitized = "".join(ch for ch in name if ch.isalnum())
        sanitized = "".join(
            capitalize(word) for word in re.split("[^a-zA-Z]", name) if word
        )

        if not sanitized:
            raise ValueError(
                f"FHIR resource name '{name}' has no alphanumeric characters."
            )
        while sanitized[0].isdigit():
            sanitized = sanitized[1:]
        sanitized = sanitized[0].upper() + sanitized[1:]
        if keyword.iskeyword(sanitized):
            sanitized = f"{sanitized}_"
        return sanitized

    def clear_cache(self) -> None:
        """Clear the construction cache."""
        self.construction_cache.clear()
