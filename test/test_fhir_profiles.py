from fhircraft.fhir.profiles import ProfiledResourceFactory, FHIRError, \
                        clear_chache, construct_profiled_resource_model, \
                            SlicingGroup, Slice, Discriminator, Constraint
from fhircraft.fhir.path import FHIRPathError
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
        with patch('fhircraft.fhir.profiles.ProfiledResourceFactory.get_structure_definition', return_value=structure_definition):
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


class TestDiscriminator(TestCase):
    
    def test_discriminator_construction(self):
        obj = Discriminator(type='value', path='code')
        assert obj.type == 'value'
        assert obj.path == 'code'
    
    def test_discriminator_type_enum(self):
        with pytest.raises(ValueError):
            Discriminator(type='invalid', path='code')

    def test_discriminator_invalid_fhirpath(self):
        with pytest.raises(FHIRPathError):
            Discriminator(type='value', path='code.coding.5')

    def test_discriminator_restricted_functions(self):
        with pytest.raises(FHIRPathError):
            Discriminator(type='value', path="code.filter(coding.code='5')")
        
class TestSlicingGroup(TestCase):
    
    def test_slicing_group_construction(self):
        obj = SlicingGroup(
            id='Observation.component', 
            path='Observation.component',
            discriminators=[Discriminator(type='value', path='Observation.component.code')],
        )
        assert obj.id == 'Observation.component'
        assert obj.path == 'Observation.component'
        assert obj.rules == 'open'
        assert obj.ordered == False
        assert obj.discriminators[0].path == 'Observation.component.code'
    
    def test_slicing_group_rules_enum(self):
        with pytest.raises(ValueError):
            SlicingGroup(
                id='Observation.component', path='Observation.component',
                discriminators=[Discriminator(type='value', path='Observation.component.code')],
                rules='invalid',
            )

    def test_slicing_group_invalid_fhirpath(self):
        with pytest.raises(FHIRPathError):
            SlicingGroup(
                id='Observation.component', path='Observation.component.0',
                discriminators=[Discriminator(type='value', path='Observation.component.code')],
            )


class TestSlice(TestCase):
    
    def setUp(self):
        self.slicing = SlicingGroup(
            id='Observation.component', 
            path='Observation.component',
            discriminators=[Discriminator(type='value', path='code')],
        )
        self.slice = Slice(
            id='Observation.component:sliceName', 
            name='sliceName',
            type='BackboneElement'
        )
        self.slicing.add_slice(self.slice)
        self.constraint = Constraint(
            id='Observation.component:sliceName.code',
            path='Observation.component.code.coding.code',
            min=0,
            max=1,
        )
    
    def test_slice_construction(self):
        assert self.slice.id == 'Observation.component:sliceName'
        assert self.slice.name == 'sliceName'
        assert self.slice.type == 'BackboneElement'
    
    def test_get_constraints_on_slice(self):
        self.constraint.path = 'Observation.component'
        self.slice.add_constraint(self.constraint)
        assert self.slice.get_constraints_on_slice() == [self.constraint]
        
    def test_slice_min_cardinality(self):
        self.constraint.path = 'Observation.component'
        self.slice.add_constraint(self.constraint)
        assert self.slice.min_cardinality == 0
        
    def test_slice_discriminating_expression_pattern(self):
        pattern = MagicMock()
        self.constraint.path = 'Observation.component.code'
        pattern.dict.return_value = {'coding': [{
            'code': "123456", 
            "system": "http://system.org",
            }]
        }
        self.constraint.pattern = pattern
        self.slice.add_constraint(self.constraint)
        assert self.slice.discriminating_expression == \
            "where(code.coding[0].code='123456').where(code.coding[0].system='http://system.org')"

        
    def __prepare_discriminator_pattern__(self):
        self.slicing.discriminators = [Discriminator(type='value', path='code')]
        pattern = MagicMock()
        self.constraint.path = 'Observation.component.code'
        pattern.dict.return_value = {'coding': [{
            'code': "123456", 
            "system": "http://system.org",
            }]
        }
        self.constraint.pattern = pattern
        self.slice.add_constraint(self.constraint)

    def test_slice_discriminating_expression_pattern(self):
        self.__prepare_discriminator_pattern__()
        assert self.slice.discriminating_expression == \
            "where(code.coding[0].code='123456').where(code.coding[0].system='http://system.org')"
        
    def test_slice_full_fhir_path_pattern(self):
        self.__prepare_discriminator_pattern__()
        assert self.slice.full_fhir_path == \
            "Observation.component.where(code.coding[0].code='123456').where(code.coding[0].system='http://system.org')"
        
        
        
    def __prepare_discriminator_fixed__(self):
        self.slicing.discriminators = [Discriminator(type='value', path='valueString')]
        self.constraint.path = 'Observation.component.valueString'
        self.constraint.fixedValue = 'myString'
        self.slice.add_constraint(self.constraint)
        
    def test_slice_discriminating_expression_fixed_value(self):
        self.__prepare_discriminator_fixed__()
        assert self.slice.discriminating_expression == "where(valueString='myString')"
        
    def test_slice_full_fhir_path_fixed_value(self):
        self.__prepare_discriminator_fixed__()
        assert self.slice.full_fhir_path == "Observation.component.where(valueString='myString')"
        
        

    def __prepare_discriminator_extension__(self):
        self.slicing.discriminators = [Discriminator(type='value', path='url')]
        self.slice.type = 'Extension'
        self.slicing.path = 'Observation.extension'
        self.constraint.path = self.slicing.path
        profile = MagicMock()
        profile.__canonical_url__ = 'http://doman.org/extension'
        self.constraint.profile = profile
        self.slice.add_constraint(self.constraint)
                
    def test_slice_discriminating_expression_extension(self):
        self.__prepare_discriminator_extension__()
        assert self.slice.discriminating_expression == "extension('http://doman.org/extension')"
         
    def test_slice_full_fhir_path_extension(self):
        self.__prepare_discriminator_extension__()
        assert self.slice.full_fhir_path == "Observation.extension('http://doman.org/extension')"
        
        
    def test_slice_discriminating_expression_index(self):
        self.slicing.discriminators = [Discriminator(type='position', path='$this')]
        assert self.slice.discriminating_expression == "index(0)"
        
        
    def __prepare_discriminator_type__(self):
        self.slicing.discriminators = [Discriminator(type='type', path='value[x]')]
        self.constraint.path = 'Observation.component.value[x]'
        self.slice.type = 'Quantity'
        self.slice.add_constraint(self.constraint)
        
    def test_slice_discriminating_expression_type(self):
        self.__prepare_discriminator_type__()
        assert self.slice.discriminating_expression == "where(value[x] is Quantity)"

    def test_slice_full_fhir_path_type(self):
        self.__prepare_discriminator_type__()
        assert self.slice.full_fhir_path == "Observation.component.where(value[x] is Quantity)"