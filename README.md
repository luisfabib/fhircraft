<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/luisfabib/fhircraft">
    <img src="docs/assets/images/logo-banner.png" width="50%">
  </a>

  <p align="center">
    Fhircraft is a Python package that dynamically generates Pydantic FHIR (Fast Healthcare Interoperability Resources) resource models from FHIR specifications, enabling comprehensive data structuring, validation, and typing within Python. It also offers a fully functional FHIRPath engine and code generation features to facilitate integration with other systems.
    <br />
    <br />
    :construction:<i> This package is under active development. Major and/or breaking changes are to be expected in future updates.</i>:construction:
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

## Why use Fhircraft?

- **Dynamic FHIR models** – Generate Pydantic FHIR resource models dynamically from FHIR specification; get all FHIR's data structuring, validation and typing in a pythonic way.

- **Simple FHIR validation** – Perform complete parsing and validation of FHIR resources without leaving Python; avoid dealing with FHIR's often complex rules and constraints. 

- **Pydantic core** – Profit from Pydantic's validation and (de)-serialization capabilities which have made it the most widely used data validation library for Python.     

- **Code generator** – Leverage the code generation features of Fhircraft to write static Pydantic/Python code that can be integrated into other systems. 

- **Pythonic FHIRPath** – Fhircraft provides a fully functional, pythonic and compliant FHIRPath engine to easily work with FHIR resources without leaving Python.  


## Usage 

### Prerequisites

A valid installation of Python >3.8 is required.  


### Installation

To install `fhircraft`, you can download and install the package via `pip`:

```bash
pip install fhircraft
``` 

### Getting Started

This is a quick reference on how to quickly accomplish the most common tasks with Fhircraft:

- #### Constructing FHIR Pydantic models 

  To generate a Pydantic model representation for a FHIR resource, use the `construct_resource_model` function. This function automatically creates a model based on the structure definition of the specified resource or profile.
  For optimal control and security, it is recommended to manage FHIR structure definitions as local files. These files should be loaded into Python and parsed into dictionary objects.
  
  ``` python 
      from fhircraft.utils import load_file
      structure_definition = load_file('fhir/patient_r4b_structuredefinition.json') 
  ``` 

- #### Generating Pydantic FHIR models' source code

  Fhircraft allows you to generate reusable source code for Pydantic FHIR models. By using the `generate_resource_model_code` function, you can obtain the source code (as a string) that defines the FHIR Pydantic model. This can be particularly useful for integrating the model into other projects or sharing it across different applications.


  ``` python
  from fhircraft.fhir.resources import generate_resource_model_code
  source_code = generate_resource_model_code(patient_model)
  ```

  You can save the generated source code and reuse it as needed. Keep in mind that the code requires Fhircraft and its dependencies to be installed in order to function properly.

- #### Validating FHIR payloads

  The generated Pydantic models can be used to validate FHIR payloads, ensuring that they conform to the structure and constraints of the specified resource or profile.

  ``` python
  from fhicraft.utils import load_file
  data = load_file('my_fhir_patient.json')
  my_patient = patient_model.model_validate(data)
  ```

  If the input data does not conform to the expected FHIR resource or profile, the Pydantic model will raise a `ValidationError`. If no error is raised, the FHIR payload is valid and successfully loaded into the model.


- #### Model manipulation using FHIRPath

  You can specify the FHIRPath expression as a string in the standard notation to interact with the resource efficiently. This feature allows for complex queries and updates, enhancing your ability to work with FHIR data programmatically.

  ``` python
  from fhicraft.fhir.path import fhirpath
  patient_surname = fhirpath.parse('Patient.name.surname').get_value(my_patient)
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
## Support

This project has been supported by the following institutions:

- **University Hospital of Zurich**
  
  <a href="https://www.usz.ch/"><img src="docs/assets/images/usz-logo.png" width="20%"></a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See ![LICENSE](https://github.com/luisfabib/fhircraft?tab=MIT-1-ov-file) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

