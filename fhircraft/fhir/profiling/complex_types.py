from pydantic import BaseModel, Field
from fhircraft.fhir.profiling import primitive_types as fhirtypes
from typing import Optional, List, Literal

class Element(BaseModel):
    id: Optional[fhirtypes.Id] = None 
    extension: Optional[List["Extension"]] = Field(        
        default_factory=list,
    )


class Attachment(Element):
    contentType: Optional[fhirtypes.Code] = Field(
        None,
        description="Identifies the type of the data in the attachment and allows a method to be chosen to interpret or render the data. The type is expressed as a MIME type."
    )
    language: Optional[fhirtypes.Code] = Field(
        None,
        description="The human language of the content. The value can be any valid BCP 47 value."
    )
    data: Optional[fhirtypes.Base64Binary] = Field(
        None,
        description="The actual data of the attachment - a sequence of bytes, base64 encoded."
    )
    url: Optional[fhirtypes.Url] = Field(
        None,
        description="A location where the data can be accessed."
    )
    size: Optional[fhirtypes.Integer] = Field(
        None,
        description="The number of bytes of data that make up this attachment (before base64 encoding, if that is done)."
    )
    hash: Optional[fhirtypes.Base64Binary] = Field(
        None,
        description="The calculated hash of the data using SHA-1. Represented using base64."
    )
    title: Optional[fhirtypes.String] = Field(
        None,
        description="A label or set of text to display in place of the data."
    )
    creation: Optional[fhirtypes.DateTime] = Field(
        None,
        description="The date that the attachment was first created."
    )

    class Config:
        schema_extra = {
            "example": {
                "contentType": "application/pdf",
                "language": "en",
                "data": "SGVsbG8gd29ybGQ=",
                "url": "http://example.org/fhir/DocumentReference/12345",
                "size": 12345,
                "hash": "2jmj7l5rSw0yVb/vlWAYkK/YBwk=",
                "title": "Example PDF",
                "creation": "2020-01-01T00:00:00Z"
            }
        }


class Coding(Element):
    system: Optional[fhirtypes.Uri] = Field(
        None,
        description="The identification of the code system that defines the meaning of the symbol in the code."
    )
    version: Optional[fhirtypes.String] = Field(
        None,
        description="The version of the code system which was used when choosing the code."
    )
    code: Optional[fhirtypes.String] = Field(
        None,
        description="A symbol in syntax defined by the system. The symbol may be a predefined code or an expression in a syntax defined by the coding system."
    )
    display: Optional[fhirtypes.String] = Field(
        None,
        description="A representation of the meaning of the code in the system, following the rules of the system."
    )
    userSelected: Optional[fhirtypes.Boolean] = Field(
        None,
        description="Indicates that this coding was chosen by a user directly - e.g., off a pick list of available items (codes or displays)."
    )

    class Config:
        schema_extra = {
            "example": {
                "system": "http://loinc.org",
                "version": "2.67",
                "code": "4548-4",
                "display": "Hematocrit [Volume Fraction] of Blood by Automated count",
                "userSelected": True
            }
        }

class CodeableConcept(Element):
    coding: Optional[List[Coding]] = Field(
        default_factory=list,
        description="A reference to a code defined by a terminology system."
    )
    text: Optional[fhirtypes.String] = Field(
        None,
        description="A human language representation of the concept as seen/selected/uttered by the user who entered the data and/or which represents the intended meaning of the user."
    )

    class Config:
        schema_extra = {
            "example": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "1234-5",
                        "display": "Example code display"
                    }
                ],
                "text": "Example text"
            }
        }


class Quantity(Element):
    value: Optional[fhirtypes.Decimal] = Field(
        None,
        description="The value of the measured amount. The value includes an implicit precision in the presentation of the value."
    )
    comparator: Optional[fhirtypes.Code] = Field(
        None,
        description="How the value should be understood and represented - whether the actual value is greater or less than the stated value due to measurement issues."
    )
    unit: Optional[fhirtypes.String] = Field(
        None,
        description="A human-readable form of the unit."
    )
    system: Optional[fhirtypes.Uri] = Field(
        None,
        description="The identification of the system that provides the coded form of the unit."
    )
    code: Optional[fhirtypes.Code] = Field(
        None,
        description="A computer processable form of the unit in some unit representation system."
    )

    class Config:
        schema_extra = {
            "example": {
                "value": 123.45,
                "comparator": ">",
                "unit": "mg",
                "system": "http://unitsofmeasure.org",
                "code": "mg"
            }
        }

