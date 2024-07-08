import inspect
from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.utils import get_fhir_model_from_field 

from jinja2 import Environment, FileSystemLoader

def generate_resource_model_code(canonical_url):

    file_loader = FileSystemLoader('fhircraft/fhir/resources/')
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('resource_template.py.j2')


    resource = ResourceFactory().construct_resource_model(canonical_url)

    def serialize_model(model, data):
        subdata = {}
        for field, info in model.model_fields.items():
            field_type = str(info.annotation)
            has_submodel = 'fhircraft.fhir.resources.factory' in field_type 
            field_type = field_type.replace('fhircraft.fhir.resources.factory.', '')
            field_type = field_type.replace('fhircraft.fhir.resources.primitive_types', 'fhir_primitive')
            field_type = field_type.replace('fhircraft.fhir.resources.complex_types', 'fhir_complex')
            field_type = field_type.replace('<class ', '').replace('>','')
            if has_submodel:
                data = serialize_model(get_fhir_model_from_field(info), data)
            subdata[field] = {
                'annotation': field_type,
                'description': info.description, 
                'alias': info.alias, 
                'default': info.default,
            }
        data.update({model: subdata})
        return data


    data = serialize_model(resource, {})

    return template.render(data=data)

