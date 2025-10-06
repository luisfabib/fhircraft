import pytest

from fhircraft.fhir.mapper.lexer import (
    FhirMappingLanguageLexer,
    FhirMappingLanguageLexerError,
)

token_test_cases = (
    # ----------------- Keywords -----------------
    ("map", (("map", "MAP"),)),
    ("imports", (("imports", "IMPORTS"),)),
    ("alias", (("alias", "ALIAS"),)),
    ("extends", (("extends", "EXTENDS"),)),
    ("default", (("default", "DEFAULT"),)),
    ("where", (("where", "WHERE"),)),
    ("check", (("check", "CHECK"),)),
    ("log", (("log", "LOG"),)),
    ("then", (("then", "THEN"),)),
    ("first", (("first", "FIRST"),)),
    ("not_first", (("not_first", "NOT_FIRST"),)),
    ("last", (("last", "LAST"),)),
    ("not_last", (("not_last", "NOT_LAST"),)),
    ("only_one", (("only_one", "ONLY_ONE"),)),
    ("share", (("share", "SHARE"),)),
    ("single", (("single", "SINGLE"),)),
    ("queried", (("queried", "QUERIED"),)),
    ("produced", (("produced", "PRODUCED"),)),
    ("conceptmap", (("conceptmap", "CONCEPTMAP"),)),
    ("prefix", (("prefix", "PREFIX"),)),
    # ----------------- Symbols -----------------
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
    (":", ((":", ":"),)),
    (";", ((";", ";"),)),
    ("[", (("[", "["),)),
    ("]", (("]", "]"),)),
    ("=", (("=", "EQUAL"),)),
    ("<", (("<", "LESS_THAN"),)),
    (">", ((">", "GREATER_THAN"),)),
    ("==", (("==", "DOUBLE_EQUAL"),)),
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
    (
        "// documentation of something",
        (("documentation of something", "DOCUMENTATION"),),
    ),
    ('"hello world"', (("hello world", "STRING"),)),
    ('"test"', (("test", "STRING"),)),
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
    # ----------------- Other -----------------
    ("->", (("->", "RIGHT_ARROW"),)),
    ("<<types>>", (("types", "GROUPTYPE"),)),
    ("<<type+>>", (("type-and-types", "GROUPTYPE"),)),
    # ----------------- Complex  -----------------
    (
        "/// name = 'title'",
        (
            ("///", "METADATA_DECLARATION"),
            ("name", "IDENTIFIER"),
            ("=", "EQUAL"),
            ("title", "STRING"),
        ),
    ),
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
        "let const = example.value;",
        (
            ("let", "LET"),
            ("const", "IDENTIFIER"),
            ("=", "EQUAL"),
            ("example", "IDENTIFIER"),
            (".", "."),
            ("value", "IDENTIFIER"),
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
    (
        "map 'some title' = title",
        (
            ("map", "MAP"),
            ("some title", "STRING"),
            ("=", "EQUAL"),
            ("title", "IDENTIFIER"),
        ),
    ),
    (
        "imports 'http://example.org'",
        (
            ("imports", "IMPORTS"),
            ("http://example.org", "STRING"),
        ),
    ),
    (
        "group patient extends person",
        (
            ("group", "GROUP"),
            ("patient", "IDENTIFIER"),
            ("extends", "EXTENDS"),
            ("person", "IDENTIFIER"),
        ),
    ),
    (
        "source src: Patient as patient",
        (
            ("source", "SOURCE"),
            ("src", "IDENTIFIER"),
            (":", ":"),
            ("Patient", "ROOT_NODE"),
            ("as", "AS"),
            ("patient", "IDENTIFIER"),
        ),
    ),
    (
        "target tgt: Patient as patient",
        (
            ("target", "TARGET"),
            ("tgt", "IDENTIFIER"),
            (":", ":"),
            ("Patient", "ROOT_NODE"),
            ("as", "AS"),
            ("patient", "IDENTIFIER"),
        ),
    ),
    (
        "where condition -> create patient",
        (
            ("where", "WHERE"),
            ("condition", "IDENTIFIER"),
            ("->", "RIGHT_ARROW"),
            ("create", "IDENTIFIER"),
            ("patient", "IDENTIFIER"),
        ),
    ),
    (
        "check src.exists()",
        (
            ("check", "CHECK"),
            ("src", "IDENTIFIER"),
            (".", "."),
            ("exists", "IDENTIFIER"),
            ("(", "("),
            (")", ")"),
        ),
    ),
    (
        "log 'Processing patient'",
        (
            ("log", "LOG"),
            ("Processing patient", "STRING"),
        ),
    ),
    # ----------------- Edge Cases for Numbers -----------------
    ("0", ((0, "INTEGER"),)),
    ("-0", ((0, "INTEGER"),)),
    ("0.0", ((0.0, "DECIMAL"),)),
    ("-0.0", ((-0.0, "DECIMAL"),)),
    ("123.456", ((123.456, "DECIMAL"),)),
    ("-999", ((-999, "INTEGER"),)),
    # ----------------- Edge Cases for Dates/Times -----------------
    ("@2024-12-31", (("@2024-12-31", "DATE"),)),
    ("@T23:59:59", (("@T23:59:59", "TIME"),)),
    ("@T23:59:59.999", (("@T23:59:59.999", "TIME"),)),
    (
        "@2024-12-31T23:59:59.999-05:00",
        (("@2024-12-31T23:59:59.999-05:00", "DATETIME"),),
    ),
    # ----------------- Multiple Tokens in Sequence -----------------
    (
        "let x = 5; let y = 10;",
        (
            ("let", "LET"),
            ("x", "IDENTIFIER"),
            ("=", "EQUAL"),
            (5, "INTEGER"),
            (";", ";"),
            ("let", "LET"),
            ("y", "IDENTIFIER"),
            ("=", "EQUAL"),
            (10, "INTEGER"),
            (";", ";"),
        ),
    ),
    (
        "src.name -> tgt.fullName",
        (
            ("src", "IDENTIFIER"),
            (".", "."),
            ("name", "IDENTIFIER"),
            ("->", "RIGHT_ARROW"),
            ("tgt", "IDENTIFIER"),
            (".", "."),
            ("fullName", "IDENTIFIER"),
        ),
    ),
    # ----------------- Mixed Operations -----------------
    (
        "first() + last()",
        (
            ("first", "FIRST"),
            ("(", "("),
            (")", ")"),
            ("+", "+"),
            ("last", "LAST"),
            ("(", "("),
            (")", ")"),
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
