# Resource Models

This guide is for developers who want to work with Fhircraft's built-in FHIR resource models. You'll learn to access core FHIR resources, create resource instances, validate data, and perform common operations using Fhircraft's pre-built Pydantic models.

Fhircraft provides ready-to-use Pydantic models for all standard FHIR resources across R4, R4B, and R5 releases. These models include automatic validation, type safety, and seamless integration with Python applications.

## Prerequisites

Before diving into this guide, make sure you understand:

- **Basic Python** and object-oriented programming
- **FHIR fundamentals** from the [FHIR Resources Overview](resources-overview.md)  
- **Pydantic basics** - See [Pydantic FHIR](pydantic-representation.md) for technical foundations

## Accessing Built-in Resources

Fhircraft provides pre-built Pydantic models for all core FHIR resources. You can access these models directly without any construction or setup.

### Using get_fhir_resource_type

The simplest way to access built-in resources is through the `get_fhir_resource_type` function:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Get the built-in Patient model for FHIR R5 (default)
Patient = get_fhir_resource_type("Patient")

# Specify a different FHIR version
PatientR4 = get_fhir_resource_type("Patient", "R4")
PatientR4B = get_fhir_resource_type("Patient", "R4B")
PatientR5 = get_fhir_resource_type("Patient", "R5")

# Get other resource types
Observation = get_fhir_resource_type("Observation")
Condition = get_fhir_resource_type("Condition")
Practitioner = get_fhir_resource_type("Practitioner")
Organization = get_fhir_resource_type("Organization")
```

## Creating Resource Instances

### Basic Resource Creation

Create FHIR resources using standard Python class instantiation with automatic validation:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Get the Patient model
Patient = get_fhir_resource_type("Patient", "R5")

# Create a basic patient
patient = Patient(
    name=[{
        "given": ["John"],
        "family": "Doe",
        "use": "official"
    }],
    gender="male",
    birthDate="1990-05-15"
)

print(f"Created patient: {patient.name[0].given[0]} {patient.name[0].family}")
```

### Using Complex Data Types

Work with FHIR's complex data types for rich resource modeling:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type
from fhircraft.fhir.resources.datatypes.R5.complex_types import (
    HumanName, ContactPoint, Address, Identifier
)

Patient = get_fhir_resource_type("Patient", "R5")

# Create a patient with comprehensive data
patient = Patient(
    # Multiple names with different uses
    name=[
        HumanName(
            given=["John", "Michael"],
            family="Doe",
            use="official",
            prefix=["Mr."]
        ),
        HumanName(
            given=["Johnny"],
            family="Doe", 
            use="nickname"
        )
    ],
    
    # Contact information
    telecom=[
        ContactPoint(
            system="phone",
            value="+1-555-123-4567",
            use="home"
        ),
        ContactPoint(
            system="email", 
            value="john.doe@example.com",
            use="work"
        )
    ],
    
    # Address information
    address=[
        Address(
            line=["123 Main Street", "Apt 4B"],
            city="Springfield",
            state="IL",
            postalCode="62701",
            country="US",
            use="home"
        )
    ],
    
    # Identifiers
    identifier=[
        Identifier(
            system="http://example.org/mrn",
            value="MRN123456",
            use="usual"
        )
    ],
    
    birthDate="1990-05-15",
    gender="male",
    active=True
)
```

### Alternative Construction Methods

#### From Dictionaries

Create resources from dictionary data (common when processing API responses):

```python
# Patient data from an API or database
patient_data = {
    "resourceType": "Patient",
    "name": [{
        "given": ["Jane"],
        "family": "Smith",
        "use": "official"
    }],
    "birthDate": "1985-03-22",
    "gender": "female",
    "active": True
}

Patient = get_fhir_resource_type("Patient")
patient = Patient.model_validate(patient_data)

