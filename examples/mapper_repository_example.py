"""
Example demonstrating FHIRMapper repository management

This example shows how to:
1. Add custom StructureDefinitions to the mapping engine
2. Load StructureDefinitions from files
3. Load FHIR packages
4. Check available resources
"""

import tempfile
import json
from pathlib import Path

from fhircraft.fhir.mapper import FHIRMapper


def example_add_custom_structure_definition():
    """Example of adding a custom StructureDefinition."""
    print("=== Adding Custom StructureDefinition ===")
    
    mapper = FHIRMapper()
    
    # Define a custom patient profile
    custom_patient_profile = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/CustomPatient",
        "version": "1.0.0",
        "name": "CustomPatient",
        "title": "Custom Patient Profile",
        "status": "draft",
        "description": "A custom patient profile with additional constraints",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": False,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Patient.identifier",
                    "path": "Patient.identifier",
                    "min": 1,
                    "mustSupport": True
                }
            ]
        }
    }
    
    # Add the custom profile
    mapper.add_structure_definition(custom_patient_profile)
    
    # Verify it was added
    if mapper.has_structure_definition("http://example.org/StructureDefinition/CustomPatient"):
        print("✓ Custom patient profile added successfully")
        
        # Get available versions
        versions = mapper.get_structure_definition_versions("http://example.org/StructureDefinition/CustomPatient")
        print(f"  Available versions: {versions}")
    else:
        print("✗ Failed to add custom patient profile")
    
    print()


def example_load_from_file():
    """Example of loading StructureDefinitions from a file."""
    print("=== Loading StructureDefinitions from File ===")
    
    mapper = FHIRMapper()
    
    # Create a bundle with multiple StructureDefinitions
    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [
            {
                "resource": {
                    "resourceType": "StructureDefinition",
                    "url": "http://example.org/StructureDefinition/CustomObservation",
                    "version": "1.0.0",
                    "name": "CustomObservation",
                    "title": "Custom Observation Profile",
                    "status": "draft",
                    "fhirVersion": "4.3.0",
                    "kind": "resource",
                    "abstract": False,
                    "type": "Observation",
                    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
                    "derivation": "constraint"
                }
            },
            {
                "resource": {
                    "resourceType": "StructureDefinition",
                    "url": "http://example.org/StructureDefinition/CustomCondition",
                    "version": "1.0.0",
                    "name": "CustomCondition",
                    "title": "Custom Condition Profile",
                    "status": "draft",
                    "fhirVersion": "4.3.0",
                    "kind": "resource",
                    "abstract": False,
                    "type": "Condition",
                    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Condition",
                    "derivation": "constraint"
                }
            }
        ]
    }
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(bundle, f, indent=2)
        temp_file = f.name
    
    try:
        # Load from file
        count = mapper.add_structure_definitions_from_file(temp_file)
        print(f"✓ Loaded {count} StructureDefinitions from file")
        
        # Verify they were loaded
        profiles = [
            "http://example.org/StructureDefinition/CustomObservation",
            "http://example.org/StructureDefinition/CustomCondition"
        ]
        
        for profile_url in profiles:
            if mapper.has_structure_definition(profile_url):
                print(f"  ✓ {profile_url} is available")
            else:
                print(f"  ✗ {profile_url} is missing")
        
    finally:
        # Clean up
        Path(temp_file).unlink()
    
    print()


def example_version_management():
    """Example of managing multiple versions."""
    print("=== Version Management ===")
    
    mapper = FHIRMapper()
    
    # Add multiple versions of the same profile
    base_profile = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/EvolvingProfile",
        "name": "EvolvingProfile",
        "title": "An Evolving Profile",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": False,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint"
    }
    
    # Add different versions
    versions_to_add = ["1.0.0", "1.1.0", "2.0.0", "2.1.0"]
    
    for version in versions_to_add:
        profile = {**base_profile, "version": version}
        mapper.add_structure_definition(profile)
    
    # Check available versions
    available_versions = mapper.get_structure_definition_versions(
        "http://example.org/StructureDefinition/EvolvingProfile"
    )
    
    print(f"✓ Added {len(versions_to_add)} versions")
    print(f"  Available versions: {available_versions}")
    
    # Test specific version checking
    for version in versions_to_add:
        if mapper.has_structure_definition(
            "http://example.org/StructureDefinition/EvolvingProfile", version
        ):
            print(f"  ✓ Version {version} is available")
        else:
            print(f"  ✗ Version {version} is missing")
    
    print()


