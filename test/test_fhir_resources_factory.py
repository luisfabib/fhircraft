import json
import keyword
import tarfile
import tempfile
import warnings
from typing import List, Optional, get_args, Any
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from parameterized import parameterized, parameterized_class
from pydantic import Field
from pydantic.aliases import AliasChoices
from pydantic.fields import FieldInfo
import pytest

import fhircraft.fhir.resources.datatypes.primitives as primitives
import fhircraft.fhir.resources.datatypes.R4B.complex_types as complex_types
from fhircraft.fhir.resources.definitions import StructureDefinition, StructureDefinitionSnapshot
from fhircraft.fhir.resources.definitions.element_definition import ElementDefinition, ElementDefinitionType
from fhircraft.fhir.resources.factory import ResourceFactory, _Unset, ElementDefinitionNode
from fhircraft.fhir.resources.repository import CompositeStructureDefinitionRepository


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
        element_type = ElementDefinitionType(code="string")
        result = self.factory._get_complex_FHIR_type(element_type)
        assert result == primitives.String

    def test_parses_fhir_primitive_datatype_as_string(self):
        result = self.factory._get_complex_FHIR_type("string")
        assert result == primitives.String

    def test_parses_fhir_complex_datatype(self):
        element_type = ElementDefinitionType(code="Coding")
        result = self.factory._get_complex_FHIR_type(element_type)
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
        
    def test_parses_fhir_profiled_type(self):
        profile_url = "http://example.org/fhir/StructureDefinition/CustomType"
        element_type = ElementDefinitionType(code="CustomType", profile=[profile_url])
        self.factory.repository.load_from_definitions(
            StructureDefinition(
                resourceType="StructureDefinition",
                url=profile_url,
                name="CustomType",
                version="1.0.0",
                status="active",
                kind="complex-type",
                abstract=False,
                type="BackboneElement",
                baseDefinition="http://hl7.org/fhir/StructureDefinition/BackboneElement",
                derivation="specialization",
                snapshot=StructureDefinitionSnapshot.model_validate({
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
                }),
            )
        )
        result = self.factory._get_complex_FHIR_type(
            element_type
        )
        assert result == self.factory.construction_cache[profile_url]

    def test_returns_field_type_name_if_not_found(self):
        with pytest.raises(RuntimeError):
            self.factory._get_complex_FHIR_type("UnknownType")


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
        assert result[1].is_required() == False

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
        assert result[1].is_required() == False

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


class TestConstructPydanticFieldWithValidationAlias(FactoryTestCase):
    """Test the _construct_Pydantic_field method with validation_alias parameter."""

    def test_constructs_field_with_validation_alias(self):
        """Test that fields can be constructed with validation aliases."""
        field_type = primitives.String
        validation_alias = AliasChoices("class", "class_")

        result = self.factory._construct_Pydantic_field(
            field_type, min_card=1, max_card=1, validation_alias=validation_alias
        )

        assert result[0] == field_type
        assert result[1].validation_alias == validation_alias

    def test_constructs_field_without_validation_alias(self):
        """Test that fields can still be constructed without validation aliases."""
        field_type = primitives.String

        result = self.factory._construct_Pydantic_field(
            field_type, min_card=1, max_card=1
        )

        assert result[0] == field_type
        assert result[1].validation_alias is None

    def test_constructs_field_with_both_alias_and_validation_alias(self):
        """Test that fields can have both alias and validation_alias."""
        field_type = primitives.String
        validation_alias = AliasChoices("class", "class_")
        alias = "_class"

        result = self.factory._construct_Pydantic_field(
            field_type,
            min_card=1,
            max_card=1,
            alias=alias,
            validation_alias=validation_alias,
        )

        assert result[0] == field_type
        assert result[1].alias == alias
        assert result[1].validation_alias == validation_alias


