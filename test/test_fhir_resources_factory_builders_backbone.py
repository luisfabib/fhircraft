from typing import List, Optional, get_args
from unittest.mock import ANY, MagicMock

import pytest
from pydantic import BaseModel
from pydantic.aliases import AliasChoices

from fhircraft.fhir.resources.base import FHIRBaseModel
from fhircraft.fhir.resources.factory.builders.backbone import BackboneFieldBuilder
from fhircraft.fhir.resources.factory.builders.base import Build


# ---------------------------------------------------------------------------
# Helpers & fixtures
# ---------------------------------------------------------------------------


def make_type_definition(type_code: str, fhir_release: str = "R4B", profile=None):
    type_def = MagicMock(name=f"mock-type-{type_code}")
    type_def.code = type_code
    type_def._fhir_release = fhir_release
    type_def.profile = [profile] if profile else None
    return type_def


def make_node(
    name: str = "component",
    path: str | None = None,
    type_code: str = "string",
    fhir_release: str = "R4B",
    is_array: bool = False,
    min_cardinality: int = 0,
    max_cardinality: int | None = None,
    documentation: str | None = None,
    fixed=None,
    pattern=None,
    constraints=None,
    default_value=None,
    max_length=None,
    min_value=None,
    max_value=None,
):
    node = MagicMock(name="mock-node")
    node.name = name
    node.id = path or f"Resource.{name}"
    node.path = path or f"Resource.{name}"
    node.is_array = is_array
    node.min_cardinality = min_cardinality
    node.max_cardinality = max_cardinality
    node.documentation = documentation
    node.fixed = fixed
    node.pattern = pattern
    node.default_value = default_value
    node.definition.constraint = constraints or []
    node.max_length = max_length
    node.min_value = min_value
    node.max_value = max_value
    node.types = [make_type_definition(type_code, fhir_release)]
    return node


def make_index(children=None):
    index = MagicMock(name="mock-index")
    index.get_children.return_value = (
        children if children is not None else [MagicMock()]
    )
    index.get_subtree.return_value = MagicMock(name="mock-subtree")
    return index


def make_builder(fhir_release: str = "R4B", base=None) -> BackboneFieldBuilder:
    ctx = MagicMock(name="mock-build-context")
    ctx.fhir_release = fhir_release
    ctx.base = base
    return BackboneFieldBuilder(context=ctx)


@pytest.fixture
def builder() -> BackboneFieldBuilder:
    # context.base=None so build() goes through resolve_type → FHIRBaseModel fallback
    return make_builder(base=None)


@pytest.fixture
def index():
    return make_index()


# A minimal FHIRBaseModel subclass used as the assembler's return value
class FakeBackboneModel(FHIRBaseModel):
    pass


@pytest.fixture
def mock_assembler(monkeypatch):
    """Patches ModelAssembler for every test; default assemble() returns FakeBackboneModel."""
    mock = MagicMock(name="MockAssembler")
    mock.return_value.assemble.return_value = FakeBackboneModel
    monkeypatch.setattr(
        "fhircraft.fhir.resources.factory.assembler.ModelAssembler", mock
    )
    return mock


# ===========================================================================
# BackboneFieldBuilder.can_handle
# ===========================================================================


def test_can_handle__returns_true_when_index_has_children(builder, index):
    node = make_node()
    index.get_children.return_value = [MagicMock()]
    assert builder.can_handle(node, index) is True


def test_can_handle__returns_false_when_index_has_no_children(builder, index):
    node = make_node()
    index.get_children.return_value = []
    assert builder.can_handle(node, index) is False


def test_can_handle__queries_index_with_node_id(builder, index):
    node = make_node(path="Observation.component")
    builder.can_handle(node, index)
    index.get_children.assert_called_with("Observation.component")


# ===========================================================================
# BackboneFieldBuilder.build
# ===========================================================================


def test_build__returns_build_instance(builder, index, mock_assembler):
    node = make_node()
    result = builder.build(node, index)
    assert isinstance(result, Build)
    assert mock_assembler.return_value.assemble.called


def test_build__result_has_exactly_one_field(builder, index, mock_assembler):
    node = make_node()
    result = builder.build(node, index)
    assert len(result.fields) == 1
    assert mock_assembler.return_value.assemble.called


def test_build__field_name_matches_node_name(builder, index, mock_assembler):
    node = make_node(name="component")
    result = builder.build(node, index)
    assert result.fields[0].name == "component"
    assert mock_assembler.return_value.assemble.called


def test_build__field_annotation_is_assembled_model(builder, index, mock_assembler):
    node = make_node()
    result = builder.build(node, index)
    assert get_args(result.fields[0].annotation)[0] is FakeBackboneModel
    assert mock_assembler.return_value.assemble.called


