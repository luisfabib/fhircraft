#!/usr/bin/env python
"""
Test cases for Structure Definition Repository
"""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict
from unittest.mock import Mock, mock_open, patch

import pytest

from fhircraft.fhir.resources.definitions import StructureDefinition
from fhircraft.fhir.resources.repository import (
    CompositeStructureDefinitionRepository,
    HttpStructureDefinitionRepository,
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

        repo.add(patient, fail_if_exists=True)

        # Adding same version should raise error
        with pytest.raises(ValueError, match="duplicated URL"):
            repo.add(patient)

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

        with pytest.raises(RuntimeError, match="Structure definition not found"):
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


if __name__ == "__main__":
    pytest.main([__file__])
