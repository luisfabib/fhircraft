# Tutorial: Building a Patient Management System

This tutorial walks you through building a small patient management system using Fhircraft. You'll learn how to create, validate, query, and transform FHIR resources in a real-world scenario.

!!! info "Prerequisites"
    - Python 3.10 or higher installed
    - Fhircraft installed (`pip install fhircraft`)
    - Basic familiarity with Python and Pydantic

## What We'll Build

We'll create a system that:

1. Creates and validates patient records
2. Manages observations (e.g., vital signs)
3. Queries data with FHIRPath
4. Transforms legacy data to FHIR format
5. Exports data for external systems

## Step 1: Setting Up the Project

Create a new directory for your project:

```bash
mkdir fhir-patient-system
cd fhir-patient-system
```

Create a Python file `patient_system.py`:

```python
"""A simple patient management system using Fhircraft."""
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type
from fhircraft.utils import load_file
from datetime import datetime

# We'll build this step by step
```

## Step 2: Creating Patient Records

Let's create a function to register new patients:

```python
def create_patient(given_name: str, family_name: str, gender: str, birth_date: str):
    """Create a new FHIR Patient resource."""
    Patient = get_fhir_resource_type("Patient", "R5")
    
    patient = Patient(
        name=[{
            "given": [given_name],
            "family": family_name,
            "use": "official"
        }],
        gender=gender,
        birthDate=birth_date,
        active=True
    )
    
    return patient

# Create a sample patient
alice = create_patient("Alice", "Johnson", "female", "1985-03-15")
print(f"Created patient: {alice.name[0].given[0]} {alice.name[0].family}")
```

!!! tip "Validation"
    Fhircraft automatically validates that `gender` is one of the allowed FHIR values (`male`, `female`, `other`, `unknown`) and that `birthDate` follows the FHIR date format.

## Step 3: Adding Observations

Now let's record vital signs for our patient:

```python
def create_observation(patient_id: str, code: str, display: str, 
                       value: float, unit: str):
    """Create a FHIR Observation for vital signs."""
    Observation = get_fhir_resource_type("Observation", "R5")
    
    observation = Observation(
        status="final",
        code={
            "coding": [{
                "system": "http://loinc.org",
                "code": code,
                "display": display
            }]
        },
        subject={
            "reference": f"Patient/{patient_id}"
        },
        valueQuantity={
            "value": value,
            "unit": unit,
            "system": "http://unitsofmeasure.org",
            "code": unit
        },
        effectiveDateTime=datetime.now().isoformat()
    )
    
    return observation

# Record vital signs for Alice
blood_pressure = create_observation(
    patient_id="alice-123",
    code="85354-9",
    display="Blood pressure systolic and diastolic",
    value=120,
    unit="mm[Hg]"
)

print(f"Recorded observation: {blood_pressure.code.coding[0].display}")
```

## Step 4: Querying with FHIRPath

Use FHIRPath to extract information from resources:

```python
# Get patient's full name
full_name = alice.fhirpath_values("name.first().given.first() & ' ' & name.first().family")
print(f"Full name: {full_name[0]}")  # Alice Johnson

# Check if patient is active
is_active = alice.fhirpath_values("active = true")
print(f"Patient active: {is_active[0]}")  # True

# Get observation value
bp_value = blood_pressure.fhirpath_values("valueQuantity.value")
print(f"Blood pressure: {bp_value[0]} mm[Hg]")  # 120
```

!!! info "FHIRPath"
    FHIRPath is the standard query language for FHIR. It works across all FHIR resources and implementations. Learn more in the [FHIRPath Guide](../user-guide/fhirpath.md).

## Step 5: Transforming Legacy Data

Many healthcare systems have legacy data formats. Let's transform them to FHIR:

```python
from fhircraft.fhir.mapper import FHIRMapper

# Legacy patient data from an old system
legacy_patient = {
    "firstName": "Bob",
    "lastName": "Smith",
    "dob": "1990-05-20",
    "sex": "M",
    "ssn": "123-45-6789"
}

# FHIR Mapping Language script
mapping = """
/// url = "http://example.org/legacy-to-fhir"
/// name = "LegacyPatientToFHIR"

uses "http://hl7.org/fhir/StructureDefinition/Patient" as target

group main(source legacy, target patient: Patient) {
    // Map basic demographics
    legacy -> patient.name as name then {
        legacy.firstName -> name.given;
        legacy.lastName -> name.family;
    };
    
    legacy.dob -> patient.birthDate;
    
    // Transform gender codes
    legacy.sex where("$this = M") -> patient.gender = 'male';
    legacy.sex where("$this = F") -> patient.gender = 'female';
    
    // Map SSN to identifier
    legacy.ssn -> patient.identifier as id then {
        legacy.ssn -> id.value;
        legacy.ssn -> id.system = 'http://hl7.org/fhir/sid/us-ssn';
    };
}
"""

# Execute the transformation
mapper = FHIRMapper()
result = mapper.execute_mapping(mapping, legacy_patient)
bob = result[0]
```

