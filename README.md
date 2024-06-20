<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/luisfabib/fhircraft">
    <img src="https://github.com/luisfabib/fhircraft/blob/main/docs/static/logo.png" width="80">
  </a>

  <h3 align="center">FHIR ⨯ OpenAPI Toolkit</h3>

  <p align="center">
   A Python toolkit for FHIR (Fast Healthcare Interoperability Resources) profile construction, validation, and integration with OpenAPI specifications, allowing seamless mapping of FHIR resources to OpenAPI-conformed API responses and vice versa
    <br />
    <br />
    :construction:<i>This is an experimental package and is not ready for production. Major changes are to be expected.</i>:construction:
    <br />
    <br />
    <a href="https://github.com/luisfabib/fhircraft"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/luisfabib/fhircraft/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/luisfabib/fhircraft/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

## Features

 :star: **Dynamic FHIR profile models:** Build and manage FHIR profiles using Pydantic objects, enabling validation of profiled FHIR resources.

 :star: **OpenAPI x FHIR Validation:** Parse OpenAPI specifications with FHIR-related extensions to validate their integration with FHIR.

 :star: **Pythonic FHIRPath:** A fully pythonic normative-compliant FHIRPath lexer and parser 

 :star: **FHIR<->OpenAPI Mapping:** Map FHIR resources to OpenAPI-conformed JSON responses and vice versa.

<p align="center" width="100%">
    <img width="60%" src="https://github.com/luisfabib/fhircraft/blob/main/docs/static/terminal.gif">
</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

A valid installation of Python 3.x is required.  


### Installation

To install `fhircraft`, you can download and install the package via `pip`:

```bash
pip install fhircraft
``` 

## Usage 

### CLI commands

The package provides a command-line interface (CLI) to conviniently access the core functionality of the package. Checkout the commands available by
```
>> fhircraft --help


 Usage: fhircraft [OPTIONS] COMMAND [ARGS]...

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                           │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.    │
│ --help                        Show this message and exit.                                                         │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ convert-api-to-fhir     Convert an API response into a FHIR resource based on the its OpenAPI specification       │
│ convert-fhir-to-api     Convert FHIR resource into an API response based on the its OpenAPI specification         │
│ get-fhir-path           Get the value in FHIR resource based on FHIRpath                                          │
│ get-json-path           Get the value in API response based on JSONpath                                           │
│ validate-openapi-spec   Validate OpenAPI specification                                                            │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
``` 

### Package 

**Mapping module** (`fhircraft.mapping`)

Provides the tools to convert API responses to FHIR resources based on its OpenAPI specification using the `x-fhirpath` and `x-fhirprofile` OAS extensions.  

```python
from fhircraft.mapping import convert_response_from_api_to_fhir, convert_response_from_fhir_to_api
from fhircraft.utils import load_file
# Load JSON API response 
response = load_file(api_response_file)
# Convert response to FHIR resource based on OpenAPI specification
converted_response = convert_response_from_api_to_fhir(response, openapi_spec_file, '/endpoint', 'get', '200')
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

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Several external packages have provided the foundation and/or have inspired components of this package: 

- `fhir.resources`: All FHIR profile models and base resources are managed using their object representation for the FHIR core resources.
- `openapi-pydantic`: The Pydantic models for the extended OpenAPI specifications were derived from its models.
- `jsonpath-ng`: USed for JSONPath functionality and inspired the implementation of the FHIRPath engine.

<!-- LICENSE -->
## License

Distributed under the MIT License. See ![LICENSE](https://github.com/luisfabib/fhircraft?tab=MIT-1-ov-file#readme) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

