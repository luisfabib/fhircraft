from typing import Union, Any, Optional, Tuple, List, Dict
from fhircraft.fhir.profiling.factory import construct_profiled_resource_model, track_slice_changes, validate_profiled_resource
from fhircraft.fhir.path import fhirpath, FHIRPathError
from fhircraft.fhir.path.utils import join_fhirpath
from fhircraft.openapi.parser import load_openapi, traverse_and_replace_references, extract_json_schema
from fhircraft.utils import remove_none_dicts, ensure_list, replace_nth
from fhircraft.openapi.models import Schema
from jsonpath_ng.ext import parse
from jsonschema import validate as validate_json_schema
from jsonschema.exceptions import ValidationError as JSONValidationError
from collections import defaultdict
import datetime
import itertools
import json
    
    
def merge_schemas(schemas):
    """
    Merge multiple schemas as per the JSON Schema 'allOf' keyword.

    Args:
        schemas (list): List of schemas to be merged.

    Returns:
        dict: Merged schema after combining all schemas.
    """
    merged_schema = {}
    aliases = []
    for schema in schemas:
        print(aliases)
        fhir_resource = schema.get('x-fhir-resource')
        if fhir_resource and fhir_resource.get('alias'): 
                aliases.append(fhir_resource.get('alias'))
        if schema.get('allOf'):
            merged_schema.update(merge_schemas(schema.get('allOf')))
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

    if merged_schema.get('x-fhir-resource'):
        merged_schema['x-fhir-resource']['alias'] = aliases
    return merged_schema


def map_json_schema_to_fhir_paths(schema: dict, current_json_path: str='', current_fhir_path: str='', current_scope: dict=None, resources: List[dict]=None):
    """
    Maps a JSON schema to FHIR paths based on the provided schema, current JSON path, current FHIR path, current scope, and list of resources.

    Args:
        schema (dict): The JSON schema to map to FHIR paths.
        current_json_path (str): The current JSON path being processed.
        current_fhir_path (str): The current FHIR path being processed.
        current_scope (dict): The current scope of the schema.
        resources (list): List of FHIR resources.

    Returns:
        tuple: A tuple containing two dictionaries - paths and schemas. 
            - paths (dict): A dictionary mapping FHIR profiles to JSON paths.
            - schemas (dict): A dictionary mapping FHIR profiles to JSON schemas.

    """
    def _merge_by_profiles(a,b):
        return {profile: a.get(profile,{}) | b.get(profile, {}) for profile in set(list(a.keys()) + list(b.keys()))}
    

    paths = defaultdict(dict)
    schemas = defaultdict(dict)    

    # Handle schema inheritance
    if 'allOf' in schema:
        all_of_schemas = schema['allOf']
        merged_schema = merge_schemas(all_of_schemas)
        # merged_schema.update(schema)
        merged_schema.update(schema)
        schema = merged_schema
        schema.pop('allOf')

    current_scope = schema.get('x-fhir-resource') or current_scope
    
    if not resources:
        resources = []
    resource = schema.get('x-fhir-resource')
    if resource and resource not in resources:
        resources.append(resource)
        
    # Handle polymorphism
    if 'anyOf' in schema:
        any_of_schemas = schema['anyOf']
        for subschema in any_of_schemas:
            sub_paths, sub_schemas = map_json_schema_to_fhir_paths(subschema, current_json_path, current_fhir_path, current_scope, resources)
            paths = _merge_by_profiles(paths, sub_paths)
            schemas = _merge_by_profiles(schemas, sub_schemas)
        return paths, schemas

    # Determine the type of the schema node
    node_type = schema.get('type')
    has_properties = bool(schema.get('properties'))
    has_items = bool(schema.get('has_items'))
    
    fhir_path = schema.get('x-fhirpath', current_fhir_path or None)
    fhir_profile = current_scope['profile']
    if fhir_path:
        # Context inheritance 
        if fhir_path.startswith('%context'):
            # Replace %context by current FHIRPath to join both paths
            fhir_path = fhir_path.replace('%context', current_fhir_path or current_scope.get('resourceType'))
        for resource in resources:
            for alias in ensure_list(resource.get('alias', [])): 
                if fhir_path.startswith(alias):
                    # Replace %<alias> by the root of the profiled resource
                    fhir_path = fhir_path.replace(alias, resource['resourceType'])
                    fhir_profile = resource['profile']
                elif fhir_path.startswith('%resource') and fhir_profile==resource['profile']:
                    # Replace %context by current FHIRPath to join both paths
                    fhir_path = fhir_path.replace('%resource', resource['resourceType'])
        
                
    # if parent_fhir_path not in fhir_path:
    #     raise FHIRPathError(f'FHIRPath inheritance error for JSON element <{current_json_path.replace("[*]","")}>:\n"{fhir_path.replace("[*]","")}" cannot be a child element of "{parent_fhir_path.replace("[*]","")}"')

    if node_type == 'object' or has_properties:
        properties = schema.get('properties', {})
        for prop, subschema in properties.items():
            prop_json_path = f"{current_json_path}.{prop}" if current_json_path else prop
            prop_paths, prop_schemas = map_json_schema_to_fhir_paths(subschema, prop_json_path, fhir_path, current_scope, resources)
            paths = _merge_by_profiles(paths, prop_paths)
            schemas = _merge_by_profiles(schemas, prop_schemas)
            
    elif node_type == 'array' or has_items:
        items = schema.get('items', {})
        item_json_path = f"{current_json_path}[*]" if current_json_path else "[*]"
        item_fhir_path = f"{fhir_path}[*]" if fhir_path else "[*]"
        item_paths, item_schemas = map_json_schema_to_fhir_paths(items, item_json_path, item_fhir_path, current_scope, resources)
        paths = _merge_by_profiles(paths, item_paths)
        schemas = _merge_by_profiles(schemas, item_schemas)
    else:
        if not current_json_path:
            paths[fhir_profile] = {}
            schemas[fhir_profile] = {}
            return paths, schemas
        paths[fhir_profile][current_json_path] = fhir_path
        schemas[fhir_profile][current_json_path] = schema
    
    return paths, schemas



