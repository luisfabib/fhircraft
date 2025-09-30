
from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
)

class Root(FHIRPath):
    """
    A class representing the root of a FHIRPath, i.e. the top-most segment of the FHIRPath
    whose collection has no parent associated.
    """

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Evaluate the collection of top-most resources in the input collection.

        Args:
            collection (Collection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (Collection): A list of FHIRPathCollectionItem instances after evaluation.
        """
        return [
            (
                FHIRPathCollectionItem(item.value, parent=None, path=Root())
                if item.parent is None
                else Root().evaluate([item.parent])[0]
            )
            for item in collection
        ]

    def __str__(self):
        return "$"

    def __repr__(self):
        return "Root()"

    def __eq__(self, other):
        return isinstance(other, Root)

    def __hash__(self):
        return hash("$rootResource")


class Parent(FHIRPath):
    """
    A class representing the parent of a FHIRPath
    """

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Evaluate the collection of parent resources in the input collection.

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.
        """
        return [item.parent for item in collection if item.parent is not None]

    def __str__(self):
        return "$"

    def __repr__(self):
        return "Parent()"

    def __eq__(self, other):
        return isinstance(other, Parent)

    def __hash__(self):
        return hash("$resource")


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
