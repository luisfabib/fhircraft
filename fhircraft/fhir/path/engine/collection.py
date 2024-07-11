"""The comparison module contains the object representations of the collection FHIRPath operators."""


from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, FHIRPath, FHIRPathError
from fhircraft.fhir.path.engine.combining import Union as UnionFunction
from fhircraft.utils import ensure_list
from typing import List, Any, Optional


class FHIRCollectionOperator(FHIRPath):
    """
    Abstract class definition for the category of collection FHIRPath operators. 
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
        
        right_collection = [ 
            item.value if isinstance(item, FHIRPathCollectionItem) else item  
                for item in ensure_list(self.right.evaluate(collection, create))
        ] if isinstance(self.right, FHIRPath) else ensure_list(self.right)

        return left_collection, right_collection

    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((self.left, self.right))
    


class Union(FHIRCollectionOperator):
    """
    A representation of the FHIRPath [`|`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Merge the two collections into a single collection, eliminating any duplicate values to 
        determine equality). There is no expectation of order in the resulting collection.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            collection (List[FHIRPathCollectionItem])): The output collection.
        """
        left, right = super().evaluate(collection,  *args, **kwargs)
        left = [FHIRPathCollectionItem(value=item) if not isinstance(item, FHIRPathCollectionItem) else item for item in left]
        right = [FHIRPathCollectionItem(value=item) if not isinstance(item, FHIRPathCollectionItem) else item for item in right]
        return UnionFunction(left).evaluate(right)


class In(FHIRCollectionOperator):
    """
    A representation of the FHIRPath [`in`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        If the left operand is a collection with a single item, this operator returns true if the item is in the 
        right operand using equality semantics. If the left-hand side of the operator is empty, the result is empty,
        if the right-hand side is empty, the result is false. If the left operand has multiple items, an exception is thrown.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            bool

        Raises:
            FHIRPathError: If the left expression evaluates to a non-singleton collection.
        """
        left, right = super().evaluate(collection,  *args, **kwargs)
        left = [FHIRPathCollectionItem(value=item) if not isinstance(item, FHIRPathCollectionItem) else item for item in left]
        if len(left)==0:
            return []
        if len(left)!=1:
            raise FHIRPathError('Left expression evaluates to a non-singleton collection.')
        value = left[0].value
        check_collection = [item.value if isinstance(item, FHIRPathCollectionItem) else item for item in right]
        return value in check_collection


class Contains(FHIRCollectionOperator):
    """
    A representation of the FHIRPath [`contains`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        If the right operand is a collection with a single item, this operator returns true if the item is in the
        left operand using equality semantics. If the right-hand side of the operator is empty, the result is empty,
        if the left-hand side is empty, the result is false. This is the converse operation of `in`.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            bool

        Raises:
            FHIRPathError: If the left expression evaluates to a non-singleton collection.
        """
        left, right = super().evaluate(collection,  *args, **kwargs)
        right = [FHIRPathCollectionItem(value=item) if not isinstance(item, FHIRPathCollectionItem) else item for item in right]
        if len(right)==0:
            return []
        if len(right)!=1:
            raise FHIRPathError('Left expression evaluates to a non-singleton collection.')
        value = right[0].value
        check_collection = [item.value if isinstance(item, FHIRPathCollectionItem) else item for item in left]
        return value in check_collection