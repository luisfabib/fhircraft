import unittest
from functools import partial
from typing import List, Optional
import pytest

from pydantic import BaseModel, Field
from pydantic import create_model as _create_model
from pydantic import field_validator, model_validator

from fhircraft.fhir.resources.datatypes.R4.core.domain_resource import DomainResource
import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.base import FHIRSliceModel
from fhircraft.fhir.resources.datatypes import primitives
from fhircraft.fhir.resources.datatypes.R4B.complex import CodeableConcept, Coding
from fhircraft.fhir.resources.generator import generate_resource_model_code


def create_model(*args, bases=(BaseModel,), **kwargs):
    """
    Helper function to create a Pydantic model dynamically.
    """
    return _create_model(*args, __base__=bases, **kwargs)


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
            "from fhircraft.fhir.resources.datatypes.R4B.complex import CodeableConcept, Coding",
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
            "from fhircraft.fhir.resources.datatypes.R4B.complex import CodeableConcept, Coding",
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
                "FHIR_ele_1_constraint_validator": (
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
            def FHIR_ele_1_constraint_validator(self):
                return validate_model_constraint(
                    self,
                    expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
                    human="All FHIR elements must have a @value or children unless an empty Parameters resource",
                    key="ele-1",
                    severity="error",
                )

        """
        self.assertBlockInCode(expected_block, model)

    def test_inherited_validators_not_included(self):
        # Create model dynamically
        model = create_model(
            "ModelWithModelValidator",
            bases=(DomainResource,),
            code=(
                CodeableConcept,
                Field(
                    description="A code field with model constraint.",
                ),
            ),
            __validators__={
                "FHIR_custom_1_constraint_validator": (
                    model_validator(mode="after")(
                        partial(
                            fhir_validators.validate_model_constraint,
                            expression="exists()",
                            human="All FHIR elements must exist.",
                            key="custom-1",
                            severity="error",
                        )
                    )
                )
            },
        )
        # Expected code block
        expected_block = """
        class ModelWithModelValidator(DomainResource):
            code: CodeableConcept = Field(
                description="A code field with model constraint.",
            )

            @model_validator(mode="after")
            def FHIR_custom_1_constraint_validator(self):
                return validate_model_constraint(
                    self,
                    expression="exists()",
                    human="All FHIR elements must exist.",
                    key="custom-1",
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
            "from fhircraft.fhir.resources.datatypes.R4B.complex import CodeableConcept, Coding",
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
            max_cardinality: ClassVar[int | None] = 2

            valueString: str = Field(
                description="A string value",
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_multiple_inheritance_slice(self):
        """Test that slice models with multiple inheritance generate correctly."""
        from fhircraft.fhir.resources.datatypes.R4B.complex.extension import Extension
        from fhircraft.fhir.resources.base import FHIRSliceModel

        # Create a model with multiple inheritance (Extension + FHIRSliceModel)
        model = _create_model(
            "ExtensionSlice",
            url=(str, Field(description="Extension URL")),
            valueString=(str, Field(description="A string value")),
            __base__=(Extension, FHIRSliceModel),
        )
        assert issubclass(model, FHIRSliceModel)
        model.min_cardinality = 1
        model.max_cardinality = 1

        expected_block = """
        class ExtensionSlice(Extension, FHIRSliceModel):
            min_cardinality: ClassVar[int] = 1
            max_cardinality: ClassVar[int | None] = 1
            
            url: str = Field(
                description="Extension URL",
            )
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

    def test_model_with_multiline_expression(self):
        # Create model with multiline FHIRPath expression
        multiline_expression = """extension.where(url = 'http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-radiotherapy-modality').exists() and
      extension.where(url = 'http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-radiotherapy-modality').value.exists() and
      extension.where(url = 'http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-radiotherapy-modality').value.coding.exists(system = 'http://snomed.info/sct' and code = '10611004')
   implies
      extension.where(url = 'http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-radiotherapy-technique').exists()"""

        model = create_model(
            "ModelWithMultilineExpression",
            code=(
                CodeableConcept,
                Field(description="A code field with multiline constraint."),
            ),
            __validators__={
                "FHIR_TechniquesForProtonBeamModality_constraint_validator": (
                    model_validator(mode="after")(
                        partial(
                            fhir_validators.validate_model_constraint,
                            expression=multiline_expression,
                            human="Allowed Techniques for Proton Beam Modality",
                            key="TechniquesForProtonBeamModality",
                            severity="error",
                        )
                    )
                )
            },
        )

        # Generate the code
        code = generate_resource_model_code(model)

        # Verify that triple quotes are used for multiline expression
        self.assertIn(
            'expression="""extension.where',
            code,
            "Multiline expression should use triple quotes",
        )
        self.assertIn("extension.where(url", code)
        self.assertIn("TechniquesForProtonBeamModality", code)

        # Verify the code is valid Python by attempting to compile it
        try:
            compile(code, "<generated>", "exec")
        except SyntaxError as e:
            self.fail(
                f"Generated code has syntax error: {e}\n\nGenerated code:\n{code}"
            )

    def test_model_with_string_containing_quotes(self):
        # Create model with expression containing double quotes
        expression_with_quotes = 'This is a "quoted" string'

        model = create_model(
            "ModelWithQuotedString",
            code=(
                CodeableConcept,
                Field(description="A code field."),
            ),
            __validators__={
                "FHIR_test_constraint": (
                    model_validator(mode="after")(
                        partial(
                            fhir_validators.validate_model_constraint,
                            expression=expression_with_quotes,
                            human="Test with quotes",
                            key="test-1",
                            severity="error",
                        )
                    )
                )
            },
        )

        # Generate the code
        code = generate_resource_model_code(model)

        # Verify that quotes are properly escaped
        self.assertIn(
            'expression="This is a \\"quoted\\" string"',
            code,
            "Double quotes should be escaped in single-line strings",
        )

        # Verify the code is valid Python
        try:
            compile(code, "<generated>", "exec")
        except SyntaxError as e:
            self.fail(
                f"Generated code has syntax error: {e}\n\nGenerated code:\n{code}"
            )

    def test_model_with_string_containing_backslashes(self):
        # Create model with expression containing backslashes
        expression_with_backslashes = "C:\\path\\to\\file"

        model = create_model(
            "ModelWithBackslashes",
            code=(
                CodeableConcept,
                Field(description="A code field."),
            ),
            __validators__={
                "FHIR_test_constraint": (
                    model_validator(mode="after")(
                        partial(
                            fhir_validators.validate_model_constraint,
                            expression=expression_with_backslashes,
                            human="Test with backslashes",
                            key="test-1",
                            severity="error",
                        )
                    )
                )
            },
        )

        # Generate the code
        code = generate_resource_model_code(model)

        # Verify the code is valid Python and backslashes are properly handled
        try:
            compile(code, "<generated>", "exec")
        except SyntaxError as e:
            self.fail(
                f"Generated code has syntax error: {e}\n\nGenerated code:\n{code}"
            )

        # Execute the code and verify the string value is preserved
        namespace = {}
        exec(code, namespace)
        # The expression string should be preserved correctly

    def test_import_grouping_by_common_parent(self):
        """Test that imports are grouped by their common parent modules."""
        # Create model with types from the same module
        model = create_model(
            "ModelWithGroupedImports",
            concept=(CodeableConcept, Field(description="A concept")),
            coding=(Coding, Field(description="A coding")),
        )

        code = generate_resource_model_code(model)

        # Should generate grouped import instead of individual imports
        self.assertBlockInCode(
            "from fhircraft.fhir.resources.datatypes.R4B.complex import CodeableConcept, Coding",
            model,
        )

        # Should NOT have individual imports
        self.assertNotIn(
            "from fhircraft.fhir.resources.datatypes.R4B.complex.codeable_concept import CodeableConcept",
            code,
        )
        self.assertNotIn(
            "from fhircraft.fhir.resources.datatypes.R4B.complex.coding import Coding",
            code,
        )

    def test_profile_with_multiple_ancestors(self):
        # Create model dynamically
        child_model = create_model(
            "ChildModel",
            bases=(DomainResource,),
            childField=(
                str,
                Field(
                    description="A field of the child model",
                ),
            ),
            __validators__={
                "FHIR_child_1_constraint_validator": (
                    model_validator(mode="after")(
                        partial(
                            fhir_validators.validate_model_constraint,
                            expression="exists()",
                            human="Child model constraint",
                            key="child-1",
                            severity="error",
                        )
                    )
                )
            },
        )
        grand_child_model = create_model(
            "GrandChildModel",
            bases=(child_model,),
            grandChildField=(
                int,
                Field(
                    description="A field of the grandchild model",
                ),
            ),
            __validators__={
                "FHIR_grandchild_1_constraint_validator": (
                    model_validator(mode="after")(
                        partial(
                            fhir_validators.validate_model_constraint,
                            expression="exists()",
                            human="Grandchild model constraint",
                            key="grandchild-1",
                            severity="error",
                        )
                    )
                )
            },
        )
        # Expected code block
        expected_block = """
        class ChildModel(DomainResource):
        
            childField: str = Field(
                description="A field of the child model",
            )

            @model_validator(mode="after")
            def FHIR_child_1_constraint_validator(self):
                return validate_model_constraint(
                    self,
                    expression="exists()",
                    human="Child model constraint",
                    key="child-1",
                    severity="error",
                )

        class GrandChildModel(ChildModel):
        
            grandChildField: int = Field(
                description="A field of the grandchild model",
            )

            @model_validator(mode="after")
            def FHIR_grandchild_1_constraint_validator(self):
                return validate_model_constraint(
                    self,
                    expression="exists()",
                    human="Grandchild model constraint",
                    key="grandchild-1",
                    severity="error",
                )
        """
        self.assertBlockInCode(expected_block, grand_child_model)

    def test_property_inheritance_skips_identical_property(self):
        """Test that inherited properties with identical implementations are skipped."""
        # Create a base model with a property
        base_model = _create_model(
            "BaseModelWithProperty",
            valueString=(primitives.String, Field(description="A value.")),
            __base__=(BaseModel,),
        )
        setattr(
            base_model,
            "value",
            property(
                partial(fhir_validators.get_type_choice_value_by_base, base="value")
            ),
        )

        # Create a derived model that inherits the same property
        derived_model = _create_model(
            "DerivedModelWithInheritedProperty",
            valueInteger=(primitives.Integer, Field(description="Another value.")),
            __base__=(base_model,),
        )
        # Inherit the property by setting it to the same implementation
        setattr(
            derived_model,
            "value",
            property(
                partial(fhir_validators.get_type_choice_value_by_base, base="value")
            ),
        )

        code = generate_resource_model_code(derived_model)
        # The property should NOT be in the derived model code since it's identical to the base
        # Count how many @property decorators appear in the generated code for the derived model
        lines = code.split("\n")
        derived_class_started = False
        derived_class_property_count = 0
        for line in lines:
            if "class DerivedModelWithInheritedProperty" in line:
                derived_class_started = True
            elif derived_class_started and line.strip().startswith("class "):
                # Another class started, so we're done with derived model
                break
            elif derived_class_started and "@property" in line:
                derived_class_property_count += 1

        self.assertEqual(
            derived_class_property_count,
            0,
            "Identical inherited property should not be in generated code for derived model",
        )

    def test_property_inheritance_includes_overridden_property(self):
        """Test that properties with different implementations are included."""
        # Create a base model with a property
        base_model = _create_model(
            "BaseModelWithOriginalProperty",
            valueString=(primitives.String, Field(description="A value.")),
            __base__=(BaseModel,),
        )
        setattr(
            base_model,
            "value",
            property(
                partial(fhir_validators.get_type_choice_value_by_base, base="value")
            ),
        )

        # Create a derived model that overrides the property with different implementation
        derived_model = _create_model(
            "DerivedModelWithOverriddenProperty",
            valueInteger=(primitives.Integer, Field(description="Another value.")),
            __base__=(base_model,),
        )
        # Override the property with different base parameter
        setattr(
            derived_model,
            "value",
            property(
                partial(
                    fhir_validators.get_type_choice_value_by_base, base="different_base"
                )
            ),
        )

        code = generate_resource_model_code(derived_model)
        # The property SHOULD be in the derived model code since it's different
        expected_block = """
        class DerivedModelWithOverriddenProperty(BaseModelWithOriginalProperty):
            valueInteger: Integer = Field(
                description="Another value.",
            )

            @property 
            def value(self):
                return get_type_choice_value_by_base(self,
                    base="different_base", 
                )
        """
        self.assertBlockInCode(expected_block, derived_model)

    def test_property_inheritance_includes_new_property(self):
        """Test that new properties not in base class are included."""
        # Create a base model without any property
        base_model = _create_model(
            "BaseModelWithoutProperty",
            valueString=(primitives.String, Field(description="A value.")),
            __base__=(BaseModel,),
        )

        # Create a derived model that adds a new property
        derived_model = _create_model(
            "DerivedModelWithNewProperty",
            valueInteger=(primitives.Integer, Field(description="Another value.")),
            __base__=(base_model,),
        )
        # Add a new property that doesn't exist in base
        setattr(
            derived_model,
            "newProperty",
            property(
                partial(fhir_validators.get_type_choice_value_by_base, base="value")
            ),
        )

        code = generate_resource_model_code(derived_model)
        # The new property SHOULD be in the derived model code
        expected_block = """
        class DerivedModelWithNewProperty(BaseModelWithoutProperty):
            valueInteger: Integer = Field(
                description="Another value.",
            )

            @property 
            def newProperty(self):
                return get_type_choice_value_by_base(self,
                    base="value", 
                )
        """
        self.assertBlockInCode(expected_block, derived_model)

    def test_property_inheritance_multiple_levels(self):
        """Test property inheritance checking across multiple levels of inheritance."""
        # Create a grandparent model with a property
        grandparent_model = _create_model(
            "GrandparentWithProperty",
            value=(primitives.String, Field(description="A value.")),
            __base__=(BaseModel,),
        )
        setattr(
            grandparent_model,
            "computedValue",
            property(
                partial(fhir_validators.get_type_choice_value_by_base, base="value")
            ),
        )

        # Create a parent model that inherits from grandparent
        parent_model = _create_model(
            "ParentModel",
            parentField=(primitives.String, Field(description="Parent field.")),
            __base__=(grandparent_model,),
        )

        # Create a child model that inherits from parent but doesn't override the property
        child_model = _create_model(
            "ChildModel",
            childField=(primitives.String, Field(description="Child field.")),
            __base__=(parent_model,),
        )

        code = generate_resource_model_code(child_model)
        # The computedValue property should NOT be in child model since it's inherited
        lines = code.split("\n")
        child_class_started = False
        child_class_has_property = False
        for line in lines:
            if "class ChildModel" in line:
                child_class_started = True
            elif child_class_started and line.strip().startswith("class "):
                break
            elif child_class_started and "@property" in line:
                child_class_has_property = True

        self.assertFalse(
            child_class_has_property,
            "Inherited property should not appear in child class",
        )

    def test_model_with_prohibited_field_renders_none_annotation(self):
        """A field with annotation=type(None) (0..0 cardinality) must render as 'None', not \"<class 'NoneType'>\"."""
        model = create_model(
            "ModelWithProhibitedField",
            active=(
                primitives.Boolean,
                Field(default=None, description="Active flag."),
            ),
            prohibited=(
                type(None),
                Field(default=None, description="Prohibited field."),
            ),
        )
        expected_block = """
            prohibited: None = Field(
                description="Prohibited field.",
                default=None,
            )
        """
        self.assertBlockInCode(expected_block, model)
        code = generate_resource_model_code(model)
        self.assertNotIn("<class 'NoneType'>", code)


@pytest.mark.parametrize(
    "model",
    [
        "Patient",
        "Observation",
        "Condition",
        "MedicationRequest",
        "Encounter",
        "Practitioner",
        "AllergyIntolerance",
        "Procedure",
        "Immunization",
        "DiagnosticReport",
        "CarePlan",
        "ServiceRequest",
        "FamilyMemberHistory",
        "Device",
        "Goal",
        "Specimen",
        "StructureDefinition",
    ],
)
def test_code_generates_for_builtin_models(model):
    """Test that code generation works for built-in FHIR resource models."""
    from fhircraft.fhir.resources.datatypes.R5 import core

    # Generate code for Patient model
    code = generate_resource_model_code(getattr(core, model))

    # Check for some expected elements in the generated code
    assert f"class {model}(DomainResource):" in code

    # Fake compile to ensure no syntax errors
    try:
        compile(code, "<generated>", "exec")
    except SyntaxError as e:
        pytest.fail(
            f"Generated code for {model} has syntax error: {e}\n\nGenerated code:\n{code}"
        )
