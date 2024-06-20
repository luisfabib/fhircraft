
from fhir.resources.R4B.elementdefinition import ElementDefinition
from fhir.resources.R4B.structuredefinition import StructureDefinition
from fhir.resources.R4B.fhirtypesvalidators import get_fhir_model_class
from fhir.resources.R4B.fhirtypes import MetaType
from fhir.resources.R4B.meta import Meta

from fhircraft.utils import get_dict_paths, load_env_variables, ensure_list, remove_none_dicts

from pydantic.v1 import ValidationError, create_model, validate_model, Extra
from pydantic.v1.error_wrappers import ErrorWrapper
from typing import List, Any, Tuple, Dict, Type, ClassVar, Union, Optional, get_origin, Literal
from fhircraft.fhir.path.utils import split_fhirpath, join_fhirpath
from fhircraft.fhir.path import fhirpath, FHIRPathError, FhirPathParserError, FhirPathLexerError
from dataclasses import dataclass, field
from enum import StrEnum
import re
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

@dataclass
class FHIRConstraint:
    key: Optional[str] = None
    severity: Optional[str] = None
    human: Optional[str] = None
    expression: Optional[str] = None
    xpath: Optional[str] = None

@dataclass
class Constraint:
    id: str
    path: str
    min: int
    max: int
    profile: Optional[object] = None
    valueType: Optional[List[str]] = field(default_factory=list)
    fixedValue: Optional[Union[str, float, int, Dict[str, Union[str, float, int]]]] = None
    pattern: Optional[Union[str, float, int, Dict[str, Union[str, float, int]]]] = None
    binding: Optional[str] = None
    constraints: Optional[List[FHIRConstraint]] = field(default_factory=list)

    @property
    def is_slice_constraint(self):
        return ':' in self.id

    def get_constrained_slice_name(self):
        slice_name = self.id.split(':')[1].split('.')[0]
        return slice_name



@dataclass
class Discriminator:
    """
    Discriminator 
    --------------
    Each discriminator is a pair of values: a type that indicates how the field 
    is processed when evaluating the discriminator, and a FHIRPath expression that 
    identifies the element in which the discriminator is found.
    """
    class DiscriminatorType(StrEnum):
        """
        There are five different processing types for discriminators: 
        """
        VALUE = "value"      
        PATTERN = "pattern"   
        EXISTS = "exists"     
        TYPE = "type"         
        PROFILE = "profile"   
        POSITION = "position" 
        
    type: DiscriminatorType 
    path: str
    _RESTRICTED_FHIRPATH_FUNCTIONS = ('extension', 'resolve', 'ofType')
  
    def __post_init__(self):
        # Check if self.type is a valid DiscriminatorType
        if not self.type in self.DiscriminatorType._value2member_map_:
            raise ValueError(f"Invalid discriminator type: '{self.type}'")
        # Parse FHIRPath to ensure it is valid
        if not fhirpath.is_valid(self.path):
            raise FHIRPathError(f'Slice discriminator FHIRPath is not valid: {self.path}')
        # Check that only the restricted FHIRPath function are used
        matches = re.finditer(r"\.?([a-zA-Z]*)\(.*\)", self.path)
        for match in matches:
            function = match.group(1)
            if function not in self._RESTRICTED_FHIRPATH_FUNCTIONS:
                raise FHIRPathError(f'Slice discriminator FHIRPath is not valid: Invalid function "{function}" used in restricted discriminator FHIRPath')
    
    def construct_fhirpath_expression(self, value=None):
        match self.type:
            case self.DiscriminatorType.VALUE | self.DiscriminatorType.PATTERN:
                return f"where({self.path}='{value}')"
            case self.DiscriminatorType.EXISTS:
                return f"where({self.path}.exists())"     
            case self.DiscriminatorType.TYPE:
                return f"where({self.path} is {value})"   
            case self.DiscriminatorType.PROFILE:
                return f"where({self.path}.conformsTo('{value}')"     
            case self.DiscriminatorType.POSITION:
                return f"index({value})"               
                
