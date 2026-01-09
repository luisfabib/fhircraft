import pathlib
import pytest
import json
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
from .mktestdocs import check_md_file


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
@patch("fhircraft.utils.load_file", mock_load_file)
@patch("builtins.open", side_effect=mock_open_func)
@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_documentation_examples(mock_file, fpath):
    # Do not test documentation pages that include many abstract python examples
    if fpath in [
        pathlib.Path("docs") / "user-guide" / "resources-construction.md",
    ]:
        pytest.skip("Skipping documentation with invalid python examples.")
    check_md_file(fpath=fpath, memory=True)


@patch(
    "fhircraft.fhir.resources.factory.ResourceFactory.load_package", mock_load_package
)
@patch("fhircraft.utils.load_file", mock_load_file)
@patch("builtins.open", side_effect=mock_open_func)
@pytest.mark.filterwarnings("ignore:.*dom-6.*")
def test_readme_examples(mock_file):
    check_md_file(fpath=pathlib.Path("README.md"), memory=True)
