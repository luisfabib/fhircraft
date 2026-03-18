"""Unit tests for FHIRModelFactory (core.py)."""

from __future__ import annotations

from pydantic import Field
from unittest.mock import MagicMock, patch

import pytest

from fhircraft.fhir.resources.factory.core import FHIRModelFactory
from fhircraft.fhir.resources.factory.exceptions import DefinitionResolutionError

# Patch targets
_SNAPSHOT_RESOLVER = "fhircraft.fhir.resources.factory.core.SnapshotResolver"
_MODEL_ASSEMBLER = "fhircraft.fhir.resources.factory.core.ModelAssembler"
_GET_FHIR_TYPE_BY_URL = "fhircraft.fhir.resources.factory.core.get_fhir_type_by_url"
_GET_FHIR_TYPE = "fhircraft.fhir.resources.factory.core.get_fhir_type"
_GET_FHIR_RELEASE = (
    "fhircraft.fhir.resources.factory.core.get_FHIR_release_from_version"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_sd(
    name: str = "MyProfile",
    url: str = "http://example.org/fhir/StructureDefinition/MyProfile",
    fhir_version: str = "4.3.0",
    base_definition: str | None = None,
    kind: str = "resource",
    abstract: bool = False,
    resource_type: str = "StructureDefinition",
    sd_type: str | None = None,
):
    sd = MagicMock(name="mock-sd")
    sd._resource_type = resource_type
    sd.name = name
    sd.url = url
    sd.fhirVersion = fhir_version
    sd.baseDefinition = base_definition
    sd.kind = kind
    sd.abstract = abstract
    sd.type = sd_type or name
    return sd


def make_registry():
    registry = MagicMock(name="mock-repository")
    registry.fhir_release = "R4"
    registry.get.return_value = make_sd()
    return registry


def make_factory(registry=None) -> FHIRModelFactory:
    return FHIRModelFactory(fhir_release="R4", registry=registry)


def make_pydantic_model():
    """Return a minimal mock that looks enough like a type for _build assertions."""
    from fhircraft.fhir.resources.base import FHIRBaseModel

    class MyProfileModel(FHIRBaseModel):
        field: str = Field(...)

    return MyProfileModel


@pytest.fixture
def factory():
    return make_factory()


# ===========================================================================
# FHIRModelFactory._sanitize_name
# ===========================================================================


def test_sanitize_name__normal_name_returned_unchanged():
    assert FHIRModelFactory._sanitize_name("Observation") == "Observation"


def test_sanitize_name__first_char_uppercased():
    assert FHIRModelFactory._sanitize_name("observation") == "Observation"


def test_sanitize_name__strips_non_alphanumeric_chars():
    assert FHIRModelFactory._sanitize_name("My-Profile!") == "MyProfile"


def test_sanitize_name__strips_leading_digits():
    assert FHIRModelFactory._sanitize_name("99Obs") == "Obs"


def test_sanitize_name__empty_after_stripping_raises_value_error():
    with pytest.raises(ValueError):
        FHIRModelFactory._sanitize_name("---")


def test_sanitize_name__hyphens_stripped():
    assert FHIRModelFactory._sanitize_name("bp-measurement") == "BpMeasurement"


# ===========================================================================
# FHIRModelFactory.reset_cache
# ===========================================================================


def test_reset_cache__empties_construction_cache(factory):
    factory.construction_cache["http://example.org/X"] = MagicMock()  # type: ignore
    factory.reset_cache()
    assert factory.construction_cache == {}


# ===========================================================================
# FHIRModelFactory.build – cache behaviour
# ===========================================================================


def test_build__returns_cached_model_on_second_call(factory):
    sd = make_sd()
    cached_model = make_pydantic_model()
    factory.construction_cache[sd.url] = cached_model

    # _normalise_structure_definition will be called; it should return the sd
    with patch.object(factory, "_normalise_structure_definition", return_value=sd):
        result = factory.build(sd)

    assert result is cached_model


def test_build__does_not_call_build_internal_when_cached(factory):
    sd = make_sd()
    factory.construction_cache[sd.url] = make_pydantic_model()

    with (
        patch.object(factory, "_normalise_structure_definition", return_value=sd),
        patch.object(factory, "_build") as mock_internal,
    ):
        factory.build(sd)

    mock_internal.assert_not_called()


def test_build__calls_build_internal_when_not_cached(factory):
    sd = make_sd()
    model = make_pydantic_model()

    with (
        patch.object(factory, "_normalise_structure_definition", return_value=sd),
        patch.object(factory, "_build", return_value=model) as mock_internal,
    ):
        factory.build(sd)

    mock_internal.assert_called_once_with(sd, mixins=None, mode="auto")


def test_build__passes_mixins_to_build_internal(factory):
    sd = make_sd()
    model = make_pydantic_model()
    mixin = MagicMock()

    with (
        patch.object(factory, "_normalise_structure_definition", return_value=sd),
        patch.object(factory, "_build", return_value=model) as mock_internal,
    ):
        factory.build(sd, mixins=[mixin])

    mock_internal.assert_called_once_with(sd, mixins=[mixin], mode="auto")


# ===========================================================================
# FHIRModelFactory._normalise_structure_definition
# ===========================================================================


def test_normalise_structure_definition__sd_object_added_to_repository_and_returned():
    registry = make_registry()
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")
    sd = make_sd()
    result = factory._normalise_structure_definition(registry, sd)
    registry.add.assert_called_once_with(sd)
    assert result is sd


# ===========================================================================
# FHIRModelFactory._build – validation
# ===========================================================================


def test_build_internal__raises_value_error_when_name_is_missing(factory):
    sd = make_sd(name="", fhir_version="4.3.0")
    with pytest.raises(ValueError, match="name"):
        factory._build(sd)


def test_build_internal__raises_value_error_when_fhir_version_is_missing(factory):
    sd = make_sd(fhir_version="")
    with pytest.raises(ValueError, match="fhirVersion"):
        factory._build(sd)


# ===========================================================================
# FHIRModelFactory._build – assembler delegation
# ===========================================================================


def _make_build_mocks(base_sd=None):
    """Return a configured set of patches for the _build happy path."""
    from fhircraft.fhir.resources.base import FHIRBaseModel

    index_mock = MagicMock(name="mock-index")
    model = make_pydantic_model()

    resolver_mock = MagicMock(name="MockSnapshotResolver")
    resolver_mock.return_value.resolve.return_value = index_mock

    assembler_mock = MagicMock(name="MockModelAssembler")
    assembler_mock.return_value.assemble.return_value = model

    base_sd_mock = base_sd or make_sd(
        name="BaseResource",
        url="http://hl7.org/fhir/StructureDefinition/DomainResource",
    )
    base_sd_mock.snapshot = MagicMock()
    base_sd_mock.snapshot.element = [MagicMock()]

    return resolver_mock, assembler_mock, base_sd_mock, model


def test_build_internal__calls_assembler_with_sanitized_name():
    factory = make_factory()
    sd = make_sd(name="my-profile", base_definition=None)
    model = make_pydantic_model()

    with (
        patch(_GET_FHIR_RELEASE, return_value="R4B"),
        patch(_SNAPSHOT_RESOLVER) as mock_resolver,
        patch(_MODEL_ASSEMBLER) as mock_assembler,
    ):
        mock_resolver.return_value.resolve.return_value = MagicMock()
        mock_assembler.return_value.assemble.return_value = model
        factory._build(sd)

    called_name = mock_assembler.return_value.assemble.call_args[0][0]
    assert called_name == "MyProfile"


def test_build_internal__result_is_cached_by_url(factory):
    sd = make_sd(base_definition=None)
    model = make_pydantic_model()

    with (
        patch(_GET_FHIR_RELEASE, return_value="R4B"),
        patch(_SNAPSHOT_RESOLVER) as mock_resolver,
        patch(_MODEL_ASSEMBLER) as mock_assembler,
    ):
        mock_resolver.return_value.resolve.return_value = MagicMock()
        mock_assembler.return_value.assemble.return_value = model
        factory._build(sd)

    assert factory.construction_cache.get(sd.url) is model


def test_build_internal__returns_assembled_model(factory):
    sd = make_sd(base_definition=None)
    model = make_pydantic_model()

    with (
        patch(_GET_FHIR_RELEASE, return_value="R4B"),
        patch(_SNAPSHOT_RESOLVER) as mock_resolver,
        patch(_MODEL_ASSEMBLER) as mock_assembler,
    ):
        mock_resolver.return_value.resolve.return_value = MagicMock()
        mock_assembler.return_value.assemble.return_value = model
        result = factory._build(sd)

    assert result is model


def test_build_internal__assembler_receives_resolver_output_as_index(factory):
    sd = make_sd(base_definition=None)
    index = MagicMock(name="resolved-index")
    model = make_pydantic_model()

    with (
        patch(_GET_FHIR_RELEASE, return_value="R4B"),
        patch(_SNAPSHOT_RESOLVER) as mock_resolver,
        patch(_MODEL_ASSEMBLER) as mock_assembler,
    ):
        mock_resolver.return_value.resolve.return_value = index
        mock_assembler.return_value.assemble.return_value = model
        factory._build(sd)

    assert mock_assembler.call_args.kwargs["index"] is index


def test_build_internal__snapshot_resolver_receives_repository(factory):
    sd = make_sd(base_definition=None)
    model = make_pydantic_model()

    with (
        patch(_GET_FHIR_RELEASE, return_value="R4B"),
        patch(_SNAPSHOT_RESOLVER) as mock_resolver,
        patch(_MODEL_ASSEMBLER) as mock_assembler,
    ):
        mock_resolver.return_value.resolve.return_value = MagicMock()
        mock_assembler.return_value.assemble.return_value = model
        factory._build(sd)

    assert mock_resolver.call_args[0][0] is factory.definition_registry


def test_build_internal__uses_registry_type_as_base_when_available():
    from fhircraft.fhir.resources.base import FHIRBaseModel

    class RegistryBase(FHIRBaseModel):
        pass

    factory = make_factory()
    sd = make_sd(base_definition="http://hl7.org/fhir/StructureDefinition/Observation")
    model = make_pydantic_model()

    base_sd = MagicMock()
    base_sd.snapshot = MagicMock()
    base_sd.snapshot.element = [MagicMock()]
    factory.definition_registry = MagicMock()  # type: ignore
    factory.definition_registry.get.return_value = base_sd  # type: ignore

    with (
        patch(_GET_FHIR_RELEASE, return_value="R4B"),
        patch(_GET_FHIR_TYPE_BY_URL, return_value=RegistryBase),
        patch(_SNAPSHOT_RESOLVER) as mock_resolver,
        patch(_MODEL_ASSEMBLER) as mock_assembler,
    ):
        mock_resolver.return_value.resolve.return_value = MagicMock()
        mock_assembler.return_value.assemble.return_value = model
        factory._build(sd)

    ctx_arg = mock_assembler.call_args.kwargs["ctx"]
    assert ctx_arg.base is RegistryBase


def test_build_internal__context_factory_is_self(factory):
    sd = make_sd(base_definition=None)
    model = make_pydantic_model()

    with (
        patch(_GET_FHIR_RELEASE, return_value="R4B"),
        patch(_SNAPSHOT_RESOLVER) as mock_resolver,
        patch(_MODEL_ASSEMBLER) as mock_assembler,
    ):
        mock_resolver.return_value.resolve.return_value = MagicMock()
        mock_assembler.return_value.assemble.return_value = model
        factory._build(sd)

    ctx_arg = mock_assembler.call_args.kwargs["ctx"]
    assert ctx_arg.factory is factory


def test_build_internal__fhir_release_set_on_model():
    from fhircraft.fhir.resources.base import FHIRBaseModel

    factory = make_factory()
    sd = make_sd(base_definition=None)

    class ModelWithAttrs(FHIRBaseModel):
        pass

    with (
        patch(_GET_FHIR_RELEASE, return_value="R4B"),
        patch(_SNAPSHOT_RESOLVER) as mock_resolver,
        patch(_MODEL_ASSEMBLER) as mock_assembler,
    ):
        mock_resolver.return_value.resolve.return_value = MagicMock()
        mock_assembler.return_value.assemble.return_value = ModelWithAttrs
        factory._build(sd)

    assert ModelWithAttrs._fhir_release == "R4B"


def test_build_internal__canonical_url_set_on_model():
    from fhircraft.fhir.resources.base import FHIRBaseModel

    factory = make_factory()
    sd = make_sd(url="http://example.org/X", base_definition=None)

    class M(FHIRBaseModel):
        pass

    with (
        patch(_GET_FHIR_RELEASE, return_value="R4B"),
        patch(_SNAPSHOT_RESOLVER) as mock_resolver,
        patch(_MODEL_ASSEMBLER) as mock_assembler,
    ):
        mock_resolver.return_value.resolve.return_value = MagicMock()
        mock_assembler.return_value.assemble.return_value = M
        factory._build(sd)

    assert M._canonical_url == "http://example.org/X"


# ===========================================================================
# FHIRModelFactory.register
# ===========================================================================


def test_register__dict_is_added_to_registry_and_returns_sd():
    registry = make_registry()
    sd = make_sd()
    registry.from_dict.return_value = sd
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")

    result = factory.register({"resourceType": "StructureDefinition"})

    registry.from_dict.assert_called_once()
    assert result is sd


def test_register__sd_object_is_added_to_registry_and_returned():
    registry = make_registry()
    sd = make_sd()
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")

    result = factory.register(sd)

    registry.add.assert_called_once_with(sd)
    assert result is sd


def test_register__invalid_input_raises_value_error():
    factory = make_factory()
    with pytest.raises(ValueError):
        factory.register(object())  # type: ignore


# ===========================================================================
# FHIRModelFactory.register_package
# ===========================================================================


def test_register_package__delegates_to_registry():
    registry = make_registry()
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")
    factory.register_package("hl7.fhir.us.core", "5.0.1")
    registry.download_package.assert_called_once_with("hl7.fhir.us.core", "5.0.1")


# ===========================================================================
# FHIRModelFactory.reset_cache
# (basic test already covered above; additional assertion tested here)
# ===========================================================================


def test_reset_cache__multiple_entries_all_removed(factory):
    factory.construction_cache["http://a.org/A"] = MagicMock()  # type: ignore
    factory.construction_cache["http://a.org/B"] = MagicMock()  # type: ignore
    factory.reset_cache()
    assert len(factory.construction_cache) == 0


# ===========================================================================
# FHIRModelFactory.has_definition / get_definition / list_definitions
# ===========================================================================


def test_has_definition__true_when_url_in_registry():
    registry = make_registry()
    registry.__contains__ = MagicMock(return_value=True)
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")
    assert factory.has_registered_definition("http://example.org/X") is True


def test_has_registered_definition__false_when_url_not_in_registry():
    registry = make_registry()
    registry.__contains__ = MagicMock(return_value=False)
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")
    assert factory.has_registered_definition("http://example.org/missing") is False


def test_get_registered_definition__delegates_to_registry_get():
    registry = make_registry()
    sd = make_sd()
    registry.get.return_value = sd
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")

    result = factory.get_registered_definition("http://example.org/X")

    registry.get.assert_called_once_with("http://example.org/X")
    assert result is sd


def test_list_registered_definitions__returns_all_urls_when_no_kind_filter():
    registry = make_registry()
    sd_a = make_sd(url="http://example.org/A", kind="resource")
    sd_b = make_sd(url="http://example.org/B", kind="complex-type")
    registry.structure_definitions_by_url = {
        "http://example.org/A": sd_a,
        "http://example.org/B": sd_b,
    }
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")

    result = factory.list_registered_definitions()

    assert sorted(result) == ["http://example.org/A", "http://example.org/B"]


def test_list_registered_definitions__filters_by_kind():
    registry = make_registry()
    sd_a = make_sd(url="http://example.org/A", kind="resource")
    sd_b = make_sd(url="http://example.org/B", kind="complex-type")
    registry.structure_definitions_by_url = {
        "http://example.org/A": sd_a,
        "http://example.org/B": sd_b,
    }
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")

    result = factory.list_registered_definitions(kind="resource")

    assert result == ["http://example.org/A"]


# ===========================================================================
# FHIRModelFactory.unregister
# ===========================================================================


def test_remove_definition__removes_from_registry_dict():
    registry = make_registry()
    sd = make_sd(url="http://example.org/X")
    registry.structure_definitions_by_url = {"http://example.org/X": sd}
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")
    factory.construction_cache["http://example.org/X"] = MagicMock()  # type: ignore

    factory.unregister("http://example.org/X")

    assert "http://example.org/X" not in registry.structure_definitions_by_url
    assert "http://example.org/X" not in factory.construction_cache


def test_remove_definition__no_op_when_url_absent():
    registry = make_registry()
    registry.structure_definitions_by_url = {}
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")
    # Should not raise
    factory.unregister("http://example.org/nonexistent")


# ===========================================================================
# FHIRModelFactory.is_built / list_built / evict / rebuild
# ===========================================================================


def test_is_built__true_when_url_in_cache(factory):
    factory.construction_cache["http://example.org/X"] = MagicMock()  # type: ignore
    assert factory.is_built("http://example.org/X") is True


def test_is_built__false_when_url_not_in_cache(factory):
    assert factory.is_built("http://example.org/missing") is False


def test_list_built__returns_all_cached_urls(factory):
    factory.construction_cache["http://example.org/A"] = MagicMock()  # type: ignore
    factory.construction_cache["http://example.org/B"] = MagicMock()  # type: ignore
    listed = factory.list_built()
    assert set(listed) == {"http://example.org/A", "http://example.org/B"}


def test_evict__removes_url_from_cache(factory):
    factory.construction_cache["http://example.org/X"] = MagicMock()  # type: ignore
    factory.evict("http://example.org/X")
    assert "http://example.org/X" not in factory.construction_cache


def test_evict__noop_when_url_absent(factory):
    # Should not raise
    factory.evict("http://example.org/nonexistent")


def test_rebuild__evicts_then_builds(factory):
    url = "http://example.org/X"
    model = make_pydantic_model()
    factory.construction_cache[url] = make_pydantic_model()  # type: ignore

    with patch.object(factory, "build", return_value=model) as mock_build:
        result = factory.rebuild(url, mode="snapshot")

    assert (
        url not in factory.construction_cache
        or factory.construction_cache[url] is model
    )
    mock_build.assert_called_once_with(canonical_url=url, mixins=None, mode="snapshot")
    assert result is model


# ===========================================================================
# FHIRModelFactory.enable/disable_internet_access
# ===========================================================================


def test_enable_internet_access__delegates_to_registry():
    registry = make_registry()
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")
    factory.enable_internet_access()
    registry.enable_internet_access.assert_called_once()


def test_disable_internet_access__delegates_to_registry():
    registry = make_registry()
    factory = FHIRModelFactory(registry=registry, fhir_release="R4")
    factory.disable_internet_access()
    registry.disable_internet_access.assert_called_once()
