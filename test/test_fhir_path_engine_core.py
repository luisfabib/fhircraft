import pytest

from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, FHIRPathError, Child, Root, Element, Index
from fhircraft.fhir.path.parser import parse
from fhircraft.utils import ensure_list
from  fhir.resources.R4B.observation import Observation, ObservationComponent
from  fhir.resources.R4B.coding import Coding 
from  fhir.resources.R4B.codeableconcept import CodeableConcept 
from  fhir.resources.R4B.identifier import Identifier 
from fhir.resources.R4B.fhirtypesvalidators import get_fhir_model_class
from unittest import TestCase
from collections import namedtuple



class TestRoot(TestCase):

    def setUp(self):
        self.resource = Observation.construct(status='final', identifier=[Identifier(value='A'), Identifier(value='B')])
        self.collection = [FHIRPathCollectionItem(self.resource, path=Root())]
    
    def test_element_evaluates_correctly(self):
        result = Root().evaluate(self.resource)
        assert len(result) == 1         
        assert result[0].value == self.resource 
        assert result[0].parent is None         
                          

class TestElement(TestCase):

    def setUp(self):
        self.resource = Observation.construct(status='final', identifier=[Identifier(value='A'), Identifier(value='B')])
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
        assert result[0].value == CodeableConcept.construct()
        assert self.resource.valueCodeableConcept == result[0].value
        
    def test_element_creates_missing_complex_list_element(self):
        result = Element('component').evaluate(self.collection, create=True)
        assert len(result) == 1
        assert result[0].value == ObservationComponent.construct()
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
             
        
class TestIndexPrimitive(TestCase):

    def setUp(self):
        TestResource = namedtuple('TestResource', 'field')
        self.resource = TestResource(field=[1, 2, 3])
        parent = FHIRPathCollectionItem(self.resource, path=Root())
        self.collection = Element('field').find(parent)
    
    def test_index_evaluates_correctly(self):
        result = Index(2).evaluate(self.collection, create=False)
        assert len(result) == 1
        assert result[0].value == 3
        assert len(self.resource.field) == 3

    def test_index_creates_missing_elements(self):
        result = Index(5).evaluate(self.collection, create=True)
        assert len(result) == 1
        assert result[0].value is None
        assert len(self.resource.field) == 6

    def test_index_does_not_modify_collection_out_of_bounds(self):
        result = Index(10).evaluate(self.collection, create=False)
        assert len(result) == 0
        assert len(self.resource.field) == 3

    def test_index_updates_value(self):
        Index(2).update(self.collection, value='value')
        assert len(self.resource.field) == 3
        assert self.resource.field[2] == 'value'

    def test_index_updates_and_creates_value(self):
        Index(10).update_or_create(self.collection, value='value')
        assert len(self.resource.field) == 11
        assert self.resource.field[10] == 'value'

    def test_index_handles_negative_indices(self):
        result = Index(-1).evaluate(self.collection, create=False)
        assert len(result) == 1
        assert result[0].value == 3        
        assert len(self.resource.field) == 3

    def test_index_handles_non_integer_indices(self):
        with pytest.raises(FHIRPathError):
            Index("a")
            


class TestIndexResources(TestCase):

    def setUp(self):
        self.resource = CodeableConcept(coding=[
            Coding(code='code-1',system='system-1'),
            Coding(code='code-2',system='system-2'),
            Coding(code='code-3',system='system-3'),
        ])
        parent = FHIRPathCollectionItem(self.resource, path=Root())
        self.collection = Element('coding').find(parent)
    
    def test_index_evaluates_correctly(self):
        result = Index(2).evaluate(self.collection, create=False)
        assert len(result) == 1
        assert result[0].value == Coding(code='code-3',system='system-3')
        assert len(self.resource.coding) == 3

    def test_index_creates_missing_elements(self):
        result = Index(5).evaluate(self.collection, create=True)
        assert len(result) == 1
        assert result[0].value == Coding.construct()
        assert len(self.resource.coding) == 6

    def test_index_does_not_modify_collection_out_of_bounds(self):
        result = Index(10).evaluate(self.collection, create=False)
        assert len(result) == 0
        assert len(self.resource.coding) == 3

    def test_index_updates_value(self):
        Index(2).update(self.collection, value=Coding(code='code-5',system='system-5'))
        assert len(self.resource.coding) == 3
        assert self.resource.coding[2] == Coding(code='code-5',system='system-5')

    def test_index_updates_and_creates_value(self):
        Index(10).update_or_create(self.collection, value=Coding(code='code-5',system='system-5'))
        assert len(self.resource.coding) == 11
        assert self.resource.coding[10] == Coding(code='code-5',system='system-5')

    def test_index_evaluates_by_reference(self):
        Index(1).child(Element('code')).evaluate(self.collection, create=False)[0].set_value('code-999')
        assert len(self.resource.coding) == 3
        assert self.resource.coding[1].code == 'code-999'

    def test_index_creates_with_empty_list(self):
        resource = CodeableConcept(coding=[])
        parent = FHIRPathCollectionItem(resource, path=Root())
        collection = Element('coding').evaluate(parent, create=True)
        Index(0).evaluate(collection, create=True)
        assert len(resource.coding) == 1
        assert resource.coding == [Coding.construct()]



