from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
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
    BackboneElement,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class TestScriptOrigin(BackboneElement):
    """
    An abstract server used in operations within this test script in the origin element.
    """

    index: fhir.integer = Field(
        description="The index of the abstract origin server starting at 1",
    )
    profile: Coding = Field(
        description="FHIR-Client | FHIR-SDC-FormFiller",
    )
    url: Optional[fhir.url] = Field(
        description="The url path of the origin server",
        default=None,
    )


class TestScriptDestination(BackboneElement):
    """
    An abstract server used in operations within this test script in the destination element.
    """

    index: fhir.integer = Field(
        description="The index of the abstract destination server starting at 1",
    )
    profile: Coding = Field(
        description="FHIR-Server | FHIR-SDC-FormManager | FHIR-SDC-FormReceiver | FHIR-SDC-FormProcessor",
    )
    url: Optional[fhir.url] = Field(
        description="The url path of the destination server",
        default=None,
    )


class TestScriptMetadataLink(BackboneElement):
    """
    A link to the FHIR specification that this test is covering.
    """

    url: fhir.uri = Field(
        description="URL to the specification",
    )
    description: Optional[fhir.string] = Field(
        description="Short description",
        default=None,
    )


class TestScriptMetadataCapability(BackboneElement):
    """
    Capabilities that must exist and are assumed to function correctly on the FHIR server being tested.
    """

    required: fhir.boolean = Field(
        description="Are the capabilities required?",
    )
    validated: fhir.boolean = Field(
        description="Are the capabilities validated?",
    )
    description: Optional[fhir.string] = Field(
        description="The expected capabilities of the server",
        default=None,
    )
    origin: Optional[ListType[fhir.integer]] = Field(
        description="Which origin server these requirements apply to",
        default=None,
    )
    destination: Optional[fhir.integer] = Field(
        description="Which server these requirements apply to",
        default=None,
    )
    link: Optional[ListType[fhir.uri]] = Field(
        description="Links to the FHIR specification",
        default=None,
    )
    capabilities: fhir.canonical = Field(
        description="Required Capability Statement",
    )


class TestScriptMetadata(BackboneElement):
    """
    The required capability must exist and are assumed to function correctly on the FHIR server being tested.
    """

    link: Optional[ListType[TestScriptMetadataLink]] = Field(
        description="Links to the FHIR specification",
        default=None,
    )
    capability: ListType[TestScriptMetadataCapability] = Field(
        description="Capabilities  that are assumed to function correctly on the FHIR server being tested",
     	min_length=1,
	)


class TestScriptScope(BackboneElement):
    """
    The scope indicates a conformance artifact that is tested by the test(s) within this test case and the expectation of the test outcome(s) as well as the intended test phase inclusion.
    """

    artifact: fhir.canonical = Field(
        description="The specific conformance artifact being tested",
    )
    conformance: Optional[CodeableConcept] = Field(
        description="required | optional | strict",
        default=None,
    )
    phase: Optional[CodeableConcept] = Field(
        description="unit | integration | production",
        default=None,
    )


class TestScriptFixture(BackboneElement):
    """
    Fixture in the test script - by reference (uri). All fixtures are required for the test script to execute.
    """

    autocreate: fhir.boolean = Field(
        description="Whether or not to implicitly create the fixture during setup",
    )
    autodelete: fhir.boolean = Field(
        description="Whether or not to implicitly delete the fixture during teardown",
    )
    resource: Optional[Reference] = Field(
        description="Reference of the resource",
        default=None,
    )


class TestScriptVariable(BackboneElement):
    """
    Variable is set based either on element value in response body or on header field value in the response headers.
    """

    name: fhir.string = Field(
        description="Descriptive name for this variable",
    )
    defaultValue: Optional[fhir.string] = Field(
        description="Default, hard-coded, or user-defined value for this variable",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Natural language description of the variable",
        default=None,
    )
    expression: Optional[fhir.string] = Field(
        description="The FHIRPath expression against the fixture body",
        default=None,
    )
    headerField: Optional[fhir.string] = Field(
        description="HTTP header field name for source",
        default=None,
    )
    hint: Optional[fhir.string] = Field(
        description="Hint help text for default value to enter",
        default=None,
    )
    path: Optional[fhir.string] = Field(
        description="XPath or JSONPath against the fixture body",
        default=None,
    )
    sourceId: Optional[fhir.id_] = Field(
        description="Fixture id_ of source expression or headerField within this variable",
        default=None,
    )


