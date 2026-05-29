"""Lightweight client for FHIR Package Registry API."""

import io
import tarfile
from typing import Optional, Union
from urllib.parse import urljoin

import requests
from pydantic import ValidationError
import json

from .models import PackageMetadata
from fhircraft.exceptions import (
    PackageException,
    PackageNotFoundError,
    PackageResolutionError,
)


class FHIRPackageRegistryClient:
    """
    Lightweight client for the FHIR Package Registry API.

    Supports both packages.simplifier.net and packages.fhir.org endpoints.
    """

    SIMPLIFIER_BASE_URL = "https://packages.simplifier.net"
    FHIR_ORG_BASE_URL = "https://packages.fhir.org"

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        session: Optional[requests.Session] = None,
    ):
        """
        Initialize the FHIR Package Registry client.

        Args:
            base_url (Optional[str]): Base URL for the API. Defaults to packages.simplifier.net
            timeout (float): Request timeout in seconds
            session (Optional[requests.Session]): Optional requests session to use
        """
        self.base_url = base_url or self.FHIR_ORG_BASE_URL
        self.timeout = timeout
        self.session = session or requests.Session()
        self.history = set()  # To track loaded packages and avoid duplicates

        # Set default headers
        self.session.headers.update(
            {
                "User-Agent": "fhircraft-package-client/1.0.0",
                "Accept": "application/json",
            }
        )

    def list_package_versions(self, package_name: str) -> PackageMetadata:
        """
        List all versions for a package.

        Args:
            package_name (str): Name of the package (e.g., "hl7.fhir.us.core")

        Returns:
            (PackageMetadata) Package metadata object with all available versions

        Raises:
            PackageNotFoundError: If the package is not found
            PackageResolutionError: For other API errors
        """
        url = urljoin(self.base_url + "/", package_name)

        try:
            response = self.session.get(url, timeout=self.timeout)

            if response.status_code == 404:
                raise PackageNotFoundError(f"Package '{package_name}' not found")

            response.raise_for_status()

            try:
                return PackageMetadata.model_validate(response.json())
            except ValidationError as e:
                raise PackageResolutionError(f"Invalid response format: {e}")

        except requests.RequestException as e:
            raise PackageResolutionError(f"Request failed: {e}")

    def download_package(
        self, package_name: str, package_version: str, extract: bool = False
    ) -> Union[bytes, tarfile.TarFile]:
        """
        Download a specific package version.

        Args:
            package_name (str): Name of the package
            package_version (str): Version of the package
            extract (bool): If True, return extracted TarFile object, otherwise raw bytes

        Returns:
            (TarFile) Raw tar.gz bytes or extracted TarFile object

        Raises:
            PackageNotFoundError: If the package or version is not found
            PackageResolutionError: For other API errors
        """
        url = urljoin(self.base_url + "/", f"{package_name}/{package_version}")

        try:
            # Use different Accept header for binary download
            headers = {"Accept": "application/tar+gzip"}
            response = self.session.get(url, headers=headers, timeout=self.timeout)

            if response.status_code == 404:
                raise PackageNotFoundError(
                    f"Package '{package_name}' version '{package_version}' not found"
                )

            response.raise_for_status()
            self.history.add(f"{package_name}@{package_version}")
            if extract:
                # Return extracted tarfile
                return tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz")
            else:
                # Return raw bytes
                return response.content

        except requests.RequestException as e:
            raise PackageResolutionError(f"Download failed: {e}")

    def get_latest_version(self, package_name: str) -> Optional[str]:
        """
        Get the latest version tag for a package.

        Args:
            package_name (str): Name of the package

        Returns:
            (str | None) Latest version string or None if not available
        """
        metadata = self.list_package_versions(package_name)
        return metadata.dist_tags.latest if metadata.dist_tags else None

    def download_latest_package(
        self, package_name: str, extract: bool = False
    ) -> Union[bytes, tarfile.TarFile]:
        """
        Download the latest version of a package.

        Args:
            package_name (str): Name of the package
            extract (bool): If True, return extracted TarFile object, otherwise raw bytes

        Returns:
            (Union[bytes, tarfile.TarFile]) Raw tar.gz bytes or extracted TarFile object

        Raises:
            PackageNotFoundError: If the package is not found or has no latest version
            FHIRPackageResolutionError: For other API errors
        """
        latest_version = self.get_latest_version(package_name)
        if not latest_version:
            raise PackageNotFoundError(
                f"No latest version found for package '{package_name}'"
            )

        return self.download_package(package_name, latest_version, extract=extract)

    def load_resources_from_package(
        self,
        target_resource: str,
        package_name: str,
        package_version: Optional[str] = None,
        install_dependencies: bool = True,
        fail_if_exists: bool = False,
    ) -> list[dict]:
        """
        Load a FHIR package from the registry and add all structure definitions.

        Args:
            package_name: Name of the package (e.g., "hl7.fhir.us.core")
            package_version: Version of the package (defaults to latest)
            install_dependencies: If True, checks and installs any dependencies of the package
            fail_if_exists: If True, raise error if package already loaded

        Raises:
            PackageNotFoundError: If package or version not found
            FHIRPackageResolutionError: If download fails
            RuntimeError: If package processing fails
        """

        # Determine version to load
        target_version = package_version
        if not target_version:
            try:
                target_version = self.get_latest_version(package_name)
            except (PackageNotFoundError, PackageResolutionError) as e:
                raise PackageNotFoundError(
                    f"Failed to get latest version for package {package_name}: {e}"
                )

        if not target_version:
            raise PackageNotFoundError(
                f"No latest version found for package {package_name}"
            )

        # Check if already loaded
        package_key = f"{package_name}@{target_version}"
        try:
            # Download and extract package
            result = self.download_package(package_name, target_version, extract=True)

            # Ensure we got a TarFile object (should be guaranteed when extract=True)
            if not isinstance(result, tarfile.TarFile):
                raise RuntimeError(
                    f"Expected TarFile object but got {type(result)} when downloading package"
                )

            try:
                results, errors = self._process_package_tar(
                    target_resource,
                    result,
                    install_dependencies,
                )

                if len(results) == 0:
                    raise RuntimeError(
                        f"No valid resources ({target_resource}) found in package"
                    )

                if errors:
                    # Log errors but don't fail if we got some definitions
                    error_summary = f"Loaded {len(results)} {target_resource} resources with {len(errors)} errors"
                    print(f"Warning: {error_summary}")
                    for error in errors[:5]:  # Show first 5 errors
                        print(f"  - {error}")
                    if len(errors) > 5:
                        print(f"  ... and {len(errors) - 5} more errors")

                return results

            except (PackageNotFoundError, PackageResolutionError) as e:
                raise e
        except Exception as e:
            raise RuntimeError(f"Failed to process package {package_key}: {e}")

    def _process_package_tar(
        self,
        target_resource: str,
        tar_file: tarfile.TarFile,
        install_dependencies: bool = True,
    ) -> tuple[list[dict], list[str]]:
        """
        Process a tar file and extract structure definitions.

        Args:
            tar_file: Opened tar file containing the package
        """
        errors = []
        results = []

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
                            if f"{dependency}@{version}" in self.history:
                                continue
                            try:
                                dependency_results = self.load_resources_from_package(
                                    target_resource,
                                    dependency,
                                    version,
                                    fail_if_exists=False,
                                )
                                results.extend(dependency_results)
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
                target_resource in member.name
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
                        if json_data.get("resourceType") == target_resource:
                            results.append(json_data)

                except Exception as e:
                    errors.append(f"Error processing {member.name}: {e}")

        return results, errors


