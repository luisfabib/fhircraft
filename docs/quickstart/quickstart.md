# Quick Start

This guide shows you how to create and work with [:material-fire: FHIR](https://hl7.org/fhir/) healthcare data using [:simple-pydantic: Pydantic](https://docs.pydantic.dev/) models in Python. FHIR (Fast Healthcare Interoperability Resources) defines how healthcare systems exchange information. Pydantic uses Python type hints to validate data when you create objects.

## Accessing Built-in FHIR Resources

FHIR resources represent different types of healthcare data - patients, observations, medications, and more. When you need to work with healthcare data in Python, you'll often receive it as JSON or need to create it from scratch. Fhircraft's models handle the validation automatically, so you don't need to worry about whether your data follows the FHIR specification.

Fhircraft includes Pydantic models for all core FHIR resources. Here's how to create a [Patient resource from FHIR R5](https://hl7.org/fhir/patient.html):

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Get the Patient model for FHIR R5
Patient = get_fhir_resource_type("Patient", "R5")

# Create a patient with automatic validation
patient = Patient(
    name=[{"given": ["Alice"], "family": "Johnson"}],
    gender="female",
    birthDate="1985-03-15"
) # (1)!

print(patient.gender)
#> "female"

print(patient.name[0].family)
#> "Johnson"
```

1. This creates a Patient object that validates the input data against the FHIR specification and allows you to access patient information through object attributes.

**Further reading:**

- [:material-fire: FHIR Patient Resource](https://hl7.org/fhir/patient.html)
- [:simple-pydantic: Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/)

## Working with FHIR resources

In real applications, you'll often receive FHIR data from APIs, databases, or files rather than creating it from scratch. This data needs validation to ensure it meets the FHIR specification before you can safely work with it. You'll also need to convert your Python objects back to JSON when sending data to other systems.

You can load FHIR data from JSON files, validate it against the FHIR specification, and convert it back to JSON:

```python
from fhircraft.utils import load_file

# Load FHIR JSON
data = load_file('patient.json')

# Validate against FHIR specification
patient = Patient.model_validate(data)

# Export back to JSON
json_str = patient.model_dump_json(indent=2) # (1)!
```

1. This loads a JSON file containing FHIR data, creates a validated Patient object from it, then exports that object back to formatted JSON.

**Further reading:**

- [:simple-pydantic: Pydantic Serialization](https://docs.pydantic.dev/latest/concepts/serialization/)
- [:material-fire: FHIR JSON Format](https://hl7.org/fhir/json.html)
    
## Querying with FHIRPath

FHIR resources can contain complex nested data structures. Instead of writing loops and conditionals to extract information, FHIRPath provides a standardized query language. This becomes particularly useful when you need to extract specific data points, perform calculations, or filter resources based on criteria.

Use [FHIRPath expressions](https://hl7.org/fhirpath/) to extract data from FHIR resources:

```python
# Get all family names
family_names = patient.fhirpath_values('Patient.name.family')
assert family_names == ["Johnson"] # (1)!

# Check if patient is female
is_female = patient.fhirpath_values("Patient.gender = 'female'")
assert is_female == [True] # (2)!
```
1. This uses a FHIRPath expression to extract all family names from the patient's name elements and returns them as a list.

2. This evaluates a boolean expression that checks whether the patient's gender equals "female" and returns the result as a list.

**Further reading:**

- [:material-fire: FHIRPath Specification](https://hl7.org/fhirpath/)

## Working with Profiles

Base FHIR resources are designed to work across all healthcare contexts, but real-world implementations often need additional constraints. FHIR profiles define these constraints - requiring certain fields, restricting values, or adding extensions. When integrating with specific healthcare systems or implementing clinical guidelines, you'll need models that validate against these profiles rather than just the base FHIR specification.

Load [:material-fire: FHIR implementation guides](https://hl7.org/fhir/implementationguide.html) and create specialized resource models:

```python
from fhircraft.fhir.resources.factory import factory

# Load an implementation guide (e.g., US Core)
factory.load_package('hl7.fhir.us.core') # (1)!

# Build a model from a profile
USCorePatient = factory.construct_resource_model(
    canonical_url='http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient'
)

# Use it like any other model
us_patient = USCorePatient(
    name=[{"given": ["Bob"], "family": "Smith"}],
    gender="male",
    birthDate="1990-01-01"
) # (2)!
```

1. This loads the US Core implementation guide package, making its profile definitions available to the factory.

2. This creates a specialized Patient model based on the US Core profile, then uses it to create a patient object that validates against the US Core constraints.

**Further reading:**

- [:material-fire: FHIR Profiles](https://hl7.org/fhir/profiling.html)
- [:material-fire: US Core Implementation Guide](http://hl7.org/fhir/us/core/)


## Transforming Data with FHIR Mapper

Healthcare organizations often have legacy systems with data in non-FHIR formats. When migrating to FHIR or integrating with FHIR-based systems, you need to transform this data systematically. The FHIR Mapping Language provides a standardized way to define these transformations, making them reproducible and maintainable.

The FHIR Mapper uses the [:material-fire: FHIR Mapping Language](https://hl7.org/fhir/mapping-language.html) to transform data between different structures:

```python
from fhircraft.fhir.mapper import FHIRMapper

# Some legacy patient data
legacy_patient = {
    "firstName": "Alice",
    "lastName": "Johnson",
    "dob": "1985-03-15",
    "sex": "F"
} # (1)!

# Write a mapping using FHIR Mapping Language
mapping_script = """
/// url = "http://example.org/legacy/map"
/// name = "Legacy Patient to FHIR Patient"

uses "http://hl7.org/fhir/StructureDefinition/Patient" as target

group main(source legacy, target patient: Patient) {
    legacy -> patient.name as name then {
        legacy.firstName -> name.given;
        legacy.lastName -> name.family;
    };
    legacy.dob -> patient.birthDate;
    legacy.sex where($this = 'F') -> patient.gender = "female";
    legacy.sex where($this = 'M') -> patient.gender = "male";
}
""" # (2)!

# Run the transformation
mapper = FHIRMapper()
targets = mapper.execute_mapping(mapping_script, legacy_patient)  # (3)!
patient = targets[0]
```

1. This defines a dictionary with legacy patient data that doesn't match the FHIR Patient structure.

2. This defines transformation rules that map fields from the legacy data structure to the corresponding FHIR Patient fields, including conditional logic for gender mapping.

3. This executes the mapping script on the legacy data and returns a list containing the transformed FHIR Patient object.

**Further reading:**

- [:material-fire: FHIR Mapping Language](https://hl7.org/fhir/mapping-language.html)
- [:material-fire: StructureMap Resource](https://hl7.org/fhir/structuremap.html)


## Further Reading

For more detailed information on specific topics:

- **[Complete Tutorial](tutorial.md)** - Build a healthcare application step-by-step
- **[User Guide](../user-guide/overview.md)** - Comprehensive documentation of all features
- **[FHIRPath Guide](../user-guide/fhirpath.md)** - Query FHIR data with expressions
- **[Mapper Guide](../user-guide/mapper.md)** - Transform data between formats

For external documentation:

- **[:simple-pydantic: Pydantic Documentation](https://docs.pydantic.dev/latest/)** - Learn about Pydantic's features
- **[:material-fire: FHIR Specification](https://hl7.org/fhir/)** - Official FHIR documentation

For community support:

- **[FAQ](../community/faq.md)** - Common questions and answers
- **[GitHub Discussions](https://github.com/luisfabib/fhircraft/discussions)** - Ask questions and share ideas
- **[GitHub Issues](https://github.com/luisfabib/fhircraft/issues)** - Report bugs or request features
