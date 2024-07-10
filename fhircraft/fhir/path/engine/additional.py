
"""
FHIR adds (compatible) functionality to the set of common FHIRPath functions. Some of these functions
are candidates for elevation to the base version of FHIRPath when the next version is released. 
"""

from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, FHIRPathFunction, Invocation, Element, Operation, FHIRPath, FHIRPathError
from fhircraft.fhir.path.engine.filtering import Where
from fhircraft.fhir.resources.datatypes.primitives import Uri, Canonical, Url
from fhircraft.utils import ensure_list, load_url
from typing import List, Any, Optional
import operator



class Extension(FHIRPathFunction):
    """
    A representation of the FHIRPath [`extension()`](https://build.fhir.org/fhirpath.html#functions) function.

    Attributes:
        url (str): URL to query the extensions.
    
    Note:
        This class is a syntactical shortcut equivalent to:

            Invocation(Element('extension'), Where(Operation(Element('url'), operator.eq, url))) 
    """
    def __init__(self, url: str):
        self.url = url

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> List[FHIRPathCollectionItem]:
        """
        Filters the input collection for items named `extension` with the given `url`.
        Will return an empty collection if the input collection is empty or the url is empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            List[FHIRPathCollectionItem]): The indexed collection item.
        """
        collection = ensure_list(collection)
        return Invocation(Element('extension'), Where(Operation(Element('url'), operator.eq, self.url))).evaluate(collection, create=False) 

    def __str__(self):
        return f'Extension("{self.url}")'

    def __repr__(self):
        return f'Extension("{self.url}")'
    
    def __eq__(self, other):
        return isinstance(other, Extension) and other.url == self.url

    def __hash__(self):
        return hash((self.url))


class TypeChoice(FHIRPath):
    
    def __init__(self, type_choice_name):
        self.type_choice_name = type_choice_name

    def evaluate(self, collection, *args, **kwargs):
        collection = ensure_list(collection)
        return  [
            FHIRPathCollectionItem(getattr(item.value, field), path=Element(field), parent=item) 
                for item in collection
                    for field in item.value.model_fields.keys() 
                        if field.startswith(self.type_choice_name) and getattr(item.value, field) 
        ]

    def __str__(self):
        return f'{self.type_choice_name}[x]'

    def __repr__(self):
        return f'{self.type_choice_name}[x]'
    
    def __eq__(self, other):
        return isinstance(other, TypeChoice) and other.type_choice_name == self.type_choice_name

    def __hash__(self):
        return hash((self.type_choice_name))




class HasValue(FHIRPathFunction):
    """
    A representation of the FHIRPath [`hasValue()`](https://build.fhir.org/fhirpath.html#functions) function.
    """
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Returns true if the input collection contains a single value which is a FHIR primitive, and it has a primitive
        value (e.g. as opposed to not having a value and just having extensions). Otherwise, the return value is empty. 

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            bool
        """
        collection = ensure_list(collection)
        if len(collection) != 1:
            return False
        item = collection[0]
        return item.value is not None



class GetValue(FHIRPathFunction):
    """
    A representation of the FHIRPath [`getValue()`](https://build.fhir.org/fhirpath.html#functions) function.
    """
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> Any:
        """
        Return the underlying system value for the FHIR primitive if the input collection contains a single
        value which is a FHIR primitive, and it has a primitive value (see discussion for hasValue()). Otherwise the return value is empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            Any: Value
        """
        collection = ensure_list(collection)
        if not HasValue().evaluate(collection):
            return []
        item = collection[0]
        return item.value


class Resolve(FHIRPathFunction):
    """
    A representation of the FHIRPath [`resolve()`](https://build.fhir.org/fhirpath.html#functions) function.
    """
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> List[FHIRPathCollectionItem]:
        """
        For each item in the collection, if it is a string that is a `uri` (or `canonical` or `url`), locate the target of the
        reference, and add it to the resulting collection. If the item does not resolve to a resource, the item is ignored 
        and nothing is added to the output collection.

        The items in the collection may also represent a `Reference`, in which case the `Reference.reference` is resolved. 
        If the input is empty, the output will be empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            collection (List[FHIRPathCollectionItem])): The output collection.
        """
        from fhircraft.fhir.resources.factory import construct_resource_model
        from fhircraft.fhir.resources.datatypes import get_FHIR_type

        collection = ensure_list(collection)
        output_collection = []
        for item in collection:
            if isinstance(item.value, (Uri, Canonical, Url)):
                resource_url = item.value 
            elif isinstance(item.value, get_FHIR_type('Reference')):
                resource_url = item.value.reference
            else:
                raise FHIRPathError('The resolve() function requires either a collection of URIs, Canonicals, URLs or References.')
            resource = load_url(resource_url)
            profile_url = resource.get('meta',{}).get('profile',[None])[0]
            if profile_url:
                profile = construct_resource_model(profile_url)
                resource = profile.model_validate(resource)
            output_collection.append(resource)
        return output_collection