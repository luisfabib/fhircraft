


## Installation

If you've got Python 3.8+ and `pip` installed, installing `fhircraft` is as simply as:

```bash
pip install fhircraft
``` 

Fhircraft has a few dependencies:

- [`Pydantic`](https://docs.pydantic.dev/latest/): Pydantic is the most widely used data validation library for Python.
- [`Python FHIR Resources`](https://github.com/nazrulworld/fhir.resources): Tools and classes for all of the FHIR Resources defined in the FHIR specification, to manipulate FHIR resources in Python.
- [`Python JSONPath Next-Generation`](https://github.com/h2non/jsonpath-ng): A standard compliant implementation of JSONPath for Python.

## Optional dependencies

To install Fhircraft's Command Line Interface (CLI) a few additional dependencies are required. 

To install them along Fhircraft:
```bash
pip install fhircraft[cli]
```  

Alternatively, the dependency can be installed manually with `pip install typer`.