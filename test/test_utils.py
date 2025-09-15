import json
import os
from typing import List, Optional, Union

import pytest
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo

from fhircraft.utils import (
    contains_only_none,
    ensure_list,
    get_dict_paths,
    is_list_field,
    load_env_variables,
    load_file,
    load_url,
    merge_dicts,
    remove_none_dicts,
    replace_nth,
)


class TestEnsureList:

    def test_ensure_list_of_ints(self):
        input_data = [1, 2, 3]
        result = ensure_list(input_data)
        assert result == input_data

    def test_ensure_list_of_strings(self):
        input_data = "hello"
        result = ensure_list(input_data)
        assert result == ["hello"]

    def test_ensure_list_of_an_int(self):
        input_data = 42
        result = ensure_list(input_data)
        assert result == [42]

    def test_ensure_list_of_a_none(self):
        input_data = None
        result = ensure_list(input_data)
        assert result == [None]

    def test_ensure_empty_list_is_list(self):
        input_data = []
        result = ensure_list(input_data)
        assert result == input_data

    def test_ensure_list_from_tuple(self):
        input_data = (1, 2, 3)
        result = ensure_list(input_data)
        assert result == [1, 2, 3]

    def test_ensure_list_of_empty_string(self):
        input_data = ""
        result = ensure_list(input_data)
        assert result == [""]


class TestGetDictPaths:

    def test_flat_dictionary(self):
        input_dict = {"a": 1, "b": 2, "c": 3}
        expected_output = {"a": 1, "b": 2, "c": 3}
        assert get_dict_paths(input_dict) == expected_output

    def test_dictionary_with_none_values(self):
        input_dict = {"a": None, "b": 2, "c": None}
        expected_output = {"b": 2}
        assert get_dict_paths(input_dict) == expected_output

    def test_nested_dictionaries(self):
        input_dict = {"a": {"b": 1, "c": {"d": 2}}}
        expected_output = {"a.b": 1, "a.c.d": 2}
        assert get_dict_paths(input_dict) == expected_output

    def test_lists_of_dictionaries(self):
        input_dict = {"a": [{"b": 1}, {"c": 2}]}
        expected_output = {"a[0].b": 1, "a[1].c": 2}
        assert get_dict_paths(input_dict) == expected_output

    def test_combine_prefix_with_keys(self):
        input_dict = {"a": {"b": 1, "c": 2}}
        prefix = "prefix"
        expected_output = {"prefix.a.b": 1, "prefix.a.c": 2}
        assert get_dict_paths(input_dict, prefix) == expected_output


class TestLoadFile:

    # Load valid YAML file and return dictionary
    def test_load_valid_yaml_file(self):
        file_path = "test_valid.yaml"
        with open(file_path, "w") as file:
            file.write("key: value\n")
        result = load_file(file_path)
        assert result == {"key": "value"}
        os.remove(file_path)

    # Load valid JSON file and return dictionary
    def test_load_valid_json_file(self):
        file_path = "test_valid.json"
        with open(file_path, "w") as file:
            json.dump({"key": "value"}, file)
        result = load_file(file_path)
        assert result == {"key": "value"}
        os.remove(file_path)

    # Correctly identify and handle .yaml file extension
    def test_handle_yaml_extension(self):
        file_path = "test_extension.yaml"
        with open(file_path, "w") as file:
            file.write("key: value\n")
        result = load_file(file_path)
        assert result == {"key": "value"}
        os.remove(file_path)

    # Raise ValueError for unsupported file extensions
    def test_unsupported_file_extension(self):
        file_path = "test_invalid.txt"
        with open(file_path, "w") as file:
            file.write("key: value\n")
        with pytest.raises(
            ValueError,
            match="Unsupported file format. Please provide a .yaml, .yml, or .json file.",
        ):
            load_file(file_path)
        os.remove(file_path)

    # Raise ValueError for YAML file content that is not a dictionary
    def test_yaml_content_not_dict(self):
        file_path = "test_invalid_content.yaml"
        with open(file_path, "w") as file:
            file.write("- item1\n- item2\n")
        with pytest.raises(
            ValueError, match="Invalid file content. File content must be a dictionary."
        ):
            load_file(file_path)
        os.remove(file_path)


