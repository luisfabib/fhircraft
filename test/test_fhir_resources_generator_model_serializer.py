from abc import ABC
from enum import Enum
import functools
from typing import Optional
from unittest.mock import MagicMock, patch
from pydantic.fields import FieldInfo
import pytest
from pydantic import (
    AliasChoices,
    AliasPath,
    BaseModel,
    Field,
    field_validator,
    model_validator,
)
from fhircraft.fhir.resources.base.models import FHIRBaseModel, FHIRSliceModel
from fhircraft.fhir.resources.datatypes import R5 as fhir
from fhircraft.fhir.resources.generator._schemas import (
    GeneratorFieldValidator,
    GeneratorModelProperty,
    GeneratorModelValidator,
    GeneratorModule,
    GeneratorModel,
)
from fhircraft.fhir.resources.generator._imports import ImportTracker
from fhircraft.fhir.resources.generator._model import ModelSerializer


@pytest.fixture
def tracker():
    return ImportTracker()


@pytest.fixture
def module():
    return GeneratorModule()


@pytest.fixture
def serializer(tracker, module):
    return ModelSerializer(tracker, module=module)


def dummy_helper(value, offset=0):
    return value + offset


# ----------------------------------------
# ModelSerializer.serialize()
# ----------------------------------------


def test_serialize__raises_when_not_pydantic_model(serializer):
    class NotAModel:
        pass

    with pytest.raises(ValueError, match="is not a Pydantic model"):
        serializer.serialize(NotAModel)  # type: ignore


def test_serialize__serializes_standard_model(serializer):
    class SimpleModel(BaseModel):
        """A simple model docstring."""

        name: str = Field(description="Name field")

    result = serializer.serialize(SimpleModel)

    assert isinstance(result, GeneratorModel)
    assert result.name == "SimpleModel"
    assert result.docstring == "A simple model docstring."
    assert "BaseModel" in result.bases
    assert len(result.fields) == 1
    assert result.fields[0].name == "name"
    assert result.fields[0].annotation == "str"
    assert result.fields[0].arguments["description"] == '"Name field"'


def test_serialize__includes_properties_and_validators(serializer):

    class ComplexModel(BaseModel):
        val: int

        @property
        def computed_prop(self):
            return self.val

        @field_validator("val", mode="after")
        def validate_val(cls, v):
            return v

        @model_validator(mode="after")
        def validate_model(self):
            return self

    result = serializer.serialize(ComplexModel)

    assert len(result.properties) == 1
    assert result.properties[0].name == "computed_prop"
    assert len(result.field_validators) == 1
    assert result.field_validators[0].name == "validate_val"
    assert len(result.model_validators) == 1
    assert result.model_validators[0].name == "validate_model"


def test_serialize__skips_inherited_properties_and_validators(serializer):

    class ParentModel(BaseModel):
        val: int

        @property
        def inherited_prop(self):
            return self.val

        @field_validator("val", mode="after")
        def inherited_field_val(cls, v):
            return v

        @model_validator(mode="after")
        def inherited_model_val(self):
            return self

    class ChildModel(ParentModel):
        pass

    result = serializer.serialize(ChildModel)

    serialized_models = [m.name for m in serializer._module.models]
    assert "ParentModel" in serialized_models

    assert len(result.properties) == 0
    assert len(result.field_validators) == 0
    assert len(result.model_validators) == 0


def test_serialize__skips_deeply_inherited_properties_and_validators(serializer):

    class GrandParentModel(BaseModel):
        val: int

        @property
        def inherited_prop(self):
            return self.val

        @field_validator("val", mode="after")
        def inherited_field_val(cls, v):
            return v

        @model_validator(mode="after")
        def inherited_model_val(self):
            return self

    class ParentModel(GrandParentModel):
        val: int

    class ChildModel(ParentModel):
        pass

    result = serializer.serialize(ChildModel)

    serialized_models = [m.name for m in serializer._module.models]
    assert "GrandParentModel" in serialized_models
    assert "ParentModel" in serialized_models

    assert len(result.properties) == 0
    assert len(result.field_validators) == 0
    assert len(result.model_validators) == 0


# ----------------------------------------
# ModelSerializer._serialize_base()
# ----------------------------------------


