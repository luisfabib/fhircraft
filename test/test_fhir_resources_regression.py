import pytest
from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.fhir.resources.generator import CodeGenerator


def _normalize(s):
    import re

    return re.sub(r"\s+", " ", s.strip())


def assertBlockInCode(code, expected_block):
    # Generate source code
    # Assert code block (normalized)
    norm_expected = _normalize(expected_block)
    norm_code = _normalize(code)
    assert (
        norm_expected in norm_code
    ), f"Expected block not found in generated code.\n\nExpected:\n{expected_block}\n\nGot:\n{code}"


@pytest.fixture
def generator():

    generator = CodeGenerator()
    yield generator


@pytest.fixture
def factory():

    factory = ResourceFactory()
    yield factory
    factory.clear_cache()


def test_regression_issue_255(factory, generator):
    # Clear factory cache to avoid state pollution from other tests

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "issue-255",
        "url": "http://example.org/fhir/StructureDefinition/issue-255",
        "version": "5.0.0",
        "name": "ProfileExample",
        "title": "Example Profile",
        "status": "draft",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Observation",
        "derivation": "constraint",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
        "differential": {
            "element": [
                {
                    "id": "Observation",
                    "path": "Observation",
                    "min": 0,
                    "max": "*",
                },
                {
                    "id": "Observation.code",
                    "path": "Observation.code",
                },
                {
                    "id": "Observation.code.coding",
                    "path": "Observation.code.coding",
                    "slicing": {
                        "discriminator": [
                            {"type": "value", "path": "code"},
                            {"type": "value", "path": "system"},
                        ],
                        "ordered": False,
                        "rules": "open",
                    },
                },
                {
                    "id": "Observation.code.coding:slicedCoding",
                    "path": "Observation.code.coding",
                    "sliceName": "slicedCoding",
                    "min": 1,
                    "max": "1",
                },
                {
                    "id": "Observation.code.coding:slicedCoding.system",
                    "path": "Observation.code.coding.system",
                    "min": 1,
                    "max": "1",
                    "type": [{"code": "uri"}],
                    "fixedUri": "http://example.org",
                },
                {
                    "id": "Observation.code.coding:slicedCoding.code",
                    "path": "Observation.code.coding.code",
                    "min": 1,
                    "max": "1",
                    "type": [{"code": "code"}],
                    "fixedCode": "12345-6",
                },
            ]
        },
    }

    model = factory.construct_resource_model(
        structure_definition=structure_definition, mode="differential"
    )

    source_code = generator.generate_resource_model_code(model)

    expected_code = '''
    class ProfileExampleSlicedCoding(Coding, FHIRSliceModel):
        """
        Code defined by a terminology system
        """
        min_cardinality: ClassVar[int] = 1
        max_cardinality: ClassVar[int] = 1
    
        system: Optional[Uri] = Field(
            description="Identity of the terminology system",
            default="http://example.org",
        )
        code: Optional[Code] = Field(
            description="Symbol in syntax defined by the system",
            default="12345-6",
        )

        @field_validator(*('system',), mode="after", check_fields=None)
        @classmethod
        def FHIR_system_fixed_value_constraint(cls, value):    
            return validate_FHIR_element_fixed_value(cls, value, 
                constant="http://example.org",
            )
            
        @field_validator(*('code',), mode="after", check_fields=None)
        @classmethod
        def FHIR_code_fixed_value_constraint(cls, value):    
            return validate_FHIR_element_fixed_value(cls, value, 
                constant="12345-6",
            )        
        
    class ProfileExampleCode(CodeableConcept):
        """
        Describes what was observed. Sometimes this is called the observation "name".
        """
    

        coding: Optional[List[Annotated[Union[ProfileExampleSlicedCoding, Coding], Field(union_mode='left_to_right')]]] = Field(
            description="Code defined by a terminology system",
            default=None,
        )
        
        @field_validator(*('coding',), mode="after", check_fields=None)
        @classmethod
        def coding_slicing_cardinality_validator(cls, value):    
            return validate_slicing_cardinalities(cls, value, 
                field_name="coding",
            )
        
    class ProfileExample(Observation):

        _canonical_url = "http://example.org/fhir/StructureDefinition/issue-255"

        meta: Optional[Meta] = Field(
            title="Meta",
            description="Metadata about the resource.",
            default_factory=lambda: Meta(profile=['http://example.org/fhir/StructureDefinition/issue-255']),
        )
        code: Optional[ProfileExampleCode] = Field(
            description="Type of observation (code / type)",
            default=None,
        )
    '''
    assertBlockInCode(source_code, expected_code.strip())
    assert (
        source_code.count("class ") == 3
    ), f"Expected exactly 3 classes to be generated, got {source_code.count('class')} \n Generated code:\n{source_code}"


