from fhircraft.mapping import  merge_schemas, map_json_paths_to_fhir_paths
from fhircraft.fhir.path.engine import FHIRPathError
import pytest

class TestMergeSchemas:

    def test_merge_schemas_non_conflicting_keys(self):
        schema1 = {'type': 'object', 'properties': {'a': {'type': 'string'}}}
        schema2 = {'type': 'object', 'properties': {'b': {'type': 'number'}}}
        expected = {'type': 'object', 'properties': {'a': {'type': 'string'}, 'b': {'type': 'number'}}}
        result = merge_schemas([schema1, schema2])
        assert result == expected

    def test_merge_schemas_nested_objects(self):
        schema1 = {'type': 'object', 'properties': {'a': {'type': 'object', 'properties': {'b': {'type': 'string'}}}}}
        schema2 = {'type': 'object', 'properties': {'a': {'type': 'object', 'properties': {'c': {'type': 'number'}}}}}
        expected = {'type': 'object', 'properties': {'a': {'type': 'object', 'properties': {'b': {'type': 'string'}, 'c': {'type': 'number'}}}}}
        result = merge_schemas([schema1, schema2])
        assert result == expected

    def test_merge_schemas_with_arrays(self):
        schema1 = {'type': 'array', 'items': [{'type': 'string'}]}
        schema2 = {'type': 'array', 'items': [{'type': 'number'}]}
        expected = {'type': 'array', 'items': [{'type': 'string'}, {'type': 'number'}]}
        result = merge_schemas([schema1, schema2])
        assert result == expected

    def test_merge_schemas_conflicting_keys_different_types(self):
        schema1 = {'type': 'object', 'properties': {'a': {'type': 'string'}}}
        schema2 = {'type': 'object', 'properties': {'a': {'type': 'number'}}}
        expected = {'type': 'object', 'properties': {'a': {'type': 'number'}}}  # Assuming the last one wins
        result = merge_schemas([schema1, schema2])
        assert result == expected

    def test_merge_schemas_conflicting_keys_same_types(self):
        schema1 = {'type': 'object', 'properties': {'a': {'type': 'string', 'maxLength': 5}}}
        schema2 = {'type': 'object', 'properties': {'a': {'type': 'string', 'minLength': 2}}}
        expected = {'type': 'object', 'properties': {'a': {'type': 'string', 'maxLength': 5, 'minLength': 2}}}
        result = merge_schemas([schema1, schema2])
        assert result == expected


class TestMapJsonPathsToFhirPaths:

    def test_correctly_maps_simple_json_paths_to_fhir_paths(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "x-fhirpath": "Patient.name"
                }
            }
        }
        expected = {"name": "Patient.name"}
        result,_ = map_json_paths_to_fhir_paths(schema)
        assert result == expected

    def test_handles_allof_schemas_by_merging_and_mapping_correctly(self):
        schema = {
            "allOf": [
                {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "x-fhirpath": "Patient.name"
                        }
                    }
                },
                {
                    "type": "object",
                    "properties": {
                        "birthDate": {
                            "type": "string",
                            "x-fhirpath": "Patient.birthDate"
                        }
                    }
                }
            ]
        }
        expected = {"name": "Patient.name", "birthDate": "Patient.birthDate"}
        result,_ = map_json_paths_to_fhir_paths(schema)
        assert result == expected

    def test_handles_nested_allof_schemas_by_merging_and_mapping_correctly(self):
        schema = {
            "allOf": [
                {
                    "allOf": [
                        {
                            "type": "object",
                            "properties": {
                                "address": {
                                    "type": "string",
                                    "x-fhirpath": "Patient.address"
                                }
                            }
                        },
                        {
                            "type": "object",
                            "properties": {
                                "job": {
                                    "type": "string",
                                    "x-fhirpath": "Patient.job"
                                }
                            }
                        },
                    ],
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "x-fhirpath": "Patient.name"
                        }
                    }
                },
                {
                    "type": "object",
                    "properties": {
                        "birthDate": {
                            "type": "string",
                            "x-fhirpath": "Patient.birthDate"
                        }
                    }
                }
            ]
        }
        expected = {"job": "Patient.job", "address": "Patient.address", "name": "Patient.name", "birthDate": "Patient.birthDate"}
        result,_ = map_json_paths_to_fhir_paths(schema)
        assert result == expected

    def test_handles_anyof_schemas_by_mapping_each_subschema_correctly(self):
        schema = {
            "anyOf": [
                {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "x-fhirpath": "Patient.name"
                        }
                    }
                },
                {
                    "type": "object",
                    "properties": {
                        "birthDate": {
                            "type": "string",
                            "x-fhirpath": "Patient.birthDate"
                        }
                    }
                }
            ]
        }
        expected = {"name": "Patient.name", "birthDate": "Patient.birthDate"}
        result,_ = map_json_paths_to_fhir_paths(schema)
        assert result == expected


    def test_raises_fhirpatherror_for_incompatible_x_fhirpath_definitions(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "x-fhirpath": "Patient.contact.name.given"
                }
            },
            "x-fhirpath": "Patient.name"
        }
        with pytest.raises(FHIRPathError):
            map_json_paths_to_fhir_paths(schema)

    def test_handles_schemas_without_type_gracefully(self):
        schema = {
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        }
        expected = {"name": "Patient.name"}
        result,_ = map_json_paths_to_fhir_paths(schema)
        assert result == expected

    def test_handles_schemas_with_unexpected_types_gracefully(self):
        schema = {
            "type": "unexpected_type",
            "x-fhirpath": "Patient.unexpected"
        }
        expected = {"": "Patient.unexpected"}
        result,_ = map_json_paths_to_fhir_paths(schema)
        assert result == expected