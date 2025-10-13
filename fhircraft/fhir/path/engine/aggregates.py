"""
FHIRPath supports a general-purpose aggregate function to enable the calculation of aggregates such as sum, min, and max to be expressed
"""

from typing import Any

import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathFunction,
)
from fhircraft.fhir.path.utils import get_expression_context
from fhircraft.utils import ensure_list


class Aggregate(FHIRPathFunction):
    """
    A representation of the FHIRPath [`aggregate()`](https://hl7.org/fhirpath/N1/#aggregateaggregator-expression-init-value-value) function.

    Args:
        expression (FHIRPath): The aggregator expression to be evaluated for each element of the input collection.
        init (Optional[Any]): Initial value for the $total variable, defaults to an empty collection if not provided.
    """

    def __init__(
        self,
        expression: FHIRPath,
        init: Any | None = None,
    ):
        self.expression = expression
        if init is None:
            self.init = None
        else:
            init = ensure_list(init)
            if len(init) != 1:
                raise ValueError("Aggregation init must be a single value, not a list")
            self.init = FHIRPathCollectionItem.wrap(init[0]).value

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Performs general-purpose aggregation by evaluating the aggregator expression for each element of the input collection.
        Within this expression, the standard iteration variables of $this and $index can be accessed, but also a $total aggregation variable.

        The value of the $total variable is set to init, or empty ({ }) if no init value is supplied, and is set to the result of
        the aggregator expression after every iteration.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.
        """
        context = environment.copy()
        for index, item in enumerate(collection):
            # Set up the environment for evaluating the expression
            context = get_expression_context(context, item, index)
            context["$total"] = context.get("$total", self.init if self.init else [])
            # Evaluate the expression
            result = self.expression.evaluate([item], context, create=create)
            # Update the total variable for the next iteration
            context["$total"] = result[0].value
        result = context.get("$total")
        if result is None:
            return []
        return [FHIRPathCollectionItem.wrap(result)]
