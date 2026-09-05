import datetime
import os
import re
from typing import Dict, List, Union

import jinja2
from pydantic import BaseModel

from fhircraft.utils import ensure_list, to_snake_case
from fhircraft import __version__ as fhircraft_version

from ._imports import ImportTracker
from ._model import ModelSerializer
from ._schemas import GeneratorModel

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)

# Filenames are derived from class names via `to_snake_case`, but this guards
# against ever joining an unexpected/malicious string onto a filesystem path.
_VALID_MODULE_NAME = re.compile(r"^[a-z_][a-z0-9_]*$")


class CodeGenerator:

    def __init__(self) -> None:
        self._tracker = ImportTracker()
        self._serializer = ModelSerializer(
            self._tracker,
        )
        self._template = JINJA_ENV.get_template("resource_template.py.j2")
        self._init_template = JINJA_ENV.get_template("init_template.py.j2")

    def generate_source(
        self,
        resources: Union[type[BaseModel], List[type[BaseModel]]],
    ) -> str:
        """
        Generate source code for one or more pydantic model classes.

        Args:
            resources: A single model class or a list of model classes to generate.

        Returns:
            A string containing valid Python source code.
        """
        self._collect(resources)
        return self._render_module(self._tracker.generated_models)

    def generate_files(
        self,
        resources: Union[type[BaseModel], List[type[BaseModel]]],
        split: bool = True,
    ) -> Dict[str, str]:
        """
        Generate an importable package (as an in-memory mapping) for one or more resources.

        Args:
            resources: A single model class or a list of model classes to generate.
            split: If True, each generated model (including transitive dependencies,
                not just the input resources) is placed in its own module. If False,
                all models are placed in a single `models.py` module.

        Returns:
            A mapping of relative filename (including `__init__.py`) to file content.
        """
        self._collect(resources)
        models = self._tracker.generated_models

        if not split:
            files = {"models.py": self._render_module(models)}
            exports = [("models", model.name) for model in models]
        else:
            files = {}
            module_names: Dict[str, str] = {}
            for model in models:
                module_name = to_snake_case(model.name)
                if not _VALID_MODULE_NAME.match(module_name):
                    raise ValueError(
                        f"Cannot derive a safe module name for class '{model.name}'."
                    )
                existing = module_names.get(module_name)
                if existing and existing != model.name:
                    raise ValueError(
                        f"Class name collision: '{existing}' and '{model.name}' both "
                        f"map to module '{module_name}.py'. Rename one of the classes."
                    )
                module_names[module_name] = model.name

            for model in models:
                module_name = to_snake_case(model.name)
                files[f"{module_name}.py"] = self._render_module(
                    [model], module_name=module_name
                )
            exports = [(to_snake_case(model.name), model.name) for model in models]

        files["__init__.py"] = self._init_template.render(
            exports=exports, metadata=self._metadata()
        )
        return files

    def generate(
        self,
        resources: Union[type[BaseModel], List[type[BaseModel]]],
        output_dir: Union[str, os.PathLike],
        split: bool = True,
        exist_ok: bool = True,
    ) -> List[str]:
        """
        Generate a fully importable Python package on disk for one or more resources.

        Args:
            resources: A single model class or a list of model classes to generate.
            output_dir: Directory the package is written to (created if missing).
            split: If True, each generated model gets its own module. If False, all
                models are written to a single `models.py` module.
            exist_ok: If False, raise if `output_dir` already exists.

        Returns:
            The absolute paths of all files written.
        """
        os.makedirs(output_dir, exist_ok=exist_ok)
        files = self.generate_files(resources, split=split)

        written_paths = []
        for filename, content in files.items():
            path = os.path.join(output_dir, filename)
            with open(path, "w") as f:
                f.write(content)
            written_paths.append(os.path.abspath(path))
        return written_paths

    def _collect(
        self, resources: Union[type[BaseModel], List[type[BaseModel]]]
    ) -> None:
        self._tracker.reset()
        for resource in ensure_list(resources):
            serialized_resource = self._serializer.serialize(resource)
            self._tracker.track_generated_model(serialized_resource)

    def _render_module(
        self, models: List[GeneratorModel], module_name: str | None = None
    ) -> str:
        if module_name is not None:
            imports = self._tracker.group_by_parent_for_model(models[0].name)
            alias_imports = self._tracker.alias_imports_for_model(models[0].name)
            imports = self._add_local_imports(imports, alias_imports, models[0])
        else:
            imports = self._tracker.group_by_parent()
            alias_imports = self._tracker.alias_imports

        return self._template.render(
            models=models,
            imports=imports,
            alias_imports=alias_imports,
            metadata=self._metadata(),
        )

    def _add_local_imports(
        self,
        imports: Dict[str, List[str]],
        alias_imports: Dict[str, str],
        model: GeneratorModel,
    ) -> Dict[str, List[str]]:
        """Add `from .other_model import Other` entries for sibling generated models."""
        refs = self._tracker.refs_by_model.get(model.name, set())
        for ref_name in sorted(refs):
            module = to_snake_case(ref_name)
            imports.setdefault(f".{module}", [])
            if ref_name not in imports[f".{module}"]:
                imports[f".{module}"].append(ref_name)
        return imports

    @staticmethod
    def _metadata() -> Dict[str, object]:
        return {
            "version": fhircraft_version,
            "timestamp": datetime.datetime.now(),
        }
