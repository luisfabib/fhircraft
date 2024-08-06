from pydantic import BaseModel , ValidationError
from fhircraft.utils import _get_deepest_args, ensure_list
from fhircraft.fhir.path import fhirpath
from typing import ClassVar
from copy import copy
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
                    slice.model_construct_with_slices()
                        for _ in range(min(slice.max_cardinality, slice_copies))
                ])
            # Set the whole list of slices in the resource
            collection = fhirpath.parse(element).find_or_create(instance)
            [col.set_literal(slice_resources) for col in collection]
        return instance
    
    @classmethod 
    def get_sliced_elements(cls):
        # Get model elements' fields
        fields = copy(cls.model_fields)
        # Get model elements' extension fields 
        fields.update({ 
            f'{field_name}.extension': next((arg.model_fields.get('extension')
                    for arg in _get_deepest_args(field.annotation)
                        if inspect.isclass(arg) and issubclass(arg, FHIRBaseModel) if arg.model_fields.get('extension'))
            , None) for field_name, field in cls.model_fields.items()  if field_name != 'extension'
        })
        # Compile the sliced elements in the model
        return {
            field_name: slices for field_name, field in fields.items() 
                if field and bool(slices := [arg
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
        model = self.__class__ 
        try:
            model.model_validate(self.model_dump())
            return True 
        except ValidationError:
            return False
    
    @property
    def has_been_modified(self):
        return self != self.__class__.model_construct_with_slices()