import re 
import traceback
from typing import List, Union
from dataclasses import make_dataclass
from pydantic.v1 import BaseModel
from pydantic import ValidationError
from fhir.resources.core.fhirabstractmodel import FHIRAbstractModel
from fhir.resources.core.utils.common import is_list_type, get_fhir_type_name, is_primitive_type
from fhir.resources.R4B.fhirtypesvalidators import get_fhir_model_class
from fhircraft.utils import ensure_list

FHIRPATH_SEPARATORS = re.compile(r'\.(?=(?:[^\)]*\([^\(]*\))*[^\(\)]*$)')
WORD_PATTERN = re.compile(r"^\D+$")
THIS_PATTERN = re.compile(r"^\$this$")
SUBSETTING_PATTERN = re.compile(r"^(.*?)\[(\d+)\]$")
EXTENSION_PATTERN = re.compile(r"extension\([\"|\'](.*?)[\"|\']\)")
WHERE_PATTERN = re.compile(r"where\((.+?)=[\"|\'](.*?)[\"|\']\)")
ITEM_PATTERN = re.compile(r"item\((\d+?)\)")
TYPE_CHOICES_PATTERN = re.compile(r"(.*?)\[x\]")
FIRST_PATTERN = re.compile(r"^first\(\)$")
LAST_PATTERN = re.compile(r"^last\(\)$")
TAIL_PATTERN = re.compile(r"^tail\(\)$")
SINGLE_PATTERN = re.compile(r"^single\(\)$")

class FHIRPathError(Exception):
    """Exception for FHIRPath-related issues"""
    pass



def validate_fhirpath(fhir_path: str) -> List[str]:
    """
    Validate a FHIR path string

    Parameters:
    - fhir_path (str): The FHIR path string to split.
    """    
    segments = split_fhirpath(fhir_path)
    for segment in segments:
        for pattern in [WORD_PATTERN, SINGLE_PATTERN, THIS_PATTERN, FIRST_PATTERN, LAST_PATTERN, TAIL_PATTERN, SUBSETTING_PATTERN, EXTENSION_PATTERN, WHERE_PATTERN, ITEM_PATTERN, TYPE_CHOICES_PATTERN]:
            if pattern.match(segment):
                break
        else:
            raise FHIRPathError(f'Invalid FHIRPath segment: {segment}')
        
def split_fhirpath(fhir_path: str) -> List[str]:
    """
    Split a FHIR path string at non-quoted dots.

    Parameters:
    - fhir_path (str): The FHIR path string to split.

    Returns:
    - List[str]: A list of strings resulting from splitting the FHIR path at non-quoted dots.
    """    
    # Split FHIR path only at non-quoted dots
    return FHIRPATH_SEPARATORS.split(fhir_path)


def join_fhirpath(*segments: str) -> str:
    """
    Join multiple FHIR path segments into a single FHIR path string.

    Parameters:
    - segments (str): Variable number of FHIR path segments to join.

    Returns:
    - str: A single FHIR path string created by joining the input segments with dots.
    """    
    return '.'.join((
        str(segment).strip('.') 
            for segment in segments if segment!=''
    )) 

