import datetime
import inspect
import logging
import warnings
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List

from fhircraft.exceptions import (
    FHIRPathException,
    FHIRPathWarning,
)
from fhircraft import SUPPORTED_FHIR_RELEASES
from fhircraft.exceptions import FHIRPathRuntimeError
from fhircraft.utils import ensure_list
from fhircraft.fhir.path.accessors import RootAccessor
from fhircraft.fhir.path.collection import FHIRPathCollection, FHIRPathCollectionItem

if TYPE_CHECKING:
    from fhircraft.fhir.resources.base import FHIRPrimitiveModel

# Get logger name
logger = logging.getLogger(__name__)


__all__ = [
    "FHIRPathNode",
    "FHIRPathCollection",
    "FHIRPathCollectionItem",
    "FHIRPathFunction",
    "Element",
    "This",
    "Literal",
    "Invocation",
    "RootElement",
    "TypeSpecifier",
]


def _targets_of(collection: Any) -> tuple:
    """Writable targets of any collection-like (plain lists derive them from their items)."""
    targets = getattr(collection, "targets", None)
    if targets is not None:
        return targets
    return tuple(i.accessor for i in collection if i.accessor is not None)


class FHIRPathNode(ABC):
    """Abstract base class for one node of a parsed FHIRPath expression tree.

    A node represents a single grammar production -- an element access, an
    invocation, a literal, a function call -- and `evaluate()` transforms an
    input collection into an output collection.
    """

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
                wrapped_data, environment=environment or dict()
            )
            trace_step(f"Evaluation completed: {len(result_collection)} results")

            if verbose:
                for i, item in enumerate(result_collection):
                    trace_step(
                        f"  Result {i}: {type(item.value).__name__} = {repr(item.value)[:50]}...",
                        1,
                    )
                    if item.canonical_path:
                        trace_step(f"    Canonical Path: {item.canonical_path}", 2)
                    if item.accessor is not None and item.accessor.parent is not None:
                        trace_step(
                            f"    Parent Canonical Path: {item.accessor.parent.canonical_path}",
                            2,
                        )

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
            result_collection = self.__evaluate_wrapped(data)

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
                    "canonical_path": (
                        str(item.canonical_path) if item.canonical_path else None
                    ),
                    "has_parent": item.accessor is not None
                    and item.accessor.parent is not None,
                    "is_writable": item.accessor is not None,
                    "element": item.accessor.element if item.accessor else None,
                    "index": item.accessor.index if item.accessor else None,
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
            except Exception:
                debug_data["trace"] = [
                    f"Failed to generate trace for expression: {self}"
                ]

        return debug_data

    @abstractmethod
    def evaluate(
        self,
        collection: FHIRPathCollection,
        environment: dict,
    ) -> FHIRPathCollection:
        """
        Evaluates the current object against the provided FHIRPathCollection.

        Args:
            collection (FHIRPathCollection): The collection of FHIRPath elements to evaluate.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection: The result of the evaluation as a FHIRPathCollection.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError()

    def single(
        self, data: Any, default: Any = None, environment: dict | None = None
    ) -> Any:
        """
        Evaluates the FHIRPath expression and returns a single value.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            default: The default value to return if no matches are found.
            environment: Optional map of additional variables to include in the evaluation context.

        Returns:
            Any: The single matching value.

        Raises:
            FHIRPathException: If more than one value is found.
        """

        collection = self._evaluate_wrapped(data, environment=environment)
        values = [item.value for item in collection]

        if len(values) == 0:
            return default
        elif len(values) == 1:
            return values[0]
        else:
            raise FHIRPathRuntimeError(
                f"Expected single value but found {len(values)} values. "
                f"Use values() to retrieve multiple values or first() to get the first one."
            )

    def count(self, data: Any, environment: dict | None = None) -> int:
        """
        Returns the number of values that match the FHIRPath expression.

        Args:
            data: The data to evaluate the FHIRPath expression against.
            environment: Optional map of additional variables to include in the evaluation context.

        Returns:
            int: The number of matching values.
        """
        return len(self._evaluate_wrapped(data, environment=environment))

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
        if not inspect.isabstract(cls) and cls.evaluate == FHIRPathNode.evaluate:
            raise TypeError(
                "Subclasses of `FHIRPath` must override the `evaluate` method"
            )
        super().__init_subclass__(**kwargs)

    def _evaluate_wrapped(
        self, data: Any, environment: dict | None = None
    ) -> FHIRPathCollection:
        # Determine %resource and %rootResource from parent tracking if available
        resource = data
        root_resource = data
        fhir_release = getattr(data, "_fhir_release", None)

        # Check if data has parent tracking attributes (from FHIRBaseModel)
        if hasattr(data, "_resource") and hasattr(data, "_root_resource"):
            res = getattr(data, "_resource", None)
            root = getattr(data, "_root_resource", None)

            # %resource: the immediate parent resource (not just any parent, but a resource type)
            # If _resource is None, fallback to data itself
            if res is not None:
                resource = res

            # %rootResource: the top-level resource
            if root is not None:
                root_resource = root

        environment = {
            "%ucum": FHIRPathCollectionItem.wrap("http://unitsofmeasure.org"),
            "%context": FHIRPathCollectionItem.wrap(data),
            "%resource": FHIRPathCollectionItem.wrap(resource),
            "%rootResource": FHIRPathCollectionItem.wrap(root_resource),
            "%fhirRelease": FHIRPathCollectionItem.wrap(fhir_release),
        } | (environment or dict())
        # Ensure that entrypoint is a list of FHIRPathCollectionItem instances
        collection = FHIRPathCollection(
            FHIRPathCollectionItem.wrap(item) for item in ensure_list(data)
        )
        result = self.evaluate(collection, environment or dict())
        return result if isinstance(result, FHIRPathCollection) else FHIRPathCollection(result)

    def _invoke(self, invocation: "FHIRPathNode") -> "FHIRPathNode":
        """
        Invoke the FHIRPath expression on the given collection.

        Args:
            invocation (FHIRPathNode): The FHIRPath expression to invoke.

        Returns:
            Invocation[Self, FHIRPathNode]: The resulting invocation after processing.
        """
        return Invocation(self, invocation)

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"


class FHIRPathFunction(FHIRPathNode, ABC):
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


class Literal(FHIRPathNode):
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
    ) -> FHIRPathCollection:
        """
        Simply returns the input collection.

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.

        Returns:
            collection (FHIRPathCollection): A list of FHIRPathCollectionItem instances after evaluation.
        """
        return [FHIRPathCollectionItem(self.value)]

    def __str__(self):
        from fhircraft.fhir.resources.base import FHIRPrimitiveModel

        _value = (
            self.value.value
            if isinstance(self.value, FHIRPrimitiveModel)
            else self.value
        )

        if isinstance(_value, bool):
            return "true" if _value else "false"
        elif isinstance(_value, str):
            return f"'{_value}'"
        elif isinstance(_value, (datetime.date, datetime.datetime, datetime.time)):
            return f"@{_value}"
        else:
            return str(_value)

    def __repr__(self):
        return "Literal(%r)" % (self.value,)

    def __eq__(self, other):
        return isinstance(other, Literal) and self.value == other.value

    def __hash__(self):
        return hash(("literal", self.value))


class Element(FHIRPathNode):
    """
    A class representing an element in a FHIRPath, used for navigating and manipulating FHIR resources.

    Attributes:
        name (str): The name of the element.
    """

    def __init__(self, name: "str | Literal | FHIRPrimitiveModel"):
        if isinstance(name, Literal) or getattr(name, "_type", None) == "string":
            name = str(name)
        if not isinstance(name, str):
            raise FHIRPathException(
                "Element() argument must be a string, got %r" % (type(name).__name__,)
            )
        self.name = name

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """Navigate to the child element named `self.name` of every input item.

        The accessors of the addressed element are retained in the result's
        `targets` even when the element is absent, so the location stays
        writable.
        """
        parents = [
            item.accessor or RootAccessor(item.value)
            for item in collection
            if item.value is not None
        ]
        if not parents:
            parents = [t for t in _targets_of(collection)]
        items: list[FHIRPathCollectionItem] = []
        targets: list = []
        for parent in parents:
            accessor = parent.child(self.name)
            if accessor is None:
                continue
            targets.append(accessor)
            value = accessor.get()
            if isinstance(value, list):
                items.extend(
                    FHIRPathCollectionItem(child, accessor.at(index))
                    for index, child in enumerate(value)
                    if child is not None
                )
            elif value is not None:
                items.append(FHIRPathCollectionItem(value, accessor))
        return FHIRPathCollection(items, targets=targets)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Element({self.name})"

    def __eq__(self, other):
        return isinstance(other, Element) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Invocation(FHIRPathNode):
    """
    A class representing an invocation in the context of FHIRPath evaluation
    indicated by two dot-separated identifiers `<left>.<right>`.

    Attributes:
        left (FHIRPathNode): The left-hand side FHIRPath segment of the invocation.
        right (FHIRPathNode): The right-hand side  FHIRPath segment of the invocation.
    """

    def __init__(self, left: FHIRPathNode, right: FHIRPathNode):
        self.left = left
        self.right = right

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Performs the evaluation of the Invocation by applying the left-hand side FHIRPath segment on the given collection to obtain a parent collection.
        Then, the right-hand side FHIRPath segment is applied on the parent collection to derive the child collection.

        Args:
            collection (FHIRPathCollection): The collection on which the evaluation is performed.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection: The resulting child collection after the evaluation process.
        """
        parent_collection = self.left.evaluate(collection, environment)
        return self.right.evaluate(parent_collection, environment)

    def __eq__(self, other):
        return (
            isinstance(other, Invocation)
            and self.left == other.left
            and self.right == other.right
        )

    def __str__(self):
        from fhircraft.fhir.path.engine.subsetting import Index

        if isinstance(self.right, Index):
            return "%s%s" % (self.left, self.right)
        return "%s.%s" % (self.left, self.right)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.left, self.right)

    def __hash__(self):
        return hash((self.left, self.right))