class TestScriptSetupActionOperation(BackboneElement):
    """
    The operation to perform.
    """

    type: Optional[Coding] = Field(
        description="The operation code type that will be executed",
        default=None,
    )
    resource: Optional[fhir.uri] = Field(
        description="Resource type",
        default=None,
    )
    label: Optional[fhir.string] = Field(
        description="Tracking/logging operation label",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Tracking/reporting operation description",
        default=None,
    )
    accept: Optional[fhir.code] = Field(
        description="Mime type to accept in the payload of the response, with charset etc",
        default=None,
    )
    contentType: Optional[fhir.code] = Field(
        description="Mime type of the request payload contents, with charset etc",
        default=None,
    )
    destination: Optional[fhir.integer] = Field(
        description="Server responding to the request",
        default=None,
    )
    encodeRequestUrl: fhir.boolean = Field(
        description="Whether or not to send the request url in encoded format",
    )
    method: Optional[fhir.code] = Field(
        description="delete | get | options | patch | post | put | head",
        default=None,
    )
    origin: Optional[fhir.integer] = Field(
        description="Server initiating the request",
        default=None,
    )
    params: Optional[fhir.string] = Field(
        description="Explicitly defined path parameters",
        default=None,
    )
    requestHeader: Optional[ListType["TestScriptSetupActionOperationRequestHeader"]] = (
        Field(
            description="Each operation can have one or more header elements",
            default=None,
        )
    )
    requestId: Optional[fhir.id_] = Field(
        description="Fixture id_ of mapped request",
        default=None,
    )
    responseId: Optional[fhir.id_] = Field(
        description="Fixture id_ of mapped response",
        default=None,
    )
    sourceId: Optional[fhir.id_] = Field(
        description="Fixture id_ of body for PUT and POST requests",
        default=None,
    )
    targetId: Optional[fhir.id_] = Field(
        description="id_ of fixture used for extracting the [id],  [type], and [vid] for GET requests",
        default=None,
    )
    url: Optional[fhir.string] = Field(
        description="Request URL",
        default=None,
    )


class TestScriptSetupActionAssert(BackboneElement):
    """
    Evaluates the results of previous operations to determine if the server under test behaves appropriately.
    """

    label: Optional[fhir.string] = Field(
        description="Tracking/logging assertion label",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Tracking/reporting assertion description",
        default=None,
    )
    direction: Optional[fhir.code] = Field(
        description="response | request",
        default=None,
    )
    compareToSourceId: Optional[fhir.string] = Field(
        description="id_ of the source fixture to be evaluated",
        default=None,
    )
    compareToSourceExpression: Optional[fhir.string] = Field(
        description="The FHIRPath expression to evaluate against the source fixture",
        default=None,
    )
    compareToSourcePath: Optional[fhir.string] = Field(
        description="XPath or JSONPath expression to evaluate against the source fixture",
        default=None,
    )
    contentType: Optional[fhir.code] = Field(
        description="Mime type to compare against the \u0027Content-Type\u0027 header",
        default=None,
    )
    defaultManualCompletion: Optional[fhir.code] = Field(
        description="fail | pass | skip | stop",
        default=None,
    )
    expression: Optional[fhir.string] = Field(
        description="The FHIRPath expression to be evaluated",
        default=None,
    )
    headerField: Optional[fhir.string] = Field(
        description="HTTP header field name",
        default=None,
    )
    minimumId: Optional[fhir.string] = Field(
        description="Fixture id_ of minimum content resource",
        default=None,
    )
    navigationLinks: Optional[fhir.boolean] = Field(
        description="Perform validation on navigation links?",
        default=None,
    )
    operator: Optional[fhir.code] = Field(
        description="equals | notEquals | in | notIn | greaterThan | lessThan | empty | notEmpty | contains | notContains | eval | manualEval",
        default=None,
    )
    path: Optional[fhir.string] = Field(
        description="XPath or JSONPath expression",
        default=None,
    )
    requestMethod: Optional[fhir.code] = Field(
        description="delete | get | options | patch | post | put | head",
        default=None,
    )
    requestURL: Optional[fhir.string] = Field(
        description="Request URL comparison value",
        default=None,
    )
    resource: Optional[fhir.uri] = Field(
        description="Resource type",
        default=None,
    )
    response: Optional[fhir.code] = Field(
        description="continue | switchingProtocols | okay | created | accepted | nonAuthoritativeInformation | noContent | resetContent | partialContent | multipleChoices | movedPermanently | found | seeOther | notModified | useProxy | temporaryRedirect | permanentRedirect | badRequest | unauthorized | paymentRequired | forbidden | notFound | methodNotAllowed | notAcceptable | proxyAuthenticationRequired | requestTimeout | conflict | gone | lengthRequired | preconditionFailed | contentTooLarge | uriTooLong | unsupportedMediaType | rangeNotSatisfiable | expectationFailed | misdirectedRequest | unprocessableContent | upgradeRequired | internalServerError | notImplemented | badGateway | serviceUnavailable | gatewayTimeout | httpVersionNotSupported",
        default=None,
    )
    responseCode: Optional[fhir.string] = Field(
        description="HTTP response code to test",
        default=None,
    )
    sourceId: Optional[fhir.id_] = Field(
        description="Fixture id_ of source expression or headerField",
        default=None,
    )
    stopTestOnFail: fhir.boolean = Field(
        description="If this assert fails, will the current test execution stop?",
    )
    validateProfileId: Optional[fhir.id_] = Field(
        description="Profile id_ of validation profile reference",
        default=None,
    )
    value: Optional[fhir.string] = Field(
        description="The value to compare to",
        default=None,
    )
    warningOnly: fhir.boolean = Field(
        description="Will this assert produce a warning only on error?",
    )
    requirement: Optional[ListType["TestScriptSetupActionAssertRequirement"]] = Field(
        description="Links or references to the testing requirements",
        default=None,
    )


