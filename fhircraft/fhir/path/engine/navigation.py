"""The tree navigation module contains the object representations of the tree-navigation category FHIRPath functions."""

from pydantic import BaseModel

from fhircraft.fhir.path.engine.core import (
    Element,
    FHIRPathCollection,
    FHIRPathFunction,
)
from fhircraft.fhir.path.engine.filtering import Repeat


class Children(FHIRPathFunction):
    """
    Representation of the FHIRPath [`children()`](https://hl7.org/fhirpath/N1/#children-collection) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns a collection with all immediate child nodes of all items in the input collection.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.
        """
        children_collection = []
        for item in collection:
            if isinstance(item.value, BaseModel):
                fields = item.value.__class__.model_fields
            elif isinstance(item.value, dict):
                fields = list(item.value.keys())
            else:
                fields = []
            for field in fields:
                children_collection.extend(
                    Element(field).evaluate([item], environment, create)
                )
        return children_collection


class Descendants(FHIRPathFunction):
    """
    Representation of the FHIRPath [`descendants()`](https://hl7.org/fhirpath/N1/#descendants-collection) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns a collection with all descendant nodes of all items in the input collection. The result does not include
        the nodes in the input collection themselves.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Note:
            This function is a shorthand for `repeat(children())`.
        """
        return Repeat(Children()).evaluate(collection, environment, create)
