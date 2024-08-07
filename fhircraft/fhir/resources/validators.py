import warnings
import traceback
from fhircraft.utils import ensure_list, merge_dicts, get_all_models_from_field
from fhircraft.fhir.resources.base import FHIRSliceModel 

def _validate_FHIR_element_constraint(value, expression, human, key, severity):
    from fhircraft.fhir.path import fhirpath, FhirPathLexerError, FhirPathParserError
    from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem
    if value is None:
        return value
    for item in ensure_list(value):
        try:
            valid = fhirpath.parse(expression).evaluate([FHIRPathCollectionItem(value=item)], create=False)
            if valid == []:
                valid = True
            error_message =  f'{human}. [{key}] -> "{expression}"'
            if severity == 'warning' and not valid:
                warnings.warn(error_message)
            else:
                assert valid, error_message
        except (ValueError, FhirPathLexerError, FhirPathParserError, AttributeError, NotImplementedError) as e:
            warnings.warn(f"Warning: FHIRPath raised {e.__class__.__name__} for expression: {expression}. {traceback.format_exc()}")
    return value

def validate_element_constraint(cls, value, expression, human, key, severity):
    return _validate_FHIR_element_constraint(value, expression, human, key, severity)

def validate_model_constraint(instance, expression, human, key, severity):
    return _validate_FHIR_element_constraint(instance, expression, human, key, severity)

def validate_FHIR_element_pattern(cls, element, pattern):
    if isinstance(pattern, list): pattern = pattern[0]
    _element = element[0] if isinstance(element, list) else element
    assert merge_dicts(_element.model_dump(), pattern.model_dump()) == _element.model_dump(), \
            f'Value does not fulfill pattern:\n{pattern.model_dump_json(indent=2)}'
    return element

def validate_type_choice_element(instance, field_types, field_name_base):
    assert sum(
        getattr(instance, field_name_base + field_type if isinstance(field_type, str) else field_type.__name__, None) is not None 
            for field_type in field_types 
    ) <= 1, f'Type choice element {field_name_base}[x] can only have one value set.'
    return instance


def validate_slicing_cardinalities(cls, values, field_name):
    slices =  get_all_models_from_field(cls.model_fields[field_name], issubclass_of=FHIRSliceModel)
    for slice in slices:
        slice_instances_count = sum([isinstance(value, slice) for value in values])
        assert slice_instances_count >= slice.min_cardinality, \
            f"Slice '{slice.__name__}' for field '{field_name}' violates its min. cardinality. Requires min. cardinality of {slice.min_cardinality}, but got {slice_instances_count}"
        assert slice_instances_count <= slice.max_cardinality, \
            f"Slice '{slice.__name__}' for field '{field_name}' violates its max. cardinality. Requires max. cardinality of {slice.max_cardinality}, but got {slice_instances_count}"
    return values
        


def get_type_choice_value_by_base(instance, base):
    for field in instance.model_fields:
        if field.startswith(base):
            value = getattr(instance, field)
            if value is not None:
                return value