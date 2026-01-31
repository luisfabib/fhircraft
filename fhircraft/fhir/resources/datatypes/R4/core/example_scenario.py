import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Boolean,
    DateTime,
    Markdown,
    Canonical,
)

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    BackboneElement,
    ContactDetail,
    UsageContext,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource


class ExampleScenarioActor(BackboneElement):
    """
    Actor participating in the resource.
    """

    actorId: Optional[String] = Field(
        description="ID or acronym of the actor",
        default=None,
    )
    actorId_ext: Optional[Element] = Field(
        description="Placeholder element for actorId extensions",
        default=None,
        alias="_actorId",
    )
    type: Optional[Code] = Field(
        description="person | entity",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    name: Optional[String] = Field(
        description="The name of the actor as shown in the page",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    description: Optional[Markdown] = Field(
        description="The description of the actor",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )


class ExampleScenarioInstanceVersion(BackboneElement):
    """
    A specific version of the resource.
    """

    versionId: Optional[String] = Field(
        description="The identifier of a specific version of a resource",
        default=None,
    )
    versionId_ext: Optional[Element] = Field(
        description="Placeholder element for versionId extensions",
        default=None,
        alias="_versionId",
    )
    description: Optional[Markdown] = Field(
        description="The description of the resource version",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )


class ExampleScenarioInstanceContainedInstance(BackboneElement):
    """
    Resources contained in the instance (e.g. the observations contained in a bundle).
    """

    resourceId: Optional[String] = Field(
        description="Each resource contained in the instance",
        default=None,
    )
    resourceId_ext: Optional[Element] = Field(
        description="Placeholder element for resourceId extensions",
        default=None,
        alias="_resourceId",
    )
    versionId: Optional[String] = Field(
        description="A specific version of a resource contained in the instance",
        default=None,
    )
    versionId_ext: Optional[Element] = Field(
        description="Placeholder element for versionId extensions",
        default=None,
        alias="_versionId",
    )


class ExampleScenarioInstance(BackboneElement):
    """
    Each resource and each version that is present in the workflow.
    """

    resourceId: Optional[String] = Field(
        description="The id of the resource for referencing",
        default=None,
    )
    resourceId_ext: Optional[Element] = Field(
        description="Placeholder element for resourceId extensions",
        default=None,
        alias="_resourceId",
    )
    resourceType: Optional[Code] = Field(
        description="The type of the resource",
        default=None,
    )
    resourceType_ext: Optional[Element] = Field(
        description="Placeholder element for resourceType extensions",
        default=None,
        alias="_resourceType",
    )
    name: Optional[String] = Field(
        description="A short name for the resource instance",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    description: Optional[Markdown] = Field(
        description="Human-friendly description of the resource instance",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    version: Optional[ListType[ExampleScenarioInstanceVersion]] = Field(
        description="A specific version of the resource",
        default=None,
    )
    containedInstance: Optional[ListType[ExampleScenarioInstanceContainedInstance]] = (
        Field(
            description="Resources contained in the instance",
            default=None,
        )
    )


class ExampleScenarioProcessStepOperationRequest(BackboneElement):
    """
    Each resource instance used by the initiator.
    """

    resourceId: Optional[String] = Field(
        description="Each resource contained in the instance",
        default=None,
    )
    resourceId_ext: Optional[Element] = Field(
        description="Placeholder element for resourceId extensions",
        default=None,
        alias="_resourceId",
    )
    versionId: Optional[String] = Field(
        description="A specific version of a resource contained in the instance",
        default=None,
    )
    versionId_ext: Optional[Element] = Field(
        description="Placeholder element for versionId extensions",
        default=None,
        alias="_versionId",
    )


class ExampleScenarioProcessStepOperation(BackboneElement):
    """
    Each interaction or action.
    """

    number: Optional[String] = Field(
        description="The sequential number of the interaction",
        default=None,
    )
    number_ext: Optional[Element] = Field(
        description="Placeholder element for number extensions",
        default=None,
        alias="_number",
    )
    type: Optional[String] = Field(
        description="The type of operation - CRUD",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    name: Optional[String] = Field(
        description="The human-friendly name of the interaction",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    initiator: Optional[String] = Field(
        description="Who starts the transaction",
        default=None,
    )
    initiator_ext: Optional[Element] = Field(
        description="Placeholder element for initiator extensions",
        default=None,
        alias="_initiator",
    )
    receiver: Optional[String] = Field(
        description="Who receives the transaction",
        default=None,
    )
    receiver_ext: Optional[Element] = Field(
        description="Placeholder element for receiver extensions",
        default=None,
        alias="_receiver",
    )
    description: Optional[Markdown] = Field(
        description="A comment to be inserted in the diagram",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    initiatorActive: Optional[Boolean] = Field(
        description="Whether the initiator is deactivated right after the transaction",
        default=None,
    )
    initiatorActive_ext: Optional[Element] = Field(
        description="Placeholder element for initiatorActive extensions",
        default=None,
        alias="_initiatorActive",
    )
    receiverActive: Optional[Boolean] = Field(
        description="Whether the receiver is deactivated right after the transaction",
        default=None,
    )
    receiverActive_ext: Optional[Element] = Field(
        description="Placeholder element for receiverActive extensions",
        default=None,
        alias="_receiverActive",
    )
    request: Optional[ExampleScenarioProcessStepOperationRequest] = Field(
        description="Each resource instance used by the initiator",
        default=None,
    )
    response: Optional[ExampleScenarioInstanceContainedInstance] = Field(
        description="Each resource instance used by the responder",
        default=None,
    )


class ExampleScenarioProcessStepAlternative(BackboneElement):
    """
    Indicates an alternative step that can be taken instead of the operations on the base step in exceptional/atypical circumstances.
    """

    title: Optional[String] = Field(
        description="Label for alternative",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    description: Optional[Markdown] = Field(
        description="A human-readable description of each option",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    step: Optional[ListType["ExampleScenarioProcessStep"]] = Field(
        description="What happens in each alternative option",
        default=None,
    )


class ExampleScenarioProcessStep(BackboneElement):
    """
    Each step of the process.
    """

    process: Optional[ListType["ExampleScenarioProcess"]] = Field(
        description="Nested process",
        default=None,
    )
    pause: Optional[Boolean] = Field(
        description="If there is a pause in the flow",
        default=None,
    )
    pause_ext: Optional[Element] = Field(
        description="Placeholder element for pause extensions",
        default=None,
        alias="_pause",
    )
    operation: Optional[ExampleScenarioProcessStepOperation] = Field(
        description="Each interaction or action",
        default=None,
    )
    alternative: Optional[ListType[ExampleScenarioProcessStepAlternative]] = Field(
        description="Alternate non-typical step action",
        default=None,
    )


class ExampleScenarioProcess(BackboneElement):
    """
    Each major process - a group of operations.
    """

    title: Optional[String] = Field(
        description="The diagram title of the group of operations",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    description: Optional[Markdown] = Field(
        description="A longer description of the group of operations",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    preConditions: Optional[Markdown] = Field(
        description="Description of initial status before the process starts",
        default=None,
    )
    preConditions_ext: Optional[Element] = Field(
        description="Placeholder element for preConditions extensions",
        default=None,
        alias="_preConditions",
    )
    postConditions: Optional[Markdown] = Field(
        description="Description of final status after the process ends",
        default=None,
    )
    postConditions_ext: Optional[Element] = Field(
        description="Placeholder element for postConditions extensions",
        default=None,
        alias="_postConditions",
    )
    step: Optional[ListType[ExampleScenarioProcessStep]] = Field(
        description="Each step of the process",
        default=None,
    )


class ExampleScenario(DomainResource):
    """
    Example of workflow instance.
    """

    _abstract = False
    _type = "ExampleScenario"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ExampleScenario"

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
    url: Optional[Uri] = Field(
        description="Canonical identifier for this example scenario, represented as a URI (globally unique)",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the example scenario",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the example scenario",
        default=None,
    )
    version_ext: Optional[Element] = Field(
        description="Placeholder element for version extensions",
        default=None,
        alias="_version",
    )
    name: Optional[String] = Field(
        description="Name for this example scenario (computer friendly)",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    experimental: Optional[Boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    experimental_ext: Optional[Element] = Field(
        description="Placeholder element for experimental extensions",
        default=None,
        alias="_experimental",
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    publisher_ext: Optional[Element] = Field(
        description="Placeholder element for publisher extensions",
        default=None,
        alias="_publisher",
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for example scenario (if applicable)",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyright_ext: Optional[Element] = Field(
        description="Placeholder element for copyright extensions",
        default=None,
        alias="_copyright",
    )
    purpose: Optional[Markdown] = Field(
        description="The purpose of the example, e.g. to illustrate a scenario",
        default=None,
    )
    purpose_ext: Optional[Element] = Field(
        description="Placeholder element for purpose extensions",
        default=None,
        alias="_purpose",
    )
    actor: Optional[ListType[ExampleScenarioActor]] = Field(
        description="Actor participating in the resource",
        default=None,
    )
    instance: Optional[ListType[ExampleScenarioInstance]] = Field(
        description="Each resource and each version that is present in the workflow",
        default=None,
    )
    process: Optional[ListType[ExampleScenarioProcess]] = Field(
        description="Each major process - a group of operations",
        default=None,
    )
    workflow: Optional[ListType[Canonical]] = Field(
        description="Another nested workflow",
        default=None,
    )
    workflow_ext: Optional[Element] = Field(
        description="Placeholder element for workflow extensions",
        default=None,
        alias="_workflow",
    )

    @model_validator(mode="after")
    def FHIR_esc_0_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="esc-0",
            severity="warning",
        )


ExampleScenarioProcessStepAlternative.model_rebuild()
ExampleScenarioProcessStep.model_rebuild()
ExampleScenarioProcess.model_rebuild()
ExampleScenario.model_rebuild()
