import yaml
import json 
import requests 
import os
from typing import List, Any, Dict, Union, get_args, get_origin
from dotenv import dotenv_values
import re
from contextlib import contextmanager
from pydantic import BaseModel as PydanticV2BaseModel
from pydantic.v1 import BaseModel as PydanticV1BaseModel


# URL regex pattern
URL_PATTERNS = re.compile(
    r'^(https?|ftp)://'                      # Scheme (HTTP, HTTPS, FTP)
    r'(?:(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,}|' # Domain name
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'   # OR IPv4 address
    r'\[?[a-fA-F0-9:]+\]?)'                  # OR IPv6 address
    r'(:\d+)?'                               # Optional port
    r'(\/[a-zA-Z0-9@:%._\+~#=\/-]*)?'        # Optional path
    r'(\?[a-zA-Z0-9@:%._\+~#&=\/-]*)?'       # Optional query
    r'(#[-a-zA-Z0-9@:%._\+~#=]*)?$'          # Optional fragment
)

# Function to check if a string is a URL
def is_url(string):
    return re.match(URL_PATTERNS, string) is not None

def load_env_variables(file_path=None):
    """
    Loads environment variables from a .env file into a dictionary without changing the global environment variables.

    :param file_path: Optional path to the .env file. If not provided, it looks for a .env file in the current directory.
    :return: A dictionary containing the environment variables from the .env file.
    """
    # Determine the file path
    env_file = file_path if file_path else '.env'
    
    # Load the .env file into a dictionary
    env_vars = dotenv_values(env_file)
    
    return env_vars

def ensure_list(item: Any) -> list:
    """
    Ensure that the input variable is converted into a list if it is not already an iterable.

    Parameters:
    variable (any): The input variable that needs to be converted into a list if it is not already an iterable.

    Returns:
    list: The input variable converted into a list, or the input variable itself if it was already an iterable.
    """
    if not isinstance(item, list):
        if isinstance(item, tuple):
            return list(item)
        return [item]
    return item

def load_file(file_path: str) -> Dict:
    """
    Load data from a file based on its extension.

    Parameters:
    file_path (str): The path to the file to load.

    Returns:
    dict: The data loaded from the file as a dictionary.

    Raises:
    ValueError: If the file content is not a dictionary (for YAML files).
    """    
    with open(file_path, 'r') as file:
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.yaml' or file_extension == '.yml':
            data = yaml.safe_load(file)
            if not isinstance(data, dict):
                raise ValueError("Invalid file content. File content must be a dictionary.")
            return data
        elif file_extension == '.json':
            return json.load(file)
        else:
            raise ValueError("Unsupported file format. Please provide a .yaml, .yml, or .json file.")

def load_url(url: str) -> Dict:
    """
    Load content from a URL and parse it based on the content type (YAML or JSON).

    Parameters:
    url (str): The URL to load content from.

    Returns:
    Union[Dict, List, Any]: Parsed content from the URL. Can be a dictionary, list, or any other valid JSON/YAML data type.

    Raises:
    ValueError: If the URL format is invalid or the content type is not supported.
    """    
    # Validate the URL format
    if not url.startswith('http://') and not url.startswith('https://'):
        raise ValueError("Invalid URL format. Please provide a valid URL starting with 'http://' or 'https://'.")
    
    # Add a timeout to the requests.get call
    # Configure proxy if needed
    settings = load_env_variables()
    proxies = {
        'https': settings.get('PROXY_URL_HTTPS'), 
        'http': settings.get('PROXY_URL_HTTP')
    } if settings.get('PROXY_URL_HTTPS') or settings.get('PROXY_URL_HTTP') else None
    # Download the StructureDefinition JSON            
    response = requests.get(url, proxies=proxies, verify=settings.get('CERTIFICATE_BUNDLE_PATH'), timeout=10)
    
    response.raise_for_status()
    content_type = response.headers['Content-Type']
    
    # Use content_type.lower() to make the content type check case-insensitive
    if 'yaml' in content_type.lower():
        try:
            return yaml.safe_load(response.text)
        except yaml.YAMLError as e:
            raise ValueError(f"Error loading YAML: {e}")
    elif 'json' in content_type.lower():
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise ValueError(f"Error loading JSON: {e}")
    else:
        raise ValueError("Unsupported content type. Please provide a URL that returns .yaml, .yml, or .json content.")

def contains_only_none(d: Any) -> bool:
    """
    Check if the input contains only None values recursively.

    Parameters:
    d (Any): The input dictionary or list to check for only None values.

    Returns:
    bool: True if the input contains only None values, False otherwise.
    """    
    if isinstance(d, dict):
        return all(contains_only_none(v) for v in d.values())
    elif isinstance(d, list):
        return all(contains_only_none(item) for item in d)
    else:
        return d is None

