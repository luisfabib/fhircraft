# FHIR Package Loading

Fhircraft provides comprehensive support for loading FHIR packages from package registries, making it easy to work with published FHIR Implementation Guides, core specifications, and custom packages. This guide covers how to use the package loading functionality to automatically download and manage FHIR structure definitions.

## Overview

FHIR packages are standardized distributions of FHIR artifacts (structure definitions, value sets, code systems, etc.) that can be published to package registries. Fhircraft's package loading system provides:

- **Automatic Package Discovery**: Download packages from public registries like packages.fhir.org
- **Version Management**: Load specific versions or automatically use the latest version
- **Local Caching**: Cache downloaded packages for offline use and performance
- **Registry Configuration**: Support for custom package registries
- **Integration**: Seamless integration with Fhircraft's model construction system

## Quick Start

### Loading a Package

The simplest way to load a FHIR package is using the ResourceFactory:

```python
from fhircraft.fhir.resources.factory import ResourceFactory

# Create factory with package support enabled
factory = ResourceFactory(enable_packages=True)

# Load US Core Implementation Guide
loaded_definitions = factory.load_package("hl7.fhir.us.core", "5.0.1")

print(f"Loaded {len(loaded_definitions)} structure definitions")

# Now you can use any structure definition from the package
patient_model = factory.construct_resource_model(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)
```

### Using the Repository System

For more control, you can work directly with the repository system:

```python
from fhircraft.fhir.resources.repository import CompositeStructureDefinitionRepository

# Create repository with package support
repo = CompositeStructureDefinitionRepository(enable_packages=True)

# Load package
repo.load_package("hl7.fhir.us.core", "5.0.1")

# Get structure definitions (automatically falls back to packages)
patient_def = repo.get("http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient")
```

## Package Registry Client

For direct interaction with package registries, use the FHIRPackageRegistryClient:

```python
from fhircraft.fhir.packages import FHIRPackageRegistryClient

# Create client
client = FHIRPackageRegistryClient()

# List available versions
package_info = client.list_package_versions("hl7.fhir.us.core")
print(f"Latest version: {package_info.dist_tags.latest}")

# Download package manually
package_data = client.download_package("hl7.fhir.us.core", "5.0.1")
```

## Configuration Options

### Factory Configuration

```python
# Configure factory with package settings
factory = ResourceFactory(
    enable_packages=True,
    registry_base_url="https://packages.fhir.org",  # Default registry
    timeout=30.0,  # Request timeout
    internet_enabled=True  # Allow internet access
)

# Configure repository with multiple sources
factory.configure_repository(
    packages=[
        "hl7.fhir.r4.core",  # Load latest version
        ("hl7.fhir.us.core", "5.0.1"),  # Load specific version
    ],
    registry_base_url="https://packages.fhir.org",
    internet_enabled=True
)
```

### Repository Configuration

```python
# Create repository with custom settings
repo = CompositeStructureDefinitionRepository(
    enable_packages=True,
    registry_base_url="https://custom.registry.com",
    timeout=60.0,
    internet_enabled=True
)

# Change registry URL at runtime
repo.set_registry_base_url("https://another.registry.com")
```

## Package Management

### Checking Loaded Packages

```python
# Check what packages are loaded
packages = factory.get_loaded_packages()
print("Loaded packages:", packages)

# Check if specific package is loaded
if factory.has_package("hl7.fhir.us.core"):
    print("US Core is loaded")

# Check specific version
if factory.has_package("hl7.fhir.us.core", "5.0.1"):
    print("US Core 5.0.1 is loaded")
```

### Package Cache Management

```python
# Remove a specific package
factory.remove_package("hl7.fhir.us.core", "5.0.1")

# Remove all versions of a package
factory.remove_package("hl7.fhir.us.core")

# Clear entire package cache
factory.clear_package_cache()
```

## Working with Multiple Sources

Fhircraft's repository system provides a unified interface that combines multiple sources with intelligent fallback:

1. **Local Definitions**: Loaded from files or directories (highest priority)
2. **Package Registry**: Loaded from FHIR packages (medium priority)
3. **HTTP Download**: Downloaded from canonical URLs (lowest priority)

```python
from pathlib import Path

# Create repository with all sources enabled
repo = CompositeStructureDefinitionRepository(
    enable_packages=True,
    internet_enabled=True
)

# Load from multiple sources
repo.load_from_directory("local_profiles/")
repo.load_package("hl7.fhir.us.core", "5.0.1")

# Getting a structure definition will check sources in priority order
patient_def = repo.get("http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient")
```

