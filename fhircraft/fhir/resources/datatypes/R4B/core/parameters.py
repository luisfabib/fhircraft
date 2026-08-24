from pydantic import Field, model_validator

NoneType = type(None)

from typing import List as ListType, Optional

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Address,
    Age,
    Annotation,
    Attachment,
    BackboneElement,
    CodeableConcept,
    Coding,
    ContactDetail,
    ContactPoint,
    Contributor,
    Count,
    DataRequirement,
    Distance,
    Dosage,
    Duration,
    Element,
    Expression,
    HumanName,
    Identifier,
    Meta,
    Money,
    ParameterDefinition,
    Period,
    Quantity,
    Range,
    Ratio,
    Reference,
    RelatedArtifact,
    SampledData,
    Signature,
    Timing,
    TriggerDefinition,
    UsageContext,
)
from .resource import Resource
from .domain_resource import DomainResource


class ParametersParameter(BackboneElement):
    """
    A parameter passed to or received from the operation.
    """

    name: fhir.string = Field(
        description="Name from the definition",
    )
    valueBase64Binary: Optional[fhir.base64Binary] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueCanonical: Optional[fhir.canonical] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueCode: Optional[fhir.code] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueDate: Optional[fhir.date_] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueDecimal: Optional[fhir.decimal] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueId: Optional[fhir.id_] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueInstant: Optional[fhir.instant] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueMarkdown: Optional[fhir.markdown] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueOid: Optional[fhir.oid] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valuePositiveInt: Optional[fhir.positiveInt] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueTime: Optional[fhir.time_] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueUnsignedInt: Optional[fhir.unsignedInt] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueUri: Optional[fhir.uri] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueUrl: Optional[fhir.url] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueUuid: Optional[fhir.uuid] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueAddress: Optional[Address] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueAge: Optional[Age] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueAnnotation: Optional[Annotation] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueContactPoint: Optional[ContactPoint] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueCount: Optional[Count] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueDistance: Optional[Distance] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueDuration: Optional[Duration] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueHumanName: Optional[HumanName] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueIdentifier: Optional[Identifier] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueMoney: Optional[Money] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valuePeriod: Optional[Period] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueRatio: Optional[Ratio] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueSampledData: Optional[SampledData] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueSignature: Optional[Signature] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueTiming: Optional[Timing] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueContactDetail: Optional[ContactDetail] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueContributor: Optional[Contributor] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueDataRequirement: Optional[DataRequirement] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueExpression: Optional[Expression] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueParameterDefinition: Optional[ParameterDefinition] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueRelatedArtifact: Optional[RelatedArtifact] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueTriggerDefinition: Optional[TriggerDefinition] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueUsageContext: Optional[UsageContext] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueDosage: Optional[Dosage] = Field(
        description="If parameter is a data type",
        default=None,
    )
    valueMeta: Optional[Meta] = Field(
        description="If parameter is a data type",
        default=None,
    )
    resource: Optional[Resource] = Field(
        description="If parameter is a whole resource",
        default=None,
    )
    part: Optional[ListType["ParametersParameter"]] = Field(
        description="Named part of a multi-part parameter",
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
                fhir.Base64Binary,
                fhir.Boolean,
                fhir.Canonical,
                fhir.Code,
                fhir.Date,
                fhir.DateTime,
                fhir.Decimal,
                fhir.Id,
                fhir.Instant,
                fhir.Integer,
                fhir.Markdown,
                fhir.Oid,
                fhir.PositiveInt,
                fhir.String,
                fhir.Time,
                fhir.UnsignedInt,
                fhir.Uri,
                fhir.Url,
                fhir.Uuid,
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
                "Coding",
                "ContactPoint",
                "Count",
                "Distance",
                "Duration",
                "HumanName",
                "Identifier",
                "Money",
                "Period",
                "Quantity",
                "Range",
                "Ratio",
                "Reference",
                "SampledData",
                "Signature",
                "Timing",
                "ContactDetail",
                "Contributor",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Dosage",
                "Meta",
            ],
            field_name_base="value",
            required=False,
        )


class Parameters(Resource):
    """
    This resource is a non-persisted resource used to pass information into and back from an [operation](https://hl7.org/fhir/R4B/operations.html). It has no other use, and there is no RESTful endpoint associated with it.
    """

    _abstract = False
    _type = "Parameters"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Parameters"

    parameter: Optional[ListType[ParametersParameter]] = Field(
        description="Operation Parameter",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_inv_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("parameter",),
            expression="(part.exists() and value.empty() and resource.empty()) or (part.empty() and (value.exists() xor resource.exists()))",
            human="A parameter must have one and only one of (value, resource, part)",
            key="inv-1",
            severity="error",
        )
