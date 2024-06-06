from fhir_openapi.openapi import extract_json_schema, resolve_ref, traverse_and_replace_references, construct_mapping_from_schema, PathMappingCollection, PathMappingProperties, map_jsonpath_values_to_fhirpaths
from fhir_openapi.path import FHIRPathError
import pytest  
import requests
from datetime import date 
from openapi_pydantic import OpenAPI, Schema
import yaml 


class TestExtractJsonSchema:

    # Extract schema for valid endpoint, method, and status code
    def test_extract_schema_valid_endpoint_method_status_code(self):
        
        expected_schema = Schema(**{
            "type": "object",
            "properties": {
                "id": {"type": "string"}
            }
        })     
            
        openapi_spec = {
            "openapi": "3.1.0","info": {"title": "Test API","version": "0.0.1"},
            "paths": { 
                "/example": {
                    "get": {
                        "responses": {'200': {
                            "description": "Simple response",
                            "content": {"application/json": { "schema": expected_schema.model_dump()}}
                        }}
                    }
                }
            }
        }   
        openapi = OpenAPI(**openapi_spec)
        schema = extract_json_schema(openapi, "/example", "get", "200")
        assert schema == expected_schema

    # Extract schema when OpenAPI spec contains multiple endpoints
    def test_extract_schema_multiple_endpoints(self):
        schema1 = Schema(**{
            "type": "object",
            "properties": {
                "id": {"type": "string"}
            }
        })
        schema2 = Schema(**{
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        })
        openapi_spec = {
            "openapi": "3.1.0","info": {"title": "Test API","version": "0.0.1"},
            "paths": {
                "/example1": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Simple response",
                                "content": {
                                    "application/json": {
                                        "schema": schema1
                                    }
                                }
                            }
                        }
                    }
                },
                "/example2": {
                    "post": {
                        "responses": {
                            "201": {
                                "description": "Simple response",
                                "content": {
                                    "application/json": {
                                        "schema": schema2
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        openapi = OpenAPI(**openapi_spec)
        schema = extract_json_schema(openapi, "/example2", "post", "201")
        assert schema == schema2

    # OpenAPI spec has no defined endpoints
    def test_no_defined_endpoints(self):
        openapi_spec = OpenAPI.model_construct()
        with pytest.raises(ValueError, match="OpenAPI specification has no defined endpoints."):
            extract_json_schema(openapi_spec, "/example", "get", "200")
            

class TestResolveRef:

    # Resolves local reference within the same file correctly
    def test_resolves_local_reference_within_same_file(self):
        root_schema = {
            "definitions": {
                "example": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    }
                }
            }
        }
        ref = "#/definitions/example"
        current_file_path = "dummy_path"
        result = resolve_ref(ref, current_file_path, root_schema)
        assert result == root_schema["definitions"]["example"]

    # Resolves URL reference correctly using requests mock with mocked Content-Type header
    def test_resolves_url_reference_correctly_with_requests_mock_with_content_type_header(self, mocker):
        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"type": "object"}
        mock_response.headers = {'Content-Type': 'application/json'}
        mocker.patch('requests.get', return_value=mock_response)

        ref = "https://example.com/schema.json"
        current_file_path = "dummy_path"
        root_schema = {}

        result = resolve_ref(ref, current_file_path, root_schema)
        assert result == {"type": "object"}

    # Resolves local file path reference correctly using load_file function with normalized paths (Fixed)
    def test_resolves_local_file_path_reference_correctly_with_join_normalized_paths(self, mocker):
        mock_load_file = mocker.patch('fhir_openapi.openapi.load_file')
        mock_load_file.return_value = {"type": "object"}
        ref = "local_schema.yaml"
        current_file_path = "/path/to/current/file.yaml"
        root_schema = {}
        result = resolve_ref(ref, current_file_path, root_schema)
        assert result == {"type": "object"}

    # Raises KeyError when a key in the reference path is not found in the root schema
    def test_raises_keyerror_for_missing_key_in_reference_path(self):
        root_schema = {
            "definitions": {
                "example": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    }
                }
            }
        }
        ref = "#/definitions/nonexistent"
        current_file_path = "dummy_path"
        with pytest.raises(KeyError):
            resolve_ref(ref, current_file_path, root_schema)
            
            
class TestTraverseAndReplaceReferences:

    # correctly resolves local references within the same file and includes the 'definitions' key in the expected result
    def test_resolves_local_references_with_definitions_key(self):
        schema = Schema.model_validate({
            "definitions": {
                "example": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    }
                }
            },
            "$ref": "#/definitions/example"
        })
        current_file_path = "test_file.json"
        root_schema = schema

        result = traverse_and_replace_references(schema, current_file_path, root_schema)
        expected = Schema.model_validate({
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "definitions": {
                "example": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    }
                }
            }
        })

        assert result.model_dump() == expected.model_dump()

    # Ensure that external references from URLs are resolved successfully with a mocked response without raising HTTP errors
    def test_resolves_external_references_from_urls_with_mock_success_response(self, mocker):
        schema = Schema.model_validate({
            "$ref": "http://example.com/schema.json"
        })
        current_file_path = "test_file.json"
        root_schema = Schema()

        visited_refs = set()

        mock_load_url = mocker.patch('fhir_openapi.openapi.load_url')
        mock_load_url.return_value = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }

        result = traverse_and_replace_references(schema, current_file_path, root_schema)
        expected = Schema.model_validate({
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        })

        assert result.model_dump() == expected.model_dump()

    # Ensure that external references from local file paths are resolved correctly with the 'os.path.normpath' function mocked.
    def test_resolves_external_references_from_local_file_paths_with_normpath_mocked(self, mocker):
        schema = Schema.model_validate({
            "$ref": "external_schema.json"
        })
        current_file_path = "/path/to/test_file.json"
        root_schema = Schema()

        mocker.patch('os.path.normpath', return_value='/path/to/external_schema.json')

        mock_load_file = mocker.patch('fhir_openapi.openapi.load_file')
        mock_load_file.return_value = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }

        result = traverse_and_replace_references(schema, current_file_path, root_schema)
        expected = Schema.model_validate({
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        })

        assert result.model_dump() == expected.model_dump()

    # Detects and handles RecursionError when circular references occur
    def test_detects_and_handles_recursion_error(self):
        schema = Schema.model_validate({
            "$ref": "#/definitions/example"
        })
        current_file_path = "test_file.json"
        root_schema = Schema.model_validate({
            "definitions": {
                "example": {
                    "$ref": "#/definitions/example"
                }
            }
        })

        with pytest.raises(RecursionError):
            traverse_and_replace_references(schema, current_file_path, root_schema)

    # handles missing keys in reference paths
    def test_handles_missing_keys_in_reference_paths(self):
        schema = Schema.model_validate({
            "$ref": "#/definitions/nonexistent"
        })
        current_file_path = "test_file.json"
        root_schema = Schema.model_validate({
            "definitions": {
                "example": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    }
                }
            }
        })

        with pytest.raises(RuntimeError, match="Error resolving reference"):
            traverse_and_replace_references(schema, current_file_path, root_schema)

    # handles invalid reference formats
    def test_handles_invalid_reference_formats(self):
        schema = Schema.model_validate({
            "$ref": "invalid_format"
        })
        current_file_path = "test_file.json"
        root_schema = Schema()

        with pytest.raises(RuntimeError, match="Error resolving reference"):
            traverse_and_replace_references(schema, current_file_path, root_schema)
            
            
            
            
