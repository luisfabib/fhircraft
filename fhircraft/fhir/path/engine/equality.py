"""The equality module contains the object representations of the equality FHIRPath operators."""

__all__ = [
    "Equals",
    "Equivalent",
    "NotEquals",
    "NotEquivalent",
]

import re
from typing import Any

from pydantic import BaseModel

from fhircraft.fhir.path.engine.core import (
    FHIRPathNode,
    FHIRPathCollection,
    FHIRPathCollectionItem,
)
from fhircraft.fhir.path.engine.literals import TypePrecisionError
from fhircraft.fhir.path.utils import _evaluate_left_right_expressions


class Equals(FHIRPathNode):
    """
    A representation of the FHIRPath [`=`](https://hl7.org/fhirpath/N1/#equals) operator.

    Attributes:
        left (FHIRPathNode | FHIRPathCollection): Left operand.
        right (FHIRPathNode | FHIRPathCollection): Right operand.
    """

    def __init__(
        self,
        left: FHIRPathNode | FHIRPathCollection,
        right: FHIRPathNode | FHIRPathCollection,
    ):
        self.left = left
        self.right = right

    def evaluate(
        self, collection: FHIRPathCollection, environment
    ) -> FHIRPathCollection:
        """
        Returns true if the left collection is equal to the right collection:
        As noted above, if either operand is an empty collection, the result is an empty collection. Otherwise:
        If both operands are collections with a single item, they must be of the same type (or be implicitly convertible to the same type), and:
            - For primitives:
                - String: comparison is based on Unicode values
                - Integer: values must be exactly equal
                - Decimal: values must be equal, trailing zeroes after the decimal are ignored
                - Boolean: values must be the same
                - Date: must be exactly the same
                - DateTime: must be exactly the same, respecting the timezone offset (though +00:00 = -00:00 = Z)
                - Time: must be exactly the same
            - For complex types, equality requires all child properties to be equal, recursively.=
        If both operands are collections with multiple items:
            - Each item must be equal
            - Comparison is order dependent
        Otherwise, equals returns false.
        Note that this implies that if the collections have a different number of items to compare, the result will be false.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection: The output collection.
        """
        left_collection, right_collection = _evaluate_left_right_expressions(
            self.left, self.right, collection, environment
        )
        if len(left_collection) == 0 or len(right_collection) == 0:
            return FHIRPathCollection([])
        elif len(left_collection) == 1 and len(right_collection) == 1:
            try:
                equals = left_collection[0] == right_collection[0]
            except TypePrecisionError:
                return FHIRPathCollection([])
        elif len(left_collection) != len(right_collection):
            equals = False
        else:
            try:
                equals = all(l == r for l, r in zip(left_collection, right_collection))
            except TypePrecisionError:
                return FHIRPathCollection([])
        return FHIRPathCollection([FHIRPathCollectionItem.wrap(equals)])

    def __str__(self):
        return f"{self.left} = {self.right}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left!s}, {self.right!s})"

    def __eq__(self, other):
        return (
            isinstance(other, Equals)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))


