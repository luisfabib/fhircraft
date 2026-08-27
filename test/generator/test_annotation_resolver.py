# Test module AnnotationSerializer

from typing import Annotated, List, Optional, Union
from datetime import datetime

import pytest

from fhircraft.fhir.resources.datatypes import R5 as fhir

from fhircraft.fhir.resources.generator._annotations import AnnotationSerializer
from fhircraft.fhir.resources.generator._imports import ImportTracker


@pytest.fixture
def tracker():
    return ImportTracker()


@pytest.fixture
def serializer(tracker):
    return AnnotationSerializer(tracker)


# ------------------------------------------------------------------
# AnnotationSerializer.serialize()
# ------------------------------------------------------------------


def test_serialize__none_type(serializer, tracker):
    assert serializer.serialize(type(None)) == "None"
    assert len(tracker.imports) == 0, "No imports should be tracked for None"


def test_serialize__builtin_type(serializer, tracker):
    assert serializer.serialize(str) == "str"
    assert len(tracker.imports) == 0, "No imports should be tracked for builtin type"


def test_serialize__builtin_type_optional(serializer, tracker):
    assert serializer.serialize(Optional[str]) == "Optional[str]"
    assert len(tracker.imports) == 1
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]


def test_serialize__builtin_type_list(serializer, tracker):
    assert serializer.serialize(List[str]) == "List[str]"
    assert len(tracker.imports) == 1
    assert "typing" in tracker.imports
    assert "List" in tracker.imports["typing"]


def test_serialize__builtin_type_optional_list(serializer, tracker):
    assert serializer.serialize(Optional[List[str]]) == "Optional[List[str]]"
    assert len(tracker.imports) == 1
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]


def test_serialize__builtin_type_list_optional(serializer, tracker):
    assert serializer.serialize(List[Optional[str]]) == "List[Optional[str]]"
    assert len(tracker.imports) == 1
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]


def test_serialize__non_fhir_type(serializer, tracker):
    result = serializer.serialize(datetime)
    assert result == "datetime"
    assert len(tracker.imports) == 1
    assert "datetime" in tracker.imports.keys()
    assert "datetime" in tracker.imports["datetime"]


def test_serialize__non_fhir_type_optional(serializer, tracker):
    result = serializer.serialize(Optional[datetime])
    assert result == "Optional[datetime]"
    assert len(tracker.imports) == 2
    assert "datetime" in tracker.imports.keys()
    assert "datetime" in tracker.imports["datetime"]
    assert "typing" in tracker.imports.keys()
    assert "Optional" in tracker.imports["typing"]


def test_serialize__non_fhir_type_list(serializer, tracker):
    result = serializer.serialize(List[datetime])
    assert result == "List[datetime]"
    assert len(tracker.imports) == 2
    assert "datetime" in tracker.imports.keys()
    assert "datetime" in tracker.imports["datetime"]
    assert "typing" in tracker.imports.keys()
    assert "List" in tracker.imports["typing"]


def test_serialize__non_fhir_type_list_optional(serializer, tracker):
    result = serializer.serialize(List[Optional[datetime]])
    assert result == "List[Optional[datetime]]"
    assert len(tracker.imports) == 2
    assert "datetime" in tracker.imports.keys()
    assert "datetime" in tracker.imports["datetime"]
    assert "typing" in tracker.imports.keys()
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]


def test_serialize__non_fhir_type_optional_list(serializer, tracker):
    result = serializer.serialize(Optional[List[datetime]])
    assert result == "Optional[List[datetime]]"
    assert len(tracker.imports) == 2
    assert "datetime" in tracker.imports.keys()
    assert "datetime" in tracker.imports["datetime"]
    assert "typing" in tracker.imports.keys()
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]


def test_serialize__resource_type(serializer, tracker):
    result = serializer.serialize(fhir.Observation)
    assert result == "fhir.Observation"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()


def test_serialize__optional_resource_type(serializer, tracker):
    result = serializer.serialize(Optional[fhir.Observation])
    assert result == "Optional[fhir.Observation]"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]


def test_serialize__list_resource_type(serializer, tracker):
    result = serializer.serialize(List[fhir.Observation])
    assert result == "List[fhir.Observation]"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()
    assert "typing" in tracker.imports
    assert "List" in tracker.imports["typing"]