def test_serialize_base__serializes_fhir_resource(serializer):
    result = serializer._serialize_base(fhir.Patient)

    assert result == "fhir.Patient"
    assert (
        "fhircraft.fhir.resources.datatypes.R5"
        in serializer._tracker.alias_imports.keys()
    )
    assert "fhir" in serializer._tracker.alias_imports.values()


def test_serialize_base__serializes_fhir_complex_with_alias(serializer):
    result = serializer._serialize_base(fhir.CodeableConcept)

    assert result == "fhir.CodeableConcept"
    assert (
        "fhircraft.fhir.resources.datatypes.R5"
        in serializer._tracker.alias_imports.keys()
    )
    assert "fhir" in serializer._tracker.alias_imports.values()


def test_serialize_base__serializes_fhir_primitive_with_alias(serializer):
    result = serializer._serialize_base(fhir.String)

    assert result == "fhir.String"
    assert (
        "fhircraft.fhir.resources.datatypes.R5"
        in serializer._tracker.alias_imports.keys()
    )
    assert "fhir" in serializer._tracker.alias_imports.values()


def test_serialize_base__serializes_fhir_slice_model(serializer):
    result = serializer._serialize_base(FHIRSliceModel)

    assert result == "FHIRSliceModel"
    assert "fhircraft.fhir.resources" in serializer._tracker.imports
    assert "FHIRSliceModel" in serializer._tracker.imports["fhircraft.fhir.resources"]


def test_serialize_base__serializes_fhir_base_model(serializer):
    result = serializer._serialize_base(FHIRBaseModel)

    assert result == "FHIRBaseModel"
    assert "fhircraft" in serializer._tracker.imports
    assert "FHIRBaseModel" in serializer._tracker.imports["fhircraft"]


def test_serialize_base__serializes_pydantic_base_model(serializer):
    result = serializer._serialize_base(BaseModel)

    assert result == "BaseModel"
    assert "pydantic" in serializer._tracker.imports
    assert "BaseModel" in serializer._tracker.imports["pydantic"]


@patch("fhircraft.fhir.resources.generator._model.ModelSerializer.serialize")
def test_serialize_base__serializes_custom_base(mock_serialize, serializer):
    mock_serialize.return_value = GeneratorModel(name="CustomBase")

    class CustomBase(BaseModel):
        pass

    result = serializer._serialize_base(CustomBase)

    assert result == "CustomBase"
    assert mock_serialize.called
    assert serializer._module.models[0].name == "CustomBase"


def test_serialize_base__serializes_non_pydantic_base(serializer):
    result = serializer._serialize_base(ABC)

    assert result == "ABC"
    assert "abc" in serializer._tracker.imports
    assert "ABC" in serializer._tracker.imports["abc"]


def test_serialize_base__serializes_non_pydantic_base_without_import(serializer):
    result = serializer._serialize_base(str)

    assert result == "str"


def test_serialize_base__raises_when_no_name(serializer):
    invalid_base = object()  # plain object or non-type instance lacking __name__
    with pytest.raises(ValueError, match="has no __name__ attribute"):
        serializer._serialize_base(invalid_base)


# ----------------------------------------
# ModelSerializer._serialize_metadata()
# ----------------------------------------


def test_serialize_metadata__extracts_fhir_slicing_cardinalities(serializer):

    class SampleSliceModel(FHIRSliceModel):
        min_cardinality = 1
        max_cardinality = 5

    result = serializer._serialize_metadata(SampleSliceModel)

    assert result.min_cardinality == 1
    assert result.max_cardinality == 5


@pytest.mark.parametrize(
    ("class_var", "value", "expected"),
    [
        ("_fhir_release", "R5", '"R5"'),
        (
            "_canonical_url",
            "http://hl7.org/fhir/StructureDefinition/Patient",
            '"http://hl7.org/fhir/StructureDefinition/Patient"',
        ),
        ("_kind", "resource", '"resource"'),
        ("_type", "Patient", '"Patient"'),
        ("_abstract", True, "True"),
    ],
)
def test_serialize_metadata__extracts_fhir_metadata(
    serializer, class_var, value, expected
):
    class SampleFHIRModel(FHIRBaseModel):
        locals()[class_var] = value

    result = serializer._serialize_metadata(SampleFHIRModel)

    assert getattr(result, class_var.lstrip("_")) == expected


