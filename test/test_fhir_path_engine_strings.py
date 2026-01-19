import pytest
from unittest.mock import patch
from fhircraft.fhir.path.engine.core import (
    FHIRPathCollectionItem,
    FHIRPathError,
    Literal,
)
from fhircraft.fhir.path.engine.environment import EnvironmentVariable
from fhircraft.fhir.path.engine.strings import *

env = dict()

# -------------
# StringManipulationFunction
# -------------


def test_string_manipulation_function_checks_singleton_collection():
    collection = [
        FHIRPathCollectionItem(value="mySubstringValue"),
        FHIRPathCollectionItem(value="mySubstringValue2"),
    ]
    with pytest.raises(FHIRPathError):
        IndexOf("Substring").evaluate(collection, env)


def test_string_manipulation_function_checks_type():
    collection = [FHIRPathCollectionItem(value=2)]
    with pytest.raises(FHIRPathError):
        IndexOf("Substring").evaluate(collection, env)


# -------------
# IndexOf
# -------------


def test_indexof_returns_empty_if_empty():
    collection = []
    result = IndexOf("").evaluate(collection, env)
    assert result == []


def test_indexof_returns_correct_index_of_substring():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = IndexOf("Substring").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=2)]


def test_indexof_returns_correct_index_of_substring_with_fhirpath():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = IndexOf(EnvironmentVariable("%substring")).evaluate(
        collection, {"%substring": "Substring"}
    )
    assert result == [FHIRPathCollectionItem(value=2)]


def test_indexof_returns_zero_if_empty_substring():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = IndexOf("").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=0)]

def test_indexof_uses_evaluation_context():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    with patch('fhircraft.fhir.path.engine.strings.Literal.evaluate', wraps=Literal("").evaluate) as mock_evaluate:
        IndexOf(Literal("")).evaluate(collection, env)
        mock_evaluate.assert_called()
        assert mock_evaluate.call_args[0][1]["$this"] == collection[0].value

def test_indexof_string_representation():
    expression = IndexOf("Substring")
    assert str(expression) == "indexOf('Substring')"


# -------------
# Substring
# -------------


def test_substring_returns_correct_index_of_substring_with_initial_index():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Substring(2).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="SubstringValue")]


def test_substring_returns_correct_index_of_substring_with_initial_and_final_index():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Substring(2, 11).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="Substring")]


def test_substring_returns_correct_index_of_substring_with_initial_and_final_index_with_fhirpath():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Substring(
        EnvironmentVariable("%start"), EnvironmentVariable("%end")
    ).evaluate(collection, {"%start": 2, "%end": 11})
    assert result == [FHIRPathCollectionItem(value="Substring")]


def test_substring_returns_correct_index_of_substring_returns_full_with_zero():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Substring(0).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="mySubstringValue")]


def test_substring_returns_correct_index_of_substring_returns_only_beginning():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Substring(0, 5).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="mySub")]


def test_substring_returns_empty_if_start_out_of_bounds():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Substring(100).evaluate(collection, env)
    assert result == []

def test_substring_uses_evaluation_context():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    with patch('fhircraft.fhir.path.engine.strings.Literal.evaluate', wraps=Literal(0).evaluate) as mock_evaluate:
        Substring(0, 5).evaluate(collection, env)
        mock_evaluate.assert_called()
        assert mock_evaluate.call_args[0][1]["$this"] == collection[0].value

def test_substring_string_representation():
    expression = Substring(2, 11)
    assert str(expression) == "substring(2, 11)"


# -------------
# StartsWith
# -------------


def test_startswith_returns_empty_if_empty():
    collection = []
    result = StartsWith("").evaluate(collection, env)
    assert result == []


def test_startswith_returns_true_if_starts_with_prefix():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = StartsWith("mySub").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=True)]


def test_startswith_returns_false_if_not_starts_with_prefix():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = StartsWith("yourSub").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=False)]


def test_startswith_returns_true_if_starts_with_prefix_with_fhirpath():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = StartsWith(EnvironmentVariable("%prefix")).evaluate(
        collection, {"%prefix": "mySub"}
    )
    assert result == [FHIRPathCollectionItem(value=True)]

def test_startswith_uses_evaluation_context():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    with patch('fhircraft.fhir.path.engine.strings.Literal.evaluate', wraps=Literal('mySub').evaluate) as mock_evaluate:
        StartsWith("mySub").evaluate(collection, env)
        mock_evaluate.assert_called()
        assert mock_evaluate.call_args[0][1]["$this"] == collection[0].value

