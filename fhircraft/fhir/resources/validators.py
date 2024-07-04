from fhircraft.fhir.path import fhirpath

def validate_element_constraint(cls, value, expression):
    assert fhirpath.parse(expression).evaluate()
    return value

def validate_type_choice_element(instance, field_types, field_name_base):
    assert sum(getattr(instance, field_name_base + field_type.__name__, None) is not None for field_type in field_types) <= 1, f'Type choice element {field_name_base}[x] can only have one value set.'
    return instance