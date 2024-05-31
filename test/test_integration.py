from fhir_openapi.profiles import construct_profiled_resource_model, validate_profiled_resource
from fhir_openapi.path import FHIRPathNavigator

from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.observation import Observation
from fhir.resources.R4B.elementdefinition import ElementDefinition
from fhir.resources.R4B.structuredefinition import StructureDefinition, StructureDefinitionSnapshot
from pydantic.v1 import BaseModel
import requests
import json
from pydantic.v1 import ValidationError
import pytest
from unittest.mock import patch, MagicMock
from unittest import TestCase 


class IntegrationTests(TestCase):
    
    def run_integration_test(self, profile_url, resource_file, mutations={}):
        profile = construct_profiled_resource_model(profile_url)
        resource = profile.parse_file(f'test\\static\\{resource_file}')
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
        resource_file = 'observation-genomic-variant-1.json'
        self.run_integration_test(profile_url, resource_file)

    def test_integration_genomic_variant_1_mutated(self):
        profile_url = 'http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant'
        resource_file = 'observation-genomic-variant-1.json'
        self.run_integration_test(profile_url, resource_file, mutations={'category.0.coding.0.code': 'wrong_code'})

    def test_integration_genomic_variant_2(self):
        profile_url = 'http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant'
        resource_file = 'observation-genomic-variant-2.json'
        self.run_integration_test(profile_url, resource_file)

    def test_integration_genomic_variant_2_mutated(self):
        profile_url = 'http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant'
        resource_file = 'observation-genomic-variant-2.json'
        self.run_integration_test(profile_url, resource_file, mutations={'component.where(code.coding.code="48013-7").valueCodeableConcept': None})

    def test_integration_genomic_variant_2_mutated(self):
        profile_url = 'http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant'
        resource_file = 'observation-genomic-variant-1.json'
        self.run_integration_test(profile_url, resource_file, mutations={'category.0.coding.0.code': 'wrong_code'})

    def test_integration_primary_cancer_condition_1(self):
        profile_url = 'http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-primary-cancer-condition'
        resource_file = 'condition-primary-cancer-1.json'
        self.run_integration_test(profile_url, resource_file)
