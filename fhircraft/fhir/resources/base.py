from copy import copy
from datetime import date, datetime, time
import enum
from functools import lru_cache
from itertools import zip_longest
import operator
import re
import threading
import warnings
from typing import (
    Any,
    ClassVar,
    Generic,
    Mapping,
    Optional,
    TypeVar,
    Union,
    Dict,
    List,
    Type,
    get_origin,
    get_args,
    Literal,
)
from xml.etree.ElementInclude import include
from typing_extensions import Self
import xml.etree.ElementTree as xml
from xml.dom import minidom
from pydantic.main import IncEx
from pydantic.config import ExtraValues
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    ValidationError,
    PrivateAttr,
    model_validator,
    field_validator,
    model_serializer,
    SerializerFunctionWrapHandler,
    SerializationInfo,
)
from pydantic_core import PydanticUndefined

from fhircraft.fhir.path.mixin import FHIRPathMixin
from fhircraft.utils import get_all_models_from_field

XML_NAMESPACE = "http://hl7.org/fhir"
xml.register_namespace("", XML_NAMESPACE)  # Register as the default XML namespace

# Thread-local context to track polymorphic operations to prevent recursion
_polymorphic_context = threading.local()


class FhirBaseModelKind(str, enum.Enum):
    """Enumeration of StructureMap model modes."""

    LOGICAL = "logical"
    PRIMITIVE_TYPE = "primitive-type"
    COMPLEX_TYPE = "complex-type"
    RESOURCE = "resource"


def _get_polymorphic_deserialization_stack():
    """Get the current polymorphic deserialization stack."""
    if not hasattr(_polymorphic_context, "deserialization_stack"):
        _polymorphic_context.deserialization_stack = set()
    return _polymorphic_context.deserialization_stack


def _get_polymorphic_serialization_stack():
    """Get the current polymorphic serialization stack."""
    if not hasattr(_polymorphic_context, "serialization_stack"):
        _polymorphic_context.serialization_stack = set()
    return _polymorphic_context.serialization_stack


