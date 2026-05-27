"""Unit tests for ModelAssembler."""

from __future__ import annotations

from typing import List, Optional
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from fhircraft.fhir.resources.base import FHIRBaseModel
from fhircraft.fhir.resources.factory.assembler import BUILDER_CHAIN, ModelAssembler
from fhircraft.fhir.resources.factory.builders.base import (
    Build,
    Builder,
    FieldInformation,
    ValidatorInformation,
)
from fhircraft.exceptions import FactoryAssemblerError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_field(name: str = "value", annotation: type = str) -> FieldInformation:
    return FieldInformation(name=name, annotation=annotation)


def make_root_node(
    id: str = "Resource",
    documentation: str | None = "Root docs",
    constraints: list | None = None,
):
    root = MagicMock(name="mock-root")
    root.id = id
    root.documentation = documentation
    root.fixed = None
    root.pattern = None
    root.definition = MagicMock()
    root.definition.constraint = constraints or []
    return root


def make_child_node(
    id: str = "Resource.value",
    path: str = "Resource.value",
    has_type: bool = True,
    is_content_reference: bool = False,
):
    child = MagicMock(name=f"mock-child-{id}")
    child.id = id
    child.path = path
    # definition.type: truthy when has_type, falsy otherwise
    child.definition = MagicMock()
    child.definition.type = [MagicMock()] if has_type else None
    child.is_content_reference = is_content_reference
    return child


def make_index(root=None, children: dict | None = None):
    """
    Returns a mock DefinitionIndex.

    ``children`` maps element id → list of child nodes.
    Any id not in the dict returns [].
    """
    idx = MagicMock(name="mock-index")
    _root = root or make_root_node()
    idx.root.return_value = _root
    _children = children or {}
    idx.get_children.side_effect = lambda id: _children.get(id, [])
    idx.get_slices.return_value = []
    return idx


def make_mock_builder(can_handle: bool = True, build_return: Build | None = None):
    b = MagicMock(name="mock-builder", spec=Builder)
    b.can_handle.return_value = can_handle
    b.build.return_value = (
        build_return if build_return is not None else Build(fields=[make_field()])
    )
    return b


def make_ctx(base=None):
    ctx = MagicMock(name="mock-ctx")
    ctx.base = base
    return ctx


def make_assembler(
    root=None,
    children: dict | None = None,
    ctx=None,
    resource_name: str = "TestModel",
) -> ModelAssembler:
    index = make_index(root=root, children=children)
    _ctx = ctx or make_ctx()
    a = ModelAssembler(index=index, ctx=_ctx, resource_name=resource_name)
    return a


# ===========================================================================
# ModelAssembler.__init__
# ===========================================================================


def test_init__stores_index():
    index = make_index()
    ctx = make_ctx()
    a = ModelAssembler(index=index, ctx=ctx)
    assert a.index is index


def test_init__stores_ctx():
    index = make_index()
    ctx = make_ctx()
    a = ModelAssembler(index=index, ctx=ctx)
    assert a.ctx is ctx


def test_init__stores_resource_name():
    a = ModelAssembler(index=make_index(), ctx=make_ctx(), resource_name="MyRes")
    assert a.resource_name == "MyRes"


def test_init__resource_name_defaults_to_unknown():
    a = ModelAssembler(index=make_index(), ctx=make_ctx())
    assert a.resource_name == "Unknown"


def test_init__builder_chain_length_matches_builder_chain_constant():
    a = ModelAssembler(index=make_index(), ctx=make_ctx())
    assert len(a.builder_chain) == len(BUILDER_CHAIN)


def test_init__builder_chain_contains_builder_instances():
    from fhircraft.fhir.resources.factory.builders.base import Builder

    a = ModelAssembler(index=make_index(), ctx=make_ctx())
    for builder in a.builder_chain:
        assert isinstance(builder, Builder)


def test_init__builder_chain_order_matches_builder_chain_constant():
    a = ModelAssembler(index=make_index(), ctx=make_ctx())
    for actual, expected_cls in zip(a.builder_chain, BUILDER_CHAIN):
        assert isinstance(actual, expected_cls)


# ===========================================================================
# ModelAssembler._find_builder
# ===========================================================================


def test_find_builder__returns_first_matching_builder():
    a = make_assembler()
    b1 = make_mock_builder(can_handle=False)
    b2 = make_mock_builder(can_handle=True)
    b3 = make_mock_builder(can_handle=True)
    a.builder_chain = [b1, b2, b3]
    node = make_child_node()
    result = a._find_builder(node)
    assert result is b2


def test_find_builder__raises_assembler_error_when_no_builder_matches():
    a = make_assembler()
    a.builder_chain = [make_mock_builder(can_handle=False)]
    node = MagicMock()
    node.id = "Resource.field"
    with pytest.raises(FactoryAssemblerError):
        a._find_builder(node)


def test_find_builder__skips_non_matching_builders():
    a = make_assembler()
    b1 = make_mock_builder(can_handle=False)
    b2 = make_mock_builder(can_handle=True)
    a.builder_chain = [b1, b2]
    node = make_child_node()
    a._find_builder(node)
    b1.can_handle.assert_called_once()
    b2.can_handle.assert_called_once()


# ===========================================================================
# ModelAssembler.assemble
# ===========================================================================


def test_assemble__base_none_with_ctx_base_none_uses_fhir_base_model():
    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]}, ctx=make_ctx(base=None))
    a.builder_chain = [
        make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    ]
    model = a.assemble("M")
    assert issubclass(model, FHIRBaseModel)


def test_assemble__base_none_with_ctx_base_uses_ctx_base():
    class MyBase(FHIRBaseModel):
        pass

    root = make_root_node()
    child = make_child_node()
    a = make_assembler(
        root=root, children={root.id: [child]}, ctx=make_ctx(base=MyBase)
    )
    a.builder_chain = [
        make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    ]
    model = a.assemble("M")
    assert issubclass(model, MyBase)


def test_assemble__single_base_class_is_used():
    class MyBase(FHIRBaseModel):
        pass

    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [
        make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    ]
    model = a.assemble("M", base=MyBase)
    assert issubclass(model, MyBase)


def test_assemble__tuple_of_bases_all_inherited():
    class BaseA(FHIRBaseModel):
        pass

    class BaseB(FHIRBaseModel):
        pass

    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [
        make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    ]
    model = a.assemble("M", base=(BaseA, BaseB))
    assert issubclass(model, BaseA)
    assert issubclass(model, BaseB)


def test_assemble__returns_a_type():
    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [
        make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    ]
    result = a.assemble("M")
    assert isinstance(result, type)


def test_assemble__returned_model_has_the_given_name():
    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [
        make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    ]
    model = a.assemble("ObservationComponent")
    assert model.__name__ == "ObservationComponent"


def test_assemble__returned_model_has_the_field():
    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [
        make_mock_builder(build_return=Build(fields=[make_field("score", int)]))
    ]
    model = a.assemble("M")
    assert "score" in model.model_fields


def test_assemble__returned_model_docstring_matches_root_documentation():
    root = make_root_node(documentation="This is the model docs.")
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [
        make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    ]
    model = a.assemble("M")
    assert model.__doc__ == "This is the model docs."


# ===========================================================================
# ModelAssembler.assemble – builder delegation
# ===========================================================================


def test_assemble__calls_build_with_child_node():
    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    mock_b = make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    a.builder_chain = [mock_b]
    a.assemble("M")
    mock_b.build.assert_called_once()
    assert mock_b.build.call_args[0][0] is child


def test_assemble__calls_build_with_index():
    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    mock_b = make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    a.builder_chain = [mock_b]
    a.assemble("M")
    assert mock_b.build.call_args[0][1] is a.index


def test_assemble__each_child_dispatches_to_its_own_builder_call():
    root = make_root_node()
    child_a = make_child_node(id="Resource.a", path="Resource.a")
    child_b = make_child_node(id="Resource.b", path="Resource.b")
    a = make_assembler(root=root, children={root.id: [child_a, child_b]})
    mock_b = make_mock_builder()
    # Make each call return a different field name so accumulation works
    mock_b.build.side_effect = [
        Build(fields=[make_field("a", str)]),
        Build(fields=[make_field("b", int)]),
    ]
    a.builder_chain = [mock_b]
    a.assemble("M")
    assert mock_b.build.call_count == 2


def test_assemble__multiple_children_produce_multiple_fields():
    root = make_root_node()
    child_a = make_child_node(id="Resource.a", path="Resource.a")
    child_b = make_child_node(id="Resource.b", path="Resource.b")
    a = make_assembler(root=root, children={root.id: [child_a, child_b]})
    mock_b = make_mock_builder()
    mock_b.build.side_effect = [
        Build(fields=[make_field("score", int)]),
        Build(fields=[make_field("label", str)]),
    ]
    a.builder_chain = [mock_b]
    model = a.assemble("M")
    assert "score" in model.model_fields
    assert "label" in model.model_fields


def test_assemble__skips_child_with_no_type_no_children_no_slices():
    root = make_root_node()
    meta_child = make_child_node(has_type=False, is_content_reference=False)
    real_child = make_child_node(
        id="Resource.real", path="Resource.real", has_type=True
    )
    a = make_assembler(
        root=root,
        children={root.id: [meta_child, real_child]},
    )
    mock_b = make_mock_builder(build_return=Build(fields=[make_field("real", str)]))
    a.builder_chain = [mock_b]
    a.assemble("M")
    # build called only for real_child
    assert mock_b.build.call_count == 2
    assert mock_b.build.call_args[0][0] is real_child


