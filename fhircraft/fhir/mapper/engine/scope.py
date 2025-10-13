from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, TypeVar, Union

from pydantic import BaseModel

from fhircraft.fhir.path.engine.core import FHIRPath
from fhircraft.fhir.resources.datatypes.R5.resources.concept_map import ConceptMap
from fhircraft.fhir.resources.datatypes.R5.resources.structure_map import (
    StructureMapGroup,
)

from .exceptions import MappingError

# Type variable for generic lookups
T = TypeVar("T")


@dataclass
class MappingScope:
    """
    A scope defines the visibility and accessibility of identifiers (variables, types, etc.)
    """

    name: str
    """Name of the scope"""

    types: Dict[str, type[BaseModel]] = field(default_factory=dict)
    """Registry of available FHIR types by identifier"""

    source_instances: Dict[str, BaseModel] = field(default_factory=dict)
    """The source instances being mapped"""

    target_instances: Dict[str, BaseModel] = field(default_factory=dict)
    """The target instances being mapped"""

    concept_maps: Dict[str, ConceptMap] = field(default_factory=dict)
    """Registry of available concept maps for value transformations"""

    groups: OrderedDict[str, StructureMapGroup] = field(default_factory=OrderedDict)
    """The groups defined on this scope"""

    variables: Dict[str, FHIRPath] = field(default_factory=dict)
    """Registry of variables mapped to resolved FHIRPath expressions"""

    processing_rules: Set[str] = field(default_factory=set)
    """Set of currently processing rules"""

    parent: Optional["MappingScope"] = None
    """Parent mapping scope"""

    def define_variable(self, identifier: str, value: FHIRPath) -> None:
        """
        Defines a new variable in the current scope.

        Args:
            identifier (str): The name of the variable to define.
            value (FHIRPath): The FHIRPath instance to assign to the variable.

        Raises:
            ValueError: If the provided value is not an instance of FHIRPath.
        """
        if not isinstance(value, FHIRPath):
            raise ValueError("Variables can only be assigned to a FHIRPath instance")
        self.variables[identifier] = value

    def get_instances(self) -> Dict[str, BaseModel]:
        """
        Returns a dictionary containing all instances from the current scope, including those inherited from the parent scope (if any), as well as target and source instances.

        Returns:
            Dict[str, BaseModel]: A dictionary mapping instance names to their corresponding BaseModel objects, aggregated from the parent scope, target instances, and source instances.
        """
        return {
            **(self.parent.get_instances() if self.parent else {}),
            **self.target_instances,
            **self.source_instances,
        }

    def get_concept_map(self, identifier: str) -> ConceptMap:
        """
        Retrieve a ConceptMap by its identifier from the current scope or any parent scopes.

        Args:
            identifier (str): The unique identifier of the ConceptMap to retrieve.

        Returns:
            ConceptMap: The ConceptMap instance associated with the given identifier.

        Raises:
            MappingError: If the ConceptMap with the specified identifier is not found in the current or any parent scopes.
        """
        concept_map = self.concept_maps.get(identifier)
        if concept_map:
            return concept_map

        if self.parent:
            return self.parent.get_concept_map(identifier)

        raise MappingError(
            f"Concept map '{identifier}' not found in current or parent scopes."
        )

    def get_target_instance(self, identifier: str) -> BaseModel:
        """
        Retrieve a target instance by its identifier from the current scope or any parent scopes.

        Args:
            identifier (str): The unique identifier of the target instance to retrieve.

        Returns:
            BaseModel: The target instance associated with the given identifier.

        Raises:
            MappingError: If the target instance is not found in the current or any parent scopes.
        """
        instance = self.target_instances.get(identifier)
        if instance:
            return instance

        if self.parent:
            return self.parent.get_target_instance(identifier)

        raise MappingError(
            f"Target instance '{identifier}' not found in current or parent scopes."
        )

    def get_source_instance(self, identifier: str) -> BaseModel:
        """
        Retrieve a source instance by its identifier from the current scope or any parent scopes.

        Args:
            identifier (str): The unique identifier of the source instance to retrieve.

        Returns:
            BaseModel: The source instance associated with the given identifier.

        Raises:
            MappingError: If the source instance is not found in the current or any parent scopes.
        """
        instance = self.source_instances.get(identifier)
        if instance:
            return instance

        if self.parent:
            return self.parent.get_source_instance(identifier)

        raise MappingError(
            f"Source instance '{identifier}' not found in current or parent scopes."
        )

    def get_type(self, identifier: str) -> type[BaseModel]:
        """
        Retrieve the type associated with the given identifier from the current scope or its parent scopes.

        Args:
            identifier (str): The identifier for which to retrieve the associated type.

        Returns:
            type[BaseModel]: The type associated with the identifier.

        Raises:
            MappingError: If the identifier is not found in the current or any parent scope.
        """
        type_ = self.types.get(identifier)
        if type_:
            return type_

        if self.parent:
            return self.parent.get_type(identifier)

        raise MappingError(
            f"Type '{identifier}' not found in current or parent scopes."
        )

    def resolve_symbol(
        self, identifier: str
    ) -> Union[FHIRPath, type[BaseModel], StructureMapGroup]:
        """
        Resolves a symbol (variable, type, or group) by its identifier from the current scope or any parent scopes.

        Args:
            identifier (str): The name of the symbol to resolve.

        Returns:
            Union[FHIRPath, type[BaseModel], StructureMapGroup]: The resolved symbol, which can be a variable, a type, or a group.

        Raises:
            MappingError: If the symbol cannot be found in the current or any parent scopes.
        """
        # Check local scope first
        if identifier in self.variables:
            return self.variables[identifier]
        elif identifier in self.types:
            return self.types[identifier]
        elif identifier in self.groups:
            return self.groups[identifier]

        # Check parent scope
        if self.parent:
            try:
                return self.parent.resolve_symbol(identifier)
            except MappingError:
                pass

        raise MappingError(
            f"Symbol '{identifier}' not found in current or parent scopes."
        )

    def has_symbol(self, identifier: str) -> bool:
        """
        Checks if a symbol with the given identifier exists in the current scope.

        Args:
            identifier (str): The name of the symbol to check.

        Returns:
            bool: True if the symbol exists, False otherwise.
        """
        try:
            self.resolve_symbol(identifier)
            return True
        except MappingError:
            return False

    def has_local_symbol(self, identifier: str) -> bool:
        """
        Checks if a symbol with the given identifier exists in the current scope only.

        Args:
            identifier (str): The name of the symbol to check.

        Returns:
            bool: True if the symbol exists, False otherwise.
        """
        return (
            identifier in self.variables
            or identifier in self.types
            or identifier in self.groups
        )

    def resolve_fhirpath(self, identifier: str) -> FHIRPath:
        """
        Resolve a symbol as a FHIRPath expression.

        Args:
            identifier: The symbol identifier to resolve
        Returns:
            The resolved FHIRPath expression
        Raises:
            MappingError: If the symbol is not found or is not a FHIRPath
        """
        symbol = self.resolve_symbol(identifier)
        if not isinstance(symbol, FHIRPath):
            raise MappingError(f"Symbol '{identifier}' is not a FHIRPath expression.")
        return symbol

    def get_all_visible_symbols(
        self,
    ) -> Dict[str, Union[FHIRPath, type[BaseModel], StructureMapGroup]]:
        """
        Retrieves all visible symbols in the current scope, including those inherited from parent scopes.

        This method aggregates symbols from the parent scope (if present) and then overrides them with
        symbols defined in the current scope. The symbols include variables, types, and groups.

        Returns:
            Dict[str, Union[FHIRPath, type[BaseModel], StructureMapGroup]]:
                A dictionary mapping symbol names to their corresponding objects, representing all
                symbols visible in the current scope.
        """
        all_symbols = {}

        # Start with parent symbols (if any)
        if self.parent:
            all_symbols.update(self.parent.get_all_visible_symbols())

        # Override with local symbols
        all_symbols.update(self.variables)
        all_symbols.update(self.types)
        all_symbols.update(self.groups)

        return all_symbols

    def get_scope_path(self) -> List[str]:
        """
        Returns the hierarchical path of scope names from the root to the current scope as a list of strings.

        If the current scope has a parent, the method recursively retrieves the parent's scope path and appends the current scope's name.
        If there is no parent, returns a list containing only the current scope's name.

        Returns:
            List[str]: The list of scope names representing the path from the root to the current scope.
        """
        if self.parent:
            return self.parent.get_scope_path() + [self.name]
        return [self.name]

    def get_scope_depth(self) -> int:
        """
        Returns the depth of the current scope within the scope hierarchy.

        Traverses up the parent scopes recursively, incrementing the depth count
        for each parent until the root scope is reached.

        Returns:
            int: The depth of the current scope, where the root scope has a depth of 0.
        """
        if self.parent:
            return self.parent.get_scope_depth() + 1
        return 0

    def create_child_scope(self, name: str) -> "MappingScope":
        """
        Creates and returns a new child MappingScope with the specified name, setting the current scope as its parent.

        Args:
            name (str): The name of the child scope to be created.

        Returns:
            MappingScope: A new instance of MappingScope with the given name and the current scope as its parent.
        """
        return MappingScope(name=name, parent=self)

    def is_processing_rule(self, rule_name: str) -> bool:
        """
        Check if a given rule name is present in the list of processing rules.

        Args:
            rule_name (str): The name of the rule to check.

        Returns:
            bool: True if the rule is in the processing rules, False otherwise.
        """
        return rule_name in self.processing_rules

    def start_processing_rule(self, rule_name: str) -> None:
        """
        Marks the beginning of processing for a specific rule by adding its name to the set of currently processing rules.

        Args:
            rule_name (str): The name of the rule to start processing.
        """
        self.processing_rules.add(rule_name)

    def finish_processing_rule(self, rule_name: str) -> None:
        """
        Marks the specified rule as finished by removing it from the set of currently processing rules.

        Args:
            rule_name (str): The name of the rule to mark as finished.
        """
        self.processing_rules.discard(rule_name)

    def __str__(self) -> str:
        parts = []
        if self.variables:
            var_names = list(self.variables.keys())
            if len(var_names) <= 3:
                parts.append(f"variables: {var_names}")
            else:
                parts.append(f"variables: {var_names[:3]}... ({len(var_names)} total)")

        if self.types:
            type_names = list(self.types.keys())
            if len(type_names) <= 3:
                parts.append(f"types: {type_names}")
            else:
                parts.append(f"types: {type_names[:3]}... ({len(type_names)} total)")

        if self.groups:
            parts.append(f"groups: {len(self.groups)}")

        if self.source_instances:
            parts.append(f"sources: {len(self.source_instances)}")

        if self.target_instances:
            parts.append(f"targets: {len(self.target_instances)}")

        if self.concept_maps:
            parts.append(f"concept_maps: {len(self.concept_maps)}")

        content = ", ".join(parts) if parts else "empty"
        return f"MappingScope({self.name}, {content})"

    def __repr__(self) -> str:
        return (
            f"MappingScope("
            f"name='{self.name}', "
            f"parent={self.parent.name if self.parent else None}, "
            f"depth={self.get_scope_depth()}, "
            f"variables={list(self.variables.keys())}, "
            f"types={list(self.types.keys())}, "
            f"groups={list(self.groups.keys())}"
            f")"
        )
