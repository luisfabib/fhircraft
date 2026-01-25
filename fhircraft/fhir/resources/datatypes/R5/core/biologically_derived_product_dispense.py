from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, DateTime

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class BiologicallyDerivedProductDispensePerformer(BackboneElement):
    """
    Indicates who or what performed an action.
    """

    function: Optional[CodeableConcept] = Field(
        description="Identifies the function of the performer during the dispense",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Who performed the action",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "actor",
                "function",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class BiologicallyDerivedProductDispense(DomainResource):
    """
    A record of dispensation of a biologically derived product.
    """

    _abstract = False
    _type = "BiologicallyDerivedProductDispense"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/BiologicallyDerivedProductDispense"
    )

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
            profile=[
                "http://hl7.org/fhir/StructureDefinition/BiologicallyDerivedProductDispense"
            ]
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
        description="Business identifier for this dispense",
        default=None,
    )
    basedOn: Optional[List[Reference]] = Field(
        description="The order or request that this dispense is fulfilling",
        default=None,
    )
    partOf: Optional[List[Reference]] = Field(
        description="Short description",
        default=None,
    )
    status: Optional[Code] = Field(
        description="preparation | in-progress | allocated | issued | unfulfilled | returned | entered-in-error | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    originRelationshipType: Optional[CodeableConcept] = Field(
        description="Relationship between the donor and intended recipient",
        default=None,
    )
    product: Optional[Reference] = Field(
        description="The BiologicallyDerivedProduct that is dispensed",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="The intended recipient of the dispensed product",
        default=None,
    )
    matchStatus: Optional[CodeableConcept] = Field(
        description="Indicates the type of matching associated with the dispense",
        default=None,
    )
    performer: Optional[List[BiologicallyDerivedProductDispensePerformer]] = Field(
        description="Indicates who or what performed an action",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where the dispense occurred",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Amount dispensed",
        default=None,
    )
    preparedDate: Optional[DateTime] = Field(
        description="When product was selected/matched",
        default=None,
    )
    preparedDate_ext: Optional[Element] = Field(
        description="Placeholder element for preparedDate extensions",
        default=None,
        alias="_preparedDate",
    )
    whenHandedOver: Optional[DateTime] = Field(
        description="When the product was dispatched",
        default=None,
    )
    whenHandedOver_ext: Optional[Element] = Field(
        description="Placeholder element for whenHandedOver extensions",
        default=None,
        alias="_whenHandedOver",
    )
    destination: Optional[Reference] = Field(
        description="Where the product was dispatched to",
        default=None,
    )
    note: Optional[List[Annotation]] = Field(
        description="Additional notes",
        default=None,
    )
    usageInstruction: Optional[String] = Field(
        description="Specific instructions for use",
        default=None,
    )
    usageInstruction_ext: Optional[Element] = Field(
        description="Placeholder element for usageInstruction extensions",
        default=None,
        alias="_usageInstruction",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "usageInstruction",
                "note",
                "destination",
                "whenHandedOver",
                "preparedDate",
                "quantity",
                "location",
                "performer",
                "matchStatus",
                "patient",
                "product",
                "originRelationshipType",
                "status",
                "partOf",
                "basedOn",
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
