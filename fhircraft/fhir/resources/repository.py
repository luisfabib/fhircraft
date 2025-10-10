import json
import os
import tarfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar, Union

# Define a type variable for the resource type
T = TypeVar("T")

import requests
from packaging import version
from pydantic_core import ValidationError

from fhircraft.fhir.packages import (
    FHIRPackageRegistryClient,
    FHIRPackageRegistryError,
    PackageNotFoundError,
)
from fhircraft.fhir.resources.definitions import StructureDefinition
from fhircraft.utils import get_FHIR_release_from_version, load_env_variables


class StructureDefinitionNotFoundError(FileNotFoundError):
    """Raised when a required structure definition cannot be resolved."""

    pass


class AbstractRepository(ABC, Generic[T]):
    """Abstract base class for generic repositories."""

    @abstractmethod
    def get(self, canonical_url: str, version: Optional[str] = None) -> T:
        """Retrieve a resource by canonical URL and optional version."""
        pass

    @abstractmethod
    def add(self, resource: T) -> None:
        """Add a resource to the repository."""
        pass

    @abstractmethod
    def has(self, canonical_url: str, version: Optional[str] = None) -> bool:
        """Check if a resource exists in the repository."""
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


class HttpStructureDefinitionRepository(AbstractRepository[StructureDefinition]):
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

    def add(self, resource: StructureDefinition) -> None:
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


