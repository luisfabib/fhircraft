from fhircraft.openapi.parser import extract_json_schema, resolve_ref, traverse_and_replace_references
from fhircraft.openapi.models import OpenAPI, Schema
import pytest  


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
            "openapi": "3.1.0","info": {"title": "Test API","version": "0[0][1]"},
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
            "openapi": "3.1.0","info": {"title": "Test API","version": "0[0][1]"},
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
        mock_load_file = mocker.patch('fhircraft.openapi.parser.load_file')
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

        mock_load_url = mocker.patch('fhircraft.openapi.parser.load_url')
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

        mock_load_file = mocker.patch('fhircraft.openapi.parser.load_file')
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
            
            

    def test_resolving_references_with_override_values(self):
        schema = Schema.model_validate({
            "components": {
                "schemas": {
                    "ReferencedObject": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                            },
                            "age": {
                                "type": "string",
                            },
                            "alive": {
                                "type": "boolean"
                            }
                        }
                    }
                }
            },
            "$ref": "#/components/schemas/ReferencedObject",
            "properties": {
                "name": {
                    "type": "string",
                    "x-custom-attribute": "custom-value"
                },
                "age": {
                    "type": "integer"
                }
            }
        })
        current_file_path = "test_file.json"
        root_schema = schema
        result = traverse_and_replace_references(schema, current_file_path, root_schema)
        assert getattr(result.properties['name'],'x-custom-attribute') == 'custom-value'
        assert getattr(result.properties['age'],'type') == 'integer'
        assert getattr(result.properties['alive'],'type') == 'boolean'