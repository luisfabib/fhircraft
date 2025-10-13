import functools
import os
import re
from collections import defaultdict
from datetime import datetime
from enum import Enum
from importlib.metadata import version
from typing import Any, Dict, ForwardRef, List, get_args

from jinja2 import Environment, FileSystemLoader, Template
from pydantic import BaseModel
from pydantic_core import PydanticUndefined

from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.utils import ensure_list, get_module_name

__all__ = ["generator", "generate_resource_model_code", "CodeGenerator"]

FACTORY_MODULE = get_module_name(ResourceFactory)
LEFT_TO_RIGHT_COMPLEX = "FieldInfo(annotation=NoneType, required=True, metadata=[_PydanticGeneralMetadata(union_mode='left_to_right')])"
LEFT_TO_RIGHT_SIMPLE = "Field(union_mode='left_to_right')"


class CodeGenerator:

    import_statements: Dict[str, List[str]]
    template: Template
    data: Dict

    def __init__(self):
        # Prepare the templating engine environment
        file_loader = FileSystemLoader(os.path.dirname(os.path.abspath(__file__)))
        env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
        env.filters["escapequotes"] = lambda s: s.replace('"', '\\"')
        env.globals.update(ismodel=lambda obj: isinstance(obj, BaseModel))
        self.template = env.get_template("resource_template.py.j2")

    def _reset_state(self) -> None:
        """
        Resets the internal state of the CodeGenerator instance.
        Clears the import statements and data dictionaries.
        """
        self.import_statements = defaultdict(list)
        self.data = {}
        self._processing_models = (
            set()
        )  # Track models being processed to prevent infinite recursion

    def _cleanup_function_argument(self, arg: Any) -> Any:
        """
        Cleans up function arguments for serialization or import statements.

        Args:
            arg (Any): The argument to clean up.

        Returns:
            Any: The cleaned-up argument.
        """
        if isinstance(arg, str):
            escape_quotes = arg.replace('"', '\\"')
            return f'"{escape_quotes}"'
        elif isinstance(arg, BaseModel):
            arguments = ", ".join(
                f"{key}={value!r}"
                for key, value in arg.model_dump(exclude_none=True).items()
            )
            self._add_import_statement(arg.__class__)
            return f"{arg.__class__.__name__}({arguments})"
        else:
            return arg

    def _add_import_statement(self, obj: Any) -> None:
        """
        Adds an import statement for the given object.

        This method inspects the module of the given object and adds an import
        statement to the `import_statements` dictionary if the module is not
        already present and the object is not a built-in.

        Args:
            obj (Any): The object for which to add an import statement.

        Raises:
            ValueError: If the object does not belong to a module.
        """
        # Get the name of the module and the object
        module_name = get_module_name(obj)
        if isinstance(obj, ForwardRef):
            return None
        if (object_name := getattr(obj, "__name__", None)) is None:
            if (object_name := getattr(obj, "_name", None)) is None:
                raise ValueError(f"Could not determine object name for import: {obj}")
        # Generate the import statement
        if (
            module_name not in [FACTORY_MODULE, "builtins"]
            and object_name not in self.import_statements[module_name]
        ):
            self.import_statements[module_name].append(object_name)

    def _recursively_import_annotation_types(self, annotation: Any) -> None:
        """
        Recursively imports annotation types and their modules for serialization or import statements.

        Args:
            annotation (_UnionGenericAlias): The annotation type to process.

        Raises:
            ValueError: If the object does not belong to a module.
        """
        # Get the type object
        if hasattr(annotation, "annotation"):
            type_obj = annotation.annotation
        else:
            type_obj = annotation
        # Ignore NoneType and strings
        if type_obj is not None and not isinstance(type_obj, str):
            if get_module_name(type_obj) == FACTORY_MODULE and issubclass(
                type_obj, BaseModel
            ):
                # If object was created by ResourceFactory, then serialize the model
                # But only if we're not already processing it (to prevent infinite recursion)
                if type_obj not in self._processing_models:
                    self._serialize_model(type_obj)
            else:
                # Otherwise, import the model's module
                self._add_import_statement(type_obj)
        # Repeat for any nested annotations
        for nested_annotation in get_args(annotation):
            self._recursively_import_annotation_types(nested_annotation)

    def _serialize_model(self, model: type[BaseModel]) -> None:
        """
        Serialize the model by extracting information about its fields and properties.

        Args:
            model (BaseModel): The model to be serialized.
        """
        # Check if we're already processing this model or have already processed it
        if model in self._processing_models or model in self.data:
            return

        # Add to processing set to prevent infinite recursion
        self._processing_models.add(model)

        try:
            model_base = model.__base__
            # Add import statement for the base class the the model inherits
            if model_base and model_base != BaseModel:
                self._add_import_statement(model.__base__)

            subdata = {}
            for field, info in model.model_fields.items():
                if (
                    model.__base__
                    and field in model.__base__.model_fields
                    and all(
                        [
                            getattr(info, slot)
                            == getattr(model.__base__.model_fields[field], slot)
                            for slot in info.__slots__
                            if not slot.startswith("_")
                        ]
                    )
                ):
                    continue
                self._recursively_import_annotation_types(info.annotation)
                annotation_string = repr(info.annotation)

                # Handle forward references
                if "ForwardRef" in annotation_string:
                    annotation_string = re.sub(
                        r"ForwardRef\('(\w+)'\)", r"'\1'", annotation_string
                    )

                # Handle self-referencing models
                elif not "Literal" in annotation_string:
                    annotation_string = re.sub(
                        rf"\b{model.__name__}\b",
                        f'"{model.__name__}"',
                        annotation_string,
                        0,
                    )

                if isinstance(info.annotation, type(Enum)):
                    if "Literal" not in self.import_statements["typing"]:
                        self.import_statements["typing"].append("Literal")
                    annotation_string = (
                        f"Literal['{info.annotation['fixedValue'].value}']"
                    )

                default = "..."
                default_factory = "..."
                if isinstance(info.default, str):
                    default = f'"{info.default}"'
                elif isinstance(info.default, BaseModel):
                    arguments = ", ".join(
                        f"{key}={value!r}"
                        for key, value in info.default.model_dump(
                            exclude_none=True
                        ).items()
                    )
                    default_factory = (
                        f"lambda: {info.default.__class__.__name__}({arguments})"
                    )
                elif info.default is not PydanticUndefined:
                    default = repr(info.default)
                elif info.default_factory is not None:
                    default_factory = info.default_factory

                subdata[field] = {
                    "annotation": annotation_string,
                    "title": info.title,
                    "description": info.description,
                    "alias": info.alias,
                    "default": default,
                    "default_factory": default_factory,
                }

            model_properties = {}
            for key, value in model.__dict__.items():
                if isinstance(value, property):
                    if not value.fget:
                        raise ValueError(
                            f"Property {key} does not have a getter function."
                        )
                    if not isinstance(value.fget, functools.partial):  # type: ignore
                        raise ValueError(
                            f"Only partial functions are supported for properties in the code generator. Property {key} uses {type(value.fget)}."
                        )
                    self._add_import_statement(value.fget.func)
                    model_properties[key] = dict(
                        func=value.fget.func,
                        args=[
                            self._cleanup_function_argument(arg)
                            for arg in value.fget.args
                        ],
                        keywords={
                            k: self._cleanup_function_argument(v)
                            for k, v in value.fget.keywords.items()
                        },
                    )

            inherited_validator_functions = [
                getattr(v.func, "__func__", v.func)
                for base in model.__bases__
                for v in [
                    *base.__pydantic_decorators__.field_validators.values(),
                    *base.__pydantic_decorators__.model_validators.values(),
                ]
            ]

            validators = {}
            for mode, _validators in zip(
                ["field", "model"],
                [
                    model.__pydantic_decorators__.field_validators,
                    model.__pydantic_decorators__.model_validators,
                ],
            ):
                for name, validator in _validators.items():
                    if isinstance(validation_function := getattr(validator.func, "__func__", validator.func), functools.partial):  # type: ignore
                        self._add_import_statement(validation_function.func)
                        func_args = [
                            self._cleanup_function_argument(arg)
                            for arg in validation_function.args
                        ]
                        func_kwargs = {
                            key: self._cleanup_function_argument(arg)
                            for key, arg in validation_function.keywords.items()
                        }
                    else:
                        if validation_function in inherited_validator_functions:
                            continue  # Skip inherited validators
                        raise ValueError(
                            "Only partial functions are supported for validators in the code generator."
                        )

                    validators[name] = dict(
                        mode=mode,
                        info=validator.info,
                        func=validation_function.func,
                        args=func_args,
                        keywords=func_kwargs,
                    )

            self.data.update(
                {
                    model: {
                        "fields": subdata,
                        "properties": model_properties,
                        "validators": validators,
                    }
                }
            )
        finally:
            # Always remove from processing set when done
            self._processing_models.discard(model)

    def generate_resource_model_code(
        self,
        resources: type[BaseModel] | List[type[BaseModel]],
        include_validators: bool = True,
    ) -> str:
        """
        Generate the source code for resource model(s) based on the input resources.

        Args:
            resources (Union[BaseModel, List[BaseModel]]): The resource(s) to generate the model code for.
            include_validators (bool): Whether to include validators in the generated code (default: `True`). Recommended to be `True` for most use cases.

        Returns:
            str: The generated source code for the resource model(s).
        """
        # Reset the internal state of the generator
        self._reset_state()
        # Serialize the model information of the input resources
        for resource in ensure_list(resources):
            self._serialize_model(resource)
        # Render the source code using Jinja2
        source_code = self.template.render(
            data=self.data,
            imports=self.import_statements,
            include_validators=include_validators,
            metadata={
                "version": version("fhircraft"),
                "timestamp": datetime.now(),
            },
        )
        # Replace the full module specification for any modules imported
        for module, objects in self.import_statements.items():
            module = module.replace(".", r"\.")
            for regex in [
                rf"(\<class \'{module}\.(\w*)\'\>)",
                r"(\<class \'(\w*)\'\>)",
            ]:
                for match in re.finditer(regex, source_code):
                    source_code = source_code.replace(match.group(1), match.group(2))
            for match in re.finditer(
                rf"({module}\.)({'|'.join(objects)})", source_code
            ):
                source_code = source_code.replace(match.group(1), "")
            source_code = source_code.replace(f"{FACTORY_MODULE}.", "")
        source_code = source_code.replace(LEFT_TO_RIGHT_COMPLEX, LEFT_TO_RIGHT_SIMPLE)
        return source_code


generator = CodeGenerator()
generate_resource_model_code = generator.generate_resource_model_code
