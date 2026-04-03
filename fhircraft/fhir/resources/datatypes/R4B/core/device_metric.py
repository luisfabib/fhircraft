import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Timing,
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
    state: Optional[Code] = Field(
        description="not-calibrated | calibration-required | calibrated | unspecified",
        default=None,
    )
    time: Optional[Instant] = Field(
        description="Describes the time last calibration has been performed",
        default=None,
    )

class DeviceMetric(DomainResource):
    """
    Describes a measurement, calculation or setting capability of a medical device.
    """

    _abstract = False
    _type = "DeviceMetric"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceMetric"

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
    color: Optional[Code] = Field(
        description="black | red | green | yellow | blue | magenta | cyan | white",
        default=None,
    )
    category: Optional[Code] = Field(
        description="measurement | setting | calculation | unspecified",
        default=None,
    )
    measurementPeriod: Optional[Timing] = Field(
        description="Describes the measurement repetition time",
        default=None,
    )
    calibration: Optional[ListType[DeviceMetricCalibration]] = Field(
        description="Describes the calibrations that have been performed or that are required to be performed",
        default=None,
    )
