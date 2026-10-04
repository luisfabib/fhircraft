"""The filtering module contains the object representations of the subsetting-category FHIRPath functions."""

__all__ = [
    "Index",
    "Single",
    "First",
    "Last",
    "Tail",
    "Skip",
    "Take",
    "Intersect",
    "Exclude",
]

from typing import List, Optional, Union

from fhircraft.fhir.path.engine.core import (
    _targets_of,
    FHIRPathNode,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathFunction,
    Literal,
)
from fhircraft.exceptions import FHIRPathException
from fhircraft.utils import ensure_list


class Index(FHIRPathNode):
    """
    A representation of the FHIRPath index [`[idx]`](https://hl7.org/fhirpath/N1/#index-integer-collection) operator.

    Attributes:
        index (int): The index value for the FHIRPath index.
    """

    def __init__(self, index: int | Literal):
        if isinstance(index, Literal):
            index = index.value
        if not isinstance(index, int):
            raise FHIRPathException("Index() argument must be an integer number.")
        self.index = index

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        The indexer operation returns a collection with only the index-th item (0-based index). If the input
        collection is empty (`[]`), or the index lies outside the boundaries of the input collection,
        an empty collection is returned.

        Args:
            collection (FHIRPathCollection): The input collection.

        Returns:
            FHIRPathCollection: The indexed collection item.

        Notes:
            When the collection addresses a single element location (e.g. `Patient.name`), the result
            carries the accessor of the indexed slot as its `target` even if that position is out of
            bounds, so that it can be written to later.
        """
        targets = _targets_of(collection)
        field_targets = [t for t in targets if t.index is None]
        if (
            len(field_targets) == 1
            and len(field_targets) == len(targets)
            and (field_targets[0].is_list or self.index == 0)
            and self.index >= 0
        ):
            slot = field_targets[0].at(self.index)
            value = slot.get()
            items = [FHIRPathCollectionItem(value, slot)] if value is not None else []
            return FHIRPathCollection(items, targets=[slot])
        if len(targets) == 1 and targets[0].index is not None and self.index == 0:
            # Index zero of a single (possibly absent) slot is that slot.
            return FHIRPathCollection(list(collection)[:1], targets=targets)
        if collection and -len(collection) <= self.index < len(collection):
            return FHIRPathCollection([collection[self.index]])
        return FHIRPathCollection()

    def __eq__(self, other):
        return isinstance(other, Index) and self.index == other.index

    def __str__(self):
        return "[%i]" % self.index

    def __repr__(self):
        return "%s(index=%r)" % (self.__class__.__name__, self.index)

    def __hash__(self):
        return hash(self.index)


class Single(FHIRPathFunction):
    """
    A representation of the FHIRPath [`single()`](https://hl7.org/fhirpath/N1/#single-collection) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Will return the single item in the input if there is just one item. If the input collection is empty (`[]`), the result is empty.
        If there are multiple items, an error is signaled to the evaluation environment. This function is useful for ensuring that an
        error is returned if an assumption about cardinality is violated at run-time.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection): The output collection.

        Info:
            Equivalent to `Index(0)` with additional error raising in case of non-singleton input collection.
        """
        if len(collection) > 1:
            raise FHIRPathException(
                f"Expected single value for single(), instead got {len(collection)} items in the collection"
            )
        return Index(0).evaluate(collection, environment)


class First(FHIRPathFunction):
    """
    A representation of the FHIRPath [`first()`](https://hl7.org/fhirpath/N1/#first-collection) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Returns a collection containing only the first item in the input collection.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection): The output collection.

        Info:
            Equivalent to `Index(0)`.
        """
        return Index(0).evaluate(collection, environment)


class Last(FHIRPathFunction):
    """
    A representation of the FHIRPath [`last()`](https://hl7.org/fhirpath/N1/#last-collection) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Returns a collection containing only the last item in the input collection.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection): The output collection.

        Info:
            Equivalent to `Index(-1)`.
        """
        return Index(-1).evaluate(collection, environment)


class Tail(FHIRPathFunction):
    """
    A representation of the FHIRPath [`tail()`](https://hl7.org/fhirpath/N1/#tail-collection) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Returns a collection containing all but the first item in the input collection. Will return
        an empty collection if the input collection has no items, or only one item.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection): The output collection.
        """
        return ensure_list(collection[1:])


class Skip(FHIRPathFunction):
    """
    A representation of the FHIRPath [`skip()`](https://hl7.org/fhirpath/N1/#skipnum-integer-collection) function.

    Attributes:
        num (int | FHIRPathNode): The number of items to skip or FHIRPath evaluating to an integer.
    """

    def __init__(self, num: int | FHIRPathNode):
        self.num = Literal(num) if not isinstance(num, FHIRPathNode) else num

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Returns a collection containing all but the first `num` items in the input collection. Will return
        an empty collection if there are no items remaining after the indicated number of items have
        been skipped, or if the input collection is empty. If `num` is less than or equal to zero, the
        input collection is simply returned.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection): The output collection.
        """
        if not isinstance(
            num := self.num.single(collection, environment=environment), int
        ):
            raise FHIRPathException(
                "Skip() argument must evaluate to an integer number."
            )
        if num <= 0:
            return []
        return ensure_list(collection[num:])


class Take(FHIRPathFunction):
    """
    A representation of the FHIRPath [`take()`](https://hl7.org/fhirpath/N1/#takenum-integer-collection) function.

    Attributes:
        num (int): The number of items to take.
    """

    def __init__(self, num: int | FHIRPathNode):
        self.num = Literal(num) if not isinstance(num, FHIRPathNode) else num

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Returns a collection containing the first `num` items in the input collection, or less if there
        are less than `num` items. If num is less than or equal to 0, or if the input collection
        is empty (`[]`), take returns an empty collection.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection): The output collection.
        """
        if not isinstance(
            num := self.num.single(collection, environment=environment), int
        ):
            raise FHIRPathException(
                "Skip() argument must evaluate to an integer number."
            )
        if num <= 0:
            return []
        return ensure_list(collection[:num])


class Intersect(FHIRPathFunction):
    """
    A representation of the FHIRPath [`intersect()`](https://hl7.org/fhirpath/N1/#intersectother-collection-collection) function.

    Attributes:
        other_collection (FHIRPathCollection): The other collection to compute the intersection with.
    """

    def __init__(self, other_collection: FHIRPathNode | FHIRPathCollection):
        self.other_collection = other_collection

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Returns the set of elements that are in both collections. Duplicate items will be eliminated
        by this function. Order of items is preserved in the result of this function.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection): The output collection.
        """
        if isinstance(self.other_collection, FHIRPathNode):
            self.other_collection = self.other_collection.evaluate(
                collection, environment
            )
        return [item for item in collection if item in self.other_collection]


class Exclude(FHIRPathFunction):
    """
    A representation of the FHIRPath [`exclude()`](https://hl7.org/fhirpath/N1/#excludeother-collection-collection) function.

    Attributes:
        other_collection (FHIRPathCollection): The other collection to compute the exclusion with.
    """

    def __init__(self, other_collection: FHIRPathNode | FHIRPathCollection):
        self.other_collection = other_collection

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict
    ) -> FHIRPathCollection:
        """
        Returns the set of elements that are not in the other collection. Duplicate items will not be
        eliminated by this function, and order will be preserved.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.

        Returns:
            FHIRPathCollection): The output collection.
        """
        if isinstance(self.other_collection, FHIRPathNode):
            self.other_collection = self.other_collection.evaluate(
                collection, environment
            )
        return [item for item in collection if item not in self.other_collection]