print(f"Validated patient: {patient.name[0].given[0]} {patient.name[0].family}")
```

#### From JSON Strings

Parse FHIR JSON directly into validated resources:

```python
# FHIR JSON from an API or file
fhir_json = '''
{
    "resourceType": "Patient",
    "id": "example-patient",
    "name": [{
        "given": ["Bob"],
        "family": "Johnson"
    }],
    "birthDate": "1975-12-01",
    "gender": "male"
}
'''

Patient = get_fhir_resource_type("Patient")
patient = Patient.model_validate_json(fhir_json)

print(f"Parsed patient ID: {patient.id}")
```

#### From XML Strings

Similarly, parse FHIR XML using `model_validate_xml()`:

```python
# FHIR XML from an API or file
fhir_xml = '''<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="example-patient"/>
  <name>
    <given value="Bob"/>
    <family value="Johnson"/>
  </name>
  <birthDate value="1975-12-01"/>
  <gender value="male"/>
</Patient>'''

Patient = get_fhir_resource_type("Patient")
patient = Patient.model_validate_xml(fhir_xml)

print(f"Parsed patient ID: {patient.id}")
```

## Validation and Error Handling

Fhircraft automatically enforces all FHIR constraints, providing comprehensive validation for data integrity.

### Basic Validation

All FHIR resources are automatically validated when created. This example shows how validation works in practice, demonstrating both successful validation and how to handle validation failures:

```python
from pydantic import ValidationError

Patient = get_fhir_resource_type("Patient")

try:
    # This will succeed - valid patient data
    valid_patient = Patient(
        name=[{"given": ["John"], "family": "Doe"}],
        gender="male"
    )
    print("Patient created successfully")
    
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### Handling Validation Errors

For robust applications, it's important to handle validation errors gracefully and provide detailed feedback. This function demonstrates how to capture and report validation errors in a user-friendly format:

```python
def create_patient_safely(patient_data: dict) -> tuple[bool, any]:
    """Safely create a patient with detailed error handling."""
    try:
        Patient = get_fhir_resource_type("Patient")
        patient = Patient.model_validate(patient_data)
        return True, patient
    except ValidationError as e:
        errors = []
        for error in e.errors():
            field_path = ".".join(str(loc) for loc in error['loc'])
            errors.append(f"{field_path}: {error['msg']}")
        return False, errors

# Test with invalid data
invalid_data = {
    "name": [],  # Empty name list - invalid
    "birthDate": "not-a-date",  # Invalid date format
    "gender": "unknown-gender"  # Invalid gender code
}

success, result = create_patient_safely(invalid_data)
if success:
    patient = result
    print(f"Patient created: {patient.id}")
else:
    errors = result
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
```

### FHIR Constraint Validation

FHIR defines invariant constraints that are automatically enforced:

```python
from fhircraft.fhir.resources.datatypes.R5.complex_types import Quantity

try:
    # This violates FHIR invariant qty-3: code requires system
    invalid_quantity = Quantity(
        value=10.5,
        unit="mg",
        code="mg"  # Code without system
    )
except ValidationError as e:
    print(f"Constraint violation: {e.errors()[0]['msg']}")
    # Output: "If a code for the unit is present, the system SHALL also be present. [qty-3]"

# Correct version with both code and system
valid_quantity = Quantity(
    value=10.5,
    unit="milligrams",
    code="mg",
    system="http://unitsofmeasure.org"
)
print("Valid quantity created")
```

## Working with Resource Data

### Accessing Resource Properties

Once you have a resource instance, you can access its properties just like any Python object. This example shows how to read various types of data from a FHIR resource:

```python
Patient = get_fhir_resource_type("Patient")
patient = Patient(
    name=[{"given": ["Alice"], "family": "Johnson"}],
    gender="female",
    birthDate="1992-08-15"
)

# Access basic properties
print(f"Resource type: {patient.resourceType}")
print(f"Patient name: {patient.name[0].given[0]} {patient.name[0].family}")
print(f"Gender: {patient.gender}")
print(f"Birth date: {patient.birthDate}")

# Check for optional properties
if patient.telecom:
    print(f"Contact info available: {len(patient.telecom)} entries")
else:
    print("No contact information")
```

