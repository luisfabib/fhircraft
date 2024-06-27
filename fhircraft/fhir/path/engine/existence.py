"""The filtering module contains the object representations of the existence-category FHIRPath functions."""

from fhircraft.fhir.path.engine.core import FHIRPath, FHIRPathCollectionItem, FHIRPathError, FHIRPathFunction
from fhircraft.fhir.path.engine.filtering import Where
from typing import List, Optional,Union



class Empty(FHIRPathFunction):
    """
    Representation of the FHIRPath [`empty()`](http://hl7.org/fhirpath/N1/#empty-boolean) function.
    """
    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> bool:
        """
        Returns `True` if the input collection is empty (`{}`) and `False` otherwise.
        
        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection
        
        Returns:
            bool
        """
        return len(collection) == 0

class Exists(FHIRPathFunction):
    """
    Representation of the FHIRPath [`exists()`](http://hl7.org/fhirpath/N1/#existscriteria-expression-boolean) function.

    Attributes:
        criteria (FHIRPath): Optional criteria to be applied to the collection prior to the determination of the exists
    """
    
    def __init__(self, criteria: FHIRPath = None):
        self.criteria = criteria

    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> bool:
        """
        Returns `True` if the collection has any elements, and `False` otherwise. 
        This is the opposite of empty(), and as such is a shorthand for empty().not().
        If the input collection is empty (`{}`), the result is `False`.
        The function can also take an optional criteria to be applied to the collection
        prior to the determination of the exists. In this case, the function is 
        shorthand for where(criteria).exists().
        
        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection
        
        Returns:
            bool
        """    
        if self.criteria:
            collection = Where(self.criteria).evaluate(collection, create=False)
        return len(collection) > 0
    
    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.criteria.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.criteria.__repr__()})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.criteria == other.criteria


class All(FHIRPathFunction):
    """
    5.1.3. All
    -------------
    Returns `True` if for every element in the input collection, criteria evaluates to `True`.
    Otherwise, the result is `False`. If the input collection is empty (`{}`), the result is `True`.
    """

    def __init__(self, criteria: FHIRPath):
        self.criteria = criteria

    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> bool:
        if len(collection) == 0:
            return True
        return all([self.criteria.evaluate([item], create=False) for item in collection])
    
    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.criteria.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.criteria.__repr__()})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.criteria == other.criteria
    


def _all_or_any_boolean(collection: List[FHIRPathCollectionItem], op: callable, boolean: bool):
    values = []
    if len(collection)==0:
        if op == any:
            return False
        else:
            return True
    for item in collection:
        if not isinstance(item.value, bool):
            raise FHIRPathError(f'The collection evaluated by allTrue() has a non-boolean value: {item.value}')
        values.append(item.value == boolean)
    return op(values)

    
class AllTrue(FHIRPathFunction):
    """
    5.1.4. allTrue
    ---------------
    Takes a collection of Boolean values and returns `True` if all the items are `True`. If any 
    items are `False`, the result is `False`. If the input is empty (`{}`), the result is `True`.
    """

    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> bool:
        return _all_or_any_boolean(collection, all, True)
    
class AnyTrue(FHIRPathFunction):
    """
    5.1.5. anyTrue
    ---------------
    Takes a collection of Boolean values and returns `True` if any of the items are `True`. 
    If all the items are `False`, or if the input is empty (`{}`), the result is `False`.
    """

    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> bool:
        return _all_or_any_boolean(collection, any, True)

class AllFalse(FHIRPathFunction):
    """
    5.1.6. allFalse
    ---------------
    Takes a collection of Boolean values and returns `True` if all the items are `False`. 
    If any items are `True`, the result is `False`. If the input is empty (`{}`), the result is `True`.
    """

    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> bool:
        return _all_or_any_boolean(collection, all, False)
    
class AnyFalse(FHIRPathFunction):
    """
    5.1.7. anyFalse
    ---------------
    Takes a collection of Boolean values and returns `True` if any of the items are `False`. If all 
    the items are `True`, or if the input is empty (`{}`), the result is `False`.
    """

    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> bool:
        return _all_or_any_boolean(collection, any, False)

class SubsetOf(FHIRPathFunction):
    """
    5.1.8. subsetOf
    ---------------
    Returns true if all items in the input collection are members of the collection passed as the 
    other argument. Membership is determined using the = (Equals) (=) operation.

    Conceptually, this function is evaluated by testing each element in the input collection for 
    membership in the other collection, with a default of true. This means that if the input collection
    is empty ({ }), the result is true, otherwise if the other collection is empty ({ }), the result is false.
    """

    def __init__(self, other: Union[List[FHIRPathCollectionItem], FHIRPath] = None):
        self.other = other

    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> bool:
        if len(collection) == 0:
            return True
        if isinstance(self.other, FHIRPath):
            other_collection = self.other.evaluate()
        else:
            other_collection = self.other
        if len(other_collection) == 0:
            return False
        for item in collection:
            if item not in other_collection:
                return False
        else:
            return True

    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.other.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.other.__repr__()})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.other == other.other


class SupersetOf(FHIRPathFunction):
    """
    5.1.9. supersetOf
    -----------------
    Returns true if all items in the collection passed as the other argument are 
    members of the input collection. Membership is determined using the = (Equals) (=) operation.

    Conceptually, this function is evaluated by testing each element in the other collection for 
    membership in the input collection, with a default of true. This means that if the other collection
    is empty ({ }), the result is true, otherwise if the input collection is empty ({ }), the result is false.
    """

    def __init__(self, other: Union[List[FHIRPathCollectionItem], FHIRPath] = None):
        self.other = other

    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> bool:
        if len(collection) == 0:
            return True
        if isinstance(self.other, FHIRPath):
            other_collection = self.other.evaluate()
        else:
            other_collection = self.other
        if len(other_collection) == 0:
            return True
        for item in other_collection:
            if item not in collection:
                return False
        else:
            return True
        
    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.other.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.other.__repr__()})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.other == other.other


class Count(FHIRPathFunction):
    """
    5.1.10. Count
    --------------
    Returns the integer count of the number of items in the input collection. Returns 0 when the input collection is empty.
    """

    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> int:
        return len(collection)

class Distinct(FHIRPathFunction):
    """
    5.1.11. distinct
    ------------------
    Returns a collection containing only the unique items in the input collection. To determine whether two items are the 
    same, the = (Equals) (=) operator is used, as defined below. If the input collection is empty ({ }), the result is empty.
    Note that the order of elements in the input collection is not guaranteed to be preserved in the result.
    """

    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> List[FHIRPathCollectionItem]:
        return list(set(collection))


class IsDistinct(FHIRPathFunction):
    """
    5.1.12. isDistinct
    ------------------
    Returns true if all the items in the input collection are distinct. 
    If the input collection is empty ({ }), the result is true.
    """

    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> bool:
        return len(list(set(collection))) == len(collection)