import logging
from itertools import *  # noqa
from fhircraft.utils import ensure_list, contains_list_type, get_fhir_model_from_field

import typing
from typing import List, Optional
from abc import ABC
from dataclasses import dataclass, field
from functools import partial

# Get logger name
logger = logging.getLogger(__name__)

class FHIRPathError(Exception):
    """
    An exception related to FHIRPath specific syntax or runtime criteria.
    """
    pass

@dataclass
class FHIRPathCollectionItem(object):
    """
    A context-aware representation of an item in a FHIRPath collection.

    Attributes
    ----------
    value (Any): The value of the collection item.
    path (Optional[FHIRPath]): The path associated with the collection item, by default This().
    element (Optional[str]): The element name of the collection item, by default None.
    index (Optional[int]): The index of the collection item, by default None.
    parent (Optional[FHIRPathCollectionItem]): The item of the parent collection from which this item was derived, by default None.
    setter (Optional[callable]): The setter function for the collection item, by default None.
    """
    value: typing.Any
    path: typing.Any = field(default_factory=lambda: This())
    element: Optional[str] = None
    index: Optional[int] = None
    parent: Optional["FHIRPathCollectionItem"] = None
    setter: Optional[callable] = None

    @classmethod
    def wrap(cls, data: typing.Union["FHIRPathCollectionItem"]):
        """
        Wraps data in a FHIRPathCollectionItem instance.

        Args:
            data (Union[FHIRPathCollectionItem): The data to be wrapped.

        Returns:
            item (FHIRPathCollectionItem): The wrapped FHIRPathCollectionItem instance.
        """
        if isinstance(data, cls):
            return data
        else:
            return cls(data)

    def set_literal(self,value):
        setattr(self.parent.value, self.path.label, value)
        
    def set_value(self,value):
        """
        Sets the value of the item using the setter function.

        Args:
            value (Any): The value to set.

        Raises:
            ValueError: If the value is a list.
            RuntimeError: If there is no setter function associated with this item.
        """        
        if self.setter:
            if isinstance(value, list):
                raise ValueError('Only single value is accepted')
            self.setter(value)
        else:
            raise RuntimeError('There is not setter function associated with this item')
    

    @property
    def field_info(self):
        """
        Retrieves the field information from the parent's value.

        Returns:
            Any: The field information, or None if not available.
        """        
        parent = self.parent.value
        if isinstance(parent, list):
            parent = parent[0]
        if hasattr(parent, 'model_fields') and hasattr(self.path, 'label'):
            return parent.model_fields.get(self.path.label)
        return None
    
    @property
    def is_list_type(self):
        """
        Checks if the field information indicates a list type.

        Returns:
            bool: True if the field information indicates a list type, False otherwise.
        """        
        if not self.field_info:
            return False
        return contains_list_type(self.field_info.annotation)

    def construct_resource(self):
        """
        Constructs a FHIR resource based on the field information.

        Returns:
            Any: The constructed FHIR resource, or None if construction fails.
        """        
        if self.field_info:
            model = get_fhir_model_from_field(self.field_info)
            return model.model_construct()    
                
    @property
    def full_path(self):
        """
        Retrieves the full path of the item.

        Returns:
            Any: The full path of the item.
        """        
        return self.path if self.parent is None else self.parent.full_path.child(self.path)

    def __repr__(self):
        return f'FHIRPathCollectionItem(value={self.value.__repr__()[:10]}, element={self.element.__repr__()[:10]}..., index={self.index}, parent={self.parent.full_path if self.parent else None})'

    def __hash__(self):
        return hash((self.value, self.path, self.parent))
        


