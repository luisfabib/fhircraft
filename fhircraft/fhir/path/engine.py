import logging
from itertools import *  # noqa
from fhircraft.fhir.path.lexer import FhirPathLexer
from fhircraft.utils import ensure_list, flatten_list_of_lists, is_list_of_lists
from fhir.resources.core.utils.common import is_list_type, get_fhir_type_name, is_primitive_type
from fhir.resources.R4B.fhirtypesvalidators import get_fhir_model_class
from fhir.resources.core.fhirabstractmodel import FHIRAbstractModel as FhirResource
import typing

# Get logger name
logger = logging.getLogger(__name__)

# Turn on/off the automatic creation of id attributes
# ... could be a kwarg pervasively but uses are rare and simple today
auto_id_field = None

NOT_SET = object()
LIST_KEY = object()

class FHIRPathError(Exception):
    pass


class FHIRPath:
    """
    The base class for FHIRPath abstract syntax; those
    methods stubbed here are the interface to supported
    FHIRPath semantics.
    """

    def get_value(self, data):
        matches = ensure_list(self.find(data))
        values = [match.value for match in matches if match.value is not None or match.value != [] or isinstance(match.value, bool)]
        if len(values) == 1:
            values = values[0]
        elif len(values) == 0:
            return None
        return values        

    def find(self, data):
        """
        All `FHIRPath` types support `find()`, which returns an iterable of `FHIRElementContext`s.
        They keep track of the path followed to the current location, so if the calling code
        has some opinion about that, it can be passed in here as a starting point.
        """
        raise NotImplementedError()

    def find_or_create(self, data):
        return self.find(data)

    def update(self, data, val):
        """
        Returns `data` with the specified path replaced by `val`. Only updates
        if the specified path exists.
        """

        raise NotImplementedError()

    def update_or_create(self, data, val):
        return self.update(data, val)

    def filter(self, fn, data):
        """
        Returns `data` with the specified path filtering nodes according
        the filter evaluation result returned by the filter function.

        Arguments:
            fn (function): unary function that accepts one argument
                and returns bool.
            data (dict|list|tuple): JSON object to filter.
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

    def make_datum(self, value):
        if isinstance(value, FHIRElementContext):
            return value
        else:
            return FHIRElementContext(value, path=Root(), context=None)


class FHIRElementContext:
    """
    Represents a datum along a path from a context.

    Essentially a zipper but with a structure represented by FHIRPath,
    and where the context is more of a parent pointer than a proper
    representation of the context.

    For quick-and-dirty work, this proxies any non-special attributes
    to the underlying datum, but the actual datum can (and usually should)
    be retrieved via the `value` attribute.

    To place `datum` within another, use `datum.in_context(context=..., path=...)`
    which extends the path. If the datum already has a context, it places the entire
    context within that passed in, so an object can be built from the inside
    out.
    """
    @classmethod
    def wrap(cls, data: typing.Union["FHIRElementContext",FhirResource]):
        if isinstance(data, cls):
            return data
        else:
            return cls(data)

    def __init__(self, value, path=None, index=None, context=None):
        self.value = value
        self.path = path or This()
        self.index =  index
        self.context = None if context is None else FHIRElementContext.wrap(context)

    def set_value(self, value): 
        if self.is_list_type: 
            value = ensure_list(value)
        else:
            if isinstance(value, list):
                if len(value)>1:
                    raise ValueError(f'Value has {len(value)} items, but element <{self.full_path}> does not allow arrays')
                value = value[0]
        parents = self.context.value
        if not isinstance(parents, list):
            parents = [parents]
        for parent in parents:
            setattr(parent, self.name, value)
            self.value = getattr(parent, self.name)

    def set_index(self, index):
        parents = []
        for item in ensure_list(self.context.value):
            if isinstance(item, list):
                parents.extend(item)  # Flatten one level
            else:
                parents.append(item)  # Preserve non-list items     
        self.value = parents[index]

    @property
    def name(self) -> str:
        return ''.join(self.path.fields)
    
    @property
    def field_info(self):
        parent = self.context.value
        if isinstance(parent, list):
            parent = parent[0]
        return parent.__fields__.get(*self.path.fields)
    
    @property
    def is_list_type(self):
        return is_list_type(self.field_info)

    def construct_resource(self):
        try:
            model = get_fhir_model_class(get_fhir_type_name(self.field_info.type_))
            model.Config.validate_assignment = False
            return model.construct()
        except KeyError:
            return None 
        
    def in_context(self, context, path):
        context = FHIRElementContext.wrap(context)

        if self.context:
            return FHIRElementContext(value=self.value, path=self.path, context=context.in_context(path=path, context=context))
        else:
            return FHIRElementContext(value=self.value, path=path, context=context)

    @property
    def full_path(self):
        return self.path if self.context is None else self.context.full_path.child(self.path)

    @property
    def id_pseudopath(self):
        """
        Looks like a path, but with ids stuck in when available
        """
        try:
            pseudopath = Fields(str(self.value[auto_id_field]))
        except (TypeError, AttributeError, KeyError): # This may not be all the interesting exceptions
            pseudopath = self.path

        if self.context:
            return self.context.id_pseudopath.child(pseudopath)
        else:
            return pseudopath

    def __repr__(self):
        return '%s(value=%r, path=%r, context=%r)' % (self.__class__.__name__, self.value, self.path, self.context)

    def __eq__(self, other):
        return isinstance(other, FHIRElementContext) and other.value == self.value and other.path == self.path and self.context == other.context


class AutoIdForDatum(FHIRElementContext):
    """
    This behaves like a FHIRElementContext, but the value is
    always the path leading up to it, not including the "id",
    and with any "id" fields along the way replacing the prior
    segment of the path

    For example, it will make "foo.bar.id" return a datum
    that behaves like FHIRElementContext(value="foo.bar", path="foo.bar.id").

    This is disabled by default; it can be turned on by
    settings the `auto_id_field` global to a value other
    than `None`.
    """

    def __init__(self, datum, id_field=None):
        """
        Invariant is that datum.path is the path from context to datum. The auto id
        will either be the id in the datum (if present) or the id of the context
        followed by the path to the datum.

        The path to this datum is always the path to the context, the path to the
        datum, and then the auto id field.
        """
        self.datum = datum
        self.id_field = id_field or auto_id_field

    @property
    def value(self):
        return str(self.datum.id_pseudopath)

    @property
    def path(self):
        return self.id_field

    @property
    def context(self):
        return self.datum

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.datum)

    def in_context(self, context, path):
        return AutoIdForDatum(self.datum.in_context(context=context, path=path))

    def __eq__(self, other):
        return isinstance(other, AutoIdForDatum) and other.datum == self.datum and self.id_field == other.id_field


class Root(FHIRPath):
    """
    The FHIRPath referring to the "root" object. Concrete syntax is '$'.
    The root is the topmost datum without any context attached.
    """

    def find(self, data):
        if not isinstance(data, FHIRElementContext):
            return [FHIRElementContext(data, path=Root(), context=None)]
        else:
            if data.context is None:
                return [FHIRElementContext(data.value, context=None, path=Root())]
            else:
                return Root().find(data.context)

    def update(self, data, val):
        return val

    def filter(self, fn, data):
        return data if fn(data) else None

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
    The FHIRPath referring to the current datum. Concrete syntax is '@'.
    """

    def find(self, datum):
        return [FHIRElementContext.wrap(datum)]

    def update(self, data, val):
        return val

    def filter(self, fn, data):
        return data if fn(data) else None

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

    def find(self, resource: FhirResource):
        return [
            submatch
                for subdata in self.left.find(resource)
                    for submatch in self.right.find(subdata)
        ]

    def update(self, resource: FhirResource, value: typing.Any):
        for element in self.left.find(resource):
            self.right.update(element, value)

    def find_or_create(self, element):
        element = FHIRElementContext.wrap(element)
        submatches = []
        for subelement in self.left.find_or_create(element):
            for submatch in self.right.find_or_create(subelement):
                submatches.append(submatch)
        return submatches

    def update_or_create(self, resource: FhirResource, value: typing.Any):
        for element in self.left.find_or_create(resource):                
            self.right.update_or_create(element, value)
        return _clean_list_keys(resource)

    def filter(self, fn, data):
        for datum in self.left.find(data):
            self.right.filter(fn, datum.value)
        return data

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

    def find(self, datum):
        datum = FHIRElementContext.wrap(datum)
        return [datum.context]

    def __eq__(self, other):
        return isinstance(other, Parent)

    def __str__(self):
        return '`parent`'

    def __repr__(self):
        return 'Parent()'

    def __hash__(self):
        return hash('parent')


