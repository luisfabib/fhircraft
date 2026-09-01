import os
import re
from datetime import datetime
from importlib.metadata import version
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


class CodeRenderer:
    """Renders serialized model data to a Python source-code string via Jinja2."""

    def __init__(self) -> None:
        env = Environment(
            loader=FileSystemLoader(TEMPLATES_DIR), trim_blocks=True, lstrip_blocks=True
        )
        env.filters["escapequotes"] = lambda s: s.replace('"', '\\"')
        env.globals["ismodel"] = lambda obj: isinstance(obj, BaseModel)
        self._template = env.get_template("resource_template.py.j2")

    def render(
        self,
        data: Dict,
        imports: Dict[str, List[str]],
        alias_imports: Dict[str, str],
        raw_imports: Dict[str, List[str]],
        include_validators: bool = True,
    ) -> str:
        code = self._template.render(
            data=data,
            imports=imports,
            alias_imports=alias_imports,
            include_validators=include_validators,
            metadata={
                "version": version("fhircraft"),
                "timestamp": datetime.now(),
            },
        )
        code = self._strip_module_prefixes(code, imports, raw_imports)
        code = self._clean_class_reprs(code, imports, data)
        code = self._clean_factory_refs(code, raw_imports)
        code = code.replace(LEFT_TO_RIGHT_COMPLEX, LEFT_TO_RIGHT_SIMPLE)
        return code

    def _strip_module_prefixes(
        self,
        code: str,
        imports: Dict[str, List[str]],
        raw_imports: Dict[str, List[str]],
    ) -> str:
        """Remove `module.` prefixes for all objects that are imported at the top."""
        for module, objects in imports.items():
            module_escaped = re.escape(module)
            for match in re.finditer(
                rf"({module_escaped}\.)({'|'.join(re.escape(o) for o in objects)})",
                code,
            ):
                code = code.replace(match.group(1), "")

        for module, objects in raw_imports.items():
            if not objects:
                continue
            module_escaped = re.escape(module)
            for match in re.finditer(
                rf"({module_escaped}\.)({'|'.join(re.escape(o) for o in objects)})",
                code,
            ):
                code = code.replace(match.group(1), "")

            parts = module.split(".")
            for module_variant in {module, parts[-1]} if len(parts) > 1 else {module}:
                for obj in objects:
                    code = re.sub(
                        rf"\b{re.escape(module_variant)}\.{re.escape(obj)}\b",
                        obj,
                        code,
                    )

        return code

    def _clean_class_reprs(
        self,
        code: str,
        imports: Dict[str, List[str]],
        data: Dict[Any, Any],
    ) -> str:
        """Replace `<class 'X'>` repr strings with bare class names."""
        all_names: set = set()
        for objects in imports.values():
            all_names.update(objects)
        for model in data:
            all_names.add(model.__name__)

        for name in all_names:
            code = re.sub(rf"<class '{re.escape(name)}'>", name, code)
            code = re.sub(rf"<class '[\w.]*\.{re.escape(name)}'>", name, code)

        for builtin in ("str", "int", "float", "bool", "list", "dict", "tuple", "set"):
            code = re.sub(rf"<class '{builtin}'>", builtin, code)

        return code

    def _clean_factory_refs(self, code: str, raw_imports: Dict[str, List[str]]) -> str:
        """Remove factory module paths and leftover `typing.` prefixes from repr() output."""
        code = code.replace(f"{FACTORY_MODULE}.", "")
        code = re.sub(re.escape(FACTORY_MODULE) + r"\.", "", code)
        code = re.sub(r"\btyping\.", "", code)
        return code
