import glob
import json
import os
import sys
import tempfile
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from pydantic import BaseModel
import pytest

from fhircraft.config import with_config
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type
from fhircraft.fhir.resources.generator import CodeGenerator

VERSIONS = ["R4"]
CORE_EXAMPLES_DIRECTORY = f"test/static/fhir-examples"


def _get_core_example_filenames(version):
    pattern = os.path.join(f"{CORE_EXAMPLES_DIRECTORY}/{version}", "*.json")
    example_files = [
        pytest.param(os.path.abspath(f), id=os.path.basename(f))
        for f in glob.glob(pattern)
    ]
    return example_files


def _assert_core_resource_compliance(fhir_release, filepath):

    with open(filepath, encoding="utf8") as file:
        fhir_resource_data = json.load(file)
    resource_type = fhir_resource_data["resourceType"]
    fhir_model = get_fhir_resource_type(resource_type, fhir_release)

    # Use the code-loaded model to validate the FHIR resource data
    assert (
        instance := fhir_model.model_validate(fhir_resource_data)
    ), "Fhircraft FHIR model failed to validate the example FHIR resource data"
    assert fhir_resource_data == json.loads(
        instance.model_dump_json()
    ), "Fhircraft FHIR model failed to recreate the original FHIR resource data"


@pytest.mark.parametrize("path", _get_core_example_filenames("R4"))
def test_R4_resource_model(path):
    _assert_core_resource_compliance("R4", path)
