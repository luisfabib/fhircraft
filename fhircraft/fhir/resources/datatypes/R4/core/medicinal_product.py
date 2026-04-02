import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Coding,
    MarketingStatus,
    Reference,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class MedicinalProductNameNamePart(BackboneElement):
    """
    Coding words or phrases of the name.
    """

    part: Optional[String] = Field(
        description="A fragment of a product name",
        default=None,
    )
    type: Optional[Coding] = Field(
        description="Idenifying type for this part of the name (e.g. strength part)",
        default=None,
    )

class MedicinalProductNameCountryLanguage(BackboneElement):
    """
    Country where the name applies.
    """

    country: Optional[CodeableConcept] = Field(
        description="Country code for where this name applies",
        default=None,
    )
    jurisdiction: Optional[CodeableConcept] = Field(
        description="Jurisdiction code for where this name applies",
        default=None,
    )
    language: Optional[CodeableConcept] = Field(
        description="Language code for this name",
        default=None,
    )

class MedicinalProductName(BackboneElement):
    """
    The product's name, including full name and possibly coded parts.
    """

    productName: Optional[String] = Field(
        description="The full product name",
        default=None,
    )
    namePart: Optional[ListType[MedicinalProductNameNamePart]] = Field(
        description="Coding words or phrases of the name",
        default=None,
    )
    countryLanguage: Optional[ListType[MedicinalProductNameCountryLanguage]] = Field(
        description="Country where the name applies",
        default=None,
    )

class MedicinalProductManufacturingBusinessOperation(BackboneElement):
    """
    An operation applied to the product, for manufacturing or adminsitrative purpose.
    """

    operationType: Optional[CodeableConcept] = Field(
        description="The type of manufacturing operation",
        default=None,
    )
    authorisationReferenceNumber: Optional[Identifier] = Field(
        description="Regulatory authorization reference number",
        default=None,
    )
    effectiveDate: Optional[DateTime] = Field(
        description="Regulatory authorization date",
        default=None,
    )
    confidentialityIndicator: Optional[CodeableConcept] = Field(
        description="To indicate if this proces is commercially confidential",
        default=None,
    )
    manufacturer: Optional[ListType[Reference]] = Field(
        description="The manufacturer or establishment associated with the process",
        default=None,
    )
    regulator: Optional[Reference] = Field(
        description="A regulator which oversees the operation",
        default=None,
    )

class MedicinalProductSpecialDesignation(BackboneElement):
    """
    Indicates if the medicinal product has an orphan designation for the treatment of a rare disease.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifier for the designation, or procedure number",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The type of special designation, e.g. orphan drug, minor use",
        default=None,
    )
    intendedUse: Optional[CodeableConcept] = Field(
        description="The intended use of the product, e.g. prevention, treatment",
        default=None,
    )
    indicationCodeableConcept: Optional[CodeableConcept] = Field(
        description="Condition for which the medicinal use applies",
        default=None,
    )
    indicationReference: Optional[Reference] = Field(
        description="Condition for which the medicinal use applies",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="For example granted, pending, expired or withdrawn",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date when the designation was granted",
        default=None,
    )
    species: Optional[CodeableConcept] = Field(
        description="Animal species for which this applies",
        default=None,
    )

    @property
    def indication(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="indication",
        )

    @model_validator(mode="after")
    def indication_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="indication",
            required=False,
        )

class MedicinalProduct(DomainResource):
    """
    Detailed definition of a medicinal product, typically for uses other than direct patient care (e.g. regulatory use).
    """

    _abstract = False
    _type = "MedicinalProduct"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MedicinalProduct"

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
        description="Business identifier for this product. Could be an MPID",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Regulatory type, e.g. Investigational or Authorized",
        default=None,
    )
    domain: Optional[Coding] = Field(
        description="If this medicine applies to human or veterinary uses",
        default=None,
    )
    combinedPharmaceuticalDoseForm: Optional[CodeableConcept] = Field(
        description="The dose form for a single part product, or combined form of a multiple part product",
        default=None,
    )
    legalStatusOfSupply: Optional[CodeableConcept] = Field(
        description="The legal status of supply of the medicinal product as classified by the regulator",
        default=None,
    )
    additionalMonitoringIndicator: Optional[CodeableConcept] = Field(
        description="Whether the Medicinal Product is subject to additional monitoring for regulatory reasons",
        default=None,
    )
    specialMeasures: Optional[ListType[String]] = Field(
        description="Whether the Medicinal Product is subject to special measures for regulatory reasons",
        default=None,
    )
    paediatricUseIndicator: Optional[CodeableConcept] = Field(
        description="If authorised for use in children",
        default=None,
    )
    productClassification: Optional[ListType[CodeableConcept]] = Field(
        description="Allows the product to be classified by various systems",
        default=None,
    )
    marketingStatus: Optional[ListType[MarketingStatus]] = Field(
        description="Marketing status of the medicinal product, in contrast to marketing authorizaton",
        default=None,
    )
    pharmaceuticalProduct: Optional[ListType[Reference]] = Field(
        description="Pharmaceutical aspects of product",
        default=None,
    )
    packagedMedicinalProduct: Optional[ListType[Reference]] = Field(
        description="Package representation for the product",
        default=None,
    )
    attachedDocument: Optional[ListType[Reference]] = Field(
        description="Supporting documentation, typically for regulatory submission",
        default=None,
    )
    masterFile: Optional[ListType[Reference]] = Field(
        description="A master file for to the medicinal product (e.g. Pharmacovigilance System Master File)",
        default=None,
    )
    contact: Optional[ListType[Reference]] = Field(
        description="A product specific contact, person (in a role), or an organization",
        default=None,
    )
    clinicalTrial: Optional[ListType[Reference]] = Field(
        description="Clinical trials or studies that this product is involved in",
        default=None,
    )
    name: Optional[ListType[MedicinalProductName]] = Field(
        description="The product\u0027s name, including full name and possibly coded parts",
        default=None,
    )
    crossReference: Optional[ListType[Identifier]] = Field(
        description="Reference to another product, e.g. for linking authorised to investigational product",
        default=None,
    )
    manufacturingBusinessOperation: Optional[
        ListType[MedicinalProductManufacturingBusinessOperation]
    ] = Field(
        description="An operation applied to the product, for manufacturing or adminsitrative purpose",
        default=None,
    )
    specialDesignation: Optional[ListType[MedicinalProductSpecialDesignation]] = Field(
        description="Indicates if the medicinal product has an orphan designation for the treatment of a rare disease",
        default=None,
    )
