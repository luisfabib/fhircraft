import json
import tarfile
import tempfile
from typing import List, Optional, get_args
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from parameterized import parameterized, parameterized_class
from pydantic import Field
from pydantic.fields import FieldInfo

import fhircraft.fhir.resources.datatypes.primitives as primitives
import fhircraft.fhir.resources.datatypes.R4B.complex_types as complex_types
from fhircraft.fhir.resources.definitions import StructureDefinition
from fhircraft.fhir.resources.definitions.element_definition import ElementDefinition
from fhircraft.fhir.resources.factory import ResourceFactory, _Unset
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
