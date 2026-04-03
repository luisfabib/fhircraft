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
    CodeableConcept,
    Reference,
    ContactDetail,
    UsageContext,
    Period,
    BackboneElement,
    Quantity,
    Duration,
    Range,
)
from .resource import Resource
from .domain_resource import DomainResource

class SpecimenDefinitionTypeTestedContainerAdditive(BackboneElement):
    """
    Substance introduced in the kind of container to preserve, maintain or enhance the specimen. Examples: Formalin, Citrate, EDTA.
    """

    additiveCodeableConcept: Optional[CodeableConcept] = Field(
        description="Additive associated with container",
        default=None,
    )
    additiveReference: Optional[Reference] = Field(
        description="Additive associated with container",
        default=None,
    )

    @property
    def additive(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="additive",
        )

    @model_validator(mode="after")
    def additive_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="additive",
            required=True,
        )

class SpecimenDefinitionTypeTestedContainer(BackboneElement):
    """
    The specimen's container.
    """

    material: Optional[CodeableConcept] = Field(
        description="The material type used for the container",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Kind of container associated with the kind of specimen",
        default=None,
    )
    cap: Optional[CodeableConcept] = Field(
        description="Color of container cap",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="The description of the kind of container",
        default=None,
    )
    capacity: Optional[Quantity] = Field(
        description="The capacity of this kind of container",
        default=None,
    )
    minimumVolumeQuantity: Optional[Quantity] = Field(
        description="Minimum volume",
        default=None,
    )
    minimumVolumeString: Optional[String] = Field(
        description="Minimum volume",
        default=None,
    )
    additive: Optional[ListType[SpecimenDefinitionTypeTestedContainerAdditive]] = Field(
        description="Additive associated with container",
        default=None,
    )
    preparation: Optional[Markdown] = Field(
        description="Special processing applied to the container for this specimen type",
        default=None,
    )

    @property
    def minimumVolume(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="minimumVolume",
        )

    @model_validator(mode="after")
    def minimumVolume_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, String],
            field_name_base="minimumVolume",
            required=False,
        )

class SpecimenDefinitionTypeTestedHandling(BackboneElement):
    """
    Set of instructions for preservation/transport of the specimen at a defined temperature interval, prior the testing process.
    """

    temperatureQualifier: Optional[CodeableConcept] = Field(
        description="Qualifies the interval of temperature",
        default=None,
    )
    temperatureRange: Optional[Range] = Field(
        description="Temperature range for these handling instructions",
        default=None,
    )
    maxDuration: Optional[Duration] = Field(
        description="Maximum preservation time",
        default=None,
    )
    instruction: Optional[Markdown] = Field(
        description="Preservation instruction",
        default=None,
    )

class SpecimenDefinitionTypeTested(BackboneElement):
    """
    Specimen conditioned in a container as expected by the testing laboratory.
    """

    isDerived: Optional[Boolean] = Field(
        description="Primary or secondary specimen",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of intended specimen",
        default=None,
    )
    preference: Optional[Code] = Field(
        description="preferred | alternate",
        default=None,
    )
    container: Optional[SpecimenDefinitionTypeTestedContainer] = Field(
        description="The specimen\u0027s container",
        default=None,
    )
    requirement: Optional[Markdown] = Field(
        description="Requirements for specimen delivery and special handling",
        default=None,
    )
    retentionTime: Optional[Duration] = Field(
        description="The usual time for retaining this kind of specimen",
        default=None,
    )
    singleUse: Optional[Boolean] = Field(
        description="Specimen for single use only",
        default=None,
    )
    rejectionCriterion: Optional[ListType[CodeableConcept]] = Field(
        description="Criterion specified for specimen rejection",
        default=None,
    )
    handling: Optional[ListType[SpecimenDefinitionTypeTestedHandling]] = Field(
        description="Specimen handling before testing",
        default=None,
    )
    testingDestination: Optional[ListType[CodeableConcept]] = Field(
        description="Where the specimen will be tested",
        default=None,
    )

class SpecimenDefinition(DomainResource):
    """
    A kind of specimen with associated set of requirements.
    """

    _abstract = False
    _type = "SpecimenDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SpecimenDefinition"

    url: Optional[Uri] = Field(
        description="Logical canonical URL to reference this SpecimenDefinition (globally unique)",
        default=None,
    )
    identifier: Optional[Identifier] = Field(
        description="Business identifier",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the SpecimenDefinition",
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
        description="Name for this {{title}} (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this SpecimenDefinition (Human friendly)",
        default=None,
    )
    derivedFromCanonical: Optional[ListType[Canonical]] = Field(
        description="Based on FHIR definition of another SpecimenDefinition",
        default=None,
    )
    derivedFromUri: Optional[ListType[Uri]] = Field(
        description="Based on external definition",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[Boolean] = Field(
        description="If this SpecimenDefinition is not for real usage",
        default=None,
    )
    subjectCodeableConcept: Optional[CodeableConcept] = Field(
        description="Type of subject for specimen collection",
        default=None,
    )
    subjectReference: Optional[Reference] = Field(
        description="Type of subject for specimen collection",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date status first applied",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="The name of the individual or organization that published the SpecimenDefinition",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Natural language description of the SpecimenDefinition",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="Content intends to support these contexts",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for this SpecimenDefinition (if applicable)",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this SpecimenDefinition is defined",
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
    approvalDate: Optional[Date] = Field(
        description="When SpecimenDefinition was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[Date] = Field(
        description="The date on which the asset content was last reviewed by the publisher",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="The effective date range for the SpecimenDefinition",
        default=None,
    )
    typeCollected: Optional[CodeableConcept] = Field(
        description="Kind of material to collect",
        default=None,
    )
    patientPreparation: Optional[ListType[CodeableConcept]] = Field(
        description="Patient preparation for collection",
        default=None,
    )
    timeAspect: Optional[String] = Field(
        description="Time aspect for collection",
        default=None,
    )
    collection: Optional[ListType[CodeableConcept]] = Field(
        description="Specimen collection procedure",
        default=None,
    )
    typeTested: Optional[ListType[SpecimenDefinitionTypeTested]] = Field(
        description="Specimen in container intended for testing by lab",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @property
    def subject(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="subject",
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
    def subject_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="subject",
            required=False,
        )
