import logging
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Iterable, List, Optional, TypeVar
from venv import create

from fhircraft.fhir.path.utils import import_fhirpath_engine
from fhircraft.utils import contains_list_type, ensure_list, get_fhir_model_from_field

if TYPE_CHECKING:
    from fhircraft.fhir.path.parser import FhirPathParser

from typing import List

from fhircraft.fhir.path.exceptions import FHIRPathError

# Get logger name
logger = logging.getLogger(__name__)

FHIRPathCollection = List["FHIRPathCollectionItem"]


class FHIRPathMixin:
    """
    Mixin class to incorporate a simple FHIRPath interface to the child class.
    """

    @property
    def fhirpath(self) -> "FhirPathParser":
        """
        Initialized FHIRPath engine instance
        """
        return import_fhirpath_engine()

    def get_fhirpath(
        self, expression: str
    ) -> typing.Union[None, typing.Any, typing.List[typing.Any]]:
        """
        Evaluates and retrieves the value(s) of a FHIRPath expression

        Args:
            expression (str): FHIRPath expression to evaluate

        Returns:
            (Union[NoneType,Any, List[Any]): The extracted value(s), or None if no values are found.
        """
        # Evaluate the FHIRPath expression
        collection = self.fhirpath.parse(expression).evaluate_for(self)
        # Get the values of the collection items
        values = [
            item.value
            for item in collection
            if item.value and not isinstance(item.value, bool)
        ]
        if len(values) == 1:
            return values[0]
        elif len(values) == 0:
            return None
        else:
            return values

    def replace_fhirpath(self, expression: str, new_value: typing.Any) -> None:
        """
        Evaluates and replaces the value given by a FHIRPath expression

        Args:
            expression (str): FHIRPath expression to evaluate
        """
        # Evaluate the FHIRPath expression
        self.fhirpath.parse(expression).evaluate_and_replace(self, new_value)


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
    setter: Optional[Callable] = None

    @classmethod
    def wrap(cls, data: Any) -> "FHIRPathCollectionItem":
        """
        Wraps data in a FHIRPathCollectionItem instance.

        Args:
            data (Any): The data to be wrapped.

        Returns:
            item (FHIRPathCollectionItem): The wrapped FHIRPathCollectionItem instance.
        """
        if isinstance(data, cls):
            return data
        else:
            return cls(data)

    def set_literal(self, value):
        if not self.parent:
            raise RuntimeError("There is no parent to set the value on")
        setattr(self.parent.value, self.path.label, value)

    def set_value(self, value):
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
                raise ValueError("Only single value is accepted")
            self.setter(value)
        else:
            raise RuntimeError("There is not setter function associated with this item")

    @property
    def field_info(self):
        """
        Retrieves the field information from the parent's value.

        Returns:
           (Any): The field information, or None if not available.
        """
        if not self.parent:
            raise RuntimeError(
                "There is no parent to retrieve the field information from"
            )
        parent = self.parent.value
        if isinstance(parent, list):
            parent = parent[0]
        if hasattr(parent.__class__, "model_fields") and hasattr(self.path, "label"):
            return parent.__class__.model_fields.get(self.path.label)
        return None

    @property
    def is_list_type(self):
        """
        Checks if the field information indicates a list type.

        Returns:
            (bool): True if the field information indicates a list type, False otherwise.
        """
        if not self.field_info:
            return False
        return contains_list_type(self.field_info.annotation)

    def construct_resource(self):
        """
        Constructs a FHIR resource based on the field information.

        Returns:
            (Any): The constructed FHIR resource, or None if construction fails.
        """
        if self.field_info:
            model = get_fhir_model_from_field(self.field_info)
            if not model:
                raise ValueError(
                    f"Could not construct resource from field information: {self.field_info}"
                )
            return model.model_construct()

    @property
    def full_path(self):
        """
        Retrieves the full path of the item.

        Returns:
            (str): The full path of the item.
        """
        return (
            self.path if self.parent is None else self.parent.full_path.child(self.path)
        )

    def __eq__(self, value: Any) -> bool:
        if isinstance(value, FHIRPathCollectionItem):
            return (
                self.value == value.value
                and self.element == value.element
                and self.index == value.index
            )
        else:
            return self.value == value

    def __repr__(self):
        return f"FHIRPathCollectionItem(value={self.value.__repr__()[:10]}, element={self.element.__repr__()[:10]}..., index={self.index}, parent={self.parent.full_path if self.parent else None})"

    def __hash__(self):
        return hash((self.path, self.parent, self.value.__repr__()))