def map_jsonpath_values_to_fhirpaths(response: dict, schema: Schema) -> dict:
    """
    Maps values from a JSON response to corresponding FHIR paths based on a provided JSON schema.

    Args:
        response (dict): The JSON response containing the data to map.
        schema (Schema): The JSON schema used to map JSON paths to FHIR paths.

    Returns:
        dict: A dictionary containing FHIR profiles as keys and their corresponding mapped items as values.

    Example:
        Given a JSON response and a JSON schema, this function maps the values from the response 
        to the corresponding FHIR paths based on the schema.

    """
    # Create the map JSONpath <-> FHIRpath
    jsonpath_to_fhirmap_map,_ = map_json_schema_to_fhir_paths(schema.model_dump(exclude_none=True, by_alias=True, round_trip=True))

    profiles_items = dict()
    for profile, mapping in jsonpath_to_fhirmap_map.items():
        items = dict()
        for json_path, fhir_path in mapping.items():
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
        profiles_items[profile] = items       
    return profiles_items

def convert_response_from_api_to_fhir(api_response: Any, openapi_file_location: str, enpoint: str, method: str, status_code: str) -> Any:
    """
    Converts an API response to FHIR resources based on a specified JSON schema.

    Args:
        api_response (Any): The API response data to be converted to FHIR resources.
        openapi_file_location (str): The location of the OpenAPI file containing the schema definitions.
        enpoint (str): The endpoint for which to extract the schema.
        method (str): The HTTP method (e.g., GET, POST) for the endpoint.
        status_code (str): The HTTP status code for which to extract the schema.

    Returns:
        Any: A list of FHIR resources constructed from the API response data.

    Raises:
        ValueError: If the schema has no FHIR profile associated via the "x-fhir-resource" attribute.
        JSONValidationError: If the API response is invalid for the specified JSON schema.

    Notes:
        - The function loads the OpenAPI specification, extracts the JSON schema for the specified endpoint, method, and status code.
        - It validates the API response against the schema and constructs FHIR resources based on the schema constraints.
        - FHIR resources are populated with values from the API response mapped to corresponding FHIR paths.
        - The function ensures tracking of changes in slices and cleans up the resources for validation.

    Example:
        convert_response_from_api_to_fhir(api_response, 'openapi.yaml', '/users', 'get', '200')
    """
    specification = load_openapi(openapi_file_location)      

    schema = extract_json_schema(specification, enpoint, method, status_code)
    schema = Schema.model_validate(traverse_and_replace_references(schema.model_dump(by_alias=True), openapi_file_location, specification.model_dump(by_alias=True)))    
    
    try:
        validate_json_schema(instance=api_response, schema=schema.model_dump(exclude_none=True, by_alias=True))
    except JSONValidationError as validation_error: 
        raise JSONValidationError(f'Invalid API response for specified JSON schema.\n{validation_error.message}')
    
    resources = []
    
    for response in ensure_list(api_response):

        if not schema.fhir_resource and schema.items:
            schema = schema.items
        # Construct FHIR profile
        if not schema.fhir_resource:
            raise ValueError(f'The schema has no FHIR profile associated via the "x-fhir-resource" attribute.')
    
        profiles_fhir_resource_values = map_jsonpath_values_to_fhirpaths(response, schema)

        for profile_url, fhir_resource_values in profiles_fhir_resource_values.items():
            
            profile = construct_profiled_resource_model(profile_url)  

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

            resources.append(resource)
            
    return resources