class TestPythonKeywordHandlingIntegration(FactoryTestCase):
    """Integration tests for Python keyword handling in resource construction."""

    def test_constructs_model_with_keyword_field_names(self):
        """Test that models can be constructed with keyword field names."""
        # Create a structure definition with a reserved keyword field
        structure_def_dict = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/TestResource",
            "name": "TestResource",
            "description": "A test resource",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "TestResource",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "TestResource",
                        "path": "TestResource",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "TestResource.class",
                        "path": "TestResource.class",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                        "short": "A class field",
                    },
                    {
                        "id": "TestResource.import",
                        "path": "TestResource.import",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                        "short": "An import field",
                    },
                ]
            },
        }

        # Construct the model
        model = self.factory.construct_resource_model(
            structure_definition=structure_def_dict
        )

        # Check that the model was created successfully
        assert model is not None
        assert hasattr(model, "model_fields")

        # Check that keyword fields were renamed with underscore suffix
        fields = model.model_fields
        assert "class_" in fields
        assert "import_" in fields
        assert "class" not in fields  # Original keyword should not be a field name
        assert "import" not in fields  # Original keyword should not be a field name

        # Check that validation aliases were set correctly
        class_field = fields["class_"]
        import_field = fields["import_"]

        assert model.__doc__ == "A test resource"

        assert class_field.validation_alias is not None
        assert import_field.validation_alias is not None
        assert isinstance(class_field.validation_alias, AliasChoices)
        assert isinstance(import_field.validation_alias, AliasChoices)

    def test_model_accepts_both_keyword_and_safe_field_names(self):
        """Test that the constructed model accepts both original and safe field names."""
        # Create a simple structure definition with a keyword field
        structure_def_dict = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/TestResource",
            "name": "TestResource",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "TestResource",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "TestResource",
                        "path": "TestResource",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "TestResource.class",
                        "path": "TestResource.class",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                        "short": "A class field",
                    },
                ]
            },
        }

        # Construct the model
        TestModel = self.factory.construct_resource_model(
            structure_definition=structure_def_dict
        )

        assert "class_" in TestModel.model_fields
        # Using the safe field name
        instance1 = TestModel(**{"class_": "test_value"})
        # Using the original keyword name (should work due to validation_alias)
        instance2 = TestModel(**{"class": "test_value"})
        assert getattr(instance1, 'class_') == "test_value"
        assert getattr(instance2, 'class_') == "test_value"

    def test_handles_choice_type_fields_with_keywords(self):
        """Test that choice type fields with keywords are handled correctly."""
        structure_def_dict = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/TestResource",
            "name": "TestResource",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "TestResource",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "TestResource",
                        "path": "TestResource",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "TestResource.class[x]",
                        "path": "TestResource.class[x]",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}, {"code": "boolean"}],
                        "short": "A choice type field with keyword name",
                    },
                ]
            },
        }

        # Construct the model
        model = self.factory.construct_resource_model(
            structure_definition=structure_def_dict
        )

        # Check that choice type fields were created with safe names
        fields = model.model_fields

        # Should have fields like classString_ instead of classString (since class is a keyword)
        choice_fields = [
            field_name
            for field_name in fields.keys()
            if field_name.startswith("class") and field_name != "class_"
        ]
        assert len(choice_fields) > 0

        # The choice fields should be safe (not starting with reserved keywords)
        for field_name in choice_fields:
            # Since 'class' is a keyword, the choice fields should be renamed
            assert not keyword.iskeyword(field_name)

    def test_handles_extension_fields_with_keywords(self):
        """Test that extension fields (_ext suffix) with keywords are handled correctly."""
        structure_def_dict = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/TestResource",
            "name": "TestResource",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "TestResource",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "TestResource",
                        "path": "TestResource",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "TestResource.for",
                        "path": "TestResource.for",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                        "short": "A primitive field with keyword name",
                    },
                ]
            },
        }

        # Construct the model
        model = self.factory.construct_resource_model(
            structure_definition=structure_def_dict
        )

        # Check that both the main field and extension field were created with safe names
        fields = model.model_fields

        assert "for_" in fields
        assert "for_ext" in fields



