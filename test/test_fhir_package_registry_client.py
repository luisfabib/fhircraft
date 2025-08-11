"""Tests for FHIR Package Registry client."""

import json
from unittest.mock import Mock, patch

import pytest

from fhircraft.fhir.packages import (
    FHIRPackageRegistryClient,
    FHIRPackageRegistryError,
    PackageMetadata,
    PackageNotFoundError,
)


class TestFHIRPackageRegistryClient:
    """Test cases for FHIRPackageRegistryClient."""

    def test_client_initialization(self):
        """Test client initialization with default and custom parameters."""
        # Default initialization
        client = FHIRPackageRegistryClient()
        assert client.base_url == FHIRPackageRegistryClient.FHIR_ORG_BASE_URL
        assert client.timeout == 30.0

        # Custom initialization
        custom_url = "https://custom.registry.com"
        client = FHIRPackageRegistryClient(base_url=custom_url, timeout=60.0)
        assert client.base_url == custom_url
        assert client.timeout == 60.0

    @patch("requests.Session.get")
    def test_list_package_versions_success(self, mock_get):
        """Test successful package version listing."""
        # Mock response data
        mock_response_data = {
            "_id": "hl7.fhir.us.core",
            "name": "hl7.fhir.us.core",
            "dist-tags": {"latest": "3.1.1"},
            "versions": {
                "3.1.1": {
                    "name": "hl7.fhir.us.core",
                    "version": "3.1.1",
                    "description": "US Core Implementation Guide",
                    "fhirVersion": "R4",
                }
            },
        }

        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        result = client.list_package_versions("hl7.fhir.us.core")

        # Assertions
        assert isinstance(result, PackageMetadata)
        assert result.id == "hl7.fhir.us.core"
        assert result.name == "hl7.fhir.us.core"
        assert result.dist_tags is not None
        assert result.dist_tags.latest == "3.1.1"
        assert result.versions is not None
        assert "3.1.1" in result.versions

    @patch("requests.Session.get")
    def test_list_package_versions_not_found(self, mock_get):
        """Test package not found error."""
        # Setup mock for 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        with pytest.raises(PackageNotFoundError) as exc_info:
            client.list_package_versions("nonexistent.package")

        assert "not found" in str(exc_info.value)

    @patch("requests.Session.get")
    def test_download_package_success(self, mock_get):
        """Test successful package download."""
        # Mock binary response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake-tar-gz-content"
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        result = client.download_package("hl7.fhir.us.core", "3.1.1")

        # Assertions
        assert isinstance(result, bytes)
        assert result == b"fake-tar-gz-content"

    @patch("requests.Session.get")
    def test_download_package_not_found(self, mock_get):
        """Test package download not found error."""
        # Setup mock for 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        with pytest.raises(PackageNotFoundError) as exc_info:
            client.download_package("nonexistent.package", "1.0.0")

        assert "not found" in str(exc_info.value)

    @patch("requests.Session.get")
    def test_get_latest_version(self, mock_get):
        """Test getting latest version."""
        # Mock response data
        mock_response_data = {
            "_id": "hl7.fhir.us.core",
            "name": "hl7.fhir.us.core",
            "dist-tags": {"latest": "3.1.1"},
        }

        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        latest = client.get_latest_version("hl7.fhir.us.core")

        # Assertions
        assert latest == "3.1.1"

    @patch("requests.Session.get")
    def test_get_latest_version_no_tags(self, mock_get):
        """Test getting latest version when no dist-tags exist."""
        # Mock response data without dist-tags
        mock_response_data = {"_id": "hl7.fhir.us.core", "name": "hl7.fhir.us.core"}

        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        latest = client.get_latest_version("hl7.fhir.us.core")

        # Assertions
        assert latest is None


class TestPackageMetadata:
    """Test cases for PackageMetadata model."""

    def test_package_metadata_validation(self):
        """Test PackageMetadata validation with valid data."""
        data = {
            "_id": "hl7.fhir.us.core",
            "name": "hl7.fhir.us.core",
            "dist-tags": {"latest": "3.1.1"},
            "versions": {
                "3.1.1": {
                    "name": "hl7.fhir.us.core",
                    "version": "3.1.1",
                    "description": "US Core Implementation Guide",
                    "fhirVersion": "R4",
                }
            },
        }

        metadata = PackageMetadata.model_validate(data)
        assert metadata.id == "hl7.fhir.us.core"
        assert metadata.name == "hl7.fhir.us.core"
        assert metadata.dist_tags is not None
        assert metadata.dist_tags.latest == "3.1.1"
        assert metadata.versions is not None
        assert "3.1.1" in metadata.versions

    def test_package_metadata_minimal(self):
        """Test PackageMetadata with minimal data."""
        data = {}
        metadata = PackageMetadata.model_validate(data)

        # All fields should be optional
        assert metadata.id is None
        assert metadata.name is None
        assert metadata.dist_tags is None
        assert metadata.versions is None
        assert metadata.versions is None
