import pytest

from fhircraft.fhir.path.engine.core import (
    Element,
    FHIRPathCollectionItem,
    FHIRPathError,
    Invocation,
    Root,
    This,
)
from fhircraft.fhir.path.engine.strings import *

# -------------
# StringManipulationFunction
# -------------


def test_string_manipulation_function_checks_singleton_collection():
    collection = [
        FHIRPathCollectionItem(value="mySubstringValue"),
        FHIRPathCollectionItem(value="mySubstringValue2"),
    ]
    with pytest.raises(FHIRPathError):
        IndexOf("Substring").evaluate(collection)


def test_string_manipulation_function_checks_type():
    collection = [FHIRPathCollectionItem(value=2)]
    with pytest.raises(FHIRPathError):
        IndexOf("Substring").evaluate(collection)


# -------------
# IndexOf
# -------------


def test_indexOf_returns_empty_if_empty():
    collection = []
    result = IndexOf("").evaluate(collection)
    assert result == []


def test_indexOf_returns_correct_index_of_substring():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = IndexOf("Substring").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=2)]


def test_indexOf_returns_zero_if_empty_substring():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = IndexOf("").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=0)]


# -------------
# Substring
# -------------


def test_substring_returns_correct_index_of_substring_with_initial_index():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Substring(2).evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="SubstringValue")]


def test_substring_returns_correct_index_of_substring_with_initial_and_final_index():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Substring(2, 11).evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="Substring")]


# -------------
# StartsWith
# -------------


def test_startswith_returns_empty_if_empty():
    collection = []
    result = StartsWith("").evaluate(collection)
    assert result == []


def test_startswith_returns_true_if_starts_with_prefix():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = StartsWith("mySub").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=True)]


def test_startswith_returns_false_if_not_starts_with_prefix():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = StartsWith("yourSub").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=False)]


# -------------
# EndsWith
# -------------


def test_endswith_returns_empty_if_empty():
    collection = []
    result = EndsWith("").evaluate(collection)
    assert result == []


def test_endswith_returns_true_if_ends_with_suffix():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = EndsWith("Value").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=True)]


def test_endswith_returns_false_if_not_ends_with_suffix():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = EndsWith("Values").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=False)]


# -------------
# Contains
# -------------


def test_contains_returns_empty_if_empty():
    collection = []
    result = Contains("").evaluate(collection)
    assert result == []


def test_contains_returns_true_if_substring_contained():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Contains("Substring").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=True)]


def test_contains_returns_false_if_not_substring_contained():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Contains("Substrings").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=False)]


# -------------
# Upper
# -------------


def test_upper_returns_empty_if_empty():
    collection = []
    result = Upper().evaluate(collection)
    assert result == []


def test_upper_returns_uppercase_string():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Upper().evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="MYSUBSTRINGVALUE")]


# -------------
# Lower
# -------------


def test_lower_returns_empty_if_empty():
    collection = []
    result = Lower().evaluate(collection)
    assert result == []


def test_lower_returns_lowercase_string():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Lower().evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="mysubstringvalue")]


# -------------
# Replace
# -------------


def test_replace_returns_empty_if_empty():
    collection = []
    result = Replace("", "").evaluate(collection)
    assert result == []


def test_replace_pattern():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Replace("my", "your").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="yourSubstringValue")]


def test_replace_all_patterns():
    collection = [FHIRPathCollectionItem(value="mySubstringmyValue")]
    result = Replace("my", "your").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="yourSubstringyourValue")]


def test_replace_sorround_all_characters():
    collection = [FHIRPathCollectionItem(value="ab")]
    result = Replace("", "X").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="XaXbX")]


# ----------------
# Matches
# ----------------


def test_matches_returns_empty_if_empty():
    collection = []
    result = Matches("").evaluate(collection)
    assert result == []


def test_matches_returns_true_if_match():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Matches(r"^(?:my).*").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=True)]


def test_matches_returns_false_if_not_match():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Matches(r"^(?:your).*").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=False)]


# ----------------
# ReplaceMatches
# ----------------


def test_replacematches_returns_empty_if_empty():
    collection = []
    result = ReplaceMatches("", "").evaluate(collection)
    assert result == []


def test_replacematches_pattern():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = ReplaceMatches(r"^(?:my)", "your").evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="yourSubstringValue")]


# ----------------
# Length
# ----------------


def test_length_returns_empty_if_empty():
    collection = []
    result = Length().evaluate(collection)
    assert result == []


def test_length_returns_correct_length():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Length().evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=16)]


# ----------------
# ToChars
# ----------------


def test_tochars_returns_empty_if_empty():
    collection = []
    result = ToChars().evaluate(collection)
    assert result == []


def test_tochars_returns_collection_of_characters():
    collection = [FHIRPathCollectionItem(value="ABC")]
    result = ToChars().evaluate(collection)
    assert [item.value for item in result] == ["A", "B", "C"]


# ----------------
# Concatenation
# ----------------


def test_concatenation_returns_empty_string_if_empty():
    collection = []
    result = Concatenation([], []).evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="")]


def test_concatenation_returns_concatenated_string():
    collection = []
    result = Concatenation(
        [FHIRPathCollectionItem(value="A")], [FHIRPathCollectionItem(value="B")]
    ).evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="AB")]


def test_concatenation_treats_empty_as_empty_string():
    collection = []
    result = Concatenation([FHIRPathCollectionItem(value="A")], []).evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="A")]
