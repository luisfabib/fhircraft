from typing import List, Optional, get_args
from unittest import TestCase

from parameterized import parameterized, parameterized_class
from pydantic import Field
from pydantic.fields import FieldInfo

import fhircraft.fhir.resources.datatypes.primitives as primitives
import fhircraft.fhir.resources.datatypes.R4B.complex_types as complex_types
from fhircraft.fhir.resources.definitions.element_definition import ElementDefinition
from fhircraft.fhir.resources.factory import ResourceFactory, _Unset


class FactoryTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = ResourceFactory()
        cls.factory.Config = cls.factory.FactoryConfig(
            FHIR_release="R4B", resource_name="Test"
        )


class TestBuildElementTreeStructure(FactoryTestCase):

    def test_correctly_builds_tree_structure(self):
        elements = [
            ElementDefinition(
                **{
                    "path": "Patient.name",
                    "id": "Patient.name",
                    "type": [{"code": "string"}],
                }
            ),
            ElementDefinition(
                **{
                    "path": "Patient.address",
                    "id": "Patient.address",
                    "type": [{"code": "Address"}],
                }
            ),
            ElementDefinition(
                **{
                    "path": "Patient.identifier",
                    "id": "Patient.identifier",
                    "type": [{"code": "Identifier"}],
                }
            ),
        ]
        nodes = self.factory._build_element_tree_structure(elements)
        node = nodes[0]
        assert "Patient" == node.node_label
        assert "name" in node.children
        assert "Patient.name" == node.children["name"].id
        assert node.children["name"].type is not None
        assert "string" == node.children["name"].type[0].code
        assert "address" in node.children
        assert "Patient.address" == node.children["address"].id
        assert node.children["address"].type is not None
        assert "Address" == node.children["address"].type[0].code
        assert "identifier" in node.children
        assert "Patient.identifier" == node.children["identifier"].id
        assert node.children["identifier"].type is not None
        assert "Identifier" == node.children["identifier"].type[0].code

    def test_handles_single_level_paths(self):
        elements = [
            ElementDefinition(
                **{"path": "name", "id": "name", "type": [{"code": "string"}]}
            ),
            ElementDefinition(
                **{"path": "address", "id": "address", "type": [{"code": "Address"}]}
            ),
        ]
        nodes = self.factory._build_element_tree_structure(elements)
        assert "name" in [node.node_label for node in nodes]
        assert "address" in [node.node_label for node in nodes]

    def test_processes_multiple_elements_with_different_paths(self):
        elements = [
            ElementDefinition(
                **{
                    "path": "Patient.name",
                    "id": "Patient.name",
                    "type": [{"code": "string"}],
                }
            ),
            ElementDefinition(
                **{
                    "path": "Patient.address.city",
                    "id": "Patient.address.city",
                    "type": [{"code": "string"}],
                }
            ),
        ]
        nodes = self.factory._build_element_tree_structure(elements)
        assert "Patient" == nodes[0].node_label
        assert "name" in nodes[0].children
        assert "address" in nodes[0].children
        assert "city" in nodes[0].children["address"].children

    def test_handles_slicing(self):
        elements = [
            ElementDefinition(
                **{"path": "component", "id": "component", "type": [{"code": "string"}]}
            ),
            ElementDefinition(
                **{
                    "path": "component",
                    "id": "component:sliceA",
                    "type": [{"code": "Address"}],
                }
            ),
            ElementDefinition(
                **{
                    "path": "component",
                    "id": "component:sliceA.valueString",
                    "type": [{"code": "string"}],
                }
            ),
        ]
        nodes = self.factory._build_element_tree_structure(elements)
        print([node.model_dump(exclude_unset=True) for node in nodes])
        assert "component" == nodes[0].node_label
        assert "sliceA" == nodes[0].slices["sliceA"].node_label
        assert (
            "valueString"
            == nodes[0].slices["sliceA"].children["valueString"].node_label
        )

    def test_handles_empty_list_of_elements(self):
        elements = []
        nodes = self.factory._build_element_tree_structure(elements)
        assert nodes == []


