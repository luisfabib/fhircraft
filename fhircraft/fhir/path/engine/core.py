import logging
from itertools import *  # noqa
from fhircraft.utils import ensure_list
from fhir.resources.core.utils.common import is_list_type, get_fhir_type_name
from fhir.resources.R4B.fhirtypesvalidators import get_fhir_model_class
from fhir.resources.core.fhirabstractmodel import FHIRAbstractModel as FhirResource
import typing
from typing import List, Optional
from abc import ABC
from dataclasses import dataclass, field
from functools import partial

# Get logger name
logger = logging.getLogger(__name__)

class FHIRPathError(Exception):
    pass


class FHIRPath(ABC):
    """
    The base class for FHIRPath abstract syntax; those
    methods stubbed here are the interface to supported
    FHIRPath semantics.
    """

    def get_value(self, data):
        collection = self.find(data)
        values = [item.value for item in collection if item.value and not isinstance(item.value, bool)]
        if len(values) == 1:
            values = values[0]
        elif len(values) == 0:
            return None
        return values        

    def find(self, collection):
        # Ensure that entrypoint is a FHIRPathCollectionItem instance
        collection = [FHIRPathCollectionItem.wrap(item) for item in ensure_list(collection)]
        return self.evaluate(collection, create=False)

    def find_or_create(self, collection):
        # Ensure that entrypoint is a FHIRPathCollectionItem instance
        collection = [FHIRPathCollectionItem.wrap(item) for item in ensure_list(collection)]
        return self.evaluate(collection, create=True)

    def update(self, collection, value):
        # Ensure that entrypoint is a FHIRPathCollectionItem instance
        collection = [FHIRPathCollectionItem.wrap(item) for item in ensure_list(collection)]
        # Collect the elements and set the values for each of them
        new_collection = self.evaluate(collection, create=False)
        for item in new_collection:
            item.set_value(value)

    def update_or_create(self, collection, value, replace=False):      
        # Ensure that entrypoint is a FHIRPathCollectionItem instance
        collection = [FHIRPathCollectionItem.wrap(item) for item in ensure_list(collection)]
        # Collect the elements and set the values for each of them
        for item in self.evaluate(collection, create=True):
            item.set_value(value)

    def evaluate(self, collection, create):
        raise NotImplementedError()        

    def child(self, child):
        """
        Equivalent to Child(self, next) but with some canonicalization
        """
        if isinstance(self, This) or isinstance(self, Root):
            return child
        elif isinstance(child, This):
            return self
        elif isinstance(child, Root):
            return child
        else:
            return Child(self, child)


class FHIRPathFunction(FHIRPath):

    def __str__(self):
        return f'{self.__class__.__name__.lower()}()'

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __eq__(self, other):
        return isinstance(other, self.__class__)


@dataclass
class FHIRPathCollectionItem(object):
    """
    A parent-aware represetation of a FHIRPath collection item.
    """
    value: typing.Any
    path: FHIRPath = field(default_factory=lambda: This())
    element: Optional[str] = None
    index: Optional[int] = None
    parent: Optional["FHIRPathCollectionItem"] = None
    setter: Optional[callable] = None

    @classmethod
    def wrap(cls, data: typing.Union["FHIRPathCollectionItem",FhirResource]):
        if isinstance(data, cls):
            return data
        else:
            return cls(data)

    def set_literal(self,value):
        setattr(self.parent.value, self.path.label, value)
        
    def set_value(self,value):
        if self.setter:
            if isinstance(value, list):
                raise ValueError('Only single value is accepted')
            self.setter(value)
        else:
            raise RuntimeError('There is not setter function associated with this item')
        

    def set_index(self, index):
        parents = []
        for item in ensure_list(self.parent.value):
            if isinstance(item, list):
                parents.extend(item)  
            else:
                parents.append(item)   
        self.value = parents[index]

    @property
    def field_info(self):
        parent = self.parent.value
        if isinstance(parent, list):
            parent = parent[0]
        if hasattr(parent, '__fields__') and hasattr(self.path, 'label'):
            return parent.__fields__.get(self.path.label)
        return None
    
    @property
    def is_list_type(self):
        if not self.field_info:
            return False
        return is_list_type(self.field_info)

    def construct_resource(self):
        try:
            model = get_fhir_model_class(get_fhir_type_name(self.field_info.type_))
            model.Config.validate_assignment = False
            return model.construct()    
        except (KeyError, AttributeError):
            return None 
        
    @property
    def full_path(self):
        return self.path if self.parent is None else self.parent.full_path.child(self.path)

    def __repr__(self):
        return f'FHIRPathCollectionItem(value={self.value.__repr__()[:10]}, element={self.element.__repr__()[:10]}..., index={self.index}, parent={self.parent.full_path if self.parent else None})'

    def __hash__(self):
        return hash((self.value, self.path, self.parent))
        



