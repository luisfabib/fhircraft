from importlib import import_module 

def get_complex_FHIR_type(type_str, release='R4B'):
    try:
        FHIR_types = import_module(f'fhircraft.fhir.resources.datatypes.{release}.complex_types')
    except ModuleNotFoundError:
        return None
    return getattr(FHIR_types, type_str, None)