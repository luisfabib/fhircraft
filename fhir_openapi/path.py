import re 
import traceback
from typing import List, Union
from dataclasses import make_dataclass
from fhir.resources.core.fhirabstractmodel import FHIRAbstractModel
from fhir.resources.core.utils.common import is_list_type, get_fhir_type_name, is_primitive_type
from fhir.resources.R4B.fhirtypesvalidators import get_fhir_model_class
from fhir_openapi.utils import ensure_list

NUMERIC_PATTERN = re.compile(r"^\d+$")
EXTENSION_PATTERN = re.compile(r"extension\([\"|\'](.*?)[\"|\']\)")
WHERE_PATTERN = re.compile(r"where\((.+?)=[\"|\'](.*?)[\"|\']\)")
ITEM_PATTERN = re.compile(r"item\((\d+?)\)")
TYPE_CHOICES_PATTERN = re.compile(r"(.*?)\[x\]")
FIRST_PATTERN = re.compile(r"^first()$")
LAST_PATTERN = re.compile(r"^last()$")
TAIL_PATTERN = re.compile(r"^tail()$")

def split_fhirpath(fhir_path: str) -> List[str]:
    # Split FHIR path only at non-quoted dots
    return re.split(r'\.(?=(?:[^\)]*\([^\(]*\))*[^\(\)]*$)', fhir_path)

def join_fhirpath(*segments: List[Union[str, int]]) -> str:
    def _clean_segment(segment: str) -> str:
        while segment.startswith('.'): 
            segment = segment[1:]
        while segment.endswith('.'): 
            segment = segment[:-1]
        return segment
    return '.'.join([_clean_segment(str(segment)) for segment in segments]) 

class FHIRPathNavigator:

    def _create_empty_segment_resource(self, element, segment):
        model_field = element.__class__.__fields__.get(segment)
        if model_field:
            field_type = get_fhir_type_name(model_field.type_)
            try:
                model = get_fhir_model_class(field_type)
            except KeyError:
                return None
            model.validate_assignment = False
            empty_resource =  model.construct()
            if is_list_type(model_field):
                if not isinstance(getattr(element, segment), list):
                    setattr(element, segment, [])
                getattr(element, segment).append(empty_resource)
            else:
                setattr(element, segment, empty_resource)  
            return empty_resource    
    
    def _set_value_at_path(self, collection, fhir_path_element, value):
        for element in collection:
            if not hasattr(element, fhir_path_element):
                self._create_empty_segment_resource(element, fhir_path_element)
                if not hasattr(element, fhir_path_element):
                    raise AttributeError(f'FHIRPath element in collection has no attribute "{fhir_path_element}"')
            setattr(element, fhir_path_element, value)

    def __init__(self, fhir_resource):
        if isinstance(fhir_resource, FHIRAbstractModel):
            self.fhir_resource = fhir_resource
            self.path_origin = fhir_resource.get_resource_type()
        elif isinstance(fhir_resource, dict):
            self.path_origin = fhir_resource.get('resource_type')
            self.fhir_resource = make_dataclass("FHIRResource", ((k, type(v)) for k, v in fhir_resource.items()))(**fhir_resource)
        else: 
            raise TypeError('Invalid resource type, must be a Pydantic FHIR model or a dict')
    
    def _extension(self, collection, statement):
        extension_url = EXTENSION_PATTERN.search(statement).group(1)
        return [
            extension for element in collection 
                    for extension in ensure_list(element.extension) 
                        if extension is not None and extension.url == extension_url
        ]

    def _where(self, collection, statement):
        condition_path, condition_value = WHERE_PATTERN.search(statement).group(1,2)
        return [
            obj for element in collection 
                    for obj in ensure_list(element) 
                         if FHIRPathNavigator(obj).get_value(condition_path) == condition_value
        ]    
    
    def _item(self, collection, statement):
        index = int(ITEM_PATTERN.search(statement).group(1))
        return [collection[index]] 
        
    def _first(self, collection):
        return [collection[0]] 
        
    def _last(self, collection):
        return [collection[-1]] 
        
    def _tail(self, collection):
        return collection[:-1]
        
    def _all_type_choices(self, collection, statement):
        type_choice_name = TYPE_CHOICES_PATTERN.search(statement).group(1)
        return [
            getattr(obj, element) 
                for obj in collection
                    for element in obj.__dict__.keys() 
                        if element.startswith(type_choice_name) and getattr(obj, element) 
        ]
        
    def _traverse_fhirpath(self, fhirpath, set_value=None):
        # Split union collection into individual path collections
        union_collection = []
        for fhir_path in fhirpath.split('|'):
            # Split the path into its segments
            fhirpath_segments = split_fhirpath(fhir_path.strip())
            # If path's entry point is the core resource, remove it
            if self.path_origin == fhirpath_segments[0]:
                traversed_path = fhirpath_segments[0]
                fhirpath_segments = fhirpath_segments[1:]
            # If a value must be set at the end of the path, remove the last segment
            if set_value is not None:
                last_fhirpath_segment = fhirpath_segments[-1]
                fhirpath_segments = fhirpath_segments[:-1]
            traversed_path = ''
            # Initialize the collection with the full resource
            collection = [self.fhir_resource]
            # Compile list of FHIRPath segment pattern handlers
            FHIRPATH_PATTERNS = {
                WHERE_PATTERN: self._where,
                EXTENSION_PATTERN: self._extension,
                ITEM_PATTERN: self._item,
                NUMERIC_PATTERN: lambda coll, segment: self._item(coll, f'item({segment})'),
                TYPE_CHOICES_PATTERN: self._all_type_choices,
                FIRST_PATTERN: lambda coll, _: self._first(coll),
                LAST_PATTERN: lambda coll, _: self._last(coll),
                TAIL_PATTERN: lambda coll, _: self._tail(coll)
            }
            # Iterate over the FHIRPath segments
            for fhirpath_segment in fhirpath_segments:
                traversed_path = join_fhirpath(traversed_path, fhirpath_segment)
                try:
                    for pattern, operation in FHIRPATH_PATTERNS.items():
                        # Look for patterns in the segment
                        if pattern.match(fhirpath_segment):
                            collection = operation(collection, fhirpath_segment)
                            break
                    else:
                        # Otherwise, assume simple element path segments
                        collection = [
                            value if getattr(element, fhirpath_segment, None)
                            else self._create_empty_segment_resource(element, fhirpath_segment)
                                for element in collection                          
                                    for value in ensure_list(getattr(element, fhirpath_segment, None)) 
                        ]   
                    # Remove any Nones from the collection
                    collection = [element for element in collection if element is not None] 
                except RuntimeError: 
                    raise KeyError(f"\nFHIRPath {traversed_path} does not exist.\n\nTraceback:\n{traceback.format_exc()}")
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
        return self._traverse_fhirpath(fhir_path)
            
    def set_value(self, fhir_path, new_value):
        self._traverse_fhirpath(fhir_path, new_value)
        
    def get_pydantic_field(self, fhir_path):
        fhirpath_segments = split_fhirpath(fhir_path)
        last_fhirpath_segment = fhirpath_segments[-1]
        fhirpath_segments = fhirpath_segments[:-1]
        if len(fhirpath_segments)>0:
            element = self._traverse_fhirpath(join_fhirpath(*fhirpath_segments))[0]
        else:
            element = self.fhir_resource
        return element.__class__.__fields__.get(last_fhirpath_segment)
    
