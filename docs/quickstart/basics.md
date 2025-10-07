# Getting Started with Fhircraft

This tutorial is for developers new to Fhircraft who want to start building FHIR-compliant applications in Python. You'll learn to create models, validate data, and work with FHIR resources using Python's type system.

By the end of this tutorial, you'll be able to generate Pydantic models from FHIR specifications and create validated FHIR resources in your Python applications.

## Accessing Core Resources

Fhircraft provides Pydantic models for all core FHIR resources out of the box. These models are generated from the official FHIR specifications and are ready to use for validation, serialization, and manipulation in your Python projects.

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Get the built-in R5 FHIR Patient core resource model
Patient = get_fhir_resource_type("Patient", "R5")

# Now create a patient instance with validation
patient = Patient(
    name=[{
        "given": ["Alice"],
        "family": "Johnson"
    }],
    gender="female",
    birthDate="1985-03-15"
)

print(f"Created patient: {patient.name[0].given[0]} {patient.name[0].family}")
```

## Creating FHIR Models

Let's start by creating a `Patient` profile model from the minimal Common Oncology Data Elements (mCODE) Implementation Guide:

```python
from fhircraft.fhir.resources.factory import factory

# Load the mCODE FHIR package
factory.load_package('hl7.fhir.us.mcode')

# Create a Patient model from the FHIR R5 specification
CancerPatient = factory.construct_resource_model(
    canonical_url='http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-patient'
)

# Now create a patient instance with validation
patient = CancerPatient(
    name=[{
        "given": ["Alice"],
        "family": "Johnson"
    }],
    gender="female",
    birthDate="1985-03-15"
)

print(f"Created cancer patient: {patient.name[0].given[0]} {patient.name[0].family}")
```

That's it! Fhircraft automatically downloads the FHIR specifications, generates a type-safe Pydantic model, adds the profiled constraints, and validates your data according to FHIR rules.

--------------

### Generating Source Code for Pydantic FHIR Models

Fhircraft enables you to generate reusable Python source code for any dynamically constructed Pydantic FHIR model. This is accomplished using the `generate_resource_model_code` function, which returns the model's class definition as a string. This feature is ideal for integrating FHIR models into other projects, sharing models with collaborators, or version-controlling your model definitions.

**Example: Exporting the Source Code for a FHIR `Patient` Model**

```python
from fhircraft.fhir.resources.generator import generate_resource_model_code

# Assume CancerPatient was created using construct_resource_model
source_code = generate_resource_model_code(CancerPatient)

# Optionally, save the code to a file for reuse
with open("cancerpatient.py", "w") as f:
    f.write(source_code)
```

The generated code is ready to use in any Python project, provided that Fhircraft and its dependencies are installed. This approach streamlines collaboration and deployment by allowing you to distribute static model definitions without requiring dynamic model construction at runtime.

-----------

### Validating FHIR Payloads

Once you've constructed a Pydantic FHIR model, you can use it to validate real-world FHIR payloads. This ensures your data strictly adheres to the structure and constraints defined by the FHIR specification or your chosen profile.

**Example: Validating a FHIR `Patient` Resource**

```python
from fhircraft.utils import load_file

# Load your FHIR resource data (as a dict) from a JSON file
data = load_file('my_fhir_patient.json')

# Validate and parse the data using the generated model
my_patient = patient_model.model_validate(data)
```

If the input data does not match the expected FHIR structure or contains invalid values, Pydantic will raise a `ValidationError` detailing the issues. If no error is raised, your payload is valid and ready for further processing.

This validation step helps catch errors early, enforce FHIR compliance, and maintain data quality throughout your workflow.

---------------
### Manipulating Models with FHIRPath

Fhircraft provides a robust FHIRPath engine with an enhanced interface, allowing you to query and modify FHIR resources using standard FHIRPath expressions directly in Python. This enables expressive, standards-compliant access to deeply nested data and supports both retrieval and update operations.

**Example: Accessing Values with FHIRPath**

The enhanced interface provides multiple methods for retrieving values based on your specific needs:

```python
from fhircraft.fhir.path import fhirpath

# Parse the FHIRPath expression
name_path = fhirpath.parse('Patient.name.family')

# Get all matching values as a list (always returns a list)
all_family_names = name_path.values(my_patient)
# Returns: ['Doe', 'Smith'] if patient has multiple names

