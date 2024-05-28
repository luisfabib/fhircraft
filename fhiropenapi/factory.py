
from fhir.resources.R4B.elementdefinition import ElementDefinition
from fhir.resources.R4B.structuredefinition import StructureDefinition

from fhir.resources.R4B.fhirtypesvalidators import get_fhir_model_class
from pydantic.v1 import ValidationError, create_model, validate_model
from pydantic.v1.error_wrappers import ErrorWrapper
from typing import List, Any, Tuple, Dict, Type, ClassVar, Union, Optional
from dataclasses import dataclass, field
from fhiropenapi.fhirpath import FHIRPathNavigator
import datetime 
import json
import requests

__all__ = ["construct_profiled_resource_model", "validate_profiled_resource"]

PATTERN_FIELDS = [field for field in ElementDefinition.__fields__.keys() if field.startswith('pattern')]
FIXED_FIELDS = [field for field in ElementDefinition.__fields__.keys() if field.startswith('fixed')]

class FHIRError(Exception):
    """Exception for FHIR-related issues"""
    pass

def get_paths(nested_dict: Union[Dict[str, Any], List[Dict[str, Any]]], prefix: str = '') -> Dict[str, Any]:
    paths = {}
    if isinstance(nested_dict, dict):
        for key, value in nested_dict.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                paths.update(get_paths(value, new_prefix))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    list_prefix = f"{new_prefix}.{i}"
                    if isinstance(item, dict):
                        paths.update(get_paths(item, list_prefix))
            else:
                if value is not None:
                    paths[new_prefix] = value
    elif isinstance(nested_dict, list):
        for i, item in enumerate(nested_dict):
            list_prefix = f"{prefix}[{i}]"
            if isinstance(item, dict):
                paths.update(get_paths(item, list_prefix))
    return paths

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
    
    def add_constraint(self, constraint):
        self.constraints.append(constraint)
    
    @property
    def pydantic_model(self):       
        base_model, element = self.path.split('.')
        return get_fhir_model_class(get_fhir_model_class(base_model).__fields__.get(element).type_.__resource_type__)
    
    @property
    def discriminator_values(self):
        for discriminator_path in self.slicing_group.discriminator_paths:
            for constraint in self.constraints:
                if constraint.pattern and discriminator_path == constraint.path:
                    return get_paths(constraint.pattern.dict(), prefix=discriminator_path.replace(self.slicing_group.path,''))
        return {}
    @property
    def fhirpath(self):
        fhir_path = self.slicing_group.path
        for path, value in self.discriminator_values.items():
            if path.startswith('.'): path = path[1:]
            fhir_path += f'.where({path}="{value}")'       
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
        return [f'{self.path}.{discriminator.path}' if discriminator.path!='$this' else self.path for discriminator in self.discriminators]
        
    def add_slice(self, slice: FHIRSlice):
        slice.slicing_group = self
        self.slices.append(slice)
    
    def has_discriminator_type(self, discriminator_type: str) -> bool:
        return any(discriminator.type == discriminator_type for discriminator in self.discriminators)

        
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
            domain, resource = profile_url.rsplit('/', 1)
            json_url = f"{domain}-{resource}.json"
        else:
            json_url = profile_url
        # Download the StructureDefinition JSON            
        response = requests.get(json_url)
        response.raise_for_status()
        structure_definition = response.json()
        # Disable certain incompatible validators             
        if 'extension' in structure_definition:
            structure_definition.pop('extension')
        ElementDefinition.__fields__['id'].validators = []
        # Parse JSON into a StructureDefinition model
        return StructureDefinition.parse_obj(structure_definition)
    
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
            if element.slicing and not 'extension' in element.id:
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
            if element.sliceName and not any([type.code == 'Extension' for type in element.type]):
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
            if element.type:
                constraint.valueType = [type.code for type in element.type]
            for pattern_field in PATTERN_FIELDS:
                pattern_value = getattr(element, pattern_field)
                if pattern_value: 
                    constraint.pattern = pattern_value

            for fixed_field in FIXED_FIELDS:
                fixed_value = getattr(element, fixed_field)
                if pattern_value: 
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
            __slicing__: ClassVar[List[FHIRSlicing]] = slicing
            __constraints__: ClassVar[List[FHIRProfileConstraint]] = constraints
            __extensions__: ClassVar[List[FHIRExtension]] = extensions
            resourceType: Optional[str]
            
            class Config:
                underscore_attrs_are_private = True
                validate_assignment = False

        profile_model = create_model(__model_name=profile_definition.name, __base__=ProfiledModel) 
        
        # Cache the profile
        factory.profiles.update({
            profile_url: profile_model
        })
        return profile_model


    def _validate_constraint(self, constrained_elements, constraint, path=None):
        validation_errors = []
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
                    'date': datetime.datetime,
                    'boolean': bool,
                    'integer': int,
                    'code': str,
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
    
    
    def validate(self, resource):
        validation_errors = []

        # Core validation
        *_, validation_error = validate_model(resource.__class__, resource.dict())
        if validation_error:
            validation_errors += [ErrorWrapper(error.exc, error._loc) for error in validation_error.raw_errors]

        # Evaluate profile constraints
        for constraint in resource.__class__.__constraints__:
            if constraint.is_slice_constraint:
                continue
            # Get the element that is constrained in the resource
            constrained_element = FHIRPathNavigator(resource).get_value(constraint.path)              
            # Validate the constraint(s) for this element(s)
            validation_errors += self._validate_constraint(constrained_element, constraint) 
            
        # Slicing validation    
        for slice_group in resource.__class__.__slicing__:
            for slice in slice_group.slices:
                sliced_entries = FHIRPathNavigator(resource).get_value(slice.fhirpath)
                if not isinstance(sliced_entries, list): 
                    sliced_entries = [sliced_entries]
                sliced_entries = [entry for entry in sliced_entries if entry is not None]
                for entry in sliced_entries:
                    # Perform basic validation
                    *_, subvalidation_errors = validate_model(entry.__class__, entry.dict())
                    if subvalidation_errors:
                        validation_errors += [ErrorWrapper(error.exc, f'{slice_group.path}:{slice.name}.{error._loc}')  for error in subvalidation_errors.raw_errors]
                    # Apply core resource validation
                    for validator in entry.__class__.__pre_root_validators__ + entry.__class__.__post_root_validators__:
                        try: 
                            validator(entry.__class__, entry.dict())
                        except validation_error:
                            validation_errors.append(ErrorWrapper(
                                validation_error), 
                                f'{slice_group.path}:{slice.name}'
                            )
                # Check for all constraints on the current slice
                for constraint in slice.constraints:
                    slice_subpath = constraint.path.replace(slice_group.path,"")             
                    constrained_slice_elements = FHIRPathNavigator(resource).get_value(slice.fhirpath + slice_subpath)
                    # Constrains on elements of the slice should only be applied if the slice is present
                    if constraint.path != slice_group.path and len(sliced_entries)==0:
                        continue
                    # Validate the constraint(s) for this slice element(s)
                    validation_errors += self._validate_constraint(constrained_slice_elements, constraint, f'{slice_group.path}:{slice.name}{slice_subpath}') 
                
        # IF there are any validation issues, raise them                     
        if validation_errors:
            raise ValidationError(validation_errors, resource.__class__)                     
        else:
            print('Resource successfully validated')


factory = ProfiledResourceFactory()
construct_profiled_resource_model = factory.construct_profiled_resource_model
validate_profiled_resource = factory.validate