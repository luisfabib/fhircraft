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


class ExampleScenarioActor(BackboneElement):
    """
    A system or person who shares or receives an instance within the scenario.
    """

    key: Optional[fhir.string] = Field(
        description="ID or acronym of the actor",
        default=None,
    )
    type: Optional[fhir.code] = Field(
        description="person | system",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Label for actor when rendering",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Details about actor",
        default=None,
    )


class ExampleScenarioInstanceVersion(BackboneElement):
    """
    Represents the instance as it was at a specific time-point.
    """

    key: Optional[fhir.string] = Field(
        description="ID or acronym of the version",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Label for instance version",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Details about version",
        default=None,
    )
    content: Optional[Reference] = Field(
        description="Example instance version data",
        default=None,
    )


class ExampleScenarioInstanceContainedInstance(BackboneElement):
    """
    References to other instances that can be found within this instance (e.g. the observations contained in a bundle).
    """

    instanceReference: Optional[fhir.string] = Field(
        description="Key of contained instance",
        default=None,
    )
    versionReference: Optional[fhir.string] = Field(
        description="Key of contained instance version",
        default=None,
    )


class ExampleScenarioInstance(BackboneElement):
    """
    A single data collection that is shared as part of the scenario.
    """

    key: Optional[fhir.string] = Field(
        description="ID or acronym of the instance",
        default=None,
    )
    structureType: Optional[Coding] = Field(
        description="Data structure for example",
        default=None,
    )
    structureVersion: Optional[fhir.string] = Field(
        description="E.g. 4.0.1",
        default=None,
    )
    structureProfileCanonical: Optional[fhir.canonical] = Field(
        description="Rules instance adheres to",
        default=None,
    )
    structureProfileUri: Optional[fhir.uri] = Field(
        description="Rules instance adheres to",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Label for instance",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Human-friendly description of the instance",
        default=None,
    )
    content: Optional[Reference] = Field(
        description="Example instance data",
        default=None,
    )
    version: Optional[ListType[ExampleScenarioInstanceVersion]] = Field(
        description="Snapshot of instance that changes",
        default=None,
    )
    containedInstance: Optional[ListType[ExampleScenarioInstanceContainedInstance]] = (
        Field(
            description="Resources contained in the instance",
            default=None,
        )
    )

    @property
    def structureProfile(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="structureProfile",
        )

    @model_validator(mode="after")
    def structureProfile_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Canonical, fhir.Uri],
            field_name_base="structureProfile",
            required=False,
        )


class ExampleScenarioProcessStepOperationRequest(BackboneElement):
    """
    A reference to the instance that is transmitted from requester to receiver as part of the invocation of the operation.
    """

    instanceReference: Optional[fhir.string] = Field(
        description="Key of contained instance",
        default=None,
    )
    versionReference: Optional[fhir.string] = Field(
        description="Key of contained instance version",
        default=None,
    )


class ExampleScenarioProcessStepOperation(BackboneElement):
    """
    The step represents a single operation invoked on receiver by sender.
    """

    type: Optional[Coding] = Field(
        description="Kind of action",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Label for step",
        default=None,
    )
    initiator: Optional[fhir.string] = Field(
        description="Who starts the operation",
        default=None,
    )
    receiver: Optional[fhir.string] = Field(
        description="Who receives the operation",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Human-friendly description of the operation",
        default=None,
    )
    initiatorActive: Optional[fhir.boolean] = Field(
        description="Initiator stays active?",
        default=None,
    )
    receiverActive: Optional[fhir.boolean] = Field(
        description="Receiver stays active?",
        default=None,
    )
    request: Optional[ExampleScenarioProcessStepOperationRequest] = Field(
        description="Instance transmitted on invocation",
        default=None,
    )
    response: Optional[ExampleScenarioInstanceContainedInstance] = Field(
        description="Instance transmitted on invocation response",
        default=None,
    )


class ExampleScenarioProcessStepAlternative(BackboneElement):
    """
    Indicates an alternative step that can be taken instead of the sub-process, scenario or operation.  E.g. to represent non-happy-path/exceptional/atypical circumstances.
    """

    title: Optional[fhir.string] = Field(
        description="Label for alternative",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Human-readable description of option",
        default=None,
    )
    step: Optional[ListType["ExampleScenarioProcessStep"]] = Field(
        description="Alternative action(s)",
        default=None,
    )


class ExampleScenarioProcessStep(BackboneElement):
    """
    A significant action that occurs as part of the process.
    """

    number: Optional[fhir.string] = Field(
        description="Sequential number of the step",
        default=None,
    )
    process: Optional["ExampleScenarioProcess"] = Field(
        description="Step is nested process",
        default=None,
    )
    workflow: Optional[fhir.canonical] = Field(
        description="Step is nested workflow",
        default=None,
    )
    operation: Optional[ExampleScenarioProcessStepOperation] = Field(
        description="Step is simple action",
        default=None,
    )
    alternative: Optional[ListType[ExampleScenarioProcessStepAlternative]] = Field(
        description="Alternate non-typical step action",
        default=None,
    )
    pause: Optional[fhir.boolean] = Field(
        description="Pause in the flow?",
        default=None,
    )


