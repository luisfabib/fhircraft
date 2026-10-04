"""FHIRPath-addressed patch operations (``add``, ``insert``, ``replace``, ``delete``, ``move``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from fhircraft.exceptions import FHIRPathEvaluationError
from fhircraft.fhir.path.collection import FHIRPathCollection
from fhircraft.fhir.path.utils import parse_fhirpath

if TYPE_CHECKING:
    from fhircraft.fhir.path.mixin import FHIRPathMixin

__all__ = ["FHIRPatch"]


class FHIRPatch:
    """Patch operations on a model, addressed by FHIRPath expressions.

    Reached through ``<model>.patch``.  Every operation resolves the expression
    to writable locations, so locations that do not exist yet (e.g.
    ``Patient.name[0].given``) can be added to.  Operations are atomic: if one
    fails, the model is restored to its previous state.

    Example:
        >>> patient.patch.add("Patient.name", {"family": "Doe"})  # doctest: +SKIP
        >>> patient.patch.replace("Patient.gender", "female")  # doctest: +SKIP
        >>> patient.patch.delete("Patient.telecom.where(system='fax')")  # doctest: +SKIP
    """

    __slots__ = ("_model",)

    def __init__(self, model: "FHIRPathMixin") -> None:
        self._model = model

    def _apply(
        self,
        expression: str,
        environment: dict | None,
        operation: Callable[[FHIRPathCollection], None],
        *,
        must_exist: bool = False,
    ) -> None:
        collection = parse_fhirpath(expression)._evaluate_wrapped(
            self._model,
            {**self._model._generate_fhirpath_environment(), **(environment or {})},
        )
        if must_exist and not collection:
            raise FHIRPathEvaluationError(
                f"Expression '{expression}' does not match any element"
            )
        snapshot = collection.snapshot() if collection.targets else None
        try:
            operation(collection)
        except Exception:
            if snapshot is not None:
                collection.restore(snapshot)
            raise

    def add(self, expression: str, value: Any, environment: dict | None = None) -> None:
        """Add *value* at the location: appended for repeating elements, assigned otherwise.

        The location need not exist yet; missing parents are created.
        """
        self._apply(expression, environment, lambda c: c.add(value))

    def insert(
        self, expression: str, value: Any, index: int, environment: dict | None = None
    ) -> None:
        """Insert *value* at position *index* of the repeating element addressed."""
        self._apply(expression, environment, lambda c: c.insert(value, index))

    def replace(
        self, expression: str, value: Any, environment: dict | None = None
    ) -> None:
        """Replace the value at every matched location.

        Raises:
            FHIRPathEvaluationError: If the expression matches nothing.
        """
        self._apply(expression, environment, lambda c: c.set(value), must_exist=True)

    def delete(self, expression: str, environment: dict | None = None) -> None:
        """Delete every matched element.

        Raises:
            FHIRPathEvaluationError: If the expression matches nothing, or an
                element is required.
        """
        self._apply(expression, environment, lambda c: c.delete(), must_exist=True)

    def move(
        self,
        expression: str,
        source: int,
        destination: int,
        environment: dict | None = None,
    ) -> None:
        """Move the entry at *source* to *destination* within the repeating element addressed."""
        self._apply(expression, environment, lambda c: c.move(source, destination))
