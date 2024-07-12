"""The tree navigation module contains the object representations of the math category FHIRPath operators/functions."""

from fhircraft.fhir.path.engine.core import FHIRPath, FHIRPathCollectionItem, FHIRPathError
from fhircraft.utils import ensure_list
from fhircraft.fhir.path.engine.literals import Quantity
from typing import List

class FHIRMathOperator(FHIRPath):
    """
    Abstract class definition for the category of math FHIRPath operators. 
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def convert_to_fhirpath_types(self, item):
        from fhircraft.fhir.resources.datatypes import get_FHIR_type
        if isinstance(item, get_FHIR_type('Quantity')):
            return Quantity(item.value, item.code)
        else:
            return item 
        
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
        return left_collection[0], right_collection[0]

    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((self.left, self.right))


class Addition(FHIRMathOperator):
    """
    A representation of the FHIRPath [`+`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        For Integer, Decimal, and quantity, adds the operands. For strings, concatenates the right 
        operand to the left operand.
        When adding quantities, the units of each quantity must be the same.


        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            result (Any): Addition result

        Raises:
            FHIRPathError: If either expression evaluates to a non-singleton collection.
        """
        left, right = super().evaluate(collection,  *args, **kwargs)
        if not isinstance(left, (int, float, str, Quantity)) or not isinstance(right, (int, float, str, Quantity)):
            return []
        try:
            return left + right
        except TypeError:
            return []


class Subtraction(FHIRMathOperator):
    """
    A representation of the FHIRPath [`-`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Subtracts the right operand from the left operand (supported for Integer, Decimal, and Quantity).
        When subtracting quantities, the units of each quantity must be the same.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            result (Any): Subtraction result

        Raises:
            FHIRPathError: If either expression evaluates to a non-singleton collection.
        """
        left, right = super().evaluate(collection,  *args, **kwargs)
        if not isinstance(left, (int, float, Quantity)) or not isinstance(right, (int, float, Quantity)):
            return []
        try:
            return left - right
        except TypeError:
            return []
        

class Multiplication(FHIRMathOperator):
    """
    A representation of the FHIRPath [`*`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Multiplies both arguments (supported for Integer, Decimal, and Quantity). For multiplication
        involving quantities, the resulting quantity will have the appropriate unit.


        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            result (Any): Multiplication result

        Raises:
            FHIRPathError: If either expression evaluates to a non-singleton collection.
        """
        left, right = super().evaluate(collection,  *args, **kwargs)
        if not isinstance(left, (int, float, Quantity)) or not isinstance(right, (int, float, Quantity)):
            return []
        try:
            return left * right
        except TypeError:
            return []



class Division(FHIRMathOperator):
    """
    A representation of the FHIRPath [`/`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Divides the left operand by the right operand (supported for Integer, Decimal, and Quantity). 
        The result of a division is always Decimal, even if the inputs are both Integer. For integer division,
        use the `div` operator.
        If an attempt is made to divide by zero, the result is empty.
        For division involving quantities, the resulting quantity will have the appropriate unit.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            result (Any): Division result

        Raises:
            FHIRPathError: If either expression evaluates to a non-singleton collection.
        """
        left, right = super().evaluate(collection,  *args, **kwargs)
        if not isinstance(left, (int, float, Quantity)) or not isinstance(right, (int, float, Quantity)):
            return []
        if right == 0:
            return []
        try:
            return left / right
        except TypeError:
            return []
    
    
class Div(FHIRMathOperator):
    """
    A representation of the FHIRPath [`div`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Performs truncated division of the left operand by the right operand (supported for Integer and Decimal). 

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            result (Any): Truncated division result

        Raises:
            FHIRPathError: If either expression evaluates to a non-singleton collection.
        """
        left, right = super().evaluate(collection,  *args, **kwargs)
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            return []
        if right == 0:
            return []
        try:
            return left // right
        except TypeError:
            return []


class Mod(FHIRMathOperator):
    """
    A representation of the FHIRPath [`mod`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Computes the remainder of the truncated division of its arguments (supported for Integer and Decimal).

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            result (Any): Truncated division remainder

        Raises:
            FHIRPathError: If either expression evaluates to a non-singleton collection.
        """
        left, right = super().evaluate(collection,  *args, **kwargs)
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            return []
        if right == 0:
            return []
        try:
            return left % right
        except TypeError:
            return []