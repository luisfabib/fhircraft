from unittest.mock import MagicMock, patch, call

import pytest

from fhircraft.fhir.resources.factory.builders.base import Build
from fhircraft.fhir.resources.factory.builders.content_reference import (
    ContentReferenceBuilder,
)
from fhircraft.fhir.resources.factory.exceptions import DefinitionIndexError

BACKBONEFIELDBUILDER_BUILD = "fhircraft.fhir.resources.factory.builders.content_reference.BackboneFieldBuilder.build"


# ---------------------------------------------------------------------------
# Helpers & fixtures
# ---------------------------------------------------------------------------


def make_node(
    is_content_reference: bool = True,
    content_reference: str = "#Resource.component",
):
    node = MagicMock(name="mock-node")
    node.is_content_reference = is_content_reference
    node.definition.contentReference = content_reference
    return node


def make_index(ref_node=None, ref_subtree=None):
    index = MagicMock(name="mock-index")
    index.get.return_value = ref_node if ref_node is not None else MagicMock()
    index.get_subtree.return_value = (
        ref_subtree if ref_subtree is not None else MagicMock()
    )
    return index


def make_builder(
    fhir_release: str = "R4B", fhir_version: str = "4.3.0"
) -> ContentReferenceBuilder:
    ctx = MagicMock(name="mock-build-context")
    ctx.fhir_release = fhir_release
    ctx.fhir_version = fhir_version
    return ContentReferenceBuilder(context=ctx)


@pytest.fixture
def builder() -> ContentReferenceBuilder:
    return make_builder()


@pytest.fixture
def index():
    return make_index()


# ===========================================================================
# ContentReferenceBuilder.can_handle
# ===========================================================================


def test_can_handle__returns_true_when_node_is_content_reference(builder, index):
    node = make_node(is_content_reference=True)
    assert builder.can_handle(node, index) is True


def test_can_handle__returns_false_when_node_is_not_content_reference(builder, index):
    node = make_node(is_content_reference=False)
    assert builder.can_handle(node, index) is False


# ===========================================================================
# ContentReferenceBuilder.build
# ===========================================================================


def test_build__returns_build_instance(builder, index):
    node = make_node(content_reference="#Resource.component")
    with patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()):
        result = builder.build(node, index)
    assert isinstance(result, Build)


def test_build__local_ref_with_hash_uses_passed_index(builder, index):
    node = make_node(content_reference="#Resource.component")
    with patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_bb:
        builder.build(node, index)
    index.get.assert_called()
    assert mock_bb.call_args[0][0] is node


def test_build__local_ref_without_hash_uses_passed_index(builder, index):
    node = make_node(content_reference="Resource.component")
    with patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_bb:
        builder.build(node, index)
    index.get.assert_called()
    assert mock_bb.call_args[0][0] is node


def test_build__local_ref_with_hash_queries_fragment_path(builder, index):
    node = make_node(content_reference="#Resource.component")
    with patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_bb:
        builder.build(node, index)
    index.get.assert_called_with("Resource.component")
    assert mock_bb.call_args[0][0] is node


def test_build__local_ref_without_hash_queries_full_ref(builder, index):
    node = make_node(content_reference="Resource.component")
    with patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_bb:
        builder.build(node, index)
    index.get.assert_called_with("Resource.component")
    assert mock_bb.call_args[0][0] is node


def test_build__local_ref_calls_get_subtree_with_fragment_path(builder, index):
    node = make_node(content_reference="#Resource.component")
    with patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_bb:
        builder.build(node, index)
    index.get_subtree.assert_called_with("Resource.component")
    assert mock_bb.call_args[0][0] is node