def test_serialize_metadata__ignores_inherited_fhir_base_model_metadata(serializer):
    class BaseFHIRModel(FHIRBaseModel):
        _fhir_release = "R5"
        _kind = "resource"

    class ChildFHIRModel(BaseFHIRModel):
        _type = "Patient"

    result = serializer._serialize_metadata(ChildFHIRModel)

    assert result.fhir_release is None
    assert result.kind is None
    assert result.type == '"Patient"'


# ----------------------------------------
# ModelSerializer._serialize_field()
# ----------------------------------------


@pytest.mark.parametrize(
    ("field_argument", "field_value", "expected_serialized"),
    (
        ["default", 2, "2"],
        ["alias", "user_name", '"user_name"'],
        [
            "validation_alias",
            AliasChoices("username", AliasPath("user", "name")),
            "AliasChoices(choices=['username', AliasPath(path=['user', 'name'])])",
        ],
        ["serialization_alias", "userName", '"userName"'],
        ["title", "User Name", '"User Name"'],
        [
            "field_title_generator",
            str,
            "str",
        ],
        ["description", "The user's name", '"The user\'s name"'],
        ["examples", ["John Doe"], '["John Doe"]'],
        ["exclude", False, "False"],
        ["exclude_if", bool, "bool"],
        ["discriminator", "type", '"type"'],
        ["deprecated", False, "False"],
        [
            "json_schema_extra",
            {"custom": "metadata"},
            '{"custom": "metadata"}',
        ],
        ["frozen", False, "False"],
        ["validate_default", True, "True"],
        ["repr", True, "True"],
        ["init", True, "True"],
        ["init_var", False, "False"],
        ["kw_only", False, "False"],
        ["pattern", r"^[A-Za-z ]+$", '"^[A-Za-z ]+$"'],
        ["strict", True, "True"],
        [
            "coerce_numbers_to_str",
            False,
            "False",
        ],
        ["gt", 0, "0"],
        ["ge", 1, "1"],
        ["lt", 100, "100"],
        ["le", 99, "99"],
        ["multiple_of", 1, "1"],
        ["allow_inf_nan", False, "False"],
        ["max_digits", 10, "10"],
        ["decimal_places", 2, "2"],
        ["min_length", 1, "1"],
        ["max_length", 100, "100"],
        ["union_mode", "smart", '"smart"'],
        ["fail_fast", True, "True"],
    ),
)
def test_serialize_field__serializes_field_with_argument(
    serializer, field_argument, field_value, expected_serialized
):
    field = Field(**{field_argument: field_value})

    result = serializer._serialize_field("test", field)

    assert result.name == "test"
    assert field_argument in result.arguments
    assert str(result.arguments[field_argument]) == expected_serialized


def test_serialize_field__serializes_annotation(serializer):
    field = FieldInfo(annotation=Optional[str], default=None)  # type: ignore

    result = serializer._serialize_field("test", field)

    assert result.name == "test"
    assert "annotation" not in result.arguments
    assert "default" in result.arguments
    assert str(result.arguments["default"]) == "None"


# ----------------------------------------
# ModelSerializer._serialize_value()
# ----------------------------------------


class SampleEnum(Enum):
    ALPHA = 1
    BETA = 2


class SampleModel(BaseModel):
    name: str
    age: int


def test_serialize_value__type(serializer):
    result = serializer._serialize_value(int)

    assert result == "int"


def test_serialize_value__list(serializer):
    result = serializer._serialize_value([1, "hello", SampleEnum.ALPHA])
    assert result == '[1, "hello", SampleEnum.ALPHA]'


def test_serialize_value__tuple(serializer):
    result = serializer._serialize_value((1, "world"))
    assert result == '(1, "world")'


def test_serialize_value__dict(serializer):
    data = {"key": 10, "mode": SampleEnum.BETA}
    result = serializer._serialize_value(data)
    assert result == '{"key": 10, "mode": SampleEnum.BETA}'


def test_serialize_value__enum(serializer):
    result = serializer._serialize_value(SampleEnum.ALPHA)
    assert result == "SampleEnum.ALPHA"