def test_serialize__optional_list_resource_type(serializer, tracker):
    result = serializer.serialize(Optional[List[fhir.Observation]])
    assert result == "Optional[List[fhir.Observation]]"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]


def test_serialize__complex_type(serializer, tracker):
    result = serializer.serialize(fhir.Coding)
    assert result == "fhir.Coding"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()


def test_serialize__optional_complex_type(serializer, tracker):
    result = serializer.serialize(Optional[fhir.Coding])
    assert result == "Optional[fhir.Coding]"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]


def test_serialize__list_complex_type(serializer, tracker):
    result = serializer.serialize(List[fhir.Coding])
    assert result == "List[fhir.Coding]"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()
    assert "typing" in tracker.imports
    assert "List" in tracker.imports["typing"]


def test_serialize__optional_list_complex_type(serializer, tracker):
    result = serializer.serialize(Optional[List[fhir.Coding]])
    assert result == "Optional[List[fhir.Coding]]"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]


def test_serialize__fhir_primitive_class(serializer, tracker):
    result = serializer.serialize(fhir.String)
    assert result == "fhir.String"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()


def test_serialize__fhir_primitive(serializer, tracker):
    result = serializer.serialize(fhir.string)
    assert result == "fhir.string"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()


def test_serialize__primitive_optional(serializer, tracker):
    result = serializer.serialize(Optional[fhir.string])
    assert result == "Optional[fhir.string]"
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]


def test_serialize__primitive_list(serializer, tracker):
    result = serializer.serialize(List[fhir.integer])
    assert result == "List[fhir.integer]"
    assert "typing" in tracker.imports
    assert "List" in tracker.imports["typing"]


def test_serialize__primitive_optional_list(serializer, tracker):
    result = serializer.serialize(Optional[List[fhir.integer]])
    assert result == "Optional[List[fhir.integer]]"
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]


def test_serialize__primitive_list_optional(serializer, tracker):
    result = serializer.serialize(List[Optional[fhir.integer]])
    assert result == "List[Optional[fhir.integer]]"
    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]


def test_serialize__union(serializer, tracker):
    result = serializer.serialize(Union[fhir.string, fhir.integer])
    assert result == "Union[fhir.string, fhir.integer]"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()
    assert "typing" in tracker.imports
    assert "Union" in tracker.imports["typing"]


def test_serialize__union_with_none(serializer, tracker):
    result = serializer.serialize(Union[fhir.string, fhir.integer, None])
    assert result == "Optional[Union[fhir.string, fhir.integer]]"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()
    assert "typing" in tracker.imports
    assert "Union" in tracker.imports["typing"]


def test_serialize__union_with_none_alt(serializer, tracker):
    result = serializer.serialize(Union[fhir.string, fhir.integer] | None)
    assert result == "Optional[Union[fhir.string, fhir.integer]]"
    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()
    assert "typing" in tracker.imports
    assert "Union" in tracker.imports["typing"]


def test_serialize__deeply_nested_annotation(serializer, tracker):
    result = serializer.serialize(
        Optional[List[Union[fhir.string, List[fhir.integer], None]]]
    )
    assert result == "Optional[List[Optional[Union[fhir.string, List[fhir.integer]]]]]"

    assert "fhir" in tracker.alias_imports.values()
    assert "fhircraft.fhir.resources.datatypes.R5" in tracker.alias_imports.keys()

    assert "typing" in tracker.imports
    assert "Optional" in tracker.imports["typing"]
    assert "List" in tracker.imports["typing"]
    assert "Union" in tracker.imports["typing"]


def test_serialize__annotated_non_primitive_unwraps(serializer):
    from pydantic import BaseModel

    inner = BaseModel
    ann = Annotated[inner, "some metadata"]
    result = serializer.serialize(ann)
    assert "BaseModel" in result


def test_serialize__registers_fhir_alias_import(serializer, tracker):
    from fhircraft.fhir.resources.datatypes.R4B import primitive as p

    serializer.serialize(p.boolean)
    assert any("fhir" in v for v in tracker.alias_imports.values())