@dataclass
class Slice:
    """
    Slice
    -----
    A slice is a specific subset or a partition of the elements that results from the slicing process.
    Each slice is defined with its own constraints or characteristics based on the slicing criteria. 
    Essentially, a slice is a unique subgroup within the repeating element that is differentiated by 
    the defined slicing criteria.   
    """
    id : str
    name : str
    type: str 
    constraints: List[Constraint] = field(default_factory=list)
    slicing: Optional["SlicingGroup"] = None
      
    @property
    def full_fhir_path(self):
        """
        Construct the full FHIRPath for the slice based on the slicing path and the discriminating expression.
        
        Returns:
        --------
        str
            The full FHIR path constructed by combining the slicing path and the discriminating expression.
        """        
        if self.slicing.path.endswith('extension') and self.discriminating_expression.startswith('extension'):
            return join_fhirpath(self.slicing.path.replace('extension',''), self.discriminating_expression)
        else:
            return join_fhirpath(self.slicing.path, self.discriminating_expression)
              
    @property
    def min_cardinality(self):
        """
        Calculate the minimum cardinality among the slice constraints.
        
        Returns:
        --------
        int
            The minimum cardinality value.
        """        
        return min([constraint.min for constraint in self.get_constraints_on_slice()])       
    
    @property
    def max_cardinality(self):
        """
        Calculate the maximum cardinality among the sliceconstraints.
        
        Returns:
        --------
        int
            The maximum cardinality value.
        """        
        return max([constraint.max for constraint in self.get_constraints_on_slice()])       
    
    @property
    def profile_constraint(self):
        return next((constraint.profile for constraint in self.constraints if constraint.profile and constraint.path == self.slicing.path),None)       
    
    
    def get_constraints_on_slice(self):
        """
        Get the constraints specific to the slice as element based on the path
        
        Returns:
        --------
        List[Constraint]
            A list of constraints that apply to this slice, filtered by the slicing path.
        """        
        return [constraint for constraint in self.constraints if constraint.path == self.slicing.path]       
    
    
    def add_constraint(self, constraint):        
        """
        Convinience function to add a constraint to to the slice.
        
        Arguments:
        ----------
        constraint: Constraint
            The constraint to be added to the slice
        """   
        if not isinstance(constraint, Constraint):
            raise TypeError('The constraint must be a valid <Constraint> instance')
        self.constraints.append(constraint)
    
    @property
    def discriminating_expression(self):
        """
        Construct the discriminating expression for the slice based on its discriminators.

        This method iterates over all discriminators in the slicing group and constructs an expression
        to identify the slice based on the discriminator type and the constraints applied to the slice.

        Returns:
        --------
        str
            The discriminating FHIRPath expression for the slice.
        
        Notes:
        ------
        The expression is constructed differently based on the type of discriminator:
        - VALUE/PATTERN: Differentiates slices by fixed values, patterns, or required ValueSet bindings.
        - EXISTS: Differentiates slices by the presence or absence of the nominated element.
        - TYPE: Differentiates slices by the type of the nominated element.
        - PROFILE: Differentiates slices by conformance to a specified profile.
        - POSITION: Differentiates slices by their index within the slicing group.
        
        Special handling is applied for 'Extension' types with profile constraints, 
        where the profile URL is included in the expression.
        """        
        expression = ''
        # Loop over all discriminators for the slice
        for discriminator in self.slicing.discriminators:
            # Get the constraints that apply specifically to the discriminator element
            discriminator_constraints = [
                constraint for constraint in self.constraints 
                if constraint.path == join_fhirpath(self.slicing.path, discriminator.path)
            ]
            # Construct the discrimination expression based on the type of discriminator
            match discriminator.type:
                case discriminator.DiscriminatorType.VALUE | discriminator.DiscriminatorType.PATTERN:
                    """
                    Discriminator - Value/Pattern
                    The slices have different values in the nominated element, as determined by the applicable 
                    fixed value, pattern, or required ValueSet binding.
                    """
                    # Handle special case of extensions
                    profile_constraint = next((constraint.profile for constraint in self.get_constraints_on_slice() if constraint.profile), None)
                    if self.type=='Extension' and profile_constraint:
                        expression = join_fhirpath(expression, f"extension('{profile_constraint.__canonical_url__}')")
                        continue
                    # Get the constrained pattern applied to the discriminator element 
                    pattern = next((constraint.pattern for constraint in discriminator_constraints if constraint.pattern),None)
                    discriminating_values = get_dict_paths(pattern.dict(), prefix=discriminator.path) if pattern else {}
                    # Get the constrained fixed values applied to the discriminator element 
                    fixedValues = {discriminator.path: constraint.fixedValue for constraint in discriminator_constraints if constraint.fixedValue}
                    discriminating_values.update(fixedValues)
                    # Get the paths to the individual values set by the pattern
                    for path, value in discriminating_values.items():
                        # Discriminating expression for current pattern value
                        expression = join_fhirpath(expression, f"where({path}='{value}')")

                case discriminator.DiscriminatorType.EXISTS:
                    """
                    Discriminator - Existence
                    The slices are differentiated by the presence or absence of the nominated element.
                    """
                    expression = join_fhirpath(expression, f"where({discriminator.path}.exists())")
                    
                case discriminator.DiscriminatorType.TYPE:
                    """
                    Discriminator - Type
                    The slices are differentiated by type of the nominated element.
                    """
                    expression = join_fhirpath(expression, f"where({discriminator.path} is {self.type})")
                    
                case discriminator.DiscriminatorType.PROFILE:
                    """
                    Discriminator - Profile
                    The slices are differentiated by conformance of the nominated element to a specified profile.
                    Note that if the path specifies .resolve() then the profile is the target profile on the reference. 
                    """
                    # raise NotImplementedError() 
                
                case discriminator.DiscriminatorType.POSITION:
                    """
                    Discriminator - Existence
                    The slices are differentiated by their index. This is only possible if all but the last 
                    slice have min=max cardinality, and the (optional) last slice contains other undifferentiated elements.
                    """
                    # Find position of current slice in slicing group
                    index = next((index for index,slice in enumerate(self.slicing.slices) if slice == self))
                    expression = join_fhirpath(expression, f"index({index})")
                    
        return expression



    
    @property
    def pydantic_model(self):       
        
        base_model, element = self.slicing.path.rsplit('.',1)
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
            __slicing__: ClassVar[List[SlicingGroup]] = self.profile_constraint.__slicing__ if self.profile_constraint else None

            def __setattr__(self, name:str, value):
                super().__setattr__(name, value)
                if name not in ['__track_changes__','__has_been_modified__'] and self.__track_changes__:
                    super().__setattr__('__has_been_modified__', True)
            
            @property
            def is_FHIR_complete(self):
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
    
    
@dataclass
class SlicingGroup:
    """
    Slicing Group
    -------------
    A collection of slices along with the rules for the slicing process.
    
    Slicing is the process of defining a way to differentiate between repeated elements within 
    a FHIR resource or profile. It allows for the creation of subsets (slices) of these elements
    based on certain criteria, such as different codes, values, or properties. Slicing is useful
    when you need to apply different constraints or requirements to different occurrences of the
    same repeating element.
    """    
    class SlicingRules(StrEnum):
        CLOSED = "closed"     
        OPEN = "open"   
        OPENATEND = "openAtEnd"   
    id : str
    path: str 
    discriminators: List[Discriminator]
    rules: SlicingRules = SlicingRules.OPEN 
    ordered: Optional[bool] = False
    slices: List[Slice] = field(default_factory=list)  # List to hold the slices
    description: Optional[str] = None  
      
    def __post_init__(self):
        # Check if self.type is a valid DiscriminatorType
        if not self.rules in self.SlicingRules._value2member_map_:
            raise ValueError(f"Invalid slicing rules: '{self.rules}'")
        # Parse FHIRPath to ensure it is valid
        if not fhirpath.is_valid(self.path):
            raise FHIRPathError(f'Slicing FHIRPath is not valid: {self.path}')
        
    def get_slice_by_name(self, slice_name):
        return next((slice for slice in self.slices if slice.name == slice_name), None)
    
    def add_slice(self, slice: Slice):
        slice.slicing = self
        self.slices.append(slice)
    


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
        fhirpath.parse(slicing.path).update_or_create(resource, slices_resources)       
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