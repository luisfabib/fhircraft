"""
Unit tests for SnapshotResolver private methods.
"""

from unittest import result

import pytest
from unittest.mock import MagicMock

from fhircraft.config import configure, reset_config
from fhircraft.fhir.resources.datatypes.R4.complex.element_definition import (
    ElementDefinition,
    ElementDefinitionType,
)
from fhircraft.fhir.resources.definitions import StructureDefinitionRegistry
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.exceptions import (
    DefinitionIndexError,
    DefinitionResolutionError,
)
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.factory.resolver import SnapshotResolver


# ------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------


def make_element(id: str, path: str | None = None, **kwargs) -> ElementDefinition:
    """Return an ElementDefinition built with model_construct (no validation)."""
    return ElementDefinition.model_construct(
        id=id,
        path=path if path is not None else id,
        **kwargs,
    )


def make_node(id: str, path: str | None = None, **kwargs) -> ElementNode:
    """Convenience wrapper — builds an ElementNode directly from kwargs."""
    return ElementNode(definition=make_element(id, path, **kwargs))


def make_base_index(*elements: ElementDefinition) -> DefinitionIndex:
    return DefinitionIndex.from_elements(list(elements))


def make_structure_def(*, snapshot_elements=None, differential_elements=None):
    """Build a minimal StructureDefinition mock."""
    sd = MagicMock()
    sd.name = "MockProfile"
    sd.url = "http://example.org/MockProfile"

    if snapshot_elements is not None:
        sd.snapshot = MagicMock()
        sd.snapshot.element = snapshot_elements
    else:
        sd.snapshot = None

    if differential_elements is not None:
        sd.differential = MagicMock()
        sd.differential.element = differential_elements
    else:
        sd.differential = None

    return sd


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture(autouse=True)
def skip_validation():
    configure(validation_mode="skip")
    yield
    reset_config()


@pytest.fixture
def resolver():
    register = StructureDefinitionRegistry(fhir_release="R4")
    register._internet_access_enabled = False  # Disable internet access for tests
    return SnapshotResolver(registry=register)


@pytest.fixture
def base_index():
    """
    A simple base snapshot containing:
      - BaseResource (root)
      - BaseResource.status  (min=0, max="1", short="The status")
      - BaseResource.component  (min=0, max="*")
      - BaseResource.component.code  (min=1, max="1", short="Component code")
    """
    return make_base_index(
        make_element("BaseResource", "BaseResource"),
        make_element(
            "BaseResource.status",
            "BaseResource.status",
            min=0,
            max="1",
            short="The status",
            type=[ElementDefinitionType(code="code")],
        ),
        make_element(
            "BaseResource.component",
            "BaseResource.component",
            min=0,
            max="*",
            short="Component list",
            type=[ElementDefinitionType(code="BackboneElement")],
        ),
        make_element(
            "BaseResource.component.code",
            "BaseResource.component.code",
            min=0,
            max="1",
            short="Component code",
            type=[ElementDefinitionType(code="CodeableConcept")],
        ),
    )


# ==================================================================
# SnapshotResolver._build_type_node
# ==================================================================


def test_build_type_node__returns_element_node(base_index, resolver):
    node = resolver._build_type_node(["Extension"], "Observation.extension", base_index)
    assert isinstance(node, ElementNode)


@pytest.mark.parametrize(
    "id",
    [
        "Observation.code.coding",
        "Observation.code:sliceA.coding",
    ],
)
def test_build_type_node__returns_correct_node(base_index, resolver, id):

    node = resolver._build_type_node(["CodeableConcept"], id, base_index)
    assert node.id == id
    assert node.path == "Observation.code.coding"
    assert node.min_cardinality == 0
    assert node.max_cardinality == None


@pytest.mark.parametrize(
    "type",
    ["string", "boolean", "integer", "decimal", "uri", "code", "dateTime"],
)
def test_build_type_node__ignores_fhir_primitive_type_nodes(base_index, resolver, type):
    with pytest.raises(DefinitionResolutionError):
        resolver._build_type_node([type], "Observation.value", base_index)


