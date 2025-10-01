"""The comparison module contains the object representations of the comparison FHIRPath operators."""

from abc import ABC

from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
)
from fhircraft.fhir.path.utils import evaluate_and_prepare_collection_values


class FHIRComparisonOperator(FHIRPath, ABC):
    """
    Abstract class definition for the category of comparison FHIRPath operators.
    """

    def __init__(
        self, left: FHIRPath | FHIRPathCollection, right: FHIRPath | FHIRPathCollection
    ):
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.__class__.__name__.lower()}({self.left.__str__(), self.right})"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))


class GreaterThan(FHIRComparisonOperator):
    """
    A representation of the FHIRPath [`>`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        The greater than operator (>) returns true if the first operand is strictly greater than the second.
        The operands must be of the same type, or convertible to the same type using an implicit conversion.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        left_value, right_value = evaluate_and_prepare_collection_values(
            self, self.left, self.right, collection, environment, create
        )
        if not left_value or not right_value:
            return []
        return [FHIRPathCollectionItem.wrap(left_value > right_value)]

    def __str__(self):
        return f"{self.left} > {self.right}"


class LessThan(FHIRComparisonOperator):
    """
    A representation of the FHIRPath [`<`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def __init__(
        self, left: FHIRPath | FHIRPathCollection, right: FHIRPath | FHIRPathCollection
    ):
        self.left = left
        self.right = right

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        The less than operator (<) returns true if the first operand is strictly less than the second.
        The operands must be of the same type, or convertible to the same type using implicit conversion.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        left_value, right_value = evaluate_and_prepare_collection_values(
            self, self.left, self.right, collection, environment, create
        )
        if not left_value or not right_value:
            return []
        return [FHIRPathCollectionItem.wrap(left_value < right_value)]

    def __str__(self):
        return f"{self.left} < {self.right}"


class LessEqualThan(FHIRComparisonOperator):
    """
    A representation of the FHIRPath [`<=`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def __init__(
        self, left: FHIRPath | FHIRPathCollection, right: FHIRPath | FHIRPathCollection
    ):
        self.left = left
        self.right = right

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        The less or equal operator (<=) returns true if the first operand is less than or equal to the second.
        The operands must be of the same type, or convertible to the same type using implicit conversion.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        left_value, right_value = evaluate_and_prepare_collection_values(
            self, self.left, self.right, collection, environment, create
        )
        if not left_value or not right_value:
            return []
        return [FHIRPathCollectionItem.wrap(left_value <= right_value)]

    def __str__(self):
        return f"{self.left} <= {self.right}"


class GreaterEqualThan(FHIRComparisonOperator):
    """
    A representation of the FHIRPath [`>=`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def __init__(
        self, left: FHIRPath | FHIRPathCollection, right: FHIRPath | FHIRPathCollection
    ):
        self.left = left
        self.right = right

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        The greater or equal operator (>=) returns true if the first operand is greater than or equal to the second.
        The operands must be of the same type, or convertible to the same type using implicit conversion.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        left_value, right_value = evaluate_and_prepare_collection_values(
            self, self.left, self.right, collection, environment, create
        )
        if not left_value or not right_value:
            return []
        return [FHIRPathCollectionItem.wrap(left_value >= right_value)]

    def __str__(self):
        return f"{self.left} >= {self.right}"
