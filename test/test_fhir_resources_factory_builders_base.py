import keyword
from typing_extensions import get_args
from unittest.mock import MagicMock
import pytest
from typing import Any, List, Optional
from pydantic.aliases import AliasChoices
from fhircraft.fhir.resources.datatypes import primitives
from fhircraft.fhir.resources.datatypes.R4 import core, complex
from fhircraft.fhir.resources.datatypes.utils import get_fhir_type
from fhircraft.fhir.resources.factory.builders.base import (
    FHIR_SD_PREFIX,
    FHIR_TYPE_EXT_URL,
    FieldInformation,
)

from fhircraft.fhir.resources.factory.builders.base import ValidatorInformation
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


def make_type(code, profile=None, fhir_release="R4", extension=None):
    """Return a minimal stand-in for an ElementDefinitionType-like object."""
    t = MagicMock()
    t.code = code
    t.profile = profile
    t._fhir_release = fhir_release
    t.extension = extension
    return t


def make_node(
    name: str = "field",
    is_array: bool = False,
    min_cardinality: int | None = 0,
    max_cardinality: int | None = None,
    documentation: str | None = None,
    default_value: Any = None,
):
    """Return a minimal mock of ElementNode."""
    node = MagicMock()
    node.name = name
    node.is_array = is_array
    node.min_cardinality = min_cardinality
    node.max_cardinality = max_cardinality
    node.documentation = documentation
    node.default_value = default_value
    node.fixed = None
    node.pattern = None
    return node


def make_constraint(
    key: str, expression: str = "true", human: str = "ok", severity: str = "error"
):
    c = MagicMock()
    c.key = key
    c.expression = expression
    c.human = human
    c.severity = severity
    return c


def make_validator_node(
    name: str = "field",
    fixed=None,
    pattern=None,
    constraints=None,
    is_array: bool = False,
    min_cardinality: int = 0,
    max_cardinality=None,
    documentation=None,
    default_value=None,
):
    node = make_node(
        name=name,
        is_array=is_array,
        min_cardinality=min_cardinality,
        max_cardinality=max_cardinality,
        documentation=documentation,
        default_value=default_value,
    )
    node.fixed = fixed
    node.pattern = pattern
    node.definition.constraint = constraints or []
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
    "code, fhir_type, expected",
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
def test_resolve_type__fhirpath_with_extension(
    builder: Builder, code, fhir_type, expected
):
    type_extension = MagicMock()
    type_extension.url = FHIR_TYPE_EXT_URL
    type_extension.valueUrl = fhir_type
    info = builder.resolve_type(
        make_type(
            code=f"http://hl7.org/fhirpath/{code}",
            extension=[type_extension],
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
        (None, False, str, None, Optional[str]),
        ("active", False, str, "active", Optional[str]),
        (None, True, str, None, Optional[List[str]]),
        ("active", True, str, ["active"], Optional[List[str]]),
        (["active"], True, str, ["active"], Optional[List[str]]),
        (["active", "final"], True, str, ["active", "final"], Optional[List[str]]),
    ],
)
def test_build_field_information__defaults(
    default, is_array, type, expected_default, expected_annotation
):
    node = make_node(is_array=is_array, default_value=default)
    info = Builder.build_field_information("status", node, type)
    assert info.name == "status"
    assert info.annotation == expected_annotation
    assert info.default == expected_default


# ===========================================================================
# Builder.build_primitive_extension_placeholder
# ===========================================================================


def test_build_primitive_extension_placeholder__returns_field_information(
    builder: Builder,
):
    node = make_node("status")
    builder.context = MagicMock(fhir_release="R4")
    result = builder.build_primitive_extension_placeholder(node)
    assert isinstance(result, FieldInformation)


@pytest.mark.parametrize(
    "field_name",
    [
        "status",
        "value",
        "birthDate",
        "id",
        "text",
        "class",
        "deceased",
    ],
)
def test_build_primitive_extension_placeholder__name_is_field_name_suffixed_with_ext(
    builder: Builder, field_name
):
    node = make_node(name=field_name)
    builder.context = MagicMock(fhir_release="R4")
    result = builder.build_primitive_extension_placeholder(node)
    assert result.name == f"{field_name}_ext"


@pytest.mark.parametrize(
    "field_name",
    [
        "status",
        "value",
        "birthDate",
        "id",
        "class",
    ],
)
def test_build_primitive_extension_placeholder__alias_is_underscore_prefixed_field_name(
    builder: Builder, field_name
):
    node = make_node(name=field_name)
    builder.context = MagicMock(fhir_release="R4")
    result = builder.build_primitive_extension_placeholder(node)
    assert result.alias == f"_{field_name}"


