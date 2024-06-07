from typing import Union, Any, Optional, Tuple, List, Dict

from dataclasses import dataclass
from fhircraft.fhir.profiles import construct_profiled_resource_model, track_slice_changes, validate_profiled_resource
from fhircraft.fhir.path import FHIRPathNavigator, join_fhirpath, split_fhirpath, FHIRPathError
from fhircraft.utils import remove_none_dicts, ensure_list
from fhircraft.openapi.parser import load_openapi, traverse_and_replace_references, extract_json_schema
from openapi_pydantic import Schema
import datetime
    

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
        if not parent_fhirpath:
            return fhirpath            
        if fhirpath.startswith('$this'):
            fhirpath = join_fhirpath(parent_fhirpath, fhirpath.replace('$this', ''))
        if parent_fhirpath not in fhirpath:
            raise FHIRPathError(f'Incompatible {X_FHIRPATH} definition for JSON element {jsonpath}:\n"{fhirpath}" cannot be a child element of "{parent_fhirpath}"')
        return fhirpath
    
    def _construct_path_mapping_collection(schema: Schema, parent_json_path: str = "", parent_fhir_path: str = None) -> PathMappingCollection:
        mappings = []
        if schema.properties:
            for property_name, property in schema.properties.items():
                full_json_path = f"{parent_json_path}.{property_name}" if parent_json_path else property_name

                
                full_fhir_path = getattr(property, X_FHIRPATH, parent_fhir_path or None)
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


def map_jsonpath_values_to_fhirpaths(response: dict, mapping_collection: PathMappingCollection, current_path='') -> dict:
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
            properties = map_jsonpath_values_to_fhirpaths(value, mapping.nested_properties, current_path=json_path)
            for subpath, value in properties.items():
                if subpath:
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
                    nested_properties = map_jsonpath_values_to_fhirpaths(
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
                    items[join_fhirpath(array_fhir_path+f'[{index}]', subpath)] = value
        else:
            if mapping.fhir_path:
                items[mapping.fhir_path] = value
    return items


def convert_response_from_api_to_fhir(response: Any, openapi_file_location: str, enpoint: str, method: str, status_code: str, profile_url: Optional[str] = None) -> Any:
    
    specification = load_openapi(openapi_file_location)      

    schema = extract_json_schema(specification, enpoint, method, status_code)
    schema = traverse_and_replace_references(schema, openapi_file_location, specification)    
    mapping_collection = construct_mapping_from_schema(schema)
    fhir_resource_values = map_jsonpath_values_to_fhirpaths(response, mapping_collection)
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
        print(f'SET {fhirpath} -> {value}')
        navigator.set_value(fhirpath, value)        
        navigator.get_value(join_fhirpath(fhirpath, 'single()'))

    # Disable tracking of changes in slices
    track_slice_changes(resource, False)
    
    # Cleanup resource and remove unused fields
    resource = profile.clean_elements_and_slices(resource)
    # Cleanup the resource from empty structures to be valid
    resource = profile.parse_obj(resource.dict())

    validate_profiled_resource(resource)
    
    return resource


def convert_response_from_fhir_to_api(response: Any, openapi_file_location: str, enpoint: str, method: str, status_code: str, profile_url: Optional[str] = None, internal_values: Optional[dict] = {}) -> Any:
        
    specification = load_openapi(openapi_file_location)      

    schema = extract_json_schema(specification, enpoint, method, status_code)
    schema = traverse_and_replace_references(schema, openapi_file_location, specification)    
    mapping_collection = construct_mapping_from_schema(schema)

    # Construct FHIR profile
    if not profile_url:
        profile_url = getattr(schema, "x-fhir-profile")
        if not profile_url:
            raise ValueError(f'The schema has no FHIR profile associated via the "x-fhir-profile" attribute.')
    profile = construct_profiled_resource_model(profile_url)  
    
    fhir_resource = profile.parse_obj(response)
    resource_navigator = FHIRPathNavigator(fhir_resource)
    
    print(schema.model_dump_json(indent=3, exclude_unset=True))
    
    def map_fhir_to_api(mapping_collection):
        data = {}
        for mapping in mapping_collection.mapping_properties:
            if mapping.nested_properties:
                value = map_fhir_to_api(mapping.nested_properties)
            elif mapping.nested_items:
                value = map_fhir_to_api(mapping.nested_items)
                value = next(iter(value.values()), {})
                if isinstance(value, dict):
                    value = {key: ensure_list(val) for key,val in value.items()}
                    if value:   
                        value = [dict(zip(value,t)) for t in zip(*value.values())]
                
            else:
                if not mapping.fhir_path:
                    continue
                value = resource_navigator.get_value(mapping.fhir_path)
                print(f'GOT {mapping.fhir_path} -> {value}')
            import json
            
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

            data[mapping.json_path.rsplit('.',1)[-1]] = _parse_types(value)
            data = remove_none_dicts(data)
        return data
    
    converted_response = map_fhir_to_api(mapping_collection)
    for json_path, value in internal_values.items():
        converted_response[json_path] = value 
    return converted_response