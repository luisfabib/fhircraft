# Managing FHIR Artifacts

This guide shows you how to organize and load FHIR structure definitions and packages from different sources. Building on the resource construction concepts covered earlier, you will learn to work with local files, download published packages, and configure Fhircraft to access multiple definition sources simultaneously.

## What Are FHIR Artifacts

FHIR artifacts are files that describe the structure and rules for healthcare data. Think of them as blueprints that tell Fhircraft how to validate and organize patient information, lab results, and other medical records. When you build a resource model using Fhircraft, the library needs these artifacts to resolve the core [structure definition](https://www.hl7.org/fhir/structuredefinition.html) and any dependent definitions it references. For example, building a patient profiled model requires the patient profile structure definition itself plus any other definitions from which it may derive.

Structure definitions are a type of FHIR [conformance resource](https://www.hl7.org/fhir/conformance-module.html) that formally defines the data elements, constraints, terminology bindings, and cardinality rules for FHIR resources and data types. The FHIR specification provides [base structure definitions](https://www.hl7.org/fhir/profilelist.html) for all standard resources like Patient, Observation, and Medication.

Artifacts are needed at resource model build time to resolve all these dependencies and create complete, validated models. Once a model is built, all the relevant information is contained within the model itself and the artifacts can be removed from memory. This means you can load artifacts, build your models, and then discard the artifacts to free up resources. The built models remain fully functional because they already contain all the validation rules and structural information they need.

Managing artifacts carefully provides important benefits beyond just building models. It gives you fine control over which structure definition files and versions your application uses, ensuring consistency and predictability. It also allows you to work in offline or restricted network settings where accessing the internet or FHIR server resources is not possible or limited. Many healthcare environments have strict security policies that prevent applications from making external network requests. By loading artifacts from local files or pre-downloaded packages, you can build FHIR models in these restricted environments without any internet dependency.

## Loading Structure Definitions from Your Computer

When you have structure definition files saved on your computer, you can load them into Fhircraft. This approach works without an internet connection and gives you full control over which definitions you use. Many organizations maintain their own structure definitions for custom data requirements or internal profiles. By storing these files locally, you ensure that your application always uses the exact versions you have tested and approved, rather than relying on external sources that might change.

### Loading from a Directory

If you have organized your structure definition files into a folder, Fhircraft can scan that folder and load all valid definitions automatically. This method works well when you maintain a collection of related definitions that your application needs. The factory looks for JSON and YAML files, validates them as structure definitions, and makes them available for model construction. Any files that are not valid structure definitions are skipped without causing errors.

This approach simplifies project setup because you can keep all your definitions in one place and load them with a single command. As you add new structure definitions to the folder, they become available immediately without changing your code:

```python
# Import the factory that manages FHIR resources
from fhircraft.fhir.resources.factory import factory

# Point to the folder containing your structure definition files
definitions_folder = "/path/to/your/definitions"

# Load all structure definitions from the folder
factory.configure_repository(directory=definitions_folder)

# Now you can create models from the loaded definitions
Patient = factory.construct_resource_model(
    canonical_url="http://example.org/StructureDefinition/MyPatient"
)

# Use the model to create a patient record
patient = Patient(
    name=[{"given": ["Maria"], "family": "Garcia"}],
    gender="female"
)

print(f"Created patient: {patient.name[0].given[0]} {patient.name[0].family}")
#> Created patient: Maria Garcia
```

### Loading from Individual Files

Sometimes you need precise control over which structure definitions get loaded. Perhaps you are working with a small set of definitions, or you want to load files from different directories, or you need to ensure only specific versions are used. In these cases, explicitly listing the files gives you that control.

This method also helps during development and testing. You can load just the definitions you are actively working with, making it easier to isolate problems and verify behavior. As your code evolves, you can add or remove files from the list without restructuring your project directories:

```python
from fhircraft.fhir.resources.factory import factory

# List the exact files you want to load
patient_file = "/path/to/patient_definition.json"
observation_file = "/path/to/observation_definition.json"

# Load the structure definitions from these files
factory.configure_repository(files=[patient_file, observation_file])

# Create models from the loaded definitions
Patient = factory.construct_resource_model(
    canonical_url="http://example.org/StructureDefinition/MyPatient"
)

Observation = factory.construct_resource_model(
    canonical_url="http://example.org/StructureDefinition/MyObservation"
)

# Use the models to create records
patient = Patient(name=[{"family": "Smith"}])
observation = Observation(status="final", code={"text": "Blood pressure"})

print(f"Loaded {len([Patient, Observation])} resource types")
```

### Loading from Python Dictionaries

In some workflows, you receive structure definitions as data rather than files. You might fetch them from a database, receive them through an API, or generate them programmatically. When structure definitions exist as Python dictionaries in your code, you can load them directly without writing temporary files to disk.

This method integrates well with dynamic applications where structure definitions might change based on user input, configuration settings, or external data sources. The factory validates the dictionary structure and adds it to the repository just as it would with a file-based definition:

```python
from fhircraft.fhir.resources.factory import factory
import json

# Read a structure definition file into a dictionary
with open("test/static/fhir-profiles-definitions/us-core-patient.json", "r") as file:
    definition_dict = json.load(file)

# Load the definition from the dictionary
factory.configure_repository(definitions=[definition_dict])

# Create a model from the loaded definition
USCorePatient = factory.construct_resource_model(
    canonical_url=definition_dict["url"]
)

print(f"Created model from dictionary: {definition_dict['name']}")
```

## Working with FHIR Packages

[FHIR packages](https://registry.fhir.org/) are standardized distribution bundles that contain complete sets of structure definitions, value sets, code systems, and other FHIR conformance resources. These packages represent collaborative work by healthcare experts, implementers, and standards bodies to create consistent, interoperable data structures. Rather than building everything from scratch, you can adopt these established standards by loading the appropriate packages.

Packages solve a practical problem: healthcare interoperability requires many structure definitions to work together consistently. A single patient record might reference dozens of related definitions for names, addresses, identifiers, extensions, and constraints. Packages bundle all these related definitions so you get everything you need in one download. They also handle version compatibility, ensuring that all the definitions within a package work together correctly. The official [FHIR Package Registry](https://registry.fhir.org/) hosts hundreds of published implementation guides and conformance resources.

Fhircraft connects to the FHIR package registry at [packages.fhir.org](https://packages.fhir.org/), downloads requested packages following the [FHIR NPM Package Specification](https://confluence.hl7.org/display/FHIR/NPM+Package+Specification), extracts the structure definitions, and caches them locally for future use. After the first download, subsequent loads use the cached version, making your application faster and reducing network dependencies.

### Loading a FHIR Package

When you know which package and version you need, you can load it directly. The [FHIR Package Registry](https://registry.fhir.org/) hosts hundreds of packages covering different healthcare domains, countries, and use cases. Each package has a unique name following the NPM naming convention and a [semantic version number](https://semver.org/). Popular packages include the [International Patient Summary](https://hl7.org/fhir/uv/ips/) for global interoperability, and [mCODE](https://hl7.org/fhir/us/mcode/) for oncology data. Here is a collection of commonly used FHIR packages:

| Package | Description | Use Case |
|---------|-------------|----------|
| `hl7.fhir.r4.core` | FHIR R4 core specification | Base FHIR R4 resources |
| `hl7.fhir.r5.core` | FHIR R5 core specification | Base FHIR R5 resources |
| `hl7.fhir.us.core` | US Core Implementation Guide | US healthcare interoperability |
| `hl7.fhir.uv.ips` | International Patient Summary | Global patient summaries |
| `hl7.fhir.us.mcode` | Minimal Common Oncology Data Elements | Cancer care data |
| `hl7.fhir.uv.smart-app-launch` | SMART Ascpp Launch | OAuth2-based app authorization |



Fhircraft downloads the package contents, extracts all structure definitions, and makes them available through their canonical URLs. The first time you load a package, Fhircraft downloads it from the internet and caches it on your computer. This download might take a few seconds depending on the package size. Subsequent loads use the cached version and complete almost instantly

Use this method to download and load a published FHIR package:

```python
from fhircraft.fhir.resources.factory import ResourceFactory

# Create a factory that can download packages
factory = ResourceFactory(enable_packages=True)

# Download and load the US Core package version 5.0.1
factory.configure_repository(
    packages=[("hl7.fhir.us.core", "5.0.1")],
    internet_enabled=True
)

# Create a model from the package
USCorePatient = factory.construct_resource_model(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

# Use the US Core patient model with its special rules
patient = USCorePatient(
    identifier=[{"system": "http://example.org", "value": "12345"}],
    name=[{"given": ["John"], "family": "Doe"}],
    gender="male"
)
print(f"Created US Core patient with ID: {patient.identifier[0].value}")
```
Real-world applications often need structure definitions from multiple packages. You might combine US Core for basic data exchange with specialty packages for oncology, cardiology, or other clinical domains. You might also need packages for different FHIR versions or international standards alongside country-specific requirements.

Loading packages individually works, but configuring the repository with all packages at once simplifies your setup code. This approach also ensures all packages load before your application starts constructing models, avoiding situations where a model construction fails because a required package is not yet available

### Loading Multiple Packages at Once

Use this method when your project needs several FHIR packages:

```python
from fhircraft.fhir.resources.factory import factory

# Configure the factory to load multiple packages
factory.configure_repository(
    packages=[
        ("hl7.fhir.us.core", "5.0.1"),  # US healthcare standards
        ("hl7.fhir.us.mcode", "1.1.0"), # Minimal Common Oncology Data Elements
    ],
    internet_enabled=True
)

# Create models from different packages
USCorePatient = factory.construct_resource_model(
    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

CancerPatient = factory.construct_resource_model(
    "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-patient"
)

# Use both models
us_patient = USCorePatient(name=[{"family": "Smith"}], gender="male")
mcode_patient = CancerPatient(name=[{"family": "Jones"}], gender="female")

print(f"Loaded {len([USCorePatient, mcode_patient])} different patient types")
```

As your application grows, you might lose track of which packages are loaded, especially if different parts of your code load different packages. Checking loaded packages helps you understand the current state of your factory and debug issues where expected structure definitions are not available.

This information is also useful for logging and diagnostics. When troubleshooting problems, knowing exactly which package versions are active helps you reproduce issues and verify that your production environment matches your testing environment

Use this method to see which packages are currently available:

```python
from fhircraft.fhir.resources.factory import factory

# Load some packages
factory.configure_repository(
    packages=[("hl7.fhir.us.core", "5.0.1")],
    internet_enabled=True
)

# Get a list of all loaded packages
loaded_packages = factory.get_loaded_packages()

# Display the loaded packages
print("Currently loaded packages:")
for name, version in loaded_packages.items():
    print(f"  - {name} version {version}")

# Check if a specific package is loaded
if factory.has_package("hl7.fhir.us.core"):
    print("US Core package is available")
else:
    print("US Core package is not loaded")
```

Packages consume memory because Fhircraft stores their structure definitions in active memory for fast access. In long-running applications or when processing many different data types, you might want to remove packages after you finish using them. This frees up memory and keeps your application responsive.

Removing packages is also useful when switching between different contexts. For example, if your application processes US data during business hours and European data overnight, you can load and unload the appropriate packages as needed rather than keeping everything in memory simultaneously

Use this method to free up memory by removing packages you no longer need:

```python
from fhircraft.fhir.resources.factory import factory

# Load a package
factory.configure_repository(
    packages=[("hl7.fhir.us.core", "5.0.1")],
    internet_enabled=True
)

# Later, remove it when you are done
factory.remove_package("hl7.fhir.us.core", "5.0.1")

# Or remove all versions of a package
factory.remove_package("hl7.fhir.us.core")

# Or clear all loaded packages at once
factory.clear_package_cache()

print("Package cache cleared")
```

## Using Canonical URLs

[Canonical URLs](https://www.hl7.org/fhir/references.html#canonical) are globally unique identifiers for FHIR conformance resources, as defined in the FHIR specification. Every structure definition has a canonical URL that identifies it unambiguously, regardless of where the definition file is stored or how it was obtained. This standardization enables interoperability because everyone can refer to the same structure definition using the same identifier. Canonical URLs follow the format of a URI but are not required to be resolvable web addresses, though many are.

When you provide a canonical URL to Fhircraft, the library follows a resolution strategy to find the corresponding structure definition. It first checks loaded local files and packages. If the definition is not found locally and internet access is enabled, Fhircraft attempts to download it from the URL. This fallback mechanism means you can reference any published structure definition without manually downloading files, while still benefiting from local caching for better performance.

### Basic URL Resolution

The canonical URL serves as the primary way to request structure definitions from the factory. Once you know the URL for a structure definition, you can construct a model from it regardless of whether that definition came from a local file, a package, or an internet download. This abstraction simplifies your code because you do not need to know or manage where definitions are stored.

Official FHIR resources, implementation guides, and custom profiles all use canonical URLs. The URL format typically includes the organization or standard followed by the resource type. For instance, US Core resources include the path segment indicating they come from the US Core implementation guide

Use this method when you know the canonical URL of the structure definition you need:

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# Create a model from the standard FHIR Patient definition
Patient = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Create a model from a US Core profile
USCorePatient = construct_resource_model(
    canonical_url="http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

# Use the models
patient = Patient(name=[{"family": "Brown"}])
us_patient = USCorePatient(
    identifier=[{"value": "123"}],
    name=[{"family": "Brown"}],
    gender="male"
)

print(f"Created {len([patient, us_patient])} patient records")
```

Structure definitions evolve over time as healthcare standards mature and requirements change. A structure definition that was appropriate last year might have new requirements this year. [Version numbers](https://www.hl7.org/fhir/versioning.html) track these changes and ensure you use the exact definition you intend. Without version specifications, you get whatever version the factory finds first, which might not match your expectations.

Two methods exist for specifying versions. You can append the version to the canonical URL using a vertical bar separator, following the [FHIR canonical reference format](https://www.hl7.org/fhir/references.html#canonical) (for example, `http://example.org/StructureDefinition/Patient|1.0.0`). Alternatively, you can pass the version as a separate parameter. Both approaches produce the same result, so choose whichever fits your code style

### Specifying Versions

Use this method when you need a specific version of a structure definition:

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# Request a specific version by adding it to the URL
PatientR4 = construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient|4.0.1"
)

# Each version may have different rules
patient_r4 = PatientR4(name=[{"family": "Wilson"}])
```

with internet access and offline mode without internet access. These modes give you control over when and how Fhircraft accesses external resources. Online mode provides convenience by automatically downloading structure definitions as needed, while offline mode ensures security and predictability by restricting the factory to local resources only.

The choice between modes depends on your environment and requirements. Development environments often benefit from online mode because you can experiment with different structure definitions without pre-downloading everything. Production environments often use offline mode after pre-loading all required definitions, ensuring that the application cannot be affected by network issues or changes to external resources.

### Working Online

Online mode enables automatic downloads when a canonical URL references a structure definition that is not available locally. This convenience accelerates development because you can try new structure definitions immediately without manually downloading and organizing files. Fhircraft handles the download, validates the definition, and caches it for future use.

The factory maintains its cache across application restarts, so each structure definition only downloads once. Even in online mode, the factory checks local sources first and only accesses the internet when necessary

Fhircraft can work in two modes: online mode (with internet access) and offline mode (without internet access). Online mode lets Fhircraft download structure definitions automatically, while offline mode only uses files already on your computer.

### Working Online

Use this method when you have internet access and want automatic downloads:

```python
from fhircraft.fhir.resources.factory import factory

# Enable internet access for automatic downloads
factory.enable_internet_access()

# Fhircraft will download this definition if it is not on your computer
Patient = factory.construct_resource_model(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Use the model
patient = Patient(name=[{"family": "Anderson"}])

print("Working in online mode with automatic downloads")
```

Offline mode prevents all internet access, ensuring the factory only uses structure definitions you have explicitly loaded from local sources. This mode is essential in secure environments where applications must not make unexpected network requests. It also provides stability by preventing external changes from affecting your application behavior.

When working offline, you must pre-load all structure definitions your application might need. If the factory encounters a canonical URL without a corresponding local definition, it raises an error rather than attempting an internet download. This fail-fast behavior helps you catch missing definitions during testing rather than at runtime in production


### Working Offline

Use this method when you do not have internet access or want to use only local files:

```python
from fhircraft.fhir.resources.factory import factory

# Configure repository with offline mode and local files
factory.configure_repository(
    directory="/path/to/definitions",
    internet_enabled=False
)

# Create models only from local files
Patient = factory.construct_resource_model(
    canonical_url="http://example.org/StructureDefinition/MyPatient"
)

# Use the model
patient = Patient(name=[{"family": "Taylor"}])

print("Working in offline mode with local files only")
```
Most applications need structure definitions from multiple sources. You might have custom profiles in local files, standard definitions from FHIR packages, and fallback access to the internet for occasional needs. Rather than configuring each source separately, you can set up everything at once using the comprehensive repository configuration.

This configuration approach creates a clear initialization point in your application where all definition sources are established. It also defines the priority order: the factory checks local directories first, then loaded packages, and finally attempts internet downloads if enabled. Understanding this priority helps you predict which version of a structure definition will be used when multiple sources provide the same canonical URL

## Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| Fhircraft cannot find a structure definition | Check that the canonical URL matches exactly. Make sure you have loaded the file, package, or enabled internet access. Verify the structure definition file is in the correct format (JSON). |
| Package download fails | Verify your internet connection. Check that the package name and version are correct. Try loading the package again after a few minutes. Visit https://registry.fhir.org to confirm the package exists. |
| Loading takes a long time | Fhircraft caches downloaded packages after the first use. Subsequent loads will be much faster. Consider loading packages once at application startup rather than repeatedly. |
| Wrong version of a structure definition is used | Specify the version explicitly in the canonical URL or as a parameter. Check loaded packages with `get_loaded_packages()` to verify versions. Clear the cache if you need to reload a different version. |
| Running out of memory with many packages | Remove packages you no longer need using `remove_package()`. Load only the packages required for your current task. Clear the entire cache with `clear_package_cache()` when switching between different projects. |

## Further Resources

[FHIR Package Registry](https://registry.fhir.org/) - Browse and search for available FHIR packages from the official registry

[FHIR Packages Documentation](https://packages.fhir.org/) - Technical documentation for the FHIR package server and NPM package format

[FHIR Structure Definitions](https://www.hl7.org/fhir/structuredefinition.html) - Detailed specification for structure definitions and profiling

[FHIR Conformance Module](https://www.hl7.org/fhir/conformance-module.html) - Overview of FHIR conformance resources including profiles, extensions, and implementation guides

[US Core Implementation Guide](https://www.hl7.org/fhir/us/core/) - The US national FHIR implementation guide for healthcare data exchange

[International Patient Summary](https://hl7.org/fhir/uv/ips/) - Global specification for patient summary documents

[FHIR Versioning](https://www.hl7.org/fhir/versioning.html) - How FHIR handles versioning of resources and conformance artifacts

[Canonical References](https://www.hl7.org/fhir/references.html#canonical) - Specification for canonical URL format and versioning syntax
