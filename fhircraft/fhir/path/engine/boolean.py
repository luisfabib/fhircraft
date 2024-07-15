
"""
For all boolean operators, the collections passed as operands are first evaluated as Booleans.
The operators then use three-valued logic to propagate empty operands.
"""

from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, FHIRPath, FHIRPathFunction
from fhircraft.utils import ensure_list
from typing import List, Any, Optional, Union

def _evaluate_boolean_expressions(left, right, collection, create):
    left_collection = left.evaluate(collection, create=create) if isinstance(left, FHIRPath) else ensure_list(left)
    if isinstance(left_collection, bool):
        left_boolean = left_collection
    else:
        if len(left_collection) > 0:
            left_boolean = bool(left_collection)
        else:
            left_boolean = None
    right_collection = right.evaluate(collection, create=create) if isinstance(right, FHIRPath) else ensure_list(right)
    if isinstance(right_collection, bool):
        right_boolean = right_collection
    else:
        if len(right_collection) > 0:
            right_boolean = bool(right_collection)
        else:
            right_boolean = None       
    return left_boolean, right_boolean

class And(FHIRPath):
    """
    A representation of the FHIRPath [`and`](https://hl7.org/fhirpath/N1/#and) boolean logic operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Returns `True` if both operands evaluate to `True`, `False` if either operand evaluates to `False`, and the empty collection (`[]`) otherwise.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            bool
        """
        left_boolean, right_boolean = _evaluate_boolean_expressions(self.left, self.right, collection, create=kwargs.get('create', False))
        if left_boolean is None:
            if right_boolean is True:
                return []
            elif right_boolean is False:
                return False
            elif right_boolean is None:
                return []
        elif right_boolean is None:
            if left_boolean is True:
                return []
            elif left_boolean is False:
                return False
            elif left_boolean is None:
                return []
        return left_boolean and right_boolean
    
    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, And) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((self.left, self.right))

class Or(FHIRPath):
    """
    A representation of the FHIRPath [`or`](https://hl7.org/fhirpath/N1/#or) boolean logic operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Returns `False` if both operands evaluate to `False`, `True` if either operand evaluates to `True`, and empty (`[]`) otherwise.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            bool
        """
        left_boolean, right_boolean = _evaluate_boolean_expressions(self.left, self.right, collection, create=kwargs.get('create', False))
        if left_boolean is None:
            if right_boolean is True:
                return True
            elif right_boolean is False:
                return []
            elif right_boolean is None:
                return []
        elif right_boolean is None:
            if left_boolean is True:
                return True
            elif left_boolean is False:
                return []
            elif left_boolean is None:
                return []
        return left_boolean or right_boolean
    
    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, Or) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((self.left, self.right))


class Xor(FHIRPath):
    """
    A representation of the FHIRPath [`xor`](https://hl7.org/fhirpath/N1/#xor) boolean logic operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Returns `True` if exactly one of the operands evaluates to `True`, `False` if either both operands evaluate to `True` or both operands evaluate to `False`, and the empty collection (`[]`) otherwise.
        
        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            bool
        """
        left_boolean, right_boolean = _evaluate_boolean_expressions(self.left, self.right, collection, create=kwargs.get('create', False))
        if left_boolean is None:
            if right_boolean is True:
                return []
            elif right_boolean is False:
                return []
            elif right_boolean is None:
                return []
        elif right_boolean is None:
            if left_boolean is True:
                return []
            elif left_boolean is False:
                return []
            elif left_boolean is None:
                return []
        return left_boolean ^ right_boolean
        
    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, Xor) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((self.left, self.right))
    
    
    
class Implies(FHIRPath):
    """
    A representation of the FHIRPath [`implies`](https://hl7.org/fhirpath/N1/#implies) boolean logic operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        If the left operand evaluates to `True`, this operator returns the boolean evaluation of the right operand. If the
        left operand evaluates to `False`, this operator returns `True`. Otherwise, this operator returns `True` if the right
        operand evaluates to `True`, and the empty collection (`[]`) otherwise.
        
        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            bool
        """
        left_boolean, right_boolean = _evaluate_boolean_expressions(self.left, self.right, collection, create=kwargs.get('create', False))
        if left_boolean is None:
            if right_boolean is True:
                return True
            elif right_boolean is False:
                return []
            elif right_boolean is None:
                return []
        elif right_boolean is None:
            if left_boolean is True:
                return []
            elif left_boolean is False:
                return True
            elif left_boolean is None:
                return []
        elif left_boolean is True:
            if right_boolean is True:
                return True
            elif right_boolean is False:
                return False
        elif right_boolean is True:
            if left_boolean is True:
                return True
            elif left_boolean is False:
                return True
        elif right_boolean is False and left_boolean is False:
            return True
    
    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, Implies) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((self.left, self.right))


class Not(FHIRPathFunction):
    """
    A representation of the FHIRPath [`not`](https://hl7.org/fhirpath/N1/#not) boolean logic function.
    """
    def evaluate(self, collection: Union[List[FHIRPathCollectionItem], bool], *args, **kwargs) -> bool:
        """
        Returns `True` if the input collection evaluates to `False`, and `False` if it evaluates to `True`. Otherwise, the result is empty (`[]`):


        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            bool
        """
        if isinstance(collection, bool):
            boolean = collection
        else:
            collection = ensure_list(collection)
            if len(collection) > 0:
                boolean = bool(collection)
            else:
                return []
        return not boolean
    