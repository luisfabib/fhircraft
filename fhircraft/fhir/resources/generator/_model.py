import ast
import functools
import inspect
import re
import textwrap
from types import FunctionType
from enum import Enum
from typing import Any, Callable

from pydantic import AliasChoices, BaseModel, Field
from pydantic.fields import FieldInfo
from pydantic._internal._decorators import (
    Decorator,
    FieldValidatorDecoratorInfo,
    ModelValidatorDecoratorInfo,
)
from pydantic_core import PydanticUndefined

from fhircraft.fhir.resources.base.models import (
    FHIRSliceModel,
    FHIRBaseModel,
)
from fhircraft.fhir.resources.base.primitives import FHIRPrimitiveModel
from ._annotations import AnnotationSerializer
from ._imports import ImportTracker

from ._schemas import (
    GeneratorFieldValidator,
    GeneratorModel,
    GeneratorModelField,
    GeneratorModelMeta,
    GeneratorModelProperty,
    GeneratorModelValidator,
    GeneratorPartialFunction,
)

PYDANTIC_FIELD_PARAMETERS = inspect.signature(Field).parameters.keys()


class ModelSerializer:
    """Walks pydantic model classes and extracts structured data for code generation."""

    def __init__(
        self,
        tracker: ImportTracker,
    ) -> None:
        self._tracker = tracker
        self._annotations = AnnotationSerializer(tracker=self._tracker, serializer=self)

    def serialize(self, model: type[BaseModel]) -> GeneratorModel:
        """Extract all code-generation data from a model class into self.data."""

        if not issubclass(model, BaseModel):
            raise ValueError(f"Model '{model.__name__}' is not a Pydantic model.")

        serialized_data = GeneratorModel(
            name=model.__name__, docstring=inspect.getdoc(model)
        )

        # Serialize base classes and track imports for all bases
        for base in model.__bases__:
            serialized_data.bases.append(self._serialize_base(base))

        # Serialize FHIR metadata
        if issubclass(model, (FHIRBaseModel, FHIRSliceModel)):
            serialized_data.meta = self._serialize_metadata(model)

        # Serialize model fields
        for field_name, field_info in model.model_fields.items():
            serialized_field = self._serialize_field(field_name, field_info)
            # Check if the field is inherited from a base class and has the same implementation
            for base in model.__mro__[1:]:
                if issubclass(base, BaseModel):
                    if field_name in base.model_fields:
                        inherited_field = self._serialize_field(
                            field_name, base.model_fields[field_name], track=False
                        )
                        if serialized_field == inherited_field:
                            break
            else:
                # Add the property to the serialized data if it is not inherited or has a different implementation
                serialized_data.fields.append(serialized_field)

        # Serialize model properties
        for name, prop in model.__dict__.items():
            if isinstance(prop, property):
                serialized_property = self._serialize_property(name, prop)
                # Check if the property is inherited from a base class and has the same implementation
                for base in model.__mro__[1:]:
                    if name in base.__dict__:
                        inherited_property = self._serialize_property(
                            name, prop, track=False
                        )
                        if serialized_property == inherited_property:
                            break
                else:
                    # Add the property to the serialized data if it is not inherited or has a different implementation
                    serialized_data.properties.append(serialized_property)

        # Serialize field validators
        for name, validator in model.__pydantic_decorators__.field_validators.items():
            serialized_validator = self._serialize_field_validator(name, validator)
            # Check if the validator is inherited from a base class and has the same implementation
            for base in model.__mro__[1:]:
                if name in base.__dict__:
                    inherited_validator = self._serialize_field_validator(
                        name, validator, track=False
                    )
                    if serialized_validator == inherited_validator:
                        break
            else:
                self._tracker.track("pydantic", "field_validator")
                # Add the validator to the serialized data if it is not inherited or has a different implementation
                serialized_data.field_validators.append(serialized_validator)

        # Serialize model validators
        for name, validator in model.__pydantic_decorators__.model_validators.items():
            serialized_validator = self._serialize_model_validator(name, validator)
            # Check if the validator is inherited from a base class and has the same implementation
            for base in model.__mro__[1:]:
                if name in base.__dict__:
                    inherited_validator = self._serialize_model_validator(
                        name, validator, track=False
                    )
                    if serialized_validator == inherited_validator:
                        break
            else:
                self._tracker.track("pydantic", "model_validator")
                # Add the validator to the serialized data if it is not inherited or has a different implementation
                serialized_data.model_validators.append(serialized_validator)

        return serialized_data

    def _serialize_base(self, base: type) -> str:
        # Get the name of the base class
        name = getattr(base, "__name__", None)
        if not name:
            raise ValueError(f"Base class '{base}' has no __name__ attribute.")
        # Get the module name for the base class
        module = self._tracker.get_shortest_public_path(base)
        if not module:
            raise ValueError(
                f"Cannot determine module for base class '{base.__name__}'."
            )
        # If base is a built-in Fhircraft FHIR model, track it as aliassed import
        if module.startswith("fhircraft"):
            if module.startswith("fhircraft.fhir.resources.datatypes"):
                self._tracker.track_alias(module, "fhir")
                name = f"fhir.{name}"
            elif module.startswith("fhircraft.fhir.resources.factory"):
                self._tracker.track_generated_model(self.serialize(base))
            else:
                self._tracker.track(module, name)
        # For any custom Pydantic models, serialize them and add to the generator's module models list
        elif issubclass(base, BaseModel) and base is not BaseModel:
            self._tracker.track_generated_model(self.serialize(base))
        else:
            self._tracker.track(module, base.__name__)
        return name

    def _serialize_metadata(
        self, model: type[FHIRSliceModel | FHIRBaseModel]
    ) -> GeneratorModelMeta:
        meta = GeneratorModelMeta()
        # Extract slicing cardinality if the model is a slice model
        if issubclass(model, FHIRSliceModel):
            meta.min_cardinality = model.min_cardinality
            meta.max_cardinality = model.max_cardinality
            self._tracker.track("typing", "ClassVar")

        # Extract FHIR metdata if the model is a FHIR model
        elif issubclass(model, FHIRBaseModel):
            for attr in (
                "_fhir_release",
                "_canonical_url",
                "_kind",
                "_type",
                "_abstract",
            ):
                value = getattr(model, attr, None)
                # Set the values onlyz if they have not been inherited from a base class
                if value is not None and not next(
                    (b for b in model.__bases__ if getattr(b, attr, None) == value),
                    None,
                ):
                    setattr(
                        meta,
                        attr.lstrip("_"),
                        self._serialize_value(value),
                    )
        return meta

    def _serialize_field(
        self, name: str, field: FieldInfo, track: bool = True
    ) -> GeneratorModelField:
        """Extract all code-generation data from a model field."""

        if track:
            self._tracker.track("pydantic", "Field")

        arguments = {}
        # Exctract direct Field attributes explicitly set (e.g. description, alias, default)
        for attr in getattr(field, "_attributes_set", set()):
            if attr == "annotation":
                continue
            value = getattr(field, attr, PydanticUndefined)
            if value is not PydanticUndefined and attr in PYDANTIC_FIELD_PARAMETERS:
                arguments[attr] = self._serialize_value(value)

        # Extract constraints stored inside item.metadata (e.g. union_mode, gt, lt, pattern)
        for meta in getattr(field, "metadata", []):
            # Handle internal Pydantic metadata containers like _PydanticGeneralMetadata
            for attr in dir(meta):
                if (
                    not attr.startswith("_")
                    and attr in PYDANTIC_FIELD_PARAMETERS
                    and (value := getattr(meta, attr)) is not PydanticUndefined
                ):
                    arguments[attr] = self._serialize_value(value)

        # Serialize the field's annotation as a string
        annotation = self._annotations.serialize(field.annotation)

        # Special case: If the field is Optional and has a min_length of 0, remove the min_length constraint (redundant)
        if "Optional" in annotation and arguments.get("min_length") == str(0):
            arguments.pop("min_length")
        # Special case: Remove trailing period from description if present (for better comparisons)
        if arguments.get("description", "").endswith('."'):
            arguments["description"] = arguments["description"][:-2] + '"'

        return GeneratorModelField(
            name=name,
            annotation=annotation,
            arguments=arguments,
        )

    def _serialize_property(
        self, name: str, property: property, track: bool = True
    ) -> GeneratorModelProperty:
        if not property.fget:
            raise ValueError(f"Property {name} has no getter.")
        if isinstance(property.fget, functools.partial):
            module = self._tracker.get_shortest_public_path(property.fget.func)
            if module and track:
                self._tracker.track(module, property.fget.func.__name__)
            return GeneratorModelProperty(
                name=name,
                partial=GeneratorPartialFunction(
                    name=property.fget.func.__name__,
                    arguments=[self._serialize_value(a) for a in property.fget.args],
                    keywords={
                        k: self._serialize_value(v)
                        for k, v in property.fget.keywords.items()
                    },
                ),
            )
        # Case 2: In-line function or classmethod (captures actual python source code)
        elif inspect.isfunction(property.fget) or isinstance(
            property.fget, FunctionType
        ):
            try:
                raw_code = inspect.getsource(property.fget)
                source_code = textwrap.dedent(raw_code).strip()
                # Validate that the source code is valid Python
                ast.parse(source_code)
            except (OSError, TypeError):
                raise ValueError(
                    f"Cannot retrieve source code for property '{name}'. "
                    "Ensure that the function is defined in a module and not in an interactive environment."
                )
            except SyntaxError as e:
                raise ValueError(
                    f"Syntax error in retrieved source code for property '{name}': {e}"
                )

            return GeneratorModelProperty(
                name=name,
                source=source_code,
            )
        else:
            raise ValueError(
                f"Property {name} is not a valid function. Expected FunctionType or functools.partial, got {type(property.fget)}."
            )

    def __extract_partial_helper_function(
        self, partial_func: functools.partial, track: bool = True
    ) -> Callable[[Any], Any]:
        helper_func = partial_func.func
        module = self._tracker.get_shortest_public_path(helper_func)
        if module and track:
            self._tracker.track(module, helper_func.__name__)
        return helper_func

    def _serialize_field_validator(
        self,
        name: str,
        validator: Decorator[FieldValidatorDecoratorInfo],
        track: bool = True,
    ) -> GeneratorFieldValidator:
        decorated_method = validator.func
        validator_func = getattr(decorated_method, "__func__", decorated_method)
        # Case 1: Dynamic partial function (delegates execution to another callable)
        if isinstance(validator_func, functools.partial):
            helper_func = self.__extract_partial_helper_function(
                validator_func, track=track
            )
            return GeneratorFieldValidator(
                name=name,
                mode=validator.info.mode,
                fields=validator.info.fields,
                check_fields=validator.info.check_fields,
                partial=GeneratorPartialFunction(
                    name=helper_func.__name__,
                    arguments=[self._serialize_value(a) for a in validator_func.args],
                    keywords={
                        k: self._serialize_value(v)
                        for k, v in validator_func.keywords.items()
                    },
                ),
            )

        # Case 2: In-line function or classmethod (captures actual python source code)
        elif inspect.isfunction(validator_func) or isinstance(
            validator_func, FunctionType
        ):
            try:
                raw_code = inspect.getsource(validator_func)
                source_code = textwrap.dedent(raw_code).strip()
                # Validate that the source code is valid Python
                ast.parse(source_code)
            except (OSError, TypeError):
                raise ValueError(
                    f"Cannot retrieve source code for field validator '{name}'. "
                    "Ensure that the function is defined in a module and not in an interactive environment."
                )
            except SyntaxError as e:
                raise ValueError(
                    f"Syntax error in retrieved source code for field validator '{name}': {e}"
                )

            return GeneratorFieldValidator(
                name=name,
                mode=validator.info.mode,
                fields=validator.info.fields,
                check_fields=validator.info.check_fields,
                source=source_code,
            )
        else:
            raise ValueError(
                f"Field validator {name} is not a valid function. Expected FunctionType or functools.partial, got {type(validator_func)}."
            )

    def _serialize_model_validator(
        self,
        name: str,
        validator: Decorator[ModelValidatorDecoratorInfo],
        track: bool = True,
    ) -> GeneratorModelValidator:
        decorated_method = validator.func
        validator_func = getattr(decorated_method, "__func__", decorated_method)
        # Case 1: Dynamic partial function (delegates execution to another callable)
        if isinstance(validator_func, functools.partial):
            helper_func = self.__extract_partial_helper_function(
                validator_func, track=track
            )
            return GeneratorModelValidator(
                name=name,
                mode=validator.info.mode,
                partial=GeneratorPartialFunction(
                    name=helper_func.__name__,
                    arguments=[self._serialize_value(a) for a in validator_func.args],
                    keywords={
                        k: self._serialize_value(v)
                        for k, v in validator_func.keywords.items()
                    },
                ),
            )
        # Case 2: In-line function or classmethod (captures actual python source code)
        elif inspect.isfunction(validator_func) or isinstance(
            validator_func, FunctionType
        ):
            try:
                raw_code = inspect.getsource(validator_func)
                source_code = textwrap.dedent(raw_code).strip()
                # Validate that the source code is valid Python
                ast.parse(source_code)
            except (OSError, TypeError):
                raise ValueError(
                    f"Cannot retrieve source code for field validator '{name}'. "
                    "Ensure that the function is defined in a module and not in an interactive environment."
                )
            except SyntaxError as e:
                raise ValueError(
                    f"Syntax error in retrieved source code for field validator '{name}': {e}"
                )

            return GeneratorModelValidator(
                name=name,
                mode=validator.info.mode,
                source=source_code,
            )
        else:
            raise ValueError(
                f"Model validator {name} is not a valid function. Expected FunctionType or functools.partial, got {type(validator_func)}."
            )

    def _serialize_value(self, value: Any) -> str:
        """Serialize a value for code generation, handling special cases."""
        if isinstance(value, type):
            return self._annotations.serialize(value)
        elif isinstance(value, bool):
            return "True" if value else "False"
        elif isinstance(value, list):
            return "[" + ", ".join(self._serialize_value(v) for v in value) + "]"
        elif isinstance(value, tuple):
            return "(" + ", ".join(self._serialize_value(v) for v in value) + ")"
        elif isinstance(value, dict):
            items = ", ".join(
                f"{self._serialize_value(k)}: {self._serialize_value(v)}"
                for k, v in value.items()
            )
            return "{" + items + "}"
        elif isinstance(value, Enum):
            self._tracker.track(value.__class__.__module__, value.__class__.__name__)
            return f"{value.__class__.__name__}.{value.name}"
        elif isinstance(value, str):
            escaped = value.replace("\\", "\\\\").replace('"', '\\"')
            every_100_chars = re.compile(r"(.{100} )", flags=re.MULTILINE)
            escaped = every_100_chars.sub("\\1\n", escaped)
            if "\n" in escaped:
                return f'"""{escaped}"""'
            else:
                return f'"{escaped}"'
        elif isinstance(value, AliasChoices):
            self._tracker.track("pydantic", "AliasChoices")
            return f"""AliasChoices({", ".join(self._serialize_value(choice) for choice in value.choices)})"""
        elif isinstance(value, FunctionType):
            funcString = str(inspect.getsourcelines(value)[0])
            return funcString.strip("['\\n']").split(" = ")[1]
        elif isinstance(value, BaseModel):
            # Handle FHIR Primitives instanciated with just the value field
            if (
                isinstance(value, FHIRPrimitiveModel)
                and not value.id
                and not value.extension
            ):
                return self._serialize_value(value.value)
            # Handle all other Pydantic models
            model_name = self._annotations.serialize(value.__class__)
            return f"{model_name}({', '.join([k + '=' + self._serialize_value(getattr(value, k)) for k in sorted(value.model_fields_set)])})"
        else:
            return repr(value)
