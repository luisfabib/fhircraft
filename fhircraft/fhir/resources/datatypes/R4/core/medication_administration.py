import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, DateTime

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    Ratio,
    BackboneElement,
    Annotation,
    Quantity,
)
from .resource import Resource
from .domain_resource import DomainResource


class MedicationAdministrationPerformer(BackboneElement):
    """
    Indicates who or what performed the medication administration and how they were involved.
    """

    function: Optional[CodeableConcept] = Field(
        description="Type of performance",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Who performed the medication administration",
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


class MedicationAdministrationDosage(BackboneElement):
    """
    Describes the medication dosage information details e.g. dose, rate, site, route, etc.
    """

    text: Optional[String] = Field(
        description="Free text dosage instructions e.g. SIG",
        default=None,
    )
    text_ext: Optional[Element] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
    site: Optional[CodeableConcept] = Field(
        description="Body site administered to",
        default=None,
    )
    route: Optional[CodeableConcept] = Field(
        description="Path of substance into body",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="How drug was administered",
        default=None,
    )
    dose: Optional[Quantity] = Field(
        description="Amount of medication per dose",
        default=None,
    )
    rateRatio: Optional[Ratio] = Field(
        description="Dose quantity per unit of time",
        default=None,
    )
    rateQuantity: Optional[Quantity] = Field(
        description="Dose quantity per unit of time",
        default=None,
    )

    @property
    def rate(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="rate",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "dose",
                "method",
                "route",
                "site",
                "text",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def rate_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Ratio, Quantity],
            field_name_base="rate",
            required=False,
        )


class MedicationAdministration(DomainResource):
    """
    Describes the event of a patient consuming or otherwise being administered a medication.  This may be as simple as swallowing a tablet or it may be a long running infusion.  Related resources tie this event to the authorizing prescription, and the specific encounter between patient and health care practitioner.
    """

    _abstract = False
    _type = "MedicationAdministration"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MedicationAdministration"

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
            profile=["http://hl7.org/fhir/StructureDefinition/MedicationAdministration"]
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
    identifier: Optional[ListType[Identifier]] = Field(
        description="External identifier",
        default=None,
    )
    instantiates: Optional[ListType[Uri]] = Field(
        description="Instantiates protocol or definition",
        default=None,
    )
    instantiates_ext: Optional[Element] = Field(
        description="Placeholder element for instantiates extensions",
        default=None,
        alias="_instantiates",
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced event",
        default=None,
    )
    status: Optional[Code] = Field(
        description="in-progress | not-done | on-hold | completed | entered-in-error | stopped | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    statusReason: Optional[ListType[CodeableConcept]] = Field(
        description="Reason administration not performed",
        default=None,
    )
    category: Optional[CodeableConcept] = Field(
        description="Type of medication usage",
        default=None,
    )
    medicationCodeableConcept: Optional[CodeableConcept] = Field(
        description="What was administered",
        default=None,
    )
    medicationReference: Optional[Reference] = Field(
        description="What was administered",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who received medication",
        default=None,
    )
    context: Optional[Reference] = Field(
        description="Encounter or Episode of Care administered as part of",
        default=None,
    )
    supportingInformation: Optional[ListType[Reference]] = Field(
        description="Additional information to support administration",
        default=None,
    )
    effectiveDateTime: Optional[DateTime] = Field(
        description="Start and end time of administration",
        default=None,
    )
    effectiveDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for effectiveDateTime extensions",
        default=None,
        alias="_effectiveDateTime",
    )
    effectivePeriod: Optional[Period] = Field(
        description="Start and end time of administration",
        default=None,
    )
    performer: Optional[ListType[MedicationAdministrationPerformer]] = Field(
        description="Who performed the medication administration and what they did",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Reason administration performed",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Condition or observation that supports why the medication was administered",
        default=None,
    )
    request: Optional[Reference] = Field(
        description="Request administration performed against",
        default=None,
    )
    device: Optional[ListType[Reference]] = Field(
        description="Device used to administer",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Information about the administration",
        default=None,
    )
    dosage: Optional[MedicationAdministrationDosage] = Field(
        description="Details of how medication was taken",
        default=None,
    )
    eventHistory: Optional[ListType[Reference]] = Field(
        description="A list of events of interest in the lifecycle",
        default=None,
    )

    @property
    def medication(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="medication",
        )

    @property
    def effective(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="effective",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "eventHistory",
                "dosage",
                "note",
                "device",
                "request",
                "reasonReference",
                "reasonCode",
                "performer",
                "supportingInformation",
                "context",
                "subject",
                "category",
                "statusReason",
                "status",
                "partOf",
                "instantiates",
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
    def FHIR_mad_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("dosage",),
            expression="dose.exists() or rate.exists()",
            human="SHALL have at least one of dosage.dose or dosage.rate[x]",
            key="mad-1",
            severity="error",
        )

    @model_validator(mode="after")
    def medication_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="medication",
            required=True,
        )

    @model_validator(mode="after")
    def effective_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period],
            field_name_base="effective",
            required=True,
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
            expression="contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url))) or descendants().where(reference = '#').exists() or descendants().where(as(canonical) = '#').exists() or descendants().where(as(canonical) = '#').exists()).not()).trace('unmatched', id).empty()",
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
