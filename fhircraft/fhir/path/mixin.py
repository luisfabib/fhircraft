from typing import TYPE_CHECKING, Any, List

from fhircraft.fhir.path.utils import import_fhirpath_engine

if TYPE_CHECKING:
    from fhircraft.fhir.path.parser import FhirPathParser


class FHIRPathMixin:
    """
    Enhanced mixin class to incorporate a comprehensive FHIRPath interface to the child class.

    This mixin provides convenient methods for working with FHIRPath expressions directly
    on FHIR resource instances, leveraging the enhanced FHIRPath interface.
    """

    @property
    def fhirpath(self) -> "FhirPathParser":
        """
        Initialized FHIRPath engine instance
        """
        return import_fhirpath_engine()

    # Enhanced interface methods
    def fhirpath_values(self, expression: str) -> List[Any]:
        """
        Evaluates a FHIRPath expression and returns all matching values as a list.

        Args:
            expression (str): FHIRPath expression to evaluate

        Returns:
            List[Any]: A list of all values that match the FHIRPath expression.
                      Returns an empty list if no matches are found.
        """
        return self.fhirpath.parse(expression).values(self)

    def fhirpath_single(self, expression: str, default: Any = None) -> Any:
        """
        Evaluates a FHIRPath expression and returns exactly one value.

        Args:
            expression (str): FHIRPath expression to evaluate
            default: The default value to return if no matches are found

        Returns:
            Any: The single matching value

        Raises:
            FHIRPathRuntimeError: If more than one value is found
        """
        return self.fhirpath.parse(expression).single(self, default=default)

    def fhirpath_first(self, expression: str, default: Any = None) -> Any:
        """
        Evaluates a FHIRPath expression and returns the first matching value.

        Args:
            expression (str): FHIRPath expression to evaluate
            default: The default value to return if no matches are found

        Returns:
            Any: The first matching value, or the default if no matches
        """
        return self.fhirpath.parse(expression).first(self, default=default)

    def fhirpath_last(self, expression: str, default: Any = None) -> Any:
        """
        Evaluates a FHIRPath expression and returns the last matching value.

        Args:
            expression (str): FHIRPath expression to evaluate
            default: The default value to return if no matches are found

        Returns:
            Any: The last matching value, or the default if no matches
        """
        return self.fhirpath.parse(expression).last(self, default=default)

    def fhirpath_exists(self, expression: str) -> bool:
        """
        Checks if a FHIRPath expression matches any values.

        Args:
            expression (str): FHIRPath expression to evaluate

        Returns:
            bool: True if at least one value matches, False otherwise
        """
        return self.fhirpath.parse(expression).exists(self)

    def fhirpath_is_empty(self, expression: str) -> bool:
        """
        Checks if a FHIRPath expression matches no values.

        Args:
            expression (str): FHIRPath expression to evaluate

        Returns:
            bool: True if no values match, False otherwise
        """
        return self.fhirpath.parse(expression).is_empty(self)

    def fhirpath_count(self, expression: str) -> int:
        """
        Returns the number of values that match a FHIRPath expression.

        Args:
            expression (str): FHIRPath expression to evaluate

        Returns:
            int: The number of matching values
        """
        return self.fhirpath.parse(expression).count(self)

    def fhirpath_update_values(self, expression: str, value: Any) -> None:
        """
        Evaluates a FHIRPath expression and sets all matching locations to the given value.

        Args:
            expression (str): FHIRPath expression to evaluate
            value (Any): The value to set at all matching locations

        Raises:
            RuntimeError: If no matching locations are found or if locations cannot be set
        """
        self.fhirpath.parse(expression).update_values(self, value)

    def fhirpath_update_single(self, expression: str, value: Any) -> None:
        """
        Evaluates a FHIRPath expression and sets exactly one matching location to the given value.

        Args:
            expression (str): FHIRPath expression to evaluate
            value (Any): The value to set at the matching location

        Raises:
            FHIRPathError: If zero or more than one matching locations are found
            RuntimeError: If the location cannot be set
        """
        self.fhirpath.parse(expression).update_single(self, value)
