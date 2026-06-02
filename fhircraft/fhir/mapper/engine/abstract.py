from abc import ABC, abstractmethod
from fhircraft.fhir.mapper.engine.scope import MappingScope
from typing import Any
import re
from fhircraft.fhir.path import FHIRPath, parse_fhirpath


class FHIRMappingEngineComponent(ABC):
    """Base class for components of the FHIR Mapper Engine."""

    fhirpath_engine = None

    @abstractmethod
    def process(self, scope: "MappingScope", *args, **kwargs) -> Any:
        """Process the component within the given mapping scope."""
        raise NotImplementedError("Subclasses must implement the process method.")

    def resolve_fhirpath_within_context(
        self, expression: str, scope: "MappingScope"
    ) -> FHIRPath:
        """Resolve FHIRPath expressions within the given context."""
        for variable_name, variable_path in scope.variables.items():
            expression = re.sub(
                rf"(?<!\.|\w){str(variable_name)}", str(variable_path), expression
            )
        return parse_fhirpath(expression)
