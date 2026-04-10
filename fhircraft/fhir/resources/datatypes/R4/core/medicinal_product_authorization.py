import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class MedicinalProductAuthorizationJurisdictionalAuthorization(BackboneElement):
    """
    Authorization in areas within a country.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="The assigned number for the marketing authorization",
        default=None,
    )
    country: Optional[CodeableConcept] = Field(
        description="Country of authorization",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Jurisdiction within a country",
        default=None,
    )
    legalStatusOfSupply: Optional[CodeableConcept] = Field(
        description="The legal status of supply in a jurisdiction or region",
        default=None,
    )
    validityPeriod: Optional[Period] = Field(
        description="The start and expected end date of the authorization",
        default=None,
    )


class MedicinalProductAuthorizationProcedure(BackboneElement):
    """
    The regulatory procedure for granting or amending a marketing authorization.
    """

    identifier: Optional[Identifier] = Field(
        description="Identifier for this procedure",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of procedure",
        default=None,
    )
    datePeriod: Optional[Period] = Field(
        description="Date of procedure",
        default=None,
    )
    dateDateTime: Optional[fhir.dateTime] = Field(
        description="Date of procedure",
        default=None,
    )
    application: Optional[ListType["MedicinalProductAuthorizationProcedure"]] = Field(
        description="Applcations submitted to obtain a marketing authorization",
        default=None,
    )

    @property
    def date(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="date",
        )

    @model_validator(mode="after")
    def date_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Period, fhir.DateTime],
            field_name_base="date",
            required=False,
        )


class MedicinalProductAuthorization(DomainResource):
    """
    The regulatory authorization of a medicinal product.
    """

    _abstract = False
    _type = "MedicinalProductAuthorization"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/MedicinalProductAuthorization"
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
        description="Business identifier for the marketing authorization, as assigned by a regulator",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="The medicinal product that is being authorized",
        default=None,
    )
    country: Optional[ListType[CodeableConcept]] = Field(
        description="The country in which the marketing authorization has been granted",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Jurisdiction within a country",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="The status of the marketing authorization",
        default=None,
    )
    statusDate: Optional[fhir.dateTime] = Field(
        description="The date at which the given status has become applicable",
        default=None,
    )
    restoreDate: Optional[fhir.dateTime] = Field(
        description="The date when a suspended the marketing or the marketing authorization of the product is anticipated to be restored",
        default=None,
    )
    validityPeriod: Optional[Period] = Field(
        description="The beginning of the time period in which the marketing authorization is in the specific status shall be specified A complete date consisting of day, month and year shall be specified using the ISO 8601 date format",
        default=None,
    )
    dataExclusivityPeriod: Optional[Period] = Field(
        description="A period of time after authorization before generic product applicatiosn can be submitted",
        default=None,
    )
    dateOfFirstAuthorization: Optional[fhir.dateTime] = Field(
        description="The date when the first authorization was granted by a Medicines Regulatory Agency",
        default=None,
    )
    internationalBirthDate: Optional[fhir.dateTime] = Field(
        description="Date of first marketing authorization for a company\u0027s new medicinal product in any country in the World",
        default=None,
    )
    legalBasis: Optional[CodeableConcept] = Field(
        description="The legal framework against which this authorization is granted",
        default=None,
    )
    jurisdictionalAuthorization: Optional[
        ListType[MedicinalProductAuthorizationJurisdictionalAuthorization]
    ] = Field(
        description="Authorization in areas within a country",
        default=None,
    )
    holder: Optional[Reference] = Field(
        description="Marketing Authorization Holder",
        default=None,
    )
    regulator: Optional[Reference] = Field(
        description="Medicines Regulatory Agency",
        default=None,
    )
    procedure: Optional[MedicinalProductAuthorizationProcedure] = Field(
        description="The regulatory procedure for granting or amending a marketing authorization",
        default=None,
    )