class Operation(FHIRPath):
    def __init__(self, left : typing.Union[str,FHIRPath], op : callable,right : typing.Union[str,FHIRPath]):
        self.left = left
        self.op = op
        self.right = right
        
    def evaluate(self, collection: List[FHIRPathCollectionItem], create: bool) -> bool:
        collection = ensure_list(collection)
        return self.op(
            [item.value for item in self.left.evaluate(collection, create)] if isinstance(self.left, FHIRPath) else ensure_list(self.left), 
            [item.value for item in self.right.evaluate(collection, create)] if isinstance(self.right, FHIRPath) else ensure_list(self.right)
        )

    def __str__(self):
        return f'{self.left}{self.op}{self.right}'

    def __repr__(self):
        return f'Operation({self.left.__repr__()}{self.op}{self.right.__repr__()})'

    def __eq__(self, other):
        return isinstance(other, Operation) and self.left == other.left and self.right == other.right and self.op == other.op

    def __hash__(self):
        return hash((self.left, self.op, self.right))
        
    


class Root(FHIRPath):
    """
    The FHIRPath referring to the "root" object. Concrete syntax is '$'.
    The root is the topmost collection without any parent attached.
    """

    def evaluate(self, collection, *args, **kwargs):
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
    The FHIRPath referring to the current collection. Concrete syntax is '@'.
    """

    def evaluate(self, collection, create):
        return ensure_list(collection)

    def __str__(self):
        return '`this`'

    def __repr__(self):
        return 'This()'

    def __eq__(self, other):
        return isinstance(other, This)

    def __hash__(self):
        return hash('this')


class Child(FHIRPath):
    """
    FHIRPath that first matches the left, then the right.
    Concrete syntax is <left> '.' <right>
    """

    def __init__(self, left:FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right

    def evaluate(self, collection: List[FHIRPathCollectionItem], create: bool):
        parent_collection = self.left.evaluate(collection, create)
        child_collection = self.right.evaluate(parent_collection, create)
        return child_collection

    def __eq__(self, other):
        return isinstance(other, Child) and self.left == other.left and self.right == other.right

    def __str__(self):
        return '%s.%s' % (self.left, self.right)

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.left, self.right)

    def __hash__(self):
        return hash((self.left, self.right))


class Parent(FHIRPath):
    """
    FHIRPath that matches the parent node of the current match.
    Will crash if no such parent exists.
    Available via named operator `parent`.
    """

    def find(self, collection):
        return [item.parent for item in collection]

    def __eq__(self, other):
        return isinstance(other, Parent)

    def __str__(self):
        return '`parent`'

    def __repr__(self):
        return 'Parent()'

    def __hash__(self):
        return hash('parent')



class Extension(FHIRPath):

    def __init__(self, url):
        self.url = url
        self.extension_class =  get_fhir_model_class('Extension')

    def evaluate(self, collection, create):
        collection = ensure_list(collection)
        return [
            item
                for item in Element('extension').find(collection)
                    if isinstance(item.value, self.extension_class) and item.value.url == self.url
        ]

    def __str__(self):
        return f'Extension("{self.url}")'

    def __repr__(self):
        return f'Extension("{self.url}")'
    
    def __eq__(self, other):
        return isinstance(other, Extension) and other.url == self.url

    def __hash__(self):
        return hash((self.url))


class TypeChoice(FHIRPath):
    
    def __init__(self, type_choice_name):
        self.type_choice_name = type_choice_name

    def evaluate(self, collection, *args, **kwargs):
        collection = ensure_list(collection)
        return  [
            FHIRPathCollectionItem(getattr(item.value, field), path=Element(field), parent=item) 
                for item in collection
                    for field in item.value.__fields__.keys() 
                        if field.startswith(self.type_choice_name) and getattr(item.value, field) 
        ]

    def __str__(self):
        return f'{self.type_choice_name}[x]'

    def __repr__(self):
        return f'{self.type_choice_name}[x]'
    
    def __eq__(self, other):
        return isinstance(other, TypeChoice) and other.type_choice_name == self.type_choice_name

    def __hash__(self):
        return hash((self.type_choice_name))
    
class Descendants(FHIRPath):
    """
    FHIRPath that matches first the left expression then any descendant
    of it which matches the right expression.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def find(self, collection):
        # <left> .. <right> ==> <left> . (<right> | *..<right> | [*]..<right>)
        #
        # With with a wonky caveat that since Slice() has funky coercions
        # we cannot just delegate to that equivalence or we'll hit an
        # infinite loop. So right here we implement the coercion-free version.

        # Get all left matches into a list
        left_matches = self.left.find(collection)
        if not isinstance(left_matches, list):
            left_matches = [left_matches]

        def match_recursively(collection):
            right_matches = self.right.find(collection)

            # Manually do the * or [*] to avoid coercion and recurse just the right-hand pattern
            if isinstance(collection.value, list):
                recursive_matches = [submatch
                                     for i in range(0, len(collection.value))
                                     for submatch in match_recursively(FHIRPathCollectionItem(collection.value[i], parent=collection, path=Index(i)))]

            elif isinstance(collection.value, dict):
                recursive_matches = [submatch
                                     for field in collection.value.keys()
                                     for submatch in match_recursively(FHIRPathCollectionItem(collection.value[field], parent=collection, path=Element(field)))]

            else:
                recursive_matches = []

            return right_matches + list(recursive_matches)

        # TODO: repeatable iterator instead of list?
        return [submatch
                for left_match in left_matches
                for submatch in match_recursively(left_match)]

    def is_singular(self):
        return False

    def update(self, data, val):
        # Get all left matches into a list
        left_matches = self.left.find(data)
        if not isinstance(left_matches, list):
            left_matches = [left_matches]

        def update_recursively(data):
            # Update only mutable values corresponding to JSON types
            if not (isinstance(data, list) or isinstance(data, dict)):
                return

            self.right.update(data, val)

            # Manually do the * or [*] to avoid coercion and recurse just the right-hand pattern
            if isinstance(data, list):
                for i in range(0, len(data)):
                    update_recursively(data[i])

            elif isinstance(data, dict):
                for field in data.keys():
                    update_recursively(data[field])

        for submatch in left_matches:
            update_recursively(submatch.value)

        return data

    def __str__(self):
        return '%s..%s' % (self.left, self.right)

    def __eq__(self, other):
        return isinstance(other, Descendants) and self.left == other.left and self.right == other.right

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.left, self.right)

    def __hash__(self):
        return hash((self.left, self.right))


