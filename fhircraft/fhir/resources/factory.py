import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.resources.datatypes import get_FHIR_type

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.constraint import Constraint
from fhircraft.fhir.resources.slicing import SlicingGroup, Slice, Discriminator
from fhircraft.fhir.path import fhirpath
from fhircraft.utils import capitalize, load_env_variables, ensure_list, remove_none_dicts

from typing import List, Any, Tuple, Dict, Type, ClassVar, Union, Optional, get_origin, Literal
from pydantic import Field, create_model, model_validator, BaseModel, field_validator
from functools import partial
import requests
import inspect

class ResourceFactory:
    profiles : dict = {}
    
    def get_structure_definition(self, profile_url: str) -> Dict[str, Any]:
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
            path_parts = element['path'].split('.')
            current = tree
            for part in path_parts:
                if 'children' not in current:
                    current['children'] = {}
                if part not in current['children']:
                    current['children'][part] = {}
                current = current['children'][part]
            
            # Keep only the name and type, ignore slices
            if ':' not in element['id']:  # Ignore slices
                current.update(element)
        return tree

    def _parse_element_type(self, field_type_name):
        if not field_type_name:
            return None
        field_type_name = field_type_name.replace('http://hl7.org/fhir/StructureDefinition/','')
        field_type_name = field_type_name.replace('http://hl7.org/fhirpath/System.','')
        field_type_name = capitalize(field_type_name)
        field_type = getattr(primitives, field_type_name, None)
        if not field_type:
            field_type = get_FHIR_type(field_type_name)
        if not field_type:
            return field_type_name
        return field_type


    def _construct_Pydantic_field(self, field_type, min_card, max_card, description=None, alias=None):
        default = None
        is_list_type = not max_card or max_card>1
        if is_list_type:
            field_type = List[field_type]
        if min_card==0:
            field_type = Optional[field_type]
        return (    
            field_type, 
                Field(
                    alias=alias,
                    default=default,
                    description=description,
                    min_length=min_card if is_list_type else None,
                    max_length=max_card if is_list_type else None
            )
        )    

    def _compile_profile_constraints(self, elements):
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
                pattern_type = self._parse_element_type(pattern_attribute.replace('pattern',''))
                if inspect.isclass(pattern_type) and issubclass(pattern_type, BaseModel):
                    constraint.pattern = pattern_type.model_validate(pattern_value)
                else:
                    constraint.pattern = pattern_value

            fixed_attribute = next((attribute for attribute in element if attribute.startswith('fixed')), None)
            fixed_value = element.get(fixed_attribute)
            if fixed_value is not None:
                fixed_type = self._parse_element_type(fixed_attribute.replace('fixed',''))
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

    def _compile_complex_element_fields(self, structure, resourceName, base):
        fields = {}
        validators = {}
        properties = {}
        for name, element in structure['children'].items():
            if base and name in base.model_fields:
                continue 

            # Get cardinality of element
            min_card = int(element['min'])
            max_card = int(element['max']) if element['max'] != '*' else None

            # Parse the FHIR types of the element
            field_types = [self._parse_element_type(field_type['code']) for field_type in element.get('type', [])]

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
            if element.get('constraint'):
                for constraint in element['constraint']:
                    validators = self._add_element_constraint_validator(name, constraint, base, validators)
            
            # If the element has child elements (e.g. BackboneElement) create the complex element and use it as a type
            if field_type is get_FHIR_type('BackboneElement') and element.get('children'):
                field_subfields, subfield_validators, subfield_properties = self._compile_complex_element_fields(element, capitalize(resourceName + capitalize(name)), field_type)
                field_type = create_model(capitalize(resourceName + capitalize(name)), **field_subfields, __base__=field_type, __validators__=subfield_validators)                
                for attribute, property_getter in properties.items():
                    setattr(field_type, attribute, property(property_getter))            

            # Create and add the Pydantic field for the FHIR element
            fields[name] = self._construct_Pydantic_field(field_type, min_card, max_card, description=element.get('short'))
            if hasattr(primitives, str(field_type)):
                fields[f'{name}_ext'] = self._construct_Pydantic_field(get_FHIR_type('Element'), 0, 1, alias=f'_{name}',description=f'Placeholder element for {name} extensions')
        return fields, validators, properties
        

    def construct_resource_model(self, canonical_url=None, structure_definition=None):
        
        if not structure_definition and canonical_url:
            structure_definition = self.get_structure_definition(canonical_url)
        
        if 'snapshot' not in structure_definition or 'element' not in structure_definition['snapshot']:
            raise ValueError("Invalid StructureDefinition: Missing 'snapshot' or 'element' field")
        
        elements = structure_definition['snapshot']['element']
        tree = self.build_tree_structure(elements)

        resourceType = structure_definition['type']
        resourceName = structure_definition['name']
        
        structure = tree['children'][resourceType]
        
        if get_FHIR_type(resourceType):
            base = get_FHIR_type('Extension')
            fields, validators, properties = {}, {}, {}
        else:
            base = get_FHIR_type('Resource')
            fields, validators, properties = self._compile_complex_element_fields(structure, resourceName, get_FHIR_type('Resource'))
        
        for constraint in structure['constraint']:
            validators = self._add_model_constraint_validator(constraint, validators)
        
        slicing, constraints = self._compile_profile_constraints(elements)
        
        
        
        fields['meta'] = (Optional[get_FHIR_type('Meta')], get_FHIR_type('Meta')(profile=[structure_definition['url']], versionId=structure_definition['version']))
        fields['resourceType'] = (Literal[f'{resourceType}'], resourceType)
        fields['profile_slicing'] = (ClassVar[List[SlicingGroup]], slicing)
        fields['canonical_url'] = (ClassVar[List[Constraint]], canonical_url)
        fields['profile_constraints'] = (ClassVar[List[Constraint]], constraints)

        model = create_model(resourceName, **fields, __base__=base, __validators__=validators)
        model.__doc__ = structure['short']
        for attribute, property_getter in properties.items():
            setattr(model, attribute, property(property_getter))

        return model 
    
    def clear_chache(self):
        self.profiles = {}


    def construct_dataelement_model(self, structure_definition):
        
        if 'snapshot' not in structure_definition or 'element' not in structure_definition['snapshot']:
            raise ValueError("Invalid StructureDefinition: Missing 'snapshot' or 'element' field")
        
        elements = structure_definition['snapshot']['element']
        tree = self.build_tree_structure(elements)

        resourceType = structure_definition['type']
        resourceName = structure_definition['name']
        
        structure = tree['children'][resourceType]
        if 'baseDefinition' in structure_definition:
            base_name = structure_definition['baseDefinition'].replace('http://hl7.org/fhir/StructureDefinition/','')
            base = self.profiles.get(base_name)
        else:
            base = BaseModel
        fields, validators, properties = self._compile_complex_element_fields(structure, resourceName, base)

        for constraint in structure.get('constraint',[]):
            validators = self._add_model_constraint_validator(constraint, validators)
        
        # slicing, constraints = self._compile_profile_constraints(elements)
        
        # fields['meta'] = (Optional[complex_types.Meta], complex_types.Meta(profile=[structure_definition['url']], versionId=structure_definition['version']))
        # fields['resourceType'] = (Literal[f'{resourceType}'], resourceType)
        # fields['profile_slicing'] = (ClassVar[List[SlicingGroup]], slicing)
        # fields['canonical_url'] = (ClassVar[List[Constraint]], canonical_url)
        # fields['profile_constraints'] = (ClassVar[List[Constraint]], constraints)

        model = create_model(resourceName, **fields, __base__=base, __validators__=validators)
        model.__doc__ = structure['short']

        for attribute, property_getter in properties.items():
            setattr(model, attribute, property(property_getter))


        self.profiles[resourceName] = model

        return model 
    
    def clear_chache(self):
        self.profiles = {}