class Where(FHIRPath):

    def __init__(self, descendant, value):
        self.descendant = descendant
        self.value = value
        
    def find(self, datum):
        matches = FHIRElementContext(value=[
                item
                for item in datum.value
                    for descendant_match in self.descendant.find(item)
                        for condition_value in ensure_list(descendant_match.value)
                            if condition_value is not None and condition_value == str(self.value)
        ], context=datum, path=datum.path)
        return [matches] 

    def update(self, data, val):
        for datum in self.find(data):
            datum.path.update(data, val)
        return data

    def filter(self, fn, data):
        for datum in self.find(data):
            datum.path.filter(fn, datum.value)
        return data

    def __str__(self):
        return f'{self.left}.Where({self.descendant}="{self.value}")'

    def __repr__(self):
        return f'{self.left}.Where({self.descendant}="{self.value}")'
    
    def __eq__(self, other):
        return isinstance(other, Where) and other.descendant == self.descendant  and other.value == self.value

    def __hash__(self):
        return hash((self.left, self.descendant, self.value))



class Extension(FHIRPath):

    def __init__(self, left, url):
        self.left = left
        self.url = url

    def find(self, element):
        element = FHIRElementContext.wrap(element)
        matches = FHIRElementContext(value=[
            extension
                for match in self.left.find(element)
                    for value in ensure_list(match.value)
                        if hasattr(value, 'extension')
                            for extension in ensure_list(value.extension)
                                if extension and isinstance(extension, get_fhir_model_class('Extension')) and extension.url == self.url
        ], context=element, path=element.context)
        return [matches]

    def update(self, data, val):
        for datum in self.find(data):
            datum.path.update(data, val)
        return data

    def filter(self, fn, data):
        for datum in self.find(data):
            datum.path.filter(fn, datum.value)
        return data

    def __str__(self):
        return f'{self.left}.Extension("{self.url}")'

    def __repr__(self):
        return f'{self.left}.Extension("{self.url}")'
    
    def __eq__(self, other):
        return isinstance(other, Extension) and other.url == self.url

    def __hash__(self):
        return hash((self.left, self.url))


