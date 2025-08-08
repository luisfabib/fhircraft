"""The equality module contains the object representations of the equality FHIRPath operators."""

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
        self, collection: FHIRPathCollection, create: bool = False
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

        Returns:
            FHIRPathCollection: The output collection.
        """
        left_collection, right_collection = evaluate_left_right_expressions(
            self.left, self.right, collection, create=create
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
        return f"{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})"

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
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        Returns true if the collections are the same. In particular, comparing empty collections for equivalence { } ~ { } will result in true.
        If both operands are collections with a single item, they must be of the same type (or implicitly convertible to the same type), and:
            - For primitives
                - String: the strings must be the same, ignoring case and locale, and normalizing whitespace (see String Equivalence for more details).
                - Integer: exactly equal
                - Decimal: values must be equal, comparison is done on values rounded to the precision of the least precise operand. Trailing zeroes after the decimal are ignored in determining precision.
                - Date, DateTime and Time: values must be equal, except that if the input values have different levels of precision, the comparison returns false, not empty ({ }).
                - Boolean: the values must be the same
            - For complex types, equivalence requires all child properties to be equivalent, recursively.
        If both operands are collections with multiple items:
            - Each item must be equivalent
            - Comparison is not order dependent
        Note that this implies that if the collections have a different number of items to compare, or if one input is a value and the other is empty ({ }), the result will be false.

        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection: The output collection.
        """

        def _handle_types(value):
            if isinstance(value, str):
                return value.lower().strip()
            else:
                return value

        left_collection, right_collection = evaluate_left_right_expressions(
            self.left, self.right, collection, create=create
        )
        if len(left_collection) == 0 and len(right_collection) == 0:
            equivalent = True
        elif len(left_collection) == 0 or len(right_collection) == 0:
            equivalent = False
        else:
            equivalent = [_handle_types(item.value) for item in left_collection] == [
                _handle_types(item.value) for item in right_collection
            ]
        return [FHIRPathCollectionItem.wrap(equivalent)]

    def __str__(self):
        return f"{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})"

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
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        The converse of the equals operator, returning true if equal returns false; false if equal
        returns true; and empty ({ }) if equal returns empty. In other words, A != B is short-hand for (A = B).not().


        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection: The output collection
        """
        return [
            FHIRPathCollectionItem.wrap(
                not Equals(self.left, self.right)
                .evaluate(collection, create=create)[0]
                .value
            )
        ]

    def __str__(self):
        return f"{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})"

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
        self, collection: FHIRPathCollection, create=False
    ) -> FHIRPathCollection:
        """
        The converse of the equivalent operator, returning true if equivalent returns
        false and false is equivalent returns true. In other words, A !~ B is short-hand for (A ~ B).not().


        Args:
            collection (FHIRPathCollection): The input collection.

        Args:
            FHIRPathCollection): The output collection.
        """
        return [
            FHIRPathCollectionItem.wrap(
                not Equivalent(self.left, self.right)
                .evaluate(collection, create=create)[0]
                .value
            )
        ]

    def __str__(self):
        return f"{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})"

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
