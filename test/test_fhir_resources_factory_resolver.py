import pytest
from unittest.mock import ANY, MagicMock, patch

from fhircraft.config import configure, reset_config
from fhircraft.fhir.resources.datatypes.R4.complex.element_definition import (
    ElementDefinition,
    ElementDefinitionType,
)

from fhircraft.fhir.resources.datatypes.R4.complex.element_definition import (
    ElementDefinitionSlicing,
    ElementDefinitionSlicingDiscriminator,
)

from fhircraft.fhir.resources.datatypes.R4.primitive import (
    String,
    Url,
    Integer,
    Uri,
)

from fhircraft.fhir.resources.definitions import StructureDefinitionRegistry
from fhircraft.fhir.resources.factory.element_node import ElementNode
from fhircraft.fhir.resources.factory.exceptions import (
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
        path=String(value=path) if path is not None else String(value=id),
        **kwargs,
    )


def make_node(id: str, path: str | None = None, **kwargs) -> ElementNode:
    """Convenience wrapper — builds an ElementNode directly from kwargs."""
    return ElementNode(definition=make_element(id, path, **kwargs))


def make_base_index(*elements: ElementDefinition) -> DefinitionIndex:
    return DefinitionIndex.from_elements(list(elements))


def make_structure_def(
    *, snapshot_elements=None, differential_elements=None, base_definition=None
):
    """Build a minimal StructureDefinition mock."""
    sd = MagicMock()
    sd.name = String(value="MockProfile")
    sd.url = Url(value="http://example.org/MockProfile")
    sd.baseDefinition = base_definition

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


def make_url_slicing() -> ElementDefinitionSlicing:
    """Return the canonical open-sliced-by-url discriminator found on extension elements."""
    return ElementDefinitionSlicing.model_construct(
        discriminator=[
            ElementDefinitionSlicingDiscriminator.model_construct(
                type="value", path="url"
            )
        ],
        rules="open",
    )


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
            min=1,
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
    "primitive_type",
    ["string", "boolean", "integer", "decimal", "uri", "code", "dateTime"],
)
def test_build_type_node__resolves_sub_elements_on_primitive_types(
    base_index, resolver, primitive_type
):
    node = resolver._build_type_node(
        [primitive_type], "Observation.extension", base_index
    )
    assert isinstance(node, ElementNode)
    assert node.id == "Observation.extension"
    assert node.path == "Observation.extension"


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


def test_build_type_node__raises_error_for_empty_datatypes(base_index, resolver):
    with pytest.raises(DefinitionResolutionError):
        resolver._build_type_node([], "Observation.value", base_index)


def test_build_type_node__returns_first_matching_for_multiple_types(
    base_index, resolver
):
    node = resolver._build_type_node(
        ["Quantity", "CodeableConcept"],
        "Observation.value.coding",
        base_index,
    )
    assert isinstance(node, ElementNode)
    assert node.id == "Observation.value.coding"
    assert node.path == "Observation.value.coding"


def test_build_type_node__skips_non_matching_first_type_for_multiple_types(
    base_index, resolver
):
    node = resolver._build_type_node(
        ["Quantity", "CodeableConcept"],
        "Observation.value.coding",
        base_index,
    )
    # coding is defined on CodeableConcept — verify cardinality comes from that definition
    assert node.min_cardinality == 0
    assert node.max_cardinality is None  # max="*" on CodeableConcept.coding


def test_build_type_node__raises_error_for_all_fhirpath_types(base_index, resolver):
    with pytest.raises(DefinitionResolutionError):
        resolver._build_type_node(
            [
                "http://hl7.org/fhirpath/System.String",
                "http://hl7.org/fhirpath/System.Integer",
            ],
            "Observation.value",
            base_index,
        )


def test_build_type_node__raises_error_when_local_id_absent_in_all_types(
    base_index, resolver
):
    with pytest.raises(DefinitionResolutionError):
        resolver._build_type_node(
            ["string", "integer", "boolean"],
            "Observation.value.nonExistentField",
            base_index,
        )


def test_build_type_node__raises_error_for_no_type_matches(base_index, resolver):
    with pytest.raises(DefinitionResolutionError):
        resolver._build_type_node(
            ["Quantity", "CodeableConcept"],
            "Observation.value.nonExistentField",
            base_index,
        )


