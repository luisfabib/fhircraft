"""
Core FHIRBaseModel — the abstract Pydantic base class for all FHIR types.
"""

import enum
import warnings
from abc import ABC
from copy import copy
from itertools import zip_longest
from typing import Any, ClassVar, Iterable, Mapping, SupportsIndex, Union, Literal
from typing_extensions import Self

from pydantic.config import ExtraValues
from pydantic import (
    BaseModel,
    ConfigDict,
    PrivateAttr,
    model_validator,
    field_validator,
    model_serializer,
    SerializerFunctionWrapHandler,
    SerializationInfo,
)
from pydantic_core import PydanticUndefined

from fhircraft.fhir.path.mixin import FHIRPathMixin
from fhircraft.fhir.resources.base.mixins import (
    FHIRContextMixin,
    FHIRXMLMixin,
    FHIRPolymorphicMixin,
)
from fhircraft.fhir.resources.base.mixins.polymorphic import (
    _get_polymorphic_deserialization_stack,
    _get_polymorphic_serialization_stack,
)

# ---------------------------------------------------------------------------
# FHIR model kind enumeration
# ---------------------------------------------------------------------------


class FHIRModelKind(str, enum.Enum):
    """Enumeration of FHIR StructureDefinition kinds."""

    LOGICAL = "logical"
    PRIMITIVE_TYPE = "primitive-type"
    COMPLEX_TYPE = "complex-type"
    RESOURCE = "resource"


# ---------------------------------------------------------------------------
# FHIRBaseModel
# ---------------------------------------------------------------------------


