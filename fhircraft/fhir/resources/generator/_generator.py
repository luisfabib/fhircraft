from typing import List, Union

from pydantic import BaseModel

from fhircraft.utils import ensure_list

from ._annotations import AnnotationSerializer
from ._defaults import DefaultExtractor
from ._imports import ImportTracker
from ._renderer import CodeRenderer
from ._serializer import ModelSerializer


class CodeGenerator:
    """
    Generates Python source code for pydantic model classes derived from FHIR profiles.

    Usage::

        gen = CodeGenerator()
        source = gen.generate(MyProfileModel)
        source = gen.generate([ModelA, ModelB], include_validators=False)
    """

    def __init__(self) -> None:
        self._tracker = ImportTracker()
        self._resolver = AnnotationSerializer(self._tracker)
        self._extractor = DefaultExtractor()
        self._serializer = ModelSerializer(
            self._tracker, self._resolver, self._extractor
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
        self._serializer.reset()

        for resource in ensure_list(resources):
            self._serializer.serialize(resource)

        grouped_imports = self._tracker.group_by_parent()

        return self._renderer.render(
            data=self._serializer.data,
            imports=grouped_imports,
            alias_imports=self._tracker.alias_imports,
            raw_imports=dict(self._tracker.imports),
            include_validators=include_validators,
        )