class TestScriptSetupAction(BackboneElement):
    """
    Action would contain either an operation or an assertion.
    """

    operation: Optional[TestScriptSetupActionOperation] = Field(
        description="The setup operation to perform",
        default=None,
    )
    assert_: Optional[TestScriptSetupActionAssert] = Field(
        description="The assertion to perform",
        default=None,
        alias="assert",
    )


class TestScriptSetup(BackboneElement):
    """
    A series of required setup operations before tests are executed.
    """

    action: ListType[TestScriptSetupAction] = Field(
        description="A setup operation or assert to perform",
     	min_length=1,
	)


class TestScriptSetupActionOperationRequestHeader(BackboneElement):
    """
    Header elements would be used to set HTTP headers.
    """

    field: fhir.string = Field(
        description="HTTP header field name",
    )
    value: fhir.string = Field(
        description="HTTP headerfield value",
    )


class TestScriptTestActionOperation(BackboneElement):
    """
    An operation would involve a REST request to a server.
    """

    type: Optional[Coding] = Field(
        description="The operation code type that will be executed",
        default=None,
    )
    resource: Optional[fhir.uri] = Field(
        description="Resource type",
        default=None,
    )
    label: Optional[fhir.string] = Field(
        description="Tracking/logging operation label",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Tracking/reporting operation description",
        default=None,
    )
    accept: Optional[fhir.code] = Field(
        description="Mime type to accept in the payload of the response, with charset etc",
        default=None,
    )
    contentType: Optional[fhir.code] = Field(
        description="Mime type of the request payload contents, with charset etc",
        default=None,
    )
    destination: Optional[fhir.integer] = Field(
        description="Server responding to the request",
        default=None,
    )
    encodeRequestUrl: Optional[fhir.boolean] = Field(
        description="Whether or not to send the request url in encoded format",
        default=None,
    )
    method: Optional[fhir.code] = Field(
        description="delete | get | options | patch | post | put | head",
        default=None,
    )
    origin: Optional[fhir.integer] = Field(
        description="Server initiating the request",
        default=None,
    )
    params: Optional[fhir.string] = Field(
        description="Explicitly defined path parameters",
        default=None,
    )
    requestHeader: Optional[ListType[TestScriptSetupActionOperationRequestHeader]] = (
        Field(
            description="Each operation can have one or more header elements",
            default=None,
        )
    )
    requestId: Optional[fhir.id_] = Field(
        description="Fixture id_ of mapped request",
        default=None,
    )
    responseId: Optional[fhir.id_] = Field(
        description="Fixture id_ of mapped response",
        default=None,
    )
    sourceId: Optional[fhir.id_] = Field(
        description="Fixture id_ of body for PUT and POST requests",
        default=None,
    )
    targetId: Optional[fhir.id_] = Field(
        description="id_ of fixture used for extracting the [id],  [type], and [vid] for GET requests",
        default=None,
    )
    url: Optional[fhir.string] = Field(
        description="Request URL",
        default=None,
    )


