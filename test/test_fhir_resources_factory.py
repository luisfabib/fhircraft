import json
import keyword
import tarfile
import tempfile
import warnings
from typing import Any, List, Optional, get_args
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

import pytest
from parameterized import parameterized, parameterized_class
from pydantic import Field
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
    ResourceFactory,
    _Unset,
)
from fhircraft.fhir.resources.repository import CompositeStructureDefinitionRepository


class FactoryTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = ResourceFactory()
        cls.factory.Config = cls.factory.FactoryConfig(
            FHIR_release="R4B", resource_name="Test", FHIR_version="4.3.0"
        )


class TestConstructPydanticFieldWithValidationAlias(FactoryTestCase):
    """Test the _construct_Pydantic_field method with validation_alias parameter."""

    def test_constructs_field_with_validation_alias(self):
        """Test that fields can be constructed with validation aliases."""
        field_type = primitives.String
        validation_alias = AliasChoices("class", "class_")

        result = self.factory._construct_Pydantic_field(
            field_type, min_card=1, max_card=1, validation_alias=validation_alias
        )

        assert result[0] == Optional[field_type]
        assert result[1].validation_alias == validation_alias

    def test_constructs_field_without_validation_alias(self):
        """Test that fields can still be constructed without validation aliases."""
        field_type = primitives.String

        result = self.factory._construct_Pydantic_field(
            field_type, min_card=1, max_card=1
        )

        assert result[0] == Optional[field_type]
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

        assert result[0] == Optional[field_type]
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
        assert getattr(instance1, "class_") == "test_value"
        assert getattr(instance2, "class_") == "test_value"

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
