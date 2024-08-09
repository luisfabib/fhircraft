from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.utils import get_all_models_from_field, get_fhir_model_from_field, ensure_list

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

from enum import EnumType

from collections import defaultdict 
from typing import Dict, List
import inspect
import re 


FACTORY_MODULE = inspect.getmodule(ResourceFactory).__name__

class CodeGenerator:
    
    import_statements: Dict[str, List[str]]
    model_reload_statements: List[str]
    
    def __init__(self):
        # Prepare the templating engine environment
        file_loader = FileSystemLoader('fhircraft/fhir/resources/')
        env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
        env.filters['escapequotes'] = lambda s: s.replace('"','\\"')
        self.template = env.get_template('resource_template.py.j2')

    def add_import_statement(self, obj):
        # Get the module of the object
        module = inspect.getmodule(obj)
        if module is None:
            raise ValueError(f"The object {obj} does not belong to a module")        
        # Get the name of the module and the object
        module_name = module.__name__
        object_name = obj.__name__
        # Generate the import statement
        if module_name != FACTORY_MODULE and object_name not in self.import_statements[module_name]:
            self.import_statements[module_name].append(object_name)
            
    def serialize_model(self, model, data):
        model_base = model.__base__ 
        # Add import statement for the base class the the model inherits
        if model_base and model_base != BaseModel:
            self.add_import_statement(model.__base__)

        subdata = {}
        for field, info in model.model_fields.items():
            if model.__base__ and field in model.__base__.model_fields and all([getattr(info, slot) == getattr(model.__base__.model_fields[field], slot) for slot in info.__slots__ if not slot.startswith('_')]):
                continue
            field_type = repr(info.annotation)
            
            if isinstance(info.annotation, EnumType):
                field_type = info.annotation
                field_type = f'''typing.Literal['{field_type['fixedValue'].value}']'''
            
            has_submodel = FACTORY_MODULE in field_type 
            
            if has_submodel:
                field_type = field_type.replace(FACTORY_MODULE + '.', '')
                for submodel in get_all_models_from_field(info):
                    data = self.serialize_model(submodel, data)
            else:
                complex_type_model = get_fhir_model_from_field(info)
                if complex_type_model:
                    self.add_import_statement(get_fhir_model_from_field(info))  
                    for module in self.import_statements:
                        field_type = field_type.replace(f'{module}.','')
                field_type = field_type.replace("<class '","").replace("'>","")

                if "NoneType" in field_type:
                    field_type = field_type.replace("NoneType", 'typing.Optional["Element"]')
                
                forward_ref_match = re.match(r".*ForwardRef\(\'(.*)\'\).*", field_type, re.MULTILINE)
                if forward_ref_match:
                    field_type = field_type.replace('ForwardRef(', '').replace(')','')
                    statement = f'{model.__name__}.model_rebuild()'
                    if statement not in self.model_reload_statements:
                        self.model_reload_statements.append(statement)
            subdata[field] = {
                'annotation': field_type,
                'description': info.description, 
                'alias': info.alias, 
                'default': info.default,
            }
        model_properties = {
            key: value.fget
            for key, value in model.__dict__.items()
            if isinstance(value, property)
        }
        data.update({model: {'fields': subdata, 'properties': model_properties}})
        return data

    def generate_resource_model_code(self, resources: type):

        self.import_statements = defaultdict(list)
        self.model_reload_statements = []
        
        data = [self.serialize_model(resource, {}) for resource in ensure_list(resources)]
        source_code = self.template.render(
            data=data, 
            imports=self.import_statements, 
            reload=self.model_reload_statements
        )
        for module in self.import_statements:
            module = module.replace('.',r'\.')
            for regex in [fr"(\<class \'{module}\.(\w*)\'\>)", r"(\<class \'(\w*)\'\>)"]:
                for match in re.finditer(regex, source_code):
                    source_code = source_code.replace(match.group(1), match.group(2))

        source_code = source_code.replace("FieldInfo(annotation=NoneType, required=True, metadata=[_PydanticGeneralMetadata(union_mode='left_to_right')])", "Field(union_mode='left_to_right')")


        return source_code
