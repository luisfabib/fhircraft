import inspect
from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.utils import get_fhir_model_from_field, ensure_list

from jinja2 import Environment, FileSystemLoader
import re 
from collections import defaultdict 
def generate_resource_model_code(resources):

    file_loader = FileSystemLoader('fhircraft/fhir/resources/')
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
    env.filters['escapequotes'] = lambda s: s.replace('"','\\"')
    template = env.get_template('resource_template.py.j2')

    imports = defaultdict(list)
    after_imports = []
    reload_models = []

    def properties(cls):
        return {
            key: value.fget
            for key, value in cls.__dict__.items()
            if isinstance(value, property)
        }

    def generate_import_statement(obj):
        if not obj: 
            return
        # Get the module of the object
        module = inspect.getmodule(obj)
        
        if module is None:
            raise ValueError(f"The object {obj} does not belong to a module")
        
        # Get the name of the module and the object
        module_name = module.__name__
        object_name = obj.__name__

        # Generate the import statement
        imports[module_name].append(object_name)
        
        return object_name
        
    def serialize_model(model, data):
        base = model.__base__ 
        if base.__name__!='BaseModel':
            generate_import_statement(model.__base__)
        subdata = {}

        for field, info in model.model_fields.items():
            if model.__base__ and field in model.__base__.model_fields:
                continue
            field_type = repr(info.annotation)
            
            has_submodel = 'fhircraft.fhir.resources.factory' in field_type 
            
            if has_submodel:
                field_type = field_type.replace('fhircraft.fhir.resources.factory.', '')
                data = serialize_model(get_fhir_model_from_field(info), data)
            else:
                complex_type_model = get_fhir_model_from_field(info)
                if complex_type_model:
                    generate_import_statement(get_fhir_model_from_field(info))  
                    for module in imports:
                        field_type = field_type.replace(f'{module}.','')
                field_type = field_type.replace("<class '","").replace("'>","")

                
                if "NoneType" in field_type:
                    field_type = field_type.replace("NoneType", 'typing.Optional["Element"]')

                forward_ref_match = re.match(r".*ForwardRef\(\'(.*)\'\).*", field_type, re.MULTILINE)
                if forward_ref_match:
                    field_type = field_type.replace('ForwardRef(', '').replace(')','')
                    statement = f'{model.__name__}.model_rebuild()'
                    if statement not in reload_models:
                        reload_models.append(statement)
            subdata[field] = {
                'annotation': field_type,
                'description': info.description, 
                'alias': info.alias, 
                'default': info.default,
            }
        data.update({model: {'fields': subdata, 'properties': properties(model)}})
        return data


    data = [serialize_model(resource, {}) for resource in ensure_list(resources)]
    source_code = template.render(data=data, imports=imports, reload=reload_models)
    for module in imports:
        module = module.replace('.','\.')
        for regex in [fr"(\<class \'{module}\.(\w*)\'\>)", r"(\<class \'(\w*)\'\>)"]:
            for match in re.finditer(regex, source_code):
                source_code = source_code.replace(match.group(1), match.group(2))


    return source_code
