from fhircraft.fhir.resources.factory import ResourceFactory, track_slice_changes, initialize_slices
from fhircraft.fhir.resources.slicing import Slice, Discriminator, SlicingGroup, Constraint
from unittest import TestCase
from unittest.mock import MagicMock

class TestBuildTreeStructure:

    def test_correctly_builds_tree_structure(self):
        elements = [
            {'path': 'Patient.name', 'id': 'Patient.name', 'type': [{'code': 'string'}]},
            {'path': 'Patient.address', 'id': 'Patient.address', 'type': [{'code': 'Address'}]},
            {'path': 'Patient.identifier', 'id': 'Patient.identifier', 'type': [{'code': 'Identifier'}]}
        ]
        resource_factory = ResourceFactory()
        tree_structure = resource_factory.build_tree_structure(elements)
        assert 'Patient' in tree_structure['children']
        assert 'name' in tree_structure['children']['Patient']['children']
        assert 'address' in tree_structure['children']['Patient']['children']
        assert 'identifier' in tree_structure['children']['Patient']['children']

    def test_handles_single_level_paths(self):
        elements = [
            {'path': 'name', 'id': 'name', 'type': [{'code': 'string'}]},
            {'path': 'address', 'id': 'address', 'type': [{'code': 'Address'}]}
        ]
        resource_factory = ResourceFactory()
        tree_structure = resource_factory.build_tree_structure(elements)
        assert 'name' in tree_structure['children']
        assert 'address' in tree_structure['children']

    def test_processes_multiple_elements_with_different_paths(self):
        elements = [
            {'path': 'Patient.name', 'id': 'Patient.name', 'type': [{'code': 'string'}]},
            {'path': 'Patient.address.city', 'id': 'Patient.address.city', 'type': [{'code': 'string'}]}
        ]
        resource_factory = ResourceFactory()
        tree_structure = resource_factory.build_tree_structure(elements)
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
        resource_factory = ResourceFactory()
        tree_structure = resource_factory.build_tree_structure(elements)
        assert 'component' in tree_structure['children']
        assert 'sliceA' in tree_structure['children']['component']['slices']
        assert 'valueString' in tree_structure['children']['component']['slices']['sliceA']['children']

    def test_handles_empty_list_of_elements(self):
        elements = []
        resource_factory = ResourceFactory()
        tree_structure = resource_factory.build_tree_structure(elements)
        assert tree_structure == {}