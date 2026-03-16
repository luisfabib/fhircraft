import warnings
from typing import Annotated, List, Optional, Union, get_args, get_origin

import pytest
from pydantic.aliases import AliasChoices

from fhircraft.fhir.resources.base import FHIRBaseModel, FHIRSliceModel
from fhircraft.fhir.resources.factory.builders.base import (
    Build,
    ValidatorInformation,
    Builder,
)
from fhircraft.fhir.resources.factory.builders.slices import (
    SlicedFieldBuilder,
    DefinitionIndex,
)
from fhircraft.fhir.resources.validators import validate_slicing_cardinalities
from fhircraft.utils import _get_deepest_args
from unittest.mock import MagicMock

MODEL_ASSEMBLER = "fhircraft.fhir.resources.factory.assembler.ModelAssembler"


class FakeBase(FHIRBaseModel):
    """Concrete base class whose __name__ appears in slice model names."""


class FakeSliceModel(FHIRSliceModel):
    """Concrete FHIRSliceModel subclass returned by the mock assembler."""


class _FakeProfiled(FHIRBaseModel):
    """Simulates a type resolved from a profile URL, e.g. a profiled Extension."""


class _FakeEntryBase(FHIRBaseModel):
    """Simulates the entry-level base resolved from the parent model field (e.g. ObservationComponent)."""


class _FakeSliceBase(FHIRSliceModel):
    """Simulates a FHIR type that already inherits from FHIRSliceModel."""


def make_builder_with_entry_base(entry_base_type: type) -> SlicedFieldBuilder:
    """Return a builder that will resolve *entry_base_type* from its context.base field annotation."""
    from pydantic import BaseModel as PydanticBaseModel

    # Dynamically build a pydantic model that exposes `component` with the right type
    ComponentHolder = type(
        "_ComponentHolder",
        (PydanticBaseModel,),
        {"__annotations__": {"component": Optional[List[entry_base_type]]}},
    )
    ComponentHolder.model_fields  # trigger pydantic field registration

    ctx = MagicMock(name="mock-ctx-with-entry-base")
    ctx.fhir_release = "R4B"
    ctx.base = ComponentHolder
    ctx.resource_name = "TestResource"
    return SlicedFieldBuilder(context=ctx)


# ---------------------------------------------------------------------------
# Helpers & Fixtures
# ---------------------------------------------------------------------------


def make_type_definition(
    type_code: str = "string", fhir_release: str = "R4B", profile=None
):
    td = MagicMock(name=f"mock-type-{type_code}")
    td.code = type_code
    td._fhir_release = fhir_release
    td.profile = [profile] if profile else None
    return td


def make_entry_node(
    name: str = "category",
    path: str | None = None,
    type_codes: list[str] | None = None,
    fhir_release: str = "R4B",
    is_slice_entry: bool = True,
    is_array: bool = True,
    min_cardinality: int = 0,
    max_cardinality: int | None = None,
    documentation: str | None = None,
    short: str | None = None,
    fixed=None,
    pattern=None,
    constraints=None,
    default_value=None,
):
    node = MagicMock(name="mock-entry-node")
    node.name = name
    node.id = path or f"Resource.{name}"
    node.path = path or f"Resource.{name}"
    node.is_slice_entry = is_slice_entry
    node.is_array = is_array
    node.min_cardinality = min_cardinality
    node.max_cardinality = max_cardinality
    node.documentation = documentation
    node.definition.short = short
    node.definition.constraint = constraints or []
    node.fixed = fixed
    node.pattern = pattern
    node.default_value = default_value
    node.max_length = None
    node.min_value = None
    node.max_value = None
    node.types = [
        make_type_definition(code, fhir_release)
        for code in (type_codes if type_codes is not None else ["CodeableConcept"])
    ]
    node.profile_urls = []
    return node


