# Resource Factory

This guide is for developers who want to construct Pydantic models from FHIR structure definitions, implementation guides, and packages. You'll learn to use Fhircraft's factory system to build type-safe FHIR models from various sources, manage repositories, and handle complex scenarios like custom profiles and multiple FHIR versions.

## Prerequisites

Before diving into this guide, make sure you understand:

- **Basic Fhircraft concepts** from the [FHIR Resources Overview](resources-overview.md)
- **FHIR structure definitions** and how they define resource shapes
- **Python imports and package management**

## Overview

Fhircraft transforms FHIR structure definitions into usable Python Pydantic models that provide type safety, validation, and easy integration with your applications. The factory system supports multiple construction methods:

- **Direct Construction** - Build models from loaded structure definitions
- **Canonical URL Resolution** - Resolve definitions from URLs with fallback strategies
- **FHIR Package Loading** - Load complete implementation guides and profiles
- **Repository Management** - Organize multiple definitions with version control

## Basic Model Construction

### Direct Model Construction from Structure Definitions

Use `construct_resource_model` to create Pydantic models from FHIR structure definitions. This method provides complete control and security by working with local files.

**Requirements:**

- Structure definitions must include a `snapshot` section (not just differential)
- Fhircraft automatically detects and handles FHIR version differences (R4, R4B, R5)

```python
from fhircraft.fhir.resources.factory import construct_resource_model
from fhircraft.utils import load_file

# Load structure definition from local file
structure_def = load_file('patient_profile.json')

# Create the Pydantic model
PatientModel = construct_resource_model(structure_definition=structure_def)

# Use the model with automatic validation
patient = PatientModel(
    name=[{"given": ["John"], "family": "Doe"}],
    birthDate="1990-05-15",
    gender="male"
)

print(f"Created model for: {structure_def['name']}")
```

### Repository-Based Management

For applications with multiple structure definitions, use the repository system for organized management:

```python
from fhircraft.fhir.resources.factory import factory

# Configure repository with multiple sources
factory.configure_repository(
    directory="./fhir-profiles",            # Load all JSON/YAML files from directory
    files=["./custom-profile.json"],        # Include specific files
    internet_enabled=True                   # Enable internet fallback for canonical URLs
)

# Reference models by their canonical URLs
CustomPatient = factory.construct_resource_model(
    canonical_url="http://example.org/StructureDefinition/CustomPatient"
)

# Use the constructed model
patient = CustomPatient(
    name=[{"given": ["Alice"], "family": "Johnson"}],
    gender="female"
)
```

## Canonical URL Resolution

Canonical URLs are globally unique identifiers for FHIR conformance resources. Fhircraft's repository system uses a smart resolution strategy that checks local definitions first, then falls back to internet downloads when needed.

### Basic URL Resolution

Canonical URLs provide a standardized way to reference FHIR structure definitions. Fhircraft can resolve these URLs automatically, checking local sources first and falling back to internet downloads when needed:

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# Construct from official FHIR Patient resource
patient_model = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Construct from a custom profile (will try local first, then download)
custom_profile_model = construct_resource_model(
    canonical_url="http://example.org/fhir/StructureDefinition/MyPatientProfile"
)

# Construct from HL7 implementation guides
us_core_patient = construct_resource_model(
    canonical_url="http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

# Specify exact versions using the canonical URL format
versioned_patient = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient|4.3.0"
)
```

### Multi-Source Resolution Strategy

Fhircraft follows a prioritized lookup strategy for robust definition resolution:

!!! tip "Resolution Priority"

    1. **Local Definitions** - Structure definitions loaded from local files (highest priority)
    2. **Package Registry** - Definitions from loaded FHIR packages (medium priority)  
    3. **Internet Fallback** - Downloads from canonical URLs if not found locally (lowest priority)
    4. **Version Support** - Handles semantic versioning with latest version tracking
    5. **Caching** - Automatically caches downloaded definitions for better performance

!!! warning "Network Dependencies"

    When using canonical URLs for definitions not available locally, ensure you have internet connectivity. For production environments, consider pre-loading all required structure definitions locally.

## FHIR Package Integration

FHIR packages contain published specifications like US Core, International Patient Summary, and other Implementation Guides. Fhircraft automatically downloads, caches, and integrates these packages into your development workflow.

### Quick Start with Packages

The fastest way to get started with FHIR packages is to load a popular implementation guide like US Core. This example shows the complete workflow from package loading to model usage:

```python
from fhircraft.fhir.resources.factory import ResourceFactory

