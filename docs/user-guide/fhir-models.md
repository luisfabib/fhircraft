
# Working with Fhircraft Models

This guide provides comprehensive information on how to work with Fhircraft's Pydantic-based FHIR models, from construction to advanced usage patterns. Whether you're building new FHIR resources from structure definitions or working with existing models, this guide covers the essential techniques and best practices.

## Overview

Working with Fhircraft models involves several key activities:

- **Model Construction**: Creating Pydantic models from FHIR structure definitions
- **Model Instantiation**: Creating and populating FHIR resource instances
- **Validation**: Leveraging automatic FHIR constraint validation
- **Serialization**: Converting between Python objects and FHIR JSON
- **Querying**: Using FHIRPath expressions for data extraction and validation
- **Error Handling**: Managing validation errors and edge cases
- **Performance Optimization**: Best practices for efficient model usage

## Constructing FHIR Pydantic models 

To generate a Pydantic model representation for a FHIR resource, use the `construct_resource_model` function. This function automatically creates a model based on the structure definition of the specified resource or profile.

!!! important "Snapshot required"

    Fhircraft requires the resource's structure definition to be in `snapshot` form. Models cannot be constructed from definitions that only include a `differential`. If the `snapshot` attribute is missing, Fhircraft will raise an error.

!!! important "FHIR versions"

    Fhircraft automatically handles differences between official FHIR releases. It uses the appropriate complex types based on the FHIR version specified in the resource's structure definition, ensuring that the constructed model conforms to the correct release.

#### Via local files (recommended)

For optimal control and security, it is recommended to manage FHIR structure definitions as local files. These files should be loaded into Python and parsed into dictionary objects.

!!! note "Loading utilities"

    Fhircraft provides utility functions to load JSON or YAML files (XML currently not supported) into Python dictionaries. 
    
    ``` python 
        from fhircraft.utils import load_file
        structure_definition = load_file('fhir/patient_r4b_structuredefinition.json') 
    ``` 

The `construct_resource_model` function takes this dictionary containing the FHIR structure definition and constructs the corresponding model.

```python
from fhircraft.fhir.resources.factory import construct_resource_model
resource_model = construct_resource_model(structure_definition=structure_definition)

# Example: Create an instance of the constructed model
resource_instance = resource_model(
    # Add your resource data here
)
```

Complete example with a custom Patient profile:

```python
from fhircraft.utils import load_file
from fhircraft.fhir.resources.factory import construct_resource_model

# Load a custom Patient profile
structure_definition = load_file('profiles/CustomPatient.json')

# Construct the model
CustomPatient = construct_resource_model(structure_definition=structure_definition)

# Create an instance with profile-specific validation
patient = CustomPatient(
    name=[{
        "given": ["John"],
        "family": "Doe"
    }],
    birthDate="1990-05-15",
    gender="male",
    # Any custom fields defined in the profile will be available here
)
```

#### Via canonical URL 

A canonical URL is a globally unique identifier for FHIR conformance resources. Fhircraft includes a limited canonical URL resolver that can locate and download a FHIR resource's structure definition via HTTP.

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# Construct from official FHIR Patient resource
patient_model = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Construct from a custom profile
custom_profile_model = construct_resource_model(
    canonical_url="http://example.org/fhir/StructureDefinition/MyPatientProfile"
)

