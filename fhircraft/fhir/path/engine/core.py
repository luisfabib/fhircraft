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

    def values(self, data: Any, environment: dict | None = None) -> List[Any]:
        """
        Evaluates the FHIRPath expression and returns all resulting values as a list.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            environment: Optional map of additional variables to include in the evaluation context.

        Returns:
            List[Any]: A list of all values that match the FHIRPath expression. Returns an empty list if no matches are found.
        """
        collection = self.__evaluate_wrapped(data, environment=environment)
        return [item.value for item in collection]

    def single(self, data: Any, default: Any = None, environment: dict | None = None) -> Any:
        """
        Evaluates the FHIRPath expression and returns a single value.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            default: The default value to return if no matches are found.
            environment: Optional map of additional variables to include in the evaluation context.

        Returns:
            Any: The single matching value.

        Raises:
            FHIRPathError: If more than one value is found.
        """
        values = self.values(data, environment=environment)
        if len(values) == 0:
            return default
        elif len(values) == 1:
            return values[0]
        else:
            raise FHIRPathRuntimeError(
                f"Expected single value but found {len(values)} values. "
                f"Use values() to retrieve multiple values or first() to get the first one."
            )

    def first(self, data: Any, default: Any = None, environment: dict | None = None) -> Any:
        """
        Evaluates the FHIRPath expression and returns the first value.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            default: The default value to return if no matches are found.
            environment: Optional map of additional variables to include in the evaluation context.

        Returns:
            Any: The first matching value, or the default if no matches.
        """
        values = self.values(data, environment=environment)
        return values[0] if values else default

    def last(self, data: Any, default: Any = None, environment: dict | None = None) -> Any:
        """
        Evaluates the FHIRPath expression and returns the last value.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            default: The default value to return if no matches are found.
            environment: Optional map of additional variables to include in the evaluation context.

        Returns:
            Any: The last matching value, or the default if no matches.
        """
        values = self.values(data, environment=environment)
        return values[-1] if values else default

    def exists(self, data: Any, environment: dict | None = None) -> bool:
        """
        Checks if the FHIRPath expression matches any values in the data.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            environment: Optional map of additional variables to include in the evaluation context.

        Returns:
            bool: True if at least one value matches, False otherwise.
        """
        return len(self.values(data, environment=environment)) > 0

    def count(self, data: Any, environment: dict | None = None) -> int:
        """
        Returns the number of values that match the FHIRPath expression.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            environment: Optional map of additional variables to include in the evaluation context.

        Returns:
            int: The number of matching values.
        """
        return len(self.values(data, environment=environment))

    def is_empty(self, data: Any, environment: dict | None = None) -> bool:
        """
        Checks if the FHIRPath expression matches no values in the data.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            environment: Optional map of additional variables to include in the evaluation context.

        Returns:
            bool: True if no values match, False otherwise.
        """
        return not self.exists(data, environment=environment)

    def update_values(self, data: Any, value: Any, environment: dict | None = None) -> None:
        """
        Evaluates the FHIRPath expression and sets all matching locations to the given value.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            value: The value to set at all matching locations.
            environment: Optional map of additional variables to include in the evaluation context.

        Raises:
            RuntimeError: If no matching locations are found or if locations cannot be set.
        """
        collection = self.__evaluate_wrapped(data, environment=environment, create=True)
        if not collection:
            raise RuntimeError(
                "No matching locations found. Cannot set value on empty result."
            )
        for item in collection:
            item.set_value(value)

    def update_single(self, data: Any, value: Any, environment: dict | None = None) -> None:
        """
        Evaluates the FHIRPath expression and sets a single matching location to the given value.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            value: The value to set at the matching location.

        Raises:
            FHIRPathError: If zero or more than one matching locations are found.
            RuntimeError: If the location cannot be set.
        """
        collection = self.__evaluate_wrapped(data, environment=environment, create=True)
        if len(collection) == 0:
            raise FHIRPathError(
                "FHIRPath yielded empty collection. Cannot set value on empty result."
            )
        elif len(collection) > 1:
            raise FHIRPathError(
                f"Expected single location but found {len(collection)} locations. "
                f"Use update_values() to set all locations."
            )
        collection[0].set_value(value)

    def trace(
        self, data: Any, verbose: bool = False, environment: dict | None = None
    ) -> List[str]:
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
            result_collection = self.evaluate(
                wrapped_data, environment=environment or dict(), create=False
            )
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

    def debug_info(self, data: Any) -> dict:
        """
        Returns debugging information about the evaluation.

        Args:
            data: The data to evaluate the FHIRPath expression against.

        Returns:
            (dict): A dictionary containing debugging information including:
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
            result_collection = self.__evaluate_wrapped(data, create=False)

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
        self,
        collection: FHIRPathCollection,
        environment: dict,
        create: bool,
    ) -> FHIRPathCollection:
        """
        Evaluates the current object against the provided FHIRPathCollection.

        Args:
            collection (FHIRPathCollection): The collection of FHIRPath elements to evaluate.
            environment (dict): The environment context for the evaluation.
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
            **kwargs (Dict): Arbitrary keyword arguments passed to the superclass.

        Raises:
            TypeError: If a non-abstract subclass does not override the `evaluate` method.
        """
        if not inspect.isabstract(cls) and cls.evaluate == FHIRPath.evaluate:
            raise TypeError(
                "Subclasses of `FHIRPath` must override the `evaluate` method"
            )
        super().__init_subclass__(**kwargs)

    def __evaluate_wrapped(
        self, data: Any, environment: dict | None = None, create=False
    ) -> FHIRPathCollection:
        environment = (environment or dict()) | {
            "%ucum": FHIRPathCollectionItem.wrap("http://unitsofmeasure.org"),
            "%context": FHIRPathCollectionItem.wrap(data),
            # TODO: Add support for %resource and %rootResource when evaluating within a contained resource context
            "%resource": FHIRPathCollectionItem.wrap(data),
            "%rootResource": FHIRPathCollectionItem.wrap(data),
        }
        # Ensure that entrypoint is a list of FHIRPathCollectionItem instances
        collection = [FHIRPathCollectionItem.wrap(item) for item in ensure_list(data)]
        return self.evaluate(collection, environment or dict(), create)

    def _invoke(self, invocation: "FHIRPath") -> "FHIRPath":
        """
        Invoke the FHIRPath expression on the given collection.

        Args:
            invocation (FHIRPath): The FHIRPath expression to invoke.

        Returns:
            Invocation[Self, FHIRPath]: The resulting invocation after processing.
        """
        return Invocation(self, invocation)

    def __get_child(self, child):
        """
        Determines and returns the appropriate child node in a path expression tree.

        Args:
            child (FHIRPath): The child node to be evaluated, which can be an instance of This, Root, or another node type.

        Returns:
            (FHIRPath) The resulting node

        Note:
            This method is used internally to manage navigation and invocation logic within the path engine.
        """
        if isinstance(self, This):
            return child
        elif isinstance(child, This):
            return self
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
    path: typing.Any = None
    element: Optional[str] = None
    index: Optional[int] = None
    parent: Optional["FHIRPathCollectionItem"] = None
    setter: Optional[Callable] = None

    def __psot_init__(self):
        self.path = self.path or This()

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
        return f"{{{self.value.__repr__()[:10]}}}"

    def __hash__(self):
        return hash((self.path, self.parent, self.value.__repr__()))


class FHIRPathFunction(FHIRPath, ABC):
    """
    Abstract base class representing a FHIRPath function, used for functional evaluation of collections.
    """

    def __arguments__(self):
        return [
            getattr(self, key)
            for key in inspect.signature(self.__init__).parameters
            if key != "self" and hasattr(self, key)
        ]

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.__arguments__() == other.__arguments__()
        )

    def __str__(self):
        return f"{self.__class__.__name__[0].lower() + self.__class__.__name__[1:]}({', '.join([str(arg) for arg in self.__arguments__() if arg is not None])})"

    def __repr__(self):
        return f"{self.__class__.__name__}({','.join([repr(arg) for arg in self.__arguments__()])})"


class Literal(FHIRPath):
    """
    A class representation of a constant literal value in the FHIRPath.

    Attributes:
        value (Any): The literal value to be represented.
    """

    def __init__(self, value: Any):
        self.value = value

    def evaluate(
        self,
        collection: FHIRPathCollection,
        environment: dict,
        create: bool = False,
    ) -> FHIRPathCollection:
        """
        Simply returns the input collection.

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): A list of FHIRPathCollectionItem instances after evaluation.
        """
        return [FHIRPathCollectionItem(self.value, parent=None, path=None)]

    def __str__(self):
        from fhircraft.fhir.resources.datatypes.utils import (
            is_date,
            is_datetime,
            is_time,
        )

        if isinstance(self.value, bool):
            return "true" if self.value else "false"
        elif is_date(self.value) or is_datetime(self.value) or is_time(self.value):
            return self.value
        elif isinstance(self.value, str):
            return f"'{self.value}'"
        else:
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
        value: typing.Any,
        item: FHIRPathCollectionItem,
        index: int,
        label: str,
        is_list_type: bool,
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
        current_values = getattr(parent, label)
        if not isinstance(current_values, list):
            if not is_list_type and isinstance(value, list):
                if value and len(value) > 1:
                    raise ValueError(
                        f"Cannot set multiple values to non-list field '{label}'"
                    )
                value = value[0] if value else None
            setattr(parent, label, value)
        else:
            if is_list_type and isinstance(value, list):
                setattr(parent, label, value)
            elif len(current_values) <= index:
                current_values.insert(index, value)
            else:
                current_values[index] = value

    def _get_collection_by_label(
        self, collection: FHIRPathCollection, label: str, create: bool
    ) -> FHIRPathCollection:
        element_collection = []
        for item in collection:
            if item.value is None:
                continue
            if isinstance(item.value, dict):
                element_value = item.value.get(label, None)
            else:
                element_value = getattr(item.value, label, None)
            if not element_value and not isinstance(element_value, bool) and create:
                element_value = self.create_element(item.value)
                if isinstance(item.value, dict):
                    item.value[label] = element_value
                else:
                    setattr(item.value, label, element_value)

            for index, value in enumerate(ensure_list(element_value)):
                if create or value is not None:
                    element = FHIRPathCollectionItem(
                        value,
                        path=Element(label),
                        parent=item,
                    )
                    element.setter = partial(
                        self.setter,
                        item=item,
                        index=index,
                        label=label,
                        is_list_type=element.is_list_type,
                    )
                    element_collection.append(element)
        return element_collection

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        return self._get_collection_by_label(
            collection, self.label, create
        ) or self._get_collection_by_label(collection, f"{self.label}_ext", create)

    def __str__(self):
        return self.label

    def __repr__(self):
        return f"Element({self.label})"

    def __eq__(self, other):
        return isinstance(other, Element) and self.label == other.label

    def __hash__(self):
        return hash(self.label)


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
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Performs the evaluation of the Invocation by applying the left-hand side FHIRPath segment on the given collection to obtain a parent collection.
        Then, the right-hand side FHIRPath segment is applied on the parent collection to derive the child collection.

        Args:
            collection (FHIRPathCollection): The collection on which the evaluation is performed.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The resulting child collection after the evaluation process.
        """
        parent_collection = self.left.evaluate(collection, environment, create)
        return self.right.evaluate(parent_collection, environment, create)

    def __eq__(self, other):
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


