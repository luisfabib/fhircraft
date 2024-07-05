from fhircraft.mapping import convert_response_from_api_to_fhir, convert_response_from_fhir_to_api
from fhircraft.utils import load_file, ensure_list
from unittest import TestCase 

import json
import pytest
import os

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

    def convert_api_to_fhir_and_assert_equal(self, api_response_file, openapi_spec_file, fhir_response_file, endpoint):
        response = load_file(api_response_file)
        if endpoint == '/endpoint-multiple':
            response = [response]
        expected_responses = [load_file(file) for file in ensure_list(fhir_response_file)]
        converted_responses = convert_response_from_api_to_fhir(response, openapi_spec_file, endpoint, 'get', '200')
        converted_responses = ensure_list(converted_responses)
        assert len(converted_responses) == len(expected_responses)
        converted_responses = sorted(converted_responses, key=lambda obj: obj.__class__.__name__)
        for converted_response, expected_response in zip(converted_responses, expected_responses):
            converted_response = json.loads(converted_response.model_dump_json(exclude_none=True, by_alias=True))
            # Asser that resulting resources are equal
            self.assertDictEqualUnorderedLists(converted_response, expected_response)
  
    def test_conversion_genomic_variant_1(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-observation-genomic-variant-1.json', 
            openapi_spec_file='test/static/openapi-genomic-variant.yaml', 
            fhir_response_file='test/static/fhir-observation-genomic-variant-1.json',
            endpoint='/endpoint'
        )
    def test_conversion_genomic_variant_1_multiple(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-observation-genomic-variant-1.json', 
            openapi_spec_file='test/static/openapi-genomic-variant.yaml', 
            fhir_response_file='test/static/fhir-observation-genomic-variant-1.json',
            endpoint='/endpoint-multiple'
        )
        
    def test_conversion_genomic_variant_2(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-observation-genomic-variant-2.json', 
            openapi_spec_file='test/static/openapi-genomic-variant.yaml', 
            fhir_response_file='test/static/fhir-observation-genomic-variant-2.json',
            endpoint='/endpoint'
        )
        
    def test_conversion_genomic_variant_3(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-observation-genomic-variant-3.json', 
            openapi_spec_file='test/static/openapi-genomic-variant.yaml', 
            fhir_response_file='test/static/fhir-observation-genomic-variant-3.json',
            endpoint='/endpoint'
        )
        
    def test_conversion_primary_cancer_condition_1(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-condition-primary-cancer-1.json', 
            openapi_spec_file='test/static/openapi-primary-cancer-condition.yaml', 
            fhir_response_file='test/static/fhir-condition-primary-cancer-1.json',
            endpoint='/endpoint'
        )
        
    def test_conversion_primary_cancer_condition_2(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-condition-primary-cancer-2.json', 
            openapi_spec_file='test/static/openapi-primary-cancer-condition.yaml', 
            fhir_response_file='test/static/fhir-condition-primary-cancer-2.json',
            endpoint='/endpoint'
        )
        
    def test_conversion_radiotherapy_1(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-procedure-radiotherapy-1.json', 
            openapi_spec_file='test/static/openapi-procedure-radiotherapy.yaml', 
            fhir_response_file='test/static/fhir-procedure-radiotherapy-1.json',
            endpoint='/endpoint'
        )

    def test_conversion_cancer_patient_1(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-patient-cancer-1.json', 
            openapi_spec_file='test/static/openapi-cancer-patient.yaml', 
            fhir_response_file='test/static/fhir-patient-cancer-1.json',
            endpoint='/endpoint'
        )
        

    def test_conversion_mixed_variant_patient_1(self):
        self.convert_api_to_fhir_and_assert_equal(
            api_response_file='test/static/api-mixed-variant-patient-1.json', 
            openapi_spec_file='test/static/openapi-mixed-variant-and-patient.yaml', 
            fhir_response_file=[
                'test/static/fhir-patient-cancer-1.json',
                'test/static/fhir-observation-genomic-variant-1.json', 
            ],
            endpoint='/endpoint'
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
        
    def test_conversion_cancer_patient_1(self):
        self.convert_fhir_to_api_and_assert_equal(
            api_response_file='test/static/api-patient-cancer-1.json', 
            openapi_spec_file='test/static/openapi-cancer-patient.yaml', 
            fhir_response_file='test/static/fhir-patient-cancer-1.json',
            internal_values={'internalId': '123456789'}
        )