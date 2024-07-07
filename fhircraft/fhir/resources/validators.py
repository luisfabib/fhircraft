import warnings

def validate_element_constraint(cls, value, expression):
    from fhircraft.fhir.path import fhirpath, FhirPathLexerError, FhirPathParserError
    from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem
    try:
        assert fhirpath.parse(expression).evaluate([FHIRPathCollectionItem(value=value)], create=False)
    except (NotImplementedError, FhirPathLexerError, FhirPathParserError) as e:
        warnings.warn(f"Warning: FHIRPath raised error for expression: {expression} \n {str(e)}")
    return value

def validate_type_choice_element(instance, field_types, field_name_base):
    assert sum(getattr(instance, field_name_base + field_type.__name__, None) is not None for field_type in field_types) <= 1, f'Type choice element {field_name_base}[x] can only have one value set.'
    return instance