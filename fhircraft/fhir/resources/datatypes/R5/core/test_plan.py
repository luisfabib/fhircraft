from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Coding,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    Reference,
    BackboneElement,
    CodeableReference,
)
from .resource import Resource
from .domain_resource import DomainResource

class TestPlanDependency(BackboneElement):
    """
    The required criteria to execute the test plan - e.g. preconditions, previous tests...
    """

    description: Optional[Markdown] = Field(
        description="Description of the dependency criterium",
        default=None,
    )
    predecessor: Optional[Reference] = Field(
        description="Link to predecessor test plans",
        default=None,
    )

class TestPlanTestCaseDependency(BackboneElement):
    """
    The required criteria to execute the test case - e.g. preconditions, previous tests.
    """

    description: Optional[Markdown] = Field(
        description="Description of the criteria",
        default=None,
    )
    predecessor: Optional[Reference] = Field(
        description="Link to predecessor test plans",
        default=None,
    )

class TestPlanTestCaseTestRunScript(BackboneElement):
    """
    The test cases in a structured language e.g. gherkin, Postman, or FHIR TestScript.
    """

    language: Optional[CodeableConcept] = Field(
        description="The language for the test cases e.g. \u0027gherkin\u0027, \u0027testscript\u0027",
        default=None,
    )
    sourceString: Optional[String] = Field(
        description="The actual content of the cases - references to TestScripts or externally defined content",
        default=None,
    )
    sourceReference: Optional[Reference] = Field(
        description="The actual content of the cases - references to TestScripts or externally defined content",
        default=None,
    )

    @property
    def source(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="source",
        )

    @model_validator(mode="after")
    def source_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[String, Reference],
            field_name_base="source",
            required=False,
        )

class TestPlanTestCaseTestRun(BackboneElement):
    """
    The actual test to be executed.
    """

    narrative: Optional[Markdown] = Field(
        description="The narrative description of the tests",
        default=None,
    )
    script: Optional[TestPlanTestCaseTestRunScript] = Field(
        description="The test cases in a structured language e.g. gherkin, Postman, or FHIR TestScript",
        default=None,
    )

class TestPlanTestCaseTestData(BackboneElement):
    """
    The test data used in the test case.
    """

    type: Optional[Coding] = Field(
        description="The type of test data description, e.g. \u0027synthea\u0027",
        default=None,
    )
    content: Optional[Reference] = Field(
        description="The actual test resources when they exist",
        default=None,
    )
    sourceString: Optional[String] = Field(
        description="Pointer to a definition of test resources - narrative or structured e.g. synthetic data generation, etc",
        default=None,
    )
    sourceReference: Optional[Reference] = Field(
        description="Pointer to a definition of test resources - narrative or structured e.g. synthetic data generation, etc",
        default=None,
    )

    @property
    def source(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="source",
        )

    @model_validator(mode="after")
    def source_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[String, Reference],
            field_name_base="source",
            required=False,
        )

class TestPlanTestCaseAssertion(BackboneElement):
    """
    The test assertions - the expectations of test results from the execution of the test case.
    """

    type: Optional[ListType[CodeableConcept]] = Field(
        description="Assertion type - for example \u0027informative\u0027 or \u0027required\u0027 ",
        default=None,
    )
    object: Optional[ListType[CodeableReference]] = Field(
        description="The focus or object of the assertion",
        default=None,
    )
    result: Optional[ListType[CodeableReference]] = Field(
        description="The actual result assertion",
        default=None,
    )

class TestPlanTestCase(BackboneElement):
    """
    The individual test cases that are part of this plan, when they they are made explicit.
    """

    sequence: Optional[Integer] = Field(
        description="Sequence of test case in the test plan",
        default=None,
    )
    scope: Optional[ListType[Reference]] = Field(
        description="The scope or artifact covered by the case",
        default=None,
    )
    dependency: Optional[ListType[TestPlanTestCaseDependency]] = Field(
        description="Required criteria to execute the test case",
        default=None,
    )
    testRun: Optional[ListType[TestPlanTestCaseTestRun]] = Field(
        description="The actual test to be executed",
        default=None,
    )
    testData: Optional[ListType[TestPlanTestCaseTestData]] = Field(
        description="The test data used in the test case",
        default=None,
    )
    assertion: Optional[ListType[TestPlanTestCaseAssertion]] = Field(
        description="Test assertions or expectations",
        default=None,
    )

class TestPlan(DomainResource):
    """
    A plan for executing testing on an artifact or specifications
    """

    _abstract = False
    _type = "TestPlan"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/TestPlan"

    url: Optional[Uri] = Field(
        description="Canonical identifier for this test plan, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier identifier for the test plan",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the test plan",
        default=None,
    )
    versionAlgorithmString: Optional[String] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this test plan (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this test plan (human friendly)",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[Boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher/steward (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Natural language description of the test plan",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction where the test plan applies (if applicable)",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this test plan is defined",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyrightLabel: Optional[String] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="The category of the Test Plan - can be acceptance, unit, performance",
        default=None,
    )
    scope: Optional[ListType[Reference]] = Field(
        description="What is being tested with this Test Plan - a conformance resource, or narrative criteria, or an external reference",
        default=None,
    )
    testTools: Optional[Markdown] = Field(
        description="A description of test tools to be used in the test plan - narrative for now",
        default=None,
    )
    dependency: Optional[ListType[TestPlanDependency]] = Field(
        description="The required criteria to execute the test plan - e.g. preconditions, previous tests",
        default=None,
    )
    exitCriteria: Optional[Markdown] = Field(
        description="The threshold or criteria for the test plan to be considered successfully executed - narrative",
        default=None,
    )
    testCase: Optional[ListType[TestPlanTestCase]] = Field(
        description="The test cases that constitute this plan",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @model_validator(mode="after")
    def versionAlgorithm_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[String, Coding],
            field_name_base="versionAlgorithm",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('^[A-Z]([A-Za-z0-9_]){1,254}$')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_cnl_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("url",),
            expression="exists() implies matches('^[^|# ]+$')",
            human="URL should not contain | or # - these characters make processing canonical references problematic",
            key="cnl-1",
            severity="warning",
        )
