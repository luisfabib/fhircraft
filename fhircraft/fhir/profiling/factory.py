
from fhir.resources.R4B.elementdefinition import ElementDefinition
from fhir.resources.R4B.structuredefinition import StructureDefinition
from fhir.resources.R4B.fhirtypesvalidators import get_fhir_model_class
from fhir.resources.R4B.fhirtypes import MetaType
from fhir.resources.R4B.meta import Meta

from fhircraft.utils import get_dict_paths, load_env_variables, ensure_list, remove_none_dicts

from pydantic.v1 import ValidationError, create_model, validate_model, Extra
from pydantic.v1.error_wrappers import ErrorWrapper
from typing import List, Any, Tuple, Dict, Type, ClassVar, Union, Optional, get_origin, Literal

from fhircraft.fhir.profiling.constraint import Constraint
from fhircraft.fhir.profiling.slicing import SlicingGroup, Slice, Discriminator
from fhircraft.fhir.path.utils import split_fhirpath, join_fhirpath
from fhircraft.fhir.path import fhirpath

import datetime 
import json
import requests
import logging

BASE_ELEMENTS = ['text', 'extension', 'id', 'fhir_comments','resource_type']

PATTERN_FIELDS = [field for field in ElementDefinition.__fields__.keys() if field.startswith('pattern')]
FIXED_FIELDS = [field for field in ElementDefinition.__fields__.keys() if field.startswith('fixed')]

class FHIRError(Exception):
    """Exception for FHIR-related issues"""
    pass


def construct_with_profiled_elements(profile):
    """
    Constructs a FHIR resource with elements profiled by the given profile.

    Parameters:
        profile: The FHIR profile containing constraints and slicing information.
    
    Returns:
        The constructed FHIR resource with profiled elements.
    """    
    # Construct FHIR resource with empty structure 
    resource = profile.construct()
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
    
    for constraint in profile.__constraints__:
        if constraint.pattern:
            fhirpath.parse(constraint.path).update_or_create(resource, constraint.pattern)
        if constraint.fixedValue:
            fhirpath.parse(constraint.path).update_or_create(resource, constraint.fixedValue)            
    return resource


def initialize_slices(resource):
    """
    Initializes slices in the resource according to the slicing information in the profile.

    Parameters:
        resource: The FHIR resource
    Return:
        resource: The FHIR resource
    """
    profile = resource.__class__
    # Go over all slices
    for slicing in profile.__slicing__:
        if '[x]' in slicing.path: continue        
        slices_resources = []
        for slice in slicing.slices:  
            # Construct empty instance of the slice
            slice_resource = slice.pydantic_model.construct()
            # Go over its constraints and set any preset values given by the profile
            slice_resource = process_slice_constraints(slice_resource, slice)
            # Check if the slice is valid by the preset values and if more than one slice instance is allowed
            if not slice_resource.is_FHIR_complete and slice.max_cardinality>1:
                # Create multiple copies of the slice, unused copies will be deleted later
                SLICE_COPIES = 9
                slices_resources.extend([
                    slice_resource.copy(deep=True) 
                        for _ in range(min(slice.max_cardinality, SLICE_COPIES))
                ])
            else:
                # Otherwise just add the slice instance to the list of slices
                slices_resources.append(slice_resource)
        # Set the whole list of slices in the resource
        collection = fhirpath.parse(slicing.path).find_or_create(resource)       
        collection[0].set_literal(slices_resources)
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
            for field, value in constraint.profile.construct_with_profiled_elements().__dict__.items():
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
    for slicing in profile.__slicing__:
        if '[x]' in slicing.path: continue
        valid_elements = ensure_list(fhirpath.parse(slicing.path).get_value(resource))    
        for entry in valid_elements:
            if entry:
                if entry.__slicing__:
                    track_slice_changes(entry, value)        
                entry.__track_changes__ = value