def test_startswith_string_representation():
    expression = StartsWith("mySub")
    assert str(expression) == "startsWith('mySub')"


# -------------
# EndsWith
# -------------


def test_endswith_returns_empty_if_empty():
    collection = []
    result = EndsWith("").evaluate(collection, env)
    assert result == []


def test_endswith_returns_true_if_ends_with_suffix():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = EndsWith("Value").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=True)]


def test_endswith_returns_false_if_not_ends_with_suffix():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = EndsWith("Values").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=False)]


def test_endswith_returns_true_if_ends_with_suffix_with_fhirpath():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = EndsWith(EnvironmentVariable("%suffix")).evaluate(
        collection, {"%suffix": "Value"}
    )
    assert result == [FHIRPathCollectionItem(value=True)]


def test_endswith_uses_evaluation_context():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    with patch('fhircraft.fhir.path.engine.strings.Literal.evaluate', wraps=Literal('mySub').evaluate) as mock_evaluate:
        EndsWith("mySub").evaluate(collection, env)
        mock_evaluate.assert_called()
        assert mock_evaluate.call_args[0][1]["$this"] == collection[0].value


def test_endswith_string_representation():
    expression = EndsWith("Value")
    assert str(expression) == "endsWith('Value')"


# -------------
# Contains
# -------------


def test_contains_returns_empty_if_empty():
    collection = []
    result = Contains("").evaluate(collection, env)
    assert result == []


def test_contains_returns_true_if_substring_contained():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Contains("Substring").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=True)]


def test_contains_returns_false_if_not_substring_contained():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Contains("Substrings").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=False)]


def test_contains_returns_true_if_substring_contained_with_fhirpath():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Contains(EnvironmentVariable("%substring")).evaluate(
        collection, {"%substring": "Substring"}
    )
    assert result == [FHIRPathCollectionItem(value=True)]


def test_contains_uses_evaluation_context():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    with patch('fhircraft.fhir.path.engine.strings.Literal.evaluate', wraps=Literal('mySub').evaluate) as mock_evaluate:
        Contains("mySub").evaluate(collection, env)
        mock_evaluate.assert_called()
        assert mock_evaluate.call_args[0][1]["$this"] == collection[0].value


def test_contains_string_representation():
    expression = Contains("Substring")
    assert str(expression) == "contains('Substring')"


# -------------
# Upper
# -------------


def test_upper_returns_empty_if_empty():
    collection = []
    result = Upper().evaluate(collection, env)
    assert result == []


def test_upper_returns_uppercase_string():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Upper().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="MYSUBSTRINGVALUE")]


def test_upper_string_representation():
    expression = Upper()
    assert str(expression) == "upper()"


# -------------
# Lower
# -------------


def test_lower_returns_empty_if_empty():
    collection = []
    result = Lower().evaluate(collection, env)
    assert result == []


def test_lower_returns_lowercase_string():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Lower().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="mysubstringvalue")]


def test_lower_string_representation():
    expression = Lower()
    assert str(expression) == "lower()"


# -------------
# Replace
# -------------


def test_replace_returns_empty_if_empty():
    collection = []
    result = Replace("", "").evaluate(collection, env)
    assert result == []


def test_replace_pattern():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Replace("my", "your").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="yourSubstringValue")]


def test_replace_empty_substitution():
    collection = [FHIRPathCollectionItem(value="Patient/123")]
    result = Replace("Patient/", "").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="123")]


def test_replace_all_patterns():
    collection = [FHIRPathCollectionItem(value="mySubstringmyValue")]
    result = Replace("my", "your").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="yourSubstringyourValue")]


def test_replace_sorround_all_characters():
    collection = [FHIRPathCollectionItem(value="ab")]
    result = Replace("", "X").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="XaXbX")]


def test_replace_pattern_with_fhirpath():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Replace(
        EnvironmentVariable("%pattern"), EnvironmentVariable("%replacement")
    ).evaluate(collection, {"%pattern": "my", "%replacement": "your"})
    assert result == [FHIRPathCollectionItem(value="yourSubstringValue")]