class SimpleQuantity(Quantity):
    class Config:
        schema_extra = {
            "example": {
                "value": 123.45,
                "unit": "mg",
                "system": "http://unitsofmeasure.org",
                "code": "mg"
            }
        }


class Money(Element):
    value: Optional[fhirtypes.Decimal] = Field(
        None,
        description="Numerical value (with implicit precision)."
    )
    currency: Optional[fhirtypes.Code] = Field(
        None,
        description="ISO 4217 Currency Code."
    )

    class Config:
        schema_extra = {
            "example": {
                "value": 100.00,
                "currency": "USD"
            }
        }

class Range(Element):
    low: Optional[Quantity] = Field(
        None,
        description="The low limit. The boundary is inclusive."
    )
    high: Optional[Quantity] = Field(
        None,
        description="The high limit. The boundary is inclusive."
    )

    class Config:
        schema_extra = {
            "example": {
                "low": {
                    "value": 10,
                    "unit": "mg",
                    "system": "http://unitsofmeasure.org",
                    "code": "mg"
                },
                "high": {
                    "value": 20,
                    "unit": "mg",
                    "system": "http://unitsofmeasure.org",
                    "code": "mg"
                }
            }
        }

class Ratio(Element):
    numerator: Optional[Quantity] = Field(
        None,
        description="The value of the numerator."
    )
    denominator: Optional[Quantity] = Field(
        None,
        description="The value of the denominator."
    )

    class Config:
        schema_extra = {
            "example": {
                "numerator": {
                    "value": 1,
                    "unit": "mg"
                },
                "denominator": {
                    "value": 1,
                    "unit": "mL"
                }
            }
        }

class RatioRange(Element):
    lowNumerator: Optional[Quantity] = Field(
        None,
        description="The low numerator limit."
    )
    highNumerator: Optional[Quantity] = Field(
        None,
        description="The high numerator limit."
    )
    denominator: Optional[Quantity] = Field(
        None,
        description="The value of the denominator."
    )

    class Config:
        schema_extra = {
            "example": {
                "lowNumerator": {
                    "value": 1,
                    "unit": "mg"
                },
                "highNumerator": {
                    "value": 2,
                    "unit": "mg"
                },
                "denominator": {
                    "value": 1,
                    "unit": "mL"
                }
            }
        }

class Period(Element):
    start: Optional[fhirtypes.DateTime] = Field(
        None,
        description="The start of the period. The boundary is inclusive."
    )
    end: Optional[fhirtypes.DateTime] = Field(
        None,
        description="The end of the period. The boundary is inclusive."
    )

    class Config:
        schema_extra = {
            "example": {
                "start": "2020-01-01T00:00:00Z",
                "end": "2020-12-31T23:59:59Z"
            }
        }

class SampledData(Element):
    origin: Quantity = Field(
        ...,
        description="Base quantity that provides the reference for the measured value relative to."
    )
    period: fhirtypes.Decimal = Field(
        ...,
        description="The length of time between sampling times."
    )
    factor: Optional[fhirtypes.Decimal] = Field(
        None,
        description="A correction factor that is applied to the sampled data points before they are added to the origin."
    )
    lowerLimit: Optional[fhirtypes.Decimal] = Field(
        None,
        description="The lower limit of detection of the measured points."
    )
    upperLimit: Optional[fhirtypes.Decimal] = Field(
        None,
        description="The upper limit of detection of the measured points."
    )
    dimensions: fhirtypes.PositiveInt = Field(
        ...,
        description="The number of sample points at each time point."
    )
    data: Optional[fhirtypes.String] = Field(
        None,
        description="A series of data points that are measured."
    )

    class Config:
        schema_extra = {
            "example": {
                "origin": {
                    "value": 0,
                    "unit": "mV",
                    "system": "http://unitsofmeasure.org",
                    "code": "mV"
                },
                "period": 10,
                "factor": 1,
                "lowerLimit": -0.5,
                "upperLimit": 0.5,
                "dimensions": 1,
                "data": "0 1 2 3 4 5 6 7 8 9"
            }
        }