def map_fhirpath_values_to_jsonpaths(resource: dict, schema: Schema) -> dict:
    """
    Maps FHIRPath values to corresponding JSON paths based on the provided resource and schema.

    Args:
        resource (dict): The FHIR resource containing the values to map.
        schema (Schema): The JSON schema used to map the values.

    Returns:
        dict: A dictionary containing the mapped values for each profile.
    """
    def _parse_types(value, json_type):
        if json_type == 'object' and hasattr(value,'json'):
            value = json.loads(value.json())
        elif json_type == 'string' and isinstance(value, (datetime.date, datetime.datetime)):
            value = value.strftime('%Y-%m-%d')
        elif json_type == 'object' and isinstance(value, dict):
            value = {key: _parse_types(val) for key,val in value.items()}
        elif json_type == 'array' and isinstance(value, list):
            value = [_parse_types(val) for val in value]
        elif json_type == 'number' and not isinstance(value, (float, int)):
            value = float(value)
        elif json_type == 'integer' and not isinstance(value, int):
            value = int(value)
        elif value is not None:
            value = str(value)
        return value
    
    # Create the map JSONpath <-> FHIRpath
    jsonpath_to_fhirmap_map, jsonpath_to_schemas = map_json_schema_to_fhir_paths(json.loads(schema.model_dump_json(exclude_none=True, by_alias=True)))
    
    profiles_items = dict()
    for profile, mapping in jsonpath_to_fhirmap_map.items():
        items = dict()
        for json_path, fhir_path in mapping.items():
            # If the JSONPath has not FHIRPath associated, just skip it
            if not fhir_path:
                continue
            path_schema = jsonpath_to_schemas[profile][json_path]
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
                        items[item_json_path] = _parse_types(value, path_schema.get('type'))
            else:
                # Otherwise just look for the value at the JSON-path
                value = fhirpath.parse(fhir_path).get_value(resource) 
                if value is not None:
                    # Assign it to the corresponding FHIR-path if there is a value 
                    items[json_path] = _parse_types(value, path_schema.get('type'))
        profiles_items[profile] = items
    return profiles_items

def convert_response_from_fhir_to_api(response: Any, openapi_file_location: str, enpoint: str, method: str, status_code: str, profile_url: Optional[str] = None, internal_values: Optional[dict] = {}) -> Any:
    """
    Converts a response from FHIR format to API format based on the provided OpenAPI specification.

    Args:
        response (Any): The response data in FHIR format to be converted.
        openapi_file_location (str): The file location of the OpenAPI specification.
        enpoint (str): The endpoint for which to extract the schema.
        method (str): The HTTP method (e.g., GET, POST) for the endpoint.
        status_code (str): The HTTP status code for which to extract the schema.
        profile_url (Optional[str]): The URL of the FHIR profile associated with the schema (default: None).
        internal_values (Optional[dict]): Internal values to be included in the conversion (default: {}).

    Returns:
        Any: The converted response data in API format.

    Raises:
        ValueError: If the schema has no FHIR profile associated via the "x-fhir-resource" attribute.

    Notes:
        - Loads the OpenAPI specification and extracts the JSON schema for the specified endpoint, method, and status code.
        - Constructs the FHIR profile based on the provided profile URL or the schema's "x-fhir-resource" attribute.
        - Parses the input response into the FHIR profile and maps FHIRPath values to corresponding JSON paths.
        - Validates the converted data against the JSON schema before returning.

    Example:
        convert_response_from_fhir_to_api(response, 'openapi_spec.yaml', '/users', 'get', '200', profile_url='https://example.com/profile')

    """
    specification = load_openapi(openapi_file_location)      

    schema = extract_json_schema(specification, enpoint, method, status_code)
    schema = Schema.model_validate(traverse_and_replace_references(schema.model_dump(by_alias=True), openapi_file_location, specification.model_dump(by_alias=True)))    

    # Construct FHIR profile
    if not profile_url and not schema.fhir_resource:
        raise ValueError(f'The schema has no FHIR profile associated via the "x-fhir-resource" attribute.')
    profile = construct_profiled_resource_model(profile_url or schema.fhir_resource.profile)  
    
    # Parse input response into the FHIR profile
    fhir_resource = profile.parse_obj(response)
    
    # Map FHIRpath valules to the corresponding JSONpaths
    profiles_json_path_values = map_fhirpath_values_to_jsonpaths(fhir_resource, schema)
    
    data = {}
    # Set the mapped values from the FHIR resource as well as the provided internal values 

    for json_path_values in profiles_json_path_values.values():
        for json_path, value in (json_path_values | internal_values).items():
            data = parse(json_path).update_or_create(data, value)

    validate_json_schema(instance=data, schema=schema.model_dump(exclude_none=True, by_alias=True))

    return data