def make_slice_node(
    slice_name: str = "laboratory",
    path: str = "Resource.category:laboratory",
    type_code: str = "CodeableConcept",
    fhir_release: str = "R4B",
    min_cardinality: int = 0,
    max_cardinality: int | None = 1,
    profile_urls: list | None = None,
):
    node = MagicMock(name=f"mock-slice-{slice_name}")
    node.id = path
    node.path = path
    node.slice_name = slice_name
    node.min_cardinality = min_cardinality
    node.max_cardinality = max_cardinality
    node.types = [make_type_definition(type_code, fhir_release)]
    node.profile_urls = profile_urls if profile_urls is not None else []
    return node


def make_index(slices=None, children=None, is_slice_entry_error=False):
    index = MagicMock(name="mock-index")
    index.get_slices.return_value = slices if slices is not None else []
    index.get_subtree.return_value = MagicMock(name="mock-subtree")
    index.get_children.return_value = children if children is not None else []
    if is_slice_entry_error:
        from fhircraft.fhir.resources.factory.index import DefinitionIndexError

        index.get_slices.side_effect = DefinitionIndexError("not a slice entry")
    return index


def make_builder(fhir_release: str = "R4B") -> SlicedFieldBuilder:
    ctx = MagicMock(name="mock-build-context")
    ctx.fhir_release = fhir_release
    ctx.base = FakeBase
    ctx.resource_name = "TestResource"
    return SlicedFieldBuilder(context=ctx)


@pytest.fixture
def builder() -> SlicedFieldBuilder:
    return make_builder()


@pytest.fixture
def index():
    return make_index()


@pytest.fixture
def assembler(monkeypatch):
    """
    Replaces ModelAssembler globally; assemble() returns FakeSliceModel by default.
    """
    mock = MagicMock(name="MockAssembler")
    mock.return_value.assemble.return_value = FakeSliceModel
    monkeypatch.setattr(MODEL_ASSEMBLER, mock)
    return mock


# ===========================================================================
# SlicedFieldBuilder._capitalise_slice_name
# ===========================================================================


def test_capitalise_slice_name__single_word(builder):
    assert builder._capitalise_slice_name("laboratory") == "Laboratory"


def test_capitalise_slice_name__hyphenated_words(builder):
    assert builder._capitalise_slice_name("vital-signs") == "VitalSigns"


def test_capitalise_slice_name__already_capitalised(builder):
    assert builder._capitalise_slice_name("Laboratory") == "Laboratory"


def test_capitalise_slice_name__multiple_hyphens(builder):
    assert (
        builder._capitalise_slice_name("blood-pressure-systolic")
        == "BloodPressureSystolic"
    )


# ===========================================================================
# SlicedFieldBuilder.can_handle
# ===========================================================================


def test_can_handle__returns_true_when_node_is_slice_entry(builder):
    node = make_entry_node(is_slice_entry=True)
    index = make_index(slices=[])
    assert builder.can_handle(node, index) is True


# ===========================================================================
# SlicedFieldBuilder.build
# ===========================================================================


def test_build__returns_build_instance(builder: Builder, index, assembler):
    node = make_entry_node()
    build = builder.build(node, index)
    assert isinstance(build, Build)


def test_build__result_has_exactly_one_field(builder: Builder, index, assembler):
    node = make_entry_node()
    build = builder.build(node, index)
    assert len(build.fields) == 1


def test_build__result_has_exactly_one_validator(builder: Builder, index, assembler):
    node = make_entry_node()
    build = builder.build(node, index)
    assert len(build.validators) == 1


def test_build__field_name_matches_node_name(builder: Builder, index, assembler):
    node = make_entry_node(name="category")
    build = builder.build(node, index)
    assert build.fields[0].name == "category"


def test_build__field_alias_is_node_raw_name(builder: Builder, index, assembler):
    node = make_entry_node(name="category")
    build = builder.build(node, index)
    assert build.fields[0].alias == "category"


def test_build__field_description_is_definition_short(
    builder: Builder, index, assembler
):
    node = make_entry_node(short="Category of observation")
    build = builder.build(node, index)
    assert build.fields[0].description == "Category of observation"


