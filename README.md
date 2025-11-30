<a name="readme-top"></a>

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/luisfabib/fhircraft">
    <img src="https://github.com/luisfabib/fhircraft/blob/main/docs/assets/images/logo-banner.png?raw=true" width="50%">
  </a>

  ![PyPI - Version](https://img.shields.io/pypi/v/fhircraft?style=flat&logo=pypi&label=PyPI%20Release&labelColor=%231e293b)
  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fhircraft?style=flat-square&logo=python&labelColor=%231e293b)
  [![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)
  ![FHIR Releases](https://img.shields.io/badge/FHIR-R4_R4B_R5-blue?style=flat&logo=fireship&logoColor=red&labelColor=%231e293b)

---
  <p align="center">
    <b>Pythonic healthcare interoperability</b><br>
    A comprehensive Python toolkit for working with FHIR healthcare data standards using Pydantic models from core and profiled FHIR specifications, all without external dependencies or complex server infrastructure.
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

---
> [!WARNING]  
> This package is under active development. Major and/or breaking changes are to be expected in future updates.

## Key Features

* Automatic validation of FHIR resources using Pydantic models generated directly from FHIR structure definitions. Catch schema violations and constraint failures without any dedicated servers.

* Work with FHIR data as standard Python objects. No XML parsing, no external FHIR servers required. Access and modify healthcare data using familiar Python syntax and patterns.

* Supports FHIR R4, R4B, and R5 out of the box. Load implementation guides and custom profiles directly from the FHIR package registry to work with specialized healthcare data models.

* Execute FHIRPath expressions directly on Python objects. Query complex nested healthcare data structures using the standard FHIR query language without additional tooling.

* Implement healthcare data transformations using the official FHIR Mapping Language. Convert between different data formats while maintaining semantic integrity and validation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Quick Start

### Prerequisites

- Python 3.10 or higher

### Installation

Install Fhircraft using your package manager of choice. To download the latest release using the `pip` manager:

```bash
pip install fhircraft
``` 
or install the latest development version:

```bash
pip install git+https://github.com/luisfabib/fhircraft.git
```

To verify your installation:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# This should work without errors
Patient = get_fhir_resource_type("Patient")
print("✓ Fhircraft installed successfully!")
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Demo

### **Built-in FHIR Resources**
Work with pre-generated Pydantic models for all standard FHIR resources. Each model includes full validation rules from the FHIR specification:

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
Extend base FHIR models with implementation guide profiles loaded directly from the official FHIR package registry:

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
Execute FHIRPath expressions directly on FHIR resource instances to extract, filter, and validate healthcare data:

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
Convert external data sources into valid FHIR resources using declarative mapping scripts:

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

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Checkout the [Contributing Guide](https://luisfabib.github.io/fhircraft/community/contributing/) for more details. Thanks to all our contributors!


<img src="https://contrib.rocks/image?repo=luisfabib/fhircraft">

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

This project is distributed under the MIT License. See [LICENSE](https://github.com/luisfabib/fhircraft?tab=MIT-1-ov-file) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

