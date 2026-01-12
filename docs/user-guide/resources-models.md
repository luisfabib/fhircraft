# Working with FHIR Resource Models

This guide shows you how to create, validate, and manipulate FHIR resources using Fhircraft's pre-built models. Building on the FHIR concepts covered earlier, you will learn practical recipes for common tasks like creating patient records, validating data from external systems, and converting between JSON and Python objects.

## Understanding Resource Models

FHIR defines over 140 different [resource types](https://www.hl7.org/fhir/resourcelist.html) like Patient, Observation, and Medication. Each resource type has a specific structure with required fields, optional fields, data types, and validation rules. Manually creating and validating these resources would require extensive code to check every constraint and relationship.

Fhircraft provides pre-built [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/) for all standard FHIR resources across R4, R4B, and R5 releases. Pydantic is a Python library that provides data validation and settings management using Python type annotations. These models automatically validate data when you create resources, ensuring compliance with FHIR specifications without writing validation code yourself.

Using these models means you can focus on your healthcare application logic rather than FHIR implementation details. The models provide type safety, catching errors during development rather than at runtime. They also integrate seamlessly with Python applications, IDEs, and type checkers, giving you autocomplete suggestions and early error detection. All validation follows the same FHIR constraints covered in earlier sections on validation configuration and resource construction.

## Getting Resource Models

Before you can create FHIR resources, you need to obtain the appropriate model class. Fhircraft provides all standard FHIR resource models ready to use without any setup or configuration. The models are organized by FHIR version, allowing you to work with the specific version your application requires.

The get_fhir_resource_type function is your entry point to these models. It takes a resource type name and optionally a FHIR version, returning the corresponding [Pydantic BaseModel](https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage) subclass. This function handles all the complexity of locating the right model for your chosen FHIR version:

```python
# Import the resource type resolver
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Get Patient model for FHIR R5 (the default version)
Patient = get_fhir_resource_type("Patient")

# Get models for specific FHIR versions
PatientR4 = get_fhir_resource_type("Patient", "R4")    # FHIR 4.0.1
PatientR4B = get_fhir_resource_type("Patient", "R4B")  # FHIR 4.3.0
PatientR5 = get_fhir_resource_type("Patient", "R5")    # FHIR 5.0.0

# Get models for other resource types
Observation = get_fhir_resource_type("Observation")    # Lab results, vital signs
Condition = get_fhir_resource_type("Condition")        # Diagnoses, problems
Practitioner = get_fhir_resource_type("Practitioner")  # Healthcare providers
Organization = get_fhir_resource_type("Organization")  # Healthcare facilities

print(f"Patient model: {Patient}")
```

The returned model is a standard Python class that you instantiate like any other class. These models use [Pydantic's validation](https://docs.pydantic.dev/latest/concepts/validators/) to ensure data correctness.

## Creating Resources

Creating FHIR resources with Fhircraft follows standard Python patterns. You instantiate the model class with keyword arguments representing the resource fields. The [Pydantic model constructor](https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage) automatically validates all data, checking types, required fields, and FHIR constraints.

### Basic Patient Creation

The most common healthcare resource is Patient, which represents people receiving care. Creating a basic patient requires only minimal information, though you can add as much detail as your application needs:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Get the Patient model for FHIR R5
Patient = get_fhir_resource_type("Patient", "R5")

# Create a patient with basic demographics
patient = Patient(
    name=[{                      # Name is an array of HumanName objects
        "given": ["John"],       # Given names (first, middle)
        "family": "Doe",         # Family name (last name)
        "use": "official"        # How this name is used
    }],
    gender="male",               # Administrative gender
    birthDate="1990-05-15"       # Date of birth in YYYY-MM-DD format
)

# Access the created data
print(f"Created patient: {patient.name[0].given[0]} {patient.name[0].family}")
print(f"Gender: {patient.gender}, DOB: {patient.birthDate}")
```

Pydantic validates all data during construction, ensuring the gender uses a valid [FHIR code](https://www.hl7.org/fhir/valueset-administrative-gender.html) and birthDate follows the proper format.

### Complete Patient Record Recipe

Real patient records contain multiple names, contact methods, addresses, and identifiers. FHIR uses [complex data types](https://www.hl7.org/fhir/datatypes.html) to represent these rich structures. This recipe shows how to create a comprehensive patient record with all common elements:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type
# Import FHIR complex data types
from fhircraft.fhir.resources.datatypes.R5.complex import (
    HumanName,      # Person names
    ContactPoint,   # Phone, email, etc.
    Address,        # Physical addresses
    Identifier      # System identifiers like MRN
)

Patient = get_fhir_resource_type("Patient", "R5")

# Create a comprehensive patient record
patient = Patient(
    # Multiple names for different contexts
    name=[
        HumanName(
            given=["John", "Michael"],  # First and middle names
            family="Doe",                # Last name
            use="official",              # Legal/official name
            prefix=["Mr."]               # Title
        ),
        HumanName(
            given=["Johnny"],
            family="Doe", 
            use="nickname"               # Informal name
        )
    ],
    
    # Contact methods (phone, email, etc.)
    telecom=[
        ContactPoint(
            system="phone",              # Type of contact
            value="+1-555-123-4567",    # Actual contact value
            use="home"                   # Context of use
        ),
        ContactPoint(
            system="email", 
            value="john.doe@example.com",
            use="work"
        )
    ],
    
    # Physical addresses
    address=[
        Address(
            line=["123 Main Street", "Apt 4B"],  # Street address lines
            city="Springfield",
            state="IL",
            postalCode="62701",
            country="US",
            use="home"                            # Address type
        )
    ],
    
    # System identifiers
    identifier=[
        Identifier(
            system="http://example.org/mrn",  # Identifier system URL
            value="MRN123456",                 # Actual identifier value
            use="usual"                        # Primary identifier
        )
    ],
    
    # Demographics
    birthDate="1990-05-15",
    gender="male",
    active=True  # Whether record is in active use
)

print(f"Created comprehensive patient: {patient.identifier[0].value}")
```

Using [Pydantic models for complex types](https://docs.pydantic.dev/latest/concepts/models/#nested-models) ensures each component validates independently, catching errors at the field level.

## Common Data Import Recipes

Healthcare applications frequently need to convert data from external systems, APIs, databases, or files into FHIR resources. These recipes show common patterns for importing data in various formats.

### Creating from API Response Data

When your application receives JSON data from a REST API, database query, or external system, you typically have Python dictionaries. Pydantic's [model_validate](https://docs.pydantic.dev/latest/concepts/models/#model-methods-and-properties) method converts dictionaries into validated model instances:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Example: Data received from a REST API or database
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

# Validate and convert dictionary to Patient model
# This performs all FHIR validation automatically
patient = Patient.model_validate(patient_data)

# Now you have a fully validated Patient object
print(f"Validated patient: {patient.name[0].given[0]} {patient.name[0].family}")
print(f"Type: {type(patient)}")
```

The [model_validate method](https://docs.pydantic.dev/latest/concepts/models/#model-methods-and-properties) is the recommended way to parse untrusted data, as it validates every field according to FHIR rules.

### Parsing FHIR JSON Files

When reading FHIR data from files, HTTP responses, or string variables, you often have JSON text rather than Python dictionaries. Pydantic's [model_validate_json](https://docs.pydantic.dev/latest/concepts/models/#creating-models-without-validation) method parses and validates JSON strings in one operation:

```python
# Example: JSON string from a file or HTTP response
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

# Parse JSON string and validate in one step
patient = Patient.model_validate_json(fhir_json)

# Access the parsed data as Python objects
print(f"Parsed patient ID: {patient.id}")
print(f"Name: {patient.name[0].family}, {patient.name[0].given[0]}")

# Practical file reading example
with open("test/static/fhir-core-examples/R5/patient-example-proband.json", "r") as file:
    patient_from_file = Patient.model_validate_json(file.read())
```

Using [model_validate_json](https://docs.pydantic.dev/latest/concepts/models/#creating-models-without-validation) is more efficient than manually parsing JSON and then validating, as it combines both operations.

### Parsing FHIR XML Files

Some healthcare systems still use XML format for FHIR data exchange. Fhircraft supports [FHIR XML](https://www.hl7.org/fhir/xml.html) parsing with the same validation as JSON:

```python
# Example: XML string from legacy system or file
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

# Parse XML and validate against FHIR specification
patient = Patient.model_validate_xml(fhir_xml)

print(f"Parsed patient ID: {patient.id}")

# Practical XML file reading example
with open("test/static/fhir-core-examples/R5/patient-example-proband.xml", "r") as file:
    patient_from_xml = Patient.model_validate_xml(file.read())
    print(patient_from_xml.gender)
    #> female
```

## Validation Recipes

Validation happens automatically whenever you create or parse FHIR resources. Understanding how validation works and how to handle errors helps you build robust healthcare applications that catch data quality issues early.

### Understanding Automatic Validation

Pydantic performs [validation automatically](https://docs.pydantic.dev/latest/concepts/validators/) during model construction. You do not need to call separate validation methods. Every time you create a resource, Pydantic checks data types, required fields, value ranges, and FHIR constraints:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type
from pydantic import ValidationError

Patient = get_fhir_resource_type("Patient")

try:
    # This succeeds - all data meets FHIR requirements
    valid_patient = Patient(
        name=[{"given": ["John"], "family": "Doe"}],
        gender="male"  # Valid FHIR gender code
    )
    print("Patient created successfully")
    print(f"Gender validated: {valid_patient.gender}")
    
except ValidationError as e:
    # Pydantic raises ValidationError when data is invalid
    print(f"Validation failed: {e}")
```

The [ValidationError](https://docs.pydantic.dev/latest/errors/errors/) contains detailed information about what went wrong, which fields are invalid, and why.

### Production Error Handling Recipe

Production applications need robust error handling that captures validation failures, logs them appropriately, and provides clear feedback. This recipe shows a reusable pattern for safe resource creation with detailed error reporting:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type
from pydantic import ValidationError
from typing import Union, List

def create_patient_safely(patient_data: dict) -> tuple[bool, Union[any, List[str]]]:
    """Safely create a patient with detailed error reporting.
    
    Returns:
        (True, patient) if successful
        (False, error_list) if validation fails
    """
    try:
        Patient = get_fhir_resource_type("Patient")
        # Attempt to validate and create the patient
        patient = Patient.model_validate(patient_data)
        return True, patient
        
    except ValidationError as e:
        # Extract human-readable error messages
        errors = []
        for error in e.errors():
            # Build field path (e.g., "name.0.given")
            field_path = ".".join(str(loc) for loc in error['loc'])
            # Combine path and error message
            errors.append(f"{field_path}: {error['msg']}")
        return False, errors

# Example: Handle data from an external system
invalid_data = {
    "name": [],                     # FHIR requires at least one name
    "birthDate": "not-a-date",      # Must be YYYY-MM-DD format
    "gender": "unknown-gender"      # Must be male|female|other|unknown
}

success, result = create_patient_safely(invalid_data)
if success:
    patient = result
    print(f"Patient created: {patient.id}")
else:
    errors = result
    print("Validation errors found:")
    for error in errors:
        print(f"  - {error}")
    # In production: log errors, alert monitoring system, etc.
```

This pattern uses Pydantic's [error handling](https://docs.pydantic.dev/latest/errors/errors/) to provide actionable feedback about data quality issues.

### FHIR Constraint Validation Recipe

Beyond basic type checking, FHIR defines [invariant constraints](https://www.hl7.org/fhir/conformance-rules.html#constraints) that enforce business rules. For example, if a Quantity has a code, it must also have a system. Fhircraft validates these constraints automatically:

```python
from fhircraft.fhir.resources.datatypes.R5.complex import Quantity
from pydantic import ValidationError

try:
    # This violates FHIR invariant qty-3
    # "If a code for the unit is present, the system SHALL also be present"
    invalid_quantity = Quantity(
        value=10.5,
        unit="mg",
        code="mg"  # Code without corresponding system - INVALID
    )
except ValidationError as e:
    print(f"Constraint violation: {e.errors()[0]['msg']}")
    # Output shows which FHIR constraint failed: [qty-3]

# Correct version follows FHIR invariant rules
valid_quantity = Quantity(
    value=10.5,
    unit="milligrams",
    code="mg",                              # UCUM code
    system="http://unitsofmeasure.org"     # Required system for code
)
print(f"Valid quantity: {valid_quantity.value} {valid_quantity.unit}")
```

These FHIR-specific constraints are documented in the [resource definitions](https://www.hl7.org/fhir/resource.html) and validated automatically by Fhircraft.

## Working with Resource Data

Once you have created or parsed a FHIR resource, you need to read its data, modify it, and export it to other systems. These recipes show common patterns for working with resource data using [Pydantic's model API](https://docs.pydantic.dev/latest/concepts/models/).

### Reading Resource Data Recipe

FHIR resources are standard Python objects with properties you access using dot notation. This recipe shows safe patterns for reading data, including handling optional fields that might not exist:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

Patient = get_fhir_resource_type("Patient")
patient = Patient(
    name=[{"given": ["Alice"], "family": "Johnson"}],
    gender="female",
    birthDate="1992-08-15"
)

# Access properties using dot notation (standard Python)
print(f"Resource type: {patient.resourceType}")  # Always "Patient"
print(f"Family name: {patient.name[0].family}")  # Access nested properties
print(f"Given name: {patient.name[0].given[0]}")  # Arrays use index
print(f"Gender: {patient.gender}")
print(f"Birth date: {patient.birthDate}")

# Safe pattern for optional fields (may be None)
if patient.telecom:  # Check if field exists
    print(f"Contact info available: {len(patient.telecom)} entries")
    for contact in patient.telecom:
        print(f"  {contact.system}: {contact.value}")
else:
    print("No contact information")

# Use getattr for dynamic field access
field_value = getattr(patient, "gender", "not specified")
print(f"Gender (safe): {field_value}")
```

Pydantic models use [Python descriptors](https://docs.pydantic.dev/latest/concepts/models/#model-methods-and-properties) for field access, providing IDE autocomplete and type checking.

### Updating Resource Data Recipe

Pydantic models are mutable by default, allowing you to modify resource properties after creation. Changes trigger validation automatically, ensuring the resource remains FHIR-compliant. This recipe shows safe patterns for updating resources:

```python
from fhircraft.fhir.resources.datatypes.R5.complex import ContactPoint
from pydantic import ValidationError

# Add new data to existing resource
patient.telecom = [
    ContactPoint(
        system="email",
        value="alice.johnson@example.com",
        use="work"
    )
]
print(f"Added contact: {patient.telecom[0].value}")

# Update existing fields
patient.active = True   # Mark record as active
patient.gender = "female"

# Append to arrays
from fhircraft.fhir.resources.datatypes.R5.complex import ContactPoint
if not patient.telecom:
    patient.telecom = []
patient.telecom.append(
    ContactPoint(system="phone", value="555-0123", use="mobile")
)

print(f"Updated patient: {patient.name[0].family}, Active: {patient.active}")
print(f"Contact methods: {len(patient.telecom)}")

# Validation happens automatically on modification
try:
    patient.gender = "invalid-code"  # This will raise ValidationError
except ValidationError as e:
    print(f"Update rejected: {e.errors()[0]['msg']}")
```

Pydantic's [validators run on assignment](https://docs.pydantic.dev/latest/concepts/validators/#field-validators) by default, catching invalid modifications immediately.

## Data Export Recipes

Healthcare systems exchange data using standardized formats. These recipes show how to convert your resource models into JSON, XML, and Python dictionaries for storage, transmission, and integration.

### Exporting to JSON Recipe

JSON is the most common format for FHIR data exchange. Pydantic provides [serialization methods](https://docs.pydantic.dev/latest/concepts/serialization/) that convert models to JSON while respecting FHIR formatting rules:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

Patient = get_fhir_resource_type("Patient")
patient = Patient(
    name=[{"given": ["John"], "family": "Doe"}],
    gender="male",
    birthDate="1990-01-15"
)

# Export to FHIR-compliant JSON string
# exclude_none=True removes fields with no value (FHIR best practice)
patient_json = patient.model_dump_json(exclude_none=True)
print("Compact JSON for API transmission:")
print(patient_json)

# Export to Python dictionary (for database storage, processing)
patient_dict = patient.model_dump(exclude_none=True)
print(f"\nDictionary keys: {list(patient_dict.keys())}")
print(f"Resource type: {patient_dict['resourceType']}")

# Save to file
with open("patient.json", "w") as file:
    file.write(patient_json)
print("Saved to patient.json")
```

The [model_dump_json method](https://docs.pydantic.dev/latest/concepts/serialization/#modelmodel_dump_json) ensures proper JSON formatting according to FHIR specifications.

### Exporting to XML Recipe

Some healthcare systems require [FHIR XML format](https://www.hl7.org/fhir/xml.html). Fhircraft provides XML serialization with proper FHIR namespace handling:

```python
# Export to FHIR XML format
# indent parameter controls formatting (None for compact, integer for spaces)
patient_xml = patient.model_dump_xml(indent=3)
print("FHIR XML:")
print(patient_xml)

# The output follows FHIR XML conventions:
# <?xml version="1.0" ?>
# <Patient xmlns="http://hl7.org/fhir">
#   <name>
#     <given value="John"/>
#     <family value="Doe"/>
#   </name>
#   <gender value="male"/>
#   <birthDate value="1990-01-15"/>
# </Patient>

# Save to XML file
with open("patient.xml", "w") as file:
    file.write(patient_xml)
```

### Advanced Export Options Recipe

Pydantic provides [extensive serialization options](https://docs.pydantic.dev/latest/concepts/serialization/) for controlling output format. These recipes show common customization patterns:

```python
# Recipe 1: Human-readable JSON for debugging
formatted_json = patient.model_dump_json(
    exclude_none=True,  # Omit empty fields
    indent=2            # Pretty print with 2 spaces
)
print("Readable JSON for debugging:")
print(formatted_json)

# Recipe 2: Export only specific fields (for APIs with field filtering)
name_and_gender = patient.model_dump(
    include={'resourceType', 'name', 'gender'}  # Only these fields
)
print(f"\nPartial export: {name_and_gender}")

# Recipe 3: Exclude sensitive or meta fields
public_data = patient.model_dump(
    exclude={'meta', 'text', 'identifier'},  # Remove internal/sensitive data
    exclude_none=True
)
print(f"\nPublic data only: {list(public_data.keys())}")

# Recipe 4: Custom serialization for databases
import json
db_record = json.dumps(
    patient.model_dump(exclude_none=True),
    ensure_ascii=False  # Preserve non-ASCII characters
)
print(f"\nDatabase-ready JSON length: {len(db_record)} chars")

# Recipe 5: Compact XML for bandwidth-limited scenarios
compact_xml = patient.model_dump_xml(indent=None)  # No whitespace
print(f"\nCompact XML length: {len(compact_xml)} chars")
```

These options use Pydantic's [include/exclude parameters](https://docs.pydantic.dev/latest/concepts/serialization/#include-and-exclude) for fine-grained control.

## Working Across FHIR Versions

Healthcare organizations transition between FHIR versions over time. Systems may need to support multiple versions simultaneously during migration periods. Fhircraft provides complete support for [FHIR R4, R4B, and R5](https://www.hl7.org/fhir/versions.html), allowing you to work with different versions in the same application.

### Using Different FHIR Versions Recipe

Each FHIR version has version-specific data types, value sets, and constraints. This recipe shows how to work with resources from different FHIR versions:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Get models for specific FHIR versions
PatientR4 = get_fhir_resource_type("Patient", "R4")    # FHIR 4.0.1
PatientR4B = get_fhir_resource_type("Patient", "R4B")  # FHIR 4.3.0
PatientR5 = get_fhir_resource_type("Patient", "R5")    # FHIR 5.0.0

# Each version may have different fields and constraints
patient_r4 = PatientR4(
    name=[{"family": "Smith", "given": ["John"]}],
    gender="male"  # R4 uses administrative-gender value set
)

patient_r5 = PatientR5(
    name=[{"family": "Doe", "given": ["Jane"]}], 
    gender="female"  # R5 may have expanded gender options
)

# Models are version-specific
print(f"R4 Patient class: {type(patient_r4).__name__}")
print(f"R5 Patient class: {type(patient_r5).__name__}")
print(f"Same patient type: {PatientR4 is PatientR5}")  # False

# Export maintains version-specific formatting
r4_json = patient_r4.model_dump_json(exclude_none=True)
r5_json = patient_r5.model_dump_json(exclude_none=True)
print(f"\nR4 JSON: {r4_json}")
print(f"R5 JSON: {r5_json}")
```

Each FHIR version has [specific validation rules](https://www.hl7.org/fhir/versions.html#change) that the models enforce automatically.

## Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| ValidationError when creating resource | Check error details with `e.errors()`. Verify required fields are present and data types match FHIR specifications. Review [FHIR resource definitions](https://www.hl7.org/fhir/resourcelist.html). |
| None values in JSON output | Use `exclude_none=True` parameter in `model_dump_json()` to omit empty fields. This follows FHIR best practices for minimal representation. |
| Cannot modify resource after creation | Ensure you are assigning to the correct attribute. Validation errors prevent invalid modifications. Check [Pydantic model configuration](https://docs.pydantic.dev/latest/concepts/models/#model-config). |
| Field not available in autocomplete | Update your IDE configuration to recognize Pydantic models. Install type stubs or use an IDE with Pydantic support like PyCharm or VS Code with Pylance. |
| JSON parsing fails with valid FHIR | Verify JSON uses correct FHIR structure. Use `model_validate_json()` instead of manual parsing. Check for encoding issues with non-ASCII characters. |
| Resource fails constraints after modification | Pydantic validates on assignment by default. Modifications must maintain FHIR compliance. Review the [specific constraint](https://www.hl7.org/fhir/conformance-rules.html#constraints) that failed. |
| Cannot serialize datetime fields | FHIR uses string representations for dates. Use FHIR date format (YYYY-MM-DD) rather than Python datetime objects. Fhircraft handles conversion automatically. |
| Different behavior across FHIR versions | Each FHIR version has specific rules. Ensure you use the correct version model. Check [FHIR version documentation](https://www.hl7.org/fhir/versions.html) for differences. |

## Further Resources

[Pydantic Documentation](https://docs.pydantic.dev/latest/) - Complete guide to Pydantic models, validation, and serialization

[Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/) - Understanding BaseModel and model construction

[Pydantic Validation](https://docs.pydantic.dev/latest/concepts/validators/) - How Pydantic validates data automatically

[Pydantic Serialization](https://docs.pydantic.dev/latest/concepts/serialization/) - Converting models to JSON, dictionaries, and other formats

[FHIR Resource List](https://www.hl7.org/fhir/resourcelist.html) - Complete list of FHIR resources with specifications

[FHIR Data Types](https://www.hl7.org/fhir/datatypes.html) - Complex and primitive data types used in FHIR

[FHIR Validation](https://www.hl7.org/fhir/validation.html) - How FHIR defines and enforces validation rules

[FHIR Conformance Rules](https://www.hl7.org/fhir/conformance-rules.html) - Constraints and invariants that govern FHIR resources

[FHIR Versions](https://www.hl7.org/fhir/versions.html) - Understanding differences between FHIR releases