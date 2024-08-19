


## Installation

If you've got Python 3.8+ and `pip>24.1` installed, installing `fhircraft` is as simply as:

```bash
pip install fhircraft
``` 

Fhircraft has a few dependencies:

- [`Pydantic`](https://docs.pydantic.dev/latest/): Pydantic is the most widely used data validation library for Python.
- [`Python JSONPath Next-Generation`](https://github.com/h2non/jsonpath-ng): A standard compliant implementation of JSONPath for Python.

You might need to update `pip` (generally recommended)

```bash
python -m pip install --upgrade pip
```

## Development installation

To install Fhircraft's development environment use 

```bash
pip install fhircraft[dev]
```  
