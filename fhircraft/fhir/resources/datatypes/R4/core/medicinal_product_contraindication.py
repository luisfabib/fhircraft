import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Reference,
    CodeableConcept,
    Population,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class MedicinalProductContraindicationOtherTherapy(BackboneElement):
    """
    Information about the use of the medicinal product in relation to other therapies described as part of the indication.
    """

    therapyRelationshipType: Optional[CodeableConcept] = Field(
        description="The type of relationship between the medicinal product indication or contraindication and another therapy",
        default=None,
    )
    medicationCodeableConcept: Optional[CodeableConcept] = Field(
        description="Reference to a specific medication (active substance, medicinal product or class of products) as part of an indication or contraindication",
        default=None,
    )
    medicationReference: Optional[Reference] = Field(
        description="Reference to a specific medication (active substance, medicinal product or class of products) as part of an indication or contraindication",
        default=None,
    )

    @property
    def medication(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="medication",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "therapyRelationshipType",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
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


class MedicinalProductContraindication(DomainResource):
    """
    The clinical particulars - indications, contraindications etc. of a medicinal product, including for regulatory purposes.
    """

    _abstract = False
    _type = "MedicinalProductContraindication"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/MedicinalProductContraindication"
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
                "http://hl7.org/fhir/StructureDefinition/MedicinalProductContraindication"
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
    subject: Optional[ListType[Reference]] = Field(
        description="The medication for which this is an indication",
        default=None,
    )
    disease: Optional[CodeableConcept] = Field(
        description="The disease, symptom or procedure for the contraindication",
        default=None,
    )
    diseaseStatus: Optional[CodeableConcept] = Field(
        description="The status of the disease or symptom for the contraindication",
        default=None,
    )
    comorbidity: Optional[ListType[CodeableConcept]] = Field(
        description="A comorbidity (concurrent condition) or coinfection",
        default=None,
    )
    therapeuticIndication: Optional[ListType[Reference]] = Field(
        description="Information about the use of the medicinal product in relation to other therapies as part of the indication",
        default=None,
    )
    otherTherapy: Optional[ListType[MedicinalProductContraindicationOtherTherapy]] = (
        Field(
            description="Information about the use of the medicinal product in relation to other therapies described as part of the indication",
            default=None,
        )
    )
    population: Optional[ListType[Population]] = Field(
        description="The population group to which this applies",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "population",
                "otherTherapy",
                "therapeuticIndication",
                "comorbidity",
                "diseaseStatus",
                "disease",
                "subject",
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
