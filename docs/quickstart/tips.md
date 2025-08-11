
# Tips and Tricks

Fhircraft streamlines working with FHIR resources in Python, but there are some nuances and best practices to be aware of. This guide highlights practical tips, common pitfalls, and troubleshooting advice to help you get the most out of Fhircraft in your projects.

### Error Handling and Common Issues

When working with Fhircraft, you may encounter several types of errors. Here's how to handle them:

**Validation Errors**
```python
from pydantic import ValidationError

try:
    invalid_patient = patient_model.model_validate({
        "resourceType": "Patient",
        "gender": "invalid_gender"  # Invalid value
    })
except ValidationError as e:
    print("Validation failed:")
    for error in e.errors():
        print(f"- {error['msg']} at {error['loc']}")
```

**FHIRPath Parsing Errors**
```python
from fhircraft.fhir.path import FhirPathParserError

try:
    result = my_patient.get_fhirpath('Patient.invalid..path')
except FhirPathParserError as e:
    print(f"FHIRPath syntax error: {e}")
```

**Network Issues with Canonical URLs**
```python
from fhircraft.fhir.resources.factory import factory, construct_resource_model

# Best practice: Pre-configure repository for local-first operation
factory.configure_repository(
    directory="/path/to/local/definitions",
    internet_enabled=False  # Disable for production
)

try:
    # This will use local definitions first
    model = construct_resource_model(
        canonical_url='http://hl7.org/fhir/StructureDefinition/Patient'
    )
except ValueError as e:
    print(f"Definition not found locally: {e}")
    # Enable internet as fallback if needed
    factory.enable_internet_access()
    model = construct_resource_model(
        canonical_url='http://hl7.org/fhir/StructureDefinition/Patient'
    )
```

------------------

### Performance Tips

**Repository and Model Caching**
Fhircraft automatically caches both structure definitions and constructed models for optimal performance:

```python
from fhircraft.fhir.resources.factory import factory, construct_resource_model

# Repository caches structure definitions
factory.configure_repository(directory="/path/to/definitions")

# First call loads definition into repository cache and constructs model
patient_model_1 = construct_resource_model(canonical_url='...')

# Second call uses cached definition and cached model (very fast)
patient_model_2 = construct_resource_model(canonical_url='...')

# Clear model cache if needed (repository cache remains)
factory.clear_chache()

# Clear everything and reconfigure if needed
factory.configure_repository(directory="/new/path", internet_enabled=False)
```

**Local-First Strategy**
- **Pre-load definitions**: Use `factory.configure_repository()` at startup
- **Disable internet**: Use `factory.disable_internet_access()` for production
- **Version pinning**: Use versioned canonical URLs like `url|4.0.1` for reproducible builds
- **Bulk loading**: Load entire directories rather than individual files

```python
# Optimal production setup
factory.configure_repository(
    directory="/app/fhir/definitions",
    internet_enabled=False  # Prevent unexpected network calls
)

# All subsequent model construction will be fast and offline
patient_model = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient|4.0.1"
)
```

------------------

### API Patterns and Best Practices

**Simple Usage Pattern**
For basic use cases, the simplified API provides everything you need:

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# Simple - uses default repository with internet fallback
Patient = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)
```

**Advanced Configuration Pattern**
For production or complex scenarios, use the factory instance directly:

```python
from fhircraft.fhir.resources.factory import factory

# One-time setup at application startup
factory.configure_repository(
    directory="/app/resources/fhir/definitions",
    files=["/app/custom/profiles.json"],
    internet_enabled=False
)

# Use throughout application
Patient = factory.construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)
CustomProfile = factory.construct_resource_model(
    canonical_url="http://example.org/fhir/StructureDefinition/CustomProfile"
)
```

**Development vs Production**
```python
# Development - flexible with internet fallback
if development_mode:
    factory.configure_repository(internet_enabled=True)

# Production - strict local-only operation
else:
    factory.configure_repository(
        directory="/app/fhir/definitions",
        internet_enabled=False
    )
```

------------------

### Common Pitfalls and Troubleshooting

**Structure Definition Requirements**
```python
# ❌ This will fail - missing snapshot
incomplete_definition = {
    "resourceType": "StructureDefinition",
    "differential": {...}  # Only differential, no snapshot
}

# ✅ This works - includes snapshot
complete_definition = {
    "resourceType": "StructureDefinition", 
    "snapshot": {...},  # Required for Fhircraft
    "differential": {...}  # Optional
}
```

**Choice Element Naming**
```python
# ❌ Wrong - using generic name
observation_data = {
    "value": "some_value"  # This won't work
}

# ✅ Correct - using specific choice element
observation_data = {
    "valueString": "some_value",  # or valueQuantity, valueBoolean, etc.
}
```

**FHIRPath Expression Syntax**
```python
# ❌ Common mistakes
my_patient.get_fhirpath('Patient.name[0].family')  # Arrays use different syntax
my_patient.get_fhirpath('Patient.name.Family')     # Case-sensitive

# ✅ Correct syntax  
my_patient.get_fhirpath('Patient.name.first().family')  # Use first() function
my_patient.get_fhirpath('Patient.name.family')          # Correct case
```

------------------

### Working with FHIR Profiles and Extensions

**Working with FHIR Profiles**
FHIR profiles extend or constrain base resources. Fhircraft can construct models from any valid FHIR profile:

```python
# Example: US Core Patient profile
us_core_patient_model = construct_resource_model(
    canonical_url='http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient'
)

# Validate data against the profile
patient_data = {
    "resourceType": "Patient",
    "identifier": [{
        "system": "http://example.org/patient-ids",
        "value": "12345"
    }],
    "name": [{
        "family": "Doe",
        "given": ["John"]
    }],
    # Additional constraints from US Core profile will be enforced
}

validated_patient = us_core_patient_model.model_validate(patient_data)
```

**Working with Extensions**
Extensions allow additional data elements beyond the base FHIR specification:

```python
# Example: Patient with extension
patient_with_extension = {
    "resourceType": "Patient",
    "id": "example",
    "extension": [{
        "url": "http://example.org/fhir/extensions/patient-importance",
        "valueString": "VIP"
    }],
    "name": [{
        "family": "Smith",
        "given": ["Jane"]
    }]
}

# Access extensions via FHIRPath
importance = my_patient.get_fhirpath(
    "Patient.extension.where(url='http://example.org/fhir/extensions/patient-importance').valueString"
)
```

------------------

### Working with FHIR Data Types

Fhircraft handles FHIR's complex data type system automatically:

**Primitive Types**
```python
# FHIR primitive types are validated according to FHIR rules
patient_data = {
    "resourceType": "Patient",
    "active": True,  # boolean
    "birthDate": "1990-01-01",  # date (YYYY-MM-DD format required)
    "id": "patient123"  # string with specific constraints
}
```

**Choice Elements (value[x])**
```python
# FHIR choice elements allow different data types
observation_data = {
    "resourceType": "Observation",
    "status": "final",
    "code": {"coding": [{"code": "weight"}]},
    # Either valueQuantity, valueString, valueBoolean, etc.
    "valueQuantity": {
        "value": 70.5,
        "unit": "kg"
    }
}
```
