import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, Instant

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
    Timing,
)
from .resource import Resource
from .domain_resource import DomainResource


class DeviceMetricCalibration(BackboneElement):
    """
    Describes the calibrations that have been performed or that are required to be performed.
    """

    type: Optional[Code] = Field(
        description="unspecified | offset | gain | two-point",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    state: Optional[Code] = Field(
        description="not-calibrated | calibration-required | calibrated | unspecified",
        default=None,
    )
    state_ext: Optional[Element] = Field(
        description="Placeholder element for state extensions",
        default=None,
        alias="_state",
    )
    time: Optional[Instant] = Field(
        description="Describes the time last calibration has been performed",
        default=None,
    )
    time_ext: Optional[Element] = Field(
        description="Placeholder element for time extensions",
        default=None,
        alias="_time",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "time",
                "state",
                "type",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class DeviceMetric(DomainResource):
    """
    Describes a measurement, calculation or setting capability of a medical device.
    """

    _abstract = False
    _type = "DeviceMetric"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceMetric"

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
            profile=["http://hl7.org/fhir/StructureDefinition/DeviceMetric"]
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
        description="Instance identifier",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Identity of metric, for example Heart Rate or PEEP Setting",
        default=None,
    )
    unit: Optional[CodeableConcept] = Field(
        description="Unit of Measure for the Metric",
        default=None,
    )
    source: Optional[Reference] = Field(
        description="Describes the link to the source Device",
        default=None,
    )
    parent: Optional[Reference] = Field(
        description="Describes the link to the parent Device",
        default=None,
    )
    operationalStatus: Optional[Code] = Field(
        description="on | off | standby | entered-in-error",
        default=None,
    )
    operationalStatus_ext: Optional[Element] = Field(
        description="Placeholder element for operationalStatus extensions",
        default=None,
        alias="_operationalStatus",
    )
    color: Optional[Code] = Field(
        description="black | red | green | yellow | blue | magenta | cyan | white",
        default=None,
    )
    color_ext: Optional[Element] = Field(
        description="Placeholder element for color extensions",
        default=None,
        alias="_color",
    )
    category: Optional[Code] = Field(
        description="measurement | setting | calculation | unspecified",
        default=None,
    )
    category_ext: Optional[Element] = Field(
        description="Placeholder element for category extensions",
        default=None,
        alias="_category",
    )
    measurementPeriod: Optional[Timing] = Field(
        description="Describes the measurement repetition time",
        default=None,
    )
    calibration: Optional[ListType[DeviceMetricCalibration]] = Field(
        description="Describes the calibrations that have been performed or that are required to be performed",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "calibration",
                "measurementPeriod",
                "category",
                "color",
                "operationalStatus",
                "parent",
                "source",
                "unit",
                "type",
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
