from typing import Any
import xml.etree.ElementTree as xml

from pydantic import BaseModel, Field, model_serializer, model_validator

from fhircraft.fhir.resources.base.model import FHIRBaseModel
from fhircraft.fhir.resources.base.mixins.xml import XML_NAMESPACE
from fhircraft.utils import get_all_models_from_field


class FHIRPrimitiveModel(FHIRBaseModel):
    """
    Base class for FHIR primitive types.

    FHIR primitives are represented as Pydantic models with a single `value` field that holds the actual primitive value.
    This design allows us to attach extensions to primitive values while still treating them as simple types in most contexts.
    """

    _kind = "primitive-type"

    value: Any | None = Field(default=None, description="The actual value")

    @model_serializer
    def _serialize_root_value(self) -> Any:
        if isinstance(self, FHIRPrimitiveModel):
            return self.value
        return self

    def _serialize_as_json(self, name: str) -> dict:
        serialized = dict()
        if self.value:
            serialized[name] = self.value
        if self.id or self.extension:
            serialized[f"_{name}"] = {}
            if self.id is not None:
                serialized[f"_{name}"]["id"] = self.id
            if self.extension is not None:
                serialized[f"_{name}"]["extension"] = [
                    ext.model_dump() for ext in self.extension
                ]
        return serialized

    def _serialize_as_xml(self, name: str, **kwargs) -> xml.Element:
        attributes = {}
        if self.value is not None:
            attributes["value"] = (
                str(self.value).lower()
                if isinstance(self.value, bool)
                else str(self.value)
            )
        if getattr(self, "id", None) is not None:
            attributes["id"] = self.id
        primitive = xml.Element(f"{{{XML_NAMESPACE}}}{name}", attrib=attributes)
        for ext in self.extension or []:
            primitive.append(ext._serialize_as_xml("extension", **kwargs))
        return primitive

    @classmethod
    def _parse_xml_to_dict(cls, element: xml.Element) -> dict:
        element_name = element.tag.split("}", 1)[-1]  # Remove namespace
        # Collect extensions if present using the correct Extension type from the field
        extensions = []
        extension_field = cls.model_fields.get("extension")
        if extension_field is not None:
            extension_type = next(get_all_models_from_field(extension_field), None)
            if extension_type is not None and issubclass(extension_type, FHIRBaseModel):
                for ext_element in element.findall(f"{{{XML_NAMESPACE}}}extension"):
                    ext_result = extension_type._parse_xml_to_dict(ext_element)
                    ext_data = ext_result.get("extension")
                    if ext_data is not None:
                        extensions.append(ext_data)
        # Extract the "id" attribute if present
        elem_id = element.attrib.get("id")
        # Extract the "value" attribute if present, converting boolean strings to actual booleans
        value = element.attrib.get("value")
        if value is not None:
            # Convert boolean strings
            if value == "true":
                value = True
            elif value == "false":
                value = False

        deserialized_data = {}
        if value is not None:
            deserialized_data[element_name] = value
        if elem_id is not None or extensions:
            deserialized_data[f"_{element_name}"] = {}
        if elem_id is not None:
            deserialized_data[f"_{element_name}"]["id"] = elem_id
        if extensions:
            deserialized_data[f"_{element_name}"]["extension"] = extensions
        return deserialized_data

    @model_validator(mode="before")
    @classmethod
    def coerce_root_value(cls, data: Any) -> Any:
        if isinstance(data, FHIRPrimitiveModel):
            return {"value": data.value}
        elif data is not None and not isinstance(data, (dict, BaseModel)):
            return {"value": data}
        return data

    def __init__(self, __value: Any | None = None, **data):
        if __value is not None:
            data.setdefault("value", __value)
        super().__init__(**data)

    def __getattr__(self, name: str):
        v = self.value
        if v is None:
            raise AttributeError(f"Cannot access '{name}' because value is None")
        return getattr(v, name)

    def __getitem__(self, key):
        v = self.value
        if v is None:
            raise TypeError("Cannot index into None value")
        return v[key]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, FHIRPrimitiveModel):
            return self.value == other.value
        return self.value == other

    def __gt__(self, other):
        return (
            self.value > other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value > other
        )

    def __rgt__(self, other):
        return (
            self.value < other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value < other
        )

    def __lt__(self, other):
        return (
            self.value < other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value < other
        )

    def __rlt__(self, other):
        return (
            self.value > other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value > other
        )

    def __ge__(self, other):
        return (
            self.value >= other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value >= other
        )

    def __rge__(self, other):
        return (
            self.value <= other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value <= other
        )

    def __le__(self, other):
        return (
            self.value <= other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value <= other
        )

    def __rle__(self, other):
        return (
            self.value >= other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value >= other
        )

    def __add__(self, other):
        return (
            self.value + other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value + other
        )

    def __radd__(self, other):
        return (
            other.value + self.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else other + self.value
        )

    def __sub__(self, other):
        return (
            self.value - other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value - other
        )

    def __rsub__(self, other):
        return (
            other.value - self.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else other - self.value
        )

    def __mul__(self, other):
        return (
            self.value * other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value * other
        )

    def __rmul__(self, other):
        return (
            self.value * other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value * other
        )

    def __truediv__(self, other):
        return (
            self.value / other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value / other
        )

    def __rtruediv__(self, other):
        return (
            other.value / self.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else other / self.value
        )

    def __mod__(self, other):
        return (
            self.value % other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value % other
        )

    def __rmod__(self, other):
        return (
            other.value % self.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else other % self.value
        )

    def __floordiv__(self, other):
        return (
            self.value // other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value // other
        )

    def __rfloordiv__(self, other):
        return (
            other.value // self.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else other // self.value
        )

    def __neg__(self):
        return -self.value  # type: ignore

    def __pos__(self):
        return +self.value  # type: ignore

    def __abs__(self):
        return abs(self.value)  # type: ignore

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return str(self.value) if self.value is not None else ""

    def __repr__(self) -> str:
        return repr(self.value)


class StringBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR string types
    """

    _kind = "string"
    value: str | None = None


class BooleanBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR boolean types
    """

    _kind = "boolean"
    value: bool | None = None


class DecimalBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR decimal types
    """

    _kind = "decimal"
    value: float | None = None


class DateBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR date types
    """

    _kind = "date"
    value: str | None = None


class DateTimeBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR dateTime types
    """

    _kind = "dateTime"
    value: str | None = None


class TimeBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR time types
    """

    _kind = "time"
    value: str | None = None


class InstantBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR instant types
    """

    _kind = "instant"
    value: str | None = None


class Base64BinaryBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR base64Binary types
    """

    _kind = "base64Binary"
    value: str | None = None


class UriBase(StringBase):
    """
    A release-independent base metaclass for FHIR uri types
    """

    _kind = "uri"


class UrlBase(UriBase):
    """
    A release-independent base metaclass for FHIR url types
    """

    _kind = "url"


class CanonicalBase(UriBase):
    """
    A release-independent base metaclass for FHIR canonical types
    """

    _kind = "canonical"


class OidBase(UriBase):
    """
    A release-independent base metaclass for FHIR oid types
    """

    _kind = "oid"


class UuidBase(UriBase):
    """
    A release-independent base metaclass for FHIR uuid types
    """

    _kind = "uuid"


class CodeBase(StringBase):
    """
    A release-independent base metaclass for FHIR code types
    """

    _kind = "code"


class IdBase(StringBase):
    """
    A release-independent base metaclass for FHIR id types
    """

    _kind = "id"


class MarkdownBase(StringBase):
    """
    A release-independent base metaclass for FHIR markdown types
    """

    _kind = "markdown"


class XhtmlBase(StringBase):
    """
    A release-independent base metaclass for FHIR xhtml types
    """

    _kind = "xhtml"


class IntegerBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR integer types
    """

    _kind = "integer"
    value: int | None = None


class PositiveIntBase(IntegerBase):
    """
    A release-independent base metaclass for FHIR positiveInt types
    """

    _kind = "positiveInt"


class UnsignedIntBase(IntegerBase):
    """
    A release-independent base metaclass for FHIR unsignedInt types
    """

    _kind = "unsignedInt"


class Integer64Base(IntegerBase):
    """
    A release-independent base metaclass for FHIR integer64 types (R5)
    """

    _kind = "integer64"
