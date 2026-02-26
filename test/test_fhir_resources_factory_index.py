import pytest
from unittest.mock import MagicMock

from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.factory.exceptions import DefinitionIndexError


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def make_node(id: str, path: str | None = None, slicing=None) -> ElementNode:
    """Create an :class:`ElementNode` backed by a MagicMock definition."""
    defn = MagicMock()
    defn.id = id
    defn.path = path if path is not None else id
    defn.slicing = slicing
    defn.contentReference = False
    local = id.rsplit(".", 1)[-1]
    defn.sliceName = local.split(":", 1)[1] if ":" in local else None
    return ElementNode(definition=defn)


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture
def simple_index():
    """Flat index with a root and two plain children."""
    return DefinitionIndex(
        [
            make_node("Observation", "Observation"),
            make_node("Observation.status", "Observation.status"),
            make_node("Observation.code", "Observation.code"),
        ]
    )


@pytest.fixture
def slicing_index():
    """Index that includes a slice entry, two named slices, and a sub-child."""
    return DefinitionIndex(
        [
            make_node("Observation", "Observation"),
            make_node(
                "Observation.component", "Observation.component", slicing=MagicMock()
            ),
            make_node("Observation.component:systolic", "Observation.component"),
            make_node("Observation.component:diastolic", "Observation.component"),
            make_node(
                "Observation.component.value[x]", "Observation.component.value[x]"
            ),
        ]
    )


# ------------------------------------------------------------------
# Construction
# ------------------------------------------------------------------


def test_index_len(simple_index):
    assert len(simple_index) == 3


def test_index_nodes_returns_all(simple_index):
    ids = {n.id for n in simple_index.nodes}
    assert ids == {"Observation", "Observation.status", "Observation.code"}


def test_index_from_elements():
    """from_elements wraps raw definitions in ElementNodes."""
    defn = MagicMock()
    defn.id = "Patient"
    defn.path = "Patient"
    defn.slicing = None
    defn.contentReference = False
    defn.sliceName = None
    index = DefinitionIndex.from_elements([defn])
    assert len(index) == 1
    assert "Patient" in index


# ------------------------------------------------------------------
# Basic access
# ------------------------------------------------------------------


def test_index_contains_known_id(simple_index):
    assert "Observation.status" in simple_index


def test_index_not_contains_unknown_id(simple_index):
    assert "Observation.unknown" not in simple_index


def test_index_get_returns_node(simple_index):
    node = simple_index.get("Observation.code")
    assert node.id == "Observation.code"


def test_index_get_raises_for_missing(simple_index):
    with pytest.raises(DefinitionIndexError):
        simple_index.get("Observation.missing")


def test_index_get_by_path_returns_nodes(slicing_index):
    nodes = slicing_index.get_by_path("Observation.component")
    assert len(nodes) >= 1
    assert all(n.path == "Observation.component" for n in nodes)


def test_index_get_by_path_raises_for_missing(simple_index):
    with pytest.raises(DefinitionIndexError):
        simple_index.get_by_path("Observation.missing")


def test_index_iter(simple_index):
    ids = [n.id for n in simple_index]
    assert sorted(ids) == sorted(
        ["Observation", "Observation.status", "Observation.code"]
    )


def test_index_ids_sorted(simple_index):
    assert simple_index.ids() == sorted(
        ["Observation", "Observation.status", "Observation.code"]
    )


def test_index_paths(simple_index):
    assert simple_index.paths() == {
        "Observation",
        "Observation.status",
        "Observation.code",
    }


# ------------------------------------------------------------------
# Root detection
# ------------------------------------------------------------------


def test_index_root_returns_root_node(simple_index):
    root = simple_index.root()
    assert root.id == "Observation"


def test_index_root_raises_when_no_root():
    index = DefinitionIndex(
        [
            make_node("Observation.status", "Observation.status"),
            make_node("Observation.code", "Observation.code"),
        ]
    )
    with pytest.raises(DefinitionIndexError):
        index.root()


def test_index_root_raises_for_multiple_roots():
    index = DefinitionIndex(
        [
            make_node("Observation", "Observation"),
            make_node("Patient", "Patient"),
        ]
    )
    with pytest.raises(DefinitionIndexError):
        index.root()


