import ply.lex

from fhircraft.fhir.path.lexer import FhirPathLexer


class FhirMappingLanguageLexerError(Exception):
    pass


class FhirMappingLanguageLexer(FhirPathLexer):
    """
    A Lexical analyzer for JsonPath.

    """

    def __init__(self, debug=False):
        self.debug = debug
        if self.__doc__ is None:
            raise FhirMappingLanguageLexerError(
                "Docstrings have been removed by design of PLY."
            )

    def tokenize(self, string):
        """
        Maps a string to an iterator over tokens. In other words: [char] -> [token]
        """

        new_lexer = ply.lex.lex(module=self)
        new_lexer.latest_newline = 0
        new_lexer.string_value = None
        new_lexer.input(string)

        while True:
            t = new_lexer.token()
            if t is None:
                break
            t.col = t.lexpos - new_lexer.latest_newline
            yield t

        if new_lexer.string_value is not None:
            raise FhirMappingLanguageLexerError(
                "Unexpected EOF in string literal or identifier"
            )

    # ============== PLY Lexer specification ==================
    #
    # Tokenizer for FHIRpath
    #
    # =========================================================

    literals = [
        ".",
        ",",
        ";",
        ":",
        "[",
        "]",
        "(",
        ")",
        "{",
        "}",
        "=",
        "+",
        "-",
        "*",
        "|",
        "/",
        "&",
        "<",
        ">",
    ]

    reserved_words = {
        # Reserved keywords (https://build.fhir.org/mapping-language.html#reserved)
        # -------------------------------------------------------------------------------
        **{
            word: word.upper()
            for word in [
                "map",
                "uses",
                "as",
                "alias",
                "imports",
                "group",
                "extends",
                "default",
                "where",
                "check",
                "log",
                "let",
                "then",
                "first",
                "not_first",
                "last",
                "not_last",
                "only_one",
                "share",
                "single",
                "source",
                "target",
                "queried",
                "produced",
                "conceptmap",
                "prefix",
            ]
        },
    }

    # List of token names
    tokens = list(set(reserved_words.values())) + [
        "IDENTIFIER",
        "DELIMITEDIDENTIFIER",
        "METADATA_DECLARATION",
        "DOCUMENTATION",
        "GROUPTYPE",
        "INTEGER",
        "DECIMAL",
        "BOOLEAN",
        "DATE",
        "TIME",
        "DATETIME",
        "STRING",
        "RIGHT_ARROW",
        "DOUBLE_EQUAL",
    ]

    def t_ignore_WHITESPACE(self, t):
        r"[\s]"
        if t.value == "\n":
            t.lexer.lineno += 1
            t.lexer.latest_newline = t.lexpos

    def t_METADATA_DECLARATION(self, t):
        r"\/\/\/"
        return t

    def t_DOCUMENTATION(self, t):
        r"\/{2}(.*)"
        for substring in ["//", "/*", "*/"]:
            t.value = t.value.replace(substring, "")
        t.value = t.value.strip()
        return t

    def t_RIGHT_ARROW(self, t):
        r"->"
        return t

    def t_DATETIME(self, t):
        r"@\d{4}(?:-\d{2}(?:-\d{2})?)?T(?:\d{2}(?:\:\d{2}(?:\:\d{2}(?:.\d{3}(?:[\+|\-]\d{2}(?:\:\d{2})?)?)?)?)?)?"
        return t

    def t_DATE(self, t):
        r"@\d{4}(?:-\d{2}(?:-\d{2})?)?"
        return t

    def t_BOOLEAN(self, t):
        r"true|false"
        return t

    def t_TIME(self, t):
        r"\@T\d{2}(?:\:\d{2}(?:\:\d{2}(?:\.\d{3}(?:[+|-]\d{2}(?:\:\d{2})?)?)?)?)?"
        return t

    def t_NUMBER(self, t):
        r"-?\d+(\.\d+)?"
        if "." in t.value:
            t.value = float(t.value)
            t.type = "DECIMAL"
        else:
            t.value = int(t.value)
            t.type = "INTEGER"
        return t

    def t_STRING(self, t):
        r"(\'([^\']*)?\')|(\"([^\"]*)?\")"
        if t.value.startswith("'") and t.value.endswith("'"):
            t.value = t.value.strip("'")
        else:
            t.value = t.value.strip('"')
        return t

    def t_GROUPTYPE(self, t):
        r"<<types>>|<<type\+>>"
        t.value = t.value.strip("<").strip(">")
        t.value = {"types": "types", "type+": "type-and-types"}[t.value]
        return t

    def t_DOUBLE_EQUAL(self, t):
        r"=="
        return t

    def t_DELIMITEDIDENTIFIER(self, t):
        r"\`[a-zA-Z][a-zA-Z0-9\-][^\`]*\`"
        t.value = t.value.strip("`")
        return t

    def t_error_invalid_function(self, t):
        r""" " """
        pass

    def t_error(self, t):
        raise FhirMappingLanguageLexerError(
            f"FHIRPath lexer error at {t.lexer.lineno}:{t.lexpos - t.lexer.latest_newline} - Unexpected character: {t.value[0]}"
        )
