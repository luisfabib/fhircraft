from fhircraft.fhir.resources.datatypes.R4 import (
    CodeableConcept,
    Extension,
    Coding,
    String,
    Code,
    Date,
    Boolean,
    Integer,
    HumanName,
)
from fhircraft.fhir.resources.base import FHIRBaseModel
from fhircraft.fhir.resources.base.mixins.xml import XML_NAMESPACE

import xml.etree.ElementTree as xml
import json

from fhircraft.fhir.resources.datatypes.R4.core.observation import Observation


class PrimitivesModel(FHIRBaseModel):
    code: Code
    date: Date
    deceased: Boolean
    count: Integer


XMLNS = {"": XML_NAMESPACE}

# ===================================================
# Primitives - JSON Serialization
# ===================================================


def test_serialize_as_json__primitive__only_value():
    primitive = String(value="Hello world")
    data = primitive._serialize_as_json("valueString")
    assert data == {"valueString": "Hello world"}


def test_serialize_as_json__primitive__only_extension():
    primitive = String(extension=[Extension(url="http://example.com", valueString="example")])  # type: ignore
    data = primitive._serialize_as_json("valueString")
    assert data == {
        "_valueString": {
            "extension": [{"url": "http://example.com", "valueString": "example"}]
        }
    }


def test_serialize_as_json__primitive__value_with_id():
    primitive = String(value="Hello world", id="123")
    data = primitive._serialize_as_json("valueString")
    assert data == {"valueString": "Hello world", "_valueString": {"id": "123"}}


def test_serialize_as_json__primitive__model_dump_json():
    instance = PrimitivesModel(
        code=Code(value="abc"),
        date=Date(value="1972-11-30"),
        deceased=Boolean(value=False),
        count=Integer(value=23),
    )

    assert instance.model_dump_json(indent=2) == json.dumps(
        {
            "code": "abc",
            "date": "1972-11-30",
            "deceased": False,
            "count": 23,
        },
        indent=2,
    )


def test_serialize_as_json__primitive__value_and_extension():
    primitive = String(value="Hello world", extension=[Extension(url="http://example.com", valueString="example")])  # type: ignore
    data = primitive._serialize_as_json("valueString")
    assert data == {
        "valueString": "Hello world",
        "_valueString": {
            "extension": [{"url": "http://example.com", "valueString": "example"}]
        },
    }


# ===================================================
# Lists - JSON Serialization
# ===================================================


def test_serialize_as_json__list_of_primitives():
    instance = HumanName(given=[String(value="Alice"), String(value="Marie")])
    data = json.loads(instance.model_dump_json())
    assert data["given"] == ["Alice", "Marie"]


def test_serialize_as_json__list_of_primitives__with_shadow():
    instance = HumanName(
        given=[
            String(value="Alice"),
            String(  # type: ignore
                value="Marie",
                extension=[Extension(url="http://example.com", valueString="example")],
            ),
        ]
    )
    data = json.loads(instance.model_dump_json())
    assert data["given"] == ["Alice", "Marie"]
    assert data["_given"] == [
        None,
        {"extension": [{"url": "http://example.com", "valueString": "example"}]},
    ]


def test_serialize_as_json__list_of_primitives__extension_only_suppresses_value_key():
    instance = HumanName(
        given=[
            String(extension=[Extension(url="http://example.com", valueString="example")])  # type: ignore,
        ]
    )
    data = json.loads(instance.model_dump_json())
    assert "given" not in data
    assert data["_given"] == [
        {"extension": [{"url": "http://example.com", "valueString": "example"}]}
    ]


# ===================================================
# Complex Types - JSON Serialization
# ===================================================


def test_serialize_as_json__complex__model_dump():
    concept = CodeableConcept(
        coding=[Coding(code="C123", system="http://example.com")],
        text="Example Code",  # type: ignore
    )
    data = concept.model_dump()
    assert data["coding"] == [{"code": "C123", "system": "http://example.com"}]
    assert data["text"] == "Example Code"


def test_serialize_as_json__complex__model_dump_json():
    concept = CodeableConcept(
        coding=[
            Coding(code="C123", system="http://snomed.info/sct", display="Sys A"),
            Coding(code="C456", system="http://loinc.org", display="Sys B"),
        ],
    )
    data = json.loads(concept.model_dump_json())
    assert len(data["coding"]) == 2
    assert data["coding"][0]["code"] == "C123"
    assert data["coding"][1]["code"] == "C456"


