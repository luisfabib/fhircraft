import yaml
import json 
import requests 
import os
from typing import List, Any, Dict, Union

def ensure_list(item: Any) -> list:
    """
    Ensure that the input variable is converted into a list if it is not already an iterable.

    Parameters:
    variable (any): The input variable that needs to be converted into a list if it is not already an iterable.

    Returns:
    list: The input variable converted into a list, or the input variable itself if it was already an iterable.
    """
    if not isinstance(item, list):
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
    response = requests.get(url, timeout=10)
    
    response.raise_for_status()
    content_type = response.headers['Content-Type']
    
    # Use content_type.lower() to make the content type check case-insensitive
    if 'yaml' in content_type.lower():
        try:
            return yaml.safe_load(response.text)
        except yaml.YAMLError as e:
            print(f"Error loading YAML: {e}")
            return None
    elif 'json' in content_type.lower():
        try:
            return response.json()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
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
                    list_prefix = f"{new_prefix}.{i}"
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