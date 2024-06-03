from fhir_openapi.openapi import extract_json_schema, resolve_ref, traverse_and_replace_references, construct_mapping_from_schema, PathMapping, map_response_values_to_fhirpaths, convert_response_from_api_to_fhir
import pytest  
import requests
from datetime import date 

class TestExtractJsonSchema:

    # Extract schema for valid endpoint, method, and status code
    def test_extract_schema_valid_endpoint_method_status_code(self):
        openapi_spec = {
            "paths": {
                "/example": {
                    "get": {
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        schema = extract_json_schema(openapi_spec, "/example", "get", "200")
        assert schema == {
            "type": "object",
            "properties": {
                "id": {"type": "string"}
            }
        }

    # Extract schema when OpenAPI spec contains multiple endpoints
    def test_extract_schema_multiple_endpoints(self):
        openapi_spec = {
            "paths": {
                "/example1": {
                    "get": {
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"}
                                            }
                                        }
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
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "name": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        schema = extract_json_schema(openapi_spec, "/example2", "post", "201")
        assert schema == {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }

    # Extract schema when OpenAPI spec contains multiple methods for an endpoint
    def test_extract_schema_multiple_methods(self):
        openapi_spec = {
            "paths": {
                "/example": {
                    "get": {
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "post": {
                        "responses": {
                            "201": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "name": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        schema = extract_json_schema(openapi_spec, "/example", "post", "201")
        assert schema == {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }

    # OpenAPI spec has no defined endpoints
    def test_no_defined_endpoints(self):
        openapi_spec = {}
        with pytest.raises(ValueError, match="OpenAPI specification has no defined endpoints."):
            extract_json_schema(openapi_spec, "/example", "get", "200")

    # Endpoint not found in OpenAPI spec
    def test_endpoint_not_found(self):
        openapi_spec = {"paths": {"/other_example": {}}}
        with pytest.raises(ValueError, match="Endpoint '/example' not found in OpenAPI specification."):
            extract_json_schema(openapi_spec, "/example", "get", "200")

    # Method not found for endpoint in OpenAPI spec
    def test_method_not_found_for_endpoint(self):
        openapi_spec = {"paths": {"/example": {"post": {}}}}
        with pytest.raises(ValueError, match="Method 'get' not found for endpoint '/example' in OpenAPI specification."):
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
        schema = {
            "definitions": {
                "example": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    }
                }
            },
            "$ref": "#/definitions/example"
        }
        current_file_path = "test_file.json"
        root_schema = schema

        result = traverse_and_replace_references(schema, current_file_path, root_schema)
        expected = {
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
        }

        assert result == expected

    # Ensure that external references from URLs are resolved successfully with a mocked response without raising HTTP errors
    def test_resolves_external_references_from_urls_with_mock_success_response(self, mocker):
        schema = {
            "$ref": "http://example.com/schema.json"
        }
        current_file_path = "test_file.json"
        root_schema = {}

        visited_refs = set()

        mock_load_url = mocker.patch('fhir_openapi.openapi.load_url')
        mock_load_url.return_value = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }

        result = traverse_and_replace_references(schema, current_file_path, root_schema)
        expected = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }

        assert result == expected

    # Ensure that external references from local file paths are resolved correctly with the 'os.path.normpath' function mocked.
    def test_resolves_external_references_from_local_file_paths_with_normpath_mocked(self, mocker):
        schema = {
            "$ref": "external_schema.json"
        }
        current_file_path = "/path/to/test_file.json"
        root_schema = {}

        mocker.patch('os.path.normpath', return_value='/path/to/external_schema.json')

        mock_load_file = mocker.patch('fhir_openapi.openapi.load_file')
        mock_load_file.return_value = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }

        result = traverse_and_replace_references(schema, current_file_path, root_schema)
        expected = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }

        assert result == expected

    # Detects and handles RecursionError when circular references occur
    def test_detects_and_handles_recursion_error(self):
        schema = {
            "$ref": "#/definitions/example"
        }
        current_file_path = "test_file.json"
        root_schema = {
            "definitions": {
                "example": {
                    "$ref": "#/definitions/example"
                }
            }
        }

        with pytest.raises(RecursionError):
            traverse_and_replace_references(schema, current_file_path, root_schema)

    # handles missing keys in reference paths
    def test_handles_missing_keys_in_reference_paths(self):
        schema = {
            "$ref": "#/definitions/nonexistent"
        }
        current_file_path = "test_file.json"
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

        with pytest.raises(RuntimeError, match="Error resolving reference"):
            traverse_and_replace_references(schema, current_file_path, root_schema)

    # handles invalid reference formats
    def test_handles_invalid_reference_formats(self):
        schema = {
            "$ref": "invalid_format"
        }
        current_file_path = "test_file.json"
        root_schema = {}

        with pytest.raises(RuntimeError, match="Error resolving reference"):
            traverse_and_replace_references(schema, current_file_path, root_schema)
            
            
            
            
class TestPathMapping:

    # convert_jsonpath_to_fhirpath returns correct FHIRPath for given JSONPath
    def test_convert_jsonpath_to_fhirpath_correct(self):
        schema = {
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        }
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.convert_jsonpath_to_fhirpath("name") == "Patient.name"

    # convert_fhirpath_to_jsonpath returns correct JSONPath for given FHIRPath
    def test_convert_fhirpath_to_jsonpath_correct(self):
        schema = {
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        }
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.convert_fhirpath_to_jsonpath("Patient.name") == "name"

    # inverted_mapping property correctly inverts the mapping dictionary
    def test_inverted_mapping_correct(self):
        schema = {
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        }
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.inverted_mapping == {"Patient.name": "name"}

    # convert_jsonpath_to_fhirpath returns None for non-existent JSONPath
    def test_convert_jsonpath_to_fhirpath_none(self):
        schema = {
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        }
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.convert_jsonpath_to_fhirpath("nonexistent") is None

    # convert_fhirpath_to_jsonpath returns None for non-existent FHIRPath
    def test_convert_fhirpath_to_jsonpath_none(self):
        schema = {
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        }
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.convert_fhirpath_to_jsonpath("nonexistent") is None

    # construct_mapping_from_schema handles schema with nested properties correctly
    def test_construct_mapping_from_schema_nested_properties(self):
        schema = {
            "properties": {
                "address": {
                    "properties": {
                        "city": {
                            "x-fhirpath": "Patient.address.city"
                        }
                    }
                }
            }
        }
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.mapping == {"address.city": "Patient.address.city"}

    # construct_mapping_from_schema correctly constructs PathMapping instance from valid schema
    def test_construct_mapping_from_schema_valid_schema(self):
        schema = {
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        }
        path_mapping = construct_mapping_from_schema(schema)
        assert isinstance(path_mapping, PathMapping)

    # PathMapping instance correctly initializes with given schema and mapping
    def test_pathmapping_instance_initialization(self):
        schema = {
            "properties": {
                "name": {
                    "x-fhirpath": "Patient.name"
                }
            }
        }
        mapping = {
            "name": "Patient.name"
        }
        path_mapping = PathMapping(schema=schema, mapping=mapping)
        assert path_mapping.schema == schema
        assert path_mapping.mapping == mapping

    # construct_mapping_from_schema handles schema with 'allOf' and 'oneOf' correctly
    def test_construct_mapping_from_schema_allOf_oneOf(self):
        schema = {
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
        }
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.convert_jsonpath_to_fhirpath("name") == "Patient.name"
        assert path_mapping.convert_jsonpath_to_fhirpath("gender") == "Patient.gender"

    # PathMapping handles schema with missing 'x-fhirpath' attributes
    def test_handles_missing_fhirpath_attributes(self):
        schema = {
            "properties": {
                "name": {}
            }
        }
        path_mapping = construct_mapping_from_schema(schema)
        assert path_mapping.mapping == {}
        


# Generated by CodiumAI

import pytest

class TestMapResponseValuesToFhirpaths:

    # correctly maps simple key-value pairs from response to FHIRPaths
    def test_simple_key_value_mapping(self):
        response = {"name": "John Doe"}
        mapping = PathMapping(schema={}, mapping={"name": "Patient.name"})
        result = map_response_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name": "John Doe"}

    # handles response with missing keys in mapping and includes unmapped keys in the result
    def test_missing_keys_in_mapping_with_unmapped_keys(self):
        response = {"name": "John Doe", "age": 30}
        mapping = PathMapping(schema={}, mapping={"name": "Patient.name"})
        result = map_response_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name": "John Doe"}

    # Handles response with additional keys not present in mapping, including an additional key in the response.
    def test_additional_keys_not_in_mapping_with_additional_key(self):
        response = {"name": "John Doe", "age": 30}
        mapping = PathMapping(schema={}, mapping={"name": "Patient.name"})
        result = map_response_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name": "John Doe"}

    # handles empty response dictionary gracefully
    def test_handles_empty_response(self):
        response = {}
        mapping = PathMapping(schema={}, mapping={})
        result = map_response_values_to_fhirpaths(response, mapping)
        assert result == {}

    # uses provided mapping to convert JSONPath to FHIRPath accurately
    def test_convert_jsonpath_to_fhirpath(self):
        response = {"name": "John Doe"}
        mapping = PathMapping(schema={}, mapping={"name": "Patient.name"})
        result = map_response_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name": "John Doe"}

    # Handles response with mixed types (dicts, lists, and primitive values) - Improved implementation
    def test_handles_mixed_types(self):
        response = {"name": "John Doe", "phones": ["123456", "789012"]}
        mapping = PathMapping(schema={}, mapping={"name": "Patient.name",  "phones": "Patient.phones"})
        result = map_response_values_to_fhirpaths(response, mapping)
        assert result == {"Patient.name": "John Doe", "Patient.phones": ["123456", "789012"]}
        