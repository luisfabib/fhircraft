from fhircraft.fhir.profiles import construct_profiled_resource_model, validate_profiled_resource
from fhircraft.fhir.path import FHIRPathNavigator
from fhircraft.mapping import convert_response_from_api_to_fhir, convert_response_from_fhir_to_api
from fhircraft.utils import load_file
from pydantic.v1 import ValidationError
from unittest import TestCase 

import json
import pytest
import os


class ValidationTests(TestCase):
    
    def run_integration_test(self, profile_url, resource_file, mutations={}):
        profile = construct_profiled_resource_model(profile_url)
        resource = profile.parse_file(os.path.join('test','static',resource_file))
        for path, value in mutations.items():
            FHIRPathNavigator(resource).set_value(path, value)
        try:
            validate_profiled_resource(resource)
            if mutations:
                pytest.fail(f'Resource validation did not catch mutation')
        except ValidationError as e:
            if not mutations:
                pytest.fail(f'Resource validation failed:\n{e}')
    
    def test_integration_genomic_variant_1(self):
        profile_url = 'http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant'
        resource_file = 'fhir-observation-genomic-variant-1.json'
        self.run_integration_test(profile_url, resource_file)

    def test_integration_genomic_variant_1_mutated(self):
        profile_url = 'http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant'
        resource_file = 'fhir-observation-genomic-variant-1.json'
        self.run_integration_test(profile_url, resource_file, mutations={'category[0].coding[0].code': 'wrong_code'})

    def test_integration_genomic_variant_2(self):
        profile_url = 'http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant'
        resource_file = 'fhir-observation-genomic-variant-2.json'
        self.run_integration_test(profile_url, resource_file)

    def test_integration_genomic_variant_2_mutated(self):
        profile_url = 'http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant'
        resource_file = 'fhir-observation-genomic-variant-1.json'
        self.run_integration_test(profile_url, resource_file, mutations={'category[0].coding[0].code': 'wrong_code'})

    def test_integration_genomic_variant_3(self):
        profile_url = 'http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant'
        resource_file = 'fhir-observation-genomic-variant-3.json'
        self.run_integration_test(profile_url, resource_file)

    def test_integration_primary_cancer_condition_1(self):
        profile_url = 'http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-primary-cancer-condition'
        resource_file = 'fhir-condition-primary-cancer-1.json'
        self.run_integration_test(profile_url, resource_file)

    def test_integration_cancer_patient_1(self):
        profile_url = 'http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-patient'
        resource_file = 'fhir-patient-cancer-1.json'
        self.run_integration_test(profile_url, resource_file)





class TestConvertResponseFromApiToFhir(TestCase):
    
    def sort_nested_lists(self,data): 
        if isinstance(data, list):
            return sorted([self.sort_nested_lists(item) for item in data], key=lambda x: str(x))
        elif isinstance(data, dict):
            sorted_items = sorted(data.items(), key=lambda x: str(x[0]))
            return {key: self.sort_nested_lists(value) for key, value in sorted_items}
        else:
            return data
        
    def assertDictEqualUnorderedLists(self, dict1, dict2):
        sorted_dict1 = self.sort_nested_lists(dict1)
        sorted_dict2 = self.sort_nested_lists(dict2)
        print(json.dumps(sorted_dict1))
        print()
        print(json.dumps(sorted_dict2))
        
        self.assertDictEqual(sorted_dict1, sorted_dict2)

    def convert_api_to_fhir_and_assert_equal(self, api_response_file, openapi_spec_file, fhir_response_file):
        response = load_file(api_response_file)
        expected_response = load_file(fhir_response_file)
        converted_response = convert_response_from_api_to_fhir(response, openapi_spec_file, '/endpoint', 'get', '200')
        converted_response = json.loads(converted_response.json())
        # Asser that resulting resources are equal
        self.assertDictEqualUnorderedLists(converted_response, expected_response)
  
    def test_conversion_genomic_variant_1(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-observation-genomic-variant-1.json', 
            openapi_spec_file='test/static/openapi-genomic-variant.yaml', 
            fhir_response_file='test/static/fhir-observation-genomic-variant-1.json',
        )
        
    def test_conversion_genomic_variant_2(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-observation-genomic-variant-2.json', 
            openapi_spec_file='test/static/openapi-genomic-variant.yaml', 
            fhir_response_file='test/static/fhir-observation-genomic-variant-2.json',
        )
        
    def test_conversion_genomic_variant_3(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-observation-genomic-variant-3.json', 
            openapi_spec_file='test/static/openapi-genomic-variant.yaml', 
            fhir_response_file='test/static/fhir-observation-genomic-variant-3.json',
        )
        
    def test_conversion_primary_cancer_condition_1(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-condition-primary-cancer-1.json', 
            openapi_spec_file='test/static/openapi-primary-cancer-condition.yaml', 
            fhir_response_file='test/static/fhir-condition-primary-cancer-1.json',
        )
        
    def test_conversion_primary_cancer_condition_2(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-condition-primary-cancer-2.json', 
            openapi_spec_file='test/static/openapi-primary-cancer-condition.yaml', 
            fhir_response_file='test/static/fhir-condition-primary-cancer-2.json',
        )
        
    def test_conversion_radiotherapy_1(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-procedure-radiotherapy-1.json', 
            openapi_spec_file='test/static/openapi-procedure-radiotherapy.yaml', 
            fhir_response_file='test/static/fhir-procedure-radiotherapy-1.json',
        )
        


