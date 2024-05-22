
# Generated by CodiumAI
from fhiropenapi.fhirpath import FHIRPathNavigator
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.extension import Extension
import pytest 

class TestFHIRPathNavigator:

    # Navigate to a valid direct attribute of the FHIR resource
    def test_navigate_to_valid_attribute(self):
        patient = Patient(id="1234")
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value("Patient.id")
        assert result == "1234", "Failed to navigate to valid attribute 'id'"

    # Attempt to navigate to a non-existent attribute
    def test_navigate_to_non_existent_attribute(self):
        patient = Patient(id="1234")
        navigator = FHIRPathNavigator(patient)
        with pytest.raises(KeyError):
            navigator.get_value("non_existent_attribute")
        
    def test_set_value_valid_direct_attribute(self):
        patient = Patient(id="1234")
        navigator = FHIRPathNavigator(patient)
        result = navigator.set_value("Patient.id", "5678")
        assert patient.id == "5678", "Failed to set value of valid direct attribute 'id'"

    def test_navigate_valid_nested_path(self):
        patient = Patient(name=[HumanName(text="John Doe")])
        navigator = FHIRPathNavigator(patient)
        result = navigator.navigate("Patient.name.0.text")
        assert result == "John Doe", "Failed to navigate through valid nested path 'name.0.text'"

    def test_navigate_list(self):
        patient = Patient(name=[HumanName(text="John Doe"), HumanName(text="Will Smith")])
        navigator = FHIRPathNavigator(patient)
        result = navigator.navigate("Patient.name.0.text")
        assert result == "John Doe", "Failed to navigate through valid nested path 'name.0.text'"
        result = navigator.navigate("Patient.name.1.text")
        assert result == "Will Smith", "Failed to navigate through valid nested path 'name.1.text'"

    def test_navigate_extension(self):
        patient = Patient(id="1234")
        patient.extension = [Extension(url='http://example.com/ext', valueString='test_value')]
        navigator = FHIRPathNavigator(patient)
        result = navigator.get_value('Patient.extension("http://example.com/ext")')
        assert result.valueString == 'test_value', "Failed to navigate to the correct extension."
    
    def test_set_extension(self):
        patient = Patient(id="1234")
        patient.extension = [Extension(url='http://example.com/ext', valueString='test_value')]
        navigator = FHIRPathNavigator(patient)
        navigator.set_value('Patient.extension("http://example.com/ext").valueString', 'test_value_new')
        assert patient.extension[0].valueString == 'test_value_new', "Failed to set value to the correct extension."
    
    def test_navigate_complex_extension(self):
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
    
    def test_navigate_where(self):
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