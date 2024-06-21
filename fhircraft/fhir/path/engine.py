import logging
from itertools import *  # noqa
from fhircraft.fhir.path.lexer import FhirPathLexer
from fhircraft.utils import ensure_list, flatten_list_of_lists, is_list_of_lists
from fhir.resources.core.utils.common import is_list_type, get_fhir_type_name, is_primitive_type
from fhir.resources.R4B.fhirtypesvalidators import get_fhir_model_class
from fhir.resources.core.fhirabstractmodel import FHIRAbstractModel as FhirResource
import typing
from abc import ABC
from dataclasses import dataclass

# Get logger name
logger = logging.getLogger(__name__)

# Turn on/off the automatic creation of id attributes
# ... could be a kwarg pervasively but uses are rare and simple today
auto_id_field = None

NOT_SET = object()
LIST_KEY = object()

class FHIRPathError(Exception):
    pass


class FHIRPath(ABC):
    """
    The base class for FHIRPath abstract syntax; those
    methods stubbed here are the interface to supported
    FHIRPath semantics.
    """

    def get_value(self, data):
        matches = ensure_list(self.find(data))
        values = [match.value for match in matches if match.value is not None and match.value != [] and not isinstance(match.value, bool)]
        if len(values) == 1:
            values = values[0]
        elif len(values) == 0:
            return None
        return values        

    def find(self, resource):
        """
        All `FHIRPath` types support `find()`, which returns an iterable of `FHIRPathCollection`s.
        They keep track of the path followed to the current location, so if the calling code
        has some opinion about that, it can be passed in here as a starting point.
        """
        # Ensure that entrypoint is a FHIRPathCollection instance
        collection = FHIRPathCollection.wrap(resource)
        return self.evaluate(collection, create=False)

    def find_or_create(self, resource):
        """
        All `FHIRPath` types support `find()`, which returns an iterable of `FHIRPathCollection`s.
        They keep track of the path followed to the current location, so if the calling code
        has some opinion about that, it can be passed in here as a starting point.
        """
        # Ensure that entrypoint is a FHIRPathCollection instance
        collection = FHIRPathCollection.wrap(resource)
        return self.evaluate(collection, create=True)

    def update(self, resource, value):
        """
        Returns `collection` with the specified path replaced by `value`. Only updates
        if the specified path exists.
        """
        # Ensure that entrypoint is a FHIRPathCollection instance
        base_collection = FHIRPathCollection.wrap(resource)
        # Collect the elements and set the values for each of them
        for collection in self.evaluate(base_collection, create=False):
            collection.set_value(value)

    def update_or_create(self, resource, value):
        """
        Returns `data` with the specified path replaced by `value`. Creates uthe specified 
        path if it does not exist.
        """        
        # Ensure that entrypoint is a FHIRPathCollection instance
        base_collection = FHIRPathCollection.wrap(resource)
        # Collect the elements and set the values for each of them
        for collection in self.evaluate(base_collection, create=True):
            collection.set_value(value)

    def evaluate(self, collection, create):
        """
        Placeholder for update logic
        """   
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

    def make_collection(self, value):
        if isinstance(value, FHIRPathCollection):
            return value
        else:
            return FHIRPathCollection(value, path=Root(), context=None)


