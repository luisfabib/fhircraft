
from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
)


class This(FHIRPath):
    """
    A class representation of the FHIRPath `$this` operator used to represent
    the item from the input collection currently under evaluation.
    """

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Simply returns the input collection.

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): The output collection.
        """
        return environment.get("this", collection)

    def __str__(self):
        return "$this"

    def __repr__(self):
        return "This()"

    def __eq__(self, other):
        return isinstance(other, This)

    def __hash__(self):
        return hash("this")


class CollectionIndex(FHIRPath):
    """
    A class representation of the FHIRPath `$index` operator used to represent
    the index of an item in the input collection currently under evaluation.
    """

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the index of each item in the input collection.

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): A list of FHIRPathCollectionItem instances after evaluation.
        """
        return [FHIRPathCollectionItem.wrap(index) for index, _ in enumerate(collection)]

    def __str__(self):
        return "$index"

    def __repr__(self):
        return "Index()"

    def __eq__(self, other):
        return isinstance(other, CollectionIndex)

    def __hash__(self):
        return hash("index")