def test_build_type_node__preserves_slicing_from_base_type(resolver):
    node = resolver._build_type_node(
        ["CodeableConcept"],
        "Observation.code.extension",
        make_base_index(make_element("Observation", "Observation")),
    )

    assert node is not None
    assert (
        node.definition.slicing is not None
    ), "_build_type_node stripped slicing from CodeableConcept.extension"
    assert node.is_slice_entry, "Type-expanded extension node should be a slice entry"


def test_build_type_node__resolves_extension_element_on_primitive_type(
    base_index, resolver
):
    # BaseResource.status has type 'code' (a primitive); its StructureDefinition
    # carries a snapshot element 'code.extension' that should be resolvable.
    node = resolver._build_type_node(
        ["code"], "BaseResource.status.extension", base_index
    )
    assert isinstance(node, ElementNode)
    assert node.id == "BaseResource.status.extension"
    assert node.path == "BaseResource.status.extension"


def test_build_intermediate_node__resolves_extension_on_primitive_element(resolver):
    index = make_base_index(
        make_element("MyProfile", "MyProfile"),
        make_element(
            "MyProfile.birthDate",
            "MyProfile.birthDate",
            min=0,
            max="1",
            type=[ElementDefinitionType(code="date")],
        ),
    )
    node = resolver._build_intermediate_node("MyProfile.birthDate.extension", index)
    assert node is not None
    assert isinstance(node, ElementNode)
    assert node.id == "MyProfile.birthDate.extension"
    assert node.path == "MyProfile.birthDate.extension"


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


def test_build_intermediate_node__polymorphic_parent_expands_via_first_matching_type(
    resolver,
):
    # Build a base_index that contains a polymorphic value[x] parent
    base_index_with_poly = make_base_index(
        make_element("Observation", "Observation"),
        make_element(
            "Observation.value[x]",
            "Observation.value[x]",
            min=0,
            max="1",
            short="Measurement value",
            type=[
                ElementDefinitionType(code="Quantity"),
                ElementDefinitionType(code="CodeableConcept"),
            ],
        ),
    )
    node = resolver._build_intermediate_node(
        "Observation.value[x].coding", base_index_with_poly
    )
    assert isinstance(node, ElementNode)
    assert node.id == "Observation.value[x].coding"
    assert node.path == "Observation.value[x].coding"


def test_build_intermediate_node__type_choice_id_returns_element_node(resolver):
    base_index_with_poly = make_base_index(
        make_element("Observation", "Observation"),
        make_element(
            "Observation.value[x]",
            "Observation.value[x]",
            min=0,
            max="1",
            short="Measurement value",
            type=[
                ElementDefinitionType(code="Quantity"),
                ElementDefinitionType(code="CodeableConcept"),
            ],
        ),
    )
    node = resolver._build_intermediate_node(
        "Observation.value[x]:valueQuantity", base_index_with_poly
    )
    assert isinstance(node, ElementNode)
    assert node.id == "Observation.value[x]:valueQuantity"


def test_build_intermediate_node__type_choice_id_has_correct_path(resolver):
    base_index_with_poly = make_base_index(
        make_element("Observation", "Observation"),
        make_element(
            "Observation.value[x]",
            "Observation.value[x]",
            min=0,
            max="1",
            type=[
                ElementDefinitionType(code="Quantity"),
                ElementDefinitionType(code="CodeableConcept"),
            ],
        ),
    )
    node = resolver._build_intermediate_node(
        "Observation.value[x]:valueQuantity", base_index_with_poly
    )
    assert node.path == "Observation.value[x]"


def test_build_intermediate_node__type_choice_id_narrows_type_list(resolver):
    base_index_with_poly = make_base_index(
        make_element("Observation", "Observation"),
        make_element(
            "Observation.value[x]",
            "Observation.value[x]",
            min=0,
            max="1",
            type=[
                ElementDefinitionType(code="Quantity"),
                ElementDefinitionType(code="CodeableConcept"),
            ],
        ),
    )
    node = resolver._build_intermediate_node(
        "Observation.value[x]:valueQuantity", base_index_with_poly
    )
    assert node.type_codes == ["Quantity"]


def test_build_intermediate_node__type_choice_id_is_not_polymorphic(resolver):
    base_index_with_poly = make_base_index(
        make_element("Observation", "Observation"),
        make_element(
            "Observation.value[x]",
            "Observation.value[x]",
            min=0,
            max="1",
            type=[
                ElementDefinitionType(code="Quantity"),
                ElementDefinitionType(code="CodeableConcept"),
            ],
        ),
    )
    node = resolver._build_intermediate_node(
        "Observation.value[x]:valueQuantity", base_index_with_poly
    )
    assert node.is_polymorphic_type is False
    assert node.is_type_choice_slice is True