def test_build__external_ref_fetches_from_registry(builder):
    resource_url = "http://hl7.org/fhir/StructureDefinition/Observation"
    node = make_node(content_reference=f"{resource_url}#Observation.component")

    # Build a fake StructureDefinition with snapshot elements
    ref_sd = MagicMock(name="ref-sd")
    ref_sd.snapshot.element = [MagicMock()]
    builder.context.registry.get.return_value = ref_sd

    with (
        patch(
            "fhircraft.fhir.resources.factory.builders.content_reference.DefinitionIndex.from_elements"
        ) as mock_from_elements,
        patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_bb,
    ):
        mock_index = make_index()
        mock_from_elements.return_value = mock_index
        builder.build(node, MagicMock())

    builder.context.registry.get.assert_called_once_with(resource_url)
    assert mock_bb.call_args[0][0] is node


def test_build__external_ref_builds_index_from_snapshot_elements(builder):
    resource_url = "http://hl7.org/fhir/StructureDefinition/Observation"
    node = make_node(content_reference=f"{resource_url}#Observation.component")

    elements = [MagicMock(), MagicMock()]
    ref_sd = MagicMock()
    ref_sd.snapshot.element = elements
    builder.context.registry.get.return_value = ref_sd

    with (
        patch(
            "fhircraft.fhir.resources.factory.builders.content_reference.DefinitionIndex.from_elements"
        ) as mock_from_elements,
        patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_bb,
    ):
        mock_index = make_index()
        mock_from_elements.return_value = mock_index
        builder.build(node, MagicMock())

    mock_from_elements.assert_called_once_with(elements)
    assert mock_bb.call_args[0][0] is node


def test_build__external_ref_queries_fragment_path_from_external_index(builder):
    resource_url = "http://hl7.org/fhir/StructureDefinition/Observation"
    node = make_node(content_reference=f"{resource_url}#Observation.component")

    ref_sd = MagicMock()
    ref_sd.snapshot.element = [MagicMock()]
    builder.context.registry.get.return_value = ref_sd

    with (
        patch(
            "fhircraft.fhir.resources.factory.builders.content_reference.DefinitionIndex.from_elements"
        ) as mock_from_elements,
        patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_bb,
    ):
        mock_index = make_index()
        mock_from_elements.return_value = mock_index
        builder.build(node, MagicMock())

    mock_index.get.assert_called_with("Observation.component")
    assert mock_bb.call_args[0][0] is node


def test_build__raises_when_external_resource_not_found(builder):
    resource_url = "http://hl7.org/fhir/StructureDefinition/Unknown"
    node = make_node(content_reference=f"{resource_url}#Unknown.field")
    builder.context.registry.get.return_value = None

    with pytest.raises(ValueError):
        builder.build(node, MagicMock())


def test_build__raises_when_external_resource_has_no_snapshot(builder):
    resource_url = "http://hl7.org/fhir/StructureDefinition/Observation"
    node = make_node(content_reference=f"{resource_url}#Observation.component")
    ref_sd = MagicMock()
    ref_sd.snapshot = None
    builder.context.registry.get.return_value = ref_sd

    with pytest.raises(ValueError):
        builder.build(node, MagicMock())


def test_build__raises_when_external_resource_has_no_snapshot_elements(builder):
    resource_url = "http://hl7.org/fhir/StructureDefinition/Observation"
    node = make_node(content_reference=f"{resource_url}#Observation.component")
    ref_sd = MagicMock()
    ref_sd.snapshot.element = None
    builder.context.registry.get.return_value = ref_sd

    with pytest.raises(ValueError):
        builder.build(node, MagicMock())


def test_build__raises_when_ref_node_not_found(builder):
    node = make_node(content_reference="#Resource.nonexistent")
    bad_index = make_index(ref_node=None)
    bad_index.get.return_value = None

    with pytest.raises(ValueError, match="Resource.nonexistent"):
        builder.build(node, bad_index)


def test_build__error_contains_missing_ref_path(builder):
    node = make_node(content_reference="#Observation.component.interpretation")
    bad_index = make_index()
    bad_index.get.return_value = None

    with pytest.raises(ValueError, match="Observation.component.interpretation"):
        builder.build(node, bad_index)