# ------------------------------------------------------------------
# Navigation — get_parent
# ------------------------------------------------------------------


@pytest.mark.parametrize(
    "id, expected_parent_id",
    [
        ("Observation.component", "Observation"),
        ("Observation.component:systolic", "Observation"),
        ("Observation.component.value[x]", "Observation.component"),
    ],
)
def test_get_parent(slicing_index, id, expected_parent_id):
    parent = slicing_index.get_parent(id)
    assert parent.id == expected_parent_id


def test_get_parent_raises_for_root(simple_index):
    with pytest.raises(DefinitionIndexError):
        simple_index.get_parent("Observation")


# ------------------------------------------------------------------
# Navigation — get_children
# ------------------------------------------------------------------


def test_get_children_returns_non_slice_children(simple_index):
    children = simple_index.get_children("Observation")
    ids = {n.id for n in children}
    assert ids == {"Observation.status", "Observation.code"}


def test_get_children_excludes_slices(slicing_index):
    children = slicing_index.get_children("Observation")
    ids = {n.id for n in children}
    assert "Observation.component:systolic" not in ids
    assert "Observation.component:diastolic" not in ids


def test_get_children_empty_for_leaf(simple_index):
    assert simple_index.get_children("Observation.code") == []


# ------------------------------------------------------------------
# Navigation — get_slices
# ------------------------------------------------------------------


def test_get_slices_returns_named_slices(slicing_index):
    slices = slicing_index.get_slices("Observation.component")
    ids = {n.id for n in slices}
    assert ids == {"Observation.component:systolic", "Observation.component:diastolic"}


def test_get_slices_raises_for_non_slice_entry(simple_index):
    with pytest.raises(DefinitionIndexError):
        simple_index.get_slices("Observation.code")


# ------------------------------------------------------------------
# Navigation — get_slice_children
# ------------------------------------------------------------------


def test_get_slice_children_returns_children_of_slice(slicing_index):
    # Build an index where a named slice itself has child elements
    index = DefinitionIndex(
        [
            make_node("Observation", "Observation"),
            make_node(
                "Observation.component", "Observation.component", slicing=MagicMock()
            ),
            make_node("Observation.component:systolic", "Observation.component"),
            make_node(
                "Observation.component:systolic.code", "Observation.component.code"
            ),
            make_node(
                "Observation.component:systolic.value[x]",
                "Observation.component.value[x]",
            ),
        ]
    )
    children = index.get_slice_children("Observation.component:systolic")
    ids = {n.id for n in children}
    assert ids == {
        "Observation.component:systolic.code",
        "Observation.component:systolic.value[x]",
    }


# ------------------------------------------------------------------
# Navigation — get_subtree
# ------------------------------------------------------------------


def test_get_subtree_includes_root_and_descendants(slicing_index):
    subtree = slicing_index.get_subtree("Observation.component")
    ids = {n.id for n in subtree}
    assert ids == {
        "Observation.component",
        "Observation.component:systolic",
        "Observation.component:diastolic",
        "Observation.component.value[x]",
    }


def test_get_subtree_excludes_unrelated_nodes(slicing_index):
    subtree = slicing_index.get_subtree("Observation.component")
    ids = {n.id for n in subtree}
    assert "Observation" not in ids


def test_get_subtree_single_leaf(simple_index):
    subtree = simple_index.get_subtree("Observation.code")
    ids = {n.id for n in subtree}
    assert ids == {"Observation.code"}


def test_get_subtree_returns_definition_index(simple_index):
    subtree = simple_index.get_subtree("Observation")
    assert isinstance(subtree, DefinitionIndex)


# ------------------------------------------------------------------
# repr
# ------------------------------------------------------------------


def test_repr_with_root(simple_index):
    r = repr(simple_index)
    assert "Observation" in r
    assert "3" in r


def test_repr_without_root():
    index = DefinitionIndex(
        [
            make_node("A.x", "A.x"),
            make_node("A.y", "A.y"),
        ]
    )
    r = repr(index)
    assert "size=" in r