# Construct from HL7 FHIR implementation guides
us_core_patient = construct_resource_model(
    canonical_url="http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)
```

!!! warning "Network dependency"

    When using canonical URLs, ensure you have internet connectivity as Fhircraft will download the structure definition from the specified URL. For production environments, consider downloading and storing structure definitions locally.

!!! note "Release version" 

    Most canonical URLs will resolve to the latest normative release of the FHIR resource.

#### Cached models

Fhircraft automatically caches constructed models based on their canonical URLs to improve performance. Subsequent calls to `construct_resource_model` with the same canonical URL will return the cached model without re-processing the structure definition.

```python
from fhircraft.fhir.resources.factory import construct_resource_model, clear_cache

# First call - downloads and constructs the model
patient_model_1 = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Second call - returns cached model (faster)
patient_model_2 = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

assert patient_model_1 is patient_model_2  # Same cached instance

# Clear the cache when needed (e.g., during testing or when structure definitions change)
clear_cache()

# This will now reconstruct the model
patient_model_3 = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)
```

!!! tip "Cache management"
    
    The cache is useful in production but may need to be cleared during development or testing. Clear the cache when:
    
    - Structure definitions have been updated
    - You want to ensure fresh model construction
    - Running unit tests that depend on model construction
    - Memory usage becomes a concern

#### Working with different FHIR releases

Fhircraft automatically detects the FHIR version from structure definitions and uses the appropriate data types. You can work with multiple FHIR releases simultaneously:

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# R4 Patient model
r4_patient_model = construct_resource_model(
    canonical_url="http://hl7.org/fhir/R4/StructureDefinition/Patient"
)

# R4B Patient model  
r4b_patient_model = construct_resource_model(
    canonical_url="http://hl7.org/fhir/R4B/StructureDefinition/Patient"
)

# R5 Patient model
r5_patient_model = construct_resource_model(
    canonical_url="http://hl7.org/fhir/R5/StructureDefinition/Patient"
)

# Each model uses version-specific data types and constraints
r4_patient = r4_patient_model(name=[{"family": "Smith"}])
r5_patient = r5_patient_model(name=[{"family": "Smith"}])
```

You can also import pre-built models for specific FHIR releases:

```python
# Direct imports for specific releases
from fhircraft.fhir.resources.datatypes.R4.complex_types import Patient as PatientR4
from fhircraft.fhir.resources.datatypes.R4B.complex_types import Patient as PatientR4B  
from fhircraft.fhir.resources.datatypes.R5.complex_types import Patient as PatientR5

# Use the appropriate model for your data
patient_r4 = PatientR4(name=[{"family": "Smith"}])
patient_r5 = PatientR5(name=[{"family": "Smith"}])
```

## Model Instantiation and Usage

### Creating Model Instances

Fhircraft models can be instantiated like any Pydantic model, with automatic FHIR-specific validation applied:

```python
from fhircraft.fhir.resources.datatypes.R5.complex_types import Patient, HumanName, ContactPoint

# Create a patient with comprehensive data
patient = Patient(
    # Required resourceType is automatically set
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
    birthDate="1990-05-15",
    gender="male",
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
    active=True
)
```

### Alternative Construction Methods

Fhircraft provides several ways to create model instances:

#### From dictionaries

```python
# From a complete dictionary
patient_data = {
    "name": [{"given": ["Jane"], "family": "Smith"}],
    "birthDate": "1985-03-22",
    "gender": "female"
}

patient = Patient.model_validate(patient_data)
```

#### From JSON strings

```python
# From FHIR JSON
fhir_json = '''
{
    "resourceType": "Patient",
    "name": [{"given": ["Bob"], "family": "Johnson"}],
    "birthDate": "1975-12-01",
    "gender": "male"
}
'''

patient = Patient.model_validate_json(fhir_json)
```

#### Using model_construct for partial data

```python
# For performance when validation isn't needed
patient = Patient.model_construct(
    name=[{"given": ["Alice"], "family": "Brown"}],
    birthDate="1992-08-30"
    # Note: gender is required but can be omitted with model_construct
)
```

### Validation and Error Handling

Fhircraft automatically validates all FHIR constraints using FHIRPath expressions, ensuring data integrity and compliance:

#### Constraint Validation

```python
from pydantic import ValidationError
from fhircraft.fhir.resources.datatypes.R5.complex_types import Patient, Quantity

try:
    # This will fail - Patient requires at least a name or identifier
    invalid_patient = Patient(
        gender="male"
        # Missing required name or identifier
    )
except ValidationError as e:
    print("Validation failed:")
    for error in e.errors():
        print(f"  {error['loc']}: {error['msg']}")
```

#### Invariant Constraint Examples

