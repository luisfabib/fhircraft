"""
FHIR adds (compatible) functionality to the set of common FHIRPath functions. Some of these functions
are candidates for elevation to the base version of FHIRPath when the next version is released.
"""

import re
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
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Filters the input collection for items named `extension` with the given `url`.
        Will return an empty collection if the input collection is empty or the url is empty.

        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection): The indexed collection item.
        """
        return Invocation(
            Element("extension"),
            Where(Equals(Element("url"), [FHIRPathCollectionItem.wrap(self.url)])),
        ).evaluate(collection, create=create)

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
        self, collection: FHIRPathCollection, create=False
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
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Returns true if the input collection contains a single value which is a FHIR primitive, and it has a primitive
        value (e.g. as opposed to not having a value and just having extensions). Otherwise, the return value is empty.

        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            bool
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
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Return the underlying system value for the FHIR primitive if the input collection contains a single
        value which is a FHIR primitive, and it has a primitive value (see discussion for hasValue()). Otherwise the return value is empty.

        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            Any: Value
        """
        if not HasValue().evaluate(collection, create=create):
            return []
        if len(collection) != 1:
            return []
        return [collection[0]]


class Resolve(FHIRPathFunction):
    """
    A representation of the FHIRPath [`resolve()`](https://build.fhir.org/fhirpath.html#functions) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        For each item in the collection, if it is a string that is a `uri` (or `canonical` or `url`), locate the target of the
        reference, and add it to the resulting collection. If the item does not resolve to a resource, the item is ignored
        and nothing is added to the output collection.

        The items in the collection may also represent a `Reference`, in which case the `Reference.reference` is resolved.
        If the input is empty, the output will be empty.

        Args:
            collection (FHIRPathCollection): The input collection.

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
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        When invoked on a single xhtml element returns true if the rules around HTML usage are met, and false if they are not.
        The return value is empty on any other kind of element, or a collection of xhtml elements.

        Args:
            collection (FHIRPathCollection): The input collection.

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
            return [FHIRPathCollectionItem.wrap(False)]
