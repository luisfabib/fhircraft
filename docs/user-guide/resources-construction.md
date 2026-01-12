# Resource Factory

This page shows you how to build custom Pydantic models from FHIR structure definitions. This is different from using pre-built resource models. You construct custom models when working with profiles, extensions, or implementation guides that modify standard FHIR resources.

The factory system takes a [structure definition](https://hl7.org/fhir/structuredefinition.html) and generates a Pydantic model class. The generated model includes all constraints, extensions, and validation rules from the profile. This means you get type safety and automatic validation for your custom FHIR profiles.

Most applications use pre-built models from the [resources and models](resources-models.md) page. You need the factory system when you work with implementation guides like [US Core](https://www.hl7.org/fhir/us/core/), [International Patient Summary](https://hl7.org/fhir/uv/ips/), or your organization's custom profiles. The factory constructs models that enforce profile-specific requirements beyond base FHIR validation.

For information about loading structure definitions and packages, see [managing FHIR artifacts](managing-fhir-artifacts.md). This page focuses on constructing models from those definitions.

## Building Models from Structure Definitions

You build models from structure definitions already loaded into memory. The structure definition is a JSON or XML document that describes the profile. The `construct_resource_model` function takes that definition and returns a Pydantic model class.

The structure definition must include a snapshot element. This contains the complete flattened view of all elements in the profile. Structure definitions with only differential elements will not work. Most published profiles include the snapshot. See the [FHIR structure definition documentation](https://hl7.org/fhir/structuredefinition.html) for details about snapshot and differential.

```python
from fhircraft.fhir.resources.factory import construct_resource_model
from fhircraft.utils import load_file

# Load the structure definition from a local JSON file
structure_def = load_file('patient_profile.json')

# Construct a Pydantic model class from the definition
# The model includes all constraints from the profile
PatientModel = construct_resource_model(structure_definition=structure_def)

# Create an instance using the generated model
# Validation happens automatically using profile rules
patient = PatientModel(
    name=[{"given": ["John"], "family": "Doe"}],
    birthDate="1990-05-15",
    gender="male"
)

print(f"Created model for: {structure_def['name']}")
```

## Building Models from Canonical URLs

After loading structure definitions into the repository, you construct models using canonical URLs. This is the most common approach for working with implementation guides. The factory looks up the definition by its canonical URL and constructs the model.

See [managing FHIR artifacts](managing-fhir-artifacts.md) for information about loading structure definitions into the repository. This section assumes you have already configured the repository.

```python
from fhircraft.fhir.resources.factory import factory

# Load structure definitions into the repository first
# See managing-fhir-artifacts.md for loading options
factory.configure_repository(
    directory="./fhir-profiles",
    internet_enabled=True
)

# Construct a model using the canonical URL
# The factory retrieves the definition from the repository
CustomPatient = factory.construct_resource_model(
    canonical_url="http://example.org/StructureDefinition/CustomPatient"
)

# Use the model like any other Pydantic model
patient = CustomPatient(
    name=[{"given": ["Alice"], "family": "Johnson"}],
    gender="female"
)
```

## Versioned Model Construction

You specify versions in canonical URLs using the pipe separator. The factory retrieves the specific version from the repository. Without a version, the factory uses the latest version available.

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# Construct using a specific version
# The version appears after the pipe character
patient_model = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient|4.0.1"
)

# Construct without specifying a version
# The factory uses the latest version in the repository
latest_patient = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Construct from implementation guide profiles
# Include the full canonical URL from the implementation guide
us_core_patient = construct_resource_model(
    canonical_url="http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)
```

See the [FHIR versioning specification](https://hl7.org/fhir/versions.html) for information about version identifiers and the [managing FHIR artifacts](managing-fhir-artifacts.md) page for details about how the repository resolves canonical URLs.

## Implementation Guide Recipe

This recipe shows the complete workflow for working with an implementation guide. You load the package, construct models for the profiles, and use those models with profile-specific validation.

```python
from fhircraft.fhir.resources.factory import ResourceFactory

# Create a factory with package support enabled
factory = ResourceFactory(enable_packages=True)

# Load the US Core implementation guide
# See managing-fhir-artifacts.md for package loading details
factory.load_package("hl7.fhir.us.core", "5.0.1")

# Construct a model for the US Core Patient profile
# The canonical URL comes from the implementation guide
USCorePatient = factory.construct_resource_model(
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

See [common FHIR packages](managing-fhir-artifacts.md#common-fhir-packages) for a list of popular implementation guides and the [FHIR package registry](https://registry.fhir.org/) for searching available packages.

## Multiple Profiles Recipe

When working with multiple implementation guides, you load all required packages and then construct models for each profile. Each model enforces its own profile constraints.

```python
from fhircraft.fhir.resources.factory import ResourceFactory

# Create factory and load multiple implementation guides
factory = ResourceFactory(enable_packages=True)

# Load both US Core and International Patient Summary
factory.load_package("hl7.fhir.us.core", "5.0.1")
factory.load_package("hl7.fhir.us.mcode", "1.1.0")

# Construct models for different profiles
USCorePatient = factory.construct_resource_model(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

CancerPatient = factory.construct_resource_model(
    "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-patient"
)

# Each model validates using its profile rules
us_patient = USCorePatient(
    identifier=[{"system": "http://example.com", "value": "123"}],
    name=[{"family": "Doe", "given": ["John"]}],
    gender="male"
)

cancer_patient = CancerPatient(
    name=[{"family": "Smith", "given": ["Alice"]}]
)

print(f"Created US Core patient with ID: {us_patient.identifier[0].value}")
print(f"Created IPS patient: {cancer_patient.name[0].given[0]} {cancer_patient.name[0].family}")
```

## Model Caching

The factory caches constructed models by their canonical URL. When you request the same canonical URL again, the factory returns the cached model instead of reconstructing it. This improves performance significantly.

You clear the cache when structure definitions change or during testing when you need fresh model construction. The cache stores references to model classes, not instances, so memory usage remains reasonable even with many cached models.

```python
from fhircraft.fhir.resources.factory import construct_resource_model, factory

# First call constructs the model and caches it
patient_model_1 = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Second call returns the cached model
# This is much faster than reconstruction
patient_model_2 = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Both variables reference the same model class
assert patient_model_1 is patient_model_2
print("Models are identical (cached)")

# Clear the cache when definitions change
factory.clear_cache()

# This reconstructs the model
patient_model_3 = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

print("Model reconstructed after cache clear")
```

See the [Pydantic performance documentation](https://docs.pydantic.dev/latest/concepts/performance/) for information about model validation performance.

## Working Across FHIR Versions

The factory detects the FHIR version from the structure definition and uses the correct data types. You do not need to specify the version manually. Different FHIR versions have different data types and constraints, and the factory handles these differences automatically.

For pre-built models without profiles, use direct imports as shown in [resources and models](resources-models.md#working-across-fhir-versions). The factory is for constructing models from custom profiles.

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# Construct models for different FHIR versions
# The factory uses version-specific data types automatically
r4_patient = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient|4.0.1"
)
# Create instances using version-appropriate data structures
patient_r4 = r4_patient(name=[{"family": "Smith"}])

print(f"R4 Patient type: {type(patient_r4)}")
```

See the [FHIR version history](https://hl7.org/fhir/history.html) for information about differences between versions.

## Checking Repository Contents

You can inspect the repository to see what definitions are available. This helps when debugging model construction issues or verifying that packages loaded correctly.

```python
from fhircraft.fhir.resources.factory import factory

# Check if a specific definition exists
has_definition = factory.repository.has(
    "http://hl7.org/fhir/StructureDefinition/Patient"
)
print(f"Patient definition available: {has_definition}")

# Get all available versions of a definition
versions = factory.repository.get_versions(
    "http://hl7.org/fhir/StructureDefinition/Patient"
)
print(f"Available versions: {versions}")

# Get the latest version
latest = factory.repository.get_latest_version(
    "http://hl7.org/fhir/StructureDefinition/Patient"
)
print(f"Latest version: {latest}")
```

See [managing FHIR artifacts](managing-fhir-artifacts.md) for information about loading definitions into the repository and controlling internet access.

## Code Generation

The code generator converts constructed Pydantic models into Python source code. This is useful when you want to save generated models to files instead of constructing them at runtime. The generated code includes all field definitions, validators, and properties from the original model.

You use code generation to avoid runtime overhead of model construction. Instead of loading structure definitions and constructing models each time your application starts, you generate the code once and import the models directly. This is especially valuable in production environments where startup time matters.

The generated code is readable Python that you can inspect, modify, and share with others. All imports are included automatically, so the generated file is self-contained.

```python
from fhircraft.fhir.resources.factory import factory
from fhircraft.fhir.resources.generator import generate_resource_model_code

# Load a package and construct a model
factory.load_package("hl7.fhir.us.core", "5.0.1")
USCorePatient = factory.construct_resource_model(
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

## Multiple Models Generation Recipe

When working with multiple profiles from an implementation guide, you generate all models together in a single file. This keeps related models organized and ensures they can reference each other correctly.

```python
from fhircraft.fhir.resources.factory import factory
from fhircraft.fhir.resources.generator import generate_resource_model_code

# Load the implementation guide
factory.load_package("hl7.fhir.us.core", "5.0.1")

# Construct multiple related models
models_to_generate = []

us_core_profiles = [
    "us-core-patient",
    "us-core-condition",
    "us-core-procedure",
]

# Construct each model and add to the list
for profile_name in us_core_profiles:
    model = factory.construct_resource_model(
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

## Generated Code Options

The generator includes options for controlling what appears in the output code. You can exclude validators when you only need the field definitions or when validators cause issues with your workflow.

```python
from fhircraft.fhir.resources.generator import generate_resource_model_code

# Generate without validators
# This creates simpler code with just field definitions
source_code = generate_resource_model_code(
    USCorePatient,
    include_validators=False
)

# The generated code will only have field definitions
# Use this when validators are not needed or cause problems
with open("us_core_patient_simple.py", "w") as f:
    f.write(source_code)
```

Validators enforce additional constraints beyond basic type checking. The [Pydantic validators documentation](https://docs.pydantic.dev/latest/concepts/validators/) explains how validators work and when to use them.

## Generated Code Structure

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

The generator handles inheritance, forward references, and circular dependencies automatically. See the [Pydantic model configuration documentation](https://docs.pydantic.dev/latest/api/config/) for information about model settings.

## Error Handling Recipe

Model construction can fail when structure definitions are missing or invalid. This recipe shows how to handle construction errors gracefully.

```python
from fhircraft.fhir.resources.factory import factory
from pydantic import ValidationError

def safe_model_construction(canonical_url: str):
    """Construct a model with error handling."""
    try:
        # Try to construct the model
        model = factory.construct_resource_model(canonical_url)
        return model
    except ValueError as e:
        # Structure definition not found or invalid
        print(f"Cannot construct model: {e}")
        return None
    except Exception as e:
        # Other construction errors
        print(f"Construction failed: {e}")
        return None

# Use the function to safely construct models
PatientModel = safe_model_construction(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

if PatientModel:
    # Proceed with model usage
    patient = PatientModel(
        identifier=[{"system": "http://example.org", "value": "123"}],
        name=[{"family": "Doe", "given": ["John"]}],
        gender="male"
    )
    print(f"Created patient: {patient.name[0].family}")
else:
    print("Model construction failed, using fallback behavior")
```

See the [Pydantic error handling documentation](https://docs.pydantic.dev/latest/errors/errors/) for information about validation errors.

## Common Problems

| Problem | Cause | Solution |
|---------|-------|----------|
| ValueError: Structure definition not found | The canonical URL is not in the repository | Load the package or file containing the definition. See [managing FHIR artifacts](managing-fhir-artifacts.md) |
| ValueError: Structure definition missing snapshot | The definition only has differential elements | Use a complete structure definition with snapshot element. Most published profiles include snapshots |
| Model construction is slow | Constructing models without caching | The factory caches models automatically. Reuse the same factory instance across your application |
| Profile constraints not enforced | Using base resource model instead of profile model | Construct a model from the profile canonical URL, not the base resource |
| Cannot find profile from implementation guide | Package not loaded or incorrect canonical URL | Verify the package is loaded and check the canonical URL in the implementation guide documentation |
| Models conflict between FHIR versions | Multiple FHIR versions loaded | Use version-specific canonical URLs or load only one FHIR version per repository |
| Memory usage increases over time | Many models cached | Clear the cache periodically with `factory.clear_cache()` if needed |
| Thread safety issues | Concurrent modifications to repository | Load all definitions during application startup before concurrent access |

## Further Resources

Pydantic Model Construction:
- [Creating models from base classes](https://docs.pydantic.dev/latest/concepts/models/#creating-models-from-base-classes)
- [Dynamic model creation](https://docs.pydantic.dev/latest/concepts/models/#dynamic-model-creation)
- [Model configuration](https://docs.pydantic.dev/latest/api/config/)
- [Custom validators](https://docs.pydantic.dev/latest/concepts/validators/)

FHIR Specifications:
- [StructureDefinition resource](https://hl7.org/fhir/structuredefinition.html)
- [Profiling FHIR](https://hl7.org/fhir/profiling.html)
- [FHIR packages](https://hl7.org/fhir/packages.html)
- [Canonical URLs](https://hl7.org/fhir/references.html#canonical)
- [FHIR versioning](https://hl7.org/fhir/versions.html)

Related Pages:
- [Managing FHIR Artifacts](managing-fhir-artifacts.md) - Loading structure definitions and packages
- [Resources and Models](resources-models.md) - Working with resource instances
- [Configuration](configuration.md) - Controlling validation behavior