def test_regression_issue_258(factory, generator):
    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "issue-258",
        "url": "http://example.org/fhir/StructureDefinition/issue-258",
        "version": "5.0.0",
        "name": "ProfileExample",
        "title": "Example Profile",
        "status": "draft",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Observation",
        "derivation": "constraint",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
        "differential": {
            "element": [
                {"id": "Observation", "path": "Observation", "min": 0, "max": "*"},
                {
                    "id": "Observation.category",
                    "path": "Observation.category",
                    "slicing": {"discriminator": [{"type": "value", "path": "coding"}]},
                },
                {
                    "id": "Observation.category:slice",
                    "path": "Observation.category",
                    "max": "2",
                    "sliceName": "slice",
                    "patternCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://example.org",
                                "code": "12345-6",
                                "display": "Fixed Category",
                            }
                        ]
                    },
                },
            ]
        },
    }

    model = factory.construct_resource_model(
        structure_definition=structure_definition, mode="differential"
    )

    source_code = generator.generate_resource_model_code(model)

    expected_code = '''
    class ProfileExampleSlice(CodeableConcept, FHIRSliceModel):
        """
        Classification of  type of observation
        """
        min_cardinality: ClassVar[int] = 0
        max_cardinality: ClassVar[int] = 2

        coding: Optional[List[Coding]] = Field(
            description="Code defined by a terminology system",
            default=[Coding(code="12345-6", display="Fixed Category", system="http://example.org")],
        )
        
        @model_validator(mode="after")
        def FHIR_slice_pattern_constraint(self):    
            return validate_FHIR_model_pattern(
                self,
                pattern=CodeableConcept(coding=[Coding(code="12345-6", display="Fixed Category", system="http://example.org")]),
            )
    
    class ProfileExample(Observation):

        _canonical_url = "http://example.org/fhir/StructureDefinition/issue-258"

        meta: Optional[Meta] = Field(
            title="Meta",
            description="Metadata about the resource.",
            default_factory=lambda: Meta(profile=['http://example.org/fhir/StructureDefinition/issue-258']),
        )
        category: Optional[List[Annotated[Union[ProfileExampleSlice, CodeableConcept], Field(union_mode='left_to_right')]]] = Field(
            description="Classification of  type of observation",
            default=None,
        )
        
        @field_validator(*('category',), mode="after", check_fields=None)
        @classmethod
        def category_slicing_cardinality_validator(cls, value):    
            return validate_slicing_cardinalities(cls, value, 
                field_name="category",
            )
    '''
    assertBlockInCode(source_code, expected_code)

    assert (
        source_code.count("class ") == 2
    ), f"Expected exactly 2 classes to be generated, got {source_code.count('class')} \n Generated code:\n{source_code}"


