"""
FHIR Mapper Module

This module provides FHIR mapping and transformation functionality:
- FHIRMapper: High-level interface for FHIR mapping operations
- StructureMap: FHIR StructureMap resource model
- ConceptMap: FHIR ConceptMap resource model

Recommended imports:
    from fhircraft.fhir.mapper import FHIRMapper
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.request import urlopen

from pydantic import BaseModel

from fhircraft.fhir.mapper.parser import FhirMappingLanguageParser
from fhircraft.fhir.resources.datatypes.R5.resources.concept_map import ConceptMap
from fhircraft.fhir.resources.datatypes.R5.resources.structure_map import StructureMap
from fhircraft.fhir.resources.repository import CompositeStructureDefinitionRepository

from .parser import FhirMappingLanguageParser

__all__ = [
    # High-level API
    "FHIRMapper",
    # Lower-level components
    "StructureMap",
    "ConceptMap",
]


class FHIRMapper:
    """
    High-level FHIR mapping interface for parsing, loading, and executing structure maps.

    This class provides a simplified interface for common FHIR mapping operations:
    - Loading structure maps from files, URLs, or JSON
    - Parsing short syntax mapping scripts into structure maps
    - Executing mappings from either structure maps or short syntax
    - Working with both FHIR resources and custom Pydantic models

    Example:
        mapper = FHIRMapper()

        # Parse and execute from short syntax
        result = mapper.execute_mapping(
            mapping_script="map 'http://example.org' = 'demo' group main(source src, target tgt) { src.name -> tgt.fullName; }",
            source_data={"name": "John Doe"},
        )

        # Load from file and execute
        structure_map = mapper.load_structure_map("mapping.json")
        result = mapper.execute_mapping(structure_map, source_data)
    """

    def __init__(
        self,
        repository: Optional[CompositeStructureDefinitionRepository] = None,
    ):
        """
        Initialize the FHIR mapper.

        Args:
            repository: Structure definition repository for resolving canonical URLs.
                       If None, creates a default repository.
        """
        self.repository = repository or CompositeStructureDefinitionRepository()
        self._engine = None  # Lazy-loaded
        self.parser = FhirMappingLanguageParser()

    @property
    def engine(self):
        """Lazy-load the mapping engine to avoid import issues."""
        if self._engine is None:
            from fhircraft.fhir.mapper.engine.core import FHIRMappingEngine

            self._engine = FHIRMappingEngine(repository=self.repository)
        return self._engine

    def load_structure_map(
        self, source: Union[str, Path, Dict[str, Any], StructureMap]
    ) -> StructureMap:
        """
        Load a StructureMap from various sources.

        Args:
            source: Can be:
                - File path (str or Path) to a JSON file containing the StructureMap
                - URL (str) to fetch the StructureMap from
                - Dictionary containing the StructureMap JSON
                - Already instantiated StructureMap object

        Returns:
            StructureMap object ready for execution

        Raises:
            ValueError: If the source format is invalid
            FileNotFoundError: If a file path doesn't exist
            Exception: If URL fetching fails
        """
        if isinstance(source, StructureMap):
            return source

        if isinstance(source, dict):
            return StructureMap.model_validate(source)

        if isinstance(source, (str, Path)):
            source_str = str(source)

            # Check if it's a URL
            if source_str.startswith(("http://", "https://")):
                try:
                    with urlopen(source_str) as response:
                        data = json.loads(response.read().decode("utf-8"))
                    return StructureMap.model_validate(data)
                except Exception as e:
                    raise Exception(
                        f"Failed to load StructureMap from URL {source_str}: {e}"
                    )

            # Treat as file path
            path = Path(source_str)
            if not path.exists():
                raise FileNotFoundError(f"StructureMap file not found: {path}")

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return StructureMap.model_validate(data)

        raise ValueError(f"Unsupported source type: {type(source)}")

    def parse_mapping_script(self, script: str) -> StructureMap:
        """
        Parse a FHIR mapping language script into a StructureMap.

        Args:
            script: FHIR mapping language script in short syntax

        Returns:
            StructureMap object parsed from the script

        Raises:
            Exception: If parsing fails due to syntax errors
        """
        try:
            return self.parser.parse(script)
        except Exception as e:
            raise Exception(f"Failed to parse mapping script: {e}")

    def execute_mapping(
        self,
        mapping: Union[str, StructureMap, Dict[str, Any]],
        source_data: Union[
            BaseModel, Dict[str, Any], Tuple[Union[BaseModel, dict], ...]
        ],
        target_data: Optional[
            Union[BaseModel, Dict[str, Any], Tuple[Union[BaseModel, dict], ...]]
        ] = None,
        group: Optional[str] = None,
    ) -> tuple[list[BaseModel], dict[str, Any]]:
        """
        Execute a mapping transformation.

        Args:
            mapping: Can be:
                - FHIR mapping language script (str)
                - StructureMap object
                - Dictionary containing StructureMap JSON
            source_data: Source data to transform. Can be:
                - Single source object (BaseModel or dict)
                - Tuple of source objects for multi-source mappings
            target_data: Optional pre-existing target objects. If None, new targets are created.
            options: Execution options to control behavior

        Returns:
            MappingResult containing the transformed target objects and metadata

        Raises:
            Exception: If mapping execution fails
        """

        # Parse/load the structure map
        if isinstance(mapping, str):
            structure_map = self.parse_mapping_script(mapping)
        elif isinstance(mapping, dict):
            structure_map = StructureMap(**mapping)
        elif isinstance(mapping, StructureMap):
            structure_map = mapping
        else:
            raise ValueError(f"Unsupported mapping type: {type(mapping)}")

        # Normalize source data to tuple
        if not isinstance(source_data, tuple):
            sources = (source_data,)
        else:
            sources = source_data

        # Normalize target data to tuple if provided
        targets = None
        if target_data is not None:
            if not isinstance(target_data, tuple):
                targets = (target_data,)
            else:
                targets = target_data

        # Execute the mapping
        try:
            return self.engine.execute(
                structure_map=structure_map,
                sources=sources,  # type: ignore
                targets=targets,  # type: ignore
                group=group,
            )
        except Exception as e:
            raise Exception(f"Mapping execution failed: {e}")

    def validate_mapping_script(self, script: str) -> bool:
        """
        Validate a FHIR mapping language script for syntax correctness.

        Args:
            script: FHIR mapping language script to validate

        Returns:
            True if the script is syntactically valid, False otherwise
        """
        return self.parser.is_valid(script)

    def list_groups(
        self, mapping: Union[str, StructureMap, Dict[str, Any]]
    ) -> List[str]:
        """
        List all group names defined in a mapping.

        Args:
            mapping: StructureMap, script, or dict containing the mapping

        Returns:
            List of group names available for execution
        """
        if isinstance(mapping, str):
            structure_map = self.parse_mapping_script(mapping)
        elif isinstance(mapping, dict):
            structure_map = StructureMap(**mapping)
        elif isinstance(mapping, StructureMap):
            structure_map = mapping
        else:
            raise ValueError(f"Unsupported mapping type: {type(mapping)}")

        return [group.name for group in (structure_map.group or []) if group.name]

    def add_structure_definition(
        self,
        structure_definition: Union[Dict[str, Any], Any],
        fail_if_exists: bool = False,
    ) -> None:
        """
        Add a StructureDefinition to the engine's repository for use in mappings.

        This allows you to register custom FHIR profiles, extensions, or other
        structure definitions that will be available when executing mappings.

        Args:
            structure_definition: StructureDefinition to add. Can be:
                - Dictionary containing StructureDefinition JSON
                - StructureDefinition instance
            fail_if_exists: If True, raises error if definition already exists

        Raises:
            ValueError: If structure definition is invalid or already exists
        """
        from fhircraft.fhir.resources.definitions import StructureDefinition

        if isinstance(structure_definition, dict):
            struct_def = StructureDefinition(**structure_definition)
        else:
            struct_def = structure_definition

        self.repository.add(struct_def, fail_if_exists=fail_if_exists)

    def add_structure_definitions_from_file(
        self, file_path: Union[str, Path], fail_if_exists: bool = False
    ) -> int:
        """
        Load StructureDefinitions from a JSON file and add them to the repository.

        Args:
            file_path: Path to JSON file containing StructureDefinition(s)
            fail_if_exists: If True, raises error if any definition already exists

        Returns:
            Number of StructureDefinitions added

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        from fhircraft.fhir.resources.definitions import StructureDefinition

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        count = 0

        # Handle both single StructureDefinition and Bundle resources
        if isinstance(data, dict):
            if data.get("resourceType") == "StructureDefinition":
                # Single StructureDefinition
                struct_def = StructureDefinition(**data)
                self.repository.add(struct_def, fail_if_exists=fail_if_exists)
                count = 1
            elif data.get("resourceType") == "Bundle" and data.get("entry"):
                # Bundle containing StructureDefinitions
                for entry in data["entry"]:
                    resource = entry.get("resource", {})
                    if resource.get("resourceType") == "StructureDefinition":
                        struct_def = StructureDefinition(**resource)
                        self.repository.add(struct_def, fail_if_exists=fail_if_exists)
                        count += 1
            else:
                raise ValueError(
                    f"File must contain a StructureDefinition or Bundle resource, got {data.get('resourceType')}"
                )
        else:
            raise ValueError("File must contain a JSON object")

        return count

    def load_fhir_package(
        self,
        package_name: str,
        package_version: Optional[str] = None,
        fail_if_exists: bool = False,
    ) -> None:
        """
        Load a FHIR package from the registry and add its StructureDefinitions.

        This is useful for loading standard FHIR profiles and extensions from
        packages like "hl7.fhir.us.core" or "hl7.fhir.r4.core".

        Args:
            package_name: Name of the FHIR package (e.g., "hl7.fhir.us.core")
            package_version: Version of the package (defaults to latest)
            fail_if_exists: If True, raises error if package already loaded

        Raises:
            RuntimeError: If internet is disabled or package loading fails
            ValueError: If package already loaded and fail_if_exists is True
        """
        if not hasattr(self.repository, "_package_repository"):
            raise RuntimeError(
                "Package loading is not supported by the current repository configuration"
            )

        package_repo = self.repository._package_repository
        if package_repo is None:
            raise RuntimeError("Package repository is not enabled")

        package_repo.load_package(
            package_name, package_version, fail_if_exists=fail_if_exists
        )

    def has_structure_definition(
        self, canonical_url: str, version: Optional[str] = None
    ) -> bool:
        """
        Check if a StructureDefinition is available in the repository.

        Args:
            canonical_url: Canonical URL of the StructureDefinition
            version: Optional specific version to check

        Returns:
            True if the StructureDefinition is available
        """
        return self.repository.has(canonical_url, version)

    def list_loaded_packages(self) -> Dict[str, str]:
        """
        Get a dictionary of loaded FHIR packages and their versions.

        Returns:
            Dictionary mapping package names to versions

        Raises:
            RuntimeError: If package loading is not supported
        """
        if not hasattr(self.repository, "_package_repository"):
            raise RuntimeError(
                "Package loading is not supported by the current repository configuration"
            )

        package_repo = self.repository._package_repository
        if package_repo is None:
            raise RuntimeError("Package repository is not enabled")

        return package_repo.get_loaded_packages()

    def get_structure_definition_versions(self, canonical_url: str) -> List[str]:
        """
        Get all available versions of a StructureDefinition.

        Args:
            canonical_url: Canonical URL of the StructureDefinition

        Returns:
            List of available versions, sorted
        """
        return self.repository.get_versions(canonical_url)
