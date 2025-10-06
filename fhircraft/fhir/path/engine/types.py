"""The tree navigation module contains the object representations of the types category FHIRPath operators/functions."""

from typing import Any

import fhircraft.fhir.path.engine.literals as fhirpath_literals
from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathFunction,
    Literal,
    This,
)
from fhircraft.fhir.path.exceptions import FHIRPathRuntimeError
from fhircraft.fhir.path.utils import evaluate_fhirpath_collection
from fhircraft.fhir.resources.datatypes import utils as type_utils


class FHIRTypesOperator(FHIRPath):
    """
    Abstract class definition for the category of types FHIRPath operators.
    """

    def __init__(self, left: FHIRPath | FHIRPathCollection, type_specifier: str):
        self.left = left
        self.type_specifier = type_specifier

    def _get_singleton_collection_value(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> Any:
        left_collection = evaluate_fhirpath_collection(
            self.left, collection, environment, create
        )
        if len(left_collection) > 1:
            raise FHIRPathRuntimeError(
                f"FHIRPath operator {self.__str__()} expected a singleton collection for the left expression, instead got a {len(collection)}-items collection."
            )
        return left_collection[0].value

    def _validate_type_specifier(self, value: Any) -> bool:
        """
        Validates the type specifier against the known FHIR types.
        Raises an error if the type specifier is not valid.
        """
        type_ = self.type_specifier
        # Handle the FHIRPath literal types as special cases
        if isinstance(value, fhirpath_literals.Quantity):
            return type_ == "Quantity"
        elif isinstance(value, fhirpath_literals.Date):
            return type_ == "Date"
        elif isinstance(value, fhirpath_literals.DateTime):
            return type_ == "DateTime"
        elif isinstance(value, fhirpath_literals.Time):
            return type_ == "Time"
        else:
            try:
                return type_utils.is_fhir_primitive_type(value, type_)
            except type_utils.FHIRTypeError:
                try:
                    return type_utils.is_fhir_complex_type(value, type_)
                except type_utils.FHIRTypeError:
                    return type_utils.is_fhir_resource_type(value, type_)

    def __str__(self):
        raise NotImplementedError("Subclasses must implement __str__ method.")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left.__repr__(), self.type_specifier.__repr__()})"

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and other.left == self.left
            and other.type_specifier == self.type_specifier
        )

    def __hash__(self):
        return hash((self.left, self.type_specifier))


class Is(FHIRTypesOperator):
    """
    A representation of the FHIRPath [`is`](https://hl7.org/fhirpath/N1/#is) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        type_specifier (str): Type specifier.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the left operand is a collection with a single item and the second operand is a type identifier,
        this operator returns true if the type of the left operand is the type specified in the second operand,
        or a subclass thereof. If the input value is not of the type, this operator returns false. If the identifier
        cannot be resolved to a valid type identifier, the evaluator will throw an error. If the input collections
        contains more than one item, the evaluator will throw an error. In all other cases this operator returns the empty collection.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        value = self._get_singleton_collection_value(collection, environment, create)
        if value is None:
            return []
        return [FHIRPathCollectionItem.wrap(self._validate_type_specifier(value))]

    def __str__(self):
        return f"{self.left} is {self.type_specifier}"


class LegacyIs(FHIRPathFunction):
    """
    The is() function is supported for backwards compatibility with previous implementations of FHIRPath.
    Just as with the is keyword, the type argument is an identifier that must resolve to the name of a type
    in a model.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        type_specifier (str): Type specifier.
    """

    def __init__(self, type_specifier: str | Literal):
        self.type_specifier = (
            type_specifier if isinstance(type_specifier, str) else type_specifier.value
        )

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        return Is(This(), self.type_specifier).evaluate(collection, environment, create)

    def __str__(self):
        return f"is({self.type_specifier})"


class As(FHIRTypesOperator):
    """
    A representation of the FHIRPath [`as`](https://hl7.org/fhirpath/N1/#as) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        type_specifier (str): Type specifier.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the left operand is a collection with a single item and the second operand is an identifier,
        this operator returns the value of the left operand if it is of the type specified in the second
        operand, or a subclass thereof. If the identifier cannot be resolved to a valid type identifier,
        the evaluator will throw an error. If there is more than one item in the input collection, the
        evaluator will throw an error. Otherwise, this operator returns the empty collection.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        value = self._get_singleton_collection_value(collection, environment, create)
        return (
            [FHIRPathCollectionItem.wrap(value)]
            if self._validate_type_specifier(value)
            else []
        )

    def __str__(self):
        return f"{self.left} as {self.type_specifier}"


class LegacyAs(FHIRPathFunction):
    """
    The as() function is supported for backwards compatibility with previous implementations of FHIRPath.
    Just as with the as keyword, the type argument is an identifier that must resolve to the name of a type
    in a model.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        type_specifier (str): Type specifier.
    """

    def __init__(self, type_specifier: str | Literal):
        self.type_specifier: str = (
            type_specifier.value
            if isinstance(type_specifier, Literal)
            else type_specifier
        )

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        return As(This(), self.type_specifier).evaluate(collection, environment, create)

    def __str__(self):
        return f"as({self.type_specifier})"