def test_regression_issue_111(factory, generator):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "example-procedure",
        "url": "http://example.org/StructureDefinition/example-procedure",
        "version": "0.1.0",
        "name": "ExampleProcedure",
        "fhirVersion": "4.0.1",
        "kind": "resource",
        "abstract": False,
        "type": "Procedure",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Procedure",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Procedure",
                    "path": "Procedure",
                },
                {
                    "id": "Procedure.code",
                    "path": "Procedure.code",
                    "patternCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
                                "code": "C93304",
                                "display": "Tumor Board Review",
                            }
                        ]
                    },
                },
                {
                    "id": "Procedure.code.text",
                    "path": "Procedure.code.text",
                    "fixedString": "Tumor Board Review",
                    "min": 0,
                },
            ]
        },
    }

    model = factory.construct_resource_model(
        structure_definition=structure_definition, mode="differential"
    )

    source_code = generator.generate_resource_model_code(model)

    expected_code = '''
    class ExampleProcedureCode(CodeableConcept):
        """
        The specific procedure that is performed. Use text if the exact nature of the procedure cannot be coded (e.g. "Laparoscopic Appendectomy").
        """
            
        text: Optional[String] = Field(
            description="Plain text representation of the concept",
            default="Tumor Board Review",
        )
        
        @field_validator(*('text',), mode="after", check_fields=None)
        @classmethod
        def FHIR_text_fixed_value_constraint(cls, value):    
            return validate_FHIR_element_fixed_value(cls, value, 
                constant="Tumor Board Review",
            )
        
    
    class ExampleProcedure(Procedure):

        _canonical_url = "http://example.org/StructureDefinition/example-procedure"

        meta: Optional[Meta] = Field(
            title="Meta",
            description="Metadata about the resource.",
            default_factory=lambda: Meta(profile=['http://example.org/StructureDefinition/example-procedure']),
        )
        code: Optional[ExampleProcedureCode] = Field(
            description="Identification of the procedure",
            default_factory=lambda: ExampleProcedureCode(coding=[Coding(code="C93304", display="Tumor Board Review", system="http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl")]),
        )
        
        @field_validator(*('code',), mode="after", check_fields=None)
        @classmethod
        def FHIR_code_pattern_constraint(cls, value):    
            return validate_FHIR_element_pattern(cls, value, 
                pattern=ExampleProcedureCode(coding=[Coding(code="C93304", display="Tumor Board Review", system="http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl")]),
            )
    '''
    assertBlockInCode(source_code, expected_code.strip())
    assert (
        source_code.count("class ") == 2
    ), f"Expected exactly 2 classes to be generated, got {source_code.count('class')} \n Generated code:\n{source_code}"


def test_regression_issue_263(factory, generator):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "vitalspanel",
        "url": "http://hl7.org/fhir/StructureDefinition/vitalspanel",
        "version": "5.0.0",
        "name": "Vitalspanel",
        "title": "Observation Vital Signs Panel Profile",
        "status": "draft",
        "experimental": False,
        "date": "2018-08-11",
        "description": "FHIR Vital Signs Panel Profile",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Observation",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Observation.code",
                    "path": "Observation.code",
                    "slicing": {
                        "discriminator": [
                            {"type": "value", "path": "code"},
                            {"type": "value", "path": "system"},
                        ],
                        "ordered": False,
                        "rules": "open",
                    },
                },
                {
                    "id": "Observation.code.coding",
                    "path": "Observation.code.coding",
                },
                {
                    "id": "Observation.code.coding:VitalsPanelCode",
                    "path": "Observation.code.coding",
                    "sliceName": "VitalsPanelCode",
                    "max": "1",
                },
                {
                    "id": "Observation.code.coding:VitalsPanelCode.system",
                    "path": "Observation.code.coding.system",
                    "type": [{"code": "uri"}],
                    "fixedUri": "http://loinc.org",
                },
                {
                    "id": "Observation.code.coding:VitalsPanelCode.code",
                    "path": "Observation.code.coding.code",
                    "type": [{"code": "code"}],
                    "fixedCode": "85353-1",
                },
            ]
        },
    }

    model = factory.construct_resource_model(
        structure_definition=structure_definition, mode="differential"
    )

    source_code = generator.generate_resource_model_code(model)

    expected_code = '''    
    class VitalspanelVitalsPanelCode(Coding, FHIRSliceModel):
        """
        Code defined by a terminology system
        """
        min_cardinality: ClassVar[int] = 0
        max_cardinality: ClassVar[int] = 1


        system: Optional[Uri] = Field(
            description="Identity of the terminology system",
            default="http://loinc.org",
        )
        code: Optional[Code] = Field(
            description="Symbol in syntax defined by the system",
            default="85353-1",
        )

        @field_validator(*('system',), mode="after", check_fields=None)
        @classmethod
        def FHIR_system_fixed_value_constraint(cls, value):    
            return validate_FHIR_element_fixed_value(cls, value, 
                constant="http://loinc.org",
            )

        @field_validator(*('code',), mode="after", check_fields=None)
        @classmethod  
        def FHIR_code_fixed_value_constraint(cls, value):    
            return validate_FHIR_element_fixed_value(cls, value, 
                constant="85353-1",
            )
        
    
    class VitalspanelCode(CodeableConcept):
        """
        Describes what was observed. Sometimes this is called the observation "name".
        """

        coding: Optional[List[Annotated[Union[VitalspanelVitalsPanelCode, Coding], Field(union_mode='left_to_right')]]] = Field(
            description="Code defined by a terminology system",
            default=None,
        )
        
        @field_validator(*('coding',), mode="after", check_fields=None)
        @classmethod
        def coding_slicing_cardinality_validator(cls, value):    
            return validate_slicing_cardinalities(cls, value, 
                field_name="coding",
            )
    '''
    assertBlockInCode(source_code, expected_code.strip())
    assert (
        source_code.count("class ") == 3
    ), f"Expected exactly 3 classes to be generated, got {source_code.count('class')} \n Generated code:\n{source_code}"