def clean_elements_and_slices(resource, depth=0):
    profile = resource.__class__
    profile.validate_assignment = False
    # Remove unused/incomplete slices
    for slicing in profile.__slicing__:
        if '[x]' in slicing.path: continue
        valid_elements = ensure_list(fhirpath.parse(slicing.path).get_value(resource))

        valid_elements = [element for element in valid_elements if element or isinstance(element, bool)]
        if not valid_elements:
            continue
        logging.debug("\t"*(depth)+f'↪ {slicing.path}: {len(valid_elements)} elements')
        for slice in slicing.slices:
            # Get all the elements that conform to this slice's definition           
            sliced_entries = ensure_list(fhirpath.parse(slice.full_fhir_path).get_value(resource))       
            sliced_entries = [entry for entry in sliced_entries if entry is not None]
            logging.debug("\t"*(depth+1)+f'↪ {slice.full_fhir_path}: {len(sliced_entries)} elements')
            
            for n,entry in enumerate(sliced_entries):
                logging.debug("\t"*(depth+2)+f'↪ {slicing.path}:{slice.name}[{n}]  (Modified:{"✓" if entry.has_been_modified else "✗"} Complete:{"✓" if entry.is_FHIR_complete else "✗"}) {"-> DELETE" if (not entry.is_FHIR_complete and not entry.has_been_modified) and entry in valid_elements else ""}' )
                if not entry.is_FHIR_complete and not entry.has_been_modified and entry in valid_elements:
                    valid_elements.remove(entry)                
                elif entry.__slicing__:
                    clean_elements_and_slices(entry, depth=depth+3)                
        # Set the new list with only the valid slices
        fhirpath.parse(slicing.path).update_or_create(resource, valid_elements)       

    # Cleanup the resource from empty structures to be valid
    for field, value in remove_none_dicts(resource.dict()).items():
        setattr(resource, field, value)
    return resource