def test_build__field_annotation_is_annotated(builder: Builder, index, assembler):
    node = make_entry_node()
    build = builder.build(node, index)
    origin = get_origin(build.fields[0].annotation)
    assert origin is Union
    # Annotated types have metadata accessible via get_args
    args = get_args(build.fields[0].annotation)
    assert len(args) >= 2  # type + at least one Field metadata


def test_build__field_annotation_union_contains_entry_type(
    builder: Builder, index, assembler
):
    # With no slices the union only contains the resolved entry types
    node = make_entry_node(type_codes=["CodeableConcept"])
    build = builder.build(node, index)
    union_type = get_args(build.fields[0].annotation)[0]
    # The union args should include the resolved Python type for CodeableConcept
    union_args = get_args(union_type)
    assert len(union_args) >= 1


def test_build__no_slices_does_not_call_assembler(builder: Builder, index, assembler):
    node = make_entry_node()
    index.get_slices.return_value = []
    builder.build(node, index)
    assembler.assert_not_called()


def test_build__one_slice_calls_assembler_once(builder: Builder, index, assembler):
    slice_node = make_slice_node()
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    builder.build(node, index)
    assert assembler.call_count == 1


def test_build__two_slices_call_assembler_twice(builder: Builder, index, assembler):
    index.get_slices.return_value = [make_slice_node("a"), make_slice_node("b")]
    node = make_entry_node()
    builder.build(node, index)
    assert assembler.call_count == 2


def test_build__assembler_called_with_slice_subtree(builder: Builder, index, assembler):
    slice_node = make_slice_node(path="Resource.category:laboratory")
    index.get_slices.return_value = [slice_node]
    subtree = MagicMock(name="slice-subtree")
    index.get_subtree.return_value = subtree
    node = make_entry_node()
    builder.build(node, index)
    assert assembler.call_args.kwargs["index"] is subtree


def test_build__assembler_called_with_builder_context(
    builder: Builder, index, assembler
):
    slice_node = make_slice_node()
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    builder.build(node, index)
    assert assembler.call_args.kwargs["ctx"] is builder.context


def test_build__get_subtree_called_with_slice_node_id(
    builder: Builder, index, assembler
):
    slice_node = make_slice_node(path="Resource.category:laboratory")
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    builder.build(node, index)
    index.get_subtree.assert_called_with("Resource.category:laboratory")


def test_build__slice_model_name_uses_context_base_name(
    builder: Builder, index, assembler
):
    slice_node = make_slice_node(slice_name="laboratory")
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    builder.build(node, index)
    called_name = assembler.return_value.assemble.call_args[0][0]
    assert called_name.startswith("TestResource")


def test_build__slice_model_name_capitalises_slice_name(
    builder: Builder, index, assembler
):
    slice_node = make_slice_node(slice_name="laboratory")
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    builder.build(node, index)
    called_name = assembler.return_value.assemble.call_args[0][0]
    assert called_name == "TestResourceLaboratory"


def test_build__slice_model_name_capitalises_hyphenated_slice_name(
    builder: Builder, index, assembler
):
    slice_node = make_slice_node(slice_name="vital-signs")
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    builder.build(node, index)
    called_name = assembler.return_value.assemble.call_args[0][0]
    assert called_name == "TestResourceVitalSigns"


def test_build__slice_model_name_capitalises_camel_case_slice_name(
    builder: Builder, index, assembler
):
    slice_node = make_slice_node(slice_name="vitalSigns")
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    builder.build(node, index)
    called_name = assembler.return_value.assemble.call_args[0][0]
    assert called_name == "TestResourceVitalSigns"


def test_build__slice_min_cardinality_set_on_model(builder: Builder, index, assembler):
    slice_node = make_slice_node(min_cardinality=1, max_cardinality=3)
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    builder.build(node, index)
    assert FakeSliceModel.min_cardinality == 1


def test_build__slice_max_cardinality_set_on_model(builder: Builder, index, assembler):
    slice_node = make_slice_node(min_cardinality=0, max_cardinality=5)
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    builder.build(node, index)
    assert FakeSliceModel.max_cardinality == 5