def test_regression_issue_262():
    from pydantic import Field, model_validator
    from typing import Optional, List
    from fhircraft.fhir.resources.datatypes.R5.core import Patient
    from typing import List, Optional
    from fhircraft.fhir.resources.datatypes.R5.complex import HumanName, Meta
    from fhircraft.fhir.resources.datatypes.primitives import String
    from fhircraft.fhir.resources.validators import validate_element_constraint

    class ExamplePatientName(HumanName):
        family: Optional[String] = Field(
            description="(USCDI) Family name (often called \u0027Surname\u0027)",
            default=None,
        )

    class ExamplePatient(Patient):

        _canonical_url = "http://example.org/fhir/StructureDefinition/example"

        meta: Optional[Meta] = Field(
            title="Meta",
            description="Metadata about the resource.",
            default_factory=lambda: Meta(
                profile=["http://example.org/fhir/StructureDefinition/example"]
            ),
        )
        name: Optional[List[ExamplePatientName]] = Field(
            description="(USCDI) A name associated with the patient",
            default=None,
        )

        @model_validator(mode="after")
        def FHIR_us_core_6_constraint_validator(self):
            return validate_element_constraint(
                self,
                elements=["name"],
                expression="(family.exists() or given.exists()) xor extension.where(url='http://hl7.org/fhir/StructureDefinition/data-absent-reason').exists()",
                human="At least name.given and/or name.family are present or, if neither is available, the Data Absent Reason Extension is present.",
                key="us-core-6",
                severity="error",
            )

    instance = ExamplePatient(
        name=[HumanName(given=["John"], family="Doe")]  # type: ignore
    )

    assert isinstance(instance, ExamplePatient)
    assert instance.name
    assert instance.name[0].given == ["John"]


