
# Generated by CodiumAI
from fhir_openapi.path import FHIRPathNavigator
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.extension import Extension
from collections import namedtuple
import pytest 

class TestFHIRPathNavigator:

    # Navigate to a valid direct attribute of the FHIR resource
    def test_get_single_valued_element(self):
        value = "1234"
        patient = Patient(id=value)
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value("Patient.id")
        assert result == value
        
    def test_get_multiple_valued_element(self):
        values = [HumanName(text="John Doe"), HumanName(text="Will Smith")]
        patient = Patient(name=values)
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value("Patient.name")
        assert result == values

    def test_navigate_without_resource_type(self):
        patient = Patient(id="1234")
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value("id")
        assert result == "1234"

    def test_set_single_valued_element(self):
        new_value = "5678"
        patient = Patient(id="1234")
        navigator = FHIRPathNavigator(patient)
        navigator.set_value("Patient.id", new_value)
        assert patient.id == new_value

    def test_set_multiple_valued_element(self):
        new_values = [HumanName(text="John Doe"), HumanName(text="Will Smith")]
        patient = Patient()
        navigator = FHIRPathNavigator(patient)
        navigator.set_value("Patient.name", new_values)
        assert patient.name == new_values

    def test_get_union(self):
        values = [HumanName(text="John Doe"), HumanName(text="Will Smith")]
        patient = Patient(name=values)
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value("Patient.name.0 | Patient.name.1")
        assert result == values

    def test_set_union(self):
        new_value = "Johnny Smith"
        patient = Patient(name=[HumanName(text="John Doe"), HumanName(text="Will Smith")])
        navigator = FHIRPathNavigator(patient)
        navigator.set_value("Patient.name.0.text | Patient.name.1.text", new_value)
        assert patient.name[0].text == new_value
        assert patient.name[1].text == new_value

    def test_get_list_item(self):
        patient = Patient(name=[HumanName(text="John Doe"), HumanName(text="Will Smith")])
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value("Patient.name.item(0).text")
        assert result == "John Doe", "Failed to navigate through valid nested path 'name.0.text'"
        result = navigator.get_value("Patient.name.item(1).text")
        assert result == "Will Smith"
        
    def test_get_list_item_by_index(self):
        patient = Patient(name=[HumanName(text="John Doe"), HumanName(text="Will Smith")])
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value("Patient.name.0.text")
        assert result == "John Doe"
        result = navigator.get_value("Patient.name.1.text")
        assert result == "Will Smith"

    def test_get_extension(self):
        patient = Patient(id="1234")
        patient.extension = [Extension(url='http://example.com/ext', valueString='test_value')]
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value('Patient.extension("http://example.com/ext")')
        assert result.valueString == 'test_value'
    
    def test_set_extension(self):
        patient = Patient(id="1234")
        patient.extension = [Extension(url='http://example.com/ext', valueString='test_value')]
        navigator = FHIRPathNavigator(patient)
        navigator.set_value('Patient.extension("http://example.com/ext").valueString', 'test_value_new')
        assert patient.extension[0].valueString == 'test_value_new'
    
    def test_get_complex_extension(self):
        patient = Patient(id="1234")
        patient.extension = [Extension(url='http://example.com/ext', valueString='test_value', extension=[Extension(url='http://example.com/ext2', valueString='test_value_2')])]
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value('Patient.extension("http://example.com/ext").extension("http://example.com/ext2")')
        assert result.valueString == 'test_value_2', "Failed to navigate to the correct complex extension."
    
    def test_set_complex_extension(self):
        patient = Patient(id="1234")
        patient.extension = [Extension(url='http://example.com/ext', valueString='test_value', extension=[Extension(url='http://example.com/ext2', valueString='test_value_2')])]
        navigator = FHIRPathNavigator(patient)
        navigator.set_value('Patient.extension("http://example.com/ext").extension("http://example.com/ext2").valueString', 'test_value_2_new')
        assert patient.extension[0].extension[0].valueString == 'test_value_2_new', "Failed to set value to the complex extension."
    
    def test_get_where(self):
        # Mocking a FHIR resource with a list of objects
        patient = Patient(name=[HumanName(family="Doe", given=["John"]), HumanName(family="Smith", given=["Will"])])
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value('Patient.name.where(family="Doe")')
        assert result.given[0] == "John", "Failed to filter items correctly with where statement."
        result = navigator.get_value('Patient.name.where(family="Smith")')
        assert result.given[0] == "Will", "Failed to filter items correctly with where statement."
        
    def test_set_where(self):
        # Mocking a FHIR resource with a list of objects
        patient = Patient(name=[HumanName(family="Doe", given=["John"]), HumanName(family="Smith", given=["Will"])])
        navigator = FHIRPathNavigator(patient)
        navigator.set_value('Patient.name.where(family="Doe").given',["Johnny"])
        assert patient.name[0].given[0] == "Johnny", "Failed to set the value of the filter item correctly with where statement."
        navigator.set_value('Patient.name.where(family="Smith").given',["Willy"])
        assert patient.name[1].given[0] == "Willy", "Failed to set the value of the filter item correctly with where statement."
        
        
    def test_navigate_type_choice(self):
        # Mocking a FHIR resource with a list of objects
        patient = Patient(deceasedBoolean=True)
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value('Patient.deceased[x]')
        assert result == True
        


