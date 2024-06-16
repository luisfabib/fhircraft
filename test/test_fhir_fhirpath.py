import pytest

from fhircraft.fhir.fhirpath import Child, Root, Fields, Index, Slice, Where, Extension, Single
from fhircraft.fhir.parser import parse
from  fhir.resources.R4B.observation import Observation 
from fhir.resources.R4B.fhirtypesvalidators import get_fhir_model_class


observation = Observation(**{
    'status': 'final', 
    'code': {
        'coding': [{'code': 'C1'}],
    }, 
    'identifier': [{
        'system': 'id_system',
        'use': 'oficial',
        'value': '123',
    },{
        'system': 'id_system',
        'use': 'oficial',
        'value': '456',
    },{
        'system': 'id_system',
        'use': 'oficial',
        'value': '789',
    }],
    'valueInteger': 5,
    'fhir_comments':'Commenting',
    'extension': [
        {
            'url': 'http://domain.org/extension-1',
            'valueString': 'extension-value-1',
            'extension': [
                {
                    'url': 'http://domain.org/extension-2',
                    'valueString': 'extension-value-2'
                }
            ]
        },
    ],
    'component': [
        {
            'code': {
                'coding': [{
                    'code': 'component-1',
                    'system': 'https://system.org'
                }]
            },
            'valueString': 'component-1-value'
        },
        {
            'code': {
                'coding': [{
                    'code': 'component-2',
                    'system': 'https://system.org'
                }]
            },
            'valueString': 'component-2-value'
        }
    ]
})

# ======== Child - FHIRPath ============
#               Find                        
# ======================================
fhirpath_child_find_test_cases = (
    (Child(Root(), Fields('status')), observation.status),
    (Child(Root(), Fields('identifier')), observation.identifier),
    (Child(Child(Root(), Fields('identifier')), Fields('value')), [id.value for id in observation.identifier]),
)
    
@pytest.mark.parametrize("path_object, expected_value", fhirpath_child_find_test_cases)
def test_fhirpath_child_find(path_object, expected_value):
    matches = path_object.find(observation)
    assert len(matches) == 1, 'No match found'
    expected_values = expected_value if isinstance(expected_value, list) else [expected_value]
    found_values = matches[0].value if isinstance(matches[0].value, list) else [matches[0].value]
    assert len(found_values) == len(expected_values)
    for value, expected in zip(found_values, expected_values):
        assert value == expected

# ======== Child - FHIRPath ============
#           Update & Create                        
# ======================================

fhirpath_child_update_test_cases = (
    # Update
    (Child(Root(), Fields('status')), 'pending', lambda obs: obs.status),
    (Child(Root(), Fields('identifier')), observation.identifier, lambda obs: obs.identifier),
    # Create
    (Child(Root(), Fields('id')), 'ID12345', lambda obs: obs.id),    
    (Child(Child(Root(), Fields('subject')), Fields('reference')), 'subjectX', lambda obs: obs.subject.reference),
)        

@pytest.mark.parametrize("path_object, update_value, getattr_fcn", fhirpath_child_update_test_cases)
def test_fhirpath_child_update(path_object, update_value, getattr_fcn):
    new_observation = observation.copy(deep=True)
    path_object.update_or_create(new_observation, update_value)
    assert getattr_fcn(new_observation) == update_value
    


# ======== Index - FHIRPath ============
#               Find                        
# ======================================
fhirpath_index_find_test_cases = (
    # Update
    (Child(Child(Root(), Fields('identifier')), Index(0)), observation.identifier[0]),
    (Child(Child(Child(Root(), Fields('identifier')), Index(0)), Fields('value')), observation.identifier[0].value),
    # Create
    (Child(Child(Root(), Fields('identifier')), Index(0)), observation.identifier[0]),
    (Child(Child(Child(Root(), Fields('identifier')), Index(0)), Fields('value')), observation.identifier[0].value),
)
    
@pytest.mark.parametrize("path_object, expected_value", fhirpath_index_find_test_cases)
def test_fhirpath_index_find(path_object, expected_value):
    matches = path_object.find(observation)
    assert len(matches) == 1, 'No match found'
    expected_values = expected_value if isinstance(expected_value, list) else [expected_value]
    found_values = matches[0].value if isinstance(matches[0].value, list) else [matches[0].value]
    assert len(found_values) == len(expected_values)
    for value, expected in zip(found_values, expected_values):
        assert value == expected
        

# ======== Index - FHIRPath ============
#           Update & Create                        
# ======================================

