#!/usr/bin/env python
"""
Structure Definition Repository
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests
from pydantic_core import ValidationError

from fhircraft.fhir.resources.definitions import StructureDefinition
from fhircraft.utils import load_env_variables


class StructureDefinitionRepository(ABC):
    """Abstract base class for structure definition repositories."""

    @abstractmethod
    def get(self, canonical_url: str) -> StructureDefinition:
        """Retrieve a structure definition by canonical URL."""
        pass

    @abstractmethod
    def add(self, structure_def: StructureDefinition) -> None:
        """Add a structure definition to the repository."""
        pass

    @abstractmethod
    def has(self, canonical_url: str) -> bool:
        """Check if a structure definition exists in the repository."""
        pass

    @abstractmethod
    def set_internet_enabled(self, enabled: bool) -> None:
        """Enable or disable internet access for this repository."""
        pass


class HttpStructureDefinitionRepository(StructureDefinitionRepository):
    """Repository that downloads structure definitions from the internet."""

    def __init__(self):
        self._internet_enabled = True

    def get(self, canonical_url: str) -> StructureDefinition:
        """Download structure definition from the internet."""
        if not self._internet_enabled:
            raise RuntimeError(
                f"Attempted to get {canonical_url} while internet access is disabled. Either enable internet access or use a local repository."
            )
        try:
            return self.__download_structure_definition(canonical_url)
        except ValidationError as ve:
            raise ValidationError(
                f"Validation error for structure definition from {canonical_url}: {ve}"
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to download structure definition from {canonical_url}: {e}"
            )

    def add(self, structure_def: StructureDefinition) -> None:
        """HTTP repository doesn't support adding definitions."""
        raise NotImplementedError(
            "HttpStructureDefinitionRepository doesn't support adding definitions"
        )

    def has(self, canonical_url: str) -> bool:
        """Check if URL can potentially be resolved."""
        return self._internet_enabled and canonical_url.startswith(
            ("http://", "https://")
        )

    def set_internet_enabled(self, enabled: bool) -> None:
        """Enable or disable internet access."""
        self._internet_enabled = enabled

    def __download_structure_definition(self, profile_url: str) -> StructureDefinition:
        """
        Downloads the structure definition of a FHIR resource from the provided profile URL.

        Parameters:
            profile_url (str): The URL of the FHIR profile from which to retrieve the structure definition.

        Returns:
            StructureDefinition: A validated StructureDefinition object.
        """
        if not profile_url.endswith(".json"):
            # Construct endpoint URL for the StructureDefinition JSON
            if profile_url.startswith("http://hl7.org/fhir/StructureDefinition"):
                domain, resource = profile_url.rsplit("/", 1)
                domain = domain.replace(
                    "http://hl7.org/fhir/StructureDefinition",
                    "https://hl7.org/fhir/R4/extension",
                )
                resource = resource.lower()
            else:
                domain, resource = profile_url.rsplit("/", 1)
            json_url = f"{domain}-{resource}.json"
        else:
            json_url = profile_url

        # Configure proxy if needed
        settings = load_env_variables()
        proxies = (
            {
                k: v
                for k, v in {
                    "https": settings.get("PROXY_URL_HTTPS"),
                    "http": settings.get("PROXY_URL_HTTP"),
                }.items()
                if v is not None
            }
            if settings.get("PROXY_URL_HTTPS") or settings.get("PROXY_URL_HTTP")
            else None
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, application/json+fhir, text/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        }
        # Download the StructureDefinition JSON
        response = requests.get(
            json_url,
            proxies=proxies,
            verify=settings.get("CERTIFICATE_BUNDLE_PATH"),
            headers=headers,
            allow_redirects=True,
        )
        response.raise_for_status()
        return StructureDefinition.model_validate(response.json())


class CompositeStructureDefinitionRepository(StructureDefinitionRepository):
    """Repository that manages local storage and optional internet fallback."""

    def __init__(self, internet_enabled: bool = True):
        self._local_definitions: Dict[str, StructureDefinition] = {}
        self._internet_enabled = internet_enabled
        self._http_repository = HttpStructureDefinitionRepository()

    def get(self, canonical_url: str) -> StructureDefinition:
        """Get structure definition with local-first, internet fallback strategy."""
        # First try local repository
        if canonical_url in self._local_definitions:
            return self._local_definitions[canonical_url]

        # Fall back to internet if enabled
        if self._internet_enabled:
            structure_definition = self._http_repository.get(canonical_url)
            if structure_definition:
                # Cache it locally for future use
                self.add(structure_definition)
                return structure_definition

        raise RuntimeError(f"Structure definition not found for {canonical_url}")

    def add(self, structure_definition: StructureDefinition) -> None:
        """Add a structure definition to local storage."""
        if (canonical_url := structure_definition.url) in self._local_definitions:
            raise ValueError(
                f"Attempted to load structure definition with duplicated URL {canonical_url} in local repository."
            )
        if not structure_definition.url:
            raise ValueError(
                "StructureDefinition must have a 'url' field to be added to the repository."
            )
        self._local_definitions[canonical_url] = structure_definition

    def has(self, canonical_url: str) -> bool:
        """Check if structure definition exists locally or can be downloaded."""
        return canonical_url in self._local_definitions or (
            self._internet_enabled and self._http_repository.has(canonical_url)
        )

    def load_from_directory(self, directory_path: Union[str, Path]) -> None:
        """Load all structure definitions from a directory."""
        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        for file_path in directory.rglob("*.json"):
            try:
                structure_def = self.__load_json_structure_definition(file_path)
                self.add(structure_def)
            except Exception as e:
                raise RuntimeError(
                    f"Error loading structure definition from {file_path}: {e}"
                )

    def load_from_files(self, *file_paths: Union[str, Path]) -> None:
        """Load structure definitions from individual files."""
        for file_path in file_paths:
            try:
                structure_def = self.__load_json_structure_definition(Path(file_path))
                self.add(structure_def)
            except Exception as e:
                raise RuntimeError(f"Failed to load {file_path}: {e}")

    def load_from_definitions(self, *definitions: Dict[str, Any]) -> None:
        """Load structure definitions from pre-loaded dictionaries."""
        for structure_def in definitions:
            structure_definition = StructureDefinition.model_validate(structure_def)
            self.add(structure_definition)

    def set_internet_enabled(self, enabled: bool) -> None:
        """Enable or disable internet access."""
        self._internet_enabled = enabled
        self._http_repository.set_internet_enabled(enabled)

    def get_loaded_urls(self) -> List[str]:
        """Get a list of all locally loaded canonical URLs."""
        return list(self._local_definitions.keys())

    def clear_local_cache(self) -> None:
        """Clear all locally cached structure definitions."""
        self._local_definitions.clear()

    def __load_json_structure_definition(self, file_path: Path) -> StructureDefinition:
        """Load and parse a JSON file."""
        with open(file_path, "r", encoding="utf-8") as file:
            return StructureDefinition.model_validate(json.load(file))


# Convenience functions for easy configuration
def configure_repository(
    directory: Optional[Union[str, Path]] = None,
    files: Optional[List[Union[str, Path]]] = None,
    definitions: Optional[List[Dict[str, Any]]] = None,
    internet_enabled: bool = True,
) -> CompositeStructureDefinitionRepository:
    """Configure a repository with various sources."""
    repo = CompositeStructureDefinitionRepository(internet_enabled=internet_enabled)

    if directory:
        repo.load_from_directory(directory)

    if files:
        repo.load_from_files(*files)

    if definitions:
        repo.load_from_definitions(*definitions)

    return repo