class FHIRPath(ABC):
    """
    Abstract base class representing a FHIRPath, used for navigating and manipulating
    FHIR resources.
    """
    
    def get_value(self, data):
        """
        Extracts the value(s) from the given data.

        Args:
            data (Any): The data from which to extract values.

        Returns:
            Any: The extracted value(s), or None if no values are found.
        """
        collection = self.find(data)
        values = [item.value for item in collection if item.value and not isinstance(item.value, bool)]
        if len(values) == 1:
            values = values[0]
        elif len(values) == 0:
            return None
        return values        

    def find(self, collection: typing.Any) -> List[FHIRPathCollectionItem]:
        """
        Finds and returns a collection of FHIRPathCollectionItem instances from the input collection.

        Args:
            collection (Any): The input collection to search.

        Returns:
            List[FHIRPathCollectionItem]: A list of FHIRPathCollectionItem instances.
        """
        # Ensure that entrypoint is a FHIRPathCollectionItem instance
        collection = [FHIRPathCollectionItem.wrap(item) for item in ensure_list(collection)]
        return self.evaluate(collection, create=False)

    def find_or_create(self, collection) -> List[FHIRPathCollectionItem]:
        """
        Finds or creates and returns a collection of FHIRPathCollectionItem instances from the input collection.

        Args:
            collection (Any): The input collection to search or create items in.

        Returns:
            List[FHIRPathCollectionItem]: A list of FHIRPathCollectionItem instances.
        """        
        # Ensure that entrypoint is a FHIRPathCollectionItem instance
        collection = [FHIRPathCollectionItem.wrap(item) for item in ensure_list(collection)]
        return self.evaluate(collection, create=True)

    def update(self, collection, value) -> None:
        """
        Updates the input collection with the given value.

        Args:
            collection (Any): The input collection to update.
            value (Any): The value to set in the collection.
        """        
        # Ensure that entrypoint is a FHIRPathCollectionItem instance
        collection = [FHIRPathCollectionItem.wrap(item) for item in ensure_list(collection)]
        # Collect the elements and set the values for each of them
        new_collection = self.evaluate(collection, create=False)
        for item in new_collection:
            item.set_value(value)

    def update_or_create(self, collection, value) -> None:     
        """
        Updates or creates the input collection with the given value.

        Args:
            collection (Any): The input collection to update or create items in.
            value (Any): The value to set in the collection.
        """         
        # Ensure that entrypoint is a FHIRPathCollectionItem instance
        collection = [FHIRPathCollectionItem.wrap(item) for item in ensure_list(collection)]
        # Collect the elements and set the values for each of them
        for item in self.evaluate(collection, create=True):
            item.set_value(value)

    def evaluate(self, collection, create: bool) -> List[FHIRPathCollectionItem]:
        """
        Evaluates the collection and returns a list of FHIRPathCollectionItem instances.

        Args:
            collection (Any): The input collection to evaluate.
            create (bool): Flag indicating whether to create new items if they do not exist.

        Returns:
            List[FHIRPathCollectionItem]: A list of FHIRPathCollectionItem instances.
            
        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError()        

    def child(self, child):
        """
        Returns the child of this FHIRPath instance with some canonicalization.

        Args:
            child (Any): The child element.

        Returns:
            (Any): The canonicalized child element.
        """
        if isinstance(self, This) or isinstance(self, Root):
            return child
        elif isinstance(child, This):
            return self
        elif isinstance(child, Root):
            return child
        else:
            return Invocation(self, child)


class FHIRPathFunction(FHIRPath):
    """
    Abstract base class representing a FHIRPath function, used for functional evaluation of collections.
    """
    def __str__(self):
        return f'{self.__class__.__name__.lower()}()'

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __eq__(self, other):
        return isinstance(other, self.__class__)



class Element(FHIRPath):
    """
    A class representing an element in a FHIRPath, used for navigating and manipulating FHIR resources.

    Attributes:
        label (str): The name of the element.
    """
    def __init__(self, label: str):
        self.label = label

    def create_element(self, parent):
        """ 
        Ensure that the input parent object has the necessary field information to create a new element based on the label provided.

        Args:
            parent: The parent object from which the element will be created.

        Returns:
            The newly created element based on the field information of the parent object, or None if the parent is invalid or lacks the required field information.

        Raises:
            KeyError: If there is an issue with retrieving the field information from the parent object.
            AttributeError: If there is an attribute error while trying to create the new element.
        """
        if not parent:
            return None
        if not hasattr(parent, 'model_fields'):
            return None 
        field_info = parent.model_fields.get(self.label)
        try:
            model = get_fhir_model_from_field(field_info)
            new_element = model.model_construct()    
        except (KeyError, AttributeError):
            new_element = None 
        if field_info and contains_list_type(field_info.annotation):
            new_element = ensure_list(new_element)
        return new_element

    @staticmethod
    def setter(value: typing.Any, item: FHIRPathCollectionItem, index: int, label: str):
        """ 
        Sets the value of the specified element in the parent object.

        Args:
            value (Any): The value to set for the element.
            item (FHIRPathCollectionItem): The parent collection item.
            index (int): The index of the element in the parent object.
            label (str): The label of the element to set.
        """
        parent = item.value
        parents = getattr(parent, label)
        if not isinstance(parents, list):
            setattr(parent, label, value)
        else:
            if len(parents)<=index:
                parents.insert(index, value)
            else:                
                parents[index] = value
        

    def evaluate(self, collection: List[FHIRPathCollectionItem], create: bool) -> List[FHIRPathCollectionItem]:
        """ 
        Evaluate the collection of FHIRPathCollectionItems and create new elements if necessary.

        Args:
            collection (List[FHIRPathCollectionItem]): A list of FHIRPathCollectionItems to evaluate.
            create (bool): A flag indicating whether to create new elements if they do not exist.

        Returns:
            List[FHIRPathCollectionItem]: A list of FHIRPathCollectionItems after evaluation.
        """
        collection = ensure_list(collection)
        element_collection = []
        for item in collection:
            if not item.value:
                continue
            element_value = getattr(item.value, self.label, None)         
            if not element_value and not isinstance(element_value, bool) and create:
                element_value = self.create_element(item.value)  
                setattr(item.value, self.label, element_value)  
            for index, value in enumerate(ensure_list(element_value)):
                element = FHIRPathCollectionItem(
                    value, 
                    path=Element(self.label), 
                    parent=item, 
                    setter=partial(self.setter, item=item, index=index, label=self.label)
                )
                # element.set_value(value)
                element_collection.append(element)
        return element_collection

    def __str__(self):
        return self.label

    def __repr__(self):
        return f'{self.__class__.__name__}({self.label})'

    def __eq__(self, other):
        return isinstance(other, Element) and self.label == other.label

    def __hash__(self):
        return hash(self.label)




class Root(FHIRPath):
    """ 
    A class representing the root of a FHIRPath, i.e. the top-most segment of the FHIRPath 
    whose collection has no parent associated.
    """
    def evaluate(self, collection, *args, **kwargs):
        """
        Evaluate the collection of top-most resources in the input collection.

        Args:
            collection: The collection of items to be evaluated.

        Returns:
            list: A list of FHIRPathCollectionItem instances after evaluation.
        """        
        collection = ensure_list(collection)
        return [
            FHIRPathCollectionItem(item, path=Root(), parent=None)
                if not isinstance(item, FHIRPathCollectionItem)
                else FHIRPathCollectionItem(item.value, parent=None, path=Root())
                    if item.parent is None else Root().find(item.parent)[0]
                        for item in collection
        ]

    def __str__(self):
        return '$'

    def __repr__(self):
        return 'Root()'

    def __eq__(self, other):
        return isinstance(other, Root)

    def __hash__(self):
        return hash('$')


class This(FHIRPath):
    """
    A class representation of the FHIRPath `$this` operator used to represent
    the item from the input collection currently under evaluation.
    """
    def evaluate(self, collection, *args, **kwargs):
        """
        Simply returns the input collection. 

        Parameters:
            create (bool): A boolean flag indicating whether to create the collection if it does not exist.

        Returns:
            list: The input collection.
        """
        return ensure_list(collection)

    def __str__(self):
        return '`this`'

    def __repr__(self):
        return 'This()'

    def __eq__(self, other):
        return isinstance(other, This)

    def __hash__(self):
        return hash('this')


class Invocation(FHIRPath):
    """
    A class representing an invocation in the context of FHIRPath evaluation 
    indicated by two dot-separated identifiers `<left>.<right>`.

    Attributes:
        left (FHIRPath): The left-hand side FHIRPath segment of the invocation.
        right (FHIRPath): The right-hand side  FHIRPath segment of the invocation.
    """
    def __init__(self, left:FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], create: bool):
        """
        Performs the evaluation of the Invocation by applying the left-hand side FHIRPath segment on the given collection to obtain a parent collection. 
        Then, the right-hand side FHIRPath segment is applied on the parent collection to derive the child collection.

        Args:
            collection (List[FHIRPathCollectionItem]): The collection on which the evaluation is performed.
            create (bool): A boolean flag indicating whether to create any missing elements.

        Returns:
            List[FHIRPathCollectionItem]: The resulting child collection after the evaluation process.
        """        
        parent_collection = self.left.evaluate(collection, create)
        child_collection = self.right.evaluate(parent_collection, create)
        return child_collection

    def __eq__(self, other):
        return isinstance(other, Invocation) and self.left == other.left and self.right == other.right

    def __str__(self):
        return '%s.%s' % (self.left, self.right)

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.left, self.right)

    def __hash__(self):
        return hash((self.left, self.right))



class Operation(FHIRPath):
    """
    A class representing an operation in FHIRPath expressions.

    Attributes:
        left (Union[str, FHIRPath]): The left operand of the operation.
        op (callable): The operation to be performed.
        right (Union[str, FHIRPath]): The right operand of the operation.
    """
    def __init__(self, left : typing.Union[str,FHIRPath], op : callable,right : typing.Union[str,FHIRPath]):
        self.left = left
        self.op = op
        self.right = right
        
    def evaluate(self, collection: List[FHIRPathCollectionItem], create: bool) -> bool:
        """ 
        Evaluates the operation on the given collection.

        Args:
            collection (List[FHIRPathCollectionItem]): The collection of FHIRPathCollectionItem instances to evaluate.
            create (bool): Flag indicating whether to create new items if they do not exist.

        Returns:
            bool: The result of the operation evaluation.
        """
        collection = ensure_list(collection)
        return self.op(
            [
                item.value if isinstance(item, FHIRPathCollectionItem) else item 
                    for item in ensure_list(self.left.evaluate(collection, create))
            ]  if isinstance(self.left, FHIRPath) else ensure_list(self.left), 
            [ 
                item.value if isinstance(item, FHIRPathCollectionItem) else item  
                    for item in ensure_list(self.right.evaluate(collection, create))
            ] if isinstance(self.right, FHIRPath) else ensure_list(self.right)
        )

    def __str__(self):
        return f'{self.left}{self.op}{self.right}'

    def __repr__(self):
        return f'Operation({self.left.__repr__()}{self.op}{self.right.__repr__()})'

    def __eq__(self, other):
        return isinstance(other, Operation) and self.left == other.left and self.right == other.right and self.op == other.op

    def __hash__(self):
        return hash((self.left, self.op, self.right))
        
    
