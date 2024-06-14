import pytest

from fhircraft.fhir.lexer import FhirPathLexer
from fhircraft.fhir.parser import FhirPathParser

# Format: (path_string, data_object, expected_value)
fhirpath_find_test_cases = (
    ('foo.bar', {'foo':{'bar': 5}}, 5),
    ('foo.bar[1]', {'foo':{'bar': [1,2,3]}}, 2),
    ('foo.bar.first()', {'foo':{'bar': [1,2,3]}}, 1),
    ('foo.bar.last()', {'foo':{'bar': [1,2,3]}}, 3),
    ('foo.bar[1].fin', {'foo':{'bar': [1,{'fin': 5}]}}, 5),
    ('foo.bar.tail()', {'foo':{'bar': [1,2,3]}}, [1,2]),
    ('foo.bar.single()', {'foo':{'bar': [1]}}, 1),
    ('foo.where(bar="7").fin', {'foo': [{'bar': 1, 'fin': 4}, {'bar': 7, 'fin': 9} ]}, 9),
    ('foo.where(bar.bizzle="7").fin', {'foo': [{'bar': {'bizzle': 1}, 'fin': 4}, {'bar': {'bizzle': 7}, 'fin': 9} ]}, 9),
    ('foo.extension("http://domain.org/extension2").fin', {'foo': [{'url': "http://domain.org/extension", 'fin': 4}, {'url': "http://domain.org/extension2", 'fin': 9} ]}, 9),
)

@pytest.mark.parametrize("path_string, data_object, expected_value", fhirpath_find_test_cases)
def test_fhirpath_find(path_string, data_object, expected_value):
    parser = FhirPathParser(lexer_class=lambda: FhirPathLexer())
    matches = parser.parse(path_string).find(data_object)
    expected_values = expected_value if isinstance(expected_value, list) else [expected_value]
    assert len(matches) > 0, 'No match found'
    assert len(matches) == len(expected_values)
    for match, expected in zip(matches, expected_values):
        assert match.value == expected

# Format: (path_string, data_object, expected_value)
fhirpath_update_test_cases = (
    ('foo.bar', {'foo':{'bar': 5}}, 8),
    ('foo.bar[1]', {'foo':{'bar': [1,2]}}, 8),
    ('foo.bar.first()', {'foo':{'bar': [1,2]}}, 8),
    ('foo.bar.last()', {'foo':{'bar': [1,2]}}, 8),
    ('foo.bar[1].fin', {'foo':{'bar': [1,{'fin': 5}]}}, 12),
    ('foo.bar.single()', {'foo':{'bar': [1]}}, 2),
    ('foo.where(bar="7").fin', {'foo': [{'bar': 1, 'fin': 4}, {'bar': 7, 'fin': 9} ]}, 2),
    ('foo.where(bar.bizzle="7").fin', {'foo': [{'bar': {'bizzle': 1}, 'fin': 4}, {'bar': {'bizzle': 7}, 'fin': 9} ]}, 6),
)

@pytest.mark.parametrize("path_string, data_object, new_value", fhirpath_update_test_cases)
def test_fhirpath_update(path_string, data_object, new_value):
    parser = FhirPathParser(lexer_class=lambda: FhirPathLexer())
    parser.parse(path_string).update(data_object, new_value)
    matches = parser.parse(path_string).find(data_object)
    assert len(matches) > 0, 'No match found'
    assert matches[0].value == new_value