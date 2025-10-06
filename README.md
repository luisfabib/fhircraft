<a name="readme-top"></a>

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/luisfabib/fhircraft">
    <img src="docs/assets/images/logo-banner.png" width="50%">
  </a>

  ![PyPI - Version](https://img.shields.io/pypi/v/fhircraft?style=flat&logo=pypi&label=PyPI%20Release&labelColor=%231e293b)
  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fhircraft?style=flat-square&logo=python&labelColor=%231e293b)
  [![license](https://img.shields.io/github/license/luisfabib/fhircraft.svg)](https://github.com/luisfabib/fhircraft/blob/main/LICENSE)
  [![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)
  ![FHIR Releases](https://img.shields.io/badge/FHIR-R4_R4B_R5-blue?style=flat&logo=fireship&logoColor=red&labelColor=%231e293b)

  <p align="center">
    Transform FHIR specifications into type-safe Python models with automatic validation, profile-friendly structures, and seamless integration. Build healthcare applications with confidence using Pydantic-powered FHIR resources, comprehensive FHIRPath querying, and declarative FHIR Mapping Language data transformation.
    <br />
    <br />
    <a href="https://luisfabib.github.io/fhircraft"><strong>Explore the Documentation »</strong></a>
    <br />
    <br />
    <a href="https://github.com/luisfabib/fhircraft/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/luisfabib/fhircraft/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

> [!WARNING]  
> This package is under active development. Major and/or breaking changes are to be expected in future updates.

## ✨ Why Choose Fhircraft?

### **Type Safety & Validation**
Generate validated Pydantic models from core or profiled FHIR specifications. Catch data errors at development time with automatic constraint checking.

### **Pythonic FHIR Development**
Work with FHIR resources using familiar Python and Pydantic patterns. No complex server infrastructure or XML parsing required - just clean, maintainable Python code.

### **Multi-Release Support**
Seamlessly work with FHIR R4, R4B, and R5 specifications. Load implementation guides and custom profiles from the global FHIR package registry.

### **Integrated FHIRPath Engine**
Query and manipulate FHIR data using the standard FHIRPath language with full Python integration. No external dependencies or separate query engines needed.

### **FHIR Mapping Language**
Transform data between different structures using the official FHIR Mapping Language. Convert legacy systems and external data into validated FHIR resources.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

Install Fhircraft using pip:

```bash
pip install fhircraft
``` 

Or install the latest development version:

```bash
pip install git+https://github.com/luisfabib/fhircraft.git
```

**Verify your installation:**

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# This should work without errors
Patient = get_fhir_resource_type("Patient")
print("✓ Fhircraft installed successfully!")
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Core Features

### **Built-in FHIR Resources**
Access pre-built Pydantic models for all standard FHIR resources across multiple versions:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Get built-in Patient model for FHIR R5
Patient = get_fhir_resource_type("Patient", "R5")

# Create and validate a patient
patient = Patient(
    name=[{"given": ["Alice"], "family": "Johnson"}],
    gender="female",
    birthDate="1985-03-15"
)

print(f"Created patient: {patient.name[0].given[0]} {patient.name[0].family}")
```

### **FHIR Package Integration**
Load implementation guides and custom profiles from the FHIR package registry:

```python
from fhircraft.fhir.resources.factory import factory

# Load US Core Implementation Guide
factory.load_package("hl7.fhir.us.core", "5.0.1")

# Create US Core Patient model with enhanced validation
USCorePatient = factory.construct_resource_model(
    canonical_url="http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
)

# Use with US Core constraints
patient = USCorePatient(
    identifier=[{"system": "http://example.org/mrn", "value": "12345"}],
    name=[{"family": "Doe", "given": ["John"]}],
    gender="male"
)
```

### **FHIRPath Querying**
Query and manipulate FHIR resources using the standard FHIRPath language:

```python
# Query patient data with FHIRPath
family_names = patient.fhirpath_values("Patient.name.family")
has_phone = patient.fhirpath_exists("Patient.telecom.where(system='phone')")

# Update data using FHIRPath expressions
patient.fhirpath_update_single("Patient.gender", "female")
patient.fhirpath_update("Patient.name.given", ["Jane", "Marie"])

print(f"Updated patient: {family_names[0]}, Phone: {has_phone}")
```

### **Data Transformation**
Transform legacy data using the FHIR Mapping Language:

```python
from fhircraft.fhir.mapper import FHIRMapper

# Legacy system data
legacy_patient = {
    "firstName": "Bob",
    "lastName": "Smith", 
    "dob": "1975-06-20",
    "sex": "M"
}

# FHIR Mapping script
mapping_script = """
map 'http://example.org/legacy-to-fhir' = 'LegacyPatient'

group main(source legacy, target patient: Patient) {
    legacy.firstName -> patient.name.given;
    legacy.lastName -> patient.name.family;
    legacy.dob -> patient.birthDate;
    legacy.sex where("$this = 'M'") -> patient.gender = 'male';
    legacy.sex where("$this = 'F'") -> patient.gender = 'female';
}
"""

# Execute transformation
mapper = FHIRMapper()
targets, metadata = mapper.execute_mapping(mapping_script, legacy_patient)
fhir_patient = targets[0]

print(f"Transformed: {fhir_patient.name[0].given[0]} {fhir_patient.name[0].family}")
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/amazing_feature`)
3. Commit your Changes (`git commit -m 'Add some amazing feature'`)
4. Push to the Branch (`git push origin feature/amazing_feature`)
5. Open a Pull Request (PR)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](https://github.com/luisfabib/fhircraft?tab=MIT-1-ov-file) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

