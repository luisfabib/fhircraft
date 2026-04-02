from typing import Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.R4.complex import Element

if TYPE_CHECKING:
    from ..primitive import *
    from fhircraft.fhir.resources.datatypes.R4.complex import (
        Age,
        Address,
        Annotation,
        Attachment,
        CodeableConcept,
        Coding,
        ContactPoint,
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
        Reference,
        SampledData,
        Signature,
        Timing,
        Dosage,
        Meta,
        ContactDetail,
        Contributor,
        DataRequirement,
        Expression,
        ParameterDefinition,
        RelatedArtifact,
        TriggerDefinition,
        UsageContext,
    )


class Extension(Element):
    """
    Optional Extensions Element
    """

    _type = "Extension"

    url: Optional[str] = Field(
        description="identifies the meaning of the extension",
        default=None,
    )
    valueBase64Binary: Optional["Base64Binary"] = Field(
        description="Value of extension",
        default=None,
    )
    valueBoolean: Optional["Boolean"] = Field(
        description="Value of extension",
        default=None,
    )
    valueCanonical: Optional["Canonical"] = Field(
        description="Value of extension",
        default=None,
    )
    valueCode: Optional["Code"] = Field(
        description="Value of extension",
        default=None,
    )
    valueDate: Optional["Date"] = Field(
        description="Value of extension",
        default=None,
    )
    valueDateTime: Optional["DateTime"] = Field(
        description="Value of extension",
        default=None,
    )
    valueDecimal: Optional["Decimal"] = Field(
        description="Value of extension",
        default=None,
    )
    valueId: Optional["Id"] = Field(
        description="Value of extension",
        default=None,
    )
    valueInstant: Optional["Instant"] = Field(
        description="Value of extension",
        default=None,
    )
    valueInteger: Optional["Integer"] = Field(
        description="Value of extension",
        default=None,
    )
    valueMarkdown: Optional["Markdown"] = Field(
        description="Value of extension",
        default=None,
    )
    valueOid: Optional["Oid"] = Field(
        description="Value of extension",
        default=None,
    )
    valuePositiveInt: Optional["PositiveInt"] = Field(
        description="Value of extension",
        default=None,
    )
    valueString: Optional["String"] = Field(
        description="Value of extension",
        default=None,
    )
    valueTime: Optional["Time"] = Field(
        description="Value of extension",
        default=None,
    )
    valueUnsignedInt: Optional["UnsignedInt"] = Field(
        description="Value of extension",
        default=None,
    )
    valueUri: Optional["Uri"] = Field(
        description="Value of extension",
        default=None,
    )
    valueUrl: Optional["Url"] = Field(
        description="Value of extension",
        default=None,
    )
    valueUuid: Optional["Uuid"] = Field(
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
    valueContributor: Optional["Contributor"] = Field(
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
        )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
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
