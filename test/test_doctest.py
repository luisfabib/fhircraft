import pathlib
import pytest
import json
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

from fhircraft.config import override_config
from fhircraft.fhir.resources.factory import FHIRModelFactory
from fhircraft.fhir.resources.datatypes.R5.core import (
    Patient,
    Observation,
    Procedure,
    Condition,
)
from .mktestdocs import check_md_file

# Store original methods before patching
_original_factory_build = FHIRModelFactory.build


def mock_load_package(self, package_name, version=None):
    """Mock load_package to load local test files instead of downloading from internet."""

    with override_config(validation_mode="skip"):
        if package_name == "hl7.fhir.us.mcode":
            # Load the local mcode cancer patient profile
            test_files_dir = (
                Path(__file__).parent / "static" / "fhir-profiles-definitions"
            )
            mcode_file = test_files_dir / "mcode-cancer-patient.json"
            with open(mcode_file, "r") as f:
                data = json.load(f)
            self.definition_registry.from_dict(data)
        elif package_name == "hl7.fhir.us.core":
            # Load the local mcode cancer patient profile
            test_files_dir = (
                Path(__file__).parent / "static" / "fhir-profiles-definitions"
            )
            mcode_file = test_files_dir / "us-core-patient.json"
            with open(mcode_file, "r") as f:
                data = json.load(f)
                self.definition_registry.from_dict(data)
        else:
            # For other packages, raise an error since we don't have mocks for them
            raise NotImplementedError(
                f"Mock not implemented for package: {package_name}"
            )


def mock_factory_build(
    self,
    canonical_url=None,
    structure_definition=None,
    mode=None,
    **kwargs,
):
    """Mock construct_resource_model"""
    if canonical_url:
        if canonical_url == "http://example.org/StructureDefinition/MyPatient":
            return Patient
        elif canonical_url == "http://hl7.org/fhir/StructureDefinition/Patient":
            return Patient
        elif canonical_url == "http://example.org/StructureDefinition/CustomPatient":
            return Patient
        elif canonical_url == "http://hl7.org/fhir/StructureDefinition/Patient":
            return Patient
        elif canonical_url == "http://hl7.org/fhir/StructureDefinition/Patient|4.0.1":
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

    with override_config(validation_mode="skip"):
        return _original_factory_build(
            self,
            canonical_url=canonical_url,
            structure_definition=structure_definition,
            mode=mode or "snapshot",
            **kwargs,
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

    elif (
        filepath == "patient.profile.json" or filepath == "custom-patient.profile.json"
    ):
        # Return contents of the test Patient structure definition
        test_file = (
            Path(__file__).parent.parent
            / "fhircraft"
            / "fhir"
            / "resources"
            / "definitions"
            / "R4"
            / "entries"
            / "patient.json"
        )
        with open(test_file, "r") as f:
            return json.load(f)
    else:
        # For other files, raise an error
        raise FileNotFoundError(f"Mock not configured for file: {filepath}")


# Store the original open function
_original_open = open


def mock_get_registered_definition(self, url):
    return MagicMock()


def mock_open_func(file, mode="r", *args, **kwargs):
    """Mock open to prevent creating files."""
    if isinstance(file, str) and "w" in mode:
        # Return a mock file object that doesn't actually write to disk
        return mock_open()()
    # For all other files, use the original open
    return _original_open(file, mode, *args, **kwargs)


@pytest.mark.parametrize("fpath", pathlib.Path("docs").glob("**/*.md"), ids=str)
@patch(
    "fhircraft.fhir.resources.factory.FHIRModelFactory.register_package",
    mock_load_package,
)
@patch("fhircraft.fhir.mapper.FHIRMapper.load_structure_map", mock_load_structure_map)
@patch(
    "fhircraft.fhir.resources.factory.FHIRModelFactory.build",
    mock_factory_build,
)
@patch(
    "fhircraft.fhir.resources.factory.FHIRModelFactory.get_registered_definition",
    mock_get_registered_definition,
)
@patch("fhircraft.utils.load_file", mock_load_file)
@patch("builtins.open", side_effect=mock_open_func)
@pytest.mark.filterwarnings("ignore:.*dom-6.*")
@pytest.mark.integration
def test_documentation_examples(mock_file, fpath):
    check_md_file(fpath=fpath, memory=True)


@patch(
    "fhircraft.fhir.resources.factory.FHIRModelFactory.register_package",
    mock_load_package,
)
@patch("fhircraft.utils.load_file", mock_load_file)
@patch("builtins.open", side_effect=mock_open_func)
@pytest.mark.filterwarnings("ignore:.*dom-6.*")
@pytest.mark.integration
def test_readme_examples(mock_file):
    check_md_file(fpath=pathlib.Path("README.md"), memory=True)