class TestGetFhirType(FactoryTestCase):

    def test_parses_fhir_primitive_datatype(self):
        result = self.factory._get_complex_FHIR_type("string")
        assert result == primitives.String

    def test_parses_fhir_complex_datatype(self):
        result = self.factory._get_complex_FHIR_type("Coding")
        assert result == complex_types.Coding

    def test_parses_fhir_complex_datatype_from_canonical_url(self):
        result = self.factory._get_complex_FHIR_type(
            "http://hl7.org/fhir/StructureDefinition/Extension"
        )
        assert result == complex_types.Extension

    def test_parses_fhir_fhirpath_datatype(self):
        result = self.factory._get_complex_FHIR_type(
            "http://hl7.org/fhirpath/System.String"
        )
        assert result == primitives.String

    def test_returns_field_type_name_if_not_found(self):
        result = self.factory._get_complex_FHIR_type("UnknownType")
        assert result == "UnknownType"


class TestConstructPydanticField(FactoryTestCase):

    def test_output_structure(self):
        result = self.factory._construct_Pydantic_field(str, min_card=1, max_card=1)
        assert isinstance(result, tuple)
        assert isinstance(result[0], type)
        assert isinstance(result[1], FieldInfo)

    def test_constructs_required_field(self):
        field_type = primitives.String
        result = self.factory._construct_Pydantic_field(
            field_type, min_card=1, max_card=1
        )
        assert result[0] == field_type
        assert result[1].is_required() == True

    def test_constructs_optional_field(self):
        field_type = primitives.String
        result = self.factory._construct_Pydantic_field(
            field_type, min_card=0, max_card=1
        )
        assert result[0] == Optional[field_type]
        assert result[1].is_required() == False
        assert result[1].default is None

    def test_constructs_required_list_field(self):
        field_type = primitives.String
        result = self.factory._construct_Pydantic_field(
            field_type, min_card=1, max_card=99999
        )
        assert result[0] == List[field_type]
        assert result[1].is_required() == True

    def test_constructs_optional_list_field(self):
        field_type = primitives.String
        result = self.factory._construct_Pydantic_field(
            field_type, min_card=0, max_card=99999
        )
        assert result[0] == Optional[List[field_type]]
        assert result[1].is_required() == False
        assert result[1].default is None


@parameterized_class(
    [
        {"prefix": "fixed"},
        {"prefix": "pattern"},
    ]
)
class TestProcessPatternOrFixedValues(FactoryTestCase):

    @parameterized.expand(
        [
            ("String", primitives.String, "test_string"),
            ("Boolean", primitives.Boolean, True),
            ("Decimal", primitives.Decimal, 2.54),
        ]
    )
    def test_processes_value_constraint_on_primitive(
        self, attribute, expected_type, expected_value
    ):
        element = ElementDefinition.model_construct(**{f"{self.prefix}{attribute}": expected_value})  # type: ignore
        result = self.factory._process_pattern_or_fixed_values(element, self.prefix)  # type: ignore
        assert (
            type(result) in get_args(expected_type.__value__)
            or type(result) is expected_type.__value__
        )
        assert result == expected_value

    @parameterized.expand(
        [
            (
                "Coding",
                complex_types.Coding,
                {"code": "1234", "system": "https://domain.org"},
            ),
            (
                "Quantity",
                complex_types.Quantity,
                {
                    "value": 23.45,
                    "unit": "mg",
                    "code": "1234",
                    "system": "https://domain.org",
                },
            ),
            (
                "CodeableConcept",
                complex_types.CodeableConcept,
                {"coding": [{"code": "1234", "system": "https://domain.org"}]},
            ),
        ]
    )
    def test_processes_value_constraint_on_complex_type(
        self, attribute, expected_type, expected_value
    ):
        element = ElementDefinition.model_construct(**{f"{self.prefix}{attribute}": expected_value})  # type: ignore
        result = self.factory._process_pattern_or_fixed_values(element, self.prefix)  # type: ignore
        assert isinstance(result, expected_type)
        assert result == expected_type.model_validate(expected_value)

    def test_processes_no_constraints(self):
        element = ElementDefinition.model_construct()
        result = self.factory._process_pattern_or_fixed_values(element, self.prefix)  # type: ignore
        assert result is None


class TestProcessCardinalityConstraints(FactoryTestCase):

    @parameterized.expand(
        [
            (ElementDefinition.model_construct(min=0, max="1"), 0, 1),
            (ElementDefinition.model_construct(min=1, max="2"), 1, 2),
            (ElementDefinition.model_construct(min=0, max="*"), 0, 99999),
        ]
    )
    def test_cardinality_constraints(self, element, expected_min, expected_max):
        min_card, max_card = self.factory._parse_element_cardinality(element)
        assert min_card == expected_min
        assert max_card == expected_max