def test_build__validators_list_is_populated(builder, index, mock_assembler):
    node = make_node(name="component", path="Resource.component")
    result = builder.build(node, index)
    assert isinstance(result.validators, list)
    assert mock_assembler.return_value.assemble.called


def test_build__raises_type_error_when_assembler_returns_none(
    builder, index, mock_assembler
):
    mock_assembler.return_value.assemble.return_value = None
    node = make_node()
    with pytest.raises(TypeError):
        builder.build(node, index)


def test_build__backbone_name_uses_base_name_and_single_path_part(
    builder, index, mock_assembler
):
    node = make_node(name="component", path="Observation.component")
    builder.build(node, index)
    called_name = mock_assembler.return_value.assemble.call_args[0][0]
    assert called_name == "FHIRBaseModelComponent"


def test_build__backbone_name_capitalises_multiple_path_parts(
    builder, index, mock_assembler
):
    node = make_node(name="value", path="Observation.component.value")
    builder.build(node, index)
    called_name = mock_assembler.return_value.assemble.call_args[0][0]
    assert called_name == "FHIRBaseModelComponentValue"


def test_build__backbone_name_strips_type_choice_marker(builder, index, mock_assembler):
    node = make_node(name="value", path="Observation.value[x]")
    builder.build(node, index)
    called_name = mock_assembler.return_value.assemble.call_args[0][0]
    # [x] is stripped before capitalisation
    assert called_name == "FHIRBaseModelValue"


def test_build__assembler_constructed_with_subtree(builder, index, mock_assembler):
    node = make_node()
    subtree = MagicMock(name="subtree")
    index.get_subtree.return_value = subtree
    builder.build(node, index)
    assert mock_assembler.call_args.kwargs["index"] is subtree


def test_build__assembler_constructed_with_builder_context(
    builder, index, mock_assembler
):
    node = make_node()
    builder.build(node, index)
    assert mock_assembler.call_args.kwargs["ctx"] is builder.context


def test_build__get_subtree_called_with_node_id(builder, index, mock_assembler):
    node = make_node(path="Observation.component")
    builder.build(node, index)
    index.get_subtree.assert_called_with("Observation.component")


def test_build__assembler_assemble_called_with_backbone_name(
    builder, index, mock_assembler
):
    node = make_node(name="component", path="Observation.component")
    builder.build(node, index)
    called_name = mock_assembler.return_value.assemble.call_args[0][0]
    assert called_name == "FHIRBaseModelComponent"


def test_build__backbone_base_is_fhir_base_model_when_context_base_is_none(
    index, mock_assembler: MagicMock
):
    builder = make_builder(base=None)
    node = make_node()
    builder.build(node, index)
    assert mock_assembler.return_value.assemble.call_args.kwargs["base"] == (
        FHIRBaseModel,
    )


def test_build__backbone_base_resolved_from_context_base_model_fields(
    index, mock_assembler
):
    class InnerModel(BaseModel):
        pass

    class ParentModel(BaseModel):
        component: Optional[InnerModel] = None

    builder = make_builder(base=ParentModel)
    node = make_node(name="component", path="ParentModel.component")
    builder.build(node, index)
    assert mock_assembler.return_value.assemble.call_args.kwargs["base"] == (
        InnerModel,
    )


def test_build__backbone_base_digs_through_optional_list(index, mock_assembler):
    class InnerModel(BaseModel):
        pass

    class ParentModel(BaseModel):
        component: Optional[List[InnerModel]] = None

    builder = make_builder(base=ParentModel)
    node = make_node(name="component", path="ParentModel.component")
    builder.build(node, index)
    assert mock_assembler.return_value.assemble.call_args.kwargs["base"] == (
        InnerModel,
    )


def test_build__backbone_base_is_fhir_base_model_when_field_not_in_context_base(
    index, mock_assembler
):
    class ParentModel(BaseModel):
        pass  # no "component" field

    builder = make_builder(base=ParentModel)
    node = make_node(name="component", path="ParentModel.component")
    builder.build(node, index)
    assert mock_assembler.return_value.assemble.call_args.kwargs["base"] == (
        FHIRBaseModel,
    )


def test_build__python_keyword_field_receives_validation_alias(
    index, mock_assembler, monkeypatch
):
    builder = make_builder(base=None)
    node = make_node(name="component")
    alias = AliasChoices("component")

    monkeypatch.setattr(
        builder,
        "handle_python_keyword",
        lambda name: ("component_", alias),
    )
    result = builder.build(node, index)
    assert result.fields[0].validation_alias == alias
    assert mock_assembler.return_value.assemble.called


def test_build__non_keyword_field_has_no_validation_alias(
    builder, index, mock_assembler
):
    node = make_node(name="component")
    result = builder.build(node, index)
    assert result.fields[0].validation_alias is None
    assert mock_assembler.return_value.assemble.called
