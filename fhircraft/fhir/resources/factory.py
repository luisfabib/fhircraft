#!/usr/bin/env python
"""
Pydantic FHIR Model Factory
"""

import inspect
import json
import warnings
from collections import defaultdict

# Standard modules
from enum import Enum
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, TypeVar, Union

import requests

# Pydantic modules
from pydantic import BaseModel, Field, create_model, field_validator, model_validator
from pydantic.dataclasses import dataclass
from pydantic.fields import FieldInfo
from pydantic.functional_validators import _decorators as _validators
from pydantic_core import PydanticUndefined
from typing_extensions import Annotated

import fhircraft.fhir.resources.datatypes.primitives as primitives

# Internal modules
import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.base import FHIRBaseModel, FHIRSliceModel
from fhircraft.fhir.resources.datatypes import get_complex_FHIR_type
from fhircraft.fhir.resources.definitions import (
    ElementDefinition,
    ElementDefinitionConstraint,
    StructureDefinition,
)
from fhircraft.fhir.resources.repository import (
    CompositeStructureDefinitionRepository,
    StructureDefinitionRepository,
)
from fhircraft.utils import (
    capitalize,
    ensure_list,
    get_FHIR_release_from_version,
    load_env_variables,
)

ModelT = TypeVar("ModelT", bound="BaseModel")
SlicedModelT = TypeVar("SlicedModelT", bound="FHIRSliceModel")

_Unset: Any = PydanticUndefined


class ElementDefinitionNode(ElementDefinition):
    """A node in the ElementDefinition tree structure."""

    node_label: str = Field(...)
    children: Dict[str, "ElementDefinitionNode"] = Field(default_factory=dict)
    slices: Dict[str, "ElementDefinitionNode"] = Field(default_factory=dict)


