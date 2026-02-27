import keyword
from unittest.mock import MagicMock
from pydantic.fields import _Unset
import pytest
from typing import Any, List, Optional
from pydantic.aliases import AliasChoices
from fhircraft.fhir.resources.datatypes import primitives
from fhircraft.fhir.resources.datatypes.R4 import core, complex
from fhircraft.fhir.resources.factory.builders.base import (
    FHIR_SD_PREFIX,
    FHIRPATH_TYPE_PREFIX,
    FieldInformation,
)
from fhircraft.fhir.resources.factory.exceptions import TypeResolutionError
from fhircraft.fhir.resources.factory.builders.base import (
    Builder,
)


# ---------------------------------------------------------------------------
# Helpers & Fixtures
# ---------------------------------------------------------------------------


def make_context(factory_build_result=None):
    ctx = MagicMock()
    if factory_build_result is not None:
        ctx.factory.build.return_value = factory_build_result
    return ctx


def make_type(code, profile=None, fhir_release="R4"):
    """Return a minimal stand-in for an ElementDefinitionType-like object."""
    t = MagicMock()
    t.code = code
    t.profile = profile
    t._fhir_release = fhir_release
    return t


def make_node(
    is_array: bool = False,
    min_cardinality: int | None = 0,
    max_cardinality: int | None = None,
    documentation: str | None = None,
):
    """Return a minimal mock of ElementNode."""
    node = MagicMock()
    node.is_array = is_array
    node.min_cardinality = min_cardinality
    node.max_cardinality = max_cardinality
    node.documentation = documentation
    return node


@pytest.fixture
def builder() -> Builder:
    class _ConcreteBuilder(Builder):

        # Not needed for these tests
        def can_handle(self, *args, **kwargs):
            pass

        # Not needed for these tests
        def build(self, *args, **kwargs):
            pass

        # Mock helper
        def make_factory_result(self, factory_build_result=None):
            self.context.factory = MagicMock()  # type: ignore[assignment]
            if factory_build_result is not None:
                self.context.factory.build.return_value = factory_build_result
            return self.context

    return _ConcreteBuilder(context=MagicMock())


# ==================================================================
# Builder.handle_python_keyword
# ==================================================================


@pytest.mark.parametrize(
    "kw",
    [
        "class",
        "for",
        "if",
        "else",
        "return",
        "import",
        "from",
        "pass",
        "def",
        "while",
        "in",
        "not",
        "and",
        "or",
        "is",
        "lambda",
        "yield",
        "with",
        "try",
        "except",
        "finally",
        "raise",
        "del",
        "global",
        "assert",
        "break",
        "continue",
        "as",
        "elif",
        "nonlocal",
        "async",
        "await",
    ],
)
def test_handle_python_keyword__python_keywords(kw: str) -> None:
    """Every Python keyword must be suffixed with '_' and have an AliasChoices."""
    assert keyword.iskeyword(kw), f"{kw!r} is expected to be a Python keyword"
    safe_name, alias = Builder.handle_python_keyword(kw)
    assert safe_name == f"{kw}_"
    assert isinstance(alias, AliasChoices)
    assert kw in alias.choices
    assert f"{kw}_" in alias.choices


@pytest.mark.parametrize(
    "kw",
    [
        "class",
        "property",
        "classmethod",
        "field_validator",
        "model_validator",
    ],
)
def test_handle_python_keyword__class_reserved_words(kw: str) -> None:
    safe, alias = Builder.handle_python_keyword(kw)
    assert safe == f"{kw}_"
    assert alias is not None


@pytest.mark.parametrize(
    "name",
    ["id", "code", "value", "identifier", "extension", "meta", "", "X"],
)
def test_handle_python_keyword__returns_unchanged(name: str) -> None:
    """Non-reserved names must be returned as-is with None alias."""
    safe, alias = Builder.handle_python_keyword(name)
    assert safe == name
    assert alias is None