```python
# Example with Quantity - unit code requires system
try:
    invalid_quantity = Quantity(
        value=10.5,
        unit="mg",
        code="mg"  # Code without system violates qty-3 invariant
    )
except ValidationError as e:
    print("Quantity validation failed:")
    print(e.errors()[0]['msg'])
    # Output: "If a code for the unit is present, the system SHALL also be present. [qty-3]"

# Valid quantity with both code and system
valid_quantity = Quantity(
    value=10.5,
    unit="milligrams", 
    code="mg",
    system="http://unitsofmeasure.org"
)
```

#### Comprehensive Error Information

```python
def validate_patient_safely(patient_data: dict) -> tuple[Patient | None, list[str]]:
    """Safely validate patient data and return detailed error information."""
    try:
        patient = Patient.model_validate(patient_data)
        return patient, []
    except ValidationError as e:
        errors = []
        for error in e.errors():
            field_path = ".".join(str(loc) for loc in error['loc'])
            errors.append(f"{field_path}: {error['msg']}")
        return None, errors

# Usage example
patient_data = {
    "name": [],  # Empty name list
    "birthDate": "invalid-date",  # Invalid date format
    "gender": "unknown"  # Invalid gender code
}

patient, validation_errors = validate_patient_safely(patient_data)
if validation_errors:
    print("Validation errors found:")
    for error in validation_errors:
        print(f"  - {error}")
```

### JSON Serialization and Deserialization

Fhircraft models provide seamless conversion between Python objects and FHIR JSON format:

#### Basic Serialization

```python
# Serialize to FHIR JSON (recommended - excludes None values)
patient_json = patient.model_dump_json(exclude_none=True)

# Serialize to Python dictionary
patient_dict = patient.model_dump(exclude_none=True)

# Include None values if needed (not typical for FHIR)
complete_dict = patient.model_dump(exclude_none=False)
```

#### Advanced Serialization Options

```python
# Serialize with aliases (FHIR uses underscored field names for extensions)
patient_json = patient.model_dump_json(by_alias=True, exclude_none=True)

# Serialize only specific fields
name_only = patient.model_dump(include={'name', 'gender'})

# Exclude specific fields
without_meta = patient.model_dump(exclude={'meta', 'text'})

# Custom serialization for specific use cases
formatted_json = patient.model_dump_json(
    exclude_none=True,
    by_alias=True,
    indent=2  # Pretty formatting for debugging
)
```

#### Deserialization from Various Sources

```python
# From FHIR JSON string
fhir_json = '{"resourceType": "Patient", "name": [{"family": "Smith"}], "gender": "female"}'
patient = Patient.model_validate_json(fhir_json)

# From dictionary (e.g., from API response)
api_response = {
    "resourceType": "Patient",
    "id": "example-patient",
    "name": [{"given": ["John"], "family": "Doe"}],
    "birthDate": "1990-01-01",
    "gender": "male"
}
patient = Patient.model_validate(api_response)

# Bulk processing multiple resources
patients_data = [
    {"name": [{"family": "Smith"}], "gender": "female"},
    {"name": [{"family": "Jones"}], "gender": "male"},
]

patients = [Patient.model_validate(data) for data in patients_data]
```

#### Round-trip Validation

```python
def test_round_trip_serialization(original_patient: Patient):
    """Test that serialization and deserialization preserve data."""
    # Serialize to JSON
    json_data = original_patient.model_dump_json(exclude_none=True)
    
    # Deserialize back to object
    reconstructed_patient = Patient.model_validate_json(json_data)
    
    # Compare (should be identical)
    assert original_patient.model_dump() == reconstructed_patient.model_dump()
    return reconstructed_patient
```


## Best Practices

### Type Safety

Leverage Python's type system with Fhircraft models:

```python
from typing import List
from fhircraft.fhir.resources.datatypes.R5.complex_types import Patient, Observation

def process_patient_data(patient: Patient) -> List[Observation]:
    """Type-safe function that processes patient data."""
    # Your IDE will provide proper autocompletion and type checking
    observations = []
    
    if patient.birthDate:
        # Create observations based on patient data
        pass
    
    return observations
```

### Error Handling

Handle validation errors gracefully:

```python
def create_safe_patient(data: dict) -> Patient | None:
    """Safely create a patient with error handling."""
    try:
        return Patient.model_validate(data)
    except ValidationError as e:
        logger.error(f"Invalid patient data: {e}")
        return None
```

