"""
FHIR adds (compatible) functionality to the set of common FHIRPath functions. Some of these functions
are candidates for elevation to the base version of FHIRPath when the next version is released.
"""

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

        if len(collection) > 1:
            raise FHIRPathError(
                f"FHIRPath operator {self.__str__()} expected a single-item collection, instead got a {len(collection)}-items collection."
            )
        value = collection[0]
        # TODO: Implement HTML validity check
        return [FHIRPathCollectionItem.wrap(True)]
