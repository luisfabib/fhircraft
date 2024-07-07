"""The tree navigation module contains the object representations of the tree-navigation category FHIRPath functions."""

from fhircraft.fhir.path.engine.core import Element, FHIRPathCollectionItem, FHIRPathFunction
from fhircraft.fhir.path.engine.filtering import Repeat
from fhircraft.utils import ensure_list
from pydantic import BaseModel
from typing import List, Optional,Union


class Children(FHIRPathFunction):
    """
    Representation of the FHIRPath [`children()`](https://hl7.org/fhirpath/N1/#children-collection) function.
    """        
    def evaluate(self, collection: List[FHIRPathCollectionItem], create: bool = False) -> List[FHIRPathCollectionItem]:
        """
        Returns a collection with all immediate child nodes of all items in the input collection.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            List[FHIRPathCollectionItem]): The collection of child items.
        """
        collection = ensure_list(collection)
        children_collection = []
        for item in collection:
            if isinstance(item.value, BaseModel):
                fields = item.value.model_fields
            elif isinstance(item.value, dict):
                fields = list(item.value.keys())
            else:
                fields = []
            for field in fields:
                children_collection.extend(
                    Element(field).evaluate(item, create)
                )
        return children_collection


class Descendants(FHIRPathFunction):
    """
    Representation of the FHIRPath [`descendants()`](https://hl7.org/fhirpath/N1/#descendants-collection) function.
    """        
    def evaluate(self, collection: List[FHIRPathCollectionItem], create: bool = False) -> List[FHIRPathCollectionItem]:
        """
        Returns a collection with all descendant nodes of all items in the input collection. The result does not include
        the nodes in the input collection themselves. 

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            List[FHIRPathCollectionItem]): The collection of descendant items.
        
        Note:
            This function is a shorthand for `repeat(children())`.
        """    
        return Repeat(Children()).evaluate(collection, create)