class Test_SplitPath:

    def test_split_simple_paths(self):
        navigator = FHIRPathNavigator(fhir_resource={})
        result = navigator._split_path("patient.name.family")
        assert result == ["patient", "name", "family"]

    def test_handle_multiple_segments(self):
        navigator = FHIRPathNavigator(fhir_resource={})
        result = navigator._split_path("patient.name.family.given")
        assert result == ["patient", "name", "family", "given"]

    def test_return_list_of_segments(self):
        navigator = FHIRPathNavigator(fhir_resource={})
        result = navigator._split_path("patient.name.family")
        assert isinstance(result, list)

    def test_handle_nested_functions(self):
        navigator = FHIRPathNavigator(fhir_resource={})
        result = navigator._split_path("patient.name.family.where(family='Smith').given")
        assert result == ["patient", "name", "family", "where(family='Smith')", "given"]

    def test_split_paths_with_dots_in_quotes(self):
        navigator = FHIRPathNavigator(fhir_resource={})
        result = navigator._split_path("patient.name.family.where(family='Smith.Jones').given")
        assert result == ["patient", "name", "family", "where(family='Smith.Jones')", "given"]

    def test_empty_input_returns_empty_list(self):
        navigator = FHIRPathNavigator(fhir_resource={})
        result = navigator._split_path("")
        assert result == ['']
        


class Test_SetValueAtPath:

    def test_set_new_value_on_all_elements(self):
        navigator = FHIRPathNavigator({'resource_type': 'TestResource'})
        collection = [type('TestObj', (object,), {'attr': 1})(), type('TestObj', (object,), {'attr': 2})()]
        navigator._set_value_at_path(collection, 'attr', 99)
        assert all(obj.attr == 99 for obj in collection)

    def test_update_multiple_elements_with_same_value(self):
        navigator = FHIRPathNavigator({'resource_type': 'TestResource'})
        collection = [type('TestObj', (object,), {'attr': 1})(), type('TestObj', (object,), {'attr': 2})()]
        navigator._set_value_at_path(collection, 'attr', 77)
        assert all(obj.attr == 77 for obj in collection)

    def test_apply_changes_to_complex_objects(self):
        navigator = FHIRPathNavigator({'resource_type': 'TestResource'})
        complex_obj = type('ComplexObj', (object,), {'nested_attr': {'inner_attr': 10}})()
        collection = [complex_obj]        
        navigator._set_value_at_path(collection, 'nested_attr', {'inner_attr': 20})
        assert complex_obj.nested_attr['inner_attr'] == 20

    def test_empty_collection_no_change(self):
        navigator = FHIRPathNavigator({'resource_type': 'TestResource'})
        collection = []
        navigator._set_value_at_path(collection, 'attr', 99)
        assert len(collection) == 0

    # fhir_path_segment is an invalid Python attribute name
    def test_invalid_attribute_name_error(self):
        navigator = FHIRPathNavigator({'resource_type': 'TestResource'})
        obj = type('TestObj', (object,), {})()
        collection = [obj]
        with pytest.raises(AttributeError):
            navigator._set_value_at_path(collection, '123invalid', 99)
            