### Performance Considerations

Optimize your Fhircraft model usage with these performance best practices:

#### Serialization Optimization

```python
# Always exclude None values for FHIR compliance and performance
patient_json = patient.model_dump_json(exclude_none=True)

# Use model_construct for performance when validation isn't needed
fast_patient = Patient.model_construct(
    name=[{"family": "Smith"}],
    gender="male"
)

# Batch validation for multiple resources
def validate_patients_batch(patient_data_list: list[dict]) -> list[Patient]:
    """Validate multiple patients efficiently."""
    validated_patients = []
    errors = []
    
    for i, data in enumerate(patient_data_list):
        try:
            patient = Patient.model_validate(data)
            validated_patients.append(patient)
        except ValidationError as e:
            errors.append(f"Patient {i}: {e}")
    
    if errors:
        print(f"Validation errors found in {len(errors)} patients")
    
    return validated_patients
```

#### Memory Management

When working with large numbers of FHIR profiles or dynamically generating many models, memory usage can increase due to model caching and Python's object retention. To avoid excessive memory consumption:

- Periodically clear the Fhircraft model cache using `clear_cache()` if you are processing thousands of unique structure definitions.
- Release references to unused models and instances so Python's garbage collector can reclaim memory.
- For long-running processes, monitor memory usage and adjust cache-clearing frequency as needed.
- Consider batching your processing and restarting the process for very large workloads to ensure a clean memory state.

```python
# Clear cache when working with many different profiles
from fhircraft.fhir.resources.factory import clear_cache

def process_large_dataset(structure_definitions: list[dict]):
    """Process large datasets efficiently."""
    for i, structure_def in enumerate(structure_definitions):
        # Clear cache periodically to manage memory
        if i % 100 == 0:
            clear_cache()
        
        model = construct_resource_model(structure_definition=structure_def)
        # Process model...
```

#### Validation Optimization

FHIR resources typically have many constraint. Their Pydantic field validators can contribute to processing overhead. For scenarios where you need to validate large volumes of resources quickly, consider the following strategies:

- **Bypass Validation**: Consider using `model_construct` when validation isn't critical, bypassing all validation functions.
- **Disable Unnecessary Validators**: If certain invariants or custom validators are not required for your use case, configure your models to skip them where possible.

These techniques help maintain high throughput and responsiveness in production systems that process large FHIR datasets.

```python
from fhircraft.fhir.resources.factory import clear_cache

model = construct_resource_model(structure_definition=structure_def)
def process_large_dataset_without_validation(structure_definitions: list[dict]):
    """Process large datasets efficiently."""
    for data in dataset:
        instance = model.model_contruct(**data) # No validation will be run
```

## Summary

Fhircraft provides a powerful and intuitive way to work with FHIR resources through Pydantic models. This guide has covered:

### Common Patterns

1. **Basic Usage**: Use `construct_resource_model()` with canonical URLs for standard profiles
2. **Data Validation**: Leverage Pydantic's validation for robust FHIR compliance
3. **FHIRPath Queries**: Use `fhirpath()` for complex data extraction and filtering
4. **Extensions**: Add both simple and complex extensions with proper validation
5. **Profiling**: Create custom profiles with additional constraints and slicing

### Best Practices Summary

- Always use `exclude_none=True` when serializing to JSON
- Cache constructed models for frequently used profiles
- Validate data early in your processing pipeline
- Use FHIRPath for complex queries rather than manual navigation
- Handle validation errors gracefully with appropriate error messages
- Test your models thoroughly, especially for custom profiles
- Consider performance implications in high-throughput scenarios

### Next Steps

To continue your journey with Fhircraft:

- Read about [Pydantic Representation](./pydantic-representation.md) for deeper understanding of the underlying concepts
- Explore the [FHIRPath documentation](./fhirpath.md) for advanced querying capabilities
- Check the API reference for detailed information about available models and methods
- Join the community to share your experiences and get help with specific use cases

Fhircraft's combination of Pydantic's validation capabilities with FHIR's rich data model provides a robust foundation for building healthcare applications that handle FHIR data with confidence.
