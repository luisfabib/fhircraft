
Welcome to the Fhircraft Quickstart Guide! Here, you'll learn how to easily install Fhircraft, construct dynamic Pydantic FHIR models, validate FHIR payloads, and more. 

## Installation

If you've got Python 3.8+ and `pip` installed, installing `fhircraft` is as simply as:

```bash
pip install fhircraft
``` 

For more details, see the [Installation instructions](installation.md).

## Features

Explore some of the key features of Fhircraft and learn how to access them quickly.

---------------

### Constructing dynamic Pydantic FHIR models

Easily generate a Pydantic model representation for a FHIR resource by using the `construct_resource_model` function. This function automatically creates a model based on the structure definition of the specified resource or profile. You can provide the resource's definition either via its canonical URL or from a local file.

For instance, to generate a Pydantic model for the core FHIR `Patient` resource:

=== "Canonical URL"

    ``` python
    from fhircraft.fhir.resources.factory import construct_resource_model
    patient_model = construct_resource_model(
        canonical_url='http://hl7.org/fhir/StructureDefinition/Patient'
    )
    ```

    !!! important "HTTP Requests"

        Specifying a FHIR resource via its canonical URL requires retrieving the resource details through HTTP requests. This operation requires an active internet connection, and data will be downloaded from the third-party domain associated with the resource. Ensure that internet access is available, and be aware that data will be obtained from external sources.


=== "Local file"

    ``` python
    from fhircraft.fhir.resources.factory import construct_resource_model
    from fhicraft.utils import load_file
    patient_model = construct_resource_model(
        structure_definition=load_file('FHIR_StructureDefinition_Patient.json')
    )
    ```

Once constructed, the model leverages the full capabilities of  [Pydantic's features](https://docs.pydantic.dev/latest/) while also adhering to all FHIR structural and validation constraints, which are implemented as Pydantic validators.

--------------

### Generating Pydantic FHIR models' source code

Fhircraft allows you to generate reusable source code for Pydantic FHIR models. By using the `generate_resource_model_code` function, you can obtain the source code (as a string) that defines the FHIR Pydantic model. This can be particularly useful for integrating the model into other projects or sharing it across different applications.


``` python
from fhircraft.fhir.resources.generator import generate_resource_model_code
source_code = generate_resource_model_code(patient_model)
```

You can save the generated source code and reuse it as needed. Keep in mind that the code requires Fhircraft and its dependencies to be installed in order to function properly.

-----------

### Validating FHIR payloads

The generated Pydantic models can be used to validate FHIR payloads, ensuring that they conform to the structure and constraints of the specified resource or profile.

``` python
from fhicraft.utils import load_file
data = load_file('my_fhir_patient.json')
my_patient = patient_model.model_validate(data)
```

If the input data does not conform to the expected FHIR resource or profile, the Pydantic model will raise a `ValidationError`. If no error is raised, the FHIR payload is valid and successfully loaded into the model.

---------------

### Model manipulation using FHIRPath

Fhircraft includes a powerful FHIRPath engine that enables you to query and manipulate FHIR resources using FHIRPath expressions in a Pythonic way. You can specify the FHIRPath expression as a string in the standard notation to interact with the resource efficiently. This feature allows for complex queries and updates, enhancing your ability to work with FHIR data programmatically.

=== "Get value"

    ``` python
    from fhicraft.fhir.path import fhirpath
    patient_surname = fhirpath.parse('Patient.name.surname').get_value(my_patient)
    ```

=== "Update value"

    ``` python
    from fhicraft.fhir.path import fhirpath
    fhirpath.parse('Patient.name.surname').update(my_patient, 'John')
    ```

------------------

## Getting Help

See the [:material-link-variant: User Guide]() for more complete documentation of all of Fhircraft's features.

For more in-depth information on Pydantic, explore the extensive  [:material-book-open-variant: Pydantic documentation](https://docs.pydantic.dev/latest/).

If you need assistance with Fhircraft, you can seek help through GitHub by participating in the :material-github: GitHub Discussions or by opening an issue in the :material-github: GitHub Issues section.