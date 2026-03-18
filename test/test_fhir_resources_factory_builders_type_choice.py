from typing import List, Optional
from unittest.mock import MagicMock, patch

import pytest

from fhircraft.fhir.resources.datatypes import primitives
from fhircraft.fhir.resources.datatypes.R4 import complex as r4_complex
from fhircraft.fhir.resources.factory.builders.base import (
    Build,
    TypeInformation,
    ValidatorInformation,
)
from fhircraft.fhir.resources.factory.builders.type_choice import TypeChoiceFieldBuilder
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
    is_polymorphic: bool = True,
    is_required: bool = False,
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
    node.path = path or f"Resource.{name}[x]"
    node.types = (
        list(types) if types else [make_type_definition(code) for code in type_codes]
    )
    node.is_polymorphic_type = is_polymorphic
    node.is_required = is_required
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
def builder() -> TypeChoiceFieldBuilder:
    ctx = MagicMock(name="mock-build-context")
    ctx.fhir_release = "R4"
    return TypeChoiceFieldBuilder(context=ctx)


# ===========================================================================
# TypeChoiceFieldBuilder.can_handle
# ===========================================================================


def test_can_handle__returns_true_when_node_is_polymorphic(builder, index):
    node = make_node("value", type_codes=["string"], is_polymorphic=True)
    assert builder.can_handle(node, index) is True


def test_can_handle__returns_false_when_node_is_not_polymorphic(builder, index):
    node = make_node("value", type_codes=["string"], is_polymorphic=False)
    assert builder.can_handle(node, index) is False


# ===========================================================================
# TypeChoiceFieldBuilder.build — return type & basic contract
# ===========================================================================


def test_build__returns_build_instance(builder, index):
    node = make_node("value", type_codes=["string"])
    result = builder.build(node, index)
    assert isinstance(result, Build)


def test_build__raises_when_no_types(builder, index):
    node = make_node("value", type_codes=[])
    with pytest.raises(TypeResolutionError):
        builder.build(node, index)


def test_build__error_message_contains_node_path(builder, index):
    node = make_node("value", type_codes=[], path="Observation.value[x]")
    with pytest.raises(TypeResolutionError, match="Observation.value"):
        builder.build(node, index)


# ===========================================================================
# Field production — one field per resolved type
# ===========================================================================


def test_build__single_type_produces_one_field(builder, index):
    node = make_node("value", type_codes=["Quantity"])
    result = builder.build(node, index)
    assert len(result.fields) == 1


def test_build__two_types_produce_two_fields(builder, index):
    node = make_node("value", type_codes=["Coding", "Quantity"])
    result = builder.build(node, index)
    # Two typed fields (no primitives, no placeholders)
    typed_fields = [f for f in result.fields if not f.name.endswith("_ext")]
    assert len(typed_fields) == 2


def test_build__three_types_produce_three_fields(builder, index):
    node = make_node("value", type_codes=["string", "Quantity", "CodeableConcept"])
    result = builder.build(node, index)
    typed_fields = [f for f in result.fields if not f.name.endswith("_ext")]
    assert len(typed_fields) == 3


def test_build__field_name_is_base_plus_type_name(builder, index):
    node = make_node("value", type_codes=["Quantity"])
    ti = make_type_info(r4_complex.Quantity, "complex-type", False)
    with patch.object(builder, "resolve_type", return_value=ti):
        result = builder.build(node, index)
    assert result.fields[0].name == "valueQuantity"


def test_build__string_type_field_name(builder, index):
    node = make_node("value", type_codes=["string"])
    result = builder.build(node, index)
    assert result.fields[0].name == "valueString"


def test_build__boolean_type_field_name(builder, index):
    node = make_node("value", type_codes=["boolean"])
    result = builder.build(node, index)
    assert result.fields[0].name == "valueBoolean"


def test_build__two_types_field_names_reflect_their_types(builder, index):
    node = make_node("value", type_codes=["string", "Quantity"])
    result = builder.build(node, index)
    names = {f.name for f in result.fields if not f.name.endswith("_ext")}
    assert "valueString" in names
    assert "valueQuantity" in names