class FHIRPath(ABC):
    """
    Abstract base class representing a FHIRPath, used for navigating and manipulating
    FHIR resources.
    """

    def evaluate_for(self, data):
        collection = self._evaluate_wrapped(data)
        values = [item.value for item in collection]
        if len(values) == 1:
            values = values[0]
        elif len(values) == 0:
            return None
        return values

    def evaluate_and_replace(self, data, value):
        new_collection = self._evaluate_wrapped(data, create=True)
        for item in new_collection:
            item.set_value(value)

    def _evaluate_wrapped(self, data: typing.Any, create=False) -> FHIRPathCollection:
        # Ensure that entrypoint is a list of FHIRPathCollectionItem instances
        collection = [FHIRPathCollectionItem.wrap(item) for item in ensure_list(data)]
        return self.evaluate(collection, create=create)

    def evaluate(
        self, collection: FHIRPathCollection, create: bool
    ) -> FHIRPathCollection:
        """
        Evaluates the collection and returns a list of FHIRPathCollectionItem instances.

        Args:
            collection (Any): The input collection to evaluate.
            create (bool): Flag indicating whether to create new items if they do not exist.

        Returns:
            FHIRPathCollection: A list of FHIRPathCollectionItem instances.

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
        return f"{self.__class__.__name__.lower()}()"

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __eq__(self, other):
        return isinstance(other, self.__class__)


class Literal(FHIRPath):
    """
    A class representation of a constant literal value in the FHIRPath.

    Attributes:
        value (Any): The literal value to be represented.
    """

    def __init__(self, value: Any):
        self.value = value

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Simply returns the input collection.

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.

        Returns:
            collection (FHIRPathCollection): A list of FHIRPathCollectionItem instances after evaluation.
        """
        return [FHIRPathCollectionItem(self.value, parent=None, path=None)]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Literal(%r)" % (self.value,)

    def __eq__(self, other):
        return isinstance(other, Literal) and self.value == other.value

    def __hash__(self):
        return hash(("literal", self.value))


class Element(FHIRPath):
    """
    A class representing an element in a FHIRPath, used for navigating and manipulating FHIR resources.

    Attributes:
        label (str): The name of the element.
    """

    def __init__(self, label: str | Literal):
        if isinstance(label, Literal):
            label = label.value
        if not isinstance(label, str):
            raise FHIRPathError("Element() argument must be a string.")
        self.label = label

    def create_element(self, parent: typing.Any) -> typing.Any:
        """
        Ensure that the input parent object has the necessary field information to create a new element based on the label provided.

        Args:
            parent (Any): The parent object from which the element will be created.

        Returns:
            element (Any): The newly created element based on the field information of the parent object, or None if the parent is invalid or lacks the required field information.

        Raises:
            KeyError: If there is an issue with retrieving the field information from the parent object.
            AttributeError: If there is an attribute error while trying to create the new element.
        """
        if not parent:
            return None
        if not hasattr(parent.__class__, "model_fields"):
            return None
        field_info = parent.__class__.model_fields.get(self.label)
        model = get_fhir_model_from_field(field_info)
        if not model:
            new_element = None
        else:
            new_element = model.model_construct()
        if field_info and contains_list_type(field_info.annotation):
            new_element = ensure_list(new_element)
        return new_element

    @staticmethod
    def setter(
        value: typing.Any, item: FHIRPathCollectionItem, index: int, label: str
    ) -> None:
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
            if len(parents) <= index:
                parents.insert(index, value)
            else:
                parents[index] = value

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        element_collection = []
        for item in collection:
            if item.value is None:
                continue
            element_value = getattr(item.value, self.label, None)
            if not element_value and not isinstance(element_value, bool) and create:
                element_value = self.create_element(item.value)
                setattr(item.value, self.label, element_value)

            for index, value in enumerate(ensure_list(element_value)):
                if create or value is not None:
                    element = FHIRPathCollectionItem(
                        value,
                        path=Element(self.label),
                        parent=item,
                        setter=partial(
                            self.setter, item=item, index=index, label=self.label
                        ),
                    )
                    element_collection.append(element)
        return element_collection

    def __str__(self):
        return self.label

    def __repr__(self):
        return f"Element({self.label})"

    def __eq__(self, other):
        return isinstance(other, Element) and self.label == other.label

    def __hash__(self):
        return hash(self.label)


