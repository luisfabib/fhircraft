from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class DeviceAssociationOperation(BackboneElement):
    """
    The details about the device when it is in use to describe its operation.
    """

    status: Optional[CodeableConcept] = Field(
        description="Device operational condition",
        default=None,
    )
    operator: Optional[List[Reference]] = Field(
        description="The individual performing the action enabled by the device",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Begin and end dates and times for the device\u0027s operation",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "period",
                "operator",
                "status",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class DeviceAssociation(DomainResource):
    """
    A record of association of a device.
    """

    _abstract = False
    _type = "DeviceAssociation"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceAssociation"

    id: Optional[String] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    id_ext: Optional[Element] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    meta: Optional[Meta] = Field(
        description="Metadata about the resource.",
        default_factory=lambda: Meta(
            profile=["http://hl7.org/fhir/StructureDefinition/DeviceAssociation"]
        ),
    )
    implicitRules: Optional[Uri] = Field(
        description="A set of rules under which this content was created",
        default=None,
    )
    implicitRules_ext: Optional[Element] = Field(
        description="Placeholder element for implicitRules extensions",
        default=None,
        alias="_implicitRules",
    )
    language: Optional[Code] = Field(
        description="Language of the resource content",
        default=None,
    )
    language_ext: Optional[Element] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    text: Optional[Narrative] = Field(
        description="Text summary of the resource, for human interpretation",
        default=None,
    )
    contained: Optional[List[Resource]] = Field(
        description="Contained, inline Resources",
        default=None,
    )
    extension: Optional[List[Extension]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: Optional[List[Extension]] = Field(
        description="Extensions that cannot be ignored",
        default=None,
    )
    identifier: Optional[List[Identifier]] = Field(
        description="Instance identifier",
        default=None,
    )
    device: Optional[Reference] = Field(
        description="Reference to the devices associated with the patient or group",
        default=None,
    )
    category: Optional[List[CodeableConcept]] = Field(
        description="Describes the relationship between the device and subject",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="implanted | explanted | attached | entered-in-error | unknown",
        default=None,
    )
    statusReason: Optional[List[CodeableConcept]] = Field(
        description="The reasons given for the current association status",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="The individual, group of individuals or device that the device is on or associated with",
        default=None,
    )
    bodyStructure: Optional[Reference] = Field(
        description="Current anatomical location of the device in/on subject",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Begin and end dates and times for the device association",
        default=None,
    )
    operation: Optional[List[DeviceAssociationOperation]] = Field(
        description="The details about the device when it is in use to describe its operation",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "operation",
                "period",
                "bodyStructure",
                "subject",
                "statusReason",
                "status",
                "category",
                "device",
                "identifier",
                "modifierExtension",
                "extension",
                "text",
                "language",
                "implicitRules",
                "meta",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "modifierExtension",
                "extension",
            ),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.contained.empty()",
            human="If the resource is contained in another resource, it SHALL NOT contain nested Resources",
            key="dom-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url))) or descendants().where(reference = '#').exists() or descendants().where(ofType(canonical) = '#').exists() or descendants().where(ofType(canonical) = '#').exists()).not()).trace('unmatched', id).empty()",
            human="If the resource is contained in another resource, it SHALL be referred to from elsewhere in the resource or SHALL refer to the containing resource",
            key="dom-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_4_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.versionId.empty() and contained.meta.lastUpdated.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a meta.versionId or a meta.lastUpdated",
            key="dom-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_5_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.security.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a security label",
            key="dom-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_6_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="text.`div`.exists()",
            human="A resource should have narrative for robust management",
            key="dom-6",
            severity="warning",
        )
