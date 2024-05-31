from typing import Union, Any, Optional

import os 
from urllib.parse import urlparse
from dataclasses import dataclass, field

from fhir_openapi.utils import load_file, load_url
from fhir_openapi.profiles import construct_profiled_resource_model, construct_with_skeleton
from fhir_openapi.path import FHIRPathNavigator
from functools import cached_property 
from fhir_openapi.utils import remove_none_dicts, ensure_list
from fhir.resources.core.utils.common import is_list_type

def extract_json_schema(openapi_spec: dict, endpoint: str, method: str, status_code: str) -> dict:
    """
    Extracts the JSON schema for a specific endpoint, method, and status code from an OpenAPI specification.

    Parameters:
    - openapi_spec (dict): The OpenAPI specification containing the endpoint definitions.
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
    paths = openapi_spec.get('paths')
    if not paths:
        raise ValueError(f"OpenAPI specification has no defined endpoints.")
    # Check if the requested enpoint exists    
    if endpoint not in paths:
        raise ValueError(f"Endpoint '{endpoint}' not found in OpenAPI specification.")
    # Check if the requested enpoint has the requested method        
    if method not in paths[endpoint]:
        raise ValueError(f"Method '{method}' not found for endpoint '{endpoint}' in OpenAPI specification.")
    # Retrieve the API endpoint's responses
    responses = paths[endpoint][method].get('responses', {})
    # Check that the desired response exists
    if status_code not in responses:
        raise ValueError(f"Status code '{status_code}' not found for endpoint '{endpoint}' and method '{method}' in OpenAPI specification.")
    # Retrieve the response's JSON schema   
    content = responses.get(status_code, {}).get('content', {})
    if 'application/json' not in content:
        raise ValueError(f"Content type 'application/json' not found for status code '{status_code}' in OpenAPI specification.")
    schema = content.get('application/json', {}).get('schema', {})
    if not schema:
        raise ValueError(f"No schema found for status code '{status_code}' in OpenAPI specification.")
    return schema


def resolve_ref(ref: str, current_file_path: str, root_schema: dict) -> dict:
    """
    Resolve a reference to a resource based on the provided reference, current file path, and root schema.

    Parameters:
    - ref (str): The reference to resolve, which can be a local reference within the same file starting with '#', a URL, or a local file path.
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
    if ref.startswith('#'):
        # Local ref within the same file
        ref_path = ref.lstrip('#/').split('/')
        ref_content = root_schema
        for part in ref_path:
            if part in ref_content:
                ref_content = ref_content[part]
            else:
                raise KeyError(f"Key '{part}' not found in the reference path.")
        return ref_content
    else:
        # Determine if the ref is a URL or local file path
        if urlparse(ref).scheme in ('http', 'https'):
            return load_url(ref)
        else:
            # Resolve relative paths
            base_path = os.path.dirname(current_file_path)
            file_path = os.path.normpath(os.path.join(base_path, ref))
            return load_file(file_path)


def traverse_and_replace_references(schema: Union[dict, list, Any], current_file_path: str, root_schema: dict) -> Union[dict, list, Any]:
    """
    Traverse the input schema recursively, replace any references with their resolved content, and merge additional attributes.

    Parameters:
    - schema (Union[dict, list, Any]): The schema to traverse and replace references within. It can be a dictionary, list, or any other valid data type.
    - current_file_path (str): The path of the current file where the schema is being processed.
    - root_schema (dict): The root schema or data structure where the references will be resolved.

    Returns:
    - Union[dict, list, Any]: The schema with references replaced by their resolved content and any additional attributes merged.

    Raises:
    - ValueError: If a circular reference is detected in the schema.
    - RuntimeError: If an error occurs while resolving a reference.

    Note:
    - This function handles both local references within the same file and external references (URLs or local file paths).
    - Circular references are prevented to avoid infinite loops during traversal.
    - Any errors that occur during reference resolution are caught and raised as a RuntimeError.
    """
    # Helper function
    def merge_additional_attributes(original_content, additional_attributes):
        merged_content = original_content.copy()
        merged_content.update(additional_attributes)
        return merged_content
    
    # Initialize set of visited references
    visited_refs = set()
    if isinstance(schema, dict):
        # Check if there are any references in the schema
        if "$ref" in schema:
            # Get the reference in the schema
            ref = schema["$ref"]
            # Prevent circular references
            if ref in visited_refs:
                raise ValueError("Circular reference detected.")
            visited_refs.add(ref)
            # Resolve the reference to get the corresponding object 
            try:
                ref_content = resolve_ref(ref, current_file_path, root_schema)
            except Exception as e:
                raise RuntimeError(f"Error resolving reference:\n{e}")
            # Recursively traverse the resolved object to resolve any nested references
            ref_content_resolved = traverse_and_replace_references(ref_content, os.path.join(os.path.dirname(current_file_path), ref), root_schema)
            # Merge the schemas
            ref_content_resolved = merge_additional_attributes(ref_content_resolved, {k: v for k, v in schema.items() if k != "$ref"})
            return ref_content_resolved
        else:
            # If not, go over the items in the schema and replace any nested references
            return { 
                key: traverse_and_replace_references(value, current_file_path, root_schema)
                    for key, value in schema.items()
            }
    elif isinstance(schema, list):
        # Go over each schema in the list
        return [
            traverse_and_replace_references(item, current_file_path, root_schema) 
                for item in schema
        ]
    else:
        return schema