class TypeChoice(FHIRPath):
    
    def __init__(self, type_choice_name):
        self.type_choice_name = type_choice_name

    def find(self, element):
        # type_choice_name = self.type_choice_name.right.fields[0]
        element = FHIRElementContext.wrap(element)
        matches = [
            FHIRElementContext(getattr(obj, field), path=Fields(field), context=element) 
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

    def find(self, datum):
        # <left> .. <right> ==> <left> . (<right> | *..<right> | [*]..<right>)
        #
        # With with a wonky caveat that since Slice() has funky coercions
        # we cannot just delegate to that equivalence or we'll hit an
        # infinite loop. So right here we implement the coercion-free version.

        # Get all left matches into a list
        left_matches = self.left.find(datum)
        if not isinstance(left_matches, list):
            left_matches = [left_matches]

        def match_recursively(datum):
            right_matches = self.right.find(datum)

            # Manually do the * or [*] to avoid coercion and recurse just the right-hand pattern
            if isinstance(datum.value, list):
                recursive_matches = [submatch
                                     for i in range(0, len(datum.value))
                                     for submatch in match_recursively(FHIRElementContext(datum.value[i], context=datum, path=Index(i)))]

            elif isinstance(datum.value, dict):
                recursive_matches = [submatch
                                     for field in datum.value.keys()
                                     for submatch in match_recursively(FHIRElementContext(datum.value[field], context=datum, path=Fields(field)))]

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

    def filter(self, fn, data):
        # Get all left matches into a list
        left_matches = self.left.find(data)
        if not isinstance(left_matches, list):
            left_matches = [left_matches]

        def filter_recursively(data):
            # Update only mutable values corresponding to JSON types
            if not (isinstance(data, list) or isinstance(data, dict)):
                return

            self.right.filter(fn, data)

            # Manually do the * or [*] to avoid coercion and recurse just the right-hand pattern
            if isinstance(data, list):
                for i in range(0, len(data)):
                    filter_recursively(data[i])

            elif isinstance(data, dict):
                for field in data.keys():
                    filter_recursively(data[field])

        for submatch in left_matches:
            filter_recursively(submatch.value)

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


class Fields(FHIRPath):
    """
    FHIRPath referring to some field of the current object.
    Concrete syntax ix comma-separated field names.

    WARNING: If '*' is any of the field names, then they will
    all be returned.
    """

    def __init__(self, *fields):
        self.fields = fields

    @staticmethod
    def get_subelement(element, field, create):
        if isinstance(element.value, list):
            field_value = []
            for value in element.value:
                if isinstance(value, list):
                    field_value.extend([getattr(val, field, None) for val in value])
                else:
                    field_value.append(getattr(value, field, None))
            empty_value = all([val is None for val in field_value])
            if len(field_value)==1:
                field_value = field_value[0]

        else:
            field_value = getattr(element.value, field, None)
            empty_value = field_value is None
        sub_element = FHIRElementContext(field_value, path=Fields(field), context=element)
        if empty_value:
            if create:
                try:
                    field_value = sub_element.construct_resource()
                    sub_element.set_value(field_value)
                except KeyError:
                    if sub_element.is_list_type:
                        sub_element.set_value([])
                        return sub_element
                    else:
                        return None            
            else:
                return None
        return sub_element


    def reified_fields(self, datum):
        if '*' not in self.fields:
            return self.fields
        else:
            fields = tuple(datum.value.__fields__keys())
            return fields

    def find(self, element: typing.Union[FHIRElementContext,FhirResource]):
        return self._find_base(element, create=False)

    def find_or_create(self, element: typing.Union[FHIRElementContext,FhirResource]):
        return self._find_base(element, create=True)

    def _find_base(self, element: typing.Union[FHIRElementContext,FhirResource], create:bool):
        # Ensure that element is of a FHIRElementContext 
        element = FHIRElementContext.wrap(element)
        # Get subelements
        field_data = [
            self.get_subelement(element, field, create)
                for field in self.reified_fields(element)
        ]
        # Clean unset values
        field_data = [fd for fd in field_data if fd is not None]
        return field_data

    def update(self, element: typing.Union[FHIRElementContext,FhirResource], value):
        return self._update_base(element, value, create=False)

    def update_or_create(self, element: typing.Union[FHIRElementContext,FhirResource], value):
        return self._update_base(element, value, create=True)

    def _update_base(self, element: typing.Union[FHIRElementContext,FhirResource], val: typing.Any, create: bool):
        element = FHIRElementContext.wrap(element)       
        if element.value is not None: 
            if isinstance(element.value, list):
                return [self._update_base(el, val, create) for el in element.value]
            for field in self.reified_fields(element):
                sub_element = FHIRElementContext(None, path=Fields(field), context=element)
                sub_element.set_value(val)
        return element

    def filter(self, fn, data):
        if data is not None:
            for field in self.reified_fields(FHIRElementContext.wrap(data)):
                if field in data:
                    if fn(data[field]):
                        data.pop(field)
        return data

    def __str__(self):
        fields_as_str = ("'" + str(f) + "'" if any([l in f for l in FhirPathLexer.literals]) else
                         str(f) for f in self.fields)
        return ','.join(fields_as_str)


    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ','.join(map(repr, self.fields)))

    def __eq__(self, other):
        return isinstance(other, Fields) and tuple(self.fields) == tuple(other.fields)

    def __hash__(self):
        return hash(tuple(self.fields))