def test_regression_issue_265(factory, generator):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "example-profile",
        "text": {
            "status": "generated",
            "div": '<div xmlns="http://www.w3.org/1999/xhtml">to do</div>',
        },
        "url": "http://hl7.org/fhir/StructureDefinition/example-profile",
        "version": "5.0.0",
        "name": "ExampleProfile",
        "title": "Example Profile",
        "status": "draft",
        "experimental": False,
        "date": "2018-08-11",
        "description": "Example Profile Description",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Observation",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Observation",
                    "path": "Observation",
                    "short": "assessment observation",
                },
                {
                    "id": "Observation.category",
                    "path": "Observation.category",
                    "min": 1,
                    "mustSupport": True,
                },
                {
                    "id": "Observation.category:slice",
                    "path": "Observation.category",
                    "sliceName": "slice",
                    "short": "Classification of type of observation",
                    "min": 0,
                    "mustSupport": False,
                    "binding": {
                        "strength": "required",
                        "valueSet": "http://hl7.org/fhir/ValueSet/observation-category",
                    },
                },
            ]
        },
    }

    model = factory.construct_resource_model(
        structure_definition=structure_definition, mode="differential"
    )

    source_code = generator.generate_resource_model_code(model)

    expected_code = '''    
    class ExampleProfile(Observation):
        """
        Example Profile Description
        """

        _canonical_url = "http://hl7.org/fhir/StructureDefinition/example-profile"

        meta: Optional[Meta] = Field(
            title="Meta",
            description="Metadata about the resource.",
            default_factory=lambda: Meta(profile=['http://hl7.org/fhir/StructureDefinition/example-profile']),
        )
        category: Optional[List[CodeableConcept]] = Field(
            description="Classification of type of observation",
            default=None,
        )
        
        @field_validator(*('category',), mode="after", check_fields=None)
        @classmethod
        def category_slicing_cardinality_validator(cls, value):    
            return validate_slicing_cardinalities(cls, value, 
                field_name="category",
            )
    '''
    assertBlockInCode(source_code, expected_code.strip())
    assert (
        source_code.count("class ") == 1
    ), f"Expected exactly 1 class to be generated, got {source_code.count('class')} \n Generated code:\n{source_code}"


def test_regression_issue_266(factory, generator):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "example-profile",
        "url": "http://hl7.org/fhir/StructureDefinition/example-profile",
        "version": "5.0.0",
        "name": "ExampleProfile",
        "title": "Example Profile",
        "status": "draft",
        "experimental": False,
        "date": "2018-08-11",
        "description": "Example Profile Description",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "AdverseEvent",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/AdverseEvent",
        "derivation": "constraint",
        "differential": {
            "element": [
                {"id": "AdverseEvent", "path": "AdverseEvent"},
                {
                    "id": "AdverseEvent.extension",
                    "path": "AdverseEvent.extension",
                    "slicing": {
                        "discriminator": [{"type": "value", "path": "url"}],
                        "ordered": False,
                        "rules": "open",
                    },
                    "min": 1,
                },
                {
                    "id": "AdverseEvent.extension:grade",
                    "path": "AdverseEvent.extension",
                    "sliceName": "grade",
                    "short": "grade",
                    "min": 1,
                    "max": "1",
                    "type": [
                        {
                            "code": "Extension",
                            "profile": [
                                "http://example.org/fhir/StructureDefinition/grade-extension"
                            ],
                        }
                    ],
                    "mustSupport": True,
                },
            ]
        },
    }

    extension_structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "grade-extension",
        "url": "http://example.org/fhir/StructureDefinition/grade-extension",
        "version": "0.1.0",
        "name": "GradeExtension",
        "title": "Grade Extension",
        "status": "active",
        "date": "2025-12-04T10:59:28+00:00",
        "description": "The grade of the adverse event",
        "fhirVersion": "5.0.0",
        "kind": "complex-type",
        "abstract": False,
        "context": [{"type": "element", "expression": "AdverseEvent.extension"}],
        "type": "Extension",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Extension",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Extension",
                    "path": "Extension",
                },
                {
                    "id": "Extension.url",
                    "path": "Extension.url",
                    "fixedUri": "http://example.org/fhir/StructureDefinition/grade-extension",
                },
                {
                    "id": "Extension.value[x]",
                    "path": "Extension.value[x]",
                    "short": "Grade",
                    "definition": "The grade of the adverse event",
                    "type": [{"code": "integer"}],
                    "min": 1,
                    "max": "1",
                },
            ]
        },
    }

    factory.configure_repository(
        definitions=[structure_definition, extension_structure_definition]
    )

    model = factory.construct_resource_model(
        structure_definition=structure_definition, mode="differential"
    )

    source_code = generator.generate_resource_model_code(model)

    expected_code = '''    
    class GradeExtension(Extension, FHIRSliceModel):
        """
        The grade of the adverse event
        """
        min_cardinality: ClassVar[int] = 1
        max_cardinality: ClassVar[int] = 1

        _canonical_url = "http://example.org/fhir/StructureDefinition/grade-extension"

        url: Optional[String] = Field(
            description="identifies the meaning of the extension",
            default="http://example.org/fhir/StructureDefinition/grade-extension",
        )
        valueInteger: Optional[Integer] = Field(
            description="Grade",
            default=None,
        )
    '''
    assertBlockInCode(source_code, expected_code.strip())
    assert (
        source_code.count("class ") == 2
    ), f"Expected exactly 2 classes to be generated, got {source_code.count('class')} \n Generated code:\n{source_code}"


