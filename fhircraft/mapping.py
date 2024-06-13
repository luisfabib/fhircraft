from typing import Union, Any, Optional, Tuple, List, Dict

from dataclasses import dataclass
from fhircraft.fhir.profiles import construct_profiled_resource_model, track_slice_changes, validate_profiled_resource
from fhircraft.fhir.path import FHIRPathNavigator, join_fhirpath, split_fhirpath, FHIRPathError
from fhircraft.utils import remove_none_dicts, ensure_list, replace_nth
from fhircraft.openapi.parser import load_openapi, traverse_and_replace_references, extract_json_schema
from openapi_pydantic import Schema
from jsonpath_ng.ext import parse
import datetime
import itertools
import logging
import json
    
    
def merge_schemas(schemas):
    """
    Merge multiple schemas as per the JSON Schema 'allOf' keyword.
    """
    merged_schema = {}
    for schema in schemas:
        for key, value in schema.items():
            if key in merged_schema:
                if isinstance(merged_schema[key], dict) and isinstance(value, dict):
                    merged_schema[key] = merge_schemas([merged_schema[key], value])
                elif isinstance(merged_schema[key], list) and isinstance(value, list):
                    merged_schema[key].extend(value)
                else:
                    # In case of conflict, keep the most restrictive schema (optional)
                    merged_schema[key] = value
            else:
                merged_schema[key] = value
    return merged_schema


def map_json_paths_to_fhir_paths(schema, current_json_path='', current_fhir_path=''):

    X_FHIRPATH = 'x-fhirpath'
    
    def _parse_and_join_fhir_path(parent_fhirpath, fhirpath):    
        if not parent_fhirpath:
            return fhirpath            
        if fhirpath.startswith('$this'):
            fhirpath = join_fhirpath(parent_fhirpath, fhirpath.replace('$this', ''))
        if parent_fhirpath not in fhirpath:
            raise FHIRPathError(f'Incompatible {X_FHIRPATH} definition for JSON element {current_json_path}:\n"{fhirpath}" cannot be a child element of "{parent_fhirpath}"')
        return fhirpath

    paths = {}
    

    # Handle 'allOf'
    if 'allOf' in schema:
        all_of_schemas = schema['allOf']
        merged_schema = merge_schemas(all_of_schemas)
        return map_json_paths_to_fhir_paths(merged_schema, current_json_path, current_fhir_path)

    # Handle 'anyOf'
    if 'anyOf' in schema:
        any_of_schemas = schema['anyOf']
        for subschema in any_of_schemas:
            paths.update(map_json_paths_to_fhir_paths(subschema, current_json_path, current_fhir_path))
        return paths

    # Determine the type of the schema node
    node_type = schema.get('type')
    has_properties = bool(schema.get('properties'))
    has_items = bool(schema.get('has_items'))
    fhir_path = _parse_and_join_fhir_path(current_fhir_path, schema.get('x-fhirpath', current_fhir_path or None)) 

    if node_type == 'object' or has_properties:
        properties = schema.get('properties', {})
        for prop, subschema in properties.items():
            prop_json_path = f"{current_json_path}.{prop}" if current_json_path else prop
            paths.update(map_json_paths_to_fhir_paths(subschema, prop_json_path, fhir_path))
    elif node_type == 'array' or has_items:
        items = schema.get('items', {})
        item_json_path = f"{current_json_path}[*]" if current_json_path else "[*]"
        item_fhir_path = f"{fhir_path}[*]" if fhir_path else "[*]"
        paths.update(map_json_paths_to_fhir_paths(items, item_json_path, item_fhir_path))
    else:
        paths[current_json_path] = fhir_path
    
    return paths

def map_jsonpath_values_to_fhirpaths(response: dict, schema: Schema) -> dict:

    # Create the map JSONpath <-> FHIRpath
    jsonpath_to_fhirmap_map = map_json_paths_to_fhir_paths(json.loads(schema.model_dump_json(exclude_none=True)))

    items = dict()
    for json_path, fhir_path in jsonpath_to_fhirmap_map.items():
        # If the JSONPath has not FHIRPath associated, just skip it
        if not fhir_path:
            continue
        # Check if there are arrays in the JSONPath
        array_splices = json_path.count('[*]')
        if array_splices>0:
            # Check how many elements in total are in the flattened (sub)arrays
            total_elements = len(parse(json_path).find(response))
            # Create individual JSON/FHIR-Paths for each of the items 
            for indices in itertools.product(*[range(total_elements)]*array_splices):
                item_fhir_path, item_json_path = fhir_path, json_path
                for n, index in enumerate(indices):
                    # Get the JSON/FHIR-paths for the specific position(s) in the (sub)arrays
                    item_fhir_path = replace_nth(item_fhir_path, r'\[\*\]', f'[{index}]', n)
                    item_json_path = replace_nth(item_json_path, r'\[\*\]', f'[{index}]', n)
                # Find the element item in the response
                match = parse(item_json_path).find(response)
                if match:
                    items[item_fhir_path] = match[0].value
        else:
            # Otherwise just look for the value at the JSON-path
            match = parse(json_path).find(response)
            if match:
                # Assign it to the corresponding FHIR-path if there is a value 
                items[fhir_path] = match[0].value
    return items


