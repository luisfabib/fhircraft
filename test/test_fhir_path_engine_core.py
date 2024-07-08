import pytest

from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, FHIRPathError, Invocation, Root, Element
from fhircraft.fhir.path.engine.subsetting import Index
from fhircraft.fhir.path.parser import parse
from fhircraft.utils import ensure_list, get_fhir_model_from_field
from fhircraft.fhir.resources.complex_types import Coding, CodeableConcept, Identifier


from unittest import TestCase


from fhircraft.fhir.resources.factory import construct_resource_model
Observation = construct_resource_model(f'https://hl7.org/fhir/R4B/observation.profile.json')
ObservationComponent = get_fhir_model_from_field(Observation.model_fields.get('component'))


class TestRoot(TestCase):

    def setUp(self):
        self.resource = Observation.model_construct(status='final', identifier=[Identifier(value='A'), Identifier(value='B')])
        self.collection = [FHIRPathCollectionItem(self.resource, path=Root())]
    
    def test_element_evaluates_correctly(self):
        result = Root().evaluate(self.resource)
        assert len(result) == 1         
        assert result[0].value == self.resource 
        assert result[0].parent is None         
                          

class TestElement(TestCase):

    def setUp(self):
        self.resource = Observation.model_construct(status='final', identifier=[Identifier(value='A'), Identifier(value='B')])
        self.collection = [FHIRPathCollectionItem(self.resource, path=Root())]
    
    def test_element_evaluates_correctly(self):
        result = Element('status').evaluate(self.collection, create=False)
        assert len(result) == 1
        assert result[0].value == 'final'                
             
    def test_element_creates_missing_primitive_element(self):
        result = Element('valueString').evaluate(self.collection, create=True)
        assert len(result) == 1
        assert result[0].value is None
        assert hasattr(self.resource, 'valueString') 
        
    def test_element_creates_missing_complex_element(self):
        result = Element('valueCodeableConcept').evaluate(self.collection, create=True)
        assert len(result) == 1
        assert result[0].value == CodeableConcept.model_construct()
        assert self.resource.valueCodeableConcept == result[0].value
        
    def test_element_creates_missing_complex_list_element(self):
        result = Element('component').evaluate(self.collection, create=True)
        assert len(result) == 1
        assert result[0].value == ObservationComponent.model_construct()
        assert self.resource.component == [result[0].value]
        
    def test_element_evaluate_element_with_list(self):
        result = Element('identifier').child(Element('value')).evaluate(self.collection, create=False)
        assert len(result) == 2
        assert result[0].value == 'A'
        assert result[1].value == 'B'
        
    def test_element_update_element_with_list(self):
        Element('identifier').child(Element('value')).update(self.collection, value='C')
        assert self.resource.identifier[0].value == 'C'
        assert self.resource.identifier[1].value == 'C'
             


observation = Observation(**{
    "resourceType": "Observation",
    "status": "final", 
    "code": {
        "coding": [{"code": "C1"}],
    }, 
    "identifier": [{
        "system": "id_system",
        "use": "oficial",
        "value": "123",
    },{
        "system": "id_system",
        "use": "oficial",
        "value": "456",
    },{
        "system": "id_system",
        "use": "oficial",
        "value": "789",
    }],
    "valueInteger": 5,
    "extension": [
        {
            "url": "http://domain.org/extension-1",
            "extension": [
                {
                    "url": "http://domain.org/extension-2",
                    "valueString": "extension-value-2"
                }
            ]
        },
    ],
    "component": [
        {
            "code": {
                "coding": [{
                    "code": "component-1",
                    "system": "https://system.org"
                }]
            },
            "valueString": "component-1-value-1"
        },
        {
            "code": {
                "coding": [{
                    "code": "component-1",
                    "system": "https://system.org"
                }]
            },
            "valueString": "component-1-value-2"
        },
        {
            "code": {
                "coding": [{
                    "code": "component-2",
                    "system": "https://system.org"
                }]
            },
            "valueCodeableConcept": {
                "coding": [{
                    "code": "component-2-code",
                    "system": "https://system.org"
                }]
            },
        }
    ]
})

# ======== Invocation - FHIRPath ============
#               Find                        
# ======================================
fhirpath_child_find_test_cases = (
    (Invocation(Root(), Element("status")), observation.status),
    (Invocation(Root(), Element("identifier")), observation.identifier),
    (Invocation(Invocation(Root(), Element("identifier")), Element("value")), [id.value for id in observation.identifier]),
)
    
@pytest.mark.parametrize("path_object, expected_value", fhirpath_child_find_test_cases)
def test_fhirpath_child_find(path_object, expected_value):
    expected_values = ensure_list(expected_value)
    collection = path_object.find(observation)
    found_values = [item.value for item in collection]
    assert len(found_values) == len(expected_values)
    for value, expected in zip(found_values, expected_values):
        assert value == expected

# ======== Invocation - FHIRPath ============
#           Update & Create                        
# ======================================

fhirpath_child_update_test_cases = (
    # Update
    (Invocation(Root(), Element("status")), "pending", lambda obs: obs.status),
    (Invocation(Invocation(Root(), Element("identifier")), Index(0)), observation.identifier[0], lambda obs: obs.identifier[0]),
    # Create
    (Invocation(Root(), Element("id")), "ID12345", lambda obs: obs.id),    
    (Invocation(Invocation(Root(), Element("subject")), Element("reference")), "subjectX", lambda obs: obs.subject.reference),
)        