class Identifier(Element):
    use: Optional[fhirtypes.Code] = Field(
        None,
        description="The purpose of this identifier."
    )
    type: Optional[CodeableConcept] = Field(
        None,
        description="A coded type for the identifier."
    )
    system: Optional[fhirtypes.Uri] = Field(
        None,
        description="The namespace for the identifier value."
    )
    value: Optional[fhirtypes.String] = Field(
        None,
        description="The value that is unique."
    )
    period: Optional[Period] = Field(
        None,
        description="Time period during which identifier is/was valid for use."
    )
    assigner: Optional["Reference"] = Field(
        None,
        description="Organization that issued the identifier."
    )

    class Config:
        schema_extra = {
            "example": {
                "use": "official",
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "MR",
                            "display": "Medical Record Number"
                        }
                    ]
                },
                "system": "http://hospital.smarthealthit.org",
                "value": "12345",
                "period": {
                    "start": "2001-05-06"
                },
                "assigner": {
                    "display": "Acme Healthcare"
                }
            }
        }


class Reference(Element):
    reference: Optional[fhirtypes.String] = Field(
        None,
        description="A reference to a location at which the other resource is found."
    )
    type: Optional[fhirtypes.Uri] = Field(
        None,
        description="The type of the resource."
    )
    identifier: Optional[Identifier] = Field(
        None,
        description="An identifier for the other resource."
    )
    display: Optional[fhirtypes.String] = Field(
        None,
        description="Plain text narrative that identifies the resource."
    )

    class Config:
        schema_extra = {
            "example": {
                "reference": "Patient/example",
                "type": "Patient",
                "identifier": {
                    "use": "official",
                    "system": "http://hospital.smarthealthit.org",
                    "value": "12345"
                },
                "display": "Example Patient"
            }
        }

class HumanName(Element):
    use: Optional[fhirtypes.Code] = Field(
        None,
        description="Identifies the purpose for this name."
    )
    text: Optional[fhirtypes.String] = Field(
        None,
        description="A full text representation of the name."
    )
    family: Optional[fhirtypes.String] = Field(
        None,
        description="The part of a name that links to the genealogy."
    )
    given: Optional[List[fhirtypes.String]] = Field(
        default_factory=list,
        description="Given names."
    )
    prefix: Optional[List[fhirtypes.String]] = Field(
        default_factory=list,
        description="Parts that come before the name."
    )
    suffix: Optional[List[fhirtypes.String]] = Field(
        default_factory=list,
        description="Parts that come after the name."
    )
    period: Optional[Period] = Field(
        None,
        description="Time period when name was/is in use."
    )

    class Config:
        schema_extra = {
            "example": {
                "use": "official",
                "text": "Mr. John Doe",
                "family": "Doe",
                "given": ["John", "Joseph"],
                "prefix": ["Mr."],
                "suffix": ["Jr."],
                "period": {
                    "start": "2001-05-06"
                }
            }
        }

class Address(Element):
    use: Optional[fhirtypes.Code] = Field(
        None,
        description="The purpose of this address."
    )
    type: Optional[fhirtypes.Code] = Field(
        None,
        description="The type of address (physical / postal)."
    )
    text: Optional[fhirtypes.String] = Field(
        None,
        description="Text representation of the address."
    )
    line: Optional[List[fhirtypes.String]] = Field(
        default_factory=list,
        description="Street name, number, direction & P.O. Box."
    )
    city: Optional[fhirtypes.String] = Field(
        None,
        description="Name of city, town etc."
    )
    district: Optional[fhirtypes.String] = Field(
        None,
        description="District name (aka county)."
    )
    state: Optional[fhirtypes.String] = Field(
        None,
        description="Sub-unit of country (abbreviations ok)."
    )
    postalCode: Optional[fhirtypes.String] = Field(
        None,
        description="Postal code for area."
    )
    country: Optional[fhirtypes.String] = Field(
        None,
        description="Country (e.g., can be ISO 3166 2 or 3 letter code)."
    )
    period: Optional[Period] = Field(
        None,
        description="Time period when address was/is in use."
    )

    class Config:
        schema_extra = {
            "example": {
                "use": "home",
                "type": "both",
                "text": "1234 Main St, Springfield, IL 62704",
                "line": ["1234 Main St"],
                "city": "Springfield",
                "district": "Sangamon",
                "state": "IL",
                "postalCode": "62704",
                "country": "USA",
                "period": {
                    "start": "2001-05-06"
                }
            }
        }