# ===================================================
# Resources - JSON Serialization
# ===================================================


def test_serialize_as_json__resource__includes_resource_type():
    instance = Observation(valueString=String(value="John"))
    data = json.loads(instance.model_dump_json())
    assert data["resourceType"] == "Observation"
    assert data["valueString"] == "John"


# ===================================================
# Primitives - XML Serialization
# ===================================================


def test_serialize_as_xml__primitive__only_value():
    primitive = String(value="Hello world")
    element = primitive._serialize_as_xml("valueString")
    assert "valueString" in element.tag
    assert element.attrib == {"value": "Hello world"}


def test_serialize_as_xml__primitive__only_extension():
    primitive = String(extension=[Extension(url="http://example.com", valueString="example")])  # type: ignore
    element = primitive._serialize_as_xml("valueString")
    assert "valueString" in element.tag
    assert (extension := element.find("extension", XMLNS)) is not None
    assert "extension" in extension.tag
    assert extension.attrib == {"url": "http://example.com"}
    assert (valueString := extension.find("valueString", XMLNS)) is not None
    assert valueString.attrib == {"value": "example"}


def test_serialize_as_xml__primitive__value_with_id():
    primitive = String(value="Hello world", id="123")
    element = primitive._serialize_as_xml("valueString")
    assert "valueString" in element.tag
    assert element.attrib == {"value": "Hello world", "id": "123"}


def test_serialize_as_xml__primitive__boolean_true():
    primitive = Boolean(value=True)
    element = primitive._serialize_as_xml("valueBoolean")
    assert "valueBoolean" in element.tag
    assert element.attrib == {"value": "true"}


def test_serialize_as_xml__primitive__boolean_false():
    primitive = Boolean(value=False)
    element = primitive._serialize_as_xml("valueBoolean")
    assert "valueBoolean" in element.tag
    assert element.attrib == {"value": "false"}


def test_serialize_as_xml__primitive__value_and_extension():
    primitive = String(  # type: ignore
        value="Hello",
        extension=[Extension(url="http://example.com", valueString="example")],
    )
    element = primitive._serialize_as_xml("valueString")
    assert element.attrib["value"] == "Hello"
    assert (ext := element.find("extension", XMLNS)) is not None
    assert ext.attrib["url"] == "http://example.com"
    assert (valueString := ext.find("valueString", XMLNS)) is not None
    assert valueString.attrib["value"] == "example"


# ===================================================
# Primitives - XML Deserialization
# ===================================================


def test_parse_xml_to_dict__primitive__only_value():
    xml_str = '<valueString xmlns="http://hl7.org/fhir" value="Hello world"/>'
    primitive = String._parse_xml_to_dict(xml.fromstring(xml_str))
    assert primitive == {"valueString": "Hello world"}


def test_parse_xml_to_dict__primitive__only_extension():
    xml_str = """
    <valueString xmlns="http://hl7.org/fhir">
        <extension url="http://example.com">
            <valueString value="example"/>
        </extension>
    </valueString>
    """
    result = String._parse_xml_to_dict(xml.fromstring(xml_str))
    assert result == {
        "_valueString": {
            "extension": [{"url": "http://example.com", "valueString": "example"}]
        }
    }


def test_parse_xml_to_dict__primitive__value_with_id():
    xml_str = '<valueString xmlns="http://hl7.org/fhir" value="Hello world" id="123"/>'
    result = String._parse_xml_to_dict(xml.fromstring(xml_str))
    assert result == {"valueString": "Hello world", "_valueString": {"id": "123"}}


def test_parse_xml_to_dict__primitive__boolean_true():
    xml_str = '<valueBoolean xmlns="http://hl7.org/fhir" value="true"/>'
    result = Boolean._parse_xml_to_dict(xml.fromstring(xml_str))
    assert result == {"valueBoolean": True}


def test_parse_xml_to_dict__primitive__boolean_false():
    xml_str = '<valueBoolean xmlns="http://hl7.org/fhir" value="false"/>'
    result = Boolean._parse_xml_to_dict(xml.fromstring(xml_str))
    assert result == {"valueBoolean": False}