def test_build__different_base_name_used_in_field(builder, index):
    node = make_node("effective", type_codes=["dateTime"])
    result = builder.build(node, index)
    names = [f.name for f in result.fields if not f.name.endswith("_ext")]
    assert "effectiveDateTime" in names


def test_build__non_keyword_typed_name_has_no_validation_alias(builder, index):
    node = make_node("value", type_codes=["Quantity"])
    ti = make_type_info(r4_complex.Quantity, "complex-type", False)
    with patch.object(builder, "resolve_type", return_value=ti):
        result = builder.build(node, index)
    assert result.fields[0].validation_alias is None


def test_build__non_array_typed_field_annotation_is_optional(builder, index):
    node = make_node("value", type_codes=["Quantity"], is_array=False)
    ti = make_type_info(r4_complex.Quantity, "complex-type", False)
    with patch.object(builder, "resolve_type", return_value=ti):
        result = builder.build(node, index)
    assert result.fields[0].annotation == Optional[r4_complex.Quantity]


def test_build__array_typed_field_annotation_is_optional_list(builder, index):
    node = make_node("value", type_codes=["Quantity"], is_array=True)
    ti = make_type_info(r4_complex.Quantity, "complex-type", False)
    with patch.object(builder, "resolve_type", return_value=ti):
        result = builder.build(node, index)
    assert result.fields[0].annotation == Optional[List[r4_complex.Quantity]]


def test_build__primitive_type_adds_ext_placeholder(builder, index):
    node = make_node("value", type_codes=["string"])
    result = builder.build(node, index)
    names = [f.name for f in result.fields]
    assert "value_ext" in names


def test_build__non_primitive_type_does_not_add_placeholder(builder, index):
    node = make_node("value", type_codes=["Quantity"])
    ti = make_type_info(r4_complex.Quantity, "complex-type", False)
    with patch.object(builder, "resolve_type", return_value=ti):
        result = builder.build(node, index)
    names = [f.name for f in result.fields]
    assert "value_ext" not in names


def test_build__primitive_placeholder_alias_is_underscore_name(builder, index):
    node = make_node("value", type_codes=["string"])
    result = builder.build(node, index)
    placeholder = next(f for f in result.fields if f.name == "value_ext")
    assert placeholder.alias == "_value"


def test_build__two_types_one_primitive_adds_exactly_one_placeholder(builder, index):
    node = make_node("value", type_codes=["string", "Quantity"])
    result = builder.build(node, index)
    ext_fields = [f for f in result.fields if f.name.endswith("_ext")]
    assert len(ext_fields) == 1


def test_build__two_primitive_types_add_two_placeholders(builder, index):
    node = make_node("value", type_codes=["string", "boolean"])
    result = builder.build(node, index)
    ext_fields = [f for f in result.fields if f.name.endswith("_ext")]
    assert len(ext_fields) == 2


def test_build__type_choice_validator_added(builder, index):
    node = make_node("value", type_codes=["string"])
    result = builder.build(node, index)
    names = [v.name for v in result.validators]
    assert "value_type_choice_validator" in names


def test_build__type_choice_validator_is_model_kind(builder, index):
    node = make_node("value", type_codes=["string"])
    result = builder.build(node, index)
    validator = next(
        v for v in result.validators if v.name == "value_type_choice_validator"
    )
    assert validator.kind == "model"


def test_build__type_choice_validator_name_uses_base_name(builder, index):
    node = make_node("effective", type_codes=["dateTime"])
    result = builder.build(node, index)
    names = [v.name for v in result.validators]
    assert "effective_type_choice_validator" in names


def test_build__type_choice_validator_arguments_contain_field_name_base(builder, index):
    node = make_node("value", type_codes=["string"])
    result = builder.build(node, index)
    validator = next(
        v for v in result.validators if v.name == "value_type_choice_validator"
    )
    assert validator.arguments["field_name_base"] == "value"