class TestConvertResponseFromFhirToApi(TestCase):
    
    def sort_nested_lists(self,data): 
        if isinstance(data, list):
            return sorted([self.sort_nested_lists(item) for item in data], key=lambda x: str(x))
        elif isinstance(data, dict):
            sorted_items = sorted(data.items(), key=lambda x: str(x[0]))
            return {key: self.sort_nested_lists(value) for key, value in sorted_items}
        else:
            return data
        
    def assertDictEqualUnorderedLists(self, dict1, dict2):
        sorted_dict1 = self.sort_nested_lists(dict1)
        sorted_dict2 = self.sort_nested_lists(dict2)
        print(json.dumps(sorted_dict1))
        print()
        print(json.dumps(sorted_dict2))
        
        self.assertDictEqual(sorted_dict1, sorted_dict2)

    def convert_fhir_to_api_and_assert_equal(self, api_response_file, openapi_spec_file, fhir_response_file, internal_values):
        response = load_file(fhir_response_file)
        expected_response = load_file(api_response_file)
        converted_response = convert_response_from_fhir_to_api(response, openapi_spec_file, '/endpoint', 'get', '200',internal_values=internal_values)
        converted_response = json.loads(json.dumps(converted_response))
        # Asser that resulting resources are equal
        self.assertDictEqualUnorderedLists(converted_response, expected_response)
  
    def test_conversion_genomic_variant_1(self):
        self.convert_fhir_to_api_and_assert_equal(
            api_response_file='test/static/api-observation-genomic-variant-1.json', 
            openapi_spec_file='test/static/openapi-genomic-variant.yaml', 
            fhir_response_file='test/static/fhir-observation-genomic-variant-1.json',
            internal_values={'internalId': '123456789'}
        )
        
    def test_conversion_genomic_variant_2(self):
        self.convert_fhir_to_api_and_assert_equal(
            api_response_file='test/static/api-observation-genomic-variant-2.json', 
            openapi_spec_file='test/static/openapi-genomic-variant.yaml', 
            fhir_response_file='test/static/fhir-observation-genomic-variant-2.json',
            internal_values={'internalId': '123456789'}
        )
        
    def test_conversion_genomic_variant_3(self):
        self.convert_fhir_to_api_and_assert_equal(
            api_response_file='test/static/api-observation-genomic-variant-3.json', 
            openapi_spec_file='test/static/openapi-genomic-variant.yaml', 
            fhir_response_file='test/static/fhir-observation-genomic-variant-3.json',
            internal_values={'internalId': '123456789'}
        )
        
    def test_conversion_primary_cancer_condition_1(self):
        self.convert_fhir_to_api_and_assert_equal(
            api_response_file='test/static/api-condition-primary-cancer-1.json', 
            openapi_spec_file='test/static/openapi-primary-cancer-condition.yaml', 
            fhir_response_file='test/static/fhir-condition-primary-cancer-1.json',
            internal_values={'internalId': '123456789'}
        )
        
    def test_conversion_primary_cancer_condition_2(self):
        self.convert_fhir_to_api_and_assert_equal(
            api_response_file='test/static/api-condition-primary-cancer-2.json', 
            openapi_spec_file='test/static/openapi-primary-cancer-condition.yaml', 
            fhir_response_file='test/static/fhir-condition-primary-cancer-2.json',
            internal_values={'internalId': '123456789'}
        )
        