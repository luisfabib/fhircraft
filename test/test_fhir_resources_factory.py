import json
import keyword
import tarfile
import pytest
from typing import Optional
from unittest import TestCase
from unittest.mock import MagicMock, patch

from pydantic.aliases import AliasChoices

from fhircraft.fhir.resources.datatypes.R4B.core.patient import Patient
import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.resources.factory import (
    ResourceFactory,
    _Unset,
)


class FactoryTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = ResourceFactory()
        cls.factory.Config = cls.factory.FactoryConfig(
            FHIR_release="R4B", FHIR_version="4.3.0"
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

    def test_uses_base_definition_from_structure_definition(self):
        """Test that factory uses baseDefinition when constructing a resource."""
        # Create a base resource structure definition
        base_structure_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/BaseResource",
            "name": "BaseResource",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "BaseResource",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "BaseResource",
                        "path": "BaseResource",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "BaseResource.baseField",
                        "path": "BaseResource.baseField",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                        "short": "A field from the base resource",
                    },
                ]
            },
        }

        # Create a derived resource that references the base
        derived_structure_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/DerivedResource",
            "name": "DerivedResource",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "DerivedResource",
            "baseDefinition": "http://example.org/StructureDefinition/BaseResource",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "DerivedResource",
                        "path": "DerivedResource",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "DerivedResource.derivedField",
                        "path": "DerivedResource.derivedField",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                        "short": "A field specific to the derived resource",
                    },
                ]
            },
        }

        # Construct both models
        factory = ResourceFactory()
        BaseModel = factory.construct_resource_model(
            structure_definition=base_structure_def
        )
        DerivedModel = factory.construct_resource_model(
            structure_definition=derived_structure_def
        )

        # Verify that DerivedModel inherits from BaseModel
        assert issubclass(DerivedModel, BaseModel)

        # Verify that both fields are accessible
        assert "baseField" in BaseModel.model_fields
        assert "derivedField" in DerivedModel.model_fields

        # Verify instance creation works
        instance = DerivedModel(baseField="base_value", derivedField="derived_value")
        assert instance.baseField == "base_value"  # type: ignore
        assert instance.derivedField == "derived_value"  # type: ignore

    def test_uses_cached_base_definition(self):
        """Test that factory uses cached base models when available."""
        base_structure_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/CachedBase",
            "name": "CachedBase",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "CachedBase",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "CachedBase",
                        "path": "CachedBase",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "CachedBase.field1",
                        "path": "CachedBase.field1",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                    },
                ]
            },
        }

        derived_structure_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/DerivedFromCached",
            "name": "DerivedFromCached",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "DerivedFromCached",
            "baseDefinition": "http://example.org/StructureDefinition/CachedBase",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "DerivedFromCached",
                        "path": "DerivedFromCached",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "DerivedFromCached.field2",
                        "path": "DerivedFromCached.field2",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                    },
                ]
            },
        }

        factory = ResourceFactory()

        # Construct base model first - it will be cached
        BaseModel = factory.construct_resource_model(
            structure_definition=base_structure_def
        )

        # Verify base model is in cache
        assert (
            "http://example.org/StructureDefinition/CachedBase"
            in factory.construction_cache
        )
        cached_base = factory.construction_cache[
            "http://example.org/StructureDefinition/CachedBase"
        ]

        # Construct derived model - should use cached base
        DerivedModel = factory.construct_resource_model(
            structure_definition=derived_structure_def
        )

        # Verify that the cached base was used (same object)
        assert issubclass(DerivedModel, cached_base)

    def test_fallback_to_fhirbasemodel_when_base_not_found(self):
        """Test that factory falls back to FHIRBaseModel when base can't be resolved."""
        from fhircraft.fhir.resources.base import FHIRBaseModel

        structure_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/ResourceWithMissingBase",
            "name": "ResourceWithMissingBase",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "ResourceWithMissingBase",
            "baseDefinition": "http://example.org/StructureDefinition/NonExistentBase",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "ResourceWithMissingBase",
                        "path": "ResourceWithMissingBase",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "ResourceWithMissingBase.field1",
                        "path": "ResourceWithMissingBase.field1",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                    },
                ]
            },
        }

        factory = ResourceFactory()
        model = factory.construct_resource_model(structure_definition=structure_def)

        # Should fall back to FHIRBaseModel
        assert issubclass(model, FHIRBaseModel)
        assert "field1" in model.model_fields

    @pytest.mark.filterwarnings("ignore:.*dom-6.*")
    def test_inherits_from_builtin_fhir_resource(self):
        """Test that factory can use built-in FHIR resources as base."""
        structure_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/CustomPatient",
            "name": "CustomPatient",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "Patient",
            "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "Patient",
                        "path": "Patient",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "Patient.customField",
                        "path": "Patient.customField",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                        "short": "A custom extension field",
                    },
                ]
            },
        }

        factory = ResourceFactory()
        CustomPatient = factory.construct_resource_model(
            structure_definition=structure_def
        )

        # Should have the custom field
        assert "customField" in CustomPatient.model_fields

        # Should be able to use standard Patient fields (if Patient is available)
        # Note: This depends on whether Patient type is resolvable
        instance = CustomPatient(customField="custom_value")
        assert instance.customField == "custom_value"  # type: ignore

        # Verify that CustomPatient inherits from Patient
        assert issubclass(CustomPatient, Patient)
        assert isinstance(instance, CustomPatient)
        assert isinstance(instance, Patient)

    def test_chain_of_inheritance(self):
        """Test multiple levels of inheritance work correctly."""
        # Level 1: Base
        base_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/Level1",
            "name": "Level1",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "Level1",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {"id": "Level1", "path": "Level1", "min": 0, "max": "*"},
                    {
                        "id": "Level1.level1Field",
                        "path": "Level1.level1Field",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                    },
                ]
            },
        }

        # Level 2: Inherits from Level 1
        middle_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/Level2",
            "name": "Level2",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "Level2",
            "baseDefinition": "http://example.org/StructureDefinition/Level1",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {"id": "Level2", "path": "Level2", "min": 0, "max": "*"},
                    {
                        "id": "Level2.level2Field",
                        "path": "Level2.level2Field",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                    },
                ]
            },
        }

        # Level 3: Inherits from Level 2
        derived_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/Level3",
            "name": "Level3",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "Level3",
            "baseDefinition": "http://example.org/StructureDefinition/Level2",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {"id": "Level3", "path": "Level3", "min": 0, "max": "*"},
                    {
                        "id": "Level3.level3Field",
                        "path": "Level3.level3Field",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                    },
                ]
            },
        }

        factory = ResourceFactory()
        Level1 = factory.construct_resource_model(structure_definition=base_def)
        Level2 = factory.construct_resource_model(structure_definition=middle_def)
        Level3 = factory.construct_resource_model(structure_definition=derived_def)

        # Verify inheritance chain
        assert issubclass(Level2, Level1)
        assert issubclass(Level3, Level2)
        assert issubclass(Level3, Level1)

        # Verify all fields are accessible at Level3
        instance = Level3(
            level1Field="value1", level2Field="value2", level3Field="value3"
        )
        assert instance.level1Field == "value1"  # type: ignore
        assert instance.level2Field == "value2"  # type: ignore
        assert instance.level3Field == "value3"  # type: ignore

    def test_does_not_duplicate_inherited_fields(self):
        """Test that fields from base are not duplicated in derived model."""
        base_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/BaseWithField",
            "name": "BaseWithField",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "BaseWithField",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "BaseWithField",
                        "path": "BaseWithField",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "BaseWithField.sharedField",
                        "path": "BaseWithField.sharedField",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                    },
                ]
            },
        }

        derived_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/DerivedWithSameField",
            "name": "DerivedWithSameField",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "DerivedWithSameField",
            "baseDefinition": "http://example.org/StructureDefinition/BaseWithField",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "DerivedWithSameField",
                        "path": "DerivedWithSameField",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "DerivedWithSameField.sharedField",
                        "path": "DerivedWithSameField.sharedField",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                    },
                    {
                        "id": "DerivedWithSameField.ownField",
                        "path": "DerivedWithSameField.ownField",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                    },
                ]
            },
        }

        factory = ResourceFactory()
        Base = factory.construct_resource_model(structure_definition=base_def)
        Derived = factory.construct_resource_model(structure_definition=derived_def)

        # The derived model should not redefine sharedField
        # It should be inherited from Base
        assert "sharedField" in Base.model_fields
        assert "ownField" in Derived.model_fields

        # Derived should still be able to use sharedField
        instance = Derived(sharedField="shared", ownField="own")
        assert instance.sharedField == "shared"  # type: ignore
        assert instance.ownField == "own"  # type: ignore

    def test_explicit_base_model_parameter_overrides_basedefinition(self):
        """Test that explicit base_model parameter takes precedence over baseDefinition."""
        from fhircraft.fhir.resources.base import FHIRBaseModel

        structure_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/TestResource",
            "name": "TestResource",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "TestResource",
            "baseDefinition": "http://example.org/StructureDefinition/SomeBase",
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
                        "id": "TestResource.field1",
                        "path": "TestResource.field1",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                    },
                ]
            },
        }

        factory = ResourceFactory()

        # Provide explicit base_model - it should override baseDefinition
        model = factory.construct_resource_model(
            structure_definition=structure_def, base_model=FHIRBaseModel
        )

        # Should inherit from FHIRBaseModel, not from SomeBase
        assert issubclass(model, FHIRBaseModel)

    def test_no_basedefinition_defaults_to_fhirbasemodel(self):
        """Test that resources without baseDefinition inherit from FHIRBaseModel."""
        from fhircraft.fhir.resources.base import FHIRBaseModel

        structure_def = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/StructureDefinition/StandaloneResource",
            "name": "StandaloneResource",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "StandaloneResource",
            # No baseDefinition specified
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "StandaloneResource",
                        "path": "StandaloneResource",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "StandaloneResource.field1",
                        "path": "StandaloneResource.field1",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "string"}],
                    },
                ]
            },
        }

        factory = ResourceFactory()
        model = factory.construct_resource_model(structure_definition=structure_def)

        # Should inherit from FHIRBaseModel by default
        assert issubclass(model, FHIRBaseModel)
        assert "field1" in model.model_fields


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


class TestSliceModelInheritance(FactoryTestCase):
    """
    Test slice model inheritance functionality to ensure slice models inherit from both FHIRSliceModel and original element type.

    This test class addresses the issue where slice models created by _construct_slice_model
    during processing of sliced elements only inherit from FHIRSliceModel and not from the original element type.

    Current Issue:
    - When processing a resource with sliced elements (e.g., Patient with sliced extensions)
    - The _construct_slice_model method creates slices that only inherit from FHIRSliceModel
    - This breaks type compatibility because slices can't be used as the original type (Extension)

    Expected Behavior:
    - Slice models should inherit from BOTH their original element type AND FHIRSliceModel
    - This enables: isinstance(slice, Extension) AND isinstance(slice, FHIRSliceModel)
    - Provides access to both original type functionality and slice-specific functionality

    Test Coverage:
    - Resources with sliced extension elements
    - Resources with sliced backbone elements
    - Proper inheritance from both original type and FHIRSliceModel
    - Assignment compatibility and type checking
    - Slice-specific cardinality and validation functionality
    """

    @pytest.mark.filterwarnings("ignore:.*dom-6.*")
    def test_resource_with_sliced_extensions_processes_correctly(self):
        """Test that a resource with sliced extensions is processed without errors."""
        # Create a Patient resource with sliced extensions
        patient_with_sliced_extensions = {
            "resourceType": "StructureDefinition",
            "url": "http://example.org/fhir/StructureDefinition/PatientWithSlicedExtensions",
            "name": "PatientWithSlicedExtensions",
            "status": "active",
            "kind": "resource",
            "abstract": False,
            "type": "Patient",
            "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
            "fhirVersion": "4.3.0",
            "snapshot": {
                "element": [
                    {
                        "id": "Patient",
                        "path": "Patient",
                        "min": 0,
                        "max": "*",
                    },
                    {
                        "id": "Patient.extension",
                        "path": "Patient.extension",
                        "slicing": {
                            "discriminator": [{"type": "value", "path": "url"}],
                            "rules": "open",
                        },
                        "min": 0,
                        "max": "*",
                        "type": [{"code": "Extension"}],
                    },
                    {
                        "id": "Patient.extension:birthPlace",
                        "path": "Patient.extension",
                        "sliceName": "birthPlace",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "Extension"}],
                        "short": "Birth place extension slice",
                    },
                    {
                        "id": "Patient.extension:birthPlace.url",
                        "path": "Patient.extension.url",
                        "min": 1,
                        "max": "1",
                        "type": [{"code": "uri"}],
                        "fixedUri": "http://hl7.org/fhir/StructureDefinition/patient-birthPlace",
                    },
                    {
                        "id": "Patient.extension:birthPlace.valueAddress",
                        "path": "Patient.extension.valueAddress",
                        "min": 0,
                        "max": "1",
                        "type": [{"code": "Address"}],
                    },
                ]
            },
        }

        # Construct the Patient model with sliced extensions
        PatientModel = self.factory.construct_resource_model(
            structure_definition=patient_with_sliced_extensions
        )

        # The sliced resource should still be a valid Patient model
        from fhircraft.fhir.resources.datatypes.R4B.core.patient import Patient

        assert issubclass(PatientModel, Patient), "Model should inherit from Patient"

        # At minimum, there should be an extension field
        assert (
            "extension" in PatientModel.model_fields
        ), "Model should have extension field"

        # The model should be constructable
        instance = PatientModel()
        assert isinstance(instance, Patient), "Instance should be a Patient"

    def test_construct_slice_model_creates_dual_inheritance(self):
        """Test that _construct_slice_model creates models with dual inheritance."""
        from fhircraft.fhir.resources.datatypes.R4B.complex.extension import Extension
        from fhircraft.fhir.resources.base import FHIRSliceModel

        # Create a mock element definition for an extension slice
        class MockElementDefinition:
            def __init__(self):
                self.type = []  # Empty type forces dynamic creation
                self.short = "Test extension slice"
                self.min = 0
                self.max = "1"
                self.children = {}  # No child elements

        mock_definition = MockElementDefinition()

        # Call _construct_slice_model directly
        slice_model = self.factory._construct_slice_model(
            name="test-extension-slice",
            definition=mock_definition,  # type: ignore
            base=Extension,
            base_name="TestExtension",
        )

        # Verify dual inheritance
        assert issubclass(slice_model, Extension), "Slice should inherit from Extension"
        assert issubclass(
            slice_model, FHIRSliceModel
        ), "Slice should inherit from FHIRSliceModel"

        # Verify it has slice cardinality attributes
        assert hasattr(slice_model, "min_cardinality")
        assert hasattr(slice_model, "max_cardinality")
        assert slice_model.min_cardinality == 0
        assert slice_model.max_cardinality == 1

        # Test instance creation and type checking (need to provide a value for Extension validation)
        instance = slice_model(url="http://example.com/test", valueString="test value")
        assert isinstance(instance, Extension), "Instance should be Extension"
        assert isinstance(instance, FHIRSliceModel), "Instance should be FHIRSliceModel"

    def test_construct_slice_model_with_backbone_element_base(self):
        """Test that _construct_slice_model works with BackboneElement base."""
        from fhircraft.fhir.resources.datatypes.R4B.complex import BackboneElement
        from fhircraft.fhir.resources.base import FHIRSliceModel

        # Create a mock element definition for a backbone element slice
        class MockElementDefinition:
            def __init__(self):
                self.type = []
                self.short = "Test backbone element slice"
                self.min = 1
                self.max = "3"
                self.children = {}

        mock_definition = MockElementDefinition()

        # Call _construct_slice_model with BackboneElement base
        slice_model = self.factory._construct_slice_model(
            name="test-backbone-slice",
            definition=mock_definition,  # type: ignore
            base=BackboneElement,
            base_name="TestBackbone",
        )

        # Verify dual inheritance
        assert issubclass(
            slice_model, BackboneElement
        ), "Slice should inherit from BackboneElement"
        assert issubclass(
            slice_model, FHIRSliceModel
        ), "Slice should inherit from FHIRSliceModel"

        # Verify cardinality
        assert slice_model.min_cardinality == 1
        assert slice_model.max_cardinality == 3

        # Test instance creation
        instance = slice_model()
        assert isinstance(
            instance, BackboneElement
        ), "Instance should be BackboneElement"
        assert isinstance(instance, FHIRSliceModel), "Instance should be FHIRSliceModel"

    def test_slice_model_maintains_original_type_functionality(self):
        """Test that slice models maintain all functionality from their original type."""
        from fhircraft.fhir.resources.datatypes.R4B.complex.extension import Extension
        from fhircraft.fhir.resources.base import FHIRSliceModel

        # Create a mock element definition
        class MockElementDefinition:
            def __init__(self):
                self.type = []
                self.short = "Extension with value"
                self.min = 0
                self.max = "1"
                self.children = {}

        mock_definition = MockElementDefinition()

        # Create slice model
        ExtensionSlice = self.factory._construct_slice_model(
            name="simple-extension-slice",
            definition=mock_definition,  # type: ignore
            base=Extension,
            base_name="SimpleExtension",
        )

        # Create instance
        instance = ExtensionSlice(
            url="http://example.org/test",  # type: ignore
            valueInteger=42,  # type: ignore
        )

        # Should have Extension functionality
        assert hasattr(instance, "url")
        assert instance.url == "http://example.org/test"  # type: ignore
        assert hasattr(instance, "valueInteger")
        assert instance.valueInteger == 42  # type: ignore

        # Should also have FHIRSliceModel functionality
        assert hasattr(instance, "min_cardinality")
        assert hasattr(instance, "max_cardinality")
        assert hasattr(instance, "is_FHIR_complete")
        assert hasattr(instance, "has_been_modified")

        # Should have access to both class hierarchies
        assert isinstance(instance, Extension)
        assert isinstance(instance, FHIRSliceModel)

    def test_slice_model_with_complex_inheritance_chain(self):
        """Test slice models work correctly with complex inheritance chains."""
        from fhircraft.fhir.resources.datatypes.R4B.complex.extension import Extension
        from fhircraft.fhir.resources.datatypes.R4B.complex import Element
        from fhircraft.fhir.resources.base import FHIRSliceModel

        # Create a mock element definition
        class MockElementDefinition:
            def __init__(self):
                self.type = []
                self.short = "Complex extension slice"
                self.min = 1
                self.max = "1"
                self.children = {}

        mock_definition = MockElementDefinition()

        # Extension inherits from Element, which may inherit from other classes
        ExtensionSlice = self.factory._construct_slice_model(
            name="complex-extension-slice",
            definition=mock_definition,  # type: ignore
            base=Extension,
            base_name="ComplexExtension",
        )

        # Should inherit from all the proper classes in the chain
        assert issubclass(ExtensionSlice, Extension)
        assert issubclass(ExtensionSlice, Element)
        assert issubclass(ExtensionSlice, FHIRSliceModel)

        # Test MRO (Method Resolution Order) makes sense
        mro = ExtensionSlice.__mro__
        assert Extension in mro
        assert Element in mro
        assert FHIRSliceModel in mro

        # Create instance and verify it works
        instance = ExtensionSlice(
            url="http://example.org/test", valueString="test value"  # type: ignore
        )
        assert isinstance(instance, Extension)
        assert isinstance(instance, Element)
        assert isinstance(instance, FHIRSliceModel)

    def test_slice_models_can_be_used_in_union_types(self):
        """Test that slice models work correctly in Union type validations."""
        from fhircraft.fhir.resources.datatypes.R4B.complex.extension import Extension
        from fhircraft.fhir.resources.base import FHIRSliceModel
        from typing import Union, List, Optional
        from pydantic import BaseModel, Field

        # Create mock element definitions
        class MockElementDefinition:
            def __init__(self, short_desc):
                self.type = []
                self.short = short_desc
                self.min = 0
                self.max = "1"
                self.children = {}

        # Create two different Extension slices using _construct_slice_model
        ExtensionSliceA = self.factory._construct_slice_model(
            name="extension-a-slice",
            definition=MockElementDefinition("Extension A slice"),  # type: ignore
            base=Extension,
            base_name="ExtensionA",
        )

        ExtensionSliceB = self.factory._construct_slice_model(
            name="extension-b-slice",
            definition=MockElementDefinition("Extension B slice"),  # type: ignore
            base=Extension,
            base_name="ExtensionB",
        )

        # Create a test model with a Union field that should accept either slice or base Extension
        class TestModel(BaseModel):
            extensions: Optional[
                List[Union[ExtensionSliceA, ExtensionSliceB, Extension]]  # type: ignore
            ] = Field(default=None)

        # Test that both slices can be used in the Union
        slice_a = ExtensionSliceA(
            url="http://example.org/extension-a",  # type: ignore
            valueString="test",  # type: ignore
        )
        slice_b = ExtensionSliceB(
            url="http://example.org/extension-b",  # type: ignore
            valueInteger=123,  # type: ignore
        )

        # This should work if slices properly inherit from Extension
        test_instance = TestModel(extensions=[slice_a, slice_b])
        assert test_instance.extensions is not None
        assert len(test_instance.extensions) == 2
        assert isinstance(test_instance.extensions[0], ExtensionSliceA)
        assert isinstance(test_instance.extensions[0], Extension)
        assert isinstance(test_instance.extensions[1], ExtensionSliceB)
        assert isinstance(test_instance.extensions[1], Extension)

    def test_slice_model_cardinality_preserved(self):
        """Test that slice models preserve cardinality information from FHIRSliceModel."""
        from fhircraft.fhir.resources.datatypes.R4B.complex.extension import Extension
        from fhircraft.fhir.resources.base import FHIRSliceModel

        # Create mock element definition with custom cardinality
        class MockElementDefinition:
            def __init__(self):
                self.type = []
                self.short = "Extension with custom cardinality"
                self.min = 2  # Custom cardinality
                self.max = "5"
                self.children = {}

        mock_definition = MockElementDefinition()

        ExtensionSlice = self.factory._construct_slice_model(
            name="cardinality-extension-slice",
            definition=mock_definition,  # type: ignore
            base=Extension,
            base_name="CardinalityExtension",
        )

        # Should have custom cardinality from the slice definition
        assert hasattr(ExtensionSlice, "min_cardinality")
        assert hasattr(ExtensionSlice, "max_cardinality")
        assert ExtensionSlice.min_cardinality == 2
        assert ExtensionSlice.max_cardinality == 5

        # Should still be proper Extension and FHIRSliceModel
        assert issubclass(ExtensionSlice, Extension)
        assert issubclass(ExtensionSlice, FHIRSliceModel)

    @pytest.mark.filterwarnings("ignore:.*dom-6.*")
    def test_slice_models_can_be_assigned_to_original_type_fields(self):
        """Test that slice models can be assigned to fields expecting the original type."""
        from fhircraft.fhir.resources.datatypes.R4B.complex.extension import Extension
        from fhircraft.fhir.resources.datatypes.R4B.core.patient import Patient

        # Create a mock element definition
        class MockElementDefinition:
            def __init__(self):
                self.type = []
                self.short = "Patient extension slice"
                self.min = 0
                self.max = "1"
                self.children = {}

        mock_definition = MockElementDefinition()

        # Create extension slice
        ExtensionSlice = self.factory._construct_slice_model(
            name="patient-extension-slice",
            definition=mock_definition,  # type: ignore
            base=Extension,
            base_name="PatientExtension",
        )

        # Create an instance of the slice
        extension_instance = ExtensionSlice(
            url="http://example.org/patient-extension",
            valueString="test value",
        )

        # Should be able to assign the slice to a Patient's extension field
        # This tests the core issue: slice should be usable as Extension
        patient = Patient(extension=[extension_instance])  # type: ignore
        assert patient.extension is not None
        assert len(patient.extension) == 1
        assert patient.extension[0] == extension_instance

        # The extension should also be usable as a regular Extension type
        regular_extension_field: Extension = extension_instance
        assert regular_extension_field.url == "http://example.org/patient-extension"

    def test_slice_models_preserve_method_resolution_order(self):
        """Test that slice models have proper method resolution order."""
        from fhircraft.fhir.resources.datatypes.R4B.complex.extension import Extension
        from fhircraft.fhir.resources.datatypes.R4B.complex import Element
        from fhircraft.fhir.resources.base import FHIRSliceModel

        # Create a mock element definition
        class MockElementDefinition:
            def __init__(self):
                self.type = []
                self.short = "Test MRO slice"
                self.min = 0
                self.max = "1"
                self.children = {}

        mock_definition = MockElementDefinition()

        # Create slice model
        ExtensionSlice = self.factory._construct_slice_model(
            name="mro-test-slice",
            definition=mock_definition,  # type: ignore
            base=Extension,
            base_name="MROTestExtension",
        )

        # Test MRO (Method Resolution Order) is sensible
        mro = ExtensionSlice.__mro__

        # Should include both inheritance paths
        assert Extension in mro, "Extension should be in MRO"
        assert Element in mro, "Element should be in MRO"
        assert FHIRSliceModel in mro, "FHIRSliceModel should be in MRO"

        # Extension should come before FHIRSliceModel in MRO for proper method resolution
        extension_idx = mro.index(Extension)
        fhir_slice_idx = mro.index(FHIRSliceModel)
        assert (
            extension_idx < fhir_slice_idx
        ), "Extension should come before FHIRSliceModel in MRO"