@pytest.mark.parametrize("path_object, update_value, getattr_fcn", fhirpath_child_update_test_cases)
def test_fhirpath_child_update(path_object, update_value, getattr_fcn):
    new_observation = observation.model_copy(deep=True)
    path_object.update_or_create(new_observation, update_value)
    assert getattr_fcn(new_observation) == update_value
    


# ======== Index - FHIRPath ============
#               Find                        
# ======================================
fhirpath_index_find_test_cases = (
    # Update
    (Invocation(Invocation(Root(), Element("identifier")), Index(0)), observation.identifier[0]),
    (Invocation(Invocation(Invocation(Root(), Element("identifier")), Index(0)), Element("value")), observation.identifier[0].value),
    # Create
    (Invocation(Invocation(Root(), Element("identifier")), Index(0)), observation.identifier[0]),
    (Invocation(Invocation(Invocation(Root(), Element("identifier")), Index(0)), Element("value")), observation.identifier[0].value),
)
    
@pytest.mark.parametrize("path_object, expected_value", fhirpath_index_find_test_cases)
def test_fhirpath_index_find(path_object, expected_value):
    expected_values = ensure_list(expected_value)
    collection = path_object.find(observation)
    found_values = [item.value for item in collection]
    assert len(found_values) == len(expected_values)
    for value, expected in zip(found_values, expected_values):
        assert value == expected

        

# ======== Index - FHIRPath ============
#           Update & Create                        
# ======================================

fhirpath_index_update_test_cases = (
    (Invocation(Invocation(Root(), Element("identifier")), Index(0)), observation.identifier[1], lambda obs: obs.identifier[0]),
    (Invocation(Invocation(Invocation(Root(), Element("identifier")), Index(0)), Element("value")), "ABC123", lambda obs: obs.identifier[0].value),
    (Invocation(Invocation(Root(), Element("identifier")), Index(4)), observation.identifier[1], lambda obs: obs.identifier[4]),
    (Invocation(Invocation(Invocation(Root(), Element("identifier")), Index(4)), Element("value")), "ABC123", lambda obs: obs.identifier[4].value),
)        

@pytest.mark.parametrize("path_object, update_value, getattr_fcn", fhirpath_index_update_test_cases)
def test_fhirpath_index_update(path_object, update_value, getattr_fcn):
    new_observation = observation.model_copy(deep=True)
    path_object.update_or_create(new_observation, update_value)
    assert getattr_fcn(new_observation) == update_value
    
    
    
fhirpath_find_test_cases = (
    ("Observation.valueInteger", observation, 5),
    ("Observation.valueInteger.single()", observation, 5),
    ("Observation.identifier.value[1]", observation, "456"),
    ("Observation.identifier[1].value", observation, "456"),
    ("Observation.identifier.value", observation, ["123","456","789"]),
    ("Observation.identifier.first().value", observation, "123"),
    ("Observation.identifier.last().value", observation, "789"),
    ("Observation.identifier.skip(2).value", observation, "789"),
    ("Observation.identifier.take(1).value", observation, "123"),
    ("Observation.extension('http://domain.org/extension-1').extension('http://domain.org/extension-2').valueString", observation, "extension-value-2"),
    ("Observation.component.where(code.coding.code='component-1')[0].value[x]", observation, "component-1-value-1"),
    ("Observation.component.where(code.coding.code='component-1')[0].valueString", observation, "component-1-value-1"),
    ("Observation.component.where(code.coding.code='component-1')[1].valueString", observation, "component-1-value-2"),
    ("Observation.component.where(code.coding.system='https://system.org').where(code.coding.code='component-2').valueCodeableConcept.coding.code", observation, "component-2-code"),
)

@pytest.mark.parametrize("path_string, data_object, expected_value", fhirpath_find_test_cases)
def test_fhirpath_find(path_string, data_object, expected_value):
    expected_values = ensure_list(expected_value)
    collection = parse(path_string).find(data_object)
    found_values = [item.value for item in collection]
    assert len(found_values) == len(expected_values)
    for value, expected in zip(found_values, expected_values):
        assert value == expected

        


fhirpath_update_test_cases = (
    ("Observation.valueInteger", 12, lambda obs: obs.valueInteger),
    ("Observation.identifier[0].value", "456", lambda obs: obs.identifier[0].value),
    ("Observation.identifier[1].system", "home", lambda obs: obs.identifier[1].system),
    ("Observation.identifier[4].value", "123", lambda obs: obs.identifier[4].value),
    ("Observation.identifier.first().value", "123", lambda obs: obs.identifier[0].value),
    ("Observation.identifier.last().value", "789", lambda obs: obs.identifier[-1].value),
    ("Observation.extension[0].extension[2].valueString", "testvalue", lambda obs: obs.extension[0].extension[2].valueString),
)

@pytest.mark.parametrize("path_string, update_value, getattr_fcn", fhirpath_update_test_cases)
def test_fhirpath_update_existing(path_string, update_value, getattr_fcn):
    _observation = observation.model_copy(deep=True)
    parse(path_string).update_or_create(_observation, update_value)
    assert getattr_fcn(_observation) == update_value