def test_serialize_value__string_escaping(serializer):
    raw_str = 'Hello "World" \\ Path'
    result = serializer._serialize_value(raw_str)
    assert result == '"Hello \\"World\\" \\\\ Path"'


def test_serialize_value__lambda_function(serializer):
    sample_lambda = lambda x: x + 1

    result = serializer._serialize_value(sample_lambda)
    assert result == "lambda x: x + 1"


def test_serialize_value__pydantic_model(serializer):
    model = SampleModel(name="Alice", age=30)
    result = serializer._serialize_value(model)
    assert result == 'SampleModel(name="Alice", age=30)'


@pytest.mark.parametrize(
    "primitive_val, expected_repr",
    [
        (42, "42"),
        (3.14, "3.14"),
        (True, "True"),
        (None, "None"),
    ],
)
def test_serialize_value__primitives_fallback(serializer, primitive_val, expected_repr):
    result = serializer._serialize_value(primitive_val)
    assert result == expected_repr


# ----------------------------------------
# ModelSerializer._serialize_property()
# ----------------------------------------


def test_serialize_property__serializes_partial_getter(serializer):
    partial_func = functools.partial(dummy_helper, 10, offset=5)
    prop = property(fget=partial_func)

    result = serializer._serialize_property("test_prop", prop)

    assert isinstance(result, GeneratorModelProperty)
    assert result.name == "test_prop"
    assert result.source is None
    assert result.partial is not None
    assert result.partial.name == "dummy_helper"
    assert result.partial.arguments == ["10"]
    assert result.partial.keywords == {"offset": "5"}
    assert "dummy_helper" in serializer._tracker.imports.get(
        dummy_helper.__module__, {}
    )


def test_serialize_property__serializes_source_getter(serializer):

    class DummyClass(BaseModel):
        @property
        def test_prop(self):
            return "value" + "suffix"

    prop = DummyClass.__dict__["test_prop"]

    result = serializer._serialize_property("test_prop", prop)

    assert isinstance(result, GeneratorModelProperty)
    assert result.name == "test_prop"
    assert result.partial is None
    assert (
        result.source
        == '@property\ndef test_prop(self):\n    return "value" + "suffix"'
    )


def test_serialize_property__raises_when_no_getter(serializer):
    prop = property(fget=None)

    with pytest.raises(ValueError, match="Property test_prop has no getter"):
        serializer._serialize_property("test_prop", prop)


def test_serialize_property__does_not_track_when_track_is_false(serializer):
    partial_func = functools.partial(dummy_helper, 10)
    prop = property(fget=partial_func)

    serializer._serialize_property("test_prop", prop, track=False)

    assert dummy_helper.__module__ not in serializer._tracker.imports


# ----------------------------------------
# ModelSerializer._serialize_model_validator()
# ----------------------------------------


def test_serialize_model_validator__serializes_partial_validator(serializer):
    partial_func = functools.partial(dummy_helper, 20, offset=3)
    mock_decorator = MagicMock()
    mock_decorator.func = partial_func
    mock_decorator.info.mode = "after"

    result = serializer._serialize_model_validator("validate_model", mock_decorator)

    assert isinstance(result, GeneratorModelValidator)
    assert result.name == "validate_model"
    assert result.mode == "after"
    assert result.partial is not None
    assert result.partial.name == "dummy_helper"
    assert result.partial.arguments == ["20"]
    assert result.partial.keywords == {"offset": "3"}


# ----------------------------------------
# ModelSerializer._serialize_field_validator()
# ----------------------------------------


def test_serialize_field_validator__serializes_partial_validator(serializer):
    partial_func = functools.partial(dummy_helper, 10, offset=2)
    mock_decorator = MagicMock()
    mock_decorator.func = partial_func
    mock_decorator.info.mode = "after"
    mock_decorator.info.fields = ("val",)
    mock_decorator.info.check_fields = True

    result = serializer._serialize_field_validator("validate_field", mock_decorator)

    assert isinstance(result, GeneratorFieldValidator)
    assert result.name == "validate_field"
    assert result.mode == "after"
    assert result.fields == ("val",)
    assert result.check_fields is True
    assert result.partial is not None
    assert result.partial.name == "dummy_helper"
    assert result.partial.arguments == ["10"]
    assert result.partial.keywords == {"offset": "2"}