class Equivalent(FHIRPathNode):
    """
    A representation of the FHIRPath [`~`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPathNode | FHIRPathCollection): Left operand.
        right (FHIRPathNode | FHIRPathCollection): Right operand.
    """

    def __init__(
        self,
        left: FHIRPathNode | FHIRPathCollection,
        right: FHIRPathNode | FHIRPathCollection,
    ):
        self.left = left
        self.right = right

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Returns true if the collections are the same. In particular, comparing empty collections for equivalence { } ~ { } will result in true.
        If both operands are collections with a single item, they must be of the same type (or implicitly convertible to the same type), and:
            - For primitives
                - String: the strings must be the same, ignoring case and locale, and normalizing whitespace.
                - Integer: exactly equal
                - Decimal: values must be equal, comparison is done on values rounded to the precision of the least precise operand. Trailing zeroes after the decimal are ignored in determining precision.
                - Date, DateTime and Time: values must be equal, except that if the input values have different levels of precision, the comparison returns false, not empty ({ }).
                - Boolean: the values must be the same
            - For complex types, equivalence requires all child properties to be equivalent, recursively, except for "id" elements.
        If both operands are collections with multiple items:
            - Each item must be equivalent
            - Comparison is not order dependent
        Note that this implies that if the collections have a different number of items to compare, or if one input is a value and the other is empty ({ }), the result will be false.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection: The output collection.
        """

        left_collection, right_collection = _evaluate_left_right_expressions(
            self.left, self.right, collection, environment
        )
        if len(left_collection) == 0 and len(right_collection) == 0:
            equivalent = True
        elif len(left_collection) == 0 or len(right_collection) == 0:
            equivalent = False
        elif len(left_collection) != len(right_collection):
            equivalent = False
        else:
            # Order-independent comparison: each item in left must have an equivalent in right
            # and vice versa (since lengths are equal, we only need to check one direction)
            remaining_right = list(right_collection)
            equivalent = True

            for left in left_collection:
                found_equivalent = False
                for i, right in enumerate(remaining_right):
                    # Use equivalence logic based on FHIRPath specification
                    if self._is_equivalent(left, right):
                        remaining_right.pop(i)
                        found_equivalent = True
                        break

                if not found_equivalent:
                    equivalent = False
                    break

        return FHIRPathCollection([FHIRPathCollectionItem.wrap(equivalent)])

    def __str__(self):
        return f"{self.left} ~ {self.right}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left!s}, {self.right!s})"

    def __eq__(self, other):
        return (
            isinstance(other, Equivalent)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))

    def _is_equivalent(self, left: Any, right: Any) -> bool:
        """
        Check if two FHIRPathCollectionItems are equivalent according to FHIRPath rules.

        Args:
            left: The left item to compare
            right: The right item to compare

        Returns:
            bool: True if the items are equivalent, False otherwise
        """
        from fhircraft.fhir.resources.base import FHIRPrimitiveModel

        if isinstance(left, FHIRPrimitiveModel):
            left = left.value
        if isinstance(right, FHIRPrimitiveModel):
            right = right.value
        # Handle None values
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False

        # Type checking - must be same type or implicitly convertible
        if type(left) != type(right):
            return False

        # String equivalence: case-insensitive and normalized whitespace
        if isinstance(left, str):
            left = re.sub(r"\s+", " ", left).strip().lower()
            right = re.sub(r"\s+", " ", right).strip().lower()
            return left == right

        # Numeric equivalence
        elif isinstance(left, (int, float)):
            # For floats: compare rounded to the least precise operand
            if isinstance(left, float):
                # Get decimal places for each operand
                def decimal_places(val: float) -> int:
                    s = f"{val:.16f}".rstrip("0").rstrip(".")
                    if "." in s:
                        return len(s.split(".")[-1])
                    return 0

                left_decimals = decimal_places(left)
                right_decimals = decimal_places(right)
                precision = min(left_decimals, right_decimals)
                # Round both to the least precise
                return round(left, precision) == round(right, precision)
            return left == right

        # Boolean equivalence
        elif isinstance(left, bool):
            return left == right

        # For complex types and other cases, fall back to regular equality
        else:
            if isinstance(left, BaseModel) and isinstance(right, BaseModel):
                left = left.model_dump(exclude={"id"}, exclude_unset=True)
                right = right.model_dump(exclude={"id"}, exclude_unset=True)
            if isinstance(left, dict):
                left.pop("id", None)
                right.pop("id", None)
            try:
                return left == right
            except TypePrecisionError:
                return False


class NotEquals(FHIRPathNode):
    """
    A representation of the FHIRPath [`!=`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPathNode | FHIRPathCollection): Left operand.
        right (FHIRPathNode | FHIRPathCollection): Right operand.
    """

    def __init__(
        self,
        left: FHIRPathNode | FHIRPathCollection,
        right: FHIRPathNode | FHIRPathCollection,
    ):
        self.left = left
        self.right = right

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        The converse of the equals operator, returning true if equal returns false; false if equal
        returns true; and empty ({ }) if equal returns empty. In other words, A != B is short-hand for (A = B).not().


        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection: The output collection
        """
        if equals_collection := Equals(self.left, self.right).evaluate(
            collection, environment
        ):
            return FHIRPathCollection(
                [FHIRPathCollectionItem.wrap(not equals_collection[0])]
            )
        else:
            return FHIRPathCollection([])

    def __str__(self):
        return f"{self.left} != {self.right}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left!s}, {self.right!s})"

    def __eq__(self, other):
        return (
            isinstance(other, NotEquals)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))


class NotEquivalent(FHIRPathNode):
    """
    A representation of the FHIRPath [`!~`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPathNode | FHIRPathCollection): Left operand.
        right (FHIRPathNode | FHIRPathCollection): Right operand.
    """

    def __init__(
        self,
        left: FHIRPathNode | FHIRPathCollection,
        right: FHIRPathNode | FHIRPathCollection,
    ):
        self.left = left
        self.right = right

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        The converse of the equivalent operator, returning true if equivalent returns
        false and false is equivalent returns true. In other words, A !~ B is short-hand for (A ~ B).not().


        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            (FHIRPathCollection): The output collection.
        """
        return FHIRPathCollection(
            [
                FHIRPathCollectionItem.wrap(
                    not (
                        Equivalent(self.left, self.right).evaluate(
                            collection, environment
                        )
                    )[0]
                )
            ]
        )

    def __str__(self):
        return f"{self.left} !~ {self.right}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left!s}, {self.right!s})"

    def __eq__(self, other):
        return (
            isinstance(other, NotEquivalent)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))
