import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.resources.datatypes import get_FHIR_type

from fhircraft.fhir.resources.base import FHIRBaseModel, FHIRSliceModel
import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.constraint import Constraint
from fhircraft.fhir.resources.slicing import SlicingGroup, Slice, Discriminator
from fhircraft.fhir.path import fhirpath
from fhircraft.utils import capitalize, load_env_variables, ensure_list, remove_none_dicts

from typing import List, Any, Tuple, Dict, Type, ClassVar, Union, Optional, get_origin, Literal
from pydantic import Field, create_model, model_validator, BaseModel, field_validator
from pydantic_core import PydanticUndefined
_Unset: Any = PydanticUndefined

from functools import partial
from typing_extensions import Annotated 
from enum import Enum
import requests
import inspect

class ResourceFactory:
    profiles : dict = {}
    
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
        """Builds a tree from a list of ElementDefinitions."""
        tree = {}
        for element in elements:
            path_parts = element['id'].split('.')
            current = tree
            for part in path_parts:
                if ':' in part:
                    part, sliceName = part.split(':')
                    current = current['children'][part]
                    if 'slices' not in current:
                        current['slices'] = {}
                    if sliceName not in current['slices']:
                        current['slices'][sliceName] = {}
                    current = current['slices'][sliceName]
                else:
                    if 'children' not in current:
                        current['children'] = {}
                    if part not in current['children']:
                        current['children'][part] = {}
                    current = current['children'][part]
            # Keep only the name and type, ignore slices
            current.update(element)
        return tree

    def _parse_element_type(self, field_type_name: str, FHIR_release: str):      
        FHIR_COMPLEX_TYPE_PREFIX = 'http://hl7.org/fhir/StructureDefinition/'
        FHIRPATH_TYPE_PREFIX = 'http://hl7.org/fhirpath/System.'
        field_type_name = str(field_type_name)
        field_type_name = field_type_name.removeprefix(FHIR_COMPLEX_TYPE_PREFIX)
        field_type_name = field_type_name.removeprefix(FHIR_COMPLEX_TYPE_PREFIX)
        field_type_name = field_type_name.removeprefix(FHIRPATH_TYPE_PREFIX)
        field_type_name = capitalize(field_type_name)
        # Check if type is a FHIR primitive datatype
        field_type = getattr(primitives, field_type_name, None)
        if not field_type:
            # Check if type is a FHIR complex datatype
            field_type = get_FHIR_type(field_type_name, FHIR_release)
        if not field_type:
            return field_type_name
        return field_type


    def _construct_Pydantic_field(self, field_type, min_card, max_card, default=_Unset, description=None, alias=None):
        is_list_type = not max_card or max_card>1
        if is_list_type:
            field_type = List[field_type]
            default = [default] if default is not _Unset and not isinstance(default, list) else default
        if min_card==0:
            field_type = Optional[field_type]
            default = None
        return (    
            field_type, 
                Field(
                    default,
                    alias=alias,
                    description=description,
                    min_length=min_card if is_list_type else None,
                    max_length=max_card if is_list_type else None
            )
        )    
    
    def _process_pattern_or_fixed_values(self, element, constraint, FHIR_release):
        constraint_attribute = next((attribute for attribute in element if attribute.startswith(constraint)), None)
        if (constrained_value := element.get(constraint_attribute)) is not None:
            cosntrained_type = self._parse_element_type(constraint_attribute.replace(constraint,''), FHIR_release)
            constrained_value = cosntrained_type.model_validate(constrained_value) \
                                if inspect.isclass(cosntrained_type) and issubclass(cosntrained_type, BaseModel) \
                                    else constrained_value    
        return constrained_value


    def process_element_slices(self, element, resourceName, field_type, FHIR_release):
        slice_types = []
        for slice_name, slice_element in element['slices'].items():
            if (slice_element_types := slice_element.get('type')) and (slice_element_canonical_urls := slice_element_types[0].get('profile')):
                slice_model = self.construct_resource_model(slice_element_canonical_urls[0])
                slice_model_name = capitalize(resourceName) + capitalize(slice_model.__name__)
                slice_model = create_model(slice_model_name, __base__=(slice_model, FHIRSliceModel))                                   
            else:
                # Construct the slice model's name
                slice_name = ''.join([capitalize(word) for word in slice_name.split('-')])
                slice_model_name = capitalize(resourceName) + capitalize(slice_name)
                # Process and compile all subfields of the slice
                slice_subfields, slice_validators, slice_properties = self._compile_complex_element_fields(slice_element, slice_model_name, FHIRSliceModel, FHIR_release)
                # Construct the slice model
                slice_model = create_model(slice_model_name, **slice_subfields, __base__=(field_type, FHIRSliceModel), __validators__=slice_validators)                                   
                # Set the properties
                for attribute, property_getter in slice_properties.items():
                    setattr(slice_model, attribute, property(property_getter))  
            # Store the specific slice cardinality
            slice_model.min_cardinality=int(slice_element['min']) if str(slice_element['min']).isnumeric() else None
            slice_model.max_cardinality=int(str(slice_element['max']).replace('*','99999')) if str(slice_element['max']).replace('*','99999').isnumeric() else None
            # Store the slice model in the list of slices of the element
            slice_types.append(slice_model)    
        # Create annotated type as union of slice models and original type (important, last in the definition) 
        return Annotated[
            Union[tuple([*slice_types, field_type])], 
            Field(union_mode='left_to_right')
        ]

    def _compile_profile_constraints(self, elements, FHIR_release):
        slicing = []
        constraints = []
        for element in elements: 
            if element.get('slicing'):
                slicing.append(
                    SlicingGroup(
                        id=element['id'],
                        path=element['path'],
                        discriminators=[Discriminator(type=d['type'], path=d['path']) for d in element['slicing']['discriminator']],
                        description=element['slicing'].get('description'),
                        rules=element['slicing'].get('rules'),
                        ordered=element['slicing'].get('ordered'),
                )
            )

            if element.get('sliceName'):
                slice = Slice(
                    id=element['id'],
                    name=element['sliceName'],
                    type=element['type'][0]['code'],
                )
                slice_group = next((slice_group for slice_group in slicing if slice_group.path == element['path']), None) 
                slice_group.add_slice(slice)        

            constraint = Constraint(
                id=element['id'],
                path=element['path'],
                min=int(element['min']) if str(element['min']).isnumeric() else None,
                max=int(str(element['max']).replace('*','99999')) if str(element['max']).replace('*','99999').isnumeric() else None,
            )
            if element.get('type') and element['type'][0]['code']=='Extension' and element['type'][0].get('profile'):
                constraint.profile = self.construct_resource_model(element['type'][0]['profile'][0])
            if element.get('type'):
                constraint.valueType = [type['code'] for type in element['type']]
            
            pattern_attribute = next((attribute for attribute in element if attribute.startswith('pattern')), None)
            pattern_value = element.get(pattern_attribute)
            if pattern_value is not None:
                pattern_type = self._parse_element_type(pattern_attribute.replace('pattern',''), FHIR_release)
                if inspect.isclass(pattern_type) and issubclass(pattern_type, BaseModel):
                    constraint.pattern = pattern_type.model_validate(pattern_value)
                else:
                    constraint.pattern = pattern_value

            fixed_attribute = next((attribute for attribute in element if attribute.startswith('fixed')), None)
            fixed_value = element.get(fixed_attribute)
            if fixed_value is not None:
                fixed_type = self._parse_element_type(fixed_attribute.replace('fixed',''), FHIR_release)
                if inspect.isclass(fixed_type) and issubclass(fixed_type, BaseModel):
                    constraint.fixedValue = fixed_type.model_validate(fixed_value)
                else:
                    constraint.fixedValue = fixed_value
                       
            if ':' in constraint.id or any([slice_group.path in constraint.path for slice_group in slicing]):
                for slice_group in slicing:
                    if ':' in constraint.id:  
                        slice = slice_group.get_slice_by_name(constraint.get_constrained_slice_name())
                        if slice:
                            slice.add_constraint(constraint)
            else: 
                constraints.append(constraint)

        return slicing, constraints

    def _add_model_constraint_validator(self, constraint: dict, validators: dict) -> dict:
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

    def _compile_complex_element_fields(self, structure, resourceName, base, FHIR_release):
        fields = {}
        validators = {}
        properties = {}
        for name, element in structure.get('children',{}).items():
            if base and name in base.model_fields:
                continue 
            
            # Get cardinality of element
            min_card = int(element['min'])
            max_card = int(element['max']) if element['max'] != '*' else None

            # Parse the FHIR types of the element
            field_types = [self._parse_element_type(field_type['code'], FHIR_release) for field_type in element.get('type', [])]

            # TODO: Handle more gracefully. 
            # If has no type, skip element
            if not field_types:
                continue 

            # Handle multi-type cases
            if len(field_types) > 0:
                # Handle type choice elements
                if '[x]' in name: 
                    # Get base name
                    name = name.replace('[x]','')
                    # Create a field for each type
                    for field_type in field_types:
                        typed_field_name = name + (field_type if isinstance(field_type, str) else field_type.__name__)
                        fields[typed_field_name] = self._construct_Pydantic_field(field_type, min_card, max_card, description=element.get('short'))
                    # Add validator to ensure only one of these fields is set                
                    validators[f'{name}_type_choice_validator'] = model_validator(mode='after')(
                        partial(
                            fhir_validators.validate_type_choice_element, 
                            field_types=field_types, 
                            field_name_base=name
                        )
                    )
                    properties[name] = partial(fhir_validators.get_type_choice_value_by_base, base=name)
                    continue
                else:
                    if len(field_types) > 1:
                        # Accept all types 
                        field_type = Union[tuple(field_types)]                 
                    else:
                        # Get single type
                        field_type = field_types[0]
            else: 
                continue
            
            field_default = _Unset 
            # Check for pattern value constraints
            if pattern_value := self._process_pattern_or_fixed_values(element, 'pattern', FHIR_release):
                field_default = pattern_value
                # Add the current field to the list of validated fields
                validators[f'FHIR_{name}_pattern_constraint'] = field_validator(name, mode='after')(partial(
                    fhir_validators.validate_FHIR_element_pattern, 
                    pattern=pattern_value,
                ))

            # Check for fixed value constraints
            if fixed_value := self._process_pattern_or_fixed_values(element, 'fixed', FHIR_release):
                singleChoice = Enum(
                    f"{element}FixedValue",
                    [('fixedValue',fixed_value)],
                    type=type(fixed_value),
                )
                field_default = singleChoice.fixedValue 
                field_type = singleChoice

            if constraints := element.get('constraint'):
                # Process FHIR constraint invariants on the element
                for constraint in constraints:
                    validators = self._add_element_constraint_validator(name, constraint, base, validators)

            # If the element has child elements (e.g. BackboneElement) create the complex element and use it as a type
            if element.get('slices'):
                field_type = self.process_element_slices(element, resourceName, field_type, FHIR_release)

            # If the element has child elements create the complex element and use it as a type
            elif element.get('children'):
                backbone_model_name = capitalize(resourceName + capitalize(name))
                field_subfields, subfield_validators, subfield_properties = self._compile_complex_element_fields(element, backbone_model_name, field_type, FHIR_release)
                for attribute, property_getter in subfield_properties.items():
                    setattr(field_type, attribute, property(property_getter))      
                if element['children']['extension'].get('slices'):
                    extension_type = self.process_element_slices(element['children']['extension'], backbone_model_name, get_FHIR_type('Extension', FHIR_release), FHIR_release)
                    extension_min_card = int(element['children']['extension']['min'])
                    extension_max_card = int(element['children']['extension']['max']) if element['children']['extension']['max'] != '*' else None
                    field_subfields['extension'] = self._construct_Pydantic_field(extension_type, extension_min_card, extension_max_card)
                field_type = create_model(backbone_model_name, **field_subfields, __base__=field_type, __validators__=subfield_validators)                
      

            # Create and add the Pydantic field for the FHIR element
            fields[name] = self._construct_Pydantic_field(field_type, min_card, max_card, default=field_default, description=element.get('short'))
            if hasattr(primitives, str(field_type)):
                fields[f'{name}_ext'] = self._construct_Pydantic_field(get_FHIR_type('Element', FHIR_release), 0, 1, alias=f'_{name}', default=field_default, description=f'Placeholder element for {name} extensions')
        
        return fields, validators, properties
        

    def construct_resource_model(self, canonical_url=None, structure_definition=None):
        
        if not structure_definition and canonical_url:
            structure_definition = self.download_structure_definition(canonical_url)
        
        if 'snapshot' not in structure_definition or 'element' not in structure_definition['snapshot']:
            raise ValueError("Invalid StructureDefinition: Missing 'snapshot' or 'element' field")
        
        elements = structure_definition['snapshot']['element']
        tree = self.build_tree_structure(elements)

        FHIR_release = get_FHIR_release_from_version(structure_definition['fhirVersion'])
        resourceType = structure_definition['type']
        resourceName = structure_definition['name']
        
        structure = tree['children'][resourceType]
        
        if get_FHIR_type(resourceType, FHIR_release):
            base = FHIRBaseModel
            fields, validators, properties = self._compile_complex_element_fields(structure, resourceName, None, FHIR_release)            
        else:
            base = get_FHIR_type('Resource', FHIR_release)
            fields, validators, properties = self._compile_complex_element_fields(structure, resourceName, None, FHIR_release)
        
        for constraint in structure['constraint']:
            validators = self._add_model_constraint_validator(constraint, validators)
        
        slicing, constraints = self._compile_profile_constraints(elements, FHIR_release)
        
        
        fields.update({
            'profile_slicing': (ClassVar[List[SlicingGroup]], slicing),
            'canonical_url': (ClassVar[List[Constraint]], canonical_url),
            'profile_constraints': (ClassVar[List[Constraint]], constraints),
        })
        
        if 'meta' in fields:
            fields['resourceType'] = (Literal[f'{resourceType}'], resourceType)
            fields['meta'] = (
                Optional[get_FHIR_type('Meta', FHIR_release)], 
                get_FHIR_type('Meta', FHIR_release)(
                    profile=[structure_definition['url']], 
                    versionId=structure_definition['version']
                )
            )


        # Construct the Pydantic model 
        model = create_model(
            resourceName, **fields, 
            __base__ = FHIRBaseModel,
            __validators__ = validators,
            __doc__ = structure['short'],
        )        
        for attribute, property_getter in properties.items():
            setattr(model, attribute, property(property_getter))

        self.profiles['resourceName'] = model
        
        return model 
    
    def clear_chache(self):
        self.profiles = {}


    def construct_dataelement_model(self, structure_definition):
        
        if 'snapshot' not in structure_definition or 'element' not in structure_definition['snapshot']:
            raise ValueError("Invalid StructureDefinition: Missing 'snapshot' or 'element' field")
        
        elements = structure_definition['snapshot']['element']
        tree = self.build_tree_structure(elements)

        FHIR_release = get_FHIR_release_from_version(structure_definition['fhirVersion'])
        resourceType = structure_definition['type']
        resourceName = structure_definition['name']
        
        structure = tree['children'][resourceType]
        if 'baseDefinition' in structure_definition:
            base_name = structure_definition['baseDefinition'].replace('http://hl7.org/fhir/StructureDefinition/','')
            base = self.profiles.get(base_name)
        else:
            base = FHIRBaseModel
        fields, validators, properties = self._compile_complex_element_fields(structure, resourceName, base, FHIR_release)

        for constraint in structure.get('constraint',[]):
            validators = self._add_model_constraint_validator(constraint, validators)
        
        model = create_model(resourceName, **fields, __base__=base, __validators__=validators)
        model.__doc__ = structure['short']

        for attribute, property_getter in properties.items():
            setattr(model, attribute, property(property_getter))


        self.profiles[resourceName] = model

        return model 
    
    def clear_chache(self):
        self.profiles = {}