class TestPathMapping:


    # construct_mapping_from_schema correctly constructs PathMapping instance from valid schema
    def test_construct_mapping_correct_data_type(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        assert isinstance(path_mapping, PathMappingCollection)


    def test_map_properties(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "name"
        assert mapping_info.fhir_path == "Patient.name"
        assert mapping_info.nested_properties is None 
        assert mapping_info.nested_items is None 
        
    def test_map_properties_nested(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {
                    "type": "object",
                    "properties": {
                        "given":{
                            "type": "string",
                            "x-fhirpath": "Patient.name.given"
                        } 
                    },
                    "x-fhirpath": "Patient.name"
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "name"
        assert mapping_info.fhir_path == "Patient.name"
        assert mapping_info.nested_properties is not None 
        assert mapping_info.nested_items is None 
        nested_mapping_info = mapping_info.nested_properties.mapping_properties[0]
        assert nested_mapping_info.json_path == 'name.given'
        assert nested_mapping_info.fhir_path == 'Patient.name.given'
        assert nested_mapping_info.nested_properties is None
        assert nested_mapping_info.nested_items is None

    def test_map_properties_array_of_objects(self):
        schema = Schema.model_validate({
            "properties": {
                "addressPeriods": {
                    "type": "array",
                    "x-fhirpath": "Patient.address",                    
                    "items": {
                        "type": "object",
                        "x-fhirpath": "Patient.address.period",                            
                        "properties": {
                            "start": {
                                "type": "string",
                                "x-fhirpath": "Patient.address.period.start",   
                            },
                            "end": {
                                "type": "string",
                                "x-fhirpath": "Patient.address.period.end",   
                            }
                        }
                    }
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "addressPeriods"
        assert mapping_info.fhir_path == "Patient.address"
        array_mapping_info = mapping_info.nested_items.mapping_properties[0]
        assert array_mapping_info.json_path == 'addressPeriods[*]'
        assert array_mapping_info.fhir_path == 'Patient.address.period'
        nested_mapping_info = array_mapping_info.nested_properties.mapping_properties[0]
        assert nested_mapping_info.json_path == 'addressPeriods[*].start'
        assert nested_mapping_info.fhir_path == 'Patient.address.period.start'
        nested_mapping_info = array_mapping_info.nested_properties.mapping_properties[1]
        assert nested_mapping_info.json_path == 'addressPeriods[*].end'
        assert nested_mapping_info.fhir_path == 'Patient.address.period.end'

    def test_map_properties_fhirpath_inheritance(self):
        schema = Schema.model_validate({
            "properties": {
                "addressPeriods": {
                    "type": "array",
                    "x-fhirpath": "Patient.address",                    
                    "items": {
                        "type": "object",
                        "x-fhirpath": "$this.period",                            
                        "properties": {
                            "start": {
                                "type": "string",
                                "x-fhirpath": "$this.start",   
                            },
                            "end": {
                                "type": "string",
                                "x-fhirpath": "$this.end",   
                            }
                        }
                    }
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "addressPeriods"
        assert mapping_info.fhir_path == "Patient.address"
        array_mapping_info = mapping_info.nested_items.mapping_properties[0]
        assert array_mapping_info.json_path == 'addressPeriods[*]'
        assert array_mapping_info.fhir_path == 'Patient.address.period'
        nested_mapping_info = array_mapping_info.nested_properties.mapping_properties[0]
        assert nested_mapping_info.json_path == 'addressPeriods[*].start'
        assert nested_mapping_info.fhir_path == 'Patient.address.period.start'
        nested_mapping_info = array_mapping_info.nested_properties.mapping_properties[1]
        assert nested_mapping_info.json_path == 'addressPeriods[*].end'
        assert nested_mapping_info.fhir_path == 'Patient.address.period.end'


    def test_map_properties_fhirpath_inheritance2(self):
        schema = Schema.model_validate({
            "properties": {
                "names": {
                    "type": "array",
                    "x-fhirpath": "Patient.name",                    
                    "items": {
                        "type": "object",
                        "properties": {
                            "oficial": {
                                "type": "string",
                                "x-fhirpath": "Patient.name.given",   
                            },
                            "nickname": {
                                "type": "string",
                            }
                        }
                    }
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "names"
        assert mapping_info.fhir_path == "Patient.name"
        array_mapping_info = mapping_info.nested_items.mapping_properties[0]
        assert array_mapping_info.json_path == 'names[*]'
        assert array_mapping_info.fhir_path == 'Patient.name'
        nested_mapping_info = array_mapping_info.nested_properties.mapping_properties[0]
        assert nested_mapping_info.json_path == 'names[*].oficial'
        assert nested_mapping_info.fhir_path == 'Patient.name.given'
        
        
    def test_map_properties_array_of_primitives(self):
        schema = Schema.model_validate({
            "properties": {
                "addresses": {
                    "type": "array",
                    "x-fhirpath": "Patient.address",                    
                    "items": {
                        "type": "string",
                        "x-fhirpath": "Patient.address.city"                            
                    }
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        mapping_info = path_mapping.mapping_properties[0]
        assert mapping_info.json_path == "addresses"
        assert mapping_info.fhir_path == "Patient.address"
        array_mapping_info = mapping_info.nested_items.mapping_properties[0]
        assert array_mapping_info.json_path == 'addresses[*]'
        assert array_mapping_info.fhir_path == 'Patient.address.city'


    def test_incompatible_fhirpaths(self):
        schema = Schema.model_validate({
            "properties": {
                "addresses": {
                    "type": "array",
                    "x-fhirpath": "Patient.address",                    
                    "items": {
                        "type": "string",
                        "x-fhirpath": "Patient.name.given"                            
                    }
                }
            }
        })
        with pytest.raises(FHIRPathError):
            construct_mapping_from_schema(schema)
        

    def test_convert_jsonpath_to_fhirpath_correct(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.convert_jsonpath_to_fhirpath("name") == "Patient.name"

    def test_convert_fhirpath_to_jsonpath_correct(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.convert_fhirpath_to_jsonpath("Patient.name") == "name"

    # construct_mapping_from_schema handles schema with 'allOf' and 'oneOf' correctly
    def test_construct_mapping_from_schema_allOf_oneOf(self):
        schema = Schema.model_validate({
            "allOf": [
                {
                    "properties": {
                        "name": {
                            "x-fhirpath": "Patient.name"
                        }
                    }
                },
                {
                    "properties": {
                        "gender": {
                            "x-fhirpath": "Patient.gender"
                        }
                    }
                }
            ]
        })
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.convert_jsonpath_to_fhirpath("name") == "Patient.name"
        assert path_mapping.convert_jsonpath_to_fhirpath("gender") == "Patient.gender"

    # PathMapping handles schema with missing 'x-fhirpath' attributes
    def test_handles_missing_fhirpath_attributes(self):
        schema = Schema.model_validate({
            "properties": {
                "name": {}
            }
        })
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping
        

class TestMapResponseValuesToFhirpaths:

    def test_maps_primitive_values(self):
        response = {"name": "John Doe"}
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="name", fhir_path="Patient.name"),
        ])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name": "John Doe"}

    def test_maps_and_omits_non_mapped_values(self):
        response = {"name": "John Doe", "age": 30}
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="name", fhir_path="Patient.name"),
        ])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name": "John Doe"}

    def test_maps_primitive_arrays(self):
        response = {"phones": ["123456", "789012"]}
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="phones", fhir_path="Patient.phones", 
                nested_items=PathMappingCollection([
                    PathMappingProperties(json_path="phones[*]", fhir_path="Patient.phones")                    
                ])
            )
        ])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.phones.0": "123456", "Patient.phones.1": "789012"}

    def test_maps_object_arrays(self):
        response = {"names": [{"first": "James", "last": "Bond"}, {"first": "Tom", "last": "Cruise"}]}
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="names", fhir_path="Patient.name", 
                nested_items=PathMappingCollection([
                    PathMappingProperties(json_path="names[*]", fhir_path="Patient.name",
                        nested_properties=PathMappingCollection([
                            PathMappingProperties(json_path="names[*].first", fhir_path="Patient.name.first"),    
                            PathMappingProperties(json_path="names[*].last", fhir_path="Patient.name.last")    
                        ])
                    )
                ])                
            )
        ])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name.0.first": "James", "Patient.name.0.last": "Bond", "Patient.name.1.first": "Tom", "Patient.name.1.last": "Cruise"}
        
        
    def test_handles_mixed_types(self):
        response = {"name": "John Doe", "phones": ["123456", "789012"]}
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="name", fhir_path="Patient.name"), 
            PathMappingProperties(json_path="phones", fhir_path="Patient.phones", 
                nested_items=PathMappingCollection([
                    PathMappingProperties(json_path="phones[*]", fhir_path="Patient.phones")                    
                ])
            )
        ])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name": "John Doe", "Patient.phones.0": "123456", "Patient.phones.1": "789012"}


    def test_map_deeply_nested(self):
        response = {
            "contacts": [
                {
                    "names": [
                        {"first": "James", "last": "Bond"}, 
                        {"first": "Daniel", "last": "Craig"}
                    ]
                },
                {
                    "names": [
                        {"first": "Ethan", "last": "Hunt"}, 
                        {"first": "Tom", "last": "Cruise"}
                    ]
                }
            ]
        }
        mapping = PathMappingCollection([
            PathMappingProperties(json_path="contacts", fhir_path="Patient.contact", 
                nested_items=PathMappingCollection([
                    PathMappingProperties(json_path="contacts[*]", fhir_path="Patient.contact",
                        nested_properties=PathMappingCollection([
                            PathMappingProperties(json_path="contacts[*].names", fhir_path="Patient.contact.name", 
                                nested_items=PathMappingCollection([
                                    PathMappingProperties(json_path="contacts[*].names[*]", fhir_path="Patient.contact.name",
                                        nested_properties=PathMappingCollection([
                                            PathMappingProperties(json_path="contacts[*].names[*].first", fhir_path="Patient.contact.name.first"),    
                                            PathMappingProperties(json_path="contacts[*].names[*].last", fhir_path="Patient.contact.name.last")
                                        ])
                                    )
                                ])
                            )    
                        ])
                    )
                ])                
            )
        ])
        expected = {
            "Patient.contact.0.name.0.first": "James", 
            "Patient.contact.0.name.0.last": "Bond", 
            "Patient.contact.0.name.1.first": "Daniel", 
            "Patient.contact.0.name.1.last": "Craig", 
            "Patient.contact.1.name.0.first": "Ethan", 
            "Patient.contact.1.name.0.last": "Hunt",
            "Patient.contact.1.name.1.first": "Tom", 
            "Patient.contact.1.name.1.last": "Cruise"
        }
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        print(result)
        assert result == expected
        
        
    def test_handles_empty_response(self):
        response = {}
        mapping = PathMappingCollection([])
        result = map_jsonpath_values_to_fhirpaths(response, mapping)
        assert result == {}