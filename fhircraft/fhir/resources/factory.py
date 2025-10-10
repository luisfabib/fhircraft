#!/usr/bin/env python
"""
Pydantic FHIR Model Factory
"""

import inspect
import keyword
import warnings

# Standard modules
from enum import Enum
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, TypeVar, Union

# Pydantic modules
from pydantic import BaseModel, Field, create_model, field_validator, model_validator
from pydantic.aliases import AliasChoices
from pydantic.dataclasses import dataclass
from pydantic.fields import FieldInfo
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
    ElementDefinitionSlicing,
    ElementDefinitionType,
    StructureDefinition,
)
from fhircraft.fhir.resources.repository import CompositeStructureDefinitionRepository
from fhircraft.utils import capitalize, ensure_list, get_FHIR_release_from_version

ModelT = TypeVar("ModelT", bound="BaseModel")
SlicedModelT = TypeVar("SlicedModelT", bound="FHIRSliceModel")

_Unset: Any = PydanticUndefined

TYPE_CHOICE_SUFFIX = "[x]"


class ElementDefinitionNode(ElementDefinition):
    """A node in the ElementDefinition tree structure."""

    node_label: str = Field(...)
    children: Dict[str, "ElementDefinitionNode"] = Field(default_factory=dict)
    slices: Dict[str, "ElementDefinitionNode"] = Field(default_factory=dict)
    root: Optional["ElementDefinitionNode"] = None


