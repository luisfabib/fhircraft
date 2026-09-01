from textwrap import dedent
import pytest

from fhircraft.fhir.resources.generator._schemas import (
    GeneratorModelField,
    GeneratorModelProperty,
    GeneratorModelValidator,
    GeneratorFieldValidator,
    GeneratorPartialFunction,
)
from fhircraft.fhir.resources.generator.core import JINJA_ENV


@pytest.fixture
def jinja_env():
    """Initializes the Jinja environment and imports the macros into memory."""

    template = JINJA_ENV.get_template("macros.py.j2")
    return template.module


# ----------------------------------------
# Template render_field() macro tests
# ----------------------------------------


def test_render_field__simple(jinja_env):
    field_obj = GeneratorModelField(
        name="age",
        annotation="int",
        arguments={"default": 0, "ge": 0},
    )

    rendered = jinja_env.render_field(field_obj)

    expected = dedent("""
        age: int = Field(
            default=0,
            ge=0,
        )
    """)
    assert rendered.strip() == expected.strip()


def test_render_field__no_arguments(jinja_env):
    field_obj = GeneratorModelField(
        name="age",
        annotation="int",
    )

    rendered = jinja_env.render_field(field_obj)

    expected = dedent("""
        age: int = Field(\n)
    """)
    assert rendered.strip() == expected.strip()


def test_render_property(jinja_env):
    prop_obj = GeneratorModelProperty(
        name="is_adult",
        partial=GeneratorPartialFunction(
            name="check_adult",
            arguments=["18"],
            keywords={"strict": True},
        ),
    )

    rendered = jinja_env.render_property(prop_obj)

    expected = dedent("""
        @property
        def is_adult(self):
            return check_adult(self,
                18,
                strict=True,
            )
    """)
    assert rendered.strip() == expected.strip()


def test_render_field_validator(jinja_env):
    validator_obj = GeneratorFieldValidator(
        fields=("age", "height"),
        mode="before",
        check_fields=True,
        name="validate_numbers",
        partial=GeneratorPartialFunction(
            name="parse_numeric",
            arguments=["allow_strings=True"],
            keywords={"custom_flag": True},
        ),
    )

    rendered = jinja_env.render_field_validator(validator_obj)

    expected = dedent("""
        @field_validator(*('age', 'height'), mode="before", check_fields=True)
        @classmethod
        def validate_numbers(cls, value):
            return parse_numeric(cls, value,
                allow_strings=True,
                custom_flag=True,
            )
    """)
    assert rendered.strip() == expected.strip()


def test_render_model_validator_partial(jinja_env):
    validator_obj = GeneratorModelValidator(
        mode="after",
        name="validate_model",
        partial=GeneratorPartialFunction(
            name="check_model_state",
            arguments=["'strict_mode'"],
            keywords={"timeout": 30},
        ),
    )

    rendered = jinja_env.render_model_validator(validator_obj)

    expected = dedent("""
        @model_validator(mode="after")
        def validate_model(self):
            return check_model_state(self,
                'strict_mode',
                timeout=30,
            )
    """)
    assert rendered.strip() == expected.strip()


def test_render_model_validator_source(jinja_env):
    validator_obj = GeneratorModelValidator(
        mode="after",
        name="validate_model",
        source="@model_validator(mode=\"after\")\ndef validate_model(self):\n    return check_model_state(self, 'strict_mode', timeout=30)",
    )

    rendered = jinja_env.render_model_validator(validator_obj)

    expected = dedent("""
        @model_validator(mode="after")
        def validate_model(self):
            return check_model_state(self, 'strict_mode', timeout=30)
    """)
    assert rendered.strip() == expected.strip()