def test_build_intermediate_node__path_lookup_ignores_slices(resolver, base_index):
    base_index.add(
        make_node(id="BaseResource.component:sliceA", path="BaseResource.component")
    )
    base_node = base_index.get("BaseResource.component")
    node = resolver._build_intermediate_node("MyProfile.component:sliceB", base_index)
    assert type(node.definition) is type(base_node.definition)


def test_build_intermediate_node__definition_class_is_same_as_base(
    resolver, base_index
):
    base_node = base_index.get("BaseResource.status")
    node = resolver._build_intermediate_node("MyProfile.status", base_index)
    assert type(node.definition) is type(base_node.definition)


def test_build_intermediate_node__preserves_slicing_from_base(resolver):
    """_build_intermediate_node expands Observation.code.extension from CodeableConcept
    (the parent type) — the resulting node must retain the slicing discriminator."""
    # Base index contains Observation.code typed as CodeableConcept; no .extension entry.
    base_with_code = make_base_index(
        make_element("Observation", "Observation"),
        make_element(
            "Observation.code",
            "Observation.code",
            min=0,
            max="1",
            type=[ElementDefinitionType(code="CodeableConcept")],
        ),
    )

    node = resolver._build_intermediate_node(
        "Observation.code.extension", base_with_code
    )

    assert node is not None
    assert node.definition.slicing is not None, (
        "_build_intermediate_node stripped slicing when expanding "
        "Observation.code.extension from CodeableConcept"
    )
    assert (
        node.is_slice_entry
    ), "Synthesised Observation.code.extension node should be a slice entry"


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


@pytest.mark.parametrize(
    "min, max, base_min, base_max, expected_min, expected_max",
    [
        (None, None, 0, "1", 0, "1"),
        (1, None, 0, "1", 0, "1"),
    ],
)
def test_merge_node_with_base__base_is_constructued(
    resolver, min, max, base_min, base_max, expected_min, expected_max
):
    diff = make_node(id="MyProfile.status", min=min, max=max)
    base = make_node(id="BaseResource.status", min=base_min, max=base_max)
    result = resolver._merge_node_with_base(diff, base)
    assert result.definition.base.min == expected_min
    assert result.definition.base.max == expected_max


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
        make_element(
            "MyProfile.component.code",
            "MyProfile.component.code",
        ),
    ]
    index = resolver._resolve_differential(diff, base_index)
    assert (node := index.get("MyProfile.component"))
    assert node.min_cardinality == 0
    assert node.max_cardinality == None
    assert (node := index.get("MyProfile.component.code"))
    assert node.min_cardinality == 1
    assert node.max_cardinality == 1


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
    assert node.min_cardinality == 1
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


def test_resolve_differential__element_not_in_base_stored_as_is(resolver, base_index):
    new_elem = make_element(
        "MyProfile.brand_new_field",
        "MyProfile.brand_new_field",
        min=0,
        max="1",
        short="Never in base",
    )
    diff = [
        make_element("MyProfile", "MyProfile"),
        new_elem,
    ]
    index = resolver._resolve_differential(diff, base_index)
    stored = index.get("MyProfile.brand_new_field")
    assert stored is not None
    assert stored.definition.short == "Never in base"
    assert stored.min_cardinality == 0
    assert stored.max_cardinality == 1


def test_resolve_differential__element_not_in_base(resolver, base_index):

    new_elem = make_element("MyProfile.novel", "MyProfile.novel", min=1, max="1")
    diff = [
        make_element("MyProfile", "MyProfile"),
        new_elem,
    ]
    with patch.object(
        resolver, "_merge_node_with_base", wraps=resolver._merge_node_with_base
    ) as mock_merge:
        index = resolver._resolve_differential(diff, base_index)

    # _merge_node_with_base must not have been called for the novel element
    novel_calls = [
        c for c in mock_merge.call_args_list if c.args[0].id == "MyProfile.novel"
    ]
    assert novel_calls == []
    # The node is still present in the result
    assert index.get("MyProfile.novel") is not None