@pytest.mark.parametrize(
    "type",
    [
        "http://hl7.org/fhirpath/System.String",
        "http://hl7.org/fhirpath/System.Integer",
        "http://hl7.org/fhirpath/System.Boolean",
        "http://hl7.org/fhirpath/System.Decimal",
    ],
)
def test_build_type_node__ignores_fhirpath_type_nodes(base_index, resolver, type):
    with pytest.raises(DefinitionResolutionError):
        resolver._build_type_node([type], "Observation.value", base_index)


# ------------------------------------------------------------------
# SnapshotResolver._build_intermediate_node
# ------------------------------------------------------------------


def test_build_intermediate_node__is_element_node(resolver, base_index):
    node = resolver._build_intermediate_node("MyProfile.status", base_index)
    assert isinstance(node, ElementNode)


@pytest.mark.parametrize(
    "requested_id",
    [
        "MyProfile.status",
        "AnotherProfile.status",
        "Observation.status",
    ],
)
def test_build_intermediate_node__node_carries_requested_id(
    resolver, base_index, requested_id
):
    node = resolver._build_intermediate_node(requested_id, base_index)
    assert node.id == requested_id


def test_build_intermediate_node__path_comes_from_base(resolver, base_index):
    node = resolver._build_intermediate_node("MyProfile.status", base_index)
    assert node.path == "MyProfile.status"


@pytest.mark.parametrize(
    "root",
    ["MyProfile", "Observation", "Condition", "BaseResource"],
)
def test_build_intermediate_node__regardless_of_profile_root(
    resolver, base_index, root
):
    node = resolver._build_intermediate_node(f"{root}.status", base_index)
    assert node.id == f"{root}.status"


def test_build_intermediate_node__return_inherited_from_base(resolver, base_index):
    node = resolver._build_intermediate_node("MyProfile.status", base_index)
    assert node.id == "MyProfile.status"
    assert node.path == "MyProfile.status"
    assert node.min_cardinality == 0
    assert node.max_cardinality == 1
    assert node.definition.short == "The status"


def test_build_intermediate_node__return_inherited_from_base_array(
    resolver, base_index
):
    node = resolver._build_intermediate_node("MyProfile.component", base_index)
    assert node.id == "MyProfile.component"
    assert node.path == "MyProfile.component"
    assert node.min_cardinality == 0
    assert node.max_cardinality == None
    assert node.definition.short == "Component list"


def test_build_intermediate_node__return_inherited_from_type(resolver, base_index):
    node = resolver._build_intermediate_node("MyProfile.component.id", base_index)
    assert node.id == "MyProfile.component.id"
    assert node.path == "MyProfile.component.id"
    assert node.min_cardinality == 0
    assert node.max_cardinality == 1
    assert node.definition.short == "Unique id for inter-element referencing"


def test_build_intermediate_node__definition_class_is_same_as_base(
    resolver, base_index
):
    base_node = base_index.get("BaseResource.status")
    node = resolver._build_intermediate_node("MyProfile.status", base_index)
    assert type(node.definition) is type(base_node.definition)


# ------------------------------------------------------------------
# SnapshotResolver._merge_node_with_base
# ------------------------------------------------------------------


def test_merge_node_with_base__returns_element_node(resolver):
    diff = make_node(id="MyProfile.status", min=1, max="1")
    base = make_node(id="BaseResource.status", min=0, max="1", short="The status")
    result = resolver._merge_node_with_base(diff, base)
    assert isinstance(result, ElementNode)


def test_merge_node_with_base__result_carries_diff_id(resolver):
    diff = make_node(id="MyProfile.status", min=1)
    base = make_node(id="BaseResource.status", min=0, max="1")
    result = resolver._merge_node_with_base(diff, base)
    assert result.id == "MyProfile.status"


def test_merge_node_with_base__result_carries_diff_path(resolver):
    diff = make_node(id="MyProfile.status", path="MyProfile.status")
    base = make_node(id="BaseResource.status", path="BaseResource.status")
    result = resolver._merge_node_with_base(diff, base)
    assert result.path == "MyProfile.status"


