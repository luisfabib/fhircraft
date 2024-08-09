from fhircraft.fhir.resources.factory import ResourceFactory, _Unset
import fhircraft.fhir.resources.datatypes.primitives as primitives
import fhircraft.fhir.resources.datatypes.R4B.complex_types as complex_types

from pydantic import Field
from pydantic.fields import FieldInfo

from unittest import TestCase 

class FactoryTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = ResourceFactory()
        cls.factory.Config = cls.factory.FactoryConfig(FHIR_release='R4B',resource_name='Test')


class TestBuildTreeStructure(FactoryTestCase):

    def test_correctly_builds_tree_structure(self):
        elements = [
            {'path': 'Patient.name', 'id': 'Patient.name', 'type': [{'code': 'string'}]},
            {'path': 'Patient.address', 'id': 'Patient.address', 'type': [{'code': 'Address'}]},
            {'path': 'Patient.identifier', 'id': 'Patient.identifier', 'type': [{'code': 'Identifier'}]}
        ]
        tree_structure = self.factory.build_tree_structure(elements)
        assert 'Patient' in tree_structure['children']
        assert 'name' in tree_structure['children']['Patient']['children']
        assert 'address' in tree_structure['children']['Patient']['children']
        assert 'identifier' in tree_structure['children']['Patient']['children']

    def test_handles_single_level_paths(self):
        elements = [
            {'path': 'name', 'id': 'name', 'type': [{'code': 'string'}]},
            {'path': 'address', 'id': 'address', 'type': [{'code': 'Address'}]}
        ]
        tree_structure = self.factory.build_tree_structure(elements)
        assert 'name' in tree_structure['children']
        assert 'address' in tree_structure['children']

    def test_processes_multiple_elements_with_different_paths(self):
        elements = [
            {'path': 'Patient.name', 'id': 'Patient.name', 'type': [{'code': 'string'}]},
            {'path': 'Patient.address.city', 'id': 'Patient.address.city', 'type': [{'code': 'string'}]}
        ]
        tree_structure = self.factory.build_tree_structure(elements)
        assert 'Patient' in tree_structure['children']
        assert 'name' in tree_structure['children']['Patient']['children']
        assert 'address' in tree_structure['children']['Patient']['children']
        assert 'city' in tree_structure['children']['Patient']['children']['address']['children']


    def test_handles_slicing(self):
        elements = [
            {'path': 'component', 'id': 'component', 'type': [{'code': 'string'}]},
            {'path': 'component', 'id': 'component:sliceA', 'type': [{'code': 'Address'}]},
            {'path': 'component', 'id': 'component:sliceA.valueString', 'type': [{'code': 'string'}]}
        ]
        tree_structure = self.factory.build_tree_structure(elements)
        assert 'component' in tree_structure['children']
        assert 'sliceA' in tree_structure['children']['component']['slices']
        assert 'valueString' in tree_structure['children']['component']['slices']['sliceA']['children']

    def test_handles_empty_list_of_elements(self):
        elements = []
        tree_structure = self.factory.build_tree_structure(elements)
        assert tree_structure == {}


class TestGetFhirType(FactoryTestCase):

    def test_parses_fhir_primitive_datatype(self):
        result = self.factory._get_FHIR_type('string')
        assert result == primitives.String

    def test_parses_fhir_complex_datatype(self):
        result = self.factory._get_FHIR_type('Coding')
        assert result == complex_types.Coding

    def test_parses_fhir_complex_datatype_from_canonical_url(self):
        result = self.factory._get_FHIR_type('http://hl7.org/fhir/StructureDefinition/Extension')
        assert result == complex_types.Extension

    def test_parses_fhir_fhirpath_datatype(self):
        result = self.factory._get_FHIR_type('http://hl7.org/fhirpath/System.String')
        assert result == primitives.String

    def test_returns_field_type_name_if_not_found(self):
        result = self.factory._get_FHIR_type('UnknownType')
        assert result == 'UnknownType'


class TestConstructPydanticField(FactoryTestCase):

    def test_output_structure(self):
        result = self.factory._construct_Pydantic_field(str, min_card=1, max_card=1)
        assert isinstance(result, tuple)
        assert isinstance(result[0], type)
        assert isinstance(result[1], FieldInfo)

    def test_constructs_required_field(self):
        field_type = primitives.String
        result = self.factory._construct_Pydantic_field(field_type, min_card=1, max_card=1)
        assert result[0] == field_type
        print(result[1])
        assert result[1].required == True