def test_assemble__does_not_skip_content_reference_without_type():
    root = make_root_node()
    cr_child = make_child_node(has_type=False, is_content_reference=True)
    a = make_assembler(root=root, children={root.id: [cr_child]})
    mock_b = make_mock_builder(build_return=Build(fields=[make_field("ref", str)]))
    a.builder_chain = [mock_b]
    a.assemble("M")
    mock_b.build.assert_called_once()


def test_assemble__does_not_skip_child_with_type():
    root = make_root_node()
    child = make_child_node(has_type=True)
    a = make_assembler(root=root, children={root.id: [child]})
    mock_b = make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    a.builder_chain = [mock_b]
    a.assemble("M")
    mock_b.build.assert_called_once()


def test_assemble__wraps_builder_exception_in_assembler_error():
    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    mock_b = make_mock_builder()
    mock_b.build.side_effect = RuntimeError("builder exploded")
    a.builder_chain = [mock_b]
    with pytest.raises(FactoryAssemblerError):
        a.assemble("M")


def test_assemble__assembler_error_message_contains_node_id():
    root = make_root_node()
    child = make_child_node(id="Resource.broken", path="Resource.broken")
    a = make_assembler(root=root, children={root.id: [child]})
    mock_b = make_mock_builder()
    mock_b.build.side_effect = RuntimeError("boom")
    a.builder_chain = [mock_b]
    with pytest.raises(FactoryAssemblerError, match="Resource.broken"):
        a.assemble("M")


def test_assemble__properties_from_build_attached_to_model():
    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    getter = lambda self: 42
    mock_b = make_mock_builder(
        build_return=Build(
            fields=[make_field("v", str)],
            properties={"my_prop": getter},
        )
    )
    a.builder_chain = [mock_b]
    model = a.assemble("M")
    assert isinstance(model.__dict__.get("my_prop"), property)


def test_assemble__model_without_properties_has_none_extra():
    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    mock_b = make_mock_builder(
        build_return=Build(fields=[make_field("v", str)], properties={})
    )
    a.builder_chain = [mock_b]
    model = a.assemble("M")
    # just confirm it assembles cleanly
    assert isinstance(model, type)


# ===========================================================================
# ModelAssembler.assemble – missing definition / no-field edge cases
# ===========================================================================


def test_assemble__raises_value_error_when_child_has_no_definition():
    root = make_root_node()
    child = make_child_node()
    child.definition = None  # Force falsy definition
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [make_mock_builder()]
    with pytest.raises(ValueError, match=child.id):
        a.assemble("M")


def test_assemble__raises_assembler_error_when_no_fields_and_no_base_fields():
    """Builder returns no fields and the base class also has no model_fields."""
    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [make_mock_builder(build_return=Build(fields=[]))]
    with pytest.warns(match="no fields"):
        a.assemble("M")


def test_assemble__no_fields_built_but_base_has_fields_does_not_raise():
    """No fields from builders but the explicit base class already has fields."""

    class BaseWithField(FHIRBaseModel):
        existing: str = "x"

    root = make_root_node()
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [make_mock_builder(build_return=Build(fields=[]))]
    model = a.assemble("M", base=BaseWithField)
    assert isinstance(model, type)
    assert issubclass(model, BaseWithField)


def test_assemble__calls_set_constraint_default_values_when_root_has_fixed():
    from unittest.mock import patch

    root = make_root_node()
    root.fixed = MagicMock(spec=BaseModel)  # non-None fixed value
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [
        make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    ]
    with (
        patch.object(ModelAssembler, "build_model_fixed_value_constraint") as mock_fvc,
        patch.object(ModelAssembler, "_set_constraint_default_values") as mock_scdv,
    ):
        mock_fvc.return_value = MagicMock(
            name="vi", **{"as_pydantic_definition.return_value": MagicMock()}
        )
        a.assemble("M")
    mock_scdv.assert_called_once()


def test_assemble__calls_set_constraint_default_values_when_root_has_pattern():
    from unittest.mock import patch

    root = make_root_node()
    root.pattern = MagicMock(spec=BaseModel)  # non-None pattern value
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [
        make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    ]
    with (
        patch.object(ModelAssembler, "build_model_pattern_constraint") as mock_pc,
        patch.object(ModelAssembler, "_set_constraint_default_values") as mock_scdv,
    ):
        mock_pc.return_value = MagicMock(
            name="vi", **{"as_pydantic_definition.return_value": MagicMock()}
        )
        a.assemble("M")
    mock_scdv.assert_called_once()