def test_build__delegates_to_backbone_builder(builder, index):
    node = make_node(content_reference="#Resource.component")
    expected = Build()
    with patch(
        BACKBONEFIELDBUILDER_BUILD,
        return_value=expected,
    ) as mock_backbone_build:
        result = builder.build(node, index)
    mock_backbone_build.assert_called_once()


def test_build__delegates_node_to_backbone_builder(builder, index):
    node = make_node(content_reference="#Resource.component")
    with patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_backbone_build:
        builder.build(node, index)
    args = mock_backbone_build.call_args
    assert args[0][0] is node


def test_build__delegates_ref_subtree_to_backbone_builder(builder):
    ref_subtree = MagicMock(name="ref-subtree")
    idx = make_index(ref_subtree=ref_subtree)
    node = make_node(content_reference="#Resource.component")

    with patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_backbone_build:
        builder.build(node, idx)
    args = mock_backbone_build.call_args
    assert args[0][1] is ref_subtree


def test_build__returns_backbone_builder_result(builder, index):
    node = make_node(content_reference="#Resource.component")
    expected = Build()
    with patch(
        BACKBONEFIELDBUILDER_BUILD,
        return_value=expected,
    ):
        result = builder.build(node, index)
    assert result is expected


def test_build__backbone_builder_receives_same_context(builder, index):
    node = make_node(content_reference="#Resource.component")
    captured = {}

    original_init = __import__(
        "fhircraft.fhir.resources.factory.builders.backbone",
        fromlist=["BackboneFieldBuilder"],
    ).BackboneFieldBuilder.__init__

    def capturing_init(self, context):
        captured["context"] = context
        original_init(self, context)

    with (
        patch(
            "fhircraft.fhir.resources.factory.builders.content_reference.BackboneFieldBuilder.__init__",
            capturing_init,
        ),
        patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()),
    ):
        builder.build(node, index)

    assert captured["context"] is builder.context


def test_build__cyclic_ref_resolves_fragment_from_index(builder):
    node = make_node(content_reference="#StructureMap.group.rule")

    # The ancestor node exists in the same index
    ancestor_node = MagicMock(name="ancestor-rule-node")
    ancestor_subtree = MagicMock(name="ancestor-rule-subtree")
    idx = make_index(ref_node=ancestor_node, ref_subtree=ancestor_subtree)

    with patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()):
        builder.build(node, idx)

    idx.get.assert_called_with("StructureMap.group.rule")


def test_build__cyclic_ref_fetches_ancestor_subtree(builder):
    node = make_node(content_reference="#StructureMap.group.rule")

    ancestor_subtree = MagicMock(name="ancestor-rule-subtree")
    idx = make_index(ref_subtree=ancestor_subtree)

    with patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_backbone_build:
        builder.build(node, idx)

    # The second positional argument to BackboneFieldBuilder.build must be the
    # ancestor's subtree, not the index of the current (nested) element.
    args = mock_backbone_build.call_args[0]
    assert args[1] is ancestor_subtree


def test_build__cyclic_ref_passes_original_node_to_backbone_builder(builder):
    node = make_node(content_reference="#StructureMap.group.rule")
    idx = make_index()

    with patch(BACKBONEFIELDBUILDER_BUILD, return_value=Build()) as mock_backbone_build:
        builder.build(node, idx)

    args = mock_backbone_build.call_args[0]
    assert args[0] is node


def test_build__cyclic_ref_returns_backbone_builder_result(builder):
    node = make_node(content_reference="#StructureMap.group.rule")
    idx = make_index()
    expected = Build()

    with patch(
        BACKBONEFIELDBUILDER_BUILD,
        return_value=expected,
    ):
        result = builder.build(node, idx)

    assert result is expected


def test_build__cyclic_ref_raises_when_ancestor_path_missing(builder):
    node = make_node(content_reference="#StructureMap.group.rule")
    idx = make_index()
    idx.get.return_value = None  # ancestor not found

    with pytest.raises(ValueError, match="StructureMap.group.rule"):
        builder.build(node, idx)
