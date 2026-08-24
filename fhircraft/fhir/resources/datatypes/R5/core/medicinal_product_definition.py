from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    MarketingStatus,
    Reference,
    CodeableReference,
    BackboneElement,
    Coding,
    Period,
    Quantity,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource


class MedicinalProductDefinitionContact(BackboneElement):
    """
    A product specific contact, person (in a role), or an organization.
    """

    type: Optional[CodeableConcept] = Field(
        description="Allows the contact to be classified, for example QPPV, Pharmacovigilance Enquiry Information",
        default=None,
    )
    contact: Reference = Field(
        description="A product specific contact, person (in a role), or an organization",
    )


class MedicinalProductDefinitionNamePart(BackboneElement):
    """
    Coding words or phrases of the name.
    """

    part: fhir.string = Field(
        description="A fragment of a product name",
    )
    type: CodeableConcept = Field(
        description="Identifying type for this part of the name (e.g. strength part)",
    )


class MedicinalProductDefinitionNameUsage(BackboneElement):
    """
    Country and jurisdiction where the name applies, and associated language.
    """

    country: CodeableConcept = Field(
        description="Country code for where this name applies",
    )
    jurisdiction: Optional[CodeableConcept] = Field(
        description="Jurisdiction code for where this name applies",
        default=None,
    )
    language: CodeableConcept = Field(
        description="Language code for this name",
    )


class MedicinalProductDefinitionName(BackboneElement):
    """
    The product's name, including full name and possibly coded parts.
    """

    productName: fhir.string = Field(
        description="The full product name",
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of product name, such as rINN, BAN, Proprietary, Non-Proprietary",
        default=None,
    )
    part: Optional[ListType[MedicinalProductDefinitionNamePart]] = Field(
        description="Coding words or phrases of the name",
        default=None,
    )
    usage: Optional[ListType[MedicinalProductDefinitionNameUsage]] = Field(
        description="Country and jurisdiction where the name applies",
        default=None,
    )


class MedicinalProductDefinitionCrossReference(BackboneElement):
    """
    Reference to another product, e.g. for linking authorised to investigational product, or a virtual product.
    """

    product: CodeableReference = Field(
        description="Reference to another product, e.g. for linking authorised to investigational product",
    )
    type: Optional[CodeableConcept] = Field(
        description="The type of relationship, for instance branded to generic or virtual to actual product",
        default=None,
    )


class MedicinalProductDefinitionOperation(BackboneElement):
    """
    A manufacturing or administrative process or step associated with (or performed on) the medicinal product.
    """

    type: Optional[CodeableReference] = Field(
        description="The type of manufacturing operation e.g. manufacturing itself, re-packaging",
        default=None,
    )
    effectiveDate: Optional[Period] = Field(
        description="Date range of applicability",
        default=None,
    )
    organization: Optional[ListType[Reference]] = Field(
        description="The organization responsible for the particular process, e.g. the manufacturer or importer",
        default=None,
    )
    confidentialityIndicator: Optional[CodeableConcept] = Field(
        description="Specifies whether this process is considered proprietary or confidential",
        default=None,
    )


class MedicinalProductDefinitionCharacteristic(BackboneElement):
    """
    Allows the key product features to be recorded, such as "sugar free", "modified release", "parallel import".
    """

    type: CodeableConcept = Field(
        description="A code expressing the type of characteristic",
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueMarkdown: Optional[fhir.markdown] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueDate: Optional[fhir.date_] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="A value for the characteristic",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                CodeableConcept,
                fhir.Markdown,
                Quantity,
                fhir.Integer,
                fhir.Date,
                fhir.Boolean,
                Attachment,
            ],
            field_name_base="value",
            required=False,
        )


class MedicinalProductDefinition(DomainResource):
    """
    Detailed definition of a medicinal product, typically for uses other than direct patient care (e.g. regulatory use, drug catalogs, to support prescribing, adverse events management etc.).
    """

    _abstract = False
    _type = "MedicinalProductDefinition"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/MedicinalProductDefinition"
    )

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for this product. Could be an MPID",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Regulatory type, e.g. Investigational or Authorized",
        default=None,
    )
    domain: Optional[CodeableConcept] = Field(
        description="If this medicine applies to human or veterinary uses",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="A business identifier relating to a specific version of the product",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="The status within the lifecycle of this product record",
        default=None,
    )
    statusDate: Optional[fhir.dateTime] = Field(
        description="The date at which the given status became applicable",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="General description of this product",
        default=None,
    )
    combinedPharmaceuticalDoseForm: Optional[CodeableConcept] = Field(
        description="The dose form for a single part product, or combined form of a multiple part product",
        default=None,
    )
    route: Optional[ListType[CodeableConcept]] = Field(
        description="The path by which the product is taken into or makes contact with the body",
        default=None,
    )
    indication: Optional[fhir.markdown] = Field(
        description="Description of indication(s) for this product, used when structured indications are not required",
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
    specialMeasures: Optional[ListType[CodeableConcept]] = Field(
        description="Whether the Medicinal Product is subject to special measures for regulatory reasons",
        default=None,
    )
    pediatricUseIndicator: Optional[CodeableConcept] = Field(
        description="If authorised for use in children",
        default=None,
    )
    classification: Optional[ListType[CodeableConcept]] = Field(
        description="Allows the product to be classified by various systems",
        default=None,
    )
    marketingStatus: Optional[ListType[MarketingStatus]] = Field(
        description="Marketing status of the medicinal product, in contrast to marketing authorization",
        default=None,
    )
    packagedMedicinalProduct: Optional[ListType[CodeableConcept]] = Field(
        description="Package type for the product",
        default=None,
    )
    comprisedOf: Optional[ListType[Reference]] = Field(
        description="Types of medicinal manufactured items and/or devices that this product consists of, such as tablets, capsule, or syringes",
        default=None,
    )
    ingredient: Optional[ListType[CodeableConcept]] = Field(
        description="The ingredients of this medicinal product - when not detailed in other resources",
        default=None,
    )
    impurity: Optional[ListType[CodeableReference]] = Field(
        description="Any component of the drug product which is not the chemical entity defined as the drug substance, or an excipient in the drug product",
        default=None,
    )
    attachedDocument: Optional[ListType[Reference]] = Field(
        description="Additional documentation about the medicinal product",
        default=None,
    )
    masterFile: Optional[ListType[Reference]] = Field(
        description="A master file for the medicinal product (e.g. Pharmacovigilance System Master File)",
        default=None,
    )
    contact: Optional[ListType[MedicinalProductDefinitionContact]] = Field(
        description="A product specific contact, person (in a role), or an organization",
        default=None,
    )
    clinicalTrial: Optional[ListType[Reference]] = Field(
        description="Clinical trials or studies that this product is involved in",
        default=None,
    )
    code: Optional[ListType[Coding]] = Field(
        description="A code that this product is known by, within some formal terminology",
        default=None,
    )
    name: ListType[MedicinalProductDefinitionName] = Field(
        description="The product\u0027s name, including full name and possibly coded parts",
    )
    crossReference: Optional[ListType[MedicinalProductDefinitionCrossReference]] = (
        Field(
            description="Reference to another product, e.g. for linking authorised to investigational product",
            default=None,
        )
    )
    operation: Optional[ListType[MedicinalProductDefinitionOperation]] = Field(
        description="A manufacturing or administrative process for the medicinal product",
        default=None,
    )
    characteristic: Optional[ListType[MedicinalProductDefinitionCharacteristic]] = (
        Field(
            description='Key product features such as "sugar free", "modified release"',
            default=None,
        )
    )
