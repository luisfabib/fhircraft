
from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.fhir.resources.generator import generate_resource_model_code
import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.utils import capitalize
import os
import json

VERSION = 'STU3'
PATH = f'fhircraft/fhir/resources/definitions/{VERSION}'
DESTINATION = f'fhircraft/fhir/resources/datatypes/{VERSION}'

structure_definitions = []
with open(os.path.join(PATH,'profiles-types.json'), 'r', encoding='utf-8') as file: 
    datatypes_bundle = json.load(file)
    structure_definitions += [resource['resource'] for resource in datatypes_bundle['entry'] if not hasattr(primitives, capitalize(resource['resource']['name']))]
with open(os.path.join(PATH,'profiles-resources.json'), 'r', encoding='utf-8') as file: 
    datatypes_bundle = json.load(file)
    structure_definitions += [resource['resource'] for resource in datatypes_bundle['entry'] if resource['resource']['name'] in ['Resource', 'DomainResource']]


factory = ResourceFactory() 

resources = []

for structure_definition in structure_definitions:
    resource = factory.construct_dataelement_model(structure_definition=structure_definition)
    resources.append(resource)

source_code = generate_resource_model_code(resources)
with open(os.path.join(DESTINATION,'complex_types.py'), '+w', encoding='utf-8') as file:
    file.write(source_code)

