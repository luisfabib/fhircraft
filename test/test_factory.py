from fhiropenapi.factory import ProfiledResourceFactory, get_paths, FHIRError, construct_profiled_resource_model

from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.observation import Observation
from fhir.resources.R4B.elementdefinition import ElementDefinition
from fhir.resources.R4B.structuredefinition import StructureDefinition, StructureDefinitionSnapshot
from pydantic.v1 import BaseModel
import requests
import json

import pytest
from unittest.mock import patch, MagicMock
from unittest import TestCase 


class TestGetPaths:

    def test_flat_dictionary(self):
        input_dict = {'a': 1, 'b': 2, 'c': 3}
        expected_output = {'a': 1, 'b': 2, 'c': 3}
        assert get_paths(input_dict) == expected_output

    def test_dictionary_with_none_values(self):
        input_dict = {'a': None, 'b': 2, 'c': None}
        expected_output = {'b': 2}
        assert get_paths(input_dict) == expected_output

    def test_nested_dictionaries(self):
        input_dict = {'a': {'b': 1, 'c': {'d': 2}}}
        expected_output = {'a.b': 1, 'a.c.d': 2}
        assert get_paths(input_dict) == expected_output

    def test_lists_of_dictionaries(self):
        input_dict = {'a': [{'b': 1}, {'c': 2}]}
        expected_output = {'a.0.b': 1, 'a.1.c': 2}
        assert get_paths(input_dict) == expected_output

    def test_combine_prefix_with_keys(self):
        input_dict = {'a': {'b': 1, 'c': 2}}
        prefix = 'prefix'
        expected_output = {'prefix.a.b': 1, 'prefix.a.c': 2}
        assert get_paths(input_dict, prefix) == expected_output
        

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
            requests.get.assert_called_once_with("https://fhir.com/StructureDefinition-fhir-profile.json")
            assert all([getattr(result, field) == value for field,value in self.expected_json.items()])
            
    def test_get_structure_definition_from_json_url(self):
        profile_url = "https://fhir.com/StructureDefinition-fhir-profile.json"
        with patch('requests.get', return_value=self.mock_response):
            factory = ProfiledResourceFactory()
            result = factory.get_structure_definition(profile_url)
            requests.get.assert_called_once_with("https://fhir.com/StructureDefinition-fhir-profile.json")
            assert all([getattr(result, field) == value for field,value in self.expected_json.items()])
            


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
        canonical_url = 'https://fhir.com/StructureDefinition/fhir-profile'
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
        with patch('fhiropenapi.factory.ProfiledResourceFactory.get_structure_definition', return_value=structure_definition):
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