def test_build__slice_bases_contain_resolved_type(builder: Builder, index, assembler):
    slice_node = make_slice_node(type_code="CodeableConcept")
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    builder.build(node, index)
    bases = assembler.return_value.assemble.call_kwargs["base"]
    # First element is the resolved CodeableConcept type (not FHIRSliceModel)
    assert bases[0] is not FHIRSliceModel


def test_build__annotation_union_contains_slice_model(
    builder: Builder, index, assembler
):
    slice_node = make_slice_node()
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    build = builder.build(node, index)
    union_args = _get_deepest_args(build.fields[0].annotation)
    assert FakeSliceModel in union_args


def test_build__annotation_union_contains_all_slice_models(
    builder: Builder, index, assembler
):
    class FakeSliceA(FHIRSliceModel):
        pass

    class FakeSliceB(FHIRSliceModel):
        pass

    assembler.return_value.assemble.side_effect = [FakeSliceA, FakeSliceB]
    index.get_slices.return_value = [make_slice_node("a"), make_slice_node("b")]
    node = make_entry_node()
    build = builder.build(node, index)
    union_type = get_args(build.fields[0].annotation)[0]
    union_args = _get_deepest_args(union_type)
    assert FakeSliceA in union_args
    assert FakeSliceB in union_args


def test_build__validator_is_ValidatorInformation(builder: Builder, index, assembler):
    node = make_entry_node()
    build = builder.build(node, index)
    assert isinstance(build.validators[0], ValidatorInformation)


def test_build__validator_kind_is_field(builder: Builder, index, assembler):
    node = make_entry_node()
    build = builder.build(node, index)
    assert build.validators[0].kind == "field"


def test_build__validator_function_is_validate_slicing_cardinalities(
    builder: Builder, index, assembler
):
    node = make_entry_node()
    build = builder.build(node, index)
    assert build.validators[0].function is validate_slicing_cardinalities


def test_build__validator_name_references_field_name(
    builder: Builder, index, assembler
):
    node = make_entry_node(name="category")
    build = builder.build(node, index)
    assert "category" in build.validators[0].name


def test_build__validator_arguments_contain_field_name(
    builder: Builder, index, assembler
):
    node = make_entry_node(name="category")
    build = builder.build(node, index)
    assert build.validators[0].arguments["field_name"] == "category"


def test_build__validator_field_matches_safe_name(builder: Builder, index, assembler):
    node = make_entry_node(name="category")
    build = builder.build(node, index)
    assert build.validators[0].field == "category"


def test_build__python_keyword_field_gets_validation_alias(
    index, assembler, monkeypatch
):
    builder = make_builder()
    node = make_entry_node(name="class")
    alias = AliasChoices("class")
    monkeypatch.setattr(
        builder,
        "handle_python_keyword",
        lambda name: ("class_", alias),
    )
    build = builder.build(node, index)
    assert build.fields[0].validation_alias == alias


def test_build__non_keyword_field_has_no_validation_alias(
    builder: Builder, index, assembler
):
    node = make_entry_node(name="category")
    build = builder.build(node, index)
    assert build.fields[0].validation_alias is None


def test_build__raises_assertion_error_when_assembler_returns_non_slice_model(
    builder: Builder, index, assembler
):
    class NotASliceModel(FHIRBaseModel):
        pass

    assembler.return_value.assemble.return_value = NotASliceModel
    slice_node = make_slice_node()
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    with pytest.raises(AssertionError):
        builder.build(node, index)


def test_build__warns_when_slice_has_multiple_types(builder: Builder, index, assembler):
    slice_node = make_slice_node()
    slice_node.types = [
        make_type_definition("CodeableConcept"),
        make_type_definition("string"),
    ]
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        builder.build(node, index)
    assert len(w) == 1
    assert issubclass(w[0].category, UserWarning)