class TestLoadUrl:

    def test_valid_url_returning_json_content(self, mocker):
        url = "http://example.com/data.json"
        mock_response = mocker.Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None
        mocker.patch("requests.get", return_value=mock_response)

        result = load_url(url)
        assert result == {"key": "value"}

    def test_valid_url_returning_yaml_content(self, mocker):
        url = "http://example.com/data.yaml"
        mock_response = mocker.Mock()
        mock_response.headers = {"Content-Type": "application/x-yaml"}
        mock_response.text = "key: value"
        mock_response.raise_for_status.return_value = None
        mocker.patch("requests.get", return_value=mock_response)

        result = load_url(url)
        assert result == {"key": "value"}

    def test_valid_url_mixed_case_content_type_json(self, mocker):
        url = "http://example.com/data.json"
        mock_response = mocker.Mock()
        mock_response.headers = {"Content-Type": "Application/Json"}
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None
        mocker.patch("requests.get", return_value=mock_response)

        result = load_url(url)
        assert result == {"key": "value"}

    def test_invalid_url_format(self):
        url = "ftp://example.com/data.json"
        with pytest.raises(
            ValueError,
            match="Invalid URL format. Please provide a valid URL starting with 'http://' or 'https://'.",
        ):
            load_url(url)

    def test_url_returning_unsupported_content_type(self, mocker):
        url = "http://example.com/data.txt"
        mock_response = mocker.Mock()
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.raise_for_status.return_value = None
        mocker.patch("requests.get", return_value=mock_response)

        with pytest.raises(
            ValueError,
            match="Unsupported content type. Please provide a URL that returns .yaml, .yml, or .json content.",
        ):
            load_url(url)


class TestContainsOnlyNone:

    # returns True for an empty dictionary
    def test_empty_dict(self):
        assert contains_only_none({}) is True

    # returns True for a dictionary with all None values
    def test_all_none_values(self):
        assert contains_only_none({"a": None, "b": None}) is True

    # returns False for a dictionary with at least one non-None value
    def test_one_non_none_value(self):
        assert contains_only_none({"a": None, "b": 1}) is False

    # handles mixed types within lists and dictionaries
    def test_mixed_types(self):
        assert contains_only_none({"a": [None, {"b": None}], "c": None}) is True
        assert contains_only_none({"a": [None, {"b": 1}], "c": None}) is False

    # handles deeply nested structures
    def test_deeply_nested_structures(self):
        nested_dict = {"a": {"b": {"c": None}}}
        assert contains_only_none(nested_dict) is True
        nested_dict_with_value = {"a": {"b": {"c": 1}}}
        assert contains_only_none(nested_dict_with_value) is False

    # handles large dictionaries and lists efficiently
    def test_large_structures(self):
        large_dict = {str(i): None for i in range(1000)}
        assert contains_only_none(large_dict) is True
        large_dict_with_value = {str(i): None for i in range(999)}
        large_dict_with_value["999"] = 1  # type: ignore
        assert contains_only_none(large_dict_with_value) is False


class TestRemoveNoneDicts:

    # remove dictionaries with all None values from a nested dictionary
    def test_remove_dicts_with_all_none_values_from_nested_dict(self):
        input_data = {
            "a": {"b": None, "c": None},
            "d": {"e": None, "f": {"g": None}},
            "h": {"i": 1, "j": None},
        }
        expected_output = {"h": {"i": 1}}
        assert remove_none_dicts(input_data) == expected_output

    # remove dictionaries with all None values from a nested list
    def test_remove_dicts_with_all_none_values_from_nested_list(self):
        input_data = {
            "a": [{"b": None, "c": None}, {"d": 1, "e": None}],
            "f": [{"g": None}],
        }
        expected_output = {
            "a": [{"d": 1}],
        }
        assert remove_none_dicts(input_data) == expected_output

    # retain dictionaries with at least one non-None value
    def test_retain_dicts_with_at_least_one_non_none_value(self):
        input_data = {"a": {"b": None, "c": 2}, "d": {"e": 3, "f": None}}
        expected_output = {"a": {"c": 2}, "d": {"e": 3}}
        assert remove_none_dicts(input_data) == expected_output

    # handle empty dictionaries and lists
    def test_handle_empty_dicts_and_lists(self):
        input_data = {"a": {}, "b": [], "c": {"d": {}, "e": []}}
        expected_output = {}
        assert remove_none_dicts(input_data) == expected_output

    # handle dictionaries with only one key-value pair being None
    def test_handle_dicts_with_one_key_value_pair_none(self):
        input_data = {"a": {"b": None}, "c": {"d": 4}}
        expected_output = {"c": {"d": 4}}
        assert remove_none_dicts(input_data) == expected_output

    # handle lists with only None values
    def test_handle_lists_with_only_none_values(self):
        input_data = {"a": [None, None], "b": [None, {"c": None}]}
        expected_output = {}
        assert remove_none_dicts(input_data) == expected_output