def construct_with_profiled_elements(profile):
    """
    Constructs a FHIR resource with elements profiled by the given profile.

    Parameters:
        profile: The FHIR profile containing constraints and slicing information.
    
    Returns:
        The constructed FHIR resource with profiled elements.
    """    
    # Construct FHIR resource with empty structure 
    resource = profile.model_construct()
    resource = set_constraints(resource)
    resource = initialize_slices(resource)
    return resource


def set_constraints(resource):
    """
    Sets preset values in the resource according to the constraints in the profile.

    Parameters:
        resource: The initialized FHIR resource
        profile: The FHIR profile containing constraints.
    Return:
        resource: The FHIR resource
    """
    profile = resource.__class__
    
    for constraint in profile.profile_constraints:
        if constraint.pattern:
            fhirpath.parse(constraint.path).update_or_create(resource, constraint.pattern)
        if constraint.fixedValue:
            fhirpath.parse(constraint.path).update_or_create(resource, constraint.fixedValue)            
    return resource


def initialize_slices(resource, slice_copies=9):
    """
    Initializes slices in the resource according to the slicing information in the profile.

    Parameters:
        resource: The FHIR resource
    Return:
        resource: The FHIR resource
    """
    profile = resource.__class__
    # Go over all slices
    for slicing in profile.profile_slicing:
        if '[x]' in slicing.path: continue        
        slices_resources = []
        for slice in slicing.slices:  
            # Construct empty instance of the slice
            slice_resource = slice.get_pydantic_model(resource).model_construct()
            # Go over its constraints and set any preset values given by the profile
            slice_resource = process_slice_constraints(slice_resource, slice)
            # Check if the slice is valid by the preset values and if more than one slice instance is allowed
            if not slice_resource.is_FHIR_complete and slice.max_cardinality>1:
                # Create multiple copies of the slice, unused copies will be deleted later
                slices_resources.extend([
                    slice_resource.model_copy(deep=True) 
                        for _ in range(min(slice.max_cardinality, slice_copies))
                ])
            else:
                # Otherwise just add the slice instance to the list of slices
                slices_resources.append(slice_resource)
        # Set the whole list of slices in the resource
        collection = fhirpath.parse(slicing.path).find_or_create(resource)
        for col in collection:
            col.set_literal(slices_resources)

    return resource


