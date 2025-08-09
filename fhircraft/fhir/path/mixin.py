from typing import Any, List, Optional, Union

from fhircraft.fhir.path import FhirPathParser
from fhircraft.fhir.path.utils import import_fhirpath_engine


class FHIRPathMixin:
    """
    Mixin class to incorporate a simple FHIRPath interface to the child class.
    """

    @property
    def fhirpath(self) -> "FhirPathParser":
        """
        Initialized FHIRPath engine instance
        """
        return import_fhirpath_engine()

    def get_fhirpath(self, expression: str) -> Union[None, Any, List[Any]]:
        """
        Evaluates and retrieves the value(s) of a FHIRPath expression

        Args:
            expression (str): FHIRPath expression to evaluate

        Returns:
            (Union[NoneType,Any, List[Any]): The extracted value(s), or None if no values are found.
        """
        # Evaluate the FHIRPath expression
        return self.fhirpath.parse(expression).evaluate_for(self)

    def replace_fhirpath(self, expression: str, new_value: Any) -> None:
        """
        Evaluates and replaces the value given by a FHIRPath expression

        Args:
            expression (str): FHIRPath expression to evaluate
        """
        # Evaluate the FHIRPath expression
        self.fhirpath.parse(expression).evaluate_and_replace(self, new_value)