class ProfiledResourceFactory:
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
        structure_definition = response.json()
        # Disable certain incompatible validators             
        if 'extension' in structure_definition:
            structure_definition.pop('extension')
        ElementDefinition.__fields__['id'].validators = []
        # Parse JSON into a StructureDefinition model
        return StructureDefinition.parse_obj(structure_definition)
    
    def clear_chache(self):
        self.profiles = {}

    def construct_profiled_resource_model(self, profile_url):
        
        # Check the factory's profiles cache store
        cached_profile = self.profiles.get(profile_url)
        if cached_profile:
            return cached_profile
        
        # Get the profile's structure definition
        profile_definition = self.get_structure_definition(profile_url)
        
        # Determine the base resource from which this profile is derived
        try:
            base_model = get_fhir_model_class(profile_definition.type)
        except KeyError:
            raise FHIRError(f"Profile's base definition '{profile_definition.type}' is not a valid FHIR core resource.")

        # Get all patterns
        slicing = getattr(base_model, '__slicing__', []) 
        constraints = getattr(base_model, '__constraints__', []) 
        
            
        
        for element in profile_definition.snapshot.element: 
            if element.slicing:
                slicing.append(
                    SlicingGroup(
                        id=element.id,
                        path=element.path,
                        discriminators=[Discriminator(type=d.type, path=d.path) for d in element.slicing.discriminator],
                        description=element.slicing.description,
                        rules=element.slicing.rules,
                        ordered=element.slicing.ordered,
                )
            )

        for element in profile_definition.snapshot.element: 
            if element.sliceName:
                slice_group = next((slice_group for slice_group in slicing if slice_group.path == element.path), None) 
                slice = Slice(
                    id=element.id,
                    name=element.sliceName,
                    type=element.type[0].code,
                )
                slice_group.add_slice(slice)        

        for element in profile_definition.snapshot.element:
            constraint = Constraint(
                id=element.id,
                path=element.path,
                min=int(element.min) if str(element.min).isnumeric() else None,
                max=int(str(element.max).replace('*','99999')) if str(element.max).replace('*','99999').isnumeric() else None,
            )
            if element.type and element.type[0].code=='Extension' and element.type[0].profile:
                constraint.profile = construct_profiled_resource_model(element.type[0].profile[0])
            if element.type:
                constraint.valueType = [type.code for type in element.type]
                
            for pattern_field in PATTERN_FIELDS:
                pattern_value = getattr(element, pattern_field, None)
                if pattern_value is not None: 
                    constraint.pattern = pattern_value

            for fixed_field in FIXED_FIELDS:
                fixed_value = getattr(element, fixed_field, None)
                if fixed_value: 
                    constraint.fixedValue = fixed_value
                       
            if ':' in constraint.id or any([slice_group.path in constraint.path for slice_group in slicing]):
                for slice_group in slicing:
                    if ':' in constraint.id:  
                        slice = slice_group.get_slice_by_name(constraint.get_constrained_slice_name())
                        if slice:
                            slice.add_constraint(constraint)
                    # else: 
                    #     for slice in slice_group.slices:
                    #         slice.add_constraint(constraint)   
            else: 
                constraints.append(constraint)
                        
        class ProfiledModel(base_model):
            __canonical_url__: ClassVar[str] = profile_url
            __slicing__: ClassVar[List[SlicingGroup]] = slicing
            __constraints__: ClassVar[List[Constraint]] = constraints
            resourceType: Optional[str] = base_model.__name__
            meta: MetaType = Meta(profile=[profile_url], versionId=profile_definition.version)
            
            class Config:
                underscore_attrs_are_private = True
                validate_assignment = False
          
            @classmethod
            def construct_with_profiled_elements(cls):
                return construct_with_profiled_elements(cls)

            @classmethod
            def clean_elements_and_slices(cls, resource):
                return clean_elements_and_slices(resource)
            
        profile_model = create_model(__model_name=profile_definition.name, __base__=ProfiledModel) 
        
        # Cache the profile
        factory.profiles.update({
            profile_url: profile_model
        })
        return profile_model

    def _check_if_path_ancestors_exist(self, resource, fhir_path):
        segments = split_fhirpath(fhir_path)
        path = segments[0] 
        for segment in segments[1:-1]:
            parent_fhir_path = join_fhirpath(path, segment)
            child_elements = fhirpath.parse(parent_fhir_path).get_value(resource)
            if not child_elements:
                return False
        return True
    
    def _validate_constraint(self, constrained_elements, constraint, path=None):
        validation_errors = []
        if constrained_elements is None:
            constrained_elements = []
        if not isinstance(constrained_elements, list):
            constrained_elements = [constrained_elements]
        for constrained_element in constrained_elements:
            if constrained_element is None:
                continue
            # Check for pattern constraints
            if constraint.pattern:
                if not constrained_element.dict() | constraint.pattern.dict() == constrained_element.dict():
                    validation_errors.append(ErrorWrapper(
                    ValueError(f'Value does not fulfill pattern:\n{json.dumps(constraint.pattern.dict(),indent=4)}'), 
                        f'{path or constraint.path}'
                    ))
                    
            if constraint.fixedValue:
                pass 
                                    
            if constraint.valueType:
                FHIR_TYPES = {
                    'string': str,
                    'dateTime': (datetime.datetime,datetime.date),
                    'instant': datetime.datetime,
                    'time': datetime.time,
                    'date': datetime.date,
                    'boolean': bool,
                    'integer': int,
                    'code': str,
                    'uri': str,
                    'url': str,
                    'http://hl7.org/fhirpath/System.String': str,
                }
                if not any([isinstance(constrained_element,FHIR_TYPES.get(type) or get_fhir_model_class(type)) for type in constraint.valueType]): 
                    validation_errors.append(ErrorWrapper(
                    TypeError(f'Value must be of type: {",".join([type.title()for type in constraint.valueType])}'), 
                        f'{path or constraint.path}'
                    ))
                        
        # Checkj for cardinality constraints
        cardinality = len(constrained_elements)
        if constraint.min:            
            if cardinality < constraint.min:
                validation_errors.append(ErrorWrapper(
                    ValueError(f'Element {constraint.path} violates min. cardinality ({cardinality}<{constraint.min}).'),
                    f'{constraint.id}'
            )) 
        if constraint.max:      
            if cardinality > constraint.max:
                validation_errors.append(ErrorWrapper(
                    ValueError(f'Element {constraint.path} violates max. cardinality ({cardinality}>{constraint.max}).'),
                    f'{constraint.id}'
                ))    
        return validation_errors
    
    
    def validate(self, resource, profile=None):
        
        if not profile:
            profile = resource.__class__
        validation_errors = []

        # Core validation
        *_, validation_error = validate_model(profile, resource.dict())
        if validation_error:
            validation_errors += [ErrorWrapper(error.exc, error._loc) for raw_errors in validation_error.raw_errors  for error in raw_errors ]

        # Evaluate profile constraints
        for constraint in profile.__constraints__:
            if constraint.is_slice_constraint:
                continue
            # Get the element that is constrained in the resource
            constrained_element = fhirpath.parse(constraint.path).get_value(resource)   
            if not constrained_element:
                # If the element does not exist, check if its ancestor exist
                if not self._check_if_path_ancestors_exist(resource, constraint.path):
                    # If not, means that the parent elements do not exist, so do not validate the constraint
                    continue   
            # Validate the constraint(s) for this element(s)
            validation_errors += self._validate_constraint(constrained_element, constraint) 
            
        # Slicing validation    
        for slice_group in profile.__slicing__:
            for slice in slice_group.slices:
                sliced_entries = fhirpath.parse(slice.full_fhir_path).get_value(resource)   

                if not isinstance(sliced_entries, list): 
                    sliced_entries = [sliced_entries]
                sliced_entries = [entry for entry in sliced_entries if entry is not None]
                for entry in sliced_entries:
                    # Perform basic validation
                    *_, subvalidation_errors = validate_model(entry.__class__, entry.dict())
                    if subvalidation_errors:
                        validation_errors += [ErrorWrapper(error.exc, f'{slice_group.path}:{slice.name}.{error._loc}')  for raw_errors in subvalidation_errors.raw_errors  for error in raw_errors ]
                    # Apply core resource validation
                    for validator in entry.__class__.__pre_root_validators__ + entry.__class__.__post_root_validators__:
                        try: 
                            validator(entry.__class__, entry.dict())
                        except ValidationError as validation_error:
                            validation_errors.append(ErrorWrapper(
                                validation_error, 
                                f'{slice_group.path}:{slice.name}'
                            ))
                # Check for all constraints on the current slice
                for constraint in slice.constraints:
                    slice_subpath = constraint.path.replace(slice_group.path,"$")    
                    # Constrains on elements of the slice should only be applied if the slice is present
                    if constraint.path != slice_group.path and len(sliced_entries)==0:
                        continue       
                    if constraint.path == slice_group.path:        
                        # Validate the constraint(s) for this slice element(s)
                        validation_errors += self._validate_constraint(sliced_entries, constraint, f'{slice_group.path}:{slice.name}{slice_subpath}') 
                    else:
                        for entry in sliced_entries:
                            constrained_slice_elements = fhirpath.parse(slice_subpath).get_value(entry)   
                            # Get the element that is constrained in the resource
                            if not constrained_slice_elements:
                                # If the element does not exist, check if its ancestor exist
                                if not self._check_if_path_ancestors_exist(entry, slice_subpath):
                                    # If not, means that the parent elements do not exist, so do not validate the constraint
                                    continue     
                            validation_errors += self._validate_constraint(constrained_slice_elements, constraint, f'{slice_group.path}:{slice.name}{slice_subpath}') 
        # IF there are any validation issues, raise them                     
        if validation_errors:
            raise ValidationError(validation_errors, profile)                     
        else:
            logging.debug('Resource successfully validated')


factory = ProfiledResourceFactory()
construct_profiled_resource_model = factory.construct_profiled_resource_model
validate_profiled_resource = factory.validate
clear_chache = factory.clear_chache