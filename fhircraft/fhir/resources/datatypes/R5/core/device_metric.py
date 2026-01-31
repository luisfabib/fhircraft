from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, Instant

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Quantity,
    BackboneElement,
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


class DeviceMetric(DomainResource):
    """
    Describes a measurement, calculation or setting capability of a device.  The DeviceMetric resource is derived from the ISO/IEEE 11073-10201 Domain Information Model standard, but is more widely applicable.
    """

    _abstract = False
    _type = "DeviceMetric"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceMetric"

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
    device: Optional[Reference] = Field(
        description="Describes the link to the Device",
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
        description="Color name (from CSS4) or #RRGGBB code",
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
    measurementFrequency: Optional[Quantity] = Field(
        description="Indicates how often the metric is taken or recorded",
        default=None,
    )
    calibration: Optional[ListType[DeviceMetricCalibration]] = Field(
        description="Describes the calibrations that have been performed or that are required to be performed",
        default=None,
    )
