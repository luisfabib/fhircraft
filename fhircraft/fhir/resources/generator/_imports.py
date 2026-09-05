from collections import defaultdict
from contextlib import contextmanager
from typing import Any, Dict, ForwardRef, Iterator, List, Set

import sys
import inspect

from fhircraft.fhir.resources.factory.core import FHIRModelFactory
from fhircraft.fhir.resources.generator._schemas import GeneratorModel
from fhircraft.utils import get_module_name


class ImportTracker:
    """Tracks all import statements needed for a code generation run."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._generated_models: Dict[str, GeneratorModel] = {}
        self._imports: Dict[str, List[str]] = defaultdict(list)
        self._alias_imports: Dict[str, str] = {}
        self._model_stack: List[str] = []
        self._imports_by_model: Dict[str, Dict[str, List[str]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self._alias_imports_by_model: Dict[str, Dict[str, str]] = defaultdict(dict)
        self._refs_by_model: Dict[str, Set[str]] = defaultdict(set)

    @contextmanager
    def model_context(self, name: str) -> Iterator[None]:
        """Attribute any imports/refs tracked while active to the given model."""
        self._model_stack.append(name)
        try:
            yield
        finally:
            self._model_stack.pop()

    @property
    def imports(self) -> Dict[str, List[str]]:
        return self._imports

    @property
    def generated_models(self) -> List[GeneratorModel]:
        return list(self._generated_models.values())

    @property
    def alias_imports(self) -> Dict[str, str]:
        return self._alias_imports

    @property
    def refs_by_model(self) -> Dict[str, Set[str]]:
        return self._refs_by_model

    def track_generated_model(self, model: GeneratorModel) -> None:
        self._generated_models[model.name] = model
        if self._model_stack and self._model_stack[-1] != model.name:
            self._refs_by_model[self._model_stack[-1]].add(model.name)

    def track(self, module: str, name: str) -> None:
        if module in (get_module_name(FHIRModelFactory), "builtins"):
            return
        if name not in self._imports[module]:
            self._imports[module].append(name)
        if self._model_stack:
            current = self._imports_by_model[self._model_stack[-1]][module]
            if name not in current:
                current.append(name)

    def track_alias(self, module: str, alias: str) -> bool:
        """Register `import module as alias`; returns False if alias is already claimed by another module."""
        existing = next((m for m, a in self._alias_imports.items() if a == alias), None)
        if existing and existing != module:
            return False
        self._alias_imports[module] = alias
        if self._model_stack:
            self._alias_imports_by_model[self._model_stack[-1]][module] = alias
        return True

    def track_pydantic(self, name: str) -> None:
        self.track("pydantic", name)

    def track_typing(self, name: str) -> None:
        self.track("typing", name)

    def group_by_parent(self) -> Dict[str, List[str]]:
        """Collapse per-class module paths into their shared parent package."""
        return self._group_by_parent(self._imports)

    def group_by_parent_for_model(self, name: str) -> Dict[str, List[str]]:
        """Collapse per-class module paths into their shared parent package, scoped to one model."""
        return self._group_by_parent(self._imports_by_model.get(name, {}))

    def alias_imports_for_model(self, name: str) -> Dict[str, str]:
        return dict(self._alias_imports_by_model.get(name, {}))

    @staticmethod
    def _group_by_parent(imports: Dict[str, List[str]]) -> Dict[str, List[str]]:
        if not imports:
            return {}
        grouped: Dict[str, List[str]] = {}
        for full_module, objects in imports.items():
            parts = full_module.split(".")
            # If the module name is a snake_case version of the single imported symbol,
            # import from the parent package instead.
            if len(objects) == 1 and parts[-1].lower().replace("_", "") == objects[
                0
            ].lower().replace("_", ""):
                parent = ".".join(parts[:-1])
                grouped.setdefault(parent, []).extend(objects)
            else:
                grouped.setdefault(full_module, []).extend(objects)
        for module in grouped:
            grouped[module] = sorted(set(grouped[module]))
        return grouped

    def get_shortest_public_path(self, obj: object) -> str | None:
        """Finds the shortest imported module path where this object is accessible."""
        target = obj if inspect.isclass(obj) or inspect.isfunction(obj) else type(obj)
        full_module = getattr(target, "__module__", None)
        name = getattr(target, "__name__", None)

        if not full_module or not name:
            return None

        top_pkg = full_module.split(".")[0]
        candidate_modules = []

        # Check loaded modules under the same top-level package
        for mod_name, mod in sys.modules.items():
            if (mod_name == top_pkg or mod_name.startswith(top_pkg + ".")) and mod:
                if getattr(mod, name, None) is target:
                    candidate_modules.append(mod_name)

        # Sort by number of dots (depth) and string length
        if candidate_modules:
            shortest_mod = min(candidate_modules, key=lambda m: (m.count("."), len(m)))
            return shortest_mod

        return full_module
