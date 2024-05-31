
import os 
import yaml
import json
import requests
from urllib.parse import urljoin, urlparse

from fhir_openapi.utils import load_file, load_url
from fhir_openapi.profiles import construct_profiled_resource_model, validate_profiled_resource, construct_with_skeleton
from fhir_openapi.path import FHIRPathNavigator

from fhir_openapi.utils import remove_none_dicts
from fhir.resources.core.utils.common import is_list_type

def resolve_ref(ref, current_file_path, root_schema):
    """Resolves a $ref, either from a URL or a local file path."""
    if ref.startswith('#'):
        # Local ref within the same file
        ref_path = ref.lstrip('#/').split('/')
        ref_content = root_schema
        for part in ref_path:
            ref_content = ref_content[part]
        return ref_content
    else:
        # Determine if the ref is a URL or local file path
        if urlparse(ref).scheme in ('http', 'https'):
            return load_url(ref)
        else:
            # Resolve relative paths
            base_path = os.path.dirname(current_file_path)
            file_path = os.path.join(base_path, ref)
            return load_file(file_path)

def extract_json_schema(openapi_spec, endpoint, method, status_code):
    """
    Extract the JSON Schema for a given endpoint, HTTP method, and response status code.

    :param openapi_spec: dict, The OpenAPI specification loaded as a Python dictionary.
    :param endpoint: str, The API endpoint (path).
    :param method: str, The HTTP method (e.g., 'get', 'post').
    :param status_code: str, The response status code (e.g., '200').
    :return: dict, The JSON Schema for the specified endpoint, method, and status code.
    """
    paths = openapi_spec.get('paths', {})
    
    if endpoint not in paths:
        raise ValueError(f"Endpoint '{endpoint}' not found in OpenAPI specification.")
    
    if method not in paths[endpoint]:
        raise ValueError(f"Method '{method}' not found for endpoint '{endpoint}' in OpenAPI specification.")
    
    responses = paths[endpoint][method].get('responses', {})

    if status_code not in responses:
        raise ValueError(f"Status code '{status_code}' not found for endpoint '{endpoint}' and method '{method}' in OpenAPI specification.")
    
    content = responses[status_code].get('content', {})
    if 'application/json' not in content:
        raise ValueError(f"Content type 'application/json' not found for status code '{status_code}' in OpenAPI specification.")

    schema = content['application/json'].get('schema', {})
    if not schema:
        raise ValueError(f"No schema found for status code '{status_code}' in OpenAPI specification.")
    return schema

def traverse_and_replace(schema, current_file_path, root_schema):
    """Recursively traverse the schema and replace $ref, merging additional attributes."""
    if isinstance(schema, dict):
        if "$ref" in schema:
            ref = schema["$ref"]
            ref_content = resolve_ref(ref, current_file_path, root_schema)
            ref_content_resolved = traverse_and_replace(ref_content, os.path.join(os.path.dirname(current_file_path), ref), root_schema)
            # Merge additional attributes, overriding those in the $ref content
            ref_content_resolved.update({k: v for k, v in schema.items() if k != "$ref"})
            return ref_content_resolved
        else:
            new_schema = {}
            for key, value in schema.items():
                new_schema[key] = traverse_and_replace(value, current_file_path, root_schema)
            return new_schema
    elif isinstance(schema, list):
        return [traverse_and_replace(item, current_file_path, root_schema) for item in schema]
    else:
        return schema

def resolve(schema, current_file_path):
    """
    Replaces all $ref in the JSON schema with their actual content and returns the full resolved JSON schema.

    :param schema: dict, The JSON schema to process.
    :param current_file_path: str, The path to the current file being parsed.
    :return: dict, The schema with all $ref replaced.
    """
    root_schema = load_file(current_file_path)
    return traverse_and_replace(schema, current_file_path, root_schema)

def extract_fhirpath_mapping_from_schema(schema):
    """
    Extracts x-fhirpath attributes from a JSON schema, including those within allOf and oneOf constructs,
    and returns a flat dictionary where the keys are JSON paths and the values are x-fhirpath attributes.

    :param schema: dict, The JSON schema to extract properties from.
    :return: dict, A flat dictionary of JSON paths and their x-fhirpath attributes.
    """
    def traverse(schema, path=""):
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

    return traverse(schema)


