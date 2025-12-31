# Getting Started with Fhircraft

If you're new to Fhircraft, this guide will walk you through the basics of working with FHIR resources in Python.

## Working with Core FHIR Resources

Fhircraft includes Pydantic models for all core FHIR resources. These models are generated directly from the official FHIR specifications, so you get full validation, serialization, and type checking without any setup:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Get the built-in R5 FHIR Patient core resource model
Patient = get_fhir_resource_type("Patient", "R5")

# Create a patient instance with automatic validation
patient = Patient(
    name=[{
        "given": ["Alice"],
        "family": "Johnson"
    }],
    gender="female",
    birthDate="1985-03-15"
)
```

Fhircraft validates both the types and any structural constraints from the FHIR specification. Since these are standard Pydantic models, you get all the usual serialization and deserialization methods. See the [Pydantic documentation](https://docs.pydantic.dev/latest/concepts/models/#model-methods-and-properties) if you need a refresher on those.

You can access the FHIR elements just like any Python object:

```python
assert patient.name[0].given[0] == "Alice" 
assert patient.name[0].family == "Johnson"
```

## Working with FHIR Profiles

Beyond core resources, you'll often need to work with FHIR profiles—specialized versions of resources with additional constraints. Here's how to create a model from the mCODE (minimal Common Oncology Data Elements) Implementation Guide:

```python
from fhircraft.fhir.resources.factory import factory

# Load the mCODE FHIR package along with its dependencies
factory.load_package('hl7.fhir.us.mcode')

# Build a model from the CancerPatient profile
CancerPatient = factory.construct_resource_model(
    canonical_url='http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-patient'
)
```

Behind the scenes, Fhircraft downloads the FHIR package, parses the structure definitions, and generates a Pydantic model with all the profile-specific constraints and validators baked in.

Once you have the model, it works just like any other FHIR resource:

```python
# Create a cancer patient instance
cancer_patient = CancerPatient(
    name=[{
        "given": ["Alice"],
        "family": "Johnson"
    }],
    gender="female",
    birthDate="1985-03-15"
)

assert cancer_patient.name[0].given[0] == "Alice" 
assert cancer_patient.name[0].family == "Johnson"
```


## Generating Source Code for Models

If you need to distribute your models or avoid runtime generation, you can export any model as Python source code:

```python
from fhircraft.fhir.resources.generator import generate_resource_model_code

# Export the CancerPatient model we created earlier
source_code = generate_resource_model_code(CancerPatient)

# Save it to a file
with open("cancerpatient.py", "w") as f:
    f.write(source_code)
```

The generated code is standalone Python that you can commit to version control or share with other teams. They'll need Fhircraft installed, but they won't need to load structure definitions or generate models at runtime.

## Validating FHIR Data

Use your models to validate FHIR JSON payloads from external systems:

```python
from fhircraft.utils import load_file

# Load FHIR JSON data
data = load_file('my_fhir_patient.json')

# Validate it against your model
my_patient = Patient.model_validate(data)
```

If the data doesn't match the FHIR structure, Pydantic raises a `ValidationError` with details about what's wrong. Otherwise, you get a validated Python object ready to use.

## Querying with FHIRPath

Fhircraft includes a FHIRPath engine for querying FHIR resources. The interface gives you several ways to retrieve values depending on what you need. The quickly query the FHIR resource with a FHIRPath use

```python
# Get the patient's last family name
all_family_names = my_patient.fhirpath_values('Patient.name.family.last()')  

assert all_family_names == ['Doe', 'Smith']
```

You can also update values through FHIRPath:

```python
# Update the patient's last family name
my_patient.fhirpath_update('Patient.name.family.last()', 'NewFamilyName')
```

## Transforming Data with FHIR Mapper

The FHIR Mapper uses the official FHIR Mapping Language to transform data between different structures. This is useful when you need to convert legacy data to FHIR or transform between different profiles:

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

# Some legacy patient data
legacy_patient = {
    "firstName": "Alice",
    "lastName": "Johnson",
    "dob": "1985-03-15",
    "sex": "F"
}

# Write a mapping using FHIR Mapping Language
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

# Run the transformation
mapper = FHIRMapper()
targets, metadata = mapper.execute_mapping(mapping_script, legacy_patient)
patient = targets[0]

print(f"Transformed: {patient.name[0].given[0]} {patient.name[0].family}")
```

The mapper handles the complexity of the transformation and validates the output automatically.

## Where to Go Next

For more details on these features, check out:

- [User Guide](../user-guide/overview.md) - Full documentation on all Fhircraft features
- [Pydantic representation of FHIR](../user-guide/pydantic-representation.md) - How Fhircraft maps FHIR to Pydantic models
- [FHIRPath Guide](../user-guide/fhirpath.md) - Complete FHIRPath reference

If you run into issues or have questions, open an issue on [GitHub](https://github.com/luisfabib/fhircraft/issues) or start a discussion in [GitHub Discussions](https://github.com/luisfabib/fhircraft/discussions).