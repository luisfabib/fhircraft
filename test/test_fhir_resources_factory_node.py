import pytest
from unittest.mock import MagicMock
from fhircraft.config import configure, reset_config
from fhircraft.fhir.resources.datatypes.R4.complex.element_definition import (
    ElementDefinition,
)
from fhircraft.fhir.resources.factory.element_node import ElementNode


@pytest.fixture
def element():
    configure(validation_mode="skip")
    yield ElementDefinition.model_construct()
    reset_config()


# ------------------------------------------------------------------
# Identity & position
# ------------------------------------------------------------------


@pytest.mark.parametrize(
    "id",
    [
        ("Resource.name"),
        ("Resource.name[x]"),
        ("Resource.value[x]"),
        ("Resource.component.value[x]"),
        ("Resource.component.code"),
        ("Resource.extensio:slice"),
        ("Resource.extensio:slice.url"),
    ],
)
def test_element_node_id(element, id):
    element.id = id
    node = ElementNode(definition=element)
    assert node.id == id


@pytest.mark.parametrize(
    "id, expected",
    [
        ("Resource.name", ["Resource", "name"]),
        ("Resource.name[x]", ["Resource", "name[x]"]),
        ("Resource.value[x]", ["Resource", "value[x]"]),
        ("Resource.component.value[x]", ["Resource", "component", "value[x]"]),
        ("Resource.component.code", ["Resource", "component", "code"]),
        ("Resource.extension:slice", ["Resource", "extension", "slice"]),
        ("Resource.extension:slice.url", ["Resource", "extension", "slice", "url"]),
    ],
)
def test_element_node_id_segments(element, id, expected):
    element.id = id
    node = ElementNode(definition=element)
    assert node.id_segments == expected


@pytest.mark.parametrize(
    "id, expected",
    [
        ("Resource", ["Resource"]),
        ("Resource.name[x]", ["Resource", "Resource.name[x]"]),
        (
            "Resource.component.value[x]",
            ["Resource", "Resource.component", "Resource.component.value[x]"],
        ),
        (
            "Resource.component.code",
            ["Resource", "Resource.component", "Resource.component.code"],
        ),
        (
            "Resource.extension:slice",
            ["Resource", "Resource.extension", "Resource.extension:slice"],
        ),
        (
            "Resource.extension:slice.url",
            [
                "Resource",
                "Resource.extension",
                "Resource.extension:slice",
                "Resource.extension:slice.url",
            ],
        ),
    ],
)
def test_element_node_id_ancestry(element, id, expected):
    element.id = id
    element.path = id
    node = ElementNode(definition=element)
    assert node.id_ancestry == expected


@pytest.mark.parametrize(
    "path",
    [
        ("Resource.name"),
        ("Resource.name[x]"),
        ("Resource.value[x]"),
        ("Resource.component.value[x]"),
        ("Resource.component.code"),
        ("Resource.extension"),
    ],
)
def test_element_node_path(element, path):
    element.path = path
    node = ElementNode(definition=element)
    assert node.path == path


@pytest.mark.parametrize(
    "path",
    [
        ("Resource.name"),
        ("Resource.name[x]"),
        ("Resource.component.code"),
    ],
)
def test_element_node_path_segments(element, path):
    element.path = path
    node = ElementNode(definition=element)
    assert node.path_segments == [seg.split(":")[0] for seg in path.split(".")]


@pytest.mark.parametrize(
    "path, expected",
    [
        ("Resource", ["Resource"]),
        ("Resource.name[x]", ["Resource", "Resource.name[x]"]),
        (
            "Resource.component.value[x]",
            ["Resource", "Resource.component", "Resource.component.value[x]"],
        ),
        (
            "Resource.component.code",
            ["Resource", "Resource.component", "Resource.component.code"],
        ),
    ],
)
def test_element_node_path_ancestry(element, path, expected):
    element.path = path
    node = ElementNode(definition=element)
    assert node.path_ancestry == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("Resource", 0),
        ("Resource.name", 1),
        ("Resource.component.value[x]", 2),
        ("Resource.component.code.coding", 3),
        ("Resource.component.code.coding.system", 4),
    ],
)
def test_element_node_depth(element, path, expected):
    element.path = path
    node = ElementNode(definition=element)
    assert node.depth == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("Resource", "Resource"),
        ("Resource.name", "name"),
        ("Resource.name[x]", "name"),
        ("Resource.value[x]", "value"),
        ("Resource.component.value[x]", "value"),
        ("Resource.component.code", "code"),
        ("Resource.extension", "extension"),
    ],
)
def test_element_node_element_name(element, path, expected):
    element.path = path
    node = ElementNode(definition=element)
    assert node.name == expected


@pytest.mark.parametrize(
    "id, expected_parent, expected_local",
    [
        ("Resource", None, "Resource"),
        ("Resource.name", "Resource", "name"),
        ("Resource.name[x]", "Resource", "name[x]"),
        ("Resource.value[x]", "Resource", "value[x]"),
        ("Resource.component.value[x]", "Resource.component", "value[x]"),
        ("Resource.component.code", "Resource.component", "code"),
        ("Resource.extension", "Resource", "extension"),
    ],
)
def test_element_node_local_and_parent_id(element, id, expected_parent, expected_local):
    element.id = id
    element.path = id
    node = ElementNode(definition=element)
    assert node.parent_id == expected_parent
    assert node.local_id == expected_local

    # ------------------------------------------------------------------
    # Structural flags
    # ------------------------------------------------------------------


