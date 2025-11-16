from typing import List, Optional, TYPE_CHECKING

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4B.complex import (
        Address,
        Age,
        Annotation,
        Attachment,
        CodeableConcept,
        CodeableReference,
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
        Money,
        ParameterDefinition,
        Period,
        Quantity,
        Range,
        Ratio,
        RatioRange,
        Reference,
        RelatedArtifact,
        SampledData,
        Signature,
        Timing,
        TriggerDefinition,
        UsageContext,
    )


class Extension(Element):
    """
    Optional Extensions Element
    """

    url: Optional[String] = Field(
        description="identifies the meaning of the extension",
        default=None,
    )
    url_ext: Optional["Element"] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    valueBase64Binary: Optional[Base64Binary] = Field(
        description="Value of extension",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="Value of extension",
        default=None,
    )
    valueCanonical: Optional[Canonical] = Field(
        description="Value of extension",
        default=None,
    )
    valueCode: Optional[Code] = Field(
        description="Value of extension",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="Value of extension",
        default=None,
    )
    valueDateTime: Optional[DateTime] = Field(
        description="Value of extension",
        default=None,
    )
    valueDecimal: Optional[Decimal] = Field(
        description="Value of extension",
        default=None,
    )
    valueId: Optional[Id] = Field(
        description="Value of extension",
        default=None,
    )
    valueInstant: Optional[Instant] = Field(
        description="Value of extension",
        default=None,
    )
    valueInteger: Optional[Integer] = Field(
        description="Value of extension",
        default=None,
    )
    valueMarkdown: Optional[Markdown] = Field(
        description="Value of extension",
        default=None,
    )
    valueOid: Optional[Oid] = Field(
        description="Value of extension",
        default=None,
    )
    valuePositiveInt: Optional[PositiveInt] = Field(
        description="Value of extension",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="Value of extension",
        default=None,
    )
    valueTime: Optional[Time] = Field(
        description="Value of extension",
        default=None,
    )
    valueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Value of extension",
        default=None,
    )
    valueUri: Optional[Uri] = Field(
        description="Value of extension",
        default=None,
    )
    valueUrl: Optional[Url] = Field(
        description="Value of extension",
        default=None,
    )
    valueUuid: Optional[Uuid] = Field(
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

    @field_validator(*("extension",), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*("extension",), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Base64Binary,
                Boolean,
                Canonical,
                Code,
                Date,
                DateTime,
                Decimal,
                Id,
                Instant,
                Integer,
                Markdown,
                Oid,
                PositiveInt,
                String,
                Time,
                UnsignedInt,
                Uri,
                Url,
                Uuid,
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
                "Contributor",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Dosage",
            ],
            field_name_base="value",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_model_validator(self):
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
