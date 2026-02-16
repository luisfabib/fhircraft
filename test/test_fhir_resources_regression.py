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
        min_cardinality: ClassVar[int] = 1
        max_cardinality: ClassVar[int] = 1
    
    
        system: Literal['http://example.org'] = Field(
            description=None,
            default="http://example.org",
        )
        code: Literal['12345-6'] = Field(
            description=None,
            default="12345-6",
        )
        
        
    class ProfileExampleCode(CodeableConcept):
        """
        Describes what was observed. Sometimes this is called the observation "name".
        """
    

        coding: Optional[List[Annotated[Union[ProfileExampleSlicedCoding, Coding], Field(union_mode='left_to_right')]]] = Field(
            description=None,
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
    # Clear factory cache to avoid state pollution from other tests
    factory.clear_cache()

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
    # Clear factory cache to avoid state pollution from other tests
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
        
        text: Literal['Tumor Board Review'] = Field(
            description=None,
            default="Tumor Board Review",
        )
        
    
    class ExampleProcedure(Procedure):

        _canonical_url = "http://example.org/StructureDefinition/example-procedure"

        meta: Optional[Meta] = Field(
            title="Meta",
            description="Metadata about the resource.",
            default_factory=lambda: Meta(profile=['http://example.org/StructureDefinition/example-procedure']),
        )
        code: ExampleProcedureCode = Field(
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
    ), f"Expected exactly 3 classes to be generated, got {source_code.count('class')} \n Generated code:\n{source_code}"