class ContactPoint(Element):
    system: Optional[fhirtypes.Code] = Field(
        None,
        description="Telecommunications form for contact point - what communications system is required to make use of the contact."
    )
    value: Optional[fhirtypes.String] = Field(
        None,
        description="The actual contact point details."
    )
    use: Optional[fhirtypes.Code] = Field(
        None,
        description="Identifies the purpose for the contact point."
    )
    rank: Optional[fhirtypes.PositiveInt] = Field(
        None,
        description="Specifies a preferred order in which to use a set of contacts."
    )
    period: Optional[Period] = Field(
        None,
        description="Time period when the contact point was/is in use."
    )

    class Config:
        schema_extra = {
            "example": {
                "system": "phone",
                "value": "(555) 555-5555",
                "use": "work",
                "rank": 1,
                "period": {
                    "start": "2010-04-01"
                }
            }
        }

class BackboneElement(Element):
    modifierExtension: Optional[List["Extension"]] = Field(
        default_factory=list,
        description="Extensions that cannot be ignored even if unrecognized."
    )

class Repeat(BaseModel):
    boundsDuration: Optional["Duration"] = Field(
        None,
        description="Length/Range of lengths, or (Start/End) Limits to the extent of the activity."
    )
    boundsRange: Optional[Range] = Field(
        None,
        description="Length/Range of lengths, or (Start/End) Limits to the extent of the activity."
    )
    boundsPeriod: Optional[Period] = Field(
        None,
        description="Length/Range of lengths, or (Start/End) Limits to the extent of the activity."
    )
    count: Optional[fhirtypes.PositiveInt] = Field(
        None,
        description="Number of times to repeat."
    )
    countMax: Optional[fhirtypes.PositiveInt] = Field(
        None,
        description="Maximum number of times to repeat."
    )
    duration: Optional[fhirtypes.Decimal] = Field(
        None,
        description="How long each repetition should last."
    )
    durationMax: Optional[fhirtypes.Decimal] = Field(
        None,
        description="The maximum amount of time a recurrent event is allowed to last."
    )
    durationUnit: Optional[fhirtypes.Code] = Field(
        None,
        description="The unit of time (UCUM)."
    )
    frequency: Optional[fhirtypes.PositiveInt] = Field(
        None,
        description="Number of times per period the event is to occur."
    )
    frequencyMax: Optional[fhirtypes.PositiveInt] = Field(
        None,
        description="Maximum number of times the event can occur per period."
    )
    period: Optional[fhirtypes.Decimal] = Field(
        None,
        description="Amount of time the study would last (per unit of time)."
    )
    periodMax: Optional[fhirtypes.Decimal] = Field(
        None,
        description="Upper limit of time for the duration of a study."
    )
    periodUnit: Optional[fhirtypes.Code] = Field(
        None,
        description="Unit of time (UCUM)."
    )
    dayOfWeek: Optional[List[fhirtypes.Code]] = Field(
        default_factory=list,
        description="If one or more days of the week is specified, then the event is limited to occur on the specified day(s)."
    )
    timeOfDay: Optional[List[fhirtypes.Time]] = Field(
        default_factory=list,
        description="Specified time(s) of day for the event."
    )
    when: Optional[List[fhirtypes.Code]] = Field(
        default_factory=list,
        description="Real world event related time events."
    )
    offset: Optional[fhirtypes.UnsignedInt] = Field(
        None,
        description="The minutes from the event. "
    )

    class Config:
        schema_extra = {
            "example": {
                "boundsDuration": {
                    "value": 30,
                    "unit": "days",
                    "system": "http://unitsofmeasure.org",
                    "code": "d"
                },
                "count": 2,
                "duration": 1,
                "durationUnit": "d",
                "frequency": 1,
                "period": 1,
                "periodUnit": "d"
            }
        }

