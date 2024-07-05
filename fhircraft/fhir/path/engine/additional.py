
"""
FHIR adds (compatible) functionality to the set of common FHIRPath functions. Some of these functions
are candidates for elevation to the base version of FHIRPath when the next version is released. 
"""

from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, FHIRPathFunction, Invocation, Element, Operation, FHIRPath
import operator
from fhircraft.fhir.path.engine.filtering import Where
from fhircraft.utils import ensure_list
from typing import List, Any, Optional



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