observation = Observation(**{
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
    "fhir_comments":"Commenting",
    "extension": [
        {
            "url": "http://domain.org/extension-1",
            "valueString": "extension-value-1",
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

# ======== Child - FHIRPath ============
#               Find                        
# ======================================
fhirpath_child_find_test_cases = (
    (Child(Root(), Element("status")), observation.status),
    (Child(Root(), Element("identifier")), observation.identifier),
    (Child(Child(Root(), Element("identifier")), Element("value")), [id.value for id in observation.identifier]),
)
    
@pytest.mark.parametrize("path_object, expected_value", fhirpath_child_find_test_cases)
def test_fhirpath_child_find(path_object, expected_value):
    expected_values = ensure_list(expected_value)
    collection = path_object.find(observation)
    found_values = [item.value for item in collection]
    assert len(found_values) == len(expected_values)
    for value, expected in zip(found_values, expected_values):
        assert value == expected

# ======== Child - FHIRPath ============
#           Update & Create                        
# ======================================

fhirpath_child_update_test_cases = (
    # Update
    (Child(Root(), Element("status")), "pending", lambda obs: obs.status),
    (Child(Child(Root(), Element("identifier")), Index(0)), observation.identifier[0], lambda obs: obs.identifier[0]),
    # Create
    (Child(Root(), Element("id")), "ID12345", lambda obs: obs.id),    
    (Child(Child(Root(), Element("subject")), Element("reference")), "subjectX", lambda obs: obs.subject.reference),
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
    (Child(Child(Root(), Element("identifier")), Index(0)), observation.identifier[0]),
    (Child(Child(Child(Root(), Element("identifier")), Index(0)), Element("value")), observation.identifier[0].value),
    # Create
    (Child(Child(Root(), Element("identifier")), Index(0)), observation.identifier[0]),
    (Child(Child(Child(Root(), Element("identifier")), Index(0)), Element("value")), observation.identifier[0].value),
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
    (Child(Child(Root(), Element("identifier")), Index(0)), observation.identifier[1], lambda obs: obs.identifier[0]),
    (Child(Child(Child(Root(), Element("identifier")), Index(0)), Element("value")), "ABC123", lambda obs: obs.identifier[0].value),
    (Child(Child(Root(), Element("identifier")), Index(4)), observation.identifier[1], lambda obs: obs.identifier[4]),
    (Child(Child(Child(Root(), Element("identifier")), Index(4)), Element("value")), "ABC123", lambda obs: obs.identifier[4].value),
)        

@pytest.mark.parametrize("path_object, update_value, getattr_fcn", fhirpath_index_update_test_cases)
def test_fhirpath_index_update(path_object, update_value, getattr_fcn):
    new_observation = observation.copy(deep=True)
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
    ("Observation.fhir_comments", observation, "Commenting"),
    ("Observation.extension('http://domain.org/extension-1').valueString", observation, "extension-value-1"),
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
    ("Observation.fhir_comments", "Commenting", lambda obs: obs.fhir_comments),
    ("Observation.extension[0].extension[2].valueString", "testvalue", lambda obs: obs.extension[0].extension[2].valueString),
)

@pytest.mark.parametrize("path_string, update_value, getattr_fcn", fhirpath_update_test_cases)
def test_fhirpath_update_existing(path_string, update_value, getattr_fcn):
    _observation = observation.copy(deep=True)
    parse(path_string).update_or_create(_observation, update_value)
    assert getattr_fcn(_observation) == update_value


fhirpath_create_test_cases = (
    ("Observation.valueInteger", 12, lambda obs: obs.valueInteger),
    ("Observation.identifier[0].value", "456", lambda obs: obs.identifier[0].value),
    ("Observation.identifier[1].value", "456", lambda obs: obs.identifier[1].value),
    ("Observation.identifier.first().value", "123", lambda obs: obs.identifier[0].value),
    ("Observation.identifier.last().value", "789", lambda obs: obs.identifier[-1].value),
    ("Observation.fhir_comments", "Commenting", lambda obs: obs.fhir_comments),
    ("Observation.extension.extension.valueString", "testvalue", lambda obs: obs.extension[0].extension[2].valueString),
    ("Patient.contact[0].telecom[0].value", "teletest", lambda pat: pat.contact[0].telecom[0].value),
    ("Patient.contact.telecom[1].use", "home", lambda pat: pat.contact[0].telecom[1].use),
    ("Patient.name[0].given[0]", "John", lambda pat: pat.name[0].given[0]),
)

@pytest.mark.parametrize("path_string, update_value, getattr_fcn", fhirpath_update_test_cases)
def test_fhirpath_create(path_string, update_value, getattr_fcn):
    Observation.Config.validate_assignment = False
    new_resource = get_fhir_model_class(path_string.split(".",1)[0]).construct()
    parse(path_string).update_or_create(new_resource, update_value)
    print(new_resource.json(indent=3))
    assert getattr_fcn(new_resource) == update_value