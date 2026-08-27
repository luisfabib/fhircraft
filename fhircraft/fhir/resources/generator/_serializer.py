import functools
import inspect
import re
from enum import Enum
from typing import Annotated, Any, Dict, get_args, get_origin

from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from typing_extensions import TypeAliasType

from fhircraft.utils import get_module_name

from ._annotations import AnnotationSerializer
from ._constants import FACTORY_MODULE
from ._defaults import DefaultExtractor
from ._imports import ImportTracker


class ModelSerializer:
    """Walks pydantic model classes and extracts structured data for code generation."""

    def __init__(
        self,
        tracker: ImportTracker,
        resolver: AnnotationSerializer,
        extractor: DefaultExtractor,
    ) -> None:
        self._tracker = tracker
        self._resolver = resolver
        self._extractor = extractor
        self._processing: set = set()
        self._data: Dict = {}

    def reset(self) -> None:
        self._processing = set()
        self._data = {}

    @property
    def data(self) -> Dict:
        return self._data

    # ------------------------------------------------------------------
    # Model classification
    # ------------------------------------------------------------------

    def _is_builtin_pydantic_model(self, model: type) -> bool:
        if model is BaseModel:
            return True
        try:
            return get_module_name(model).startswith("pydantic")
        except Exception:
            return False

    def _is_fhir_framework_model(self, model: type) -> bool:
        """Framework models (e.g. DomainResource) are imported, not re-serialized."""
        try:
            module_name = get_module_name(model)
            return (
                module_name.startswith("fhircraft.fhir.resources")
                and module_name != FACTORY_MODULE
            )
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Import resolution
    # ------------------------------------------------------------------

    def resolve_imports(self, annotation: Any) -> None:
        """Walk annotation tree registering all required imports; serializes embedded factory models."""
        resolved_primitive = self._resolver.resolve_annotated_primitive(annotation)
        if resolved_primitive is not None:
            module, _ = resolved_primitive
            primitive_module = self._resolver.get_primitive_package_module(module)
            if primitive_module:
                self._tracker.track_alias(primitive_module, "fhir")
            return

        resolved_primitive_class = self._resolver.resolve_primitive_class_alias(
            annotation
        )
        if resolved_primitive_class is not None:
            primitive_module, _ = resolved_primitive_class
            self._tracker.track_alias(primitive_module, "fhir")
            return

        origin = get_origin(annotation)
        if origin is not None:
            origin_name = getattr(origin, "__name__", None)
            if origin_name:
                _map = {"list": "List", "dict": "Dict", "tuple": "Tuple", "set": "Set"}
                typing_name = _map.get(origin_name, origin_name)
                if typing_name and typing_name != "UnionType":
                    self._tracker.track_typing(typing_name)

        type_obj = getattr(annotation, "annotation", annotation)

        if type_obj is not None and not isinstance(type_obj, str):
            is_factory_model = False
            if isinstance(type_obj, type):
                try:
                    is_factory_model = get_module_name(
                        type_obj
                    ) == FACTORY_MODULE and issubclass(type_obj, BaseModel)
                except (TypeError, AttributeError):
                    pass

            if is_factory_model:
                if type_obj not in self._processing:
                    self.serialize(type_obj)
            elif get_origin(type_obj) is Annotated:
                self._tracker.track_typing("Annotated")
            else:
                try:
                    self._tracker.track_obj(type_obj)
                except Exception:
                    pass

        for nested in get_args(annotation):
            self.resolve_imports(nested)

    def _add_constant_value_imports(self, instance: BaseModel) -> None:
        self.resolve_imports(instance.__class__)
        for fieldname in sorted(
            instance.model_fields_set or instance.__class__.model_fields
        ):
            value = getattr(instance, fieldname)
            if isinstance(value, BaseModel):
                self._add_constant_value_imports(value)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, BaseModel):
                        self._add_constant_value_imports(item)

    # ------------------------------------------------------------------
    # Argument cleanup
    # ------------------------------------------------------------------

    def clean_argument(self, arg: Any) -> Any:
        """Normalize a partial-function argument for source-code output."""
        if isinstance(arg, str):
            if "\n" in arg:
                escaped = arg.replace("\\", "\\\\").replace('"""', r"\"\"\"")
                return f'"""{escaped}"""'
            escaped = arg.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"'
        if isinstance(arg, BaseModel):
            self._add_constant_value_imports(arg)
            return repr(arg)
        if isinstance(arg, list):
            result = []
            for item in arg:
                if isinstance(item, (type, TypeAliasType)):
                    try:
                        self._tracker.track_obj(item)
                        result.append(getattr(item, "__name__", repr(item)))
                    except Exception:
                        result.append(repr(item))
                else:
                    result.append(item)
            return result
        return arg

    # ------------------------------------------------------------------
    # Core serialization
    # ------------------------------------------------------------------

    def serialize(self, model: type[BaseModel]) -> None:
        """Extract all code-generation data from a model class into self.data."""
        if model in self._processing or model in self._data:
            return
        self._processing.add(model)
        try:
            self._serialize(model)
        finally:
            self._processing.discard(model)

    def _serialize(self, model: type[BaseModel]) -> None:
        for base in model.__bases__:
            if not base:
                continue
            if self._is_builtin_pydantic_model(base) or self._is_fhir_framework_model(
                base
            ):
                self._tracker.track_obj(base)
            elif base is not BaseModel:
                self.serialize(base)

        fields = self._extract_fields(model)
        if fields:
            self._tracker.track_pydantic("Field")

        properties = self._extract_properties(model)
        validators = self._extract_validators(model)

        if hasattr(model, "min_cardinality") or hasattr(model, "max_cardinality"):
            self._tracker.track_typing("ClassVar")

        if (
            (kind := getattr(model, "_kind", None))
            and getattr(kind, "__class__", None)
            and kind.__class__.__name__ == "FHIRModelKind"
        ):
            from fhircraft.fhir.resources.base import FHIRModelKind as _FBMKind

            self._tracker.track_obj(_FBMKind)

        self._data[model] = {
            "fields": fields,
            "properties": properties,
            "validators": validators,
        }

    def _extract_fields(self, model: type[BaseModel]) -> Dict:
        fields = {}
        for field, info in model.model_fields.items():
            # Skip fields that are identical to the parent's definition
            if (
                model.__base__
                and field in model.__base__.model_fields
                and all(
                    getattr(info, slot)
                    == getattr(model.__base__.model_fields[field], slot)
                    for slot in info.__slots__
                    if not slot.startswith("_")
                )
            ):
                continue

            original_annotation = model.__annotations__.get(field, info.annotation)
            self.resolve_imports(info.annotation)
            annotation_string = self._resolver.to_string(original_annotation)

            if "ForwardRef" in annotation_string:
                annotation_string = re.sub(
                    r"ForwardRef\('(\w+)'\)", r"'\1'", annotation_string
                )
            elif "Literal" not in annotation_string:
                annotation_string = re.sub(
                    rf"(?<!\.)(\b{model.__name__}\b)",
                    f'"{model.__name__}"',
                    annotation_string,
                )

            if isinstance(info.annotation, type(Enum)):
                self._tracker.track_typing("Literal")
                annotation_string = f"Literal['{info.annotation['fixedValue'].value}']"

            default = "..."
            default_factory = "..."
            if isinstance(info.default, str):
                default = f'"{info.default}"'
            elif isinstance(info.default, BaseModel):
                self._add_constant_value_imports(info.default)
                default_factory = f"lambda: {repr(info.default)}"
            elif info.default is not PydanticUndefined:
                default = repr(info.default)
            elif info.default_factory is not None:
                default_factory = self._extractor.extract_default_factory(
                    info.default_factory
                )

            fields[field] = {
                "annotation": annotation_string,
                "title": str(info.title) if info.title is not None else None,
                "description": (
                    str(info.description) if info.description is not None else None
                ),
                "alias": info.alias,
                "default": default,
                "default_factory": default_factory,
            }
        return fields

    def _extract_properties(self, model: type[BaseModel]) -> Dict:
        def _get_inherited(base_class):
            props = {}
            for base in base_class.__bases__:
                if not issubclass(base, BaseModel):
                    continue
                for key, val in base.__dict__.items():
                    if isinstance(val, property) and val.fget:
                        props[key] = val.fget
                props.update(_get_inherited(base))
            return props

        def _equivalent(a, b):
            if isinstance(a, functools.partial) and isinstance(b, functools.partial):
                return (
                    a.func == b.func and a.args == b.args and a.keywords == b.keywords
                )
            try:
                return inspect.getsource(a) == inspect.getsource(b)
            except (OSError, TypeError):
                return False

        inherited = _get_inherited(model)
        properties = {}
        for key, val in model.__dict__.items():
            if not isinstance(val, property):
                continue
            if key in inherited and _equivalent(val.fget, inherited[key]):
                continue
            if not val.fget:
                raise ValueError(f"Property {key} on {model.__name__} has no getter.")
            if isinstance(val.fget, functools.partial):
                self._tracker.track_obj(val.fget.func)
                properties[key] = {
                    "func": val.fget.func,
                    "args": [self.clean_argument(a) for a in val.fget.args],
                    "keywords": {
                        k: self.clean_argument(v) for k, v in val.fget.keywords.items()
                    },
                }
        return properties

    def _extract_validators(self, model: type[BaseModel]) -> Dict:
        def _get_inherited_fns(base_class):
            fns = []
            for base in base_class.__bases__:
                if not issubclass(base, BaseModel):
                    continue
                fns.extend(
                    getattr(v.func, "__func__", v.func)
                    for v in [
                        *base.__pydantic_decorators__.field_validators.values(),
                        *base.__pydantic_decorators__.model_validators.values(),
                    ]
                )
                fns.extend(_get_inherited_fns(base))
            return fns

        inherited_fns = _get_inherited_fns(model)
        validators = {}
        for mode, _validators in zip(
            ("field", "model"),
            (
                model.__pydantic_decorators__.field_validators,
                model.__pydantic_decorators__.model_validators,
            ),
        ):
            for name, validator in _validators.items():
                fn = getattr(validator.func, "__func__", validator.func)
                if not isinstance(fn, functools.partial) or fn in inherited_fns:
                    continue
                self._tracker.track_obj(fn.func)
                validators[name] = {
                    "mode": mode,
                    "info": validator.info,
                    "func": fn.func,
                    "args": [self.clean_argument(a) for a in fn.args],
                    "keywords": {
                        k: self.clean_argument(v) for k, v in fn.keywords.items()
                    },
                }
                self._tracker.track_pydantic(
                    "field_validator" if mode == "field" else "model_validator"
                )
        return validators
