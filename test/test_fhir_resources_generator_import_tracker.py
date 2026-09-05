from typing import ForwardRef

import pytest

from fhircraft.fhir.resources.factory.core import FHIRModelFactory
from fhircraft.fhir.resources.generator._imports import ImportTracker
from fhircraft.utils import get_module_name


@pytest.fixture
def tracker():
    return ImportTracker()


# ----------------------------------------
# ImportTracker.track()
# ----------------------------------------


def test_track__adds_name_to_module(tracker):
    tracker.track("mypackage.mymodule", "MyClass")
    assert "MyClass" in tracker.imports["mypackage.mymodule"]


def test_track__deduplicates_same_name(tracker):
    tracker.track("mypackage.mymodule", "MyClass")
    tracker.track("mypackage.mymodule", "MyClass")
    assert tracker.imports["mypackage.mymodule"].count("MyClass") == 1


def test_track__excludes_builtins_module(tracker):
    tracker.track("builtins", "str")
    assert "builtins" not in tracker.imports


def test_track__excludes_factory_module(tracker):
    FACTORY_MODULE = get_module_name(FHIRModelFactory)
    tracker.track(FACTORY_MODULE, "SomeFactoryClass")
    assert FACTORY_MODULE not in tracker.imports


# ----------------------------------------
# ImportTracker.track_alias()
# ----------------------------------------


def test_track_alias__registers_alias(tracker):
    result = tracker.track_alias("some.module", "sm")
    assert result is True
    assert tracker.alias_imports["some.module"] == "sm"


def test_track_alias__same_module_same_alias_is_idempotent(tracker):
    tracker.track_alias("some.module", "sm")
    result = tracker.track_alias("some.module", "sm")
    assert result is True


def test_track_alias__returns_false_on_alias_conflict(tracker):
    tracker.track_alias("module.a", "alias")
    result = tracker.track_alias("module.b", "alias")
    assert result is False
    assert "module.b" not in tracker.alias_imports


# ----------------------------------------
# ImportTracker.track_typing() and ImportTracker.track_pydantic()
# ----------------------------------------


def test_track_typing__registers_import(tracker):
    tracker.track_typing("Optional")
    assert "Optional" in tracker.imports["typing"]


def test_track_pydantic__registers_import(tracker):
    tracker.track_pydantic("Field")
    assert "Field" in tracker.imports["pydantic"]


def test_track_typing__no_duplicates(tracker):
    tracker.track_typing("List")
    tracker.track_typing("List")
    assert tracker.imports["typing"].count("List") == 1


# ----------------------------------------
# ImportTracker.group_by_parent()
# ----------------------------------------


def test_group_by_parent__empty_returns_empty(tracker):
    assert tracker.group_by_parent() == {}


def test_group_by_parent__collapses_snake_module_to_parent(tracker):
    # codeable_concept -> CodeableConcept: module is snake_case of class name
    tracker.track("a.b.codeable_concept", "CodeableConcept")
    grouped = tracker.group_by_parent()
    assert "a.b" in grouped
    assert "CodeableConcept" in grouped["a.b"]
    assert "a.b.codeable_concept" not in grouped


def test_group_by_parent__keeps_multi_import_module_as_is(tracker):
    tracker.track("a.b.utils", "Foo")
    tracker.track("a.b.utils", "Bar")
    grouped = tracker.group_by_parent()
    assert "a.b.utils" in grouped
    assert sorted(grouped["a.b.utils"]) == ["Bar", "Foo"]


def test_group_by_parent__merges_sibling_classes_into_same_parent(tracker):
    tracker.track("a.b.coding", "Coding")
    tracker.track("a.b.codeable_concept", "CodeableConcept")
    grouped = tracker.group_by_parent()
    assert "a.b" in grouped
    assert "Coding" in grouped["a.b"]
    assert "CodeableConcept" in grouped["a.b"]


def test_group_by_parent__objects_are_sorted(tracker):
    tracker.track("a.b.utils", "Zebra")
    tracker.track("a.b.utils", "Alpha")
    grouped = tracker.group_by_parent()
    assert grouped["a.b.utils"] == ["Alpha", "Zebra"]


# ----------------------------------------
# ImportTracker.reset()
# ----------------------------------------


def test_reset__clears_imports(tracker):
    tracker.track("some.module", "Foo")
    tracker.track_alias("some.module", "sm")
    tracker.reset()
    assert not any(tracker.imports.values())
    assert tracker.alias_imports == {}