@pytest.mark.parametrize("fhir_release", ["R4", "R4B", "R5"])
def test_build_primitive_extension_placeholder__annotation_non_array_is_optional_element(
    builder: Builder, fhir_release
):
    Element = get_fhir_type("Element", fhir_release)
    builder.context = MagicMock(fhir_release=fhir_release)
    node = make_node(name="status", is_array=False)
    result = builder.build_primitive_extension_placeholder(node)
    assert result.annotation == Optional[Element]


@pytest.mark.parametrize("fhir_release", ["R4", "R4B", "R5"])
def test_build_primitive_extension_placeholder__annotation_array_is_optional_list_of_element(
    builder: Builder, fhir_release
):
    Element = get_fhir_type("Element", fhir_release)
    builder.context = MagicMock(fhir_release=fhir_release)
    node = make_node(name="name", is_array=True)
    result = builder.build_primitive_extension_placeholder(node)
    assert result.annotation == Optional[List[Element]]


@pytest.mark.parametrize("fhir_release", ["R4", "R4B", "R5"])
def test_build_primitive_extension_placeholder__element_type_matches_fhir_release(
    builder: Builder, fhir_release
):
    expected_Element = get_fhir_type("Element", fhir_release)
    builder.context = MagicMock(fhir_release=fhir_release)
    node = make_node(name="status")
    result = builder.build_primitive_extension_placeholder(node)

    inner = get_args(result.annotation)  # (Element, NoneType)
    assert expected_Element in inner


@pytest.mark.parametrize(
    "field_name",
    [
        "status",
        "class",
        "birthDate",
        "id",
        "gender",
        "text",
    ],
)
def test_build_primitive_extension_placeholder__validation_alias_is_none_for_normal_names(
    builder: Builder, field_name
):
    node = make_node(name=field_name)
    builder.context = MagicMock(fhir_release="R4")
    result = builder.build_primitive_extension_placeholder(node)
    assert result.validation_alias is None


# ==================================================================
# Builder.build_field_validators
# ==================================================================


def test_build_field_validators__returns_list(builder: Builder):
    node = make_validator_node()
    result = builder.build_field_validators(node, "field")
    assert isinstance(result, list)


def test_build_field_validators__empty_when_nothing_set(builder: Builder):
    node = make_validator_node()
    result = builder.build_field_validators(node, "field")
    assert result == []


def test_build_field_validators__fixed_adds_one_validator(builder: Builder):
    node = make_validator_node(fixed="active")
    result = builder.build_field_validators(node, "status")
    assert len(result) == 1


def test_build_field_validators__fixed_returns_validator_information(builder: Builder):
    node = make_validator_node(fixed="active")
    result = builder.build_field_validators(node, "status")
    assert isinstance(result[0], ValidatorInformation)


def test_build_field_validators__fixed_validator_name(builder: Builder):
    node = make_validator_node(fixed="active")
    result = builder.build_field_validators(node, "status")
    assert result[0].name == "FHIR_status_fixed_value_constraint"


def test_build_field_validators__fixed_validator_kind_is_field(builder: Builder):
    node = make_validator_node(fixed="active")
    result = builder.build_field_validators(node, "status")
    assert result[0].kind == "field"


def test_build_field_validators__fixed_validator_field_matches_safe_name(
    builder: Builder,
):
    node = make_validator_node(fixed="active")
    result = builder.build_field_validators(node, "status")
    assert result[0].field == "status"


def test_build_field_validators__fixed_validator_arguments_contain_constant(
    builder: Builder,
):
    node = make_validator_node(fixed="active")
    result = builder.build_field_validators(node, "status")
    assert result[0].arguments == {"constant": "active"}


@pytest.mark.parametrize("fixed_value", ["active", 42, True, {"code": "abc"}])
def test_build_field_validators__fixed_value_forwarded(builder: Builder, fixed_value):
    node = make_validator_node(fixed=fixed_value)
    result = builder.build_field_validators(node, "status")
    assert result[0].arguments["constant"] == fixed_value


def test_build_field_validators__pattern_adds_one_validator(builder: Builder):
    node = make_validator_node(pattern={"system": "http://loinc.org"})
    result = builder.build_field_validators(node, "code")
    assert len(result) == 1