def get_FHIR_release_from_version(version):
    version = version.split('-')[0]
    version = tuple([int(digit) for digit in version.split('.')])
    if version >= (0,4,0) and version <= (1,0,2):
        return 'DSTU2'
    elif version >= (1,1,0) and version <= (3,0,2):
        return 'STU3'
    elif version >= (3,2,0) and version <= (4,0,1):
        return 'R4'
    elif version >= (4,1,0) and version <= (4,3,0):
        return 'R4B'
    elif version >= (4,2,0) and version <= (5,0,0):
        return 'R5'
    elif version >= (6,0,0):
        return 'R6'



# def process_slice_constraints(slice_resource, slice):
#     """
#     Processes and sets constraints within a slice.

#     Parameters:
#         slice_resource: The FHIR resource of the corresponding slice
#         slice: The slice containing constraints.
#     Returns:
#         slice_resource: The FHIR resource of the corresponding slice    
#     """
#     for constraint in slice.constraints:
#         slice_element = constraint.path.replace(slice.slicing.path, '').lstrip('.')
#         if '[x]' in slice_element:
#             continue
        
#         if constraint.profile:
#             for field, value in construct_with_profiled_elements(constraint.profile).__dict__.items():
#                 if field in slice_resource.model_fields and value:
#                     setattr(slice_resource, field, value)
#             return slice_resource
        