class TestLoadEnvVariables:

    def test_load_env_variables_default_path(self, mocker):
        mock_dotenv_values = mocker.patch("fhircraft.utils.dotenv_values")
        mock_dotenv_values.return_value = {"TEST_VAR": "value"}
        result = load_env_variables()
        mock_dotenv_values.assert_called_once_with(".env")
        assert result == {"TEST_VAR": "value"}

    def test_load_env_variables_custom_path(self, mocker):
        mock_dotenv_values = mocker.patch("fhircraft.utils.dotenv_values")
        mock_dotenv_values.return_value = {"ANOTHER_VAR": "another_value"}
        result = load_env_variables("custom.env")
        mock_dotenv_values.assert_called_once_with("custom.env")
        assert result == {"ANOTHER_VAR": "another_value"}

    def test_load_env_variables_no_file(self, mocker):
        mock_dotenv_values = mocker.patch("fhircraft.utils.dotenv_values")
        mock_dotenv_values.return_value = {}
        result = load_env_variables("nonexistent.env")
        mock_dotenv_values.assert_called_once_with("nonexistent.env")
        assert result == {}


class TestMergeDicts:

    # Merging two dictionaries with non-overlapping keys
    def test_non_overlapping_keys(self):
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3, "d": 4}
        result = merge_dicts(dict1, dict2)
        expected = {"a": 1, "b": 2, "c": 3, "d": 4}
        assert result == expected

    # Merging two dictionaries with overlapping keys and non-conflicting values
    def test_overlapping_keys_non_conflicting_values(self):
        dict1 = {"a": 1, "b": {"x": 10}}
        dict2 = {"b": {"y": 20}, "c": 3}
        result = merge_dicts(dict1, dict2)
        expected = {"a": 1, "b": {"x": 10, "y": 20}, "c": 3}
        assert result == expected

    # Merging dictionaries where values are lists of equal length
    def test_lists_of_equal_length(self):
        dict1 = {"a": [1, 2], "b": [3, 4]}
        dict2 = {"a": [5, 6], "b": [7, 8]}
        result = merge_dicts(dict1, dict2)
        expected = {"a": [1, 2], "b": [3, 4]}
        assert result == expected

    # Merging dictionaries where one dictionary is empty
    def test_one_empty_dictionary(self):
        dict1 = {}
        dict2 = {"a": 1, "b": 2}
        result = merge_dicts(dict1, dict2)
        expected = {"a": 1, "b": 2}
        assert result == expected

    # Merging dictionaries where both dictionaries are empty
    def test_both_empty_dictionaries(self):
        dict1 = {}
        dict2 = {}
        result = merge_dicts(dict1, dict2)
        expected = {}
        assert result == expected

    # Merging dictionaries with deeply nested structures
    def test_deeply_nested_structures(self):
        dict1 = {"a": {"b": {"c": 1}}}
        dict2 = {"a": {"b": {"d": 2}}}
        result = merge_dicts(dict1, dict2)
        expected = {"a": {"b": {"c": 1, "d": 2}}}
        assert result == expected


class TestReplaceNth:

    # Replace the nth occurrence of a substring in a string correctly
    def test_replace_nth_correctly(self):
        result = replace_nth("hello world hello world", "world", "there", 2)
        assert result == "hello world hello there"

    # Handle cases where the substring appears exactly n times
    def test_substring_appears_exactly_n_times(self):
        result = replace_nth("abc abc abc", "abc", "xyz", 3)
        assert result == "abc abc xyz"

    # Return the modified string with the nth occurrence replaced
    def test_return_modified_string(self):
        result = replace_nth("one two three two one", "two", "four", 1)
        assert result == "one four three two one"


class TestIsListField:

    class ModelWithList(BaseModel):
        items: List[int]

    class ModelWithOptionalList(BaseModel):
        items: Optional[List[str]]

    class ModelWithUnionList(BaseModel):
        items: Union[List[int], int]

    class ModelWithNonList(BaseModel):
        value: int

    def test_is_list_field_with_list_annotation(self):
        field = self.ModelWithList.model_fields["items"]
        assert is_list_field(field) is True

    def test_is_list_field_with_optional_list(self):
        field = self.ModelWithOptionalList.model_fields["items"]
        assert is_list_field(field) is True

    def test_is_list_field_with_union_list(self):
        field = self.ModelWithUnionList.model_fields["items"]
        assert is_list_field(field) is True

    def test_is_list_field_with_non_list(self):
        field = self.ModelWithNonList.model_fields["value"]
        assert is_list_field(field) is False

    def test_is_list_field_with_fieldinfo_direct(self):
        # Simulate a FieldInfo with annotation
        fieldinfo = FieldInfo(default=None, annotation=List[int])
        assert is_list_field(fieldinfo) is True

    def test_is_list_field_with_fieldinfo_non_list(self):
        fieldinfo = FieldInfo(default=None, annotation=int)
        assert is_list_field(fieldinfo) is False

    def test_is_list_field_with_missing_annotation_and_type(self):
        class Dummy:
            pass

        dummy = Dummy()
        assert is_list_field(dummy) is False