### Modifying Resource Data

FHIR resources are mutable Python objects, so you can update their properties after creation. This is useful for building resources incrementally or updating data based on new information:

```python
# Add contact information
from fhircraft.fhir.resources.datatypes.R5.complex_types import ContactPoint

patient.telecom = [
    ContactPoint(
        system="email",
        value="alice.johnson@example.com",
        use="work"
    )
]

# Update existing data
patient.active = True
patient.gender = "female"

print(f"Updated patient: {patient.name[0].family}, Active: {patient.active}")
```

## Serialization and Deserialization

### JSON Serialization

Converting FHIR resources to and from JSON is essential for API communication and data storage. Fhircraft provides convenient methods for serialization that ensure FHIR compliance:

```python
Patient = get_fhir_resource_type("Patient")
patient = Patient(
    name=[{"given": ["John"], "family": "Doe"}],
    gender="male",
    birthDate="1990-01-15"
)

# Serialize to FHIR JSON (recommended - excludes None values)
patient_json = patient.model_dump_json(exclude_none=True)
print("FHIR JSON:")
print(patient_json)

# Serialize to Python dictionary
patient_dict = patient.model_dump(exclude_none=True)
print(f"Dictionary keys: {list(patient_dict.keys())}")
```

### XML Serialization

Fhircraft also supports FHIR XML format:

```python
# Serialize to FHIR XML
patient_xml = patient.model_dump_xml(pretty=True)
print("FHIR XML:")
print(patient_xml)
# Output:
# <?xml version="1.0" ?>
# <Patient xmlns="http://hl7.org/fhir">
#   <name>
#     <given value="John"/>
#     <family value="Doe"/>
#   </name>
#   <gender value="male"/>
#   <birthDate value="1990-01-15"/>
# </Patient>
```

### Advanced Options

For different use cases, you may need specific serialization formats or want to include/exclude certain fields. These options provide fine-grained control over the output:

```python
# Pretty-formatted JSON for debugging
formatted_json = patient.model_dump_json(
    exclude_none=True,
    indent=2
)
print("Formatted JSON:")
print(formatted_json)

# Pretty-formatted XML
formatted_xml = patient.model_dump_xml(pretty=True)
print("Formatted XML:")
print(formatted_xml)

# Include only specific fields
name_only = patient.model_dump(include={'resourceType', 'name', 'gender'})
print(f"Partial data: {name_only}")

# Exclude specific fields
without_meta = patient.model_dump(exclude={'meta', 'text'}, exclude_none=True)
```

## Working with Multiple FHIR Versions

### Version-Specific Models

Fhircraft supports multiple FHIR versions simultaneously. Each version has specific data types and validation rules, so you can work with the appropriate version for your use case:

```python
# Create patients using different FHIR versions
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

PatientR4 = get_fhir_resource_type("Patient", "R4")
PatientR5 = get_fhir_resource_type("Patient", "R5")

# Each version has specific constraints and features
patient_r4 = PatientR4(
    name=[{"family": "Smith", "given": ["John"]}],
    gender="male"
)

patient_r5 = PatientR5(
    name=[{"family": "Doe", "given": ["Jane"]}], 
    gender="female"
)

print(f"R4 Patient: {type(patient_r4).__name__}")
print(f"R5 Patient: {type(patient_r5).__name__}")
```

## What's Next?

Now that you understand how to work with built-in FHIR resources, explore these related topics:

- **[Resource Factory](resources-construction.md)** - Learn to build custom models from FHIR specifications and packages
- **[FHIR Path](fhirpath.md)** - Master querying and updating resources with FHIRPath expressions
- **[Pydantic FHIR](pydantic-representation.md)** - Understand the technical foundations of FHIR representation
- **[FHIR Mapper](mapper.md)** - Transform external data into validated FHIR resources

For a comprehensive overview of all Fhircraft capabilities, see the [User Guide overview](overview.md).

---

**Continue learning:** [Resource Factory →](resources-construction.md)