# Get a single value (raises error if multiple values found)
family_name = name_path.single(my_patient)
# Returns: 'Doe' or raises FHIRPathRuntimeError if multiple names exist

# Get the first value (safe for multiple values)
first_family_name = name_path.first(my_patient)
# Returns: 'Doe' (first family name) or None if no names

# Get the last value
last_family_name = name_path.last(my_patient)
# Returns: 'Smith' (last family name) or None if no names

# Check if values exist
has_family_name = name_path.exists(my_patient)
# Returns: True if patient has any family names

# Count matching values
name_count = name_path.count(my_patient)
# Returns: 2 if patient has 2 family names

# Check if path is empty
is_empty = name_path.is_empty(my_patient)
# Returns: True if patient has no family names
```

**Example: Updating Values with FHIRPath**

```python
# Update all matching values
name_path.update_values(my_patient, 'NewFamilyName')
# Sets all family names to 'NewFamilyName'

# Update a single value (safer for single-value fields)
gender_path = fhirpath.parse('Patient.gender')
gender_path.update_single(my_patient, 'female')
# Sets gender to 'female', raises error if multiple gender values exist
```

**Example: Using Default Values**

```python
# Get values with fallback defaults
birth_date = fhirpath.parse('Patient.birthDate').first(my_patient, default='1900-01-01')
# Returns actual birth date or '1900-01-01' if not set

phone = fhirpath.parse('Patient.telecom.where(system="phone").value').single(
    my_patient, 
    default='No phone number'
)
# Returns phone number or default message if not found
```

With these methods, you can efficiently navigate and manipulate FHIR resources, making complex data operations straightforward and Pythonic.

------------------

### Transforming Data with FHIR Mapper

Fhircraft provides a powerful mapping engine that transforms data between different structures using the official FHIR Mapping Language (FML). This is perfect for converting legacy system data to FHIR or transforming between different FHIR profiles.

**Example: Converting Legacy Data to FHIR Patient**

```python
from fhircraft.fhir.mapper import FHIRMapper

# Legacy system patient data
legacy_patient = {
    "firstName": "Alice",
    "lastName": "Johnson",
    "dob": "1985-03-15",
    "sex": "F"
}

# Mapping script using FHIR Mapping Language
mapping_script = """
/// url = "http://example.org/legacy/map"
/// name = "Legacy Patient to FHIR Patient"

uses "http://example.org/legacy/LegacyPatient" as source
uses "http://hl7.org/fhir/StructureDefinition/Patient" as target

group main(source legacy: LegacyPatient, target patient: Patient) {
    legacy.firstName -> patient.name.given;
    legacy.lastName -> patient.name.family;
    legacy.dob -> patient.birthDate;
    legacy.sex where('$this = "F"') -> patient.gender = 'female';
    legacy.sex where('$this = "M"') -> patient.gender = 'male';
}
"""

# Execute the transformation
mapper = FHIRMapper()
targets, metadata = mapper.execute_mapping(mapping_script, legacy_patient)
patient = targets[0]

print(f"Transformed patient: {patient.name[0].given[0]} {patient.name[0].family}")
print(f"Birth date: {patient.birthDate}")
print(f"Gender: {patient.gender}")
```

The FHIR Mapper handles complex transformations, validation, and error handling automatically, making it easy to integrate diverse data sources into your FHIR-compliant applications.

--------------------

## Getting Help

**📚 Documentation**

- [:material-link-variant: User Guide](../user-guide/overview.md) - Complete documentation of all Fhircraft features

- [:material-book-open-variant: Pydantic Documentation](https://docs.pydantic.dev/latest/) - Learn more about Pydantic's powerful features

- [:material-fire-circle: FHIRPath Documentation](https://hl7.org/fhirpath/N1/) - Official FHIRPath specification

**💬 Community & Support**

- [:material-github: GitHub Issues](https://github.com/luisfabib/fhircraft/issues) - Report bugs or request features

- [:material-github: GitHub Discussions](https://github.com/luisfabib/fhircraft/discussions) - Ask questions and share ideas

**🚀 Next Steps**

Ready to dive deeper? Explore these advanced topics:

1. [Pydantic representation of FHIR](../user-guide/pydantic-representation.md) - Detailed description of how Fhircraft represents FHIR within Pydantic

2. [Working with Fhircraft Models](../user-guide/fhir-models.md) - Advanced model construction and validation

3. [FHIRPath Guide](../user-guide/fhirpath.md) - Master the FHIRPath expression language

