import unittest
from functools import partial
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic import create_model as _create_model
from pydantic import field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.base import FHIRSliceModel
from fhircraft.fhir.resources.datatypes import primitives
from fhircraft.fhir.resources.datatypes.R4B.complex import CodeableConcept, Coding
from fhircraft.fhir.resources.generator import generate_resource_model_code


def create_model(*args, **kwargs):
    """
    Helper function to create a Pydantic model dynamically.
    """
    return _create_model(*args, __base__=(BaseModel,), **kwargs)


def create_slice_model(*args, **kwargs):
    """
    Helper function to create a Pydantic model dynamically.
    """
    return _create_model(*args, __base__=(FHIRSliceModel,), **kwargs)


class TestJinjaTemplateRendering(unittest.TestCase):

    def _normalize(self, s):
        import re

        return re.sub(r"\s+", " ", s.strip())

    def assertBlockInCode(self, expected_block, model):
        # Generate source code
        code = generate_resource_model_code(model)
        # Assert code block (normalized)
        norm_expected = self._normalize(expected_block)
        norm_code = self._normalize(code)
        self.assertIn(
            norm_expected,
            norm_code,
            f"Expected block not found in generated code.\n\nExpected:\n{expected_block}\n\nGot:\n{code}",
        )

    def test_simple_model(self):
        # Create model dynamically
        model = create_model(
            "SimpleModel",
            id=(primitives.String, Field(description="The unique identifier.")),
            value=(primitives.Integer, Field(default=42, description="A value.")),
        )
        # Expected code block
        expected_class = """
        class SimpleModel(BaseModel):
            id: String = Field(
                description="The unique identifier.",
            )
            value: Integer = Field(
                description="A value.",
                default=42,
            )
        """
        self.assertBlockInCode(expected_class, model)

    def test_model_with_alias(self):
        # Create model dynamically
        model = create_model(
            "ModelWithAlias",
            name=(
                primitives.String,
                Field(alias="fullName", description="The person name."),
            ),
        )
        # Expected code block
        expected_block = """
        class ModelWithAlias(BaseModel):
            name: String = Field(
                description="The person name.",
                alias="fullName",
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_optional(self):
        # Create model dynamically
        model = create_model(
            "ModelWithOptional",
            description=(
                Optional[primitives.String],
                Field(default=None, description="Optional description."),
            ),
        )
        # Expected code block
        expected_block = """
        class ModelWithOptional(BaseModel):
            description: Optional[String] = Field(
                description="Optional description.",
                default=None,
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_list(self):
        # Create model dynamically
        model = create_model(
            "ModelWithList",
            items=(
                List[primitives.Integer],
                Field(default_factory=list, description="A list of items."),
            ),
        )
        # Expected code block
        expected_block = """
        class ModelWithList(BaseModel):
            items: List[Integer] = Field(
                description="A list of items.",
                default_factory=list,
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_default_factory_model(self):
        # Create model dynamically
        model = create_model(
            "ModelWithDefaultFactoryModel",
            codes=(
                CodeableConcept,
                Field(
                    default=CodeableConcept(
                        coding=[Coding(code="12345", system="http://example.org")]
                    ),
                    description="A default CodeableConcept.",
                ),
            ),
        )
        # Expected code block
        expected_block = """
        class ModelWithDefaultFactoryModel(BaseModel):
            codes: CodeableConcept = Field(
                description="A default CodeableConcept.",
                default_factory=lambda: CodeableConcept(coding=[Coding(code="12345", system="http://example.org")]),
            )
        """
        self.assertBlockInCode(expected_block, model)
        self.assertBlockInCode(
            "from fhircraft.fhir.resources.datatypes.R4B.complex.codeable_concept import CodeableConcept",
            model,
        )
        self.assertBlockInCode(
            "from fhircraft.fhir.resources.datatypes.R4B.complex.coding import Coding",
            model,
        )

    def test_model_with_field_validator(self):
        # Create model dynamically
        model = create_model(
            "ModelWithPatternValidator",
            code=(
                CodeableConcept,
                Field(
                    description="A code field with pattern constraint.",
                ),
            ),
            __validators__={
                "FHIR_code_pattern_constraint": (
                    field_validator(*("code",), mode="after", check_fields=None)(
                        partial(
                            fhir_validators.validate_FHIR_element_pattern,
                            pattern=CodeableConcept(
                                coding=[
                                    Coding(
                                        system="http://example.org",
                                        display="code",
                                        code="12345",
                                    )
                                ]
                            ),
                        )
                    )
                )
            },
        )
        # Expected code block
        expected_block = """
        class ModelWithPatternValidator(BaseModel):
            code: CodeableConcept = Field(
                description="A code field with pattern constraint.",
            )

            @field_validator(*('code',), mode="after", check_fields=None)
            @classmethod
            def FHIR_code_pattern_constraint(cls, value):    
                return validate_FHIR_element_pattern(cls, value,
                    pattern=CodeableConcept(coding=[Coding(code="12345",  display="code", system="http://example.org")]),
                )
        """
        self.assertBlockInCode(expected_block, model)
        # Check imports
        self.assertBlockInCode(
            "from fhircraft.fhir.resources.datatypes.R4B.complex.codeable_concept import CodeableConcept",
            model,
        )
        self.assertBlockInCode(
            "from fhircraft.fhir.resources.datatypes.R4B.complex.coding import Coding",
            model,
        )

    def test_model_with_model_validator(self):
        # Create model dynamically
        model = create_model(
            "ModelWithModelValidator",
            code=(
                CodeableConcept,
                Field(
                    description="A code field with model constraint.",
                ),
            ),
            __validators__={
                "FHIR_ele_1_constraint_model_validator": (
                    model_validator(mode="after")(
                        partial(
                            fhir_validators.validate_model_constraint,
                            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
                            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
                            key="ele-1",
                            severity="error",
                        )
                    )
                )
            },
        )
        # Expected code block
        expected_block = """
        class ModelWithModelValidator(BaseModel):
            code: CodeableConcept = Field(
                description="A code field with model constraint.",
            )

            @model_validator(mode="after")
            def FHIR_ele_1_constraint_model_validator(self):
                return validate_model_constraint(
                    self,
                    expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
                    human="All FHIR elements must have a @value or children unless an empty Parameters resource",
                    key="ele-1",
                    severity="error",
                )

        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_field_title(self):
        # Create model dynamically
        model = create_model(
            "ModelWithTitle",
            code=(
                primitives.String,
                Field(title="Code Field", description="A code with title."),
            ),
        )
        expected_block = """
        class ModelWithTitle(BaseModel):
            code: String = Field(
                title="Code Field",
                description="A code with title.",
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_multiple_field_validators(self):
        # Create model dynamically
        model = create_model(
            "ModelWithValidators",
            codeA=(CodeableConcept, Field(description="A first code.")),
            codeB=(CodeableConcept, Field(description="A second code.")),
            __validators__={
                "FHIR_codeA_pattern_constraint": (
                    field_validator(*("codeA",), mode="after", check_fields=None)(
                        partial(
                            fhir_validators.validate_FHIR_element_pattern,
                            pattern=CodeableConcept(
                                coding=[
                                    Coding(
                                        system="http://example.org",
                                        display="code-1",
                                        code="12345",
                                    )
                                ]
                            ),
                        )
                    )
                ),
                "FHIR_codeB_pattern_constraint": (
                    field_validator(*("codeB",), mode="after", check_fields=None)(
                        partial(
                            fhir_validators.validate_FHIR_element_pattern,
                            pattern=CodeableConcept(
                                coding=[
                                    Coding(
                                        system="http://example.org",
                                        display="code-2",
                                        code="67890",
                                    )
                                ]
                            ),
                        )
                    )
                ),
            },
        )
        expected_block = """
        class ModelWithValidators(BaseModel):
            codeA: CodeableConcept = Field(
                description="A first code.",
            )
            codeB: CodeableConcept = Field(
                description="A second code.",
            )

            @field_validator(*('codeA',), mode="after", check_fields=None)
            @classmethod
            def FHIR_codeA_pattern_constraint(cls, value):    
                return validate_FHIR_element_pattern(cls, value,
                    pattern=CodeableConcept(coding=[Coding(code="12345", display="code-1", system="http://example.org")]),
                )

            @field_validator(*('codeB',), mode="after", check_fields=None)
            @classmethod
            def FHIR_codeB_pattern_constraint(cls, value):    
                return validate_FHIR_element_pattern(cls, value,
                    pattern=CodeableConcept(coding=[Coding(code="67890", display="code-2", system="http://example.org")]),
                )
        """
        self.assertBlockInCode(expected_block, model)
        # Check imports
        self.assertBlockInCode(
            "from fhircraft.fhir.resources.datatypes.R4B.complex.codeable_concept import CodeableConcept",
            model,
        )
        self.assertBlockInCode(
            "from fhircraft.fhir.resources.datatypes.R4B.complex.coding import Coding",
            model,
        )

    def test_model_with_list_of_complex(self):
        # Create model dynamically
        model = create_model(
            "ModelWithComplexList",
            codings=(
                List[Coding],
                Field(default_factory=list, description="A list of Coding objects."),
            ),
        )
        expected_block = """
        class ModelWithComplexList(BaseModel):
            codings: List[Coding] = Field(
                description="A list of Coding objects.",
                default_factory=list,
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_docstring(self):
        # Create model dynamically
        model = create_model(
            "ModelWithDocstring",
            value=(primitives.String, Field(description="A string field.")),
            __doc__="This is a model with a docstring.",
        )
        expected_block = '''
        class ModelWithDocstring(BaseModel):
            """
            This is a model with a docstring.
            """
            value: String = Field(
                description="A string field.",
            )

        '''
        self.assertBlockInCode(expected_block, model)

    def test_model_with_fixed_value_enum_field(self):
        # Define an Enum
        from enum import Enum

        class Color(Enum):
            fixedValue = "red"

        model = create_model(
            "ModelWithEnum", color=(Color, Field(description="A color enum."))
        )
        expected_block = """
        class ModelWithEnum(BaseModel):
            color: Literal['red'] = Field(
                description="A color enum.",
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_sliced_field(self):

        model = create_slice_model(
            "Slice", valueString=(str, Field(description="A string value"))
        )
        model.min_cardinality = 0
        model.max_cardinality = 2
        expected_block = """
        class Slice(FHIRSliceModel):
            min_cardinality: ClassVar[int] = 0
            max_cardinality: ClassVar[int] = 2
            valueString: str = Field(
                description="A string value",
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_property_method(self):
        # Create model with a property
        model = create_model(
            "ModelWithProperty",
            valueString=(primitives.String, Field(description="A value.")),
            valueInteger=(primitives.Integer, Field(description="A value.")),
        )
        # Add a property method
        setattr(
            model,
            "value",
            property(
                partial(fhir_validators.get_type_choice_value_by_base, base="value")
            ),
        )

        expected_block = """
        class ModelWithProperty(BaseModel):
            valueString: String = Field(
                description="A value.",
            )
            valueInteger: Integer = Field(
                description="A value.",
            )

            @property 
            def value(self):
                return get_type_choice_value_by_base(self,
                    base="value", 
                )
        """
        self.assertBlockInCode(expected_block, model)
