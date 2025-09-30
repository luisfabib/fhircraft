"""
FHIR adds (compatible) functionality to the set of common FHIRPath functions. Some of these functions
are candidates for elevation to the base version of FHIRPath when the next version is released.
"""

import calendar
import re
import sys
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

from fhircraft.fhir.path.engine.core import (
    Element,
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathError,
    FHIRPathFunction,
    Invocation,
    Literal,
)
from fhircraft.fhir.path.engine.equality import Equals
from fhircraft.fhir.path.engine.filtering import Where
from fhircraft.fhir.path.engine.literals import Quantity
from fhircraft.utils import ensure_list, load_url


class Extension(FHIRPathFunction):
    """
    A representation of the FHIRPath [`extension()`](https://build.fhir.org/fhirpath.html#functions) function.

    Attributes:
        url (str): URL to query the extensions.

    Note:
        This class is a syntactical shortcut equivalent to:

            Invocation(Element('extension'), Where(Equals(Element('url'), url)))
    """

    def __init__(self, url: str | Literal):
        if isinstance(url, Literal):
            url = url.value
        if not isinstance(url, str):
            raise FHIRPathError("Extension() argument must be a string.")
        self.url = url

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Filters the input collection for items named `extension` with the given `url`.
        Will return an empty collection if the input collection is empty or the url is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): The output collection.
        """
        return Invocation(
            Element("extension"),
            Where(Equals(Element("url"), [FHIRPathCollectionItem.wrap(self.url)])),
        ).evaluate(collection, environment, create)

    def __str__(self):
        return f'Extension("{self.url}")'

    def __repr__(self):
        return f'Extension("{self.url}")'

    def __eq__(self, other):
        return isinstance(other, Extension) and str(other.url) == str(self.url)

    def __hash__(self):
        return hash((self.url))


class TypeChoice(FHIRPath):

    def __init__(self, type_choice_name: str | Literal):
        if isinstance(type_choice_name, Literal):
            type_choice_name = type_choice_name.value
        if not isinstance(type_choice_name, str):
            raise FHIRPathError("TypeChoice() argument must be a string.")
        self.type_choice_name = type_choice_name

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        return [
            FHIRPathCollectionItem(
                getattr(item.value, field), path=Element(field), parent=item
            )
            for item in collection
            for field in item.value.__class__.model_fields.keys()
            if field.startswith(self.type_choice_name) and getattr(item.value, field)
        ]

    def __str__(self):
        return f"{self.type_choice_name}[x]"

    def __repr__(self):
        return f"{self.type_choice_name}[x]"

    def __eq__(self, other):
        return (
            isinstance(other, TypeChoice)
            and other.type_choice_name == self.type_choice_name
        )

    def __hash__(self):
        return hash((self.type_choice_name))


class HasValue(FHIRPathFunction):
    """
    A representation of the FHIRPath [`hasValue()`](https://build.fhir.org/fhirpath.html#functions) function.
    """

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns true if the input collection contains a single value which is a FHIR primitive, and it has a primitive
        value (e.g. as opposed to not having a value and just having extensions). Otherwise, the return value is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): The output collection.
        """
        if len(collection) != 1:
            has_value = False
        else:
            # TODO: add check for primitive
            item = collection[0]
            has_value = item.value is not None
        return [FHIRPathCollectionItem.wrap(has_value)]


class GetValue(FHIRPathFunction):
    """
    A representation of the FHIRPath [`getValue()`](https://build.fhir.org/fhirpath.html#functions) function.
    """

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Return the underlying system value for the FHIR primitive if the input collection contains a single
        value which is a FHIR primitive, and it has a primitive value (see discussion for hasValue()). Otherwise the return value is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): The output collection.
        """
        if not HasValue().evaluate(collection, environment, create=create):
            return []
        if len(collection) != 1:
            return []
        return [collection[0]]


class Resolve(FHIRPathFunction):
    """
    A representation of the FHIRPath [`resolve()`](https://build.fhir.org/fhirpath.html#functions) function.
    """

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        For each item in the collection, if it is a string that is a `uri` (or `canonical` or `url`), locate the target of the
        reference, and add it to the resulting collection. If the item does not resolve to a resource, the item is ignored
        and nothing is added to the output collection.

        The items in the collection may also represent a `Reference`, in which case the `Reference.reference` is resolved.
        If the input is empty, the output will be empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): The output collection.
        """
        from fhircraft.fhir.resources.factory import construct_resource_model

        output_collection = []
        for item in collection:
            if "Reference" in type(item.value).__name__:
                resource_url = item.value.reference
            elif isinstance(item.value, str):
                resource_url = item.value
            else:
                raise FHIRPathError(
                    "The resolve() function requires either a collection of URIs, Canonicals, URLs or References."
                )
            if not resource_url.startswith("http://") and not resource_url.startswith(
                "https://"
            ):
                return []
            resource = load_url(resource_url)
            profile_url = resource.get("meta", {}).get("profile", [None])[0]
            if profile_url:
                profile = construct_resource_model(profile_url)
                resource = profile.model_validate(resource)
            output_collection.append(resource)
        return output_collection


class HtmlChecks(FHIRPathFunction):
    """
    A representation of the FHIRPath [`htmlChecks()`](https://build.fhir.org/fhirpath.html#functions) function.
    """

    # Allowed HTML elements based on HTML 4.0 chapters 7-11 (except section 4 of chapter 9) and 15
    ALLOWED_ELEMENTS = {
        # Text formatting (chapter 7)
        "b",
        "big",
        "i",
        "s",
        "small",
        "tt",
        "u",
        "strong",
        "em",
        "dfn",
        "code",
        "samp",
        "kbd",
        "var",
        "cite",
        "abbr",
        "acronym",
        "sub",
        "sup",
        "span",
        "bdo",
        # Lists (chapter 10)
        "ul",
        "ol",
        "li",
        "dl",
        "dt",
        "dd",
        # Tables (chapter 11)
        "table",
        "caption",
        "thead",
        "tbody",
        "tfoot",
        "colgroup",
        "col",
        "tr",
        "th",
        "td",
        # Block elements (chapter 8)
        "div",
        "p",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "blockquote",
        "pre",
        "address",
        # Links and images (chapter 15 + special allowance)
        "a",
        "img",
        # Line breaks
        "br",
        "hr",
    }

    # Forbidden elements that must not be present
    FORBIDDEN_ELEMENTS = {
        "head",
        "body",
        "html",
        "script",
        "form",
        "input",
        "button",
        "select",
        "textarea",
        "base",
        "link",
        "meta",
        "title",
        "style",
        "object",
        "embed",
        "applet",
        "frame",
        "frameset",
        "iframe",
        "noframes",
    }

    # Event attributes that are not allowed
    EVENT_ATTRIBUTES = {
        "onclick",
        "ondblclick",
        "onmousedown",
        "onmouseup",
        "onmouseover",
        "onmousemove",
        "onmouseout",
        "onfocus",
        "onblur",
        "onkeypress",
        "onkeydown",
        "onkeyup",
        "onsubmit",
        "onreset",
        "onselect",
        "onchange",
        "onload",
        "onunload",
    }

    class XHTMLValidator(HTMLParser):
        def __init__(self):
            super().__init__()
            self.errors = []
            self.has_content = False
            self.in_div = False
            self.div_count = 0

        def handle_starttag(self, tag, attrs):
            # Check if this is the root div
            if tag == "div":
                self.div_count += 1
                if self.div_count == 1:
                    self.in_div = True
                    # Check for required xmlns attribute
                    xmlns_found = False
                    for attr_name, attr_value in attrs:
                        if (
                            attr_name == "xmlns"
                            and attr_value == "http://www.w3.org/1999/xhtml"
                        ):
                            xmlns_found = True
                        elif attr_name.lower() in HtmlChecks.EVENT_ATTRIBUTES:
                            self.errors.append(
                                f"Event attribute '{attr_name}' is not allowed"
                            )
                    if not xmlns_found and self.div_count == 1:
                        self.errors.append(
                            "Root div element must have xmlns='http://www.w3.org/1999/xhtml'"
                        )

            # Check if element is allowed
            if tag.lower() not in HtmlChecks.ALLOWED_ELEMENTS:
                if tag.lower() in HtmlChecks.FORBIDDEN_ELEMENTS:
                    self.errors.append(f"Forbidden element '{tag}' found")
                else:
                    self.errors.append(f"Element '{tag}' is not in the allowed set")

            # Check attributes for event handlers and external references
            for attr_name, attr_value in attrs:
                attr_lower = attr_name.lower()

                # Check for event attributes
                if attr_lower in HtmlChecks.EVENT_ATTRIBUTES:
                    self.errors.append(
                        f"Event attribute '{attr_name}' is not allowed on '{tag}'"
                    )

                # Check for external stylesheet references
                if (
                    tag.lower() == "link"
                    and attr_value
                    and attr_lower == "rel"
                    and "stylesheet" in attr_value.lower()
                ):
                    self.errors.append("External stylesheet references are not allowed")

                # Check for external script sources
                if tag.lower() == "script" and attr_lower == "src":
                    self.errors.append("External script references are not allowed")

        def handle_endtag(self, tag):
            if tag == "div":
                self.div_count -= 1
                if self.div_count == 0:
                    self.in_div = False

        def handle_data(self, data):
            if self.in_div and data.strip():
                self.has_content = True

        def handle_startendtag(self, tag, attrs):
            # Handle self-closing tags like <img/>, <br/>
            if tag == "img" and self.in_div:
                self.has_content = True
            self.handle_starttag(tag, attrs)

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        When invoked on a single xhtml element returns true if the rules around HTML usage are met, and false if they are not.
        The return value is empty on any other kind of element, or a collection of xhtml elements.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            bool

        Raises:
            FHIRPathError: If the collection is not a single item.
        """

        collection = ensure_list(collection)

        if len(collection) != 1:
            return []  # Return empty for non-single collections

        item = collection[0]

        # Check if the item is an XHTML string
        if not isinstance(item.value, str):
            return []  # Return empty for non-string values

        xhtml_content = item.value.strip()

        if not xhtml_content:
            return [FHIRPathCollectionItem.wrap(False)]

        try:
            # Basic XML well-formedness check
            try:
                ET.fromstring(xhtml_content)
            except ET.ParseError:
                return [FHIRPathCollectionItem.wrap(False)]

            # Check if it starts with a div element
            if not re.match(r"^\s*<div\s", xhtml_content, re.IGNORECASE):
                return [FHIRPathCollectionItem.wrap(False)]

            # Validate HTML structure and content
            validator = self.XHTMLValidator()
            validator.feed(xhtml_content)

            # Check validation results
            if validator.errors:
                return [FHIRPathCollectionItem.wrap(False)]

            # Check if div has non-whitespace content
            if not validator.has_content:
                return [FHIRPathCollectionItem.wrap(False)]

            # Check for HTML entities (not allowed, should use Unicode)
            if re.search(
                r"&(?!#\d+;|#x[0-9a-fA-F]+;|amp;|lt;|gt;|quot;|apos;)", xhtml_content
            ):
                return [FHIRPathCollectionItem.wrap(False)]

            return [FHIRPathCollectionItem.wrap(True)]

        except Exception:
            return [FHIRPathCollectionItem.wrap(False)]


class ElementDefinition(FHIRPathFunction):
    """
    A representation of the FHIRPath [`elementDefinition()`](https://www.hl7.org/fhir/fhirpath.html) function.
    """

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the FHIR element definition information for each element in the input collection.
        If the input collection is empty, the return value will be empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Raises:
            NotImplementedError: This FHIRPath function is not supported.
        """
        raise NotImplementedError(
            "The FHIRPath elementDefinition() function is not supported."
        )


class LowBoundary(FHIRPathFunction):
    """
    A representation of the FHIRPath [`lowBoundary()`](https://www.hl7.org/fhir/fhirpath.html) function.
    """

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the low boundary of a quantity or range based on precision.
        For date/time values, returns the earliest possible moment.
        For decimal values, returns the lowest value within precision range.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): The output collection.
        """
        if not collection:
            return []

        result = []
        for item in collection:
            value = item.value

            if isinstance(value, str):
                # Handle date/time strings
                if self._is_datetime_string(value):
                    low_boundary = self._get_datetime_low_boundary(value)
                    result.append(FHIRPathCollectionItem.wrap(low_boundary))
                else:
                    result.append(item)  # Return as-is for non-datetime strings
            elif isinstance(value, (int, float)):
                # Handle numeric values - determine precision and calculate boundary
                low_boundary = self._get_numeric_low_boundary(value)
                result.append(FHIRPathCollectionItem.wrap(low_boundary))
            elif isinstance(value, Quantity):
                # Handle Quantity type
                new_quantity = Quantity(
                    value=self._get_numeric_low_boundary(value.value),
                    unit=value.unit if hasattr(value, "unit") else None,
                )
                result.append(FHIRPathCollectionItem.wrap(new_quantity))
            else:
                result.append(item)  # Return as-is for other types

        return result

    def _is_datetime_string(self, value: str) -> bool:
        """Check if string represents a date/time value"""
        # Match FHIR date/datetime patterns
        datetime_pattern = r"^\d{4}(-\d{2}(-\d{2}(T\d{2}(:\d{2}(:\d{2}(\.\d+)?)?)?(Z|[+-]\d{2}:\d{2})?)?)?)?$"
        return bool(re.match(datetime_pattern, value))

    def _get_datetime_low_boundary(self, value: str) -> str:
        """Get the earliest possible moment for a date/time string"""
        if len(value) == 4:  # Year only: @2018
            return f"{value}-01-01T00:00:00.000"
        elif len(value) == 7:  # Year-month: @2018-03
            return f"{value}-01T00:00:00.000"
        elif len(value) == 10:  # Date: @2018-03-15
            return f"{value}T00:00:00.000"
        elif (
            "T" in value
            and not value.endswith("Z")
            and "+" not in value
            and "-" not in value[-6:]
        ):
            # Incomplete time, fill with zeros
            if value.count(":") == 0:  # Only hour
                return f"{value}:00:00.000"
            elif value.count(":") == 1:  # Hour and minute
                return f"{value}:00.000"
            else:
                return f"{value}.000" if "." not in value else value
        else:
            return value  # Already complete or has timezone

    def _get_numeric_low_boundary(self, value) -> float:
        """Get the low boundary for a numeric value based on precision"""
        if isinstance(value, int):
            # Integer precision: boundary is value - 0.5
            return value
        elif isinstance(value, float):
            # Determine decimal places for precision
            return value - sys.float_info.epsilon
        return value


class HighBoundary(FHIRPathFunction):
    """
    A representation of the FHIRPath [`highBoundary()`](https://www.hl7.org/fhir/fhirpath.html) function.
    """

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the high boundary of a quantity or range based on precision.
        For date/time values, returns the latest possible moment.
        For decimal values, returns the highest value within precision range.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): The output collection.
        """
        if not collection:
            return []

        result = []
        for item in collection:
            value = item.value

            if isinstance(value, str):
                # Handle date/time strings
                if self._is_datetime_string(value):
                    high_boundary = self._get_datetime_high_boundary(value)
                    result.append(FHIRPathCollectionItem.wrap(high_boundary))
                else:
                    result.append(item)  # Return as-is for non-datetime strings
            elif isinstance(value, (int, float)):
                # Handle numeric values - determine precision and calculate boundary
                high_boundary = self._get_numeric_high_boundary(value)
                result.append(FHIRPathCollectionItem.wrap(high_boundary))
            elif isinstance(value, Quantity):
                # Handle Quantity type
                new_quantity = Quantity(
                    value=self._get_numeric_high_boundary(value.value),
                    unit=value.unit if hasattr(value, "unit") else None,
                )
                result.append(FHIRPathCollectionItem.wrap(new_quantity))
            else:
                result.append(item)  # Return as-is for other types

        return result

    def _is_datetime_string(self, value: str) -> bool:
        """Check if string represents a date/time value"""
        datetime_pattern = r"^\d{4}(-\d{2}(-\d{2}(T\d{2}(:\d{2}(:\d{2}(\.\d+)?)?)?(Z|[+-]\d{2}:\d{2})?)?)?)?$"
        return bool(re.match(datetime_pattern, value))

    def _get_datetime_high_boundary(self, value: str) -> str:
        """Get the latest possible moment for a date/time string"""
        import calendar

        if len(value) == 4:  # Year only: @2018
            return f"{value}-12-31T23:59:59.999"
        elif len(value) == 7:  # Year-month: @2018-03
            year, month = map(int, value.split("-"))
            last_day = calendar.monthrange(year, month)[1]
            return f"{value}-{last_day:02d}T23:59:59.999"
        elif len(value) == 10:  # Date: @2018-03-15
            return f"{value}T23:59:59.999"
        elif (
            "T" in value
            and not value.endswith("Z")
            and "+" not in value
            and "-" not in value[-6:]
        ):
            # Incomplete time, fill with maximum values
            if value.count(":") == 0:  # Only hour
                return f"{value}:59:59.999"
            elif value.count(":") == 1:  # Hour and minute
                return f"{value}:59.999"
            else:
                return f"{value}.999" if "." not in value else value
        else:
            return value  # Already complete or has timezone

    def _get_numeric_high_boundary(self, value) -> float:
        """Get the high boundary for a numeric value based on precision"""
        if isinstance(value, int):
            # Integer precision: boundary is value + 0.5 (exclusive)
            return value
        elif isinstance(value, float):
            # Determine decimal places for precision
            return value + sys.float_info.epsilon
        return value