class Timing(BackboneElement):
    event: Optional[List[fhirtypes.DateTime]] = Field(
        default_factory=list,
        description="When the event(s) is/are to occur."
    )
    repeat: Optional[Repeat] = Field(
        None,
        description="A set of rules that describe when the event is scheduled."
    )
    code: Optional[CodeableConcept] = Field(
        None,
        description="A code for the timing schedule."
    )

    class Config:
        schema_extra = {
            "example": {
                "event": ["2012-05-31T09:00:00Z"],
                "repeat": {
                    "frequency": 1,
                    "period": 1,
                    "periodUnit": "d"
                },
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "1234-5",
                            "display": "Timing code"
                        }
                    ],
                    "text": "Every morning at 9am"
                }
            }
        }

class Signature(Element):
    type: List[Coding] = Field(
        ...,
        description="Indicates the reason for the signature."
    )
    when: fhirtypes.Instant = Field(
        ...,
        description="When the signature was created."
    )
    who: Reference = Field(
        ...,
        description="A reference to who signed the document."
    )
    onBehalfOf: Optional[Reference] = Field(
        None,
        description="A reference to who is represented by the signature."
    )
    targetFormat: Optional[fhirtypes.Code] = Field(
        None,
        description="The technical format of the signed resources."
    )
    sigFormat: Optional[fhirtypes.Code] = Field(
        None,
        description="The technical format of the signature."
    )
    data: Optional[fhirtypes.Base64Binary] = Field(
        None,
        description="The actual signature content."
    )

    class Config:
        schema_extra = {
            "example": {
                "type": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
                        "code": "TREAT",
                        "display": "Treatment"
                    }
                ],
                "when": "2017-01-01T12:00:00Z",
                "who": {
                    "reference": "Practitioner/example"
                },
                "onBehalfOf": {
                    "reference": "Organization/example"
                },
                "targetFormat": "application/fhir+xml",
                "sigFormat": "application/jose",
                "data": "dGVzdA=="
            }
        }

class Annotation(Element):
    authorReference: Optional[Reference] = Field(
        None,
        description="Reference to the individual responsible for the annotation."
    )
    authorString: Optional[fhirtypes.String] = Field(
        None,
        description="Name of the individual responsible for the annotation."
    )
    time: Optional[fhirtypes.DateTime] = Field(
        None,
        description="Indicates when this particular annotation was made."
    )
    text: fhirtypes.String = Field(
        ...,
        description="The text of the annotation."
    )

    class Config:
        schema_extra = {
            "example": {
                "authorString": "Practitioner/example",
                "time": "2018-01-01T12:00:00Z",
                "text": "This is an annotation."
            }
        }

class Resource(BaseModel):
    resourceType: str = Field(
        ...,
        description="Type of the resource."
    )

    class Config:
        schema_extra = {
            "example": {
                "resourceType": "Patient"
            }
        }


class Meta(Element):
    versionId: Optional[fhirtypes.Id] = Field(
        None,
        description="The version specific identifier."
    )
    lastUpdated: Optional[fhirtypes.Instant] = Field(
        None,
        description="When the resource version last changed."
    )
    source: Optional[fhirtypes.Uri] = Field(
        None,
        description="A uri that identifies the source system of the resource."
    )
    profile: Optional[List[fhirtypes.Canonical]] = Field(
        default_factory=list,
        description="A list of profiles the resource claims to conform to."
    )
    security: Optional[List[Coding]] = Field(
        default_factory=list,
        description="Security labels applied to the resource."
    )
    tag: Optional[List[Coding]] = Field(
        default_factory=list,
        description="Tags applied to the resource."
    )

    class Config:
        schema_extra = {
            "example": {
                "versionId": "1",
                "lastUpdated": "2020-01-01T12:00:00Z",
                "source": "http://hospital.smarthealthit.org",
                "profile": [
                    "http://hl7.org/fhir/StructureDefinition/Patient"
                ],
                "security": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
                        "code": "TREAT",
                        "display": "Treatment"
                    }
                ],
                "tag": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
                        "code": "HTEST",
                        "display": "test health data"
                    }
                ]
            }
        }

