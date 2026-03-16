# Managing FHIR Artifacts

This guide shows you how to organize and load FHIR structure definitions and packages from different sources. Building on the resource construction concepts covered earlier, you will learn to work with local files, download published packages, and configure Fhircraft to access multiple definition sources simultaneously.

## What Are FHIR Artifacts

FHIR artifacts are files that describe the structure and rules for healthcare data. Think of them as blueprints that tell Fhircraft how to validate and organize patient information, lab results, and other medical records. When you build a resource model using Fhircraft, the library needs these artifacts to resolve the core [:material-fire: Structure Definition](https://www.hl7.org/fhir/structuredefinition.html) and any dependent definitions it references. For example, building a patient profiled model requires the patient profile structure definition itself plus any other definitions from which it may derive.

Structure definitions are a type of FHIR [:material-fire: Conformance Resource](https://www.hl7.org/fhir/conformance-module.html) that formally defines the data elements, constraints, terminology bindings, and cardinality rules for FHIR resources and data types. The FHIR specification provides [:material-fire: Base Structure Definitions](https://www.hl7.org/fhir/profilelist.html) for all standard resources like, e.g. [:material-fire: Patient](https://www.hl7.org/fhir/patient.html), [:material-fire: Observation](https://www.hl7.org/fhir/observation.html), and [:material-fire: Condition](https://www.hl7.org/fhir/condition.html). These are provided by Fhircraft and do not need to be provided.

Artifacts are needed at resource model build time to resolve all these dependencies and create complete, validated models. Once a model is built, all the relevant information is contained within the model itself and the artifacts can be removed from memory. This means you can load artifacts, build your models, and then discard the artifacts to free up resources. The built models remain fully functional because they already contain all the validation rules and structural information they need.

!!! note "Note"

    Managing artifacts carefully provides important benefits beyond just building models. It gives you fine control over which structure definition files and versions your application uses, ensuring consistency and predictability. It also allows you to work in offline or restricted network settings where accessing the internet or FHIR server resources is not possible or limited. Many healthcare environments have strict security policies that prevent applications from making external network requests. By loading artifacts from local files or pre-downloaded packages, you can build FHIR models in these restricted environments without any internet dependency.

## Factory Repository

The `factory` repository is a central storage and indexing system within Fhircraft resource model factory that manages all loaded structure definitions and makes them available for resource model construction. Think of it as a library catalog: when you load structure definitions from files, directories, packages, or the internet, they all get registered in this repository. When you later request a model using a canonical URL, the factory searches the repository to find the matching structure definition.

Understanding the repository helps you make informed decisions about when to load definitions, how to organize your project resources, and how to optimize your application's startup time and memory footprint. The following sections show you specific methods for loading structure definitions into the repository from different sources.

??? abstract "Technical Documentation"

    [`fhircraft.fhir.resources.repository`](/fhircraft/reference/fhir-resources-repository/)


## Loading Structure Definitions from Your Computer

When you have structure definition files saved on your computer, you can load them into Fhircraft. This approach works without an internet connection and gives you full control over which definitions you use. Many organizations maintain their own structure definitions for custom data requirements or internal profiles. By storing these files locally, you ensure that your application always uses the exact versions you have tested and approved, rather than relying on external sources that might change.

### Loading from files or Python Dictionaries

Sometimes you need precise control over which structure definitions get loaded. Perhaps you are working with a small set of definitions, or you want to load files from different directories, or you need to ensure only specific versions are used. In these cases, explicitly listing the files gives you that control.

In some workflows, you receive structure definitions as data rather than files. You might fetch them from a database, receive them through an API, or generate them programmatically. When structure definitions exist as Python dictionaries in your code, you can load them directly without writing temporary files to disk.

This method also helps during development and testing. You can load just the definitions you are actively working with, making it easier to isolate problems and verify behavior. As your code evolves, you can add or remove files from the list without restructuring your project directories:

```python
import json
from fhircraft.fhir.resources import ResourceFactory
factory = ResourceFactory(fhir_release="R4")

# Read a structure definition file into a dictionary
with open("test/static/fhir-profiles-definitions/us-core-patient.json", "r") as file:
    definition_dict = json.load(file)

# Load the definition from the dictionary
factory.add_structure_definition(definition_dict)

# Create a model from the loaded definition
USCorePatient = factory.build(
    canonical_url=definition_dict["url"]
)

# Use the model to create a patient record
patient = USCorePatient(
    name=[{"given": ["Maria"], "family": "Garcia"}],
    gender="female"
)

print(f"Created patient: {patient.name[0].given[0]} {patient.name[0].family}")
#> Created patient: Maria Garcia
```

## Working with FHIR Packages

[:material-fire: FHIR packages](https://registry.fhir.org/) are standardized distribution bundles that contain complete sets of structure definitions, value sets, code systems, and other FHIR conformance resources. These packages represent collaborative work by healthcare experts, implementers, and standards bodies to create consistent, interoperable data structures. Rather than building everything from scratch, you can adopt these established standards by loading the appropriate packages.

Packages solve a practical problem: healthcare interoperability requires many structure definitions to work together consistently. A single patient record might reference dozens of related definitions for names, addresses, identifiers, extensions, and constraints. Packages bundle all these related definitions so you get everything you need in one download. They also handle version compatibility, ensuring that all the definitions within a package work together correctly. The official [:material-fire: FHIR Package Registry](https://registry.fhir.org/) hosts hundreds of published implementation guides and conformance resources. Each package has a unique name following the NPM naming convention and a [semantic version number](https://semver.org/). Popular packages include the [:material-fire: International Patient Summary](https://hl7.org/fhir/uv/ips/) for global interoperability, and [:material-fire: mCODE](https://hl7.org/fhir/us/mcode/) for oncology data. Here is an exemplary collection of FHIR packages:

| Package | Description | Use Case |
|---------|-------------|----------|
| `hl7.fhir.r4.core` | FHIR R4 core specification | Base FHIR R4 resources |
| `hl7.fhir.r5.core` | FHIR R5 core specification | Base FHIR R5 resources |
| `hl7.fhir.us.core` | US Core Implementation Guide | US healthcare interoperability |
| `hl7.fhir.uv.ips` | International Patient Summary | Global patient summaries |
| `hl7.fhir.us.mcode` | Minimal Common Oncology Data Elements | Cancer care data |
| `hl7.fhir.uv.smart-app-launch` | SMART Ascpp Launch | OAuth2-based app authorization |

Fhircraft connects to the FHIR package registry at [:material-fire: `packages.fhir.org`](https://packages.fhir.org/), downloads requested packages (and their dependencies) following the [:material-fire: FHIR NPM Package Specification](https://confluence.hl7.org/display/FHIR/NPM+Package+Specification), extracts the structure definitions, and caches them locally for future use. After the first download, subsequent loads use the cached version, making your application faster and reducing network dependencies.

!!! warning "Internet Access"

    The following functionality and examples require a connection to the internet and to 3rd party servers. 

!!! example "Loading a FHIR Package"

    When you know which package and version you need, you can load it directly. Fhircraft downloads the package contents, extracts all structure definitions, and makes them available through their canonical URLs. The first time you load a package, Fhircraft downloads it from the internet and caches it on your computer. This download might take a few seconds depending on the package size, number of dependencies, and download speed. Subsequent loads use the cached version and complete almost instantly

    Use this method to download and load a published FHIR package:

    ```python
    from fhircraft.fhir.resources.factory import ResourceFactory

    # Create a factory that can download packages
    factory = ResourceFactory(fhir_release="R4")

    # Download and load the US Core package version 5.0.1
    factory.load_package("hl7.fhir.us.core", "5.0.1")

    # Create a model from the package
    USCorePatient = factory.build(
        "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
    )

    # Use the US Core patient model with its special rules
    patient = USCorePatient(
        identifier=[{"system": "http://example.org", "value": "12345"}],
        name=[{"given": ["John"], "family": "Doe"}],
        gender="male"
    )
    print(f"Created US Core patient with ID: {patient.identifier[0].value}")
    #> Created US Core patient with ID: 12345
    ```


!!! example "Loading Multiple Packages at Once"

    Real-world applications often need structure definitions from multiple packages. You might combine US Core for basic data exchange with specialty packages for oncology, cardiology, or other clinical domains. You might also need packages for different FHIR versions or international standards alongside country-specific requirements.

    Loading packages individually works, but configuring the repository with all packages at once simplifies your setup code. This approach also ensures all packages load before your application starts constructing models, avoiding situations where a model construction fails because a required package is not yet available

    Use this method when your project needs several FHIR packages:

    ```python
    from fhircraft.fhir.resources import ResourceFactory
    factory = ResourceFactory(fhir_release="R4")

    # Configure the factory to load multiple packages
    factory.load_package("hl7.fhir.us.core", "5.0.1")  # US healthcare standards
    factory.load_package("hl7.fhir.us.mcode", "1.1.0"), # Minimal Common Oncology Data Elements

    # Create models from different packages
    USCorePatient = factory.build(
        "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
    )

    CancerPatient = factory.build(
        "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-patient"
    )

    # Use both models
    us_patient = USCorePatient(name=[{"family": "Smith"}], gender="male")
    mcode_patient = CancerPatient(name=[{"family": "Jones"}], gender="female")

    print(f"Loaded {len([USCorePatient, mcode_patient])} different patient types")
    ```

## Canonical URLs

[:material-fire: Canonical URLs](https://www.hl7.org/fhir/references.html#canonical) are globally unique identifiers for FHIR conformance resources, as defined in the FHIR specification. Every structure definition has a canonical URL that identifies it unambiguously, regardless of where the definition file is stored or how it was obtained. This standardization enables interoperability because everyone can refer to the same structure definition using the same identifier. Canonical URLs follow the format of a URI but are not required to be resolvable web addresses, though many are.

When you provide a canonical URL to Fhircraft, the library follows a resolution strategy to find the corresponding structure definition. It first checks loaded local files and packages. If the definition is not found locally and internet access is enabled, Fhircraft attempts to download it from the URL. This fallback mechanism means you can reference any published structure definition without manually downloading files, while still benefiting from local caching for better performance.

!!! warning "Limitations of Internet-Based Canonical URL Resolution"

    While Fhircraft can attempt to download structure definitions directly from canonical URLs when internet access is enabled, this approach has important limitations. Canonical URLs are identifiers and may not point to downloadable files. Internet downloads create network dependencies that can fail in restricted environments, introduce security and compliance concerns in healthcare settings, and significantly impact performance compared to local files. Additionally, you lose version control when relying on external servers that might update definitions without notice. 
    
    *Best Practice*: For production applications, explicitly load structure definitions from packages or local files rather than relying on internet resolution. Use internet access primarily during development, and pre-load all required definitions during application initialization to ensure predictable, secure, and performant operation.

### Basic URL Resolution

The canonical URL serves as the primary way to request structure definitions from the factory. Once you know the URL for a structure definition, you can construct a model from it regardless of whether that definition came from a local file, a package, or an internet download. This abstraction simplifies your code because you do not need to know or manage where definitions are stored.

```python
from fhircraft.fhir.resources import ResourceFactory

factory = ResourceFactory(fhir_release="R4")

# Create a model from the standard FHIR Patient definition
Patient = factory.build(
    canonical_url="http://hl7.org/fhir/StructureDefinition/Patient"
)

# Create a model from a US Core profile
USCorePatient = factory.build(
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


## Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| Fhircraft cannot find a structure definition | Check that the canonical URL matches exactly. Make sure you have loaded the file, package, or enabled internet access. Verify the structure definition file is in the correct format (JSON). |
| Package download fails | Verify your internet connection. Check that the package name and version are correct. Try loading the package again after a few minutes. Visit the [:material-fire: FHIR Package Registry](https://registry.fhir.org) to confirm the package exists. |
| Loading takes a long time | Fhircraft caches downloaded packages after the first use. Subsequent loads will be much faster. Consider loading packages once at application startup rather than repeatedly. |
| Wrong version of a structure definition is used | Specify the version explicitly in the canonical URL or as a parameter. Check loaded packages with `get_loaded_packages()` to verify versions. Clear the cache if you need to reload a different version. |
| Running out of memory with many packages | Remove packages you no longer need using `remove_package()`. Load only the packages required for your current task. Clear the entire cache with `clear_package_cache()` when switching between different projects. |

## Further Resources

* [:material-fire: FHIR Package Registry](https://registry.fhir.org/) - Browse and search for available FHIR packages from the official registry

* [:material-fire: FHIR Packages Documentation](https://packages.fhir.org/) - Technical documentation for the FHIR package server and NPM package format

* [:material-fire: FHIR Structure Definitions](https://www.hl7.org/fhir/structuredefinition.html) - Detailed specification for structure definitions and profiling

* [:material-fire: FHIR Conformance Module](https://www.hl7.org/fhir/conformance-module.html) - Overview of FHIR conformance resources including profiles, extensions, and implementation guides

* [:material-fire: US Core Implementation Guide](https://www.hl7.org/fhir/us/core/) - The US national FHIR implementation guide for healthcare data exchange

* [:material-fire: International Patient Summary](https://hl7.org/fhir/uv/ips/) - Global specification for patient summary documents

* [:material-fire: FHIR Versioning](https://www.hl7.org/fhir/versioning.html) - How FHIR handles versioning of resources and conformance artifacts

* [:material-fire: Canonical References](https://www.hl7.org/fhir/references.html#canonical) - Specification for canonical URL format and versioning syntax