class TestScriptSetupActionAssertRequirement(BackboneElement):
    """
    Links or references providing traceability to the testing requirements for this assert.
    """

    linkUri: Optional[fhir.uri] = Field(
        description="Link or reference to the testing requirement",
        default=None,
    )
    linkCanonical: Optional[fhir.canonical] = Field(
        description="Link or reference to the testing requirement",
        default=None,
    )

    @property
    def link(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="link",
        )

    @model_validator(mode="after")
    def link_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Uri, fhir.Canonical],
            field_name_base="link",
            required=False,
        )


class TestScriptTestActionAssert(BackboneElement):
    """
    Evaluates the results of previous operations to determine if the server under test behaves appropriately.
    """

    label: Optional[fhir.string] = Field(
        description="Tracking/logging assertion label",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Tracking/reporting assertion description",
        default=None,
    )
    direction: Optional[fhir.code] = Field(
        description="response | request",
        default=None,
    )
    compareToSourceId: Optional[fhir.string] = Field(
        description="id_ of the source fixture to be evaluated",
        default=None,
    )
    compareToSourceExpression: Optional[fhir.string] = Field(
        description="The FHIRPath expression to evaluate against the source fixture",
        default=None,
    )
    compareToSourcePath: Optional[fhir.string] = Field(
        description="XPath or JSONPath expression to evaluate against the source fixture",
        default=None,
    )
    contentType: Optional[fhir.code] = Field(
        description="Mime type to compare against the \u0027Content-Type\u0027 header",
        default=None,
    )
    defaultManualCompletion: Optional[fhir.code] = Field(
        description="fail | pass | skip | stop",
        default=None,
    )
    expression: Optional[fhir.string] = Field(
        description="The FHIRPath expression to be evaluated",
        default=None,
    )
    headerField: Optional[fhir.string] = Field(
        description="HTTP header field name",
        default=None,
    )
    minimumId: Optional[fhir.string] = Field(
        description="Fixture id_ of minimum content resource",
        default=None,
    )
    navigationLinks: Optional[fhir.boolean] = Field(
        description="Perform validation on navigation links?",
        default=None,
    )
    operator: Optional[fhir.code] = Field(
        description="equals | notEquals | in | notIn | greaterThan | lessThan | empty | notEmpty | contains | notContains | eval | manualEval",
        default=None,
    )
    path: Optional[fhir.string] = Field(
        description="XPath or JSONPath expression",
        default=None,
    )
    requestMethod: Optional[fhir.code] = Field(
        description="delete | get | options | patch | post | put | head",
        default=None,
    )
    requestURL: Optional[fhir.string] = Field(
        description="Request URL comparison value",
        default=None,
    )
    resource: Optional[fhir.uri] = Field(
        description="Resource type",
        default=None,
    )
    response: Optional[fhir.code] = Field(
        description="continue | switchingProtocols | okay | created | accepted | nonAuthoritativeInformation | noContent | resetContent | partialContent | multipleChoices | movedPermanently | found | seeOther | notModified | useProxy | temporaryRedirect | permanentRedirect | badRequest | unauthorized | paymentRequired | forbidden | notFound | methodNotAllowed | notAcceptable | proxyAuthenticationRequired | requestTimeout | conflict | gone | lengthRequired | preconditionFailed | contentTooLarge | uriTooLong | unsupportedMediaType | rangeNotSatisfiable | expectationFailed | misdirectedRequest | unprocessableContent | upgradeRequired | internalServerError | notImplemented | badGateway | serviceUnavailable | gatewayTimeout | httpVersionNotSupported",
        default=None,
    )
    responseCode: Optional[fhir.string] = Field(
        description="HTTP response code to test",
        default=None,
    )
    sourceId: Optional[fhir.id_] = Field(
        description="Fixture id_ of source expression or headerField",
        default=None,
    )
    stopTestOnFail: Optional[fhir.boolean] = Field(
        description="If this assert fails, will the current test execution stop?",
        default=None,
    )
    validateProfileId: Optional[fhir.id_] = Field(
        description="Profile id_ of validation profile reference",
        default=None,
    )
    value: Optional[fhir.string] = Field(
        description="The value to compare to",
        default=None,
    )
    warningOnly: Optional[fhir.boolean] = Field(
        description="Will this assert produce a warning only on error?",
        default=None,
    )
    requirement: Optional[ListType[TestScriptSetupActionAssertRequirement]] = Field(
        description="Links or references to the testing requirements",
        default=None,
    )