class Age(Quantity):
    class Config:
        schema_extra = {
            "example": {
                "value": 30,
                "unit": "years",
                "system": "http://unitsofmeasure.org",
                "code": "a"
            }
        }

class CodeableReference(Element):
    concept: Optional[CodeableConcept] = Field(
        None,
        description="A reference to a concept."
    )
    reference: Optional[Reference] = Field(
        None,
        description="A reference to another resource."
    )

    class Config:
        schema_extra = {
            "example": {
                "concept": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "123456",
                            "display": "Example concept"
                        }
                    ],
                    "text": "Example concept text"
                },
                "reference": {
                    "reference": "Patient/example"
                }
            }
        }

class Count(Quantity):
    class Config:
        schema_extra = {
            "example": {
                "value": 10,
                "unit": "times",
                "system": "http://unitsofmeasure.org",
                "code": "count"
            }
        }

class Distance(Quantity):
    class Config:
        schema_extra = {
            "example": {
                "value": 5,
                "unit": "km",
                "system": "http://unitsofmeasure.org",
                "code": "km"
            }
        }

class Duration(Quantity):
    class Config:
        schema_extra = {
            "example": {
                "value": 30,
                "unit": "minutes",
                "system": "http://unitsofmeasure.org",
                "code": "min"
            }
        }

class ContactDetail(Element):
    name: Optional[fhirtypes.String] = Field(
        None,
        description="The name of the individual to contact."
    )
    telecom: Optional[List[ContactPoint]] = Field(
        default_factory=list,
        description="The contact details for the individual."
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "telecom": [
                    {
                        "system": "phone",
                        "value": "(555) 555-5555",
                        "use": "work"
                    }
                ]
            }
        }

class Contributor(Element):
    type: fhirtypes.Code = Field(
        ...,
        description="The type of contributor."
    )
    name: fhirtypes.String = Field(
        ...,
        description="The name of the contributor."
    )
    contact: Optional[List[ContactDetail]] = Field(
        default_factory=list,
        description="The contact details of the contributor."
    )

    class Config:
        schema_extra = {
            "example": {
                "type": "author",
                "name": "Jane Smith",
                "contact": [
                    {
                        "name": "John Doe",
                        "telecom": [
                            {
                                "system": "phone",
                                "value": "(555) 555-5555",
                                "use": "work"
                            }
                        ]
                    }
                ]
            }
        }

class DataRequirement(Element):
    type: fhirtypes.Code = Field(
        ...,
        description="The type of data."
    )
    profile: Optional[List[fhirtypes.Canonical]] = Field(
        default_factory=list,
        description="The profile of the data."
    )
    subjectCodeableConcept: Optional[CodeableConcept] = Field(
        None,
        description="The codeable concept of the subject."
    )
    subjectReference: Optional[Reference] = Field(
        None,
        description="The reference of the subject."
    )

    class Config:
        schema_extra = {
            "example": {
                "type": "Observation",
                "profile": [
                    "http://hl7.org/fhir/StructureDefinition/vitalsigns"
                ],
                "subjectCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "123456",
                            "display": "Example subject"
                        }
                    ],
                    "text": "Example subject text"
                },
                "subjectReference": {
                    "reference": "Patient/example"
                }
            }
        }

