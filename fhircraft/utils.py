import inspect
import json
import os
import re
import sys
from typing import (
    Any,
    Dict,
    Generator,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

T = TypeVar("T")

import requests
import yaml
from dotenv import dotenv_values
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo

# URL regex pattern
URL_PATTERNS = re.compile(
    r"^(https?|ftp)://"  # Scheme (HTTP, HTTPS, FTP)
    r"(?:(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,}|"  # Domain name
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # OR IPv4 address
    r"\[?[a-fA-F0-9:]+\]?)"  # OR IPv6 address
    r"(:\d+)?"  # Optional port
    r"(\/[a-zA-Z0-9@:%._\+~#=\/-]*)?"  # Optional path
    r"(\?[a-zA-Z0-9@:%._\+~#&=\/-]*)?"  # Optional query
    r"(#[-a-zA-Z0-9@:%._\+~#=]*)?$"  # Optional fragment
)


def is_url(string: str) -> bool:
    """Check if the input string is a valid URL.

    Args:
        string (str): The input string to check.

    Returns:
        bool: True if the input string is a valid URL, False otherwise.
    """
    return re.match(URL_PATTERNS, string) is not None


def capitalize(string: str) -> str:
    """
    Capitalize the first letter of a given string.

    Parameters:
        string (str): The input string to capitalize.

    Returns:
        str: The string with the first letter capitalized.
    """
    return string[0].upper() + string[1:]


def load_env_variables(file_path: Optional[str] = None) -> dict:
    """
    Loads environment variables from a .env file into a dictionary without changing the global environment variables.

    Args:
        file_path (Optional[str]): Optional path to the .env file. If not provided, it looks for a .env file in the current directory.

    Returns:
        vars (dict): A dictionary containing the environment variables from the .env file.
    """
    # Determine the file path
    env_file = file_path if file_path else ".env"

    # Load the .env file into a dictionary
    env_vars = dotenv_values(env_file)

    return env_vars


def ensure_list(variable: Any) -> list:
    """
    Ensure that the input variable is converted into a list if it is not already an iterable.

    Args:
        variable (any): The input variable that needs to be converted into a list if it is not already an iterable.

    Returns:
        variable (list): The input variable converted into a list, or the input variable itself if it was already an iterable.
    """
    if not isinstance(variable, list):
        if isinstance(variable, tuple):
            return list(variable)
        return [variable]
    return variable


def load_file(file_path: str) -> Dict:
    """
    Load data from a file based on its extension.

    Args:
        file_path (str): The path to the file to load.

    Returns:
        data (dict): The data loaded from the file as a dictionary.

    Raises:
        ValueError: If the file content is not a dictionary (for YAML files).
    """
    with open(file_path, "r") as file:
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == ".yaml" or file_extension == ".yml":
            data = yaml.safe_load(file)
            if not isinstance(data, dict):
                raise ValueError(
                    "Invalid file content. File content must be a dictionary."
                )
            return data
        elif file_extension == ".json":
            return json.load(file)
        else:
            raise ValueError(
                "Unsupported file format. Please provide a .yaml, .yml, or .json file."
            )


def load_url(url: str) -> Dict:
    """
    Load content from a URL and parse it based on the content type (YAML or JSON).

    Args:
        url (str): The URL to load content from.

    Returns:
        Union[Dict, List, Any]: Parsed content from the URL. Can be a dictionary, list, or any other valid JSON/YAML data type.

    Raises:
        ValueError: If the URL format is invalid or the content type is not supported.
    """
    # Validate the URL format
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError(
            "Invalid URL format. Please provide a valid URL starting with 'http://' or 'https://'."
        )

    # Add a timeout to the requests.get call
    # Configure proxy if needed
    settings = load_env_variables()
    proxies = None
    if settings.get("PROXY_URL_HTTPS") or settings.get("PROXY_URL_HTTP"):
        # Only include keys with non-None string values
        proxies = {}
        if settings.get("PROXY_URL_HTTPS") is not None:
            proxies["https"] = str(settings.get("PROXY_URL_HTTPS"))
        if settings.get("PROXY_URL_HTTP") is not None:
            proxies["http"] = str(settings.get("PROXY_URL_HTTP"))
        if not proxies:
            proxies = None
    # Download the StructureDefinition JSON
    response = requests.get(
        url, proxies=proxies, verify=settings.get("CERTIFICATE_BUNDLE_PATH"), timeout=10
    )

    response.raise_for_status()
    content_type = response.headers["Content-Type"]

    # Use content_type.lower() to make the content type check case-insensitive
    if "yaml" in content_type.lower():
        try:
            return yaml.safe_load(response.text)
        except yaml.YAMLError as e:
            raise ValueError(f"Error loading YAML: {e}")
    elif "json" in content_type.lower():
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise ValueError(f"Error loading JSON: {e}")
    else:
        raise ValueError(
            "Unsupported content type. Please provide a URL that returns .yaml, .yml, or .json content."
        )


def contains_only_none(d: Any) -> bool:
    """
    Check if the input contains only None values recursively.

    Args:
        d (Any): The input dictionary or list to check for only None values.

    Returns:
        result (bool): True if the input contains only None values, False otherwise.
    """
    if isinstance(d, dict):
        return all(contains_only_none(v) for v in d.values())
    elif isinstance(d, list):
        return all(contains_only_none(item) for item in d)
    else:
        return d is None


def remove_none_dicts(
    d: Union[Dict[str, Any], List[Any], Any],
) -> Union[Dict[str, Any], List[Any], Any]:
    """
    Remove any dictionaries with all values being None from the input dictionary recursively.

    Args:
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


def get_dict_paths(
    nested_dict: Union[Dict[str, Any], List[Dict[str, Any]]], prefix: str = ""
) -> Dict[str, Any]:
    """
    Get all paths in a nested dictionary with their corresponding values.

    Args:
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


def replace_nth(string, sub, wanted, n):
    """
    Replace the nth occurrence of a substring in a string.

    Args:
        string (str): The original string.
        sub (str): The substring to be replaced.
        wanted (str): The new substring to replace with.
        n (int): The occurrence number of the substring to replace.

    Returns:
        string (str): The updated string after replacing the nth occurrence of the substring.
    """
    pattern = re.compile(sub)
    where = [m for m in pattern.finditer(string)][n - 1]
    before = string[: where.start()]
    after = string[where.end() :]
    newString = before + wanted + after
    return newString


def contains_list_type(tp: Any) -> bool:
    """Recursively check if List is anywhere in the variable's typing."""
    # Check if the current type is a List
    if get_origin(tp) in [List, list]:
        return True

    # Recursively check the type arguments
    for arg in get_args(tp):
        if contains_list_type(arg):
            return True

    return False


def _get_deepest_args(tp: Any) -> list:
    """Recursively get the deepest type arguments of nested typing constructs."""
    args = get_args(tp)
    if not args:
        # Base case: no further nested types
        return [tp]
    # Recursively find the deepest types
    deepest_args = []
    for arg in args:
        deepest_args.extend(_get_deepest_args(arg))
    return deepest_args


T_ = TypeVar("T_")


def get_all_models_from_field(
    field: FieldInfo, issubclass_of: type[T_] = BaseModel
) -> Generator[Type[T_], None, None]:
    return (
        arg
        for arg in _get_deepest_args(field.annotation)
        if inspect.isclass(arg) and issubclass(arg, issubclass_of)
    )


def get_fhir_model_from_field(field: FieldInfo) -> type[BaseModel] | None:
    return next(get_all_models_from_field(field), None)


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Merge two dictionaries recursively, merging lists element by element and dictionaries at the same index.

    If a key exists in both dictionaries, the values are merged based on their types. If a key exists only in one dictionary, it is added to the merged dictionary.

    Args:
        dict1 (dict): The first dictionary to merge.
        dict2 (dict): The second dictionary to merge.

    Returns:
        dict: The merged dictionary.

    Example:
        >>> dict1 = {'a': 1, 'b': {'c': 2, 'd': [3, 4]}, 'e': [5, 6]}
        >>> dict2 = {'b': {'c': 3, 'd': [4, 5]}, 'e': [6, 7], 'f': 8}
        >>> merge_dicts(dict1, dict2)
        {'a': 1, 'b': {'c': 3, 'd': [3, 4, 5]}, 'e': [5, 6, 7], 'f': 8}
    """

    def merge_lists(list1, list2):
        # Merge two lists element by element
        merged_list = []
        for idx in range(max(len(list1), len(list2))):
            if idx < len(list1) and idx < len(list2):
                if isinstance(list1[idx], dict) and isinstance(list2[idx], dict):
                    # Merge dictionaries at the same index
                    merged_list.append(merge_dicts(list1[idx], list2[idx]))
                else:
                    # If they are not dictionaries, choose the element from the first list
                    merged_list.append(list1[idx])
            elif idx < len(list1):
                merged_list.append(list1[idx])
            else:
                merged_list.append(list2[idx])
        return merged_list

    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if key in merged_dict:
            if isinstance(merged_dict[key], list) and isinstance(value, list):
                merged_dict[key] = merge_lists(merged_dict[key], value)
            elif isinstance(merged_dict[key], dict) and isinstance(value, dict):
                merged_dict[key] = merge_dicts(merged_dict[key], value)
            else:
                merged_dict[key] = value
        else:
            merged_dict[key] = value
    return merged_dict


def get_FHIR_release_from_version(version: str) -> str:
    # Check format of the version string
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        raise ValueError(f'FHIR version must be in "x.y.z" format, got "{version}"')
    # Parse version string into a three-digit tuple
    version = version.split("-")[0]
    version_tuple = tuple([int(digit) for digit in version.split(".")])
    # Assign FHIR release based on version number (Referece: http://hl7.org/fhir/directory.html)
    if version_tuple >= (0, 4, 0) and version_tuple <= (1, 0, 2):
        return "DSTU2"
    elif version_tuple >= (1, 1, 0) and version_tuple <= (3, 0, 2):
        return "STU3"
    elif version_tuple >= (3, 2, 0) and version_tuple <= (4, 0, 1):
        return "R4"
    elif version_tuple >= (4, 1, 0) and version_tuple <= (4, 3, 0):
        return "R4B"
    elif version_tuple >= (4, 2, 0) and version_tuple <= (5, 0, 0):
        return "R5"
    elif version_tuple >= (6, 0, 0):
        return "R6"
    elif version_tuple >= (3, 2, 0) and version_tuple <= (4, 0, 1):
        return "R4"
    elif version_tuple >= (4, 1, 0) and version_tuple <= (4, 3, 0):
        return "R4B"
    elif version_tuple >= (4, 2, 0) and version_tuple <= (5, 0, 0):
        return "R5"
    elif version_tuple >= (6, 0, 0):
        return "R6"
    else:
        raise ValueError(
            f"FHIR version {version} is not supported. Supported versions are: "
            "DSTU2, STU3, R4, R4B, R5, and R6."
        )


def get_module_name(obj: Any) -> str:
    """
    Returns the name of the module to which the given object belongs.

    Args:
        obj (Any): The object whose module name is to be retrieved.

    Returns:
        str: The name of the module containing the object.

    Raises:
        ValueError: If the object does not belong to any module.
    """
    module = inspect.getmodule(obj)
    if module is None:
        raise ValueError(f"The object {obj} does not belong to a module")
    return module.__name__


def is_list_field(field) -> bool:
    """
    Determines if a given Pydantic field or FieldInfo is a list type,
    including Optional[List[T]] and Union[List[T], ...].
    """
    annotation = getattr(field, "annotation", None)
    if annotation is None:
        annotation = getattr(field, "outer_type_", None)
    if annotation is None:
        annotation = getattr(field, "type_", None)
    if annotation is None:
        return False

    def _is_list_type(ann):
        origin = getattr(ann, "__origin__", None)
        if origin in (list, List):
            return True
        if origin is Union:
            return any(_is_list_type(arg) for arg in getattr(ann, "__args__", ()))
        return False

    return _is_list_type(annotation)


def model_rebuild_all():
    """
    Call model_rebuild() on all Pydantic models defined in the module where this function is called.
    This is useful when models have forward references or need to be re-evaluated
    after all classes have been defined.
    """
    caller_module_name = inspect.currentframe().f_back.f_globals["__name__"]  # type: ignore
    for name, obj in inspect.getmembers(
        sys.modules[caller_module_name], inspect.isclass
    ):
        # Only call model_rebuild for classes defined in the caller's module
        if obj.__module__ == caller_module_name and hasattr(obj, "model_rebuild"):
            obj.model_rebuild()