class FHIRBaseModel(
    BaseModel,
    ABC,
    FHIRContextMixin,
    FHIRXMLMixin,
    FHIRPolymorphicMixin,
    FHIRPathMixin,
):
    """
    Abstract base class for all FHIR resource and data-type models.

    Extends Pydantic's BaseModel with FHIR-specific behaviour:
    - Hierarchical parent-context tracking (_parent / _index)
    - Polymorphic serialization and deserialization
    - XML serialization and deserialization
    - Profile-slice construction and introspection
    - FHIRPath expression evaluation (via FHIRPathMixin)

    **This class is abstract and may not be instantiated directly.**
    All concrete FHIR types are generated subclasses that define _type.
    """

    model_config = ConfigDict(
        defer_build=True,
        validate_by_alias=True,
        validate_by_name=True,
        extra="forbid",
    )

    # ------------------------------------------------------------------
    # Structural class-level metadata (set by generator / factory)
    # ------------------------------------------------------------------

    _fhir_release: ClassVar[str]
    _abstract: ClassVar[bool] = False
    _kind: ClassVar[
        FHIRModelKind | Literal["primitive-type", "complex-type", "resource", "logical"]
    ] = "logical"
    _type: ClassVar[str]
    _canonical_url: ClassVar[str | None]

    # ------------------------------------------------------------------
    # Polymorphism feature flags — subclasses may override these ClassVars
    # to opt out of polymorphic behaviour for specific model hierarchies.
    # ------------------------------------------------------------------

    _polymorphic_serialization_enabled: ClassVar[bool] = True
    _polymorphic_deserialization_enabled: ClassVar[bool] = True

    @classmethod
    def _get_fhir_type(cls) -> str | None:
        """Return the FHIR type identifier for this class (e.g. 'Patient')."""
        return getattr(cls, "_type", None)

    # ------------------------------------------------------------------
    # Pydantic lifecycle
    # ------------------------------------------------------------------

    def model_post_init(self, context: Any) -> None:
        """Wire up parent-context tracking after construction."""
        self._set_resource_context()

    # ------------------------------------------------------------------
    # Pydantic validators
    # ------------------------------------------------------------------

    @model_validator(mode="before")
    @classmethod
    def _process_primitive_shadow_fields(cls, data: Any) -> Any:
        """Merge FHIR _fieldname shadow keys into their corresponding fields."""
        if not isinstance(data, dict):
            return data

        shadow_keys = [
            k
            for k in list(data.keys())
            if isinstance(k, str) and k.startswith("_") and len(k) > 1
        ]
        if not shadow_keys:
            return data

        data = dict(data)
        for shadow_key in shadow_keys:
            field_name = shadow_key[1:]
            shadow_data = data.pop(shadow_key, None)

            if shadow_data is None:
                continue

            if not isinstance(shadow_data, (dict, list)):
                data[shadow_key] = shadow_data
                continue

            existing = data.get(field_name)

            if isinstance(shadow_data, list):
                if existing is None:
                    data[field_name] = list(shadow_data)
                elif isinstance(existing, list):
                    merged = []
                    for val, ext in zip_longest(existing, shadow_data, fillvalue=None):
                        if ext is None:
                            merged.append(val)
                        elif val is None:
                            merged.append(ext)
                        elif isinstance(val, dict):
                            merged.append({**val, **ext})
                        else:
                            merged.append({"value": val, **ext})
                    data[field_name] = merged
            elif isinstance(shadow_data, dict):
                if existing is None:
                    data[field_name] = shadow_data
                elif isinstance(existing, dict):
                    data[field_name] = {**existing, **shadow_data}
                else:
                    data[field_name] = {"value": existing, **shadow_data}

        return data

    @model_validator(mode="before")
    @classmethod
    def _validate_resource_type(cls, data: Any) -> Any:
        """Reject payloads whose resourceType does not match this class."""
        if cls._is_resource():
            if "resourceType" not in cls.model_fields:
                if isinstance(data, dict) and "resourceType" in data:
                    data = data.copy()
                    resource_type = data.pop("resourceType")
                    if resource_type != cls._type:
                        raise ValueError(
                            f"Invalid resourceType '{resource_type}' for model "
                            f"'{cls.__name__}', expected '{cls._type}'."
                        )
                elif isinstance(data, FHIRBaseModel):
                    if data._type != cls._type:
                        raise ValueError(
                            f"Invalid resourceType '{data._type}' for model "
                            f"'{cls.__name__}', expected '{cls._type}'."
                        )
        return data

    @field_validator("*", mode="before")
    @classmethod
    def _validate_polymorphic_fields(cls, value: Any, info: Any) -> Any:
        """Apply polymorphic deserialization to FHIR fields during validation."""
        if not cls._polymorphic_deserialization_enabled:
            return value

        if not hasattr(info, "field_name") or not info.field_name:
            return value

        field_name = info.field_name
        if field_name not in cls.model_fields:
            return value

        field_info = cls.model_fields[field_name]
        base_type = cls._get_field_base_type(field_info)

        if not (
            base_type is not object
            and hasattr(base_type, "__mro__")
            and issubclass(base_type, FHIRBaseModel)
        ):
            return value

        is_abstract = base_type._abstract is True

        is_parent_instance = False
        if isinstance(value, FHIRBaseModel):
            is_parent_instance = type(value) is not base_type and issubclass(
                base_type, type(value)
            )
        elif isinstance(value, list):
            is_parent_instance = any(
                isinstance(item, FHIRBaseModel)
                and type(item) is not base_type
                and issubclass(base_type, type(item))
                for item in value
            )

        if not (is_abstract or is_parent_instance):
            return value

        context_key = (cls, field_name, base_type)
        stack = _get_polymorphic_deserialization_stack()
        if context_key in stack:
            return value

        stack.add(context_key)
        try:
            return cls._deserialize_polymorphically(value, base_type)
        except Exception:
            return value
        finally:
            stack.discard(context_key)

    # ------------------------------------------------------------------
    # Pydantic serializer
    # ------------------------------------------------------------------

    @model_serializer(mode="wrap")
    def _serialize_polymorphic_fields(
        self, serializer: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> Any:
        """Apply polymorphic serialization and emit FHIR _fieldname shadow data."""
        if (
            not isinstance(self, FHIRBaseModel)
            or not self._polymorphic_serialization_enabled
        ):
            return serializer(self)

        object_id = id(self)
        stack = _get_polymorphic_serialization_stack()
        if object_id in stack:
            return serializer(self)

        stack.add(object_id)
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                warnings.filterwarnings(
                    "ignore", message=".*Pydantic serializer warnings.*"
                )
                warnings.filterwarnings(
                    "ignore", message=".*PydanticSerializationUnexpectedValue.*"
                )
                data = serializer(self)

            for field_name, field_info in type(self).model_fields.items():
                value = getattr(self, field_name, None)
                if value is None:
                    continue

                if field_name in data:
                    base_type = self._get_field_base_type(field_info)
                    if (
                        base_type is not object
                        and hasattr(base_type, "__mro__")
                        and issubclass(base_type, FHIRBaseModel)
                    ):
                        data[field_name] = self._serialize_fhir_field_polymorphically(
                            value
                        )

                shadow = self._get_primitive_shadow_data(value)
                if shadow is not None:
                    data[f"_{field_name}"] = shadow
                    serialized = data.get(field_name)
                    if serialized is None:
                        data.pop(field_name, None)
                    elif isinstance(serialized, list) and all(
                        v is None for v in serialized
                    ):
                        data.pop(field_name, None)

            if (
                self._is_resource()
                and hasattr(self, "_type")
                and "resourceType" not in list(info.exclude or [])
            ):
                data["resourceType"] = self._type

            return data
        finally:
            stack.discard(object_id)

    # ------------------------------------------------------------------
    # Field mutation hook
    # ------------------------------------------------------------------

    def __setattr__(self, name: str, value: Any) -> None:
        """Propagate parent context whenever a field is assigned after construction."""
        super().__setattr__(name, value)
        if not name.startswith("_"):
            self._propagate_context_to_value(value)

    # ------------------------------------------------------------------
    # Public serialization API
    # ------------------------------------------------------------------

    @classmethod
    def _fhir_dump_kwargs(cls) -> dict[str, Any]:
        """Default keyword arguments applied by model_dump and model_dump_json."""
        return {"by_alias": True, "exclude_none": True}

    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        kwargs.update(self._fhir_dump_kwargs())
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args: Any, **kwargs: Any) -> str:
        kwargs.update(self._fhir_dump_kwargs())
        return super().model_dump_json(*args, **kwargs)

    # ------------------------------------------------------------------
    # Public deserialization API
    # ------------------------------------------------------------------

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: Any = None,
        extra: ExtraValues | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self:
        """Validate *obj* and return a model instance."""
        if by_alias is not None:
            warnings.warn(
                "FHIRBaseModel.model_validate does not support by_alias. Ignoring.",
                UserWarning,
                stacklevel=2,
            )
        if extra is not None:
            warnings.warn(
                "FHIRBaseModel.model_validate does not support extra. Ignoring.",
                UserWarning,
                stacklevel=2,
            )
        if by_name is not None:
            warnings.warn(
                "FHIRBaseModel.model_validate does not support by_name. Ignoring.",
                UserWarning,
                stacklevel=2,
            )
        return super().model_validate(
            obj, strict=strict, from_attributes=from_attributes, context=context
        )

    @classmethod
    def model_validate_json(
        cls,
        json_data: str | bytes | bytearray,
        *,
        strict: bool | None = False,
        context: Any = None,
        extra: ExtraValues | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self:
        """Deserialize *json_data* and return a validated model instance."""
        if by_alias is not None:
            warnings.warn(
                "FHIRBaseModel.model_validate_json does not support by_alias. Ignoring.",
                UserWarning,
                stacklevel=2,
            )
        if extra is not None:
            warnings.warn(
                "FHIRBaseModel.model_validate_json does not support extra. Ignoring.",
                UserWarning,
                stacklevel=2,
            )
        if by_name is not None:
            warnings.warn(
                "FHIRBaseModel.model_validate_json does not support by_name. Ignoring.",
                UserWarning,
                stacklevel=2,
            )
        return super().model_validate_json(json_data, strict=strict, context=context)

    # ------------------------------------------------------------------
    # Public construction API
    # ------------------------------------------------------------------

    @classmethod
    def model_construct(
        cls, set_defaults: bool = True, *args: Any, **kwargs: Any
    ) -> Self:
        """
        Construct a model instance without running validation.

        Args:
            set_defaults: When True (default), fields with a default value or
                factory are pre-populated.

        Returns:
            An unvalidated instance of the model.
        """
        instance = super().model_construct(*args, **kwargs)
        if not set_defaults:
            instance._set_resource_context()
            return instance

        for field_name, field in cls.model_fields.items():
            if getattr(instance, field_name, None) is not None:
                continue
            if field.default not in (PydanticUndefined, None):
                setattr(instance, field_name, copy(field.default))
            elif field.default_factory not in (PydanticUndefined, None):
                setattr(instance, field_name, field.default_factory())  # type: ignore[call-arg]

        instance._set_resource_context()
        return instance

    def model_copy(
        self, *, update: Mapping[str, Any] | None = None, deep: bool = False
    ) -> Self:
        """
        Return a copy of this instance with parent context reset.

        Args:
            update: Optional field updates to apply to the copy.
            deep: Whether to perform a deep copy.

        Returns:
            A copied instance with no parent context.
        """
        copied: Self = BaseModel.model_copy(self, update=update, deep=deep)  # type: ignore[arg-type]
        copied._set_resource_context()
        return copied

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __deepcopy__(self, memo: dict[int, Any] | None = None) -> Self:
        """
        Deep-copy via serialize → deserialize to avoid circular parent references.

        Args:
            memo: Standard deepcopy memo dict.

        Returns:
            A fully independent copy with fresh parent context.
        """
        copied = type(self).model_validate(self.model_dump())
        if memo is not None:
            memo[id(self)] = copied
        return copied

    def __eq__(self, other: object) -> bool:
        """
        Compare field values only, excluding tracking attributes (_parent, _index).

        Avoids infinite recursion through circular _parent chains.
        """
        if not isinstance(other, type(self)):
            return False
        return self.model_dump() == other.model_dump()

    def _get_repr_args(self) -> list[str]:
        repr_args = []
        for fieldname in sorted(self.model_fields_set or type(self).model_fields):
            value = getattr(self, fieldname)
            if isinstance(value, BaseModel):
                value = repr(value)
            elif isinstance(value, str):
                value = f'"{value}"'
            repr_args.append(f"{fieldname}={value}")
        return repr_args

    def __repr__(self) -> str:
        return f"{type(self).__name__}({', '.join(self._get_repr_args())})"


# ------------------------------------------------------------------
# Other models
# ------------------------------------------------------------------


class FHIRSliceModel(FHIRBaseModel):
    """
    Base class for representation of FHIR profiled slices as Pydantic objects.

    Expands the `FHIRBaseModel` class with slice-specific methods.
    """

    min_cardinality: ClassVar[int] = 0
    max_cardinality: ClassVar[int | None] = None


class FHIRList(list):
    """
    Custom list wrapper that maintains parent context on mutations.

    This list automatically propagates _parent, _root_resource, _resource, and _index context
    to FHIRBaseModel items when they are added via append, extend, insert, or __setitem__.
    """

    def __init__(
        self, items: Iterable[Any] | None = None, parent: FHIRBaseModel | None = None
    ):
        """Initialize FHIRList with items and context.

        Args:
            items: Initial items for the list.
            parent: The parent FHIRBaseModel instance that owns this list.
        """
        super().__init__(items or [])
        self._parent = parent
        self._propagate_context()

    def _propagate_context(self):
        """Set _parent and _index on all current FHIRBaseModel items."""
        if self._parent is None:
            return

        for index, item in enumerate(self):
            if isinstance(item, FHIRBaseModel):
                object.__setattr__(item, "_parent", self._parent)
                object.__setattr__(item, "_index", index)

    def append(self, item: Any):
        """Append item and propagate context."""
        super().append(item)
        if isinstance(item, FHIRBaseModel):
            object.__setattr__(item, "_parent", self._parent)
            object.__setattr__(item, "_index", len(self) - 1)

    def extend(self, items: Iterable[Any]):
        """Extend list and propagate context to new items."""
        start_index = len(self)
        super().extend(items)
        for offset, item in enumerate(items):
            if isinstance(item, FHIRBaseModel):
                object.__setattr__(item, "_parent", self._parent)
                object.__setattr__(item, "_index", start_index + offset)

    def insert(self, index: SupportsIndex, item: Any):
        """Insert item and propagate context."""
        super().insert(index, item)
        if isinstance(item, FHIRBaseModel):
            object.__setattr__(item, "_parent", self._parent)
            object.__setattr__(item, "_index", index)
        # Re-index all items after insertion point
        for i in range(int(index) + 1, len(self)):
            if isinstance(self[i], FHIRBaseModel):
                object.__setattr__(self[i], "_index", i)

    def __setitem__(self, index, item):
        """Set item and propagate context."""
        super().__setitem__(index, item)
        if isinstance(item, FHIRBaseModel):
            if isinstance(index, int):
                object.__setattr__(item, "_parent", self._parent)
                object.__setattr__(item, "_index", index)
            else:
                # Slice assignment – re-propagate to fix indices.
                self._propagate_context()
        elif isinstance(item, list):
            # Slice assignment with a plain list – re-propagate to fix indices.
            self._propagate_context()