class Union(FHIRPath):
    """
    FHIRPath that returns the union of the results of each match.
    This is pretty shoddily implemented for now. The nicest semantics
    in case of mismatched bits (list vs atomic) is to put
    them all in a list, but I haven't done that yet.

    WARNING: Any appearance of this being the _concatenation_ is
    coincidence. It may even be a bug! (or laziness)
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def is_singular(self):
        return False

    def find(self, data):
        return self.left.find(data) + self.right.find(data)

    def __eq__(self, other):
        return isinstance(other, Union) and self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash((self.left, self.right))

class Intersect(FHIRPath):
    """
    FHIRPath for bits that match *both* patterns.

    This can be accomplished a couple of ways. The most
    efficient is to actually build the intersected
    AST as in building a state machine for matching the
    intersection of regular languages. The next
    idea is to build a filtered data and match against
    that.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def is_singular(self):
        return False

    def find(self, data):
        raise NotImplementedError()

    def __eq__(self, other):
        return isinstance(other, Intersect) and self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash((self.left, self.right))


class Element(FHIRPath):
    """
    FHIRPath referring to some element in the FHIR resource.
    """

    def __init__(self, label: str):
        self.label = label

    def create_element(self, parent):
        if not parent:
            return None
        if not hasattr(parent, '__fields__'):
            return None 
        field_info = parent.__fields__.get(self.label)
        try:
            model = get_fhir_model_class(get_fhir_type_name(field_info.type_))
            model.Config.validate_assignment = False
            new_element = model.construct()    
        except (KeyError, AttributeError):
            new_element = None 
        if is_list_type(field_info):
            new_element = ensure_list(new_element)
        return new_element

    @staticmethod
    def setter(value, item, index, label):
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