fhirpath_index_update_test_cases = (
    (Child(Child(Root(), Fields('identifier')), Index(0)), observation.identifier[1], lambda obs: obs.identifier[0]),
    (Child(Child(Child(Root(), Fields('identifier')), Index(0)), Fields('value')), 'ABC123', lambda obs: obs.identifier[0].value),
    (Child(Child(Root(), Fields('identifier')), Index(4)), observation.identifier[1], lambda obs: obs.identifier[4]),
    (Child(Child(Child(Root(), Fields('identifier')), Index(4)), Fields('value')), 'ABC123', lambda obs: obs.identifier[4].value),
)        

@pytest.mark.parametrize("path_object, update_value, getattr_fcn", fhirpath_index_update_test_cases)
def test_fhirpath_index_update(path_object, update_value, getattr_fcn):
    new_observation = observation.copy(deep=True)
    path_object.update_or_create(new_observation, update_value)
    assert getattr_fcn(new_observation) == update_value
    
    
    
fhirpath_find_test_cases = (
    ('Observation.valueInteger', observation, 5),
    ('Observation.identifier.value[1]', observation, '456'),
    ('Observation.identifier[1].value', observation, '456'),
    ('Observation.identifier.value', observation, ['123','456','789']),
    ('Observation.identifier.first().value', observation, '123'),
    ('Observation.identifier.last().value', observation, '789'),
    ('Observation.fhir_comments', observation, 'Commenting'),
    ('Observation.extension("http://domain.org/extension-1").valueString', observation, 'extension-value-1'),
    ('Observation.extension("http://domain.org/extension-1").extension("http://domain.org/extension-2").valueString', observation, 'extension-value-2'),
    ('Observation.component.where(code.coding.code="component-1").valueString', observation, 'component-1-value'),
    ('Observation.component.where(code.coding.system="https://system.org").where(code.coding.code="component-1").valueString', observation, 'component-1-value'),
)

@pytest.mark.parametrize("path_string, data_object, expected_value", fhirpath_find_test_cases)
def test_fhirpath_find(path_string, data_object, expected_value):
    match = parse(path_string).find(data_object)
    assert len(match) == 1, 'No match found'
    expected_values = expected_value if isinstance(expected_value, list) else [expected_value]
    found_values = match[0].value if isinstance(match[0].value, list) else [match[0].value]
    assert len(found_values) == len(expected_values)
    for value, expected in zip(found_values, expected_values):
        assert value == expected
        


fhirpath_update_test_cases = (
    ('Observation.valueInteger', 12, lambda obs: obs.valueInteger),
    ('Observation.identifier[0].value', '456', lambda obs: obs.identifier[0].value),
    ('Observation.identifier[1].system', 'home', lambda obs: obs.identifier[1].system),
    ('Observation.identifier[4].value', '123', lambda obs: obs.identifier[4].value),
    ('Observation.identifier.first().value', '123', lambda obs: obs.identifier[0].value),
    ('Observation.identifier.last().value', '789', lambda obs: obs.identifier[-1].value),
    ('Observation.fhir_comments', 'Commenting', lambda obs: obs.fhir_comments),
    ('Observation.extension[0].extension[2].valueString', 'testvalue', lambda obs: obs.extension[0].extension[2].valueString),
)

@pytest.mark.parametrize("path_string, update_value, getattr_fcn", fhirpath_update_test_cases)
def test_fhirpath_update_existing(path_string, update_value, getattr_fcn):
    _observation = observation.copy(deep=True)
    parse(path_string).update_or_create(_observation, update_value)
    assert getattr_fcn(_observation) == update_value


fhirpath_create_test_cases = (
    ('Observation.valueInteger', 12, lambda obs: obs.valueInteger),
    ('Observation.identifier[0].value', '456', lambda obs: obs.identifier[0].value),
    ('Observation.identifier[1].value', '456', lambda obs: obs.identifier[1].value),
    ('Observation.identifier.first().value', '123', lambda obs: obs.identifier[0].value),
    ('Observation.identifier.last().value', '789', lambda obs: obs.identifier[-1].value),
    ('Observation.fhir_comments', 'Commenting', lambda obs: obs.fhir_comments),
    ('Patient.contact[0].telecom[0].value', 'teletest', lambda pat: pat.contact[0].telecom[0].value),
    ('Patient.contact.telecom[1].use', 'home', lambda pat: pat.contact[0].telecom[1].use),
    ('Patient.name[0].given[0]', 'John', lambda pat: pat.name[0].given[0]),
)

@pytest.mark.parametrize("path_string, update_value, getattr_fcn", fhirpath_update_test_cases)
def test_fhirpath_create(path_string, update_value, getattr_fcn):
    Observation.Config.validate_assignment = False
    new_resource = get_fhir_model_class(path_string.split('.',1)[0]).construct()
    parse(path_string).update_or_create(new_resource, update_value)
    assert getattr_fcn(new_resource) == update_value