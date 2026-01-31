import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Boolean,
    Decimal,
    Integer,
)

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    CodeableConcept,
    Identifier,
    BackboneElement,
    Range,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class ObservationDefinitionQuantitativeDetails(BackboneElement):
    """
    Characteristics for quantitative results of this observation.
    """

    customaryUnit: Optional[CodeableConcept] = Field(
        description="Customary unit for quantitative results",
        default=None,
    )
    unit: Optional[CodeableConcept] = Field(
        description="SI unit for quantitative results",
        default=None,
    )
    conversionFactor: Optional[Decimal] = Field(
        description="SI to Customary unit conversion factor",
        default=None,
    )
    conversionFactor_ext: Optional[Element] = Field(
        description="Placeholder element for conversionFactor extensions",
        default=None,
        alias="_conversionFactor",
    )
    decimalPrecision: Optional[Integer] = Field(
        description="Decimal precision of observation quantitative results",
        default=None,
    )
    decimalPrecision_ext: Optional[Element] = Field(
        description="Placeholder element for decimalPrecision extensions",
        default=None,
        alias="_decimalPrecision",
    )


class ObservationDefinitionQualifiedInterval(BackboneElement):
    """
    Multiple  ranges of results qualified by different contexts for ordinal or continuous observations conforming to this ObservationDefinition.
    """

    category: Optional[Code] = Field(
        description="reference | critical | absolute",
        default=None,
    )
    category_ext: Optional[Element] = Field(
        description="Placeholder element for category extensions",
        default=None,
        alias="_category",
    )
    range: Optional[Range] = Field(
        description="The interval itself, for continuous or ordinal observations",
        default=None,
    )
    context: Optional[CodeableConcept] = Field(
        description="Range context qualifier",
        default=None,
    )
    appliesTo: Optional[ListType[CodeableConcept]] = Field(
        description="Targetted population of the range",
        default=None,
    )
    gender: Optional[Code] = Field(
        description="male | female | other | unknown",
        default=None,
    )
    gender_ext: Optional[Element] = Field(
        description="Placeholder element for gender extensions",
        default=None,
        alias="_gender",
    )
    age: Optional[Range] = Field(
        description="Applicable age range, if relevant",
        default=None,
    )
    gestationalAge: Optional[Range] = Field(
        description="Applicable gestational age range, if relevant",
        default=None,
    )
    condition: Optional[String] = Field(
        description="Condition associated with the reference range",
        default=None,
    )
    condition_ext: Optional[Element] = Field(
        description="Placeholder element for condition extensions",
        default=None,
        alias="_condition",
    )


class ObservationDefinition(DomainResource):
    """
    Set of definitional characteristics for a kind of observation or measurement produced or consumed by an orderable health care service.
    """

    _abstract = False
    _type = "ObservationDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ObservationDefinition"

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
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Category of observation",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Type of observation (code / type)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for this ObservationDefinition instance",
        default=None,
    )
    permittedDataType: Optional[ListType[Code]] = Field(
        description="Quantity | CodeableConcept | string | boolean | integer | Range | Ratio | SampledData | time | dateTime | Period",
        default=None,
    )
    permittedDataType_ext: Optional[Element] = Field(
        description="Placeholder element for permittedDataType extensions",
        default=None,
        alias="_permittedDataType",
    )
    multipleResultsAllowed: Optional[Boolean] = Field(
        description="Multiple results allowed",
        default=None,
    )
    multipleResultsAllowed_ext: Optional[Element] = Field(
        description="Placeholder element for multipleResultsAllowed extensions",
        default=None,
        alias="_multipleResultsAllowed",
    )
    method: Optional[CodeableConcept] = Field(
        description="Method used to produce the observation",
        default=None,
    )
    preferredReportName: Optional[String] = Field(
        description="Preferred report name",
        default=None,
    )
    preferredReportName_ext: Optional[Element] = Field(
        description="Placeholder element for preferredReportName extensions",
        default=None,
        alias="_preferredReportName",
    )
    quantitativeDetails: Optional[ObservationDefinitionQuantitativeDetails] = Field(
        description="Characteristics of quantitative results",
        default=None,
    )
    qualifiedInterval: Optional[ListType[ObservationDefinitionQualifiedInterval]] = (
        Field(
            description="Qualified range for continuous and ordinal observation results",
            default=None,
        )
    )
    validCodedValueSet: Optional[Reference] = Field(
        description="Value set of valid coded values for the observations conforming to this ObservationDefinition",
        default=None,
    )
    normalCodedValueSet: Optional[Reference] = Field(
        description="Value set of normal coded values for the observations conforming to this ObservationDefinition",
        default=None,
    )
    abnormalCodedValueSet: Optional[Reference] = Field(
        description="Value set of abnormal coded values for the observations conforming to this ObservationDefinition",
        default=None,
    )
    criticalCodedValueSet: Optional[Reference] = Field(
        description="Value set of critical coded values for the observations conforming to this ObservationDefinition",
        default=None,
    )
