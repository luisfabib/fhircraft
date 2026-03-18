from typing import List, Optional
from unittest.mock import MagicMock, patch
from typing import get_args

import pytest
from pydantic.aliases import AliasChoices

from fhircraft.fhir.resources.datatypes import primitives
from fhircraft.fhir.resources.datatypes.R4 import complex as r4_complex, core as r4_core
from fhircraft.fhir.resources.factory.builders.base import (
    Build,
    Builder,
    TypeInformation,
)
from fhircraft.fhir.resources.factory.builders.simple import SimpleFieldBuilder
from fhircraft.fhir.resources.factory.exceptions import TypeResolutionError


# ---------------------------------------------------------------------------
# Helpers & fixtures
# ---------------------------------------------------------------------------


def make_type_definition(type_code, profile=None):
    type_def = MagicMock(name="mock-element-definition-type")
    type_def.code = type_code
    type_def._fhir_release = "R4"
    type_def.profile = [profile] if profile else None
    return type_def


def make_node(
    name: str,
    types=(),
    type_codes=(),
    is_array: bool = False,
    min_cardinality: int = 0,
    max_cardinality: int | None = None,
    documentation: str | None = None,
    fixed=None,
    pattern=None,
    constraints=None,
    default_value=None,
    path: str | None = None,
):
    node = MagicMock()
    node.name = name
    node.path = path or f"Resource.{name}"

    node.types = (
        list(types) if types else [make_type_definition(code) for code in type_codes]
    )
    node.is_array = is_array
    node.min_cardinality = min_cardinality
    node.max_cardinality = max_cardinality
    node.documentation = documentation
    node.fixed = fixed
    node.pattern = pattern
    node.default_value = default_value
    node.definition.constraint = constraints or []
    node.max_length = None
    node.min_value = None
    node.max_value = None
    return node


def make_type_info(
    python_type, kind: str = "complex-type", requires_primitive_extension: bool = False
):
    return TypeInformation(
        type=python_type,
        kind=kind,
        requires_primitive_extension=requires_primitive_extension,
    )


@pytest.fixture
def index():
    return MagicMock(name="mock-index")


@pytest.fixture
def builder() -> SimpleFieldBuilder:
    ctx = MagicMock(name="mock-build-context")
    ctx.fhir_release = "R4"
    return SimpleFieldBuilder(context=ctx)


# ===========================================================================
# SimpleFieldBuilder.can_handle
# ===========================================================================


def test_can_handle_returns_correct_value(builder):
    assert builder.can_handle(MagicMock(), MagicMock()) is True


# ===========================================================================
# SimpleFieldBuilder.build
# ===========================================================================


def test_build__returns_build_instance(builder: Builder, index):
    node = make_node("status", type_codes=["string"])
    result = builder.build(node, index)
    assert isinstance(result, Build)


def test_build__raises_when_no_types(builder: Builder, index):
    node = make_node("value", type_codes=[])
    with pytest.raises(TypeResolutionError, match="value"):
        builder.build(node, index)


def test_build__error_message_contains_node_path(builder: Builder, index):
    node = make_node("value", type_codes=[], path="Observation.value")
    with pytest.raises(TypeResolutionError, match="Observation.value"):
        builder.build(node, index)


def test_build__single_complex_type_produces_one_field(builder: Builder, index):
    node = make_node("code", type_codes=["CodeableConcept"])
    build = builder.build(node, index)
    assert len(build.fields) == 1


def test_build__single_resource_type_produces_one_field(builder: Builder, index):
    node = make_node("subject", type_codes=["Patient"])
    build = builder.build(node, index)
    assert len(build.fields) == 1


def test_build__no_ext_placeholder_for_complex_type(builder: Builder, index):
    node = make_node("code", type_codes=["CodeableConcept"])
    build = builder.build(node, index)
    names = [f.name for f in build.fields]
    assert "code_ext" not in names


def test_build__primitive_type_produces_two_fields(builder: Builder, index):
    node = make_node("status", type_codes=["string"])
    build = builder.build(node, index)
    assert len(build.fields) == 2


def test_build__primitive_placeholder_field_name(builder: Builder, index):
    node = make_node("status", type_codes=["string"])
    build = builder.build(node, index)
    names = [f.name for f in build.fields]
    assert "status_ext" in names


def test_build__primitive_placeholder_does_not_set_default(builder: Builder, index):
    node = make_node("status", type_codes=["string"], default_value="active")
    build = builder.build(node, index)
    placeholder = next((f for f in build.fields if f.name == "status_ext"), None)
    assert placeholder is not None
    assert placeholder.default is None


def test_build__primitive_placeholder_alias_is_underscore_name(builder: Builder, index):
    node = make_node("status", type_codes=["string"])
    build = builder.build(node, index)
    placeholder = next(f for f in build.fields if f.name == "status_ext")
    assert placeholder.alias == "_status"


