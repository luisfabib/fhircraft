# FHIRcraft - FHIR x OpenAPI Toolset 

`fhircraft` is a Python toolkit for FHIR (Fast Healthcare Interoperability Resources) profile construction, validation, and integration with OpenAPI specifications. It allows for seamless mapping of FHIR resources to OpenAPI-conformed API responses and vice versa.

## Features

- **Pydantic FHIR Profile models:** Build and manage FHIR profiles using Pydantic objects, enabling seamless validation of profiled FHIR resources.
- **OpenAPI x FHIR Validation:** Parse OpenAPI specifications with FHIR-related extensions to validate their integration with FHIR.
- **Pythonic FHIRPath:** A fully pythonic normative-compliant FHIRPath lexer and parser 
- **FHIR<->OpenAPI Mapping:** Map FHIR resources to OpenAPI-conformed JSON responses and vice versa.

![](https://github.com/luisfabib/fhircraft/blob/main/docs/static/terminal.gif)

## Installation

To install fhircraft, use pip:

```bash
pip install fhircraft
``` 

## Usage 

TODO 


## Contributing

We welcome contributions! Please read our Contributing Guidelines (TODO) before submitting a pull request.

## Acknowledgements

- `fhir.resources`: All FHIR profile models and base resources are managed using their object representation for the FHIR core resources.
- `openapi-pydantic`: The Pydantic models for the extended OpenAPI specifications were derived from its models.
- `jsonpath-ng`: USed for JSONPath functionality and inspired the implementation of the FHIRPath engine.

## License

This project is licensed under the MIT License. See the ![LICENSE](https://github.com/luisfabib/fhircraft?tab=MIT-1-ov-file#readme) for details.
