#!/usr/bin/env python
"""
Pydantic FHIR Model Factory
"""

# Internal modules
import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.resources.datatypes import get_complex_FHIR_type
from fhircraft.fhir.resources.base import FHIRBaseModel, FHIRSliceModel
from fhircraft.utils import capitalize, load_env_variables, ensure_list, get_FHIR_release_from_version

# Pydantic modules
from pydantic import Field, create_model, model_validator, BaseModel, field_validator
from pydantic_core import PydanticUndefined
from pydantic.dataclasses import dataclass

# Standard modules
from enum import Enum
from functools import partial
from typing import List, Any, Dict, Union, Optional, Literal, Tuple
from typing_extensions import Annotated 
from collections import defaultdict
import requests
import inspect

_Unset: Any = PydanticUndefined

class ResourceFactory:
    
    @dataclass
    class FactoryConfig:
        """Represents the configuration for the Factory class.

        Attributes:
            FHIR_release (str): The FHIR release version.
            resource_name (str): The name of the resource.
        """
        FHIR_release: str
        resource_name: str
    
    Config: Optional[FactoryConfig]
    construction_cache : Dict[str, BaseModel] = {}
    
    def download_structure_definition(self, profile_url: str) -> Dict[str, Any]:
        """
        Retrieves the structure definition of a FHIR resource from the provided profile URL.
        
        Parameters:
            profile_url (str): The URL of the FHIR profile from which to retrieve the structure definition.
            
        Returns:
            Dict[str, Any]: A dictionary representing the structure definition of the FHIR resource.
        """       
        
        if not profile_url.endswith('.json'):
            # Construct endpoint URL for the StructureDefinition JSON
            if profile_url.startswith('http://hl7.org/fhir/StructureDefinition'):
                domain, resource = profile_url.rsplit('/', 1)
                domain = domain.replace('http://hl7.org/fhir/StructureDefinition','https://hl7.org/fhir/R4/extension')
                resource = resource.lower()
            else:
                domain, resource = profile_url.rsplit('/', 1)
            json_url = f"{domain}-{resource}.json"
        else:
            json_url = profile_url

        # Configure proxy if needed
        settings = load_env_variables()
        proxies = {
            'https': settings.get('PROXY_URL_HTTPS'), 
            'http': settings.get('PROXY_URL_HTTP')
        } if settings.get('PROXY_URL_HTTPS') or settings.get('PROXY_URL_HTTP') else None
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        # Download the StructureDefinition JSON            
        response = requests.get(json_url, proxies=proxies, verify=settings.get('CERTIFICATE_BUNDLE_PATH'), headers=headers)     
        response.raise_for_status()
        return response.json()
        

    def build_tree_structure(self, elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds a tree from a list of ElementDefinitions.

        Parameters:
            elements (List[Dict[str, Any]]): A list of ElementDefinitions to build the tree from.

        Returns:
            Dict[str, Any]: A tree structure representing the ElementDefinitions.
        """
        tree = defaultdict(dict)
        for element in elements:
            current = tree
            for part in element['id'].split('.'):
                if ':' in part:
                    # Handle slice definitions
                    part, sliceName = part.split(':')
                    current = current['children'][part]
                    current['slices'] = current.get('slices', {})
                    current = current['slices'].setdefault(sliceName, {})
                else:
                    # Handle children elements
                    current['children'] = current.get('children', {})
                    current = current['children'].setdefault(part, {})
            current.update(element)
        return tree

    def _get_complex_FHIR_type(self, field_type_name: str) -> Union[type,str]:     
        """
        Parses and loads the FHIR element type based on the provided field type name.

        Args:
            field_type_name (str): The name of the field type to be parsed.

        Returns:
            Union[type, str]: The parsed FHIR element type, returns input string if type not found.
        """         
        FHIR_COMPLEX_TYPE_PREFIX = 'http://hl7.org/fhir/StructureDefinition/'
        FHIRPATH_TYPE_PREFIX = 'http://hl7.org/fhirpath/System.'
        # Pre-process the type string
        field_type_name = str(field_type_name)
        field_type_name = field_type_name.removeprefix(FHIR_COMPLEX_TYPE_PREFIX)
        field_type_name = field_type_name.removeprefix(FHIRPATH_TYPE_PREFIX)
        field_type_name = capitalize(field_type_name)
        # Check if type is a FHIR primitive datatype
        field_type = getattr(primitives, field_type_name, None)
        if not field_type:
            # Check if type is a FHIR complex datatype
            field_type = get_complex_FHIR_type(field_type_name, self.Config.FHIR_release)
        if not field_type:
            return field_type_name
        return field_type

    def _create_model_with_properties(self, name: str, fields: dict, base: Union[Tuple[type], type], validators: dict, properties: dict) -> BaseModel:
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
    
    def _construct_Pydantic_field(self, field_type: type, min_card: int, max_card: int, 
                default: Any=_Unset, description: Optional[str]=None, alias: Optional[str]=None
        ) -> Field:
        """ 
        Constructs a Pydantic field based on the provided parameters.

        Args:
            field_type (type): The type of the field.
            min_card (int): The minimum cardinality of the field.
            max_card (int): The maximum cardinality of the field.
            default (Any, optional): The default value of the field. Defaults to _Unset.
            description (str, optional): The description of the field. Defaults to None.
            alias (str, optional): The alias of the field. Defaults to None.

        Returns:
            Field: The constructed Pydantic field.
        """        
        # Determine whether typing should be a list based on max. cardinality
        is_list_type = max_card is None or max_card>1
        if is_list_type:
            field_type = List[field_type]
            default = ensure_list(default) if default is not _Unset else default
        # Determine whether the field is optional
        if min_card==0:
            field_type = Optional[field_type]
            default = None
        # Construct the Pydantic field
        return (    
            field_type, Field(
                default,
                alias=alias,
                description=description,
                min_length=min_card if is_list_type else None,
                max_length=max_card if is_list_type else None
            )
        )    
    
    def _process_pattern_or_fixed_values(self, element: Dict[str, Any], constraint_prefix: str) -> Any:
        """
        Process the pattern or fixed values of a StructureDefinition element.

        Parameters:
            element (Dict[str, Any]): The element to process.
            constraint_prefix (str): The prefix indicating pattern or fixed values.

        Returns:
            Any: The constrained value after processing.
        """        
        # Determine the name of the StructureDefinition element's attribute that starts with either the prefix 'fixed[x]' or 'pattern[x]' 
        constraint_attribute = next((attribute for attribute in element if attribute.startswith(constraint_prefix)), None)
        if (constrained_value := element.get(constraint_attribute)) is not None:
            # Get the type of value that is constrained to a preset value
            constrained_type = self._get_complex_FHIR_type(constraint_attribute.replace(constraint_prefix,''))
            # Parse the value
            constrained_value = constrained_type.model_validate(constrained_value) \
                                if inspect.isclass(constrained_type) and issubclass(constrained_type, BaseModel) \
                                    else constrained_value    
        return constrained_value

    def _process_choice_type_field(self, name, field_types, cardinality, fields, validators, properties, description=None):
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
        name = name.replace('[x]','')
        # Create a field for each type
        for field_type in field_types:
            typed_field_name = name + (field_type if isinstance(field_type, str) else field_type.__name__)
            fields[typed_field_name] = self._construct_Pydantic_field(field_type, cardinality[0], cardinality[1], description=description)
        # Add validator to ensure only one of these fields is set                
        validators[f'{name}_type_choice_validator'] = model_validator(mode='after')(
            partial(
                fhir_validators.validate_type_choice_element, 
                field_types=field_types, 
                field_name_base=name
            )
        )
        properties[name] = partial(fhir_validators.get_type_choice_value_by_base, base=name)
        return fields, validators, properties

    def _process_element_slices(self, element: dict, field_type: type) -> Annotated:
        """
        Process the FHIR element slices to construct Pydantic models.

        Args:
            element (dict): The element containing slice information.
            field_type (type): The type of the field.

        Returns:
            Annotated:  A union of slice models and the original type.
        """
        slice_types = []
        for slice_name, slice_element in element['slices'].items():
            if (slice_element_types := slice_element.get('type')) and (slice_element_canonical_urls := slice_element_types[0].get('profile')):
                # Construct the slice model from the canonical URL
                slice_model = ResourceFactory().construct_resource_model(slice_element_canonical_urls[0], base_model=FHIRSliceModel)
            else:
                # Construct the slice model's name
                slice_name = ''.join([capitalize(word) for word in slice_name.split('-')])
                slice_model_name = capitalize(slice_name)
                # Process and compile all subfields of the slice
                slice_subfields, slice_validators, slice_properties = self._process_FHIR_structure_into_Pydantic_components(slice_element, FHIRSliceModel)
                # Construct the slice model
                slice_model = self._create_model_with_properties(slice_model_name, 
                                    fields=slice_subfields, 
                                    base=(field_type, FHIRSliceModel), 
                                    validators=slice_validators, 
                                    properties=slice_properties
                )
            # Store the specific slice cardinality
            slice_model.min_cardinality, slice_model.max_cardinality = self._process_cardinality_constraints(slice_element)
            # Store the slice model in the list of slices of the element
            slice_types.append(slice_model)    
        # Create annotated type as union of slice models and original type (important, last in the definition) 
        return Annotated[
            Union[tuple([*slice_types, field_type])], 
            Field(union_mode='left_to_right')
        ]
        
    def _process_cardinality_constraints(self, element):
        """
        Process the cardinality constraints of a FHIR element.

        Args:
            element (Dict[str, Any]): The element containing cardinality information.

        Returns:
            Tuple[int, int]: A tuple containing the minimum and maximum cardinality values.
        """
        min_card = int(element['min']) if str(element['min']).isnumeric() else None
        max_card = int(max_string) if (max_string := str(element['max']).replace('*','99999')).isnumeric() else None
        return min_card, max_card

    def _add_model_constraint_validator(self, constraint: dict, validators: dict) -> dict:
        """
        Adds a model constraint validator based on the provided constraint.

        Args:
            constraint (dict): The constraint details including expression, human-readable description, key, and severity.
            validators (dict): The dictionary of validators to update with the new constraint validator.

        Returns:
            dict: The updated dictionary of validators.
        """        
        # Construct function name for validator
        constraint_name = constraint['key'].replace('-','_')
        validator_name = f"FHIR_{constraint_name}_constraint_model_validator"
        # Add the current field to the list of validated fields
        validators[validator_name] = model_validator(mode='after')(partial(
            fhir_validators.validate_model_constraint, 
            expression=constraint['expression'],
            human=constraint['human'],
            key=constraint['key'],
            severity=constraint['severity'],
        ))
        return validators
            
    def _add_element_constraint_validator(self, field: str, constraint: dict, base: Any, validators: dict) -> dict:
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
        constraint_name = constraint['key'].replace('-','_')
        validator_name = f"FHIR_{constraint_name}_constraint_validator"
        # Check if validator has already been constructed for another field
        validate_fields = [field]
        # Get the list of fields already being validated by this constraint
        if validator_name in validators:
            validate_fields.extend(validators.get(validator_name).decorator_info.fields)
        # Get the list of fields already being validated by this constraint in base model
        if base and validator_name in base.__pydantic_decorators__.field_validators:
            validate_fields.extend(base.__pydantic_decorators__.field_validators[validator_name].info.fields) 
        # Add the current field to the list of validated fields
        validators[validator_name] = field_validator(*validate_fields, mode='after')(partial(
            fhir_validators.validate_element_constraint, 
            expression=constraint['expression'],
            human=constraint['human'],
            key=constraint['key'],
            severity=constraint['severity'],
        ))
        return validators

    def _process_FHIR_structure_into_Pydantic_components(self, structure: dict, base: BaseModel=None):
        """
        Processes the FHIR structure elements into Pydantic components.

        Args:
            structure (dict): The structure containing FHIR elements.
            base (BaseModel, optional): The base model to check for existing validators. Defaults to None.

        Returns:
            Tuple[dict, dict, dict]: A tuple containing fields, validators, and properties.
        """        
        fields = {}
        validators = {}
        properties = {}
        for name, element in structure.get('children',{}).items():
            if base and name in base.model_fields:
                continue 
            # Get cardinality of element
            min_card, max_card = self._process_cardinality_constraints(element)
            # Parse the FHIR types of the element
            field_types = [self._get_complex_FHIR_type(field_type['code']) for field_type in element.get('type', [])]
            # If has no type, skip element
            if not field_types:
                continue 
            # Handle type choice elements
            if '[x]' in name: 
                fields, validators, properties = self._process_choice_type_field(
                    name, field_types, [min_card, max_card], fields, validators, properties, 
                    description=element.get('short')
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
            if pattern_value := self._process_pattern_or_fixed_values(element, 'pattern'):
                field_default = pattern_value
                # Add the current field to the list of validated fields
                validators[f'FHIR_{name}_pattern_constraint'] = field_validator(name, mode='after')(partial(
                    fhir_validators.validate_FHIR_element_pattern, 
                    pattern=pattern_value,
                ))
            # Check for fixed value constraints
            if fixed_value := self._process_pattern_or_fixed_values(element, 'fixed'):
                # Use enum with single choice since Literal definition does not work at runtime
                singleChoice = Enum(
                    f"{name}FixedValue",
                    [('fixedValue',fixed_value)],
                    type=type(fixed_value),
                )
                field_default = singleChoice.fixedValue 
                field_type = singleChoice
            # Process FHIR constraint invariants on the element
            if constraints := element.get('constraint'):
                for constraint in constraints:
                    validators = self._add_element_constraint_validator(name, constraint, base, validators)
            # Process FHIR slicing on the element, if present
            if element.get('slices'):
                field_type = self._process_element_slices(element, field_type)
                # Add slicing cardinality validator for field
                validators[f'{name}_slicing_cardinality_validator'] = field_validator(name, mode='after')(partial(
                    fhir_validators.validate_slicing_cardinalities, field_name=name)
                )                
            # Process element children, if present
            elif element.get('children'):
                backbone_model_name = capitalize(self.Config.resource_name).strip() + capitalize(name).strip()
                field_subfields, subfield_validators, subfield_properties = self._process_FHIR_structure_into_Pydantic_components(element, field_type)
                for attribute, property_getter in subfield_properties.items():
                    setattr(field_type, attribute, property(property_getter))      
                if element['children']['extension'].get('slices'):
                    extension_type = self._process_element_slices(element['children']['extension'], get_complex_FHIR_type('Extension', self.Config.FHIR_release))
                    # Get cardinality of extension element
                    extension_min_card, extension_max_card = self._process_cardinality_constraints(element['children']['extension'])
                    # Add slicing cardinality validator for field
                    subfield_validators[f'extension_slicing_cardinality_validator'] = field_validator('extension', mode='after')(partial(
                        fhir_validators.validate_slicing_cardinalities, field_name='extension')
                    )                               
                    field_subfields['extension'] = self._construct_Pydantic_field(extension_type, extension_min_card, extension_max_card)
                field_type = create_model(backbone_model_name, **field_subfields, __base__=field_type, __validators__=subfield_validators)                
            # Create and add the Pydantic field for the FHIR element
            fields[name] = self._construct_Pydantic_field(
                field_type, min_card, max_card, 
                default=field_default, 
                description=element.get('short')
            )
            # IF the field is of primitive type, add aliased field to accomodate their extensions
            if hasattr(primitives, str(field_type)):
                fields[f'{name}_ext'] = self._construct_Pydantic_field(
                    get_complex_FHIR_type('Element'), 
                    min_card=0, max_card=1, 
                    alias=f'_{name}', 
                    default=field_default, 
                    description=f'Placeholder element for {name} extensions'
                )
        return fields, validators, properties
        

    def construct_resource_model(self, canonical_url: str=None, structure_definition: dict=None, base_model: type=FHIRBaseModel) -> FHIRBaseModel:
        """
        Constructs a Pydantic model based on the provided FHIR structure definition.

        Args:
            canonical_url (dict): The FHIR resource's or profile's canonical URL from which to download the StructureDefinition.
            structure_definition (dict): The FHIR StructureDefinition to build the model from.

        Returns:
            model (BaseModel): The constructed Pydantic model representing the FHIR resource.
        """
        # If the model has been constructed before, return the cached model
        if canonical_url in self.construction_cache:
            return self.construction_cache[canonical_url]
        # Download the FHIR structure definition if the canonical URL has been specified        
        if not structure_definition and canonical_url:
            structure_definition = self.download_structure_definition(canonical_url)
        # Check that the snapshot is available in the FHIR structure definition
        if 'snapshot' not in structure_definition or 'element' not in structure_definition['snapshot']:
            raise ValueError("Invalid StructureDefinition: Missing 'snapshot' or 'element' field")
        # Pre-process the snapshort elements into a tree structure to simplify model construction later
        tree = self.build_tree_structure(structure_definition['snapshot']['element'])
        resource_type = structure_definition['type']
        structure = tree['children'][resource_type]
        # Configure the factory for the current FHIR environment
        self.Config = self.FactoryConfig(
            FHIR_release = get_FHIR_release_from_version(structure_definition['fhirVersion']), 
            resource_name = structure_definition['name'], 
        )
        # Process the FHIR resource's elements & constraints into Pydantic fields & validators
        fields, validators, properties = self._process_FHIR_structure_into_Pydantic_components(structure)
        # Process resource-level constraints 
        for constraint in structure['constraint']:
            validators = self._add_model_constraint_validator(constraint, validators)
        # If the resource has metadata, prefill the information       
        if 'meta' in fields:
            fields['resourceType'] = (
                Literal[f'{resource_type}'], resource_type
            )
            fields['meta'] = (
                Optional[get_complex_FHIR_type('Meta', self.Config.FHIR_release)], 
                get_complex_FHIR_type('Meta', self.Config.FHIR_release)(
                    profile=[structure_definition['url']], 
                    versionId=structure_definition['version']
                )
            )
        # Construct the Pydantic model representing the FHIR resource
        model = self._create_model_with_properties(self.Config.resource_name, 
            fields=fields, 
            base=base_model, 
            validators=validators, 
            properties=properties
        )            
        # Add the current model to the cache
        self.construction_cache[canonical_url] = model
        return model 
    

    def construct_dataelement_model(self, structure_definition):
        if 'snapshot' not in structure_definition or 'element' not in structure_definition['snapshot']:
            raise ValueError("Invalid StructureDefinition: Missing 'snapshot' or 'element' field")
        resource_type = structure_definition['type']
        elements = structure_definition['snapshot']['element']
        tree = self.build_tree_structure(elements)        
        # Configure the factory for the current FHIR environment
        self.Config = self.FactoryConfig(
            FHIR_release = get_FHIR_release_from_version(structure_definition['fhirVersion']), 
            resource_name = structure_definition['name'], 
        )
        structure = tree['children'][resource_type]
        if 'baseDefinition' in structure_definition:
            base_name = structure_definition['baseDefinition'].replace('http://hl7.org/fhir/StructureDefinition/','')
            base = self.construction_cache.get(base_name)
        else:
            base = FHIRBaseModel
        fields, validators, properties = self._process_FHIR_structure_into_Pydantic_components(structure, base)
        for constraint in structure.get('constraint',[]):
            validators = self._add_model_constraint_validator(constraint, validators)
        model = create_model(self.Config.resource_name, **fields, __base__=base, __validators__=validators)
        model.__doc__ = structure['short']
        for attribute, property_getter in properties.items():
            setattr(model, attribute, property(property_getter))
        return model 
    
    def clear_chache(self):
        """
        Clears the factory cache.
        """
        self.construction_cache = {}

factory = ResourceFactory()
construct_resource_model = factory.construct_resource_model
clear_chache = factory.clear_chache