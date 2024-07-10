
def get_FHIR_type(type_str, version='R4B'):
    try:
        import fhircraft.fhir.resources.datatypes.R4B.complex_types as R4B_types
    except ModuleNotFoundError:
        return None
    if version == 'R4B':
        return getattr(R4B_types, type_str, None)