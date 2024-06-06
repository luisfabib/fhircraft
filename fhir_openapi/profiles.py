
from fhir.resources.R4B.elementdefinition import ElementDefinition
from fhir.resources.R4B.structuredefinition import StructureDefinition
from fhir.resources.core.utils.common import is_list_type, get_fhir_type_name, is_primitive_type
from fhir.resources.R4B.fhirtypesvalidators import get_fhir_model_class
from fhir.resources.R4B.fhirtypes import MetaType
from fhir.resources.R4B.meta import Meta

from fhir_openapi.utils import get_dict_paths, load_env_variables, ensure_list, remove_none_dicts

from pydantic.v1 import ValidationError, create_model, validate_model, Extra
from pydantic.v1.error_wrappers import ErrorWrapper
from typing import List, Any, Tuple, Dict, Type, ClassVar, Union, Optional, get_origin
from dataclasses import dataclass, field
from fhir_openapi.path import FHIRPathNavigator, split_fhirpath, join_fhirpath
from copy import deepcopy
import datetime 
import json
import requests


PATTERN_FIELDS = [field for field in ElementDefinition.__fields__.keys() if field.startswith('pattern')]
FIXED_FIELDS = [field for field in ElementDefinition.__fields__.keys() if field.startswith('fixed')]

class FHIRError(Exception):
    """Exception for FHIR-related issues"""
    pass

@dataclass
class FHIRConstraint:
    key: Optional[str] = None
    severity: Optional[str] = None
    human: Optional[str] = None
    expression: Optional[str] = None
    xpath: Optional[str] = None

@dataclass
class FHIRBinding:
    strength: Optional[str] = None
    valueSet: Optional[str] = None

@dataclass
class FHIRPattern:
    value: Optional[Union[str, float, int, Dict[str, Union[str, float, int]]]] = None

@dataclass
class FHIRProfileConstraint:
    id: str
    path: str
    min: int
    max: int
    profile: Optional[object] = None
    valueType: Optional[List[str]] = field(default_factory=list)
    fixedValue: Optional[Union[str, float, int, Dict[str, Union[str, float, int]]]] = None
    pattern: Optional[Union[str, float, int, Dict[str, Union[str, float, int]]]] = None
    binding: Optional[FHIRBinding] = None
    constraints: Optional[List[FHIRConstraint]] = field(default_factory=list)

    @property
    def is_slice_constraint(self):
        return ':' in self.id

    def get_constrained_slice_name(self):
        slice_name = self.id.split(':')[1].split('.')[0]
        return slice_name

@dataclass
class FHIRDiscriminator:
    type: str  # E.g., "pattern"
    path: str  # E.g., "code"
    
@dataclass
class FHIRExtension:
    id : str
    name : str
    path : str
    url: str
    constraints: List[FHIRProfileConstraint] = field(default_factory=list)
        
@dataclass
class FHIRSlice:
    id : str
    name : str
    type: str  # Type of the slice
    constraints: List[FHIRProfileConstraint] = field(default_factory=list)
    slicing_group: Optional[object] = None
    
    @property
    def min_cardinality(self):
        return min([constraint.min for constraint in self.constraints if constraint.min and constraint.path == self.slicing_group.path])       
    
    @property
    def profile_constraint(self):
        return next((constraint.profile for constraint in self.constraints if constraint.profile and constraint.path == self.slicing_group.path),None)       
    
    @property
    def max_cardinality(self):
        return max([constraint.max for constraint in self.constraints if constraint.max and constraint.path == self.slicing_group.path])       
    
    
    def add_constraint(self, constraint):
        self.constraints.append(constraint)
    
    @property
    def pydantic_model(self):       
        
        base_model, element = self.slicing_group.path.rsplit('.',1)
        if element.lower() == 'extension':
            model = get_fhir_model_class('Extension')
        else:
            element = get_fhir_model_class(base_model).__fields__.get(element)
            if not element:
                return None
            model = get_fhir_model_class(element.type_.__resource_type__)
        
        class ProfiledSlice(model, extra=Extra.allow):
            __track_changes__: bool = False 
            __has_been_modified__: bool = False
            __slicing__: ClassVar[List[FHIRSlicing]] = self.profile_constraint.__slicing__ if self.profile_constraint else None

            def __setattr__(self, name:str, value):
                super().__setattr__(name, value)
                if name not in ['__track_changes__','__has_been_modified__'] and self.__track_changes__:
                    super().__setattr__('__has_been_modified__', True)
            
            @property
            def is_FHIR_complete(self):
                BASE_ELEMENTS = ['text', 'extension', 'id', 'fhir_comments','resource_type']
                slice_available_elements = sorted(set([name for name in self.__class__.__fields__ if '__' not in name and name not in BASE_ELEMENTS]))
                slice_preset_elements = sorted(set([name for name, value in self.dict().items() if (value is not None or value!=[]) and '__' not in name and name not in BASE_ELEMENTS]))
                return slice_available_elements == slice_preset_elements
            
            @property
            def has_been_modified(self):
                if self.__has_been_modified__: 
                    return True
                else:
                    for element in self.__dict__.values():
                        elements = ensure_list(element)
                        for _element in elements:
                            if getattr(_element, 'has_been_modified', None):
                                return True
                return False
            
        slice_model = create_model(__model_name=model.__name__, __base__=ProfiledSlice) 
        slice_model.validate_assignment = False
        return slice_model
    
    @property
    def discriminator_values(self):
        for discriminator_path in self.slicing_group.discriminator_paths:
            for constraint in self.constraints:
                if constraint.pattern and discriminator_path == constraint.path:
                    return get_dict_paths(constraint.pattern.dict(), prefix=discriminator_path.replace(self.slicing_group.path,''))
        return {}
    
    @property
    def fhirpath(self):
        fhir_path = self.slicing_group.path
        for path, value in self.discriminator_values.items():
            if path.startswith('.'): path = path[1:]
            fhir_path = join_fhirpath(fhir_path, f'where({path}="{value}")')       
        if self.profile_constraint:
            if fhir_path.rsplit('.' ,1)[1] == 'extension':
                fhir_path = fhir_path.rsplit('.',1)[0]
            fhir_path = join_fhirpath(fhir_path, f'extension("{self.profile_constraint.__canonical_url__}")')   
        return fhir_path 