def test_regression_issue_279(factory, generator):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "my-condition",
        "url": "http://example.org/fhir/StructureDefinition/condition",
        "name": "MyCondition",
        "title": "Condition Profile",
        "status": "active",
        "description": "A description",
        "fhirVersion": "4.0.1",
        "kind": "resource",
        "abstract": False,
        "type": "Condition",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Condition",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Condition.clinicalStatus.extension:slice1",
                    "path": "Condition.clinicalStatus.extension",
                    "sliceName": "slice1",
                    "min": 0,
                    "max": "1",
                    "type": [
                        {
                            "code": "Extension",
                            "profile": [
                                "http://example.org/fhir/StructureDefinition/my-extension-1"
                            ],
                        }
                    ],
                },
                {
                    "id": "Condition.clinicalStatus.extension:slice2",
                    "path": "Condition.clinicalStatus.extension",
                    "sliceName": "slice2",
                    "min": 0,
                    "max": "1",
                    "type": [
                        {
                            "code": "Extension",
                            "profile": [
                                "http://example.org/fhir/StructureDefinition/my-extension-2"
                            ],
                        }
                    ],
                },
            ]
        },
    }

    extension_1_structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "my-extension-1",
        "url": "http://example.org/fhir/StructureDefinition/my-extension-1",
        "name": "MyExtension1",
        "title": "My Extension 1",
        "status": "active",
        "description": "A description of my extension 1.",
        "fhirVersion": "4.0.1",
        "kind": "complex-type",
        "abstract": False,
        "context": [
            {"expression": "Condition.clinicalStatus.extension", "type": "element"}
        ],
        "type": "Extension",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Extension",
        "derivation": "constraint",
        "differential": {
            "element": [
                {"id": "Extension", "path": "Extension"},
                {
                    "id": "Extension.url",
                    "path": "Extension.url",
                    "fixedUri": "http://example.org/fhir/StructureDefinition/my-extension-1",
                },
                {
                    "id": "Extension.value[x]",
                    "path": "Extension.value[x]",
                    "type": [{"code": "CodeableConcept"}],
                    "binding": {
                        "strength": "required",
                        "valueSet": "http://example.org/fhir/ValueSet/my-value-set-1",
                    },
                },
            ]
        },
    }

    extension_2_structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "my-extension-2",
        "url": "http://example.org/fhir/StructureDefinition/my-extension-2",
        "name": "MyExtension2",
        "title": "My Extension 2",
        "status": "active",
        "description": "A description of my extension 2.",
        "fhirVersion": "4.0.1",
        "kind": "complex-type",
        "abstract": False,
        "context": [
            {"expression": "Condition.clinicalStatus.extension", "type": "element"}
        ],
        "type": "Extension",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Extension",
        "derivation": "constraint",
        "differential": {
            "element": [
                {"id": "Extension", "path": "Extension"},
                {
                    "id": "Extension.url",
                    "path": "Extension.url",
                    "fixedUri": "http://example.org/fhir/StructureDefinition/my-extension-2",
                },
                {
                    "id": "Extension.value[x]",
                    "path": "Extension.value[x]",
                    "type": [{"code": "Reference"}],
                },
            ]
        },
    }

    factory.configure_repository(
        definitions=[
            structure_definition,
            extension_1_structure_definition,
            extension_2_structure_definition,
        ]
    )

    model = factory.construct_resource_model(
        structure_definition=structure_definition, mode="differential"
    )

    source_code = generator.generate_resource_model_code(model)

    expected_code = """    
    class MyExtension1(Extension, FHIRSliceModel):
    """
    assertBlockInCode(source_code, expected_code.strip())

    expected_code = """    
    class MyExtension2(Extension, FHIRSliceModel):
    """
    assertBlockInCode(source_code, expected_code.strip())

    expected_code = """    
    class MyConditionClinicalStatus(CodeableConcept):
    """
    assertBlockInCode(source_code, expected_code.strip())

    assert (
        source_code.count("class ") == 4
    ), f"Expected exactly 4 classes to be generated, got {source_code.count('class')} \n Generated code:\n{source_code}"


