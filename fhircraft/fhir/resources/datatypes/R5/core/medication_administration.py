from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Boolean,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    CodeableReference,
    Period,
    Timing,
    BackboneElement,
    Annotation,
    Quantity,
    Ratio,
)
from .resource import Resource
from .domain_resource import DomainResource


class MedicationAdministrationPerformer(BackboneElement):
    """
    The performer of the medication treatment.  For devices this is the device that performed the administration of the medication.  An IV Pump would be an example of a device that is performing the administration. Both the IV Pump and the practitioner that set the rate or bolus on the pump can be listed as performers.
    """

    function: Optional[CodeableConcept] = Field(
        description="Type of performance",
        default=None,
    )
    actor: Optional[CodeableReference] = Field(
        description="Who or what performed the medication administration",
        default=None,
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
    def rate_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Ratio, Quantity],
            field_name_base="rate",
            required=False,
        )


class MedicationAdministration(DomainResource):
    """
    Describes the event of a patient consuming or otherwise being administered a medication.  This may be as simple as swallowing a tablet or it may be a long running infusion. Related resources tie this event to the authorizing prescription, and the specific encounter between patient and health care practitioner. This event can also be used to record waste using a status of not-done and the appropriate statusReason.
    """

    _abstract = False
    _type = "MedicationAdministration"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MedicationAdministration"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External identifier",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Plan this is fulfilled by this administration",
        default=None,
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
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Type of medication administration",
        default=None,
    )
    medication: Optional[CodeableReference] = Field(
        description="What was administered",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who received medication",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter administered as part of",
        default=None,
    )
    supportingInformation: Optional[ListType[Reference]] = Field(
        description="Additional information to support administration",
        default=None,
    )
    occurenceDateTime: Optional[DateTime] = Field(
        description="Specific date/time or interval of time during which the administration took place (or did not take place)",
        default=None,
    )
    occurenceDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for occurenceDateTime extensions",
        default=None,
        alias="_occurenceDateTime",
    )
    occurencePeriod: Optional[Period] = Field(
        description="Specific date/time or interval of time during which the administration took place (or did not take place)",
        default=None,
    )
    occurenceTiming: Optional[Timing] = Field(
        description="Specific date/time or interval of time during which the administration took place (or did not take place)",
        default=None,
    )
    recorded: Optional[DateTime] = Field(
        description="When the MedicationAdministration was first captured in the subject\u0027s record",
        default=None,
    )
    recorded_ext: Optional[Element] = Field(
        description="Placeholder element for recorded extensions",
        default=None,
        alias="_recorded",
    )
    isSubPotent: Optional[Boolean] = Field(
        description="Full dose was not administered",
        default=None,
    )
    isSubPotent_ext: Optional[Element] = Field(
        description="Placeholder element for isSubPotent extensions",
        default=None,
        alias="_isSubPotent",
    )
    subPotentReason: Optional[ListType[CodeableConcept]] = Field(
        description="Reason full dose was not administered",
        default=None,
    )
    performer: Optional[ListType[MedicationAdministrationPerformer]] = Field(
        description="Who or what performed the medication administration and what type of performance they did",
        default=None,
    )
    reason: Optional[ListType[CodeableReference]] = Field(
        description="Concept, condition or observation that supports why the medication was administered",
        default=None,
    )
    request: Optional[Reference] = Field(
        description="Request administration performed against",
        default=None,
    )
    device: Optional[ListType[CodeableReference]] = Field(
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
    def occurence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurence",
        )

    @model_validator(mode="after")
    def occurence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period, Timing],
            field_name_base="occurence",
            required=True,
        )

    @model_validator(mode="after")
    def FHIR_mad_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("dosage",),
            expression="(dose.exists() or rate.exists() or text.exists())",
            human="If dosage attribute is present then SHALL have at least one of dosage.text or dosage.dose or dosage.rate[x]",
            key="mad-1",
            severity="error",
        )