def convert_response_from_api_to_fhir(response: Any, openapi_file_location: str, enpoint: str, method: str, status_code: str, profile_url: Optional[str] = None) -> Any:
    
    specification = load_openapi(openapi_file_location)      

    schema = extract_json_schema(specification, enpoint, method, status_code)
    schema = traverse_and_replace_references(schema, openapi_file_location, specification)    
    fhir_resource_values = map_jsonpath_values_to_fhirpaths(response, schema)
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
        navigator.set_value(fhirpath, value)        
        navigator.get_value(join_fhirpath(fhirpath, 'single()'))

    # Disable tracking of changes in slices
    track_slice_changes(resource, False)
    
    # Cleanup resource and remove unused fields
    resource = profile.clean_elements_and_slices(resource)
    # Cleanup the resource from empty structures to be valid
    resource = profile.parse_obj(remove_none_dicts(resource.dict()))

    validate_profiled_resource(resource)
    
    return resource



def map_fhirpath_values_to_jsonpaths(resource: dict, schema: Schema) -> dict:
    
    def _parse_types(value):
        if hasattr(value,'json'):
            value = json.loads(value.json())
        elif isinstance(value, (datetime.date, datetime.datetime)):
            value = value.strftime('%Y-%m-%d')
        elif isinstance(value, dict):
            value = {key: _parse_types(val) for key,val in value.items()}
        elif isinstance(value, list):
            value = [_parse_types(val) for val in value]
        elif value is not None:
            value = str(value)
        return value
    
    navigator = FHIRPathNavigator(resource)
    # Create the map JSONpath <-> FHIRpath
    jsonpath_to_fhirmap_map = map_json_paths_to_fhir_paths(json.loads(schema.model_dump_json(exclude_none=True)))
    
    items = dict()
    for json_path, fhir_path in jsonpath_to_fhirmap_map.items():
        # If the JSONPath has not FHIRPath associated, just skip it
        if not fhir_path:
            continue
        # Check if there are arrays in the JSONPath
        array_splices = json_path.count('[*]')
        if array_splices>0:
            # Check how many elements in total are in the flattened (sub)arrays
            total_elements = len(navigator.get_value(fhir_path.replace('[*]','')) or [])
            # Create individual JSON/FHIR-Paths for each of the items 
            for indices in itertools.product(*[range(total_elements)]*array_splices):
                item_fhir_path, item_json_path = fhir_path, json_path
                for n, index in enumerate(indices):
                    # Get the JSON/FHIR-paths for the specific position(s) in the (sub)arrays
                    item_fhir_path = replace_nth(item_fhir_path, r'\[\*\]', f'[{index}]', n)
                    item_json_path = replace_nth(item_json_path, r'\[\*\]', f'[{index}]', n)
                # Find the element item in the response
                value = navigator.get_value(item_fhir_path)
                if value is not None:
                    items[item_json_path] = _parse_types(value)
        else:
            # Otherwise just look for the value at the JSON-path
            value = navigator.get_value(fhir_path)
            if value is not None:
                # Assign it to the corresponding FHIR-path if there is a value 
                items[json_path] = _parse_types(value)
    return items

def convert_response_from_fhir_to_api(response: Any, openapi_file_location: str, enpoint: str, method: str, status_code: str, profile_url: Optional[str] = None, internal_values: Optional[dict] = {}) -> Any:
        
    specification = load_openapi(openapi_file_location)      

    schema = extract_json_schema(specification, enpoint, method, status_code)
    schema = traverse_and_replace_references(schema, openapi_file_location, specification)    

    # Construct FHIR profile
    if not profile_url:
        profile_url = getattr(schema, "x-fhir-profile")
        if not profile_url:
            raise ValueError(f'The schema has no FHIR profile associated via the "x-fhir-profile" attribute.')
    profile = construct_profiled_resource_model(profile_url)  
    
    # Parse input response into the FHIR profile
    fhir_resource = profile.parse_obj(response)
    
    # Map FHIRpath valules to the corresponding JSONpaths
    json_path_values = map_fhirpath_values_to_jsonpaths(fhir_resource, schema)

    data = {}
    # Set the mapped values from the FHIR resource as well as the provided internal values 
    for json_path, value in (json_path_values | internal_values).items():
        data = parse(json_path).update_or_create(data, value)
    return data
