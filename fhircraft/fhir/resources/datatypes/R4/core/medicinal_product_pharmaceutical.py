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
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
    Quantity,
    Duration,
    Ratio,
)
from .resource import Resource
from .domain_resource import DomainResource


class MedicinalProductPharmaceuticalCharacteristics(BackboneElement):
    """
    Characteristics e.g. a products onset of action.
    """

    code: Optional[CodeableConcept] = Field(
        description="A coded characteristic",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="The status of characteristic e.g. assigned or pending",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "status",
                "code",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod(
    BackboneElement
):
    """
    A species specific time during which consumption of animal product is not appropriate.
    """

    tissue: Optional[CodeableConcept] = Field(
        description="Coded expression for the type of tissue for which the withdrawal period applues, e.g. meat, milk",
        default=None,
    )
    value: Optional[Quantity] = Field(
        description="A value for the time",
        default=None,
    )
    supportingInformation: Optional[String] = Field(
        description="Extra information about the withdrawal period",
        default=None,
    )
    supportingInformation_ext: Optional[Element] = Field(
        description="Placeholder element for supportingInformation extensions",
        default=None,
        alias="_supportingInformation",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "supportingInformation",
                "value",
                "tissue",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies(BackboneElement):
    """
    A species for which this route applies.
    """

    code: Optional[CodeableConcept] = Field(
        description="Coded expression for the species",
        default=None,
    )
    withdrawalPeriod: Optional[
        ListType[
            MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod
        ]
    ] = Field(
        description="A species specific time during which consumption of animal product is not appropriate",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "withdrawalPeriod",
                "code",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class MedicinalProductPharmaceuticalRouteOfAdministration(BackboneElement):
    """
    The path by which the pharmaceutical product is taken into or makes contact with the body.
    """

    code: Optional[CodeableConcept] = Field(
        description="Coded expression for the route",
        default=None,
    )
    firstDose: Optional[Quantity] = Field(
        description="The first dose (dose quantity) administered in humans can be specified, for a product under investigation, using a numerical value and its unit of measurement",
        default=None,
    )
    maxSingleDose: Optional[Quantity] = Field(
        description="The maximum single dose that can be administered as per the protocol of a clinical trial can be specified using a numerical value and its unit of measurement",
        default=None,
    )
    maxDosePerDay: Optional[Quantity] = Field(
        description="The maximum dose per day (maximum dose quantity to be administered in any one 24-h period) that can be administered as per the protocol referenced in the clinical trial authorisation",
        default=None,
    )
    maxDosePerTreatmentPeriod: Optional[Ratio] = Field(
        description="The maximum dose per treatment period that can be administered as per the protocol referenced in the clinical trial authorisation",
        default=None,
    )
    maxTreatmentPeriod: Optional[Duration] = Field(
        description="The maximum treatment period during which an Investigational Medicinal Product can be administered as per the protocol referenced in the clinical trial authorisation",
        default=None,
    )
    targetSpecies: Optional[
        ListType[MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies]
    ] = Field(
        description="A species for which this route applies",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "targetSpecies",
                "maxTreatmentPeriod",
                "maxDosePerTreatmentPeriod",
                "maxDosePerDay",
                "maxSingleDose",
                "firstDose",
                "code",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class MedicinalProductPharmaceutical(DomainResource):
    """
    A pharmaceutical product described in terms of its composition and dose form.
    """

    _abstract = False
    _type = "MedicinalProductPharmaceutical"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/MedicinalProductPharmaceutical"
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
                "http://hl7.org/fhir/StructureDefinition/MedicinalProductPharmaceutical"
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
    identifier: Optional[ListType[Identifier]] = Field(
        description="An identifier for the pharmaceutical medicinal product",
        default=None,
    )
    administrableDoseForm: Optional[CodeableConcept] = Field(
        description="The administrable dose form, after necessary reconstitution",
        default=None,
    )
    unitOfPresentation: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    ingredient: Optional[ListType[Reference]] = Field(
        description="Ingredient",
        default=None,
    )
    device: Optional[ListType[Reference]] = Field(
        description="Accompanying device",
        default=None,
    )
    characteristics: Optional[
        ListType[MedicinalProductPharmaceuticalCharacteristics]
    ] = Field(
        description="Characteristics e.g. a products onset of action",
        default=None,
    )
    routeOfAdministration: Optional[
        ListType[MedicinalProductPharmaceuticalRouteOfAdministration]
    ] = Field(
        description="The path by which the pharmaceutical product is taken into or makes contact with the body",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "routeOfAdministration",
                "characteristics",
                "device",
                "ingredient",
                "unitOfPresentation",
                "administrableDoseForm",
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
