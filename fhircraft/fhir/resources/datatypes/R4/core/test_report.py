import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    BackboneElement,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource

class TestReportParticipant(BackboneElement):
    """
    A participant in the test execution, either the execution engine, a client, or a server.
    """

    type: Optional[Code] = Field(
        description="test-engine | client | server",
        default=None,
    )
    uri: Optional[Uri] = Field(
        description="The uri of the participant. An absolute URL is preferred",
        default=None,
    )
    display: Optional[String] = Field(
        description="The display name of the participant",
        default=None,
    )

class TestReportSetupActionOperation(BackboneElement):
    """
    The operation performed.
    """

    result: Optional[Code] = Field(
        description="pass | skip | fail | warning | error",
        default=None,
    )
    message: Optional[Markdown] = Field(
        description="A message associated with the result",
        default=None,
    )
    detail: Optional[Uri] = Field(
        description="A link to further details on the result",
        default=None,
    )

class TestReportSetupActionAssert(BackboneElement):
    """
    The results of the assertion performed on the previous operations.
    """

    result: Optional[Code] = Field(
        description="pass | skip | fail | warning | error",
        default=None,
    )
    message: Optional[Markdown] = Field(
        description="A message associated with the result",
        default=None,
    )
    detail: Optional[String] = Field(
        description="A link to further details on the result",
        default=None,
    )

class TestReportSetupAction(BackboneElement):
    """
    Action would contain either an operation or an assertion.
    """

    operation: Optional[TestReportSetupActionOperation] = Field(
        description="The operation to perform",
        default=None,
    )
    assert_: Optional[TestReportSetupActionAssert] = Field(
        description="The assertion to perform",
        default=None,
        alias="assert",
    )

class TestReportSetup(BackboneElement):
    """
    The results of the series of required setup operations before the tests were executed.
    """

    action: Optional[ListType[TestReportSetupAction]] = Field(
        description="A setup operation or assert that was executed",
        default=None,
    )

class TestReportTestActionOperation(BackboneElement):
    """
    An operation would involve a REST request to a server.
    """

    result: Optional[Code] = Field(
        description="pass | skip | fail | warning | error",
        default=None,
    )
    message: Optional[Markdown] = Field(
        description="A message associated with the result",
        default=None,
    )
    detail: Optional[Uri] = Field(
        description="A link to further details on the result",
        default=None,
    )

class TestReportTestActionAssert(BackboneElement):
    """
    The results of the assertion performed on the previous operations.
    """

    result: Optional[Code] = Field(
        description="pass | skip | fail | warning | error",
        default=None,
    )
    message: Optional[Markdown] = Field(
        description="A message associated with the result",
        default=None,
    )
    detail: Optional[String] = Field(
        description="A link to further details on the result",
        default=None,
    )

class TestReportTestAction(BackboneElement):
    """
    Action would contain either an operation or an assertion.
    """

    operation: Optional[TestReportTestActionOperation] = Field(
        description="The operation performed",
        default=None,
    )
    assert_: Optional[TestReportTestActionAssert] = Field(
        description="The assertion performed",
        default=None,
        alias="assert",
    )

class TestReportTest(BackboneElement):
    """
    A test executed from the test script.
    """

    name: Optional[String] = Field(
        description="Tracking/logging name of this test",
        default=None,
    )
    description: Optional[String] = Field(
        description="Tracking/reporting short description of the test",
        default=None,
    )
    action: Optional[ListType[TestReportTestAction]] = Field(
        description="A test operation or assert that was performed",
        default=None,
    )

class TestReportTeardownAction(BackboneElement):
    """
    The teardown action will only contain an operation.
    """

    operation: Optional[TestReportSetupActionOperation] = Field(
        description="The teardown operation performed",
        default=None,
    )

class TestReportTeardown(BackboneElement):
    """
    The results of the series of operations required to clean up after all the tests were executed (successfully or otherwise).
    """

    action: Optional[ListType[TestReportTeardownAction]] = Field(
        description="One or more teardown operations performed",
        default=None,
    )

class TestReport(DomainResource):
    """
    A summary of information based on the results of executing a TestScript.
    """

    _abstract = False
    _type = "TestReport"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/TestReport"

    contained: Optional[ListType[Resource]] = Field(
        description="Contained, inline Resources",
        default=None,
    )
    extension: Optional[ListType[Extension]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: Optional[ListType[Extension]] = Field(
        description="Extensions that cannot be ignored",
        default=None,
    )
    identifier: Optional[Identifier] = Field(
        description="External identifier",
        default=None,
    )
    name: Optional[String] = Field(
        description="Informal name of the executed TestScript",
        default=None,
    )
    status: Optional[Code] = Field(
        description="completed | in-progress | waiting | stopped | entered-in-error",
        default=None,
    )
    testScript: Optional[Reference] = Field(
        description="Reference to the  version-specific TestScript that was executed to produce this TestReport",
        default=None,
    )
    result: Optional[Code] = Field(
        description="pass | fail | pending",
        default=None,
    )
    score: Optional[Decimal] = Field(
        description="The final score (percentage of tests passed) resulting from the execution of the TestScript",
        default=None,
    )
    tester: Optional[String] = Field(
        description="Name of the tester producing this report (Organization or individual)",
        default=None,
    )
    issued: Optional[DateTime] = Field(
        description="When the TestScript was executed and this TestReport was generated",
        default=None,
    )
    participant: Optional[ListType[TestReportParticipant]] = Field(
        description="A participant in the test execution, either the execution engine, a client, or a server",
        default=None,
    )
    setup: Optional[TestReportSetup] = Field(
        description="The results of the series of required setup operations before the tests were executed",
        default=None,
    )
    test: Optional[ListType[TestReportTest]] = Field(
        description="A test executed from the test script",
        default=None,
    )
    teardown: Optional[TestReportTeardown] = Field(
        description="The results of running the series of required clean up steps",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_inv_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("setup.action",),
            expression="operation.exists() xor assert.exists()",
            human="Setup action SHALL contain either an operation or assert but not both.",
            key="inv-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_inv_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("test.action",),
            expression="operation.exists() xor assert.exists()",
            human="Test action SHALL contain either an operation or assert but not both.",
            key="inv-2",
            severity="error",
        )