class FHIRPathCollection:
    """
    A context-aware represetation of a FHIRPath collection.
    """
    @classmethod
    def wrap(cls, data: typing.Union["FHIRPathCollection",FhirResource]):
        if isinstance(data, cls):
            return data
        else:
            return cls(data)

    def __init__(self, value, path=None, index=None, context=None):
        self.value = value
        self.path = path or This()
        self.index =  index
        self.context = None if context is None else FHIRPathCollection.wrap(context)

    def set_value(self, value): 
        """
        Set the value of the current FHIRPathCollection instance.

        Parameters:
        value (any): The value to be set for the current FHIRPathCollection instance.

        Raises:
        ValueError: If the value has more than one item and the element does not allow arrays.
        """        
        if self.is_list_type: 
            value = ensure_list(value)
        else:
            if isinstance(value, list):
                if len(value)>1:
                    raise ValueError(f'Value has {len(value)} items, but element <{self.full_path}> does not allow arrays')
                value = value[0]
        parents = ensure_list(self.context.value)
        if getattr(self.path, 'index', None) is not None: 
                parents[self.path.index] = value
        elif getattr(self.path, 'label', None) is not None:
            for parent in parents:
                setattr(parent, self.path.label, value)
                self.value = getattr(parent, self.path.label)
        else:
            raise NotImplementedError()
        
    def set_index(self, index):
        parents = []
        for item in ensure_list(self.context.value):
            if isinstance(item, list):
                parents.extend(item)  
            else:
                parents.append(item)   
        self.value = parents[index]

    @property
    def field_info(self):
        parent = self.context.value
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
        return self.path if self.context is None else self.context.full_path.child(self.path)


    def __repr__(self):
        return '%s(value=%r, path=%r, context=%r)' % (self.__class__.__name__, self.value, self.path, self.context)

    def __eq__(self, other):
        return isinstance(other, FHIRPathCollection) and other.value == self.value and other.path == self.path and self.context == other.context


class BinaryExpression(FHIRPath):
    def __init__(self, left : typing.Union[str,FHIRPath], op : callable,right : typing.Union[str,FHIRPath]):
        self.left = left
        self.op = op
        self.right = right
        
    def evaluate(self, collection, create):
        return self.op(
            self.left.get_value(collection) if isinstance(self.left, FHIRPath) else self.left, 
            self.right.get_value(collection) if isinstance(self.right, FHIRPath) else self.right
        )

    def __str__(self):
        return f'{self.left}{self.op}{self.right}'

    def __repr__(self):
        return f'BinaryExpression({self.left.__repr__()}{self.op}{self.right.__repr__()})'

    def __eq__(self, other):
        return isinstance(other, BinaryExpression) and self.left == other.left and self.right == other.right and self.op == other.op

    def __hash__(self):
        return hash((self.left, self.op, self.right))
        
    


class Root(FHIRPath):
    """
    The FHIRPath referring to the "root" object. Concrete syntax is '$'.
    The root is the topmost collection without any context attached.
    """

    def evaluate(self, collection, create):
        if not isinstance(collection, FHIRPathCollection):
            return [FHIRPathCollection(collection, path=Root(), context=None)]
        else:
            if collection.context is None:
                return [FHIRPathCollection(collection.value, context=None, path=Root())]
            else:
                return Root().find(collection.context)

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
        return [FHIRPathCollection.wrap(collection)]

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

    def evaluate(self, collection: FHIRPathCollection, create: bool):
        return [
            child_collection
                for parent_collection in self.left.evaluate(collection, create)
                    for child_collection in self.right.evaluate(parent_collection, create)
        ]

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
        collection = FHIRPathCollection.wrap(collection)
        return [collection.context]

    def __eq__(self, other):
        return isinstance(other, Parent)

    def __str__(self):
        return '`parent`'

    def __repr__(self):
        return 'Parent()'

    def __hash__(self):
        return hash('parent')


class Where(FHIRPath):

    def __init__(self, expression: BinaryExpression):
        self.expression = expression
        
    def evaluate(self, collection, create):
        matches = FHIRPathCollection(value=[
                item
                for item in ensure_list(collection.value)
                    if self.expression.evaluate(item, create) 
        ], context=collection, path=collection.path)
        return [matches] 

    def __str__(self):
        return f'Where({self.expression})'

    def __repr__(self):
        return f'Where({self.expression.__repr__})'
    
    def __eq__(self, other):
        return isinstance(other, Where) and other.expression == self.expression

    def __hash__(self):
        return hash((self.expression))



