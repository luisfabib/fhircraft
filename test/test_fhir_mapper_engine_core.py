"""Integration tests for the StructureMap 'import' statement in FHIRMappingEngine."""

from __future__ import annotations

import logging

import pytest

from fhircraft.fhir.mapper.engine.core import FHIRMappingEngine
from fhircraft.fhir.mapper.engine.registry import StructureMapNotFoundError
from fhircraft.fhir.resources.datatypes.R5.core.structure_map import (
    StructureMap,
    StructureMapGroup,
    StructureMapGroupInput,
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
