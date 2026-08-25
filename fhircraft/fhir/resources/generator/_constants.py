from fhircraft.fhir.resources.factory import FHIRModelFactory
from fhircraft.utils import get_module_name

FACTORY_MODULE = get_module_name(FHIRModelFactory)
LEFT_TO_RIGHT_COMPLEX = "FieldInfo(annotation=NoneType, required=True, metadata=[_PydanticGeneralMetadata(union_mode='left_to_right')])"
LEFT_TO_RIGHT_SIMPLE = "Field(union_mode='left_to_right')"
