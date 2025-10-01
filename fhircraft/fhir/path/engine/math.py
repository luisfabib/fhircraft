"""The tree navigation module contains the object representations of the math category FHIRPath operators/functions."""

from math import ceil, exp, floor, log, sqrt
from typing import Callable

from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathFunction,
    Literal,
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
        raise NotImplementedError("Subclasses must implement __str__ method.")

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
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        For Integer, Decimal, and quantity, adds the operands. For strings, concatenates the right
        operand to the left operand.
        When adding quantities, the units of each quantity must be the same.


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

    def __str__(self):
        return f"{self.left} + {self.right}"


class Subtraction(FHIRMathOperator):
    """
    A representation of the FHIRPath [`-`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Subtracts the right operand from the left operand (supported for Integer, Decimal, and Quantity).
        When subtracting quantities, the units of each quantity must be the same.

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

    def __str__(self):
        return f"{self.left} - {self.right}"


class Multiplication(FHIRMathOperator):
    """
    A representation of the FHIRPath [`*`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Multiplies both arguments (supported for Integer, Decimal, and Quantity). For multiplication
        involving quantities, the resulting quantity will have the appropriate unit.


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

    def __str__(self):
        return f"{self.left} * {self.right}"


class Division(FHIRMathOperator):
    """
    A representation of the FHIRPath [`/`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Divides the left operand by the right operand (supported for Integer, Decimal, and Quantity).
        The result of a division is always Decimal, even if the inputs are both Integer. For integer division,
        use the `div` operator.
        If an attempt is made to divide by zero, the result is empty.
        For division involving quantities, the resulting quantity will have the appropriate unit.

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

    def __str__(self):
        return f"{self.left} / {self.right}"


class Div(FHIRMathOperator):
    """
    A representation of the FHIRPath [`div`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Performs truncated division of the left operand by the right operand (supported for Integer and Decimal).

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

    def __str__(self):
        return f"{self.left} div {self.right}"


class Mod(FHIRMathOperator):
    """
    A representation of the FHIRPath [`mod`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Computes the remainder of the truncated division of its arguments (supported for Integer and Decimal).

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

    def __str__(self):
        return f"{self.left} mod {self.right}"


class FHIRPathMathFunction(FHIRPathFunction):
    """
    Abstract class definition for the category of math FHIRPath functions.
    """

    math_operation: Callable

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Computes the computed value based on its argument (supported for Integer, Decimal and Quantity values).

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: For non-singleton collections.
        """
        if len(collection) == 0:
            return []
        elif len(collection) > 1:
            raise FHIRPathRuntimeError("Input collection must be a singleton.")
        value = collection[0].value
        if isinstance(value, (int, float)):
            value = self.math_operation(value)
        elif isinstance(value, (Quantity)):
            value = Quantity(self.math_operation(value.value), value.unit)
        else:
            raise FHIRPathRuntimeError(
                f"FHIRPath function {self.__class__.__name__}() cannot compute abs for {type(value).__name__}."
            )
        return [FHIRPathCollectionItem.wrap(value)]


class Abs(FHIRPathMathFunction):
    """
    A representation of the FHIRPath [`abs`](https://hl7.org/fhirpath/N1/#abs-integer-decimal-quantity) function.
    """

    math_operation = abs


class Ceiling(FHIRPathMathFunction):
    """
    A representation of the FHIRPath [`ceiling`](https://hl7.org/fhirpath/N1/#ceiling-integer) function.
    """

    math_operation = ceil


class Exp(FHIRPathMathFunction):
    """
    A representation of the FHIRPath [`exp`](https://hl7.org/fhirpath/N1/#exp-decimal) function.
    """

    math_operation = exp


class Floor(FHIRPathMathFunction):
    """
    A representation of the FHIRPath [`floor`](https://hl7.org/fhirpath/N1/#floor-integer) function.
    """

    math_operation = floor


class Ln(FHIRPathMathFunction):
    """
    A representation of the FHIRPath [`ln`](https://hl7.org/fhirpath/N1/#ln-decimal) function.
    """

    math_operation = log


class Log(FHIRPathMathFunction):
    """
    A representation of the FHIRPath [`log`](https://hl7.org/fhirpath/N1/#log-decimal) function.

    Attributes:
        base (int | Literal): The base of the logarithm. Must be an integer greater than 1.
    """

    def __init__(self, base: int | Literal):
        self.base = base if not isinstance(base, Literal) else base.value
        if not isinstance(self.base, int) or self.base <= 1:
            raise FHIRPathRuntimeError(
                "The base argument of the log function must be an integer greater than 1."
            )
        self.math_operation = lambda x: log(x, self.base)


class Power(FHIRPathMathFunction):
    """
    A representation of the FHIRPath [`power`](https://hl7.org/fhirpath/N1/#powerexponent-integer-decimal-integer-decimal) function.

    Attributes:
        exponent (int | float | Literal): The exponent to which the input value is raised..
    """

    def __init__(self, exponent: int | float | Literal):
        self.exponent = (
            exponent if not isinstance(exponent, Literal) else exponent.value
        )
        if not isinstance(self.exponent, (int, float)):
            raise FHIRPathRuntimeError(
                "The exponent argument of the power function must be a number."
            )
        self.math_operation = lambda x: pow(x, self.exponent)


class Round(FHIRPathMathFunction):
    """
    A representation of the FHIRPath [`round`](https://hl7.org/fhirpath/N1/#roundprecision-integer-decimal) function.
    """

    def __init__(self, precision: int | Literal):
        self.precision = (
            precision if not isinstance(precision, Literal) else precision.value
        )
        if not isinstance(self.precision, int) or self.precision < 0:
            raise FHIRPathRuntimeError(
                "The precision argument of the round function must be a non-negative integer."
            )
        self.math_operation = lambda x: round(x, self.precision)


class Sqrt(FHIRPathMathFunction):
    """
    A representation of the FHIRPath [`sqrt`](https://hl7.org/fhirpath/N1/#sqrt-decimal) function.
    """

    math_operation = sqrt


class Truncate(FHIRPathMathFunction):
    """
    A representation of the FHIRPath [`truncate`](https://hl7.org/fhirpath/N1/#truncate-integer) function.
    """

    math_operation = int