# Convenience functions for common use cases
def get_package_metadata(
    package_name: str, base_url: Optional[str] = None
) -> PackageMetadata:
    """
    Convenience function to get package metadata.

    Args:
        package_name (str): Name of the package
        base_url (Optional[str]): Optional base URL (defaults to packages.simplifier.net)

    Returns:
        (PackageMetadata) Metadata of the package
    """
    client = FHIRPackageRegistryClient(base_url=base_url)
    return client.list_package_versions(package_name)


def download_package(
    package_name: str,
    package_version: str,
    base_url: Optional[str] = None,
    extract: bool = False,
) -> Union[bytes, tarfile.TarFile]:
    """
    Convenience function to download a package.

    Args:
        package_name (str): Name of the package
        package_version (str): Version of the package
        base_url (Optional[str]): Optional base URL (defaults to packages.simplifier.net)
        extract (bool): If True, return extracted TarFile object, otherwise raw bytes

    Returns:
        (Union[bytes, tarfile.TarFile]) Raw tar.gz bytes or extracted TarFile object
    """
    client = FHIRPackageRegistryClient(base_url=base_url)
    return client.download_package(package_name, package_version, extract=extract)


def download_latest_package(
    package_name: str, base_url: Optional[str] = None, extract: bool = False
) -> Union[bytes, tarfile.TarFile]:
    """
    Convenience function to download the latest version of a package.

    Args:
        package_name (str): Name of the package
        base_url (Optional[str]): Optional base URL (defaults to packages.simplifier.net)
        extract (bool): If True, return extracted TarFile object, otherwise raw bytes

    Returns:
        (Union[bytes, tarfile.TarFile]) Raw tar.gz bytes or extracted TarFile object
    """
    client = FHIRPackageRegistryClient(base_url=base_url)
    return client.download_latest_package(package_name, extract=extract)
