"""The tree navigation module contains the object representations of the types category FHIRPath operators/functions."""

from fhircraft.fhir.path.engine.core import FHIRPath, FHIRPathCollectionItem, FHIRPathError
from fhircraft.utils import ensure_list
from fhircraft.fhir.resources.datatypes import get_FHIR_type
from typing import List

class FHIRTypesOperator(FHIRPath):
    """
    Abstract class definition for the category of types FHIRPath operators. 
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        create = kwargs.get('create')
        left_collection = [
            item.value if isinstance(item, FHIRPathCollectionItem) else item 
                for item in ensure_list(self.left.evaluate(collection, create))
        ]  if isinstance(self.left, FHIRPath) else ensure_list(self.left)
        left_collection = [self.convert_to_fhirpath_types(item) for item in left_collection]

        right_collection = [ 
            item.value if isinstance(item, FHIRPathCollectionItem) else item  
                for item in ensure_list(self.right.evaluate(collection, create))
        ] if isinstance(self.right, FHIRPath) else ensure_list(self.right)
        right_collection = [self.convert_to_fhirpath_types(item) for item in right_collection]

        if len(left_collection)>1:
            raise FHIRPathError(f'FHIRPath operator {self.__str__()} expected a single-item collection for the left expression, instead got a {len(collection)}-items collection.')
        if len(left_collection)>1:
            raise FHIRPathError(f'FHIRPath operator {self.__str__()} expected a single-item collection for the right expression, instead got a {len(collection)}-items collection.')
        if len(left_collection)==0 or len(right_collection)==0:
            return None, None
        return left_collection[0], right_collection[0]

    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((self.left, self.right))


class Is(FHIRTypesOperator):
    """
    A representation of the FHIRPath [`is`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        The greater than operator (>) returns true if the first operand is strictly greater than the second.
        The operands must be of the same type, or convertible to the same type using an implicit conversion.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            bool

        Raises:
            FHIRPathError: If either expression evaluates to a non-singleton collection.
        """
        left, right = super().evaluate(collection,  *args, **kwargs)
        if not left and not right: return None, None
        return left > right
