# Working with FHIR Resource Models

This guide shows you how to create, validate, and manipulate FHIR resources using Fhircraft's pre-built models. Building on the FHIR concepts covered earlier, you will learn practical recipes for common tasks like creating patient records, validating data from external systems, and converting between JSON and Python objects.

## Understanding Resource Models

FHIR defines over 140 different [:material-fire: Resource Types](https://www.hl7.org/fhir/resourcelist.html) like [:material-fire: Patient](https://www.hl7.org/fhir/patient.html), [:material-fire: Observation](https://www.hl7.org/fhir/observation.html), and [:material-fire: Condition](https://www.hl7.org/fhir/condition.html). Each resource type has a specific structure with required fields, optional fields, data types, and validation rules. Manually creating and validating these resources would require extensive code to check every constraint and relationship.

Fhircraft provides pre-built [:simple-pydantic: Pydantic models](https://docs.pydantic.dev/latest/concepts/models/) for all standard FHIR resources across all supported releases that subclass the [`FHIRBaseModel`](../../reference/fhir-resources-base/#fhircraft.fhir.resources.base.FHIRBaseModel) base class. These models automatically validate data when you create resources, ensuring compliance with FHIR specifications without writing validation code yourself or requiring an external validation service.

Using these models means you can focus on your healthcare application logic rather than FHIR implementation details. The models provide type safety, catching errors during development rather than at runtime. They also integrate seamlessly with Python applications, IDEs, and type checkers, giving you autocomplete suggestions and early error detection. All validation follows the same FHIR constraints covered in earlier sections on validation configuration and resource construction.

## Getting Resource Models

Before you can create FHIR resources, you need to obtain the appropriate model class. Fhircraft provides all standard FHIR resource models ready to use without any setup or configuration. The models are organized by FHIR version, allowing you to work with the specific version your application requires.

The [`get_fhir_type`](../../reference/fhir-resources-type-utils/#fhircraft.fhir.resources.datatypes.utils.get_fhir_type) function is your entry point to these models. It takes a resource type name and optionally a FHIR version, returning the corresponding [:simple-pydantic: Pydantic BaseModel](https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage) subclass. Alternatively, if familiar with the Fhircraft modules, the models can be directly imported from their corresponding module.


=== "Resolver Function"

    ```python
    # Import the resource type resolver
    from fhircraft.fhir.resources import get_fhir_type

    # Get built-in models
    Patient = get_fhir_type("Patient", "R4B")
    Condition = get_fhir_type("Condition", "R4B")

    print(Patient)
    #> <class 'fhircraft.fhir.resources.datatypes.R4B.core.patient.Patient'>

    print(Condition)
    #> <class 'fhircraft.fhir.resources.datatypes.R4B.core.condition.Condition'>
    ```


=== "Direct Import"

    ```python
    # Import the resource models directly
    from fhircraft.fhir.resources.datatypes.R4B.core import Patient, Condition

    print(Patient)
    #> <class 'fhircraft.fhir.resources.datatypes.R4B.core.patient.Patient'>

    print(Condition)
    #> <class 'fhircraft.fhir.resources.datatypes.R4B.core.condition.Condition'>
    ```

Accessing the right model for a chosen FHIR version can be similarly achieved with both approaches:


=== "Resolver Function"

    ```python
    # Import the resource type resolver
    from fhircraft.fhir.resources import get_fhir_type

    # Get models for specific FHIR versions
    PatientR4B = get_fhir_type("Patient", "R4B") 
    PatientR5 = get_fhir_type("Patient", "R5") 

    print(PatientR4B._fhir_release)
    #> R4B

    print(PatientR5._fhir_release)
    #> R5
    ```

=== "Direct Import"

    ```python
    # Import the resource models directly
    from fhircraft.fhir.resources.datatypes.R4B.core import Patient as PatientR4B
    from fhircraft.fhir.resources.datatypes.R5.core import Patient as PatientR5

    print(PatientR4B._fhir_release)
    #> R4B

    print(PatientR5._fhir_release)
    #> R5
    ```


The returned model is a standard Python class that you instantiate like any other class. These models use [:simple-pydantic: Pydantic's validation](https://docs.pydantic.dev/latest/concepts/validators/) to ensure data correctness.

## Creating Resources

Creating FHIR resources with Fhircraft follows standard Python patterns. You instantiate the model class with keyword arguments representing the resource fields. The [:simple-pydantic: Pydantic model constructor](https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage) automatically validates all data, checking types, required fields, and FHIR constraints. 

!!! example "Basic Patient Creation"

    One of the most common healthcare resource is [:material-fire: Patient](https://www.hl7.org/fhir/patient.html), which represents a person receiving care. Creating a basic patient requires only minimal information, though you can add as much detail as your application needs:

    ```python
    from fhircraft.fhir.resources import get_fhir_type

    # Get the Patient model for FHIR R5
    Patient = get_fhir_type("Patient", "R5")

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

    print(f"Created patient: {patient.name[0].given[0]} {patient.name[0].family}")
    #> Created patient: John Doe

    print(f"Gender: {patient.gender}, DOB: {patient.birthDate}")
    #> Gender: male, DOB: 1990-05-15
    ```

    Pydantic validates all data during construction, ensuring the `gender` and `birthDate` follow the proper format.


!!! example "Complete Patient Record Recipe"

    Real patient records contain multiple names, contact methods, addresses, and identifiers. FHIR uses [:material-fire: Complex Types](https://www.hl7.org/fhir/datatypes.html) to represent these rich structures. This recipe shows how to create a comprehensive patient record with all common elements:

    ```python
    from fhircraft.fhir.resources import get_fhir_type
    # Import FHIR complex data types
    from fhircraft.fhir.resources.datatypes.R5.complex import (
        HumanName,      # Person names
        ContactPoint,   # Phone, email, etc.
        Address,        # Physical addresses
        Identifier      # System identifiers like MRN
    )

    Patient = get_fhir_type("Patient", "R5")

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

    print(f"Created comprehensive patient with ID: {patient.identifier[0].value}")
    #> Created comprehensive patient with ID: MRN123456
    ```

    Using [:simple-pydantic: Pydantic models for nested types](https://docs.pydantic.dev/latest/concepts/models/#nested-models) ensures each component validates independently, catching errors at the field level.


Healthcare applications frequently need to convert data from external systems, APIs, databases, or files into FHIR resources. When your application receives data from a REST API, database query, or external system, you typically will end up with Python dictionaries or dataclass objects. Pydantic's [:simple-pydantic: `model_validate`](https://docs.pydantic.dev/latest/concepts/models/#model-methods-and-properties) method converts data objects such as dictionaries into validated model instances.

!!! example "Validating an API Response Data"

    ```python
    from fhircraft.fhir.resources import get_fhir_type

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

    Patient = get_fhir_type("Patient", "R5")

    # Validate and convert dictionary to Patient model
    # This performs all FHIR validation automatically
    patient = Patient.model_validate(patient_data)

    # Now you have a fully validated Patient object
    print(f"Validated patient: {patient.name[0].given[0]} {patient.name[0].family}")
    #> Validated patient: Jane Smith 

    print(f"Type: {type(patient)}")
    #> Type: <class 'fhircraft.fhir.resources.datatypes.R5.core.patient.Patient'>
    ```

    The [:simple-pydantic: `model_validate`](https://docs.pydantic.dev/latest/concepts/models/#model-methods-and-properties) method is the recommended way to parse untrusted data, as it validates every field according to FHIR rules.

!!! danger "No Terminology Validation"

    Fhircraft does not support validation of terminologies. This means that validation does not verify whether specific codes or CodeableConcepts are correct within the ValueSets or CodeSystems bound to the resource's elements.

### Parsing FHIR JSON Files

When reading FHIR data from files, HTTP responses, or string variables, you often have JSON text rather than Python dictionaries. Fhircraft's [`FHIRBaseModel`](../../reference/fhir-resources-base/#fhircraft.fhir.resources.base.FHIRBaseModel) subclasses implement and extension of Pydantic's [:simple-pydantic: `model_validate_json`](https://docs.pydantic.dev/latest/concepts/models/#creating-models-without-validation) method that parses and validates FHIR JSON strings in one operation:

```python
# Example: JSON string from a file or HTTP response
fhir_json = '''
{
    "resourceType": "Patient",
    "id": "example-patient",
    "name": [{
        "given": ["Bob", "Carl"],
        "family": "Johnson"
    }],
    "birthDate": "1975-12-01",
    "gender": "male"
}
'''

Patient = get_fhir_type("Patient", "R4")

# Parse JSON string and validate in one step
patient = Patient.model_validate_json(fhir_json)

# Access the parsed data as Python objects
print(f"Parsed patient ID: {patient.id}")
#> Parsed patient ID: example-patient

print(f"Name: {patient.name[0].family}, {' '.join(patient.name[0].given)}")
#> Name: Johnson, Bob Carl
```

Using [:simple-pydantic: `model_validate_json`](https://docs.pydantic.dev/latest/concepts/models/#creating-models-without-validation) is more efficient than manually parsing JSON and then validating, as it combines both operations.

### Parsing FHIR XML Files

Some healthcare systems still use XML format for FHIR data exchange. Fhircraft supports [FHIR XML](https://www.hl7.org/fhir/xml.html) parsing for all subclasses of [`FHIRBaseModel`](../../reference/fhir-resources-base/#fhircraft.fhir.resources.base.FHIRBaseModel) using [`model_validate_xml`](../../reference/fhir-resources-base/#fhircraft.fhir.resources.base.FHIRBaseModel.model_validate_xml) method that parses and validates FHIR XML strings in one operation:

```python
# Example: XML string from legacy system or file
fhir_xml = '''<?xml version="1.0"?>
<Patient xmlns="http://hl7.org/fhir">
  <id value="example-patient"/>
  <name>
    <given value="Bob"/>
    <given value="Carl"/>
    <family value="Johnson"/>
  </name>
  <birthDate value="1975-12-01"/>
  <gender value="male"/>
</Patient>'''

Patient = get_fhir_type("Patient", "R4")

# Parse XML and validate against FHIR specification
patient = Patient.model_validate_xml(fhir_xml)

# Access the parsed data as Python objects
print(f"Parsed patient ID: {patient.id}")
#> Parsed patient ID: example-patient

print(f"Name: {patient.name[0].family}, {' '.join(patient.name[0].given)}")
#> Name: Johnson, Bob Carl
```

## Working with Resource Data

Once you have created or parsed a FHIR resource, you need to read its data, modify it, and export it to other systems. These recipes show common patterns for working with resource data using [:simple-pydantic: Pydantic's model API](https://docs.pydantic.dev/latest/concepts/models/).

### Reading Resource Data

FHIR resource models are standard Python objects with properties you access using dot notation. This recipe shows safe patterns for reading data, including handling optional fields that might not exist:

```python
from fhircraft.fhir.resources import get_fhir_type

Patient = get_fhir_type("Patient", "R4")
patient = Patient(
    name=[{"given": ["Alice"], "family": "Johnson"}],
    gender="female",
    birthDate="1992-08-15"
)

# Access properties using dot notation (standard Python)
print(f"Family name: {patient.name[0].family}")  # Access nested properties
#> Family name: Johnson
print(f"Given name: {patient.name[0].given[0]}")  # Arrays use index
#> Given name: Alice
print(f"Gender: {patient.gender}")
#> Gender: female
print(f"Birth date: {patient.birthDate}")
#> Birth date: 1992-08-15
 
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

!!! tip "Accessing Nested Data with FHIRPath"

    Due to the complex and nested structure of FHIR resources, accessing deeply-nested attributes can be cumbersome and can be simplified by using [FHIRPath queries](./fhirpath.md). 

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
#> Added contact: alice.johnson@example.com

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

print(f"Updated patient gender to {patient.gender} and active to {patient.active}")
#> Updated patient gender to female and active to True
print(f"Contact methods: {patient.telecom[-1].system}")
#> Contact methods: phone

# Validation happens automatically on modification
try:
    patient.gender = "invalid-code"  # This will raise ValidationError
except ValidationError as e:
    print(f"Update rejected: {e.errors()[0]['msg']}")
```

Pydantic's [validators run on assignment](https://docs.pydantic.dev/latest/concepts/validators/#field-validators) by default, catching invalid modifications immediately.

!!! tip "Simplifying Deep Updates with FHIRPath"

    When modifying deeply-nested values in complex resources, standard Python attribute access can become verbose. Fhircraft offers a more concise alternative through [FHIRPath-based updates](./fhirpath.md), allowing you to target and modify specific elements using path expressions.


## Data Export

Healthcare systems exchange data using standardized formats. These recipes show how to convert your resource models into JSON, XML, and Python dictionaries for storage, transmission, and integration.

### Exporting to JSON

FHIR JSON is the most common format for FHIR data exchange. Pydantic provides multiple [:simple-pydantic: serialization methods](https://docs.pydantic.dev/latest/concepts/serialization/) that convert models to JSON while respecting FHIR formatting rules:

```python
from fhircraft.fhir.resources import get_fhir_type

Patient = get_fhir_type("Patient", "R4")
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

The [:simple-pydantic: `model_dump_json`](https://docs.pydantic.dev/latest/concepts/serialization/#modelmodel_dump_json) method ensures proper JSON formatting according to FHIR specifications.

### Exporting to XML Recipe

Some healthcare systems require [FHIR XML format](https://www.hl7.org/fhir/xml.html). Fhircraft provides XML serialization with proper FHIR namespace handling through the [`model_dump_xml`](../../reference/fhir-resources-base/#fhircraft.fhir.resources.base.FHIRBaseModel.model_dump_xml) method.

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

## Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| ValidationError when creating resource | Check error details with `e.errors()`. Verify required fields are present and data types match FHIR specifications. Review [:material-fire: FHIR resource definitions](https://www.hl7.org/fhir/resourcelist.html). |
| None values in JSON output | Use `exclude_none=True` parameter in `model_dump_json()` to omit empty fields. This follows FHIR best practices for minimal representation. |
| Cannot modify resource after creation | Ensure you are assigning to the correct attribute. Validation errors prevent invalid modifications. Check [:simple-pydantic: Pydantic model configuration](https://docs.pydantic.dev/latest/concepts/models/#model-config). |
| Field not available in autocomplete | Update your IDE configuration to recognize Pydantic models. Install type stubs or use an IDE with Pydantic support like PyCharm or VS Code with Pylance. |
| JSON parsing fails with valid FHIR | Verify JSON uses correct FHIR structure. Use `model_validate_json()` instead of manual parsing. Check for encoding issues with non-ASCII characters. |
| Resource fails constraints after modification | Pydantic validates on assignment by default. Modifications must maintain FHIR compliance. Review the [:material-fire: Specific Constraint](https://www.hl7.org/fhir/conformance-rules.html#constraints) that failed. |
| Cannot serialize datetime fields | FHIR uses string representations for dates. Use FHIR date format (YYYY-MM-DD) rather than Python datetime objects. Fhircraft handles conversion automatically. |
| Different behavior across FHIR versions | Each FHIR version has specific rules. Ensure you use the correct version model. Check [:material-fire: FHIR version documentation](https://www.hl7.org/fhir/versions.html) for differences. |

## Further Resources

* [:simple-pydantic: Pydantic Documentation](https://docs.pydantic.dev/latest/) - Complete guide to Pydantic models, validation, and serialization

* [:simple-pydantic: Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/) - Understanding BaseModel and model construction

* [:simple-pydantic: Pydantic Validation](https://docs.pydantic.dev/latest/concepts/validators/) - How Pydantic validates data automatically

* [:simple-pydantic: Pydantic Serialization](https://docs.pydantic.dev/latest/concepts/serialization/) - Converting models to JSON, dictionaries, and other formats

* [:material-fire: FHIR Resource List](https://www.hl7.org/fhir/resourcelist.html) - Complete list of FHIR resources with specifications

* [:material-fire: FHIR Data Types](https://www.hl7.org/fhir/datatypes.html) - Complex and primitive data types used in FHIR

* [:material-fire: FHIR Validation](https://www.hl7.org/fhir/validation.html) - How FHIR defines and enforces validation rules

* [:material-fire: FHIR Conformance Rules](https://www.hl7.org/fhir/conformance-rules.html) - Constraints and invariants that govern FHIR resources

* [:material-fire: FHIR Versions](https://www.hl7.org/fhir/versions.html) - Understanding differences between FHIR releases