"""The filtering module contains the object representations of the existence-category FHIRPath functions."""

from typing import Callable

from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathFunction,
)
from fhircraft.fhir.path.engine.filtering import Where
from fhircraft.fhir.path.exceptions import FHIRPathError
from fhircraft.fhir.path.utils import get_expression_context


class Empty(FHIRPathFunction):
    """
    Representation of the FHIRPath [`empty()`](http://hl7.org/fhirpath/N1/#empty-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns `True` if the input collection is empty (`{}`) and `False` otherwise.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        return [FHIRPathCollectionItem.wrap(len(collection) == 0)]


class Exists(FHIRPathFunction):
    """
    Representation of the FHIRPath [`exists()`](http://hl7.org/fhirpath/N1/#existscriteria-expression-boolean) function.

    Attributes:
        criteria (FHIRPath): Optional criteria to be applied to the collection prior to the determination of the exists
    """

    def __init__(self, criteria: FHIRPath | None = None):
        self.criteria = criteria

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns `True` if the collection has any elements, and `False` otherwise.
        This is the opposite of empty(), and as such is a shorthand for empty().not().
        If the input collection is empty (`{}`), the result is `False`.
        The function can also take an optional criteria to be applied to the collection
        prior to the determination of the exists. In this case, the function is
        shorthand for where(criteria).exists().

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        if self.criteria:
            collection = Where(self.criteria).evaluate(collection, environment, create)
        return [FHIRPathCollectionItem.wrap(len(collection) > 0)]

    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.criteria.__str__() if self.criteria else ""})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.criteria.__repr__() if self.criteria else ""})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.criteria == other.criteria


class All(FHIRPathFunction):
    """
    Representation of the FHIRPath [`all()`](https://hl7.org/fhirpath/N1/#allcriteria-expression-boolean) function.

    Attributes:
        criteria (FHIRPath): Criteria to be applied to the collection prior to the evalution.
    """

    def __init__(self, criteria: FHIRPath | FHIRPathCollection):
        self.criteria = criteria

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns `True` if for every element in the input collection, criteria evaluates to `True`.
        Otherwise, the result is `False`. If the input collection is empty (`{}`), the result is `True`.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        if len(collection) == 0:
            return [FHIRPathCollectionItem.wrap(True)]
        return [
            FHIRPathCollectionItem.wrap(
                all(
                    [
                        (
                            self.criteria.evaluate(
                                [item],
                                get_expression_context(environment, item, index),
                                create,
                            )
                            if isinstance(self.criteria, FHIRPath)
                            else item.value == self.criteria
                        )
                        for index, item in enumerate(collection)
                    ]
                )
            )
        ]

    def __str__(self):
        return f"{self.__class__.__name__.lower()}({self.criteria.__str__()})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.criteria.__repr__()})"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.criteria == other.criteria


def _all_or_any_boolean(
    collection: FHIRPathCollection, op: Callable, boolean: bool
) -> FHIRPathCollection:
    values = []
    if len(collection) == 0:
        if op == any:
            return [FHIRPathCollectionItem.wrap(False)]
        else:
            return [FHIRPathCollectionItem.wrap(True)]
    for item in collection:
        if not isinstance(item.value, bool):
            raise FHIRPathError(
                f"The collection evaluated by allTrue() has a non-boolean value: {item.value}"
            )
        values.append(item.value == boolean)
    return [FHIRPathCollectionItem.wrap(op(values))]


class AllTrue(FHIRPathFunction):
    """
    Representation of the FHIRPath [`allTrue()`](https://hl7.org/fhirpath/N1/#alltrue-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Takes a collection of Boolean values and returns `True` if all the items are `True`. If any
        items are `False`, the result is `False`. If the input is empty (`{}`), the result is `True`.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        return _all_or_any_boolean(collection, all, True)


class AnyTrue(FHIRPathFunction):
    """
    Representation of the FHIRPath [`anyTrue()`](https://hl7.org/fhirpath/N1/#anytrue-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Takes a collection of Boolean values and returns `True` if any of the items are `True`.
        If all the items are `False`, or if the input is empty (`{}`), the result is `False`.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        return _all_or_any_boolean(collection, any, True)


class AllFalse(FHIRPathFunction):
    """
    Representation of the FHIRPath [`allFalse()`](https://hl7.org/fhirpath/N1/#allfalse-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Takes a collection of Boolean values and returns `True` if all the items are `False`.
        If any items are `True`, the result is `False`. If the input is empty (`{}`), the result is `True`.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        return _all_or_any_boolean(collection, all, False)


class AnyFalse(FHIRPathFunction):
    """
    Representation of the FHIRPath [`anyFalse()`](https://hl7.org/fhirpath/N1/#anyfalse-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Takes a collection of Boolean values and returns `True` if any of the items are `False`. If all
        the items are `True`, or if the input is empty (`{}`), the result is `False`.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        return _all_or_any_boolean(collection, any, False)


class SubsetOf(FHIRPathFunction):
    """
    Representation of the FHIRPath [`subsetOf()`](https://hl7.org/fhirpath/N1/#subsetofother-collection-boolean) function.

    Attributes:
        other (Union[FHIRPathCollection, FHIRPath]): other collection to which to determine whether input is a subset of.
    """

    def __init__(self, other: FHIRPathCollection | FHIRPath):
        self.other = other

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns `True` if all items in the input collection are members of the collection passed as the
        other argument.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Note:
            Conceptually, this function is evaluated by testing each element in the input collection for
            membership in the other collection, with a default of `True`. This means that if the input collection
            is empty (`[]`), the result is `True`, otherwise if the other collection is empty, the result is `False`.
        """
        if len(collection) == 0:
            return [FHIRPathCollectionItem.wrap(True)]
        other_collection = (
            self.other.evaluate(collection, environment, create)
            if isinstance(self.other, FHIRPath)
            else self.other
        )
        if len(other_collection) == 0:
            return [FHIRPathCollectionItem.wrap(False)]
        for item in collection:
            if item not in other_collection:
                return [FHIRPathCollectionItem.wrap(False)]
        else:
            return [FHIRPathCollectionItem.wrap(True)]

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.other == other.other


class SupersetOf(FHIRPathFunction):
    """
    Representation of the FHIRPath [`supersetOf()`](https://hl7.org/fhirpath/N1/#supersetofother-collection-boolean) function.

    Attributes:
        other (Union[FHIRPathCollection, FHIRPath]): Other collection to which to determine whether input is a superset of.
    """

    def __init__(self, other: FHIRPathCollection | FHIRPath):
        self.other = other

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns true if all items in the collection passed as the other argument are
        members of the input collection. Membership is determined using the = (Equals) (=) operation.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Note:
            Conceptually, this function is evaluated by testing each element in the other collection for
            membership in the input collection, with a default of `True`. This means that if the other collection
            is empty (`[]`), the result is `True`, otherwise if the other collection is empty, the result is `False`.
        """
        if len(collection) == 0:
            return [FHIRPathCollectionItem.wrap(True)]
        other_collection = (
            self.other.evaluate(collection, environment, create)
            if isinstance(self.other, FHIRPath)
            else self.other
        )
        if len(other_collection) == 0:
            return [FHIRPathCollectionItem.wrap(True)]
        for item in other_collection:
            if item not in collection:
                return [FHIRPathCollectionItem.wrap(False)]
        else:
            return [FHIRPathCollectionItem.wrap(True)]

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.other == other.other


class Count(FHIRPathFunction):
    """
    Representation of the FHIRPath [`count()`](https://hl7.org/fhirpath/N1/#count-integer) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the integer count of the number of items in the input collection. Returns 0 when the input collection is empty.


        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        return [FHIRPathCollectionItem.wrap(len(collection))]


class Distinct(FHIRPathFunction):
    """
    Representation of the FHIRPath [`distinct()`](https://hl7.org/fhirpath/N1/#distinct-collection) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns a collection containing only the unique items in the input collection. If the input collection is empty (`[]`), the result is empty.
        Note that the order of elements in the input collection is not guaranteed to be preserved in the result.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        return list(set(collection))


class IsDistinct(FHIRPathFunction):
    """
    Representation of the FHIRPath [`isDistinct()`](https://hl7.org/fhirpath/N1/#isdistinct-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns `True` if all the items in the input collection are distinct.
        If the input collection is empty (`[]`), the result is `True`.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection
        """
        return [
            FHIRPathCollectionItem.wrap(len(list(set(collection))) == len(collection))
        ]