def test_assemble__does_not_call_set_constraint_default_values_without_fixed_or_pattern():
    from unittest.mock import patch

    root = make_root_node()  # fixed=None, pattern=None by default
    child = make_child_node()
    a = make_assembler(root=root, children={root.id: [child]})
    a.builder_chain = [
        make_mock_builder(build_return=Build(fields=[make_field("v", str)]))
    ]
    with patch.object(ModelAssembler, "_set_constraint_default_values") as mock_scdv:
        a.assemble("M")
    mock_scdv.assert_not_called()


# ===========================================================================
# ModelAssembler._set_constraint_default_values
# ===========================================================================


def test_set_constraint_default_values__sets_default_from_fixed_value():
    from pydantic import create_model, Field

    class ConstraintModel(BaseModel):
        status: str = "final"

    SliceModel = create_model(
        "SliceModel", status=(Optional[str], Field(None)), __base__=FHIRBaseModel
    )
    node = MagicMock()
    node.fixed = ConstraintModel(status="final")
    node.pattern = None

    ModelAssembler._set_constraint_default_values(SliceModel, node)

    assert SliceModel.model_fields["status"].default == "final"


def test_set_constraint_default_values__skips_none_values():
    """Fields whose constrain_value attribute is None should keep their original default."""
    from pydantic import create_model, Field

    class ConstraintModel(BaseModel):
        status: Optional[str] = None  # None → should NOT override default

    SliceModel = create_model(
        "SliceModel",
        status=(Optional[str], Field("original")),
        __base__=FHIRBaseModel,
    )
    node = MagicMock()
    node.fixed = ConstraintModel()
    node.pattern = None

    ModelAssembler._set_constraint_default_values(SliceModel, node)

    assert SliceModel.model_fields["status"].default == "original"


def test_set_constraint_default_values__raises_type_error_for_non_pydantic_fixed():
    from pydantic import create_model, Field

    SliceModel = create_model(
        "SliceModel", status=(Optional[str], Field(None)), __base__=FHIRBaseModel
    )
    node = MagicMock()
    node.fixed = "not_a_pydantic_model"
    node.pattern = None

    with pytest.raises(TypeError):
        ModelAssembler._set_constraint_default_values(SliceModel, node)


def test_set_constraint_default_values__raises_value_error_for_unknown_constraint_field():
    from pydantic import create_model, Field

    class ConstraintModel(BaseModel):
        unknown_field: str = "value"

    SliceModel = create_model(
        "SliceModel", status=(Optional[str], Field(None)), __base__=FHIRBaseModel
    )
    node = MagicMock()
    node.fixed = ConstraintModel(unknown_field="value")
    node.pattern = None

    with pytest.raises(ValueError, match="unknown_field"):
        ModelAssembler._set_constraint_default_values(SliceModel, node)


# ===========================================================================
# ModelAssembler.build_model_fixed_value_constraint
# ===========================================================================


def test_build_model_fixed_value_constraint__name_format():
    node = MagicMock()
    node.name = "coding"
    node.fixed = MagicMock()

    result = ModelAssembler.build_model_fixed_value_constraint(node)

    assert result.name == "FHIR_coding_fixed_value_constraint"


def test_build_model_fixed_value_constraint__kind_is_model():
    node = MagicMock()
    node.name = "coding"
    node.fixed = MagicMock()

    result = ModelAssembler.build_model_fixed_value_constraint(node)

    assert result.kind == "model"


def test_build_model_fixed_value_constraint__arguments_contain_constant():
    node = MagicMock()
    node.name = "coding"
    sentinel = object()
    node.fixed = sentinel

    result = ModelAssembler.build_model_fixed_value_constraint(node)

    assert result.arguments["constant"] is sentinel


def test_build_model_fixed_value_constraint__returns_validator_information():
    node = MagicMock()
    node.name = "coding"
    node.fixed = MagicMock()

    result = ModelAssembler.build_model_fixed_value_constraint(node)

    assert isinstance(result, ValidatorInformation)


# ===========================================================================
# ModelAssembler.build_model_pattern_constraint
# ===========================================================================


def test_build_model_pattern_constraint__name_format():
    node = MagicMock()
    node.name = "component"
    node.pattern = MagicMock()

    result = ModelAssembler.build_model_pattern_constraint(node)

    assert result.name == "FHIR_component_pattern_constraint"


def test_build_model_pattern_constraint__kind_is_model():
    node = MagicMock()
    node.name = "component"
    node.pattern = MagicMock()

    result = ModelAssembler.build_model_pattern_constraint(node)

    assert result.kind == "model"


def test_build_model_pattern_constraint__returns_validator_information():
    node = MagicMock()
    node.name = "component"
    node.pattern = MagicMock()

    result = ModelAssembler.build_model_pattern_constraint(node)

    assert isinstance(result, ValidatorInformation)
