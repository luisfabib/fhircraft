import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
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

    actorId: Optional[fhir.string] = Field(
        description="ID or acronym of the actor",
        default=None,
    )
    type: Optional[fhir.code] = Field(
        description="person | entity",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="The name of the actor as shown in the page",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="The description of the actor",
        default=None,
    )


class ExampleScenarioInstanceVersion(BackboneElement):
    """
    A specific version of the resource.
    """

    versionId: Optional[fhir.string] = Field(
        description="The identifier of a specific version of a resource",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="The description of the resource version",
        default=None,
    )


class ExampleScenarioInstanceContainedInstance(BackboneElement):
    """
    Resources contained in the instance (e.g. the observations contained in a bundle).
    """

    resourceId: Optional[fhir.string] = Field(
        description="Each resource contained in the instance",
        default=None,
    )
    versionId: Optional[fhir.string] = Field(
        description="A specific version of a resource contained in the instance",
        default=None,
    )


class ExampleScenarioInstance(BackboneElement):
    """
    Each resource and each version that is present in the workflow.
    """

    resourceId: Optional[fhir.string] = Field(
        description="The id of the resource for referencing",
        default=None,
    )
    resourceType: Optional[fhir.code] = Field(
        description="The type of the resource",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="A short name for the resource instance",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Human-friendly description of the resource instance",
        default=None,
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

    resourceId: Optional[fhir.string] = Field(
        description="Each resource contained in the instance",
        default=None,
    )
    versionId: Optional[fhir.string] = Field(
        description="A specific version of a resource contained in the instance",
        default=None,
    )


class ExampleScenarioProcessStepOperation(BackboneElement):
    """
    Each interaction or action.
    """

    number: Optional[fhir.string] = Field(
        description="The sequential number of the interaction",
        default=None,
    )
    type: Optional[fhir.string] = Field(
        description="The type of operation - CRUD",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="The human-friendly name of the interaction",
        default=None,
    )
    initiator: Optional[fhir.string] = Field(
        description="Who starts the transaction",
        default=None,
    )
    receiver: Optional[fhir.string] = Field(
        description="Who receives the transaction",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="A comment to be inserted in the diagram",
        default=None,
    )
    initiatorActive: Optional[fhir.boolean] = Field(
        description="Whether the initiator is deactivated right after the transaction",
        default=None,
    )
    receiverActive: Optional[fhir.boolean] = Field(
        description="Whether the receiver is deactivated right after the transaction",
        default=None,
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

    title: Optional[fhir.string] = Field(
        description="Label for alternative",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="A human-readable description of each option",
        default=None,
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
    pause: Optional[fhir.boolean] = Field(
        description="If there is a pause in the flow",
        default=None,
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

    title: Optional[fhir.string] = Field(
        description="The diagram title of the group of operations",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="A longer description of the group of operations",
        default=None,
    )
    preConditions: Optional[fhir.markdown] = Field(
        description="Description of initial status before the process starts",
        default=None,
    )
    postConditions: Optional[fhir.markdown] = Field(
        description="Description of final status after the process ends",
        default=None,
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
    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this example scenario, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the example scenario",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the example scenario",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this example scenario (computer friendly)",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
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
        description="Name of the publisher (organization or individual)",
        default=None,
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
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="The purpose of the example, e.g. to illustrate a scenario",
        default=None,
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
    workflow: Optional[ListType[fhir.canonical]] = Field(
        description="Another nested workflow",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_esc_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="esc-0",
            severity="warning",
        )