def test_per_slice__profile_urls_causes_resolve_type_to_be_called(
    index, assembler, monkeypatch
):
    """When slice_node.profile_urls is truthy, resolve_type is used for that slice's base."""
    builder = make_builder()
    resolved = MagicMock(type=_FakeProfiled)
    resolve_type_mock = MagicMock(return_value=resolved)
    monkeypatch.setattr(builder, "resolve_type", resolve_type_mock)

    slice_node = make_slice_node(profile_urls=["http://example.org/fhir/profile"])
    index.get_slices.return_value = [slice_node]
    node = make_entry_node(name="component", type_codes=["Extension"])

    builder.build(node, index)

    resolve_type_mock.assert_called()


def test_per_slice__profile_urls_uses_resolved_type_as_slice_base(
    index, assembler, monkeypatch
):
    """Slice base equals the type returned by resolve_type when profile_urls is set."""
    builder = make_builder()
    resolved = MagicMock(type=_FakeProfiled)
    monkeypatch.setattr(builder, "resolve_type", lambda _: resolved)

    slice_node = make_slice_node(profile_urls=["http://example.org/fhir/profile"])
    index.get_slices.return_value = [slice_node]
    node = make_entry_node(name="component", type_codes=["Extension"])

    builder.build(node, index)

    bases = assembler.return_value.assemble.call_args.kwargs["base"]
    assert _FakeProfiled in bases


def test_per_slice__profile_urls_overrides_slice_entry_base(
    index, assembler, monkeypatch
):
    """profile_urls takes precedence: even when slice_entry_base resolves to _FakeEntryBase,
    the profiled type is used as slice base instead."""
    builder = make_builder_with_entry_base(_FakeEntryBase)
    resolved = MagicMock(type=_FakeProfiled)
    monkeypatch.setattr(builder, "resolve_type", lambda _: resolved)

    slice_node = make_slice_node(
        slice_name="profiled",
        path="Resource.component:profiled",
        profile_urls=["http://example.org/fhir/profile"],
    )
    index.get_slices.return_value = [slice_node]
    node = make_entry_node(name="component", type_codes=["Extension"])

    builder.build(node, index)

    bases = assembler.return_value.assemble.call_args.kwargs["base"]
    assert _FakeProfiled in bases
    assert _FakeEntryBase not in bases


def test_per_slice__no_entry_base_and_has_types_calls_resolve_type(
    index, assembler, monkeypatch
):
    """When slice_entry_base is None (no base model, no entry-level type) and the
    slice node has types, resolve_type is invoked for the slice's type."""
    ctx = MagicMock(name="mock-ctx-no-base")
    ctx.fhir_release = "R4B"
    ctx.base = None
    ctx.resource_name = "TestResource"
    builder = SlicedFieldBuilder(context=ctx)

    resolved = MagicMock(type=_FakeProfiled)
    resolve_type_mock = MagicMock(return_value=resolved)
    monkeypatch.setattr(builder, "resolve_type", resolve_type_mock)

    slice_node = make_slice_node(type_code="CodeableConcept")
    index.get_slices.return_value = [slice_node]
    # No types on the entry node → entry-level fallback also stays None,
    # so the per-slice elif fires.
    node = make_entry_node(name="category", type_codes=[])

    builder.build(node, index)

    resolve_type_mock.assert_called_with(slice_node.types[0])


def test_per_slice__no_entry_base_uses_resolved_type_as_slice_base(
    index, assembler, monkeypatch
):
    """slice_base is the type resolved from the slice node when slice_entry_base is None."""
    ctx = MagicMock(name="mock-ctx-no-base")
    ctx.fhir_release = "R4B"
    ctx.base = None
    ctx.resource_name = "TestResource"
    builder = SlicedFieldBuilder(context=ctx)

    resolved = MagicMock(type=_FakeProfiled)
    monkeypatch.setattr(builder, "resolve_type", lambda _: resolved)

    slice_node = make_slice_node(type_code="CodeableConcept")
    index.get_slices.return_value = [slice_node]
    # No types on the entry node keeps slice_entry_base=None so the per-slice elif fires.
    node = make_entry_node(name="category", type_codes=[])

    builder.build(node, index)

    bases = assembler.return_value.assemble.call_args.kwargs["base"]
    assert _FakeProfiled in bases


