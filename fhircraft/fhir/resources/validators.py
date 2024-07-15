import warnings
import traceback
from fhircraft.utils import ensure_list 

def _validate_FHIR_element_constraint(value, expression, human, key, severity):
    from fhircraft.fhir.path import fhirpath, FhirPathLexerError, FhirPathParserError
    from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem
    if value is None:
        return value
    for item in ensure_list(value):
        try:
            valid = fhirpath.parse(expression).evaluate([FHIRPathCollectionItem(value=item)], create=False)
            print(valid, '<-', expression, value)
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

def validate_type_choice_element(instance, field_types, field_name_base):
    assert sum(getattr(instance, field_name_base + field_type if isinstance(field_type, str) else field_type.__name__, None) is not None for field_type in field_types) <= 1, f'Type choice element {field_name_base}[x] can only have one value set.'
    return instance

def get_type_choice_value_by_base(instance, base):
    for field in instance.model_fields:
        if field.startswith(base):
            value = getattr(instance, field)
            if value is not None:
                return value