class This(FHIRPath):
    """
    A representation of a current element. Used for internal purposes and has no FHIRPath shorthand notation.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Simply returns the input collection.

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): The output collection.
        """
        return environment.get("this", collection)

    def __str__(self):
        return ""

    def __repr__(self):
        return "This()"

    def __eq__(self, other):
        return isinstance(other, This)

    def __hash__(self):
        return hash("")


class RootElement(FHIRPath):
    """
    A class representing the root of a FHIRPath, i.e. the top-most segment of the FHIRPath
    whose collection has no parent associated.

    Attributes:
        type (str): The expected FHIR resource type of the root element, by default.
    """

    def __init__(self, type: str = "Resource"):
        self.type = type

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Evaluate the input collection to assert that the entries are valid FHIR resources of the given type.

        Args:
            collection (Collection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (Collection): The same collection after validation.
        """
        for item in collection:
            resource = item.value
            # Check if resource is of valid type
            if (
                isinstance(resource, dict)
                and (
                    "resourceType" not in resource
                    or not resource["resourceType"] == self.type
                )
            ) or (
                not isinstance(resource, dict)
                and (
                    not hasattr(resource, "resourceType")
                    or not resource.resourceType == self.type
                )
            ):
                raise FHIRPathError(
                    f"Root element must be a valid FHIR resource of type {self.type}."
                )
        return collection

    def __str__(self):
        return self.type

    def __repr__(self):
        return f'RootElement("{self.type}")'

    def __eq__(self, other):
        return isinstance(other, RootElement) and self.type == other.type

    def __hash__(self):
        return hash(self.type)
