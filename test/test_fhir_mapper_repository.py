"""
Test the new repository management methods in FHIRMapper.
"""

import tempfile
import json
from pathlib import Path

from fhircraft.fhir.mapper import FHIRMapper


def test_add_structure_definition():
    """Test adding a StructureDefinition to the repository."""
    mapper = FHIRMapper()
    
    # Create a minimal StructureDefinition
    struct_def = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/TestProfile",
        "version": "1.0.0",
        "name": "TestProfile",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": False,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint"
    }
    
    # Add the structure definition
    mapper.add_structure_definition(struct_def)
    
    # Check if it was added
    assert mapper.has_structure_definition("http://example.org/StructureDefinition/TestProfile", "1.0.0")
    print("✓ Successfully added StructureDefinition to repository")


def test_add_structure_definitions_from_file():
    """Test loading StructureDefinitions from a file."""
    mapper = FHIRMapper()
    
    # Create a temporary file with a StructureDefinition
    struct_def = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/FileTestProfile",
        "version": "1.0.0",
        "name": "FileTestProfile",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": False,
        "type": "Observation",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
        "derivation": "constraint"
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(struct_def, f, indent=2)
        temp_file = f.name
    
    try:
        # Load from file
        count = mapper.add_structure_definitions_from_file(temp_file)
        assert count == 1
        
        # Check if it was added
        assert mapper.has_structure_definition("http://example.org/StructureDefinition/FileTestProfile")
        print("✓ Successfully loaded StructureDefinition from file")
        
    finally:
        # Clean up
        Path(temp_file).unlink()


def test_add_bundle_from_file():
    """Test loading StructureDefinitions from a Bundle file."""
    mapper = FHIRMapper()
    
    # Create a Bundle with StructureDefinitions
    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [
            {
                "resource": {
                    "resourceType": "StructureDefinition",
                    "url": "http://example.org/StructureDefinition/BundleTest1",
                    "version": "1.0.0",
                    "name": "BundleTest1",
                    "status": "draft",
                    "fhirVersion": "4.3.0",
                    "kind": "resource",
                    "abstract": False,
                    "type": "Patient",
                    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
                    "derivation": "constraint"
                }
            },
            {
                "resource": {
                    "resourceType": "StructureDefinition",
                    "url": "http://example.org/StructureDefinition/BundleTest2",
                    "version": "1.0.0",
                    "name": "BundleTest2",
                    "status": "draft",
                    "fhirVersion": "4.3.0",
                    "kind": "resource",
                    "abstract": False,
                    "type": "Observation",
                    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
                    "derivation": "constraint"
                }
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(bundle, f, indent=2)
        temp_file = f.name
    
    try:
        # Load from bundle file
        count = mapper.add_structure_definitions_from_file(temp_file)
        assert count == 2
        
        # Check if both were added
        assert mapper.has_structure_definition("http://example.org/StructureDefinition/BundleTest1")
        assert mapper.has_structure_definition("http://example.org/StructureDefinition/BundleTest2")
        print("✓ Successfully loaded StructureDefinitions from Bundle file")
        
    finally:
        # Clean up
        Path(temp_file).unlink()


def test_duplicate_handling():
    """Test duplicate handling with fail_if_exists parameter."""
    mapper = FHIRMapper()
    
    struct_def = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/DuplicateTest",
        "version": "1.0.0",
        "name": "DuplicateTest",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": False,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint"
    }
    
    # Add first time - should succeed
    mapper.add_structure_definition(struct_def, fail_if_exists=False)
    assert mapper.has_structure_definition("http://example.org/StructureDefinition/DuplicateTest")
    
    # Add again with fail_if_exists=False - should succeed (overwrite)
    mapper.add_structure_definition(struct_def, fail_if_exists=False)
    
    # Add again with fail_if_exists=True - should raise error
    try:
        mapper.add_structure_definition(struct_def, fail_if_exists=True)
        assert False, "Expected ValueError but none was raised"
    except ValueError as e:
        assert "duplicated" in str(e)
        print("✓ Duplicate handling works correctly")


def test_version_management():
    """Test version management functions."""
    mapper = FHIRMapper()
    
    # Add multiple versions of the same profile
    base_struct_def = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/VersionTest",
        "name": "VersionTest",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": False,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint"
    }
    
    # Add version 1.0.0
    struct_def_v1 = {**base_struct_def, "version": "1.0.0"}
    mapper.add_structure_definition(struct_def_v1)
    
    # Add version 1.1.0
    struct_def_v1_1 = {**base_struct_def, "version": "1.1.0"}
    mapper.add_structure_definition(struct_def_v1_1)
    
    # Add version 2.0.0
    struct_def_v2 = {**base_struct_def, "version": "2.0.0"}
    mapper.add_structure_definition(struct_def_v2)
    
    # Check versions
    versions = mapper.get_structure_definition_versions("http://example.org/StructureDefinition/VersionTest")
    assert "1.0.0" in versions
    assert "1.1.0" in versions
    assert "2.0.0" in versions
    assert len(versions) == 3
    
    print(f"✓ Version management works correctly. Found versions: {versions}")


def run_all_tests():
    """Run all repository management tests."""
    print("Testing FHIRMapper repository management methods...\n")
    
    test_add_structure_definition()
    test_add_structure_definitions_from_file()
    test_add_bundle_from_file()
    test_duplicate_handling()
    test_version_management()
    
    print("\n✅ All repository management tests passed!")


if __name__ == "__main__":
    run_all_tests()
