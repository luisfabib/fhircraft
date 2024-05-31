
from fhir_openapi.utils import ensure_list, get_dict_paths, load_file, load_url, contains_only_none, remove_none_dicts
import os 
import json
import pytest

class TestEnsureList:

    # input is already a list
    def test_input_is_already_a_list(self):
        input_data = [1, 2, 3]
        result = ensure_list(input_data)
        assert result == input_data

    # input is a string
    def test_input_is_a_string(self):
        input_data = "hello"
        result = ensure_list(input_data)
        assert result == ["hello"]

    # input is an integer
    def test_input_is_an_integer(self):
        input_data = 42
        result = ensure_list(input_data)
        assert result == [42]

    # input is None
    def test_input_is_none(self):
        input_data = None
        result = ensure_list(input_data)
        assert result == [None]

    # input is an empty list
    def test_input_is_an_empty_list(self):
        input_data = []
        result = ensure_list(input_data)
        assert result == input_data

    # input is an empty string
    def test_input_is_an_empty_string(self):
        input_data = ""
        result = ensure_list(input_data)
        assert result == [""]

class TestGetDictPaths:

    def test_flat_dictionary(self):
        input_dict = {'a': 1, 'b': 2, 'c': 3}
        expected_output = {'a': 1, 'b': 2, 'c': 3}
        assert get_dict_paths(input_dict) == expected_output

    def test_dictionary_with_none_values(self):
        input_dict = {'a': None, 'b': 2, 'c': None}
        expected_output = {'b': 2}
        assert get_dict_paths(input_dict) == expected_output

    def test_nested_dictionaries(self):
        input_dict = {'a': {'b': 1, 'c': {'d': 2}}}
        expected_output = {'a.b': 1, 'a.c.d': 2}
        assert get_dict_paths(input_dict) == expected_output

    def test_lists_of_dictionaries(self):
        input_dict = {'a': [{'b': 1}, {'c': 2}]}
        expected_output = {'a.0.b': 1, 'a.1.c': 2}
        assert get_dict_paths(input_dict) == expected_output

    def test_combine_prefix_with_keys(self):
        input_dict = {'a': {'b': 1, 'c': 2}}
        prefix = 'prefix'
        expected_output = {'prefix.a.b': 1, 'prefix.a.c': 2}
        assert get_dict_paths(input_dict, prefix) == expected_output
        

class TestLoadFile:

    # Load valid YAML file and return dictionary
    def test_load_valid_yaml_file(self):
        file_path = 'test_valid.yaml'
        with open(file_path, 'w') as file:
            file.write("key: value\n")
        result = load_file(file_path)
        assert result == {"key": "value"}
        os.remove(file_path)

    # Load valid JSON file and return dictionary
    def test_load_valid_json_file(self):
        file_path = 'test_valid.json'
        with open(file_path, 'w') as file:
            json.dump({"key": "value"}, file)
        result = load_file(file_path)
        assert result == {"key": "value"}
        os.remove(file_path)

    # Correctly identify and handle .yaml file extension
    def test_handle_yaml_extension(self):
        file_path = 'test_extension.yaml'
        with open(file_path, 'w') as file:
            file.write("key: value\n")
        result = load_file(file_path)
        assert result == {"key": "value"}
        os.remove(file_path)

    # Raise ValueError for unsupported file extensions
    def test_unsupported_file_extension(self):
        file_path = 'test_invalid.txt'
        with open(file_path, 'w') as file:
            file.write("key: value\n")
        with pytest.raises(ValueError, match="Unsupported file format. Please provide a .yaml, .yml, or .json file."):
            load_file(file_path)
        os.remove(file_path)

    # Raise ValueError for YAML file content that is not a dictionary
    def test_yaml_content_not_dict(self):
        file_path = 'test_invalid_content.yaml'
        with open(file_path, 'w') as file:
            file.write("- item1\n- item2\n")
        with pytest.raises(ValueError, match="Invalid file content. File content must be a dictionary."):
            load_file(file_path)
        os.remove(file_path)


