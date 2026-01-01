
# Installation

This installation guide is for developers who want to add Fhircraft to their Python projects. You'll get Fhircraft running in your environment and be ready to build FHIR-compliant applications.

## Quick Install

Install Fhircraft using pip if you have Python 3.10+ installed:

```bash
pip install fhircraft
```

Or install the latest development version:

```bash
pip install git+https://github.com/luisfabib/fhircraft.git
```

## System Requirements

**Required:**

- Python 3.10 or higher
- pip package manager

**Optional but recommended:**

- Internet connection (for downloading FHIR specifications)
- Basic familiarity with [Pydantic](https://docs.pydantic.dev/latest/) (Fhircraft's foundation)

## Verify Installation

Test your installation by creating a simple FHIR model:

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# This should work without errors
Patient = construct_resource_model(
    canonical_url='http://hl7.org/fhir/StructureDefinition/Patient'
)
print("Fhircraft installed successfully!")
```


## Development installation


If you want to contribute to Fhircraft or work with the latest development version:

```bash
# Clone the repository
git clone https://github.com/luisfabib/fhircraft.git
cd fhircraft

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```
For detailed instructions on developing and contributing to Fhircraft, see the [:octicons-devices-16: Contributing Guide](../community/contributing.md).


------------