from typing import Annotated, List, Optional, Union

import pytest

from fhircraft.fhir.resources.generator._annotations import AnnotationResolver
from fhircraft.fhir.resources.generator._imports import ImportTracker


@pytest.fixture
def tracker():
    return ImportTracker()


@pytest.fixture
def resolver(tracker):
    return AnnotationResolver(tracker)


class TestGetPrimitivePackageModule:
    def test_returns_primitive_package(self, resolver):
        assert resolver.get_primitive_package_module("a.b.primitive.string") == "a.b.primitive"

    def test_returns_none_if_no_primitive_segment(self, resolver):
        assert resolver.get_primitive_package_module("a.b.complex") is None

    def test_returns_none_if_primitive_is_first_segment(self, resolver):
        assert resolver.get_primitive_package_module("primitive.string") is None


class TestResolveAnnotatedPrimitive:
    def test_returns_none_for_plain_type(self, resolver):
        assert resolver.resolve_annotated_primitive(str) is None

    def test_returns_none_for_non_annotated_generic(self, resolver):
        assert resolver.resolve_annotated_primitive(List[str]) is None

    def test_finds_fhir_primitive(self, resolver):
        from fhircraft.fhir.resources.datatypes.R4B import primitive as p
        result = resolver.resolve_annotated_primitive(p.string)
        assert result is not None
        module_name, alias_name = result
        assert alias_name == "string"
        assert "primitive" in module_name


class TestResolvePrimitiveClassAlias:
    def test_returns_none_for_plain_builtin(self, resolver):
        assert resolver.resolve_primitive_class_alias(str) is None

    def test_returns_none_for_non_primitive_class(self, resolver):
        from pydantic import BaseModel
        assert resolver.resolve_primitive_class_alias(BaseModel) is None

    def test_finds_fhir_string_class(self, resolver):
        from fhircraft.fhir.resources.datatypes.R4B.primitive.string import String
        result = resolver.resolve_primitive_class_alias(String)
        assert result is not None
        primitive_module, alias_name = result
        assert "primitive" in primitive_module
        assert alias_name == "string"


class TestToString:
    def test_none_type(self, resolver):
        assert resolver.to_string(type(None)) == "None"

    def test_plain_type_uses_repr(self, resolver):
        from pydantic import BaseModel
        result = resolver.to_string(BaseModel)
        assert "BaseModel" in result

    def test_fhir_primitive_alias(self, resolver):
        from fhircraft.fhir.resources.datatypes.R4B import primitive as p
        result = resolver.to_string(p.string)
        assert result == "fhir.string"

    def test_fhir_primitive_class(self, resolver):
        from fhircraft.fhir.resources.datatypes.R4B.primitive.string import String
        result = resolver.to_string(String)
        assert result == "fhir.string"

    def test_optional_primitive(self, resolver, tracker):
        from fhircraft.fhir.resources.datatypes.R4B import primitive as p
        result = resolver.to_string(Optional[p.string])
        assert result == "Optional[fhir.string]"
        assert "Optional" in tracker.imports["typing"]

    def test_list_primitive(self, resolver, tracker):
        from fhircraft.fhir.resources.datatypes.R4B import primitive as p
        result = resolver.to_string(List[p.integer])
        assert result == "List[fhir.integer]"
        assert "List" in tracker.imports["typing"]

    def test_union_with_none(self, resolver, tracker):
        from fhircraft.fhir.resources.datatypes.R4B import primitive as p
        result = resolver.to_string(Union[p.string, p.integer, None])
        assert "Optional" in result
        assert "fhir.string" in result
        assert "fhir.integer" in result

    def test_union_without_none(self, resolver, tracker):
        from fhircraft.fhir.resources.datatypes.R4B import primitive as p
        result = resolver.to_string(Union[p.string, p.integer])
        assert result.startswith("Union[")
        assert "Union" in tracker.imports["typing"]

    def test_annotated_non_primitive_unwraps(self, resolver):
        from pydantic import BaseModel
        inner = BaseModel
        ann = Annotated[inner, "some metadata"]
        result = resolver.to_string(ann)
        assert "BaseModel" in result

    def test_registers_fhir_alias_import(self, resolver, tracker):
        from fhircraft.fhir.resources.datatypes.R4B import primitive as p
        resolver.to_string(p.boolean)
        assert any("fhir" in v for v in tracker.alias_imports.values())
