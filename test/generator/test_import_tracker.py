from collections import defaultdict
from typing import ForwardRef

import pytest

from fhircraft.fhir.resources.generator._imports import ImportTracker


@pytest.fixture
def tracker():
    return ImportTracker()


class TestTrack:
    def test_adds_name_to_module(self, tracker):
        tracker.track("mypackage.mymodule", "MyClass")
        assert "MyClass" in tracker.imports["mypackage.mymodule"]

    def test_deduplicates_same_name(self, tracker):
        tracker.track("mypackage.mymodule", "MyClass")
        tracker.track("mypackage.mymodule", "MyClass")
        assert tracker.imports["mypackage.mymodule"].count("MyClass") == 1

    def test_excludes_builtins_module(self, tracker):
        tracker.track("builtins", "str")
        assert "builtins" not in tracker.imports

    def test_excludes_factory_module(self, tracker):
        from fhircraft.fhir.resources.generator._constants import FACTORY_MODULE
        tracker.track(FACTORY_MODULE, "SomeFactoryClass")
        assert FACTORY_MODULE not in tracker.imports


class TestTrackObj:
    def test_skips_forward_ref(self, tracker):
        tracker.track_obj(ForwardRef("MyModel"))
        assert not any(tracker.imports.values())

    def test_adds_class_import(self, tracker):
        from pydantic import BaseModel
        tracker.track_obj(BaseModel)
        assert "BaseModel" in tracker.imports["pydantic"]

    def test_raises_for_unnamed_object(self, tracker):
        class _Anon:
            pass
        _Anon.__name__ = None  # type: ignore
        _Anon._name = None  # type: ignore
        with pytest.raises(ValueError, match="Could not determine object name"):
            tracker.track_obj(_Anon)


class TestTrackAlias:
    def test_registers_alias(self, tracker):
        result = tracker.track_alias("some.module", "sm")
        assert result is True
        assert tracker.alias_imports["some.module"] == "sm"

    def test_same_module_same_alias_is_idempotent(self, tracker):
        tracker.track_alias("some.module", "sm")
        result = tracker.track_alias("some.module", "sm")
        assert result is True

    def test_returns_false_on_alias_conflict(self, tracker):
        tracker.track_alias("module.a", "alias")
        result = tracker.track_alias("module.b", "alias")
        assert result is False
        assert "module.b" not in tracker.alias_imports


class TestTrackTypingAndPydantic:
    def test_track_typing(self, tracker):
        tracker.track_typing("Optional")
        assert "Optional" in tracker.imports["typing"]

    def test_track_pydantic(self, tracker):
        tracker.track_pydantic("Field")
        assert "Field" in tracker.imports["pydantic"]

    def test_no_duplicates(self, tracker):
        tracker.track_typing("List")
        tracker.track_typing("List")
        assert tracker.imports["typing"].count("List") == 1


class TestGroupByParent:
    def test_empty_returns_empty(self, tracker):
        assert tracker.group_by_parent() == {}

    def test_collapses_snake_module_to_parent(self, tracker):
        # codeable_concept -> CodeableConcept: module is snake_case of class name
        tracker.track("a.b.codeable_concept", "CodeableConcept")
        grouped = tracker.group_by_parent()
        assert "a.b" in grouped
        assert "CodeableConcept" in grouped["a.b"]
        assert "a.b.codeable_concept" not in grouped

    def test_keeps_multi_import_module_as_is(self, tracker):
        tracker.track("a.b.utils", "Foo")
        tracker.track("a.b.utils", "Bar")
        grouped = tracker.group_by_parent()
        assert "a.b.utils" in grouped
        assert sorted(grouped["a.b.utils"]) == ["Bar", "Foo"]

    def test_merges_sibling_classes_into_same_parent(self, tracker):
        tracker.track("a.b.coding", "Coding")
        tracker.track("a.b.codeable_concept", "CodeableConcept")
        grouped = tracker.group_by_parent()
        assert "a.b" in grouped
        assert "Coding" in grouped["a.b"]
        assert "CodeableConcept" in grouped["a.b"]

    def test_objects_are_sorted(self, tracker):
        tracker.track("a.b.utils", "Zebra")
        tracker.track("a.b.utils", "Alpha")
        grouped = tracker.group_by_parent()
        assert grouped["a.b.utils"] == ["Alpha", "Zebra"]


class TestReset:
    def test_clears_imports(self, tracker):
        tracker.track("some.module", "Foo")
        tracker.track_alias("some.module", "sm")
        tracker.reset()
        assert not any(tracker.imports.values())
        assert tracker.alias_imports == {}