def test_merge_node_with_base__falls_back_to_base_path_when_diff_path_absent(resolver):
    diff = ElementNode(
        definition=ElementDefinition.model_construct(id="MyProfile.status", path=None)
    )
    base = make_node(
        id="BaseResource.status", path="BaseResource.status", min=0, max="1"
    )
    result = resolver._merge_node_with_base(diff, base)
    assert result.path == "BaseResource.status"


def test_merge_node_with_base__base_fields_inherited_when_not_in_diff(resolver):
    diff = make_node(id="MyProfile.status")
    base = make_node(id="BaseResource.status", min=0, max="1", short="The status")
    result = resolver._merge_node_with_base(diff, base)
    assert result.min_cardinality == 0
    assert result.max_cardinality == 1
    assert result.definition.short == "The status"


def test_merge_node_with_base__diff_cardinality_overrides_base(resolver):
    diff = make_node(id="MyProfile.status", min=1, max="4", short="Overridden status")
    base = make_node(id="BaseResource.status", min=0, max="*", short="The status")
    result = resolver._merge_node_with_base(diff, base)
    assert result.min_cardinality == 1
    assert result.max_cardinality == 4
    assert result.definition.short == "Overridden status"


def test_merge_node_with_base__definition_class_matches_base(resolver):
    diff = make_node(id="MyProfile.status", min=1)
    base = make_node(id="BaseResource.status", min=0, max="1")
    result = resolver._merge_node_with_base(diff, base)
    assert type(result.definition) is type(base.definition)


def test_merge_node_with_base__base_type_kept_when_diff_has_none(resolver):
    base_type = [ElementDefinitionType.model_construct(code="code")]
    diff = make_node(id="MyProfile.status")  # no type
    base = make_node(id="BaseResource.status", min=0, max="1", type=base_type)
    result = resolver._merge_node_with_base(diff, base)
    assert result.type_codes == ["code"]


# ------------------------------------------------------------------
# SnapshotResolver._resolve_differential
# ------------------------------------------------------------------


def test_resolve_differential__returns_definition_index(resolver, base_index):
    diff = [make_element("MyProfile.status", "MyProfile.status")]
    result = resolver._resolve_differential(diff, base_index)
    assert isinstance(result, DefinitionIndex)


def test_resolve_differential__diff_element_present_in_base(resolver, base_index):
    diff = [
        make_element("MyProfile", "MyProfile"),
        make_element("MyProfile.status", "MyProfile.status", min=1, max="1"),
    ]
    index = resolver._resolve_differential(diff, base_index)
    assert "MyProfile.status" in index


def test_resolve_differential__diff_overrides_base_min(resolver, base_index):
    diff = [
        make_element("MyProfile", "MyProfile"),
        make_element("MyProfile.status", "MyProfile.status", min=1),
    ]
    index = resolver._resolve_differential(diff, base_index)
    assert (node := index.get("MyProfile.status"))
    assert node.min_cardinality == 1
    assert node.max_cardinality == 1


def test_resolve_differential__diff_overrides_base_max(resolver, base_index):
    diff = [
        make_element("MyProfile", "MyProfile"),
        make_element("MyProfile.status", "MyProfile.status", max="0"),
    ]
    index = resolver._resolve_differential(diff, base_index)
    assert (node := index.get("MyProfile.status"))
    assert node.min_cardinality == 0
    assert node.max_cardinality == 0


def test_resolve_differential__intermediate_nodes_filled_from_base(
    resolver, base_index
):
    diff = [
        make_element("MyProfile", "MyProfile"),
        make_element("MyProfile.component.code", "MyProfile.component.code", max="*"),
    ]
    index = resolver._resolve_differential(diff, base_index)
    assert (node := index.get("MyProfile.component"))
    assert node.min_cardinality == 0
    assert node.max_cardinality == None
    assert (node := index.get("MyProfile.component.code"))
    assert node.min_cardinality == 0
    assert node.max_cardinality == None


