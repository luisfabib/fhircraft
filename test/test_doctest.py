import pathlib
import pytest
import json
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

from fhircraft.fhir.resources.factory import ConstructionMode, factory, ResourceFactory
from fhircraft.fhir.resources.datatypes.R5.core import (
    Patient,
    Observation,
    Procedure,
    Condition,
)
from .mktestdocs import check_md_file

# Store original methods before patching
_original_configure_repository = ResourceFactory.configure_repository
_original_construct_resource_model = ResourceFactory.construct_resource_model


def mock_load_package(self, package_name, version=None):
    """Mock load_package to load local test files instead of downloading from internet."""
    if package_name == "hl7.fhir.us.mcode":
        # Load the local mcode cancer patient profile
        test_files_dir = Path(__file__).parent / "static" / "fhir-profiles-definitions"
        mcode_file = test_files_dir / "mcode-cancer-patient.json"
        self.repository.load_from_files(mcode_file)
    elif package_name == "hl7.fhir.us.core":
        # Load the local mcode cancer patient profile
        test_files_dir = Path(__file__).parent / "static" / "fhir-profiles-definitions"
        mcode_file = test_files_dir / "us-core-patient.json"
        self.repository.load_from_files(mcode_file)
    else:
        # For other packages, raise an error since we don't have mocks for them
        raise NotImplementedError(f"Mock not implemented for package: {package_name}")


def mock_configure_repository(
    self,
    directory=None,
    files=None,
    definitions=None,
    packages=None,
    internet_enabled=False,
):
    """Mock configure_repository to use local test files instead of downloading from internet."""
    if directory or files:
        return _original_configure_repository(
            self,
            directory="test/static/fhir-profiles-definitions",
            internet_enabled=internet_enabled,
        )
    elif definitions:
        return _original_configure_repository(
            self, definitions=definitions, internet_enabled=internet_enabled
        )
    elif packages:
        return _original_configure_repository(
            self, packages=packages, internet_enabled=internet_enabled
        )
    else:
        raise ValueError("Either directory/files or definitions must be provided.")


def mock_construct_resource_model(
    self, canonical_url=None, structure_definition=None, mode=None
):
    """Mock construct_resource_model"""
    if canonical_url:
        if canonical_url == "http://example.org/StructureDefinition/MyPatient":
            return Patient
        elif canonical_url == "http://hl7.org/fhir/StructureDefinition/Patient":
            return Patient
        elif canonical_url == "http://example.org/StructureDefinition/CustomPatient":
            return Patient
        elif canonical_url == "http://example.org/StructureDefinition/MyObservation":
            return Observation
        elif (
            canonical_url
            == "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-patient"
        ):
            return Patient
        elif canonical_url.startswith(
            "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
        ):
            return Patient
        elif canonical_url.startswith(
            "http://hl7.org/fhir/us/core/StructureDefinition/us-core-condition"
        ):
            return Condition
        elif canonical_url.startswith(
            "http://hl7.org/fhir/us/core/StructureDefinition/us-core-procedure"
        ):
            return Procedure
    return _original_construct_resource_model(
        self,
        canonical_url=canonical_url,
        structure_definition=structure_definition,
        mode=ConstructionMode.AUTO,
    )


def mock_load_structure_map(self, source):
    """Mock load_structure_map to load local test files instead of downloading from internet."""
    if source in [
        "patient-mapping.json",
        "https://example.org/fhir/StructureMap/PatientMapping",
    ]:
        test_file = (
            Path(__file__).parent
            / "static"
            / "fhir-mapping-language"
            / "patient-mapping-example.json"
        )
        with open(test_file, "r") as f:
            return json.load(f)
    else:
        # For other sources, raise an error since we don't have mocks for them
        raise NotImplementedError(f"Mock not implemented for package: {source}")


def mock_load_file(filepath):
    """Mock load_file to return test data instead of reading arbitrary files."""
    if filepath == "patient.json" or filepath == "my_fhir_patient.json":
        # Return contents of the test Patient resource
        test_file = (
            Path(__file__).parent
            / "static"
            / "fhir-profiles-examples"
            / "Patient-cancer-patient-jenny-m.json"
        )
        with open(test_file, "r") as f:
            return json.load(f)

    elif filepath == "patient_profile.json":
        # Return contents of the test Patient structure definition
        test_file = (
            Path(__file__).parent
            / "static"
            / "fhir-profiles-definitions"
            / "us-core-patient.json"
        )
        with open(test_file, "r") as f:
            return json.load(f)
    else:
        # For other files, raise an error
        raise FileNotFoundError(f"Mock not configured for file: {filepath}")


# Store the original open function
_original_open = open


def mock_open_func(file, mode="r", *args, **kwargs):
    """Mock open to prevent creating files."""
    if isinstance(file, str) and "w" in mode:
        # Return a mock file object that doesn't actually write to disk
        return mock_open()()
    # For all other files, use the original open
    return _original_open(file, mode, *args, **kwargs)


@pytest.mark.parametrize("fpath", pathlib.Path("docs").glob("**/*.md"), ids=str)
@patch(
    "fhircraft.fhir.resources.factory.ResourceFactory.load_package", mock_load_package
)
@patch("fhircraft.fhir.mapper.FHIRMapper.load_structure_map", mock_load_structure_map)
@patch(
    "fhircraft.fhir.resources.factory.ResourceFactory.construct_resource_model",
    mock_construct_resource_model,
)
@patch(
    "fhircraft.fhir.resources.factory.ResourceFactory.configure_repository",
    mock_configure_repository,
)
@patch("fhircraft.utils.load_file", mock_load_file)
@patch("builtins.open", side_effect=mock_open_func)
@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_documentation_examples(mock_file, fpath):
    check_md_file(fpath=fpath, memory=True)


@patch(
    "fhircraft.fhir.resources.factory.ResourceFactory.load_package", mock_load_package
)
@patch("fhircraft.utils.load_file", mock_load_file)
@patch("builtins.open", side_effect=mock_open_func)
@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_readme_examples(mock_file):
    check_md_file(fpath=pathlib.Path("README.md"), memory=True)