def example_error_handling():
    """Example of error handling with duplicates."""
    print("=== Error Handling ===")
    
    mapper = FHIRMapper()
    
    profile = {
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
    mapper.add_structure_definition(profile, fail_if_exists=False)
    print("✓ Added profile first time")
    
    # Add again with fail_if_exists=False - should succeed (overwrite)
    mapper.add_structure_definition(profile, fail_if_exists=False)
    print("✓ Overwrote profile (fail_if_exists=False)")
    
    # Add again with fail_if_exists=True - should fail
    try:
        mapper.add_structure_definition(profile, fail_if_exists=True)
        print("✗ Expected error but succeeded")
    except ValueError as e:
        print(f"✓ Correctly raised error: {e}")
    
    print()


def example_mapping_with_custom_profile():
    """Example of using custom profiles in mappings."""
    print("=== Using Custom Profiles in Mappings ===")
    
    mapper = FHIRMapper()
    
    # Add a custom profile for the source
    source_profile = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/SourcePatient",
        "version": "1.0.0",
        "name": "SourcePatient",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": False,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint"
    }
    
    # Add a custom profile for the target
    target_profile = {
        "resourceType": "StructureDefinition",
        "url": "http://example.org/StructureDefinition/TargetPatient",
        "version": "1.0.0",
        "name": "TargetPatient",
        "status": "draft",
        "fhirVersion": "4.3.0",
        "kind": "resource",
        "abstract": False,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint"
    }
    
    # Add both profiles
    mapper.add_structure_definition(source_profile)
    mapper.add_structure_definition(target_profile)
    
    # Create a mapping that uses these profiles
    mapping_script = f"""
    map 'http://example.org/PatientTransform' = 'PatientTransform'
    
    uses 'http://example.org/StructureDefinition/SourcePatient' as source
    uses 'http://example.org/StructureDefinition/TargetPatient' as target
    
    group main(source src : SourcePatient, target tgt : TargetPatient) {{
        src.name -> tgt.name;
        src.identifier -> tgt.identifier;
    }}
    """
    
    print("✓ Added custom profiles for source and target")
    print("✓ Created mapping script that references custom profiles")
    print("  Mapping can now be parsed and executed with these profiles available")
    
    # Parse the mapping (this would use the custom profiles)
    try:
        structure_map = mapper.parse_mapping_script(mapping_script)
        print(f"✓ Successfully parsed mapping: {structure_map.name}")
        
        # Show the structure references
        for structure in structure_map.structure or []:
            print(f"  - Uses {structure.mode} structure: {structure.url}")
            
    except Exception as e:
        print(f"✗ Failed to parse mapping: {e}")
    
    print()


def example_inspect_repository():
    """Example of inspecting repository contents."""
    print("=== Inspecting Repository Contents ===")
    
    mapper = FHIRMapper()
    
    # Add some test profiles
    profiles = [
        {
            "url": "http://example.org/StructureDefinition/TestA",
            "version": "1.0.0",
            "name": "TestA"
        },
        {
            "url": "http://example.org/StructureDefinition/TestB",
            "version": "1.0.0",
            "name": "TestB"
        },
        {
            "url": "http://example.org/StructureDefinition/TestA",
            "version": "2.0.0",
            "name": "TestA"
        }
    ]
    
    for profile_data in profiles:
        profile = {
            "resourceType": "StructureDefinition",
            **profile_data,
            "status": "draft",
            "fhirVersion": "4.3.0",
            "kind": "resource",
            "abstract": False,
            "type": "Patient",
            "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
            "derivation": "constraint"
        }
        mapper.add_structure_definition(profile)
    
    # Check what's available
    test_urls = [
        "http://example.org/StructureDefinition/TestA",
        "http://example.org/StructureDefinition/TestB",
        "http://example.org/StructureDefinition/TestC"  # This one doesn't exist
    ]
    
    print("Repository contents check:")
    for url in test_urls:
        if mapper.has_structure_definition(url):
            versions = mapper.get_structure_definition_versions(url)
            print(f"  ✓ {url} - versions: {versions}")
        else:
            print(f"  ✗ {url} - not found")
    
    print()


if __name__ == "__main__":
    """Run all repository management examples."""
    print("FHIRMapper Repository Management Examples")
    print("=" * 50)
    
    example_add_custom_structure_definition()
    example_load_from_file() 
    example_version_management()
    example_error_handling()
    example_mapping_with_custom_profile()
    example_inspect_repository()
    
    print("🎉 All repository management examples completed!")
