from typing import Union, Any, Optional, Tuple, List, Dict

import os 
from urllib.parse import urlparse
from dataclasses import dataclass, asdict
import traceback
from fhir_openapi.utils import load_file, load_url
from fhir_openapi.profiles import construct_profiled_resource_model, track_slice_changes
from fhir_openapi.path import FHIRPathNavigator, join_fhirpath, split_fhirpath, FHIRPathError
from functools import cached_property 
from fhir_openapi.utils import remove_none_dicts, ensure_list
from fhir.resources.core.utils.common import is_list_type
from openapi_pydantic import OpenAPI, Schema, Reference

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

    
@dataclass
class PathMappingProperties:
    fhir_path: str
    json_path: str
    nested_items: Optional[object] = None
    nested_properties: Optional[object] = None

@dataclass
class PathMappingCollection:
    mapping_properties: List[PathMappingProperties]
    
    def find_by_json_path(self, jsonpath):
        return next((mapping for mapping in self.mapping_properties if mapping.json_path == jsonpath), None)
    
    def find_by_fhir_path(self, fhirpath):
        return next((mapping for mapping in self.mapping_properties if mapping.fhir_path == fhirpath), None)
    
    def convert_fhirpath_to_jsonpath(self, fhirpath: str) -> Union[str, None]:
        return self.find_by_fhir_path(fhirpath).json_path

    def convert_jsonpath_to_fhirpath(self, jsonpath: str) -> Union[str, None]:
        return self.find_by_json_path(jsonpath).fhir_path
    
    
def construct_mapping_from_schema(schema: Schema) -> PathMappingCollection:

    X_FHIRPATH = 'x-fhirpath'
    
    def _parse_fhirpath(jsonpath, fhirpath, parent_fhirpath):    
        if fhirpath.startswith('$this'):
            fhirpath = join_fhirpath(parent_fhirpath, fhirpath.replace('$this', ''))
        if parent_fhirpath not in fhirpath:
            raise FHIRPathError(f'Incompatible {X_FHIRPATH} definition for JSON element {jsonpath}:\n"{fhirpath}" cannot be a child element of "{parent_fhirpath}"')
        return fhirpath
    
    def _construct_path_mapping_collection(schema: Schema, parent_json_path: str = "", parent_fhir_path: str = "") -> PathMappingCollection:
        mappings = []
        if schema.properties:
            for property_name, property in schema.properties.items():
                full_json_path = f"{parent_json_path}.{property_name}" if parent_json_path else property_name
                if not hasattr(property, X_FHIRPATH):
                    continue 
                full_fhir_path = getattr(property, X_FHIRPATH, parent_fhir_path)
                full_fhir_path = _parse_fhirpath(full_json_path, full_fhir_path, parent_fhir_path)
                property_mapping = PathMappingProperties(
                    fhir_path=full_fhir_path,
                    json_path=full_json_path,
                )
                                        
                if property.properties:
                    property_mapping.nested_properties = _construct_path_mapping_collection(property, full_json_path, full_fhir_path)

                if property.items:
                    property_mapping.nested_items = _construct_path_mapping_collection(property, full_json_path, full_fhir_path)

                mappings.append(property_mapping)
                
        if schema.items:
            full_json_path = f'{parent_json_path}[*]'
            full_fhir_path = getattr(schema.items, X_FHIRPATH, parent_fhir_path)
            full_fhir_path = _parse_fhirpath(full_json_path, full_fhir_path, parent_fhir_path)
            mappings.append(
                PathMappingProperties(
                    fhir_path=full_fhir_path,
                    json_path=full_json_path,
                    nested_properties=None if schema.items.type!='object' else _construct_path_mapping_collection(schema.items, full_json_path, full_fhir_path),  
                ) 
            )            
                
        if schema.allOf:
            for sub_schema in schema.allOf:
                mapping_collection = _construct_path_mapping_collection(sub_schema, parent_json_path, parent_fhir_path)
                mappings.extend(mapping_collection.mapping_properties)

        if schema.oneOf:
            for sub_schema in schema.oneOf:
                mapping_collection = _construct_path_mapping_collection(sub_schema, parent_json_path, parent_fhir_path)
                mappings.extend(mapping_collection.mapping_properties)
        
        return PathMappingCollection(mappings)
    return _construct_path_mapping_collection(schema)


