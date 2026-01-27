from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Canonical,
    Boolean,
    DateTime,
    Markdown,
    Date,
)

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
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
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
    minimumVolumeString_ext: Optional[Element] = Field(
        description="Placeholder element for minimumVolumeString extensions",
        default=None,
        alias="_minimumVolumeString",
    )
    additive: Optional[List[SpecimenDefinitionTypeTestedContainerAdditive]] = Field(
        description="Additive associated with container",
        default=None,
    )
    preparation: Optional[Markdown] = Field(
        description="Special processing applied to the container for this specimen type",
        default=None,
    )
    preparation_ext: Optional[Element] = Field(
        description="Placeholder element for preparation extensions",
        default=None,
        alias="_preparation",
    )

    @property
    def minimumVolume(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="minimumVolume",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "preparation",
                "additive",
                "capacity",
                "description",
                "cap",
                "type",
                "material",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
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
    instruction_ext: Optional[Element] = Field(
        description="Placeholder element for instruction extensions",
        default=None,
        alias="_instruction",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "instruction",
                "maxDuration",
                "temperatureRange",
                "temperatureQualifier",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class SpecimenDefinitionTypeTested(BackboneElement):
    """
    Specimen conditioned in a container as expected by the testing laboratory.
    """

    isDerived: Optional[Boolean] = Field(
        description="Primary or secondary specimen",
        default=None,
    )
    isDerived_ext: Optional[Element] = Field(
        description="Placeholder element for isDerived extensions",
        default=None,
        alias="_isDerived",
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of intended specimen",
        default=None,
    )
    preference: Optional[Code] = Field(
        description="preferred | alternate",
        default=None,
    )
    preference_ext: Optional[Element] = Field(
        description="Placeholder element for preference extensions",
        default=None,
        alias="_preference",
    )
    container: Optional[SpecimenDefinitionTypeTestedContainer] = Field(
        description="The specimen\u0027s container",
        default=None,
    )
    requirement: Optional[Markdown] = Field(
        description="Requirements for specimen delivery and special handling",
        default=None,
    )
    requirement_ext: Optional[Element] = Field(
        description="Placeholder element for requirement extensions",
        default=None,
        alias="_requirement",
    )
    retentionTime: Optional[Duration] = Field(
        description="The usual time for retaining this kind of specimen",
        default=None,
    )
    singleUse: Optional[Boolean] = Field(
        description="Specimen for single use only",
        default=None,
    )
    singleUse_ext: Optional[Element] = Field(
        description="Placeholder element for singleUse extensions",
        default=None,
        alias="_singleUse",
    )
    rejectionCriterion: Optional[List[CodeableConcept]] = Field(
        description="Criterion specified for specimen rejection",
        default=None,
    )
    handling: Optional[List[SpecimenDefinitionTypeTestedHandling]] = Field(
        description="Specimen handling before testing",
        default=None,
    )
    testingDestination: Optional[List[CodeableConcept]] = Field(
        description="Where the specimen will be tested",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "testingDestination",
                "handling",
                "rejectionCriterion",
                "singleUse",
                "retentionTime",
                "requirement",
                "container",
                "preference",
                "type",
                "isDerived",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class SpecimenDefinition(DomainResource):
    """
    A kind of specimen with associated set of requirements.
    """

    _abstract = False
    _type = "SpecimenDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SpecimenDefinition"

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
            profile=["http://hl7.org/fhir/StructureDefinition/SpecimenDefinition"]
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
    url: Optional[Uri] = Field(
        description="Logical canonical URL to reference this SpecimenDefinition (globally unique)",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    identifier: Optional[Identifier] = Field(
        description="Business identifier",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the SpecimenDefinition",
        default=None,
    )
    version_ext: Optional[Element] = Field(
        description="Placeholder element for version extensions",
        default=None,
        alias="_version",
    )
    versionAlgorithmString: Optional[String] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmString_ext: Optional[Element] = Field(
        description="Placeholder element for versionAlgorithmString extensions",
        default=None,
        alias="_versionAlgorithmString",
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this {{title}} (computer friendly)",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    title: Optional[String] = Field(
        description="Name for this SpecimenDefinition (Human friendly)",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    derivedFromCanonical: Optional[List[Canonical]] = Field(
        description="Based on FHIR definition of another SpecimenDefinition",
        default=None,
    )
    derivedFromCanonical_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for derivedFromCanonical extensions",
        default=None,
        alias="_derivedFromCanonical",
    )
    derivedFromUri: Optional[List[Uri]] = Field(
        description="Based on external definition",
        default=None,
    )
    derivedFromUri_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for derivedFromUri extensions",
        default=None,
        alias="_derivedFromUri",
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
        description="If this SpecimenDefinition is not for real usage",
        default=None,
    )
    experimental_ext: Optional[Element] = Field(
        description="Placeholder element for experimental extensions",
        default=None,
        alias="_experimental",
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
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    publisher: Optional[String] = Field(
        description="The name of the individual or organization that published the SpecimenDefinition",
        default=None,
    )
    publisher_ext: Optional[Element] = Field(
        description="Placeholder element for publisher extensions",
        default=None,
        alias="_publisher",
    )
    contact: Optional[List[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Natural language description of the SpecimenDefinition",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    useContext: Optional[List[UsageContext]] = Field(
        description="Content intends to support these contexts",
        default=None,
    )
    jurisdiction: Optional[List[CodeableConcept]] = Field(
        description="Intended jurisdiction for this SpecimenDefinition (if applicable)",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this SpecimenDefinition is defined",
        default=None,
    )
    purpose_ext: Optional[Element] = Field(
        description="Placeholder element for purpose extensions",
        default=None,
        alias="_purpose",
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
    copyrightLabel: Optional[String] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    copyrightLabel_ext: Optional[Element] = Field(
        description="Placeholder element for copyrightLabel extensions",
        default=None,
        alias="_copyrightLabel",
    )
    approvalDate: Optional[Date] = Field(
        description="When SpecimenDefinition was approved by publisher",
        default=None,
    )
    approvalDate_ext: Optional[Element] = Field(
        description="Placeholder element for approvalDate extensions",
        default=None,
        alias="_approvalDate",
    )
    lastReviewDate: Optional[Date] = Field(
        description="The date on which the asset content was last reviewed by the publisher",
        default=None,
    )
    lastReviewDate_ext: Optional[Element] = Field(
        description="Placeholder element for lastReviewDate extensions",
        default=None,
        alias="_lastReviewDate",
    )
    effectivePeriod: Optional[Period] = Field(
        description="The effective date range for the SpecimenDefinition",
        default=None,
    )
    typeCollected: Optional[CodeableConcept] = Field(
        description="Kind of material to collect",
        default=None,
    )
    patientPreparation: Optional[List[CodeableConcept]] = Field(
        description="Patient preparation for collection",
        default=None,
    )
    timeAspect: Optional[String] = Field(
        description="Time aspect for collection",
        default=None,
    )
    timeAspect_ext: Optional[Element] = Field(
        description="Placeholder element for timeAspect extensions",
        default=None,
        alias="_timeAspect",
    )
    collection: Optional[List[CodeableConcept]] = Field(
        description="Specimen collection procedure",
        default=None,
    )
    typeTested: Optional[List[SpecimenDefinitionTypeTested]] = Field(
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
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "typeTested",
                "collection",
                "timeAspect",
                "patientPreparation",
                "typeCollected",
                "effectivePeriod",
                "lastReviewDate",
                "approvalDate",
                "copyrightLabel",
                "copyright",
                "purpose",
                "jurisdiction",
                "useContext",
                "description",
                "contact",
                "publisher",
                "date",
                "experimental",
                "status",
                "derivedFromUri",
                "derivedFromCanonical",
                "title",
                "name",
                "version",
                "identifier",
                "url",
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
