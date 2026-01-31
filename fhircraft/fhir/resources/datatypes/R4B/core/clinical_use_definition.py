import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, Markdown

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
    CodeableReference,
    Range,
)
from .resource import Resource
from .domain_resource import DomainResource


class ClinicalUseDefinitionContraindicationOtherTherapy(BackboneElement):
    """
    Information about the use of the medicinal product in relation to other therapies described as part of the contraindication.
    """

    relationshipType: Optional[CodeableConcept] = Field(
        description="The type of relationship between the product indication/contraindication and another therapy",
        default=None,
    )
    therapy: Optional[CodeableReference] = Field(
        description="Reference to a specific medication as part of an indication or contraindication",
        default=None,
    )


class ClinicalUseDefinitionContraindication(BackboneElement):
    """
    Specifics for when this is a contraindication.
    """

    diseaseSymptomProcedure: Optional[CodeableReference] = Field(
        description="The situation that is being documented as contraindicating against this item",
        default=None,
    )
    diseaseStatus: Optional[CodeableReference] = Field(
        description="The status of the disease or symptom for the contraindication",
        default=None,
    )
    comorbidity: Optional[ListType[CodeableReference]] = Field(
        description="A comorbidity (concurrent condition) or coinfection",
        default=None,
    )
    indication: Optional[ListType[Reference]] = Field(
        description="The indication which this is a contraidication for",
        default=None,
    )
    otherTherapy: Optional[
        ListType[ClinicalUseDefinitionContraindicationOtherTherapy]
    ] = Field(
        description="Information about use of the product in relation to other therapies described as part of the contraindication",
        default=None,
    )


class ClinicalUseDefinitionIndicationOtherTherapy(BackboneElement):
    """
    Information about the use of the medicinal product in relation to other therapies described as part of the indication.
    """

    relationshipType: Optional[CodeableConcept] = Field(
        description="The type of relationship between the product indication/contraindication and another therapy",
        default=None,
    )
    therapy: Optional[CodeableReference] = Field(
        description="Reference to a specific medication as part of an indication or contraindication",
        default=None,
    )


class ClinicalUseDefinitionIndication(BackboneElement):
    """
    Specifics for when this is an indication.
    """

    diseaseSymptomProcedure: Optional[CodeableReference] = Field(
        description="The situation that is being documented as an indicaton for this item",
        default=None,
    )
    diseaseStatus: Optional[CodeableReference] = Field(
        description="The status of the disease or symptom for the indication",
        default=None,
    )
    comorbidity: Optional[ListType[CodeableReference]] = Field(
        description="A comorbidity or coinfection as part of the indication",
        default=None,
    )
    intendedEffect: Optional[CodeableReference] = Field(
        description="The intended effect, aim or strategy to be achieved",
        default=None,
    )
    durationRange: Optional[Range] = Field(
        description="Timing or duration information",
        default=None,
    )
    durationString: Optional[String] = Field(
        description="Timing or duration information",
        default=None,
    )
    durationString_ext: Optional[Element] = Field(
        description="Placeholder element for durationString extensions",
        default=None,
        alias="_durationString",
    )
    undesirableEffect: Optional[ListType[Reference]] = Field(
        description="An unwanted side effect or negative outcome of the subject of this resource when being used for this indication",
        default=None,
    )
    otherTherapy: Optional[ListType[ClinicalUseDefinitionIndicationOtherTherapy]] = (
        Field(
            description="The use of the medicinal product in relation to other therapies described as part of the indication",
            default=None,
        )
    )

    @property
    def duration(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="duration",
        )

    @model_validator(mode="after")
    def duration_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Range, String],
            field_name_base="duration",
            required=False,
        )


class ClinicalUseDefinitionInteractionInteractant(BackboneElement):
    """
    The specific medication, food, substance or laboratory test that interacts.
    """

    itemReference: Optional[Reference] = Field(
        description="The specific medication, food or laboratory test that interacts",
        default=None,
    )
    itemCodeableConcept: Optional[CodeableConcept] = Field(
        description="The specific medication, food or laboratory test that interacts",
        default=None,
    )

    @property
    def item(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="item",
        )

    @model_validator(mode="after")
    def item_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="item",
            required=True,
        )