def test_regression_issue_278(factory, generator):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "my-adverse-event",
        "url": "http://example.org/fhir/StructureDefinition/adverse-event",
        "name": "MyAdverseEvent",
        "title": "Adverse Event Profile",
        "status": "active",
        "description": "A description",
        "fhirVersion": "4.0.1",
        "kind": "resource",
        "abstract": False,
        "type": "AdverseEvent",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/AdverseEvent",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "AdverseEvent",
                    "path": "AdverseEvent",
                    "short": "Adverse Event Profile",
                    "definition": "A description",
                    "min": 0,
                    "max": "*",
                },
                {
                    "id": "AdverseEvent.extension",
                    "path": "AdverseEvent.extension",
                    "slicing": {
                        "discriminator": [{"type": "value", "path": "url"}],
                        "ordered": False,
                        "rules": "open",
                    },
                    "min": 1,
                },
                {
                    "id": "AdverseEvent.extension:my-extension",
                    "path": "AdverseEvent.extension",
                    "sliceName": "myExtension",
                    "short": "My Extension",
                    "type": [
                        {
                            "code": "Extension",
                            "profile": [
                                "http://example.org/fhir/StructureDefinition/my-extension"
                            ],
                        }
                    ],
                },
            ]
        },
    }

    extension_structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "my-extension",
        "url": "http://example.org/fhir/StructureDefinition/my-extension",
        "name": "MyExtension",
        "title": "My Extension",
        "status": "active",
        "description": "A description of my extension.",
        "fhirVersion": "4.0.1",
        "kind": "complex-type",
        "abstract": False,
        "context": [{"expression": "AdverseEvent.extension", "type": "element"}],
        "type": "Extension",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Extension",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Extension",
                    "path": "Extension",
                },
                {
                    "id": "Extension.extension",
                    "path": "Extension.extension",
                    "max": "0",
                },
                {
                    "id": "Extension.url",
                    "path": "Extension.url",
                    "fixedUri": "http://example.org/fhir/StructureDefinition/my-extension",
                },
                {
                    "id": "Extension.value[x]",
                    "path": "Extension.value[x]",
                    "short": "Custom value",
                    "definition": "The custom value of the extension",
                    "type": [{"code": "integer"}],
                },
            ]
        },
    }

    factory.configure_repository(
        definitions=[
            structure_definition,
            extension_structure_definition,
        ]
    )

    model = factory.construct_resource_model(
        structure_definition=structure_definition, mode="differential"
    )

    source_code = generator.generate_resource_model_code(model)

    expected_code = """    
    valueInteger: Optional[Integer] = Field(
        description="Custom value",
        default=None,
    )
    """
    assertBlockInCode(source_code, expected_code.strip())

    assert (
        source_code.count("class ") == 2
    ), f"Expected exactly 2 classes to be generated, got {source_code.count('class')} \n Generated code:\n{source_code}"
