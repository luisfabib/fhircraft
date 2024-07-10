import inspect
from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.utils import get_fhir_model_from_field, ensure_list

from jinja2 import Environment, FileSystemLoader
import re 

def generate_resource_model_code(resources):

    file_loader = FileSystemLoader('fhircraft/fhir/resources/')
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('resource_template.py.j2')

    before_imports = []
    after_imports = []
    reload_models = []

    def properties(cls):
        return {
            key: value.fget
            for key, value in cls.__dict__.items()
            if isinstance(value, property)
        }
        
    def serialize_model(model, data):
        # base = model.__base__.__name__ 
        # if base!='BaseModel':
        #     before_imports.append(f'from fhircraft.fhir.resources.datatypes.R4B.{base.lower()} import {base}')
        subdata = {}

        for field, info in model.model_fields.items():
            if model.__base__ and field in model.__base__.model_fields:
                continue
            field_type = repr(info.annotation)
            has_submodel = 'fhircraft.fhir.resources.factory' in field_type 
            field_type = field_type.replace('fhircraft.fhir.resources.factory.', '')
            field_type = field_type.replace('fhircraft.fhir.resources.primitive_types', 'fhir_primitive')
            field_type = field_type.replace('fhircraft.fhir.resources.complex_types', 'fhir_complex')
            field_type = field_type.replace('<class ', '').replace('>','')

            if "'NoneType'" in field_type:
                field_type = field_type.replace("'NoneType'", 'typing.Optional["Element"]')

            forward_ref_match = re.match(r".*ForwardRef\(\'(.*)\'\).*", field_type, re.MULTILINE)
            if forward_ref_match:
                forward_ref = forward_ref_match.group(1)
                field_type = field_type.replace('ForwardRef(', '').replace(')','')
                # statement = f'from fhircraft.fhir.resources.datatypes.R4B.{forward_ref.lower()} import {forward_ref}'
                # if statement not in after_imports:
                #     after_imports.append(statement)
                statement = f'{model.__name__}.model_rebuild()'
                if statement not in reload_models:
                    reload_models.append(statement)
            if has_submodel:
                data = serialize_model(get_fhir_model_from_field(info), data)
            subdata[field] = {
                'annotation': field_type,
                'description': info.description, 
                'alias': info.alias, 
                'default': info.default,
            }
        data.update({model: {'fields': subdata, 'properties': properties(model)}})
        return data


    data = [serialize_model(resource, {}) for resource in ensure_list(resources)]

    return template.render(data=data, imports={'before': before_imports, 'after': after_imports}, reload=reload_models)

