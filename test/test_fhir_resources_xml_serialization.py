import pytest
from xml.etree import ElementTree as ET
from fhircraft.fhir.resources.base import FHIRBaseModel
from pydantic import Field
from typing import Optional, List

# FHIR namespace
FHIR_NS = '{http://hl7.org/fhir}'


def strip_ns(tag):
    """Strip namespace from tag for easier testing."""
    return tag.split('}')[-1] if '}' in tag else tag


class SimplePatient(FHIRBaseModel):
    """Simple Patient model for testing basic XML serialization."""
    resourceType: str = Field(default="Patient")
    id: Optional[str] = None
    active: Optional[bool] = None
    gender: Optional[str] = None
    birthDate: Optional[str] = None


class TestBasicXMLSerialization:
    """Test basic XML serialization functionality."""

    def test_simple_resource_xml(self):
        """Test XML serialization of a simple resource with primitive fields."""
        patient = SimplePatient(
            id="example",
            active=True,
            gender="male",
            birthDate="1974-12-25"
        )
        
        xml_output = patient.model_dump_xml(pretty=False)
        
        # Parse the XML
        root = ET.fromstring(xml_output)
        
        # Verify root element (with namespace)
        assert strip_ns(root.tag) == "Patient"
        assert FHIR_NS in root.tag  # namespace should be present
        
        # Verify child elements using namespace
        id_elem = root.find(f'{FHIR_NS}id')
        assert id_elem is not None
        assert id_elem.get('value') == "example"
        
        active_elem = root.find(f'{FHIR_NS}active')
        assert active_elem is not None
        assert active_elem.get('value') == "true"
        
        gender_elem = root.find(f'{FHIR_NS}gender')
        assert gender_elem is not None
        assert gender_elem.get('value') == "male"
        
        birthDate_elem = root.find(f'{FHIR_NS}birthDate')
        assert birthDate_elem is not None
        assert birthDate_elem.get('value') == "1974-12-25"

    def test_xml_with_none_values(self):
        """Test that None values are excluded from XML output."""
        patient = SimplePatient(
            id="example",
            active=True
            # gender and birthDate are None
        )
        
        xml_output = patient.model_dump_xml(pretty=False)
        root = ET.fromstring(xml_output)
        
        # Verify only non-None fields are present
        assert root.find(f'{FHIR_NS}id') is not None
        assert root.find(f'{FHIR_NS}active') is not None
        assert root.find(f'{FHIR_NS}gender') is None
        assert root.find(f'{FHIR_NS}birthDate') is None

    def test_xml_pretty_printing(self):
        """Test that pretty printing formats XML correctly."""
        patient = SimplePatient(
            id="example",
            active=True,
            gender="female"
        )
        
        xml_output = patient.model_dump_xml(pretty=True)
        
        # Pretty printed XML should contain newlines and indentation
        assert '\n' in xml_output
        assert '  ' in xml_output  # indentation
        
        # Should still be valid XML
        root = ET.fromstring(xml_output)
        assert strip_ns(root.tag) == "Patient"

    def test_xml_namespace(self):
        """Test that FHIR namespace is correctly added."""
        patient = SimplePatient(id="example")
        xml_output = patient.model_dump_xml(pretty=False)
        root = ET.fromstring(xml_output)
        
        # Namespace should be in the tag
        assert FHIR_NS in root.tag
        # Or check that xmlns is in the serialized XML string
        assert 'xmlns="http://hl7.org/fhir"' in xml_output


class MockHumanName(FHIRBaseModel):
    """Mock HumanName for testing complex types."""
    use: Optional[str] = None
    family: Optional[str] = None
    given: Optional[List[str]] = None


class MockAddress(FHIRBaseModel):
    """Mock Address for testing complex types."""
    use: Optional[str] = None
    line: Optional[List[str]] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None


class PatientWithComplexTypes(FHIRBaseModel):
    """Patient with complex types for testing."""
    resourceType: str = Field(default="Patient")
    id: Optional[str] = None
    name: Optional[List[MockHumanName]] = None
    address: Optional[List[MockAddress]] = None


