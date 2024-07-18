from pydantic import BaseModel 

class FHIRBaseModel(BaseModel):
    
    def model_dump(self, *args, **kwargs):
        kwargs.update({'by_alias': True, 'exclude_none': True})
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        kwargs.update({'by_alias': True, 'exclude_none': True})
        return super().model_dump_json(*args, **kwargs)