class ClinicalUseDefinitionInteraction(BackboneElement):
    """
    Specifics for when this is an interaction.
    """

    interactant: Optional[ListType[ClinicalUseDefinitionInteractionInteractant]] = (
        Field(
            description="The specific medication, food, substance or laboratory test that interacts",
            default=None,
        )
    )
    type: Optional[CodeableConcept] = Field(
        description="The type of the interaction e.g. drug-drug interaction, drug-lab test interaction",
        default=None,
    )
    effect: Optional[CodeableReference] = Field(
        description='The effect of the interaction, for example "reduced gastric absorption of primary medication"',
        default=None,
    )
    incidence: Optional[CodeableConcept] = Field(
        description="The incidence of the interaction, e.g. theoretical, observed",
        default=None,
    )
    management: Optional[ListType[CodeableConcept]] = Field(
        description="Actions for managing the interaction",
        default=None,
    )


class ClinicalUseDefinitionUndesirableEffect(BackboneElement):
    """
    Describe the possible undesirable effects (negative outcomes) from the use of the medicinal product as treatment.
    """

    symptomConditionEffect: Optional[CodeableReference] = Field(
        description="The situation in which the undesirable effect may manifest",
        default=None,
    )
    classification: Optional[CodeableConcept] = Field(
        description="High level classification of the effect",
        default=None,
    )
    frequencyOfOccurrence: Optional[CodeableConcept] = Field(
        description="How often the effect is seen",
        default=None,
    )


class ClinicalUseDefinitionWarning(BackboneElement):
    """
    A critical piece of information about environmental, health or physical risks or hazards that serve as caution to the user. For example 'Do not operate heavy machinery', 'May cause drowsiness', or 'Get medical advice/attention if you feel unwell'.
    """

    description: Optional[Markdown] = Field(
        description="A textual definition of this warning, with formatting",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    code: Optional[CodeableConcept] = Field(
        description="A coded or unformatted textual definition of this warning",
        default=None,
    )


class ClinicalUseDefinition(DomainResource):
    """
    A single issue - either an indication, contraindication, interaction or an undesirable effect for a medicinal product, medication, device or procedure.
    """

    _abstract = False
    _type = "ClinicalUseDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ClinicalUseDefinition"

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
        description="Business identifier for this issue",
        default=None,
    )
    type: Optional[Code] = Field(
        description="indication | contraindication | interaction | undesirable-effect | warning",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description='A categorisation of the issue, primarily for dividing warnings into subject heading areas such as "Pregnancy", "Overdose"',
        default=None,
    )
    subject: Optional[ListType[Reference]] = Field(
        description="The medication or procedure for which this is an indication",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="Whether this is a current issue or one that has been retired etc",
        default=None,
    )
    contraindication: Optional[ClinicalUseDefinitionContraindication] = Field(
        description="Specifics for when this is a contraindication",
        default=None,
    )
    indication: Optional[ClinicalUseDefinitionIndication] = Field(
        description="Specifics for when this is an indication",
        default=None,
    )
    interaction: Optional[ClinicalUseDefinitionInteraction] = Field(
        description="Specifics for when this is an interaction",
        default=None,
    )
    population: Optional[ListType[Reference]] = Field(
        description="The population group to which this applies",
        default=None,
    )
    undesirableEffect: Optional[ClinicalUseDefinitionUndesirableEffect] = Field(
        description="A possible negative outcome from the use of this treatment",
        default=None,
    )
    warning: Optional[ClinicalUseDefinitionWarning] = Field(
        description="Critical environmental, health or physical risks or hazards. For example \u0027Do not operate heavy machinery\u0027, \u0027May cause drowsiness\u0027",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_cud_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(ClinicalUseDefinition.indication.count() + ClinicalUseDefinition.contraindication.count() + ClinicalUseDefinition.interaction.count() + ClinicalUseDefinition.undesirableEffect.count() + ClinicalUseDefinition.warning.count())  < 2",
            human="Indication, Contraindication, Interaction, UndesirableEffect and Warning cannot be used in the same instance",
            key="cud-1",
            severity="error",
        )
