"""The filtering module contains the object representations of the subsetting-category FHIRPath functions."""

from functools import partial
from typing import List, Optional, Union

from fhircraft.fhir.path.engine.core import (
    Element,
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathFunction,
    Literal,
)
from fhircraft.fhir.path.exceptions import FHIRPathError
from fhircraft.utils import ensure_list


class Index(FHIRPath):
    """
    A representation of the FHIRPath index [`[idx]`](https://hl7.org/fhirpath/N1/#index-integer-collection) operator.

    Attributes:
        index (int): The index value for the FHIRPath index.
    """

    def __init__(self, index: int | Literal):
        if isinstance(index, Literal):
            index = index.value
        if not isinstance(index, int):
            raise FHIRPathError("Index() argument must be an integer number.")
        self.index = index

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        The indexer operation returns a collection with only the index-th item (0-based index). If the input
        collection is empty (`[]`), or the index lies outside the boundaries of the input collection,
        an empty collection is returned.

        Args:
            collection (FHIRPathCollection): The input collection.
            create (bool): Pad the collection array if the index lies out of bounds of the collection.

        Returns:
            FHIRPathCollection): The indexed collection item.

        Raises:
            FhirPathError: If `create=True` and collection is composed of items with different parent elements.

        Notes:
            The collection padding with `create=True` allows the function to create and later access new elements.
            The padded object is initialized based on the collection items' common parent (if exists).
            Therefore, this option is only available for a homogeneous collection of items.
        """
        # Check whether array is too short and it can be extended
        if len(collection) <= self.index and create:
            # Calculate how many elements must be padded
            pad = self.index - len(collection) + 1
            all_same_parent = collection and all(
                [
                    (
                        item.parent.value
                        in [
                            subitem.parent.value
                            for subitem in collection
                            if subitem.parent
                        ]
                        if item.parent
                        else True
                    )
                    for item in collection
                ]
            )
            if all_same_parent:
                parent_array = collection[0]
                if parent_array.parent:
                    new_values = ensure_list(
                        parent_array.parent.value.get(parent_array.path.label)
                        if isinstance(parent_array.parent.value, dict)
                        else getattr(parent_array.parent.value, parent_array.path.label)
                    )
                    if hasattr(new_values[0].__class__, "model_construct"):
                        new_values.extend(
                            [parent_array.construct_resource() for __ in range(pad)]
                        )
                    else:
                        new_values.extend([None for __ in range(pad)])
                else:
                    new_values = collection
                    new_values.extend(
                        [FHIRPathCollectionItem.wrap(None) for __ in range(pad)]
                    )
                return [
                    FHIRPathCollectionItem(
                        new_values[self.index],
                        path=Element(parent_array.element or ""),
                        setter=(
                            partial(parent_array.setter, index=self.index)
                            if parent_array.setter
                            else None
                        ),
                        parent=parent_array.parent,
                    )
                ]
            else:
                raise FHIRPathError(
                    f"Cannot create new array element due to inhomogeneity in parents"
                )
        # If index is within array bounds, get element
        if collection and len(collection) > self.index:
            return [collection[self.index]]
        # Else return empty list
        return []

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
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Will return the single item in the input if there is just one item. If the input collection is empty (`[]`), the result is empty.
        If there are multiple items, an error is signaled to the evaluation environment. This function is useful for ensuring that an
        error is returned if an assumption about cardinality is violated at run-time.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.

        Info:
            Equivalent to `Index(0)` with additional error raising in case of non-singleton input collection.
        """
        if len(collection) > 1:
            raise FHIRPathError(
                f"Expected single value for single(), instead got {len(collection)} items in the collection"
            )
        return Index(0).evaluate(collection, environment, create=False)


class First(FHIRPathFunction):
    """
    A representation of the FHIRPath [`first()`](https://hl7.org/fhirpath/N1/#first-collection) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns a collection containing only the first item in the input collection.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.

        Info:
            Equivalent to `Index(0)`.
        """
        return Index(0).evaluate(collection, environment, create=False)


class Last(FHIRPathFunction):
    """
    A representation of the FHIRPath [`last()`](https://hl7.org/fhirpath/N1/#last-collection) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns a collection containing only the last item in the input collection.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.

        Info:
            Equivalent to `Index(-1)`.
        """
        return Index(-1).evaluate(collection, environment, create=False)


class Tail(FHIRPathFunction):
    """
    A representation of the FHIRPath [`tail()`](https://hl7.org/fhirpath/N1/#tail-collection) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns a collection containing all but the first item in the input collection. Will return
        an empty collection if the input collection has no items, or only one item.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.
        """
        return ensure_list(collection[1:])


class Skip(FHIRPathFunction):
    """
    A representation of the FHIRPath [`skip()`](https://hl7.org/fhirpath/N1/#skipnum-integer-collection) function.

    Attributes:
        num (int): The number of items to skip.
    """

    def __init__(self, num: int | Literal):
        if isinstance(num, Literal):
            num = num.value
        if not isinstance(num, int):
            raise FHIRPathError("Skip() argument must be an integer number.")
        self.num = num

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns a collection containing all but the first `num` items in the input collection. Will return
        an empty collection if there are no items remaining after the indicated number of items have
        been skipped, or if the input collection is empty. If `num` is less than or equal to zero, the
        input collection is simply returned.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.
        """
        if self.num <= 0:
            return []
        return ensure_list(collection[self.num :])


class Take(FHIRPathFunction):
    """
    A representation of the FHIRPath [`take()`](https://hl7.org/fhirpath/N1/#takenum-integer-collection) function.

    Attributes:
        num (int): The number of items to take.
    """

    def __init__(self, num: int | Literal):
        if isinstance(num, Literal):
            num = num.value
        if not isinstance(num, int):
            raise FHIRPathError("Take() argument must be an integer number.")
        self.num = num

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns a collection containing the first `num` items in the input collection, or less if there
        are less than `num` items. If num is less than or equal to 0, or if the input collection
        is empty (`[]`), take returns an empty collection.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.
        """
        if self.num <= 0:
            return []
        return ensure_list(collection[: self.num])


class Intersect(FHIRPathFunction):
    """
    A representation of the FHIRPath [`intersect()`](https://hl7.org/fhirpath/N1/#intersectother-collection-collection) function.

    Attributes:
        other_collection (FHIRPathCollection): The other collection to compute the intersection with.
    """

    def __init__(self, other_collection: FHIRPath | FHIRPathCollection):
        self.other_collection = other_collection

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the set of elements that are in both collections. Duplicate items will be eliminated
        by this function. Order of items is preserved in the result of this function.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.
        """
        if isinstance(self.other_collection, FHIRPath):
            self.other_collection = self.other_collection.evaluate(
                collection, environment, create
            )
        return [item for item in collection if item in self.other_collection]


class Exclude(FHIRPathFunction):
    """
    A representation of the FHIRPath [`exclude()`](https://hl7.org/fhirpath/N1/#excludeother-collection-collection) function.

    Attributes:
        other_collection (FHIRPathCollection): The other collection to compute the exclusion with.
    """

    def __init__(self, other_collection: FHIRPath | FHIRPathCollection):
        self.other_collection = other_collection

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the set of elements that are not in the other collection. Duplicate items will not be
        eliminated by this function, and order will be preserved.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.
        """
        if isinstance(self.other_collection, FHIRPath):
            self.other_collection = self.other_collection.evaluate(
                collection, environment, create
            )
        return [item for item in collection if item not in self.other_collection]
