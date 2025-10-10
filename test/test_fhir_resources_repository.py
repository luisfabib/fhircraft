#!/usr/bin/env python
"""
Test cases for Structure Definition Repository
"""

import json
import tarfile
import tempfile
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock, Mock, mock_open, patch

import tarfile
import json
from unittest import mock
import pytest
import io 
from fhircraft.fhir.resources.repository import PackageStructureDefinitionRepository
from fhircraft.fhir.resources.definitions import StructureDefinition

import pytest

from fhircraft.fhir.packages import FHIRPackageRegistryError, PackageNotFoundError
from fhircraft.fhir.resources.definitions import StructureDefinition
from fhircraft.fhir.resources.repository import (
    CompositeStructureDefinitionRepository,
    HttpStructureDefinitionRepository,
    PackageStructureDefinitionRepository,
    configure_repository,
)

# Sample structure definition data for testing
SAMPLE_PATIENT_R4 = {
    "resourceType": "StructureDefinition",
    "url": "http://hl7.org/fhir/StructureDefinition/Patient",
    "version": "4.0.0",
    "name": "Patient",
    "status": "active",
    "kind": "resource",
    "abstract": False,
    "type": "Patient",
    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/DomainResource",
    "derivation": "specialization",
    "snapshot": {
        "element": [
            {
                "id": "Patient",
                "path": "Patient",
                "definition": "Demographics and other administrative information about an individual or animal receiving care or other health-related services.",
                "min": 0,
                "max": "*",
                "base": {"path": "Patient", "min": 0, "max": "*"},
                "constraint": [
                    {
                        "key": "dom-2",
                        "severity": "error",
                        "human": "If the resource is contained in another resource, it SHALL NOT contain nested Resources",
                        "expression": "contained.contained.empty()",
                    }
                ],
                "isModifier": False,
            }
        ]
    },
}

SAMPLE_PATIENT_R4B = {
    "resourceType": "StructureDefinition",
    "url": "http://hl7.org/fhir/StructureDefinition/Patient",
    "version": "4.3.0",
    "name": "Patient",
    "status": "active",
    "kind": "resource",
    "abstract": False,
    "type": "Patient",
    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/DomainResource",
    "derivation": "specialization",
    "snapshot": {
        "element": [
            {
                "id": "Patient",
                "path": "Patient",
                "definition": "Demographics and other administrative information about an individual or animal receiving care or other health-related services.",
                "min": 0,
                "max": "*",
                "base": {"path": "Patient", "min": 0, "max": "*"},
                "constraint": [
                    {
                        "key": "dom-2",
                        "severity": "error",
                        "human": "If the resource is contained in another resource, it SHALL NOT contain nested Resources",
                        "expression": "contained.contained.empty()",
                    }
                ],
                "isModifier": False,
            }
        ]
    },
}

SAMPLE_OBSERVATION = {
    "resourceType": "StructureDefinition",
    "url": "http://hl7.org/fhir/StructureDefinition/Observation",
    "version": "4.0.0",
    "name": "Observation",
    "status": "active",
    "kind": "resource",
    "abstract": False,
    "type": "Observation",
    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/DomainResource",
    "derivation": "specialization",
    "snapshot": {
        "element": [
            {
                "id": "Observation",
                "path": "Observation",
                "definition": "Measurements and simple assertions made about a patient, device or other subject.",
                "min": 0,
                "max": "*",
                "base": {"path": "Observation", "min": 0, "max": "*"},
                "constraint": [
                    {
                        "key": "obs-6",
                        "severity": "error",
                        "human": "dataAbsentReason SHALL only be present if Observation.value[x] is not present",
                        "expression": "dataAbsentReason.empty() or value.empty()",
                    }
                ],
                "isModifier": False,
            }
        ]
    },
}