#         if constraint.fixedValue:
#             fhirpath.parse(slice_element).update_or_create(slice_resource, constraint.fixedValue)       
#         if constraint.pattern:
#             if slice_element == '':
#                 for field, value in constraint.pattern.__dict__.items():
#                     setattr(slice_resource, field, value)
#             else:
#                 fhirpath.parse(slice_element).update_or_create(slice_resource, constraint.pattern)       
    
#     return slice_resource


def track_slice_changes(resource, value):
    profile = resource.__class__
    for element in profile.get_sliced_elements():
        valid_elements = [col.value for col in fhirpath.parse(element).find_or_create(resource) if col.value is not None]        
        for entry in valid_elements:
            if isinstance(entry, FHIRSliceModel):
                entry.__track_changes__ = value
            elif hasattr(entry, 'get_sliced_elements'):
                track_slice_changes(entry, value)        


def clean_elements_and_slices(resource):
    profile = resource.__class__
    print('CLEANING: ', profile)
    profile.validate_assignment = False
    # Remove unused/incomplete slices
    for element, slices in profile.get_sliced_elements().items():
        valid_elements = [col.value for col in fhirpath.parse(element).find_or_create(resource) if col.value is not None]        
        valid_elements = [element for element in valid_elements if element or isinstance(element, bool)]
        new_valid_elements = []
        if not valid_elements:
            continue
        for slice in slices:
            print('        Slice: ', slice)
            # Get all the elements that conform to this slice's definition           
            sliced_entries = [entry for entry in valid_elements if isinstance(entry, slice)] 
            for entry in sliced_entries:
                if entry.get_sliced_elements():
                    entry = clean_elements_and_slices(entry) 
                if (entry.is_FHIR_complete and entry.has_been_modified) \
                    or (entry.is_FHIR_complete  and not entry.has_been_modified and slice.min_cardinality>0):
                    if entry not in new_valid_elements:
                        new_valid_elements.append(entry)                

        # Set the new list with only the valid slices
        collection = fhirpath.parse(element).find_or_create(resource)
        [col.set_literal(new_valid_elements) for col in collection]
        

    return resource


factory = ResourceFactory()
construct_resource_model = factory.construct_resource_model
clear_chache = factory.clear_chache