def test_resolve_differential__calls_merge_when_base_node_found(resolver, base_index):

    diff = [
        make_element("MyProfile", "MyProfile"),
        make_element("MyProfile.status", "MyProfile.status", min=1),
    ]
    sentinel = make_node(id="MyProfile.status", min=1, max="1")

    with patch.object(
        resolver, "_merge_node_with_base", return_value=sentinel
    ) as mock_merge:
        index = resolver._resolve_differential(diff, base_index)

    # At least one call must have the diff status node and base status node
    assert mock_merge.called
    call_args_list = mock_merge.call_args_list
    # Find the call for MyProfile.status
    status_calls = [c for c in call_args_list if c.args[0].id == "MyProfile.status"]
    assert len(status_calls) == 1
    diff_arg, base_arg = status_calls[0].args
    assert diff_arg.id == "MyProfile.status"
    assert base_arg.id == "BaseResource.status"


def test_resolve_differential__merge_result_is_stored_not_diff_node(
    resolver, base_index
):
    merged_sentinel = make_node(id="MyProfile.status", min=99, max="99")

    diff = [
        make_element("MyProfile", "MyProfile"),
        make_element("MyProfile.status", "MyProfile.status", min=1),
    ]
    with patch.object(resolver, "_merge_node_with_base", return_value=merged_sentinel):
        index = resolver._resolve_differential(diff, base_index)

    stored = index.get("MyProfile.status")
    assert stored is merged_sentinel


def test_resolve_differential__extension_slice_on_complex_field_is_present(resolver):
    # Build a minimal Observation snapshot — only the top-level 'code' field.
    obs_snapshot = [
        make_element("Observation", "Observation"),
        make_element(
            "Observation.code",
            "Observation.code",
            min=0,
            max="1",
            type=[ElementDefinitionType(code="CodeableConcept")],
        ),
    ]
    base_index = make_base_index(*obs_snapshot)

    # The differential introduces a slice on Observation.code.extension.
    diff = [
        make_element("Observation", "Observation"),
        make_element("Observation.code", "Observation.code"),
        make_element("Observation.code.extension", "Observation.code.extension"),
        make_element(
            "Observation.code.extension:mySlice",
            "Observation.code.extension",
            min=0,
            max="1",
            type=[ElementDefinitionType(code="Extension")],
        ),
    ]

    result = resolver._resolve_differential(diff, base_index)

    # The slice entry node must be present and must be recognised as such.
    ext_node = result.get("Observation.code.extension")
    assert (
        ext_node is not None
    ), "Observation.code.extension missing from resolved index"
    assert (
        ext_node.is_slice_entry
    ), "Observation.code.extension must be a slice entry so SlicedFieldBuilder handles it"

    # The named slice must be present in the index.
    assert (
        "Observation.code.extension:mySlice" in result
    ), "Observation.code.extension:mySlice missing — slice was silently dropped"


def test_resolve_differential__slicing_preserved_on_intermediate_complex_type_node(
    resolver,
):
    obs_snapshot = [
        make_element("Observation", "Observation"),
        make_element(
            "Observation.code",
            "Observation.code",
            min=0,
            max="1",
            type=[ElementDefinitionType(code="CodeableConcept")],
        ),
    ]
    base_index = make_base_index(*obs_snapshot)

    diff = [
        make_element("Observation", "Observation"),
        make_element("Observation.code", "Observation.code"),
        make_element("Observation.code.extension", "Observation.code.extension"),
        make_element(
            "Observation.code.extension:mySlice",
            "Observation.code.extension",
            min=1,
            max="1",
            type=[ElementDefinitionType(code="Extension")],
        ),
    ]

    result = resolver._resolve_differential(diff, base_index)

    ext_node = result.get("Observation.code.extension")
    assert ext_node is not None
    assert ext_node.definition.slicing is not None, (
        "slicing was stripped when building the intermediate "
        "Observation.code.extension node from CodeableConcept"
    )


def test_resolve_differential__base_index_has_slice_and_non_sliced_child(
    resolver,
):
    base_snapshot = [
        make_element("Observation", "Observation"),
        make_element(
            "Observation.component",
            "Observation.component",
            min=0,
            max="*",
            type=[ElementDefinitionType(code="BackboneElement")],
        ),
        make_element(
            "Observation.component:conclusion-string",
            "Observation.component",
            min=0,
            max="1",
        ),
        make_element(
            "Observation.component.code",
            "Observation.component.code",
            min=1,
            max="1",
            type=[ElementDefinitionType(code="CodeableConcept")],
        ),
        make_element(
            "Observation.component:conclusion-string.code",
            "Observation.component.code",
            min=1,
            max="1",
        ),
    ]
    base_index = make_base_index(*base_snapshot)

    diff = [
        make_element("MyProfile", "MyProfile"),
        make_element(
            "MyProfile.component",
            "MyProfile.component",
            min=0,
            max="*",
        ),
        make_element(
            "MyProfile.component:sliceA",
            "MyProfile.component",
            min=1,
            max="1",
        ),
        make_element(
            "MyProfile.component:sliceA.code",
            "MyProfile.component.code",
            min=1,
            max="1",
            short="Constrained slice code",
        ),
    ]

    result = resolver._resolve_differential(diff, base_index)
    node = result.get("MyProfile.component:sliceA.code")
    assert node is not None
    assert node.min_cardinality == 1
    assert node.max_cardinality == 1


