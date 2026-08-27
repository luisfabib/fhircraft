# Test module AnnotationAssembler

from typing import Annotated, List, Optional, Union
from datetime import datetime

import pytest

from fhircraft.fhir.resources.datatypes import R5 as fhir

from fhircraft.fhir.resources.generator._annotations import AnnotationAssembler
from fhircraft.fhir.resources.generator._imports import ImportTracker


@pytest.fixture
def tracker():
    return ImportTracker()


@pytest.fixture
def assembler(tracker):
    return AnnotationAssembler(tracker)


class TestGetPrimitivePackageModule:
    def test_returns_primitive_package(self, assembler):
        assert assembler.get_primitive_package_module("a.b.primitive.string") == "a.b.primitive"

    def test_returns_none_if_no_primitive_segment(self, assembler):
        assert assembler.get_primitive_package_module("a.b.complex") is None

    def test_returns_none_if_primitive_is_first_segment(self, assembler):
        assert assembler.get_primitive_package_module("primitive.string") is None


class TestResolveAnnotatedPrimitive:
    def test_returns_none_for_plain_type(self, assembler):
        assert assembler.resolve_annotated_primitive(str) is None

    def test_returns_none_for_non_annotated_generic(self, assembler):
        assert assembler.resolve_annotated_primitive(List[str]) is None

    def test_finds_fhir_primitive(self, assembler):
        from fhircraft.fhir.resources.datatypes.R4B import primitive as p
        result = assembler.resolve_annotated_primitive(p.string)
        assert result is not None
        module_name, alias_name = result
        assert alias_name == "string"
        assert "primitive" in module_name


class TestResolvePrimitiveClassAlias:
    def test_returns_none_for_plain_builtin(self, assembler):
        assert assembler.resolve_primitive_class_alias(str) is None

    def test_returns_none_for_non_primitive_class(self, assembler):
        from pydantic import BaseModel
        assert assembler.resolve_primitive_class_alias(BaseModel) is None

    def test_finds_fhir_string_class(self, assembler):
        from fhircraft.fhir.resources.datatypes.R4B.primitive.string import String
        result = assembler.resolve_primitive_class_alias(String)
        assert result is not None
        primitive_module, alias_name = result
        assert "primitive" in primitive_module
        assert alias_name == "string"



#------------------------------------------------------------------
# AnnotationAssembler.to_string()
#------------------------------------------------------------------

def test_to_string__none_type(assembler, tracker):
    assert assembler.to_string(type(None)) == "None"
    assert len(tracker.imports) == 0, "No imports should be tracked for None"

def test_to_string__builtin_type(assembler, tracker):
    assert assembler.to_string(str) == "str"
    assert len(tracker.imports) == 0, "No imports should be tracked for builtin type"

def test_to_string__builtin_type_optional(assembler, tracker):
    assert assembler.to_string(Optional[str]) == "Optional[str]"
    assert len(tracker.imports) == 1
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]

def test_to_string__builtin_type_list(assembler, tracker):
    assert assembler.to_string(List[str]) == "List[str]"
    assert len(tracker.imports) == 1
    assert "typing" in tracker.imports
    assert "List" in tracker.imports["typing"]

def test_to_string__builtin_type_optional_list(assembler, tracker):
    assert assembler.to_string(Optional[List[str]]) == "Optional[List[str]]"
    assert len(tracker.imports) == 1
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]

def test_to_string__builtin_type_list_optional(assembler, tracker):
    assert assembler.to_string(List[Optional[str]]) == "List[Optional[str]]"
    assert len(tracker.imports) == 1
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]

def test_to_string__non_fhir_type(assembler, tracker):
    result = assembler.to_string(datetime)
    assert result == "datetime"
    assert len(tracker.imports) == 1
    assert "datetime" in tracker.imports.keys()
    assert "datetime" in tracker.imports["datetime"]

def test_to_string__non_fhir_type_optional(assembler, tracker):
    result = assembler.to_string(Optional[datetime])
    assert result == "Optional[datetime]"
    assert len(tracker.imports) == 2
    assert "datetime" in tracker.imports.keys()
    assert "datetime" in tracker.imports["datetime"]
    assert "typing" in tracker.imports.keys()
    assert "Optional" in tracker.imports["typing"]

