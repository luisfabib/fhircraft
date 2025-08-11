"""Lightweight client for FHIR Package Registry API."""

import io
import tarfile
from typing import Optional, Union
from urllib.parse import urljoin

import requests
from pydantic import ValidationError

from .models import PackageMetadata


class FHIRPackageRegistryError(Exception):
    """Base exception for FHIR Package Registry client errors."""

    pass


class PackageNotFoundError(FHIRPackageRegistryError):
    """Raised when a package is not found."""

    pass


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
            FHIRPackageRegistryError: For other API errors
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
                raise FHIRPackageRegistryError(f"Invalid response format: {e}")

        except requests.RequestException as e:
            raise FHIRPackageRegistryError(f"Request failed: {e}")

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
            FHIRPackageRegistryError: For other API errors
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

            if extract:
                # Return extracted tarfile
                return tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz")
            else:
                # Return raw bytes
                return response.content

        except requests.RequestException as e:
            raise FHIRPackageRegistryError(f"Download failed: {e}")

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
            FHIRPackageRegistryError: For other API errors
        """
        latest_version = self.get_latest_version(package_name)
        if not latest_version:
            raise PackageNotFoundError(
                f"No latest version found for package '{package_name}'"
            )

        return self.download_package(package_name, latest_version, extract=extract)


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