class TestResourceFactoryPackageMethods(TestCase):
    """Test ResourceFactory package-related methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory_with_packages = ResourceFactory(
            enable_packages=True, internet_enabled=False
        )
        self.factory_without_packages = ResourceFactory(
            enable_packages=False, internet_enabled=False
        )

    def test_load_package_without_package_support(self):
        """Test load_package raises error when package support is disabled."""
        with self.assertRaises(RuntimeError):
            self.factory_without_packages.load_package("test.package")

    def test_get_loaded_packages_without_package_support(self):
        """Test get_loaded_packages returns empty dict when package support is disabled."""
        result = self.factory_without_packages.get_loaded_packages()
        assert result == {}

    def test_has_package_without_package_support(self):
        """Test has_package returns False when package support is disabled."""
        result = self.factory_without_packages.has_package("test.package")
        assert result is False

    def test_remove_package_without_package_support(self):
        """Test remove_package does nothing when package support is disabled."""
        # Should not raise an exception
        self.factory_without_packages.remove_package("test.package")

    def test_set_registry_base_url_without_package_support(self):
        """Test set_registry_base_url raises error when package support is disabled."""
        with self.assertRaises(RuntimeError) as context:
            self.factory_without_packages.set_registry_base_url("https://example.com")

    def test_clear_package_cache_without_package_support(self):
        """Test clear_package_cache does nothing when package support is disabled."""
        # Should not raise an exception
        self.factory_without_packages.clear_package_cache()

    def test_get_loaded_packages_with_package_support(self):
        """Test get_loaded_packages works when package support is enabled."""
        result = self.factory_with_packages.get_loaded_packages()
        assert isinstance(result, dict)
        assert len(result) == 0  # Should be empty initially

    def test_has_package_with_package_support(self):
        """Test has_package works when package support is enabled."""
        result = self.factory_with_packages.has_package("nonexistent.package")
        assert result is False

    def test_set_registry_base_url_with_package_support(self):
        """Test set_registry_base_url works when package support is enabled."""
        # Should not raise an exception
        self.factory_with_packages.set_registry_base_url("https://example.com")

    def test_clear_package_cache_with_package_support(self):
        """Test clear_package_cache works when package support is enabled."""
        # Should not raise an exception
        self.factory_with_packages.clear_package_cache()

    @patch("fhircraft.fhir.packages.client.FHIRPackageRegistryClient.download_package")
    def test_load_package_success(self, mock_download):
        """Test successful package loading."""
        # Create mock tar file with sample StructureDefinition
        mock_tar = MagicMock(spec=tarfile.TarFile)
        mock_member = MagicMock()
        mock_member.isfile.return_value = True
        mock_member.name = "package/StructureDefinition-Patient.json"

        sample_patient = {
            "resourceType": "StructureDefinition",
            "url": "http://hl7.org/fhir/StructureDefinition/Patient",
            "version": "4.0.0",
            "name": "Patient",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "Patient",
            "baseDefinition": "http://hl7.org/fhir/StructureDefinition/DomainResource",
            "derivation": "specialization",
            "snapshot": {
                "element": [{"id": "Patient", "path": "Patient", "min": 0, "max": "*"}]
            },
        }

        mock_file = MagicMock()
        mock_file.read.return_value = json.dumps(sample_patient).encode("utf-8")

        mock_tar.getmembers.return_value = [mock_member]
        mock_tar.extractfile.return_value = mock_file
        mock_download.return_value = mock_tar

        # Enable internet for this test
        factory_with_internet = ResourceFactory(
            enable_packages=True, internet_enabled=True
        )

        # Load package
        factory_with_internet.load_package("test.package", "1.0.0")

        # Verify results
        mock_download.assert_called_once_with("test.package", "1.0.0", extract=True)
        result = factory_with_internet.get_loaded_packages()
        assert len(result) == 1

    def test_load_package_internet_disabled(self):
        """Test load_package fails when internet is disabled."""
        with self.assertRaises(RuntimeError) as context:
            self.factory_with_packages.load_package("test.package")

        self.assertIn("internet access is disabled", str(context.exception).lower())


class TestContentReferenceResolution(FactoryTestCase):
    """Test cases for contentReference resolution functionality."""

    def setUp(self):
        super().setUp()
        # Create a mock root structure for testing
        self.root_structure = ElementDefinitionNode(
            id="TestResource",
            path="TestResource",
            node_label="TestResource",
            children={},
            slices={},
            root=None
        )
        self.root_structure.root = self.root_structure

    def test_resolve_content_reference_type_simple(self):
        """Test resolving a simple contentReference to a primitive type."""
        # Create referenced element with primitive type
        referenced_element = ElementDefinitionNode(
            id="TestResource.targetField",
            path="TestResource.targetField",
            node_label="targetField",
            type=[ElementDefinitionType(code="string")],
            children={},
            slices={}
        )
        self.root_structure.children["targetField"] = referenced_element
        
        # Test resolution
        resolved_type = self.factory._resolve_content_reference_type(
            referenced_element, self.root_structure
        )
        
        self.assertEqual(resolved_type, primitives.String)

    def test_resolve_content_reference_type_complex_with_children(self):
        """Test resolving contentReference to an element with children (backbone element)."""
        # Create referenced element with children
        referenced_element = ElementDefinitionNode(
            id="TestResource.backboneField",
            path="TestResource.backboneField",
            node_label="backboneField",
            children={
                "subField": ElementDefinitionNode(
                    id="TestResource.backboneField.subField",
                    path="TestResource.backboneField.subField",
                    node_label="subField",
                    type=[ElementDefinitionType(code="string")],
                    children={},
                    slices={}
                )
            },
            slices={}
        )
        self.root_structure.children["backboneField"] = referenced_element
        
        # Test resolution
        resolved_type = self.factory._resolve_content_reference_type(
            referenced_element, self.root_structure
        )
        
        # Should create a backbone model
        self.assertTrue(hasattr(resolved_type, '__name__'))
        self.assertTrue(hasattr(resolved_type, 'model_fields'))
        self.assertIn('subField', resolved_type.model_fields)

    def test_content_reference_with_invalid_path(self):
        """Test handling of contentReference with invalid path."""
        # Create structure with invalid contentReference
        structure = ElementDefinitionNode(
            id="TestResource",
            path="TestResource",
            node_label="TestResource",
            children={
                "invalidRefField": ElementDefinitionNode(
                    id="TestResource.invalidRefField",
                    path="TestResource.invalidRefField",
                    node_label="invalidRefField",
                    contentReference="#TestResource.nonExistentField",
                    children={},
                    slices={}
                )
            },
            slices={},
            root=None
        )
        structure.root = structure
        structure.children["invalidRefField"].root = structure
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            fields, _, _ = self.factory._process_FHIR_structure_into_Pydantic_components(structure)
            
            # Should create field with Any type and generate warning
            self.assertIn("invalidRefField", fields)
            self.assertTrue(len(w) > 0)
            self.assertIn("Could not resolve content reference", str(w[0].message))

    def test_construct_resource_model_with_content_reference(self):
        """Test complete resource model construction with contentReference."""
        mock_structure_definition = {
            "resourceType": "StructureDefinition",
            "id": "test-content-ref",
            "url": "http://example.org/StructureDefinition/test-content-ref",
            "name": "TestContentRef",
            "status": "draft",
            "fhirVersion": "4.0.1",
            "kind": "resource",
            "abstract": False,
            "type": "TestResource",
            "baseDefinition": "http://hl7.org/fhir/StructureDefinition/DomainResource",
            "derivation": "specialization",
            "snapshot": {
                "element": [
                    {
                        "id": "TestResource",
                        "path": "TestResource",
                        "min": 0,
                        "max": "*",
                        "base": {"path": "TestResource", "min": 0, "max": "*"},
                        "type": [{"code": "DomainResource"}]
                    },
                    {
                        "id": "TestResource.earlyField",
                        "path": "TestResource.earlyField",
                        "min": 0,
                        "max": "1",
                        "contentReference": "#TestResource.laterField"
                    },
                    {
                        "id": "TestResource.laterField",
                        "path": "TestResource.laterField",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}]
                    }
                ]
            }
        }
        
        # Should not raise exception
        model = self.factory.construct_resource_model(
            structure_definition=mock_structure_definition
        )
        
        self.assertEqual(model.__name__, "TestContentRef")
        self.assertIn('earlyField', model.model_fields)
        self.assertIn('laterField', model.model_fields)
