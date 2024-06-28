"""The filtering module contains the object representations of the combining-category FHIRPath functions."""

from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, FHIRPathFunction
from fhircraft.utils import ensure_list
from typing import List

class Union(FHIRPathFunction):
    """
    A representation of the FHIRPath [`union()`](https://hl7.org/fhirpath/N1/#unionother-collection) function.

    Attributes:
        other_collection (List[FHIRPathCollectionItem]): The other collection to combine with.
    """
    def __init__(self, other_collection: List[FHIRPathCollectionItem]):
        self.other_collection = ensure_list(other_collection)

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> List[FHIRPathCollectionItem]:
        """
        Merge the two collections into a single collection, eliminating any duplicate values. 
        
        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            List[FHIRPathCollectionItem]): The output collection.
        """ 
        collection = ensure_list(collection)
        return sorted(list(set(collection) | set(self.other_collection)), key=lambda item: item.value)


class Combine(FHIRPathFunction):
    """
    A representation of the FHIRPath [`combine()`](https://hl7.org/fhirpath/N1/#combineother-collection-collection) function.

    Attributes:
        other_collection (List[FHIRPathCollectionItem]): The other collection to combine with.
    """
    def __init__(self, other_collection: List[FHIRPathCollectionItem]):
        self.other_collection = ensure_list(other_collection)

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> List[FHIRPathCollectionItem]:
        """
        Merge the input and other collections into a single collection without eliminating duplicate
        values. Combining an empty collection with a non-empty collection will return the non-empty
        collection.
        
        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            List[FHIRPathCollectionItem]): The output collection.
        """ 
        collection = ensure_list(collection)
        return collection + self.other_collection
