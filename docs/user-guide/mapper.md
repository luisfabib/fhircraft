# FHIR Mapper

This guide is for developers who want to transform data between different structures using Fhircraft's FHIR Mapping Language implementation. You'll learn to convert legacy system data to FHIR resources, transform between FHIR profiles, and handle complex data transformations with automatic validation.

## Prerequisites

Before working with the FHIR Mapper, you should understand:

- **FHIR resource basics** from [FHIR Resources Overview](resources-overview.md)
- **Creating and validating resources** from [Resource Models](resources-models.md)
- **Basic FHIR Mapping Language concepts** - See the [official specification](https://hl7.org/fhir/mapping-language.html)

## Overview

Fhircraft's FHIR Mapper implements the official [FHIR Mapping Language](https://hl7.org/fhir/mapping-language.html), enabling you to write declarative transformation rules that reliably convert data while maintaining FHIR compliance and type safety.

All mapped data is automatically validated using the resource models you learned about in previous sections, ensuring output compliance with FHIR specifications.

!!! important "Early FHIR Feature"

    The FHIR Mapping Language specification is specified as a `Maturity Level 0 (Draft)`, meaning that both the language specification and its implementations are bound to change in the future.

## Quick Start

Transform legacy patient data to a FHIR Patient resource:

```python
from fhircraft.fhir.mapper import FHIRMapper

# Legacy system data
legacy_patient = {
    "firstName": "Alice",
    "lastName": "Johnson",
    "dob": "1985-03-15",
    "sex": "F"
}

# Mapping script
mapping_script = """
map 'http://example.org/legacy-to-fhir' = 'LegacyPatient'

group main(source legacy, target patient: Patient) {
    legacy -> patient.name as name then {
        legacy.firstName -> name.given;
        legacy.lastName -> name.family;
    };
    legacy.dob -> patient.birthDate;
    legacy.sex where($this = 'F') -> patient.gender = 'female';
    legacy.sex where($this = 'M') -> patient.gender = 'male';
}
"""

# Execute transformation
mapper = FHIRMapper()
targets = mapper.execute_mapping(mapping_script, legacy_patient)
patient = targets[0]

print(f"Transformed: {patient}")
```

## Understanding FHIR Mapping

The FHIR Mapping Language provides a declarative way to transform data between different structures. Think of it as writing rules that describe how to copy, transform, and validate data from source formats into FHIR-compliant resources.

### Key Benefits

**Declarative Approach**: Instead of writing imperative code with loops and conditions, you declare what the end result should look like. The mapper handles the execution details.

**Automatic Validation**: Every transformation automatically validates the output against FHIR constraints, catching errors before they reach your application.

**Maintainable Rules**: Mapping rules are easier to read, modify, and audit compared to custom transformation code.

**Standards Compliance**: Built on the official FHIR specification, ensuring compatibility with other FHIR systems. The maps are FHIR-compliant and can be used within other FHIR systems outside of Fhircraft.

### When to Use FHIR Mapper

**Use FHIR Mapper when:**

- Converting legacy system data to FHIR resources
- Transforming between different FHIR profiles (e.g., US Core to International)
- Standardizing data from multiple sources with different schemas
- Need audit trails and transformation metadata
- Working with complex nested data structures
- Applying consistent business rules across transformations
- Mapping within a FHIR server

**Consider alternatives when:**

- Simple one-to-one field copying without validation needs
- One-time data migration where mapping rules won't be reused
- Performance is absolutely critical (direct Python code may be faster)
- Working with identical source and target structures

## Basic Mapping Concepts

### Mapping Structure

Every FHIR mapping consists of three main parts:

1. **Map Declaration**: Defines the mapping's identity and metadata
2. **Uses Statements**: Declare the structure definitions for source and target data
3. **Groups**: Contain the actual transformation rules

### Simple Field Mapping

The most basic transformation copies values directly from source fields to target fields:

```python
from fhircraft.fhir.mapper import FHIRMapper

# Basic mapping structure
script = """
map 'http://example.org/simple-mapping' = 'SimpleMapping'

group main(source src, target tgt) {
    // Direct field copying
    src.name -> tgt.fullName;
    src.age -> tgt.yearsOld;
    src.email -> tgt.contactEmail;
}
"""

source_data = {"name": "John Doe", "age": 30, "email": "john@example.com"}
mapper = FHIRMapper()
targets = mapper.execute_mapping(script, source_data)
```

### Working with FHIR Resources

Transform data into validated FHIR resources by specifying structure definitions:

```python
# Mapping to FHIR Patient
script = """
map 'http://example.org/patient-mapping' = 'PatientMapping'

uses "http://hl7.org/fhir/StructureDefinition/Patient" alias Patient as target

group main(source legacy, target patient: Patient) {
    legacy -> patient.name as name then {
        legacy.firstName -> name.given;
        legacy.lastName -> name.family;
    };
    legacy.dob -> patient.birthDate;
    legacy.sex where($this = 'F') -> patient.gender = 'female';
    legacy.sex where($this = 'M') -> patient.gender = 'male';
}
"""

legacy_data = {
    "firstName": "Alice", 
    "lastName": "Johnson",
    "dob": "1985-03-15",
    "sex": "F"
}

targets = mapper.execute_mapping(script, legacy_data)
patient = targets[0]  # Validated FHIR Patient resource
```

## Complex Mappings

### Nested Object Transformations

FHIR resources often contain nested objects and complex structures. This example demonstrates how to map data into FHIR's hierarchical structure, creating nested objects as needed:

```python
script = """
map 'http://example.org/nested' = 'NestedMapping'

group main(source src, target patient: Patient) {
    // Map to nested structures
    src -> patient.name as name then {
        src.fullName -> name.text;
        src.firstName -> name.given;
        src.lastName -> name.family;
    };
    
    // Transform collections
    src.phoneNumbers -> patient.telecom as telecom then {
        phoneNumbers.number -> telecom.value;
        phoneNumbers.type -> telecom.system;
    };
    
    // Conditional nested mapping
    src.emergencyContact where(exists()) -> patient.contact as contact then {
        emergencyContact.name -> contact.name as cname then {
            emergencyContact.name -> cname.text;
        };
        emergencyContact.relationship -> contact.relationship as rel then {
            emergencyContact.relationship -> rel.text;
        };
    };
}
"""

source_data = {
    "fullName": "Alice Johnson",
    "firstName": "Alice",
    "lastName": "Johnson",
    "phoneNumbers": [
        {"number": "555-0123", "type": "phone"},
        {"number": "alice@email.com", "type": "email"}
    ],
    "emergencyContact": {
        "name": "Bob Johnson",
        "relationship": "spouse"
    }
}
```

### Multiple Groups

Organize complex mappings using multiple transformation groups:

```python
script = """
map 'http://example.org/multi-group' = 'MultiGroup'

group main(source src, target patient: Patient) {
    src -> patient then demographics(src, patient);
    src -> patient then contacts(src, patient);
    src -> patient then identifiers(src, patient);
}

group demographics(source src, target patient: Patient) {
    src.name -> patient.name as name then {
        src.name -> name.text;
    };
    src.birthDate -> patient.birthDate;
    src.gender -> patient.gender;
}

group contacts(source src, target patient: Patient) {
    src.phone as phone -> patient.telecom as tel then {
        phone -> tel.value, tel.system='phone';
    };
    src.email as email -> patient.telecom as email then {
        email -> email.value, email.system='email';
    };
}

group identifiers(source src, target patient: Patient) {
    src.ssn -> patient.identifier as id then {
        ssn -> id.value, id.system='http://hl7.org/fhir/sid/us-ssn';
    };
}
"""

# Execute specific group
targets = mapper.execute_mapping(script, source_data, group="demographics")
```

## Multi-Source Transformations

Combine data from multiple sources into a single FHIR resource:

```python
script = """
map 'http://example.org/multi-source' = 'MultiSource'

group main(source demographics, source insurance, target patient: Patient) {
    // Data from demographics source
    demographics.name -> patient.name as name then {
        demographics.name -> name.text;
    };
    demographics.birthDate -> patient.birthDate;
    demographics.gender -> patient.gender;
    
    // Data from insurance source
    insurance -> patient.identifier as id then {
        insurance.policyNumber -> id.value;
        insurance.carrier -> id.system;
        insurance.memberSince -> id.period as period then {
            insurance.memberSince -> period.start;
        };
    };
}
"""

# Multiple source data
demo_data = {
    "name": "Alice Johnson",
    "birthDate": "1985-03-15",
    "gender": "female"
}
insurance_data = {
    "policyNumber": "POL-12345",
    "carrier": "ACME Insurance",
    "memberSince": "2020-01-01"
}

# Pass sources as tuple
targets = mapper.execute_mapping(
    script,
    (demo_data, insurance_data)
)
```

## Loading Structure Maps

### From Files and URLs

For complex mappings or reusable transformations, you can store mapping definitions in files or load them from remote URLs. This approach promotes maintainability and sharing of mapping logic:

```python
# Load from JSON file
structure_map = mapper.load_structure_map("patient-mapping.json")
targets = mapper.execute_mapping(structure_map, source_data)

# Load from URL
structure_map = mapper.load_structure_map(
    "https://example.org/fhir/StructureMap/PatientMapping"
)
```

### Working with Structure Definitions

Register custom structure definitions for complex mappings:

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# Define custom source structure
source_structure_def = {
    "resourceType": "StructureDefinition",
    "url": "http://example.org/StructureDefinition/LegacyPatient",
    "version": "0.1.0",
    "name": "LegacyPatient",
    "status": "draft",
    "kind" : "resource",
    "abstract" : False,
    "type" : "LegacyPatient",
}

# Register with mapper
mapper.add_structure_definition(source_structure_def)

# Use in mapping script
script = """
map 'http://example.org/legacy' = 'LegacyMapping'

uses "http://example.org/StructureDefinition/LegacyPatient" alias LegacyPatient as source
uses "http://hl7.org/fhir/StructureDefinition/Patient" alias Patient as target

group main(source legacy: LegacyPatient, target patient: Patient) {
    legacy.fullName -> patient.name as name then {
        legacy.fullName -> name.text;
    };
    legacy.dateOfBirth -> patient.birthDate;
}
"""
```

## Error Handling

Handle mapping failures gracefully:

```python
from fhircraft.fhir.mapper.engine.exceptions import MappingError

try:
    targets = mapper.execute_mapping(script, source_data)
    patient = targets[0]
except MappingError as e:
    print(f"Mapping failed: {e}")
    print(f"Rule: {e.rule_path}")
    print(f"Context: {e.context}")
except ValidationError as e:
    print(f"FHIR validation failed: {e}")
```
