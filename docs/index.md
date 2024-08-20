# Welcome to

<!-- PROJECT LOGO -->
<img src="assets/images/logo-banner.png" width="75%">

[![CI](https://github.com/luisfabib/fhircraft/actions/workflows/CI.yaml/badge.svg?branch=main&event=push)](https://github.com/luisfabib/fhircraft/actions/workflows/CI.yaml)
[![releases](https://img.shields.io/github/v/release/luisfabib/fhircraft)](https://github.com/luisfabib/fhircraft)
[![versions](https://img.shields.io/pypi/pyversions/fhircraft.svg)](https://github.com/luisfabib/fhircraft)
[![license](https://img.shields.io/github/license/luisfabib/fhircraft.svg)](https://github.com/luisfabib/fhircraft/blob/main/LICENSE)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)
![FHIR Releases](https://img.shields.io/badge/FHIR-R4_R4B_R5-blue?style=flat&logo=fireship&logoColor=red&labelColor=%231e293b)

Fhircraft is a Python package that dynamically generates Pydantic FHIR (Fast Healthcare Interoperability Resources) resource models from FHIR specifications, enabling comprehensive data structuring, validation, and typing within Python. It also offers a fully functional FHIRPath engine and code generation features to facilitate integration with other systems.

!!! important "Active development"

    This package is under active development. Major and/or breaking changes are to be expected in future updates.


## Why use Fhircraft?

- **Dynamic FHIR models** – Generate Pydantic FHIR resource models dynamically from FHIR specification; get all FHIR's data structuring, validation and typing in a pythonic way.

- **Simple FHIR validation** – Perform complete parsing and validation of FHIR resources without leaving Python; avoid dealing with FHIR's often complex rules and constraints. 

- **Pydantic core** – Profit from Pydantic's validation and (de)-serialization capabilities which have made it the most widely used data validation library for Python.     

- **Code generator** – Leverage the code generation features of Fhircraft to write static Pydantic/Python code that can be integrated into other systems. 

- **Pythonic FHIRPath** – Fhircraft provides a fully functional, pythonic and compliant FHIRPath engine to easily work with FHIR resources without leaving Python.  
