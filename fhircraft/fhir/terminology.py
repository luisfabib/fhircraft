"""Terminology service abstractions for FHIRcraft."""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class TerminologyService(Protocol):
    """Pluggable terminology service used by FHIRPath terminology functions."""

    def codesystem_lookup(
        self,
        *,
        code: str,
        system: str | None = None,
        version: str | None = None,
    ) -> Any:
        """
        Implements the CodeSystem/$lookup operation.

        Given a code/system, or a Coding, get additional details about the concept,
        including definition, status, designations, and properties. One of the products
        of this operation is a full decomposition of a code from a structured terminology.

        Args:
            code: The code to look up.
            system: The code system the code belongs to (optional if the code is unique across all systems).
            version: The version of the code system to look up (optional).
        """
        ...

    def validate_valueset_code(
        self,
        *,
        url: str | None = None,
        code: str | None = None,
        system: str | None = None,
        version: str | None = None,
        display: str | None = None,
    ) -> bool:
        """
        Implements the ValueSet/$validate-code operation.

        Validate that a coded value is in the set of codes allowed by a valueset.

        Args:
            url: The URL of the valueset to validate against.
            code: The code to validate.
            system: The system of the code to validate.
            version: The version of the code system or value set to validate against.
            display: The display string to validate (optional).
        """
        ...

    def validate_codesystem_code(
        self,
        *,
        url: str | None = None,
        code: str | None = None,
        version: str | None = None,
        display: str | None = None,
    ) -> bool:
        """
        Implements the CodeSystem/$validate-code operation.

        Validate that a coded value is in the set of codes allowed by a codesystem.

        Args:
            url: The URL of the codesystem to validate against.
            code: The code to validate.
            version: The version of the codesystem to validate against.
            display: The display string to validate (optional).
        """
        ...

    def codesystem_subsumes(
        self,
        codeA: str,
        codeB: str,
        system: str | None = None,
        version: str | None = None,
    ) -> bool | None:
        """
        Implements the CodeSystem/$subsumes operation.

        Determine if one code is subsumed by another within a code system.

        Args:
            codeA: The first code to compare.
            codeB: The second code to compare.
            system: The code system the codes belong to (optional if the codes are unique across all systems).
            version: The version of the code system to use for comparison (optional).

        Returns:
            True if the source code subsumes the target code, False if not, or None if unknown.
        """
        ...


__all__ = ["TerminologyService"]