class Extension(FHIRPath):

    def __init__(self, url):
        self.url = url

    def evaluate(self, collection, create):
        collection = FHIRPathCollection.wrap(collection)
        matches = FHIRPathCollection(value=[
            extension
                    for value in ensure_list(collection.value)
                        if hasattr(value, 'extension')
                            for extension in ensure_list(value.extension)
                                if extension and isinstance(extension, get_fhir_model_class('Extension')) and extension.url == self.url
        ], context=collection, path=collection.context)
        return [matches]

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

    def evaluate(self, element, create):
        element = FHIRPathCollection.wrap(element)
        matches = [
            FHIRPathCollection(getattr(obj, field), path=Element(field), context=element) 
                for obj in ensure_list(element.value)
                    for field in obj.__fields__.keys() 
                        if field.startswith(self.type_choice_name) and getattr(obj, field) 
        ]
        return matches

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
                                     for submatch in match_recursively(FHIRPathCollection(collection.value[i], context=collection, path=Index(i)))]

            elif isinstance(collection.value, dict):
                recursive_matches = [submatch
                                     for field in collection.value.keys()
                                     for submatch in match_recursively(FHIRPathCollection(collection.value[field], context=collection, path=Element(field)))]

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

    def evaluate(self, collection: FHIRPathCollection, create: bool):
        parents = ensure_list(collection.value)
        element_collections = []
        for parent in parents:
            element = getattr(parent, self.label, None)
            # Create new collection for the element 
            element_collection = FHIRPathCollection(element, path=Element(self.label), context=collection)
            if element is None and create:
                    element = element_collection.construct_resource()
                    if is_list_type(element_collection.field_info):
                        element = [element]
                    element_collection.set_value(element)
            element_collections.append(element_collection)
        if len(element_collections)==1:
            return [element_collections[0]]
        else:
            return [FHIRPathCollection([col.value for col in element_collections], path=Element(self.label), context=collection)]


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
        evaluate(collection: FHIRPathCollection, create: bool): Evaluates the index on the given FHIRPathCollection.
    """
    def __init__(self, index: int):
        if not isinstance(index, int):
            raise FHIRPathError('Index() argument must be an integer number.')
        self.index = index
    
    def evaluate(self, collection: FHIRPathCollection, create: bool) -> typing.List[FHIRPathCollection]:
        """
        Evaluates the index on the given collection.

        Parameters:
            collection (FHIRPathCollection): The FHIRPathCollection on which the index is evaluated.
            create (bool): A flag indicating whether to create new elements if the array is too short.

        Returns:
            List[FHIRPathCollection]: A list containing the FHIRPathCollection of the element at the specified index, if within array bounds.

        Raises:
            FHIRPathError: If the collection value is not a list, or if the index is out of bounds and create is False.
        """        
        # Ensure that we are working with an array            
        array = ensure_list(collection.value)
        # Check wheter array is too short and it can be extended 
        if len(array) <= self.index and create:
            # Calculate how many elements must be padded
            pad = self.index - len(array) + 1
            if collection.context:
                array.extend([collection.construct_resource() for __ in range(pad)])   
            else:
                array.extend([FHIRPathCollection.wrap(None) for __ in range(pad)])
        # If index is within array bounds, get element
        if array and len(array) > self.index:
            item_collection = FHIRPathCollection(array[self.index], path=self,  context=collection)            
            return [item_collection]
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
    def __init__(self, start=None, end=None, step=None):
        self.start = start
        self.end = end
        self.step = step

    def evaluate(self, collection, create):
        collection = FHIRPathCollection.wrap(collection)

        # Used for catching null value instead of empty list in path
        if not collection.value:
            return []
        if self.end < 0:
            self.end = len(collection.value) + self.end + 1 
        # Here's the hack. If it is a dictionary or some kind of constant,
        # put it in a single-element list
        if (isinstance(collection.value, dict) or isinstance(collection.value, int) or isinstance(collection.value, str)):
            return self.find(FHIRPathCollection([collection.value], path=collection.path, context=collection.context))

        # Some iterators do not support slicing but we can still
        # at least work for '*'
        if self.start is None and self.end is None and self.step is None:
            return [FHIRPathCollection(collection.value[i], path=Index(i), context=collection) for i in range(0, len(collection.value))]
        else:
            return [FHIRPathCollection(collection.value[i], path=Index(i), context=collection) for i in range(0, len(collection.value))[self.start:self.end:self.step]]

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
