"""
For all boolean operators, the collections passed as operands are first evaluated as Booleans.
The operators then use three-valued logic to propagate empty operands.
"""

from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathFunction,
)
from fhircraft.fhir.path.exceptions import FHIRPathRuntimeError


def _evaluate_boolean_expressions(
    left: FHIRPath | FHIRPathCollection,
    right: FHIRPath | FHIRPathCollection,
    collection: FHIRPathCollection,
    environment: dict,
    create: bool,
) -> tuple[bool | None, bool | None]:
    """
    Evaluates the boolean values of two FHIRPath expressions or collections within a given context.

    Args:
        left (FHIRPath | FHIRPathCollection): The left operand, which can be a FHIRPath expression or a collection.
        right (FHIRPath | FHIRPathCollection): The right operand, which can be a FHIRPath expression or a collection.
        collection (FHIRPathCollection): The context collection used for evaluation.
        environment (dict): The environment context for the evaluation.
        create (bool): Whether to create missing elements during evaluation.

    Returns:
        tuple[bool | None, bool | None]: A tuple containing the boolean values of the left and right operands.
            Each value is True, False, or None if the operand cannot be evaluated to a boolean.
    """
    left_collection = (
        left.evaluate(collection, environment, create)
        if isinstance(left, FHIRPath)
        else left
    )
    if isinstance(left_collection, bool):
        left_boolean = left_collection
    else:
        if len(left_collection) > 0:
            left_boolean = bool(left_collection[0].value)
        else:
            left_boolean = None
    right_collection = (
        right.evaluate(collection, environment, create)
        if isinstance(right, FHIRPath)
        else right
    )
    if isinstance(right_collection, bool):
        right_boolean = right_collection
    else:
        if len(right_collection) > 0:
            right_boolean = bool(right_collection[0].value)
        else:
            right_boolean = None
    return left_boolean, right_boolean


class And(FHIRPath):
    """
    A representation of the FHIRPath [`and`](https://hl7.org/fhirpath/N1/#and) boolean logic operator.

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
        Returns `True` if both operands evaluate to `True`, `False` if either operand evaluates to `False`, and the empty collection (`[]`) otherwise.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        left_boolean, right_boolean = _evaluate_boolean_expressions(
            self.left, self.right, collection, environment, create=create
        )
        if left_boolean is None:
            if right_boolean is True:
                return []
            elif right_boolean is False:
                return [FHIRPathCollectionItem.wrap(False)]
            elif right_boolean is None:
                return []
        elif right_boolean is None:
            if left_boolean is True:
                return []
            elif left_boolean is False:
                return [FHIRPathCollectionItem.wrap(False)]
            elif left_boolean is None:
                return []
        return [FHIRPathCollectionItem.wrap(left_boolean and right_boolean)]

    def __str__(self):
        return f"{self.left} and {self.right}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, And)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))


class Or(FHIRPath):
    """
    A representation of the FHIRPath [`or`](https://hl7.org/fhirpath/N1/#or) boolean logic operator.

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
        Returns `False` if both operands evaluate to `False`, `True` if either operand evaluates to `True`, and empty (`[]`) otherwise.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        left_boolean, right_boolean = _evaluate_boolean_expressions(
            self.left, self.right, collection, environment, create=create
        )
        if left_boolean is None:
            if right_boolean is True:
                return [FHIRPathCollectionItem.wrap(True)]
            elif right_boolean is False:
                return []
            elif right_boolean is None:
                return []
        elif right_boolean is None:
            if left_boolean is True:
                return [FHIRPathCollectionItem.wrap(True)]
            elif left_boolean is False:
                return []
            elif left_boolean is None:
                return []
        return [FHIRPathCollectionItem.wrap(left_boolean or right_boolean)]

    def __str__(self):
        return f"{self.left} or {self.right}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, Or)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))


class Xor(FHIRPath):
    """
    A representation of the FHIRPath [`xor`](https://hl7.org/fhirpath/N1/#xor) boolean logic operator.

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
        Returns `True` if exactly one of the operands evaluates to `True`, `False` if either both operands evaluate to `True` or both operands evaluate to `False`, and the empty collection (`[]`) otherwise.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        left_boolean, right_boolean = _evaluate_boolean_expressions(
            self.left, self.right, collection, environment, create
        )
        if left_boolean is None or right_boolean is None:
            return []
        return [FHIRPathCollectionItem.wrap(left_boolean ^ right_boolean)]

    def __str__(self):
        return f"{self.left} xor {self.right}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, Xor)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))


class Implies(FHIRPath):
    """
    A representation of the FHIRPath [`implies`](https://hl7.org/fhirpath/N1/#implies) boolean logic operator.

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
        If the left operand evaluates to `True`, this operator returns the boolean evaluation of the right operand. If the
        left operand evaluates to `False`, this operator returns `True`. Otherwise, this operator returns `True` if the right
        operand evaluates to `True`, and the empty collection (`[]`) otherwise.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        left_boolean, right_boolean = _evaluate_boolean_expressions(
            self.left, self.right, collection, environment, create
        )
        if left_boolean is None:
            if right_boolean is True:
                return [FHIRPathCollectionItem.wrap(True)]
            elif right_boolean is False:
                return []
            elif right_boolean is None:
                return []
        elif right_boolean is None:
            if left_boolean is True:
                return []
            elif left_boolean is False:
                return [FHIRPathCollectionItem.wrap(True)]
            elif left_boolean is None:
                return []
        elif left_boolean is True:
            if right_boolean is True:
                return [FHIRPathCollectionItem.wrap(True)]
            elif right_boolean is False:
                return [FHIRPathCollectionItem.wrap(False)]
        elif right_boolean is True:
            if left_boolean is True:
                return [FHIRPathCollectionItem.wrap(True)]
            elif left_boolean is False:
                return [FHIRPathCollectionItem.wrap(True)]
        elif right_boolean is False and left_boolean is False:
            return [FHIRPathCollectionItem.wrap(True)]
        return []

    def __str__(self):
        return f"{self.left} implies {self.right}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, Implies)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))


class Not(FHIRPathFunction):
    """
    A representation of the FHIRPath [`not`](https://hl7.org/fhirpath/N1/#not) boolean logic function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns `True` if the input collection evaluates to `False`, and `False` if it evaluates to `True`. Otherwise, the result is empty (`[]`):


        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        if len(collection) > 1:
            raise FHIRPathRuntimeError(
                "Cannot assert Not() for a collection that has more than one item."
            )
        elif len(collection) == 0:
            return []
        else:
            boolean = bool(collection[0].value)
            return [FHIRPathCollectionItem.wrap(not boolean)]