def test_per_slice__entry_base_used_when_no_profile_urls(index, assembler, monkeypatch):
    """When slice_entry_base is resolved and slice has no profile_urls, it is reused."""
    builder = make_builder_with_entry_base(_FakeEntryBase)

    # resolve_type should NOT be called for the per-slice branch in this case
    resolve_type_spy = MagicMock(
        side_effect=AssertionError("resolve_type must not be called per-slice")
    )
    monkeypatch.setattr(builder, "resolve_type", resolve_type_spy)

    slice_node = make_slice_node(profile_urls=[])
    index.get_slices.return_value = [slice_node]
    node = make_entry_node(name="component", type_codes=["BackboneElement"])

    builder.build(node, index)

    bases = assembler.return_value.assemble.call_args.kwargs["base"]
    assert _FakeEntryBase in bases


def test_per_slice__entry_base_does_not_call_resolve_type_per_slice(
    index, assembler, monkeypatch
):
    """When slice_entry_base is non-None and no profile_urls, resolve_type is never invoked."""
    builder = make_builder_with_entry_base(_FakeEntryBase)
    resolve_type_mock = MagicMock(return_value=MagicMock(type=_FakeProfiled))
    monkeypatch.setattr(builder, "resolve_type", resolve_type_mock)

    slice_node = make_slice_node(profile_urls=[])
    index.get_slices.return_value = [slice_node]
    node = make_entry_node(name="component", type_codes=["BackboneElement"])

    builder.build(node, index)

    resolve_type_mock.assert_not_called()


def test_per_slice__fhirslicemodel_base_not_duplicated_in_bases(
    index, assembler, monkeypatch
):
    """When slice_base already inherits from FHIRSliceModel, it is not re-added."""
    builder = make_builder()
    monkeypatch.setattr(
        builder, "resolve_type", lambda _: MagicMock(type=_FakeSliceBase)
    )

    slice_node = make_slice_node()
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()

    builder.build(node, index)

    bases = assembler.return_value.assemble.call_args.kwargs["base"]
    assert bases == (_FakeSliceBase,)


def test_per_slice__non_fhirslicemodel_base_gets_fhirslicemodel_appended(
    index, assembler, monkeypatch
):
    """When slice_base does NOT inherit from FHIRSliceModel, FHIRSliceModel is appended."""
    builder = make_builder()
    monkeypatch.setattr(
        builder, "resolve_type", lambda _: MagicMock(type=_FakeEntryBase)
    )

    slice_node = make_slice_node()
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()

    builder.build(node, index)

    bases = assembler.return_value.assemble.call_args.kwargs["base"]
    assert _FakeEntryBase in bases
    assert FHIRSliceModel in bases


def test_per_slice__fhirslicemodel_itself_as_base_not_duplicated(
    index, assembler, monkeypatch
):
    """Passing FHIRSliceModel itself as the base should result in a single-element tuple."""
    builder = make_builder()
    monkeypatch.setattr(
        builder, "resolve_type", lambda _: MagicMock(type=FHIRSliceModel)
    )

    slice_node = make_slice_node()
    index.get_slices.return_value = [slice_node]
    node = make_entry_node()

    builder.build(node, index)

    bases = assembler.return_value.assemble.call_args.kwargs["base"]
    assert bases == (FHIRSliceModel,)


def test_per_slice__assert_fires_when_slice_base_is_not_a_type(
    index, assembler, monkeypatch
):
    """An AssertionError is raised when slice_base resolves to a non-type value."""
    ctx = MagicMock(name="mock-ctx-no-base")
    ctx.fhir_release = "R4B"
    ctx.base = None
    ctx.resource_name = "TestResource"
    builder = SlicedFieldBuilder(context=ctx)

    # resolve_type returns an instance (not a class)
    monkeypatch.setattr(builder, "resolve_type", lambda _: MagicMock(type="not-a-type"))

    slice_node = make_slice_node(type_code="CodeableConcept")
    index.get_slices.return_value = [slice_node]
    node = make_entry_node(name="category", type_codes=["CodeableConcept"])

    with pytest.raises(AssertionError):
        builder.build(node, index)
