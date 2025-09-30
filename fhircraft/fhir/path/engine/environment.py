
from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    This,
)

class ContextualVariable(FHIRPath):
    """
    A base class for FHIRPath contextual variables such as `$this`, `$index`, and `$total`.
    """
    variable: str

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Evaluates the contextual variable within the given environment.

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): A list of FHIRPathCollectionItem instances after evaluation.
        """
        if self.variable not in environment:
            raise ValueError(f"The {self.variable} operator is not defined within the current context.")
        value = environment[self.variable]
        if value is None or value == []:
            return []
        return [FHIRPathCollectionItem.wrap(value)]

    def __str__(self):
        return self.variable

    def __repr__(self):
        return self.__class__.__name__ + "()"

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return hash(self.variable)
    
class ContextualThis(ContextualVariable):
    """
    A class representation of the FHIRPath `$this` operator used to represent
    the item from the input collection currently under evaluation.
    """
    variable = "$this"

    def evaluate(
        self,  collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Evaluates the contextual variable within the given environment. For `$this`, if the variable is not defined in the current context
        it returns the current collection being evaluated (for compatibility with the FHIR restricted subset where `$this` can refer to
        any element that has focus).

        Args:
            collection (FHIRPathCollection): The collection of items to be evaluated.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            collection (FHIRPathCollection): A list of FHIRPathCollectionItem instances after evaluation.
        """
        if self.variable not in environment:
            return collection
        return [FHIRPathCollectionItem.wrap(environment[self.variable])]

class ContextualIndex(ContextualVariable):
    """
    A class representation of the FHIRPath `$index` operator used to represent
    the index of an item in the input collection currently under evaluation.
    """
    variable = "$index"

class ContextualTotal(ContextualVariable):
    """
    A class representation of the FHIRPath `$total` operator used to represent
    an aggregated value over a collection within a context.
    """
    variable = "$total"