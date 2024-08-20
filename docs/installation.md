


## Installation

If you've got Python 3.8+ and `pip>24.1` installed, installing `fhircraft` is as simple as:

```bash
pip install fhircraft
``` 

or install it from the source via:

```bash
pip install git+https://github.com/luisfabib/fhircraft.git
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
pip install -e .[dev, docs]
```  
