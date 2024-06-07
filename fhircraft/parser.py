from typing import Union, Any, Optional, Tuple, List, Dict

import os 
from urllib.parse import urlparse
from fhircraft.utils import load_file, load_url
from openapi_pydantic import OpenAPI, Schema

def load_openapi(openapi_file_location):
    if urlparse(openapi_file_location).scheme in ['http', 'https']:
        specification = load_url(openapi_file_location)
    else:
        specification = load_file(openapi_file_location)      
    return OpenAPI.model_validate(specification)

def extract_json_schema(openapi: OpenAPI, endpoint: str, method: str, status_code: str) -> Schema:
    """
    Extracts the JSON schema for a specific endpoint, method, and status code from an OpenAPI specification.

    Parameters:
    - openapi (dict): The OpenAPI specification containing the endpoint definitions.
    - endpoint (str): The endpoint for which to extract the schema.
    - method (str): The HTTP method (e.g., GET, POST) for the endpoint.
    - status_code (str): The HTTP status code for which to extract the schema.

    Returns:
    - dict: The JSON schema for the specified endpoint, method, and status code.

    Raises:
    - ValueError: If the OpenAPI specification has no defined endpoints, the endpoint is not found in the 
                  specification, the method is not found for the endpoint, the status code is not found
                  for the endpoint and method, or if the content type 'application/json' is not found 
                  for the status code.
    """
    # Get the API endpoints
    if not openapi.paths:
        raise ValueError(f"OpenAPI specification has no defined endpoints.")
    # Check if the requested enpoint exists    
    if endpoint not in openapi.paths:
        raise ValueError(f"Endpoint '{endpoint}' not found in OpenAPI specification.")
    # Check if the requested enpoint has the requested method        
    if not getattr(openapi.paths[endpoint], method):
        raise ValueError(f"Method '{method}' not specified for endpoint '{endpoint}' in OpenAPI specification.")
    # Retrieve the API endpoint's responses
    responses = getattr(openapi.paths[endpoint], method).responses
    # Check that the desired response exists
    if status_code not in responses:
        raise ValueError(f"Status code '{status_code}' not found for endpoint '{endpoint}' and method '{method}' in OpenAPI specification.")
    # Retrieve the response's JSON schema   
    content = responses.get(status_code).content
    if 'application/json' not in content:
        raise ValueError(f"Content type 'application/json' not found for status code '{status_code}' in OpenAPI specification.")
    schema = content.get('application/json', {}).media_type_schema
    if not schema:
        raise ValueError(f"No schema found for status code '{status_code}' in OpenAPI specification.")
    return schema


def resolve_ref(reference: str, current_file_path: str, root_schema: dict) -> dict:
    """
    Resolve a reference to a resource based on the provided reference, current file path, and root schema.

    Parameters:
    - reference (str): The reference to resolve, which can be a local reference within the same file starting with '#', a URL, or a local file path.
    - current_file_path (str): The path of the current file where the reference is being resolved.
    - root_schema (dict): The root schema or data structure where the reference will be resolved.

    Returns:
    - dict or list or any: The resolved content based on the reference. It can be a dictionary, list, or any other valid data type.

    Raises:
    - KeyError: If a key in the reference path is not found in the root schema.
    - ValueError: If the reference format is invalid or the content type is not supported when resolving a URL.

    Note:
    - If the reference starts with '#', it is assumed to be a local reference within the same file.
    - If the reference is a URL, it will be loaded using the 'load_url' function.
    - If the reference is a local file path, it will be resolved based on the current file path.
    """    
    if reference.startswith('#'):
        # Local ref within the same file
        ref_path = reference.lstrip('#/').split('/')
        ref_content = root_schema
        for part in ref_path:
            if hasattr(ref_content, part):
                ref_content = getattr(ref_content, part)
            elif part in ref_content: 
                ref_content = ref_content[part]
            else:
                raise KeyError(f"Key '{part}' not found in the reference path.")
        return ref_content
    else:
        # Determine if the ref is a URL or local file path
        if urlparse(reference).scheme in ('http', 'https'):
            return load_url(reference)
        else:
            # Resolve relative paths
            base_path = os.path.dirname(current_file_path)
            file_path = os.path.normpath(os.path.join(base_path, reference))
            return load_file(file_path)


def traverse_and_replace_references(schema: Union[Schema, List[Schema]], current_file_path: str, root_schema: dict) -> Union[Schema, List[Schema]]:
    """
    Traverse the input schema recursively, replace any references with their resolved content, and merge additional attributes.

    Parameters:
    - schema (Union[Schema, List[Schema]]): The schema to traverse and replace references within. It can be a dictionary, list, or any other valid data type.
    - current_file_path (str): The path of the current file where the schema is being processed.
    - root_schema (dict): The root schema or data structure where the references will be resolved.

    Returns:
    - Union[Schema, List[Schema]]: The schema with references replaced by their resolved content and any additional attributes merged.

    Raises:
    - ValueError: If a circular reference is detected in the schema.
    - RuntimeError: If an error occurs while resolving a reference.

    Note:
    - This function handles both local references within the same file and external references (URLs or local file paths).
    - Circular references are prevented to avoid infinite loops during traversal.
    - Any errors that occur during reference resolution are caught and raised as a RuntimeError.
    """
    # Initialize set of visited references
    visited_refs = set()
    def process_iteratively(schema: Union[Schema, List[Schema]], current_file_path: str, root_schema: dict) -> dict:
        if isinstance(schema, dict):
            # Check if there are any references in the schema
            if "$ref" in schema or "ref" in schema:
                # Get the reference in the schema
                ref = schema.get('$ref') or schema.get('ref')
                # Prevent circular references
                if ref in visited_refs:
                    raise RecursionError("Circular reference detected.")
                visited_refs.add(current_file_path)
                # Resolve the reference to get the corresponding object 
                try:
                    ref_content = resolve_ref(ref, current_file_path, root_schema)
                except Exception as e:
                    raise RuntimeError(f"Error resolving reference:\n{e}")
                # Recursively traverse the resolved object to resolve any nested references
                ref_content_resolved = process_iteratively(ref_content, os.path.join(os.path.dirname(current_file_path), ref), root_schema)
                # Merge the schemas
                schema_resolved = {k: v for k, v in schema.items() if k not in ["$ref","ref"] and k is not None}
                schema_resolved.update(ref_content_resolved)
                return schema_resolved
            else:
                # If not, go over the items in the schema and replace any nested references
                return { 
                    key: process_iteratively(value, current_file_path, root_schema)
                        for key, value in schema.items()
                }
        elif isinstance(schema, list):
            # Go over each schema in the list
            return [
                process_iteratively(item, current_file_path, root_schema) 
                    for item in schema
            ]
        else:
            return schema

    schema_data = process_iteratively(schema.model_dump(exclude_unset=True), current_file_path, root_schema.model_dump(exclude_unset=True))
    return Schema.model_validate(schema_data)