@pytest.mark.parametrize(
    "path, expected",
    [
        ("Resource", True),
        ("Resource.name", False),
        ("Resource.value[x]", False),
    ],
)
def test_element_node_is_root(element, path, expected):
    element.path = path
    node = ElementNode(definition=element)
    assert node.is_root == expected


@pytest.mark.parametrize(
    "id, expected",
    [
        ("Resource", False),
        ("Resource.name", False),
        ("Resource.name:surname", True),
        ("Resource.value[x]", False),
        ("Resource.value[x]:valueString", True),
    ],
)
def test_element_node_is_slice(element, id, expected):
    element.id = id
    node = ElementNode(definition=element)
    assert node.is_slice == expected


@pytest.mark.parametrize(
    "slicing, expected",
    [
        (MagicMock(), True),
        (None, False),
    ],
)
def test_element_node_is_slice_entry(element, slicing, expected):
    element.slicing = slicing
    node = ElementNode(definition=element)
    assert node.is_slice_entry == expected


@pytest.mark.parametrize(
    "reference, expected",
    [
        (MagicMock(), True),
        (None, False),
    ],
)
def test_element_node_is_content_reference(element, reference, expected):
    element.contentReference = reference
    node = ElementNode(definition=element)
    assert node.is_content_reference == expected


# ------------------------------------------------------------------
# Slice identity
# ------------------------------------------------------------------


@pytest.mark.parametrize(
    "id, expected",
    [
        ("Resource.name:surname", "surname"),
        ("Resource.value[x]:valueString", "valueString"),
        ("Resource.extension.value[x]:valueString", "valueString"),
    ],
)
def test_element_node_slice_name(element, id, expected):
    element.id = id
    node = ElementNode(definition=element)
    assert node.slice_name == expected


@pytest.mark.parametrize(
    "id, expected",
    [
        ("Resource.name:surname", ["surname"]),
        ("Resource.value[x]:valueString", ["valueString"]),
        ("Resource.extension.value[x]:valueString", ["valueString"]),
        ("Resource.extension:slice.value[x]:valueString", ["slice", "valueString"]),
    ],
)
def test_element_node_slice_ancestry(element, id, expected):
    element.id = id
    node = ElementNode(definition=element)
    assert node.slice_ancestry == expected


@pytest.mark.parametrize(
    "slicing, expected",
    [
        (MagicMock(ordered=True), True),
        (MagicMock(ordered=False), False),
        (MagicMock(ordered=None), False),
    ],
)
def test_element_node_is_slicing_ordered(element, slicing, expected):
    element.slicing = slicing
    node = ElementNode(definition=element)
    assert node.is_slicing_ordered == expected


@pytest.mark.parametrize(
    "slicing, expected",
    [
        (MagicMock(rules="openAtEnd"), "openAtEnd"),
        (MagicMock(rules="open"), "open"),
        (MagicMock(rules="closed"), "closed"),
        (MagicMock(rules=None), "open"),
    ],
)
def test_element_node_slicing_rules(element, slicing, expected):
    element.slicing = slicing
    node = ElementNode(definition=element)
    assert node.slicing_rules == expected


# ------------------------------------------------------------------
# Cardinality
# ------------------------------------------------------------------


@pytest.mark.parametrize(
    "element, expected_min, expected_max",
    [
        (MagicMock(min=0, max="0"), 0, 0),
        (MagicMock(min=0, max="1"), 0, 1),
        (MagicMock(min=1, max="2"), 1, 2),
        (MagicMock(min=0, max="*"), 0, None),
    ],
)
def test_cardinality_constraints(element, expected_min, expected_max):
    node = ElementNode(definition=element)
    assert node.min_cardinality == expected_min
    assert node.max_cardinality == expected_max


@pytest.mark.parametrize(
    "element, expected",
    [
        (MagicMock(min=0), False),
        (MagicMock(min=1), True),
        (MagicMock(min=2), True),
    ],
)
def test_cardinality_is_required(element, expected):
    node = ElementNode(definition=element)
    assert node.is_required == expected


@pytest.mark.parametrize(
    "element, expected",
    [
        (MagicMock(max=0), True),
        (MagicMock(max=1), False),
        (MagicMock(max=2), False),
    ],
)
def test_cardinality_is_prohibited(element, expected):
    node = ElementNode(definition=element)
    assert node.is_prohibited == expected


@pytest.mark.parametrize(
    "element, expected",
    [
        (MagicMock(max="0"), False),
        (MagicMock(max="1"), False),
        (MagicMock(max="2"), True),
        (MagicMock(max="*"), True),
    ],
)
def test_cardinality_is_array(element, expected):
    node = ElementNode(definition=element)
    assert node.is_array == expected


# ------------------------------------------------------------------
# Type helpers
# ------------------------------------------------------------------


@pytest.mark.parametrize(
    "path, expected",
    [
        ("Resource.name", False),
        ("Resource.name[x]", True),
        ("Resource.value[x]", True),
        ("Resource.component.value[x]", True),
        ("Resource.component.code", False),
        ("Resource.extension", False),
    ],
)
def test_element_node_is_polymorphic_type(element, path, expected):
    element.path = path
    node = ElementNode(definition=element)
    assert node.is_polymorphic_type == expected
