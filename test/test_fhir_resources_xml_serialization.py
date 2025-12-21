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


class TestXMLDeserialization:
    """Test XML deserialization functionality with mocked models."""

    def test_simple_deserialization(self):
        """Test deserialization of simple XML with primitives."""
        xml = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="test-123"/>
  <active value="true"/>
  <gender value="male"/>
  <birthDate value="1980-06-15"/>
</Patient>"""
        
        patient = SimplePatient.model_validate_xml(xml)
        
        assert patient.resourceType == "Patient"
        assert patient.id == "test-123"
        assert patient.active is True
        assert patient.gender == "male"
        assert patient.birthDate == "1980-06-15"

    def test_boolean_deserialization(self):
        """Test that boolean values are correctly deserialized."""
        xml_true = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="bool-true"/>
  <active value="true"/>
</Patient>"""
        
        xml_false = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="bool-false"/>
  <active value="false"/>
</Patient>"""
        
        patient_true = SimplePatient.model_validate_xml(xml_true)
        patient_false = SimplePatient.model_validate_xml(xml_false)
        
        assert patient_true.active is True
        assert isinstance(patient_true.active, bool)
        assert patient_false.active is False
        assert isinstance(patient_false.active, bool)

    def test_deserialization_with_none_values(self):
        """Test that missing optional fields are None after deserialization."""
        xml = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="minimal"/>
</Patient>"""
        
        patient = SimplePatient.model_validate_xml(xml)
        
        assert patient.id == "minimal"
        assert patient.active is None
        assert patient.gender is None
        assert patient.birthDate is None

    def test_roundtrip_simple(self):
        """Test serialize → deserialize roundtrip for simple resource."""
        original = SimplePatient(
            id="roundtrip-test",
            active=True,
            gender="female",
            birthDate="1995-03-20"
        )
        
        # Serialize to XML
        xml = original.model_dump_xml(pretty=False)
        
        # Deserialize back
        restored = SimplePatient.model_validate_xml(xml)
        
        # Verify all fields match
        assert restored.id == original.id
        assert restored.active == original.active
        assert restored.gender == original.gender
        assert restored.birthDate == original.birthDate

    def test_roundtrip_pretty_printed(self):
        """Test roundtrip with pretty printed XML."""
        original = SimplePatient(
            id="pretty-test",
            active=False,
            gender="other"
        )
        
        # Serialize with pretty printing
        xml = original.model_dump_xml(pretty=True)
        
        # Pretty printed XML should still deserialize correctly
        restored = SimplePatient.model_validate_xml(xml)
        
        assert restored.id == original.id
        assert restored.active == original.active
        assert restored.gender == original.gender

    def test_complex_type_deserialization(self):
        """Test deserialization of resources with complex types."""
        xml = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="complex-test"/>
  <name>
    <use value="official"/>
    <family value="Smith"/>
    <given value="John"/>
    <given value="Michael"/>
  </name>
</Patient>"""
        
        patient = PatientWithComplexTypes.model_validate_xml(xml)
        
        assert patient.id == "complex-test"
        assert len(patient.name) == 1
        assert patient.name[0].use == "official"
        assert patient.name[0].family == "Smith"
        assert patient.name[0].given == ["John", "Michael"]

    def test_single_element_becomes_list(self):
        """Test that single complex type element is deserialized as a list."""
        xml = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="list-test"/>
  <name>
    <family value="Doe"/>
  </name>
</Patient>"""
        
        patient = PatientWithComplexTypes.model_validate_xml(xml)
        
        # name should be a list even with single element
        assert isinstance(patient.name, list)
        assert len(patient.name) == 1
        assert patient.name[0].family == "Doe"

    def test_multiple_complex_types_deserialization(self):
        """Test deserialization with multiple instances of complex types."""
        xml = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="multi-complex"/>
  <name>
    <use value="official"/>
    <family value="Chalmers"/>
  </name>
  <name>
    <use value="maiden"/>
    <family value="Windsor"/>
  </name>
</Patient>"""
        
        patient = PatientWithComplexTypes.model_validate_xml(xml)
        
        assert len(patient.name) == 2
        assert patient.name[0].use == "official"
        assert patient.name[0].family == "Chalmers"
        assert patient.name[1].use == "maiden"
        assert patient.name[1].family == "Windsor"

    def test_nested_list_deserialization(self):
        """Test nested list fields (e.g., given names within name)."""
        xml = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="nested-list"/>
  <name>
    <family value="Johnson"/>
    <given value="Alice"/>
    <given value="Marie"/>
    <given value="Elizabeth"/>
  </name>
</Patient>"""
        
        patient = PatientWithComplexTypes.model_validate_xml(xml)
        
        assert len(patient.name) == 1
        assert patient.name[0].family == "Johnson"
        assert isinstance(patient.name[0].given, list)
        assert len(patient.name[0].given) == 3
        assert patient.name[0].given == ["Alice", "Marie", "Elizabeth"]

    def test_address_with_multiple_lines_deserialization(self):
        """Test Address with multiple line elements."""
        xml = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="address-test"/>
  <address>
    <use value="home"/>
    <line value="534 Erewhon St"/>
    <line value="Apt 42"/>
    <city value="PleasantVille"/>
    <state value="Vic"/>
    <postalCode value="3999"/>
  </address>