def test_build__type_choice_validator_arguments_contain_field_types(builder, index):
    node = make_node("value", type_codes=["string"])
    result = builder.build(node, index)
    validator = next(
        v for v in result.validators if v.name == "value_type_choice_validator"
    )
    assert "field_types" in validator.arguments
    assert len(validator.arguments["field_types"]) == 1


def test_build__type_choice_validator_field_types_contain_all_resolved_types(
    builder, index
):
    node = make_node("value", type_codes=["string", "Quantity"])
    ti1 = make_type_info(primitives.String, "primitive", True)
    ti2 = make_type_info(r4_complex.Quantity, "complex-type", False)
    with patch.object(builder, "resolve_type", side_effect=[ti1, ti2]):
        result = builder.build(node, index)
    validator = next(
        v for v in result.validators if v.name == "value_type_choice_validator"
    )
    assert primitives.String in validator.arguments["field_types"]
    assert r4_complex.Quantity in validator.arguments["field_types"]


def test_build__type_choice_validator_required_false_by_default(builder, index):
    node = make_node("value", type_codes=["string"], is_required=False)
    result = builder.build(node, index)
    validator = next(
        v for v in result.validators if v.name == "value_type_choice_validator"
    )
    assert validator.arguments["required"] is False


def test_build__type_choice_validator_required_true_when_node_is_required(
    builder, index
):
    node = make_node("value", type_codes=["string"], is_required=True)
    result = builder.build(node, index)
    validator = next(
        v for v in result.validators if v.name == "value_type_choice_validator"
    )
    assert validator.arguments["required"] is True


def test_build__type_choice_validator_is_valid_validator_information(builder, index):
    node = make_node("value", type_codes=["string"])
    result = builder.build(node, index)
    validator = next(
        v for v in result.validators if v.name == "value_type_choice_validator"
    )
    assert isinstance(validator, ValidatorInformation)


def test_build__property_added_for_base_name(builder, index):
    node = make_node("value", type_codes=["string"])
    result = builder.build(node, index)
    assert "value" in result.properties


def test_build__property_is_callable(builder, index):
    node = make_node("value", type_codes=["string"])
    result = builder.build(node, index)
    assert callable(result.properties["value"])


def test_build__property_key_matches_base_name(builder, index):
    node = make_node("effective", type_codes=["dateTime"])
    result = builder.build(node, index)
    assert "effective" in result.properties


def test_build__fixed_value_on_typed_field_produces_fixed_validator(builder, index):
    node = make_node("value", type_codes=["string"], fixed="active")
    result = builder.build(node, index)
    names = [v.name for v in result.validators]
    assert any("fixed_value_constraint" in n for n in names)


def test_build__pattern_on_typed_field_produces_pattern_validator(builder, index):
    node = make_node(
        "value", type_codes=["Coding"], pattern={"system": "http://loinc.org"}
    )
    ti = make_type_info(r4_complex.Coding, "complex-type", False)
    with patch.object(builder, "resolve_type", return_value=ti):
        result = builder.build(node, index)
    names = [v.name for v in result.validators]
    assert any("pattern_constraint" in n for n in names)


def test_build__constraint_on_node_produces_model_validator(builder, index):
    constraint = MagicMock()
    constraint.key = "obs-7"
    constraint.expression = "value.exists()"
    constraint.human = "value must exist"
    constraint.severity = "error"
    node = make_node("value", type_codes=["string"], constraints=[constraint])
    result = builder.build(node, index)
    kinds = [v.kind for v in result.validators]
    assert "model" in kinds


def test_build__no_extra_validators_when_nothing_set(builder, index):
    node = make_node("value", type_codes=["Quantity"])
    ti = make_type_info(r4_complex.Quantity, "complex-type", False)
    with patch.object(builder, "resolve_type", return_value=ti):
        result = builder.build(node, index)
    # Only the type-choice validator should be present
    assert len(result.validators) == 1
    assert result.validators[0].name == "value_type_choice_validator"