def test_build_intermediate_node__base_has_named_slice_child_with_same_path(
    resolver,
):
    """Regression: _build_intermediate_node must synthesise a node correctly when
    the base index contains a named-slice child that shares a path with the base
    element ('Observation.component:conclusion-string.code' has path
    'Observation.component.code', same as 'Observation.component.code').

    The intermediate id under test is 'MyProfile.component:sliceA.code':
    its id_segments differ from the base element (contains ':sliceA'), so the
    id-based lookup fails and the resolver falls back to the path-based lookup.
    Before the fix, get_single_by_path found TWO nodes for path
    'Observation.component.code' (the base element plus the conclusion-string
    slice child) and raised DefinitionIndexError."""
    base_snapshot = [
        make_element("Observation", "Observation"),
        make_element(
            "Observation.component",
            "Observation.component",
            min=0,
            max="*",
            type=[ElementDefinitionType(code="BackboneElement")],
        ),
        make_element(
            "Observation.component:conclusion-string",
            "Observation.component",
            min=0,
            max="1",
        ),
        make_element(
            "Observation.component.code",
            "Observation.component.code",
            min=1,
            max="1",
            type=[ElementDefinitionType(code="CodeableConcept")],
        ),
        make_element(
            "Observation.component:conclusion-string.code",
            "Observation.component.code",
            min=1,
            max="1",
        ),
    ]
    base_index = make_base_index(*base_snapshot)

    # :sliceA is not in the base, so id lookup fails and path lookup is used.
    node = resolver._build_intermediate_node(
        "MyProfile.component:sliceA.code", base_index
    )
    assert node is not None
    assert node.id == "MyProfile.component:sliceA.code"
    assert node.path == "MyProfile.component.code"


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
    result = resolver.resolve(sd, mode="snapshot")
    assert isinstance(result, DefinitionIndex)


def test_resolve__snapshot_mode_index_contains_all_elements(resolver, base_index):
    elements = [n.definition for n in base_index.nodes]
    sd = make_structure_def(snapshot_elements=elements)
    result = resolver.resolve(sd, mode="snapshot")
    for elem in elements:
        assert elem.id in result


def test_resolve__snapshot_mode_raises_when_snapshot_is_none(resolver, base_index):
    sd = make_structure_def(snapshot_elements=None)
    with pytest.raises(AssertionError):
        resolver.resolve(sd, mode="snapshot")


def test_resolve__snapshot_mode_raises_when_snapshot_elements_is_none(
    resolver, base_index
):
    sd = make_structure_def(snapshot_elements=None)
    sd.snapshot = MagicMock()
    sd.snapshot.element = None
    with pytest.raises(AssertionError):
        resolver.resolve(sd, mode="snapshot")


def test_resolve__snapshot_mode_raises_when_snapshot_elements_contain_none(
    resolver, base_index
):
    elements = [n.definition for n in base_index.nodes]
    elements.append(None)
    sd = make_structure_def(snapshot_elements=elements)
    with pytest.raises(AssertionError):
        resolver.resolve(sd, mode="snapshot")


# ------------------------------------------------------------------
# mode="differential"
# ------------------------------------------------------------------


def test_resolve__differential_mode_delegates_to_resolve_differential(
    resolver, base_index
):
    diff_elements = [make_element("MyProfile.status", "MyProfile.status")]
    sd = make_structure_def(differential_elements=diff_elements)
    sd.baseDefinition = "http://example.org/BaseResource"

    base_sd = make_structure_def(
        snapshot_elements=[n.definition for n in base_index.nodes]
    )
    resolver._registry.get = MagicMock(return_value=base_sd)

    expected = DefinitionIndex(list(base_index.nodes))
    resolver._resolve_differential = MagicMock(return_value=expected)
    resolver._resolve_content_references = MagicMock(return_value=expected)

    result = resolver.resolve(sd, mode="differential")

    resolver._resolve_differential.assert_called_once_with(diff_elements, ANY)
    resolver._resolve_content_references.assert_called_with(expected)
    assert result is expected


