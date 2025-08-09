
# Installation 

These instructions will walk you through the steps to quickly install Fhircraft, outline its requirements, and provide instructions for setting up a development environment.

## Quick Installation

If you've got Python 3.10+ and `pip>24.1` installed, installing `fhircraft` is as simple as:

```bash
pip install fhircraft
``` 

or install it from the source via:

```bash
pip install git+https://github.com/luisfabib/fhircraft.git
```

## Requirements

- Python 3.10 or newer
- `pip` package manager

Optional (for advanced features):

- Internet access (to fetch FHIR StructureDefinitions by canonical URL)
- Local FHIR StructureDefinition files (for offline model construction)
- Familiarity with [:simple-pydantic: Pydantic](https://docs.pydantic.dev/latest/) is helpful but not required

### Dependencies

Fhircraft has the following core dependencies:

- **Pydantic** (≥2.7) - For data validation and serialization
- **requests** - For fetching FHIR structure definitions via HTTP
- **ply** (≥3.11) - For FHIRPath parsing
- **jsonschema** (>4) - For JSON schema validation
- **pyyaml** (6.0.1) - For YAML file support
- **jsonpath-ng** (>1) - For JSON path operations
- **jinja2** (≥3.1) - For code generation templates

You might need to update `pip` (generally recommended)

```bash
python -m pip install --upgrade pip
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