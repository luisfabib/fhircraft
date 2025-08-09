import inspect
import logging
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, List, Optional

from fhircraft.fhir.path.exceptions import FHIRPathError, FHIRPathRuntimeError
from fhircraft.utils import contains_list_type, ensure_list, get_fhir_model_from_field

# Get logger name
logger = logging.getLogger(__name__)

FHIRPathCollection = List["FHIRPathCollectionItem"]


class FHIRPath(ABC):
    """Abstract base class for FHIRPath expressions."""

    def values(self, data) -> List[Any]:
        """
        Evaluates the FHIRPath expression and returns all resulting values as a list.

        Args:
            data: The data to evaluate the FHIRPath expression against.

        Returns:
            List[Any]: A list of all values that match the FHIRPath expression. Returns an empty list if no matches are found.
        """
        collection = self.__evaluate_wrapped(data)
        return [item.value for item in collection]

    def single(self, data, default=None) -> Any:
        """
        Evaluates the FHIRPath expression and returns a single value.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            default: The default value to return if no matches are found.

        Returns:
            Any: The single matching value.

        Raises:
            FHIRPathError: If more than one value is found.
        """
        values = self.values(data)
        if len(values) == 0:
            return default
        elif len(values) == 1:
            return values[0]
        else:
            raise FHIRPathRuntimeError(
                f"Expected single value but found {len(values)} values. "
                f"Use values() to retrieve multiple values or first() to get the first one."
            )

    def first(self, data, default=None) -> Any:
        """
        Evaluates the FHIRPath expression and returns the first value.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            default: The default value to return if no matches are found.

        Returns:
            Any: The first matching value, or the default if no matches.
        """
        values = self.values(data)
        return values[0] if values else default

    def last(self, data, default=None) -> Any:
        """
        Evaluates the FHIRPath expression and returns the last value.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            default: The default value to return if no matches are found.

        Returns:
            Any: The last matching value, or the default if no matches.
        """
        values = self.values(data)
        return values[-1] if values else default

    def exists(self, data) -> bool:
        """
        Checks if the FHIRPath expression matches any values in the data.

        Args:
            data: The data to evaluate the FHIRPath expression against.

        Returns:
            bool: True if at least one value matches, False otherwise.
        """
        return len(self.values(data)) > 0

    def count(self, data) -> int:
        """
        Returns the number of values that match the FHIRPath expression.

        Args:
            data: The data to evaluate the FHIRPath expression against.

        Returns:
            int: The number of matching values.
        """
        return len(self.values(data))

    def is_empty(self, data) -> bool:
        """
        Checks if the FHIRPath expression matches no values in the data.

        Args:
            data: The data to evaluate the FHIRPath expression against.

        Returns:
            bool: True if no values match, False otherwise.
        """
        return not self.exists(data)

    def update_values(self, data, value) -> None:
        """
        Evaluates the FHIRPath expression and sets all matching locations to the given value.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            value: The value to set at all matching locations.

        Raises:
            RuntimeError: If no matching locations are found or if locations cannot be set.
        """
        collection = self.__evaluate_wrapped(data, create=True)
        if not collection:
            raise RuntimeError(
                "No matching locations found. Cannot set value on empty result."
            )
        for item in collection:
            item.set_value(value)

    def update_single(self, data, value) -> None:
        """
        Evaluates the FHIRPath expression and sets a single matching location to the given value.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            value: The value to set at the matching location.

        Raises:
            FHIRPathError: If zero or more than one matching locations are found.
            RuntimeError: If the location cannot be set.
        """
        collection = self.__evaluate_wrapped(data, create=True)
        if len(collection) == 0:
            raise FHIRPathError(
                "No matching locations found. Cannot set value on empty result."
            )
        elif len(collection) > 1:
            raise FHIRPathError(
                f"Expected single location but found {len(collection)} locations. "
                f"Use update_values() to set all locations."
            )
        collection[0].set_value(value)

    def trace(self, data, verbose: bool = False) -> List[str]:
        """
        Returns a trace of evaluation steps for debugging purposes.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            verbose: If True, includes detailed information about each step.

        Returns:
            List[str]: A list of trace messages showing the evaluation steps.
        """
        trace_messages = []

        def trace_step(message: str, level: int = 0):
            indent = "  " * level
            trace_messages.append(f"{indent}{message}")

        try:
            # Start tracing
            trace_step(f"Starting evaluation of: {self}")
            trace_step(f"Input data type: {type(data).__name__}")

            if verbose:
                trace_step(f"Input data: {repr(data)[:100]}...")

            # Wrap data and trace collection creation
            wrapped_data = [
                FHIRPathCollectionItem.wrap(item) for item in ensure_list(data)
            ]
            trace_step(f"Created collection with {len(wrapped_data)} items")

            if verbose:
                for i, item in enumerate(wrapped_data):
                    trace_step(
                        f"  Item {i}: {type(item.value).__name__} = {repr(item.value)[:50]}...",
                        1,
                    )

            # Evaluate and trace results
            result_collection = self.evaluate(wrapped_data, create=False)
            trace_step(f"Evaluation completed: {len(result_collection)} results")

            if verbose:
                for i, item in enumerate(result_collection):
                    trace_step(
                        f"  Result {i}: {type(item.value).__name__} = {repr(item.value)[:50]}...",
                        1,
                    )
                    if item.path:
                        trace_step(f"    Path: {item.path}", 2)
                    if item.parent:
                        trace_step(f"    Parent: {type(item.parent.value).__name__}", 2)

            # Extract values for final result
            values = [item.value for item in result_collection]
            trace_step(f"Final result: {len(values)} values")

        except Exception as e:
            trace_step(f"ERROR during evaluation: {type(e).__name__}: {str(e)}")
            trace_step(f"Expression: {self}")

        return trace_messages

    def debug_info(self, data) -> dict:
        """
        Returns debugging information about the evaluation.

        Args:
            data: The data to evaluate the FHIRPath expression against.

        Returns:
            dict: A dictionary containing debugging information including:
                - expression: String representation of the FHIRPath expression
                - expression_type: Type of the FHIRPath expression
                - input_data_type: Type of the input data
                - input_data_size: Size/length of input data if applicable
                - result_count: Number of results from evaluation
                - result_types: Types of result values
                - evaluation_success: Whether evaluation completed successfully
                - error: Error information if evaluation failed
                - collection_items: Information about FHIRPathCollectionItem objects
        """
        debug_data = {
            "expression": str(self),
            "expression_type": type(self).__name__,
            "expression_repr": repr(self),
            "input_data_type": type(data).__name__,
            "input_data_size": None,
            "result_count": 0,
            "result_types": [],
            "result_values": [],
            "evaluation_success": False,
            "error": None,
            "collection_items": [],
            "trace": [],
        }

        try:
            # Analyze input data
            if hasattr(data, "__len__") and not isinstance(data, str):
                debug_data["input_data_size"] = len(data)

            # Get trace information
            debug_data["trace"] = self.trace(data, verbose=True)

            # Perform evaluation
            wrapped_data = [
                FHIRPathCollectionItem.wrap(item) for item in ensure_list(data)
            ]
            result_collection = self.evaluate(wrapped_data, create=False)

            # Analyze results
            debug_data["result_count"] = len(result_collection)
            debug_data["evaluation_success"] = True

            for item in result_collection:
                debug_data["result_types"].append(type(item.value).__name__)
                debug_data["result_values"].append(repr(item.value)[:100])

                # Collection item details
                item_info = {
                    "value_type": type(item.value).__name__,
                    "value_repr": repr(item.value)[:100],
                    "path": str(item.path) if item.path else None,
                    "path_type": type(item.path).__name__ if item.path else None,
                    "has_parent": item.parent is not None,
                    "has_setter": item.setter is not None,
                    "element": item.element,
                    "index": item.index,
                }
                debug_data["collection_items"].append(item_info)

            # Remove duplicates from result_types
            debug_data["result_types"] = list(set(debug_data["result_types"]))

        except Exception as e:
            debug_data["evaluation_success"] = False
            debug_data["error"] = {
                "type": type(e).__name__,
                "message": str(e),
                "expression": str(self),
            }

            # Still try to get trace even if evaluation failed
            try:
                debug_data["trace"] = self.trace(data, verbose=True)
            except:
                debug_data["trace"] = [
                    f"Failed to generate trace for expression: {self}"
                ]

        return debug_data

    @abstractmethod
    def evaluate(
        self, collection: FHIRPathCollection, create: bool
    ) -> FHIRPathCollection:
        """
        Evaluates the current object against the provided FHIRPathCollection.

        Args:
            collection (FHIRPathCollection): The collection of FHIRPath elements to evaluate.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The result of the evaluation as a FHIRPathCollection.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError()

    def __init_subclass__(cls, **kwargs):
        """
        Called when a class is subclassed. Ensures that any non-abstract subclass of `FHIRPath`
        overrides the `evaluate` method. Raises a TypeError if the subclass does not provide its own
        implementation of `evaluate`.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.

        Raises:
            TypeError: If a non-abstract subclass does not override the `evaluate` method.
        """
        if not inspect.isabstract(cls) and cls.evaluate == FHIRPath.evaluate:
            raise TypeError(
                "Subclasses of `FHIRPath` must override the `evaluate` method"
            )
        super().__init_subclass__(**kwargs)

    def __evaluate_wrapped(self, data: typing.Any, create=False) -> FHIRPathCollection:
        # Ensure that entrypoint is a list of FHIRPathCollectionItem instances
        collection = [FHIRPathCollectionItem.wrap(item) for item in ensure_list(data)]
        return self.evaluate(collection, create=create)

    def __get_child(self, child):
        """
        Determines and returns the appropriate child node in a path expression tree.

        Args:
            child: The child node to be evaluated, which can be an instance of This, Root, or another node type.

        Returns:
            The resulting node based on the following logic:
                - If the current node is an instance of This or Root, returns the child node.
                - If the child node is an instance of This, returns the current node.
                - If the child node is an instance of Root, returns the child node.
                - Otherwise, returns a new Invocation node combining the current node and the child.

        Note:
            This method is used internally to manage navigation and invocation logic within the path engine.
        """
        if isinstance(self, This) or isinstance(self, Root):
            return child
        elif isinstance(child, This):
            return self
        elif isinstance(child, Root):
            return child
        else:
            return Invocation(self, child)


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
            self.path
            if self.parent is None
            else self.parent.full_path.__get_child(self.path)
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


class FHIRPathFunction(FHIRPath, ABC):
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