class Expression(Element):
    description: Optional[fhirtypes.String] = Field(
        None,
        description="A brief, natural language description of the condition."
    )
    name: Optional[fhirtypes.Id] = Field(
        None,
        description="A short name assigned to the expression to allow for multiple reuse."
    )
    language: fhirtypes.Code = Field(
        ...,
        description="The media type of the language for the expression."
    )
    expression: Optional[fhirtypes.String] = Field(
        None,
        description="An expression in the specified language that returns a value."
    )
    reference: Optional[fhirtypes.Uri] = Field(
        None,
        description="A URI that provides a reference to the expression."
    )

    class Config:
        schema_extra = {
            "example": {
                "description": "Example expression",
                "name": "ExampleExpression",
                "language": "text/fhirpath",
                "expression": "Patient.name.given",
                "reference": "http://example.org/fhirpath"
            }
        }



class Extension(Element):
    url: fhirtypes.Uri = Field(
        ...,
        description="Source of the definition for the extension code - a logical name or a URL."
    )
    valueBase64Binary : Optional[fhirtypes.Base64Binary] = None
    valueBoolean : Optional[fhirtypes.Boolean] = None
    valueCanonical : Optional[fhirtypes.Canonical] = None
    valueCode : Optional[fhirtypes.Code] = None
    valueDate : Optional[fhirtypes.Date] = None
    valueDateTime : Optional[fhirtypes.DateTime] = None
    valueDecimal : Optional[fhirtypes.Decimal] = None
    valueId : Optional[fhirtypes.Id] = None
    valueInstant : Optional[fhirtypes.Instant] = None
    valueInteger : Optional[fhirtypes.Integer] = None
    valueMarkdown : Optional[fhirtypes.Markdown] = None
    valueOid : Optional[fhirtypes.Oid] = None
    valuePositiveInt : Optional[fhirtypes.PositiveInt] = None
    valueString : Optional[fhirtypes.String] = None
    valueTime : Optional[fhirtypes.Time] = None
    valueUnsignedInt : Optional[fhirtypes.UnsignedInt] = None
    valueUri : Optional[fhirtypes.Uri] = None
    valueUrl : Optional[fhirtypes.Url] = None
    valueUuid : Optional[fhirtypes.Uuid] = None
    valueAddress : Optional[Address] = None
    valueAge : Optional[Age] = None
    valueAnnotation : Optional[Annotation] = None
    valueAttachment : Optional[Attachment] = None
    valueCodeableConcept : Optional[CodeableConcept] = None
    valueCodeableReference : Optional[CodeableReference] = None
    valueCoding : Optional[Coding] = None
    valueContactPoint : Optional[ContactPoint] = None
    valueCount : Optional[Count] = None
    valueDistance : Optional[Distance] = None
    valueDuration : Optional[Duration] = None
    valueHumanName : Optional[HumanName] = None
    valueIdentifier : Optional[Identifier] = None
    valueMoney :  Optional[Money] = None
    valuePeriod :  Optional[Period] = None
    valueQuantity :  Optional[Quantity] = None
    valueRange :  Optional[Range] = None
    valueRatio :  Optional[Ratio] = None
    valueRatioRange :  Optional[RatioRange] = None
    valueReference :  Optional[Reference] = None
    valueSampledData :  Optional[SampledData] = None
    valueSignature :  Optional[Signature] = None
    valueTiming :  Optional[Timing] = None
    valueContactDetail :  Optional[ContactDetail] = None
    valueContributor :  Optional[Contributor] = None
    valueDataRequirement :  Optional[DataRequirement] = None
    valueExpression :  Optional[Expression] = None
    # valueParameterDefinition :  Optional[ParameterDefinition] = None
    # valueRelatedArtifact :  Optional[RelatedArtifact] = None
    # valueTriggerDefinition :  Optional[TriggerDefinition] = None
    # valueUsageContext :  Optional[UsageContext] = None
    # valueDosage :  Optional[Dosage] = None

    # @root_validator(pre=True)
    # def check_value_x(cls, values):
    #     value_fields = ['valueInteger', 'valueString', 'valueBoolean', 'valueDateTime', 'valueCode']
    #     value_count = sum([1 for field in value_fields if values.get(field) is not None])
    #     if value_count > 1:
    #         raise ValueError("Only one of the value[x] fields can be set.")
    #     return values

    class Config:
        schema_extra = {
            "example": {
                "url": "http://example.org/fhir/StructureDefinition/example",
                "valueString": "example value"
            }
        }