def test_resolve_differential__multiple_diff_elements_all_in_result(
    resolver, base_index
):
    diff = [
        make_element("MyProfile", "MyProfile"),
        make_element("MyProfile.status", "MyProfile.status", min=1),
        make_element("MyProfile.component", "MyProfile.component", max="*"),
        make_element(
            "MyProfile.component:sliceA", "MyProfile.component", min=2, max="3"
        ),
        make_element("MyProfile.component:sliceB", "MyProfile.component", min=3),
        make_element(
            "MyProfile.component:sliceB.code", "MyProfile.component.code", max="1"
        ),
        make_element(
            "MyProfile.component:sliceB.code.coding.system",
            "MyProfile.component.code.coding.system",
            fixedString="http://example.org/system",
        ),
    ]
    index = resolver._resolve_differential(diff, base_index)
    assert (node := index.get("MyProfile.status"))
    assert node.min_cardinality == 1
    assert node.max_cardinality == 1
    assert (node := index.get("MyProfile.component"))
    assert node.min_cardinality == 0
    assert node.max_cardinality == None
    assert (node := index.get("MyProfile.component:sliceA"))
    assert node.min_cardinality == 2
    assert node.max_cardinality == 3
    assert (node := index.get("MyProfile.component:sliceB"))
    assert node.min_cardinality == 3
    assert node.max_cardinality == None
    assert (node := index.get("MyProfile.component:sliceB.code"))
    assert node.min_cardinality == 0
    assert node.max_cardinality == 1
    assert (node := index.get("MyProfile.component:sliceB.code.coding.system"))
    assert node.min_cardinality == 0
    assert node.max_cardinality == 1
    assert node.definition.fixedString == "http://example.org/system"


def test_resolve_differential__raises_when_element_has_no_id(resolver, base_index):
    diff = [ElementDefinition.model_construct(id=None, path="MyProfile.status")]
    with pytest.raises(DefinitionResolutionError):
        resolver._resolve_differential(diff, base_index)


def test_resolve_differential__raises_for_empty_diff(resolver, base_index):
    with pytest.raises(DefinitionResolutionError):
        resolver._resolve_differential([], base_index)


# ==================================================================
# SnapshotResolver._resolve_content_references
# ==================================================================


def test_resolve_content_references__returns_definition_index(resolver, base_index):
    result = resolver._resolve_content_references(base_index)
    assert isinstance(result, DefinitionIndex)


def test_resolve_content_references__passthrough_nodes_without_content_reference(
    resolver, base_index
):
    result = resolver._resolve_content_references(base_index)
    result_ids = {n.id for n in result.nodes}
    base_ids = {n.id for n in base_index.nodes}
    assert result_ids == base_ids


def test_resolve_content_references__resolves_hash_prefixed_local_reference(
    resolver, base_index
):
    cr_elem = make_element(
        "BaseResource.extra",
        "BaseResource.extra",
        contentReference="#BaseResource.status",
    )
    index = DefinitionIndex.from_elements(
        [n.definition for n in base_index.nodes] + [cr_elem]
    )
    result = resolver._resolve_content_references(index)
    extra_node = result.get("BaseResource.extra")
    assert extra_node is not None
    assert extra_node.definition.short == "The status"


def test_resolve_content_references__resolved_node_keeps_its_own_id(
    resolver, base_index
):
    cr_elem = make_element(
        "BaseResource.extra",
        "BaseResource.extra",
        contentReference="#BaseResource.status",
    )
    index = DefinitionIndex.from_elements(
        [n.definition for n in base_index.nodes] + [cr_elem]
    )
    result = resolver._resolve_content_references(index)
    extra_node = result.get("BaseResource.extra")
    assert extra_node.id == "BaseResource.extra"


def test_resolve_content_references__resolves_bare_path_reference(resolver, base_index):
    """A contentReference without '#' resolves from the same index."""
    cr_elem = make_element(
        "BaseResource.extra",
        "BaseResource.extra",
        contentReference="BaseResource.status",
    )
    index = DefinitionIndex.from_elements(
        [n.definition for n in base_index.nodes] + [cr_elem]
    )
    result = resolver._resolve_content_references(index)
    extra_node = result.get("BaseResource.extra")
    assert extra_node is not None
    assert extra_node.definition.short == "The status"


