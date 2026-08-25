import sys
from typing import Annotated, Any, Optional, Tuple, get_args, get_origin

from ._imports import ImportTracker


class AnnotationResolver:
    """Converts type annotations to source-code strings for code generation."""

    def __init__(self, tracker: ImportTracker) -> None:
        self._tracker = tracker

    # ------------------------------------------------------------------
    # Primitive resolution helpers
    # ------------------------------------------------------------------

    def get_primitive_package_module(self, module: str) -> Optional[str]:
        """Return the `...primitive` package path from a primitive submodule path."""
        parts = module.split(".")
        try:
            idx = parts.index("primitive")
        except ValueError:
            return None
        if idx < 1:
            return None
        return ".".join(parts[: idx + 1])

    def resolve_annotated_primitive(self, annotation: Any) -> Optional[Tuple[str, str]]:
        """Return (module, alias_name) if the annotation is a module-level Annotated primitive alias."""
        if get_origin(annotation) is not Annotated:
            return None
        for meta in getattr(annotation, "__metadata__", ()):
            func = getattr(meta, "func", None)
            if func is None:
                continue
            klass = getattr(func, "__self__", None)
            if not isinstance(klass, type):
                continue
            module = sys.modules.get(klass.__module__)
            if module is None:
                continue
            for name, val in vars(module).items():
                if val is annotation and not name.startswith("_"):
                    return klass.__module__, name
        return None

    def resolve_primitive_class_alias(self, annotation: Any) -> Optional[Tuple[str, str]]:
        """Return (primitive_module, alias_name) if annotation is a primitive class (e.g. String)."""
        if not isinstance(annotation, type):
            return None
        module_name = getattr(annotation, "__module__", "")
        if ".primitive." not in module_name:
            return None
        module = sys.modules.get(module_name)
        if module is None:
            return None
        for name, val in vars(module).items():
            if name.startswith("_") or get_origin(val) is not Annotated:
                continue
            for meta in getattr(val, "__metadata__", ()):
                func = getattr(meta, "func", None)
                klass = getattr(func, "__self__", None)
                if klass is annotation:
                    primitive_module = self.get_primitive_package_module(module_name)
                    return (primitive_module, name) if primitive_module else None
        return None

    # ------------------------------------------------------------------
    # Main public method
    # ------------------------------------------------------------------

    def to_string(self, annotation: Any) -> str:
        """Convert a type annotation to a source-code string, registering required imports."""
        import types as _types
        from typing import Union

        if annotation is type(None):
            return "None"

        resolved_class = self.resolve_primitive_class_alias(annotation)
        if resolved_class is not None:
            primitive_module, alias_name = resolved_class
            if self._tracker.track_alias(primitive_module, "fhir"):
                return f"fhir.{alias_name}"
            return alias_name

        resolved = self.resolve_annotated_primitive(annotation)
        if resolved is not None:
            module, name = resolved
            primitive_module = self.get_primitive_package_module(module)
            if primitive_module and self._tracker.track_alias(primitive_module, "fhir"):
                return f"fhir.{name}"
            return name

        origin = get_origin(annotation)
        args = get_args(annotation)

        # Non-primitive Annotated: unwrap and use the inner type
        if origin is Annotated:
            return self.to_string(args[0]) if args else repr(annotation)

        if not args:
            return repr(annotation)

        def _has_annotated_or_primitive(ann: Any) -> bool:
            if get_origin(ann) is Annotated:
                return True
            if self.resolve_primitive_class_alias(ann) is not None:
                return True
            return any(_has_annotated_or_primitive(a) for a in get_args(ann))

        if not any(_has_annotated_or_primitive(a) for a in args):
            return repr(annotation)

        is_union = origin is Union or (
            hasattr(_types, "UnionType") and isinstance(annotation, _types.UnionType)
        )
        if is_union:
            non_none = [a for a in args if a is not type(None)]
            has_none = len(non_none) < len(args)
            parts = [self.to_string(a) for a in non_none]
            if has_none and len(parts) == 1:
                self._tracker.track_typing("Optional")
                return f"Optional[{parts[0]}]"
            if has_none:
                self._tracker.track_typing("Optional")
                self._tracker.track_typing("Union")
                return f"Optional[Union[{', '.join(parts)}]]"
            self._tracker.track_typing("Union")
            return f"Union[{', '.join(parts)}]"

        origin_name = getattr(origin, "__name__", None) or getattr(origin, "_name", None)
        if origin_name:
            _map = {"list": "List", "dict": "Dict", "tuple": "Tuple", "set": "Set"}
            origin_name = _map.get(origin_name, origin_name)
            if origin_name in ("List", "Dict", "Set", "Tuple", "FrozenSet"):
                self._tracker.track_typing(origin_name)
            parts = [self.to_string(a) for a in args]
            return f"{origin_name}[{', '.join(parts)}]"

        return repr(annotation)