!!! success "Automatic Validation"
    The mapper automatically validates the output against the FHIR specification. Invalid transformations will raise clear validation errors.

## Step 6: Creating a Bundle

Group multiple resources together:

```python
def create_patient_bundle(patient, observations):
    """Create a FHIR Bundle with patient and observations."""
    Bundle = get_fhir_resource_type("Bundle", "R5")
    
    entries = [
        {
            "resource": patient.model_dump(mode="json"),
            "fullUrl": f"urn:uuid:{patient.id or 'temp-patient-id'}"
        }
    ]
    
    for obs in observations:
        entries.append({
            "resource": obs.model_dump(mode="json"),
            "fullUrl": f"urn:uuid:{obs.id or 'temp-obs-id'}"
        })
    
    bundle = Bundle(
        type="collection",
        entry=entries
    )
    
    return bundle

# Create a bundle with Alice and her observations
bundle = create_patient_bundle(alice, [blood_pressure])
print(f"Bundle contains {len(bundle.entry)} resources")
```

## Step 7: Exporting Data

Export resources for external systems or storage:

```python
import json

def export_to_json(resource, filename):
    """Export a FHIR resource to JSON file."""
    json_data = resource.model_dump_json(indent=2, exclude_none=True)
    
    with open(filename, 'w') as f:
        f.write(json_data)
    
    print(f"Exported to {filename}")

# Export individual resources
export_to_json(alice, "alice_patient.json")
export_to_json(blood_pressure, "alice_bp.json")
export_to_json(bundle, "alice_bundle.json")
```

## Step 8: Validation and Error Handling

Handle validation errors gracefully:

```python
from pydantic import ValidationError

def safe_create_patient(data: dict):
    """Create a patient with error handling."""
    Patient = get_fhir_resource_type("Patient", "R5")
    
    try:
        patient = Patient.model_validate(data)
        return patient, None
    except ValidationError as e:
        # Return None and error details
        return None, e.errors()

# Try with invalid data
invalid_data = {
    "name": [{"given": ["Test"]}],  # Missing family name
    "gender": "invalid-gender",      # Invalid gender code
    "birthDate": "not-a-date"        # Invalid date format
}

patient, errors = safe_create_patient(invalid_data)
if errors:
    print("Validation failed:")
    for error in errors:
        print(f"  - {error['loc']}: {error['msg']}")
```

## Complete Example

Here's the complete `patient_system.py`:

```python
"""A simple patient management system using Fhircraft."""
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type
from fhircraft.fhir.mapper import FHIRMapper
from pydantic import ValidationError
from datetime import datetime
import json

def create_patient(given_name: str, family_name: str, gender: str, birth_date: str):
    """Create a new FHIR Patient resource."""
    Patient = get_fhir_resource_type("Patient", "R5")
    return Patient(
        name=[{"given": [given_name], "family": family_name, "use": "official"}],
        gender=gender,
        birthDate=birth_date,
        active=True
    )

def create_observation(patient_id: str, code: str, display: str, 
                       value: float, unit: str):
    """Create a FHIR Observation for vital signs."""
    Observation = get_fhir_resource_type("Observation", "R5")
    return Observation(
        status="final",
        code={"coding": [{"system": "http://loinc.org", "code": code, "display": display}]},
        subject={"reference": f"Patient/{patient_id}"},
        valueQuantity={"value": value, "unit": unit, 
                      "system": "http://unitsofmeasure.org", "code": unit},
        effectiveDateTime=datetime.now().isoformat()
    )

def export_to_json(resource, filename):
    """Export a FHIR resource to JSON file."""
    with open(filename, 'w') as f:
        f.write(resource.model_dump_json(indent=2, exclude_none=True))
    print(f"Exported to {filename}")

if __name__ == "__main__":
    # Create patient
    alice = create_patient("Alice", "Johnson", "female", "1985-03-15")
    print(f"✓ Created patient: {alice.name[0].given[0]} {alice.name[0].family}")
    
    # Record observation
    bp = create_observation("alice-123", "85354-9", 
                           "Blood pressure systolic", 120, "mm[Hg]")
    print(f"✓ Recorded: {bp.code.coding[0].display}")
    
    # Query with FHIRPath
    is_active = alice.fhirpath_values("active = true")[0]
    print(f"✓ Patient active: {is_active}")
    
    # Export
    export_to_json(alice, "alice_patient.json")
    print("✓ Patient management system ready!")
```

Run it:

```bash
python patient_system.py
```

## What You've Learned

✅ Creating and validating FHIR resources  
✅ Working with relationships between resources  
✅ Querying data with FHIRPath  
✅ Transforming legacy data to FHIR  
✅ Creating bundles and exporting data  
✅ Handling validation errors  

## Next Steps

- **[User Guide](../user-guide/overview.md)** - Explore all Fhircraft features in depth
- **[FHIRPath Guide](../user-guide/fhirpath.md)** - Master advanced querying techniques
- **[Mapper Guide](../user-guide/mapper.md)** - Learn complex data transformations
- **[API Reference](../reference/fhir-resources-base.md)** - Detailed API documentation