## Common Patterns

### Loading Core FHIR Specifications

```python
# Load FHIR R4 core specification
factory.load_package("hl7.fhir.r4.core")

# Load FHIR R5 core specification
factory.load_package("hl7.fhir.r5.core")
```

### Loading Implementation Guides

```python
# Load US Core Implementation Guide
factory.load_package("hl7.fhir.us.core", "5.0.1")

# Load International Patient Summary
factory.load_package("hl7.fhir.uv.ips", "1.1.0")

# Load SMART App Launch
factory.load_package("hl7.fhir.uv.smart-app-launch", "2.0.0")
```

### Batch Configuration

```python
# Configure factory with multiple packages at once
factory.configure_repository(
    directory="local_profiles/",
    packages=[
        "hl7.fhir.r4.core",
        ("hl7.fhir.us.core", "5.0.1"),
        ("hl7.fhir.uv.ips", "1.1.0"),
    ],
    internet_enabled=True
)
```

## Error Handling

### Common Exceptions

```python
from fhircraft.fhir.packages import PackageNotFoundError, FHIRPackageRegistryError

try:
    factory.load_package("nonexistent.package")
except PackageNotFoundError as e:
    print(f"Package not found: {e}")
except FHIRPackageRegistryError as e:
    print(f"Registry error: {e}")
```

### Offline Mode

```python
# Disable internet access (useful for production environments)
factory = ResourceFactory(
    enable_packages=True,
    internet_enabled=False  # Only use cached packages
)

# This will work if package is already cached
try:
    factory.load_package("hl7.fhir.us.core", "5.0.1")
except RuntimeError as e:
    print("Package not in cache and internet disabled")
```

## Best Practices

### 1. Version Pinning
Always specify exact versions in production environments:

```python
# Good: Specific version
factory.load_package("hl7.fhir.us.core", "5.0.1")

# Avoid: Latest version (can change)
factory.load_package("hl7.fhir.us.core")  # Gets latest
```

### 2. Offline-First Approach
For production systems, consider pre-loading packages and disabling internet access:

```python
# Development: Load packages with internet enabled
if development_mode:
    factory = ResourceFactory(enable_packages=True, internet_enabled=True)
    factory.load_package("hl7.fhir.us.core", "5.0.1")
    
# Production: Use cached packages only
else:
    factory = ResourceFactory(enable_packages=True, internet_enabled=False)
```

### 3. Error Handling
Always handle package loading errors gracefully:

```python
def load_packages_safely(factory, packages):
    loaded = []
    for package_spec in packages:
        try:
            if isinstance(package_spec, tuple):
                name, version = package_spec
                definitions = factory.load_package(name, version)
            else:
                definitions = factory.load_package(package_spec)
            loaded.extend(definitions)
        except (PackageNotFoundError, FHIRPackageRegistryError) as e:
            print(f"Failed to load {package_spec}: {e}")
    return loaded
```

### 4. Resource Management
Clear package cache when appropriate to manage memory:

```python
# After processing, clear cache to free memory
factory.clear_package_cache()

# Or remove specific packages no longer needed
factory.remove_package("temporary.package")
```

## Advanced Usage

### Custom Registry

```python
# Use a custom package registry
factory = ResourceFactory(
    enable_packages=True,
    registry_base_url="https://mycompany.packages.com"
)
```

### Integration with Model Construction

```python
# Load packages and construct models in one workflow
factory = ResourceFactory(enable_packages=True)

# Load required packages
factory.load_package("hl7.fhir.us.core", "5.0.1")

# Construct models from package definitions
USCorePatient = factory.construct_resource_model(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

USCoreCondition = factory.construct_resource_model(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-condition"
)

# Use the models
patient = USCorePatient(
    resourceType="Patient",
    identifier=[{"system": "http://example.com", "value": "123"}],
    name=[{"family": "Doe", "given": ["John"]}]
)
```

## Troubleshooting

### Package Not Found
- Verify the package name and version exist on the registry
- Check internet connectivity
- Ensure the registry URL is correct

### Download Failures
- Check network connectivity
- Verify registry accessibility
- Try increasing the timeout value

### Cache Issues
- Clear the package cache and reload
- Check file permissions in cache directory
- Verify disk space availability

### Structure Definition Not Found
- Ensure the package containing the definition is loaded
- Check the canonical URL is correct
- Verify the structure definition exists in the package
