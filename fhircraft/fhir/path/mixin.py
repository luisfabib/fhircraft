from typing import TYPE_CHECKING, Any, List, ClassVar
from fhircraft.fhir.path.utils import parse_fhirpath
from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem

if TYPE_CHECKING:
    from fhircraft.fhir.path.parser import FHIRPathParser


class FHIRPathMixin:
    """
    Enhanced mixin class to incorporate a comprehensive FHIRPath interface to the child class.

    This mixin provides convenient methods for working with FHIRPath expressions directly
    on FHIR resource instances, leveraging the enhanced FHIRPath interface.
    """

    def _generate_fhirpath_environment(self):
        environment = {}
        if release := getattr(self, "_fhir_release", None):
            environment["%fhirRelease"] = FHIRPathCollectionItem.wrap(release)
        return environment


    # Enhanced interface methods
    def fhirpath_values(
        self, expression: str, environment: dict | None = None
    ) -> List[Any]:
        """
        Evaluates a FHIRPath expression and returns all matching values as a list.

        Args:
            expression (str): FHIRPath expression to evaluate

        Returns:
            List[Any]: A list of all values that match the FHIRPath expression.
                      Returns an empty list if no matches are found.
            environment (dict | None): Optional environment variables for evaluation
        """
        return parse_fhirpath(expression).values(
            self,
            environment={
                **self._generate_fhirpath_environment(),
                **(environment or {}),
            },
        )

    def fhirpath_single(
        self, expression: str, default: Any = None, environment: dict | None = None
    ) -> Any:
        """
        Evaluates a FHIRPath expression and returns exactly one value.

        Args:
            expression (str): FHIRPath expression to evaluate
            default: The default value to return if no matches are found
            environment (dict | None): Optional environment variables for evaluation

        Returns:
            Any: The single matching value

        Raises:
            FHIRPathRuntimeError: If more than one value is found
        """
        return parse_fhirpath(expression).single(
            self,
            default=default,
            environment={
                **self._generate_fhirpath_environment(),
                **(environment or {}),
            },
        )

    def fhirpath_first(
        self, expression: str, default: Any = None, environment: dict | None = None
    ) -> Any:
        """
        Evaluates a FHIRPath expression and returns the first matching value.

        Args:
            expression (str): FHIRPath expression to evaluate
            default: The default value to return if no matches are found
            environment (dict | None): Optional environment variables for evaluation

        Returns:
            Any: The first matching value, or the default if no matches
        """
        return parse_fhirpath(expression).first(
            self,
            default=default,
            environment={
                **self._generate_fhirpath_environment(),
                **(environment or {}),
            },
        )

    def fhirpath_last(
        self, expression: str, default: Any = None, environment: dict | None = None
    ) -> Any:
        """
        Evaluates a FHIRPath expression and returns the last matching value.

        Args:
            expression (str): FHIRPath expression to evaluate
            default: The default value to return if no matches are found
            environment (dict | None): Optional environment variables for evaluation

        Returns:
            Any: The last matching value, or the default if no matches
        """
        return parse_fhirpath(expression).last(
            self,
            default=default,
            environment={
                **self._generate_fhirpath_environment(),
                **(environment or {}),
            },
        )

    def fhirpath_exists(self, expression: str, environment: dict | None = None) -> bool:
        """
        Checks if a FHIRPath expression matches any values.

        Args:
            expression (str): FHIRPath expression to evaluate
            environment (dict | None): Optional environment variables for evaluation

        Returns:
            bool: True if at least one value matches, False otherwise
        """
        return parse_fhirpath(expression).exists(
            self,
            environment={
                **self._generate_fhirpath_environment(),
                **(environment or {}),
            },
        )

    def fhirpath_is_empty(
        self, expression: str, environment: dict | None = None
    ) -> bool:
        """
        Checks if a FHIRPath expression matches no values.

        Args:
            expression (str): FHIRPath expression to evaluate
            environment (dict | None): Optional environment variables for evaluation

        Returns:
            bool: True if no values match, False otherwise
        """
        return parse_fhirpath(expression).is_empty(
            self,
            environment={
                **self._generate_fhirpath_environment(),
                **(environment or {}),
            },
        )

    def fhirpath_count(self, expression: str, environment: dict | None = None) -> int:
        """
        Returns the number of values that match a FHIRPath expression.

        Args:
            expression (str): FHIRPath expression to evaluate
            environment (dict | None): Optional environment variables for evaluation

        Returns:
            int: The number of matching values
        """
        return parse_fhirpath(expression).count(
            self,
            environment={
                **self._generate_fhirpath_environment(),
                **(environment or {}),
            },
        )

    def fhirpath_update_values(
        self, expression: str, value: Any, environment: dict | None = None
    ) -> None:
        """
        Evaluates a FHIRPath expression and sets all matching locations to the given value.

        Args:
            expression (str): FHIRPath expression to evaluate
            value (Any): The value to set at all matching locations
            environment (dict | None): Optional environment variables for evaluation

        Raises:
            RuntimeError: If no matching locations are found or if locations cannot be set
        """
        parse_fhirpath(expression).update_values(
            self,
            value,
            environment={
                **self._generate_fhirpath_environment(),
                **(environment or {}),
            },
        )

    def fhirpath_update_single(
        self, expression: str, value: Any, environment: dict | None = None
    ) -> None:
        """
        Evaluates a FHIRPath expression and sets exactly one matching location to the given value.

        Args:
            expression (str): FHIRPath expression to evaluate
            value (Any): The value to set at the matching location
            environment (dict | None): Optional environment variables for evaluation

        Raises:
            FHIRPathException: If zero or more than one matching locations are found
            RuntimeError: If the location cannot be set
        """
        parse_fhirpath(expression).update_single(
            self,
            value,
            environment={
                **self._generate_fhirpath_environment(),
                **(environment or {}),
            },
        )
