import pytest

from fhircraft.fhir.lexer import FhirPathLexer, FhirPathLexerError

token_test_cases = (
    ("$", (("$", "$"),)),
    ('"hello"', (("hello", "ID"),)),
    ("'goodbye'", (("goodbye", "ID"),)),
    ("'doublequote\"'", (('doublequote"', "ID"),)),
    (r'"doublequote\""', (('doublequote"', "ID"),)),
    (r"'singlequote\''", (("singlequote'", "ID"),)),
    ('"singlequote\'"', (("singlequote'", "ID"),)),
    ("fuzz", (("fuzz", "ID"),)),
    ("1", ((1, "NUMBER"),)),
    ("45", ((45, "NUMBER"),)),
    ("-1", ((-1, "NUMBER"),)),
    (" -13 ", ((-13, "NUMBER"),)),
    (" 1.24 ", ((1.24, "NUMBER"),)),
    (" -2.52 ", ((-2.52, "NUMBER"),)),
    ('"fuzz.bang"', (("fuzz.bang", "ID"),)),
    ("fuzz.bang", (("fuzz", "ID"), (".", "."), ("bang", "ID"))),
    ("fuzz.*", (("fuzz", "ID"), (".", "."), ("*", "*"))),
    ("&", (("&", "&"),)),
    ("@", (("@", "ID"),)),
    ("`this`", (("this", "NAMED_OPERATOR"),)),
    ("|", (("|", "|"),)),
    ("where", (("where", "WHERE"),)),
    ("first", (("first", "FIRST"),)),
    ("last", (("last", "LAST"),)),
    ("tail", (("tail", "TAIL"),)),
    ("single", (("single", "SINGLE"),)),
    ("extension", (("extension", "EXTENSION"),)),
    ("Observation", (("Observation", "RESOURCE_BASE"),)),
    ("CodeableConcept", (("CodeableConcept", "RESOURCE_BASE"),)),
)


@pytest.mark.parametrize("string, expected_token_info", token_test_cases)
def test_lexer(string, expected_token_info):
    lexer = FhirPathLexer(debug=True)
    tokens = list(lexer.tokenize(string))
    assert len(tokens) == len(expected_token_info)
    for token, (expected_value, expected_type) in zip(tokens, expected_token_info):
        assert token.type == expected_type
        assert token.value == expected_value


invalid_token_test_cases = (
    "'\"",
    "\"'",
    '`"',
    "`'",
    '"`',
    "'`",
    "?",    
    "?",
    "$.foo.bar.#",
)


@pytest.mark.parametrize("string", invalid_token_test_cases)
def test_lexer_errors(string):
    with pytest.raises(FhirPathLexerError):
        list(FhirPathLexer().tokenize(string))