class FHIRBaseModel(BaseModel, FHIRPathMixin):
    """
    Base class for representation of FHIR resources as Pydantic objects.

    Expands the Pydantic [BaseModel](https://docs.pydantic.dev/latest/api/base_model/) class with FHIR-specific methods.
    """

    model_config = ConfigDict(
        defer_build=True,
        validate_by_alias=True,
        validate_by_name=True,
        extra="forbid",
    )
    _fhir_release: ClassVar[str]

    # Structureal metadata
    _abstract: ClassVar[bool] = False
    _kind: ClassVar[
        FhirBaseModelKind
        | Literal["primitive-type", "complex-type", "resource", "logical"]
    ] = "logical"
    _type: ClassVar[str]
    _canonical_url: ClassVar[str | None]

    # Configuration for polymorphic behavior
    _enable_polymorphic_serialization: ClassVar[bool] = True
    _enable_polymorphic_deserialization: ClassVar[bool] = True

    # Parent tracking attributes (stored – others computed lazily)
    _parent: Union["FHIRBaseModel", None] = PrivateAttr(default=None)
    _index: Union[int, None] = PrivateAttr(default=None)

    @property
    def _root_resource(self) -> "FHIRBaseModel":
        """Walk up the _parent chain to return the topmost node (the document root)."""
        node = self
        while node._parent is not None:
            node = node._parent
        return node

    @property
    def _resource(self) -> "Union[FHIRBaseModel, None]":
        """Walk up the _parent chain to return the nearest enclosing resource/logical node."""
        node: "Union[FHIRBaseModel, None]" = self
        while node is not None:
            if node._is_resource():
                return node
            node = node._parent
        return None

    @classmethod
    def _is_resource(cls) -> bool:
        """Check if this instance is a FHIR resource."""
        return (
            cls._kind == FhirBaseModelKind.RESOURCE
            or cls._kind == FhirBaseModelKind.LOGICAL
        )

    def model_post_init(self, context: Any) -> None:
        """Initialize model and set up parent tracking."""
        # After construction, propagate context to all nested fields
        self._set_resource_context()

    @model_validator(mode="before")
    @classmethod
    def _process_primitive_shadow_fields(cls, data: Any) -> Any:
        """Process FHIR _fieldname shadow keys, merging id/extension into the corresponding field."""
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

        if cls._is_resource():
            if not "resourceType" in cls.model_fields:
                if isinstance(data, dict) and "resourceType" in data:
                    data = data.copy()
                    resource_type = data.pop("resourceType")
                    if resource_type != cls._type:
                        raise ValueError(
                            f"Invalid resourceType '{resource_type}' for model '{cls.__name__}', expected '{cls._type}'."
                        )

                elif isinstance(data, FHIRBaseModel):
                    if data._type != cls._type:
                        raise ValueError(
                            f"Invalid resourceType '{data._type}' for model '{cls.__name__}', expected '{cls._type}'."
                        )
        return data

    @field_validator("*", mode="before")
    @classmethod
    def _validate_polymorphic_fields(cls, value: Any, info) -> Any:
        """Apply polymorphic deserialization to FHIR fields during validation."""
        # Check if polymorphic deserialization is enabled
        if not cls._enable_polymorphic_deserialization:
            return value

        # Only process if we have field info
        if not hasattr(info, "field_name") or not info.field_name:
            return value

        field_name = info.field_name

        # Get field info from model fields
        if field_name not in cls.model_fields:
            return value

        field_info = cls.model_fields[field_name]
        base_type = cls._get_field_base_type(field_info)

        # Check if polymorphic deserialization should apply:
        # 1. Abstract FHIR base types (always)
        # 2. Non-abstract FHIR types when receiving an instance of a parent class
        should_apply_polymorphic = (
            base_type != object
            and hasattr(base_type, "__mro__")
            and issubclass(base_type, FHIRBaseModel)
        )

        if not should_apply_polymorphic:
            return value

        # Check if this is an abstract type or if we're receiving a parent class instance
        is_abstract = base_type._abstract is True

        # Check if we have a parent class instance
        is_parent_instance = False
        if isinstance(value, FHIRBaseModel):
            # Single instance: check if it's a parent class
            is_parent_instance = type(value) != base_type and issubclass(
                base_type, type(value)
            )
        elif isinstance(value, list):
            # List: check if any items are parent class instances
            is_parent_instance = any(
                isinstance(item, FHIRBaseModel)
                and type(item) != base_type
                and issubclass(base_type, type(item))
                for item in value
            )

        if not (is_abstract or is_parent_instance):
            return value

        # Create a unique key for this deserialization context
        context_key = (cls, field_name, base_type)
        stack = _get_polymorphic_deserialization_stack()

        # Check if we're already processing this context to prevent recursion
        if context_key in stack:
            return value

        # Add to stack and process
        stack.add(context_key)
        try:
            result = cls._deserialize_polymorphically(value, base_type)
            return result
        except Exception:
            return value
        finally:
            # Always remove from stack when done
            stack.discard(context_key)

    @model_serializer(mode="wrap")
    def _serialize_polymorphic_fields(
        self, serializer: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> Any:
        """Apply polymorphic serialization to FHIR fields during serialization."""
        # Check if polymorphic serialization is enabled
        if (
            not isinstance(self, FHIRBaseModel)
            or not self._enable_polymorphic_serialization
        ):
            return serializer(self)

        # Check if we're already serializing this object to prevent recursion
        object_id = id(self)
        stack = _get_polymorphic_serialization_stack()
        if object_id in stack:
            # Already serializing this object, use normal serializer to avoid recursion
            return serializer(self)

        # Add to stack
        stack.add(object_id)
        try:
            # Get the base serialization with warnings suppressed
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                warnings.filterwarnings(
                    "ignore", message=".*Pydantic serializer warnings.*"
                )
                warnings.filterwarnings(
                    "ignore", message=".*PydanticSerializationUnexpectedValue.*"
                )
                data = serializer(self)

            # Apply polymorphic serialization to FHIR fields and collect primitive shadow data
            for field_name, field_info in type(self).model_fields.items():
                value = getattr(self, field_name, None)
                if value is None:
                    continue

                if field_name in data:
                    base_type = self._get_field_base_type(field_info)
                    if (
                        base_type != object
                        and hasattr(base_type, "__mro__")
                        and issubclass(base_type, FHIRBaseModel)
                    ):
                        data[field_name] = self._serialize_fhir_field_polymorphically(
                            value
                        )

                shadow = self._get_primitive_shadow_data(value)
                if shadow is not None:
                    data[f"_{field_name}"] = shadow
                    # Suppress the primitive fieldname key when:
                    # - scalar: serialized value is None
                    # - list: ALL serialized values are None (extension-only, no actual values)
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
            # Always remove from stack when done
            stack.discard(object_id)

    @classmethod
    @lru_cache(maxsize=256)
    def _get_all_subclasses(cls, base_class: Type) -> List[Type]:
        """Get all subclasses of a base class recursively, with caching.

        Returns subclasses in depth-first order, with most specialized classes first.
        This ensures polymorphic deserialization tries the most specific matches first.
        """
        subclasses = []
        for subclass in base_class.__subclasses__():
            # Add specialized subclasses first (depth-first)
            subclasses.extend(cls._get_all_subclasses(subclass))
            # Then add the current subclass
            subclasses.append(subclass)
        return subclasses

    @classmethod
    def _get_field_base_type(cls, field_info: Any) -> Type:
        """Extract the base type from a field annotation."""
        annotation = (
            field_info.annotation if hasattr(field_info, "annotation") else field_info
        )

        # Handle Optional[List[SomeType]] -> SomeType
        origin = get_origin(annotation)
        if origin is Union:  # Optional case
            args = get_args(annotation)
            # Find the non-None type
            non_none_types = [arg for arg in args if arg is not type(None)]
            if non_none_types:
                annotation = non_none_types[0]
                origin = get_origin(annotation)

        # Handle List[SomeType] -> SomeType
        if origin in (list, List):
            args = get_args(annotation)
            if args:
                annotation = args[0]

        # Return the final type
        if isinstance(annotation, type):
            return annotation

        return object  # Fallback

    def __setattr__(self, name: str, value: Any):
        """Override to propagate context when fields are assigned after construction."""
        # Call parent __setattr__ first
        super().__setattr__(name, value)

        # Only propagate context for actual fields (not private attributes)
        if not name.startswith("_"):
            # Propagate context to newly assigned value
            self._propagate_context_to_value(value)

    def _set_resource_context(
        self,
        parent: Union["FHIRBaseModel", None] = None,
        root: Union["FHIRBaseModel", None] = None,
        resource: Union["FHIRBaseModel", None] = None,
        index: Union[int, None] = None,
    ):
        """
        Set parent and index context for this instance, then propagate to direct children.

        ``_root_resource`` and ``_resource`` are computed lazily by walking ``_parent``,
        so only ``_parent`` and ``_index`` need to be stored.  The ``root`` and
        ``resource`` arguments are accepted for backwards-compatibility but ignored.

        Args:
            parent: The parent FHIRBaseModel instance (if this is a nested field)
            root: Ignored – resolved lazily via the ``_root_resource`` property.
            resource: Ignored – resolved lazily via the ``_resource`` property.
            index: The index of this instance in a list (if applicable)
        """
        object.__setattr__(self, "_parent", parent)
        object.__setattr__(self, "_index", index)

        # Propagate _parent / _index to direct children only.
        # Deeper descendants were already wired by their own model_post_init call;
        # they resolve _root_resource / _resource lazily via property traversal.
        for field_name in type(self).model_fields:
            value = getattr(self, field_name, None)
            if value is not None:
                self._propagate_context_to_value(value)

    def _propagate_context_to_value(self, value: Any):
        """
        Propagate parent context to a direct child field value.

        Only ``_parent`` and ``_index`` are written; ``_root_resource`` and
        ``_resource`` are resolved lazily by property traversal.

        Args:
            value: The field value (can be FHIRBaseModel, list, or other)
        """
        if isinstance(value, FHIRBaseModel):
            # Set _parent directly – no recursive descent needed.
            object.__setattr__(value, "_parent", self)
            object.__setattr__(value, "_index", None)
        elif isinstance(value, list):
            if not isinstance(value, FHIRList):
                # Wrap plain list in FHIRList to track future mutations.
                fhir_list = FHIRList(value, parent=self)
                for field_name in type(self).model_fields:
                    if getattr(self, field_name, None) is value:
                        object.__setattr__(self, field_name, fhir_list)
                        break
            else:
                # Re-point existing FHIRList at the current parent.
                value._parent = self
                value._propagate_context()

    def model_dump_json(self, *args, **kwargs):
        kwargs.update({"by_alias": True, "exclude_none": True})
        return super().model_dump_json(*args, **kwargs)

    def model_dump(self, *args, **kwargs):
        kwargs.update({"by_alias": True, "exclude_none": True})
        return super().model_dump(*args, **kwargs)

    def model_dump_xml(
        self,
        *,
        indent: int | None = None,
        ensure_ascii: bool = True,
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        exclude_unset: bool = False,
        exclude_none: bool = False,
        exclude_defaults: bool = False,
    ) -> str:
        """
        Serialize the FHIR resource to XML format according to FHIR specification.

        Args:
            indent: Indentation to use in the XML output. If None is passed, the output will be compact.
            ensure_ascii: Whether to escape non-ASCII characters.
            include: Fields to include in the output
            exclude: Fields to exclude from the output
            exclude_unset: Whether to exclude fields that were not explicitly set
            exclude_none: Whether to exclude fields with None values
            exclude_defaults: Whether to exclude fields with default values

        Returns:
            A string containing the XML representation of the FHIR resource
        """

        # Build the XML tree
        root = self.serialize_as_xml(
            name=self._type,
            include=include,
            exclude=exclude,
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
        )
        tree = xml.ElementTree(root)

        if indent is not None:
            # Optional: Add indentation for readability
            xml.indent(tree, space="  " * indent)

        # Convert to string; default_namespace adds xmlns="..." to the root element
        return xml.tostring(
            root,
            encoding="unicode" if ensure_ascii else "unicode",
            xml_declaration=True,
        )

    def serialize_as_xml(self, name: str, **kwargs) -> xml.Element:
        """Serialize this instance as an XML element (not a string)."""
        element = xml.Element(f"{{{XML_NAMESPACE}}}{name}")
        for subelement_name in self.model_dump(**kwargs):
            if subelement := getattr(self, subelement_name, None):
                if isinstance(subelement, FHIRBaseModel):
                    element.append(
                        subelement.serialize_as_xml(subelement_name, **kwargs)
                    )
                elif isinstance(subelement, (list, FHIRList)):
                    for item in subelement:
                        if isinstance(item, FHIRBaseModel):
                            element.append(
                                item.serialize_as_xml(subelement_name, **kwargs)
                            )

        # Handle special case for Extension.url which is an attribute, not a child element
        if self._type == "Extension" and getattr(self, "url", None) is not None:
            element.attrib["url"] = self.url  # type: ignore

        # Handle resource Id as an attribute, not a child element
        if getattr(self, "id", None) is not None:
            element.attrib["id"] = self.id  # type: ignore

        return element

    @staticmethod
    def _get_primitive_shadow_data(value: Any) -> "Any | None":
        """Return the _fieldname shadow dict/list for a primitive with id/extension, or None."""
        if isinstance(value, FHIRPrimitiveModel):
            shadow: dict = {}
            if getattr(value, "id", None) is not None:
                shadow["id"] = value.id
            ext = getattr(value, "extension", None)
            if ext:
                shadow["extension"] = [e.model_dump() for e in ext]
            return shadow if shadow else None
        elif isinstance(value, list):
            shadow_list = []
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

    def _serialize_fhir_field_polymorphically(self, value: Any) -> Any:
        """Serialize FHIR fields polymorphically to preserve runtime type information."""
        # Handle lists/sequences
        if isinstance(value, (list, tuple)):
            return [self._serialize_fhir_field_polymorphically(item) for item in value]

        # Handle FHIR models - serialize them using their runtime type
        if isinstance(value, FHIRBaseModel):
            # Use normal model_dump which includes polymorphic serialization
            # The polymorphic serialization has built-in recursion protection
            return value.model_dump()

        return value

    @classmethod
    def model_construct(cls, set_defaults=True, *args, **kwargs) -> Self:
        """
        Constructs a model without running validation, with an option to set default values for fields that have them defined.

        Args:
            set_defaults (bool): Optional, if `True`, sets default values for fields that have them defined (default is `True`).

        Returns:
            instance (Self): An instance of the model.
        """
        instance = super().model_construct(*args, **kwargs)

        if not set_defaults:
            # Still need to set context even if not setting defaults
            instance._set_resource_context()
            return instance

        # Set default values for fields that have them defined
        for field_name, field in cls.model_fields.items():
            if getattr(instance, field_name, None) is not None:
                continue
            if field.default not in (PydanticUndefined, None):
                setattr(instance, field_name, copy(field.default))
            elif field.default_factory not in (PydanticUndefined, None):
                setattr(instance, field_name, field.default_factory)

        # Set context after all fields are set
        instance._set_resource_context()
        return instance

    @classmethod
    def model_validate(
        cls,
        obj,
        *,
        strict=None,
        from_attributes=None,
        context=None,
        extra: ExtraValues | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self:
        """Override model_validate to provide default kwargs for FHIR resources."""
        if by_alias is not None:
            warnings.warn(
                "Fhircraft model_validate does not support by_alias.  Ignoring argument.",
                UserWarning,
            )
        if extra is not None:
            warnings.warn(
                "Fhircraft model_validate does not support extra. Ignoring argument.",
                UserWarning,
            )
        if by_name is not None:
            warnings.warn(
                "Fhircraft model_validate does not support by_name. Ignoring argument.",
                UserWarning,
            )
        instance = super().model_validate(
            obj, strict=strict, from_attributes=from_attributes, context=context
        )
        return instance

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
        """
        Override model_validate_json to provide default kwargs for FHIR resources.

        Args:
            json_data: JSON string to deserialize
            strict: Whether to validate strictly
            context: Additional context for validation
            extra: Extra parameters
        """
        if by_alias is not None:
            warnings.warn(
                "Fhircraft model_validate does not support by_alias.  Ignoring argument.",
                UserWarning,
            )
        if extra is not None:
            warnings.warn(
                "Fhircraft model_validate does not support extra. Ignoring argument.",
                UserWarning,
            )
        if by_name is not None:
            warnings.warn(
                "Fhircraft model_validate does not support by_name. Ignoring argument.",
                UserWarning,
            )
        instance = super().model_validate_json(
            json_data, strict=strict, context=context
        )

        # model_post_init already propagated _parent links bottom-up during
        # construction; no additional traversal is required here.
        return instance

    @classmethod
    def model_validate_xml(
        cls, xml_data: str, *, strict: bool | None = None, context: Any = None
    ) -> Self:
        """
        Deserialize FHIR XML data into a model instance.

        Args:
            xml_data: XML string to deserialize
            strict: Whether to validate strictly
            context: Additional context for validation

        Returns:
            An instance of the model populated from the XML data
        """
        from xml.etree.ElementTree import fromstring

        # Parse the XML
        root = fromstring(xml_data)

        # Convert XML to dictionary, passing model class for type checking
        data = cls._xml_element_to_dict(root, model_class=cls)

        # Use existing model_validate with the dictionary
        return cls.model_validate(data, strict=strict, context=context)

    @classmethod
    def _xml_element_to_dict(
        cls, element: xml.Element, model_class: Type | None = None
    ) -> Any:
        """
        Convert an XML element tree to a dictionary structure.

        Args:
            element: The XML element to convert
            model_class: The model class to use for type checking (optional)

        Returns:
            A dictionary representation of the XML element
        """
        from typing import get_origin, get_args

        # Strip namespace from tag
        tag = element.tag.split("}")[-1] if "}" in element.tag else element.tag

        # Start with an empty dict
        result = {}

        # Handle primitive value attribute
        if "value" in element.attrib:
            # This is a primitive field, return just the value
            value = element.attrib["value"]
            # Convert boolean strings
            if value == "true":
                return True
            elif value == "false":
                return False
            # Return as string - let Pydantic handle type conversion
            return value

        # Process child elements
        child_dict = {}
        for child in element:
            child_tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag

            # Determine the model class for the child if possible
            child_model_class = None
            if (
                model_class
                and hasattr(model_class, "model_fields")
                and child_tag in model_class.model_fields
            ):
                field_info = model_class.model_fields[child_tag]
                annotation = field_info.annotation
                # Try to extract the inner type from List[X] or Optional[List[X]]
                origin = get_origin(annotation)
                if origin is list:
                    args = get_args(annotation)
                    if args and hasattr(args[0], "model_fields"):
                        child_model_class = args[0]
                elif hasattr(annotation, "__args__"):
                    for arg in getattr(annotation, "__args__", []):
                        if get_origin(arg) is list:
                            args = get_args(arg)
                            if args and hasattr(args[0], "model_fields"):
                                child_model_class = args[0]
                            break
                        elif hasattr(arg, "model_fields"):
                            child_model_class = arg

            child_value = cls._xml_element_to_dict(child, model_class=child_model_class)

            # Handle repeated elements (lists)
            if child_tag in child_dict:
                # Convert to list if not already
                if not isinstance(child_dict[child_tag], list):
                    child_dict[child_tag] = [child_dict[child_tag]]
                child_dict[child_tag].append(child_value)
            else:
                child_dict[child_tag] = child_value

        # Merge child elements into result
        result.update(child_dict)

        # Post-process: Convert single values to lists if the model field expects a list
        # This handles cases like meta.profile which should always be a list
        if model_class and hasattr(model_class, "model_fields"):
            for field_name, field_value in list(result.items()):
                if field_name == "resourceType":
                    continue

                # Check if this field exists in the model and should be a list
                if field_name in model_class.model_fields:
                    field_info = model_class.model_fields[field_name]
                    annotation = field_info.annotation

                    # Check if the annotation is a List type
                    origin = get_origin(annotation)
                    # Handle Optional[List[...]] or List[...] or list[...]
                    if origin is list:
                        # Field expects a list, ensure value is a list
                        if not isinstance(field_value, list):
                            result[field_name] = [field_value]
                    elif hasattr(annotation, "__args__"):
                        # Handle Union types (Optional is Union[X, None])
                        for arg in getattr(annotation, "__args__", []):
                            if get_origin(arg) is list:
                                # Field expects a list, ensure value is a list
                                if not isinstance(field_value, list):
                                    result[field_name] = [field_value]
                                break

        # If result only contains resourceType and nothing else, just return the dict
        if len(result) == 1 and "resourceType" in result:
            return result

        return result if result else None

    @classmethod
    def _deserialize_polymorphically(cls, value: Any, base_type: Type) -> Any:
        """Deserialize a value using the best matching subclass.

        Handles:
        - Lists of items to deserialize recursively
        - FHIR instances (parent class instances) by converting to dict for re-validation
        - Dictionaries (potential FHIR objects) by trying subclasses
        """
        # Handle lists
        if isinstance(value, list):
            return [cls._deserialize_polymorphically(item, base_type) for item in value]

        # Handle FHIRBaseModel instances (e.g., parent class instances for profile fields)
        if isinstance(value, FHIRBaseModel):
            # If the value is already an instance of the target type or a subclass, return as-is
            if isinstance(value, base_type):
                return value

            # Convert the parent instance to a dictionary for re-validation against the target type
            # This allows Pydantic to validate and convert it properly
            value_dict = value.model_dump()
            # Recursively deserialize the dictionary
            return cls._deserialize_polymorphically(value_dict, base_type)

        # Handle dictionaries (potential FHIR objects)
        if isinstance(value, dict):
            # Find the best matching subclass
            subclasses = cls._get_all_subclasses(base_type)
            for subclass in subclasses:
                try:
                    # Try to instantiate with the subclass
                    # Recursion is now prevented at the field validator level
                    result = subclass.model_validate(
                        value,
                    )
                    return result
                except (ValidationError, ValueError, TypeError) as e:
                    # If specific class fails, continue trying other subclasses
                    continue

            # If no subclass worked, try the base type as fallback
            try:
                result = base_type.model_validate(
                    value,
                )
                return result
            except (ValidationError, ValueError, TypeError):
                # If base type also fails, return original value
                pass

        return value

    def model_copy(
        self, *, update: Mapping[str, Any] | None = None, deep: bool = False
    ) -> Self:
        """
        Override model_copy to reset parent context on copied instance.

        Args:
            update: Optional dict of field updates to apply to the copy
            deep: Whether to perform a deep copy

        Returns:
            A copied instance with reset parent context
        """
        # Avoid calling __deepcopy__ since model_copy(deep=True) calls it without memo
        # Instead, let Pydantic do the copy, then reset context
        copied: Self = BaseModel.model_copy(self, update=update, deep=deep)  # type: ignore
        # Reset context - copied instance should be a new root
        copied._set_resource_context()
        return copied

    def __deepcopy__(self, memo: dict[int, Any] | None = None) -> Self:
        """
        Override deepcopy to handle circular parent references properly.

        Args:
            memo: Dictionary for tracking already copied objects

        Returns:
            A deep copied instance with reset parent context
        """
        # Simple approach: serialize and deserialize to get a deep copy
        # This avoids recursion issues and properly handles all Pydantic internals
        data = self.model_dump()
        copied = type(self).model_validate(data)

        if memo is not None:
            # Register in memo
            memo[id(self)] = copied

        # Context is automatically set during model_validate via __init__
        return copied

    def __eq__(self, other):
        """
        Override equality to exclude tracking attributes from comparison.

        This prevents infinite recursion when comparing models with circular
        parent references via _parent and _root_resource.
        """
        if not isinstance(other, type(self)):
            return False

        # Compare only the actual field values, not tracking attributes
        # We use model_dump to get just the field data without private attributes
        return self.model_dump() == other.model_dump()

    @classmethod
    def model_construct_with_slices(cls, slice_copies: int = 9) -> object:
        """
        Constructs a model with sliced elements by creating empty slice instances based on the specified number of slice copies.
        The method iterates over the sliced elements of the class, generates slice resources, and sets them in the resource collection.

        Args:
            slice_copies (int): Optional, an integer specifying the number of copies for each slice (default is 9).

        Returns:
            instance (Self): An instance of the model with the sliced elements constructed.
        """
        from fhircraft.fhir.path.parser import fhirpath

        instance = super().model_construct()
        for element, slices in cls.get_sliced_elements().items():
            slice_resources = []
            for slice in slices:
                # Add empty slice instances
                slice_resources.extend(
                    [
                        slice.model_construct_with_slices()
                        for _ in range(min(slice.max_cardinality or 9999, slice_copies))
                    ]
                )
            # Set the whole list of slices in the resource
            collection = fhirpath.parse(element).__evaluate_wrapped(
                instance, create=True
            )
            [item.set_literal(slice_resources) for item in collection]
        return instance

    @classmethod
    def get_sliced_elements(cls) -> dict[str, list[type["FHIRSliceModel"]]]:
        """
        Get the sliced elements from the model fields and their extension fields.
        Sliced elements are filtered based on being instances of `FHIRSliceModel`.

        Returns:
            slices (dict): A dictionary with field names as keys and corresponding sliced elements as values.
        """
        # Get model elements' extension fields
        extensions = {
            f"{field_name}.extension": next(
                (
                    arg.model_fields.get("extension")
                    for arg in get_all_models_from_field(field)
                    if arg.model_fields.get("extension")
                ),
                None,
            )
            for field_name, field in cls.model_fields.items()
            if field_name != "extension"
        }
        fields = {
            **cls.model_fields,
            **extensions,
        }
        # Compile the sliced elements in the model
        return {
            field_name: slices
            for field_name, field in fields.items()
            if field
            and bool(
                slices := list(
                    get_all_models_from_field(field, issubclass_of=FHIRSliceModel)
                )
            )
        }

    @classmethod
    def clean_unusued_slice_instances(cls, resource):
        """
        Cleans up unused or incomplete slice instances within the given FHIR resource by iterating through the
        sliced elements of the class, identifying valid elements, and updating the resource with only the valid slices.
        """
        from fhircraft.fhir.path.parser import fhirpath

        # Remove unused/incomplete slices
        for element, slices in cls.get_sliced_elements().items():
            valid_elements = [
                col.value
                for col in fhirpath.parse(element).__evaluate_wrapped(
                    resource, create=True
                )
                if col.value is not None
            ]
            new_valid_elements = []
            if not valid_elements:
                continue
            for slice in slices:
                # Get all the elements that conform to this slice's definition
                sliced_entries = [
                    entry for entry in valid_elements if isinstance(entry, slice)
                ]
                for entry in sliced_entries:
                    if slice.get_sliced_elements():
                        entry = slice.clean_unusued_slice_instances(entry)
                    if (entry.is_FHIR_complete and entry.has_been_modified) or (
                        entry.is_FHIR_complete
                        and not entry.has_been_modified
                        and slice.min_cardinality > 0
                    ):
                        if entry not in new_valid_elements:
                            new_valid_elements.append(entry)
            # Set the new list with only the valid slices
            collection = fhirpath.parse(element).__evaluate_wrapped(
                resource, create=True
            )
            [col.set_literal(new_valid_elements) for col in collection]
        return resource

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


class FHIRPrimitiveModel(FHIRBaseModel):
    """
    Base class for FHIR primitive types.

    FHIR primitives are represented as Pydantic models with a single `value` field that holds the actual primitive value.
    This design allows us to attach extensions to primitive values while still treating them as simple types in most contexts.
    """

    _kind = "primitive-type"

    value: Any | None = Field(default=None, description="The actual value")

    @model_serializer
    def serialize_root_value(self) -> Any:
        if isinstance(self, FHIRPrimitiveModel):
            return self.value
        return self

    def serialize_as_json(self, name: str) -> dict:
        serialized = dict()
        if self.value:
            serialized[name] = self.value
        if self.id or self.extension:
            serialized[f"_{name}"] = {}
            if self.id is not None:
                serialized[f"_{name}"]["id"] = self.id
            if self.extension is not None:
                serialized[f"_{name}"]["extension"] = [
                    ext.model_dump() for ext in self.extension
                ]
        return serialized

    def serialize_as_xml(self, name: str, **kwargs) -> xml.Element:
        attributes = {}
        if self.value is not None:
            attributes["value"] = (
                str(self.value).lower()
                if isinstance(self.value, bool)
                else str(self.value)
            )
        if getattr(self, "id", None) is not None:
            attributes["id"] = self.id
        primitive = xml.Element(f"{{{XML_NAMESPACE}}}{name}", attrib=attributes)
        for ext in self.extension or []:
            primitive.append(ext.serialize_as_xml("extension", **kwargs))
        return primitive

    @model_validator(mode="before")
    @classmethod
    def coerce_root_value(cls, data: Any) -> Any:
        if isinstance(data, FHIRPrimitiveModel):
            return {"value": data.value}
        elif data is not None and not isinstance(data, (dict, BaseModel)):
            return {"value": data}
        return data

    def __init__(self, __value: Any | None = None, **data):
        if __value is not None:
            data.setdefault("value", __value)
        super().__init__(**data)

    def __getattr__(self, name: str):
        v = self.value
        if v is None:
            raise AttributeError(f"Cannot access '{name}' because value is None")
        return getattr(v, name)

    def __getitem__(self, key):
        v = self.value
        if v is None:
            raise TypeError("Cannot index into None value")
        return v[key]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, FHIRPrimitiveModel):
            return self.value == other.value
        return self.value == other

    def __gt__(self, other):
        return (
            self.value > other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value > other
        )

    def __rgt__(self, other):
        return (
            self.value < other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value < other
        )

    def __lt__(self, other):
        return (
            self.value < other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value < other
        )

    def __rlt__(self, other):
        return (
            self.value > other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value > other
        )

    def __ge__(self, other):
        return (
            self.value >= other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value >= other
        )

    def __rge__(self, other):
        return (
            self.value <= other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value <= other
        )

    def __le__(self, other):
        return (
            self.value <= other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value <= other
        )

    def __rle__(self, other):
        return (
            self.value >= other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value >= other
        )

    def __add__(self, other):
        return (
            self.value + other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value + other
        )

    def __radd__(self, other):
        return (
            other.value + self.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else other + self.value
        )

    def __sub__(self, other):
        return (
            self.value - other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value - other
        )

    def __rsub__(self, other):
        return (
            other.value - self.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else other - self.value
        )

    def __mul__(self, other):
        return (
            self.value * other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value * other
        )

    def __rmul__(self, other):
        return (
            self.value * other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value * other
        )

    def __truediv__(self, other):
        return (
            self.value / other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value / other
        )

    def __rtruediv__(self, other):
        return (
            other.value / self.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else other / self.value
        )

    def __mod__(self, other):
        return (
            self.value % other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value % other
        )

    def __rmod__(self, other):
        return (
            other.value % self.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else other % self.value
        )

    def __floordiv__(self, other):
        return (
            self.value // other.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else self.value // other
        )

    def __rfloordiv__(self, other):
        return (
            other.value // self.value  # type: ignore
            if isinstance(other, FHIRPrimitiveModel)
            else other // self.value
        )

    def __neg__(self):
        return -self.value  # type: ignore

    def __pos__(self):
        return +self.value  # type: ignore

    def __abs__(self):
        return abs(self.value)  # type: ignore

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return str(self.value) if self.value is not None else ""

    def __repr__(self) -> str:
        return repr(self.value)


class StringBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR string types
    """

    _kind = "string"
    value: str | None = None


class BooleanBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR boolean types
    """

    _kind = "boolean"
    value: bool | None = None


class DecimalBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR decimal types
    """

    _kind = "decimal"
    value: float | None = None


class DateBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR date types
    """

    _kind = "date"
    value: str | None = None


class DateTimeBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR dateTime types
    """

    _kind = "dateTime"
    value: str | None = None


class TimeBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR time types
    """

    _kind = "time"
    value: str | None = None


class InstantBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR instant types
    """

    _kind = "instant"
    value: str | None = None


class Base64BinaryBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR base64Binary types
    """

    _kind = "base64Binary"
    value: str | None = None


class UriBase(StringBase):
    """
    A release-independent base metaclass for FHIR uri types
    """

    _kind = "uri"


class UrlBase(UriBase):
    """
    A release-independent base metaclass for FHIR url types
    """

    _kind = "url"


class CanonicalBase(UriBase):
    """
    A release-independent base metaclass for FHIR canonical types
    """

    _kind = "canonical"


class OidBase(UriBase):
    """
    A release-independent base metaclass for FHIR oid types
    """

    _kind = "oid"


class UuidBase(UriBase):
    """
    A release-independent base metaclass for FHIR uuid types
    """

    _kind = "uuid"


class CodeBase(StringBase):
    """
    A release-independent base metaclass for FHIR code types
    """

    _kind = "code"


class IdBase(StringBase):
    """
    A release-independent base metaclass for FHIR id types
    """

    _kind = "id"


class MarkdownBase(StringBase):
    """
    A release-independent base metaclass for FHIR markdown types
    """

    _kind = "markdown"


class XhtmlBase(StringBase):
    """
    A release-independent base metaclass for FHIR xhtml types
    """

    _kind = "xhtml"


class IntegerBase(FHIRPrimitiveModel):
    """
    A release-independent base metaclass for FHIR integer types
    """

    _kind = "integer"
    value: int | None = None


class PositiveIntBase(IntegerBase):
    """
    A release-independent base metaclass for FHIR positiveInt types
    """

    _kind = "positiveInt"


class UnsignedIntBase(IntegerBase):
    """
    A release-independent base metaclass for FHIR unsignedInt types
    """

    _kind = "unsignedInt"


class Integer64Base(IntegerBase):
    """
    A release-independent base metaclass for FHIR integer64 types (R5)
    """

    _kind = "integer64"


class FHIRSliceModel(FHIRBaseModel):
    """
    Base class for representation of FHIR profiled slices as Pydantic objects.

    Expands the `FHIRBaseModel` class with slice-specific methods.
    """

    min_cardinality: ClassVar[int] = 0
    max_cardinality: ClassVar[int | None] = None

    @property
    def is_FHIR_complete(self):
        """
        Validates if the FHIR model is complete by attempting to validate the model dump.
        Returns `True` if the model is complete, `False` otherwise.
        """
        model = self.__class__
        try:
            model.model_validate(self.model_dump())
            return True
        except ValidationError:
            return False

    @property
    def has_been_modified(self):
        """
        Checks if the FHIRSliceModel instance has been modified by comparing it with a new instance constructed with slices.
        Returns `True` if the instance has been modified, `False` otherwise.
        """
        return self != self.__class__.model_construct_with_slices()


class FHIRList(list):
    """
    Custom list wrapper that maintains parent context on mutations.

    This list automatically propagates _parent, _root_resource, _resource, and _index context
    to FHIRBaseModel items when they are added via append, extend, insert, or __setitem__.
    """

    def __init__(self, items=None, parent=None, root=None, resource=None):
        """Initialize FHIRList with items and context.

        ``root`` and ``resource`` are accepted for backwards-compatibility but
        are no longer stored; they are resolved lazily via ``_parent`` on items.
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

    def append(self, item):
        """Append item and propagate context."""
        super().append(item)
        if isinstance(item, FHIRBaseModel):
            object.__setattr__(item, "_parent", self._parent)
            object.__setattr__(item, "_index", len(self) - 1)

    def extend(self, items):
        """Extend list and propagate context to new items."""
        start_index = len(self)
        super().extend(items)
        for offset, item in enumerate(items):
            if isinstance(item, FHIRBaseModel):
                object.__setattr__(item, "_parent", self._parent)
                object.__setattr__(item, "_index", start_index + offset)

    def insert(self, index, item):
        """Insert item and propagate context."""
        super().insert(index, item)
        if isinstance(item, FHIRBaseModel):
            object.__setattr__(item, "_parent", self._parent)
            object.__setattr__(item, "_index", index)
        # Re-index all items after insertion point
        for i in range(index + 1, len(self)):
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
