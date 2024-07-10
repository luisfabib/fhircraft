from fhircraft.fhir.resources.generator import generate_resource_model_code 
from fhircraft.fhir.resources.factory import construct_resource_model
import pytest 
import os 
import glob
import json 
import importlib
import tempfile
import sys

EXAMPLES_DIRECTORY = 'test/static/fhir-core-examples/R4B'
    
def _get_example_filenames(prefix):
    pattern = os.path.join(EXAMPLES_DIRECTORY, prefix)
    example_files = [os.path.basename(f) for f in glob.glob(pattern)]
    return example_files

fhir_resources_test_cases = [
    [
    (resource_label, filename)
        for filename in _get_example_filenames(f'{resource_label}-*')
    ] for resource_label in [
        'observation',
        'condition',
    ]
]
fhir_resources_test_cases = [case for cases in fhir_resources_test_cases for case in cases]
@pytest.mark.parametrize("resource_label, filename", fhir_resources_test_cases)
def test_construct_core_resource(resource_label, filename):   
    # Create temp directory for storing generated code
    with tempfile.TemporaryDirectory() as d:
        # Generate source code for Pydantic FHIR model
        resource = construct_resource_model(canonical_url=f'https://hl7.org/fhir/R4B/{resource_label}.profile.json')
        source_code = generate_resource_model_code(resource)
        print(source_code)
        # Store source code in a file        
        temp_file_name = os.path.join(d, 'temp_test.py')    
        with open(temp_file_name, "w") as test_file:
            test_file.write(source_code)
        # Load the Pydantic FHIR model
        spec = importlib.util.spec_from_file_location('module', temp_file_name)
        module = importlib.util.module_from_spec(spec)
        sys.modules["module.name"] = module
        spec.loader.exec_module(module)
        # Use the auto-generated model to validate a FHIR resource
        with open(os.path.join(os.path.abspath(EXAMPLES_DIRECTORY), filename), encoding="utf8") as file:
            fhir_resource = json.load(file)
            fhir_resource_instance = getattr(module, resource_label.capitalize()).model_validate(fhir_resource)
            assert json.loads(fhir_resource_instance.model_dump_json(exclude_unset=True, by_alias=True)) == fhir_resource
            
            