def process_slice_constraints(slice_resource, slice):
    """
    Processes and sets constraints within a slice.

    Parameters:
        slice_resource: The FHIR resource of the corresponding slice
        slice: The slice containing constraints.
    Returns:
        slice_resource: The FHIR resource of the corresponding slice    
    """
    for constraint in slice.constraints:
        slice_element = constraint.path.replace(slice.slicing.path, '').lstrip('.')
        if '[x]' in slice_element:
            continue
        
        if constraint.profile:
            for field, value in construct_with_profiled_elements(constraint.profile).__dict__.items():
                if field in slice_resource.model_fields and value:
                    setattr(slice_resource, field, value)
            return slice_resource
        
        if constraint.fixedValue:
            fhirpath.parse(slice_element).update_or_create(slice_resource, constraint.fixedValue)       
        if constraint.pattern:
            if slice_element == '':
                for field, value in constraint.pattern.__dict__.items():
                    setattr(slice_resource, field, value)
            else:
                fhirpath.parse(slice_element).update_or_create(slice_resource, constraint.pattern)       
    
    return slice_resource


def track_slice_changes(resource, value):
    profile = resource.__class__
    for slicing in profile.profile_slicing:
        if '[x]' in slicing.path: continue
        valid_elements = ensure_list(fhirpath.parse(slicing.path).get_value(resource))    
        for entry in valid_elements:
            if entry:
                if getattr(entry,'profile_slicing', None):
                    track_slice_changes(entry, value)        
                entry.__track_changes__ = value


def clean_elements_and_slices(resource, depth=0):
    profile = resource.__class__
    profile.validate_assignment = False
    # Remove unused/incomplete slices
    for slicing in profile.profile_slicing:
        if '[x]' in slicing.path: continue
        valid_elements = ensure_list(fhirpath.parse(slicing.path).get_value(resource))

        valid_elements = [element for element in valid_elements if element or isinstance(element, bool)]
        if not valid_elements:
            continue
        print("\t"*(depth)+f'↪ {slicing.path}: {len(valid_elements)} elements')
        for slice in slicing.slices:
            # Get all the elements that conform to this slice's definition           
            sliced_entries = ensure_list(fhirpath.parse(slice.full_fhir_path).get_value(resource))       
            sliced_entries = [entry for entry in sliced_entries if entry is not None]
            print("\t"*(depth+1)+f'↪ {slice.full_fhir_path}: {len(sliced_entries)} elements')
            
            for n,entry in enumerate(sliced_entries):
                print("\t"*(depth+2)+f'↪ {slicing.path}:{slice.name}[{n}]  (Modified:{"✓" if entry.has_been_modified else "✗"} Complete:{"✓" if entry.is_FHIR_complete else "✗"}) {"-> DELETE" if (not entry.is_FHIR_complete and not entry.has_been_modified) and entry in valid_elements else ""}' )
                if not entry.is_FHIR_complete and not entry.has_been_modified and entry in valid_elements:
                    valid_elements.remove(entry)                
                elif entry.profile_slicing:
                    clean_elements_and_slices(entry, depth=depth+3)                
        # Set the new list with only the valid slices
        collection = fhirpath.parse(slicing.path).find_or_create(resource)
        for col in collection:
            col.set_literal(valid_elements)
    return resource


factory = ResourceFactory()
construct_resource_model = factory.construct_resource_model
clear_chache = factory.clear_chache