@dataclass
class FHIRSlicing:
    id : str
    path: str  # The path within the resource where slicing is applied
    discriminators: List[FHIRDiscriminator]  # List of discriminators used for slicing
    description: Optional[str] = None  # Optional description of the slicing
    rules: Optional[str] = "open"  # Rules for the slicing, default is "open"
    slices: List[FHIRSlice] = field(default_factory=list)  # List to hold the slices
    
    def get_slice_by_name(self, slice_name):
        return next((slice for slice in self.slices if slice.name == slice_name), None)
    
    @property
    def discriminator_paths(self) -> str:
        return [
            join_fhirpath(self.path, discriminator.path) 
                if discriminator.path!='$this' else self.path 
                    for discriminator in self.discriminators
        ]
        
    def add_slice(self, slice: FHIRSlice):
        slice.slicing_group = self
        self.slices.append(slice)
    
    def has_discriminator_type(self, discriminator_type: str) -> bool:
        return any(discriminator.type == discriminator_type for discriminator in self.discriminators)

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
    navigator = FHIRPathNavigator(resource)
    for constraint in profile.__constraints__:
        if constraint.pattern:
            navigator.set_value(constraint.path, constraint.pattern)
        if constraint.fixedValue:
            navigator.set_value(constraint.path, constraint.fixedValue)
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
    navigator = FHIRPathNavigator(resource)
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
        navigator.set_value(slicing.path, slices_resources)
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
    slice_navigator = FHIRPathNavigator(slice_resource)    
    for constraint in slice.constraints:
        slice_element = constraint.path.replace(slice.slicing_group.path, '').lstrip('.')
        if '[x]' in slice_element:
            continue
        
        if constraint.profile:
            for field, value in constraint.profile.construct_with_profiled_elements().__dict__.items():
                setattr(slice_resource, field, value)
            return slice_resource
        
        if constraint.fixedValue:
            slice_navigator.set_value(slice_element, constraint.fixedValue)
        
        if constraint.pattern:
            if slice_element == '':
                for field, value in constraint.pattern.__dict__.items():
                    setattr(slice_resource, field, value)
            else:
                is_list = is_list_type(slice_navigator.get_pydantic_field(slice_element))
                pattern = [constraint.pattern] if is_list and not isinstance(constraint.pattern, list) else constraint.pattern
                slice_navigator.set_value(slice_element, pattern)
    return slice_resource


def track_slice_changes(resource, value):
    profile = resource.__class__
    navigator = FHIRPathNavigator(resource)    
    for slicing in profile.__slicing__:
        if '[x]' in slicing.path: continue
        valid_elements = ensure_list(navigator.get_value(slicing.path))
        for entry in valid_elements:
            if entry:
                if entry.__slicing__:
                    track_slice_changes(entry, value)        
                entry.__track_changes__ = value


