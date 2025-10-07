"""The equality module contains the object representations of the equality FHIRPath operators."""

from pydantic import BaseModel

from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
)
from fhircraft.fhir.path.utils import evaluate_left_right_expressions


class Equals(FHIRPath):
    """
    A representation of the FHIRPath [`=`](https://hl7.org/fhirpath/N1/#equals) operator.

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
        self, collection: FHIRPathCollection, environment, create: bool = False
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
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.
        """
        left_collection, right_collection = evaluate_left_right_expressions(
            self.left, self.right, collection, environment, create
        )
        if len(left_collection) == 0 or len(right_collection) == 0:
            equals = []
        elif len(left_collection) == 1 and len(right_collection) == 1:
            equals = left_collection[0] == right_collection[0]
        elif len(left_collection) != len(right_collection):
            equals = False
        else:
            equals = all(l == r for l, r in zip(left_collection, right_collection))
        return [FHIRPathCollectionItem.wrap(equals)]

    def __str__(self):
        return f"{self.left} == {self.right}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, Equals)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))


class Equivalent(FHIRPath):
    """
    A representation of the FHIRPath [`~`](https://hl7.org/fhirpath/N1/#and) operator.

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
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.
        """

        left_collection, right_collection = evaluate_left_right_expressions(
            self.left, self.right, collection, environment, create
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

            for left_item in left_collection:
                found_equivalent = False
                for i, right_item in enumerate(remaining_right):
                    # Use equivalence logic based on FHIRPath specification
                    if self._is_equivalent(left_item, right_item):
                        remaining_right.pop(i)
                        found_equivalent = True
                        break

                if not found_equivalent:
                    equivalent = False
                    break

        return [FHIRPathCollectionItem.wrap(equivalent)]

    def __str__(self):
        return f"{self.left} ~ {self.right}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, Equivalent)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))

    def _is_equivalent(
        self, left_item: FHIRPathCollectionItem, right_item: FHIRPathCollectionItem
    ) -> bool:
        """
        Check if two FHIRPathCollectionItems are equivalent according to FHIRPath rules.

        Args:
            left_item: The left item to compare
            right_item: The right item to compare

        Returns:
            bool: True if the items are equivalent, False otherwise
        """
        left_value = left_item.value
        right_value = right_item.value

        # Handle None values
        if left_value is None and right_value is None:
            return True
        if left_value is None or right_value is None:
            return False

        # Type checking - must be same type or implicitly convertible
        if type(left_value) != type(right_value):
            return False

        # String equivalence: case-insensitive and normalized whitespace
        if isinstance(left_value, str):
            return left_value.lower().strip() == right_value.lower().strip()

        # Numeric equivalence
        elif isinstance(left_value, (int, float)):
            # For floats: compare rounded to the least precise operand
            if isinstance(left_value, float):
                # Get decimal places for each operand
                def decimal_places(val: float) -> int:
                    s = f"{val:.16f}".rstrip("0").rstrip(".")
                    if "." in s:
                        return len(s.split(".")[-1])
                    return 0

                left_decimals = decimal_places(left_value)
                right_decimals = decimal_places(right_value)
                precision = min(left_decimals, right_decimals)
                # Round both to the least precise
                return round(left_value, precision) == round(right_value, precision)
            return left_value == right_value

        # Boolean equivalence
        elif isinstance(left_value, bool):
            return left_value == right_value

        # For complex types and other cases, fall back to regular equality
        else:
            if isinstance(left_value, BaseModel) and isinstance(right_value, BaseModel):
                left_value = left_value.model_dump(exclude={"id"}, exclude_unset=True)
                right_value = right_value.model_dump(exclude={"id"}, exclude_unset=True)
            if isinstance(left_value, dict):
                left_value.pop("id", None)
                right_value.pop("id", None)
            return left_value == right_value


class NotEquals(FHIRPath):
    """
    A representation of the FHIRPath [`!=`](https://hl7.org/fhirpath/N1/#and) operator.

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
        The converse of the equals operator, returning true if equal returns false; false if equal
        returns true; and empty ({ }) if equal returns empty. In other words, A != B is short-hand for (A = B).not().


        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        return [
            FHIRPathCollectionItem.wrap(
                not Equals(self.left, self.right)
                .evaluate(collection, environment, create)[0]
                .value
            )
        ]

    def __str__(self):
        return f"{self.left} != {self.right}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, NotEquals)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))


class NotEquivalent(FHIRPath):
    """
    A representation of the FHIRPath [`!~`](https://hl7.org/fhirpath/N1/#and) operator.

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
        The converse of the equivalent operator, returning true if equivalent returns
        false and false is equivalent returns true. In other words, A !~ B is short-hand for (A ~ B).not().


        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            (FHIRPathCollection): The output collection.
        """
        return [
            FHIRPathCollectionItem.wrap(
                not Equivalent(self.left, self.right)
                .evaluate(collection, environment, create)[0]
                .value
            )
        ]

    def __str__(self):
        return f"{self.left} !~ {self.right}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, NotEquivalent)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))
