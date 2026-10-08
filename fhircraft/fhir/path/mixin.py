from typing import Any, List

from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem
from fhircraft.fhir.path.patch import FHIRPatch
from fhircraft.fhir.path.utils import parse_fhirpath


class FHIRPathMixin:
    """
    Adds a FHIRPath interface to a model.

    - ``model.query(expression)`` returns the matching values as a list.
    - ``model.patch.<operation>(expression, ...)`` modifies the model through
      FHIRPath-addressed patch operations (see `FHIRPatch`).
    """

    def _generate_fhirpath_environment(self) -> dict:
        environment = {}
        if release := getattr(self, "_fhir_release", None):
            environment["%fhirRelease"] = FHIRPathCollectionItem.wrap(release)
        return environment

    def query(self, expression: str, environment: dict | None = None) -> List[Any]:
        """
        Evaluate a FHIRPath expression against this model.

        Args:
            expression: FHIRPath expression to evaluate.
            environment: Optional environment variables (e.g. ``%name``) for the evaluation.

        Returns:
            The values matched by the expression; empty list if there are none.
        """
        collection = parse_fhirpath(expression)._evaluate_wrapped(
            self, {**self._generate_fhirpath_environment(), **(environment or {})}
        )
        return [item.value for item in collection]

    @property
    def patch(self) -> FHIRPatch:
        """FHIRPath-addressed patch operations: add, insert, replace, delete, move."""
        return FHIRPatch(self)
