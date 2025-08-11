#!/usr/bin/env python
"""
Structure Definition Repository
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from packaging import version
from pydantic_core import ValidationError

from fhircraft.fhir.resources.definitions import StructureDefinition
from fhircraft.utils import load_env_variables


class StructureDefinitionRepository(ABC):
    """Abstract base class for structure definition repositories."""

    @abstractmethod
    def get(
        self, canonical_url: str, version: Optional[str] = None
    ) -> StructureDefinition:
        """Retrieve a structure definition by canonical URL and optional version."""
        pass

    @abstractmethod
    def add(self, structure_def: StructureDefinition) -> None:
        """Add a structure definition to the repository."""
        pass

    @abstractmethod
    def has(self, canonical_url: str, version: Optional[str] = None) -> bool:
        """Check if a structure definition exists in the repository."""
        pass

    @abstractmethod
    def get_versions(self, canonical_url: str) -> List[str]:
        """Get all available versions for a canonical URL."""
        pass

    @abstractmethod
    def get_latest_version(self, canonical_url: str) -> Optional[str]:
        """Get the latest version for a canonical URL."""
        pass

    @abstractmethod
    def set_internet_enabled(self, enabled: bool) -> None:
        """Enable or disable internet access for this repository."""
        pass

    @staticmethod
    def parse_canonical_url(canonical_url: str) -> Tuple[str, Optional[str]]:
        """Parse a canonical URL to extract base URL and version."""
        if "|" in canonical_url:
            base_url, version = canonical_url.split("|", 1)
            return base_url.strip(), version.strip()
        return canonical_url.strip(), None

    @staticmethod
    def format_canonical_url(base_url: str, version: Optional[str] = None) -> str:
        """Format a canonical URL with optional version."""
        if version:
            return f"{base_url}|{version}"
        return base_url


class HttpStructureDefinitionRepository(StructureDefinitionRepository):
    """Repository that downloads structure definitions from the internet."""

    def __init__(self):
        self._internet_enabled = True

    def get(
        self, canonical_url: str, version: Optional[str] = None
    ) -> StructureDefinition:
        """Download structure definition from the internet."""
        if not self._internet_enabled:
            raise RuntimeError(
                f"Attempted to get {canonical_url} while internet access is disabled. Either enable internet access or use a local repository."
            )

        # Parse URL to handle versioned URLs
        base_url, parsed_version = self.parse_canonical_url(canonical_url)
        target_version = version or parsed_version

        # Format the URL for download (with version if specified)
        download_url = (
            self.format_canonical_url(base_url, target_version)
            if target_version
            else base_url
        )

        try:
            return self.__download_structure_definition(download_url)
        except ValidationError as ve:
            raise ValidationError(
                f"Validation error for structure definition from {download_url}: {ve}"
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to download structure definition from {download_url}: {e}"
            )

    def add(self, structure_def: StructureDefinition) -> None:
        """HTTP repository doesn't support adding definitions."""
        raise NotImplementedError(
            "HttpStructureDefinitionRepository doesn't support adding definitions"
        )

    def has(self, canonical_url: str, version: Optional[str] = None) -> bool:
        """Check if URL can potentially be resolved."""
        base_url, parsed_version = self.parse_canonical_url(canonical_url)
        return self._internet_enabled and base_url.startswith(("http://", "https://"))

    def get_versions(self, canonical_url: str) -> List[str]:
        """HTTP repository can't list versions without downloading."""
        raise NotImplementedError(
            "HttpStructureDefinitionRepository doesn't support getting versions"
        )

    def get_latest_version(self, canonical_url: str) -> Optional[str]:
        """HTTP repository can't determine latest version without downloading."""
        raise NotImplementedError(
            "HttpStructureDefinitionRepository doesn't support getting latest version"
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
        # Structure: {base_url: {version: StructureDefinition}}
        self._local_definitions: Dict[str, Dict[str, StructureDefinition]] = {}
        # Track latest versions: {base_url: latest_version}
        self._latest_versions: Dict[str, str] = {}
        self._internet_enabled = internet_enabled
        self._http_repository = HttpStructureDefinitionRepository()

    def get(
        self, canonical_url: str, version: Optional[str] = None
    ) -> StructureDefinition:
        """Get structure definition with local-first, internet fallback strategy."""
        base_url, parsed_version = self.parse_canonical_url(canonical_url)
        target_version = version or parsed_version

        # First try local repository
        if base_url in self._local_definitions:
            if target_version:
                # Look for specific version
                if target_version in self._local_definitions[base_url]:
                    return self._local_definitions[base_url][target_version]
            else:
                # Get latest version if no version specified
                latest_version = self.get_latest_version(base_url)
                if (
                    latest_version
                    and latest_version in self._local_definitions[base_url]
                ):
                    return self._local_definitions[base_url][latest_version]

        # Fall back to internet if enabled
        if self._internet_enabled:
            structure_definition = self._http_repository.get(canonical_url, version)
            if structure_definition:
                # Cache it locally for future use
                self.add(structure_definition)
                return structure_definition

        version_info = f" version {target_version}" if target_version else ""
        raise RuntimeError(
            f"Structure definition not found for {base_url}{version_info}"
        )

    def add(self, structure_definition: StructureDefinition) -> None:
        """Add a structure definition to local storage."""
        if not structure_definition.url:
            raise ValueError(
                "StructureDefinition must have a 'url' field to be added to the repository."
            )

        base_url, version = self.parse_canonical_url(structure_definition.url)

        # Use the structure definition's version field if no version in URL
        if not version and structure_definition.version:
            version = structure_definition.version

        if not version:
            raise ValueError(
                f"StructureDefinition for {base_url} must have a version (either in URL or version field)."
            )

        # Initialize base URL storage if needed
        if base_url not in self._local_definitions:
            self._local_definitions[base_url] = {}

        # Check for duplicates
        if version in self._local_definitions[base_url]:
            raise ValueError(
                f"Attempted to load structure definition with duplicated URL {base_url} version {version} in local repository."
            )

        # Store the definition
        self._local_definitions[base_url][version] = structure_definition

        # Update latest version tracking
        self._update_latest_version(base_url, version)

    def has(self, canonical_url: str, version: Optional[str] = None) -> bool:
        """Check if structure definition exists locally or can be downloaded."""
        base_url, parsed_version = self.parse_canonical_url(canonical_url)
        target_version = version or parsed_version

        # Check local storage
        if base_url in self._local_definitions:
            if target_version:
                return target_version in self._local_definitions[base_url]
            else:
                # Has any version locally
                return bool(self._local_definitions[base_url])

        # Check if can be downloaded
        return self._internet_enabled and self._http_repository.has(
            canonical_url, version
        )

    def get_versions(self, canonical_url: str) -> List[str]:
        """Get all available versions for a canonical URL."""
        base_url, _ = self.parse_canonical_url(canonical_url)

        if base_url in self._local_definitions:
            # Sort versions using semantic versioning
            versions = list(self._local_definitions[base_url].keys())
            try:
                return sorted(versions, key=lambda v: version.parse(v))
            except version.InvalidVersion:
                # Fall back to string sorting if not semantic versions
                return sorted(versions)

        return []

    def get_latest_version(self, canonical_url: str) -> Optional[str]:
        """Get the latest version for a canonical URL."""
        base_url, _ = self.parse_canonical_url(canonical_url)
        return self._latest_versions.get(base_url)

    def _update_latest_version(self, base_url: str, new_version: str) -> None:
        """Update the latest version tracking for a base URL."""
        current_latest = self._latest_versions.get(base_url)

        if not current_latest:
            self._latest_versions[base_url] = new_version
            return

        try:
            # Use semantic versioning comparison
            if version.parse(new_version) > version.parse(current_latest):
                self._latest_versions[base_url] = new_version
        except version.InvalidVersion:
            # Fall back to string comparison if not semantic versions
            if new_version > current_latest:
                self._latest_versions[base_url] = new_version

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
        """Get a list of all locally loaded canonical URLs (base URLs)."""
        return list(self._local_definitions.keys())

    def get_all_loaded_urls_with_versions(self) -> Dict[str, List[str]]:
        """Get all loaded URLs with their available versions."""
        return {
            base_url: self.get_versions(base_url)
            for base_url in self._local_definitions.keys()
        }

    def clear_local_cache(self) -> None:
        """Clear all locally cached structure definitions."""
        self._local_definitions.clear()
        self._latest_versions.clear()

    def remove_version(self, canonical_url: str, version: Optional[str] = None) -> None:
        """Remove a specific version or all versions of a structure definition."""
        base_url, parsed_version = self.parse_canonical_url(canonical_url)
        target_version = version or parsed_version

        if base_url not in self._local_definitions:
            return

        if target_version:
            # Remove specific version
            self._local_definitions[base_url].pop(target_version, None)

            # Update latest version if we removed it
            if self._latest_versions.get(base_url) == target_version:
                remaining_versions = self.get_versions(base_url)
                if remaining_versions:
                    self._latest_versions[base_url] = remaining_versions[
                        -1
                    ]  # Last in sorted list
                else:
                    self._latest_versions.pop(base_url, None)

            # Clean up empty base URL entries
            if not self._local_definitions[base_url]:
                del self._local_definitions[base_url]
        else:
            # Remove all versions
            del self._local_definitions[base_url]
            self._latest_versions.pop(base_url, None)

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