def test_resolve__differential_mode_returns_definition_index(resolver, base_index):
    diff_elements = [make_element("MyProfile.status", "MyProfile.status")]
    sd = make_structure_def(differential_elements=diff_elements)
    sd.baseDefinition = "http://example.org/BaseResource"

    base_sd = make_structure_def(
        snapshot_elements=[n.definition for n in base_index.nodes]
    )
    resolver._registry.get = MagicMock(return_value=base_sd)

    resolver._resolve_differential = MagicMock(
        return_value=DefinitionIndex(list(base_index.nodes))
    )
    resolver._resolve_content_references = MagicMock(
        return_value=DefinitionIndex(list(base_index.nodes))
    )
    result = resolver.resolve(sd, mode="differential")
    assert isinstance(result, DefinitionIndex)


def test_resolve__differential_mode_raises_when_differential_is_none(
    resolver, base_index
):
    sd = make_structure_def(differential_elements=None)
    with pytest.raises(AssertionError):
        resolver.resolve(sd, mode="differential")


def test_resolve__differential_mode_raises_when_differential_elements_is_none(
    resolver, base_index
):
    sd = make_structure_def(differential_elements=None)
    sd.differential = MagicMock()
    sd.differential.element = None
    with pytest.raises(AssertionError):
        resolver.resolve(sd, mode="differential")


def test_resolve__differential_mode_raises_when_differential_elements_contain_none(
    resolver, base_index
):
    diff_elements = [make_element("MyProfile.status", "MyProfile.status"), None]
    sd = make_structure_def(differential_elements=diff_elements)
    with pytest.raises(AssertionError):
        resolver.resolve(sd, mode="differential")


def test_resolve__auto_mode_uses_differential_when_present(resolver, base_index):
    diff_elements = [
        make_element("MyProfile", "MyProfile"),
        make_element("MyProfile.status", "MyProfile.status"),
    ]
    sd = make_structure_def(
        differential_elements=diff_elements,
        base_definition="http://example.org/BaseResource",
    )

    base_sd = make_structure_def(
        snapshot_elements=[n.definition for n in base_index.nodes]
    )
    resolver._registry.get = MagicMock(return_value=base_sd)

    expected = DefinitionIndex(list(base_index.nodes))
    resolver._resolve_differential = MagicMock(return_value=expected)
    resolver._resolve_content_references = MagicMock(return_value=expected)

    result = resolver.resolve(sd, mode="auto")

    resolver._resolve_differential.assert_called_once_with(diff_elements, ANY)
    assert result is expected


def test_resolve__auto_mode_uses_snapshot_when_no_differential(resolver, base_index):
    elements = [n.definition for n in base_index.nodes]
    sd = make_structure_def(snapshot_elements=elements)  # differential=None by default

    result = resolver.resolve(sd, mode="auto")

    assert isinstance(result, DefinitionIndex)


def test_resolve__auto_mode_is_default(resolver, base_index):
    diff_elements = [
        make_element("MyProfile", "MyProfile"),
        make_element("MyProfile.status", "MyProfile.status"),
    ]
    sd = make_structure_def(
        differential_elements=diff_elements,
        base_definition="http://example.org/BaseResource",
    )

    base_sd = make_structure_def(
        snapshot_elements=[n.definition for n in base_index.nodes]
    )
    resolver._registry.get = MagicMock(return_value=base_sd)

    expected = DefinitionIndex(list(base_index.nodes))
    resolver._resolve_differential = MagicMock(return_value=expected)
    resolver._resolve_content_references = MagicMock(return_value=expected)

    result = resolver.resolve(sd)  # no mode kwarg

    resolver._resolve_differential.assert_called_once()
    assert result is expected


def test_resolve__differential_resolves_base_via_registry(resolver, base_index):
    diff_elements = [
        make_element("MyProfile", "MyProfile"),
        make_element("MyProfile.status", "MyProfile.status", min=1),
    ]
    sd = make_structure_def(
        differential_elements=diff_elements,
        base_definition="http://example.org/BaseResource",
    )

    base_sd = make_structure_def(
        snapshot_elements=[n.definition for n in base_index.nodes]
    )
    resolver._registry.get = MagicMock(return_value=base_sd)

    result = resolver.resolve(sd, mode="differential")

    resolver._registry.get.assert_called_once_with("http://example.org/BaseResource")
    assert isinstance(result, DefinitionIndex)
    assert "MyProfile.status" in result


