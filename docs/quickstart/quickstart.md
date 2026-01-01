# Quick Start

Get up and running with Fhircraft in 5 minutes. This guide shows you the essential features to start working with FHIR resources in Python.

## Your First FHIR Resource

Fhircraft includes Pydantic models for all core FHIR resources. Create and validate a patient resource:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Get the Patient model for FHIR R5
Patient = get_fhir_resource_type("Patient", "R5")

# Create a patient with automatic validation
patient = Patient(
    name=[{"given": ["Alice"], "family": "Johnson"}],
    gender="female",
    birthDate="1985-03-15"
)

# Access data like any Python object
print(f"{patient.name[0].given[0]} {patient.name[0].family}")  # Alice Johnson
```

!!! tip "Pydantic Models"
    These are standard Pydantic models with all the validation and serialization features you expect. See [Pydantic's documentation](https://docs.pydantic.dev/latest/) for more details.

## Working with FHIR JSON

Load and validate FHIR JSON data from external systems:

```python
from fhircraft.utils import load_file

# Load FHIR JSON
data = load_file('patient.json')

# Validate against FHIR specification
patient = Patient.model_validate(data)

# Export back to JSON
json_str = patient.model_dump_json(indent=2)
```

## Querying with FHIRPath

Use FHIRPath expressions to query FHIR resources:

```python
# Get all family names
family_names = patient.fhirpath_values('Patient.name.family')
print(family_names)  # ['Johnson']

# Check if patient is female
is_female = patient.fhirpath_values("Patient.gender = 'female'")
print(is_female)  # [True]
```

## Working with Profiles

Load implementation guides and create specialized resource models:

```python
from fhircraft.fhir.resources.factory import factory

# Load an implementation guide (e.g., US Core)
factory.load_package('hl7.fhir.us.core')

# Build a model from a profile
USCorePatient = factory.construct_resource_model(
    canonical_url='http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient'
)

# Use it like any other model
us_patient = USCorePatient(
    name=[{"given": ["Bob"], "family": "Smith"}],
    gender="male",
    birthDate="1990-01-01"
)
```

## Next Steps

Now that you've seen the basics, dive deeper:

- **[Complete Tutorial](tutorial.md)** - Build a small healthcare application step-by-step
- **[User Guide](../user-guide/overview.md)** - Comprehensive documentation of all features
- **[FHIRPath Guide](../user-guide/fhirpath.md)** - Master querying FHIR data
- **[Mapper Guide](../user-guide/mapper.md)** - Transform data between formats

!!! question "Need Help?"
    - Check the [FAQ](../community/faq.md) for common questions
    - Browse [GitHub Discussions](https://github.com/luisfabib/fhircraft/discussions)
    - Report issues on [GitHub](https://github.com/luisfabib/fhircraft/issues)
