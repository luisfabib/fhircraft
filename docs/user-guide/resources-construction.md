---
icon: lucide/factory
---

# Constructing Dynamic FHIR Models

This guide shows you how to build custom Pydantic FHIR models from FHIR [:lucide-flame: Structure Definitions](https://hl7.org/fhir/structuredefinition.html). This is different from using pre-built resource models. You need the factory system when you work with implementation guides like [:lucide-flame: US Core](https://www.hl7.org/fhir/us/core/), [:lucide-flame: International Patient Summary](https://hl7.org/fhir/uv/ips/), or your own custom profiles. The factory constructs models that enforce profile-specific requirements beyond base FHIR validation.

The factory system takes a [:lucide-flame: Structure Definitions](https://hl7.org/fhir/structuredefinition.html) and generates a [:simple-pydantic: Pydantic model](https://docs.pydantic.dev/latest/concepts/models/) class. The generated model includes all constraints, extensions, and validation rules from the profile. This means you get type safety and automatic validation for your custom FHIR profiles. 

!!! note

    For information about loading structure definitions and packages, see [managing FHIR artifacts](managing-fhir-artifacts.md). This guide focuses on constructing models from those definitions.

## Building Models

### Construction Mode

The factory supports two construction approaches:

- **Snapshot mode**: Builds models from complete, flattened snapshot elements. The snapshot contains the complete view of all elements with all inherited properties resolved.
- **Differential mode**: Builds models from differential elements that only specify changes from the base definition. The factory automatically resolves and merges these with the base profile.

The factory automatically detects which mode to use based on what elements are present in the structure definition. When both snapshot and differential elements exist, the factory prefers differential mode. You can also explicitly specify the construction mode.

See the [:lucide-flame: FHIR structure definition documentation](https://hl7.org/fhir/structuredefinition.html) for details about snapshot and differential elements.

### Snapshot Mode Construction

Snapshot mode works with structure definitions that contain complete element definitions. This mode is useful for base resource definitions and profiles that include full snapshots.

```python
from fhircraft import FHIRModelFactory, get_fhir_type, FHIRBaseModel

# Create a new factory set to the R4 FHIR release
factory = FHIRModelFactory(fhir_release="R4")

# Structure definition with snapshot elements
snapshot_structure_def = {
    "resourceType": "StructureDefinition",
    "name": "LegacyPatient",
    "type": "Resource",
    "url": "http://example.org/fhir/StructureDefinition/LegacyPatient",
    "fhirVersion": "4.0.1",
    "kind": "logical",
    "status": "draft",
    "abstract": True,
    "snapshot": {
        "element": [
            {
                "id": "LegacyPatient",
                "path": "LegacyPatient",
                "min": 0,
                "max": "*",
                "definition": "A legacy patient",
                "base": {"path": "Resource", "min": 0, "max": "*"},
            },
            {
                "id": "LegacyPatient.fullName",
                "path": "LegacyPatient.fullName",
                "min": 1,
                "max": "1",
                "type": [{"code": "string"}],
                "definition": "A legacy patient's full name",
                "base": {"path": "Element", "min": 0, "max": "1"},
            }
        ]
    }
}

# Construct the resource
LegacyPatient = factory.build(
    structure_definition=snapshot_structure_def,
    mode="snapshot"
)

assert issubclass(LegacyPatient, FHIRBaseModel)

Patient = get_fhir_type("Patient", "R4")
assert not issubclass(LegacyPatient, Patient) # (2)!

instance = LegacyPatient(fullName="Maria Johnson")

print(f"Legacy patient name: {instance.fullName}")
#> Legacy patient name: Maria Johnson
```

1. This option could be left out and the factory would automatically switch to snapshot mode.
2. Check that `LegacyPatient` actually inherits from the `FHIRBaseModel` model but is unrelated to the `Patient` resource.


!!! tip "Snapshot Use Cases"

    Use *snapshot mode* when:

    - Working with base FHIR resource definitions
    - The structure definition only contains snapshot elements
    - You need complete element definitions without relying on base resolution
    - Debugging model construction issues by examining the full flattened structure

### Differential Mode Construction

Differential mode works with structure definitions that only specify changes from a base definition. The factory automatically resolves the base definition and merges the differential constraints with it. This is the standard approach for FHIR profiles and implementation guides.

```python
from fhircraft import FHIRModelFactory, get_fhir_type
from pydantic import ValidationError 

# Structure definition with only differential elements
differential_structure_def = {
    "resourceType": "StructureDefinition",
    "name": "MyPatient",
    "type": "Patient",
    "url": "http://example.org/fhir/StructureDefinition/MyPatient",
    "fhirVersion": "4.0.1",
    "kind": "resource",
    "status": "draft",
    "abstract": False,
    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
    "differential": {
        "element": [
            {
                "id": "Patient.identifier",
                "path": "Patient.identifier",
                "max": "2"
            }
        ]
    }
}

# Explicitly use differential mode
MyPatient = FHIRModelFactory(fhir_release="R4").build(
    structure_definition=differential_structure_def,
    mode="differential" # (1)!
)

assert issubclass(MyPatient, FHIRBaseModel)
assert issubclass(MyPatient, Patient) # (2)!

# Valid patient
patient = MyPatient(
    identifier=[{"system": "http://example.org", "value": "12345"}], 
) 


print(f"My patient ID: {patient.identifier[0].value}")
#> My patient ID: 12345

try:
    # Invalid patient
    patient = MyPatient(
        identifier=[
            {"system": "http://example.org", "value": "12345"},
            {"system": "http://example.org", "value": "67890"},
            {"system": "http://example.org", "value": "54321"},
        ], 
    ) # (3)!
except ValidationError:
    print("Invalid MyPatient was caught successfuly")

```

1. This option could be left out and the factory would automatically switch to differential mode.
2. Check that `MyPatient` actually inherits from the `Patient` resource model
3. While it is a valid `Patient` instance, it violates one of the `MyPatient` additional constraints, resulting in a validation error.

!!! tip "Differential Use Cases"

    Use *differential mode* when:

    - Working with implementation guide profiles
    - The structure definition only contains differential elements
    - You want to leverage profile inheritance and constraint layering
    - Building models that extend or constrain base profiles

### Choosing Between Modes

The factory automatically selects the appropriate mode using these rules:

1. If you specify a mode explicitly, the factory uses that mode and validates the structure definition contains the required elements
2. In AUTO mode (the default), the factory prefers differential if both snapshot and differential exist
3. If only one element type exists, the factory uses that mode
4. If neither exists, the factory raises an error

Most published implementation guide profiles include both snapshot and differential elements. The factory defaults to differential mode in these cases because it correctly handles profile inheritance and constraint layering.

```python
from fhircraft import FHIRModelFactory

# AUTO mode (default) - factory decides based on available elements
model_auto = FHIRModelFactory(fhir_release="R4").build(
    canonical_url="http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

# Explicit SNAPSHOT mode - use the complete flattened view
model_snapshot = FHIRModelFactory(fhir_release="R4").build(
    canonical_url="http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient",
    mode="snapshot"
)

# Explicit DIFFERENTIAL mode - use constraints from profile only
model_differential = FHIRModelFactory(fhir_release="R4").build(
    canonical_url="http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient",
    mode="differential"
)
```

### Constructing from Structure Definitions

You can build models from structure definitions already loaded into memory. The structure definition is a JSON or XML document that describes the profile, loaded into memory in the form of a `StructureDefinition` or dictionary object. The [`build`](../reference/fhir-resources-factory#fhircraft.fhir.resources.factory.core.FHIRModelFactory.build) method of the factory takes that definition and returns the constructed model.

```python
from fhircraft import FHIRModelFactory
from fhircraft.utils import load_file

# Load the structure definition from a local JSON file
structure_def = load_file('patient.profile.json')

# Construct a Pydantic model class from the definition
# The factory automatically detects whether to use snapshot or differential mode
ProfiledPatient = FHIRModelFactory(fhir_release="R4").build(structure_definition=structure_def)

# Create an instance using the generated model
# Validation happens automatically using profile rules
patient = ProfiledPatient(
    name=[{"given": ["John"], "family": "Doe"}],
    birthDate="1990-05-15",
    gender="male"
)

print(f"Created model for: {structure_def['name']}")
```


#### Constructing from Canonical URLs

If the structure definitions have been loaded into the repository, you construct models referencing their structure definition's canonical URLs. This is the most common approach for working with implementation guides. The factory looks up the definition by its canonical URL and constructs the model.

!!! important 

    See [managing FHIR artifacts](managing-fhir-artifacts.md) for information about loading structure definitions into the repository. This section assumes you have already configured the repository.

```python
from fhircraft import FHIRModelFactory
from fhircraft.utils import load_file
import json 

factory = FHIRModelFactory(fhir_release="R4")

# Load the custom patient profile definition from a file into the factory
struct_def = load_file("custom-patient.profile.json") 
factory.register(struct_def)

# Construct a model using the canonical URL
# The factory retrieves the definition from the repository
CustomPatient = factory.build(
    canonical_url="http://example.org/StructureDefinition/CustomPatient"
)

# Use the model like any other Pydantic model
patient = CustomPatient(
    name=[{"given": ["Alice"], "family": "Johnson"}],
    gender="female"
)
```


!!! example "Implementation Guide Recipe"

    This recipe shows the complete workflow for working with an implementation guide. You load the package, construct models for the profiles, and use those models with profile-specific validation.

    ```python
    from fhircraft import FHIRModelFactory

    factory = FHIRModelFactory(fhir_release="R4")

    # Load the US Core implementation guide
    # See managing-fhir-artifacts.md for package loading details
    factory.register_package("hl7.fhir.us.core", "5.0.1")

    # Construct a model for the US Core Patient profile
    # The canonical URL comes from the implementation guide
    USCorePatient = factory.build(
        "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
    )

    # Create a patient using the profile model
    # US Core Patient requires an identifier
    patient = USCorePatient(
        name=[{"given": ["John"], "family": "Doe"}],
        gender="male",
        identifier=[{  # Required by US Core
            "system": "http://example.org/mrn",
            "value": "12345"
        }]
    )

    print(f"Created US Core patient: {patient.name[0].given[0]} {patient.name[0].family}")
    ```

!!! example "Multiple Profiles Recipe"

    When working with multiple implementation guides, you load all required packages and then construct models for each profile. Each model enforces its own profile constraints.

    ```python
    from fhircraft import FHIRModelFactory

    factory = FHIRModelFactory(fhir_release="R4")

    # Load both US Core and International Patient Summary
    factory.register_package("hl7.fhir.us.core", "5.0.1")
    factory.register_package("hl7.fhir.us.mcode", "1.1.0")

    # Construct models for different profiles
    USCorePatient = factory.build(
        "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
    )

    CancerPatient = factory.build(
        "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-patient"
    )

    # Each model validates using its profile rules
    us_patient = USCorePatient(
        name=[{"family": "Doe", "given": ["John"]}],
        gender="male"
    )

    cancer_patient = CancerPatient(
        name=[{"family": "Smith", "given": ["Alice"]}],
        gender="female"
    )

    print(f"Created US Core patient with name: {us_patient.name[0].given[0]} {us_patient.name[0].family}")
    #> Created US Core patient with name: John Doe

    print(f"Created mCODE cancer patient with name: {cancer_patient.name[0].given[0]} {cancer_patient.name[0].family}")
    #> Created mCODE cancer patient with name: Alice Smith
    ```

See the [:lucide-flame: FHIR versioning specification](https://hl7.org/fhir/versions.html) for information about version identifiers and the [managing FHIR artifacts](managing-fhir-artifacts.md) guide for details about how the repository resolves canonical URLs.


## Model Caching

The factory caches constructed models by their canonical URL. When you request the same canonical URL again, the factory returns the cached model instead of reconstructing it. This improves performance significantly, especially when constructing models that might depend on previously constructed models which would otherwise be re-constructed or lead to circular loops.

You clear the cache when structure definitions change or during testing when you need fresh model construction. The cache stores references to model classes, not instances, so memory usage remains reasonable even with many cached models.

```python
from fhircraft import FHIRModelFactory
from time import time 

factory = FHIRModelFactory(fhir_release="R4")

# First call constructs the model and caches it
start_time = time()
patient_model_1 = factory.build(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)
original_construction_time = (end_time := time()) - start_time


# Second call returns the cached model
start_time = time()
patient_model_2 = factory.build(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)
cached_construction_time = (end_time := time()) - start_time
 
assert patient_model_1 is patient_model_2 # (1)!
print(f"Cached: {cached_construction_time}s")
print(f"Original: {original_construction_time}s") # (2)!

# Clear the cache when definitions change
factory.reset_cache()


```

1. Both variables reference the same model class
2. The cached result is obtained much faster than the original

See the [:simple-pydantic: Pydantic performance documentation](https://docs.pydantic.dev/latest/concepts/performance/) for information about model validation performance.


### Inspecting the cache

`is_built` and `list_built` let you query what is currently cached without triggering any builds:

```python
from fhircraft import FHIRModelFactory
factory = FHIRModelFactory(fhir_release="R4")

url = "http://hl7.org/fhir/StructureDefinition/Patient"

Patient = factory.build(canonical_url=url)
print(factory.is_built(url))      # True
print(factory.list_built())       # [url, ...]
```

### Evicting a single model

`evict` removes one URL from the cache. The next call to `build` for that URL will construct a fresh model. Use this when you have updated the underlying StructureDefinition and want the change reflected without discarding other cached models:

```python
from fhircraft import FHIRModelFactory
factory = FHIRModelFactory(fhir_release="R4")

url = "http://hl7.org/fhir/StructureDefinition/Patient"
factory.evict(url)
print(factory.is_built(url))  # False
```

### Forcing a rebuild

`rebuild` combines `evict` with an immediate `build` call, returning the freshly constructed model:

```python
from fhircraft import FHIRModelFactory
factory = FHIRModelFactory(fhir_release="R4")

url = "http://hl7.org/fhir/StructureDefinition/Patient"

# Force a fresh build of an already-cached model
Patient = factory.rebuild(url)
```

### Resetting the entire cache

`reset_cache` discards all cached models at once. Use it when you have reloaded a batch of definitions and want all subsequent builds to start fresh:

```python
from fhircraft import FHIRModelFactory
factory = FHIRModelFactory(fhir_release="R4")

factory.reset_cache()
print(factory.list_built())  # []
```

## Code Generation

The code generator converts constructed Pydantic models into Python source code. This is useful when you want to save generated models to files instead of constructing them at runtime. The generated code includes all field definitions, validators, and properties from the original model.

You can use code generation to avoid runtime overhead of model construction. Instead of loading structure definitions and constructing models each time your application starts, you generate the code once and import the models directly. This is especially valuable in production environments where startup time matters or to generate a re-usable a codebase for Python-based FHIR service or application.

The generated code is readable Python that you can inspect, modify, and share with others. All imports are included automatically, so the generated file is self-contained.

```python
from fhircraft import FHIRModelFactory
from fhircraft.fhir.resources.generator import generate_resource_model_code

factory = FHIRModelFactory(fhir_release="R4")

# Load a package and construct a model
factory.register_package("hl7.fhir.us.core", "5.0.1")
USCorePatient = factory.build(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

# Generate Python source code for the model
# The code includes all fields, validators, and imports
source_code = generate_resource_model_code(USCorePatient)

# Save to a file for later import
with open("us_core_patient.py", "w") as f:
    f.write(source_code)

print("Generated model saved to us_core_patient.py")
```

See the [Pydantic JSON schema documentation](https://docs.pydantic.dev/latest/concepts/json_schema/) for information about model introspection.

!!! example "Multiple Models Generation"

    When working with multiple profiles from an implementation guide, you generate all models together in a single file. This keeps related models organized and ensures they can reference each other correctly.

    ```python
    from fhircraft import FHIRModelFactory
    from fhircraft.fhir.resources.generator import generate_resource_model_code

    factory = FHIRModelFactory(fhir_release="R4")
    
    # Load the implementation guide
    factory.register_package("hl7.fhir.us.core", "5.0.1")

    # Construct multiple related models
    models_to_generate = []

    us_core_profiles = [
        "us-core-patient",
        "us-core-condition",
        "us-core-procedure",
    ]

    # Construct each model and add to the list
    for profile_name in us_core_profiles:
        model = factory.build(
            f"http://hl7.org/fhir/us/core/StructureDefinition/{profile_name}"
        )
        models_to_generate.append(model)

    # Generate source code for all models together
    # This ensures proper cross-references between models
    source_code = generate_resource_model_code(models_to_generate)

    # Save to a single module file
    with open("us_core_models.py", "w") as f:
        f.write(source_code)

    print(f"Generated {len(models_to_generate)} models in us_core_models.py")
    ```

### Generated Code Structure

The generated code follows a consistent structure. It starts with imports, then defines models in dependency order so that base classes appear before derived classes. Each model includes field definitions with type annotations, default values, and metadata.

Here is what the generated code looks like:

```python
# Generated automatically - includes timestamp and version

from typing import List, Optional
from pydantic import BaseModel, Field
from fhircraft.fhir.resources.datatypes.R4.complex import Identifier, HumanName

class Patient(BaseModel):
    """US Core Patient Profile"""
    
    identifier: List[Identifier] = Field(
        ...,
        description="An identifier for this patient"
    )
    
    name: List[HumanName] = Field(
        ...,
        description="A name associated with the patient"
    )
    
    gender: Optional[str] = Field(
        None,
        description="male | female | other | unknown"
    )
```

The generator handles inheritance, forward references, and circular dependencies automatically.

## Common Problems

| Problem | Cause | Solution |
|---------|-------|----------|
| ValueError: Structure definition not found | The canonical URL is not in the repository | Load the package or file containing the definition. See [managing FHIR artifacts](managing-fhir-artifacts.md) |
| ValueError: SNAPSHOT mode requested but no snapshot element | Explicitly requested snapshot mode for a differential-only structure definition | Use `'differential'` or `'auto'` instead |
| ValueError: DIFFERENTIAL mode requested but no differential element | Explicitly requested differential mode for a snapshot-only structure definition | Use `'snapshot'` or `'auto'` instead |
| ValueError: Must have either snapshot or differential | Structure definition contains neither snapshot nor differential elements | Ensure the structure definition is valid and contains element definitions |
| Model construction is slow | Constructing models without caching | The factory caches models automatically. Reuse the same factory instance across your application |
| Profile constraints not enforced | Using base resource model instead of profile model | Construct a model from the profile canonical URL, not the base resource |
| Base definition not found in differential mode | The baseDefinition URL cannot be resolved | Ensure the base profile is loaded into the repository before constructing the differential profile |
| Cannot find profile from implementation guide | Package not loaded or incorrect canonical URL | Verify the package is loaded and check the canonical URL in the implementation guide documentation |
| Models conflict between FHIR versions | Multiple FHIR versions loaded | Use version-specific canonical URLs or load only one FHIR version per repository |
| Memory usage increases over time | Many models cached | Clear the cache periodically with `factory.reset_cache()` if needed |
| Thread safety issues | Concurrent modifications to repository | Load all definitions during application startup before concurrent access |
