import os
from typing import List, Union

import jinja2
from pydantic import BaseModel

from fhircraft.fhir.resources.generator._schemas import GeneratorModule
from fhircraft.utils import ensure_list

from ._imports import ImportTracker
from ._renderer import CodeRenderer
from ._model import ModelSerializer

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)


class CodeGenerator:

    def __init__(self) -> None:
        self._tracker = ImportTracker()
        self._module = GeneratorModule()
        self._serializer = ModelSerializer(
            self._tracker,
            self._module,
        )
        self._renderer = CodeRenderer()

    def generate(
        self,
        resources: Union[type[BaseModel], List[type[BaseModel]]],
        include_validators: bool = True,
    ) -> str:
        """
        Generate source code for one or more pydantic model classes.

        Args:
            resources: A single model class or a list of model classes to generate.
            include_validators: Whether to include field/model validators (default True).

        Returns:
            A string containing valid Python source code.
        """
        self._tracker.reset()

        for resource in ensure_list(resources):
            serialized_resource = self._serializer.serialize(resource)

        grouped_imports = self._tracker.group_by_parent()

        return self._renderer.render(
            data=self._module,
            imports=self._tracker.group_by_parent(),
            alias_imports=self._tracker.alias_imports,
            raw_imports=dict(self._tracker.imports),
            include_validators=include_validators,
        )