def remove_none_dicts(d: Union[Dict[str, Any], List[Any], Any]) -> Union[Dict[str, Any], List[Any], Any]:
    """
    Remove any dictionaries with all values being None from the input dictionary recursively.

    Parameters:
    d (Union[Dict[str, Any], List[Any], Any]): The input dictionary or list to remove None values from.

    Returns:
    Union[Dict[str, Any], List[Any], Any]: The dictionary or list with None values removed.
    """
    if not isinstance(d, dict):
        return d    
    new_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = remove_none_dicts(v)
            if not contains_only_none(v):
                new_dict[k] = v
        elif isinstance(v, list):
            new_list = []
            for item in v:
                if isinstance(item, dict):
                    item = remove_none_dicts(item)
                    if not contains_only_none(item):
                        new_list.append(item)
                elif item is not None:
                    new_list.append(item)
            if new_list:
                new_dict[k] = new_list
        elif v is not None:
            new_dict[k] = v
    return new_dict


def get_dict_paths(nested_dict: Union[Dict[str, Any], List[Dict[str, Any]]], prefix: str = '') -> Dict[str, Any]:
    """
    Get all paths in a nested dictionary with their corresponding values.

    Parameters:
    nested_dict (Union[Dict[str, Any], List[Dict[str, Any]]]): The nested dictionary or list of dictionaries to extract paths from.
    prefix (str): The prefix to be added to the paths (default is '').

    Returns:
    Dict[str, Any]: A dictionary containing all paths in the nested dictionary with their corresponding values.
    """
    paths = {}
    if isinstance(nested_dict, dict):
        for key, value in nested_dict.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                paths.update(get_dict_paths(value, new_prefix))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    list_prefix = f"{new_prefix}[{i}]"
                    if isinstance(item, dict):
                        paths.update(get_dict_paths(item, list_prefix))
            else:
                if value is not None:
                    paths[new_prefix] = value
    elif isinstance(nested_dict, list):
        for i, item in enumerate(nested_dict):
            list_prefix = f"{prefix}[{i}]"
            if isinstance(item, dict):
                paths.update(get_dict_paths(item, list_prefix))
    return paths

def find_all_values_for_key(nested_object, key, current_path=''):
    """
    Recursively finds all values for a given key in a deeply nested object and returns a dictionary
    with JSONPaths as keys and the values as values.

    :param nested_object: The nested object (dictionary or list) to search.
    :param key: The key whose values are to be found.
    :param current_path: The current JSONPath (used during recursion).
    :return: A dictionary with JSONPaths as keys and the corresponding values as values.
    """
    values = {}

    if isinstance(nested_object, dict):
        for k, v in nested_object.items():
            new_path = f"{current_path}.{k}" if current_path else k
            if k == key:
                values[new_path] = v
            if isinstance(v, (dict, list)):
                values.update(find_all_values_for_key(v, key, new_path))
    elif isinstance(nested_object, list):
        for i, item in enumerate(nested_object):
            new_path = f"{current_path}[{i}]"
            if isinstance(item, (dict, list)):
                values.update(find_all_values_for_key(item, key, new_path))

    return values


def replace_nth(string, sub, wanted, n):
    pattern = re.compile(sub)
    where = [m for m in pattern.finditer(string)][n-1]
    before = string[:where.start()]
    after = string[where.end():]
    newString = before + wanted + after
    return newString

def is_list_of_lists(variable):
    if isinstance(variable, list) and all(isinstance(i, list) for i in variable):
        return True
    return False

def flatten_list_of_lists(list_of_lists):
    if not is_list_of_lists(list_of_lists):
        raise ValueError("Input is not a list of lists")
    return [item for sublist in list_of_lists for item in sublist]


@contextmanager
def suspend_assignment_validation(cls: Union[PydanticV1BaseModel,PydanticV2BaseModel], validate=False):
    
    def _get_validate_assignment():
        if isinstance(cls, PydanticV2BaseModel) or issubclass(cls, PydanticV2BaseModel):
            return cls.model_config.get('validate_assignment', True)
        elif isinstance(cls, PydanticV1BaseModel) or issubclass(cls, PydanticV1BaseModel): 
            return cls.Config.validate_assignment
        else: 
            raise TypeError('Must be a valid Pydantic v1 or v2 BaseModel')
            
    def _set_validate_assignment(val=None):
        if isinstance(cls, PydanticV2BaseModel) or issubclass(cls, PydanticV2BaseModel):
            cls.model_config['validate_assignment'] = val
        elif isinstance(cls, PydanticV1BaseModel) or issubclass(cls, PydanticV1BaseModel): 
            cls.Config.validate_assignment = val
        else: 
            raise TypeError('Must be a valid Pydantic v1 or v2 BaseModel')
            
    # Store the original value
    original_value = _get_validate_assignment()
    
    try:
        # Set validate_assignment to False
        _set_validate_assignment(validate)
        yield cls
    finally:
        _set_validate_assignment(original_value)
