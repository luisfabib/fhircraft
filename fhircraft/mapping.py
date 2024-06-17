from typing import Union, Any, Optional, Tuple, List, Dict
from fhircraft.fhir.profiles import construct_profiled_resource_model, track_slice_changes, validate_profiled_resource
from fhircraft.fhir.path import fhirpath, FHIRPathError
from fhircraft.fhir.path.utils import join_fhirpath
from fhircraft.openapi.parser import load_openapi, traverse_and_replace_references, extract_json_schema
from fhircraft.utils import remove_none_dicts, ensure_list, replace_nth
from fhircraft.openapi.models import Schema
from jsonpath_ng.ext import parse
from jsonschema import validate as validate_json_schema
from jsonschema.exceptions import ValidationError as JSONValidationError
import datetime
import itertools
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

    def _parse_and_join_fhir_path(parent_fhir_path, fhir_path):    
        if not parent_fhir_path:
            return fhir_path            
        if fhir_path.startswith('$this'):
            fhir_path = join_fhirpath(parent_fhir_path, fhir_path.replace('$this', ''))
        if parent_fhir_path not in fhir_path:
            raise FHIRPathError(f'Incompatible FHIRPath definition for JSON element {current_json_path}:\n"{fhir_path}" cannot be a child element of "{parent_fhir_path}"')
        return fhir_path

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
    jsonpath_to_fhirmap_map = map_json_paths_to_fhir_paths(json.loads(schema.model_dump_json(exclude_none=True, by_alias=True)))

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
                    value = match[0].value
                    items[item_fhir_path] = str(value) if value is not None and not isinstance(value, bool) else value
        else:
            # Otherwise just look for the value at the JSON-path
            match = parse(json_path).find(response)
            if match:
                value = match[0].value
                # Assign it to the corresponding FHIR-path if there is a value 
                items[fhir_path] = str(value) if value is not None and not isinstance(value, bool) else value
    return items

def convert_response_from_api_to_fhir(response: Any, openapi_file_location: str, enpoint: str, method: str, status_code: str, profile_url: Optional[str] = None) -> Any:
    
    specification = load_openapi(openapi_file_location)      

    schema = extract_json_schema(specification, enpoint, method, status_code)
    schema = traverse_and_replace_references(schema, openapi_file_location, specification)    
    
    try:
        validate_json_schema(instance=response, schema=schema.model_dump(exclude_none=True, by_alias=True))
    except JSONValidationError as validation_error: 
        raise JSONValidationError(f'Invalid API response for specified JSON schema.\n{validation_error.message}')
        
    fhir_resource_values = map_jsonpath_values_to_fhirpaths(response, schema)
    # Construct FHIR profile
    if not profile_url and not schema.fhirprofile:
        raise ValueError(f'The schema has no FHIR profile associated via the "x-fhir-profile" attribute.')
    profile = construct_profiled_resource_model(profile_url or schema.fhirprofile)  

    # Construct FHIR resource with propulated fields according to the profile constraints 
    resource = profile.construct_with_profiled_elements()

    # Enable tracking of changes in slices (to determine which slices were given values)
    track_slice_changes(resource, True)

    # Set the values of the API response
    for fhir_path, value in fhir_resource_values.items():
        fhirpath.parse(fhir_path).update_or_create(resource, value)        
    
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
    
    # Create the map JSONpath <-> FHIRpath
    jsonpath_to_fhirmap_map = map_json_paths_to_fhir_paths(json.loads(schema.model_dump_json(exclude_none=True, by_alias=True)))
    
    items = dict()
    for json_path, fhir_path in jsonpath_to_fhirmap_map.items():
        # If the JSONPath has not FHIRPath associated, just skip it
        if not fhir_path:
            continue
        # Check if there are arrays in the JSONPath
        array_splices = json_path.count('[*]')
        if array_splices>0:
            # Check how many elements in total are in the flattened (sub)arrays            
            total_elements = len(fhirpath.parse(fhir_path.replace('[*]','')).get_value(resource)  or [])
            # Create individual JSON/FHIR-Paths for each of the items 
            for indices in itertools.product(*[range(total_elements)]*array_splices):
                item_fhir_path, item_json_path = fhir_path, json_path
                for n, index in enumerate(indices):
                    # Get the JSON/FHIR-paths for the specific position(s) in the (sub)arrays
                    item_fhir_path = replace_nth(item_fhir_path, r'\[\*\]', f'[{index}]', n)
                    item_json_path = replace_nth(item_json_path, r'\[\*\]', f'[{index}]', n)
                # Find the element item in the response
                value = fhirpath.parse(item_fhir_path).get_value(resource) 
                if value is not None:
                    items[item_json_path] = _parse_types(value)
        else:
            # Otherwise just look for the value at the JSON-path
            value = fhirpath.parse(fhir_path).get_value(resource) 
            if value is not None:
                # Assign it to the corresponding FHIR-path if there is a value 
                items[json_path] = _parse_types(value)
    return items

def convert_response_from_fhir_to_api(response: Any, openapi_file_location: str, enpoint: str, method: str, status_code: str, profile_url: Optional[str] = None, internal_values: Optional[dict] = {}) -> Any:
        
    specification = load_openapi(openapi_file_location)      

    schema = extract_json_schema(specification, enpoint, method, status_code)
    schema = traverse_and_replace_references(schema, openapi_file_location, specification)    

    # Construct FHIR profile
    if not profile_url and not schema.fhirprofile:
        raise ValueError(f'The schema has no FHIR profile associated via the "x-fhir-profile" attribute.')
    profile = construct_profiled_resource_model(profile_url or schema.fhirprofile)  
    
    # Parse input response into the FHIR profile
    fhir_resource = profile.parse_obj(response)
    
    # Map FHIRpath valules to the corresponding JSONpaths
    json_path_values = map_fhirpath_values_to_jsonpaths(fhir_resource, schema)
    
    data = {}
    # Set the mapped values from the FHIR resource as well as the provided internal values 

    for json_path, value in (json_path_values | internal_values).items():
        data = parse(json_path).update_or_create(data, value)
    return data