def test_build_field_validators__pattern_returns_validator_information(
    builder: Builder,
):
    node = make_validator_node(pattern={"system": "http://loinc.org"})
    result = builder.build_field_validators(node, "code")
    assert isinstance(result[0], ValidatorInformation)


def test_build_field_validators__pattern_validator_name(builder: Builder):
    node = make_validator_node(pattern={"system": "http://loinc.org"})
    result = builder.build_field_validators(node, "code")
    assert result[0].name == "FHIR_code_pattern_constraint"


def test_build_field_validators__pattern_validator_kind_is_field(builder: Builder):
    node = make_validator_node(pattern={"system": "http://loinc.org"})
    result = builder.build_field_validators(node, "code")
    assert result[0].kind == "field"


def test_build_field_validators__pattern_validator_field_matches_safe_name(
    builder: Builder,
):
    node = make_validator_node(pattern={"system": "http://loinc.org"})
    result = builder.build_field_validators(node, "code")
    assert result[0].field == "code"


def test_build_field_validators__single_constraint_adds_one_validator(builder: Builder):
    node = make_validator_node(constraints=[make_constraint("ele-1")])
    result = builder.build_field_validators(node, "value")
    assert len(result) == 1


def test_build_field_validators__constraint_validator_kind_is_model(builder: Builder):
    node = make_validator_node(constraints=[make_constraint("ele-1")])
    result = builder.build_field_validators(node, "value")
    assert result[0].kind == "model"


def test_build_field_validators__constraint_validator_name_derived_from_key(
    builder: Builder,
):
    node = make_validator_node(constraints=[make_constraint("ele-1")])
    result = builder.build_field_validators(node, "value")
    assert result[0].name == "FHIR_ele_1_constraint_validator"


def test_build_field_validators__constraint_validator_arguments(builder: Builder):
    c = make_constraint(
        "ele-1",
        expression="hasValue()",
        human="All FHIR elements must have a value or child elements",
        severity="error",
    )
    node = make_validator_node(constraints=[c])
    result = builder.build_field_validators(node, "value")
    args = result[0].arguments
    assert args["expression"] == "hasValue()"
    assert args["human"] == "All FHIR elements must have a value or child elements"
    assert args["key"] == "ele-1"
    assert args["severity"] == "error"


def test_build_field_validators__multiple_constraints_each_produce_validator(
    builder: Builder,
):
    node = make_validator_node(
        constraints=[
            make_constraint("ele-1"),
            make_constraint("obs-6"),
            make_constraint("obs-7"),
        ]
    )
    result = builder.build_field_validators(node, "value")
    assert len(result) == 3


def test_build_field_validators__constraint_key_hyphens_replaced_with_underscores(
    builder: Builder,
):
    node = make_validator_node(constraints=[make_constraint("obs-6-custom-key")])
    result = builder.build_field_validators(node, "value")
    assert result[0].name == "FHIR_obs_6_custom_key_constraint_validator"


def test_build_field_validators__fixed_and_pattern_produce_two_validators(
    builder: Builder,
):
    node = make_validator_node(fixed="active", pattern={"system": "x"})
    result = builder.build_field_validators(node, "code")
    assert len(result) == 2
    names = {v.name for v in result}
    assert "FHIR_code_fixed_value_constraint" in names
    assert "FHIR_code_pattern_constraint" in names


def test_build_field_validators__fixed_and_constraint_produce_two_validators(
    builder: Builder,
):
    node = make_validator_node(fixed="active", constraints=[make_constraint("ele-1")])
    result = builder.build_field_validators(node, "status")
    assert len(result) == 2


def test_build_field_validators__pattern_and_constraint_produce_two_validators(
    builder: Builder,
):
    node = make_validator_node(
        pattern={"system": "http://loinc.org"},
        constraints=[make_constraint("ele-1")],
    )
    result = builder.build_field_validators(node, "code")
    assert len(result) == 2


def test_build_field_validators__all_three_sources_produce_correct_total(
    builder: Builder,
):
    node = make_validator_node(
        fixed="active",
        pattern={"system": "x"},
        constraints=[make_constraint("ele-1"), make_constraint("ele-2")],
    )
    result = builder.build_field_validators(node, "code")
    assert len(result) == 4


@pytest.mark.parametrize("safe_name", ["status", "class_", "value", "for_"])
def test_build_field_validators__safe_name_used_in_validator_names(
    builder: Builder, safe_name
):
    node = make_validator_node(fixed="x", pattern={"a": 1})
    result = builder.build_field_validators(node, safe_name)
    assert result[0].name == f"FHIR_{safe_name}_fixed_value_constraint"
    assert result[1].name == f"FHIR_{safe_name}_pattern_constraint"


