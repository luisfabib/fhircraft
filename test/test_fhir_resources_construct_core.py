from fhircraft.fhir.resources.factory import ResourceFactory
import pytest 
import glob 
import json
import os

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
        'careplan',
        'condition',
        'medicationadministration',
        'observation',
        'organization',
        'patient',
        'practicioner',
        'procedure',
        'questionnaire',
    ]
]
fhir_resources_test_cases = [case for cases in fhir_resources_test_cases for case in cases]
@pytest.mark.parametrize("resource_label, filename", fhir_resources_test_cases)
def test_construct_core_resource(resource_label, filename):   
    resource_model = ResourceFactory().construct_resource_model(f'https://hl7.org/fhir/R4B/{resource_label}.profile.json')

    with open(os.path.join(os.path.abspath(EXAMPLES_DIRECTORY), filename), encoding="utf8") as file:
        fhir_resource = json.load(file)
        fhir_resource_instance = resource_model.model_validate(fhir_resource)
        assert json.loads(fhir_resource_instance.model_dump_json(exclude_unset=True, by_alias=True)) == fhir_resource
            
            
