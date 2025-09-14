from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, TypeVar, Union

from pydantic import BaseModel

from fhircraft.fhir.mapper.structures.ConceptMap import ConceptMap
from fhircraft.fhir.mapper.structures.StructureMap import StructureMapGroup
from fhircraft.fhir.path.engine.core import FHIRPath

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
        """Define a new variable in this scope"""
        if not isinstance(value, FHIRPath):
            raise ValueError("Variables can only be assigned to a FHIRPath instance")
        self.variables[identifier] = value

    def get_instances(self) -> Dict[str, BaseModel]:
        return {
            **(self.parent.get_instances() if self.parent else {}),
            **self.target_instances,
            **self.source_instances,
        }

    def get_concept_map(self, identifier: str) -> ConceptMap:
        """Get a concept map by its identifier, searching parent scopes if needed"""
        concept_map = self.concept_maps.get(identifier)
        if concept_map:
            return concept_map

        if self.parent:
            return self.parent.get_concept_map(identifier)

        raise MappingError(
            f"Concept map '{identifier}' not found in current or parent scopes."
        )

    def get_target_instance(self, identifier: str) -> BaseModel:
        """Get a target instance by its identifier, searching parent scopes if needed"""
        instance = self.target_instances.get(identifier)
        if instance:
            return instance

        if self.parent:
            return self.parent.get_target_instance(identifier)

        raise MappingError(
            f"Target instance '{identifier}' not found in current or parent scopes."
        )

    def get_source_instance(self, identifier: str) -> BaseModel:
        """Get a source instance by its identifier, searching parent scopes if needed"""
        instance = self.source_instances.get(identifier)
        if instance:
            return instance

        if self.parent:
            return self.parent.get_source_instance(identifier)

        raise MappingError(
            f"Source instance '{identifier}' not found in current or parent scopes."
        )

    def get_type(self, identifier: str) -> type[BaseModel]:
        """Get a type by its identifier, searching parent scopes if needed"""
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
        Resolve a symbol (variable, type, or group) by identifier.

        Searches in the following order:
        1. Local variables
        2. Local types
        3. Local groups
        4. Parent scope (recursively)

        Args:
            identifier: The symbol identifier to resolve

        Returns:
            The resolved symbol

        Raises:
            MappingError: If the symbol is not found in any scope
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
        """Check if a symbol exists in this scope or any parent scope"""
        try:
            self.resolve_symbol(identifier)
            return True
        except MappingError:
            return False

    def has_local_symbol(self, identifier: str) -> bool:
        """Check if a symbol exists in the current scope only"""
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
        Get all symbols visible from this scope, including inherited symbols.

        Child scope symbols override parent scope symbols with the same identifier.

        Returns:
            Dictionary mapping identifiers to their resolved symbols
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
        """Get the hierarchical path from root scope to this scope"""
        if self.parent:
            return self.parent.get_scope_path() + [self.name]
        return [self.name]

    def get_scope_depth(self) -> int:
        """Get the depth of this scope in the hierarchy (root = 0)"""
        if self.parent:
            return self.parent.get_scope_depth() + 1
        return 0

    def create_child_scope(self, name: str) -> "MappingScope":
        """Create a new child scope with this scope as parent"""
        return MappingScope(name=name, parent=self)

    def is_processing_rule(self, rule_name: str) -> bool:
        """Check if a rule is currently being processed (cycle detection)."""
        return rule_name in self.processing_rules

    def start_processing_rule(self, rule_name: str) -> None:
        """Mark a rule as being processed."""
        self.processing_rules.add(rule_name)

    def finish_processing_rule(self, rule_name: str) -> None:
        """Mark a rule as finished processing."""
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