class This(FHIRPathNode):
    """
    A representation of a current element. Used for internal purposes and has no FHIRPath shorthand notation.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Simply returns the input collection.

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.

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


class RootElement(FHIRPathNode):
    """
    A class representing the root of a FHIRPath, i.e. the top-most segment of the FHIRPath
    whose collection has no parent associated.

    Attributes:
        type (str): The expected FHIR resource type of the root element, by default.
    """

    def __init__(self, type: str = "Resource"):
        self.type = type

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Evaluate the input collection to assert that the entries are valid FHIR resources of the given type.

        Args:
            collection (Collection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.

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
                and (not hasattr(resource, "_type") or not resource._type == self.type)
            ):
                raise FHIRPathException(
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


class TypeSpecifier(FHIRPathNode):
    """
    A type specifier is an identifier that must resolve to the name of a type in a model.
    Type specifiers can have qualifiers, e.g. FHIR.Patient, where the qualifier is the name of the model.

    Attributes:
        specifier (str): The type specifier string.
        namespace (Optional[str]): The namespace of the type specifier, by default "FHIR".
    """

    def __init__(self, specifier: str):
        if "." in specifier:
            namespace, specifier = specifier.split(".", 1)
        else:
            namespace = None
        self.specifier: str = specifier
        self.namespace: str | None = namespace

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Evaluate the input collection to assert that the entries are valid FHIR resources of the given type.
        The type is resolved based on the namespace and specifier using the FHIR release specified in the environment
        variable `%fhirRelease`. If the variable is not present, it defaults to "R4" and will warn on usage.

        Args:
            collection (Collection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.

        Returns:
            collection (Collection): The same collection after validation.
        """
        from fhircraft.fhir.resources.datatypes.utils import get_fhir_type

        namespace = self.namespace or "FHIR"
        if namespace == "FHIR":
            self.specifier = self.specifier[0].upper() + self.specifier[1:]
            release = environment.get("%fhirRelease")
            if release:
                release = (
                    release.value
                    if isinstance(release, FHIRPathCollectionItem)
                    else release
                )
            if release not in SUPPORTED_FHIR_RELEASES:
                warnings.warn(
                    f"Unsupported %fhirRelease '{release}' found in environment. Defaulting to R4 for type resolution.",
                    FHIRPathWarning,
                    stacklevel=2,
                )
                release = "R4"
            if not release:
                warnings.warn(
                    "No %fhirRelease found in environment. Defaulting to R4 for type resolution.",
                    FHIRPathWarning,
                    stacklevel=2,
                )
                release = "R4"
            resolved_type = get_fhir_type(self.specifier, release)
        elif namespace == "System":
            from fhircraft.fhir.path.engine.literals import (
                Date,
                DateTime,
                Quantity,
                Time,
            )

            match self.specifier:
                case "String":
                    resolved_type = str
                case "Boolean":
                    resolved_type = bool
                case "Integer":
                    resolved_type = int
                case "Long":
                    resolved_type = int
                case "Decimal":
                    resolved_type = float
                case "Date":
                    resolved_type = Date
                case "DateTime":
                    resolved_type = DateTime
                case "Time":
                    resolved_type = Time
                case "Quantity":
                    resolved_type = Quantity
                case _:
                    raise NameError(
                        f"Unknown type specifier '{self.specifier}' in System namespace"
                    )
        else:
            raise NameError(
                f"Unknown namespace '{self.namespace}' for type specifier '{self.specifier}'"
            )
        return [FHIRPathCollectionItem(value=resolved_type)]

    def __str__(self):
        return (
            self.namespace + "." + self.specifier if self.namespace else self.specifier
        )

    def __repr__(self):
        return (
            f'TypeSpecifier("{self.namespace}.{self.specifier}")'
            if self.namespace
            else f'TypeSpecifier("{self.specifier}")'
        )

    def __eq__(self, other):
        return (
            isinstance(other, TypeSpecifier)
            and self.namespace == other.namespace
            and self.specifier == other.specifier
        )

    def __hash__(self):
        return hash((self.namespace, self.specifier))