class PackageStructureDefinitionRepository(AbstractRepository[StructureDefinition]):
    """Repository that can load FHIR packages from package registries."""

    def __init__(
        self,
        internet_enabled: bool = True,
        registry_base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """
        Initialize the package repository.

        Args:
            internet_enabled: Whether to enable internet access
            registry_base_url: Base URL for package registry (defaults to packages.fhir.org)
            timeout: Request timeout in seconds
        """
        self._internet_enabled = internet_enabled
        self._package_client = FHIRPackageRegistryClient(
            base_url=registry_base_url, timeout=timeout
        )
        # Structure: {base_url: {version: StructureDefinition}}
        self._local_definitions: Dict[str, Dict[str, StructureDefinition]] = {}
        # Track latest versions: {base_url: latest_version}
        self._latest_versions: Dict[str, str] = {}
        # Track loaded packages to avoid duplicate loading
        self._loaded_packages: Dict[str, str] = {}  # {package_name: version}

    def get(
        self, canonical_url: str, version: Optional[str] = None
    ) -> StructureDefinition:
        """Get structure definition from loaded packages."""
        base_url, parsed_version = self.parse_canonical_url(canonical_url)
        target_version = version or parsed_version

        # Check local storage
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

        version_info = f" version {target_version}" if target_version else ""
        raise RuntimeError(
            f"Structure definition not found for {base_url}{version_info}. "
            f"Load the appropriate package first using load_package()."
        )

    def add(self, resource: StructureDefinition) -> None:
        """Add a structure definition to the repository."""
        if not resource.url:
            raise ValueError(
                "StructureDefinition must have a 'url' field to be added to the repository."
            )

        base_url, version = self.parse_canonical_url(resource.url)

        # Use the structure definition's version field if no version in URL
        if not version and resource.version:
            version = resource.version

        if not version:
            raise ValueError(
                f"StructureDefinition for {base_url} must have a version (either in URL or version field)."
            )

        # Initialize base URL storage if needed
        if base_url not in self._local_definitions:
            self._local_definitions[base_url] = {}

        # Store the definition
        self._local_definitions[base_url][version] = resource

        # Update latest version tracking
        self._update_latest_version(base_url, version)

    def has(self, canonical_url: str, version: Optional[str] = None) -> bool:
        """Check if structure definition exists in loaded packages."""
        base_url, parsed_version = self.parse_canonical_url(canonical_url)
        target_version = version or parsed_version

        # Check local storage
        if base_url in self._local_definitions:
            if target_version:
                return target_version in self._local_definitions[base_url]
            else:
                # Has any version locally
                return bool(self._local_definitions[base_url])

        return False

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

    def set_internet_enabled(self, enabled: bool) -> None:
        """Enable or disable internet access."""
        self._internet_enabled = enabled

    def load_package(
        self,
        package_name: str,
        package_version: Optional[str] = None,
        install_dependencies: bool = True,
        fail_if_exists: bool = False,
    ) -> None:
        """
        Load a FHIR package from the registry and add all structure definitions.

        Args:
            package_name: Name of the package (e.g., "hl7.fhir.us.core")
            package_version: Version of the package (defaults to latest)
            install_dependencies: If True, checks and installs any dependencies of the package
            fail_if_exists: If True, raise error if package already loaded

        Raises:
            PackageNotFoundError: If package or version not found
            FHIRPackageRegistryError: If download fails
            RuntimeError: If package processing fails
        """
        if not self._internet_enabled:
            raise RuntimeError(
                f"Cannot load package {package_name} while internet access is disabled"
            )

        # Determine version to load
        target_version = package_version
        if not target_version:
            try:
                target_version = self._package_client.get_latest_version(package_name)
            except (PackageNotFoundError, FHIRPackageRegistryError) as e:
                raise PackageNotFoundError(
                    f"Failed to get latest version for package {package_name}: {e}"
                )

        if not target_version:
            raise PackageNotFoundError(
                f"No latest version found for package {package_name}"
            )

        # Check if already loaded
        package_key = f"{package_name}@{target_version}"
        if package_key in self._loaded_packages and fail_if_exists:
            raise ValueError(f"Package {package_key} is already loaded")

        try:
            # Download and extract package
            result = self._package_client.download_package(
                package_name, target_version, extract=True
            )

            # Ensure we got a TarFile object (should be guaranteed when extract=True)
            if not isinstance(result, tarfile.TarFile):
                raise RuntimeError(
                    f"Expected TarFile object but got {type(result)} when downloading package"
                )

            try:
                self._process_package_tar(
                    result, package_name, target_version, install_dependencies
                )
            finally:
                result.close()

            # Track loaded package
            self._loaded_packages[package_key] = target_version

        except (PackageNotFoundError, FHIRPackageRegistryError) as e:
            raise e
        except Exception as e:
            raise RuntimeError(
                f"Failed to process package {package_name}@{target_version}: {e}"
            )

    def _process_package_tar(
        self,
        tar_file: tarfile.TarFile,
        package_name: str,
        package_version: str,
        install_dependencies: bool = True,
    ) -> None:
        """
        Process a tar file and extract structure definitions.

        Args:
            tar_file: Opened tar file containing the package
            package_name: Name of the package for error reporting
            package_version: Version of the package for error reporting
        """
        structure_def_count = 0
        errors = []

        # First, look for package.json to find dependencies
        if install_dependencies:
            package_json_member = None
            for member in tar_file.getmembers():
                if member.name.endswith("package.json") and member.isfile():
                    package_json_member = member
                    break
            if package_json_member:
                try:
                    package_obj = tar_file.extractfile(package_json_member)
                    if package_obj:
                        content = package_obj.read().decode("utf-8")
                        package_info = json.loads(content)
                        # Download dependencies
                        for dependency, version in package_info.get(
                            "dependencies", {}
                        ).items():
                            # Check if dependency has already been loaded
                            if self.has_package(dependency, version):
                                continue
                            try:
                                self.load_package(
                                    dependency, version, fail_if_exists=False
                                )
                            except Exception as e:
                                errors.append(
                                    f"Failed to download and load dependency {dependency}: {e}"
                                )
                except Exception as e:
                    errors.append(
                        f"Error processing package.json looking for dependencies: {e}"
                    )

        for member in tar_file.getmembers():
            if not member.isfile():
                continue

            # Look for StructureDefinition JSON files
            # Common patterns: package/StructureDefinition-*.json, package/profiles/*.json, etc.
            if member.name.endswith(".json") and (
                "StructureDefinition" in member.name
                or "/profiles/" in member.name
                or "/extensions/" in member.name
                or "/types/" in member.name
            ):
                try:
                    # Extract and parse the file
                    file_obj = tar_file.extractfile(member)
                    if file_obj:
                        content = file_obj.read().decode("utf-8")
                        json_data = json.loads(content)

                        # Check if it's a StructureDefinition resource
                        if json_data.get("resourceType") == "StructureDefinition":
                            structure_def = StructureDefinition.model_validate(
                                json_data
                            )
                            self.add(structure_def)
                            structure_def_count += 1

                except Exception as e:
                    errors.append(f"Error processing {member.name}: {e}")

        if structure_def_count == 0:
            raise RuntimeError(
                f"No StructureDefinition resources found in package {package_name}@{package_version}"
            )

        if errors:
            # Log errors but don't fail if we got some definitions
            error_summary = f"Loaded {structure_def_count} StructureDefinitions with {len(errors)} errors"
            print(f"Warning: {error_summary}")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more errors")

    def get_loaded_packages(self) -> Dict[str, str]:
        """Get a dictionary of loaded packages and their versions."""
        return self._loaded_packages.copy()

    def has_package(
        self, package_name: str, package_version: Optional[str] = None
    ) -> bool:
        """
        Check if a package is loaded.

        Args:
            package_name: Name of the package
            package_version: Version of the package (if None, checks any version)

        Returns:
            True if package is loaded
        """
        if package_version:
            return f"{package_name}@{package_version}" in self._loaded_packages
        else:
            return any(
                key.startswith(f"{package_name}@") for key in self._loaded_packages
            )

    def remove_package(
        self, package_name: str, package_version: Optional[str] = None
    ) -> None:
        """
        Remove a loaded package and all its structure definitions.

        Args:
            package_name: Name of the package
            package_version: Version of the package (if None, removes all versions)
        """
        if package_version:
            package_key = f"{package_name}@{package_version}"
            if package_key in self._loaded_packages:
                del self._loaded_packages[package_key]
        else:
            # Remove all versions of the package
            keys_to_remove = [
                key
                for key in self._loaded_packages
                if key.startswith(f"{package_name}@")
            ]
            for key in keys_to_remove:
                del self._loaded_packages[key]

        # Note: This doesn't remove the actual structure definitions from the local cache
        # as they might be used by other packages or loaded separately.

    def set_registry_base_url(self, base_url: str) -> None:
        """Change the package registry base URL."""
        self._package_client.base_url = base_url

    def clear_local_cache(self) -> None:
        """Clear all locally cached structure definitions."""
        self._local_definitions.clear()
        self._latest_versions.clear()
        self._loaded_packages.clear()


class CompositeStructureDefinitionRepository(AbstractRepository[StructureDefinition]):
    """
    CompositeStructureDefinitionRepository provides a unified interface for managing, retrieving, and caching FHIR
    StructureDefinition resources from multiple sources, including local storage, FHIR packages, and online repositories.

    This repository supports:
        - Local caching of StructureDefinitions, with version tracking and duplicate prevention.
        - Optional integration with FHIR package repositories for bulk loading and management of definitions.
        - Online retrieval of StructureDefinitions when enabled, with automatic local caching of downloaded resources.
        - Utilities for loading definitions from files, directories, or pre-loaded dictionaries.
        - Management of loaded packages, including loading, checking, and removal.
        - Version management, including retrieval of all available versions, the latest version, and removal of specific versions.
    """

    def __init__(
        self,
        internet_enabled: bool = True,
        enable_packages: bool = True,
        registry_base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        # Structure: {base_url: {version: StructureDefinition}}
        self._local_definitions: Dict[str, Dict[str, StructureDefinition]] = {}
        # Track latest versions: {base_url: latest_version}
        self._latest_versions: Dict[str, str] = {}
        self._internet_enabled = internet_enabled
        self._http_repository = HttpStructureDefinitionRepository()

        # Optional package repository
        self._package_repository: Optional[PackageStructureDefinitionRepository] = None
        if enable_packages:
            self._package_repository = PackageStructureDefinitionRepository(
                internet_enabled=internet_enabled,
                registry_base_url=registry_base_url,
                timeout=timeout,
            )

    def get(
        self, canonical_url: str, version: Optional[str] = None
    ) -> StructureDefinition:
        """
        Retrieve a StructureDefinition resource by its canonical URL and optional version.

        This method attempts to find the requested StructureDefinition in the following order:
        1. Local repository: Checks for the resource in the local cache, optionally by version.
        2. Package repository: If available, attempts to retrieve the resource from a package repository.
        3. Internet: If enabled, tries to fetch the resource from an online repository.

        If the resource is found in the package or internet repository, it is cached locally for future use.

        Args:
            canonical_url (str): The canonical URL of the StructureDefinition to retrieve.
            version (Optional[str], optional): The specific version of the StructureDefinition to retrieve.
                If not provided, the latest version is used if available.

        Returns:
            StructureDefinition: The requested StructureDefinition resource.

        Raises:
            RuntimeError: If the StructureDefinition cannot be found in any repository.
        """
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

        # Try package repository if available
        if self._package_repository and self._package_repository.has(
            canonical_url, version
        ):
            try:
                structure_definition = self._package_repository.get(
                    canonical_url, version
                )
                # Cache it locally for future use
                self.add(structure_definition)
                return structure_definition
            except RuntimeError:
                # Package repository couldn't find it, continue to internet fallback
                pass

        # Last chance, lookg for canonical resource definition
        # Try to find the resource in the local FHIR definitions bundle if available
        current_file_path = Path(__file__).resolve()
        profiles_path = (
            current_file_path.parent
            / "definitions"
            / get_FHIR_release_from_version(version or "4.0.0")
            / "profiles-resources.json"
        )
        if profiles_path.exists():
            with open(profiles_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                entry = next(
                    (
                        entry
                        for entry in data["entry"]
                        if entry["resource"]["url"] == canonical_url
                        and entry["resource"]["resourceType"] == "StructureDefinition"
                    ),
                    None,
                )
                if entry:
                    structure_def = StructureDefinition.model_validate(
                        entry["resource"]
                    )
                    self.add(structure_def)
                    return structure_def

        # Fall back to internet if enabled
        if self._internet_enabled:
            structure_definition = self._http_repository.get(canonical_url, version)
            if structure_definition:
                # Cache it locally for future use
                self.add(structure_definition)
                return structure_definition

        version_info = f" version {target_version}" if target_version else ""
        raise StructureDefinitionNotFoundError(
            f"Structure definition not found for {base_url}{version_info}. Either load it locally, load the appropriate package, or enable internet access to download it."
        )

    def add(self, resource: StructureDefinition, fail_if_exists: bool = False) -> None:
        """
        Adds a StructureDefinition to the local repository.

        Args:
            resource (StructureDefinition): The StructureDefinition instance to add.
                Must have a 'url' field, and a version either in the URL or in the 'version' field.
            fail_if_exists (bool, optional): If True, raises a ValueError if a StructureDefinition
                with the same base URL and version already exists in the repository. Defaults to False.

        Raises:
            ValueError: If the StructureDefinition does not have a 'url' field.
            ValueError: If the StructureDefinition does not have a version (in the URL or 'version' field).
            ValueError: If a duplicate StructureDefinition is added and fail_if_exists is True.

        """
        if not resource.url:
            raise ValueError(
                "StructureDefinition must have a 'url' field to be added to the repository."
            )

        base_url, version = self.parse_canonical_url(resource.url)

        # Use the structure definition's version field if no version in URL
        if not version:
            version = resource.version or resource.fhirVersion

        if not version:
            raise ValueError(
                f"StructureDefinition for {base_url} must have a version (either in URL or version field)."
            )

        # Initialize base URL storage if needed
        if base_url not in self._local_definitions:
            self._local_definitions[base_url] = {}

        # Check for duplicates
        if version in self._local_definitions[base_url] and fail_if_exists:
            raise ValueError(
                f"Attempted to load structure definition with duplicated URL {base_url} version {version} in local repository."
            )

        # Store the definition
        self._local_definitions[base_url][version] = resource

        # Update latest version tracking
        self._update_latest_version(base_url, version)

    def has(self, canonical_url: str, version: Optional[str] = None) -> bool:
        """
        Check if a resource with the given canonical URL and optional version exists in the repository.
        This method searches for the resource in the following order:
        1. Local storage: Checks if the resource is available locally, optionally matching the specified version.
        2. Package repository: If configured, checks if the resource exists in the package repository.
        3. HTTP repository: If internet access is enabled, checks if the resource can be found via the HTTP repository.
        Args:
            canonical_url (str): The canonical URL of the resource to check.
            version (Optional[str], optional): The specific version of the resource to check for. Defaults to None.
        Returns:
            bool: True if the resource exists in any of the repositories or can be downloaded; False otherwise.
        """

        base_url, parsed_version = self.parse_canonical_url(canonical_url)
        target_version = version or parsed_version

        # Check local storage
        if base_url in self._local_definitions:
            if target_version:
                if target_version in self._local_definitions[base_url]:
                    return True
            else:
                # Has any version locally
                if self._local_definitions[base_url]:
                    return True

        # Check package repository if available
        if self._package_repository and self._package_repository.has(
            canonical_url, version
        ):
            return True

        # Check if can be downloaded
        return self._internet_enabled and self._http_repository.has(
            canonical_url, version
        )

    def get_versions(self, canonical_url: str) -> List[str]:
        """
        Retrieve all available versions for a given canonical URL.
        Args:
            canonical_url (str): The canonical URL of the resource, possibly including a version.
        Returns:
            List[str]: A sorted list of version strings available for the specified canonical URL.
                Versions are sorted using semantic versioning if possible; otherwise, they are sorted lexicographically.
        """

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
        """
        Retrieve the latest version string for a given FHIR resource canonical URL.
        Args:
            canonical_url (str): The canonical URL of the FHIR resource, possibly including a version.
        Returns:
            Optional[str]: The latest version string associated with the base canonical URL,
                           or None if no version is found.
        """

        base_url, _ = self.parse_canonical_url(canonical_url)
        return self._latest_versions.get(base_url)

    def _update_latest_version(self, base_url: str, new_version: str) -> None:
        """
        Updates the latest version for a given base URL if the new version is greater.
        Compares the provided new_version with the currently stored latest version for the specified base_url.
        Uses semantic versioning for comparison when possible; falls back to string comparison if versions are not valid semantic versions.
        Args:
            base_url (str): The base URL whose latest version is being tracked.
            new_version (str): The new version string to compare and potentially set as the latest.
        Returns:
            None
        """

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
        """
        Loads all JSON structure definitions from the specified directory and adds them to the repository.
        Args:
            directory_path (Union[str, Path]): The path to the directory containing JSON structure definition files.
        Raises:
            FileNotFoundError: If the specified directory does not exist.
            RuntimeError: If an error occurs while loading or adding a structure definition from a file.
        """

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
        """
        Loads FHIR StructureDefinition resources from one or more JSON files and adds them to the repository.
        Args:
            *file_paths (Union[str, Path]): One or more file paths to JSON files containing FHIR StructureDefinition resources.
        Raises:
            RuntimeError: If loading or parsing any of the files fails, a RuntimeError is raised with details about the file and the error.
        """

        for file_path in file_paths:
            try:
                structure_def = self.__load_json_structure_definition(Path(file_path))
                self.add(structure_def)
            except Exception as e:
                raise RuntimeError(f"Failed to load {file_path}: {e}")

    def load_from_definitions(
        self, *definitions: Dict[str, Any] | StructureDefinition
    ) -> None:
        """
        Loads FHIR structure definitions from one or more pre-loaded dictionaries.
        Each dictionary in `definitions` should represent a FHIR StructureDefinition resource.
        The method validates each dictionary and adds the resulting StructureDefinition
        object to the repository.
        Args:
            *definitions (Dict[str, Any]): One or more dictionaries representing FHIR StructureDefinition resources.
        Raises:
            ValidationError: If any of the provided dictionaries do not conform to the StructureDefinition model.
        """

        """Load structure definitions from pre-loaded dictionaries."""
        for structure_def in definitions:
            structure_definition = StructureDefinition.model_validate(structure_def)
            self.add(structure_definition)

    def set_internet_enabled(self, enabled: bool) -> None:
        """
        Enables or disables internet access for the repository and its underlying HTTP repository.
        Args:
            enabled (bool): If True, internet access is enabled; if False, it is disabled.
        """

        self._internet_enabled = enabled
        self._http_repository.set_internet_enabled(enabled)

    def get_loaded_urls(self) -> List[str]:
        """
        Returns a list of URLs for all FHIR definitions currently loaded in the repository.

        Returns:
            List[str]: A list containing the URLs of the loaded FHIR definitions.
        """
        return list(self._local_definitions.keys())

    def get_all_loaded_urls_with_versions(self) -> Dict[str, List[str]]:
        """
        Returns a dictionary mapping each loaded base URL to a list of its available versions.

        Returns:
            Dict[str, List[str]]: A dictionary where the keys are base URLs (str) and the values are lists of version strings (List[str]) associated with each URL.
        """
        return {
            base_url: self.get_versions(base_url)
            for base_url in self._local_definitions.keys()
        }

    def clear_local_cache(self) -> None:
        """
        Clears the local cache of definitions and latest versions.
        This method removes all entries from the internal caches used to store local definitions
        and their latest versions, effectively resetting the local state.
        """
        self._local_definitions.clear()
        self._latest_versions.clear()

    def remove_version(self, canonical_url: str, version: Optional[str] = None) -> None:
        """
        Remove a specific version or all versions of a resource identified by its canonical URL.
        Args:
            canonical_url (str): The canonical URL of the resource, optionally including a version.
            version (Optional[str], optional): The specific version to remove. If not provided, the version is parsed from the canonical URL if present.
                                               If neither is provided, all versions for the base URL are removed.
        Returns:
            None
        Behavior:
            - If a version is specified (either as an argument or in the canonical URL), removes only that version.
            - If the removed version was the latest, updates the latest version to the next available one.
            - If no versions remain for the base URL, cleans up internal data structures.
            - If no version is specified, removes all versions associated with the base URL.
        """

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
        """
        Loads a FHIR StructureDefinition from a JSON file.
        Args:
            file_path (Path): The path to the JSON file containing the StructureDefinition.
        Returns:
            StructureDefinition: The validated StructureDefinition object parsed from the JSON file.
        Raises:
            FileNotFoundError: If the specified file does not exist.
            JSONDecodeError: If the file is not valid JSON.
            ValidationError: If the JSON does not conform to the StructureDefinition model.
        """

        with open(file_path, "r", encoding="utf-8") as file:
            return StructureDefinition.model_validate(json.load(file))

    # Package-specific convenience methods
    def load_package(self, package_name: str, version: Optional[str] = None) -> None:
        """
        Loads a FHIR package into the repository, making its structure definitions available.
        Args:
            package_name (str): The name of the FHIR package to load.
            version (Optional[str], optional): The specific version of the package to load. If None, the latest version is used.
        Raises:
            RuntimeError: If package support is not enabled for this repository.
        Side Effects:
            - Loads the specified package into the internal package repository.
            - Adds any new structure definitions from the package to the local cache, avoiding duplicates.
        """

        if not self._package_repository:
            raise RuntimeError("Package support is not enabled for this repository")

        # Load the package (this modifies the package repository's internal state)
        self._package_repository.load_package(package_name, version)

        # Get all structure definitions from the package repository
        # and add any that aren't already in our local cache
        loaded_definitions = []
        for url in self._package_repository._local_definitions:
            for ver, structure_def in self._package_repository._local_definitions[
                url
            ].items():
                # Check if we already have this exact version locally
                if (
                    url not in self._local_definitions
                    or ver not in self._local_definitions[url]
                ):
                    self.add(structure_def)
                    loaded_definitions.append(structure_def)

    def get_loaded_packages(self) -> Dict[str, str]:
        """
        Returns a dictionary of loaded FHIR packages.

        Returns:
            Dict[str, str]: A dictionary where the keys are package names and the values are their corresponding versions.
        """

        if not self._package_repository:
            return {}
        return self._package_repository.get_loaded_packages()

    def has_package(self, package_name: str, version: Optional[str] = None) -> bool:
        """
        Check if a package with the specified name and optional version exists in the package repository.
        Args:
            package_name (str): The name of the package to check for.
            version (Optional[str], optional): The specific version of the package to check. Defaults to None.
        Returns:
            bool: True if the package (and version, if specified) exists in the repository, False otherwise.
        """

        if not self._package_repository:
            return False
        return self._package_repository.has_package(package_name, version)

    def remove_package(self, package_name: str, version: Optional[str] = None) -> None:
        """
        Remove a package from the package repository.
        Args:
            package_name (str): The name of the package to remove.
            version (Optional[str], optional): The specific version of the package to remove. If None, all versions may be removed. Defaults to None.
        Returns:
            None
        """

        if not self._package_repository:
            return
        self._package_repository.remove_package(package_name, version)

    def set_registry_base_url(self, base_url: str) -> None:
        """
        Sets the base URL for the package registry.
        Args:
            base_url (str): The base URL to be used for the package registry.
        Raises:
            RuntimeError: If package support is not enabled for this repository.
        """

        if not self._package_repository:
            raise RuntimeError("Package support is not enabled for this repository")
        self._package_repository.set_registry_base_url(base_url)

    def clear_package_cache(self) -> None:
        if self._package_repository:
            self._package_repository.clear_local_cache()


# Convenience functions for easy configuration
def configure_repository(
    directory: Optional[Union[str, Path]] = None,
    files: Optional[List[Union[str, Path]]] = None,
    definitions: Optional[List[Dict[str, Any]]] = None,
    internet_enabled: bool = True,
) -> CompositeStructureDefinitionRepository:
    """
    Configures and returns a CompositeStructureDefinitionRepository by loading structure definitions
    from a directory, a list of files, or a list of definition dictionaries.
    Args:
        directory (Optional[Union[str, Path]]): Path to a directory containing structure definition files to load.
        files (Optional[List[Union[str, Path]]]): List of file paths to structure definition files to load.
        definitions (Optional[List[Dict[str, Any]]]): List of structure definition dictionaries to load directly.
        internet_enabled (bool): Whether to enable internet access for the repository (default is True).
    Returns:
        CompositeStructureDefinitionRepository: The configured repository with the loaded structure definitions.
    """
    repo = CompositeStructureDefinitionRepository(internet_enabled=internet_enabled)

    if directory:
        repo.load_from_directory(directory)

    if files:
        repo.load_from_files(*files)

    if definitions:
        repo.load_from_definitions(*definitions)

    return repo