def test_to_string__non_fhir_type_list(assembler, tracker):
    result = assembler.to_string(List[datetime])
    assert result == "List[datetime]"
    assert len(tracker.imports) == 2
    assert "datetime" in tracker.imports.keys()
    assert "datetime" in tracker.imports["datetime"]
    assert "typing" in tracker.imports.keys()
    assert "List" in tracker.imports["typing"]

def test_to_string__non_fhir_type_list_optional(assembler, tracker):
    result = assembler.to_string(List[Optional[datetime]])
    assert result == "List[Optional[datetime]]"
    assert len(tracker.imports) == 2
    assert "datetime" in tracker.imports.keys()
    assert "datetime" in tracker.imports["datetime"]
    assert "typing" in tracker.imports.keys()
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]

def test_to_string__non_fhir_type_optional_list(assembler, tracker):
    result = assembler.to_string(Optional[List[datetime]])
    assert result == "Optional[List[datetime]]"
    assert len(tracker.imports) == 2
    assert "datetime" in tracker.imports.keys()
    assert "datetime" in tracker.imports["datetime"]
    assert "typing" in tracker.imports.keys()
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]

def test_to_string__complex_type(assembler, tracker):
    result = assembler.to_string(fhir.Coding)
    assert result == "fhir.Coding"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()

def test_to_string__fhir_primitive_class(assembler, tracker):
    result = assembler.to_string(fhir.String)
    assert result == "fhir.string"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()

def test_to_string__fhir_primitive(assembler, tracker):
    result = assembler.to_string(fhir.string)
    assert result == "fhir.string"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()

def test_to_string__primitive_optional(assembler, tracker):
    result = assembler.to_string(Optional[fhir.string])
    assert result == "Optional[fhir.string]"
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]

def test_to_string__primitive_list(assembler, tracker):
    result = assembler.to_string(List[fhir.integer])
    assert result == "List[fhir.integer]"
    assert "typing" in tracker.imports
    assert "List" in tracker.imports["typing"]

def test_to_string__primitive_optional_list(assembler, tracker):
    result = assembler.to_string(Optional[List[fhir.integer]])
    assert result == "Optional[List[fhir.integer]]"
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]

def test_to_string__primitive_list_optional(assembler, tracker):
    result = assembler.to_string(List[Optional[fhir.integer]])
    assert result == "List[Optional[fhir.integer]]"
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]


def test_to_string__union(assembler, tracker):
    result = assembler.to_string(Union[fhir.string, fhir.integer])
    assert result == "Union[fhir.string, fhir.integer]"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R4B.primitive" in tracker.alias_imports.keys()
    assert "typing" in tracker.imports
    assert "Union" in tracker.imports["typing"]


def test_to_string__union_with_none(assembler, tracker):
    result = assembler.to_string(Union[fhir.string, fhir.integer, None])
    assert result == "Union[fhir.string, fhir.integer, None]"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R4B.primitive" in tracker.alias_imports.keys()
    assert "typing" in tracker.imports
    assert "Union" in tracker.imports["typing"]


def test_to_string__deeply_nested_annotation(assembler, tracker):
    result = assembler.to_string(Optional[List[Union[fhir.string, List[fhir.integer], None]]])
    assert result == "Optional[List[Union[fhir.string, List[fhir.integer], None]]]"

    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()

    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]
    assert "Union" in tracker.imports["typing"]



def test_to_string__annotated_non_primitive_unwraps(assembler):
    from pydantic import BaseModel
    inner = BaseModel
    ann = Annotated[inner, "some metadata"]
    result = assembler.to_string(ann)
    assert "BaseModel" in result

def test_to_string__registers_fhir_alias_import(assembler, tracker):
    from fhircraft.fhir.resources.datatypes.R4B import primitive as p
    assembler.to_string(p.boolean)
    assert any("fhir" in v for v in tracker.alias_imports.values())