</Patient>"""
        
        patient = PatientWithComplexTypes.model_validate_xml(xml)
        
        assert len(patient.address) == 1
        addr = patient.address[0]
        assert addr.use == "home"
        assert isinstance(addr.line, list)
        assert len(addr.line) == 2
        assert addr.line == ["534 Erewhon St", "Apt 42"]
        assert addr.city == "PleasantVille"
        assert addr.state == "Vic"
        assert addr.postalCode == "3999"

    def test_roundtrip_complex_types(self):
        """Test serialize → deserialize roundtrip for complex structures."""
        original = PatientWithComplexTypes(
            id="complex-roundtrip",
            name=[
                MockHumanName(
                    use="official",
                    family="Williams",
                    given=["Robert", "James"]
                ),
                MockHumanName(
                    use="nickname",
                    given=["Bob"]
                )
            ],
            address=[
                MockAddress(
                    use="home",
                    line=["123 Main St", "Apt 4B"],
                    city="Springfield"
                )
            ]
        )
        
        # Serialize
        xml = original.model_dump_xml(pretty=True)
        
        # Deserialize
        restored = PatientWithComplexTypes.model_validate_xml(xml)
        
        # Verify structure preserved
        assert restored.id == original.id
        assert len(restored.name) == 2
        assert restored.name[0].use == "official"
        assert restored.name[0].family == "Williams"
        assert restored.name[0].given == ["Robert", "James"]
        assert restored.name[1].use == "nickname"
        assert restored.name[1].given == ["Bob"]
        assert len(restored.address) == 1
        assert restored.address[0].use == "home"
        assert restored.address[0].line == ["123 Main St", "Apt 4B"]
        assert restored.address[0].city == "Springfield"

    def test_namespace_stripping(self):
        """Test that FHIR namespace is properly stripped during deserialization."""
        # XML with explicit namespace
        xml_with_ns = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="ns-test"/>
  <gender value="other"/>
</Patient>"""
        
        # XML without namespace (should still work)
        xml_without_ns = """<?xml version="1.0"?>
<Patient>
  <id value="ns-test"/>
  <gender value="other"/>
</Patient>"""
        
        patient_with_ns = SimplePatient.model_validate_xml(xml_with_ns)
        patient_without_ns = SimplePatient.model_validate_xml(xml_without_ns)
        
        assert patient_with_ns.id == "ns-test"
        assert patient_with_ns.gender == "other"
        assert patient_without_ns.id == "ns-test"
        assert patient_without_ns.gender == "other"

    def test_mixed_content_deserialization(self):
        """Test deserialization with both simple and complex fields."""
        xml = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="mixed-test"/>
  <name>
    <family value="Mixture"/>
    <given value="Test"/>
  </name>
  <gender value="unknown"/>
  <birthDate value="2000-01-01"/>
  <address>
    <city value="TestCity"/>
  </address>
</Patient>"""
        
        patient = PatientWithComplexTypes.model_validate_xml(xml)
        
        # Simple fields
        assert patient.id == "mixed-test"
        # Complex fields
        assert len(patient.name) == 1
        assert patient.name[0].family == "Mixture"
        assert len(patient.address) == 1
        assert patient.address[0].city == "TestCity"

    def test_empty_resource_deserialization(self):
        """Test deserialization of minimal resource."""
        xml = """<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
</Patient>"""
        
        patient = SimplePatient.model_validate_xml(xml)
        
        assert patient.resourceType == "Patient"
        assert patient.id is None
        assert patient.active is None
        assert patient.gender is None
        assert patient.birthDate is None

    def test_double_roundtrip(self):
        """Test serialize → deserialize → serialize → deserialize."""
        original = PatientWithComplexTypes(
            id="double-roundtrip",
            name=[
                MockHumanName(
                    family="Test",
                    given=["Double", "Roundtrip"]
                )
            ]
        )
        
        # First roundtrip
        xml1 = original.model_dump_xml()
        restored1 = PatientWithComplexTypes.model_validate_xml(xml1)
        
        # Second roundtrip
        xml2 = restored1.model_dump_xml()
        restored2 = PatientWithComplexTypes.model_validate_xml(xml2)
        
        # All should match
        assert restored2.id == original.id
        assert restored2.name[0].family == original.name[0].family
        assert restored2.name[0].given == original.name[0].given

    def test_external_xml_format(self):
        """Test parsing XML in format that might come from external FHIR server."""
        # Simulates real FHIR server response with XML declaration and encoding
        external_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="external-123"/>
  <name>
    <use value="official"/>
    <family value="External"/>
    <given value="Patient"/>
  </name>
</Patient>"""
        
        patient = PatientWithComplexTypes.model_validate_xml(external_xml)
        
        assert patient.id == "external-123"
        assert len(patient.name) == 1
        assert patient.name[0].family == "External"
        assert patient.name[0].given == ["Patient"]
