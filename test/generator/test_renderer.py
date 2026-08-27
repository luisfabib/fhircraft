import pytest

from fhircraft.fhir.resources.generator._renderer import CodeRenderer
from fhircraft.fhir.resources.generator._constants import FACTORY_MODULE


@pytest.fixture
def renderer():
    return CodeRenderer()


class TestStripModulePrefixes:
    def test_removes_full_module_prefix(self, renderer):
        code = "x: pydantic.BaseModel = Field()"
        result = renderer._strip_module_prefixes(
            code,
            imports={"pydantic": ["BaseModel"]},
            raw_imports={"pydantic": ["BaseModel"]},
        )
        assert "pydantic.BaseModel" not in result
        assert "BaseModel" in result

    def test_removes_last_component_prefix(self, renderer):
        code = "x: mymodule.MyClass = Field()"
        result = renderer._strip_module_prefixes(
            code,
            imports={},
            raw_imports={"a.b.mymodule": ["MyClass"]},
        )
        assert "mymodule.MyClass" not in result


class TestCleanClassReprs:
    def test_replaces_class_repr(self, renderer):
        from pydantic import BaseModel

        code = "x: <class 'BaseModel'> = ..."
        result = renderer._clean_class_reprs(
            code, imports={"pydantic": ["BaseModel"]}, data={}
        )
        assert "<class 'BaseModel'>" not in result
        assert "BaseModel" in result

    def test_replaces_qualified_class_repr(self, renderer):
        code = "x: <class 'pydantic.main.BaseModel'> = ..."
        result = renderer._clean_class_reprs(
            code, imports={"pydantic": ["BaseModel"]}, data={}
        )
        assert "<class" not in result

    def test_replaces_builtin_repr(self, renderer):
        code = "x: <class 'str'>"
        result = renderer._clean_class_reprs(code, imports={}, data={})
        assert "<class 'str'>" not in result
        assert "str" in result

    def test_uses_data_model_names(self, renderer):
        class FakeModel:
            __name__ = "FakeModel"

        code = "<class 'FakeModel'>"
        result = renderer._clean_class_reprs(code, imports={}, data={FakeModel: {}})
        assert "FakeModel" in result
        assert "<class" not in result


class TestCleanFactoryRefs:
    def test_removes_factory_module_prefix(self, renderer):
        code = f"{FACTORY_MODULE}.SomeClass()"
        result = renderer._clean_factory_refs(code, raw_imports={})
        assert FACTORY_MODULE not in result
        assert "SomeClass()" in result

    def test_removes_typing_prefix(self, renderer):
        code = "typing.Optional[str]"
        result = renderer._clean_factory_refs(code, raw_imports={})
        assert "typing." not in result
        assert "Optional[str]" in result


class TestRenderIntegration:
    def test_render_produces_valid_python(self, renderer):
        from pydantic import BaseModel, Field, create_model

        Model = create_model(
            "RenderTest", x=(int, Field(default=1, description="A value."))
        )

        from fhircraft.fhir.resources.generator._imports import ImportTracker
        from fhircraft.fhir.resources.generator._annotations import AnnotationSerializer
        from fhircraft.fhir.resources.generator._defaults import DefaultExtractor
        from fhircraft.fhir.resources.generator._serializer import ModelSerializer

        tracker = ImportTracker()
        resolver = AnnotationSerializer(tracker)
        extractor = DefaultExtractor()
        serializer = ModelSerializer(tracker, resolver, extractor)
        serializer.serialize(Model)

        code = renderer.render(
            data=serializer.data,
            imports=tracker.group_by_parent(),
            alias_imports=tracker.alias_imports,
            raw_imports=dict(tracker.imports),
        )
        assert "class RenderTest" in code
        assert "x:" in code
        assert "Field(" in code

    def test_include_validators_false_omits_validators(self, renderer):
        import functools
        from pydantic import BaseModel, Field, field_validator, create_model
        import fhircraft.fhir.resources.validators as fhir_validators

        Model = create_model(
            "ValidatorModel",
            x=(int, Field(default=1)),
            __validators__={
                "validate_x": field_validator("x")(
                    classmethod(
                        functools.partial(
                            fhir_validators.validate_type, expected_types=[int]
                        )
                    )
                )
            },
        )

        from fhircraft.fhir.resources.generator._imports import ImportTracker
        from fhircraft.fhir.resources.generator._annotations import AnnotationSerializer
        from fhircraft.fhir.resources.generator._defaults import DefaultExtractor
        from fhircraft.fhir.resources.generator._serializer import ModelSerializer

        tracker = ImportTracker()
        resolver = AnnotationSerializer(tracker)
        extractor = DefaultExtractor()
        serializer = ModelSerializer(tracker, resolver, extractor)
        serializer.serialize(Model)

        code_with = renderer.render(
            data=serializer.data,
            imports=tracker.group_by_parent(),
            alias_imports=tracker.alias_imports,
            raw_imports=dict(tracker.imports),
            include_validators=True,
        )
        tracker.reset()
        serializer.reset()
        serializer.serialize(Model)
        code_without = renderer.render(
            data=serializer.data,
            imports=tracker.group_by_parent(),
            alias_imports=tracker.alias_imports,
            raw_imports=dict(tracker.imports),
            include_validators=False,
        )
        assert "@field_validator" in code_with
        assert "@field_validator" not in code_without
