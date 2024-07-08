import warnings
from fhircraft.utils import ensure_list 

def validate_element_constraint(cls, value, expression, human, key):
    from fhircraft.fhir.path import fhirpath, FhirPathLexerError, FhirPathParserError
    from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem
    if value is None:
        return value
    for item in ensure_list(value):
        try:
            assert fhirpath.parse(expression).evaluate([FHIRPathCollectionItem(value=item)], create=False), f'{human} ([Invariant {key}] {expression})'
        except (NotImplementedError, FhirPathLexerError, FhirPathParserError) as e:
            warnings.warn(f"Warning: FHIRPath raised error for expression: {expression} \n {str(e)}")
    return value

def validate_type_choice_element(instance, field_types, field_name_base):
    assert sum(getattr(instance, field_name_base + field_type.__name__, None) is not None for field_type in field_types) <= 1, f'Type choice element {field_name_base}[x] can only have one value set.'
    return instance