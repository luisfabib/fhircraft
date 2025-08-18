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
from fhircraft.fhir.resources.datatypes.utils import validate_fhir_type


class FHIRTypesOperator(FHIRPath):
    """
    Abstract class definition for the category of types FHIRPath operators.
    """

    def __init__(self, left: FHIRPath | FHIRPathCollection, type_specifier: str):
        self.left = left
        self.type_specifier = type_specifier

    def _get_singleton_collection_value(
        self, collection: FHIRPathCollection, create=False
    ) -> Any:
        left_collection = evaluate_fhirpath_collection(self.left, collection, create)
        if len(left_collection) > 1:
            raise FHIRPathRuntimeError(
                f"FHIRPath operator {self.__str__()} expected a singleton collection for the left expression, instead got a {len(collection)}-items collection."
            )
        return left_collection[0].value

    def _validate_type_specifier(
        self, collection: FHIRPathCollection, create: bool
    ) -> bool:
        """
        Validates the type specifier against the known FHIR types.
        Raises an error if the type specifier is not valid.
        """
        type_ = self.type_specifier
        value = self._get_singleton_collection_value(collection, create)
        print(
            "Validating type specifier:",
            type_,
            "for value:",
            value,
            "of type:",
            type(value),
        )
        # Handle the FHIRPath literal types as special cases
        if isinstance(value, fhirpath_literals.Quantity):
            return type_ == "Quantity"
        elif isinstance(value, fhirpath_literals.Date):
            return type_ == "Date"
        elif isinstance(value, fhirpath_literals.DateTime):
            return type_ == "DateTime"
        elif isinstance(value, fhirpath_literals.Time):
            return type_ == "Time"
        return bool(
            validate_fhir_type(
                value,
                type_,
                raise_on_error=False,
            )
        )

    def __str__(self):
        return f"{self.__class__.__name__.lower()}({self.left.__str__(), self.type_specifier.__str__()})"

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
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        If the left operand is a collection with a single item and the second operand is a type identifier,
        this operator returns true if the type of the left operand is the type specified in the second operand,
        or a subclass thereof. If the input value is not of the type, this operator returns false. If the identifier
        cannot be resolved to a valid type identifier, the evaluator will throw an error. If the input collections
        contains more than one item, the evaluator will throw an error. In all other cases this operator returns the empty collection.

        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        return [
            FHIRPathCollectionItem.wrap(
                self._validate_type_specifier(collection, create)
            )
        ]


class LegacyIs(FHIRPathFunction):
    """
    The is() function is supported for backwards compatibility with previous implementations of FHIRPath.
    Just as with the is keyword, the type argument is an identifier that must resolve to the name of a type
    in a model.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        type_specifier (str): Type specifier.
    """

    def __init__(self, type_specifier: str):
        self.type_specifier = type_specifier

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        return Is(This(), self.type_specifier).evaluate(collection, create)


class As(FHIRTypesOperator):
    """
    A representation of the FHIRPath [`as`](https://hl7.org/fhirpath/N1/#as) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        type_specifier (str): Type specifier.
    """

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        If the left operand is a collection with a single item and the second operand is an identifier,
        this operator returns the value of the left operand if it is of the type specified in the second
        operand, or a subclass thereof. If the identifier cannot be resolved to a valid type identifier,
        the evaluator will throw an error. If there is more than one item in the input collection, the
        evaluator will throw an error. Otherwise, this operator returns the empty collection.

        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        value = self._get_singleton_collection_value(collection, create)
        return (
            [FHIRPathCollectionItem.wrap(value)]
            if self._validate_type_specifier(collection, create)
            else []
        )


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
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        return As(This(), self.type_specifier).evaluate(collection)