@dataclass
class PathMapping:
    """
    A dataclass representing a mapping between FHIRPath and JSONPath expressions.

    Parameters:
    - schema (dict): The schema containing the FHIRPath expressions.
    - mapping (dict): The mapping between FHIRPath and JSONPath expressions.

    Attributes:
    - schema (dict): The schema containing the FHIRPath expressions.
    - mapping (dict): The mapping between FHIRPath and JSONPath expressions.

    Methods:
    - convert_fhirpath_to_jsonpath(fhirpath: str) -> Union[str, None]: Converts a FHIRPath expression to a JSONPath expression.
    - convert_jsonpath_to_fhirpath(jsonpath: str) -> Union[str, None]: Converts a JSONPath expression to a FHIRPath expression.
    """    
    schema: dict
    mapping: dict

    @cached_property
    def inverted_mapping(self):
        return {v: k for k, v in self.mapping.items()}
    
    def convert_fhirpath_to_jsonpath(self, fhirpath: str) -> Union[str, None]:
        return self.inverted_mapping.get(fhirpath)

    def convert_jsonpath_to_fhirpath(self, jsonpath: str) -> Union[str, None]:
        return self.mapping.get(jsonpath)
    
    
def construct_mapping_from_schema(schema: dict) -> PathMapping:
    """
    Constructs a mapping from a given schema.

    Parameters:
    - schema (dict): The schema from which to construct the mapping.

    Returns:
    - PathMapping: An object containing the mapping generated from the schema.
    """
    def traverse(schema: dict, path: str = "") -> dict:
        properties = {}
        if 'properties' in schema:
            for prop_name, prop_attributes in schema['properties'].items():
                full_path = f"{path}.{prop_name}" if path else prop_name
                if 'x-fhirpath' in prop_attributes:
                    properties[full_path] = prop_attributes['x-fhirpath']
                if 'properties' in prop_attributes:
                    nested_properties = traverse(prop_attributes, full_path)
                    nested_properties = {
                        prop: value.replace('$this.','') 
                        for prop,value in nested_properties.items()
                    }
                    properties.update(nested_properties)
                if 'items' in prop_attributes:
                    nested_properties = traverse(prop_attributes, full_path)
                    nested_properties = {
                        prop: value.replace('$this.','')
                        for prop,value in nested_properties.items()
                    }                    
                    properties.update(nested_properties)
        
        if 'items' in schema:
            sub_properties = traverse(schema['items'], path)
            properties.update(sub_properties)
            if 'x-fhirpath' in schema['items']:
                properties[path] = schema['items']['x-fhirpath']
                
        if 'allOf' in schema:
            for sub_schema in schema['allOf']:
                sub_properties = traverse(sub_schema, path)
                properties.update(sub_properties)

        if 'oneOf' in schema:
            for sub_schema in schema['oneOf']:
                sub_properties = traverse(sub_schema, path)
                properties.update(sub_properties)
        
        return properties
    return PathMapping(schema=schema, mapping=traverse(schema))


def map_response_values_to_fhirpaths(response: dict, mapping: PathMapping, current_path='') -> dict:
    """
    Map response values to FHIRPaths based on the provided mapping.

    Parameters:
    - response (dict): The response dictionary containing the values to be mapped.
    - mapping (PathMapping): An instance of PathMapping class containing the mapping between FHIRPath and JSONPath expressions.
    - current_path (str): The current path being processed, used for recursive mapping. Default is an empty string.

    Returns:
    dict: A dictionary containing the mapped FHIRPaths and their corresponding values.
    """
    items = {}
    for parameter, value in response.items():
        # Construct the JSONpath for the response's value
        json_path = f"{current_path}.{parameter}" if current_path else parameter
        # Map it to the corresponding FHIRpath
        fhir_path = mapping.convert_jsonpath_to_fhirpath(json_path)
        if not fhir_path:
            continue
        # Update the map based on the type of value 
        if isinstance(value, dict):
            items[fhir_path] = map_response_values_to_fhirpaths(value, mapping, current_path=json_path)
        elif isinstance(value, list):
            items[fhir_path] = [
                item if not isinstance(item, dict) 
                    else map_response_values_to_fhirpaths(item, mapping, current_path=json_path) 
                        for item in value
            ]
        else:
            items[fhir_path] = value
    return items