@dataclass
class ResourceFactoryValidators:
    """Container for resource-level validators."""

    _validators: dict = Field(default_factory=dict)

    def get_all(self) -> dict:
        return self._validators

    def add(self, validator_name: str, validator: Any) -> None:
        self._validators[validator_name] = validator

    def add_model_constraint_validator(self, constraint: ElementDefinitionConstraint):
        """
        Adds a model constraint validator based on the provided constraint.

        Args:
            constraint (dict): The constraint details including expression, human-readable description, key, and severity.
        """
        # Construct function name for validator
        constraint_name = constraint.key.replace("-", "_")
        validator_name = f"FHIR_{constraint_name}_constraint_model_validator"
        # Add the current field to the list of validated fields
        if constraint.expression:
            self._validators[validator_name] = model_validator(mode="after")(
                partial(
                    fhir_validators.validate_model_constraint,
                    expression=constraint.expression,
                    human=constraint.human,
                    key=constraint.key,
                    severity=constraint.severity,
                )
            )

    def add_element_constraint_validator(
        self,
        field: str,
        constraint: ElementDefinitionConstraint,
        base: Any,
    ):
        """
        Adds a validator for a specific element constraint to the validators dictionary.

        Args:
            field (str): The field to validate.
            constraint (dict): The details of the constraint including expression, human-readable description, key, and severity.
            base (Any): The base model to check for existing validators.
        """
        # Construct function name for validator
        constraint_name = constraint.key.replace("-", "_")
        validator_name = f"FHIR_{constraint_name}_constraint_validator"
        # Check if validator has already been constructed for another field
        validate_fields = [field]
        # Get the list of fields already being validated by this constraint
        if validator_name in self._validators:
            validator = self._validators.get(validator_name)
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
            self._validators[validator_name] = field_validator(
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

    def add_slicing_validator(self, field: str):
        """
        Adds a validator to ensure that slicing rules are followed for sliced elements.
        """
        self._validators[f"{field}_slicing_cardinality_validator"] = field_validator(
            field, mode="after"
        )(
            partial(
                fhir_validators.validate_slicing_cardinalities,
                field_name=field,
            )
        )

    def add_type_choice_validator(
        self,
        field: str,
        allowed_types: List[Union[str, type]],
        required: bool = False,
    ):
        """
        Adds a validator to ensure that the field's value matches one of the allowed types.

        Args:
            field (str): The field to validate.
            allowed_types (List[Union[str, type]]): List of allowed types for the field.
            required (bool): Whether the field is required. Defaults to `False`.
        """
        self._validators[f"{field}_type_choice_validator"] = model_validator(
            mode="after"
        )(
            partial(
                fhir_validators.validate_type_choice_element,
                field_types=allowed_types,
                field_name_base=field,
                required=required,
            )
        )


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
        FHIR_version: str
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
        self.paths_in_processing: set[str] = set()
        self.local_cache: Dict[str, type[BaseModel]] = {}
        self.Config: ResourceFactory.FactoryConfig

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

    def resolve_structure_definition(
        self, canonical_url: str, version: str | None = None
    ) -> StructureDefinition:
        """Resolve structure definition using the repository."""
        if structure_def := self.repository.get(canonical_url, version):
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
                                "root": root,
                                "path": "__root__",
                                **(
                                    element.model_dump(exclude_unset=True)
                                    if index == len(id_parts) - 1
                                    else {}
                                ),
                            }
                        ),
                    )
        result = list(root.children.values())
        return result

    def _resolve_FHIR_type(
        self, element_type: ElementDefinitionType | str
    ) -> type | str:
        """
        Resolves and returns the Python type corresponding to a FHIR complex or primitive type
        based on the provided ElementDefinitionType.

        This method processes the type code from the element definition, handling FHIR and FHIRPath
        type prefixes, and attempts to resolve it as a FHIR primitive or complex type. If the type
        cannot be resolved directly, it attempts to construct a resource model from a provided
        profile URL. Raises a RuntimeError if the type cannot be resolved.

        Args:
            element_type (ElementDefinitionType | str): The FHIR element type definition to resolve.

        Returns:
            type: The resolved Python type corresponding to the FHIR type.

        Raises:
            RuntimeError: If the FHIR type cannot be resolved and no profile canonical URL is provided,
                          or if the profile URL cannot be resolved to a resource model.
        """
        FHIR_COMPLEX_TYPE_PREFIX = "http://hl7.org/fhir/StructureDefinition/"
        FHIRPATH_TYPE_PREFIX = "http://hl7.org/fhirpath/System."
        element_type_code = (
            element_type.code
            if isinstance(element_type, ElementDefinitionType)
            else element_type
        )
        # Pre-process the type string
        element_type_code = element_type_code.removeprefix(FHIR_COMPLEX_TYPE_PREFIX)
        element_type_code = element_type_code.removeprefix(FHIRPATH_TYPE_PREFIX)
        element_type_code = capitalize(element_type_code)
        # Check if type is a FHIR primitive datatype
        field_type = getattr(primitives, element_type_code, None)
        if field_type:
            return field_type
        try:
            # Check if type is a FHIR complex datatype
            return get_complex_FHIR_type(element_type_code, self.Config.FHIR_release)
        except (ModuleNotFoundError, AttributeError):
            if isinstance(element_type, ElementDefinitionType) and element_type.profile:
                # Try to resolve custom type from profile URL
                if type_structure_definition := self.resolve_structure_definition(
                    element_type.profile[0]
                ):
                    return self.construct_resource_model(
                        structure_definition=type_structure_definition,
                        base_model=FHIRBaseModel,
                    )
                else:
                    raise RuntimeError(
                        f"Could not resolve the canonical URL '{element_type.profile[0]}' for the FHIR type '{element_type_code}'. Please add the resource to the factory repository."
                    )
            elif isinstance(element_type, ElementDefinitionType) and element_type.code:
                return self.local_cache.get(element_type.code, element_type.code)

            else:
                raise RuntimeError(
                    f"Could not resolve FHIR type '{element_type_code}' and no profile canonical URL provided in the element definition"
                )

    def _construct_model_with_properties(
        self,
        name: str,
        fields: dict,
        base: Tuple[type[ModelT], ...],
        validators: dict,
        properties: dict,
        docstring: str | None = None,
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

        Note:
            Additional properties are added at runtime and are not reflected in the static type.
        """
        # Construct the slice model
        model = create_model(
            name, **fields, __base__=base, __validators__=validators, __doc__=docstring
        )
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
        validation_alias: Optional[AliasChoices] = None,
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
            validation_alias (AliasChoices, optional): The validation alias choices for the field. Defaults to None.

        Returns:
            Tuple[Any, FieldInfo]: The constructed Pydantic field type and Field instance.
        """
        # Determine whether typing should be a list based on max. cardinality
        is_list_type = max_card is None or max_card > 1
        actual_field_type = field_type
        # Handle list types
        if is_list_type:
            actual_field_type = List[actual_field_type]

        # All fields are non-required and non-nullable
        if default is _Unset:
            default = None
        elif is_list_type:
            default = ensure_list(default)

        if default is None:
            actual_field_type = Optional[actual_field_type]
        # Construct the Pydantic field
        return (
            actual_field_type,
            Field(
                default,
                alias=alias,
                validation_alias=validation_alias,
                description=description,
                min_length=min_card if is_list_type else None,
                max_length=max_card if is_list_type else None,
            ),
        )

    def _handle_python_reserved_keyword(
        self, field_name: str
    ) -> Tuple[str, Optional[AliasChoices]]:
        """
        Handles Python reserved keywords in field names by appending an underscore
        and creating appropriate validation aliases.

        Args:
            field_name (str): The original field name

        Returns:
            Tuple[str, Optional[AliasChoices]]: The processed field name and optional alias choices
        """
        CLASS_RESERVED_KEYWORDS = {
            "property",
            "classmethod",
            "field_validator",
            "model_validator",
        }
        if keyword.iskeyword(field_name) or field_name in CLASS_RESERVED_KEYWORDS:
            # Append underscore to make it a valid Python identifier
            safe_field_name = f"{field_name}_"
            # Create validation alias that accepts both original name and modified name
            validation_alias = AliasChoices(field_name, safe_field_name)
            return safe_field_name, validation_alias
        return field_name, None

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
            constrained_type = self._resolve_FHIR_type(
                constraint_attribute.replace(constraint_prefix, "")
            )
            # Parse the value
            constrained_value = (
                constrained_type.model_validate(
                    constrained_value.model_dump()
                    if isinstance(constrained_value, BaseModel)
                    else constrained_value
                )
                if inspect.isclass(constrained_type)
                and issubclass(constrained_type, BaseModel)
                else constrained_value
            )
        return constrained_value

    def _construct_type_choice_fields(
        self,
        basename: str,
        field_types: List,
        max_card: int,
        description: str | None = None,
    ) -> Dict[str, Tuple[Any, FieldInfo]]:
        """
        Constructs a dictionary of Pydantic fields for FHIR type choice elements.

        For FHIR elements that allow multiple types (denoted by [x]), this method generates
        a field for each possible type, handling Python reserved keywords and setting appropriate
        cardinality and descriptions.

        Args:
            name (str): The base name of the FHIR element, without containing '[x]'.
            field_types (List[Union[str, type]]): List of possible types for the element.
            max_cardinality (int | None): Minimum and maximum allowed occurrences.
            description (Optional[str]): Description of the field(s).

        Returns:
            Dict[str, Tuple[Any, FieldInfo]]: A dictionary mapping safe field names to their
            corresponding type and Pydantic FieldInfo.
        """
        # Get base name
        fields = {}
        # Create a field for each type
        for field_type in field_types:
            typed_field_name = basename + (
                field_type if isinstance(field_type, str) else field_type.__name__
            )
            # Handle Python reserved keywords
            safe_typed_field_name, validation_alias = (
                self._handle_python_reserved_keyword(typed_field_name)
            )
            fields[safe_typed_field_name] = self._construct_Pydantic_field(
                field_type,
                min_card=0,
                max_card=max_card,
                description=description,
                validation_alias=validation_alias,
            )
        return fields

    def _construct_slice_model(
        self, name: str, definition: ElementDefinitionNode, base: type[BaseModel]
    ) -> type[FHIRSliceModel]:
        """
        Constructs a Pydantic model representing a FHIR slice based on the provided element definition.

        This method handles two scenarios:
        1. If the element definition specifies a canonical profile URL, it constructs the slice model using the referenced resource model.
        2. Otherwise, it dynamically generates a model name, processes the element definition into Pydantic fields, validators, and properties, and constructs the slice model accordingly.

        The resulting model is always a subclass of `FHIRSliceModel`, and its cardinality constraints are set based on the element definition.

        Args:
            name (str): The name of the slice.
            definition (ElementDefinitionNode): The FHIR element definition node describing the slice.
            base (type[BaseModel]): The base Pydantic model to inherit from.

        Returns:
            type[FHIRSliceModel]: The constructed slice model class.

        Raises:
            AssertionError: If the constructed model is not a subclass of `FHIRSliceModel`.
        """
        if (types := definition.type) and (canonical_urls := types[0].profile):
            # Construct the slice model from the canonical URL
            slice_model = self.construct_resource_model(
                canonical_urls[0], base_model=FHIRSliceModel
            )
        else:
            # Construct the slice model's name
            slice_model_name = capitalize(
                "".join([capitalize(word) for word in name.split("-")])
            )
            # Process and compile all subfields of the slice
            slice_subfields, slice_validators, slice_properties = (
                self._process_FHIR_structure_into_Pydantic_components(
                    definition, FHIRSliceModel
                )
            )
            # Construct the slice model
            bases = (
                (base,)
                if base is FHIRSliceModel or issubclass(base, FHIRSliceModel)
                else (base, FHIRSliceModel)
            )
            slice_model = self._construct_model_with_properties(
                slice_model_name,
                fields=slice_subfields,
                base=bases,
                validators=slice_validators.get_all(),
                properties=slice_properties,
                docstring=definition.short,
            )
        assert issubclass(
            slice_model, FHIRSliceModel
        ), f"Slice model {slice_model} is not a subclass of FHIRSliceModel"
        # Store the specific slice cardinality
        slice_model.min_cardinality, slice_model.max_cardinality = (
            self._parse_element_cardinality(definition)
        )
        return slice_model

    def _construct_annotated_sliced_field(
        self, slices: Dict[str, ElementDefinitionNode], field_type: type[BaseModel]
    ) -> Annotated:
        """
        Constructs an annotated field representing a union of sliced models and the base field type.

        Args:
            slices (Dict[str, ElementDefinitionNode]): A dictionary mapping slice names to their corresponding ElementDefinitionNode objects.
            field_type (type[BaseModel]): The base model type for the field.

        Returns:
            (Annotated): An annotated type representing a union of all constructed slice models and the base field type, with additional field metadata specifying union mode as "left_to_right".
        """
        return Annotated[
            Union[
                tuple(
                    [
                        *[
                            self._construct_slice_model(
                                slice_name, slice_element, field_type
                            )
                            for slice_name, slice_element in slices.items()
                        ],
                        field_type,
                    ]
                )
            ],
            Field(union_mode="left_to_right"),
        ]

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

    def _resolve_content_reference(
        self, element: ElementDefinitionNode
    ) -> ElementDefinitionNode:
        """
        Resolves the content reference for a given ElementDefinitionNode by copying relevant fields
        from the referenced element to the current element. Adds cycle detection to prevent infinite recursion.
        Args:
            element (ElementDefinitionNode): The element node containing a content reference.

        Returns:
            ElementDefinitionNode: The updated element node with fields populated from the referenced element.

        Raises:
            ValueError: If the provided element does not have a content reference.

        Warns:
            UserWarning: If the content reference cannot be resolved or a cycle is detected.
        """
        if not element.contentReference:
            raise ValueError("Element does not have a content reference")

        resource_url, reference_path = element.contentReference.split("#")
        if not resource_url:
            search = element.root
        else:
            # Resolve the resource URL to a StructureDefinition
            structure_definition = self.resolve_structure_definition(
                resource_url, self.Config.FHIR_version
            )
            if not structure_definition:
                raise ValueError(f"Could not resolve resource URL: {resource_url}")
            if not structure_definition.snapshot:
                raise ValueError(f"StructureDefinition {resource_url} has no snapshot")
            search_tree = self._build_element_tree_structure(
                structure_definition.snapshot.element
            )
            # Create a root node to search from, similar to how it's done in _build_element_tree_structure
            search = search_tree[0].root if search_tree else None
        referenced_element = None
        parts = reference_path.split(".")

        # Detect cycles
        if reference_path in self.paths_in_processing or element.path.startswith(
            reference_path + "."
        ):
            backbone_model_name = capitalize(
                self.Config.resource_name if self.Config else "Unknown"
            ).strip() + "".join(
                [capitalize(label).strip() for label in reference_path.split(".")[1:]]
            )
            element.type = [ElementDefinitionType(code=backbone_model_name)]
            element.children = {}
            return element
        self.paths_in_processing.add(reference_path)

        for part in parts:
            if not search or not search.children:
                break
            search = search.children.get(part)
        else:
            if search:
                referenced_element = search

        if not referenced_element:
            warnings.warn(
                f"Could not resolve content reference: {element.contentReference}."
            )
            self.paths_in_processing.remove(reference_path)
            return element

        for field in ("children", "type", "maxLength", "binding"):
            setattr(element, field, getattr(referenced_element, field, None))
        for field in (
            "defaultValue",
            "fixed",
            "pattern",
            "example",
            "minValue",
            "maxValue",
        ):
            for attr in element.__class__.model_fields:
                if (
                    attr.startswith(field)
                    and getattr(referenced_element, attr, None) is not None
                ):
                    setattr(element, attr, getattr(referenced_element, attr, None))

        return element

    def _construct_primitive_extension_field(
        self,
        name: str,
    ) -> dict[str, Tuple[Any, FieldInfo]]:
        """
        Constructs a Pydantic field for a FHIR primitive extension.

        This method creates a field for the extension element associated with a FHIR primitive field,
        handling Python reserved keywords in the field name and setting appropriate field metadata.

        Args:
            name (str): The name of the FHIR primitive field for which to construct the extension field.

        Returns:
            Dict[str, Tuple[Any, FieldInfo]]: A dictionary mapping the safe extension field name to a tuple containing the field type and its Pydantic FieldInfo configuration.
        """
        safe_ext_field_name, ext_validation_alias = (
            self._handle_python_reserved_keyword(f"{name}_ext")
        )
        return {
            safe_ext_field_name: self._construct_Pydantic_field(
                get_complex_FHIR_type(
                    "Element", self.Config.FHIR_release if self.Config else "4.3.0"
                ),
                min_card=0,
                max_card=1,
                alias=f"_{name}",
                validation_alias=ext_validation_alias,
                default=None,
                description=f"Placeholder element for {name} extensions",
            )
        }

    def _process_FHIR_structure_into_Pydantic_components(
        self, structure: ElementDefinitionNode, base: Any | None = None
    ) -> Tuple[
        Dict[str, Any],
        ResourceFactoryValidators,
        Dict[str, Callable[..., Any]],
    ]:
        """
        Processes the FHIR structure elements into Pydantic components.

        Args:
            structure (dict): The structure containing FHIR elements.
            base (type[BaseModel], optional): The base model to check for existing validators. Defaults to None.
            resolving_paths (set, optional): Set of paths currently being resolved to prevent circular references.

        Returns:
            Tuple[dict, dict, dict]: A tuple containing fields, validators, and properties.
        """
        fields = {}
        validators = ResourceFactoryValidators()
        properties = {}
        for name, element in structure.children.items():

            # Prevent circular references
            if base and name in base.model_fields:
                continue

            # Handle Python reserved keywords for field names early
            safe_field_name, validation_alias = self._handle_python_reserved_keyword(
                name
            )

            # -------------------------------------
            # Element content references
            # -------------------------------------
            if element.contentReference:
                element = self._resolve_content_reference(element)

            # -------------------------------------
            # Type resolution
            # -------------------------------------
            # Parse the FHIR types of the element
            field_types = (
                [self._resolve_FHIR_type(field_type) for field_type in element.type]
                if element.type
                else []
            )
            # If element has no type, skip it
            if not field_types:
                continue

            # Unify types into single annotation
            field_type = (
                Union[tuple(field_types)] if len(field_types) > 1 else field_types[0]
            )

            # -------------------------------------
            # Cardinality
            # -------------------------------------
            # Get cardinality of element
            min_card, max_card = self._parse_element_cardinality(element)

            # -------------------------------------
            # Type choice elements
            # -------------------------------------
            if TYPE_CHOICE_SUFFIX in name:
                basename = name.strip(TYPE_CHOICE_SUFFIX)
                # Handle type choice elements
                fields.update(
                    self._construct_type_choice_fields(
                        basename,
                        field_types,
                        max_card,
                        element.short,
                    )
                )
                # Add validator to ensure only one of these fields is set
                validators.add_type_choice_validator(
                    field=basename,
                    allowed_types=field_types,
                    required=min_card > 0,
                )
                # Add property to access the values of the choice element without knowing the type set
                properties[basename] = partial(
                    fhir_validators.get_type_choice_value_by_base, base=basename
                )
                continue

            # Start by not setting any default value (important, 'None' implies optional in Pydantic)
            field_default = _Unset

            # -------------------------------------
            # Pattern value constraints
            # -------------------------------------
            if pattern_value := self._process_pattern_or_fixed_values(
                element, "pattern"
            ):
                field_default = pattern_value
                # Add the current field to the list of validated fields
                validators.add(
                    f"FHIR_{name}_pattern_constraint",
                    field_validator(safe_field_name, mode="after")(
                        partial(
                            fhir_validators.validate_FHIR_element_pattern,
                            pattern=pattern_value,
                        )
                    ),
                )

            # -------------------------------------
            # Fixed value constraints
            # -------------------------------------
            if fixed_value := self._process_pattern_or_fixed_values(element, "fixed"):
                # Use enum with single choice since Literal definition does not work at runtime
                singleChoice = Enum(
                    f"{name}FixedValue",
                    [("fixedValue", fixed_value)],
                    type=type(fixed_value),
                )
                field_default = fixed_value
                field_type = singleChoice

            # -------------------------------------
            # Fixed value constraints
            # -------------------------------------
            if constraints := element.constraint:
                # Process FHIR constraint invariants on the element
                for constraint in constraints:
                    validators.add_element_constraint_validator(
                        safe_field_name, constraint, base
                    )

            # -------------------------------------
            # Slicing
            # -------------------------------------
            if element.slices:
                # Process FHIR slicing on the element
                assert isinstance(field_type, type) and issubclass(
                    field_type, BaseModel
                ), f"Expected field_type to be a BaseModel subclass but got {field_type} for element {element.path}"
                field_type = self._construct_annotated_sliced_field(
                    element.slices, field_type
                )
                # Add slicing cardinality validator for field
                validators.add_slicing_validator(field=safe_field_name)

            # -------------------------------------
            # Children elements
            # -------------------------------------
            elif element.children:
                # Process element children
                assert isinstance(field_type, type) and issubclass(
                    field_type, BaseModel
                ), f"Expected field_type to be a BaseModel subclass but got {field_type} for element {element.path}"
                backbone_model_name = capitalize(
                    self.Config.resource_name if self.Config else "Unknown"
                ).strip() + "".join(
                    [capitalize(label).strip() for label in element.path.split(".")[1:]]
                )
                field_subfields, subfield_validators, subfield_properties = (
                    self._process_FHIR_structure_into_Pydantic_components(
                        element, field_type
                    )
                )
                # -------------------------------------
                # Complex extensions
                # -------------------------------------
                if (
                    "extension" in element.children
                    and element.children["extension"].slices
                ):
                    extension_slice_base_type = get_complex_FHIR_type(
                        "Extension",
                        self.Config.FHIR_release if self.Config else "4.3.0",
                    )
                    extension_type = self._construct_annotated_sliced_field(
                        element.children["extension"].slices, extension_slice_base_type
                    )

                    # Get cardinality of extension element
                    extension_min_card, extension_max_card = (
                        self._parse_element_cardinality(element.children["extension"])
                    )
                    # Add slicing cardinality validator for field
                    subfield_validators.add_slicing_validator(field="extension")
                    field_subfields["extension"] = self._construct_Pydantic_field(
                        extension_type, extension_min_card, extension_max_card
                    )
                field_type = self._construct_model_with_properties(
                    backbone_model_name,
                    fields=field_subfields,
                    base=(field_type,),
                    validators=subfield_validators.get_all(),
                    properties=subfield_properties,
                    docstring=element.definition,
                )
                self.local_cache[backbone_model_name] = field_type

            # Handle Python reserved keywords for field names
            safe_field_name, validation_alias = self._handle_python_reserved_keyword(
                name
            )
            # Create and add the Pydantic field for the FHIR element
            fields[safe_field_name] = self._construct_Pydantic_field(
                field_type,
                min_card,
                max_card,
                default=field_default,
                description=element.short,
                validation_alias=validation_alias,
            )

            # -------------------------------------
            # Primitive extensions
            # -------------------------------------
            if hasattr(primitives, str(field_type)):
                # If the field is of primitive type, add aliased field to accomodate their extensions
                fields.update(self._construct_primitive_extension_field(name))
        return fields, validators, properties

    def construct_resource_model(
        self,
        canonical_url: str | None = None,
        structure_definition: Union[str, dict, StructureDefinition] | None = None,
        base_model: type[ModelT] | None = None,
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
        self.paths_in_processing: set[str] = set()
        self.local_cache: Dict[str, type[BaseModel]] = dict()

        # Resolve the FHIR structure definition
        _structure_definition = None
        if isinstance(structure_definition, StructureDefinition):
            _structure_definition = structure_definition
        elif isinstance(structure_definition, str):
            _structure_definition = self.repository.load_from_files(
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
                "StructureDefinition does not specify FHIR version, defaulting to 4.3.0."
            )
        self.Config = self.FactoryConfig(
            FHIR_release=get_FHIR_release_from_version(
                _structure_definition.fhirVersion or "4.3.0"
            ),
            FHIR_version=_structure_definition.fhirVersion or "4.3.0",
            resource_name=_structure_definition.name,
        )
        # Process the FHIR resource's elements & constraints into Pydantic fields & validators
        fields, validators, properties = (
            self._process_FHIR_structure_into_Pydantic_components(structure)
        )
        # Process resource-level constraints
        for constraint in structure.constraint or []:
            validators.add_model_constraint_validator(constraint)
        if "contained" in fields:
            validators.add(
                "contained_FHIR_resource_validator",
                field_validator("contained", mode="plain")(
                    partial(
                        fhir_validators.validate_contained_resource,
                        release=self.Config.FHIR_release,
                    )
                ),
            )
        # If the resource has metadata, prefill the information
        if "meta" in fields:
            Meta = get_complex_FHIR_type(
                "Meta", self.Config.FHIR_release if self.Config else "4.3.0"
            )
            fields["resourceType"] = (Literal[f"{resource_type}"], resource_type)
            fields["meta"] = (
                Optional[Meta],
                Field(
                    title="Meta",
                    description="Metadata about the resource.",
                    default=Meta(
                        profile=[_structure_definition.url],
                        versionId=_structure_definition.version,
                    ),
                ),
            )

        # Check if a base model is provided, otherwise determine it from the StructureDefinition
        if not (base := base_model):
            # Determine the base model to inherit from for the current resource
            if base_canonical_url := _structure_definition.baseDefinition:
                # TODO: Handle non-FHIRBaseModel bases
                print("Base canonical URL:", base_canonical_url)
                base = self.construction_cache.get(base_canonical_url, FHIRBaseModel)
            else:
                base = FHIRBaseModel

        # Construct the Pydantic model representing the FHIR resource
        model = self._construct_model_with_properties(
            self.Config.resource_name if self.Config else _structure_definition.name,
            fields=fields,
            base=(base,),
            validators=validators.get_all(),
            properties=properties,
            docstring=_structure_definition.description,
        )
        # Add the current model to the cache
        self.construction_cache[_structure_definition.url] = model
        return model

    def clear_cache(self):
        """
        Clears the factory cache.
        """
        self.construction_cache = {}


# Create default factory instance
factory = ResourceFactory()

# Public API
construct_resource_model = factory.construct_resource_model