def test_build__primitive_main_field_comes_first(builder: Builder, index):
    node = make_node("status", type_codes=["string"])
    build = builder.build(node, index)
    assert build.fields[0].name == "status"
    assert build.fields[1].name == "status_ext"


@pytest.mark.parametrize(
    "keyword_name, safe_name",
    [
        ("class", "class_"),
        ("for", "for_"),
        ("import", "import_"),
    ],
)
def test_build__python_keyword_name_is_made_safe(
    builder: Builder, index, keyword_name, safe_name
):
    node = make_node(keyword_name, type_codes=["string"])
    build = builder.build(node, index)
    assert build.fields[0].name == safe_name


@pytest.mark.parametrize("keyword_name", ["class", "for", "import"])
def test_build__python_keyword_field_has_validation_alias(
    builder: Builder, index, keyword_name
):
    node = make_node(keyword_name, type_codes=["string"])
    build = builder.build(node, index)
    assert isinstance(build.fields[0].validation_alias, AliasChoices)


def test_build__normal_name_has_no_validation_alias(builder: Builder, index):
    node = make_node("status", type_codes=["string"])
    build = builder.build(node, index)
    assert build.fields[0].validation_alias is None


def test_build__non_array_annotation_is_optional(builder: Builder, index):
    node = make_node("status", type_codes=["CodeableConcept"], is_array=False)
    ti = make_type_info(r4_complex.CodeableConcept, "complex-type", False)
    with patch.object(builder, "resolve_type", return_value=ti):
        result = builder.build(node, index)
    assert result.fields[0].annotation == Optional[r4_complex.CodeableConcept]


def test_build__array_annotation_is_optional_list(builder: Builder, index):
    node = make_node("name", type_codes=["HumanName"], is_array=True)
    result = builder.build(node, index)
    assert result.fields[0].annotation == Optional[List[r4_complex.HumanName]]


def test_build__two_types_annotation_contains_both_types(builder: Builder, index):
    node = make_node("name", type_codes=["Quantity", "string"])
    build = builder.build(node, index)
    inner = get_args(build.fields[0].annotation)  # unwrap Optional
    union_args = set()
    for arg in inner:
        union_args.update(get_args(arg) or [arg])
    assert r4_complex.Quantity in union_args
    assert primitives.String in union_args


def test_build__two_types_one_primitive_adds_placeholder(builder: Builder, index):
    """When any resolved type requires_primitive_extension, a placeholder is added."""
    node = make_node("value", type_codes=["Quantity", "string"])
    build = builder.build(node, index)
    assert len(build.fields) == 2
    assert build.fields[1].name == "value_ext"


def test_build__two_types_neither_primitive_no_placeholder(builder: Builder, index):
    node = make_node("value", type_codes=["CodeableConcept", "Quantity"])
    build = builder.build(node, index)
    assert len(build.fields) == 1


def test_build__validators_list_populated_from_build_field_validators(
    builder: Builder, index
):
    node = make_node("status", type_codes=["code"], fixed="active")
    build = builder.build(node, index)
    assert len(build.validators) > 0


def test_build__no_validators_when_nothing_set(builder: Builder, index):
    node = make_node("status", type_codes=["code"])
    build = builder.build(node, index)
    assert build.validators == []


def test_build__fixed_value_produces_validator(builder: Builder, index):
    node = make_node("status", type_codes=["code"], fixed="active")
    build = builder.build(node, index)
    names = [v.name for v in build.validators]
    assert "FHIR_status_fixed_value_constraint" in names


def test_build__pattern_value_produces_validator(builder: Builder, index):
    node = make_node(
        "code", type_codes=["Coding"], pattern={"system": "http://loinc.org"}
    )
    build = builder.build(node, index)
    names = [v.name for v in build.validators]
    assert "FHIR_code_pattern_constraint" in names


def test_build__validator_uses_safe_name_for_python_keyword_field(
    builder: Builder, index
):
    node = make_node("class", type_codes=["code"], fixed="active")
    build = builder.build(node, index)
    names = [v.name for v in build.validators]
    assert "FHIR_class__fixed_value_constraint" in names


def test_build__constraint_produces_model_validator(builder: Builder, index):
    constraint = MagicMock()
    constraint.key = "obs-6"
    constraint.expression = "value.empty() or component.empty()"
    constraint.human = (
        "dataAbsentReason SHALL only be present if Observation.value[x] is not present"
    )
    constraint.severity = "error"
    node = make_node("value", type_codes=["string"], constraints=[constraint])
    build = builder.build(node, index)
    kinds = [v.kind for v in build.validators]
    assert "model" in kinds