class TestLoadUrl:

    # Valid URL returning JSON content
    def test_valid_url_returning_json_content(self, mocker):
        url = "http://example.com/data.json"
        mock_response = mocker.Mock()
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None
        mocker.patch('requests.get', return_value=mock_response)
    
        result = load_url(url)
        assert result == {"key": "value"}

    # Valid URL returning YAML content
    def test_valid_url_returning_yaml_content(self, mocker):
        url = "http://example.com/data.yaml"
        mock_response = mocker.Mock()
        mock_response.headers = {'Content-Type': 'application/x-yaml'}
        mock_response.text = "key: value"
        mock_response.raise_for_status.return_value = None
        mocker.patch('requests.get', return_value=mock_response)
    
        result = load_url(url)
        assert result == {"key": "value"}

    # Valid URL with mixed case content type headers for JSON
    def test_valid_url_mixed_case_content_type_json(self, mocker):
        url = "http://example.com/data.json"
        mock_response = mocker.Mock()
        mock_response.headers = {'Content-Type': 'Application/Json'}
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None
        mocker.patch('requests.get', return_value=mock_response)
    
        result = load_url(url)
        assert result == {"key": "value"}

    # Invalid URL format not starting with 'http://' or 'https://'
    def test_invalid_url_format(self):
        url = "ftp://example.com/data.json"
        with pytest.raises(ValueError, match="Invalid URL format. Please provide a valid URL starting with 'http://' or 'https://'."):
            load_url(url)

    # URL returning unsupported content type
    def test_url_returning_unsupported_content_type(self, mocker):
        url = "http://example.com/data.txt"
        mock_response = mocker.Mock()
        mock_response.headers = {'Content-Type': 'text/plain'}
        mock_response.raise_for_status.return_value = None
        mocker.patch('requests.get', return_value=mock_response)
    
        with pytest.raises(ValueError, match="Unsupported content type. Please provide a URL that returns .yaml, .yml, or .json content."):
            load_url(url)

    # URL returning malformed JSON
    def test_url_returning_malformed_json(self, mocker):
        url = "http://example.com/data.json"
        mock_response = mocker.Mock()
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        mock_response.raise_for_status.return_value = None
        mocker.patch('requests.get', return_value=mock_response)
    
        result = load_url(url)
        assert result is None


class TestContainsOnlyNone:

    # returns True for an empty dictionary
    def test_empty_dict(self):
        assert contains_only_none({}) is True

    # returns True for a dictionary with all None values
    def test_all_none_values(self):
        assert contains_only_none({'a': None, 'b': None}) is True

    # returns False for a dictionary with at least one non-None value
    def test_one_non_none_value(self):
        assert contains_only_none({'a': None, 'b': 1}) is False

    # handles mixed types within lists and dictionaries
    def test_mixed_types(self):
        assert contains_only_none({'a': [None, {'b': None}], 'c': None}) is True
        assert contains_only_none({'a': [None, {'b': 1}], 'c': None}) is False

    # handles deeply nested structures
    def test_deeply_nested_structures(self):
        nested_dict = {'a': {'b': {'c': None}}}
        assert contains_only_none(nested_dict) is True
        nested_dict_with_value = {'a': {'b': {'c': 1}}}
        assert contains_only_none(nested_dict_with_value) is False

    # handles large dictionaries and lists efficiently
    def test_large_structures(self):
        large_dict = {str(i): None for i in range(1000)}
        assert contains_only_none(large_dict) is True
        large_dict_with_value = {str(i): None for i in range(999)}
        large_dict_with_value['999'] = 1
        assert contains_only_none(large_dict_with_value) is False
        
class TestRemoveNoneDicts:

    # remove dictionaries with all None values from a nested dictionary
    def test_remove_dicts_with_all_none_values_from_nested_dict(self):
        input_data = {
            "a": {"b": None, "c": None},
            "d": {"e": None, "f": {"g": None}},
            "h": {"i": 1, "j": None}
        }
        expected_output = {
            "h": {"i": 1}
        }
        assert remove_none_dicts(input_data) == expected_output

    # remove dictionaries with all None values from a nested list
    def test_remove_dicts_with_all_none_values_from_nested_list(self):
        input_data = {
            "a": [{"b": None, "c": None}, {"d": 1, "e": None}],
            "f": [{"g": None}]
        }
        expected_output = {
            "a": [{"d": 1}],
        }
        assert remove_none_dicts(input_data) == expected_output

    # retain dictionaries with at least one non-None value
    def test_retain_dicts_with_at_least_one_non_none_value(self):
        input_data = {
            "a": {"b": None, "c": 2},
            "d": {"e": 3, "f": None}
        }
        expected_output = {
            "a": {"c": 2},
            "d": {"e": 3}
        }
        assert remove_none_dicts(input_data) == expected_output

    # handle empty dictionaries and lists
    def test_handle_empty_dicts_and_lists(self):
        input_data = {
            "a": {},
            "b": [],
            "c": {"d": {}, "e": []}
        }
        expected_output = {}
        assert remove_none_dicts(input_data) == expected_output

    # handle dictionaries with only one key-value pair being None
    def test_handle_dicts_with_one_key_value_pair_none(self):
        input_data = {
            "a": {"b": None},
            "c": {"d": 4}
        }
        expected_output = {
            "c": {"d": 4}
        }
        assert remove_none_dicts(input_data) == expected_output

    # handle lists with only None values
    def test_handle_lists_with_only_none_values(self):
        input_data = {
            "a": [None, None],
            "b": [None, {"c": None}]
        }
        expected_output = {}
        assert remove_none_dicts(input_data) == expected_output