class TestStructureDefinitionRepository:
    """Test cases for the repository functionality."""

    @pytest.fixture
    def empty_repository(self):
        """Create an empty repository for testing."""
        return CompositeStructureDefinitionRepository(internet_enabled=False)

    @pytest.fixture
    def populated_repository(self):
        """Create a repository with sample data."""
        repo = CompositeStructureDefinitionRepository(internet_enabled=False)

        # Add different versions of Patient
        patient_r4 = StructureDefinition.model_validate(SAMPLE_PATIENT_R4)
        patient_r4b = StructureDefinition.model_validate(SAMPLE_PATIENT_R4B)
        observation = StructureDefinition.model_validate(SAMPLE_OBSERVATION)

        repo.add(patient_r4)
        repo.add(patient_r4b)
        repo.add(observation)

        return repo

    def test_parse_canonical_url(self):
        """Test URL parsing functionality."""
        # Test URL without version
        base_url, version = CompositeStructureDefinitionRepository.parse_canonical_url(
            "http://hl7.org/fhir/StructureDefinition/Patient"
        )
        assert base_url == "http://hl7.org/fhir/StructureDefinition/Patient"
        assert version is None

        # Test URL with version
        base_url, version = CompositeStructureDefinitionRepository.parse_canonical_url(
            "http://hl7.org/fhir/StructureDefinition/Patient|4.0.0"
        )
        assert base_url == "http://hl7.org/fhir/StructureDefinition/Patient"
        assert version == "4.0.0"

        # Test URL with whitespace
        base_url, version = CompositeStructureDefinitionRepository.parse_canonical_url(
            " http://hl7.org/fhir/StructureDefinition/Patient | 4.0.0 "
        )
        assert base_url == "http://hl7.org/fhir/StructureDefinition/Patient"
        assert version == "4.0.0"

    def test_format_canonical_url(self):
        """Test URL formatting functionality."""
        # Test without version
        url = CompositeStructureDefinitionRepository.format_canonical_url(
            "http://hl7.org/fhir/StructureDefinition/Patient"
        )
        assert url == "http://hl7.org/fhir/StructureDefinition/Patient"

        # Test with version
        url = CompositeStructureDefinitionRepository.format_canonical_url(
            "http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0"
        )
        assert url == "http://hl7.org/fhir/StructureDefinition/Patient|4.0.0"

    def test_add_structure_definition(self, empty_repository):
        """Test adding structure definitions."""
        repo = empty_repository
        patient = StructureDefinition.model_validate(SAMPLE_PATIENT_R4)

        # Test successful addition
        repo.add(patient)
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")

    def test_add_duplicate_version(self, empty_repository):
        """Test adding duplicate versions raises error."""
        repo = empty_repository
        patient = StructureDefinition.model_validate(SAMPLE_PATIENT_R4)

        repo.add(patient)

        # Adding same version should raise error
        with pytest.raises(ValueError, match="duplicated URL"):
            repo.add(patient, fail_if_exists=True)

    def test_add_without_version(self, empty_repository):
        """Test adding structure definition without version raises error."""
        repo = empty_repository
        invalid_data = SAMPLE_PATIENT_R4.copy()
        del invalid_data["version"]

        patient = StructureDefinition.model_validate(invalid_data)

        with pytest.raises(ValueError, match="must have a version"):
            repo.add(patient)

    def test_add_without_url(self, empty_repository):
        """Test adding structure definition without URL raises error."""
        repo = empty_repository
        invalid_data = SAMPLE_PATIENT_R4.copy()
        del invalid_data["url"]

        # This should fail at StructureDefinition validation level
        with pytest.raises(Exception):
            StructureDefinition.model_validate(invalid_data)

    def test_get_structure_definition(self, populated_repository):
        """Test retrieving structure definitions."""
        repo = populated_repository

        # Test getting specific version
        patient_r4 = repo.get(
            "http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0"
        )
        assert patient_r4.version == "4.0.0"

        patient_r4b = repo.get(
            "http://hl7.org/fhir/StructureDefinition/Patient", "4.3.0"
        )
        assert patient_r4b.version == "4.3.0"

        # Test getting latest version (should be 4.3.0)
        patient_latest = repo.get("http://hl7.org/fhir/StructureDefinition/Patient")
        assert patient_latest.version == "4.3.0"

    def test_get_structure_definition_with_versioned_url(self, populated_repository):
        """Test retrieving structure definitions using versioned URLs."""
        repo = populated_repository

        # Test versioned URL
        patient = repo.get("http://hl7.org/fhir/StructureDefinition/Patient|4.0.0")
        assert patient.version == "4.0.0"

    def test_get_nonexistent_structure_definition(self, empty_repository):
        """Test retrieving non-existent structure definition raises error."""
        repo = empty_repository

        with pytest.raises(Exception):
            repo.get("http://hl7.org/fhir/StructureDefinition/NonExistent")

    def test_has_structure_definition(self, populated_repository):
        """Test checking if structure definitions exist."""
        repo = populated_repository

        # Test existing definitions
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.3.0")
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Observation")

        # Test non-existing definitions
        assert not repo.has("http://hl7.org/fhir/StructureDefinition/NonExistent")
        assert not repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "5.0.0")

    def test_get_versions(self, populated_repository):
        """Test getting all versions for a URL."""
        repo = populated_repository

        # Test Patient versions (should be sorted)
        versions = repo.get_versions("http://hl7.org/fhir/StructureDefinition/Patient")
        assert versions == ["4.0.0", "4.3.0"]

        # Test Observation versions
        versions = repo.get_versions(
            "http://hl7.org/fhir/StructureDefinition/Observation"
        )
        assert versions == ["4.0.0"]

        # Test non-existent URL
        versions = repo.get_versions(
            "http://hl7.org/fhir/StructureDefinition/NonExistent"
        )
        assert versions == []

    def test_get_latest_version(self, populated_repository):
        """Test getting latest version for a URL."""
        repo = populated_repository

        # Test Patient latest version
        latest = repo.get_latest_version(
            "http://hl7.org/fhir/StructureDefinition/Patient"
        )
        assert latest == "4.3.0"

        # Test Observation latest version
        latest = repo.get_latest_version(
            "http://hl7.org/fhir/StructureDefinition/Observation"
        )
        assert latest == "4.0.0"

        # Test non-existent URL
        latest = repo.get_latest_version(
            "http://hl7.org/fhir/StructureDefinition/NonExistent"
        )
        assert latest is None

    def test_remove_version(self, populated_repository):
        """Test removing specific versions."""
        repo = populated_repository

        # Remove specific version
        repo.remove_version("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")

        assert not repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.3.0")

        # Latest version should still be 4.3.0
        latest = repo.get_latest_version(
            "http://hl7.org/fhir/StructureDefinition/Patient"
        )
        assert latest == "4.3.0"

    def test_remove_latest_version(self, populated_repository):
        """Test removing latest version updates tracking."""
        repo = populated_repository

        # Remove latest version (4.3.0)
        repo.remove_version("http://hl7.org/fhir/StructureDefinition/Patient", "4.3.0")

        # Latest should now be 4.0.0
        latest = repo.get_latest_version(
            "http://hl7.org/fhir/StructureDefinition/Patient"
        )
        assert latest == "4.0.0"

    def test_remove_all_versions(self, populated_repository):
        """Test removing all versions of a URL."""
        repo = populated_repository

        # Remove all versions
        repo.remove_version("http://hl7.org/fhir/StructureDefinition/Patient")

        assert not repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
        assert (
            repo.get_latest_version("http://hl7.org/fhir/StructureDefinition/Patient")
            is None
        )

    def test_clear_local_cache(self, populated_repository):
        """Test clearing the local cache."""
        repo = populated_repository

        # Verify repository has data
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient")

        # Clear cache
        repo.clear_local_cache()

        # Verify repository is empty
        assert not repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
        assert repo.get_loaded_urls() == []

    def test_get_loaded_urls(self, populated_repository):
        """Test getting all loaded URLs."""
        repo = populated_repository

        urls = repo.get_loaded_urls()
        assert "http://hl7.org/fhir/StructureDefinition/Patient" in urls
        assert "http://hl7.org/fhir/StructureDefinition/Observation" in urls
        assert len(urls) == 2

    def test_get_all_loaded_urls_with_versions(self, populated_repository):
        """Test getting all URLs with their versions."""
        repo = populated_repository

        urls_with_versions = repo.get_all_loaded_urls_with_versions()

        patient_versions = urls_with_versions[
            "http://hl7.org/fhir/StructureDefinition/Patient"
        ]
        assert patient_versions == ["4.0.0", "4.3.0"]

        observation_versions = urls_with_versions[
            "http://hl7.org/fhir/StructureDefinition/Observation"
        ]
        assert observation_versions == ["4.0.0"]

    def test_load_from_definitions(self, empty_repository):
        """Test loading from pre-loaded definitions."""
        repo = empty_repository

        repo.load_from_definitions(SAMPLE_PATIENT_R4, SAMPLE_OBSERVATION)

        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Observation")

    def test_load_from_files(self, empty_repository):
        """Test loading from files."""
        repo = empty_repository

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f1:
            json.dump(SAMPLE_PATIENT_R4, f1)
            f1_path = f1.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f2:
            json.dump(SAMPLE_OBSERVATION, f2)
            f2_path = f2.name

        try:
            repo.load_from_files(f1_path, f2_path)

            assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
            assert repo.has("http://hl7.org/fhir/StructureDefinition/Observation")
        finally:
            # Clean up temporary files
            Path(f1_path).unlink()
            Path(f2_path).unlink()

    def test_load_from_directory(self, empty_repository):
        """Test loading from directory."""
        repo = empty_repository

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files
            (temp_path / "patient.json").write_text(json.dumps(SAMPLE_PATIENT_R4))
            (temp_path / "observation.json").write_text(json.dumps(SAMPLE_OBSERVATION))
            (temp_path / "not_json.txt").write_text("not a json file")

            repo.load_from_directory(temp_path)

            assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
            assert repo.has("http://hl7.org/fhir/StructureDefinition/Observation")

    def test_load_from_nonexistent_directory(self, empty_repository):
        """Test loading from non-existent directory raises error."""
        repo = empty_repository

        with pytest.raises(FileNotFoundError):
            repo.load_from_directory("/nonexistent/directory")

    def test_internet_enabled_toggle(self):
        """Test enabling/disabling internet access."""
        repo = CompositeStructureDefinitionRepository(internet_enabled=True)

        # Initially enabled
        assert repo._internet_enabled is True

        # Disable
        repo.set_internet_enabled(False)
        assert repo._internet_enabled is False

        # Enable
        repo.set_internet_enabled(True)
        assert repo._internet_enabled is True

    @patch("requests.get")
    def test_http_repository_download(self, mock_get):
        """Test HTTP repository downloading."""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_PATIENT_R4
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        http_repo = HttpStructureDefinitionRepository()

        result = http_repo.get("http://hl7.org/fhir/StructureDefinition/Patient")

        assert result.url == "http://hl7.org/fhir/StructureDefinition/Patient"
        assert result.version == "4.0.0"

    def test_http_repository_disabled_internet(self):
        """Test HTTP repository with disabled internet."""
        http_repo = HttpStructureDefinitionRepository()
        http_repo.set_internet_enabled(False)

        with pytest.raises(RuntimeError, match="internet access is disabled"):
            http_repo.get("http://hl7.org/fhir/StructureDefinition/Patient")

    def test_configure_repository_function(self):
        """Test the configure_repository convenience function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test file
            (temp_path / "patient.json").write_text(json.dumps(SAMPLE_PATIENT_R4))

            # Test configuration
            repo = configure_repository(
                directory=temp_path,
                definitions=[SAMPLE_OBSERVATION],
                internet_enabled=False,
            )

            assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
            assert repo.has("http://hl7.org/fhir/StructureDefinition/Observation")
            assert repo._internet_enabled is False


class TestPackageStructureDefinitionRepository:
    """Test cases for the PackageStructureDefinitionRepository functionality."""

    @pytest.fixture
    def package_repository(self):
        """Create a package repository for testing."""
        return PackageStructureDefinitionRepository(internet_enabled=False)

    @pytest.fixture
    def mock_package_tar(self):
        """Create a mock tar file with sample StructureDefinition."""
        # Create a mock tar file with a sample StructureDefinition
        mock_tar = MagicMock(spec=tarfile.TarFile)

        # Mock tar member
        mock_member = MagicMock()
        mock_member.isfile.return_value = True
        mock_member.name = "package/StructureDefinition-Patient.json"

        # Mock file content
        mock_file = MagicMock()
        mock_file.read.return_value = json.dumps(SAMPLE_PATIENT_R4).encode("utf-8")

        mock_tar.getmembers.return_value = [mock_member]
        mock_tar.extractfile.return_value = mock_file

        return mock_tar

    def test_package_repository_initialization(self):
        """Test PackageStructureDefinitionRepository initialization."""
        # Test default initialization
        repo = PackageStructureDefinitionRepository()
        assert repo._internet_enabled is True
        assert isinstance(repo._loaded_packages, dict)
        assert len(repo._loaded_packages) == 0

        # Test with disabled internet
        repo_no_internet = PackageStructureDefinitionRepository(internet_enabled=False)
        assert repo_no_internet._internet_enabled is False

        # Test with custom registry URL
        repo_custom = PackageStructureDefinitionRepository(
            registry_base_url="https://custom.registry.com"
        )
        assert repo_custom._package_client.base_url == "https://custom.registry.com"

    def test_package_repository_add_and_get(self, package_repository):
        """Test adding and retrieving structure definitions in package repository."""
        repo = package_repository
        patient = StructureDefinition.model_validate(SAMPLE_PATIENT_R4)

        # Add structure definition
        repo.add(patient)

        # Test retrieval
        retrieved = repo.get("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")
        assert retrieved.url == patient.url
        assert retrieved.version == patient.version

        # Test retrieval without version (should get latest)
        retrieved_latest = repo.get("http://hl7.org/fhir/StructureDefinition/Patient")
        assert retrieved_latest.version == "4.0.0"

    def test_package_repository_has(self, package_repository):
        """Test checking existence of structure definitions in package repository."""
        repo = package_repository
        patient = StructureDefinition.model_validate(SAMPLE_PATIENT_R4)

        # Initially should not exist
        assert not repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
        assert not repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")

        # After adding should exist
        repo.add(patient)
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")
        assert not repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "5.0.0")

    def test_package_repository_load_package_internet_disabled(
        self, package_repository
    ):
        """Test that loading package fails when internet is disabled."""
        repo = package_repository

        with pytest.raises(RuntimeError, match="internet access is disabled"):
            repo.load_package("test.package")

    @patch("fhircraft.fhir.packages.client.FHIRPackageRegistryClient.download_package")
    def test_package_repository_load_package_success(
        self, mock_download, package_repository, mock_package_tar
    ):
        """Test successful package loading."""
        repo = package_repository
        repo._internet_enabled = True  # Enable internet for this test

        # Mock the download to return our mock tar file
        mock_download.return_value = mock_package_tar

        # Load package
        repo.load_package("test.package", "1.0.0")

        # Verify download was called
        mock_download.assert_called_once_with("test.package", "1.0.0", extract=True)

        # Verify structure definition was loaded
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")

        # Verify package is tracked
        assert "test.package@1.0.0" in repo.get_loaded_packages()

    def test_package_repository_has_package(self, package_repository):
        """Test checking if packages are loaded."""
        repo = package_repository

        # Initially no packages
        assert not repo.has_package("test.package")
        assert not repo.has_package("test.package", "1.0.0")

        # Manually add a package to loaded packages
        repo._loaded_packages["test.package@1.0.0"] = "1.0.0"

        # Now should exist
        assert repo.has_package("test.package")
        assert repo.has_package("test.package", "1.0.0")
        assert not repo.has_package("test.package", "2.0.0")

    def test_package_repository_remove_package(self, package_repository):
        """Test removing loaded packages."""
        repo = package_repository

        # Add some packages
        repo._loaded_packages["test.package@1.0.0"] = "1.0.0"
        repo._loaded_packages["test.package@2.0.0"] = "2.0.0"
        repo._loaded_packages["other.package@1.0.0"] = "1.0.0"

        # Remove specific version
        repo.remove_package("test.package", "1.0.0")
        assert not repo.has_package("test.package", "1.0.0")
        assert repo.has_package("test.package", "2.0.0")
        assert repo.has_package("other.package", "1.0.0")

        # Remove all versions of a package
        repo.remove_package("test.package")
        assert not repo.has_package("test.package")
        assert repo.has_package("other.package", "1.0.0")

    def test_package_repository_get_loaded_packages(self, package_repository):
        """Test getting loaded packages."""
        repo = package_repository

        # Initially empty
        packages = repo.get_loaded_packages()
        assert isinstance(packages, dict)
        assert len(packages) == 0

        # Add some packages
        repo._loaded_packages["test.package@1.0.0"] = "1.0.0"
        repo._loaded_packages["other.package@2.0.0"] = "2.0.0"

        packages = repo.get_loaded_packages()
        assert len(packages) == 2
        assert "test.package@1.0.0" in packages
        assert "other.package@2.0.0" in packages

    def test_package_repository_clear_cache(self, package_repository):
        """Test clearing the package repository cache."""
        repo = package_repository
        patient = StructureDefinition.model_validate(SAMPLE_PATIENT_R4)

        # Add data
        repo.add(patient)
        repo._loaded_packages["test.package@1.0.0"] = "1.0.0"

        # Verify data exists
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
        assert len(repo.get_loaded_packages()) == 1

        # Clear cache
        repo.clear_local_cache()

        # Verify data is gone
        assert not repo.has("http://hl7.org/fhir/StructureDefinition/Patient")
        assert len(repo.get_loaded_packages()) == 0


class TestCompositeRepositoryPackageIntegration:
    """Test cases for package integration in CompositeStructureDefinitionRepository."""

    @pytest.fixture
    def composite_repo_with_packages(self):
        """Create a composite repository with package support enabled."""
        return CompositeStructureDefinitionRepository(
            internet_enabled=False, enable_packages=True
        )

    @pytest.fixture
    def composite_repo_without_packages(self):
        """Create a composite repository without package support."""
        return CompositeStructureDefinitionRepository(
            internet_enabled=False, enable_packages=False
        )

    def test_composite_repository_initialization_with_packages(self):
        """Test CompositeStructureDefinitionRepository initialization with packages."""
        # Test with packages enabled (default)
        repo = CompositeStructureDefinitionRepository(internet_enabled=False)
        assert repo._package_repository is not None
        assert isinstance(
            repo._package_repository, PackageStructureDefinitionRepository
        )

        # Test with packages explicitly enabled
        repo_enabled = CompositeStructureDefinitionRepository(
            internet_enabled=False, enable_packages=True
        )
        assert repo_enabled._package_repository is not None

        # Test with packages disabled
        repo_disabled = CompositeStructureDefinitionRepository(
            internet_enabled=False, enable_packages=False
        )
        assert repo_disabled._package_repository is None

        # Test with custom registry URL
        repo_custom = CompositeStructureDefinitionRepository(
            internet_enabled=False,
            enable_packages=True,
            registry_base_url="https://custom.registry.com",
            timeout=60.0,
        )
        assert repo_custom._package_repository is not None
        assert (
            repo_custom._package_repository._package_client.base_url
            == "https://custom.registry.com"
        )

    def test_composite_repository_package_methods_when_disabled(
        self, composite_repo_without_packages
    ):
        """Test package methods raise errors when packages are disabled."""
        repo = composite_repo_without_packages

        # All package methods should raise RuntimeError
        with pytest.raises(RuntimeError, match="Package support is not enabled"):
            repo.load_package("test.package")

        with pytest.raises(RuntimeError, match="Package support is not enabled"):
            repo.set_registry_base_url("https://example.com")

        # These methods should gracefully handle disabled packages
        assert repo.get_loaded_packages() == {}
        assert not repo.has_package("test.package")
        repo.remove_package("test.package")  # Should not raise
        repo.clear_package_cache()  # Should not raise

    def test_composite_repository_package_methods_when_enabled(
        self, composite_repo_with_packages
    ):
        """Test package methods work when packages are enabled."""
        repo = composite_repo_with_packages

        # These should not raise errors
        packages = repo.get_loaded_packages()
        assert isinstance(packages, dict)
        assert len(packages) == 0

        assert not repo.has_package("test.package")
        repo.remove_package("test.package")  # Should not raise
        repo.clear_package_cache()  # Should not raise
        repo.set_registry_base_url("https://example.com")  # Should not raise

    @patch("fhircraft.fhir.packages.client.FHIRPackageRegistryClient.download_package")
    def test_composite_repository_load_package_integration(
        self, mock_download, composite_repo_with_packages
    ):
        """Test package loading integration in composite repository."""
        repo = composite_repo_with_packages
        repo._package_repository._internet_enabled = (
            True  # Enable internet for package repo
        )

        # Create mock tar file
        mock_tar = MagicMock(spec=tarfile.TarFile)
        mock_member = MagicMock()
        mock_member.isfile.return_value = True
        mock_member.name = "package/StructureDefinition-Patient.json"
        mock_file = MagicMock()
        mock_file.read.return_value = json.dumps(SAMPLE_PATIENT_R4).encode("utf-8")
        mock_tar.getmembers.return_value = [mock_member]
        mock_tar.extractfile.return_value = mock_file
        mock_download.return_value = mock_tar

        # Load package
        repo.load_package("test.package", "1.0.0")

        # Verify results
        loaded_packages = [
            repo._package_repository.get(
                "http://hl7.org/fhir/StructureDefinition/Patient"
            )
        ]
        assert len(loaded_packages) == 1
        assert (
            loaded_packages[0].url == "http://hl7.org/fhir/StructureDefinition/Patient"
        )
        assert loaded_packages[0].version == "4.0.0"

        # Verify structure definition is available in main repository
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")
        patient = repo.get("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")
        assert patient.url == "http://hl7.org/fhir/StructureDefinition/Patient"

        # Verify package is tracked
        packages = repo.get_loaded_packages()
        assert "test.package@1.0.0" in packages

    def test_composite_repository_package_fallback_in_get(
        self, composite_repo_with_packages
    ):
        """Test that get() method falls back to package repository."""
        repo = composite_repo_with_packages
        patient = StructureDefinition.model_validate(SAMPLE_PATIENT_R4)

        # Add structure definition to package repository only
        repo._package_repository.add(patient)

        # Should be found via package repository fallback
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")

        # Getting it should work and cache it locally
        retrieved = repo.get("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")
        assert retrieved.url == patient.url
        assert retrieved.version == patient.version

        # Should now be available in local repository too
        assert (
            "http://hl7.org/fhir/StructureDefinition/Patient" in repo._local_definitions
        )

    def test_composite_repository_package_fallback_in_has(
        self, composite_repo_with_packages
    ):
        """Test that has() method checks package repository."""
        repo = composite_repo_with_packages
        patient = StructureDefinition.model_validate(SAMPLE_PATIENT_R4)

        # Initially not available
        assert not repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")

        # Add to package repository only
        repo._package_repository.add(patient)

        # Should now be found via package repository
        assert repo.has("http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0")
        assert repo.has(
            "http://hl7.org/fhir/StructureDefinition/Patient"
        )  # Latest version

    def test_composite_repository_package_and_local_priority(
        self, composite_repo_with_packages
    ):
        """Test that local repository takes priority over package repository."""
        repo = composite_repo_with_packages

        # Create two different versions of the same structure definition
        patient_r4 = StructureDefinition.model_validate(SAMPLE_PATIENT_R4)
        patient_r4b = StructureDefinition.model_validate(SAMPLE_PATIENT_R4B)

        # Add one version to package repository
        repo._package_repository.add(patient_r4)

        # Add different version to local repository
        repo.add(patient_r4b)

        # Local should take priority
        retrieved = repo.get("http://hl7.org/fhir/StructureDefinition/Patient", "4.3.0")
        assert retrieved.version == "4.3.0"

        # Package version should still be accessible with specific version
        retrieved_r4 = repo.get(
            "http://hl7.org/fhir/StructureDefinition/Patient", "4.0.0"
        )
        assert retrieved_r4.version == "4.0.0"

        # Latest version should be from local (4.3.0 > 4.0.0)
        latest = repo.get("http://hl7.org/fhir/StructureDefinition/Patient")
        assert latest.version == "4.3.0"




def make_tarfile_with_structuredefs(struct_defs, package_json=None):
    """Helper to create an in-memory tarfile with StructureDefinition JSON files and optional package.json."""
    tar_bytes = io.BytesIO()
    with tarfile.open(fileobj=tar_bytes, mode="w") as tar:
        # Add StructureDefinition files
        for idx, struct_def in enumerate(struct_defs):
            file_content = json.dumps(struct_def).encode("utf-8")
            tarinfo = tarfile.TarInfo(name=f"package/StructureDefinition-{idx}.json")
            tarinfo.size = len(file_content)
            tar.addfile(tarinfo, io.BytesIO(file_content))
        # Add package.json if provided
        if package_json:
            pkg_content = json.dumps(package_json).encode("utf-8")
            tarinfo = tarfile.TarInfo(name="package/package.json")
            tarinfo.size = len(pkg_content)
            tar.addfile(tarinfo, io.BytesIO(pkg_content))
    tar_bytes.seek(0)
    # Return the BytesIO object so the caller can open the tarfile as needed
    return tar_bytes

def valid_structure_definition(url="http://example.org/StructureDefinition/test", version="1.0.0"):
    return {
        "resourceType": "StructureDefinition",
        "url": url,
        "version": version,
        "name": "TestStructureDefinition",
        "status": "active",
        "kind": "resource",
        "abstract": False,
        "type": "Observation",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
        "derivation": "constraint"
    }

class TestProcessPackageTar:
    def setup_method(self):
        self.repo = PackageStructureDefinitionRepository()
        # Patch self.add to track calls
        self.add_patcher = mock.patch.object(self.repo, "add", wraps=self.repo.add)
        self.mock_add = self.add_patcher.start()

    def teardown_method(self):
        self.add_patcher.stop()

    def test_extracts_and_adds_structure_definitions(self):
        struct_defs = [
            valid_structure_definition(url="http://example.org/StructureDefinition/one", version="1.0.0"),
            valid_structure_definition(url="http://example.org/StructureDefinition/two", version="2.0.0"),
        ]
        tar_bytes = make_tarfile_with_structuredefs(struct_defs)
        with tarfile.open(fileobj=tar_bytes, mode="r") as tar:
            self.repo._process_package_tar(tar, "testpkg", "1.0.0")
        # Should call add for each StructureDefinition
        assert self.mock_add.call_count == 2
        urls = [call.args[0].url for call in self.mock_add.call_args_list]
        assert "http://example.org/StructureDefinition/one" in urls
        assert "http://example.org/StructureDefinition/two" in urls

    def test_raises_if_no_structure_definitions_found(self):
        tar_bytes = make_tarfile_with_structuredefs([])
        with tarfile.open(fileobj=tar_bytes, mode="r") as tar:
            with pytest.raises(RuntimeError, match="No StructureDefinition resources found"):
                self.repo._process_package_tar(tar, "testpkg", "1.0.0")

    def test_ignores_non_structuredefinition_json_files(self):
        # Add a non-StructureDefinition JSON file
        tar_bytes = io.BytesIO()
        with tarfile.open(fileobj=tar_bytes, mode="w") as tar:
            content = json.dumps({"resourceType": "Patient"}).encode("utf-8")
            tarinfo = tarfile.TarInfo(name="package/Patient-1.json")
            tarinfo.size = len(content)
            tar.addfile(tarinfo, io.BytesIO(content))
        tar_bytes.seek(0)
        with tarfile.open(fileobj=tar_bytes, mode="r") as tar:
            with pytest.raises(RuntimeError, match="No StructureDefinition resources found"):
                self.repo._process_package_tar(tar, "testpkg", "1.0.0")

    def test_processes_package_json_and_loads_dependencies(self):
        struct_defs = [valid_structure_definition()]
        package_json = {"dependencies": {"dep.pkg": "1.2.3"}}
        tar_bytes = make_tarfile_with_structuredefs(struct_defs, package_json=package_json)
        # Patch load_package to track dependency loading
        with tarfile.open(fileobj=tar_bytes, mode="r") as tar:
            with mock.patch.object(self.repo, "load_package") as mock_load_package:
                self.repo._process_package_tar(tar, "testpkg", "1.0.0")
                mock_load_package.assert_any_call("dep.pkg", "1.2.3", fail_if_exists=False)
        # Should still add the StructureDefinition
        assert self.mock_add.call_count == 1

    def test_logs_errors_but_continues_on_partial_failure(self, capsys):
        # One valid, one invalid StructureDefinition
        struct_defs = [
            valid_structure_definition(),
            {"resourceType": "StructureDefinition", "invalid": "data"}
        ]
        tar_bytes = make_tarfile_with_structuredefs(struct_defs)
        # Should not raise, but print a warning
        with tarfile.open(fileobj=tar_bytes, mode="r") as tar:
            self.repo._process_package_tar(tar, "testpkg", "1.0.0")
        captured = capsys.readouterr()
        assert "Warning:" in captured.out
        assert "Error processing" in captured.out
        # Only one valid StructureDefinition added
        assert self.mock_add.call_count == 1