import unittest
from pydantic import BaseModel, Field
from typing import Optional, List
from fhircraft.fhir.resources.generator import generate_resource_model_code
from fhircraft.fhir.resources.datatypes import primitives 

class SimpleModel(BaseModel):
    id: primitives.String = Field(description="The unique identifier.")
    value: primitives.Integer = Field(default=42, description="A value.")

class ModelWithAlias(BaseModel):
    name: primitives.String = Field(alias="fullName", description="The person name.")

class ModelWithOptional(BaseModel):
    description: Optional[primitives.String] = Field(default=None, description="Optional description.")

class ModelWithList(BaseModel):
    items: List[primitives.Integer] = Field(default_factory=list, description="A list of items.")

class ModelWithProperty(BaseModel):
    value: primitives.Integer = Field(default=1)
    @property
    def double(self):
        return self.value * 2

class TestJinjaTemplateRendering(unittest.TestCase):

    def _normalize(self, s):
        import re
        return re.sub(r'\s+', ' ', s.strip())

    def assertBlockInCode(self, expected_block, code):
        norm_expected = self._normalize(expected_block)
        norm_code = self._normalize(code)
        self.assertIn(norm_expected, norm_code, f'Expected block not found in generated code.\n\nExpected:\n{expected_block}\n\nGot:\n{code}')

    def test_simple_model(self):
        code = generate_resource_model_code(SimpleModel)
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
        self.assertBlockInCode(expected_class, code)

    def test_model_with_alias(self):
        code = generate_resource_model_code(ModelWithAlias)
        expected_block = """
        class ModelWithAlias(BaseModel):
            name: String = Field(
                description="The person name.",
                alias="fullName",
            )
        """
        self.assertBlockInCode(expected_block, code)

    def test_model_with_optional(self):
        code = generate_resource_model_code(ModelWithOptional)
        expected_block = """
        class ModelWithOptional(BaseModel):
            description: Optional[String] = Field(
                description="Optional description.",
                default=None,
            )
        """
        self.assertBlockInCode(expected_block, code)

    def test_model_with_list(self):
        code = generate_resource_model_code(ModelWithList)
        expected_block = """
        class ModelWithList(BaseModel):
            items: List[Integer] = Field(
                description="A list of items.",
                default_factory=list,
            )
        """
        self.assertBlockInCode(expected_block, code)

    def test_model_with_property(self):
        code = generate_resource_model_code(ModelWithProperty)
        # Accept either the property as generated or the fallback property
        expected_property = """
        @property
        def double(self):
            return self.value * 2
        """
        self.assertBlockInCode(expected_property, code)

if __name__ == "__main__":
    unittest.main()
