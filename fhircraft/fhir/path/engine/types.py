"""The tree navigation module contains the object representations of the types category FHIRPath operators/functions."""

from fhircraft.fhir.path.engine.core import FHIRPath, FHIRPathCollectionItem, FHIRPathError, FHIRPathFunction, This
from fhircraft.utils import ensure_list
from fhircraft.fhir.path.engine.literals import Quantity, DateTime, Date, Time
from typing import List

class FHIRTypesOperator(FHIRPath):
    """
    Abstract class definition for the category of types FHIRPath operators. 
    """
    def __init__(self, left: FHIRPath, type_specifier: str):
        self.left = left
        self.type_specifier = type_specifier

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        create = kwargs.get('create')
        left_collection = [
            item.value if isinstance(item, FHIRPathCollectionItem) else item 
                for item in ensure_list(self.left.evaluate(collection, create))
        ]  if isinstance(self.left, FHIRPath) else ensure_list(self.left)

        if len(left_collection)>1:
            raise FHIRPathError(f'FHIRPath operator {self.__str__()} expected a single-item collection for the left expression, instead got a {len(collection)}-items collection.')

        type = {
            'String': str,
            'Decimal': (int, float),
            'Integer': int,
            'Quantity': Quantity,
            'DateTime': DateTime,
            'Boolean': bool,
            'Time': Time,
            'Date': Date,

        }.get(self.type_specifier)

        return left_collection[0], type

    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.left.__str__(), self.type_specifier.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left.__repr__(), self.type_specifier.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.left == self.left and other.type_specifier == self.type_specifier

    def __hash__(self):
        return hash((self.left, self.type_specifier))


class Is(FHIRTypesOperator):
    """
    A representation of the FHIRPath [`is`](https://hl7.org/fhirpath/N1/#is) operator.

    Attributes:
        left (FHIRPath): Left operand.
        type_specifier (str): Type specifier.
    """
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        If the left operand is a collection with a single item and the second operand is a type identifier,
        this operator returns true if the type of the left operand is the type specified in the second operand,
        or a subclass thereof. If the input value is not of the type, this operator returns false. If the identifier
        cannot be resolved to a valid type identifier, the evaluator will throw an error. If the input collections 
        contains more than one item, the evaluator will throw an error. In all other cases this operator returns the empty collection.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            bool

        Raises:
            FHIRPathError: If either expression evaluates to a non-singleton collection.
        """
        # TODO: Implement propert type specifier handling
        value, type = super().evaluate(collection,  *args, **kwargs)
        print(value, type)
        return isinstance(value, type) if type else []



class LegacyIs(FHIRPathFunction):
    """ 
    The is() function is supported for backwards compatibility with previous implementations of FHIRPath. 
    Just as with the is keyword, the type argument is an identifier that must resolve to the name of a type
    in a model.
    """
    def __init__(self, type_specifier:str):
        self.type_specifier = type_specifier

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        return Is(This(), self.type_specifier).evaluate(collection)

class As(FHIRTypesOperator):
    """
    A representation of the FHIRPath [`as`](https://hl7.org/fhirpath/N1/#as) operator.

    Attributes:
        left (FHIRPath): Left operand.
        type_specifier (str): Type specifier.
    """
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        If the left operand is a collection with a single item and the second operand is an identifier,
        this operator returns the value of the left operand if it is of the type specified in the second
        operand, or a subclass thereof. If the identifier cannot be resolved to a valid type identifier,
        the evaluator will throw an error. If there is more than one item in the input collection, the 
        evaluator will throw an error. Otherwise, this operator returns the empty collection.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            bool

        Raises:
            FHIRPathError: If either expression evaluates to a non-singleton collection.
        """
        # TODO: Implement propert type specifier handling
        value, type = super().evaluate(collection,  *args, **kwargs)
        return value if type is not None and isinstance(value, type) else []


class LegacyAs(FHIRPathFunction):
    """ 
    The as() function is supported for backwards compatibility with previous implementations of FHIRPath.
    Just as with the as keyword, the type argument is an identifier that must resolve to the name of a type 
    in a model.  
    """
    def __init__(self, type_specifier:str):
        self.type_specifier = type_specifier

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        return As(This(), self.type_specifier).evaluate(collection)