def test_handle_python_keyword__alias_contains_both_original_and_safe_name() -> None:
    """AliasChoices must contain both the original keyword and the safe alias."""
    original = "class"
    safe, alias = Builder.handle_python_keyword(original)
    assert alias is not None
    assert original in alias.choices
    assert safe in alias.choices


def test_handle_python_keyword__alias_choices_order() -> None:
    """Original name should appear before the safe name in AliasChoices."""
    _, alias = Builder.handle_python_keyword("for")
    assert alias is not None
    assert alias.choices[0] == "for"
    assert alias.choices[1] == "for_"


# ==================================================================
# Builder.resolve_type
# ==================================================================


def test_resolve_type__raises_when_code_is_none(builder: Builder):
    with pytest.raises(TypeResolutionError, match="no code"):
        builder.resolve_type(make_type(code=None))


def test_resolve_type__raises_when_code_is_empty_string(builder: Builder):
    with pytest.raises(TypeResolutionError):
        builder.resolve_type(make_type(code=""))


FHIR_PRIMITIVE_CODES = [
    ("string", primitives.String),
    ("integer", primitives.Integer),
    ("integer64", primitives.Integer64),
    ("positiveInt", primitives.PositiveInt),
    ("boolean", primitives.Boolean),
    ("decimal", primitives.Decimal),
    ("date", primitives.Date),
    ("dateTime", primitives.DateTime),
    ("time", primitives.Time),
    ("code", primitives.Code),
    ("id", primitives.Id),
    ("uri", primitives.Uri),
    ("canonical", primitives.Canonical),
]


@pytest.mark.parametrize(
    "code, expected",
    FHIR_PRIMITIVE_CODES,
)
def test_resolve_type__primitive(builder: Builder, code, expected):
    # Simulate a primitive: not a subclass of FHIRBaseModel
    info = builder.resolve_type(make_type(code=code))
    assert info.kind == "primitive"
    assert info.requires_primitive_extension == True
    assert info.type is expected


@pytest.mark.parametrize(
    "code, expected",
    FHIR_PRIMITIVE_CODES,
)
def test_resolve_type__primitive_absolute_url(builder: Builder, code, expected):
    info = builder.resolve_type(make_type(code=f"{FHIR_SD_PREFIX}{code}"))
    assert info.kind == "primitive"
    assert info.requires_primitive_extension == True
    assert info.type is expected


FHIRPATH_CODES = [
    ("System.String", primitives.String),
    ("System.Integer", primitives.Integer),
    ("System.Boolean", primitives.Boolean),
    ("System.Decimal", primitives.Decimal),
    ("System.Date", primitives.Date),
    ("System.DateTime", primitives.DateTime),
    ("System.Time", primitives.Time),
]


@pytest.mark.parametrize(
    "code, expected",
    FHIRPATH_CODES,
)
def test_resolve_type__fhirpath_without_profile(builder: Builder, code, expected):
    info = builder.resolve_type(make_type(code=f"http://hl7.org/fhirpath/{code}"))
    assert info.kind == "primitive"
    assert info.requires_primitive_extension == False
    assert info.type is expected


@pytest.mark.parametrize(
    "code, profile, expected",
    [
        ("System.String", "Uri", primitives.Uri),
        ("System.String", "Code", primitives.Code),
        ("System.String", "Canonical", primitives.Canonical),
        ("System.Integer", "Integer64", primitives.Integer64),
        ("System.Integer", "PositiveInt", primitives.PositiveInt),
        ("System.Boolean", "Boolean", primitives.Boolean),
        ("System.Decimal", "Decimal", primitives.Decimal),
        ("System.Date", "Date", primitives.Date),
        ("System.DateTime", "DateTime", primitives.DateTime),
        ("System.Time", "Time", primitives.Time),
    ],
)
def test_resolve_type__fhirpath_with_profile(builder: Builder, code, profile, expected):
    info = builder.resolve_type(
        make_type(
            code=f"http://hl7.org/fhirpath/{code}",
            profile=[f"{FHIR_SD_PREFIX}{profile}"],
        )
    )
    assert info.kind == "primitive"
    assert info.requires_primitive_extension == False
    assert info.type is expected


