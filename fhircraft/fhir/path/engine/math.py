"""The tree navigation module contains the object representations of the math category FHIRPath operators/functions."""

from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
)
from fhircraft.fhir.path.engine.literals import Quantity
from fhircraft.fhir.path.exceptions import FHIRPathRuntimeError
from fhircraft.fhir.path.utils import evaluate_and_prepare_collection_values


class FHIRMathOperator(FHIRPath):
    """
    Abstract class definition for the category of math FHIRPath operators.
    """

    def __init__(
        self, left: FHIRPath | FHIRPathCollection, right: FHIRPath | FHIRPathCollection
    ):
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})"

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


class Addition(FHIRMathOperator):
    """
    A representation of the FHIRPath [`+`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        For Integer, Decimal, and quantity, adds the operands. For strings, concatenates the right
        operand to the left operand.
        When adding quantities, the units of each quantity must be the same.


        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        left_value, right_value = evaluate_and_prepare_collection_values(
            self, self.left, self.right, collection, create
        )
        if left_value is None or right_value is None:
            return []
        elif isinstance(left_value, str) and isinstance(right_value, str):
            return [FHIRPathCollectionItem.wrap(left_value + right_value)]
        elif isinstance(left_value, (int, float)) and isinstance(
            right_value, (int, float)
        ):
            return [FHIRPathCollectionItem.wrap(left_value + right_value)]
        elif isinstance(left_value, (Quantity)) and isinstance(right_value, (Quantity)):
            if left_value.unit != right_value.unit:
                raise FHIRPathRuntimeError(
                    f"FHIRPath operator {self.__str__()} cannot add quantities with different units: {left_value.unit} and {right_value.unit}."
                )
            return [FHIRPathCollectionItem.wrap(left_value + right_value)]
        else:
            raise FHIRPathRuntimeError(
                f"FHIRPath operator {self.__str__()} cannot add {type(left_value).__name__} and {type(right_value).__name__}."
            )


class Subtraction(FHIRMathOperator):
    """
    A representation of the FHIRPath [`-`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Subtracts the right operand from the left operand (supported for Integer, Decimal, and Quantity).
        When subtracting quantities, the units of each quantity must be the same.

        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        left_value, right_value = evaluate_and_prepare_collection_values(
            self, self.left, self.right, collection, create
        )
        if left_value is None or right_value is None:
            return []
        elif isinstance(left_value, (int, float)) and isinstance(
            right_value, (int, float)
        ):
            return [FHIRPathCollectionItem.wrap(left_value - right_value)]
        elif isinstance(left_value, (Quantity)) and isinstance(right_value, (Quantity)):
            if left_value.unit != right_value.unit:
                raise FHIRPathRuntimeError(
                    f"FHIRPath operator {self.__str__()} cannot subtract quantities with different units: {left_value.unit} and {right_value.unit}."
                )
            return [FHIRPathCollectionItem.wrap(left_value - right_value)]
        else:
            raise FHIRPathRuntimeError(
                f"FHIRPath operator {self.__str__()} cannot subtract {type(left_value).__name__} and {type(right_value).__name__}."
            )


class Multiplication(FHIRMathOperator):
    """
    A representation of the FHIRPath [`*`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Multiplies both arguments (supported for Integer, Decimal, and Quantity). For multiplication
        involving quantities, the resulting quantity will have the appropriate unit.


        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """

        left_value, right_value = evaluate_and_prepare_collection_values(
            self, self.left, self.right, collection, create
        )
        if left_value is None or right_value is None:
            return []
        elif isinstance(left_value, (int, float)) and isinstance(
            right_value, (int, float)
        ):
            return [FHIRPathCollectionItem.wrap(left_value * right_value)]
        elif isinstance(left_value, (Quantity)) and isinstance(right_value, (Quantity)):
            return [FHIRPathCollectionItem.wrap(left_value * right_value)]
        else:
            raise FHIRPathRuntimeError(
                f"FHIRPath operator {self.__str__()} cannot multiply {type(left_value).__name__} and {type(right_value).__name__}."
            )


class Division(FHIRMathOperator):
    """
    A representation of the FHIRPath [`/`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Divides the left operand by the right operand (supported for Integer, Decimal, and Quantity).
        The result of a division is always Decimal, even if the inputs are both Integer. For integer division,
        use the `div` operator.
        If an attempt is made to divide by zero, the result is empty.
        For division involving quantities, the resulting quantity will have the appropriate unit.

        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        left_value, right_value = evaluate_and_prepare_collection_values(
            self, self.left, self.right, collection, create
        )
        if left_value is None or right_value is None:
            return []
        if right_value == 0:
            return []
        elif isinstance(left_value, (int, float)) and isinstance(
            right_value, (int, float)
        ):
            return [FHIRPathCollectionItem.wrap(left_value / right_value)]
        elif isinstance(left_value, (Quantity)) and isinstance(right_value, (Quantity)):
            return [FHIRPathCollectionItem.wrap(left_value / right_value)]
        else:
            raise FHIRPathRuntimeError(
                f"FHIRPath operator {self.__str__()} cannot divide {type(left_value).__name__} and {type(right_value).__name__}."
            )


class Div(FHIRMathOperator):
    """
    A representation of the FHIRPath [`div`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Performs truncated division of the left operand by the right operand (supported for Integer and Decimal).

        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        left_value, right_value = evaluate_and_prepare_collection_values(
            self, self.left, self.right, collection, create
        )
        if left_value is None or right_value is None:
            return []
        if right_value == 0:
            return []
        elif isinstance(left_value, (int, float)) and isinstance(
            right_value, (int, float)
        ):
            return [FHIRPathCollectionItem.wrap(left_value // right_value)]
        elif isinstance(left_value, (Quantity)) and isinstance(right_value, (Quantity)):
            return [FHIRPathCollectionItem.wrap(left_value // right_value)]
        else:
            raise FHIRPathRuntimeError(
                f"FHIRPath operator {self.__str__()} cannot divide {type(left_value).__name__} and {type(right_value).__name__}."
            )


class Mod(FHIRMathOperator):
    """
    A representation of the FHIRPath [`mod`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Computes the remainder of the truncated division of its arguments (supported for Integer and Decimal).

        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If either expression evaluates to a non-singleton collection.
        """
        left_value, right_value = evaluate_and_prepare_collection_values(
            self, self.left, self.right, collection, create
        )
        if left_value is None or right_value is None:
            return []
        elif isinstance(left_value, (int, float)) and isinstance(
            right_value, (int, float)
        ):
            return [FHIRPathCollectionItem.wrap(left_value % right_value)]
        else:
            raise FHIRPathRuntimeError(
                f"FHIRPath operator {self.__str__()} cannot divide {type(left_value).__name__} and {type(right_value).__name__}."
            )