class ResourceFactory:
    """Factory for constructing Pydantic models from FHIR StructureDefinitions.

    The ResourceFactory provides functionality to:
    - Load StructureDefinitions from various sources (files, directories, dictionaries)
    - Load FHIR packages from package registries
    - Construct Pydantic models from StructureDefinitions
    - Cache constructed models for performance
    - Manage internet access and package registry configuration
    """

    @dataclass
    class FactoryConfig:
        """Represents the configuration for the Factory class.

        Attributes:
            FHIR_release (str): The FHIR release version.
            resource_name (str): The name of the resource.
        """

        FHIR_release: str
        resource_name: str

    def __init__(
        self,
        repository: Optional[CompositeStructureDefinitionRepository] = None,
        internet_enabled: bool = True,
        enable_packages: bool = True,
        registry_base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """Initialize the ResourceFactory.

        Args:
            repository: Custom repository to use. If None, creates a default CompositeStructureDefinitionRepository
            internet_enabled: Whether to enable internet access for downloading definitions
            enable_packages: Whether to enable FHIR package support
            registry_base_url: Base URL for the FHIR package registry
            timeout: Request timeout in seconds for package downloads
        """
        if repository is None:
            self.repository = CompositeStructureDefinitionRepository(
                internet_enabled=internet_enabled,
                enable_packages=enable_packages,
                registry_base_url=registry_base_url,
                timeout=timeout,
            )
        else:
            self.repository = repository

        self.construction_cache: Dict[str, type[BaseModel]] = {}
        self.Config: Optional[ResourceFactory.FactoryConfig] = None

    # Convenience functions for easy configuration
    def configure_repository(
        self,
        directory: Optional[Union[str, Path]] = None,
        files: Optional[List[Union[str, Path]]] = None,
        definitions: Optional[List[Dict[str, Any]]] = None,
        packages: Optional[List[Union[str, Tuple[str, str]]]] = None,
        internet_enabled: bool = True,
        registry_base_url: Optional[str] = None,
    ) -> None:
        """Configure the factory repository with various sources.

        Args:
            directory: Directory containing structure definition files
            files: List of individual structure definition files to load
            definitions: List of structure definition dictionaries to load
            packages: List of FHIR packages to load. Each can be a package name (string)
                     or a tuple of (package_name, version)
            internet_enabled: Whether to enable internet access
            registry_base_url: Base URL for the package registry
        """
        self.repository.set_internet_enabled(internet_enabled)

        if registry_base_url and hasattr(self.repository, "set_registry_base_url"):
            self.repository.set_registry_base_url(registry_base_url)

        if directory:
            self.load_definitions_from_directory(directory)

        if files:
            self.load_definitions_from_files(*files)

        if definitions:
            self.load_definitions_from_list(*definitions)

        if packages:
            for package in packages:
                if isinstance(package, str):
                    self.load_package(package)
                elif isinstance(package, tuple) and len(package) == 2:
                    self.load_package(package[0], package[1])
                else:
                    raise ValueError(f"Invalid package specification: {package}")

    def disable_internet_access(self) -> None:
        """Toggle offline mode (disable internet access) to avoid external requests."""
        self.repository.set_internet_enabled(False)

    def enable_internet_access(self) -> None:
        """Toggle online mode (enable internet access) to allow external requests."""
        self.repository.set_internet_enabled(True)

    def load_definitions_from_directory(self, directory_path: Union[str, Path]) -> None:
        """
        Load FHIR structure definitions from the specified directory.

        This method attempts to load structure definitions into the repository from the given directory path.
        If the underlying repository supports loading from a directory (i.e., implements `load_from_directory`),
        the method delegates the loading process to it. Otherwise, a NotImplementedError is raised.

        Args:
            directory_path (Union[str, Path]): The path to the directory containing structure definitions.

        Raises:
            NotImplementedError: If the repository does not support loading from a directory.
        """
        """Load structure definitions from a directory."""
        if hasattr(self.repository, "load_from_directory"):
            self.repository.load_from_directory(directory_path)
        else:
            raise NotImplementedError(
                "Repository does not support loading from directory"
            )

    def load_definitions_from_files(self, *file_paths: Union[str, Path]) -> None:
        """
        Loads resource definitions from the specified file paths into the repository.

        This method delegates the loading process to the repository's `load_from_files` method,
        if it exists. If the repository does not support loading from files, a NotImplementedError is raised.

        Args:
            *file_paths (Union[str, Path]): One or more file paths from which to load resource definitions.

        Raises:
            NotImplementedError: If the repository does not support loading from files.
        """
        if hasattr(self.repository, "load_from_files"):
            self.repository.load_from_files(*file_paths)
        else:
            raise NotImplementedError("Repository does not support loading from files")

    def load_definitions_from_list(self, *definitions: Dict[str, Any]) -> None:
        """
        Loads resource definitions into the repository from a list of definition dictionaries.

        This method forwards the provided definitions to the repository's `load_from_definitions`
        method if it exists. If the repository does not support loading from definitions,
        a NotImplementedError is raised.

        Args:
            *definitions (Dict[str, Any]): One or more resource definition dictionaries to load.

        Raises:
            NotImplementedError: If the repository does not support loading from definitions.
        """
        if hasattr(self.repository, "load_from_definitions"):
            self.repository.load_from_definitions(*definitions)
        else:
            raise NotImplementedError(
                "Repository does not support loading from definitions"
            )

    def load_package(self, package_name: str, version: Optional[str] = None) -> None:
        """Load a FHIR package and return loaded structure definitions.

        Args:
            package_name: Name of the package (e.g., "hl7.fhir.us.core")
            version: Version of the package (defaults to latest)

        Returns:
            List of StructureDefinition objects that were loaded

        Raises:
            RuntimeError: If package support is not enabled in the repository
        """
        if hasattr(self.repository, "load_package"):
            self.repository.load_package(package_name, version)
        else:
            raise NotImplementedError("Repository does not support package loading")

    def get_loaded_packages(self) -> Dict[str, str]:
        """Get dictionary of loaded FHIR packages (name -> version).

        Returns:
            Dictionary mapping package names to their loaded versions
        """
        if hasattr(self.repository, "get_loaded_packages"):
            return self.repository.get_loaded_packages()
        else:
            return {}

    def has_package(self, package_name: str, version: Optional[str] = None) -> bool:
        """Check if a package is loaded.

        Args:
            package_name (str): Name of the package
            version (Optional[str]): Version of the package (if None, checks any version)

        Returns:
            True if package is loaded
        """
        if hasattr(self.repository, "has_package"):
            return self.repository.has_package(package_name, version)
        else:
            return False

    def remove_package(self, package_name: str, version: Optional[str] = None) -> None:
        """Remove a loaded package.

        Args:
            package_name (str): Name of the package
            version (Optional[str]): Version of the package (if None, removes all versions)
        """
        if hasattr(self.repository, "remove_package"):
            self.repository.remove_package(package_name, version)

    def set_registry_base_url(self, base_url: str) -> None:
        """Set the FHIR package registry base URL.

        Args:
            base_url (str): The base URL for the package registry

        Raises:
            RuntimeError: If package support is not enabled in the repository
        """
        if hasattr(self.repository, "set_registry_base_url"):
            self.repository.set_registry_base_url(base_url)
        else:
            raise NotImplementedError(
                "Repository does not support package registry configuration"
            )

    def clear_package_cache(self) -> None:
        """Clear the package cache."""
        if hasattr(self.repository, "clear_package_cache"):
            self.repository.clear_package_cache()

    def resolve_structure_definition(self, canonical_url: str) -> StructureDefinition:
        """Resolve structure definition using the repository."""
        if structure_def := self.repository.get(canonical_url):
            return structure_def
        raise ValueError(f"Could not resolve structure definition: {canonical_url}")

    def _build_element_tree_structure(
        self, elements: List[ElementDefinition]
    ) -> List[ElementDefinitionNode]:
        """
        Builds a hierarchical tree structure of ElementDefinitionNode objects from a flat list of ElementDefinition elements.

        This method organizes the provided FHIR ElementDefinition elements into a nested tree based on their dot-separated IDs,
        handling both regular child elements and slice definitions (denoted by a colon in the ID part).

        Args:
            elements (List[ElementDefinition]):
                A list of ElementDefinition objects representing the structure to be organized.

        Returns:
            List[ElementDefinitionNode]:
                A list of top-level ElementDefinitionNode objects representing the root children of the constructed tree.

        Notes:
            - Slice definitions (e.g., "element:sliceName") are handled by creating separate nodes under the appropriate parent.
            - Each node in the tree is an instance of ElementDefinitionNode, with children and slices populated as needed.
            - The root node is a synthetic node and is not included in the returned list.
        """
        root = ElementDefinitionNode(
            id="__root__",
            path="__root__",
            node_label="__root__",
            children={},
            slices={},
        )
        for element in elements:
            current = root
            id_parts = (element.id or "").split(".")
            for index, part in enumerate(id_parts):
                if ":" in part:
                    # Handle slice definitions
                    part, sliceName = part.split(":")
                    current = current.children[part]
                    current.slices = current.slices or {}
                    current = current.slices.setdefault(
                        sliceName,
                        ElementDefinitionNode.model_validate(
                            {
                                "node_label": sliceName,
                                "path": "__root__",
                                **(
                                    element.model_dump(exclude_unset=True)
                                    if index == len(id_parts) - 1
                                    else {}
                                ),
                            }
                        ),
                    )
                else:
                    # Handle children elements
                    current.children = current.children or {}
                    current = current.children.setdefault(
                        part,
                        ElementDefinitionNode.model_validate(
                            {
                                "node_label": part,
                                "path": "__root__",
                                **(
                                    element.model_dump(exclude_unset=True)
                                    if index == len(id_parts) - 1
                                    else {}
                                ),
                            }
                        ),
                    )
        return list(root.children.values())

    def _get_complex_FHIR_type(self, field_type_name: str) -> type | str:
        """
        Parses and loads the FHIR element type based on the provided field type name.

        Args:
            field_type_name (str): The name of the field type to be parsed.

        Returns:
            Union[type, str]: The parsed FHIR element type, returns input string if type not found.
        """
        FHIR_COMPLEX_TYPE_PREFIX = "http://hl7.org/fhir/StructureDefinition/"
        FHIRPATH_TYPE_PREFIX = "http://hl7.org/fhirpath/System."
        # Pre-process the type string
        field_type_name = str(field_type_name)
        field_type_name = field_type_name.removeprefix(FHIR_COMPLEX_TYPE_PREFIX)
        field_type_name = field_type_name.removeprefix(FHIRPATH_TYPE_PREFIX)
        field_type_name = capitalize(field_type_name)
        # Check if type is a FHIR primitive datatype
        field_type = getattr(primitives, field_type_name, None)
        if field_type:
            return field_type
        try:
            # Check if type is a FHIR complex datatype
            return get_complex_FHIR_type(
                field_type_name, self.Config.FHIR_release if self.Config else "R4B"
            )
        except (ModuleNotFoundError, AttributeError):
            return field_type_name

    def _create_model_with_properties(
        self,
        name: str,
        fields: dict,
        base: Tuple[type[ModelT], ...],
        validators: dict,
        properties: dict,
    ) -> type[ModelT]:
        """
        Constructs a Pydantic model with specified fields, base, validators, and properties.

        Parameters:
            name (str): The name of the model to be created.
            fields (dict): Dictionary of fields for the model.
            base (Union[Tuple[type], type]): Base type or tuple of base types for the model.
            validators (dict): Dictionary of validators for the model.
            properties (dict): Dictionary of properties to be set for the model.

        Returns:
            BaseModel: The constructed Pydantic model.
        """
        # Construct the slice model
        model = create_model(name, **fields, __base__=base, __validators__=validators)
        # Set the properties
        for attribute, property_getter in properties.items():
            setattr(model, attribute, property(property_getter))
        return model

    def _construct_Pydantic_field(
        self,
        field_type: Any,
        min_card: int,
        max_card: int,
        default: Any = _Unset,
        description: Optional[str] = None,
        alias: Optional[str] = None,
    ) -> Tuple[Any, FieldInfo]:
        """
        Constructs a Pydantic field based on the provided parameters.
        Constructs a Pydantic field based on the provided parameters.

        Args:
            field_type (type): The type of the field.
            min_card (int): The minimum cardinality of the field.
            max_card (int): The maximum cardinality of the field.
            default (Any, optional): The default value of the field. Defaults to _Unset.
            description (str, optional): The description of the field. Defaults to None.
            alias (str, optional): The alias of the field. Defaults to None.

        Returns:
            Tuple[Any, FieldInfo]: The constructed Pydantic field type and Field instance.
        """
        # Determine whether typing should be a list based on max. cardinality
        is_list_type = max_card is None or max_card > 1
        actual_field_type = field_type
        if is_list_type:
            actual_field_type = List[actual_field_type]
            default = ensure_list(default) if default is not _Unset else default
        # Determine whether the field is optional
        if min_card == 0:
            actual_field_type = Optional[actual_field_type]
            default = None
        # Construct the Pydantic field
        return (
            actual_field_type,
            Field(
                default,
                alias=alias,
                description=description,
                min_length=min_card if is_list_type else None,
                max_length=max_card if is_list_type else None,
            ),
        )

    def _process_pattern_or_fixed_values(
        self, element: ElementDefinition, constraint_prefix: str
    ) -> Any:
        """
        Process the pattern or fixed values of a StructureDefinition element.

        Parameters:
            element (Dict[str, Any]): The element to process.
            constraint_prefix (str): The prefix indicating pattern or fixed values.

        Returns:
            Any: The constrained value after processing.
        """
        # Determine the name of the StructureDefinition element's attribute that starts with either the prefix 'fixed[x]' or 'pattern[x]'
        constraint_attribute, constrained_value = next(
            (
                (attribute, getattr(element, attribute))
                for attribute in element.__class__.model_fields
                if attribute.startswith(constraint_prefix)
                and getattr(element, attribute) is not None
            ),
            ("", None),
        )
        if constrained_value:
            # Get the type of value that is constrained to a preset value
            constrained_type = self._get_complex_FHIR_type(
                constraint_attribute.replace(constraint_prefix, "")
            )
            # Parse the value
            constrained_value = (
                constrained_type.model_validate(constrained_value)
                if inspect.isclass(constrained_type)
                and issubclass(constrained_type, BaseModel)
                else constrained_value
            )
        return constrained_value

    def _process_choice_type_field(
        self,
        name,
        field_types,
        cardinality,
        fields,
        validators,
        properties,
        description=None,
    ):
        """
        Processes choice type fields by creating Pydantic fields for each type, adding validators, and setting properties.

        Args:
            name (str): The name of the field.
            field_types (List[type]): The types of the field.
            cardinality (List[int]): The cardinality constraints of the field.
            fields (dict): Dictionary of fields for the model.
            validators (dict): Dictionary of validators for the model.
            properties (dict): Dictionary of properties to be set for the model.
            description (str, optional): The description of the field. Defaults to None.

        Returns:
            Tuple[dict, dict, dict]: A tuple containing updated fields, validators, and properties.
        """
        # Get base name
        name = name.replace("[x]", "")
        # Create a field for each type
        for field_type in field_types:
            typed_field_name = name + (
                field_type if isinstance(field_type, str) else field_type.__name__
            )
            fields[typed_field_name] = self._construct_Pydantic_field(
                field_type, cardinality[0], cardinality[1], description=description
            )
        # Add validator to ensure only one of these fields is set
        validators[f"{name}_type_choice_validator"] = model_validator(mode="after")(
            partial(
                fhir_validators.validate_type_choice_element,
                field_types=field_types,
                field_name_base=name,
            )
        )
        properties[name] = partial(
            fhir_validators.get_type_choice_value_by_base, base=name
        )
        return fields, validators, properties

    def _build_element_slice_models(
        self, element: ElementDefinitionNode, slice_base: Any
    ) -> List[type[FHIRSliceModel]]:
        """
        Constructs and returns a list of FHIR slice model classes for a given element definition.

        This method processes the "slices" defined within the provided element dictionary,
        generating a Pydantic model class for each slice. If a canonical profile URL is specified
        for a slice, the corresponding resource model is constructed using that profile. Otherwise,
        a new model is dynamically created based on the slice's structure and properties.

        Each generated slice model is ensured to be a subclass of `FHIRSliceModel`, and its
        cardinality constraints (min and max) are set according to the slice definition.

        Args:
            element (dict): The element definition containing slice information.
            slice_base (type[BaseModel]): The base model class to use for the generated slice models.

        Returns:
            List[type[FHIRSliceModel]]: A list of dynamically constructed FHIR slice model classes.
        """
        slice_types = []
        for slice_name, slice_element in element.slices.items():
            if (slice_element_types := slice_element.type) and (
                slice_element_canonical_urls := slice_element_types[0].profile
            ):
                # Construct the slice model from the canonical URL
                slice_model = self.construct_resource_model(
                    slice_element_canonical_urls[0], base_model=FHIRSliceModel
                )
            else:
                # Construct the slice model's name
                slice_name = "".join(
                    [capitalize(word) for word in slice_name.split("-")]
                )
                slice_model_name = capitalize(slice_name)
                # Process and compile all subfields of the slice
                slice_subfields, slice_validators, slice_properties = (
                    self._process_FHIR_structure_into_Pydantic_components(
                        slice_element, FHIRSliceModel
                    )
                )
                # Construct the slice model
                bases = (
                    (slice_base,)
                    if slice_base is FHIRSliceModel
                    else (slice_base, FHIRSliceModel)
                )
                slice_model = self._create_model_with_properties(
                    slice_model_name,
                    fields=slice_subfields,
                    base=bases,
                    validators=slice_validators,
                    properties=slice_properties,
                )
            assert issubclass(
                slice_model, FHIRSliceModel
            ), f"Slice model {slice_model} is not a subclass of FHIRSliceModel"
            # Store the specific slice cardinality
            slice_model.min_cardinality, slice_model.max_cardinality = (
                self._parse_element_cardinality(slice_element)
            )
            # Store the slice model in the list of slices of the element
            slice_types.append(slice_model)
        # Create annotated type as union of slice models and original type (important, last in the definition)
        return slice_types

    def _parse_element_cardinality(self, element: ElementDefinition) -> Tuple[int, int]:
        """
        Parses the cardinality constraints from a FHIR element definition.

        Args:
            element (dict): A dictionary representing a FHIR element, expected to contain
                "min" and "max" keys indicating the minimum and maximum cardinality.

        Returns:
            tuple: A tuple (min_card, max_card) where:
                - min_card (int): The minimum allowed occurrences of the element.
                - max_card (int): The maximum allowed occurrences of the element.
        Notes:
            - If "min" is not numeric, defaults to 0.
            - If "max" is "*", uses 99999 as a stand-in for unbounded.
            - If "max" is not numeric or "*", attempts to convert to infinity.
        """
        min_card = int(element.min) if element.min else 0
        max_string = str(element.max)
        if max_string == "*":
            max_card = 99999
        elif max_string.isnumeric():
            max_card = int(max_string)
        else:
            max_card = 99999
        return min_card, max_card

    def _add_model_constraint_validator(
        self, constraint: ElementDefinitionConstraint, validators: dict
    ) -> dict:
        """
        Adds a model constraint validator based on the provided constraint.

        Args:
            constraint (dict): The constraint details including expression, human-readable description, key, and severity.
            validators (dict): The dictionary of validators to update with the new constraint validator.

        Returns:
            dict: The updated dictionary of validators.
        """
        # Construct function name for validator
        constraint_name = constraint.key.replace("-", "_")
        validator_name = f"FHIR_{constraint_name}_constraint_model_validator"
        # Add the current field to the list of validated fields
        if constraint.expression:
            validators[validator_name] = model_validator(mode="after")(
                partial(
                    fhir_validators.validate_model_constraint,
                    expression=constraint.expression,
                    human=constraint.human,
                    key=constraint.key,
                    severity=constraint.severity,
                )
            )
        return validators

    def _add_element_constraint_validator(
        self,
        field: str,
        constraint: ElementDefinitionConstraint,
        base: Any,
        validators: dict,
    ) -> dict:
        """
        Adds a validator for a specific element constraint to the validators dictionary.

        Args:
            field (str): The field to validate.
            constraint (dict): The details of the constraint including expression, human-readable description, key, and severity.
            base (Any): The base model to check for existing validators.
            validators (dict): The dictionary of validators to update.

        Returns:
            dict: The updated dictionary of validators.
        """
        # Construct function name for validator
        constraint_name = constraint.key.replace("-", "_")
        validator_name = f"FHIR_{constraint_name}_constraint_validator"
        # Check if validator has already been constructed for another field
        validate_fields = [field]
        # Get the list of fields already being validated by this constraint
        if validator_name in validators:
            validator = validators.get(validator_name)
            if validator:
                validate_fields.extend(validator.decorator_info.fields)
        # Get the list of fields already being validated by this constraint in base model
        if base and validator_name in base.__pydantic_decorators__.field_validators:
            validate_fields.extend(
                base.__pydantic_decorators__.field_validators[
                    validator_name
                ].info.fields
            )
        # Add the current field to the list of validated fields
        if constraint.expression:
            validators[validator_name] = field_validator(
                *validate_fields, mode="after"
            )(
                partial(
                    fhir_validators.validate_element_constraint,
                    expression=constraint.expression,
                    human=constraint.human,
                    key=constraint.key,
                    severity=constraint.severity,
                )
            )
        return validators

    def _process_FHIR_structure_into_Pydantic_components(
        self, structure: ElementDefinitionNode, base: Any | None = None
    ) -> Tuple[
        Dict[str, Any],
        Dict[str, Callable],
        Dict[str, Callable[..., Any]],
    ]:
        """
        Processes the FHIR structure elements into Pydantic components.

        Args:
            structure (dict): The structure containing FHIR elements.
            base (type[BaseModel], optional): The base model to check for existing validators. Defaults to None.

        Returns:
            Tuple[dict, dict, dict]: A tuple containing fields, validators, and properties.
        """
        fields = {}
        validators = {}
        properties = {}
        for name, element in structure.children.items():
            if base and name in base.model_fields:
                continue
            # Get cardinality of element
            min_card, max_card = self._parse_element_cardinality(element)
            # Parse the FHIR types of the element
            field_types = (
                [
                    self._get_complex_FHIR_type(field_type.code)
                    for field_type in element.type
                ]
                if element.type
                else []
            )
            # If has no type, skip element
            if not field_types:
                continue
            # Handle type choice elements
            if "[x]" in name:
                fields, validators, properties = self._process_choice_type_field(
                    name,
                    field_types,
                    [min_card, max_card],
                    fields,
                    validators,
                    properties,
                    description=element.short,
                )
                continue
            # Handle number of element types
            if len(field_types) > 1:
                # Accept all types
                field_type = Union[tuple(field_types)]
            else:
                # Get single type
                field_type = field_types[0]
            # Start by not setting any default value (important, 'None' implies optional in Pydantic)
            field_default = _Unset
            # Check for pattern value constraints
            if pattern_value := self._process_pattern_or_fixed_values(
                element, "pattern"
            ):
                field_default = pattern_value
                # Add the current field to the list of validated fields
                validators[f"FHIR_{name}_pattern_constraint"] = field_validator(
                    name, mode="after"
                )(
                    partial(
                        fhir_validators.validate_FHIR_element_pattern,
                        pattern=pattern_value,
                    )
                )
            # Check for fixed value constraints
            if fixed_value := self._process_pattern_or_fixed_values(element, "fixed"):
                # Use enum with single choice since Literal definition does not work at runtime
                singleChoice = Enum(
                    f"{name}FixedValue",
                    [("fixedValue", fixed_value)],
                    type=type(fixed_value),
                )
                field_default = fixed_value
                field_type = singleChoice
            # Process FHIR constraint invariants on the element
            if constraints := element.constraint:
                for constraint in constraints:
                    validators = self._add_element_constraint_validator(
                        name, constraint, base, validators
                    )
            # Process FHIR slicing on the element, if present
            if element.slices:
                field_type = Annotated[
                    Union[
                        tuple(
                            [
                                *self._build_element_slice_models(element, field_type),
                                field_type,
                            ]
                        )
                    ],
                    Field(union_mode="left_to_right"),
                ]
                # Add slicing cardinality validator for field
                validators[f"{name}_slicing_cardinality_validator"] = field_validator(
                    name, mode="after"
                )(
                    partial(
                        fhir_validators.validate_slicing_cardinalities, field_name=name
                    )
                )
            # Process element children, if present
            elif element.children:
                backbone_model_name = (
                    capitalize(
                        self.Config.resource_name if self.Config else "Unknown"
                    ).strip()
                    + capitalize(name).strip()
                )
                field_subfields, subfield_validators, subfield_properties = (
                    self._process_FHIR_structure_into_Pydantic_components(
                        element, field_type
                    )
                )
                for attribute, property_getter in subfield_properties.items():
                    setattr(field_type, attribute, property(property_getter))
                if element.children["extension"].slices:
                    extension_slice_base_type = get_complex_FHIR_type(
                        "Extension", self.Config.FHIR_release if self.Config else "R4B"
                    )
                    extension_type = Annotated[
                        Union[
                            tuple(
                                [
                                    *self._build_element_slice_models(
                                        element.children["extension"],
                                        extension_slice_base_type,
                                    ),
                                    extension_slice_base_type,
                                ]
                            )
                        ],
                        Field(union_mode="left_to_right"),
                    ]

                    self._build_element_slice_models(
                        element.children["extension"],
                        get_complex_FHIR_type(
                            "Extension",
                            self.Config.FHIR_release if self.Config else "R4B",
                        ),
                    )
                    # Get cardinality of extension element
                    extension_min_card, extension_max_card = (
                        self._parse_element_cardinality(element.children["extension"])
                    )
                    # Add slicing cardinality validator for field
                    subfield_validators[
                        f"extension_slicing_cardinality_validator"
                    ] = field_validator("extension", mode="after")(
                        partial(
                            fhir_validators.validate_slicing_cardinalities,
                            field_name="extension",
                        )
                    )
                    field_subfields["extension"] = self._construct_Pydantic_field(
                        extension_type, extension_min_card, extension_max_card
                    )
                field_type = create_model(
                    backbone_model_name,
                    **field_subfields,
                    __base__=(field_type,),  # type: ignore
                    __validators__=subfield_validators,
                )
            # Create and add the Pydantic field for the FHIR element
            fields[name] = self._construct_Pydantic_field(
                field_type,
                min_card,
                max_card,
                default=field_default,
                description=element.short,
            )
            # IF the field is of primitive type, add aliased field to accomodate their extensions
            if hasattr(primitives, str(field_type)):
                fields[f"{name}_ext"] = self._construct_Pydantic_field(
                    get_complex_FHIR_type("Element"),
                    min_card=0,
                    max_card=1,
                    alias=f"_{name}",
                    default=field_default,
                    description=f"Placeholder element for {name} extensions",
                )
        return fields, validators, properties

    def construct_resource_model(
        self,
        canonical_url: str | None = None,
        structure_definition: Union[str, dict, StructureDefinition] | None = None,
        base_model: type[ModelT] = FHIRBaseModel,
    ) -> type[ModelT | BaseModel]:
        """
        Constructs a Pydantic model based on the provided FHIR structure definition.

        Args:
            canonical_url (dict): The FHIR resource's or profile's canonical URL from which to download the StructureDefinition.
            structure_definition (Union[str,dict]): The FHIR StructureDefinition to build the model from specified as a filename or as a dictionary.

        Returns:
            model (BaseModel): The constructed Pydantic model representing the FHIR resource.
        """
        # If the model has been constructed before, return the cached model
        if canonical_url in self.construction_cache:
            return self.construction_cache[canonical_url]

        # Resolve the FHIR structure definition
        _structure_definition = None
        if isinstance(structure_definition, str):
            _structure_definition = self.repository.__load_json_structure_definition(
                Path(structure_definition)
            )
        elif isinstance(structure_definition, dict):
            _structure_definition = StructureDefinition.model_validate(
                structure_definition
            )
        elif canonical_url:
            _structure_definition = self.resolve_structure_definition(canonical_url)
        if not _structure_definition:
            raise ValueError(
                "No StructureDefinition provided or downloaded. Please provide a valid StructureDefinition."
            )
        # Parse and validate the StructureDefinition
        _structure_definition = StructureDefinition.model_validate(
            _structure_definition
        )
        # Check that the snapshot is available in the FHIR structure definition
        if (
            not _structure_definition.snapshot
            or not _structure_definition.snapshot.element
        ):
            raise ValueError(
                "Invalid StructureDefinition: Missing 'snapshot' or 'element' field"
            )
        # Pre-process the snapshot elements into a tree structure to simplify model construction later
        nodes = self._build_element_tree_structure(
            _structure_definition.snapshot.element
        )
        assert (
            len(nodes) == 1
        ), "StructureDefinition snapshot must have exactly one root element."
        structure = nodes[0]
        resource_type = _structure_definition.type
        # Configure the factory for the current FHIR environment
        if not _structure_definition.fhirVersion:
            warnings.warn(
                "StructureDefinition does not specify FHIR version, defaulting to R4B."
            )
        self.Config = self.FactoryConfig(
            FHIR_release=get_FHIR_release_from_version(
                _structure_definition.fhirVersion or "R4B"
            ),
            resource_name=_structure_definition.name,
        )
        # Process the FHIR resource's elements & constraints into Pydantic fields & validators
        fields, validators, properties = (
            self._process_FHIR_structure_into_Pydantic_components(structure)
        )
        # Process resource-level constraints
        for constraint in structure.constraint or []:
            validators = self._add_model_constraint_validator(constraint, validators)
        # If the resource has metadata, prefill the information
        if "meta" in fields:
            Meta = get_complex_FHIR_type(
                "Meta", self.Config.FHIR_release if self.Config else "R4B"
            )
            fields["resourceType"] = (Literal[f"{resource_type}"], resource_type)
            fields["meta"] = (
                Optional[Meta],
                Meta(
                    profile=[_structure_definition.url],
                    versionId=_structure_definition.version,
                ),
            )
        # Construct the Pydantic model representing the FHIR resource
        model = self._create_model_with_properties(
            self.Config.resource_name if self.Config else _structure_definition.name,
            fields=fields,
            base=(base_model,),
            validators=validators,
            properties=properties,
        )
        # Add the current model to the cache
        self.construction_cache[_structure_definition.url] = model
        return model

    def construct_dataelement_model(self, structure_definition):
        if (
            "snapshot" not in structure_definition
            or "element" not in structure_definition["snapshot"]
        ):
            raise ValueError(
                "Invalid StructureDefinition: Missing 'snapshot' or 'element' field"
            )
        elements = structure_definition["snapshot"]["element"]
        nodes = self._build_element_tree_structure(elements)
        assert (
            len(nodes) == 1
        ), "StructureDefinition snapshot must have exactly one root element."
        structure = nodes[0]
        # Configure the factory for the current FHIR environment
        self.Config = self.FactoryConfig(
            FHIR_release=get_FHIR_release_from_version(
                structure_definition["fhirVersion"]
            ),
            resource_name=structure_definition["name"],
        )
        if "baseDefinition" in structure_definition:
            base_name = structure_definition["baseDefinition"].replace(
                "http://hl7.org/fhir/StructureDefinition/", ""
            )
            base = self.construction_cache.get(base_name)
        else:
            base = FHIRBaseModel
        fields, validators, properties = (
            self._process_FHIR_structure_into_Pydantic_components(structure, base)
        )
        for constraint in structure.constraint or []:
            validators = self._add_model_constraint_validator(constraint, validators)
        model = create_model(
            self.Config.resource_name if self.Config else structure_definition["name"],
            **fields,
            __base__=base,
            __validators__=validators,
        )
        model.__doc__ = structure.short
        for attribute, property_getter in properties.items():
            setattr(model, attribute, property(property_getter))
        return model

    def clear_chache(self):
        """
        Clears the factory cache.
        """
        self.construction_cache = {}


# Create default factory instance
factory = ResourceFactory()

# Public API
construct_resource_model = factory.construct_resource_model