FHIR_COMPLEX_CODES = [
    ("Element", complex.Element),
    ("Coding", complex.Coding),
    ("Extension", complex.Extension),
    ("CodeableConcept", complex.CodeableConcept),
    ("HumanName", complex.HumanName),
]


@pytest.mark.parametrize(
    "code, expected",
    FHIR_COMPLEX_CODES,
)
def test_resolve_type__complex(builder: Builder, code, expected):
    info = builder.resolve_type(make_type(code=code))
    assert info.kind == "complex-type"
    assert info.requires_primitive_extension == False
    assert info.type is expected


@pytest.mark.parametrize(
    "code, expected",
    FHIR_COMPLEX_CODES,
)
def test_resolve_type__complex_absolute_url(builder: Builder, code, expected):
    info = builder.resolve_type(make_type(code=f"{FHIR_SD_PREFIX}{code}"))
    assert info.kind == "complex-type"
    assert info.requires_primitive_extension == False
    assert info.type is expected


FHIR_RESOURCE_CODES = [
    ("Patient", core.Patient),
    ("Observation", core.Observation),
    ("Condition", core.Condition),
    ("Medication", core.Medication),
    ("Practitioner", core.Practitioner),
]


@pytest.mark.parametrize(
    "code, expected",
    FHIR_RESOURCE_CODES,
)
def test_resolve_type__resource(builder: Builder, code, expected):
    info = builder.resolve_type(make_type(code=code))
    assert info.kind == "resource"
    assert info.requires_primitive_extension == False
    assert info.type is expected


@pytest.mark.parametrize(
    "code, expected",
    FHIR_RESOURCE_CODES,
)
def test_resolve_type__resource_absolute_url(builder: Builder, code, expected):
    info = builder.resolve_type(make_type(code=f"{FHIR_SD_PREFIX}{code}"))
    assert info.kind == "resource"
    assert info.requires_primitive_extension == False
    assert info.type is expected


@pytest.mark.parametrize(
    "kind, id, expected,",
    [
        ("complex-type", "extension-profile", complex.Extension),
        ("resource", "medication-profile", core.Medication),
    ],
)
def test_profile_profile(builder: Builder, kind, id, expected):
    builder.make_factory_result(factory_build_result=expected)  # type: ignore

    profile_url = f"http://example.org/fhir/org/StructureDefinition/{id}"
    info = builder.resolve_type(make_type(code="Reference", profile=[profile_url]))
    assert info.kind == kind
    assert info.requires_primitive_extension == False
    assert info.type is expected


# ==================================================================
# Builder.build_field_information
# ==================================================================


def test_build_field_information__returns_field_information_instance():
    node = make_node()
    result = Builder.build_field_information("status", node, str)
    assert isinstance(result, FieldInformation)


@pytest.mark.parametrize(
    "default, is_array, type, expected_default, expected_annotation",
    [
        (_Unset, False, str, None, Optional[str]),
        (None, False, str, None, Optional[str]),
        ("active", False, str, "active", Optional[str]),
        (_Unset, True, str, None, Optional[List[str]]),
        ("active", True, str, ["active"], Optional[List[str]]),
        (["active"], True, str, ["active"], Optional[List[str]]),
        (["active", "final"], True, str, ["active", "final"], Optional[List[str]]),
    ],
)
def test_build_field_information__default_unset_becomes_none(
    default, is_array, type, expected_default, expected_annotation
):
    node = make_node(is_array=is_array)
    info = Builder.build_field_information("status", node, type, default=default)
    assert info.name == "status"
    assert info.annotation is expected_annotation
    assert info.default == expected_default