def map_fhirpaths(d, mapping, parent_key='', sep='.'):
    """
    Flattens a nested dictionary.

    :param d: dict, The dictionary to flatten.
    :param parent_key: str, The base key for recursion (used internally).
    :param sep: str, The separator between keys.
    :return: dict, A flattened dictionary with JSON paths as keys.
    """
    items = {}
    for key, value in d.items():
        json_path = f"{parent_key}{sep}{key}" if parent_key else key
        fhir_path = mapping[json_path]
        if isinstance(value, dict):
            items[fhir_path] = map_fhirpaths(value, mapping, parent_key=json_path, sep=sep)
        elif isinstance(value, list):
            items[fhir_path] = [map_fhirpaths(item, mapping, parent_key=json_path, sep=sep) for item in value]
        else:
            items[fhir_path] = value
    return items


def convert_response_from_api_to_fhir(response, openapi_specification, enpoint, method, status_code):
    
    specification = load_file(openapi_specification)        
    schema = extract_json_schema(specification, enpoint, method, status_code)
    schema = resolve(schema, openapi_specification)
    mapping = extract_fhirpath_mapping_from_schema(schema)
    fhir_resource_values = map_fhirpaths(response, mapping)

    profile_url = schema.get('items').get("x-fhir-profile")
    profile = construct_profiled_resource_model(profile_url)  

    resource = construct_with_skeleton(profile)
    navigator = FHIRPathNavigator(resource)

    for constraint in profile.__constraints__:
        if constraint.pattern:
            navigator.set_value(constraint.path, constraint.pattern)        

    for slicing in profile.__slicing__:
        slices_data = []
        if '[x]' in slicing.path: continue
        for slice in slicing.slices:
            if not slice.pydantic_model:
                continue 
            slice_data = construct_with_skeleton(slice.pydantic_model)
            slice_navigator = FHIRPathNavigator(slice_data)

            for constraint in slice.constraints:
                slice_element = constraint.path.replace(slice.slicing_group.path+'.','')
                if '[x]' in slice_element: continue
                if constraint.fixedValue:
                    slice_navigator.set_value(slice_element, constraint.pattern)
                if constraint.pattern:
                    is_list = is_list_type(slice_navigator.get_pydantic_field(slice_element))
                    pattern = constraint.pattern
                    if is_list and not isinstance(pattern, list):
                        pattern = [pattern]
                    slice_navigator.set_value(slice_element, pattern)

            slices_data.append(slice_data)
        navigator.set_value(slicing.path, slices_data)        

    for fhirpath, value in fhir_resource_values.items():
        if isinstance(value, dict):
            for subpath,subvalue in value.items():
                navigator.set_value(fhirpath + '.' + subpath, subvalue)
        else:
            navigator.set_value(fhirpath, value)        


    for slicing in profile.__slicing__:
        if '[x]' in slicing.path: continue
        valid_slices = navigator.get_value(slicing.path)
        if not isinstance(valid_slices, list):
            valid_slices = [valid_slices]    
        for slice in slicing.slices:
            sliced_entries = navigator.get_value(slice.fhirpath)
            if not isinstance(sliced_entries, list):
                sliced_entries = [sliced_entries]
            pattern_elements = sorted([constraint.path for constraint in slice.constraints if constraint.pattern and not '[x]' in constraint.path])
            min_cardinality = max([constraint.min for constraint in slice.constraints if constraint.path == slicing.path])
            for entry in sliced_entries:
                nonempty_elements = sorted([f'{slicing.path}.{element}' for element in remove_none_dicts(entry.dict()) ])
                if min_cardinality<1 and nonempty_elements == pattern_elements:
                    valid_slices.remove(entry)
        navigator.set_value(slicing.path, valid_slices)

    data = remove_none_dicts(resource.dict()) 
    resource = profile.parse_obj(data)

    return resource