def convert_response_from_api_to_fhir(response: Any, openapi_specification: str, enpoint: str, method: str, status_code: str, profile_url: Optional[str] = None) -> Any:
    
    if urlparse(openapi_specification).scheme in ['http', 'https']:
        specification = load_url(openapi_specification)
    else:
        specification = load_file(openapi_specification)        

    schema = extract_json_schema(specification, enpoint, method, status_code)
    schema = traverse_and_replace_references(schema, openapi_specification, specification)    
    mapping = construct_mapping_from_schema(schema)
    fhir_resource_values = map_response_values_to_fhirpaths(response, mapping)

    # Construct FHIR profile
    if not profile_url:
        profile_url = schema.get('items',schema).get("x-fhir-profile")
        if not profile_url:
            raise ValueError(f'The schema has no FHIR profile associated via the "x-fhir-profile" attribute.')
    profile = construct_profiled_resource_model(profile_url)  

    # Construct FHIR resource with empty structure 
    resource = construct_with_skeleton(profile)
    navigator = FHIRPathNavigator(resource)

    # Set any preset values given by the constraints
    for constraint in profile.__constraints__:
        if constraint.pattern:
            navigator.set_value(constraint.path, constraint.pattern)        
        if constraint.fixedValue:
            navigator.set_value(constraint.path, constraint.fixedValue)        

    # Initialize slices in the resource
    for slicing in profile.__slicing__:
        slices_data = []
        if '[x]' in slicing.path: continue
        # Go over all slices
        for slice in slicing.slices:
            if not slice.pydantic_model:
                continue
            # Construct empty slice structure  
            slice_data = construct_with_skeleton(slice.pydantic_model)
            slice_navigator = FHIRPathNavigator(slice_data)
            # Iterate over the slice's constrains
            for constraint in slice.constraints:
                # Get the constrained element's internal path within the slice
                slice_element = constraint.path.replace(slice.slicing_group.path+'.','')
                if '[x]' in slice_element: continue
                # Set any preset values given by the constraints
                if constraint.fixedValue:
                    slice_navigator.set_value(slice_element, constraint.pattern)
                if constraint.pattern:
                    is_list = is_list_type(slice_navigator.get_pydantic_field(slice_element))
                    pattern = constraint.pattern
                    if is_list and not isinstance(pattern, list):
                        pattern = [pattern]
                    slice_navigator.set_value(slice_element, pattern)
            # Add initialized slice resource to the list
            slices_data.append(slice_data)
        # Set the full group of initialized slices to the sliced resource element
        navigator.set_value(slicing.path, slices_data)        

    # Set the values of the API response
    for fhirpath, value in fhir_resource_values.items():
        if isinstance(value, dict):
            for subpath,subvalue in value.items():
                navigator.set_value(fhirpath + '.' + subpath, subvalue)
        else:
            navigator.set_value(fhirpath, value)        

    # Remove unused/incomplete slices
    for slicing in profile.__slicing__:
        if '[x]' in slicing.path: continue
        valid_slices = ensure_list(navigator.get_value(slicing.path))
        for slice in slicing.slices:
            # Get all the elements that conform to this slice's definition           
            sliced_entries = ensure_list(navigator.get_value(slice.fhirpath))
            # Get list of slice elements that have been set by the constraints
            pattern_elements = sorted([
                constraint.path 
                    for constraint in slice.constraints 
                        if (constraint.pattern or constraint.fixedValue) and not '[x]' in constraint.path
            ])
            # Get the min. cardinality of this constraint
            min_cardinality = max([
                constraint.min 
                 for constraint in slice.constraints 
                        if constraint.path == slicing.path
            ])
            # Check for each sliced entry whether they are unusued/incomplete
            for entry in sliced_entries:
                # Get the list of non-empty slice elements
                nonempty_elements = sorted([
                    f'{slicing.path}.{element}' 
                        for element in remove_none_dicts(entry.dict()) 
                ])
                # If the only elements set are those set by the constraints, and the slice is not needed, remove it
                if min_cardinality<1 and nonempty_elements == pattern_elements:
                    valid_slices.remove(entry)
        # Set the new list with only the valid slices
        navigator.set_value(slicing.path, valid_slices)

    # Cleanup the resource from empty structures to be valid
    resource = profile.parse_obj(remove_none_dicts(resource.dict()) )

    return resource