class Index(FHIRPath):
    """
    FHIRPath that matches indices of the current datum, or none if not large enough.
    Concrete syntax is brackets.

    WARNING: If the datum is None or not long enough, it will not crash but will not match anything.
    NOTE: For the concrete syntax of `[*]`, the abstract syntax is a Slice() with no parameters (equiv to `[:]`
    """

    def __init__(self, index):
        self.index = index

    def _pad_array(self, element:FHIRElementContext) -> FHIRElementContext:
        # Use a list comprehension to flatten the list of lists
        array = []
        for item in element.value:
            if isinstance(item, list):
                array.extend(item)  # Flatten one level
            else:
                array.append(item)  # Preserve non-list items
        
        if len(array) <= self.index:          
            pad = self.index - len(array) + 1
            array.extend([element.construct_resource() for __ in range(pad)])   
            element.set_value(array)
        
    def find(self, datum):
        return self._find_base(datum, create=False)

    def find_or_create(self, datum):   
        return self._find_base(datum, create=True)

    def _find_base(self, element: typing.Union[FHIRElementContext,FhirResource], create: bool):
        element = FHIRElementContext.wrap(element)
        if create:
            self._pad_array(element)
        if element.value and len(element.value) > self.index:
            item_element = FHIRElementContext(None, path=self,  context=element)
            item_element.set_index(self.index)
            return [item_element]
        else:
            return []

    def update(self, data: typing.Union[FHIRElementContext,FhirResource], val: typing.Any):
        return self._update_base(data, val, create=False)

    def update_or_create(self, data: typing.Union[FHIRElementContext,FhirResource], val: typing.Any):
        return self._update_base(data, val, create=True)

    def _update_base(self, element: typing.Union[FHIRElementContext,FhirResource], val: typing.Any, create: bool):
        element = FHIRElementContext.wrap(element)                          
        if create:
            self._pad_array(element)
        array = element.value
        if hasattr(val, '__call__'):
            array[self.index] = val.__call__(array[self.index], element, self.index)
        elif len(array) > self.index:
            array[self.index] = val
        element.set_value(array)
        return element

    def filter(self, fn, data):
        if fn(data[self.index]):
            data.pop(self.index) 
        return data

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

    def _find_base(self, datum, create):
        if not datum.value or len(datum.value) != 1:
            raise FHIRPathError(f'Expected single value for {datum.full_path}.single(), instead got {len(datum.value)} values')
        return super()._find_base(datum, create)

    def _update_base(self, data, val, create):
        if not isinstance(val, list):
            vals = [val]
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

    def find(self, datum):
        datum = FHIRElementContext.wrap(datum)

        # Used for catching null value instead of empty list in path
        if not datum.value:
            return []
        if self.end < 0:
            self.end = len(datum.value) + self.end 
        # Here's the hack. If it is a dictionary or some kind of constant,
        # put it in a single-element list
        if (isinstance(datum.value, dict) or isinstance(datum.value, int) or isinstance(datum.value, str)):
            return self.find(FHIRElementContext([datum.value], path=datum.path, context=datum.context))

        # Some iterators do not support slicing but we can still
        # at least work for '*'
        if self.start is None and self.end is None and self.step is None:
            return [FHIRElementContext(datum.value[i], path=Index(i), context=datum) for i in range(0, len(datum.value))]
        else:
            return [FHIRElementContext(datum.value[i], path=Index(i), context=datum) for i in range(0, len(datum.value))[self.start:self.end:self.step]]

    def update(self, data, val):
        for datum in self.find(data):
            datum.path.update(data, val)
        return data

    def filter(self, fn, data):
        while True:
            length = len(data)
            for datum in self.find(data):
                data = datum.path.filter(fn, data)
                if len(data) < length:
                    break

            if length == len(data):
                break
        return data

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


def _create_list_key(dict_):
    """
    Adds a list to a dictionary by reference and returns the list.

    See `_clean_list_keys()`
    """
    dict_[LIST_KEY] = new_list = [{}]
    return new_list


def _clean_list_keys(struct_):
    """
    Replace {LIST_KEY: ['foo', 'bar']} with ['foo', 'bar'].

    >>> _clean_list_keys({LIST_KEY: ['foo', 'bar']})
    ['foo', 'bar']

    """
    if(isinstance(struct_, list)):
        for ind, value in enumerate(struct_):
            struct_[ind] = _clean_list_keys(value)
    elif(isinstance(struct_, dict)):
        if(LIST_KEY in struct_):
            return _clean_list_keys(struct_[LIST_KEY])
        else:
            for key, value in struct_.items():
                struct_[key] = _clean_list_keys(value)
    return struct_