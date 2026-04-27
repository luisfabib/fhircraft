"""Unit and integration tests for core FHIRMappingEngine methods."""

from __future__ import annotations

import logging

import pytest
from pydantic import BaseModel

from fhircraft.fhir.mapper.engine.core import (
    ArbitraryModel,
    FHIRMappingEngine,
    StructureMapModelMode,
)
from fhircraft.fhir.mapper.engine.registry import StructureMapNotFoundError
from fhircraft.fhir.resources.datatypes.R5.core.structure_map import (
    StructureMap,
    StructureMapGroup,
    StructureMapGroupInput,
    StructureMapStructure,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _group(name: str) -> StructureMapGroup:
    """Minimal group with only a source input — avoids needing a typed target model."""
    return StructureMapGroup(
        name=name,
        typeMode="none",
        input=[
            StructureMapGroupInput(name="src", mode="source"),
        ],
        rule=[],
    )


def _sm(url: str, group_names=None) -> StructureMap:
    return StructureMap(
        url=url,
        name=url.split("/")[-1],
        status="active",
        group=[_group(n) for n in (group_names or [])],
    )


def _main_map(import_urls: list[str]) -> StructureMap:
    return StructureMap(
        url="http://example.org/Main",
        name="Main",
        status="active",
        import_=import_urls,  # type: ignore[attr-defined]
        group=[_group("main")],
    )


def _engine(maps=None) -> FHIRMappingEngine:
    engine = FHIRMappingEngine()
    for sm in maps or []:
        engine.structure_map_registry.add(sm)
    return engine


# ---------------------------------------------------------------------------
# FHIRMappingEngine.execute() - Import resolution
# ---------------------------------------------------------------------------


def test_execute__raises_structure_map_not_found_when_import_not_registered():
    engine = _engine()
    with pytest.raises(StructureMapNotFoundError, match="http://example.org/Missing"):
        engine.execute(_main_map(["http://example.org/Missing"]), ({"x": 1},))


def test_execute__no_error_when_all_imports_are_registered():
    imported = _sm("http://example.org/Imported")
    engine = _engine(maps=[imported])
    result = engine.execute(_main_map(["http://example.org/Imported"]), ({"x": 1},))
    assert isinstance(result, tuple)


def test_execute__multiple_imports_all_registered():
    sm1 = _sm("http://example.org/LibA")
    sm2 = _sm("http://example.org/LibB")
    engine = _engine(maps=[sm1, sm2])
    result = engine.execute(
        _main_map(["http://example.org/LibA", "http://example.org/LibB"]),
        ({"x": 1},),
    )
    assert isinstance(result, tuple)


def test_execute__multiple_imports_one_missing_raises():
    sm1 = _sm("http://example.org/LibA")
    engine = _engine(maps=[sm1])
    with pytest.raises(StructureMapNotFoundError, match="http://example.org/LibB"):
        engine.execute(
            _main_map(["http://example.org/LibA", "http://example.org/LibB"]),
            ({"x": 1},),
        )


def test_execute__wildcard_import_matches_registered_maps():
    sm1 = _sm("http://example.org/datatypes/CD")
    sm2 = _sm("http://example.org/datatypes/TS")
    engine = _engine(maps=[sm1, sm2])
    result = engine.execute(_main_map(["http://example.org/datatypes/*"]), ({"x": 1},))
    assert isinstance(result, tuple)


def test_execute__wildcard_no_match_logs_warning_and_continues(caplog):
    engine = _engine()
    with caplog.at_level(logging.WARNING, logger="fhircraft.fhir.mapper.engine.core"):
        result = engine.execute(
            _main_map(["http://example.org/nomatch/*"]), ({"x": 1},)
        )
    assert any("matched no registered" in r.message for r in caplog.records)
    assert isinstance(result, tuple)


def test_execute__imported_map_groups_are_in_scope(caplog):
    imported = _sm("http://example.org/Lib", group_names=["helperGroup"])
    engine = _engine(maps=[imported])

    executed_map = _main_map(["http://example.org/Lib"])
    # Execute with an empty main group (no rules) — just check scope availability
    result = engine.execute(executed_map, ({"x": 1},))
    assert isinstance(result, tuple)


def test_execute__versioned_import_url_resolves_to_base_url():
    sm = _sm("http://example.org/Lib")
    engine = _engine(maps=[sm])
    # Import with explicit version
    result = engine.execute(_main_map(["http://example.org/Lib|1.0.0"]), ({"x": 1},))
    assert isinstance(result, tuple)


# ---------------------------------------------------------------------------
# _resolve_structure_definitions
# ---------------------------------------------------------------------------


def _sm_structs(structures: list[StructureMapStructure]) -> StructureMap:
    """StructureMap carrying only a minimal group and the given structure list."""
    return StructureMap(
        url="http://example.org/Test",
        name="Test",
        status="active",
        structure=structures,
        group=[_group("main")],
    )


def test_resolve__no_structures_returns_empty_dict():
    """None structure list → empty dict (arbitrary data allowed)."""
    engine = FHIRMappingEngine()
    sm = StructureMap(
        url="http://example.org/Test",
        name="Test",
        status="active",
        structure=None,
        group=[_group("main")],
    )
    result = engine._resolve_structure_definitions(sm, StructureMapModelMode.SOURCE)
    assert result == {}


def test_resolve__empty_structure_list_returns_empty_dict():
    """Empty structure list is falsy and should return an empty dict."""
    engine = FHIRMappingEngine()
    sm = _sm_structs([])
    result = engine._resolve_structure_definitions(sm, StructureMapModelMode.SOURCE)
    assert result == {}


def test_resolve__core_fhir_type_returns_actual_class():
    """A canonical URL under hl7.org/fhir/StructureDefinition/ resolves to the real type."""
    engine = FHIRMappingEngine()
    sm = _sm_structs(
        [
            StructureMapStructure(
                url="http://hl7.org/fhir/StructureDefinition/Patient",
                mode="source",
            )
        ]
    )
    result = engine._resolve_structure_definitions(sm, StructureMapModelMode.SOURCE)
    assert "Patient" in result
    assert result["Patient"] is not ArbitraryModel
    assert issubclass(result["Patient"], BaseModel)


def test_resolve__core_fhir_type_with_alias_uses_alias_as_key():
    """When an alias is given for a core FHIR type, the alias is the dict key."""
    engine = FHIRMappingEngine()
    sm = _sm_structs(
        [
            StructureMapStructure(
                url="http://hl7.org/fhir/StructureDefinition/Patient",
                mode="source",
                alias="Src",
            )
        ]
    )
    result = engine._resolve_structure_definitions(sm, StructureMapModelMode.SOURCE)
    assert "Src" in result
    assert "Patient" not in result
    assert result["Src"] is not ArbitraryModel


def test_resolve__unknown_core_fhir_type_falls_back_to_arbitrary(caplog):
    """An hl7 URL whose type name doesn't exist falls back to ArbitraryModel.

    get_fhir_type raises AttributeError for the unknown short name, then the registry
    lookup raises StructureDefinitionNotFoundError — both are now caught.
    """
    engine = FHIRMappingEngine()
    sm = _sm_structs(
        [
            StructureMapStructure(
                url="http://hl7.org/fhir/StructureDefinition/NonExistentType99999",
                mode="source",
                alias="Broken",
            )
        ]
    )
    with caplog.at_level(logging.WARNING):
        result = engine._resolve_structure_definitions(sm, StructureMapModelMode.SOURCE)
    assert "Broken" in result
    assert result["Broken"] is ArbitraryModel


def test_resolve__registry_lookup_failure_falls_back_to_arbitrary_with_alias(caplog):
    """When the StructureDefinitionRegistry cannot find a URL the entry uses ArbitraryModel.

    StructureDefinitionNotFoundError is now caught alongside KeyError/ValueError/AttributeError.
    """
    engine = FHIRMappingEngine()
    sm = _sm_structs(
        [
            StructureMapStructure(
                url="http://example.org/StructureDefinition/Unknown",
                mode="source",
                alias="MyAlias",
            )
        ]
    )
    with caplog.at_level(logging.WARNING, logger="fhircraft.fhir.mapper.engine.core"):
        result = engine._resolve_structure_definitions(sm, StructureMapModelMode.SOURCE)
    assert "MyAlias" in result
    assert result["MyAlias"] is ArbitraryModel
    assert any("Could not resolve" in r.message for r in caplog.records)


def test_resolve__registry_lookup_failure_no_alias_uses_url_as_key(caplog):
    """When registry lookup fails and no alias is set, the URL itself is used as key.

    StructureDefinitionNotFoundError is now caught alongside KeyError/ValueError/AttributeError.
    """
    engine = FHIRMappingEngine()
    url = "http://example.org/StructureDefinition/Unknown"
    sm = _sm_structs([StructureMapStructure(url=url, mode="source")])
    with caplog.at_level(logging.WARNING, logger="fhircraft.fhir.mapper.engine.core"):
        result = engine._resolve_structure_definitions(sm, StructureMapModelMode.SOURCE)
    assert url in result
    assert result[url] is ArbitraryModel


def test_resolve__non_matching_mode_is_excluded():
    """A structure whose mode differs from the requested mode is not included."""
    engine = FHIRMappingEngine()
    sm = _sm_structs(
        [
            StructureMapStructure(
                url="http://hl7.org/fhir/StructureDefinition/Patient",
                mode="target",
                alias="Pat",
            )
        ]
    )
    result = engine._resolve_structure_definitions(sm, StructureMapModelMode.SOURCE)
    assert result == {}


def test_resolve__queried_mode_returns_only_queried_structures():
    engine = FHIRMappingEngine()
    sm = _sm_structs(
        [
            StructureMapStructure(
                url="http://hl7.org/fhir/StructureDefinition/Patient",
                mode="queried",
                alias="QueriedPat",
            ),
            StructureMapStructure(
                url="http://hl7.org/fhir/StructureDefinition/Patient",
                mode="source",
                alias="SrcPat",
            ),
        ]
    )
    result = engine._resolve_structure_definitions(sm, StructureMapModelMode.QUERIED)
    assert "QueriedPat" in result
    assert "SrcPat" not in result


def test_resolve__produced_mode_returns_only_produced_structures():
    engine = FHIRMappingEngine()
    sm = _sm_structs(
        [
            StructureMapStructure(
                url="http://hl7.org/fhir/StructureDefinition/Patient",
                mode="produced",
                alias="ProducedPat",
            ),
            StructureMapStructure(
                url="http://hl7.org/fhir/StructureDefinition/Patient",
                mode="source",
                alias="SrcPat",
            ),
        ]
    )
    result = engine._resolve_structure_definitions(sm, StructureMapModelMode.PRODUCED)
    assert "ProducedPat" in result
    assert "SrcPat" not in result


def test_resolve__multiple_structures_same_mode_all_returned():
    engine = FHIRMappingEngine()
    sm = _sm_structs(
        [
            StructureMapStructure(
                url="http://hl7.org/fhir/StructureDefinition/Patient",
                mode="source",
                alias="Pat",
            ),
            StructureMapStructure(
                url="http://hl7.org/fhir/StructureDefinition/Observation",
                mode="source",
                alias="Obs",
            ),
        ]
    )
    result = engine._resolve_structure_definitions(sm, StructureMapModelMode.SOURCE)
    assert "Pat" in result
    assert "Obs" in result
    assert len(result) == 2


def test_resolve__missing_url_logs_warning_and_uses_alias(caplog):
    """A structure with no URL logs a warning and stores ArbitraryModel under the alias."""
    engine = FHIRMappingEngine()
    sm = _sm_structs([StructureMapStructure(mode="source", alias="NoUrl")])
    with caplog.at_level(logging.WARNING, logger="fhircraft.fhir.mapper.engine.core"):
        result = engine._resolve_structure_definitions(sm, StructureMapModelMode.SOURCE)
    assert any("missing URL" in r.message for r in caplog.records)
    assert result["NoUrl"] is ArbitraryModel


def test_resolve__missing_url_no_alias_uses_arbitrary_key(caplog):
    """A structure with no URL and no alias falls back to the key 'arbitrary'."""
    engine = FHIRMappingEngine()
    sm = _sm_structs([StructureMapStructure(mode="source")])
    with caplog.at_level(logging.WARNING, logger="fhircraft.fhir.mapper.engine.core"):
        result = engine._resolve_structure_definitions(sm, StructureMapModelMode.SOURCE)
    assert "arbitrary" in result
    assert result["arbitrary"] is ArbitraryModel