def clean_elements_and_slices(resource, depth=0):
    profile = resource.__class__
    profile.validate_assignment = False
    navigator = FHIRPathNavigator(resource)    
    # Remove unused/incomplete slices
    for slicing in profile.__slicing__:
        if '[x]' in slicing.path: continue
        valid_elements = ensure_list(navigator.get_value(slicing.path))
        valid_elements = [element for element in valid_elements if element is not None]
        if not valid_elements:
            continue
        print("\t"*(depth)+f'↪ {slicing.path}: {len(valid_elements)} elements')
        for slice in slicing.slices:
            # Get all the elements that conform to this slice's definition           
            sliced_entries = ensure_list(navigator.get_value(slice.fhirpath))
            sliced_entries = [entry for entry in sliced_entries if entry is not None]
            print("\t"*(depth+1)+f'↪ {slice.fhirpath}: {len(sliced_entries)} elements')
            
            for n,entry in enumerate(sliced_entries):
                print("\t"*(depth+2)+f'↪ {slicing.path}:{slice.name}[{n}]  (Modified:{"✓" if entry.has_been_modified else "✗"} Complete:{"✓" if entry.is_FHIR_complete else "✗"}) {"-> DELETE" if (not entry.is_FHIR_complete and not entry.has_been_modified) and entry in valid_elements else ""}' )
                if not entry.is_FHIR_complete and not entry.has_been_modified and entry in valid_elements:
                    valid_elements.remove(entry)                
                elif entry.__slicing__:
                    clean_elements_and_slices(entry, depth=depth+3)                
        # Set the new list with only the valid slices
        navigator.set_value(slicing.path, valid_elements)
        
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
        extensions = getattr(base_model, '__extensions__', []) 
        
                
        for element in profile_definition.snapshot.element: 
            if element.slicing and any([type.code == 'Extension' for type in element.type]):
                extensions.append(
                    FHIRExtension(
                        id=element.id,
                        path=element.path,
                        name=element.sliceName,
                        url=next((type.profile for type in element.type), None)
                )
            )
        
        for element in profile_definition.snapshot.element: 
            if element.slicing:
                slicing.append(
                    FHIRSlicing(
                        id=element.id,
                        path=element.path,
                        discriminators=element.slicing.discriminator,
                        description=element.slicing.description,
                        rules=element.slicing.rules,
                )
            )

        for element in profile_definition.snapshot.element: 
            if element.sliceName:
                slice_group = next((slice_group for slice_group in slicing if slice_group.path == element.path), None) 
                slice = FHIRSlice(
                    id=element.id,
                    name=element.sliceName,
                    type=element.type,
                )
                slice_group.add_slice(slice)        

        for element in profile_definition.snapshot.element:
            constraint = FHIRProfileConstraint(
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
            __slicing__: ClassVar[List[FHIRSlicing]] = slicing
            __constraints__: ClassVar[List[FHIRProfileConstraint]] = constraints
            __extensions__: ClassVar[List[FHIRExtension]] = extensions
            resourceType: Optional[str]
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

    def _check_if_path_ancestors_exist(self, resource, fhirpath):
        elements = FHIRPathNavigator(resource, allow_dynamic_paths=False)  
        for segment in split_fhirpath(fhirpath)[:-1]:
            child_elements = elements.get_value(segment)
            if child_elements:
                elements = FHIRPathNavigator(ensure_list(child_elements)[0], allow_dynamic_paths=False)
            else: 
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
                    print('type(constrained_element) =',type(constrained_element))
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
    
    
    def validate(self, resource):
        validation_errors = []

        # Core validation
        *_, validation_error = validate_model(resource.__class__, resource.dict())
        if validation_error:
            validation_errors += [ErrorWrapper(error.exc, error._loc) for raw_errors in validation_error.raw_errors  for error in raw_errors ]

        # Evaluate profile constraints
        for constraint in resource.__class__.__constraints__:
            if constraint.is_slice_constraint:
                continue
            # Get the element that is constrained in the resource
            constrained_element = FHIRPathNavigator(resource, allow_dynamic_paths=False).get_value(constraint.path)   
            if not constrained_element:
                # If the element does not exist, check if its ancestor exist
                if not self._check_if_path_ancestors_exist(resource, constraint.path):
                    # If not, means that the parent elements do not exist, so do not validate the constraint
                    continue   
            # Validate the constraint(s) for this element(s)
            validation_errors += self._validate_constraint(constrained_element, constraint) 
            
        # Slicing validation    
        for slice_group in resource.__class__.__slicing__:
            for slice in slice_group.slices:
                sliced_entries = FHIRPathNavigator(resource, allow_dynamic_paths=False).get_value(slice.fhirpath)
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
                    slice_subpath = constraint.path.replace(slice_group.path,"")    
                    # Constrains on elements of the slice should only be applied if the slice is present
                    if constraint.path != slice_group.path and len(sliced_entries)==0:
                        continue       
                    if constraint.path == slice_group.path:        
                        # Validate the constraint(s) for this slice element(s)
                        validation_errors += self._validate_constraint(sliced_entries, constraint, f'{slice_group.path}:{slice.name}{slice_subpath}') 
                    else:
                        for entry in sliced_entries:
                            constrained_slice_elements = FHIRPathNavigator(entry, allow_dynamic_paths=False).get_value(slice_subpath)
                            # Get the element that is constrained in the resource
                            if not constrained_slice_elements:
                                # If the element does not exist, check if its ancestor exist
                                if not self._check_if_path_ancestors_exist(entry, slice_subpath):
                                    # If not, means that the parent elements do not exist, so do not validate the constraint
                                    continue     
                            validation_errors += self._validate_constraint(constrained_slice_elements, constraint, f'{slice_group.path}:{slice.name}{slice_subpath}') 
        # IF there are any validation issues, raise them                     
        if validation_errors:
            raise ValidationError(validation_errors, resource.__class__)                     
        else:
            print('Resource successfully validated')


factory = ProfiledResourceFactory()
construct_profiled_resource_model = factory.construct_profiled_resource_model
validate_profiled_resource = factory.validate
clear_chache = factory.clear_chache