class TestComplexTypeXMLSerialization:
    """Test XML serialization of complex types and nested structures."""

    def test_complex_type_serialization(self):
        """Test serialization of resources with complex types."""
        patient = PatientWithComplexTypes(
            id="example",
            name=[
                MockHumanName(
                    use="official",
                    family="Chalmers",
                    given=["Peter", "James"]
                )
            ]
        )
        
        xml_output = patient.model_dump_xml(pretty=False)
        root = ET.fromstring(xml_output)
        
        # Verify name element
        name_elem = root.find(f'{FHIR_NS}name')
        assert name_elem is not None
        
        # Verify nested elements
        use_elem = name_elem.find(f'{FHIR_NS}use')
        assert use_elem is not None
        assert use_elem.get('value') == "official"
        
        family_elem = name_elem.find(f'{FHIR_NS}family')
        assert family_elem is not None
        assert family_elem.get('value') == "Chalmers"
        
        # Verify list of primitives (given names)
        given_elems = name_elem.findall(f'{FHIR_NS}given')
        assert len(given_elems) == 2
        assert given_elems[0].get('value') == "Peter"
        assert given_elems[1].get('value') == "James"

    def test_multiple_complex_types(self):
        """Test serialization with multiple instances of complex types."""
        patient = PatientWithComplexTypes(
            id="example",
            name=[
                MockHumanName(use="official", family="Chalmers"),
                MockHumanName(use="maiden", family="Windsor")
            ]
        )
        
        xml_output = patient.model_dump_xml(pretty=False)
        root = ET.fromstring(xml_output)
        
        # Should have two name elements
        name_elems = root.findall(f'{FHIR_NS}name')
        assert len(name_elems) == 2
        
        # Verify each name
        assert name_elems[0].find(f'{FHIR_NS}use').get('value') == "official"
        assert name_elems[0].find(f'{FHIR_NS}family').get('value') == "Chalmers"
        
        assert name_elems[1].find(f'{FHIR_NS}use').get('value') == "maiden"
        assert name_elems[1].find(f'{FHIR_NS}family').get('value') == "Windsor"

    def test_nested_complex_types(self):
        """Test deeply nested complex types."""
        patient = PatientWithComplexTypes(
            id="example",
            address=[
                MockAddress(
                    use="home",
                    line=["534 Erewhon St"],
                    city="PleasantVille",
                    state="Vic",
                    postalCode="3999"
                )
            ]
        )
        
        xml_output = patient.model_dump_xml(pretty=False)
        root = ET.fromstring(xml_output)
        
        address_elem = root.find(f'{FHIR_NS}address')
        assert address_elem is not None
        
        # Verify nested primitives
        use_elem = address_elem.find(f'{FHIR_NS}use')
        assert use_elem is not None
        assert use_elem.get('value') == "home"
        
        # Verify list within complex type
        line_elem = address_elem.find(f'{FHIR_NS}line')
        assert line_elem is not None
        assert line_elem.get('value') == "534 Erewhon St"
        
        city_elem = address_elem.find(f'{FHIR_NS}city')
        assert city_elem is not None
        assert city_elem.get('value') == "PleasantVille"


class TestBooleanSerialization:
    """Test boolean value serialization in XML."""

    def test_boolean_true_lowercase(self):
        """Test that boolean true is serialized as 'true' (lowercase)."""
        patient = SimplePatient(id="test", active=True)
        xml_output = patient.model_dump_xml(pretty=False)
        root = ET.fromstring(xml_output)
        
        active_elem = root.find(f'{FHIR_NS}active')
        assert active_elem.get('value') == "true"  # lowercase, not "True"

    def test_boolean_false_lowercase(self):
        """Test that boolean false is serialized as 'false' (lowercase)."""
        patient = SimplePatient(id="test", active=False)
        xml_output = patient.model_dump_xml(pretty=False)
        root = ET.fromstring(xml_output)
        
        active_elem = root.find(f'{FHIR_NS}active')
        assert active_elem.get('value') == "false"  # lowercase, not "False"


class TestEmptyResource:
    """Test XML serialization of empty or minimal resources."""

    def test_resource_with_only_type(self):
        """Test serialization of resource with only resourceType."""
        patient = SimplePatient()
        xml_output = patient.model_dump_xml(pretty=False)
        root = ET.fromstring(xml_output)
        
        # Should have root element with namespace
        assert strip_ns(root.tag) == "Patient"
        assert FHIR_NS in root.tag
        
        # Should have no child elements (all fields are None)
        assert len(list(root)) == 0


class TestXMLValidation:
    """Test that generated XML is well-formed."""

    def test_xml_is_well_formed(self):
        """Test that generated XML can be parsed without errors."""
        patient = PatientWithComplexTypes(
            id="example",
            name=[
                MockHumanName(
                    use="official",
                    family="Chalmers",
                    given=["Peter", "James"]
                )
            ],
            address=[
                MockAddress(
                    use="home",
                    line=["534 Erewhon St", "Apt 42"],
                    city="PleasantVille"
                )
            ]
        )
        
        xml_output = patient.model_dump_xml(pretty=True)
        
        # Should parse without errors
        try:
            root = ET.fromstring(xml_output)
            assert root is not None
        except ET.ParseError as e:
            pytest.fail(f"Generated XML is not well-formed: {e}")

    def test_xml_roundtrip_structure(self):
        """Test that XML maintains structure through serialization."""
        patient = SimplePatient(
            id="test-123",
            active=True,
            gender="other",
            birthDate="2000-01-01"
        )
        
        xml_output = patient.model_dump_xml(pretty=False)
        root = ET.fromstring(xml_output)
        
        # Verify all fields are present in XML
        assert root.find(f'{FHIR_NS}id').get('value') == "test-123"
        assert root.find(f'{FHIR_NS}active').get('value') == "true"
        assert root.find(f'{FHIR_NS}gender').get('value') == "other"
        assert root.find(f'{FHIR_NS}birthDate').get('value') == "2000-01-01"