# Enable package loading
factory = ResourceFactory(enable_packages=True)

# Load US Core Implementation Guide version 5.0.1
factory.load_package("hl7.fhir.us.core", "5.0.1")

# Create a US Core Patient model with enhanced validation
USCorePatient = factory.construct_resource_model(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

# Use the model with US Core constraints
patient = USCorePatient(
    name=[{"given": ["John"], "family": "Doe"}],
    gender="male",
    # US Core requires identifier
    identifier=[{
        "system": "http://example.org/mrn",
        "value": "12345"
    }]
)

print(f"Created US Core patient: {patient.name[0].given[0]} {patient.name[0].family}")
```

### Batch Package Loading

Load multiple packages efficiently for comprehensive profile support:

```python
# Configure factory with multiple packages at once
factory.configure_repository(
    directory="local_profiles/",  # Load local files first
    packages=[
        "hl7.fhir.r4.core",                    # Latest version of FHIR R4 core
        ("hl7.fhir.us.core", "5.0.1"),        # Specific version of US Core
        ("hl7.fhir.uv.ips", "1.1.0"),         # International Patient Summary
        ("hl7.fhir.us.mcode", "3.0.0"),       # Minimal Common Oncology Data Elements
    ],
    internet_enabled=True
)

# All structure definitions from loaded packages are now available
USCorePatient = factory.construct_resource_model(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

IPSPatient = factory.construct_resource_model(
    "http://hl7.org/fhir/uv/ips/StructureDefinition/Patient-uv-ips"
)
```

### Common FHIR Packages

| Package | Description | Use Case |
|---------|-------------|----------|
| `hl7.fhir.r4.core` | FHIR R4 core specification | Base FHIR R4 resources |
| `hl7.fhir.r5.core` | FHIR R5 core specification | Base FHIR R5 resources |
| `hl7.fhir.us.core` | US Core Implementation Guide | US healthcare interoperability |
| `hl7.fhir.uv.ips` | International Patient Summary | Global patient summaries |
| `hl7.fhir.us.mcode` | Minimal Common Oncology Data Elements | Cancer care data |
| `hl7.fhir.uv.smart-app-launch` | SMART App Launch | OAuth2-based app authorization |

### Package Management Operations

Once you've loaded packages, you'll often need to inspect what's available, manage versions, or clean up when packages are no longer needed. These operations help you maintain control over your loaded packages:

```python
# Check what packages are loaded
packages = factory.get_loaded_packages()
print("Loaded packages:", packages)

# Check if specific package is loaded
if factory.has_package("hl7.fhir.us.core"):
    print("US Core is available")

# Remove packages when no longer needed
factory.remove_package("hl7.fhir.us.core", "5.0.1")

# Clear entire package cache
factory.clear_package_cache()

print(f"Cache cleared, {len(factory.get_loaded_packages())} packages remaining")
```

### Error Handling for Package Operations

Package loading can fail for various reasons - network issues, missing packages, or incorrect versions. Robust applications should handle these errors gracefully and provide helpful feedback:

```python
from fhircraft.fhir.packages import PackageNotFoundError, FHIRPackageRegistryError

def load_package_safely(package_name: str, version: str = None) -> bool:
    """Safely load a FHIR package with error handling."""
    try:
        factory.load_package(package_name, version)
        print(f"Successfully loaded {package_name} {version or 'latest'}")
        return True
    except PackageNotFoundError as e:
        print(f"Package not found: {e}")
        return False
    except FHIRPackageRegistryError as e:
        print(f"Registry error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error loading package: {e}")
        return False

# Usage
success = load_package_safely("hl7.fhir.us.core", "5.0.1")
if success:
    # Proceed with model construction
    pass
```

## Advanced Package Management

### Configuration Options

For production applications or specialized environments, you may need to customize the factory behavior. These configuration options provide control over package sources, timeouts, and access permissions:

```python
# Configure factory with custom settings
factory = ResourceFactory(
    enable_packages=True,
    registry_base_url="https://packages.fhir.org",  # Default FHIR package registry
    timeout=30.0,                                   # Request timeout in seconds
    internet_enabled=True                           # Allow internet access
)

# Configure repository with comprehensive options
factory.configure_repository(
    directory="./local_profiles",                   # Local structure definitions
    packages=[
        "hl7.fhir.r4.core",                       # Load latest version
        ("hl7.fhir.us.core", "5.0.1"),           # Load specific version
    ],
    registry_base_url="https://packages.fhir.org",
    internet_enabled=True,
    timeout=30.0
)
```

### Direct Package Registry Access

For advanced scenarios, interact directly with the FHIR package registry:

```python
from fhircraft.fhir.packages import FHIRPackageRegistryClient

# Create client for direct registry interaction
client = FHIRPackageRegistryClient()

# List available versions of a package
package_info = client.list_package_versions("hl7.fhir.us.core")
print(f"Latest version: {package_info.dist_tags.latest}")
print(f"All versions: {list(package_info.versions.keys())}")

# Download package manually (for custom processing)
package_data = client.download_package("hl7.fhir.us.core", "5.0.1")
print(f"Downloaded package size: {len(package_data)} bytes")
```

### Working with Multiple Package Sources

For complex applications, you might need to combine multiple sources of structure definitions - local files, different packages, and internet resources. The composite repository provides a unified interface:

```python
from pathlib import Path
from fhircraft.fhir.resources.repository import CompositeStructureDefinitionRepository

# Create repository with all sources enabled
repo = CompositeStructureDefinitionRepository(
    enable_packages=True,
    internet_enabled=True
)

# Load from multiple sources
repo.load_from_directory("local_profiles/")
repo.load_package("hl7.fhir.us.core", "5.0.1")

# Getting a structure definition checks sources in priority order
patient_def = repo.get("http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient")
if patient_def:
    print(f"Found definition for: {patient_def['name']}")
```

### Integrated Construction Workflow

Combine package loading with model construction for complete workflows:

```python
# Complete workflow: Load packages and construct models
factory = ResourceFactory(enable_packages=True)

# Load required packages for comprehensive coverage
packages_to_load = [
    ("hl7.fhir.us.core", "5.0.1"),
    ("hl7.fhir.uv.ips", "1.1.0")
]

for package_name, version in packages_to_load:
    factory.load_package(package_name, version)

# Construct models from package definitions
USCorePatient = factory.construct_resource_model(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

USCoreCondition = factory.construct_resource_model(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-condition"
)

IPSPatient = factory.construct_resource_model(
    "http://hl7.org/fhir/uv/ips/StructureDefinition/Patient-uv-ips"
)

# Use the models with proper validation
us_patient = USCorePatient(
    identifier=[{"system": "http://example.com", "value": "123"}],
    name=[{"family": "Doe", "given": ["John"]}],
    gender="male"
)

print(f"Created US Core patient: {us_patient.id}")
```

## Model Caching and Performance

### Automatic Model Caching

Fhircraft automatically caches constructed models based on their canonical URLs to improve performance:

```python
from fhircraft.fhir.resources.factory import construct_resource_model, factory

# First call - downloads and constructs the model
patient_model_1 = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Second call - returns cached model (much faster)
patient_model_2 = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Verify they're the same cached instance
assert patient_model_1 is patient_model_2
print("Models are identical (cached)")

# Clear the cache when needed
factory.clear_cache()

# This will now reconstruct the model
patient_model_3 = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

print("Model reconstructed after cache clear")
```

### Cache Management Best Practices

!!! tip "When to Clear Cache"
    
    Clear the cache when:
    
    - **Structure definitions have been updated** - Ensure you're using the latest versions
    - **During development/testing** - Ensure fresh model construction between test runs
    - **Memory optimization** - Free memory when working with many different profiles
    - **Version switching** - When changing between different versions of the same profile

!!! note "Performance Considerations"
    
    - **Cache hits are ~1000x faster** than model reconstruction
    - **Memory usage grows** with the number of unique canonical URLs
    - **Thread safety** - Cache is safe for concurrent read access
    - **Production deployment** - Consider warming the cache with frequently used models

## Multi-Version FHIR Support

### Working with Different FHIR Releases

Fhircraft automatically detects the FHIR version from structure definitions and uses the appropriate data types:

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

print(f"R4 Patient type: {type(r4_patient)}")
print(f"R5 Patient type: {type(r5_patient)}")
```

### Direct Version-Specific Imports

For explicit version control, import pre-built models for specific FHIR releases:

```python
# Direct imports for specific releases
from fhircraft.fhir.resources.datatypes.R4.complex_types import Patient as PatientR4
from fhircraft.fhir.resources.datatypes.R4B.complex_types import Patient as PatientR4B  
from fhircraft.fhir.resources.datatypes.R5.complex_types import Patient as PatientR5

# Use the appropriate model for your data version
patient_r4 = PatientR4(name=[{"family": "Smith"}])
patient_r5 = PatientR5(name=[{"family": "Smith"}])

# Each model enforces version-specific constraints
print(f"R4 Patient resourceType: {patient_r4.resourceType}")
print(f"R5 Patient resourceType: {patient_r5.resourceType}")
```

## Repository System Management

### Basic Repository Configuration

The repository system provides efficient storage, versioning, and retrieval of structure definitions:

```python
from fhircraft.fhir.resources.factory import factory

# Configure repository with multiple sources
factory.configure_repository(
    directory="/path/to/structure/definitions",    # Load all JSON files from directory
    files=[                                        # Load specific files
        "/path/to/custom/profile1.json",
        "/path/to/custom/profile2.json"
    ],
    definitions=[structure_def_dict],              # Load from pre-loaded dictionaries
    internet_enabled=True                          # Allow internet fallback
)

# Use canonical URLs - will check local first, then internet
Patient = factory.construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)
```

### Advanced Repository Operations

The repository system provides fine-grained control over how definitions are loaded and managed. These operations are useful for dynamic loading, offline operation, and repository introspection:

```python
from fhircraft.fhir.resources.factory import factory

# Load definitions incrementally
factory.load_definitions_from_directory("/path/to/core/definitions")
factory.load_definitions_from_files("/path/to/custom/profile.json")

# Control internet access dynamically
factory.disable_internet_access()  # Offline mode for production
print("Internet access disabled")

# Perform offline operations...

factory.enable_internet_access()   # Re-enable for development
print("Internet access restored")

# Check repository status
repository = factory.repository
has_definition = repository.has("http://hl7.org/fhir/StructureDefinition/Patient")
available_versions = repository.get_versions("http://hl7.org/fhir/StructureDefinition/Patient")
latest_version = repository.get_latest_version("http://hl7.org/fhir/StructureDefinition/Patient")

print(f"Patient definition available: {has_definition}")
print(f"Available versions: {available_versions}")
print(f"Latest version: {latest_version}")
```

### Versioned Structure Definitions

The repository system supports FHIR versioning using the canonical URL format `url|version`:

```python
from fhircraft.fhir.resources.factory import factory

# Load specific version
patient_v401 = factory.construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient|4.0.1"
)

# Load latest version (default behavior)
patient_latest = factory.construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Check available versions
versions = factory.repository.get_versions("http://hl7.org/fhir/StructureDefinition/Patient")
print(f"Available versions: {versions}")

# Get version metadata
version_info = factory.repository.get_version_info("http://hl7.org/fhir/StructureDefinition/Patient|4.0.1")
print(f"Version info: {version_info}")
```

## Best Practices

### Production Deployment

!!! tip "Production Configuration"
    
    For production environments:
    
    1. **Pre-load all definitions** - Load all required structure definitions at application startup
    2. **Disable internet access** - Use `factory.disable_internet_access()` to prevent unexpected network calls
    3. **Version pinning** - Use specific versions in canonical URLs for reproducible builds
    4. **Local storage** - Store structure definitions in your application's resources directory
    5. **Cache warming** - Pre-construct frequently used models to improve runtime performance

```python
def setup_production_factory() -> ResourceFactory:
    """Configure factory for production use."""
    factory = ResourceFactory(
        enable_packages=True,
        internet_enabled=False  # Disable internet for production
    )
    
    # Load all required packages with specific versions
    required_packages = [
        ("hl7.fhir.us.core", "5.0.1"),
        ("hl7.fhir.uv.ips", "1.1.0"),
    ]
    
    for package_name, version in required_packages:
        factory.load_package(package_name, version)
    
    # Pre-construct frequently used models
    common_models = [
        "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient",
        "http://hl7.org/fhir/us/core/StructureDefinition/us-core-condition",
    ]
    
    for canonical_url in common_models:
        factory.construct_resource_model(canonical_url)
        
    return factory
```

### Error Handling and Validation

Model construction can fail for various reasons - missing definitions, network issues, or invalid structure definitions. Implementing comprehensive error handling ensures your application remains stable:

```python
def safe_model_construction(canonical_url: str) -> tuple[bool, any]:
    """Safely construct a model with comprehensive error handling."""
    try:
        model = factory.construct_resource_model(canonical_url)
        return True, model
    except PackageNotFoundError as e:
        print(f"Package not found for {canonical_url}: {e}")
        return False, f"Package not found: {e}"
    except ValueError as e:
        print(f"Invalid structure definition for {canonical_url}: {e}")
        return False, f"Invalid definition: {e}"
    except Exception as e:
        print(f"Unexpected error constructing {canonical_url}: {e}")
        return False, f"Construction failed: {e}"

# Usage
success, result = safe_model_construction("http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient")
if success:
    PatientModel = result
    print(f"Successfully constructed model")
else:
    error_message = result
    print(f"Failed to construct model: {error_message}")
```

### Memory and Performance Optimization

!!! warning "Memory Considerations"
    
    - **Repository keeps definitions in memory** for fast access
    - **Monitor memory usage** with many definitions
    - **Consider on-demand loading** for large applications
    - **Clear caches periodically** if memory becomes a concern

!!! note "Thread Safety"
    
    - **Repository is thread-safe** for read operations
    - **Avoid concurrent modifications** from multiple threads
    - **Cache access is atomic** for model retrieval
    - **Package loading should be done in main thread**

## Troubleshooting

### Common Issues and Solutions

#### Package Not Found
```python
# Issue: PackageNotFoundError when loading package
try:
    factory.load_package("hl7.fhir.us.core", "999.0.0")  # Non-existent version
except PackageNotFoundError:
    print("Check package name and version at https://packages.fhir.org")
```

#### Internet Access Issues
```python
# Issue: Cannot download canonical URLs
factory.disable_internet_access()
# Ensure all required definitions are loaded locally
```

#### Version Conflicts
```python
# Issue: Multiple versions of same package
factory.remove_package("hl7.fhir.us.core", "4.0.0")  # Remove old version
factory.load_package("hl7.fhir.us.core", "5.0.1")    # Load new version
```

#### Cache Issues
```python
# Issue: Stale cached models
factory.clear_cache()  # Clear all cached models
# Reconstruct models with updated definitions
```

## What's Next?

Now that you understand model construction, explore these related topics:

- **[Resource Models](resources-models.md)** - Learn to create and work with resource instances
- **[Pydantic FHIR](pydantic-representation.md)** - Understand the technical foundations of FHIR representation
- **[FHIR Path](fhirpath.md)** - Query and manipulate resources with FHIRPath expressions
- **[FHIR Mapper](mapper.md)** - Transform external data into FHIR resources

---

**Continue learning:** [Resource Models →](resources-models.md)