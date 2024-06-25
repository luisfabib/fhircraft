import pytest

from fhircraft.fhir.path.lexer import FhirPathLexer, FhirPathLexerError

token_test_cases = (
    # ---------- Contextual Operators ------------
    ("$", (("$", "CONTEXTUAL_OPERATOR"),)),
    ("$this", (("$this", "CONTEXTUAL_OPERATOR"),)),
    ("$index", (("$index", "CONTEXTUAL_OPERATOR"),)),
    ("$total", (("$total", "CONTEXTUAL_OPERATOR"),)),
    # -------- Environmental Operators -----------
    ("%resource", (("%resource", "ENVIRONMENTAL_VARIABLE"),)),
    ("%context", (("%context", "ENVIRONMENTAL_VARIABLE"),)),
    # ----------------- Symbols -----------------
    (".", ((".", "."),)),
    (",", ((",", ","),)),
    ("+", (("+", "+"),)),
    ("-", (("-", "-"),)),
    ("*", (("*", "*"),)),
    ("/", (("/", "/"),)),
    ("|", (("|", "|"),)),
    ("&", (("&", "&"),)),
    ("=", (("=", "="),)),
    (">", ((">", ">"),)),
    ("!", (("!", "!"),)),
    ("(", (("(", "("),)),
    (")", ((")", ")"),)),
    ("}", (("}", "}"),)),
    ("{", (("{", "{"),)),
    # ----------------- Literals -----------------
    ("// comment line", ()),
    ("/* multiline \n comment */", ()),
    ("true", (("true", "BOOLEAN"),)),
    ("false", (("false", "BOOLEAN"),)),
    ("1", ((1, "INTEGER"),)),
    ("45", ((45, "INTEGER"),)),
    ("-1", ((-1, "INTEGER"),)),
    (" -13 ", ((-13, "INTEGER"),)),
    (" 1.24 ", ((1.24, "DECIMAL"),)),
    (" -2.52 ", ((-2.52, "DECIMAL"),)),
    ("@2024-01-02", (('2024-01-02', "DATE"),)),
    ("@2024-01", (('2024-01', "DATE"),)),
    ("@2024", (('2024', "DATE"),)),
    ("@T14:30", (('14:30', "TIME"),)),
    ("@T14:30:14.559", (('14:30:14.559', "TIME"),)),
    ("@T14:30:14.559Z", (('14:30:14.559Z', "TIME"),)),
    ("'string'", (("string", "STRING"),)),
    ("'test string'", (("test string", "STRING"),)),
    # ----------------- Identifiers -----------------
    ("parent", (("parent", "IDENTIFIER"),)),
    ("_parent", (("_parent", "IDENTIFIER"),)),
    ("parent12", (("parent12", "IDENTIFIER"),)),
    ("_parent12", (("_parent12", "IDENTIFIER"),)),
    ("_12345", (("_12345", "IDENTIFIER"),)),
    ("`parent`", (("parent", "IDENTIFIER"),)),
    ("`parent name`", (("parent name", "IDENTIFIER"),)),
    ("parent.child", (("parent", "IDENTIFIER"), (".", "."), ("child", "IDENTIFIER"))),
    ("parent.*", (("parent", "IDENTIFIER"), (".", "."), ("*", "*"))),
    # -------------  Functions --------------
    ("where", (("where", "IDENTIFIER"),)),
    ("where(arg1,arg2)", (("where", "IDENTIFIER"),("(", "("),("arg1", "IDENTIFIER"),(",", ","),("arg2", "IDENTIFIER"),(")", ")"))),
    ("first", (("first", "IDENTIFIER"),)),
    ("last", (("last", "IDENTIFIER"),)),
    ("tail", (("tail", "IDENTIFIER"),)),
    ("single", (("single", "IDENTIFIER"),)),
    ("extension", (("extension", "IDENTIFIER"),)),
    # --------------  Keywords ---------------
    ("and", (("and", "BOOLEAN_OPERATOR"),)),
    ("or", (("or", "BOOLEAN_OPERATOR"),)),
    ("xor", (("xor", "BOOLEAN_OPERATOR"),)),
    ("implies", (("implies", "BOOLEAN_OPERATOR"),)),
    ("as", (("as", "TYPES_OPERATOR"),)),
    ("is", (("is", "TYPES_OPERATOR"),)),
    ("year", (("year", "CALENDAR_DURATION"),)),
    ("month", (("month", "CALENDAR_DURATION"),)),
    ("week", (("week", "CALENDAR_DURATION"),)),
    ("day", (("day", "CALENDAR_DURATION"),)),
    # -------------  Root Nodes --------------
    ("Observation", (("Observation", "ROOT_NODE"),)),
    ("CodeableConcept", (("CodeableConcept", "ROOT_NODE"),)),
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
    '"double quote string"',
    "$.foo.bar.#",
)


@pytest.mark.parametrize("string", invalid_token_test_cases)
def test_lexer_errors(string):
    with pytest.raises(FhirPathLexerError):
        list(FhirPathLexer().tokenize(string))