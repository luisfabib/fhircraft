from abc import ABC, abstractmethod
from fhircraft.fhir.mapper.engine.scope import MappingScope
from typing import Any
import re
from fhircraft.fhir.path.engine.core import FHIRPath
from fhircraft.fhir.path import fhirpath as fhirpath_parser


class FHIRMappingEngineComponent(ABC):
    """Base class for components of the FHIR Mapper Engine."""

    @abstractmethod
    def process(self, scope: "MappingScope") -> Any:
        """Process the component within the given mapping scope."""
        raise NotImplementedError("Subclasses must implement the process method.")

    @staticmethod
    def resolve_fhirpath_within_context(
        expression: str, scope: "MappingScope"
    ) -> FHIRPath:
        """Resolve FHIRPath expressions within the given context."""
        for variable_name, variable_path in scope.variables.items():
            expression = re.sub(
                rf"(?<!\.|\w){variable_name}", str(variable_path), expression
            )
        return fhirpath_parser.parse(expression)
