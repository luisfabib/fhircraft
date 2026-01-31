import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Markdown,
    DateTime,
)

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    CodeableReference,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class RegulatedAuthorizationCase(BackboneElement):
    """
    The case or regulatory procedure for granting or amending a regulated authorization. An authorization is granted in response to submissions/applications by those seeking authorization. A case is the administrative process that deals with the application(s) that relate to this and assesses them. Note: This area is subject to ongoing review and the workgroup is seeking implementer feedback on its use (see link at bottom of page).
    """

    identifier: Optional[Identifier] = Field(
        description="Identifier by which this case can be referenced",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The defining type of case",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="The status associated with the case",
        default=None,
    )
    datePeriod: Optional[Period] = Field(
        description="Relevant date for this case",
        default=None,
    )
    dateDateTime: Optional[DateTime] = Field(
        description="Relevant date for this case",
        default=None,
    )
    dateDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for dateDateTime extensions",
        default=None,
        alias="_dateDateTime",
    )
    application: Optional[ListType["RegulatedAuthorizationCase"]] = Field(
        description="Applications submitted to obtain a regulated authorization. Steps within the longer running case or procedure",
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
            field_types=[Period, DateTime],
            field_name_base="date",
            required=False,
        )

class RegulatedAuthorization(DomainResource):
    """
    Regulatory approval, clearance or licencing related to a regulated product, treatment, facility or activity that is cited in a guidance, regulation, rule or legislative act. An example is Market Authorization relating to a Medicinal Product.
    """

    _abstract = False
    _type = "RegulatedAuthorization"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/RegulatedAuthorization"

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
        description="Business identifier for the authorization, typically assigned by the authorizing body",
        default=None,
    )
    subject: Optional[ListType[Reference]] = Field(
        description="The product type, treatment, facility or activity that is being authorized",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Overall type of this authorization, for example drug marketing approval, orphan drug designation",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="General textual supporting information",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    region: Optional[ListType[CodeableConcept]] = Field(
        description="The territory in which the authorization has been granted",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="The status that is authorised e.g. approved. Intermediate states can be tracked with cases and applications",
        default=None,
    )
    statusDate: Optional[DateTime] = Field(
        description="The date at which the current status was assigned",
        default=None,
    )
    statusDate_ext: Optional[Element] = Field(
        description="Placeholder element for statusDate extensions",
        default=None,
        alias="_statusDate",
    )
    validityPeriod: Optional[Period] = Field(
        description="The time period in which the regulatory approval etc. is in effect, e.g. a Marketing Authorization includes the date of authorization and/or expiration date",
        default=None,
    )
    indication: Optional[CodeableReference] = Field(
        description="Condition for which the use of the regulated product applies",
        default=None,
    )
    intendedUse: Optional[CodeableConcept] = Field(
        description="The intended use of the product, e.g. prevention, treatment",
        default=None,
    )
    basis: Optional[ListType[CodeableConcept]] = Field(
        description="The legal/regulatory framework or reasons under which this authorization is granted",
        default=None,
    )
    holder: Optional[Reference] = Field(
        description="The organization that has been granted this authorization, by the regulator",
        default=None,
    )
    regulator: Optional[Reference] = Field(
        description="The regulatory authority or authorizing body granting the authorization",
        default=None,
    )
    case: Optional[RegulatedAuthorizationCase] = Field(
        description="The case or regulatory procedure for granting or amending a regulated authorization. Note: This area is subject to ongoing review and the workgroup is seeking implementer feedback on its use (see link at bottom of page)",
        default=None,
    )

