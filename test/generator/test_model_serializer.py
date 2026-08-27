from typing import List, Optional

import pytest
from pydantic import BaseModel, Field, create_model

from fhircraft.fhir.resources.generator._annotations import AnnotationSerializer
from fhircraft.fhir.resources.generator._defaults import DefaultExtractor
from fhircraft.fhir.resources.generator._imports import ImportTracker
from fhircraft.fhir.resources.generator._serializer import ModelSerializer


@pytest.fixture
def tracker():
    return ImportTracker()


@pytest.fixture
def resolver(tracker):
    return AnnotationSerializer(tracker)


@pytest.fixture
def extractor():
    return DefaultExtractor()


@pytest.fixture
def serializer(tracker, resolver, extractor):
    return ModelSerializer(tracker, resolver, extractor)


class TestModelClassification:
    def test_identifies_base_model_as_pydantic(self, serializer):
        assert serializer._is_builtin_pydantic_model(BaseModel) is True

    def test_identifies_pydantic_subclass(self, serializer):
        class MyModel(BaseModel):
            pass

        # MyModel defined here is NOT from pydantic, so should be False
        assert serializer._is_builtin_pydantic_model(MyModel) is False

    def test_identifies_fhir_framework_model(self, serializer):
        from fhircraft.fhir.resources.datatypes.R4.core.domain_resource import (
            DomainResource,
        )

        assert serializer._is_fhir_framework_model(DomainResource) is True

    def test_factory_model_is_not_framework(self, serializer):
        from fhircraft.fhir.resources.factory import FHIRModelFactory

        factory = FHIRModelFactory(fhir_release="R4B")
        sd = {
            "resourceType": "StructureDefinition",
            "id": "test-sd",
            "url": "http://example.org/test-sd",
            "version": "4.3.0",
            "name": "TestSD",
            "status": "draft",
            "fhirVersion": "4.3.0",
            "kind": "resource",
            "abstract": False,
            "type": "Observation",
            "derivation": "constraint",
            "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
            "differential": {"element": [{"id": "Observation", "path": "Observation"}]},
        }
        model = factory.build(structure_definition=sd, mode="differential")
        assert serializer._is_fhir_framework_model(model) is False


class TestCleanArgument:
    def test_plain_string(self, serializer):
        result = serializer.clean_argument("hello")
        assert result == '"hello"'

    def test_string_with_quotes(self, serializer):
        result = serializer.clean_argument('say "hi"')
        assert '\\"hi\\"' in result

    def test_multiline_string(self, serializer):
        result = serializer.clean_argument("line1\nline2")
        assert result.startswith('"""')
        assert result.endswith('"""')

    def test_list_of_plain_values(self, serializer):
        result = serializer.clean_argument([1, 2, 3])
        assert result == [1, 2, 3]

    def test_list_of_types(self, serializer, tracker):
        from pydantic import BaseModel

        result = serializer.clean_argument([BaseModel])
        assert result == ["BaseModel"]
        assert "BaseModel" in tracker.imports["pydantic"]

    def test_non_string_passthrough(self, serializer):
        assert serializer.clean_argument(42) == 42
        assert serializer.clean_argument(None) is None


class TestSerialize:
    def test_serializes_simple_model(self, serializer):
        Model = create_model("SimpleModel", name=(str, Field(description="A name.")))
        serializer.serialize(Model)
        assert Model in serializer.data
        assert "name" in serializer.data[Model]["fields"]

    def test_skips_inherited_unchanged_field(self, serializer):
        Base = create_model("Base", value=(int, Field(default=0)))
        Child = create_model("Child", __base__=Base)
        serializer.serialize(Child)
        assert "value" not in serializer.data[Child]["fields"]

    def test_includes_overridden_field(self, serializer):
        Base = create_model("BaseOvr", value=(int, Field(default=0)))
        Child = create_model("ChildOvr", __base__=Base, value=(int, Field(default=99)))
        serializer.serialize(Child)
        assert "value" in serializer.data[Child]["fields"]

    def test_cycle_detection_prevents_infinite_recursion(self, serializer):
        # A model whose field references itself
        SelfRef = create_model("SelfRef", child=(Optional["SelfRef"], Field(default=None)))  # type: ignore
        serializer.serialize(SelfRef)
        assert SelfRef in serializer.data

    def test_tracks_pydantic_field_import(self, serializer, tracker):
        Model = create_model("Tracked", x=(int, Field(default=1)))
        serializer.serialize(Model)
        assert "Field" in tracker.imports["pydantic"]

    def test_reset_clears_data(self, serializer):
        Model = create_model("Tmp", x=(int, ...))
        serializer.serialize(Model)
        assert serializer.data
        serializer.reset()
        assert not serializer.data

    def test_field_annotation_string_captured(self, serializer):
        from fhircraft.fhir.resources.datatypes.R4B import primitive as p

        Model = create_model("PrimModel", code=(p.string, Field(description="code")))
        serializer.serialize(Model)
        ann = serializer.data[Model]["fields"]["code"]["annotation"]
        assert "fhir.string" in ann

    def test_field_default_captured(self, serializer):
        Model = create_model("DefModel", count=(int, Field(default=5)))
        serializer.serialize(Model)
        assert serializer.data[Model]["fields"]["count"]["default"] == "5"

    def test_field_default_factory_captured(self, serializer):
        Model = create_model("FacModel", items=(List[str], Field(default_factory=list)))
        serializer.serialize(Model)
        assert serializer.data[Model]["fields"]["items"]["default_factory"] == "list"
