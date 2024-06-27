"""The filtering module contains the object representations of the filtering-category FHIRPath functions."""

from fhircraft.fhir.path.engine.core import FHIRPath, FHIRPathCollectionItem, FHIRPathFunction
from fhircraft.utils import ensure_list
from typing import List, Optional,Union


class Where(FHIRPathFunction):
    """
    Representation of the FHIRPath [`where()`](http://hl7.org/fhirpath/N1/#wherecriteria-expression-collection) function.

    Attributes:
        expression (FHIRPath): Expression to evaluate for each collection item. 
    """
    def __init__(self, expression: FHIRPath):
        self.expression = expression
        
    def evaluate(self, collection: List[FHIRPathCollectionItem], create: bool = False) -> List[FHIRPathCollectionItem]:
        """
        Returns a collection containing only those elements in the input collection for which
        the stated criteria expression evaluates to `True`. Elements for which the expression
        evaluates to false or empty (`[]`) are not included in the result.
        If the input collection is empty (`[]`), the result is empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
            create (bool): Whether to auto-generate missing path segments.
        
        Returns:
            List[FHIRPathCollectionItem]): The output collection.
        """    
        collection = ensure_list(collection)
        return [item for item in collection if self.expression.evaluate(item, create)]

    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.expression.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.expression.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, Where) and other.expression == self.expression

    def __hash__(self):
        return hash((self.expression))


class Select(FHIRPathFunction):
    """
    Representation of the FHIRPath [`select()`](http://hl7.org/fhirpath/N1/#selectprojection-expression-collection) function.
    
    Attributes:
        projection (FHIRPath): Expression to evaluate for each collection item. 
    """
    def __init__(self, projection: FHIRPath):
        self.projection = projection
        
    def evaluate(self, collection: List[FHIRPathCollectionItem], create: bool = False) -> List[FHIRPathCollectionItem]:
        """
        Evaluates the projection expression for each item in the input collection. The result of each
        evaluation is added to the output collection. If the evaluation results in a collection with
        multiple items, all items are added to the output collection (collections resulting from 
        evaluation of projection are flattened). This means that if the evaluation for an element 
        results in the empty collection (`[]`), no element is added to the result, and that if the 
        input collection is empty (`[]`), the result is empty as well.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
            create (bool): Whether to auto-generate missing path segments.
        
        Returns:
            List[FHIRPathCollectionItem]): The output collection.
        """    
        collection = ensure_list(collection)
        return [projected_item for item in collection for projected_item in self.projection.evaluate(item, create)]

    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.projection.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.projection.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, Select) and other.projection == self.projection

    def __hash__(self):
        return hash((self.projection))


class Repeat(FHIRPathFunction):
    """
    Representation of the FHIRPath [`repeat()`](http://hl7.org/fhirpath/N1/#repeatprojection-expression-collection) function.
    
    Attributes:
        projection (FHIRPath): Expression to evaluate for each collection item. 
    """
    def __init__(self, projection: FHIRPath):
        self.projection = projection
        
    def evaluate(self, collection: List[FHIRPathCollectionItem], create: bool = False) -> List[FHIRPathCollectionItem]:
        """
        A version of select that will repeat the projection and add it to the output collection, as
        long as the projection yields new items (as determined by the = (Equals) (=) operator).

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
            create (bool): Whether to auto-generate missing path segments.
        
        Returns:
            List[FHIRPathCollectionItem]): The output collection.
        """ 
        collection = ensure_list(collection)
        def project_recursively(input_collection):
            output_collection = []
            for item in input_collection:
                new_collection = self.projection.evaluate(item, create)
                output_collection.extend(new_collection)
                if len(new_collection)>0:
                    output_collection.extend(project_recursively(new_collection))
            return output_collection
        return project_recursively(collection)

    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.projection.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.projection.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, Repeat) and other.projection == self.projection

    def __hash__(self):
        return hash((self.projection))




class OfType(FHIRPathFunction):
    """
    Representation of the FHIRPath [`ofType()`](http://hl7.org/fhirpath/N1/#oftypetype-type-specifier-collection) function.
    
    Attributes:
        type (class): Type class 
    """
    def __init__(self, type: FHIRPath):
        self.type = type
        
    def evaluate(self, collection: List[FHIRPathCollectionItem]) -> List[FHIRPathCollectionItem]:
        """
        Returns a collection that contains all items in the input collection that are of the given type
        or a subclass thereof. If the input collection is empty (`[]`), the result is empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            List[FHIRPathCollectionItem]): The output collection.
        """ 
        collection = ensure_list(collection)
        return [item for item in collection if isinstance(item.value, self.type)]

    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.type.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.type.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, OfType) and other.type == self.type

    def __hash__(self):
        return hash((self.type))
