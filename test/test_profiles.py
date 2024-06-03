from fhir_openapi.profiles import ProfiledResourceFactory, FHIRError, clear_chache, construct_profiled_resource_model, construct_with_skeleton

from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.observation import Observation
from fhir.resources.R4B.extension import Extension
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.elementdefinition import ElementDefinition
from fhir.resources.R4B.structuredefinition import StructureDefinition, StructureDefinitionSnapshot
from pydantic.v1 import BaseModel
import requests
import json

import pytest
from unittest.mock import patch, MagicMock
from unittest import TestCase 

        

class TestGetStructureDefinition(TestCase):

    def setUp(self):
        self.expected_json = {
            'id': 'example',
            'status': 'active',
            'type': 'Observation',
            'name': 'Profile',
            'kind': 'resource',
            'abstract': False,
            'url': 'https://fhir.com/StructureDefinition/fhir-profile',
        }
        self.mock_response = MagicMock()
        self.mock_response.json.return_value = self.expected_json
        self.mock_response.raise_for_status = MagicMock()
        
    def test_get_structure_definition_from_canonical_url(self):
        profile_url = "https://fhir.com/StructureDefinition/fhir-profile"
        with patch('requests.get', return_value=self.mock_response):
            factory = ProfiledResourceFactory()
            result = factory.get_structure_definition(profile_url)
            assert all([getattr(result, field) == value for field,value in self.expected_json.items()])
            
    def test_get_structure_definition_from_json_url(self):
        profile_url = "https://fhir.com/StructureDefinition-fhir-profile.json"
        with patch('requests.get', return_value=self.mock_response):
            factory = ProfiledResourceFactory()
            result = factory.get_structure_definition(profile_url)
            assert all([getattr(result, field) == value for field,value in self.expected_json.items()])

class TestConstructWithSkeleton:
    
    def test_construct_skeleton_basic(self):            
        resource = construct_with_skeleton(CodeableConcept)
        assert isinstance(resource, CodeableConcept)
        assert isinstance(resource.coding, list)
        assert len(resource.coding) == 1
        assert isinstance(resource.coding[0], Coding)
        assert resource.coding[0].code is None
        assert resource.coding[0].system is None
        assert resource.coding[0].version is None
        assert resource.coding[0].display is None
        
    def test_construct_skeleton_nested(self):            
        resource = construct_with_skeleton(Extension)
        assert isinstance(resource, Extension)
        assert isinstance(resource.valueCodeableConcept, CodeableConcept)
        assert isinstance(resource.valueCodeableConcept.coding, list)
        assert len(resource.valueCodeableConcept.coding) == 1
        assert isinstance(resource.valueCodeableConcept.coding[0], Coding)
        assert resource.valueCodeableConcept.coding[0].code is None
        assert resource.valueCodeableConcept.coding[0].system is None
        assert resource.valueCodeableConcept.coding[0].version is None
        assert resource.valueCodeableConcept.coding[0].display is None
        
        
        
class TestConstructProfiledResourceModel:

    def _slicing_definition(self,
            id="Observation.category", 
            path="Observation.category", 
            type="CodeableConcept", 
            discriminator_type="value",
            discriminator_path="coding", 
            rules='open'):
        return {
            'id': id,
            'path':	path,
            'type': [{'code': type}],
            'slicing':	{
                'discriminator': [{	
                    'type':	discriminator_type,
                    'path':	discriminator_path,
                }],
                'rules': rules
            },
        }

    def _construct_mocked_profile(self, element_definitions=[], base_model='Observation'):
        canonical_url = f'https://fhir.com/StructureDefinition/fhir-profile-{base_model.lower()}'
        structure_definition = StructureDefinition(
            id='example',
            status='active',
            type=base_model,
            name=f'Profiled{base_model}',
            kind='resource',
            abstract=False,
            url=canonical_url,
            snapshot=StructureDefinitionSnapshot(element=[
                ElementDefinition.parse_obj(definition) for definition in element_definitions
            ])
        )
        with patch('fhir_openapi.profiles.ProfiledResourceFactory.get_structure_definition', return_value=structure_definition):
            clear_chache()
            profile_model = construct_profiled_resource_model(canonical_url)
            return profile_model

    def test_profiled_model_type(self):
        profile_model = self._construct_mocked_profile()
        assert issubclass(profile_model,BaseModel), 'Expected profiled model to be a Pydantic model'
        assert issubclass(profile_model,Observation), 'Expected profiled model to be an Observation resource'
      
    def test_profile_model_private_attributes(self):
        profile_model = self._construct_mocked_profile()
        assert hasattr(profile_model,'__slicing__') and len(profile_model.__slicing__)==0
        assert hasattr(profile_model,'__constraints__') and len(profile_model.__constraints__)==0
        assert hasattr(profile_model,'__extensions__') and len(profile_model.__extensions__)==0
        
    def test_profile_model_name(self):
        profile_model = self._construct_mocked_profile(base_model='Patient')
        assert profile_model.__name__ == 'ProfiledPatient'
        
    def test_valid_base_model(self):
        profile_model = self._construct_mocked_profile(base_model='Patient')
        assert issubclass(profile_model,Patient), 'Expected profiled model to be an Observation resource'

    def test_invalid_base_model(self):
        with pytest.raises(FHIRError):
            self._construct_mocked_profile(base_model='InvalidResource')

    def test_profile_with_sliced_element(self):
        element_definitions = [self._slicing_definition(
            id="Observation.category", 
            path="Observation.category", 
            type="CodeableConcept", 
            discriminator_type="value",
            discriminator_path="coding", 
            rules='open'
        )]
        profile_model = self._construct_mocked_profile(element_definitions)
        assert len(profile_model.__slicing__) == 1
        slicing = profile_model.__slicing__[0]
        assert slicing.id == 'Observation.category'
        assert slicing.path == 'Observation.category'
        assert slicing.rules == 'open'
        assert slicing.discriminators[0].type == 'value'
        assert slicing.discriminators[0].path == 'coding'
        

    def test_profile_with_multiple_sliced_elements(self):
        element_definitions = [
            self._slicing_definition(
                id="Observation.category", 
                path="Observation.category", 
                type="CodeableConcept", 
                discriminator_type="value",
                discriminator_path="coding", 
                rules='open'
            ),           
            self._slicing_definition(
                id="Observation.component", 
                path="Observation.component", 
                type="BackboneElement", 
                discriminator_type="pattern",
                discriminator_path="coding", 
                rules='open'
            )
        ]
        profile_model = self._construct_mocked_profile(element_definitions)
        assert len(profile_model.__slicing__) == 2
        slicing = profile_model.__slicing__[1]
        assert slicing.id == 'Observation.component'
        assert slicing.path == 'Observation.component'
        assert slicing.rules == 'open'
        assert slicing.discriminators[0].type == 'pattern'
        assert slicing.discriminators[0].path == 'coding'
        


    def test_profile_with_extensions(self):
        element_definitions = [
            self._slicing_definition(
                id="Observation.extension", 
                path="Observation.extension", 
                type="CodeableConcept", 
                discriminator_type="value",
                discriminator_path="url", 
                rules='open'
            ),
        ]
        profile_model = self._construct_mocked_profile(element_definitions)
        assert len(profile_model.__slicing__) == 1
        slicing = profile_model.__slicing__[0]
        assert slicing.id == 'Observation.extension'
        assert slicing.path == 'Observation.extension'
        assert slicing.rules == 'open'
        assert slicing.discriminators[0].type == 'value'
        assert slicing.discriminators[0].path == 'url'
        
