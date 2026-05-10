from .model import FHIRBaseModel, FHIRSliceModel, FhirBaseModelKind

XML_NAMESPACE = "http://hl7.org/fhir"

from .list import FHIRList
from .primitives import (
    FHIRPrimitiveModel,
    StringBase,
    BooleanBase,
    IntegerBase,
    DecimalBase,
    DateBase,
    DateTimeBase,
    TimeBase,
    UriBase,
    UrlBase,
    CodeBase,
    IdBase,
    OidBase,
    CanonicalBase,
    UuidBase,
    InstantBase,
    MarkdownBase,
    PositiveIntBase,
    UnsignedIntBase,
    Base64BinaryBase,
    XhtmlBase,
    Integer64Base,
)