def test_resolve_content_references__external_reference_uses_registry(
    resolver, base_index
):
    """An external contentReference (URL#path) is resolved via the registry."""
    ext_sd = MagicMock()
    ext_sd.snapshot = MagicMock()
    ext_sd.snapshot.element = [
        make_element("External.status", "External.status", short="External status")
    ]
    resolver._registry.get = MagicMock(return_value=ext_sd)

    cr_elem = make_element(
        "BaseResource.extra",
        "BaseResource.extra",
        contentReference="http://example.org/External#External.status",
    )
    index = DefinitionIndex.from_elements(
        [n.definition for n in base_index.nodes] + [cr_elem]
    )
    result = resolver._resolve_content_references(index)
    extra_node = result.get("BaseResource.extra")
    assert extra_node is not None
    assert extra_node.definition.short == "External status"
    resolver._registry.get.assert_called_once_with("http://example.org/External")


def test_resolve_content_references__raises_when_external_resource_not_found(
    resolver, base_index
):
    resolver._registry.get = MagicMock(return_value=None)
    cr_elem = make_element(
        "BaseResource.extra",
        "BaseResource.extra",
        contentReference="http://example.org/Missing#Missing.field",
    )
    index = DefinitionIndex.from_elements(
        [n.definition for n in base_index.nodes] + [cr_elem]
    )
    with pytest.raises(ValueError):
        resolver._resolve_content_references(index)


def test_resolve_content_references__raises_when_external_resource_has_no_snapshot(
    resolver, base_index
):
    ext_sd = MagicMock()
    ext_sd.snapshot = None
    resolver._registry.get = MagicMock(return_value=ext_sd)

    cr_elem = make_element(
        "BaseResource.extra",
        "BaseResource.extra",
        contentReference="http://example.org/External#External.field",
    )
    index = DefinitionIndex.from_elements(
        [n.definition for n in base_index.nodes] + [cr_elem]
    )
    with pytest.raises(ValueError):
        resolver._resolve_content_references(index)


def test_resolve_content_references__mixed_nodes_all_present_in_result(
    resolver, base_index
):
    """Non-reference and resolved reference nodes all appear in result."""
    cr_elem = make_element(
        "BaseResource.extra",
        "BaseResource.extra",
        contentReference="#BaseResource.component",
    )
    index = DefinitionIndex.from_elements(
        [n.definition for n in base_index.nodes] + [cr_elem]
    )
    result = resolver._resolve_content_references(index)
    for n in base_index.nodes:
        assert n.id in result
    assert "BaseResource.extra" in result


# ==================================================================
# SnapshotResolver.resolve
# ==================================================================


def test_resolve__snapshot_mode_returns_definition_index(resolver, base_index):
    elements = list(base_index.nodes)
    sd = make_structure_def(snapshot_elements=[n.definition for n in elements])
    result = resolver.resolve(sd, base_index, mode="snapshot")
    assert isinstance(result, DefinitionIndex)


def test_resolve__snapshot_mode_index_contains_all_elements(resolver, base_index):
    elements = [n.definition for n in base_index.nodes]
    sd = make_structure_def(snapshot_elements=elements)
    result = resolver.resolve(sd, base_index, mode="snapshot")
    for elem in elements:
        assert elem.id in result


def test_resolve__snapshot_mode_raises_when_snapshot_is_none(resolver, base_index):
    sd = make_structure_def(snapshot_elements=None)
    with pytest.raises(AssertionError):
        resolver.resolve(sd, base_index, mode="snapshot")


def test_resolve__snapshot_mode_raises_when_snapshot_elements_is_none(
    resolver, base_index
):
    sd = make_structure_def(snapshot_elements=None)
    sd.snapshot = MagicMock()
    sd.snapshot.element = None
    with pytest.raises(AssertionError):
        resolver.resolve(sd, base_index, mode="snapshot")