def test_parse_xml_to_dict__primitive__value_and_extension():
    xml_str = """
    <valueString xmlns="http://hl7.org/fhir" value="Hello">
        <extension url="http://example.com">
            <valueString value="example"/>
        </extension>
    </valueString>
    """
    result = String._parse_xml_to_dict(xml.fromstring(xml_str))
    assert result == {
        "valueString": "Hello",
        "_valueString": {
            "extension": [{"url": "http://example.com", "valueString": "example"}]
        },
    }


# ===================================================
# Complex Type - XML Serialization
# ===================================================


def test_serialize_as_xml__complex__only_values():
    primitive = Coding(code="C123", system="http://example.com", display="Example Code")
    element = primitive._serialize_as_xml("valueCoding")
    assert "valueCoding" in element.tag
    assert (code := element.find("code", XMLNS)) is not None
    assert code.attrib == {"value": "C123"}
    assert (system := element.find("system", XMLNS)) is not None
    assert system.attrib == {"value": "http://example.com"}
    assert (display := element.find("display", XMLNS)) is not None
    assert display.attrib == {"value": "Example Code"}


def test_serialize_as_xml__complex__with_id():
    primitive = Coding(display="Example Code", id="123")
    element = primitive._serialize_as_xml("valueCoding")
    assert "valueCoding" in element.tag
    assert element.attrib == {"id": "123"}
    assert (display := element.find("display", XMLNS)) is not None
    assert display.attrib == {"value": "Example Code"}


def test_serialize_as_xml__complex__list_of_complex_types():
    concept = CodeableConcept(
        coding=[
            Coding(code="C123", system="http://example.com"),
            Coding(code="C456", system="http://example2.com"),
        ]
    )
    element = concept._serialize_as_xml("valueCodeableConcept")
    assert "valueCodeableConcept" in element.tag
    codings = element.findall("coding", XMLNS)
    assert len(codings) == 2
    assert codings[0].find("code", XMLNS).attrib == {"value": "C123"}  # type: ignore
    assert codings[1].find("code", XMLNS).attrib == {"value": "C456"}  # type: ignore


def test_serialize_as_xml__complex__list_of_primitives():
    instance = HumanName(given=[String(value="Alice"), String(value="Marie")])
    element = instance._serialize_as_xml("name")
    assert "name" in element.tag
    given_elements = element.findall("given", XMLNS)
    assert len(given_elements) == 2
    assert given_elements[0].attrib == {"value": "Alice"}
    assert given_elements[1].attrib == {"value": "Marie"}


def test_serialize_as_xml__complex__nested_complex_type():
    concept = CodeableConcept(
        coding=[
            Coding(
                code="official", system="http://terminology.hl7.org/CodeSystem/v2-0203"
            )
        ],
        text="Official Identifier",  # type: ignore
    )
    element = concept._serialize_as_xml("type")
    assert "type" in element.tag
    codings = element.findall("coding", XMLNS)
    assert len(codings) == 1
    assert codings[0].find("code", XMLNS).attrib == {"value": "official"}  # type: ignore
    assert (text_el := element.find("text", XMLNS)) is not None
    assert text_el.attrib == {"value": "Official Identifier"}


# ===================================================
# Complex Type - XML Deserialization
# ===================================================


def test_parse_xml_to_dict__complex__coding():
    xml_str = """
    <valueCoding xmlns="http://hl7.org/fhir">
        <system value="http://example.org/system"/>
        <code value="abc"/>
        <display value="Example Code"/>
    </valueCoding>
    """
    result = Coding._parse_xml_to_dict(xml.fromstring(xml_str))
    assert result == {
        "valueCoding": {
            "system": "http://example.org/system",
            "code": "abc",
            "display": "Example Code",
        }
    }


def test_parse_xml_to_dict__complex__coding__with_id():
    xml_str = """
    <valueCoding xmlns="http://hl7.org/fhir" id="c1">
        <code value="abc"/>
    </valueCoding>
    """
    result = Coding._parse_xml_to_dict(xml.fromstring(xml_str))
    assert result == {"valueCoding": {"code": "abc", "id": "c1"}}


def test_parse_xml_to_dict__complex__codeable_concept__with_text():
    xml_str = """
    <type xmlns="http://hl7.org/fhir">
        <coding>
            <system value="http://example.com"/>
            <code value="official"/>
        </coding>
        <text value="Official Identifier"/>
    </type>
    """
    result = CodeableConcept._parse_xml_to_dict(xml.fromstring(xml_str))
    assert result == {
        "type": {
            "coding": [{"system": "http://example.com", "code": "official"}],
            "text": "Official Identifier",
        }
    }


