import pytest

from fhircraft.fhir.mapping.lexer import (
    FhirMappingLanguageLexer,
    FhirMappingLanguageLexerError,
)

token_test_cases = (  # ----------------- Symbols -----------------
    (".", ((".", "."),)),
    (",", ((",", ","),)),
    ("+", (("+", "+"),)),
    ("-", (("-", "-"),)),
    ("*", (("*", "*"),)),
    ("/", (("/", "/"),)),
    ("|", (("|", "|"),)),
    ("&", (("&", "&"),)),
    ("(", (("(", "("),)),
    (")", ((")", ")"),)),
    ("}", (("}", "}"),)),
    ("{", (("{", "{"),)),
    ("{}", (("{", "{"), ("}", "}"))),
    # ----------------- Literals -----------------
    ("true", (("true", "BOOLEAN"),)),
    ("false", (("false", "BOOLEAN"),)),
    ("1", ((1, "INTEGER"),)),
    ("45", ((45, "INTEGER"),)),
    ("-1", ((-1, "INTEGER"),)),
    (" -13 ", ((-13, "INTEGER"),)),
    (" 1.24 ", ((1.24, "DECIMAL"),)),
    (" -2.52 ", ((-2.52, "DECIMAL"),)),
    ("@2024-01-02", (("@2024-01-02", "DATE"),)),
    ("@2024-01", (("@2024-01", "DATE"),)),
    ("@2024", (("@2024", "DATE"),)),
    ("@T14:30", (("@T14:30", "TIME"),)),
    ("@T14:30:14.559", (("@T14:30:14.559", "TIME"),)),
    ("@T14:30:14.559+02:30", (("@T14:30:14.559+02:30", "TIME"),)),
    (
        "@2014-01-02T14:30:13.346+02:30",
        (("@2014-01-02T14:30:13.346+02:30", "DATETIME"),),
    ),
    ("@2014-01-02T14:30", (("@2014-01-02T14:30", "DATETIME"),)),
    ("@2014T14", (("@2014T14", "DATETIME"),)),
    ("@2014T", (("@2014T", "DATETIME"),)),
    ("'string'", (("string", "STRING"),)),
    ("'test string'", (("test string", "STRING"),)),
    ("'string1' 'string2'", (("string1", "STRING"), ("string2", "STRING"))),
    # ----------------- Identifiers -----------------
    ("parent", (("parent", "IDENTIFIER"),)),
    ("_parent", (("_parent", "IDENTIFIER"),)),
    ("parent12", (("parent12", "IDENTIFIER"),)),
    ("_parent12", (("_parent12", "IDENTIFIER"),)),
    ("_12345", (("_12345", "IDENTIFIER"),)),
    ("`parent`", (("parent", "DELIMITEDIDENTIFIER"),)),
    ("`div`", (("div", "DELIMITEDIDENTIFIER"),)),
    ("`parent name`", (("parent name", "DELIMITEDIDENTIFIER"),)),
    ("parent.child", (("parent", "IDENTIFIER"), (".", "."), ("child", "IDENTIFIER"))),
    ("parent.*", (("parent", "IDENTIFIER"), (".", "."), ("*", "*"))),
    ("<<types>>", (("types", "GROUPTYPE"),)),
    ("<<type+>>", (("type-and-types", "GROUPTYPE"),)),
    (
        "/// name = 'title'",
        (
            ("///", "METADATA_DECLARATION"),
            ("name", "IDENTIFIER"),
            ("=", "EQUAL"),
            ("title", "STRING"),
        ),
    ),
    # ----------------- COMPLEX  -----------------
    (
        "uses 'http://example.org' as source",
        (
            ("uses", "USES"),
            ("http://example.org", "STRING"),
            ("as", "AS"),
            ("source", "SOURCE"),
        ),
    ),
    (
        "let my_const = 12;",
        (
            ("let", "LET"),
            ("my_const", "IDENTIFIER"),
            ("=", "EQUAL"),
            (12, "INTEGER"),
            (";", ";"),
        ),
    ),
    (
        "group example(source src, target tgt){}",
        (
            ("group", "GROUP"),
            ("example", "IDENTIFIER"),
            ("(", "("),
            ("source", "SOURCE"),
            ("src", "IDENTIFIER"),
            (",", ","),
            ("target", "TARGET"),
            ("tgt", "IDENTIFIER"),
            (")", ")"),
            ("{", "{"),
            ("}", "}"),
        ),
    ),
)


@pytest.mark.parametrize("string, expected_token_info", token_test_cases)
def test_lexer(string, expected_token_info):
    lexer = FhirMappingLanguageLexer(debug=True)
    tokens = list(lexer.tokenize(string))
    assert len(tokens) == len(expected_token_info)
    for token, (expected_value, expected_type) in zip(tokens, expected_token_info):
        assert token.type == expected_type
        assert token.value == expected_value
    for token, (expected_value, expected_type) in zip(tokens, expected_token_info):
        assert token.type == expected_type
        assert token.value == expected_value