def test_resolve__differential_recursive_chain(resolver, base_index):
    # Deepest base — provides the snapshot for the whole chain.
    root_sd = make_structure_def(
        snapshot_elements=[n.definition for n in base_index.nodes]
    )

    # Mid-level differential: adds min=1 on status.
    mid_diff = [
        make_element("MidProfile", "MidProfile"),
        make_element("MidProfile.status", "MidProfile.status", min=1),
    ]
    mid_sd = make_structure_def(
        differential_elements=mid_diff,
        base_definition="http://example.org/RootResource",
    )

    # Top-level differential: further restricts max="1" on status.
    top_diff = [
        make_element("TopProfile", "TopProfile"),
        make_element("TopProfile.status", "TopProfile.status", max="0"),
    ]
    top_sd = make_structure_def(
        differential_elements=top_diff, base_definition="http://example.org/MidProfile"
    )

    resolver._registry.get = MagicMock(
        side_effect=lambda url: {
            "http://example.org/MidProfile": mid_sd,
            "http://example.org/RootResource": root_sd,
        }[url]
    )

    result = resolver.resolve(top_sd, mode="differential")

    assert isinstance(result, DefinitionIndex)
    node = result.get("TopProfile.status")
    assert node is not None
    assert node.max_cardinality == 0


def test_resolve__differential_raises_when_base_definition_is_missing(resolver):
    sd = make_structure_def(
        differential_elements=[
            make_element("MyProfile", "MyProfile"),
            make_element("MyProfile.status", "MyProfile.status"),
        ]
    )

    with pytest.raises(DefinitionResolutionError):
        resolver.resolve(sd, mode="differential")


def test_resolve__differential_no_snapshot_mismatched_root_falls_back_to_partial(
    resolver, base_index
):
    # Snapshot uses 'BaseResource' as the root.
    root_sd = make_structure_def(
        snapshot_elements=[n.definition for n in base_index.nodes]
    )

    # Mid profile uses a *different* root name ('MidProfile'), which is the
    # non-standard scenario covered by the guard clause.
    mid_diff = [
        make_element("MidProfile", "MidProfile"),
        make_element("MidProfile.status", "MidProfile.status", min=1),
    ]
    mid_sd = make_structure_def(
        differential_elements=mid_diff,
        base_definition="http://example.org/BaseResource",
    )

    top_diff = [
        make_element("TopProfile", "TopProfile"),
        make_element("TopProfile.status", "TopProfile.status", max="0"),
    ]
    top_sd = make_structure_def(
        differential_elements=top_diff,
        base_definition="http://example.org/MidProfile",
    )

    resolver._registry.get = MagicMock(
        side_effect=lambda url: {
            "http://example.org/MidProfile": mid_sd,
            "http://example.org/BaseResource": root_sd,
        }[url]
    )

    # Must not raise a DefinitionIndexError about multiple root candidates.
    result = resolver.resolve(top_sd, mode="differential")

    assert isinstance(result, DefinitionIndex)
    node = result.get("TopProfile.status")
    assert node is not None
    assert node.max_cardinality == 0


def test_resolve__differential_no_snapshot_base_uses_ancestor_snapshot(
    resolver, base_index
):
    # Bottom of the chain — has a real snapshot that includes 'category'.
    root_sd = make_structure_def(
        snapshot_elements=[
            make_element("BaseResource", "BaseResource"),
            make_element(
                "BaseResource.status",
                "BaseResource.status",
                min=0,
                max="1",
                type=[ElementDefinitionType(code="code")],
            ),
            make_element(
                "BaseResource.category",
                "BaseResource.category",
                min=0,
                max="*",
                type=[ElementDefinitionType(code="CodeableConcept")],
            ),
        ]
    )

    # Mid-level: diff-only, only mentions 'status', never mentions 'category'.
    mid_sd = make_structure_def(
        differential_elements=[
            make_element("BaseResource", "BaseResource"),
            make_element("BaseResource.status", "BaseResource.status", min=1),
        ],
        base_definition="http://example.org/BaseResource",
    )

    # Top-level: constrains 'category', which MidProfile never mentioned.
    top_sd = make_structure_def(
        differential_elements=[
            make_element("BaseResource", "BaseResource"),
            make_element("BaseResource.category", "BaseResource.category", min=1),
        ],
        base_definition="http://example.org/MidProfile",
    )

    resolver._registry.get = MagicMock(
        side_effect=lambda url: {
            "http://example.org/MidProfile": mid_sd,
            "http://example.org/BaseResource": root_sd,
        }[url]
    )

    result = resolver.resolve(top_sd, mode="differential")

    assert isinstance(result, DefinitionIndex)
    # category must be present and carry its type from the ancestor snapshot
    category_node = result.get("BaseResource.category")
    assert category_node is not None
    assert category_node.min_cardinality == 1  # overridden by top diff


