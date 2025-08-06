from importlib import import_module


def get_complex_FHIR_type(type_str: str, release="R4B") -> type:
    FHIR_types = import_module(
        f"fhircraft.fhir.resources.datatypes.{release}.complex_types"
    )
    return getattr(FHIR_types, type_str)
