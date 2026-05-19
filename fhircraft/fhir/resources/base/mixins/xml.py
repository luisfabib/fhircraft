"""
XML serialization/deserialization mixin for FHIRBaseModel.

Keeps all XML (de)serialization logic — including the FHIR XML namespace constant and the
namespace registration side-effect — in one place.
"""

import xml.etree.ElementTree as xml
from typing import Any, TYPE_CHECKING, Type, TypeVar

from pydantic.main import IncEx

from fhircraft.utils import get_all_models_from_field, is_list_field

if TYPE_CHECKING:
    from fhircraft.fhir.resources.base.models import FHIRBaseModel

T = TypeVar("T", bound="FHIRXMLMixin")

XML_NAMESPACE = "http://hl7.org/fhir"
xml.register_namespace("", XML_NAMESPACE)  # Register as the default FHIR XML namespace


class FHIRXMLMixin:
    """
    Mixin providing XML serialization and deserialization for FHIR models.

    Implements the FHIR XML format as described in the FHIR specification,
    including correct handling of primitive shadow elements and namespace.
    """

    def model_dump_xml(
        self,
        *,
        indent: int | None = None,
        ensure_ascii: bool = True,
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        exclude_unset: bool = False,
        exclude_none: bool = False,
        exclude_defaults: bool = False,
    ) -> str:
        """
        Serialize the FHIR resource to an XML string.

        Args:
            indent: Number of indent levels.  ``None`` produces compact output.
            ensure_ascii: When True, non-ASCII characters are escaped.
            include: Fields to include (passed through to model_dump).
            exclude: Fields to exclude (passed through to model_dump).
            exclude_unset: Exclude fields that were not explicitly set.
            exclude_none: Exclude fields whose value is None.
            exclude_defaults: Exclude fields that equal their default value.

        Returns:
            An XML string conforming to the FHIR XML format.
        """
        root_el = self._serialize_as_xml(
            name=self._type,  # type: ignore[attr-defined]
            include=include,
            exclude=exclude,
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
        )
        tree = xml.ElementTree(root_el)
        if indent is not None:
            xml.indent(tree, space="  " * indent)
        return xml.tostring(
            root_el,
            encoding="unicode" if ensure_ascii else "unicode",
            xml_declaration=True,
        )

    @classmethod
    def model_validate_xml(
        cls: Type[T],
        xml_data: str,
        *,
        strict: bool | None = None,
        context: Any = None,
    ) -> T:
        """
        Deserialize a FHIR XML string into a model instance.

        Args:
            xml_data: The XML string to deserialize.
            strict: Whether to validate strictly.
            context: Additional context forwarded to model_validate.

        Returns:
            A validated model instance populated from the XML data.
        """
        root_el = xml.fromstring(xml_data)
        data = cls._parse_xml_to_dict(root_el)
        inner = next(iter(data.values()), {})
        return cls.model_validate(inner, strict=strict, context=context)  # type: ignore[attr-defined]

    # ------------------------------------------------------------------
    # Private XML processing methods
    # ------------------------------------------------------------------

    def _serialize_as_xml(self, name: str, **kwargs: Any) -> xml.Element:
        """
        Serialize this model instance as an ``xml.Element`` (not a string).

        Args:
            name: The XML element tag name (without namespace).
            **kwargs: Additional keyword arguments forwarded to model_dump.

        Returns:
            An ``xml.Element`` representing this model.
        """
        from fhircraft.fhir.resources.base.models import FHIRBaseModel, FHIRList

        element = xml.Element(f"{{{XML_NAMESPACE}}}{name}")

        for subelement_name in self.model_dump(**kwargs):  # type: ignore[attr-defined]
            if subelement := getattr(self, subelement_name, None):
                if isinstance(subelement, FHIRBaseModel):
                    element.append(
                        subelement._serialize_as_xml(subelement_name, **kwargs)
                    )
                elif isinstance(subelement, (list, FHIRList)):
                    for item in subelement:
                        if isinstance(item, FHIRBaseModel):
                            element.append(
                                item._serialize_as_xml(subelement_name, **kwargs)
                            )

        # Extension.url is an XML attribute, not a child element.
        if self._type == "Extension" and getattr(self, "url", None) is not None:  # type: ignore[attr-defined]
            element.attrib["url"] = self.url  # type: ignore[attr-defined]

        # Resource id is an XML attribute, not a child element.
        if getattr(self, "id", None) is not None:
            element.attrib["id"] = self.id  # type: ignore[attr-defined]

        return element

    @classmethod
    def _parse_xml_to_dict(cls, element: xml.Element) -> dict[str, Any]:
        """
        Recursively parse an ``xml.Element`` into a dict suitable for model_validate.

        Returns a dict keyed by the element's local name (namespace stripped),
        whose value is the field-level data dictionary.

        Args:
            element: The XML element to parse.

        Returns:
            ``{element_local_name: {field: value, ...}}``
        """
        from fhircraft.fhir.resources.base.models import FHIRBaseModel

        deserialized_data: dict[str, Any] = {}
        element_name = element.tag.split("}", 1)[-1]  # Strip namespace

        for field, field_info in cls.model_fields.items():  # type: ignore[attr-defined]
            # Some fields are encoded as XML attributes rather than child elements.
            if field == "url" and (url := element.attrib.get("url")):
                deserialized_data["url"] = url
                continue
            if field == "id" and (_id := element.attrib.get("id")):
                deserialized_data["id"] = _id
                continue
            if field == "value" and (value := element.attrib.get("value")):
                deserialized_data["value"] = value
                continue

            field_type = next(get_all_models_from_field(field_info), None)
            if field_type is not None and not issubclass(field_type, FHIRBaseModel):
                continue

            if is_list_field(field_info):
                children = element.findall(f"{{{XML_NAMESPACE}}}{field}")
                if children and field_type is not None:
                    values: list = []
                    shadows: list = []
                    has_shadow = False
                    for child in children:
                        child_result = field_type._parse_xml_to_dict(child)
                        item_value = child_result.get(field)
                        shadow_value = child_result.get(f"_{field}")
                        values.append(item_value)
                        if shadow_value is not None:
                            shadows.append(shadow_value)
                            has_shadow = True
                        else:
                            shadows.append(None)
                    deserialized_data[field] = values
                    if has_shadow:
                        deserialized_data[f"_{field}"] = shadows
            else:
                child = element.find(f"{{{XML_NAMESPACE}}}{field}")
                if child is not None and field_type is not None:
                    deserialized_data.update(field_type._parse_xml_to_dict(child))

        return {element_name: deserialized_data}