def test_resolve__differential_no_snapshot_base_preserves_mid_constraints(
    resolver, base_index
):
    root_sd = make_structure_def(
        snapshot_elements=[
            make_element("BaseResource", "BaseResource"),
            make_element(
                "BaseResource.status",
                "BaseResource.status",
                min=0,
                max="1",
                type=[ElementDefinitionType(code="code")],
            ),
            make_element(
                "BaseResource.category",
                "BaseResource.category",
                min=0,
                max="*",
                type=[ElementDefinitionType(code="CodeableConcept")],
            ),
        ]
    )

    # MidProfile raises min on 'status' to 1, never mentions 'category'.
    mid_sd = make_structure_def(
        differential_elements=[
            make_element("BaseResource", "BaseResource"),
            make_element("BaseResource.status", "BaseResource.status", min=1),
        ],
        base_definition="http://example.org/BaseResource",
    )

    # TopProfile restricts 'category' to max="1"; doesn't mention 'status'.
    top_sd = make_structure_def(
        differential_elements=[
            make_element("BaseResource", "BaseResource"),
            make_element("BaseResource.category", "BaseResource.category", max="1"),
        ],
        base_definition="http://example.org/MidProfile",
    )

    resolver._registry.get = MagicMock(
        side_effect=lambda url: {
            "http://example.org/MidProfile": mid_sd,
            "http://example.org/BaseResource": root_sd,
        }[url]
    )

    result = resolver.resolve(top_sd, mode="differential")

    # category must appear with TopProfile's max=1 applied on top of the ancestor
    # type definition (CodeableConcept) which MidProfile never touched.
    category_node = result.get("BaseResource.category")
    assert category_node is not None
    assert category_node.max_cardinality == 1
    # Type must be resolved from the ancestor snapshot, not be empty.
    assert (
        category_node.types
    ), "category node has no types — ancestor snapshot was not used"
    assert any(str(t.code) == "CodeableConcept" for t in category_node.types)


# ==================================================================
# SnapshotResolver._build_full_ancestor_index
# ==================================================================


def test_build_full_ancestor_index__returns_index_from_nearest_snapshot(
    resolver, base_index
):
    snapshot_sd = make_structure_def(
        snapshot_elements=[n.definition for n in base_index.nodes]
    )
    diff_only_sd = make_structure_def(
        differential_elements=[
            make_element("BaseResource", "BaseResource"),
        ],
        base_definition="http://example.org/RootResource",
    )

    resolver._registry.get = MagicMock(return_value=snapshot_sd)

    result = resolver._build_full_ancestor_index(diff_only_sd)

    assert isinstance(result, DefinitionIndex)
    assert result.root().id == "BaseResource"
    assert result.get("BaseResource.status") is not None


def test_build_full_ancestor_index__skips_multiple_snapshotless_ancestors(
    resolver, base_index
):
    # Three-level chain: A (diff-only) → B (diff-only) → C (has snapshot)
    sd_c = make_structure_def(
        snapshot_elements=[n.definition for n in base_index.nodes]
    )
    sd_b = make_structure_def(
        differential_elements=[make_element("BaseResource", "BaseResource")],
        base_definition="http://example.org/C",
    )
    sd_a = make_structure_def(
        differential_elements=[make_element("BaseResource", "BaseResource")],
        base_definition="http://example.org/B",
    )

    resolver._registry.get = MagicMock(
        side_effect=lambda url: {
            "http://example.org/B": sd_b,
            "http://example.org/C": sd_c,
        }[url]
    )

    result = resolver._build_full_ancestor_index(sd_a)

    assert isinstance(result, DefinitionIndex)
    assert result.root().id == "BaseResource"


def test_build_full_ancestor_index__raises_when_chain_has_no_snapshot(resolver):
    sd_b = make_structure_def(
        differential_elements=[make_element("MyProfile", "MyProfile")],
        base_definition=None,  # chain terminates here with no snapshot
    )
    sd_a = make_structure_def(
        differential_elements=[make_element("MyProfile", "MyProfile")],
        base_definition="http://example.org/B",
    )

    resolver._registry.get = MagicMock(return_value=sd_b)

    with pytest.raises(DefinitionResolutionError):
        resolver._build_full_ancestor_index(sd_a)