class Index(FHIRPath):
    """
    A FHIRPath segment representing an index operator.

    Attributes:
        index (int): The index value for the FHIRPath index.

    Methods:
        evaluate(collection: FHIRPathCollectionItem, create: bool): Evaluates the index on the given FHIRPathCollectionItem.
    """
    def __init__(self, index: int):
        if not isinstance(index, int):
            raise FHIRPathError('Index() argument must be an integer number.')
        self.index = index
    
    def evaluate(self, collection: FHIRPathCollectionItem, create: bool) -> typing.List[FHIRPathCollectionItem]:
        """
        Evaluates the index on the given collection.

        Parameters:
            collection (FHIRPathCollectionItem): The FHIRPathCollectionItem on which the index is evaluated.
            create (bool): A flag indicating whether to create new elements if the array is too short.

        Returns:
            List[FHIRPathCollectionItem]: A list containing the FHIRPathCollectionItem of the element at the specified index, if within array bounds.

        Raises:
            FHIRPathError: If the collection value is not a list, or if the index is out of bounds and create is False.
        """        
        # Ensure that we are working with an array            
        collection = ensure_list(collection)
        # Check wheter array is too short and it can be extended 
        if len(collection) <= self.index and create:
            # Calculate how many elements must be padded
            pad = self.index - len(collection) + 1
            # if collection.parent:
            #     collection.extend([collection.construct_resource() for __ in range(pad)])   
            # else:
            all_same_parent = all([item.parent.value == collection[0].parent.value for item in collection])
            if all_same_parent:
                parent_array = collection[0]
                new_values = ensure_list(getattr(parent_array.parent.value, parent_array.path.label))
                if parent_array.parent:
                    new_values.extend([parent_array.construct_resource() for __ in range(pad)])   
                else:
                    new_values.extend([None for __ in range(pad)])
                return [FHIRPathCollectionItem(new_values[self.index], path=Element(parent_array.element), setter=partial(parent_array.setter, index=self.index), parent=parent_array.parent)]
            else:
                raise FHIRPathError(f'Cannot create new array element due to inhomogeneity in parents')
        # If index is within array bounds, get element
        if collection and len(collection) > self.index:
            return [collection[self.index]]
        # Else return empty list
        return []

    def __eq__(self, other):
        return isinstance(other, Index) and self.index == other.index

    def __str__(self):
        return '[%i]' % self.index

    def __repr__(self):
        return '%s(index=%r)' % (self.__class__.__name__, self.index)
        
    def __hash__(self):
        return hash(self.index)



class Single(Index):
    
    def __init__(self):
        super().__init__(index=0)

    def _find_base(self, collection, create):
        vals = ensure_list(collection.value)
        if not collection.value or len(vals) != 1:
            raise FHIRPathError(f'Expected single value for {collection.full_path}.single(), instead got {len(vals)} values')
        return super()._find_base(collection, create)

    def _update_base(self, data, val, create):
        vals = ensure_list(val)
        if len(vals) != 1:
            raise FHIRPathError(f'Expected single value, instead got {len(vals)} values')
        return super()._update_base(data, val, create)


class Slice(FHIRPath):
    """
    FHIRPath matching a slice of an array.

    Because of a mismatch between JSON and XML when schema-unaware,
    this always returns an iterable; if the incoming data
    was not a list, then it returns a one element list _containing_ that
    data.

    Consider these two docs, and their schema-unaware translation to JSON:

    <a><b>hello</b></a> ==> {"a": {"b": "hello"}}
    <a><b>hello</b><b>goodbye</b></a> ==> {"a": {"b": ["hello", "goodbye"]}}

    If there were a schema, it would be known that "b" should always be an
    array (unless the schema were wonky, but that is too much to fix here)
    so when querying with JSON if the one writing the JSON knows that it
    should be an array, they can write a slice operator and it will coerce
    a non-array value to an array.

    This may be a bit unfortunate because it would be nice to always have
    an iterator, but dictionaries and other objects may also be iterable,
    so this is the compromise.
    """
    def __init__(self, start=None, end=None, step=1):
        self.start = start
        self.end = end
        self.step = step

    def evaluate(self, collection, *args, **kwargs):
        collection = ensure_list(collection)
        # Slice the collection
        return collection[self.start:self.step:self.end]
        
    def __str__(self):
        if self.start is None and self.end is None and self.step is None:
            return '[*]'
        else:
            return '[%s%s%s]' % (self.start or '',
                                   ':%d'%self.end if self.end else '',
                                   ':%d'%self.step if self.step else '')

    def __repr__(self):
        return '%s(start=%r,end=%r,step=%r)' % (self.__class__.__name__, self.start, self.end, self.step)

    def __eq__(self, other):
        return isinstance(other, Slice) and other.start == self.start and self.end == other.end and other.step == self.step

    def __hash__(self):
        return hash((self.start, self.end, self.step))