def test_parse_xml_to_dict__complex__codeable_concept__multiple_codings():
    xml_str = """
    <code xmlns="http://hl7.org/fhir">
        <coding>
            <system value="http://snomed.info/sct"/>
            <code value="C123"/>
        </coding>
        <coding>
            <system value="http://loinc.org"/>
            <code value="L456"/>
        </coding>
    </code>
    """
    result = CodeableConcept._parse_xml_to_dict(xml.fromstring(xml_str))
    assert len(result["code"]["coding"]) == 2
    assert result["code"]["coding"][0] == {
        "system": "http://snomed.info/sct",
        "code": "C123",
    }
    assert result["code"]["coding"][1] == {
        "system": "http://loinc.org",
        "code": "L456",
    }


def test_parse_xml_to_dict__complex__human_name__list_of_primitives():
    xml_str = """
    <name xmlns="http://hl7.org/fhir">
        <family value="Smith"/>
        <given value="Alice"/>
        <given value="Marie"/>
    </name>
    """
    result = HumanName._parse_xml_to_dict(xml.fromstring(xml_str))
    assert result == {"name": {"family": "Smith", "given": ["Alice", "Marie"]}}


def test_model_validate_xml__complex__coding():
    xml_str = """
    <Coding xmlns="http://hl7.org/fhir">
        <system value="http://example.org/system"/>
        <code value="abc"/>
        <display value="Example Code"/>
    </Coding>
    """
    coding = Coding.model_validate_xml(xml_str)
    assert coding is not None
    assert str(coding.system) == "http://example.org/system"
    assert str(coding.code) == "abc"
    assert str(coding.display) == "Example Code"


def test_model_validate_xml__complex__codeable_concept():
    xml_str = """
    <CodeableConcept xmlns="http://hl7.org/fhir">
        <coding>
            <system value="http://snomed.info/sct"/>
            <code value="C123"/>
            <display value="Finding"/>
        </coding>
        <text value="Finding"/>
    </CodeableConcept>
    """
    concept = CodeableConcept.model_validate_xml(xml_str)
    assert concept.coding is not None
    assert len(concept.coding) == 1
    assert str(concept.coding[0].system) == "http://snomed.info/sct"
    assert str(concept.coding[0].code) == "C123"
    assert str(concept.text) == "Finding"


def test_model_validate_xml__complex__human_name__with_given_list():
    xml_str = """
    <HumanName xmlns="http://hl7.org/fhir">
        <family value="Smith"/>
        <given value="Alice"/>
        <given value="Marie"/>
    </HumanName>
    """
    name = HumanName.model_validate_xml(xml_str)
    assert str(name.family) == "Smith"
    assert name.given is not None
    assert len(name.given) == 2
    assert str(name.given[0]) == "Alice"
    assert str(name.given[1]) == "Marie"


# ===================================================
# Resources - XML Deserialization
# ===================================================


def test_model_validate_xml__resource__observation():
    xml_str = """
    <Observation xmlns="http://hl7.org/fhir">
        <status value="final"/>
        <code>
            <coding>
                <system value="http://loinc.org"/>
                <code value="29463-7"/>
                <display value="Body Weight"/>
            </coding>
        </code>
        <valueString value="72 kg"/>
    </Observation>
    """
    obs = Observation.model_validate_xml(xml_str)
    assert str(obs.status) == "final"
    assert obs.code is not None
    assert obs.code.coding is not None
    assert len(obs.code.coding) == 1
    assert str(obs.code.coding[0].code) == "29463-7"
    assert str(obs.valueString) == "72 kg"


# ===================================================
# Resources - XML Serialization
# ===================================================


def test_serialize_as_xml__resource__element_tag_is_type():
    instance = Observation(valueString=String(value="John"))
    element = instance._serialize_as_xml(instance._type)
    assert "Observation" in element.tag
    assert (name_el := element.find("valueString", XMLNS)) is not None
    assert name_el.attrib == {"value": "John"}


def test_serialize_as_xml__resource__model_dump_xml_includes_xmlns():
    instance = Observation(valueString=String(value="John"))
    xml_str = instance.model_dump_xml()
    assert 'xmlns="http://hl7.org/fhir"' in xml_str
    assert "<Observation" in xml_str
    assert 'value="John"' in xml_str
