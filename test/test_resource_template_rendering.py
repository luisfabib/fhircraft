import unittest
from functools import partial
from pydantic import BaseModel, Field, create_model as _create_model
from typing import Optional, List
from fhircraft.fhir.resources.generator import generate_resource_model_code
from fhircraft.fhir.resources.datatypes import primitives 
from fhircraft.fhir.resources.datatypes.R4B.complex_types import CodeableConcept, Coding
import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, field_validator, model_validator, BaseModel

def create_model(*args, **kwargs):
    """
    Helper function to create a Pydantic model dynamically.
    """
    return _create_model(*args, __base__=(BaseModel,), **kwargs)

class TestJinjaTemplateRendering(unittest.TestCase):

    def _normalize(self, s):
        import re
        return re.sub(r'\s+', ' ', s.strip())

    def assertBlockInCode(self, expected_block, model):
        # Generate source code
        code = generate_resource_model_code(model)
        # Assert code block (normalized)
        norm_expected = self._normalize(expected_block)
        norm_code = self._normalize(code)
        self.assertIn(norm_expected, norm_code, f'Expected block not found in generated code.\n\nExpected:\n{expected_block}\n\nGot:\n{code}')

    def test_simple_model(self):
        # Create model dynamically
        model = create_model('SimpleModel',
            id=(primitives.String, Field(description="The unique identifier.")),
            value=(primitives.Integer, Field(default=42, description="A value."))
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
        model = create_model('ModelWithAlias',
            name=(primitives.String, Field(alias="fullName", description="The person name."))
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
        model = create_model('ModelWithOptional',
            description=(Optional[primitives.String], Field(default=None, description="Optional description."))
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
        model = create_model('ModelWithList',
            items=(List[primitives.Integer], Field(default_factory=list, description="A list of items."))
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

    def test_model_with_pattern_validator(self):
        # Create model dynamically
        model = create_model('ModelWithPatternValidator',
            code=(CodeableConcept, Field(
                description="A code field with pattern constraint.",
            )),
            __validators__={
                'FHIR_code_pattern_constraint': (
                    field_validator(*('code',), mode="after", check_fields=None)(
                        partial(fhir_validators.validate_FHIR_element_pattern, 
                                pattern=CodeableConcept(coding=[Coding(system='http://loinc.org', display='Lifestyle', code='LA32823-9')])
                        )
                    )
                )
            }
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
                    pattern=CodeableConcept(coding=[{'system': 'http://loinc.org', 'code': 'LA32823-9', 'display': 'Lifestyle'}]),
                )
        """
        self.assertBlockInCode(expected_block, model)


if __name__ == "__main__":
    unittest.main()