def test_replace_uses_evaluation_context():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    with patch('fhircraft.fhir.path.engine.strings.Literal.evaluate', wraps=Literal('mySub').evaluate) as mock_evaluate:
        Replace("mySub", "yourSub").evaluate(collection, env)
        mock_evaluate.assert_called()
        assert mock_evaluate.call_args[0][1]["$this"] == collection[0].value


def test_replace_string_representation():
    expression = Replace("my", "your")
    assert str(expression) == "replace('my', 'your')"


# ----------------
# Matches
# ----------------


def test_matches_returns_empty_if_empty():
    collection = []
    result = Matches("").evaluate(collection, env)
    assert result == []


def test_matches_returns_true_if_match():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Matches(r"^(?:my).*").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=True)]


def test_matches_returns_false_if_not_match():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Matches(r"^(?:your).*").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=False)]


def test_matches_returns_true_if_match_with_fhirpath():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Matches(EnvironmentVariable("%regex")).evaluate(
        collection, {"%regex": r"^(?:my).*"}
    )
    assert result == [FHIRPathCollectionItem(value=True)]


def test_matches_uses_evaluation_context():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    with patch('fhircraft.fhir.path.engine.strings.Literal.evaluate', wraps=Literal('mySub').evaluate) as mock_evaluate:
        Matches("mySub").evaluate(collection, env)
        mock_evaluate.assert_called()
        assert mock_evaluate.call_args[0][1]["$this"] == collection[0].value


def test_matches_string_representation():
    expression = Matches(r"^(?:my).*")
    assert str(expression) == "matches('^(?:my).*')"


# ----------------
# ReplaceMatches
# ----------------


def test_replacematches_returns_empty_if_empty():
    collection = []
    result = ReplaceMatches("", "").evaluate(collection, env)
    assert result == []


def test_replacematches_pattern():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = ReplaceMatches(r"^(?:my)", "your").evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="yourSubstringValue")]


def test_replacematches_pattern_with_fhirpath():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = ReplaceMatches(
        EnvironmentVariable("%pattern"), EnvironmentVariable("%replacement")
    ).evaluate(collection, {"%pattern": r"^(?:my)", "%replacement": "your"})
    assert result == [FHIRPathCollectionItem(value="yourSubstringValue")]


def test_replacematches_uses_evaluation_context():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    with patch('fhircraft.fhir.path.engine.strings.Literal.evaluate', wraps=Literal('mySub').evaluate) as mock_evaluate:
        ReplaceMatches("mySub", "yourSub").evaluate(collection, env)
        mock_evaluate.assert_called()
        assert mock_evaluate.call_args[0][1]["$this"] == collection[0].value



def test_replacematches_string_representation():
    expression = ReplaceMatches(r"^(?:my)", "your")
    assert str(expression) == "replaceMatches('^(?:my)', 'your')"


# ----------------
# Length
# ----------------


def test_length_returns_empty_if_empty():
    collection = []
    result = Length().evaluate(collection, env)
    assert result == []


def test_length_returns_correct_length():
    collection = [FHIRPathCollectionItem(value="mySubstringValue")]
    result = Length().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=16)]


def test_length_string_representation():
    expression = Length()
    assert str(expression) == "length()"


# ----------------
# ToChars
# ----------------


def test_tochars_returns_empty_if_empty():
    collection = []
    result = ToChars().evaluate(collection, env)
    assert result == []


def test_tochars_returns_collection_of_characters():
    collection = [FHIRPathCollectionItem(value="ABC")]
    result = ToChars().evaluate(collection, env)
    assert [item.value for item in result] == ["A", "B", "C"]


def test_tochars_string_representation():
    expression = ToChars()
    assert str(expression) == "toChars()"


# ----------------
# Concatenation
# ----------------


def test_concatenation_returns_empty_string_if_empty():
    collection = []
    result = Concatenation([], []).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="")]


def test_concatenation_returns_concatenated_string():
    collection = []
    result = Concatenation(
        [FHIRPathCollectionItem(value="Abc")], [FHIRPathCollectionItem(value="Bcd")]
    ).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="AbcBcd")]


def test_concatenation_treats_empty_as_empty_string():
    collection = []
    result = Concatenation([FHIRPathCollectionItem(value="Abc")], []).evaluate(
        collection, env
    )
    assert result == [FHIRPathCollectionItem(value="Abc")]


def test_concatenation_string_representation():
    expression = Concatenation(Literal("Abc"), Literal("Bcd"))
    assert str(expression) == "'Abc' & 'Bcd'"
