from pydantic import BaseModel , ValidationError
from fhircraft.utils import get_all_models_from_field
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
        from fhircraft.fhir.path import fhirpath
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
                    for arg in get_all_models_from_field(field) if arg.model_fields.get('extension'))
            , None) for field_name, field in cls.model_fields.items()  if field_name != 'extension'
        })
        # Compile the sliced elements in the model
        return {
            field_name: slices for field_name, field in fields.items() 
                if field and bool(slices := list(get_all_models_from_field(field, issubclass_of=FHIRSliceModel))) 
        } 

    @classmethod
    def clean_unusued_slice_instances(cls, resource):
        from fhircraft.fhir.path import fhirpath
        # Remove unused/incomplete slices
        for element, slices in cls.get_sliced_elements().items():
            valid_elements = [col.value for col in fhirpath.parse(element).find_or_create(resource) if col.value is not None]        
            new_valid_elements = []
            if not valid_elements:
                continue
            for slice in slices:
                # Get all the elements that conform to this slice's definition           
                sliced_entries = [entry for entry in valid_elements if isinstance(entry, slice)] 
                for entry in sliced_entries:
                    if slice.get_sliced_elements():
                        entry = slice.clean_unusued_slice_instances(entry) 
                    if (entry.is_FHIR_complete and entry.has_been_modified) \
                        or (entry.is_FHIR_complete  and not entry.has_been_modified and slice.min_cardinality>0):
                        if entry not in new_valid_elements:
                            new_valid_elements.append(entry)                
            # Set the new list with only the valid slices
            collection = fhirpath.parse(element).find_or_create(resource)
            [col.set_literal(new_valid_elements) for col in collection]
        return resource
        
    

class FHIRSliceModel(FHIRBaseModel):
    min_cardinality: ClassVar[int] = 0
    max_cardinality: ClassVar[int] = 1
    
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