class ExampleScenarioProcess(BackboneElement):
    """
    A group of operations that represents a significant step within a scenario.
    """

    title: Optional[fhir.string] = Field(
        description="Label for procss",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Human-friendly description of the process",
        default=None,
    )
    preConditions: Optional[fhir.markdown] = Field(
        description="Status before process starts",
        default=None,
    )
    postConditions: Optional[fhir.markdown] = Field(
        description="Status after successful completion",
        default=None,
    )
    step: Optional[ListType[ExampleScenarioProcessStep]] = Field(
        description="Event within of the process",
        default=None,
    )


class ExampleScenario(DomainResource):
    """
    A walkthrough of a workflow showing the interaction between systems and the instances shared, possibly including the evolution of instances over time.
    """

    _abstract = False
    _type = "ExampleScenario"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ExampleScenario"

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
    versionAlgorithmString: Optional[fhir.string] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="To be removed?",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this example scenario (human friendly)",
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
        description="Name of the publisher/steward (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the ExampleScenario",
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
    purpose: Optional[fhir.markdown] = Field(
        description="The purpose of the example, e.g. to illustrate a scenario",
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
    actor: Optional[ListType[ExampleScenarioActor]] = Field(
        description="Individual involved in exchange",
        default=None,
    )
    instance: Optional[ListType[ExampleScenarioInstance]] = Field(
        description="Data used in the scenario",
        default=None,
    )
    process: Optional[ListType[ExampleScenarioProcess]] = Field(
        description="Major process within scenario",
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
    def FHIR_exs_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("instance",),
            expression="structureType.exists() and structureType.memberOf('http://hl7.org/fhir/ValueSet/resource-types').not() implies structureVersion.exists()",
            human="StructureVersion is required if structureType is not FHIR (but may still be present even if FHIR)",
            key="exs-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("instance",),
            expression="content.exists() implies version.empty()",
            human="instance.content is only allowed if there are no instance.versions",
            key="exs-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="status='active' or status='retired' implies actor.exists()",
            human="Must have actors if status is active or required",
            key="exs-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_4_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="status='active' or status='retired' implies process.exists()",
            human="Must have processes if status is active or required",
            key="exs-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_5_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("process",),
            expression="%resource.status='active' or %resource.status='retired' implies step.exists()",
            human="Processes must have steps if ExampleScenario status is active or required",
            key="exs-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_6_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="actor.key.count() = actor.key.distinct().count()",
            human="Actor keys must be unique",
            key="exs-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_7_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="actor.title.count() = actor.title.distinct().count()",
            human="Actor titles must be unique",
            key="exs-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_8_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="instance.key.count() = instance.key.distinct().count()",
            human="Instance keys must be unique",
            key="exs-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_9_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="instance.title.count() = instance.title.distinct().count()",
            human="Instance titles must be unique",
            key="exs-9",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_10_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("instance",),
            expression="version.key.count() = version.key.distinct().count()",
            human="Version keys must be unique within an instance",
            key="exs-10",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_11_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("instance",),
            expression="version.title.count() = version.title.distinct().count()",
            human="Version titles must be unique within an instance",
            key="exs-11",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_12_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="process.title.count() = process.title.distinct().count()",
            human="Process titles must be unique",
            key="exs-12",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_13_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("process.step",),
            expression="alternative.title.count() = alternative.title.distinct().count()",
            human="Alternative titles must be unique within a step",
            key="exs-13",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_14_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("instance.containedInstance",),
            expression="%resource.instance.where(key=%context.instanceReference).exists()",
            human="InstanceReference must be a key of an instance defined in the ExampleScenario",
            key="exs-14",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_15_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("instance.containedInstance",),
            expression="versionReference.empty() implies %resource.instance.where(key=%context.instanceReference).version.empty()",
            human="versionReference must be specified if the referenced instance defines versions",
            key="exs-15",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_16_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("instance.containedInstance",),
            expression="versionReference.exists() implies %resource.instance.where(key=%context.instanceReference).version.where(key=%context.versionReference).exists()",
            human="versionReference must be a key of a version within the instance pointed to by instanceReference",
            key="exs-16",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_17_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("process.step.operation",),
            expression="initiator.exists() implies initiator = 'OTHER' or %resource.actor.where(key=%context.initiator).exists()",
            human="If specified, initiator must be a key of an actor within the ExampleScenario",
            key="exs-17",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_18_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("process.step.operation",),
            expression="receiver.exists() implies receiver = 'OTHER' or %resource.actor.where(key=%context.receiver).exists()",
            human="If specified, receiver must be a key of an actor within the ExampleScenario",
            key="exs-18",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_19_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("actor",),
            expression="%resource.process.descendants().select(operation).where(initiator=%context.key or receiver=%context.key).exists()",
            human="Actor should be referenced in at least one operation",
            key="exs-19",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_exs_20_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("instance",),
            expression="%resource.process.descendants().select(instanceReference).where($this=%context.key).exists()",
            human="Instance should be referenced in at least one location",
            key="exs-20",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_exs_21_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("instance",),
            expression="version.exists() implies version.key.intersect(%resource.process.descendants().where(instanceReference = %context.key).versionReference).exists()",
            human="Instance version should be referenced in at least one operation",
            key="exs-21",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_exs_22_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("process.step",),
            expression="(process.exists() implies workflow.empty() and operation.empty()) and (workflow.exists() implies operation.empty())",
            human="Can have a process, a workflow, one or more operations or none of these, but cannot have a combination",
            key="exs-22",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exs_23_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("actor",),
            expression="key != 'OTHER'",
            human="actor.key canot be 'OTHER'",
            key="exs-23",
            severity="error",
        )
