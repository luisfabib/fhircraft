"""
Integration tests for CodeGenerator. These tests validate the full pipeline
by asserting on both the output code string and the intermediate serializer data.
"""
import unittest
from functools import partial
from typing import List, Optional

import pytest
from pydantic import BaseModel, Field
from pydantic import create_model as _create_model
from pydantic import field_validator, model_validator

from fhircraft.fhir.resources.base import FHIRSliceModel
from fhircraft.fhir.resources.datatypes.R4.core.domain_resource import DomainResource
from fhircraft.fhir.resources.datatypes.R4B import primitive as primitives
from fhircraft.fhir.resources.datatypes.R4B.complex import CodeableConcept, Coding
import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.generator import CodeGenerator, generate_code


def create_model(*args, bases=(BaseModel,), **kwargs):
    return _create_model(*args, __base__=bases, **kwargs)


def create_slice_model(*args, **kwargs):
    return _create_model(*args, __base__=(FHIRSliceModel,), **kwargs)


class TestCodeGenerator(unittest.TestCase):

    def setUp(self):
        self.gen = CodeGenerator()

    def _normalize(self, s):
        import re
        return re.sub(r"\s+", " ", s.strip()).replace("'", '"')

    def assertBlockInCode(self, expected_block, model):
        code = self.gen.generate(model)
        norm_expected = self._normalize(expected_block)
        norm_code = self._normalize(code)
        self.assertIn(
            norm_expected,
            norm_code,
            f"Expected block not found in generated code.\n\nExpected:\n{expected_block}\n\nGot:\n{code}",
        )

    # ------------------------------------------------------------------
    # Basic field rendering
    # ------------------------------------------------------------------

    def test_simple_model(self):
        model = create_model(
            "SimpleModel",
            id=(primitives.String, Field(description="The unique identifier.")),
            value=(primitives.Integer, Field(default=42, description="A value.")),
        )
        expected_class = """
        class SimpleModel(BaseModel):
            id: fhir.string = Field(
                description="The unique identifier.",
            )
            value: fhir.integer = Field(
                description="A value.",
                default=42,
            )
        """
        self.assertBlockInCode(expected_class, model)

    def test_model_with_alias(self):
        model = create_model(
            "ModelWithAlias",
            name=(primitives.String, Field(alias="fullName", description="The person name.")),
        )
        expected_block = """
        class ModelWithAlias(BaseModel):
            name: fhir.string = Field(
                description="The person name.",
                alias="fullName",
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_optional(self):
        model = create_model(
            "ModelWithOptional",
            description=(Optional[primitives.String], Field(default=None, description="Optional description.")),
        )
        expected_block = """
        class ModelWithOptional(BaseModel):
            description: Optional[fhir.string] = Field(
                description="Optional description.",
                default=None,
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_list(self):
        model = create_model(
            "ModelWithList",
            items=(List[primitives.Integer], Field(default_factory=list, description="A list of items.")),
        )
        expected_block = """
        class ModelWithList(BaseModel):
            items: List[fhir.integer] = Field(
                description="A list of items.",
                default_factory=list,
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_default_factory_model(self):
        model = create_model(
            "ModelWithDefaultFactoryModel",
            codes=(
                CodeableConcept,
                Field(
                    default=CodeableConcept(coding=[Coding(code="12345", system="http://example.org")]),
                    description="A default CodeableConcept.",
                ),
            ),
        )
        expected_block = """
        class ModelWithDefaultFactoryModel(BaseModel):

            codes: CodeableConcept = Field(
                description="A default CodeableConcept.",
                default_factory=lambda: CodeableConcept(coding=[Coding(code='12345', system='http://example.org')]),
            )
        """
        self.assertBlockInCode(expected_block, model)
        self.assertBlockInCode(
            "from fhircraft.fhir.resources.datatypes.R4B.complex import CodeableConcept, Coding",
            model,
        )

    def test_model_with_field_title(self):
        model = create_model(
            "ModelWithTitle",
            code=(primitives.String, Field(title="Code Field", description="A code with title.")),
        )
        expected_block = """
        class ModelWithTitle(BaseModel):
            code: fhir.string = Field(
                title="Code Field",
                description="A code with title.",
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_list_of_complex(self):
        model = create_model(
            "ModelWithComplexList",
            codings=(List[Coding], Field(default_factory=list, description="A list of Coding objects.")),
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
        model = create_model(
            "ModelWithDocstring",
            value=(primitives.string, Field(description="A string field.")),
            __doc__="This is a model with a docstring.",
        )
        expected_block = '''
        class ModelWithDocstring(BaseModel):
            """
            This is a model with a docstring.
            """
            value: fhir.string = Field(
                description="A string field.",
            )
        '''
        self.assertBlockInCode(expected_block, model)

    def test_model_with_fixed_value_enum_field(self):
        from enum import Enum

        class Color(Enum):
            fixedValue = "red"

        model = create_model("ModelWithEnum", color=(Color, Field(description="A color enum.")))
        expected_block = """
        class ModelWithEnum(BaseModel):
            color: Literal['red'] = Field(
                description="A color enum.",
            )
        """
        self.assertBlockInCode(expected_block, model)

    def test_model_with_prohibited_field_renders_none_annotation(self):
        model = create_model(
            "ModelWithProhibitedField",
            active=(primitives.boolean, Field(default=None, description="Active flag.")),
            prohibited=(type(None), Field(default=None, description="Prohibited field.")),
        )
        expected_block = """
            prohibited: None = Field(
                description="Prohibited field.",
                default=None,
            )
        """
        self.assertBlockInCode(expected_block, model)
        code = self.gen.generate(model)
        self.assertNotIn("<class 'NoneType'>", code)

    # ------------------------------------------------------------------
    # Slice models
    # ------------------------------------------------------------------

    def test_model_with_sliced_field(self):
        model = create_slice_model("Slice", valueString=(str, Field(description="A string value")))
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
        from fhircraft.fhir.resources.datatypes.R4B.complex.extension import Extension
        from fhircraft.fhir.resources.datatypes.R4B.primitive import string

        model = _create_model(
            "ExtensionSlice",
            url=(str, Field(description="Extension URL")),
            valueString=(string, Field(description="A string value")),
            __base__=(Extension, FHIRSliceModel),
        )
        model.min_cardinality = 1
        model.max_cardinality = 1
        expected_block = """
        class ExtensionSlice(Extension, FHIRSliceModel):
            min_cardinality: ClassVar[int] = 1
            max_cardinality: ClassVar[int | None] = 1

            url: str = Field(
                description="Extension URL",
            )
            valueString: fhir.string = Field(
                description="A string value",
            )
        """
        self.assertBlockInCode(expected_block, model)

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------

    def test_model_with_field_validator(self):
        model = create_model(
            "ModelWithPatternValidator",
            code=(CodeableConcept, Field(description="A code field with pattern constraint.")),
            __validators__={
                "FHIR_code_pattern_constraint": field_validator(*("code",), mode="after", check_fields=None)(
                    partial(
                        fhir_validators.validate_FHIR_element_pattern,
                        pattern=CodeableConcept(
                            coding=[Coding(system="http://example.org", display="code", code="12345")]
                        ),
                    )
                )
            },
        )
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
        self.assertBlockInCode(
            "from fhircraft.fhir.resources.datatypes.R4B.complex import CodeableConcept, Coding",
            model,
        )

    def test_model_with_model_validator(self):
        model = create_model(
            "ModelWithModelValidator",
            code=(CodeableConcept, Field(description="A code field with model constraint.")),
            __validators__={
                "FHIR_ele_1_constraint_validator": model_validator(mode="after")(
                    partial(
                        fhir_validators.validate_model_constraint,
                        expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
                        human="All FHIR elements must have a @value or children unless an empty Parameters resource",
                        key="ele-1",
                        severity="error",
                    )
                )
            },
        )
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
        model = create_model(
            "ModelWithModelValidator",
            bases=(DomainResource,),
            code=(CodeableConcept, Field(description="A code field with model constraint.")),
            __validators__={
                "FHIR_custom_1_constraint_validator": model_validator(mode="after")(
                    partial(
                        fhir_validators.validate_model_constraint,
                        expression="exists()",
                        human="All FHIR elements must exist.",
                        key="custom-1",
                        severity="error",
                    )
                )
            },
        )
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

    def test_model_with_multiple_field_validators(self):
        model = create_model(
            "ModelWithValidators",
            codeA=(CodeableConcept, Field(description="A first code.")),
            codeB=(CodeableConcept, Field(description="A second code.")),
            __validators__={
                "FHIR_codeA_pattern_constraint": field_validator(*("codeA",), mode="after", check_fields=None)(
                    partial(
                        fhir_validators.validate_FHIR_element_pattern,
                        pattern=CodeableConcept(
                            coding=[Coding(system="http://example.org", display="code-1", code="12345")]
                        ),
                    )
                ),
                "FHIR_codeB_pattern_constraint": field_validator(*("codeB",), mode="after", check_fields=None)(
                    partial(
                        fhir_validators.validate_FHIR_element_pattern,
                        pattern=CodeableConcept(
                            coding=[Coding(system="http://example.org", display="code-2", code="67890")]
                        ),
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
        self.assertBlockInCode(
            "from fhircraft.fhir.resources.datatypes.R4B.complex import CodeableConcept, Coding",
            model,
        )

    def test_include_validators_false_omits_validators(self):
        model = create_model(
            "ValidatorSkipModel",
            code=(CodeableConcept, Field(description="A code.")),
            __validators__={
                "FHIR_v": model_validator(mode="after")(
                    partial(fhir_validators.validate_model_constraint, expression="true", human="h", key="k", severity="error")
                )
            },
        )
        code = self.gen.generate(model, include_validators=False)
        self.assertNotIn("@model_validator", code)
        self.assertNotIn("@field_validator", code)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    def test_model_with_property_method(self):
        model = create_model(
            "ModelWithProperty",
            valueString=(primitives.string, Field(description="A value.")),
            valueInteger=(primitives.integer, Field(description="A value.")),
        )
        setattr(model, "value", property(partial(fhir_validators.get_type_choice_value_by_base, base="value")))
        expected_block = """
        class ModelWithProperty(BaseModel):
            valueString: fhir.string = Field(
                description="A value.",
            )
            valueInteger: fhir.integer = Field(
                description="A value.",
            )

            @property
            def value(self):
                return get_type_choice_value_by_base(self,
                    base="value",
                )
        """
        self.assertBlockInCode(expected_block, model)

    def test_property_inheritance_skips_identical_property(self):
        base_model = _create_model(
            "BaseModelWithProperty",
            valueString=(primitives.String, Field(description="A value.")),
            __base__=(BaseModel,),
        )
        setattr(base_model, "value", property(partial(fhir_validators.get_type_choice_value_by_base, base="value")))
        derived_model = _create_model(
            "DerivedModelWithInheritedProperty",
            valueInteger=(primitives.Integer, Field(description="Another value.")),
            __base__=(base_model,),
        )
        setattr(derived_model, "value", property(partial(fhir_validators.get_type_choice_value_by_base, base="value")))
        code = self.gen.generate(derived_model)
        lines = code.split("\n")
        in_derived = False
        derived_property_count = 0
        for line in lines:
            if "class DerivedModelWithInheritedProperty" in line:
                in_derived = True
            elif in_derived and line.strip().startswith("class "):
                break
            elif in_derived and "@property" in line:
                derived_property_count += 1
        self.assertEqual(derived_property_count, 0)

    def test_property_inheritance_includes_overridden_property(self):
        base_model = _create_model(
            "BaseModelWithOriginalProperty",
            valueString=(primitives.String, Field(description="A value.")),
            __base__=(BaseModel,),
        )
        setattr(base_model, "value", property(partial(fhir_validators.get_type_choice_value_by_base, base="value")))
        derived_model = _create_model(
            "DerivedModelWithOverriddenProperty",
            valueInteger=(primitives.Integer, Field(description="Another value.")),
            __base__=(base_model,),
        )
        setattr(derived_model, "value", property(partial(fhir_validators.get_type_choice_value_by_base, base="different_base")))
        expected_block = """
        class DerivedModelWithOverriddenProperty(BaseModelWithOriginalProperty):
            valueInteger: fhir.integer = Field(
                description="Another value.",
            )

            @property
            def value(self):
                return get_type_choice_value_by_base(self,
                    base="different_base",
                )
        """
        self.assertBlockInCode(expected_block, derived_model)

    # ------------------------------------------------------------------
    # Import grouping
    # ------------------------------------------------------------------

    def test_import_grouping_by_common_parent(self):
        model = create_model(
            "ModelWithGroupedImports",
            concept=(CodeableConcept, Field(description="A concept")),
            coding=(Coding, Field(description="A coding")),
        )
        self.assertBlockInCode(
            "from fhircraft.fhir.resources.datatypes.R4B.complex import CodeableConcept, Coding",
            model,
        )
        code = self.gen.generate(model)
        self.assertNotIn("from fhircraft.fhir.resources.datatypes.R4B.complex.codeable_concept import", code)

    # ------------------------------------------------------------------
    # Inheritance chain
    # ------------------------------------------------------------------

    def test_profile_with_multiple_ancestors(self):
        child_model = create_model(
            "ChildModel",
            bases=(DomainResource,),
            childField=(str, Field(description="A field of the child model")),
            __validators__={
                "FHIR_child_1_constraint_validator": model_validator(mode="after")(
                    partial(fhir_validators.validate_model_constraint, expression="exists()", human="Child model constraint", key="child-1", severity="error")
                )
            },
        )
        grand_child_model = create_model(
            "GrandChildModel",
            bases=(child_model,),
            grandChildField=(int, Field(description="A field of the grandchild model")),
            __validators__={
                "FHIR_grandchild_1_constraint_validator": model_validator(mode="after")(
                    partial(fhir_validators.validate_model_constraint, expression="exists()", human="Grandchild model constraint", key="grandchild-1", severity="error")
                )
            },
        )
        expected_block = """
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

    # ------------------------------------------------------------------
    # String argument edge cases
    # ------------------------------------------------------------------

    def test_model_with_multiline_expression(self):
        multiline_expression = (
            "extension.where(url = 'http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-radiotherapy-modality').exists() and\n"
            "      extension.where(url = 'http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-radiotherapy-technique').exists()"
        )
        model = create_model(
            "ModelWithMultilineExpression",
            code=(CodeableConcept, Field(description="A code field.")),
            __validators__={
                "FHIR_Technique_validator": model_validator(mode="after")(
                    partial(fhir_validators.validate_model_constraint, expression=multiline_expression, human="Technique constraint", key="Technique", severity="error")
                )
            },
        )
        code = self.gen.generate(model)
        self.assertIn('expression="""extension.where', code)
        try:
            compile(code, "<generated>", "exec")
        except SyntaxError as e:
            self.fail(f"Generated code has syntax error: {e}\n\nGenerated code:\n{code}")

    def test_model_with_string_containing_quotes(self):
        model = create_model(
            "ModelWithQuotedString",
            code=(CodeableConcept, Field(description="A code field.")),
            __validators__={
                "FHIR_test_constraint": model_validator(mode="after")(
                    partial(fhir_validators.validate_model_constraint, expression='This is a "quoted" string', human="Test", key="test-1", severity="error")
                )
            },
        )
        code = self.gen.generate(model)
        self.assertIn('expression="This is a \\"quoted\\" string"', code)
        try:
            compile(code, "<generated>", "exec")
        except SyntaxError as e:
            self.fail(f"Generated code has syntax error: {e}\n\n{code}")

    # ------------------------------------------------------------------
    # Intermediate data assertions (not possible with the old design)
    # ------------------------------------------------------------------

    def test_serializer_data_contains_field_info(self):
        model = create_model("DataCheck", x=(int, Field(default=5, description="An int.")))
        self.gen.generate(model)
        assert model in self.gen._serializer.data
        field_data = self.gen._serializer.data[model]["fields"]["x"]
        assert field_data["description"] == "An int."
        assert field_data["default"] == "5"

    def test_tracker_records_pydantic_field_import(self):
        model = create_model("ImportCheck", y=(str, Field(default="hello")))
        self.gen.generate(model)
        assert "Field" in self.gen._tracker.imports["pydantic"]


# ------------------------------------------------------------------
# Module-level convenience function
# ------------------------------------------------------------------

class TestGenerateCodeFunction:
    def test_returns_string(self):
        model = _create_model("FnTest", x=(int, Field(default=1)))
        result = generate_code(model)
        assert isinstance(result, str)
        assert "class FnTest" in result

    def test_accepts_list(self):
        A = _create_model("FA", x=(int, Field(default=1)))
        B = _create_model("FB", y=(str, Field(default="a")))
        result = generate_code([A, B])
        assert "class FA" in result
        assert "class FB" in result

    def test_include_validators_false(self):
        model = _create_model("FnNoVal", x=(int, Field(default=1)))
        result = generate_code(model, include_validators=False)
        assert "class FnNoVal" in result


# ------------------------------------------------------------------
# Built-in FHIR model code generation smoke tests
# ------------------------------------------------------------------

@pytest.mark.parametrize(
    "model_name",
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
def test_code_generates_for_builtin_models(model_name):
    from fhircraft.fhir.resources.datatypes.R5 import core
    code = generate_code(getattr(core, model_name))
    assert f"class {model_name}(DomainResource):" in code
    compile(code, "<generated>", "exec")
