import sys
import types
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Dict,
    FrozenSet,
    List,
    Optional,
    Set,
    Tuple,
    ForwardRef,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel
from pydantic_core import PydanticUndefined

if TYPE_CHECKING:
    from ._imports import ImportTracker
    from ._model import ModelSerializer


class AnnotationSerializer:
    """Recursively serializes Python type annotations into source-code strings while registering necessary imports."""

    # Standard typing generics mapping for Python 3.9+ built-in origins (e.g. list -> List)
    _GENERIC_MAP = {
        list: List,
        dict: Dict,
        set: Set,
        tuple: Tuple,
        frozenset: FrozenSet,
    }

    def __init__(
        self,
        tracker: "ImportTracker",
        serializer: "ModelSerializer",
    ) -> None:
        self._tracker = tracker
        self._model_serializer = serializer

    def serialize(self, annotation: Any) -> str:
        """Entry point to convert any type annotation into a source-code string."""
        if annotation is None or annotation is type(None):
            return "None"

        if type(annotation) is ForwardRef:
            return f'"{annotation.__forward_arg__}"'

        # 1. Handle Annotated types (extract inner type or resolve FHIR primitive metadata)
        origin = get_origin(annotation)
        if origin is Annotated:
            return self._handle_annotated(annotation)

        # 2. Handle standard primitives and explicit class types (non-generic leaves)
        if isinstance(annotation, type) and not origin:
            return self._handle_concrete_type(annotation)

        # 3. Handle Primitive Class Aliases (FHIR metadata resolution fallback)
        resolved_primitive = self._resolve_primitive_alias(annotation)
        if resolved_primitive:
            return resolved_primitive

        # 4. Handle Generics & Compound Types recursively (Union, Optional, List, Dict, etc.)
        args = get_args(annotation)

        if origin and args:
            return self._handle_generic(origin, args, annotation)

        # 5. Handle string instances
        if isinstance(annotation, str):
            return f'"{annotation}"'

        name = getattr(annotation, "__name__", str(annotation))
        module_path = self._tracker.get_shortest_public_path(annotation)
        if module_path:
            self._track_and_format_type(annotation)
        return name

    # ------------------------------------------------------------------
    # Internal Handlers
    # ------------------------------------------------------------------

    def _handle_annotated(self, annotation: Any) -> str:
        """Process Annotated[T, metadata_1, metadata_2, ...]."""
        # Check if this Annotated instance is a special FHIR primitive alias
        resolved = self._resolve_annotated_primitive(annotation)
        if resolved:
            return resolved

        args = get_args(annotation)
        if not args:
            return self._handle_concrete_type(annotation)

        target_type = args[0]
        metadata_items = args[1:]

        # Process the inner target type recursively
        type_str = self.serialize(target_type)

        if not metadata_items:
            return type_str

        # Serialize all metadata arguments (e.g. FieldInfo or raw strings/objects)
        serialized_metadata = [
            self._serialize_metadata(item) for item in metadata_items
        ]

        self._tracker.track_typing("Annotated")
        return f"Annotated[{type_str}, {', '.join(serialized_metadata)}]"

    def _serialize_metadata(self, item: Any) -> str:
        """Serializes metadata objects inside Annotated[...] (strings, types, or Pydantic FieldInfo)."""
        if isinstance(item, str):
            return repr(item)

        item_type = type(item)

        # Handle Pydantic v2 FieldInfo dynamically
        if item_type.__name__ == "FieldInfo":
            self._tracker.track("pydantic", "Field")

            kwargs: list[str] = []

            # Exctract direct Field attributes explicitly set (e.g. description, alias, default)
            for attr in getattr(item, "_attributes_set", set()):
                val = getattr(item, attr, PydanticUndefined)
                if val is not PydanticUndefined:
                    serialized_val = (
                        self.serialize(val) if isinstance(val, type) else repr(val)
                    )
                    kwargs.append(f"{attr}={serialized_val}")

            # Extract constraints stored inside item.metadata (e.g. union_mode, gt, lt, pattern)
            for meta in getattr(item, "metadata", []):
                # Handle internal Pydantic metadata containers like _PydanticGeneralMetadata
                for attr in dir(meta):
                    if (
                        not attr.startswith("_")
                        and (value := getattr(meta, attr)) is not PydanticUndefined
                    ):
                        # Avoid duplicate keys if already extracted from _attributes_set
                        if not any(kw.startswith(f"{attr}=") for kw in kwargs):
                            serialized_val = (
                                self.serialize(value)
                                if isinstance(value, type)
                                else repr(value)
                            )
                            kwargs.append(f"{attr}={serialized_val}")

            return f"Field({', '.join(kwargs)})"

        if isinstance(item, type):
            return self._handle_concrete_type(item)

        return repr(item)

    def _handle_concrete_type(self, cls: type) -> str:
        """Format concrete types (str, int, custom models, Pydantic models)."""
        # Built-in types (e.g. int, str, float, bool)
        if cls.__module__ == "builtins":
            return cls.__name__

        return self._track_and_format_type(cls)

    def _handle_generic(
        self, origin: Any, args: Tuple[Any, ...], annotation: Any
    ) -> str:
        """Recursively format compound generic types (Unions, Optional, List, Dict, etc.)."""
        # --- Handle Union / Optional ---
        is_union = origin is Union or (
            hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)
        )

        if is_union:
            non_none = [a for a in args if a is not type(None)]
            has_none = len(non_none) < len(args)

            # Serialize inner args recursively
            serialized_args = [self.serialize(a) for a in non_none]

            if has_none:
                self._tracker.track("typing", "Optional")
                if len(serialized_args) == 1:
                    return f"Optional[{serialized_args[0]}]"

                self._tracker.track("typing", "Union")
                return f"Optional[Union[{', '.join(serialized_args)}]]"

            self._tracker.track("typing", "Union")
            return f"Union[{', '.join(serialized_args)}]"

        # Handle Container Generics (List, Dict, Tuple, Set, etc.)
        origin = self._GENERIC_MAP.get(origin, origin)
        origin_name = getattr(origin, "__name__", None) or getattr(
            origin, "_name", None
        )
        if origin_name:
            module_path: str | None = self._tracker.get_shortest_public_path(origin)
            if module_path:
                self._tracker.track(module_path, origin_name)
            serialized_args = [self.serialize(a) for a in args]
            return f"{origin_name}[{', '.join(serialized_args)}]"

        # Fallback for complex/custom generic origins
        return self._track_and_format_type(origin)

    def _track_and_format_type(self, target: Any) -> str:
        """Registers module imports via ImportTracker and applies the 'fhir.' alias prefix if applicable."""
        module_path: Optional[str] = self._tracker.get_shortest_public_path(target)
        name: str = getattr(target, "__name__", str(target))

        if module_path:
            # Check for fhircraft datatypes module pattern: fhircraft.fhir.resources.datatypes
            if "fhircraft.fhir.resources.datatypes" in module_path:
                self._tracker.track_alias(module_path, "fhir")
                return f"fhir.{name}"
            # Handle Pydantic BaseModel subclasses
            elif issubclass(target, BaseModel) and target is not BaseModel:
                model = self._model_serializer.serialize(target)
                self._tracker.track_generated_model(model)
            # Fallback to standard tracker resolution
            else:
                self._tracker.track(module_path, name)

        return name

    # ------------------------------------------------------------------
    # FHIR & Primitive Metadata Resolvers
    # ------------------------------------------------------------------

    def _resolve_annotated_primitive(self, annotation: Any) -> Optional[str]:
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
                    primitive_module = self._tracker.get_shortest_public_path(klass)
                    if primitive_module:
                        self._tracker.track_alias(primitive_module, "fhir")
                        return f"fhir.{name}"
                    return name
        return None

    def _resolve_primitive_alias(self, annotation: Any) -> Optional[str]:
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
                    primitive_module = self._tracker.get_shortest_public_path(klass)
                    if primitive_module:
                        self._tracker.track_alias(primitive_module, "fhir")
                        return f"fhir.{name}"
                    return name
        return None

    def _get_primitive_package_module(self, module: str) -> Optional[str]:
        parts = module.split(".")
        try:
            idx = parts.index("primitive")
            if idx >= 1:
                return ".".join(parts[: idx + 1])
        except ValueError:
            pass
        return None