def test_resolve__snapshot_mode_raises_when_snapshot_elements_contain_none(
    resolver, base_index
):
    elements = [n.definition for n in base_index.nodes]
    elements.append(None)
    sd = make_structure_def(snapshot_elements=elements)
    with pytest.raises(AssertionError):
        resolver.resolve(sd, base_index, mode="snapshot")


# ------------------------------------------------------------------
# mode="differential"
# ------------------------------------------------------------------


def test_resolve__differential_mode_delegates_to_resolve_differential(
    resolver, base_index
):
    diff_elements = [make_element("MyProfile.status", "MyProfile.status")]
    sd = make_structure_def(differential_elements=diff_elements)

    expected = DefinitionIndex(list(base_index.nodes))
    resolver._resolve_differential = MagicMock(return_value=expected)
    resolver._resolve_content_references = MagicMock(return_value=expected)

    result = resolver.resolve(sd, base_index, mode="differential")

    resolver._resolve_differential.assert_called_once_with(diff_elements, base_index)
    resolver._resolve_content_references.assert_called_once_with(expected)
    assert result is expected


def test_resolve__differential_mode_returns_definition_index(resolver, base_index):
    diff_elements = [make_element("MyProfile.status", "MyProfile.status")]
    sd = make_structure_def(differential_elements=diff_elements)

    resolver._resolve_differential = MagicMock(
        return_value=DefinitionIndex(list(base_index.nodes))
    )
    resolver._resolve_content_references = MagicMock(
        return_value=DefinitionIndex(list(base_index.nodes))
    )
    result = resolver.resolve(sd, base_index, mode="differential")
    assert isinstance(result, DefinitionIndex)


def test_resolve__differential_mode_raises_when_differential_is_none(
    resolver, base_index
):
    sd = make_structure_def(differential_elements=None)
    with pytest.raises(AssertionError):
        resolver.resolve(sd, base_index, mode="differential")


def test_resolve__differential_mode_raises_when_differential_elements_is_none(
    resolver, base_index
):
    sd = make_structure_def(differential_elements=None)
    sd.differential = MagicMock()
    sd.differential.element = None
    with pytest.raises(AssertionError):
        resolver.resolve(sd, base_index, mode="differential")


def test_resolve__differential_mode_raises_when_differential_elements_contain_none(
    resolver, base_index
):
    diff_elements = [make_element("MyProfile.status", "MyProfile.status"), None]
    sd = make_structure_def(differential_elements=diff_elements)
    with pytest.raises(AssertionError):
        resolver.resolve(sd, base_index, mode="differential")


def test_resolve__auto_mode_uses_differential_when_present(resolver, base_index):
    diff_elements = [make_element("MyProfile.status", "MyProfile.status")]
    sd = make_structure_def(differential_elements=diff_elements)

    expected = DefinitionIndex(list(base_index.nodes))
    resolver._resolve_differential = MagicMock(return_value=expected)
    resolver._resolve_content_references = MagicMock(return_value=expected)

    result = resolver.resolve(sd, base_index, mode="auto")

    resolver._resolve_differential.assert_called_once_with(diff_elements, base_index)
    assert result is expected


def test_resolve__auto_mode_uses_snapshot_when_no_differential(resolver, base_index):
    elements = [n.definition for n in base_index.nodes]
    sd = make_structure_def(snapshot_elements=elements)  # differential=None by default

    result = resolver.resolve(sd, base_index, mode="auto")

    assert isinstance(result, DefinitionIndex)


def test_resolve__auto_mode_is_default(resolver, base_index):
    diff_elements = [make_element("MyProfile.status", "MyProfile.status")]
    sd = make_structure_def(differential_elements=diff_elements)

    expected = DefinitionIndex(list(base_index.nodes))
    resolver._resolve_differential = MagicMock(return_value=expected)
    resolver._resolve_content_references = MagicMock(return_value=expected)

    result = resolver.resolve(sd, base_index)  # no mode kwarg

    resolver._resolve_differential.assert_called_once()
    assert result is expected