def map_response_values_to_fhirpaths(response: dict, mapping_collection: PathMappingCollection, current_path='') -> dict:
    """
    Map response values to FHIRPaths based on the provided mapping.

    Parameters:
    - response (dict): The response dictionary containing the values to be mapped.
    - mapping_collection (PathMappingCollection): An instance of PathMappingCollection class containing the mapping between FHIRPath and JSONPath expressions.
    - current_path (str): The current path being processed, used for recursive mapping. Default is an empty string.

    Returns:
    dict: A dictionary containing the mapped FHIRPaths and their corresponding values.
    """
    items = dict()
    for parameter, value in response.items():
        # Construct the JSONpath for the response's value
        json_path = f"{current_path}.{parameter}" if current_path else parameter
        # Map it to the corresponding FHIRpath
        mapping = mapping_collection.find_by_json_path(json_path)
        if not mapping:
           continue
        if mapping.nested_properties:
            # Update the map based on the type of value 
            if not isinstance(value, dict):
                raise TypeError(f'Expected JSON value at "{json_path}" to be a dict.')
            properties = map_response_values_to_fhirpaths(value, mapping.nested_properties, current_path=json_path)
            for subpath, value in properties.items():
                items[subpath] = value 
        elif mapping.nested_items:
            if not isinstance(value, list):
                raise TypeError(f'Expected JSON value at "{json_path}" to be a list.')
            # Rename for clarity
            values = value
            json_path = f'{json_path}[*]'
            # Get fhirpath pointing to a list element
            array_fhir_path = mapping.fhir_path
            # Get the mapping of the elements in the array
            array_elements_mapping = mapping.nested_items.find_by_json_path(json_path)
            array_element_fhir_path = array_elements_mapping.fhir_path
            # Iterate over the different array values
            for index, value in enumerate(values):
                if isinstance(value, dict):
                    # If the value is an object (dict), recursively map its values
                    nested_properties = map_response_values_to_fhirpaths(
                        response=value, 
                        mapping_collection=array_elements_mapping.nested_properties or array_elements_mapping.nested_items, 
                        current_path=json_path
                    )
                else:
                    # Otherwise just assign the value to the array element path
                    nested_properties = {array_element_fhir_path: value}
                # For each subpath and value generate a one-to-one mapping to a FHIR path
                for subpath, value in nested_properties.items():
                    subpath = subpath.replace(array_fhir_path, '')
                    print(f'{join_fhirpath(array_fhir_path, index, subpath)} = {value}')
                    items[join_fhirpath(array_fhir_path, index, subpath)] = value
        else:
            items[mapping.fhir_path] = value
    return items



def convert_response_from_api_to_fhir(response: Any, openapi_file_location: str, enpoint: str, method: str, status_code: str, profile_url: Optional[str] = None) -> Any:
    
    specification = load_openapi(openapi_file_location)      

    schema = extract_json_schema(specification, enpoint, method, status_code)
    schema = traverse_and_replace_references(schema, openapi_file_location, specification)    
    # print('schema',schema.model_dump_json(indent=3, exclude_unset=True))
    fhirpath_mapping = construct_mapping_from_schema(schema)
    import json
    fhir_resource_values = map_response_values_to_fhirpaths(response, fhirpath_mapping)

    # Construct FHIR profile
    if not profile_url:
        profile_url = getattr(schema, "x-fhir-profile")
        if not profile_url:
            raise ValueError(f'The schema has no FHIR profile associated via the "x-fhir-profile" attribute.')
    profile = construct_profiled_resource_model(profile_url)  

    # Construct FHIR resource with propulated fields according to the profile constraints 
    resource = profile.construct_with_profiled_elements()
    navigator = FHIRPathNavigator(resource)

    # Enable tracking of changes in slices (to determine which slices were given values)
    track_slice_changes(resource, True)

    # Set the values of the API response
    for fhirpath, value in fhir_resource_values.items():
        fhirpath = fhirpath.replace('..','.')
        print(f'SET {fhirpath} -> {value}')
        try:            
            navigator.set_value(fhirpath, value)        
        except:
            raise AttributeError(f'\nError setting API response value: \n\t{value}\n to FHIR path: \n\t{fhirpath}\n\nTraceback:\n{traceback.format_exc()}')
    
    # Disable tracking of changes in slices
    track_slice_changes(resource, False)
    
    # Cleanup resource and remove unused fields
    resource = profile.clean_elements_and_slices(resource)
    return resource