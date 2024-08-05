from pydantic import BaseModel 
from fhircraft.utils import _get_deepest_args, ensure_list
from typing import ClassVar
import inspect 

class FHIRBaseModel(BaseModel):
    
    def model_dump(self, *args, **kwargs):
        kwargs.update({'by_alias': True, 'exclude_none': True})
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        kwargs.update({'by_alias': True, 'exclude_none': True})
        return super().model_dump_json(*args, **kwargs)

    @classmethod 
    def model_construct_with_slices(cls, slice_copies=9):
        instance = super().model_construct()
        for element, slices in cls.get_sliced_elements().items():
            slice_resources = []
            for slice in slices:
                # Add empty slice instances
                slice_resources.extend([
                    slice.model_construct()
                        for _ in range(min(slice.max_cardinality, slice_copies))
                ])
            # Set the whole list of slices in the resource
            setattr(instance, element, slice_resources)
        return instance
    
    @classmethod 
    def get_sliced_elements(cls):
        return {
            field_name: slices for field_name, field in cls.model_fields.items() 
                if bool(slices := [arg
                    for arg in _get_deepest_args(field.annotation)
                    if inspect.isclass(arg) and issubclass(arg, FHIRSliceModel) 
            ]) 
        } 
    

class FHIRSliceModel(FHIRBaseModel):
    __track_changes__: bool = False 
    __has_been_modified__: bool = False
    min_cardinality: ClassVar[int] = 0
    max_cardinality: ClassVar[int] = 1
    
    def __setattr__(self, name:str, value):
        super().__setattr__(name, value)
        if name not in ['__track_changes__','__has_been_modified__'] and self.__track_changes__:
            super().__setattr__('__has_been_modified__', True)
    
    @property
    def is_FHIR_complete(self):
        BASE_ELEMENTS = ['text','extension', 'id', 'resourceType']
        slice_available_elements = sorted(set([name for name in self.__class__.model_fields if '_ext' not in name and not name.startswith('_') and name not in BASE_ELEMENTS]))
        slice_preset_elements = sorted(set([name for name, value in self.model_dump().items() if (value is not None or value!=[]) and '_ext' not in name and not name.startswith('_')  and name not in BASE_ELEMENTS]))
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