"""
ContextVar-based recursion guards and polymorphic serialization/deserialization mixin.

Uses contextvars.ContextVar instead of threading.local so the recursion guards
are safe for both threaded and async (asyncio / FastAPI) workloads.
"""

from contextvars import ContextVar
from functools import lru_cache
from typing import Any, Union, List, Type, get_origin, get_args, TYPE_CHECKING

from pydantic import ValidationError

if TYPE_CHECKING:
    from fhircraft.fhir.resources.base.model import FHIRBaseModel

# ---------------------------------------------------------------------------
# Async-safe recursion guards
# ---------------------------------------------------------------------------

_deser_stack: ContextVar[set | None] = ContextVar("_fhir_deser_stack", default=None)
_ser_stack: ContextVar[set | None] = ContextVar("_fhir_ser_stack", default=None)


def _get_polymorphic_deserialization_stack() -> set:
    """Return the per-task/thread deserialization recursion guard set."""
    stack = _deser_stack.get(None)
    if stack is None:
        stack = set()
        _deser_stack.set(stack)
    return stack


def _get_polymorphic_serialization_stack() -> set:
    """Return the per-task/thread serialization recursion guard set."""
    stack = _ser_stack.get(None)
    if stack is None:
        stack = set()
        _ser_stack.set(stack)
    return stack


# ---------------------------------------------------------------------------
# Mixin
# ---------------------------------------------------------------------------


class FHIRPolymorphicMixin:
    """
    Mixin providing polymorphic serialization and deserialization helpers.

    These are *helpers* called from the Pydantic validators/serializers that
    remain on FHIRBaseModel; they are not validators themselves and carry no
    Pydantic decorator magic.
    """

    @classmethod
    @lru_cache(maxsize=256)
    def _get_all_subclasses(cls, base_class: type) -> list[type]:
        """
        Return all subclasses of *base_class* recursively, depth-first.

        Most-specialised classes appear first so polymorphic deserialization
        picks the tightest matching subclass.  Results are cached per
        (caller-class, base_class) pair.
        """
        subclasses: list[type] = []
        for subclass in base_class.__subclasses__():
            subclasses.extend(cls._get_all_subclasses(subclass))
            subclasses.append(subclass)
        return subclasses

    @classmethod
    def _get_field_base_type(cls, field_info: Any) -> type:
        """
        Extract the concrete element type from a field annotation.

        Unwraps Optional[...] and List[...] to return the innermost type.
        Returns ``object`` when the type cannot be resolved.
        """
        annotation = (
            field_info.annotation if hasattr(field_info, "annotation") else field_info
        )

        origin = get_origin(annotation)
        if origin is Union:
            non_none = [a for a in get_args(annotation) if a is not type(None)]
            if non_none:
                annotation = non_none[0]
                origin = get_origin(annotation)

        if origin in (list, List):
            args = get_args(annotation)
            if args:
                annotation = args[0]

        return annotation if isinstance(annotation, type) else object

    @classmethod
    def _deserialize_polymorphically(cls, value: Any, base_type: type) -> Any:
        """
        Deserialize *value* using the best-matching subclass of *base_type*.

        Handles:
        - Lists — each item is deserialized recursively.
        - FHIRBaseModel instances — up-cast parent instances to the correct subtype.
        - Dicts — tried against each subclass in depth-first order, then the base type.
        """
        from fhircraft.fhir.resources.base.model import FHIRBaseModel

        if isinstance(value, list):
            return [cls._deserialize_polymorphically(item, base_type) for item in value]

        if isinstance(value, FHIRBaseModel):
            if isinstance(value, base_type):
                return value
            return cls._deserialize_polymorphically(value.model_dump(), base_type)

        if isinstance(value, dict):
            for subclass in cls._get_all_subclasses(base_type):
                try:
                    return subclass.model_validate(value)
                except (ValidationError, ValueError, TypeError):
                    continue
            try:
                return base_type.model_validate(value)
            except (ValidationError, ValueError, TypeError):
                pass

        return value

    def _serialize_fhir_field_polymorphically(self, value: Any) -> Any:
        """
        Serialize a FHIR field value using its runtime type.

        Ensures that specialised subclass fields (e.g. profile-constrained
        resources) are serialized with all their fields, not just those of the
        declared base type.
        """
        from fhircraft.fhir.resources.base.model import FHIRBaseModel

        if isinstance(value, (list, tuple)):
            return [self._serialize_fhir_field_polymorphically(item) for item in value]
        if isinstance(value, FHIRBaseModel):
            return value.model_dump()
        return value

    @staticmethod
    def _get_primitive_shadow_data(value: Any) -> "Any | None":
        """
        Return the FHIR _fieldname shadow dict/list for a primitive that carries
        an id or extension, or None when no shadow data is present.
        """
        from fhircraft.fhir.resources.base.primitives import FHIRPrimitiveModel

        if isinstance(value, FHIRPrimitiveModel):
            shadow: dict = {}
            if getattr(value, "id", None) is not None:
                shadow["id"] = value.id
            ext = getattr(value, "extension", None)
            if ext:
                shadow["extension"] = [e.model_dump() for e in ext]
            return shadow if shadow else None

        if isinstance(value, list):
            shadow_list: list = []
            has_shadow = False
            for item in value:
                if isinstance(item, FHIRPrimitiveModel):
                    item_shadow: dict = {}
                    if getattr(item, "id", None) is not None:
                        item_shadow["id"] = item.id
                    ext = getattr(item, "extension", None)
                    if ext:
                        item_shadow["extension"] = [e.model_dump() for e in ext]
                    if item_shadow:
                        has_shadow = True
                    shadow_list.append(item_shadow if item_shadow else None)
                else:
                    shadow_list.append(None)
            return shadow_list if has_shadow else None

        return None
