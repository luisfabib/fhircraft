"""The filtering module contains the object representations of the filtering-category FHIRPath functions."""

from typing import List, Optional, Union

from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathFunction,
    This,
)
from fhircraft.fhir.path.engine.types import As
from fhircraft.fhir.path.utils import get_expression_context
from fhircraft.utils import ensure_list


class Where(FHIRPathFunction):
    """
    Representation of the FHIRPath [`where()`](http://hl7.org/fhirpath/N1/#wherecriteria-expression-collection) function.

    Attributes:
        expression (FHIRPath): Expression to evaluate for each collection item.
    """

    def __init__(self, expression: FHIRPath):
        self.expression = expression

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns a collection containing only those elements in the input collection for which
        the stated criteria expression evaluates to `True`. Elements for which the expression
        evaluates to false or empty (`[]`) are not included in the result.
        If the input collection is empty (`[]`), the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.
        """
        collection = ensure_list(collection)
        expression_collection = [
            self.expression.evaluate(
                [item], get_expression_context(environment, item, index), create
            )
            for index, item in enumerate(collection)
        ]
        checks = [
            bool(collection[0].value) if len(collection) > 0 else False
            for collection in expression_collection
        ]
        return [item for item, check in zip(collection, checks) if check]

    def __str__(self):
        return f"{self.__class__.__name__.lower()}({self.expression.__str__()})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.expression.__repr__()})"

    def __eq__(self, other):
        return isinstance(other, Where) and other.expression == self.expression

    def __hash__(self):
        return hash((self.expression))


class Select(FHIRPathFunction):
    """
    Representation of the FHIRPath [`select()`](http://hl7.org/fhirpath/N1/#selectprojection-expression-collection) function.

    Attributes:
        projection (FHIRPath): Expression to evaluate for each collection item.
    """

    def __init__(self, projection: FHIRPath):
        self.projection = projection

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Evaluates the projection expression for each item in the input collection. The result of each
        evaluation is added to the output collection. If the evaluation results in a collection with
        multiple items, all items are added to the output collection (collections resulting from
        evaluation of projection are flattened). This means that if the evaluation for an element
        results in the empty collection (`[]`), no element is added to the result, and that if the
        input collection is empty (`[]`), the result is empty as well.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.
        """
        collection = ensure_list(collection)
        return [
            projected_item
            for index, item in enumerate(collection)
            for projected_item in ensure_list(
                self.projection.evaluate(
                    [item], get_expression_context(environment, item, index), create
                )
            )
        ]

    def __str__(self):
        return f"{self.__class__.__name__.lower()}({self.projection.__str__()})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.projection.__repr__()})"

    def __eq__(self, other):
        return isinstance(other, Select) and other.projection == self.projection

    def __hash__(self):
        return hash((self.projection))


class Repeat(FHIRPathFunction):
    """
    Representation of the FHIRPath [`repeat()`](http://hl7.org/fhirpath/N1/#repeatprojection-expression-collection) function.

    Attributes:
        projection (FHIRPath): Expression to evaluate for each collection item.
    """

    def __init__(self, projection: FHIRPath):
        self.projection = projection

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        A version of select that will repeat the projection and add it to the output collection, as
        long as the projection yields new items (as determined by the = (Equals) (=) operator).

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.
        """

        def project_recursively(input_collection):
            output_collection = []
            for index, item in enumerate(input_collection):
                new_collection = self.projection.evaluate(
                    [item], get_expression_context(environment, item, index), create
                )
                output_collection.extend(new_collection)
                if len(new_collection) > 0:
                    output_collection.extend(project_recursively(new_collection))
            return output_collection

        return project_recursively(collection)

    def __str__(self):
        return f"{self.__class__.__name__.lower()}({self.projection.__str__()})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.projection.__repr__()})"

    def __eq__(self, other):
        return isinstance(other, Repeat) and other.projection == self.projection

    def __hash__(self):
        return hash((self.projection))


class OfType(FHIRPathFunction):
    """
    Representation of the FHIRPath [`ofType()`](http://hl7.org/fhirpath/N1/#oftypetype-type-specifier-collection) function.

    Attributes:
        type (class): Type class
    """

    def __init__(self, _type: str):
        self.type = _type

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns a collection that contains all items in the input collection that are of the given type
        or a subclass thereof. If the input collection is empty (`[]`), the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection): The output collection.
        """
        collection = ensure_list(collection)
        filtered_collection = []
        for item in collection:
            filtered_collection.extend(
                As(This(), self.type).evaluate([item], environment, create)
            )
        return filtered_collection

    def __str__(self):
        return f"ofType({self.type})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.type.__repr__()})"

    def __eq__(self, other):
        return isinstance(other, OfType) and other.type == self.type

    def __hash__(self):
        return hash((self.type))
