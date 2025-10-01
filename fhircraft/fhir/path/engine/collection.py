"""The comparison module contains the object representations of the collection FHIRPath operators."""

from fhircraft.fhir.path.engine.combining import Union as UnionFunction
from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
)
from fhircraft.fhir.path.exceptions import FHIRPathRuntimeError
from fhircraft.fhir.path.utils import evaluate_left_right_expressions


class FHIRCollectionOperator(FHIRPath):
    """
    Abstract class definition for the category of collection FHIRPath operators.
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


class Union(FHIRCollectionOperator):
    """
    A representation of the FHIRPath [`|`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Merge the two collections into a single collection, eliminating any duplicate values to
        determine equality). There is no expectation of order in the resulting collection.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.
        """
        left_collection, right_collection = evaluate_left_right_expressions(
            self.left, self.right, collection, environment, create=create
        )
        return UnionFunction(left_collection).evaluate(
            right_collection, environment, create
        )

    def __str__(self):
        return f"{self.left} | {self.right}"


class In(FHIRCollectionOperator):
    """
    A representation of the FHIRPath [`in`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the left operand is a collection with a single item, this operator returns true if the item is in the
        right operand using equality semantics. If the left-hand side of the operator is empty, the result is empty,
        if the right-hand side is empty, the result is false. If the left operand has multiple items, an exception is thrown.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathRuntimeError: If the left expression evaluates to a non-singleton collection.
        """
        left_collection, right_collection = evaluate_left_right_expressions(
            self.left, self.right, collection, environment, create
        )
        if len(left_collection) == 0:
            return []
        if len(right_collection) == 0:
            return [FHIRPathCollectionItem.wrap(False)]
        if len(left_collection) != 1:
            raise FHIRPathRuntimeError(
                "Left expression evaluates to a non-singleton collection."
            )
        value = left_collection[0].value
        check_collection = [
            item.value if isinstance(item, FHIRPathCollectionItem) else item
            for item in right_collection
        ]
        return [FHIRPathCollectionItem.wrap(value in check_collection)]

    def __str__(self):
        return f"{self.left} in {self.right}"


class Contains(FHIRCollectionOperator):
    """
    A representation of the FHIRPath [`contains`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the right operand is a collection with a single item, this operator returns true if the item is in the
        left operand using equality semantics. If the right-hand side of the operator is empty, the result is empty,
        if the left-hand side is empty, the result is false. This is the converse operation of `in`.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If the left expression evaluates to a non-singleton collection.
        """
        left_collection, right_collection = evaluate_left_right_expressions(
            self.left, self.right, collection, environment, create
        )
        if len(right_collection) == 0:
            return []
        if len(left_collection) == 0:
            return [FHIRPathCollectionItem.wrap(False)]
        if len(right_collection) != 1:
            raise FHIRPathRuntimeError(
                "Right expression evaluates to a non-singleton collection."
            )
        value = right_collection[0].value
        check_collection = [
            item.value if isinstance(item, FHIRPathCollectionItem) else item
            for item in left_collection
        ]
        return [FHIRPathCollectionItem.wrap(value in check_collection)]

    def __str__(self):
        return f"{self.left} contains {self.right}"