@pytest.mark.parametrize("safe_name", ["status", "class_", "value", "for_"])
def test_build_field_validators__field_attribute_uses_safe_name(
    builder: Builder, safe_name
):
    node = make_validator_node(fixed="x")
    result = builder.build_field_validators(node, safe_name)
    assert result[0].field == safe_name


def test_build_field_validators__fixed_as_pydantic_definition_returns_name_and_callable(
    builder: Builder,
):
    node = make_validator_node(fixed="active")
    validator_info = builder.build_field_validators(node, "status")[0]
    fn = validator_info.as_pydantic_definition()
    assert fn is not None


def test_build_field_validators__pattern_as_pydantic_definition_returns_name_and_callable(
    builder: Builder,
):
    node = make_validator_node(pattern={"system": "x"})
    validator_info = builder.build_field_validators(node, "code")[0]
    fn = validator_info.as_pydantic_definition()
    assert fn is not None


def test_build_field_validators__constraint_as_pydantic_definition_returns_name_and_callable(
    builder: Builder,
):
    node = make_validator_node(constraints=[make_constraint("ele-1")])
    validator_info = builder.build_field_validators(node, "value")[0]
    fn = validator_info.as_pydantic_definition()
    assert fn is not None


# ===========================================================================
# Builder.resolve_type_from_base_model
# ===========================================================================

from pydantic import BaseModel as PydanticBaseModel


class _InnerModel(PydanticBaseModel):
    """A simple nested BaseModel used as a field type."""

    value: str = ""


def _set_base(builder: Builder, base: type) -> Builder:
    """Point builder.context.base at *base* for resolve_type_from_base_model calls."""
    builder.context.base = base  # type: ignore
    return builder


def test_resolve_type_from_base_model__returns_none_when_field_absent(
    builder: Builder,
):

    class _DirectModel(PydanticBaseModel):
        inner: _InnerModel

    _set_base(builder, _DirectModel)
    assert builder.resolve_type_from_base_model("nonexistent") is None


def test_resolve_type_from_base_model__returns_type_for_direct_model_annotation(
    builder: Builder,
):

    class _DirectModel(PydanticBaseModel):
        inner: _InnerModel

    _set_base(builder, _DirectModel)
    result = builder.resolve_type_from_base_model("inner")
    assert result is _InnerModel


def test_resolve_type_from_base_model__unwraps_optional_model(
    builder: Builder,
):

    class _OptionalModel(PydanticBaseModel):
        inner: Optional[_InnerModel] = None

    _set_base(builder, _OptionalModel)
    result = builder.resolve_type_from_base_model("inner")
    assert result is _InnerModel


def test_resolve_type_from_base_model__unwraps_list_of_model(
    builder: Builder,
):

    class _ListModel(PydanticBaseModel):
        inner: List[_InnerModel]

    _set_base(builder, _ListModel)
    result = builder.resolve_type_from_base_model("inner")
    assert result is _InnerModel


def test_resolve_type_from_base_model__unwraps_optional_list_of_model(
    builder: Builder,
):

    class _OptionalListModel(PydanticBaseModel):
        inner: Optional[List[_InnerModel]] = None

    _set_base(builder, _OptionalListModel)
    result = builder.resolve_type_from_base_model("inner")
    assert result is _InnerModel


def test_resolve_type_from_base_model__returns_none_for_str_field(
    builder: Builder,
):

    class _PrimitiveModel(PydanticBaseModel):
        name: str = ""

    _set_base(builder, _PrimitiveModel)
    assert builder.resolve_type_from_base_model("name") is None


def test_resolve_type_from_base_model__returns_none_for_optional_str_field(
    builder: Builder,
):

    class _OptionalPrimitiveModel(PydanticBaseModel):
        name: Optional[str] = None

    _set_base(builder, _OptionalPrimitiveModel)
    assert builder.resolve_type_from_base_model("name") is None


def test_resolve_type_from_base_model__returns_none_for_list_of_str_field(
    builder: Builder,
):

    class _ListPrimitiveModel(PydanticBaseModel):
        names: List[str] = []

    _set_base(builder, _ListPrimitiveModel)
    assert builder.resolve_type_from_base_model("names") is None


def test_resolve_type_from_base_model__returns_none_when_base_is_not_pydantic_model(
    builder: Builder,
):
    class PlainClass:
        pass

    builder.context.base = PlainClass  # type: ignore
    assert builder.resolve_type_from_base_model("inner") is None
