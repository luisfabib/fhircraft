from typing import Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import DataType

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R5.complex import (
        DataType,
        Address,
        Element,
        Age,
        Annotation,
        Attachment,
        CodeableConcept,
        CodeableReference,
        Coding,
        ContactDetail,
        ContactPoint,
        DataRequirement,
        Dosage,
        Expression,
        Count,
        Distance,
        Duration,
        HumanName,
        Identifier,
        Money,
        Period,
        Quantity,
        Range,
        Ratio,
        RatioRange,
        Reference,
        SampledData,
        Signature,
        Timing,
        ParameterDefinition,
        RelatedArtifact,
        TriggerDefinition,
        UsageContext,
        Availability,
        ExtendedContactDetail,
        Meta,
    )


class Extension(DataType):
    """
    Optional Extensions Element
    """

    _type = "Extension"

    url: Optional[str] = Field(
        description="identifies the meaning of the extension",
        default=None,
    )
    valueBase64Binary: Optional[fhir.base64Binary] = Field(
        description="Value of extension",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Value of extension",
        default=None,
    )
    valueCanonical: Optional[fhir.canonical] = Field(
        description="Value of extension",
        default=None,
    )
    valueCode: Optional[fhir.code] = Field(
        description="Value of extension",
        default=None,
    )
    valueDate: Optional[fhir.date_] = Field(
        description="Value of extension",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="Value of extension",
        default=None,
    )
    valueDecimal: Optional[fhir.decimal] = Field(
        description="Value of extension",
        default=None,
    )
    valueId: Optional[fhir.id_] = Field(
        description="Value of extension",
        default=None,
    )
    valueInstant: Optional[fhir.instant] = Field(
        description="Value of extension",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Value of extension",
        default=None,
    )
    valueInteger64: Optional[fhir.integer64] = Field(
        description="Value of extension",
        default=None,
    )
    valueMarkdown: Optional[fhir.markdown] = Field(
        description="Value of extension",
        default=None,
    )
    valueOid: Optional[fhir.oid] = Field(
        description="Value of extension",
        default=None,
    )
    valuePositiveInt: Optional[fhir.positiveInt] = Field(
        description="Value of extension",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Value of extension",
        default=None,
    )
    valueTime: Optional[fhir.time_] = Field(
        description="Value of extension",
        default=None,
    )
    valueUnsignedInt: Optional[fhir.unsignedInt] = Field(
        description="Value of extension",
        default=None,
    )
    valueUri: Optional[fhir.uri] = Field(
        description="Value of extension",
        default=None,
    )
    valueUrl: Optional[fhir.url] = Field(
        description="Value of extension",
        default=None,
    )
    valueUuid: Optional[fhir.uuid] = Field(
        description="Value of extension",
        default=None,
    )
    valueAddress: Optional["Address"] = Field(
        description="Value of extension",
        default=None,
    )
    valueAge: Optional["Age"] = Field(
        description="Value of extension",
        default=None,
    )
    valueAnnotation: Optional["Annotation"] = Field(
        description="Value of extension",
        default=None,
    )
    valueAttachment: Optional["Attachment"] = Field(
        description="Value of extension",
        default=None,
    )
    valueCodeableConcept: Optional["CodeableConcept"] = Field(
        description="Value of extension",
        default=None,
    )
    valueCodeableReference: Optional["CodeableReference"] = Field(
        description="Value of extension",
        default=None,
    )
    valueCoding: Optional["Coding"] = Field(
        description="Value of extension",
        default=None,
    )
    valueContactPoint: Optional["ContactPoint"] = Field(
        description="Value of extension",
        default=None,
    )
    valueCount: Optional["Count"] = Field(
        description="Value of extension",
        default=None,
    )
    valueDistance: Optional["Distance"] = Field(
        description="Value of extension",
        default=None,
    )
    valueDuration: Optional["Duration"] = Field(
        description="Value of extension",
        default=None,
    )
    valueHumanName: Optional["HumanName"] = Field(
        description="Value of extension",
        default=None,
    )
    valueIdentifier: Optional["Identifier"] = Field(
        description="Value of extension",
        default=None,
    )
    valueMoney: Optional["Money"] = Field(
        description="Value of extension",
        default=None,
    )
    valuePeriod: Optional["Period"] = Field(
        description="Value of extension",
        default=None,
    )
    valueQuantity: Optional["Quantity"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRange: Optional["Range"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRatio: Optional["Ratio"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRatioRange: Optional["RatioRange"] = Field(
        description="Value of extension",
        default=None,
    )
    valueReference: Optional["Reference"] = Field(
        description="Value of extension",
        default=None,
    )
    valueSampledData: Optional["SampledData"] = Field(
        description="Value of extension",
        default=None,
    )
    valueSignature: Optional["Signature"] = Field(
        description="Value of extension",
        default=None,
    )
    valueTiming: Optional["Timing"] = Field(
        description="Value of extension",
        default=None,
    )
    valueContactDetail: Optional["ContactDetail"] = Field(
        description="Value of extension",
        default=None,
    )
    valueDataRequirement: Optional["DataRequirement"] = Field(
        description="Value of extension",
        default=None,
    )
    valueExpression: Optional["Expression"] = Field(
        description="Value of extension",
        default=None,
    )
    valueParameterDefinition: Optional["ParameterDefinition"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRelatedArtifact: Optional["RelatedArtifact"] = Field(
        description="Value of extension",
        default=None,
    )
    valueTriggerDefinition: Optional["TriggerDefinition"] = Field(
        description="Value of extension",
        default=None,
    )
    valueUsageContext: Optional["UsageContext"] = Field(
        description="Value of extension",
        default=None,
    )
    valueAvailability: Optional["Availability"] = Field(
        description="Value of extension",
        default=None,
    )
    valueExtendedContactDetail: Optional["ExtendedContactDetail"] = Field(
        description="Value of extension",
        default=None,
    )
    valueDosage: Optional["Dosage"] = Field(
        description="Value of extension",
        default=None,
    )
    valueMeta: Optional["Meta"] = Field(
        description="Value of extension",
        default=None,
    )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                "Base64Binary",
                "Boolean",
                "Canonical",
                "Code",
                "Date",
                "DateTime",
                "Decimal",
                "Id",
                "Instant",
                "Integer",
                "Integer64",
                "Markdown",
                "Oid",
                "PositiveInt",
                "String",
                "Time",
                "UnsignedInt",
                "Uri",
                "Url",
                "Uuid",
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
                "CodeableReference",
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
                "RatioRange",
                "Reference",
                "SampledData",
                "Signature",
                "Timing",
                "ContactDetail",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Availability",
                "ExtendedContactDetail",
                "Dosage",
                "Meta",
            ],
            field_name_base="value",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )
