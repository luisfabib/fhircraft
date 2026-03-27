import json
import keyword
import tarfile
from annotated_types import MaxLen, MinLen
import pytest
from typing import Optional, List, Union
from unittest.mock import MagicMock, patch

from pydantic.aliases import AliasChoices
from pydantic import ValidationError, Field
from fhircraft.fhir.resources.base import FHIRBaseModel

from fhircraft.fhir.resources.datatypes.R4B.core.patient import Patient
import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.resources.factory import (
    FHIRModelFactory,
)
from fhircraft.fhir.resources.base import FHIRBaseModel, BaseModel
from fhircraft.fhir.resources.datatypes.R4B.core import StructureDefinition
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Extension,
    BackboneElement,
    Element,
)
from fhircraft.fhir.resources.base import FHIRSliceModel


class MockType:
    profile = ["http://example.org/fhir/StructureDefinition/DummySlice"]


class MockElementDefinitionNode:
    def __init__(self, definition, children=None, slices=None):
        self.definition = definition
        self.children = children or dict()
        self.slices = slices or dict()


class MockElementDefinition:
    def __init__(
        self,
        type=None,
        short="A dummy slice",
        min=1,
        max="*",
        definition="Dummy element definition",
    ):
        self.type = type or []
        self.short = short
        self.min = min
        self.max = max
        self.definition = definition


@pytest.fixture
def factory():
    factory = FHIRModelFactory(fhir_release="R4")
    return factory


def test_factory__constructs_model_with_keyword_field_names(factory: FHIRModelFactory):
    """Test that models can be constructed with keyword field names."""
    # Create a structure definition with a reserved keyword field
    structure_def_dict = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/TestResource",
        "name": "TestResource",
        "description": "A test resource",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "TestResource",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "TestResource",
                    "path": "TestResource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of TestResource",
                    "base": {"path": "TestResource", "min": 0, "max": "*"},
                },
                {
                    "id": "TestResource.class",
                    "path": "TestResource.class",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "short": "A class field",
                    "definition": "A class field",
                    "base": {"path": "TestResource.class", "min": 0, "max": "1"},
                },
                {
                    "id": "TestResource.import",
                    "path": "TestResource.import",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "short": "An import field",
                    "definition": "An import field",
                    "base": {"path": "TestResource.import", "min": 0, "max": "1"},
                },
            ]
        },
    }

    # Construct the model
    model = factory.build(structure_def_dict)

    # Check that the model was created successfully
    assert model is not None
    assert hasattr(model, "model_fields")

    # Check that keyword fields were renamed with underscore suffix
    fields = model.model_fields
    fieldnames = set(fields.keys())
    assert "class_" in fieldnames
    assert "import_" in fieldnames
    assert "class" not in fieldnames  # Original keyword should not be a field name
    assert "import" not in fieldnames  # Original keyword should not be a field name

    # Check that validation aliases were set correctly
    class_field = fields["class_"]
    import_field = fields["import_"]

    assert model.__doc__ == "Base definition of TestResource"

    assert class_field.validation_alias is not None
    assert import_field.validation_alias is not None
    assert isinstance(class_field.validation_alias, AliasChoices)
    assert isinstance(import_field.validation_alias, AliasChoices)


def test_factory___accepts_both_keyword_and_safe_field_names(factory: FHIRModelFactory):
    """Test that the constructed model accepts both original and safe field names."""
    # Create a simple structure definition with a keyword field
    structure_def_dict = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/TestResource",
        "name": "TestResource",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "TestResource",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "TestResource",
                    "path": "TestResource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of TestResource",
                    "base": {"path": "TestResource", "min": 0, "max": "*"},
                },
                {
                    "id": "TestResource.class",
                    "path": "TestResource.class",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "short": "A class field",
                    "definition": "A class field",
                    "base": {"path": "TestResource.class", "min": 0, "max": "1"},
                },
            ]
        },
    }

    # Construct the model
    TestModel = factory.build(structure_def_dict)

    assert "class_" in TestModel.model_fields
    # Using the safe field name
    instance1 = TestModel(**{"class_": "test_value"})
    # Using the original keyword name (should work due to validation_alias)
    instance2 = TestModel(**{"class": "test_value"})
    assert getattr(instance1, "class_") == "test_value"
    assert getattr(instance2, "class_") == "test_value"


def test_factory__handles_choice_type_fields_with_keywords(factory: FHIRModelFactory):
    structure_def_dict = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/TestResource",
        "name": "TestResource",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "TestResource",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "TestResource",
                    "path": "TestResource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of TestResource",
                    "base": {"path": "TestResource", "min": 0, "max": "*"},
                },
                {
                    "id": "TestResource.class[x]",
                    "path": "TestResource.class[x]",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}, {"code": "boolean"}],
                    "short": "A choice type field with keyword name",
                    "definition": "A choice type field with keyword name",
                    "base": {"path": "TestResource.class[x]", "min": 0, "max": "1"},
                },
            ]
        },
    }

    # Construct the model
    model = factory.build(structure_def_dict)

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


def test_factory__handles_extension_fields_with_keywords(factory: FHIRModelFactory):
    """Test that extension fields (_ext suffix) with keywords are handled correctly."""
    structure_def_dict = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/TestResource",
        "name": "TestResource",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "TestResource",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "TestResource",
                    "path": "TestResource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of TestResource",
                    "base": {"path": "TestResource", "min": 0, "max": "*"},
                },
                {
                    "id": "TestResource.for",
                    "path": "TestResource.for",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "short": "A primitive field with keyword name",
                    "definition": "A primitive field with keyword name",
                    "base": {"path": "TestResource.for", "min": 0, "max": "1"},
                },
            ]
        },
    }

    # Construct the model
    model = factory.build(structure_def_dict)

    # Check that both the main field and extension field were created with safe names
    fields = model.model_fields

    assert "for_" in fields
    assert "for_ext" in fields


def test_factory__uses_base_definition_from_structure_definition(
    factory: FHIRModelFactory,
):
    # Create a base resource structure definition
    base_structure_def = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/BaseResource",
        "name": "BaseResource",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "BaseResource",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "BaseResource",
                    "path": "BaseResource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of BaseResource",
                    "base": {"path": "BaseResource", "min": 0, "max": "*"},
                },
                {
                    "id": "BaseResource.baseField",
                    "path": "BaseResource.baseField",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "short": "A field from the base resource",
                    "definition": "A field from the base resource",
                    "base": {
                        "path": "BaseResource.baseField",
                        "min": 0,
                        "max": "1",
                    },
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
        "abstract": True,
        "type": "DerivedResource",
        "baseDefinition": "http://example.org/StructureDefinition/BaseResource",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "DerivedResource",
                    "path": "DerivedResource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of DerivedResource",
                    "base": {"path": "DerivedResource", "min": 0, "max": "*"},
                },
                {
                    "id": "DerivedResource.derivedField",
                    "path": "DerivedResource.derivedField",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "short": "A field specific to the derived resource",
                    "definition": "A field specific to the derived resource",
                    "base": {
                        "path": "DerivedResource.derivedField",
                        "min": 0,
                        "max": "1",
                    },
                },
            ]
        },
    }

    # Construct both models
    BaseModel = factory.build(base_structure_def)
    DerivedModel = factory.build(derived_structure_def)

    # Verify that DerivedModel inherits from BaseModel
    assert issubclass(DerivedModel, BaseModel)

    # Verify that both fields are accessible
    assert "baseField" in BaseModel.model_fields
    assert "derivedField" in DerivedModel.model_fields

    # Verify instance creation works
    instance = DerivedModel(baseField="base_value", derivedField="derived_value")
    assert instance.baseField == "base_value"  # type: ignore
    assert instance.derivedField == "derived_value"  # type: ignore


def test_factory__uses_cached_base_definition(factory: FHIRModelFactory):
    base_structure_def = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/CachedBase",
        "name": "CachedBase",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "CachedBase",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "CachedBase",
                    "path": "CachedBase",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of CachedBase",
                    "base": {"path": "CachedBase", "min": 0, "max": "*"},
                },
                {
                    "id": "CachedBase.field1",
                    "path": "CachedBase.field1",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Field 1 of CachedBase",
                    "base": {"path": "CachedBase.field1", "min": 0, "max": "1"},
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
        "abstract": True,
        "type": "DerivedFromCached",
        "baseDefinition": "http://example.org/StructureDefinition/CachedBase",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "DerivedFromCached",
                    "path": "DerivedFromCached",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of DerivedFromCached",
                    "base": {"path": "DerivedFromCached", "min": 0, "max": "*"},
                },
                {
                    "id": "DerivedFromCached.field2",
                    "path": "DerivedFromCached.field2",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Field 2 of DerivedFromCached",
                    "base": {
                        "path": "DerivedFromCached.field2",
                        "min": 0,
                        "max": "1",
                    },
                },
            ]
        },
    }

    # Construct base model first - it will be cached
    BaseModel = factory.build(base_structure_def)

    # Verify base model is in cache
    assert (
        "http://example.org/StructureDefinition/CachedBase"
        in factory.construction_cache
    )
    cached_base = factory.construction_cache[
        "http://example.org/StructureDefinition/CachedBase"
    ]

    # Construct derived model - should use cached base
    DerivedModel = factory.build(derived_structure_def)

    # Verify that the cached base was used (same object)
    assert issubclass(DerivedModel, cached_base)


def test_factory__inherits_from_builtin_fhir_resource(factory: FHIRModelFactory):
    """Test that factory can use built-in FHIR resources as base."""
    structure_def = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/CustomPatient",
        "name": "CustomPatient",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "Patient",
                    "path": "Patient",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Patient",
                    "base": {"path": "Patient", "min": 0, "max": "*"},
                },
                {
                    "id": "Patient.customField",
                    "path": "Patient.customField",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "short": "A custom extension field",
                    "definition": "A custom extension field",
                    "base": {"path": "Patient.customField", "min": 0, "max": "1"},
                },
            ]
        },
    }

    CustomPatient = factory.build(structure_def)

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


def test_factory__chain_of_inheritance(factory: FHIRModelFactory):
    # Level 1: Base
    base_def = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/Level1",
        "name": "Level1",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "Level1",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "Level1",
                    "path": "Level1",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Level1",
                    "base": {"path": "Level1", "min": 0, "max": "*"},
                },
                {
                    "id": "Level1.level1Field",
                    "path": "Level1.level1Field",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Level 1 field",
                    "base": {"path": "Level1.level1Field", "min": 0, "max": "1"},
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
        "abstract": True,
        "type": "Level2",
        "baseDefinition": "http://example.org/StructureDefinition/Level1",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "Level2",
                    "path": "Level2",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Level2",
                    "base": {"path": "Level2", "min": 0, "max": "*"},
                },
                {
                    "id": "Level2.level2Field",
                    "path": "Level2.level2Field",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Level 2 field",
                    "base": {"path": "Level2.level2Field", "min": 0, "max": "1"},
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
        "abstract": True,
        "type": "Level3",
        "baseDefinition": "http://example.org/StructureDefinition/Level2",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "Level3",
                    "path": "Level3",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Level3",
                    "base": {"path": "Level3", "min": 0, "max": "*"},
                },
                {
                    "id": "Level3.level3Field",
                    "path": "Level3.level3Field",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Level 3 field",
                    "base": {"path": "Level3.level3Field", "min": 0, "max": "1"},
                },
            ]
        },
    }

    Level1 = factory.build(base_def)
    Level2 = factory.build(middle_def)
    Level3 = factory.build(derived_def)

    # Verify inheritance chain
    assert issubclass(Level2, Level1)
    assert issubclass(Level3, Level2)
    assert issubclass(Level3, Level1)

    # Verify all fields are accessible at Level3
    instance = Level3(level1Field="value1", level2Field="value2", level3Field="value3")
    assert instance.level1Field == "value1"  # type: ignore
    assert instance.level2Field == "value2"  # type: ignore
    assert instance.level3Field == "value3"  # type: ignore


def test_factory__does_not_duplicate_inherited_fields(factory: FHIRModelFactory):
    base_def = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/BaseWithField",
        "name": "BaseWithField",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "BaseWithField",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "BaseWithField",
                    "path": "BaseWithField",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of BaseWithField",
                    "base": {"path": "BaseWithField", "min": 0, "max": "*"},
                },
                {
                    "id": "BaseWithField.sharedField",
                    "path": "BaseWithField.sharedField",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Shared field in BaseWithField",
                    "base": {
                        "path": "BaseWithField.sharedField",
                        "min": 0,
                        "max": "1",
                    },
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
        "abstract": True,
        "type": "DerivedWithSameField",
        "baseDefinition": "http://example.org/StructureDefinition/BaseWithField",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "DerivedWithSameField",
                    "path": "DerivedWithSameField",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of DerivedWithSameField",
                    "base": {"path": "DerivedWithSameField", "min": 0, "max": "*"},
                },
                {
                    "id": "DerivedWithSameField.sharedField",
                    "path": "DerivedWithSameField.sharedField",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Shared field in DerivedWithSameField",
                    "base": {
                        "path": "DerivedWithSameField.sharedField",
                        "min": 0,
                        "max": "1",
                    },
                },
                {
                    "id": "DerivedWithSameField.ownField",
                    "path": "DerivedWithSameField.ownField",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Own field in DerivedWithSameField",
                    "base": {
                        "path": "DerivedWithSameField.ownField",
                        "min": 0,
                        "max": "1",
                    },
                },
            ]
        },
    }

    Base = factory.build(base_def)
    Derived = factory.build(derived_def)

    # The derived model should not redefine sharedField
    # It should be inherited from Base
    assert "sharedField" in Base.model_fields
    assert "ownField" in Derived.model_fields

    # Derived should still be able to use sharedField
    instance = Derived(sharedField="shared", ownField="own")
    assert instance.sharedField == "shared"  # type: ignore
    assert instance.ownField == "own"  # type: ignore


def test_factory__allows_mixing_additional_parent_classes(
    factory: FHIRModelFactory,
):
    """Test that explicit base_model parameter takes precedence over baseDefinition."""
    from fhircraft.fhir.resources.base import FHIRBaseModel

    structure_def = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/TestResource",
        "name": "TestResource",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "TestResource",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Basic",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "TestResource",
                    "path": "TestResource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of TestResource",
                    "base": {"path": "TestResource", "min": 0, "max": "*"},
                },
                {
                    "id": "TestResource.field1",
                    "path": "TestResource.field1",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Field 1 of TestResource",
                    "base": {"path": "TestResource.field1", "min": 0, "max": "1"},
                },
            ]
        },
    }

    class AdditionalMixin:
        pass

    # Provide explicit base_model - it should override baseDefinition
    model = factory.build(structure_def, mixins=(AdditionalMixin,))

    # Should inherit from FHIRBaseModel, not from SomeBase
    assert issubclass(model, FHIRBaseModel)
    assert issubclass(model, AdditionalMixin)


def test_factory__no_basedefinition_defaults_to_fhirbasemodel(
    factory: FHIRModelFactory,
):
    """Test that resources without baseDefinition inherit from FHIRBaseModel."""
    from fhircraft.fhir.resources.base import FHIRBaseModel

    structure_def = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/StandaloneResource",
        "name": "StandaloneResource",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "StandaloneResource",
        # No baseDefinition specified
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "StandaloneResource",
                    "path": "StandaloneResource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of StandaloneResource",
                    "base": {"path": "StandaloneResource", "min": 0, "max": "*"},
                },
                {
                    "id": "StandaloneResource.field1",
                    "path": "StandaloneResource.field1",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Field 1 of StandaloneResource",
                    "base": {
                        "path": "StandaloneResource.field1",
                        "min": 0,
                        "max": "1",
                    },
                },
            ]
        },
    }

    model = factory.build(structure_def)

    # Should inherit from FHIRBaseModel by default
    assert issubclass(model, FHIRBaseModel)
    assert "field1" in model.model_fields


def test_factory__resource_with_sliced_extensions_processes_correctly(
    factory: FHIRModelFactory,
):
    # Create a Patient resource with sliced extensions
    patient_with_sliced_extensions = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/fhir/StructureDefinition/PatientWithSlicedExtensions",
        "name": "PatientWithSlicedExtensions",
        "status": "active",
        "kind": "resource",
        "abstract": True,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "snapshot": {
            "element": [
                {
                    "id": "Patient",
                    "path": "Patient",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Patient",
                    "base": {"path": "Patient", "min": 0, "max": "*"},
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
                    "definition": "Extension field with slicing",
                    "base": {"path": "Patient.extension", "min": 0, "max": "*"},
                },
                {
                    "id": "Patient.extension:birthPlace",
                    "path": "Patient.extension",
                    "sliceName": "birthPlace",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "Extension"}],
                    "short": "Birth place extension slice",
                    "definition": "Birth place extension slice",
                    "base": {"path": "Patient.extension", "min": 0, "max": "*"},
                },
                {
                    "id": "Patient.extension:birthPlace.url",
                    "path": "Patient.extension.url",
                    "min": 1,
                    "max": "1",
                    "type": [{"code": "uri"}],
                    "fixedUri": "http://hl7.org/fhir/StructureDefinition/patient-birthPlace",
                    "definition": "URL for birth place extension",
                    "base": {"path": "Extension.url", "min": 1, "max": "1"},
                },
                {
                    "id": "Patient.extension:birthPlace.valueAddress",
                    "path": "Patient.extension.valueAddress",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "Address"}],
                    "definition": "Address value for birth place",
                    "base": {
                        "path": "Extension.valueAddress",
                        "min": 0,
                        "max": "1",
                    },
                },
            ]
        },
    }

    # Construct the Patient model with sliced extensions
    PatientModel = factory.build(patient_with_sliced_extensions)

    # The sliced resource should still be a valid Patient model
    from fhircraft.fhir.resources.datatypes.R4B.core.patient import Patient

    assert issubclass(PatientModel, Patient), "Model should inherit from Patient"

    # At minimum, there should be an extension field
    assert "extension" in PatientModel.model_fields, "Model should have extension field"

    # The model should be constructable
    instance = PatientModel()
    assert isinstance(instance, Patient), "Instance should be a Patient"


def test_factory__constructs_model_from_differential_auto_mode(
    factory: FHIRModelFactory,
):
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-patient-profile",
        "url": "http://example.org/StructureDefinition/test-patient-profile",
        "name": "TestPatientProfile",
        "title": "Test Patient Profile",
        "status": "draft",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": True,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Patient",
                    "path": "Patient",
                    "short": "Test patient profile",
                    "min": 0,
                    "max": "*",
                    "definition": "Test patient profile",
                    "base": {"path": "Patient", "min": 0, "max": "*"},
                },
                {
                    "id": "Patient.identifier",
                    "path": "Patient.identifier",
                    "min": 1,
                    "max": "*",
                    "definition": "Patient identifier",
                    "base": {"path": "Patient.identifier", "min": 0, "max": "*"},
                },
            ]
        },
    }

    # This should auto-detect DIFFERENTIAL mode
    model = factory.build(differential_sd, mode="auto")

    assert model is not None
    assert model.__name__ == "TestPatientProfile"
    model_fields = model.model_fields.keys()
    assert "identifier" in model_fields


def test_factory__caches_differential_model(factory: FHIRModelFactory):
    """Test that differential models are cached."""
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-cached-profile",
        "url": "http://example.org/StructureDefinition/test-cached-profile",
        "name": "TestCachedProfile",
        "status": "draft",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": True,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Patient",
                    "path": "Patient",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Patient",
                    "base": {"path": "Patient", "min": 0, "max": "*"},
                },
                {"id": "Patient.id", "path": "Patient.id", "min": 1, "max": "1"},
            ]
        },
    }

    model1 = factory.build(differential_sd, mode="differential")

    # Second construction should return cached model
    model2 = factory.build(canonical_url=differential_sd["url"], mode="differential")

    assert model1 is model2


def test_factory__differential_inherits_from_base(factory: FHIRModelFactory):
    """Test that differential models inherit from their base."""
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-inheritance",
        "url": "http://example.org/StructureDefinition/test-inheritance",
        "name": "TestInheritance",
        "status": "draft",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": True,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint",
        "differential": {
            "element": [
                {"id": "Patient", "path": "Patient", "min": 0, "max": "*"},
                {"id": "Patient.id", "path": "Patient.id", "min": 1, "max": "1"},
            ]
        },
    }

    model = factory.build(differential_sd, mode="differential")

    # Should inherit from FHIRBaseModel (since base Patient might not be available)
    assert issubclass(model, FHIRBaseModel)


def test_factory__constructs_model_from_snapshot_auto_mode(factory: FHIRModelFactory):
    """Test that models can be constructed from snapshot with AUTO mode."""
    snapshot_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-snapshot-patient",
        "url": "http://example.org/StructureDefinition/test-snapshot-patient",
        "name": "TestSnapshotPatient",
        "status": "draft",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": True,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint",
        "snapshot": {
            "element": [
                {
                    "id": "Patient",
                    "path": "Patient",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Patient",
                    "base": {"path": "Patient", "min": 0, "max": "*"},
                },
                {
                    "id": "Patient.id",
                    "path": "Patient.id",
                    "min": 1,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Patient identifier",
                    "base": {"path": "Patient.id", "min": 0, "max": "*"},
                },
            ]
        },
    }

    model = factory.build(snapshot_sd, mode="auto")

    assert model is not None
    assert model.__name__ == "TestSnapshotPatient"


def test_factory__constructs_model_from_snapshot_explicit_mode(
    factory: FHIRModelFactory,
):
    """Test that models can be constructed with explicit SNAPSHOT mode."""
    snapshot_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-snapshot-explicit",
        "url": "http://example.org/StructureDefinition/test-snapshot-explicit",
        "name": "TestSnapshotExplicit",
        "status": "draft",
        "version": "2.1.0",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": True,
        "type": "Patient",
        "snapshot": {
            "element": [
                {
                    "id": "Patient",
                    "path": "Patient",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Patient",
                    "base": {"path": "Patient", "min": 0, "max": "*"},
                },
                {
                    "id": "Patient.id",
                    "path": "Patient.id",
                    "min": 1,
                    "max": "*",
                    "type": [{"code": "string"}],
                    "definition": "Patient identifier",
                    "base": {"path": "Patient.id", "min": 0, "max": "*"},
                },
            ]
        },
    }

    model = factory.build(snapshot_sd, mode="snapshot")

    assert model is not None
    assert model.__name__ == "TestSnapshotExplicit"


def test_factory__construct_diff_min_cardinality(factory: FHIRModelFactory):
    """Test that construct_resource_model sets construction_mode in Config."""
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-diff-mode",
        "url": "http://example.org/StructureDefinition/test-diff-mode",
        "name": "TestDiffMode",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": True,
        "type": "Resource",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Basic",
        "differential": {
            "element": [
                {
                    "id": "Resource.id",
                    "path": "Resource.id",
                    "min": 1,
                    "max": "1",
                    "definition": "Required element",
                    "base": {"path": "Resource.id", "min": 0, "max": "1"},
                }
            ]
        },
    }

    mock_resource = factory.build(differential_sd, mode="differential")

    assert "id" in mock_resource.model_fields
    # Assert element
    element = mock_resource.model_fields.get("id")
    assert element is not None, "Profiled element field not found in model fields"
    assert (
        element.annotation == Optional[primitives.String]
    ), "Profiled element field does not have correct type annotation"

    # Assert metadata
    element_metadata = element.metadata
    assert element_metadata is not None, "No metadata found for profiled element"

    # Test valid dataset
    assert (
        mock_resource.model_validate({"id": "test"}) is not None
    ), "Valid dataset did not validate correctly"
    # Test invalid dataset
    with pytest.raises(ValidationError):
        mock_resource.model_validate({"id": ["test"]})


def test_factory__construct_diff_fixed_value_constraint(factory: FHIRModelFactory):
    """Test that differential can add fixed value constraints to elements."""
    # Create base with a status field
    base_sd = {
        "resourceType": "StructureDefinition",
        "id": "mock-base-status",
        "url": "http://example.org/StructureDefinition/mock-base-status",
        "name": "MockBaseStatus",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": True,
        "type": "Resource",
        "snapshot": {
            "element": [
                {
                    "id": "Resource",
                    "path": "Resource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Resource",
                    "base": {"path": "Resource", "min": 0, "max": "*"},
                },
                {
                    "id": "Resource.status",
                    "path": "Resource.status",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "code"}],
                    "definition": "The status of the resource",
                    "base": {"path": "Resource.status", "min": 0, "max": "1"},
                },
            ]
        },
    }
    factory.definition_registry.from_dict(base_sd)
    factory.build(base_sd)

    # Apply fixed value constraint in differential
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-diff-fixed",
        "url": "http://example.org/StructureDefinition/test-diff-fixed",
        "name": "TestDiffFixed",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": True,
        "type": "Resource",
        "baseDefinition": "http://example.org/StructureDefinition/mock-base-status",
        "differential": {
            "element": [
                {
                    "id": "Resource.status",
                    "path": "Resource.status",
                    "fixedCode": "active",
                }
            ]
        },
    }

    mock_resource = factory.build(differential_sd, mode="differential")

    # Status field should exist
    assert "status" in mock_resource.model_fields

    # Test that only the fixed value is accepted
    instance = mock_resource.model_validate({"status": "active"})
    assert instance.status == "active"  # type: ignore

    # Test that other values are rejected
    with pytest.raises(ValidationError):
        mock_resource.model_validate({"status": "inactive"})


def test_factory__construct_diff_pattern_value_constraint(factory: FHIRModelFactory):
    """Test that differential can add pattern value constraints to elements."""
    # Create base with a coding field
    base_sd = {
        "resourceType": "StructureDefinition",
        "id": "mock-base-coding",
        "url": "http://example.org/StructureDefinition/mock-base-coding",
        "name": "MockBaseCoding",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": True,
        "type": "Resource",
        "snapshot": {
            "element": [
                {
                    "id": "Resource",
                    "path": "Resource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Resource",
                    "base": {"path": "Resource", "min": 0, "max": "*"},
                },
                {
                    "id": "Resource.code",
                    "path": "Resource.code",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "Coding"}],
                    "definition": "A code field",
                    "base": {"path": "Resource.code", "min": 0, "max": "1"},
                },
            ]
        },
    }
    factory.definition_registry.from_dict(base_sd)
    factory.build(base_sd)

    # Apply pattern constraint in differential
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-diff-pattern",
        "url": "http://example.org/StructureDefinition/test-diff-pattern",
        "name": "TestDiffPattern",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Resource",
        "baseDefinition": "http://example.org/StructureDefinition/mock-base-coding",
        "differential": {
            "element": [
                {
                    "id": "Resource.code",
                    "path": "Resource.code",
                    "patternCoding": {
                        "system": "http://example.org/codesystem",
                        "code": "test-code",
                    },
                }
            ]
        },
    }

    mock_resource = factory.build(differential_sd, mode="differential")

    # Code field should exist and have a pattern validator
    assert "code" in mock_resource.model_fields

    # Check that model has the pattern constraint validator
    validator_names = [
        name for name in dir(mock_resource) if "pattern_constraint" in name
    ]
    assert len(validator_names) > 0, "Pattern constraint validator not found"

    mock_resource.model_validate(
        {"code": {"system": "http://example.org/codesystem", "code": "test-code"}}
    )

    # Test that other values are rejected
    with pytest.raises(ValidationError):
        mock_resource.model_validate(
            {"code": {"system": "http://wrong-system", "code": "wrong-code"}}
        )


def test_construct_diff_type_choice_element(factory: FHIRModelFactory):
    """Test that differential can constrain type choice elements."""
    # Create base with a value[x] type choice field
    base_sd = {
        "resourceType": "StructureDefinition",
        "id": "mock-base-choice",
        "url": "http://example.org/StructureDefinition/mock-base-choice",
        "name": "MockBaseChoice",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": True,
        "type": "Resource",
        "snapshot": {
            "element": [
                {
                    "id": "Resource",
                    "path": "Resource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Resource",
                    "base": {"path": "Resource", "min": 0, "max": "*"},
                },
                {
                    "id": "Resource.value[x]",
                    "path": "Resource.value[x]",
                    "min": 0,
                    "max": "1",
                    "definition": "A value that can be of multiple types",
                    "base": {"path": "Resource.value[x]", "min": 0, "max": "1"},
                    "type": [
                        {"code": "string"},
                        {"code": "integer"},
                        {"code": "boolean"},
                    ],
                },
            ]
        },
    }
    factory.definition_registry.from_dict(base_sd)
    factory.build(base_sd)

    # Constrain type choice to only string and integer in differential
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-diff-choice",
        "url": "http://example.org/StructureDefinition/test-diff-choice",
        "name": "TestDiffChoice",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Observation",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
        "differential": {
            "element": [
                {
                    "id": "Observation",
                    "path": "Observation",
                },
                {
                    "id": "Observation.value[x]",
                    "path": "Observation.value[x]",
                    "min": 0,
                    "max": "1",
                    "type": [
                        {"code": "string"},
                    ],
                },
            ]
        },
    }

    mock_resource = factory.build(differential_sd, mode="differential")

    # Test that property accessor works
    assert hasattr(mock_resource, "value")

    # Test valid data with string
    instance = mock_resource.model_validate({"valueString": "test"})
    assert instance.value == "test"  # type: ignore

    with pytest.raises(ValidationError):
        mock_resource.model_validate({"valueInteger": 2})


def test_construct_diff_nested_backbone_element(factory: FHIRModelFactory):
    """Test that differential can constrain nested backbone elements."""
    # Create base with simple nested structure using ContactPoint
    base_sd = {
        "resourceType": "StructureDefinition",
        "id": "mock-base-telecom",
        "url": "http://example.org/StructureDefinition/mock-base-telecom",
        "name": "MockBaseTelecom",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": True,
        "type": "Resource",
        "snapshot": {
            "element": [
                {
                    "id": "Resource",
                    "path": "Resource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Resource",
                    "base": {"path": "Resource", "min": 0, "max": "*"},
                },
                {
                    "id": "Resource.telecom",
                    "path": "Resource.telecom",
                    "min": 0,
                    "max": "*",
                    "type": [{"code": "ContactPoint"}],
                    "definition": "Contact details for the resource",
                    "base": {"path": "Resource.telecom", "min": 0, "max": "*"},
                },
            ]
        },
    }
    factory.definition_registry.from_dict(base_sd)
    factory.build(base_sd)

    # Constrain telecom in differential to be required
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-diff-telecom",
        "url": "http://example.org/StructureDefinition/test-diff-telecom",
        "name": "TestDiffTelecom",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Resource",
        "baseDefinition": "http://example.org/StructureDefinition/mock-base-telecom",
        "differential": {
            "element": [
                {
                    "id": "Resource.telecom",
                    "path": "Resource.telecom",
                    "min": 1,
                    "max": "*",
                }
            ]
        },
    }

    mock_resource = factory.build(differential_sd, mode="differential")

    # Telecom field should exist
    assert "telecom" in mock_resource.model_fields

    # Check that it's required (min cardinality 1)
    telecom_metadata = mock_resource.model_fields["telecom"].metadata
    assert (
        next((meta for meta in telecom_metadata if isinstance(meta, MinLen))).min_length
        == 1
    )

    # Test valid data with required telecom
    instance = mock_resource.model_validate(
        {"telecom": [{"system": "phone", "value": "555-1234"}]}
    )
    assert instance.telecom is not None  # type: ignore

    # Test invalid data without required telecom
    with pytest.raises(ValidationError):
        mock_resource.model_validate({"telecom": []})


def test_construct_diff_element_cardinality(factory: FHIRModelFactory):
    """Test that differential can constrain element cardinality."""
    # Create base with identifier field that can be sliced
    base_sd = {
        "resourceType": "StructureDefinition",
        "id": "mock-base-identifier",
        "url": "http://example.org/StructureDefinition/mock-base-identifier",
        "name": "MockBaseIdentifier",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": True,
        "type": "Resource",
        "snapshot": {
            "element": [
                {
                    "id": "Resource",
                    "path": "Resource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Resource",
                    "base": {"path": "Resource", "min": 0, "max": "*"},
                },
                {
                    "id": "Resource.identifier",
                    "path": "Resource.identifier",
                    "min": 0,
                    "max": "*",
                    "base": {"path": "Resource.identifier", "min": 0, "max": "*"},
                    "definition": "An identifier for the resource",
                    "type": [{"code": "Identifier"}],
                },
            ]
        },
    }
    factory.definition_registry.from_dict(base_sd)
    factory.build(base_sd)

    # Constrain identifier field cardinality in differential
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-diff-identifier",
        "url": "http://example.org/StructureDefinition/test-diff-identifier",
        "name": "TestDiffIdentifier",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Resource",
        "baseDefinition": "http://example.org/StructureDefinition/mock-base-identifier",
        "differential": {
            "element": [
                {
                    "id": "Resource.identifier",
                    "path": "Resource.identifier",
                    "min": 1,
                    "max": "3",
                },
            ]
        },
    }

    mock_resource = factory.build(differential_sd, mode="differential")

    # Identifier field should exist with new constraints
    assert "identifier" in mock_resource.model_fields
    identifier = mock_resource.model_fields["identifier"]
    identifier_metadata = identifier.metadata

    # Verify constraints
    assert (
        next(
            (meta for meta in identifier_metadata if isinstance(meta, MinLen))
        ).min_length
        == 1
    )
    assert (
        next(
            (meta for meta in identifier_metadata if isinstance(meta, MaxLen))
        ).max_length
        == 3
    )


def test_construct_diff_constraint_invariant(factory: FHIRModelFactory):
    """Test that differential can add constraint invariants to elements."""
    # Create base
    base_sd = {
        "resourceType": "StructureDefinition",
        "id": "mock-base-constraint",
        "url": "http://example.org/StructureDefinition/mock-base-constraint",
        "name": "MockBaseConstraint",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": True,
        "type": "Resource",
        "snapshot": {
            "element": [
                {
                    "id": "Resource",
                    "path": "Resource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Resource",
                    "base": {"path": "Resource", "min": 0, "max": "*"},
                },
                {
                    "id": "Resource.value[x]",
                    "path": "Resource.value[x]",
                    "min": 0,
                    "max": "1",
                    "definition": "A value field",
                    "base": {"path": "Resource.value[x]", "min": 0, "max": "1"},
                    "type": [{"code": "integer"}],
                },
            ]
        },
    }
    factory.definition_registry.from_dict(base_sd)
    factory.build(base_sd)

    # Add constraint in differential
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-diff-constraint",
        "url": "http://example.org/StructureDefinition/test-diff-constraint",
        "name": "TestDiffConstraint",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Resource",
        "baseDefinition": "http://example.org/StructureDefinition/mock-base-constraint",
        "differential": {
            "element": [
                {
                    "id": "Resource",
                    "path": "Resource",
                    "constraint": [
                        {
                            "key": "val-1",
                            "severity": "error",
                            "human": "Value must be positive",
                            "expression": "value > 0",
                        },
                    ],
                },
                {
                    "id": "Resource.value[x]",
                    "path": "Resource.value[x]",
                },
            ]
        },
    }

    mock_resource = factory.build(differential_sd, mode="differential")

    # Value field should exist
    assert "valueInteger" in mock_resource.model_fields

    # Check that constraint validator was added
    validator_names = [
        name
        for name in dir(mock_resource)
        if "val-1" in name or "constraint" in name.lower()
    ]
    assert len(validator_names) > 0, "Constraint validator not found"

    # Check that valid value passes
    instance = mock_resource.model_validate({"valueInteger": 5})
    assert instance.valueInteger == 5  # type: ignore

    # Check that invalid value raises error
    with pytest.raises(ValidationError):
        mock_resource.model_validate({"valueInteger": -2})


def test_construct_diff_multiple_elements_constraints(factory: FHIRModelFactory):
    """Test that differential can apply different constraint types to multiple elements."""
    # Create base with multiple fields
    base_sd = {
        "resourceType": "StructureDefinition",
        "id": "mock-base-multi",
        "url": "http://example.org/StructureDefinition/mock-base-multi",
        "name": "MockBaseMulti",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": True,
        "type": "Resource",
        "snapshot": {
            "element": [
                {
                    "id": "Resource",
                    "path": "Resource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Resource",
                    "base": {"path": "Resource", "min": 0, "max": "*"},
                },
                {
                    "id": "Resource.status",
                    "path": "Resource.status",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "code"}],
                    "definition": "Status field",
                    "base": {"path": "Resource.status", "min": 0, "max": "1"},
                },
                {
                    "id": "Resource.priority",
                    "path": "Resource.priority",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "code"}],
                    "definition": "Priority field",
                    "base": {"path": "Resource.priority", "min": 0, "max": "1"},
                },
                {
                    "id": "Resource.text",
                    "path": "Resource.text",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "Text field",
                    "base": {"path": "Resource.text", "min": 0, "max": "1"},
                },
            ]
        },
    }
    factory.definition_registry.from_dict(base_sd)
    factory.build(base_sd)

    # Apply different constraints to different elements
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-diff-multi-constraints",
        "url": "http://example.org/StructureDefinition/test-diff-multi-constraints",
        "name": "TestDiffMultiConstraints",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Resource",
        "baseDefinition": "http://example.org/StructureDefinition/mock-base-multi",
        "differential": {
            "element": [
                {
                    "id": "Resource.status",
                    "path": "Resource.status",
                    "min": 1,  # Make required
                    "fixedCode": "active",  # Fix value
                },
                {
                    "id": "Resource.priority",
                    "path": "Resource.priority",
                    "patternCode": "high",  # Pattern constraint
                },
                {
                    "id": "Resource.text",
                    "path": "Resource.text",
                    "min": 1,  # Make required
                    "max": "1",
                },
            ]
        },
    }

    mock_resource = factory.build(differential_sd, mode="differential")

    # All fields should exist
    assert "status" in mock_resource.model_fields
    assert "priority" in mock_resource.model_fields
    assert "text" in mock_resource.model_fields

    # Test valid instance with all constraints satisfied
    instance = mock_resource.model_validate(
        {"status": "active", "priority": "high", "text": "Test text"}
    )
    assert instance.status == "active"  # type: ignore

    # Test that fixed value is enforced
    with pytest.raises(ValidationError):
        mock_resource.model_validate({"status": "inactive", "text": "Test text"})

    # Test that pattern is enforced
    with pytest.raises(ValidationError):
        mock_resource.model_validate(
            {
                "priority": "wrong",
            }
        )


def test_construct_diff_inherits_base_structure(factory: FHIRModelFactory):
    """Test that differential models properly inherit complete structure from base."""
    # Create base with multiple nested elements
    base_sd = {
        "resourceType": "StructureDefinition",
        "id": "mock-base-complex",
        "url": "http://example.org/StructureDefinition/mock-base-complex",
        "name": "MockBaseComplex",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": True,
        "type": "Resource",
        "snapshot": {
            "element": [
                {
                    "id": "Resource",
                    "path": "Resource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Resource",
                    "base": {"path": "Resource", "min": 0, "max": "*"},
                },
                {
                    "id": "Resource.field1",
                    "path": "Resource.field1",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "string"}],
                    "definition": "First field",
                    "base": {"path": "Resource.field1", "min": 0, "max": "1"},
                },
                {
                    "id": "Resource.field2",
                    "path": "Resource.field2",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "integer"}],
                    "definition": "Second field",
                    "base": {"path": "Resource.field2", "min": 0, "max": "1"},
                },
                {
                    "id": "Resource.field3",
                    "path": "Resource.field3",
                    "min": 0,
                    "max": "1",
                    "type": [{"code": "boolean"}],
                    "definition": "Third field",
                    "base": {"path": "Resource.field3", "min": 0, "max": "1"},
                },
            ]
        },
    }
    factory.definition_registry.from_dict(base_sd)
    factory.build(base_sd)

    # Differential only constrains one field
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-diff-inherit",
        "url": "http://example.org/StructureDefinition/test-diff-inherit",
        "name": "TestDiffInherit",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Resource",
        "baseDefinition": "http://example.org/StructureDefinition/mock-base-complex",
        "differential": {
            "element": [
                {
                    "id": "Resource.field1",
                    "path": "Resource.field1",
                    "min": 1,  # Only constrain field1
                }
            ]
        },
    }

    mock_resource = factory.build(differential_sd, mode="differential")

    # All fields from base should be present
    assert "field1" in mock_resource.model_fields
    assert "field2" in mock_resource.model_fields
    assert "field3" in mock_resource.model_fields

    # Other fields should work normally
    instance = mock_resource.model_validate(
        {"field1": "required_value", "field2": 42, "field3": True}
    )
    assert instance.field1 == "required_value"  # type: ignore
    assert instance.field2 == 42  # type: ignore
    assert instance.field3 == True  # type: ignore


def test_factory__construct_diff_sliced_backbone_elements(factory: FHIRModelFactory):
    """Test that differential can slice backbone elements with specific constraints."""
    # Create base with component backbone element
    base_sd = {
        "resourceType": "StructureDefinition",
        "id": "mock-base-component",
        "url": "http://example.org/StructureDefinition/mock-base-component",
        "name": "MockBaseComponent",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": True,
        "type": "Resource",
        "snapshot": {
            "element": [
                {
                    "id": "Resource",
                    "path": "Resource",
                    "min": 0,
                    "max": "*",
                    "definition": "Base definition of Resource",
                    "base": {"path": "Resource", "min": 0, "max": "*"},
                },
                {
                    "id": "Resource.component",
                    "path": "Resource.component",
                    "min": 0,
                    "max": "*",
                    "type": [{"code": "BackboneElement"}],
                    "definition": "Component backbone element",
                    "base": {"path": "Resource.component", "min": 0, "max": "*"},
                },
                {
                    "id": "Resource.component.code",
                    "path": "Resource.component.code",
                    "min": 1,
                    "max": "1",
                    "type": [{"code": "CodeableConcept"}],
                    "definition": "Code for the component",
                    "base": {
                        "path": "Resource.component.code",
                        "min": 1,
                        "max": "1",
                    },
                },
                {
                    "id": "Resource.component.value[x]",
                    "path": "Resource.component.value[x]",
                    "min": 0,
                    "max": "1",
                    "type": [
                        {"code": "Quantity"},
                        {"code": "string"},
                    ],
                    "definition": "Value for the component",
                    "base": {
                        "path": "Resource.component.value[x]",
                        "min": 0,
                        "max": "1",
                    },
                },
            ]
        },
    }
    factory.definition_registry.from_dict(base_sd)
    factory.build(base_sd)

    # Slice component by code
    differential_sd = {
        "resourceType": "StructureDefinition",
        "id": "test-diff-component-slice",
        "url": "http://example.org/StructureDefinition/test-diff-component-slice",
        "name": "TestDiffComponentSlice",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "version": "1.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Resource",
        "baseDefinition": "http://example.org/StructureDefinition/mock-base-component",
        "differential": {
            "element": [
                {
                    "id": "Resource.component",
                    "path": "Resource.component",
                    "slicing": {
                        "discriminator": [{"type": "pattern", "path": "code"}],
                        "rules": "open",
                    },
                    "min": 2,
                    "max": "*",
                },
                {
                    "id": "Resource.component:systolic",
                    "path": "Resource.component",
                    "sliceName": "systolic",
                    "min": 1,
                    "max": "1",
                },
                {
                    "id": "Resource.component:systolic.code",
                    "path": "Resource.component.code",
                    "patternCodeableConcept": {
                        "coding": [{"system": "http://loinc.org", "code": "8480-6"}]
                    },
                },
                {
                    "id": "Resource.component:systolic.value[x]",
                    "path": "Resource.component.value[x]",
                    "min": 1,
                    "max": "1",
                    "type": [{"code": "Quantity"}],
                },
                {
                    "id": "Resource.component:diastolic",
                    "path": "Resource.component",
                    "sliceName": "diastolic",
                    "min": 1,
                    "max": "1",
                },
                {
                    "id": "Resource.component:diastolic.code",
                    "path": "Resource.component.code",
                    "patternCodeableConcept": {
                        "coding": [{"system": "http://loinc.org", "code": "8462-4"}]
                    },
                },
                {
                    "id": "Resource.component:diastolic.value[x]",
                    "path": "Resource.component.value[x]",
                    "min": 1,
                    "max": "1",
                    "type": [{"code": "Quantity"}],
                },
            ]
        },
    }

    mock_resource = factory.build(differential_sd, mode="differential")

    # Component field should exist
    assert "component" in mock_resource.model_fields

    # Check cardinality constraint (min 2)
    component_metadata = mock_resource.model_fields["component"].metadata
    assert (
        next(
            (meta for meta in component_metadata if isinstance(meta, MinLen))
        ).min_length
        == 2
    )

    # Test valid instance with both required slices
    instance = mock_resource.model_validate(
        {
            "component": [
                {
                    "code": {
                        "coding": [{"system": "http://loinc.org", "code": "8480-6"}]
                    },
                    "valueQuantity": {"value": 120, "unit": "mmHg"},
                },
                {
                    "code": {
                        "coding": [{"system": "http://loinc.org", "code": "8462-4"}]
                    },
                    "valueQuantity": {"value": 80, "unit": "mmHg"},
                },
            ]
        }
    )
    assert instance.component is not None  # type: ignore
    assert len(instance.component) == 2  # type: ignore
