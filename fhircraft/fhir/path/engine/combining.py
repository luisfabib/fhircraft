"""The filtering module contains the object representations of the combining-category FHIRPath functions."""

from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathFunction,
)
from fhircraft.utils import ensure_list


class Union(FHIRPathFunction):
    """
    A representation of the FHIRPath [`union()`](https://hl7.org/fhirpath/N1/#unionother-collection) function.

    Attributes:
        other_collection (FHIRPathCollection): The other collection to combine with.
    """

    def __init__(self, other_collection: FHIRPath | FHIRPathCollection):
        self.other_collection = other_collection

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Merge the two collections into a single collection, eliminating any duplicate values.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.
        """
        if isinstance(self.other_collection, FHIRPath):
            self.other_collection = self.other_collection.evaluate(
                collection, environment, create
            )
        return [
            FHIRPathCollectionItem.wrap(item)
            for item in sorted(
                list(set(collection) | set(self.other_collection)),
                key=lambda item: item.value,
            )
        ]


class Combine(FHIRPathFunction):
    """
    A representation of the FHIRPath [`combine()`](https://hl7.org/fhirpath/N1/#combineother-collection-collection) function.

    Attributes:
        other_collection (FHIRPathCollection): The other collection to combine with.
    """

    def __init__(self, other_collection: FHIRPath | FHIRPathCollection):
        self.other_collection = other_collection

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Merge the input and other collections into a single collection without eliminating duplicate
        values. Combining an empty collection with a non-empty collection will return the non-empty
        collection.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.
        """
        if isinstance(self.other_collection, FHIRPath):
            self.other_collection = self.other_collection.evaluate(
                collection, environment, create
            )
        return collection + self.other_collection
