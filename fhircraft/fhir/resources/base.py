from copy import copy
import enum
from functools import lru_cache
import json
import threading
import warnings
from typing import Any, ClassVar, Union, Dict, List, Type, get_origin, get_args, Literal
from typing_extensions import Self
from xml.etree.ElementTree import Element as ET_Element, tostring, SubElement
from xml.dom import minidom
from pydantic.main import IncEx
from pydantic.config import ExtraValues
from pydantic import (
    BaseModel,
    ConfigDict,
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


# Thread-local context to track polymorphic operations to prevent recursion
_polymorphic_context = threading.local()


class FhirBaseModelKind(str, enum.Enum):
    """Enumeration of StructureMap model modes."""

    LOGICAL = "logical"
    PRIMITIVE = "primitive"
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
        FhirBaseModelKind | Literal["primitive", "complex-type", "resource", "logical"]
    ] = "logical"
    _type: ClassVar[str]
    _canonical_url: ClassVar[str | None]

    # Configuration for polymorphic behavior
    _enable_polymorphic_serialization: ClassVar[bool] = True
    _enable_polymorphic_deserialization: ClassVar[bool] = True

    # Parent tracking attributes
    _parent: Union["FHIRBaseModel", None] = PrivateAttr(default=None)
    _root_resource: Union["FHIRBaseModel", None] = PrivateAttr(default=None)
    _resource: Union["FHIRBaseModel", None] = PrivateAttr(default=None)
    _index: Union[int, None] = PrivateAttr(default=None)

    @property
    def _is_resource(self) -> bool:
        """Check if this instance is a FHIR resource."""
        return (
            self._kind == FhirBaseModelKind.RESOURCE
            or self._kind == FhirBaseModelKind.LOGICAL
        )

    def model_post_init(self, context: Any) -> None:
        """Initialize model and set up parent tracking."""
        # After construction, propagate context to all nested fields
        self._set_resource_context()

    @model_validator(mode="before")
    @classmethod
    def _validate_resource_type(cls, data: Any) -> Any:
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

        # Only apply to FHIR fields
        if (
            base_type != object
            and hasattr(base_type, "__mro__")
            and issubclass(base_type, FHIRBaseModel)
        ):
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
                # If polymorphic deserialization fails, return original value
                return value
            finally:
                # Always remove from stack when done
                stack.discard(context_key)

        return value

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

            # Apply polymorphic serialization to FHIR fields
            for field_name, field_info in self.__class__.model_fields.items():
                if field_name in data:
                    value = getattr(self, field_name, None)
                    if value is not None:
                        base_type = self._get_field_base_type(field_info)
                        if (
                            base_type != object
                            and hasattr(base_type, "__mro__")
                            and issubclass(base_type, FHIRBaseModel)
                        ):
                            # Apply polymorphic serialization to this field
                            data[field_name] = (
                                self._serialize_fhir_field_polymorphically(value)
                            )
            if (
                self._is_resource
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
        Set parent and root resource context for this instance.

        Args:
            parent: The parent FHIRBaseModel instance (if this is a nested field)
            root: The root resource instance (top-level resource)
            resource: The immediate parent resource instance
            index: The index of this instance in a list (if applicable)
        """
        # Set parent
        object.__setattr__(self, "_parent", parent)

        # Set index
        object.__setattr__(self, "_index", index)

        # Set root: if root is provided, use it; otherwise if parent exists, use parent's root; otherwise self is root
        if root is not None:
            object.__setattr__(self, "_root_resource", root)
        elif parent is not None and hasattr(parent, "_root_resource"):
            object.__setattr__(
                self, "_root_resource", getattr(parent, "_root_resource", parent)
            )
        else:
            # This instance is the root
            object.__setattr__(self, "_root_resource", self)

        # Set resource: if this instance is a resource, it becomes the _resource
        # otherwise inherit from parent or explicit resource parameter
        if self._is_resource:
            # This is a resource or logical model itself
            object.__setattr__(self, "_resource", self)
        elif resource is not None:
            # Explicit resource provided
            object.__setattr__(self, "_resource", resource)
        elif parent is not None and hasattr(parent, "_resource"):
            # Inherit resource from parent
            object.__setattr__(self, "_resource", getattr(parent, "_resource", None))
        else:
            # No resource context
            object.__setattr__(self, "_resource", None)

        # Propagate context to all nested fields
        for field_name in self.__class__.model_fields:
            value = getattr(self, field_name, None)
            if value is not None:
                self._propagate_context_to_value(value)

    def _propagate_context_to_value(self, value: Any):
        """
        Propagate parent context to a field value.

        Args:
            value: The field value (can be FHIRBaseModel, list, or other)
        """
        if isinstance(value, FHIRBaseModel):
            # Single FHIR model - set context
            # Determine resource: if self is a resource, use self; otherwise use self's _resource
            resource_context = (
                self if self._is_resource else getattr(self, "_resource", None)
            )
            value._set_resource_context(
                parent=self,
                root=getattr(self, "_root_resource", self),
                resource=resource_context,
                index=None,
            )
        elif isinstance(value, list):
            # Convert to FHIRList if not already
            if not isinstance(value, FHIRList):
                # Replace the list with FHIRList
                resource_context = (
                    self if self._is_resource else getattr(self, "_resource", None)
                )
                fhir_list = FHIRList(
                    value,
                    parent=self,
                    root=getattr(self, "_root_resource", self),
                    resource=resource_context,
                )
                # Find which field this list belongs to and replace it
                for field_name in self.__class__.model_fields:
                    if getattr(self, field_name, None) is value:
                        object.__setattr__(self, field_name, fhir_list)
                        break
            else:
                # Update context of existing FHIRList
                resource_context = (
                    self if self._is_resource else getattr(self, "_resource", None)
                )
                value._parent = self
                value._root = getattr(self, "_root_resource", self)
                value._resource = resource_context
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
        # Register the FHIR namespace with empty prefix (default namespace)
        from xml.etree.ElementTree import register_namespace

        register_namespace("", "http://hl7.org/fhir")

        # Determine the root element name BEFORE filtering (so exclude_defaults doesn't affect it)
        if self._is_resource:
            root_name = self._type
        else:
            root_name = self.__class__.__name__

        # Get the data as a dictionary with filtering options
        data = self.model_dump(
            by_alias=True,
            include=include,
            exclude=exclude,
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
        )

        # Create the root element with FHIR namespace using Clark notation
        # This creates the element in the namespace but serializes with xmlns attribute
        root = ET_Element(f"{{http://hl7.org/fhir}}{root_name}")

        # Build the XML tree
        self._build_xml_element(root, data, root_name)

        # Convert to string with encoding option
        encoding = "unicode" if ensure_ascii else "unicode"
        xml_str = tostring(root, encoding=encoding)

        # Pretty print if requested
        if indent is not None:
            try:
                dom = minidom.parseString(xml_str)
                xml_str = dom.toprettyxml(indent="  " * indent)
                # Remove extra blank lines and XML declaration if not needed
                lines = [line for line in xml_str.split("\n") if line.strip()]
                # Keep XML declaration
                xml_str = "\n".join(lines)
            except Exception:
                # If pretty printing fails, return the raw XML
                pass

        return xml_str

    def _build_xml_element(
        self, parent: ET_Element, data: Dict[str, Any], parent_name: str | None = None
    ):
        """
        Recursively build XML elements from the data dictionary.

        Args:
            parent: The parent XML element
            data: The data dictionary to serialize
            parent_name: The name of the parent element (used for context)
        """
        for field_name, value in data.items():
            if value is None:
                continue

            # Skip resourceType as it's already the root element
            if field_name == "resourceType":
                continue

            # Handle primitive extension fields (fields ending with _ext or starting with _)
            if field_name.endswith("_ext") or (
                field_name.startswith("_") and field_name != "_value"
            ):
                # These are handled with their corresponding primitive fields
                continue

            # Get the actual field name (without _ext suffix)
            base_field_name = field_name

            # Check if this field has an extension companion
            ext_field_name = f"{field_name}_ext"
            ext_data = data.get(ext_field_name) if ext_field_name in data else None

            # Handle lists
            if isinstance(value, list):
                for item in value:
                    self._add_field_element(parent, base_field_name, item, ext_data)
            else:
                self._add_field_element(parent, base_field_name, value, ext_data)

    def _add_field_element(
        self, parent: ET_Element, field_name: str, value: Any, ext_data: Any = None
    ):
        """
        Add a field element to the parent XML element.

        Args:
            parent: The parent XML element
            field_name: The name of the field
            value: The value of the field
            ext_data: Extension data for primitive fields (if any)
        """
        if value is None:
            return

        # Create the field element with namespace
        field_elem = SubElement(parent, f"{{http://hl7.org/fhir}}{field_name}")

        # Handle different value types
        if isinstance(value, dict):
            # For resources in arrays (like contained), wrap in proper element
            if isinstance(value, FHIRBaseModel) and value._is_resource:
                # Create a child element with the resource type name
                resource_elem = SubElement(
                    field_elem, f"{{http://hl7.org/fhir}}{value._type}"
                )
                self._build_xml_element(resource_elem, value, value._type)
            else:
                # Complex type - build directly into field_elem
                self._build_xml_element(field_elem, value, field_name)

        elif isinstance(value, (str, int, float, bool)):
            # Primitive type - use value attribute
            field_elem.set(
                "value", str(value).lower() if isinstance(value, bool) else str(value)
            )

            # Add extension elements if present
            if ext_data and isinstance(ext_data, dict):
                self._build_xml_element(field_elem, ext_data, field_name)
        else:
            # Other types - convert to string
            field_elem.set("value", str(value))

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
        cls, obj, *, strict=None, from_attributes=None, context=None
    ) -> Self:
        """Override model_validate to provide default kwargs for FHIR resources."""
        instance = super().model_validate(
            obj, strict=strict, from_attributes=from_attributes, context=context
        )

        # Set up resource context for the root instance if it's a resource
        if instance._is_resource:
            instance._set_resource_context(
                parent=None, root=instance, resource=instance
            )

        return instance

    @classmethod
    def model_validate_json(
        cls,
        json_data: str,
        *,
        strict: bool = False,
        context: Any = None,
        extra: ExtraValues | None = None,
    ) -> Self:
        """
        Override model_validate_json to provide default kwargs for FHIR resources.

        Args:
            json_data: JSON string to deserialize
            strict: Whether to validate strictly
            context: Additional context for validation
            extra: Extra parameters
        """
        instance = super().model_validate_json(
            json_data, strict=strict, context=context
        )

        # Set up resource context for the root instance if it's a resource
        if instance._is_resource:
            instance._set_resource_context(
                parent=None, root=instance, resource=instance
            )

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
        cls, element: ET_Element, model_class: Type | None = None
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
        """Deserialize a value using the best matching subclass."""
        # Handle lists
        if isinstance(value, list):
            return [cls._deserialize_polymorphically(item, base_type) for item in value]

        # Handle dictionaries (potential FHIR objects)
        if isinstance(value, dict):
            # Find the best matching subclass
            subclasses = cls._get_all_subclasses(base_type)
            for subclass in subclasses:
                try:
                    # Try to instantiate with the subclass
                    # Recursion is now prevented at the field validator level
                    result = subclass.model_validate(value)
                    return result
                except (ValidationError, ValueError, TypeError):
                    # If specific class fails, continue trying other subclasses
                    continue

            # If no subclass worked, try the base type as fallback
            try:
                result = base_type.model_validate(value)
                return result
            except (ValidationError, ValueError, TypeError):
                # If base type also fails, return original value
                pass

        return value

    def model_copy(
        self, *, update: dict[str, Any] | None = None, deep: bool = False
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

    def __deepcopy__(self, memo: dict) -> Self:
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
        copied = self.__class__.model_validate(data)

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
        if not isinstance(other, self.__class__):
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
        from fhircraft.fhir.path import fhirpath

        instance = super().model_construct()
        for element, slices in cls.get_sliced_elements().items():
            slice_resources = []
            for slice in slices:
                # Add empty slice instances
                slice_resources.extend(
                    [
                        slice.model_construct_with_slices()
                        for _ in range(min(slice.max_cardinality, slice_copies))
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
        from fhircraft.fhir.path import fhirpath

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
        for fieldname in sorted(self.model_fields_set or self.__class__.model_fields):
            value = getattr(self, fieldname)
            if isinstance(value, BaseModel):
                value = repr(value)
            elif isinstance(value, str):
                value = f'"{value}"'
            repr_args.append(f"{fieldname}={value}")
        return repr_args

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(self._get_repr_args())})"


class FHIRSliceModel(FHIRBaseModel):
    """
    Base class for representation of FHIR profiled slices as Pydantic objects.

    Expands the `FHIRBaseModel` class with slice-specific methods.
    """

    min_cardinality: ClassVar[int] = 0
    max_cardinality: ClassVar[int] = 1

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
        """Initialize FHIRList with items and context."""
        super().__init__(items or [])
        self._parent = parent
        self._root = root
        self._resource = resource
        self._propagate_context()

    def _propagate_context(self):
        """Propagate context to all current items and their nested children."""
        # Only propagate if we have a parent (otherwise we don't have context yet)
        if self._parent is None:
            return

        for index, item in enumerate(self):
            if isinstance(item, FHIRBaseModel):
                item._set_resource_context(
                    parent=self._parent,
                    root=self._root,
                    resource=self._resource,
                    index=index,
                )

    def append(self, item):
        """Append item and propagate context."""
        super().append(item)
        if isinstance(item, FHIRBaseModel):
            # Index is the last position
            index = len(self) - 1
            item._set_resource_context(
                parent=self._parent,
                root=self._root,
                resource=self._resource,
                index=index,
            )

    def extend(self, items):
        """Extend list and propagate context to new items."""
        start_index = len(self)
        super().extend(items)
        # Only propagate to newly added items
        for offset, item in enumerate(items):
            if isinstance(item, FHIRBaseModel):
                item._set_resource_context(
                    parent=self._parent,
                    root=self._root,
                    resource=self._resource,
                    index=start_index + offset,
                )

    def insert(self, index, item):
        """Insert item and propagate context."""
        super().insert(index, item)
        if isinstance(item, FHIRBaseModel):
            item._set_resource_context(
                parent=self._parent,
                root=self._root,
                resource=self._resource,
                index=index,
            )
        # Re-index all items after insertion point
        for i in range(index + 1, len(self)):
            if isinstance(self[i], FHIRBaseModel):
                object.__setattr__(self[i], "_index", i)

    def __setitem__(self, index, item):
        """Set item and propagate context."""
        super().__setitem__(index, item)
        if isinstance(item, FHIRBaseModel):
            # Handle single item
            if isinstance(index, int):
                item._set_resource_context(
                    parent=self._parent,
                    root=self._root,
                    resource=self._resource,
                    index=index,
                )
            else:
                # Handle slice assignment - can't easily track indices
                # So we re-propagate to all items
                self._propagate_context()
        elif isinstance(item, list):
            # Handle slice assignment like lst[1:3] = [...]
            # Re-propagate to all items to fix indices
            self._propagate_context()