class TestScriptTestAction(BackboneElement):
    """
    Action would contain either an operation or an assertion.
    """

    operation: Optional[TestScriptTestActionOperation] = Field(
        description="The setup operation to perform",
        default=None,
    )
    assert_: Optional[TestScriptTestActionAssert] = Field(
        description="The setup assertion to perform",
        default=None,
        alias="assert",
    )


class TestScriptTest(BackboneElement):
    """
    A test in this script.
    """

    name: Optional[fhir.string] = Field(
        description="Tracking/logging name of this test",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Tracking/reporting short description of the test",
        default=None,
    )
    action: ListType[TestScriptTestAction] = Field(
        description="A test operation or assert to perform",
     	min_length=1,
	)


class TestScriptTeardownAction(BackboneElement):
    """
    The teardown action will only contain an operation.
    """

    operation: TestScriptSetupActionOperation = Field(
        description="The teardown operation to perform",
    )


class TestScriptTeardown(BackboneElement):
    """
    A series of operations required to clean up after all the tests are executed (successfully or otherwise).
    """

    action: ListType[TestScriptTeardownAction] = Field(
        description="One or more teardown operations to perform",
     	min_length=1,
	)


class TestScript(DomainResource):
    """
    A structured set of tests against a FHIR server or client implementation to determine compliance against the FHIR specification.
    """

    _abstract = False
    _type = "TestScript"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/TestScript"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this test script, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the test script",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the test script",
        default=None,
    )
    versionAlgorithmString: Optional[fhir.string] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: fhir.string = Field(
        description="Name for this test script (computer friendly)",
    )
    title: Optional[fhir.string] = Field(
        description="Name for this test script (human friendly)",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | active | retired | unknown",
    )
    experimental: Optional[fhir.boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[fhir.string] = Field(
        description="Name of the publisher/steward (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the test script",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for test script (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this test script is defined",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyrightLabel: Optional[fhir.string] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    origin: Optional[ListType[TestScriptOrigin]] = Field(
        description="An abstract server representing a client or sender in a message exchange",
        default=None,
    )
    destination: Optional[ListType[TestScriptDestination]] = Field(
        description="An abstract server representing a destination or receiver in a message exchange",
        default=None,
    )
    metadata: Optional[TestScriptMetadata] = Field(
        description="Required capability that is assumed to function correctly on the FHIR server being tested",
        default=None,
    )
    scope: Optional[ListType[TestScriptScope]] = Field(
        description="Indication of the artifact(s) that are tested by this test case",
        default=None,
    )
    fixture: Optional[ListType[TestScriptFixture]] = Field(
        description="Fixture in the test script - by reference (uri)",
        default=None,
    )
    profile: Optional[ListType[fhir.canonical]] = Field(
        description="Reference of the validation profile",
        default=None,
    )
    variable: Optional[ListType[TestScriptVariable]] = Field(
        description="Placeholder for evaluated elements",
        default=None,
    )
    setup: Optional[TestScriptSetup] = Field(
        description="A series of required setup operations before tests are executed",
        default=None,
    )
    test: Optional[ListType[TestScriptTest]] = Field(
        description="A test in this script",
        default=None,
    )
    teardown: Optional[TestScriptTeardown] = Field(
        description="A series of required clean up steps",
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
            field_types=[fhir.String, Coding],
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

    @model_validator(mode="after")
    def FHIR_tst_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("setup.action",),
            expression="operation.exists() xor assert.exists()",
            human="Setup action SHALL contain either an operation or assert but not both.",
            key="tst-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("test.action",),
            expression="operation.exists() xor assert.exists()",
            human="Test action SHALL contain either an operation or assert but not both.",
            key="tst-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("variable",),
            expression="expression.empty() or headerField.empty() or path.empty()",
            human="Variable can only contain one of expression, headerField or path.",
            key="tst-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_4_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("metadata",),
            expression="capability.required.exists() or capability.validated.exists()",
            human="TestScript metadata capability SHALL contain required or validated or both.",
            key="tst-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_5_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("setup.action.assert_",),
            expression="extension.exists() or (contentType.count() + expression.count() + headerField.count() + minimumId.count() + navigationLinks.count() + path.count() + requestMethod.count() + resource.count() + responseCode.count() + response.count() + validateProfileId.count() <=1) or (((expression.count() + minimumId.count() <=2) or (expression.count() + validateProfileId.count() <=2)) and (expression.count() + path.count() <=1) and (minimumId.count() + validateProfileId.count() <=1)) or (((path.count() + minimumId.count() <=2) or (path.count() + validateProfileId.count() <=2)) and (expression.count() + path.count() <=1) and (minimumId.count() + validateProfileId.count() <=1))",
            human="Only a single assertion SHALL be present within setup action assert element.",
            key="tst-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_6_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("test.action.assert_",),
            expression="extension.exists() or (contentType.count() + expression.count() + headerField.count() + minimumId.count() + navigationLinks.count() + path.count() + requestMethod.count() + resource.count() + responseCode.count() + response.count() + validateProfileId.count() <=1) or (((expression.count() + minimumId.count() <=2) or (expression.count() + validateProfileId.count() <=2)) and (expression.count() + path.count() <=1) and (minimumId.count() + validateProfileId.count() <=1)) or (((path.count() + minimumId.count() <=2) or (path.count() + validateProfileId.count() <=2)) and (expression.count() + path.count() <=1) and (minimumId.count() + validateProfileId.count() <=1))",
            human="Only a single assertion SHALL be present within test action assert element.",
            key="tst-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_7_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("setup.action.operation",),
            expression="sourceId.exists() or (targetId.count() + url.count() + params.count() = 1) or (type.code in ('capabilities' |'search' | 'transaction' | 'history'))",
            human="Setup operation SHALL contain either sourceId or targetId or params or url.",
            key="tst-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_8_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("test.action.operation",),
            expression="sourceId.exists() or (targetId.count() + url.count() + params.count() = 1) or (type.code in ('capabilities' | 'search' | 'transaction' | 'history'))",
            human="Test operation SHALL contain either sourceId or targetId or params or url.",
            key="tst-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_9_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("teardown.action.operation",),
            expression="sourceId.exists() or (targetId.count() + url.count() + params.count() = 1) or (type.code in ('capabilities' | 'search' | 'transaction' | 'history'))",
            human="Teardown operation SHALL contain either sourceId or targetId or params or url.",
            key="tst-9",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_10_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("setup.action.assert_",),
            expression="compareToSourceId.empty() xor (compareToSourceExpression.exists() or compareToSourcePath.exists())",
            human="Setup action assert SHALL contain either compareToSourceId and compareToSourceExpression, compareToSourceId and compareToSourcePath or neither.",
            key="tst-10",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_11_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("test.action.assert_",),
            expression="compareToSourceId.empty() xor (compareToSourceExpression.exists() or compareToSourcePath.exists())",
            human="Test action assert SHALL contain either compareToSourceId and compareToSourceExpression, compareToSourceId and compareToSourcePath or neither.",
            key="tst-11",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_12_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("setup.action.assert_",),
            expression="(response.empty() and responseCode.empty() and direction = 'request') or direction.empty() or direction = 'response'",
            human="Setup action assert response and responseCode SHALL be empty when direction equals request",
            key="tst-12",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tst_13_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("test.action.assert_",),
            expression="(response.empty() and responseCode.empty() and direction = 'request') or direction.empty() or direction = 'response'",
            human="Test action assert response and response and responseCode SHALL be empty when direction equals request",
            key="tst-13",
            severity="error",
        )
