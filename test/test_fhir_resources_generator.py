import glob
import importlib
import json
import os
import sys
import tempfile

import pytest

from fhircraft.fhir.resources.factory import clear_chache, construct_resource_model
from fhircraft.fhir.resources.generator import CodeGenerator

VERSIONS = ["R4B", "R5"]
CORE_EXAMPLES_DIRECTORY = f"test/static/fhir-core-examples"
PROFILES_EXAMPLES_DIRECTORY = f"test/static/fhir-profiles-examples"
PROFILES_DEFINTIONS_DIRECTORY = f"test/static/fhir-profiles-definitions"


def _get_core_example_filenames(prefix, version):
    pattern = os.path.join(f"{CORE_EXAMPLES_DIRECTORY}/{version}", prefix)
    example_files = [os.path.basename(f) for f in glob.glob(pattern)]
    return example_files


fhir_resources_test_cases = {
    version: [
        case
        for cases in [
            [
                (resource_label, filename)
                for filename in _get_core_example_filenames(
                    f"{resource_label}-*", version
                )
            ]
            for resource_label in [
                "observation",
                "condition",
                "patient",
                "practicioner",
                "procedure",
                "medicationadministration",
                "organization",
            ]
        ]
        for case in cases
    ]
    for version in VERSIONS
}


def _assert_construct_core_resource(version, resource_label, filename):
    # Create temp directory for storing generated code
    with tempfile.TemporaryDirectory() as d:
        # Generate source code for Pydantic FHIR model
        resource = construct_resource_model(
            canonical_url=f"https://hl7.org/fhir/{version}/{resource_label}.profile.json"
        )
        source_code = CodeGenerator().generate_resource_model_code(resource)
        # Store source code in a file
        temp_file_name = os.path.join(d, "temp_test.py")
        with open(temp_file_name, "w") as test_file:
            test_file.write(source_code)
        # Load the Pydantic FHIR model
        spec = importlib.util.spec_from_file_location("module", temp_file_name)
        module = importlib.util.module_from_spec(spec)
        sys.modules["module.name"] = module
        spec.loader.exec_module(module)
        # Use the auto-generated model to validate a FHIR resource
        with open(
            os.path.join(
                os.path.abspath(f"{CORE_EXAMPLES_DIRECTORY}/{version}"), filename
            ),
            encoding="utf8",
        ) as file:
            fhir_resource = json.load(file)
            fhir_resource_instance = getattr(
                module, resource_label.capitalize()
            ).model_validate(fhir_resource)
            assert json.loads(fhir_resource_instance.model_dump_json()) == fhir_resource


@pytest.mark.parametrize("resource_label, filename", fhir_resources_test_cases["R4B"])
def test_construct_R4B_core_resource(resource_label, filename):
    print(fhir_resources_test_cases)
    _assert_construct_core_resource("R4B", resource_label, filename)


@pytest.mark.parametrize("resource_label, filename", fhir_resources_test_cases["R5"])
def test_construct_R5_core_resource(resource_label, filename):
    _assert_construct_core_resource("R5", resource_label, filename)


def _get_profiles_example_filenames(prefix):
    pattern = os.path.join(f"{PROFILES_EXAMPLES_DIRECTORY}", prefix)
    example_files = [os.path.basename(f) for f in glob.glob(pattern)]
    return example_files


fhir_profiles_test_cases = [
    case
    for cases in [
        [
            filename
            for filename in _get_profiles_example_filenames(f"{resource_label}-*")
        ]
        for resource_label in [
            "Observation",
            "Condition",
            "Patient",
        ]
    ]
    for case in cases
]


def mock_resolve_profile_canonical_url(canonical_url: str):
    MAP = {
        "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-primary-cancer-condition": "mcode-primary-cancer-condition.json",
        "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-related-medication-administration": "mcode-cancer-related-medication-administration.json",
        "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-tnm-distant-metastases-category": "mcode-tnm-distant-metastases-category.json",
        "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-patient": "mcode-cancer-patient.json",
        "http://hl7.org/fhir/us/core/StructureDefinition/us-core-practitioner": "us-core-practitioner.json",
        "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-radiotherapy-course-summary": "mcode-radiotherapy-course-summary.json",
        "http://hl7.org/fhir/us/core/StructureDefinition/us-core-procedure": "us-core-procedure.json",
        "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-human-specimen": "mcode-human-specimen.json",
    }
    # Use the auto-generated model to validate a FHIR resource
    with open(
        os.path.join(
            os.path.abspath(f"{PROFILES_DEFINTIONS_DIRECTORY}"), MAP[canonical_url]
        ),
        encoding="utf8",
    ) as file:
        return json.load(file)


@pytest.mark.parametrize("filename", fhir_profiles_test_cases)
def test_construct_profiled_resource(filename):
    # Use the auto-generated model to validate a FHIR resource
    with open(
        os.path.join(os.path.abspath(f"{PROFILES_EXAMPLES_DIRECTORY}"), filename),
        encoding="utf8",
    ) as file:
        fhir_resource = json.load(file)

    # Create temp directory for storing generated code
    with tempfile.TemporaryDirectory() as d:
        # Generate source code for Pydantic FHIR model
        resource = construct_resource_model(
            structure_definition=mock_resolve_profile_canonical_url(
                fhir_resource["meta"]["profile"][0]
            )
        )
        clear_chache()
        source_code = CodeGenerator().generate_resource_model_code(resource)
        # Store source code in a file
        temp_file_name = os.path.join(d, f"temp_test_{resource.__name__}.py")
        with open(temp_file_name, "w") as test_file:
            test_file.write(source_code)
        # print(source_code)
        # Load the Pydantic FHIR model
        spec = importlib.util.spec_from_file_location("module", temp_file_name)
        module = importlib.util.module_from_spec(spec)
        sys.modules["module.name"] = module
        spec.loader.exec_module(module)

    fhir_resource_instance = getattr(module, resource.__name__).model_validate(
        fhir_resource
    )
    assert json.loads(fhir_resource_instance.model_dump_json()) == fhir_resource
