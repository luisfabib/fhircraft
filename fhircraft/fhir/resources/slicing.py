from fhircraft.fhir.path import fhirpath, FHIRPathError, FhirPathParserError, FhirPathLexerError
from fhircraft.fhir.path.utils import split_fhirpath, join_fhirpath
from fhircraft.fhir.resources.constraint import Constraint
from fhircraft.fhir.resources.datatypes import get_FHIR_type
from fhircraft.utils import get_dict_paths, ensure_list, get_fhir_model_from_field
from pydantic import create_model
from typing import List, ClassVar, Optional
from dataclasses import dataclass, field
from enum import Enum
import re 

@dataclass
class Discriminator:
    """
    Discriminator 
    --------------
    Each discriminator is a pair of values: a type that indicates how the field 
    is processed when evaluating the discriminator, and a FHIRPath expression that 
    identifies the element in which the discriminator is found.
    """
    class DiscriminatorType(Enum):
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
        self.type = self.DiscriminatorType(self.type)
        # Check if self.type is a valid DiscriminatorType
        if not self.type in self.DiscriminatorType:
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
                
@dataclass
class Slice:
    """
    A slice is a specific subset or a partition of the elements that results from the slicing process.
    Each slice is defined with its own constraints or characteristics based on the slicing criteria. 
    Essentially, a slice is a unique subgroup within the repeating element that is differentiated by 
    the defined slicing criteria.   
    
    Attributes:
        id (str): Identifier of the slice as given in the `StructureDefinition`.
        name (str): Name of the slice as given in the `StructureDefinition`.
        type (str): Type of slice.
        constraints (List[Constraint]): Collection of constraints on this slice.
        slicing (Optional[SlicingGroup]): Slicing group to which this slice belongs.
        
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
            path (str): The full FHIR path constructed by combining the slicing path and the discriminating expression.
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
            min_cardinality (int): The minimum cardinality value.
        """        
        return min([constraint.min for constraint in self.get_constraints_on_slice()] or [0]) 
    
    @property
    def max_cardinality(self):
        """
        Calculate the maximum cardinality among the sliceconstraints.
        
        Returns:
            max_cardinality (int): The maximum cardinality value.
        """        
        return max([constraint.max for constraint in self.get_constraints_on_slice()] or [1])      
    
    @property
    def profile_constraint(self):
        return next((constraint.profile for constraint in self.constraints if constraint.profile and constraint.path == self.slicing.path),None)       
    
    
    def get_constraints_on_slice(self):
        """
        Get the constraints specific to the slice as element based on the path
        
        Returns:
            (List[Constraint]): A list of constraints that apply to this slice, filtered by the slicing path.
        """        
        return [constraint for constraint in self.constraints if constraint.path == self.slicing.path]       
    
    
    def add_constraint(self, constraint):        
        """
        Convinience function to add a constraint to to the slice.
        
        Args:
        constraint (Constraint): The constraint to be added to the slice
        
        Raises:
            TypeError: If constraint is not an instance of `Constraint`.
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
            expression (str): The discriminating FHIRPath expression for the slice.
        
        Notes:
            The expression is constructed differently based on the type of discriminator:
            
            - `VALUE/PATTERN`: Differentiates slices by fixed values, patterns, or required `ValueSet` bindings.
            - `EXISTS`: Differentiates slices by the presence or absence of the nominated element.
            - `TYPE`: Differentiates slices by the type of the nominated element.
            - `PROFILE`: Differentiates slices by conformance to a specified profile.
            - `POSITION`: Differentiates slices by their index within the slicing group.
        
        Info:
            Special handling is applied for `Extension` types with profile constraints, 
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
            if discriminator.type is discriminator.DiscriminatorType.VALUE or discriminator.type is discriminator.DiscriminatorType.PATTERN:
                """
                Discriminator - Value/Pattern
                The slices have different values in the nominated element, as determined by the applicable 
                fixed value, pattern, or required ValueSet binding.
                """
                # Handle special case of extensions
                profile_constraint = next((constraint.profile for constraint in self.get_constraints_on_slice() if constraint.profile), None)
                if self.type=='Extension' and profile_constraint:
                    expression = join_fhirpath(expression, f"extension('{profile_constraint.canonical_url}')")
                    continue
                # Get the constrained pattern applied to the discriminator element 
                pattern = next((constraint.pattern for constraint in discriminator_constraints if constraint.pattern),None)
                discriminating_values = get_dict_paths(pattern.model_dump(), prefix=discriminator.path) if pattern else {}
                # Get the constrained fixed values applied to the discriminator element 
                fixedValues = {discriminator.path: constraint.fixedValue for constraint in discriminator_constraints if constraint.fixedValue}
                discriminating_values.update(fixedValues)
                # Get the paths to the individual values set by the pattern
                for path, value in discriminating_values.items():
                    # Discriminating expression for current pattern value
                    expression = join_fhirpath(expression, f"where({path}='{value}')")

            elif discriminator.type is discriminator.DiscriminatorType.EXISTS:
                """
                Discriminator - Existence
                The slices are differentiated by the presence or absence of the nominated element.
                """
                expression = join_fhirpath(expression, f"where({discriminator.path}.exists())")
                    
            elif discriminator.type is discriminator.DiscriminatorType.TYPE:
                """
                Discriminator - Type
                The slices are differentiated by type of the nominated element.
                """
                expression = join_fhirpath(expression, f"where({discriminator.path} is {self.type})")
                    
            elif discriminator.type is discriminator.DiscriminatorType.PROFILE:
                """
                Discriminator - Profile
                The slices are differentiated by conformance of the nominated element to a specified profile.
                Note that if the path specifies .resolve() then the profile is the target profile on the reference. 
                """
                # raise NotImplementedError() 
                
            elif discriminator.type is discriminator.DiscriminatorType.POSITION:
                """
                Discriminator - Existence
                The slices are differentiated by their index. This is only possible if all but the last 
                slice have min=max cardinality, and the (optional) last slice contains other undifferentiated elements.
                """
                # Find position of current slice in slicing group
                index = next((index for index,slice in enumerate(self.slicing.slices) if slice == self))
                expression = join_fhirpath(expression, f"index({index})")
                    
        return expression

    def get_pydantic_model(self, resource):       
        
        base_path, element = self.slicing.path.rsplit('.',1)
        base = fhirpath.parse(base_path).get_value(resource)
        if element.lower() == 'extension':
            model = get_FHIR_type('Extension')
        else:
            model = get_fhir_model_from_field(base.model_fields.get(element))
        
        class ProfiledSlice(model):
            __track_changes__: bool = False 
            __has_been_modified__: bool = False
            profile_slicing: ClassVar[List[SlicingGroup]] = self.profile_constraint.profile_slicing if self.profile_constraint else None

            def __setattr__(self, name:str, value):
                super().__setattr__(name, value)
                if name not in ['__track_changes__','__has_been_modified__'] and self.__track_changes__:
                    super().__setattr__('__has_been_modified__', True)
            
            @property
            def is_FHIR_complete(self):
                BASE_ELEMENTS = ['text','extension', 'id', 'resourceType']
                slice_available_elements = sorted(set([name for name in self.__class__.model_fields if '_ext' not in name and not name.startswith('_') and name not in BASE_ELEMENTS]))
                slice_preset_elements = sorted(set([name for name, value in self.model_dump(by_alias=True, exclude_unset=True).items() if (value is not None or value!=[]) and '_ext' not in name and not name.startswith('_')  and name not in BASE_ELEMENTS]))
                print(slice_available_elements)
                print(slice_preset_elements)
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
            
        slice_model = create_model(__model_name=f'Sliced{model.__name__}', __base__=ProfiledSlice) 
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
    class SlicingRules(Enum):
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
        self.rules = self.SlicingRules(self.rules)
        # Check if self.type is a valid DiscriminatorType
        if not self.rules in self.SlicingRules:
            raise ValueError(f"Invalid slicing rules: '{self.rules}'")
        # Parse FHIRPath to ensure it is valid
        if not fhirpath.is_valid(self.path):
            raise FHIRPathError(f'Slicing FHIRPath is not valid: {self.path}')
        
    def get_slice_by_name(self, slice_name):
        return next((slice for slice in self.slices if slice.name == slice_name), None)
    
    def add_slice(self, slice: Slice):
        slice.slicing = self
        self.slices.append(slice)
    