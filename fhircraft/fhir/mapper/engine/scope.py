from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel

from fhircraft.fhir.mapper.structures.ConceptMap import ConceptMap
from fhircraft.fhir.mapper.structures.StructureMap import StructureMapGroup
from fhircraft.fhir.path.engine.core import FHIRPath

from .exceptions import MappingError


@dataclass
class MappingScope:
    """
    A scope defines the visibility and accessibility of identifiers (variables, types, etc.)
    """

    name: str
    """Name of the scope"""

    types: Dict[str, type[BaseModel]] = field(default_factory=dict)
    """Mapping of types"""

    source_instances: Dict[str, BaseModel] = field(default_factory=dict)
    """The source instances being mapped"""

    target_instances: Dict[str, BaseModel] = field(default_factory=dict)
    """The target instances being mapped"""

    concept_maps: Dict[str, ConceptMap] = field(default_factory=dict)

    groups: OrderedDict[str, StructureMapGroup] = field(default_factory=OrderedDict)
    """The groups defined on this scope"""

    variables: Dict[str, FHIRPath] = field(default_factory=dict)
    """Mapping variables names to resolved FHIRPaths"""

    processing_rules: Set[str] = field(default_factory=set)
    """Set of currently processing rules"""

    parent: Optional["MappingScope"] = None
    """Parent mapping scope"""

    def define(self, variable: str, value: FHIRPath) -> None:
        """Define a new variable in this scope"""
        if not isinstance(value, FHIRPath):
            raise ValueError("Variables can only be assigned to a FHIRPath instance")
        self.variables[variable] = value

    def get_instances(self) -> Dict[str, BaseModel]:
        return {
            **(self.parent.get_instances() if self.parent else {}),
            **self.target_instances,
            **self.source_instances,
        }

    def get_concept_map(self, identifier: str) -> ConceptMap:
        """Get a concept map by its identifier"""
        concept_map = self.concept_maps.get(identifier) or (
            self.parent.get_concept_map(identifier) if self.parent else None
        )
        if not concept_map:
            raise MappingError(
                f"Concept map '{identifier}' not found in current or parent scopes."
            )
        return concept_map

    def get_target_instance(self, identifier: str) -> BaseModel:
        """Get a target instance by its identifier"""
        instance = self.target_instances.get(identifier) or (
            self.parent.get_target_instance(identifier) if self.parent else None
        )
        if not instance:
            raise MappingError(
                f"Target instance '{identifier}' not found in current or parent scopes."
            )
        return instance

    def get_source_instance(self, identifier: str) -> BaseModel:
        """Get a source instance by its identifier"""
        instance = self.source_instances.get(identifier) or (
            self.parent.get_source_instance(identifier) if self.parent else None
        )
        if not instance:
            raise MappingError(
                f"Source instance '{identifier}' not found in current or parent scopes."
            )
        return instance

    def get_type(self, identifier: str) -> type[BaseModel]:
        """Get a type by its identifier"""
        type_ = self.types.get(identifier) or (
            self.parent.get_type(identifier) if self.parent else None
        )
        if not type_:
            raise MappingError(
                f"Type '{identifier}' not found in current or parent scopes."
            )
        return type_

    def lookup(self, identifier: str) -> Any:
        """Look up a variable, checking parent scopes if not found locally"""
        if identifier in self.variables:
            return self.variables[identifier]
        elif identifier in self.types:
            return self.types[identifier]
        elif identifier in self.groups:
            return self.groups[identifier]
        elif self.parent:
            try:
                return self.parent.lookup(identifier)
            except MappingError:
                pass
        raise MappingError(f"Variable or identifier '{identifier}' not found.")

    def exists(self, identifier: str) -> bool:
        """Check if identifier exists in this scope or any parent scope"""
        return self.lookup(identifier) is not None

    def exists_local(self, identifier: str) -> bool:
        """Check if identifier exists in the current scope only"""
        return identifier in self.variables or identifier in self.types

    def get_all_symbols(self) -> Dict[str, Any]:
        """Get all symbols visible from this scope (including inherited)"""
        all_symbols = {}
        if self.parent:
            all_symbols.update(self.parent.get_all_symbols())
        all_symbols.update(self.variables)
        return all_symbols

    def get_path(self) -> List[str]:
        """Get the path from root to this scope"""
        if self.parent:
            return self.parent.get_path() + [self.name]
        return [self.name]

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
        return f"Scope({self.name}, variables: {list(self.variables.keys())}, types: {list(self.types.keys())})"

    def __repr__(self) -> str:
        return f"Scope(name='{self.name}', parent={self.parent.name if self.parent else None}, variables={list(self.variables.keys())}, types={list(self.types.keys())})"

        return f"Scope(name='{self.name}', parent={self.parent.name if self.parent else None}, variables={list(self.variables.keys())}, types={list(self.types.keys())})"