class Root(FHIRPath):
    """
    A class representing the root of a FHIRPath, i.e. the top-most segment of the FHIRPath
    whose collection has no parent associated.
    """

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Evaluate the collection of top-most resources in the input collection.

        Args:
            collection (Collection): The collection of items to be evaluated.

        Returns:
            collection (Collection): A list of FHIRPathCollectionItem instances after evaluation.
        """
        return [
            (
                FHIRPathCollectionItem(item.value, parent=None, path=Root())
                if item.parent is None
                else Root().evaluate([item.parent])[0]
            )
            for item in collection
        ]

    def __str__(self):
        return "$"

    def __repr__(self):
        return "Root()"

    def __eq__(self, other):
        return isinstance(other, Root)

    def __hash__(self):
        return hash("$rootResource")


class Parent(FHIRPath):
    """
    A class representing the parent of a FHIRPath
    """

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Evaluate the collection of parent resources in the input collection.

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.

        Returns:
            FHIRPathCollection: The output collection.
        """
        return [item.parent for item in collection if item.parent is not None]

    def __str__(self):
        return "$"

    def __repr__(self):
        return "Parent()"

    def __eq__(self, other):
        return isinstance(other, Parent)

    def __hash__(self):
        return hash("$resource")


class This(FHIRPath):
    """
    A class representation of the FHIRPath `$this` operator used to represent
    the item from the input collection currently under evaluation.
    """

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Simply returns the input collection.

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.

        Returns:
            collection (FHIRPathCollection): A list of FHIRPathCollectionItem instances after evaluation.
        """
        return collection

    def __str__(self):
        return "`this`"

    def __repr__(self):
        return "This()"

    def __eq__(self, other):
        return isinstance(other, This)

    def __hash__(self):
        return hash("this")


class Invocation(FHIRPath):
    """
    A class representing an invocation in the context of FHIRPath evaluation
    indicated by two dot-separated identifiers `<left>.<right>`.

    Attributes:
        left (FHIRPath): The left-hand side FHIRPath segment of the invocation.
        right (FHIRPath): The right-hand side  FHIRPath segment of the invocation.
    """

    def __init__(self, left: FHIRPath, right: FHIRPath):
        self.left = left
        self.right = right

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Performs the evaluation of the Invocation by applying the left-hand side FHIRPath segment on the given collection to obtain a parent collection.
        Then, the right-hand side FHIRPath segment is applied on the parent collection to derive the child collection.

        Args:
            collection (FHIRPathCollection): The collection on which the evaluation is performed.
            create (bool): A boolean flag indicating whether to create any missing elements.

        Returns:
            FHIRPathCollection: The resulting child collection after the evaluation process.
        """
        parent_collection = self.left.evaluate(collection, create)
        return self.right.evaluate(parent_collection, create)

    def __eq__(self, other):
        print(f"Comparing {self} with {other}")
        print(f"A: {self.left}, B: {other.left}", self.left == other.left)
        print(f"A: {self.right}, B: {other.right}", self.right == other.right)
        return (
            isinstance(other, Invocation)
            and self.left == other.left
            and self.right == other.right
        )

    def __str__(self):
        return "%s.%s" % (self.left, self.right)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.left, self.right)

    def __hash__(self):
        return hash((self.left, self.right))
        return hash((self.left, self.right))
