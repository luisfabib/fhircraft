import warnings
from typing import List, Optional, get_args
from unittest import TestCase, mock

import pytest
from parameterized import parameterized, parameterized_class
from pydantic import BaseModel, Field
from pydantic.aliases import AliasChoices
from pydantic.fields import FieldInfo

import fhircraft.fhir.resources.datatypes.primitives as primitives
import fhircraft.fhir.resources.datatypes.R4B.complex_types as complex_types
from fhircraft.fhir.resources.definitions import (
    StructureDefinition,
    StructureDefinitionSnapshot,
)
from fhircraft.fhir.resources.definitions.element_definition import (
    ElementDefinition,
    ElementDefinitionType,
)
from fhircraft.fhir.resources.factory import (
    ElementDefinitionNode,
    FHIRSliceModel,
    ResourceFactory,
    ResourceFactoryValidators,
)


class FactoryTestCase(TestCase):
    """
    Test case for verifying the behavior of the ResourceFactory class and its configuration helpers.

    This class sets up a ResourceFactory instance with a specific configuration for testing purposes.
    The configuration uses FHIR release "R4B" and resource name "Test".

    Class Attributes:
        factory (ResourceFactory): An instance of ResourceFactory configured for testing.

    Methods:
        setUpClass: Initializes the ResourceFactory and its configuration before running tests.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = ResourceFactory()
        cls.factory.Config = cls.factory.FactoryConfig(
            FHIR_release="R4B", resource_name="Test", FHIR_version="4.3.0"
        )


# ----------------------------------------------------------------
# _build_element_tree_structure()
# ----------------------------------------------------------------


class TestBuildElementTreeStructure(FactoryTestCase):
    """
    Unit tests for the _build_element_tree_structure method of the factory.
    """

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


# ----------------------------------------------------------------
# _resolve_FHIR_type()
# ----------------------------------------------------------------


class TestGetComplexFhirType(FactoryTestCase):
    """
    Unit tests for the _resolve_FHIR_type method of the FHIR resource factory.
    """

    def test_parses_fhir_primitive_datatype(self):
        element_type = ElementDefinitionType(code="string")
        result = self.factory._resolve_FHIR_type(element_type)
        assert result == primitives.String

    def test_parses_fhir_primitive_datatype_as_string(self):
        result = self.factory._resolve_FHIR_type("string")
        assert result == primitives.String

    def test_parses_fhir_complex_datatype(self):
        element_type = ElementDefinitionType(code="Coding")
        result = self.factory._resolve_FHIR_type(element_type)
        assert result == complex_types.Coding

    def test_parses_fhir_complex_datatype_from_canonical_url(self):
        result = self.factory._resolve_FHIR_type(
            "http://hl7.org/fhir/StructureDefinition/Extension"
        )
        assert result == complex_types.Extension

    def test_parses_fhir_fhirpath_datatype(self):
        result = self.factory._resolve_FHIR_type(
            "http://hl7.org/fhirpath/System.String"
        )
        assert result == primitives.String

    def test_parses_fhir_profiled_type(self):
        profile_url = "http://example.org/fhir/StructureDefinition/CustomType"
        element_type = ElementDefinitionType(code="CustomType", profile=[profile_url])
        self.factory.repository.load_from_definitions(
            StructureDefinition(
                resourceType="StructureDefinition",
                url=profile_url,
                name="CustomType",
                version="1.0.0",
                fhirVersion="4.0.0",
                status="active",
                kind="complex-type",
                abstract=False,
                type="BackboneElement",
                baseDefinition="http://hl7.org/fhir/StructureDefinition/BackboneElement",
                derivation="specialization",
                snapshot=StructureDefinitionSnapshot.model_validate(
                    {
                        "element": [
                            {
                                "id": "CustomType",
                                "path": "CustomType",
                                "min": 0,
                                "max": "*",
                            },
                            {
                                "id": "CustomType.customField",
                                "path": "CustomType.customField",
                                "min": 0,
                                "max": "1",
                                "type": [{"code": "string"}],
                            },
                        ]
                    }
                ),
            )
        )
        result = self.factory._resolve_FHIR_type(element_type)
        assert result == self.factory.construction_cache[profile_url]

    def test_returns_field_type_name_if_not_found(self):
        with pytest.raises(RuntimeError):
            self.factory._resolve_FHIR_type("UnknownType")


# ----------------------------------------------------------------
# _construct_model_with_properties()
# ----------------------------------------------------------------


class TestConstructModelWithProperties(FactoryTestCase):
    """
    Unit tests for the _construct_model_with_properties method of the ResourceFactory.
    """

    # Dummy base model for inheritance
    class DummyBaseModel(BaseModel):
        pass

    def setUp(self):
        super().setUp()

    def test_creates_model_with_given_properties(self):
        properties = {
            "field1": (str, Field(default="value1")),
            "field2": (int, Field(default=42)),
        }
        model_name = "TestModel"
        result = self.factory._construct_model_with_properties(
            model_name, properties, (self.DummyBaseModel,), dict(), dict()
        )
        assert issubclass(result, self.DummyBaseModel)
        instance = result(field1="abc", field2=123)  # type: ignore
        assert hasattr(instance, "field1")
        assert instance.field1 == "abc"  # type: ignore
        assert hasattr(instance, "field2")
        assert instance.field2 == 123  # type: ignore

    def test_model_inherits_base_model(self):
        properties = {
            "fieldA": (str, Field(default="A")),
        }
        model_name = "InheritedModel"
        result = self.factory._construct_model_with_properties(
            model_name, properties, (self.DummyBaseModel,), dict(), dict()
        )
        assert issubclass(result, self.DummyBaseModel)

    def test_model_fields_have_correct_defaults(self):
        properties = {
            "fieldX": (str, Field(default="defaultX")),
            "fieldY": (int, Field(default=99)),
        }
        model_name = "DefaultsModel"
        result = self.factory._construct_model_with_properties(
            model_name, properties, (self.DummyBaseModel,), dict(), dict()
        )
        instance = result()
        assert hasattr(instance, "fieldX")
        assert instance.fieldX == "defaultX"  # type: ignore
        assert hasattr(instance, "fieldY")
        assert instance.fieldY == 99  # type: ignore

    def test_model_fields_are_required_when_no_default(self):
        properties = {
            "requiredField": (str, Field()),
        }
        model_name = "RequiredModel"
        result = self.factory._construct_model_with_properties(
            model_name, properties, (self.DummyBaseModel,), dict(), dict()
        )
        with pytest.raises(Exception):
            result()

    def test_model_with_empty_properties(self):
        model_name = "EmptyModel"
        result = self.factory._construct_model_with_properties(
            model_name, {}, (self.DummyBaseModel,), dict(), dict()
        )
        instance = result()
        assert isinstance(instance, result)


# ----------------------------------------------------------------
# _construct_Pydantic_field()
# ----------------------------------------------------------------


class TestConstructPydanticField(FactoryTestCase):
    """
    Unit tests for the _construct_Pydantic_field method of the factory class.

    Each test asserts the correct type, FieldInfo properties, and default values according to the cardinality and field type.
    """

    def test_output_structure(self):
        result = self.factory._construct_Pydantic_field(str, min_card=1, max_card=1)
        assert isinstance(result, tuple)
        assert isinstance(result[1], FieldInfo)

    def test_constructs_required_field(self):
        field_type = primitives.String
        result = self.factory._construct_Pydantic_field(
            field_type, min_card=1, max_card=1
        )
        assert result[0] == Optional[field_type]
        assert result[1].is_required() == False

    def test_constructs_non_optional_field(self):
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
        assert result[0] == Optional[List[field_type]]
        assert result[1].is_required() == False

    def test_constructs_optional_list_field(self):
        field_type = primitives.String
        result = self.factory._construct_Pydantic_field(
            field_type, min_card=0, max_card=99999
        )
        assert result[0] == Optional[List[field_type]]
        assert result[1].is_required() == False
        assert result[1].default is None


# ----------------------------------------------------------------
# _handle_python_reserved_keyword()
# ----------------------------------------------------------------


class TestHandlePythonReservedKeyword(FactoryTestCase):
    """Test the _handle_python_reserved_keyword method."""

    def test_handles_non_keyword_field_name(self):
        """Test that non-keyword field names are returned unchanged."""
        field_name = "name"
        safe_field_name, validation_alias = (
            self.factory._handle_python_reserved_keyword(field_name)
        )

        assert safe_field_name == "name"
        assert validation_alias is None

    def test_handles_keyword_field_name(self):
        """Test that keyword field names are processed correctly."""
        field_name = "class"  # Python reserved keyword
        safe_field_name, validation_alias = (
            self.factory._handle_python_reserved_keyword(field_name)
        )

        assert safe_field_name == "class_"
        assert isinstance(validation_alias, AliasChoices)

    @parameterized.expand(
        [
            ("and",),
            ("or",),
            ("not",),
            ("if",),
            ("else",),
            ("elif",),
            ("while",),
            ("for",),
            ("def",),
            ("class",),
            ("import",),
            ("from",),
            ("try",),
            ("except",),
            ("finally",),
            ("with",),
            ("as",),
            ("pass",),
            ("break",),
            ("continue",),
            ("return",),
            ("yield",),
            ("lambda",),
            ("global",),
            ("nonlocal",),
            ("assert",),
            ("del",),
            ("is",),
            ("in",),
            ("True",),
            ("False",),
            ("None",),
            ("property",),
            ("classmethod",),
            ("field_validator",),
            ("model_validator",),
        ]
    )
    def test_handles_all_python_keywords(self, keyword_name):
        """Test that all Python reserved keywords are handled correctly."""
        safe_field_name, validation_alias = (
            self.factory._handle_python_reserved_keyword(keyword_name)
        )

        assert safe_field_name == f"{keyword_name}_"
        assert isinstance(validation_alias, AliasChoices)
        # Note: AliasChoices.choices might not be directly accessible, so we test functionality

    def test_handles_field_with_underscore_suffix(self):
        """Test handling of field names that already have underscore suffix."""
        field_name = "class_"  # Not a keyword due to underscore
        safe_field_name, validation_alias = (
            self.factory._handle_python_reserved_keyword(field_name)
        )

        assert safe_field_name == "class_"
        assert validation_alias is None


# ----------------------------------------------------------------
# _process_pattern_or_fixed_values()
# ----------------------------------------------------------------


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


# ----------------------------------------------------------------
# _construct_type_choice_fields()
# ----------------------------------------------------------------


class TestProcessChoiceTypeField(FactoryTestCase):
    """
    Unit tests for the _construct_type_choice_fields method of the ResourceFactory.
    """

    def setUp(self):
        super().setUp()
        self.factory._handle_python_reserved_keyword = mock.Mock(
            side_effect=lambda name: (name, None)
        )

    def test_single_choice_type_field(self):
        # Simulate a choice type element with one possible type
        element_types = [primitives.String]
        basename = "value"
        max_card = 1
        fields = self.factory._construct_type_choice_fields(
            basename, element_types, max_card
        )
        assert isinstance(fields, dict)
        assert "valueString" in fields
        field_type, field_info = fields["valueString"]
        assert field_type == Optional[primitives.String]
        assert field_info.default is None

    def test_multiple_choice_type_fields(self):
        # Simulate a choice type element with multiple possible types
        element_types = [
            primitives.String,
            primitives.Boolean,
            complex_types.Coding,
        ]
        basename = "value"
        max_card = 1
        fields = self.factory._construct_type_choice_fields(
            basename, element_types, max_card
        )
        assert isinstance(fields, dict)
        assert "valueString" in fields
        assert "valueBoolean" in fields
        assert "valueCoding" in fields
        assert fields["valueString"][0] == Optional[primitives.String]
        assert fields["valueBoolean"][0] == Optional[primitives.Boolean]
        assert fields["valueCoding"][0] == Optional[complex_types.Coding]

    def test_choice_type_with_list_cardinality(self):
        # Simulate a choice type element with list cardinality
        element_types = [primitives.String]
        basename = "value"
        max_card = 99999
        fields = self.factory._construct_type_choice_fields(
            basename, element_types, max_card
        )
        assert "valueString" in fields
        field_type, field_info = fields["valueString"]
        assert field_type == Optional[List[primitives.String]]
        assert field_info.default is None

    def test_choice_type_with_required_cardinality(self):
        # Simulate a choice type element with required cardinality
        element_types = [primitives.Boolean]
        basename = "value"
        max_card = 1
        fields = self.factory._construct_type_choice_fields(
            basename, element_types, max_card
        )
        assert "valueBoolean" in fields
        field_type, field_info = fields["valueBoolean"]
        assert field_type == Optional[primitives.Boolean]


# ----------------------------------------------------------------
# _parse_element_cardinality()
# ----------------------------------------------------------------


class TestParseCardinalityConstraints(FactoryTestCase):

    @parameterized.expand(
        [
            (ElementDefinition.model_construct(min=0, max="0"), 0, 0),
            (ElementDefinition.model_construct(min=0, max="1"), 0, 1),
            (ElementDefinition.model_construct(min=1, max="2"), 1, 2),
            (ElementDefinition.model_construct(min=0, max="*"), 0, 99999),
        ]
    )
    def test_cardinality_constraints(self, element, expected_min, expected_max):
        min_card, max_card = self.factory._parse_element_cardinality(element)
        assert min_card == expected_min
        assert max_card == expected_max


# ----------------------------------------------------------------
# _construct_slice_model()
# ----------------------------------------------------------------


class TestConstructSliceModel(FactoryTestCase):
    """
    Unit tests for the ResourceFactory._construct_slice_model method, verifying correct construction of FHIR slice models.

    Dummy classes are used to simulate FHIR types, element definitions, and models for isolated testing.
    """

    class DummyType:
        profile = ["http://example.org/fhir/StructureDefinition/DummySlice"]

    class DummyElementDefinitionNode:
        def __init__(self, type_=None, short="A dummy slice", min_=1, max_="*"):
            self.type = type_ or []
            self.short = short
            self.min = min_
            self.max = max_

    class DummyBaseModel:
        pass

    class DummyFHIRSliceModel(FHIRSliceModel):
        pass

    def setUp(self):
        super().setUp()
        # Mock methods in ResourceFactory that are called by _construct_slice_model
        self.factory.construct_resource_model = mock.Mock(
            return_value=self.DummyFHIRSliceModel
        )
        self.factory._process_FHIR_structure_into_Pydantic_components = mock.Mock(
            return_value=({"field1": (str, None)}, ResourceFactoryValidators(), {})
        )
        self.factory._construct_model_with_properties = mock.Mock(
            return_value=self.DummyFHIRSliceModel
        )
        self.factory._parse_element_cardinality = mock.Mock(return_value=(1, 99999))

    def test_construct_slice_model_with_profile(self):
        definition = self.DummyElementDefinitionNode(type_=[self.DummyType()])
        result = self.factory._construct_slice_model("dummy-slice", definition, self.DummyBaseModel)  # type: ignore
        # Assertions
        self.factory.construct_resource_model.assert_called_once_with(  # type: ignore
            "http://example.org/fhir/StructureDefinition/DummySlice",
            base_model=FHIRSliceModel,
        )
        self.assertTrue(issubclass(result, self.DummyFHIRSliceModel))
        self.assertTrue(issubclass(result, FHIRSliceModel))
        self.assertEqual(result.min_cardinality, 1)
        self.assertEqual(result.max_cardinality, 99999)

    def test_construct_slice_model_without_profile(self):
        definition = self.DummyElementDefinitionNode(type_=[])
        result = self.factory._construct_slice_model("dummy-slice", definition, self.DummyBaseModel)  # type: ignore
        self.factory._process_FHIR_structure_into_Pydantic_components.assert_called_once()  # type: ignore
        # Assertions
        self.factory._construct_model_with_properties.assert_called_once()  # type: ignore
        self.assertTrue(issubclass(result, self.DummyFHIRSliceModel))
        self.assertTrue(issubclass(result, FHIRSliceModel))
        self.assertEqual(result.min_cardinality, 1)
        self.assertEqual(result.max_cardinality, 99999)

    def test_construct_slice_model_base_is_FHIRSliceModel(self):
        definition = self.DummyElementDefinitionNode(type_=[])
        result = self.factory._construct_slice_model("dummy-slice", definition, self.DummyFHIRSliceModel)  # type: ignore
        # Assertions
        self.factory._construct_model_with_properties.assert_called()  # type: ignore
        self.assertTrue(issubclass(result, self.DummyFHIRSliceModel))
        self.assertTrue(issubclass(result, FHIRSliceModel))
        self.assertEqual(result.min_cardinality, 1)
        self.assertEqual(result.max_cardinality, 99999)


# ----------------------------------------------------------------
# _construct_primitive_extension_field()
# ----------------------------------------------------------------


class TestConstructPrimitiveExtensionField(FactoryTestCase):
    """
    Unit tests for the _construct_primitive_extension_field method of the ResourceFactory.
    """

    def setUp(self):
        super().setUp()
        # Patch _handle_python_reserved_keyword to avoid alias logic for simplicity
        self.factory._handle_python_reserved_keyword = mock.Mock(
            side_effect=lambda name: (name, None)
        )

    def test_creates_extension_field_for_primitive(self):
        field_name = "name"
        fields = self.factory._construct_primitive_extension_field(field_name)
        # Should return a tuple (type, FieldInfo)
        assert "name_ext" in fields
        field = fields["name_ext"]
        assert isinstance(field, tuple)
        assert field[0] is Optional[complex_types.Element]
        assert isinstance(field[1], FieldInfo)
        assert field[1].default is None

    def test_extension_field_handles_reserved_keyword(self):
        # Simulate a field name that is a Python reserved keyword
        field_name = "class"
        # Patch to simulate reserved keyword handling
        self.factory._handle_python_reserved_keyword = mock.Mock(
            return_value=("class_", None)
        )
        fields = self.factory._construct_primitive_extension_field(field_name)
        assert "class_" in fields
        field = fields["class_"]
        assert isinstance(field, tuple)
        assert field[0] is Optional[complex_types.Element]
        assert isinstance(field[1], FieldInfo)
        assert field[1].default is None


# ----------------------------------------------------------------
# _resolve_content_reference()
# ----------------------------------------------------------------
class TestResolveContentReference(FactoryTestCase):
    """
    Unit tests for the _resolve_content_reference method of the ResourceFactory.
    """

    def setUp(self):
        super().setUp()

        self.root = ElementDefinitionNode(
            id="__root__",
            path="__root__",
            node_label="__root__",
            children={},
            slices={},
        )
        # Patch _build_element_tree_structure to return a mock tree
        self.mock_tree = ElementDefinitionNode(
            node_label="Patient",
            id="Patient",
            path="Patient",
            root=self.root,
            type=[ElementDefinitionType(code="Patient")],
            children={
                "gender": ElementDefinitionNode(
                    node_label="gender",
                    id="Patient.gender",
                    path="Patient.gender",
                    root=self.root,
                    children={},
                    type=[ElementDefinitionType(code="string")],
                    fixedString="female",
                ),
                "name": ElementDefinitionNode(
                    node_label="name",
                    id="Patient.name",
                    path="Patient.name",
                    root=self.root,
                    type=[ElementDefinitionType(code="BackboneElement")],
                    children={
                        "given": ElementDefinitionNode(
                            node_label="given",
                            id="Patient.name.given",
                            path="Patient.name.given",
                            root=self.root,
                            children={},
                            type=[ElementDefinitionType(code="string")],
                        ),
                        "family": ElementDefinitionNode(
                            node_label="family",
                            id="Patient.name.family",
                            path="Patient.name.family",
                            root=self.root,
                            children={},
                            type=[ElementDefinitionType(code="string")],
                        ),
                        "other": ElementDefinitionNode(
                            node_label="other",
                            id="Patient.name.other",
                            path="Patient.name.other",
                            root=self.root,
                            children={},
                            contentReference="#Patient.gender.name",
                        ),
                    },
                ),
                "address": ElementDefinitionNode(
                    node_label="address",
                    id="Patient.address",
                    path="Patient.address",
                    root=self.root,
                    children={},
                    type=[ElementDefinitionType(code="Address")],
                ),
            },
        )
        self.root.children = {"Patient": self.mock_tree}

    def test_resolves_valid_content_reference(self):
        # Simulate an element with a valid contentReference
        element = ElementDefinitionNode(
            path="dummy",
            node_label="dummy",
            contentReference="#Patient.gender",
            root=self.root,
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = self.factory._resolve_content_reference(element)
        assert isinstance(result, ElementDefinitionNode)
        assert result.node_label == "dummy"
        assert result.type == self.mock_tree.children["gender"].type
        assert result.fixedString == "female"

    def test_resolves_valid_content_reference_with_children(self):
        # Simulate an element with a valid contentReference
        element = ElementDefinitionNode(
            path="dummy",
            node_label="dummy",
            contentReference="#Patient.name",
            root=self.root,
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = self.factory._resolve_content_reference(element)
        assert isinstance(result, ElementDefinitionNode)
        assert result.node_label == "dummy"
        assert result.type == self.mock_tree.children["name"].type
        assert result.children == self.mock_tree.children["name"].children

    def test_resolves_content_reference_to_root(self):
        # Reference to the root node
        element = ElementDefinitionNode(
            path="dummy",
            node_label="dummy",
            contentReference="#Patient",
            root=self.root,
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = self.factory._resolve_content_reference(element)
        assert isinstance(result, ElementDefinitionNode)
        assert result.node_label == "dummy"
        assert result.type == self.mock_tree.type

    def test_returns_original_node_for_invalid_reference(self):
        # Reference to a non-existent node
        element = ElementDefinitionNode(
            path="dummy",
            node_label="dummy",
            contentReference="#Patient.nonexistent",
            root=self.root,
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = self.factory._resolve_content_reference(element)
        assert result is element

    def test_valid_url_content_reference(self):
        # Reference to a valid URL
        element = ElementDefinitionNode(
            path="dummy",
            node_label="dummy",
            contentReference="http://hl7.org/fhir/StructureDefinition/Observation#Observation.category",
            root=self.root,
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = self.factory._resolve_content_reference(element)
        assert isinstance(result, ElementDefinitionNode)
        assert result.node_label == "dummy"
        assert result.type == [ElementDefinitionType(code="CodeableConcept")]
        assert result.binding
        assert (
            result.binding.valueSet
            == "http://hl7.org/fhir/ValueSet/observation-category"
        )