class FHIRPathNavigator:

    def __init__(self, fhir_resource: Union[FHIRAbstractModel, dict], allow_dynamic_paths: bool=True):
        """
        Initialize the FHIRPathNavigator class.

        Parameters:
        - fhir_resource: Union[FHIRAbstractModel, dict] - The FHIR resource to navigate.
        - allow_dynamic_paths: bool - Flag indicating whether dynamic paths are allowed.

        Raises:
        - TypeError: If the fhir_resource is not a Pydantic FHIR model or a dict.
        """        
        self.allow_dynamic_paths = allow_dynamic_paths
        self.traversed_path = None        
        if isinstance(fhir_resource, FHIRAbstractModel):
            self.fhir_resource = fhir_resource
            self.path_origin = fhir_resource.get_resource_type()
        elif isinstance(fhir_resource, dict):
            self.path_origin = fhir_resource.get('resource_type')
            self.fhir_resource = make_dataclass("FHIRResource", ((k, type(v)) for k, v in fhir_resource.items()))(**fhir_resource)
        else: 
            raise TypeError('Invalid resource type, must be a Pydantic FHIR model or a dict')
        # Compile list of FHIRPath segment pattern handlers
        self.FHIRPATH_PATTERNS = {
            WHERE_PATTERN: self._where,
            EXTENSION_PATTERN: self._extension,
            ITEM_PATTERN: self._item,
            TYPE_CHOICES_PATTERN: self._all_type_choices,
            FIRST_PATTERN: lambda coll, _: self._first(coll),
            LAST_PATTERN: lambda coll, _: self._last(coll),
            TAIL_PATTERN: lambda coll, _: self._tail(coll),
            SINGLE_PATTERN: lambda coll, _: self._single(coll),
        }
    
    def _extend_array_with_empty_element(self, array_fhir_path: str):
        """
        Extends an array at the specified FHIR path by adding an empty element if needed.
        """        
        # Parse and cleanup the FHIR path string
        array_fhir_path,_ = self._check_segment_subsetting(array_fhir_path)   
        # Get the current elements in the array
        array_elements = ensure_list(self._traverse_fhirpath(array_fhir_path))
        if not array_elements:
            return None
        if isinstance(array_elements[0],BaseModel):
            # Construct empty FHIR resource
            new_element = array_elements[0].__class__.construct()
            # Add it to the array
            array_elements.append(new_element)
        else:
            array_elements.append(None)
        # Set the extended array to the FHIR path element
        self._traverse_fhirpath(array_fhir_path, array_elements)
        return array_elements
    
    def _create_empty_segment_resource(self, element, segment=None):
        """
        Creates and returns an empty resource for the specified segment of the given element.
        """
        if segment is not None:
            model_field = element.__class__.__fields__.get(segment)
            if not model_field:
                return None
            if is_list_type(model_field):
                if not isinstance(getattr(element, segment), list):
                    setattr(element, segment, [])
            field_type = get_fhir_type_name(model_field.type_)
            try:
                model = get_fhir_model_class(field_type)
            except KeyError:
                return None
            model.validate_assignment = False
            empty_resource =  model.construct()
            if is_list_type(model_field):
                getattr(element, segment).append(empty_resource)
            else:
                setattr(element, segment, empty_resource)   
            return empty_resource                   
        else:
            model_field = None 
            model = element.__class__ 
            model.validate_assignment = False
            empty_resource =  model.construct() 
        return empty_resource    
    
    def _set_value_at_path(self, collection, segment, value):
        """
        Set the value at the specified FHIR path to the new provided value.
        """
        for element in collection:
            segment, subset_index = self._check_segment_subsetting(segment)     

            if getattr(element, segment, None) is None:
                self._create_empty_segment_resource(element, segment)
                if not hasattr(element, segment):
                    raise FHIRPathError(f"Cannot set value ({value}) to FHIR path ({self.fhirpath})")
            array = getattr(element, segment, None)
            if subset_index is not None and isinstance(array, list):
                while len(array)<=subset_index:
                    if len(array)>0 and isinstance(array[0], BaseModel):
                        array = self._extend_array_with_empty_element(join_fhirpath(self.traversed_path, segment))
                    else:
                        array.append(None)
                array[subset_index] = value
                setattr(element, segment, array)
            else:
                setattr(element, segment, value)
                
    
    def _check_segment_subsetting(self, segment: str):
        """
        Checks if the segment contains a subset index and extracts it if present.
        """        
        subset_index = None
        if SUBSETTING_PATTERN.match(segment):
            segment, subset_index = SUBSETTING_PATTERN.search(segment).group(1,2)      
            subset_index = int(subset_index)
        return segment, subset_index
    
    
    def _extension(self, collection: List, segment: str):
        """
        Returns a collection of extensions from the given collection that match the specified extension URL.
        """        
        extension_url = EXTENSION_PATTERN.search(segment).group(1)
        return [
            extension for element in collection 
                    for extension in ensure_list(element.extension) 
                        if extension is not None and extension.url == extension_url
        ]

    def _where(self, collection, segment):
        """
        Returns a collection of elements from the given collection that match the specified condition.
        """        
        condition_path, condition_value = WHERE_PATTERN.search(segment).group(1,2)
        return [
            obj for element in collection 
                    for obj in ensure_list(element) 
                         if FHIRPathNavigator(obj).get_value(condition_path) == condition_value
        ]    
    
    def _get_index(self, collection, index):
        """
        Returns the element at the specified index in the given collection.
        """        
        while len(collection)<=index:
            if self.allow_dynamic_paths:
                collection = self._extend_array_with_empty_element(self.traversed_path)
            else:
                collection.append(None)
        return [collection[index]] 
    
    def _item(self, collection, segment):
        """
        Parses the segment and returns the element at the specified index in the given collection.
        """        
        index = int(ITEM_PATTERN.search(segment).group(1))
        return self._get_index(collection, index)
        
    def _first(self, collection):
        """
        Returns the first element in the given collection.
        """
        return self._get_index(collection, index=0)
        
    def _last(self, collection):
        """
        Returns the last element in the given collection.
        """
        return self._get_index(collection, index=-1)
        
    def _tail(self, collection):
        """
        Returns the all elements except the last in the given collection.
        """        
        return collection[:-1]
    
    def _single(self, collection):
        """
        Returns a single item from the given collection.

        Raises:
        - FHIRPathError: If the collection does not contain exactly one item.
        """        
        if len(collection)!=1:
            raise FHIRPathError(f'Expected collection of path "{self.fhirpath}" to have one single item (instead {len(collection)} items collected)')
        return [collection[0]]
    
    def _all_type_choices(self, collection, statement):
        """
        Returns a list of values for a specific type choice element from the given collection.
        """
        type_choice_name = TYPE_CHOICES_PATTERN.search(statement).group(1)
        return [
            getattr(obj, element) 
                for obj in collection
                    for element in obj.__dict__.keys() 
                        if element.startswith(type_choice_name) and getattr(obj, element) 
        ]
        
    def _traverse_fhirpath(self, fhirpath, set_value=None):
        """
        Traverse the given FHIR path and return the corresponding elements or set a new value if specified.

        Parameters:
        - fhirpath (str): The FHIR path to traverse.
        - set_value (Any): The new value to set at the end of the path, default is None.

        Returns:
        - Union[Any, List[Any]]: The element(s) at the specified FHIR path.

        Raises:
        - ValueError: If no FHIR path is specified (fhir_path=None).
        - FHIRPathError: If the FHIR path does not exist.

        """        
        if fhirpath is None:
            raise ValueError('No FHIRPath has been specified (fhir_path=None)')
        self.traversed_path = ''
        self.fhirpath = fhirpath
        # Split union collection into individual path collections
        union_collection = []
        for fhir_path in fhirpath.split('|'):
            # Split the path into its segments
            fhirpath_segments = split_fhirpath(fhir_path.strip())
            # If path's entry point is the core resource, remove it
            if self.path_origin == fhirpath_segments[0]:
                self.traversed_path = fhirpath_segments[0]
                fhirpath_segments = fhirpath_segments[1:]
            # If a value must be set at the end of the path, remove the last segment
            if set_value is not None:
                last_fhirpath_segment = fhirpath_segments[-1]
                fhirpath_segments = fhirpath_segments[:-1]
            # Initialize the collection with the full resource
            collection = [self.fhir_resource]
            # Iterate over the FHIRPath segments
            for fhirpath_segment in fhirpath_segments:
                self.traversed_path = join_fhirpath(self.traversed_path, fhirpath_segment)

                fhirpath_segment, subset_index = self._check_segment_subsetting(fhirpath_segment)             
                    
                try:
                    for pattern, operation in self.FHIRPATH_PATTERNS.items():
                        # Look for patterns in the segment
                        if pattern.match(fhirpath_segment):
                            collection = operation(collection, fhirpath_segment)
                            break
                    else:
                        # Otherwise, assume simple element path segments
                        collection = [
                            value if getattr(element, fhirpath_segment, None)
                            else self._create_empty_segment_resource(element, fhirpath_segment) if self.allow_dynamic_paths else None
                                for element in collection                          
                                    for value in ensure_list(getattr(element, fhirpath_segment, None)) 
                        ]   
                    # Remove any Nones from the collection
                    collection = [element for element in collection if element is not None] 
                    
                    if subset_index is not None:
                        collection = self._get_index(collection, subset_index)
                        
                except RuntimeError: 
                    raise FHIRPathError(f"\nFHIRPath {self.traversed_path} does not exist.\n\nTraceback:\n{traceback.format_exc()}")
            # If a value must be set...
            if set_value is not None: 
                self._set_value_at_path(collection, last_fhirpath_segment, set_value)
            # Add the finished collection for this FHIRpath to the union's collection
            union_collection.extend(collection)
        # Return single values if there is a single one in the collection
        if len(union_collection) <= 1:
                union_collection = union_collection[0] if len(union_collection) == 1 else None          
        return union_collection
    
    def get_value(self, fhir_path):
        """
        Get the value at the specified FHIR path.

        Parameters:
        - fhir_path (str): The FHIR path to traverse and retrieve the value.

        Returns:
        - Union[Any, List[Any]]: The element(s) at the specified FHIR path.

        Raises:
        - ValueError: If no FHIR path is specified (fhir_path=None).
        - FHIRPathError: If the FHIR path does not exist.
        """        
        return self._traverse_fhirpath(fhir_path)
            
    def set_value(self, fhir_path, new_value):
        """
        Set the value at the specified FHIR path to the new provided value.

        Parameters:
        - fhir_path (str): The FHIR path where the new value should be set.
        - new_value (Any): The new value to set at the specified FHIR path.

        Returns:
        - None

        Raises:
        - ValueError: If no FHIR path is specified (fhir_path=None).
        - FHIRPathError: If the FHIR path does not exist.
        """        
        self._traverse_fhirpath(fhir_path, new_value)
        
    def get_pydantic_field(self, fhir_path):
        """
        Get the Pydantic field at the specified FHIR path.

        Parameters:
        - fhir_path (str): The FHIR path to traverse and retrieve the Pydantic field.

        Returns:
        - Optional[Field]: The Pydantic field at the specified FHIR path, or None if not found.

        Raises:
        - ValueError: If no FHIR path is specified (fhir_path=None).
        - FHIRPathError: If the FHIR path does not exist.
        """        
        fhirpath_segments = split_fhirpath(fhir_path)
        last_fhirpath_segment = fhirpath_segments[-1]
        fhirpath_segments = fhirpath_segments[:-1]
        if len(fhirpath_segments)>0:
            element = self._traverse_fhirpath(join_fhirpath(*fhirpath_segments))[0]
        else:
            element = self.fhir_resource
        return element.__class__.__fields__.get(last_fhirpath_segment)
    
