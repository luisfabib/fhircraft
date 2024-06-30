# OpenAPI FHIR Extensions

The `fhircraft` package allows the conversion of API payloads to FHIR responses (and vice versa) by introducing a series of OpenAPI Specification (OAS) extensions in the schemas. These extensions enable mapping of schema properties to FHIRPaths, allowing for flexible and accurate transformation of data.

## `x-fhir-resource`

The `x-fhir-resource` attribute is used to provide metadata about the FHIR resource associated with a particular schema. Esentially, a FHIR resource will be generated for each `x-fhir-resource` attribute in a schema. 

The extension is represented as an object with the following properties:

| Property           | Type  | Description                  | Default |
| ------------------ | ---- | ----------------------------- | ------- |
| `profile`          | `str` | URL of the FHIR profile to which the resource should conform.   | *required* |
| `resourceType`     | `str` | Specifies the type of FHIR resource (e.g., `Patient`, `Encounter`, `Condition`). Must match the base resource of the profile that the resource conforms to. | *required* |
| `alias`            | `str` | A FHIRPath environment variable (e.g., `%resourceA`) used to differentiate the FHIRPaths of multiple resources within the same schema. This alias facilitates the resolution of FHIRPaths when multiple resources are involved. | *unset* |

### Usage 

#### Root level scope

Include the `x-fhir-resource` attribute at the root level of the schema to define the primary FHIR resource type and profile.

``` yaml title="patient_schema.yaml" hl_lines="2 3 4"
type: object
x-fhir-resource:
    profile: http://domain.org/profile
    resourceType: Patient
properties:
    ...
``` 

In the example above, any payload conforming to the `patient_schema.yaml` can be mapped to a `Patient` FHIR resource that conforms to the `http://domain.org/profile`. 
The definition of the individual data elements is done via the `x-fhirpath` attribute (see below). 
The `x-fhir-resource` attribute also initializes the scope for the FHIRPaths of the resource it defines, and all subschemas' FHIRPaths will referer to this resource (see `aliases` for the exceptions).  


!!! warning "Profile settings"

    Ensure that the `resourceType` and `profile` are correctly specified to avoid mapping errors. Incorrect or missing values can later lead to incorrect FHIR path mappings.


#### Subschema scopes

Include the `x-fhir-resource` attribute within subschemas where applicable to specify different resource types or profiles for nested structures. 
This allows the mapping of one schema to multiple FHIR resources.

``` yaml title="patient_schema.yaml" hl_lines="9 10 11"
type: object
x-fhir-resource:
    profile: http://domain.org/profile
    resourceType: Patient
properties:
    ... 
    data:
        type: object
        x-fhir-resource:
            profile: http://domain.org/profile
            resourceType: Observation
        properties:
            ...
``` 


#### Polymorphism

For schemas with polymorphic structures (e.g., `anyOf`), the `x-fhir-resource` attribute ensures that each subschema is correctly mapped to its respective FHIR resource.


## `x-fhirpath`

The `x-fhirpath` extension specifies the FHIRPath to which the schema property/item should be mapped. The FHIRPath must conform to one of the following categories:


!!! info "FHIRPath Requirements"

    In addition to these rules, to enable the bidirectional conversion between an API payload and its FHIR resource counterpart,
     the FHIRPaths provided by `x-fhirpath` must fulfill the following requirements:

    - It must be a valid path in conformance with the [FHIRPath Normative Release v2](http://hl7.org/fhirpath/N1/).
    - Must finish in an element or function invocation that returns a FHIRPath collection.  
 
### Usage

#### Complete path
    
FHIRPaths can be complete FHIPaths starting from the a core FHIR model (e.g. a base resource, such as `Observation` or `Patient`):

``` yaml title="patient_schema.yaml" hl_lines="8 11"
x-fhir-resource:
    profile: http://domain.org/profile
    resourceType: Patient
type: object
properties:
    name:
        type: string
        x-fhirpath: Patient.name.given
    surname:
        type: string
        x-fhirpath: Patient.name.family
```


#### Contextual path

FHIRPaths can start with the `%context` variable, referring to the schema's parent element's FHIRPath. This is particularly useful for setting up the [inheritance]() of repetitive schema blocks. 
The `%context` variable will be replace on runtime by the FHIRPath of the closest ancestor with a valid `x-fhirpath` attribute. 

``` yaml title="patient_schema.yaml"  hl_lines="8 12 15"
x-fhir-resource:
    profile: http://domain.org/profile
    resourceType: Patient
type: object
properties:
    name:
        type: object
        x-fhirpath: Patient.name
        properties:
            given:
                type: string
                x-fhirpath: '%context.given'
            surname:
                type: string
                x-fhirpath: '%context.family'
```

#### Alias path

FHIRPaths can start with a `%<alias>` variable, where `<alias>` is one
of the aliases defined in an ancestor's `x-fhir-resource`. The 
`x-fhir-resource` core resource defined in `resourceType` is substituted for the `%alias` variable.
Aliases enable differentiation of FHIR resource scopes within the same schema.


``` yaml title="patient_schema.yaml"  hl_lines="9 12"
x-fhir-resource:
    profile: http://domain.org/profile
    resourceType: Patient
    alias: '%patient'
    type: object
    properties:
        name:
            type: string
            x-fhirpath: '%patient.name.given'
        surname:
            type: string
            x-fhirpath: '%patient.name.family'
```



## Reference 

### General Rules

----------------------
#### :octicons-law-24: Rule 1 <br> FHIR Resource Scopes

Every schema that should be mappable to a FHIR resource must have the `x-fhir-resource` attribute defined with `resourceType`, `profile`, and optionally `alias`.

!!! example

    Defining a schema to be mapped to a FHIR resource is as easy as adding the `x-fhir-resource` attribute.

    ``` yaml
    schemas:
        MyPatient:
            type: object
            x-fhir-resource:
                profile: http://domain.org/CustomClientProfile
                resourceType: Patient
    ```

    This example will correspond to a mapping between any payload conform to the `MyPatient` schema and a FHIR `CustomClientProfile` (`Patient`) resource. 

    | JSON Path   | FHIR Path             |
    | ----------- | --------------------- |
    | `MyPatient` | `CustomClientProfile` |

!!! example 

    Mapping to further FHIR reosurces is easily accomplished by defining new `x-fhir-resource` even within the scope of another `x-fhir-resource` attribute.

    ``` yaml
    schemas:
        MyPatient:
            type: object
            x-fhir-resource:
                profile: http://domain.org/CustomClientProfile
                resourceType: Patient
            properties:
                bloodPressure:
                    type: object
                    x-fhir-resource:
                        profile: http://domain.org/VitalSignsProfile
                        resourceType: Observation

    ```

    This example defines the mapping from the `MyPatient` to two FHIR profiled resources `CustomClientProfile` (which is scoped for all `MyPatient` properties except `bloodPressure`) and `VitalSignsProfile` (which is scoped for all subschemas of the property `bloodPressure`)

    | JSON Path       | FHIR Path                  |
    | --------------- | -------------------------- |
    | `MyPatient`     | `CustomClientProfile`      |
    | `bloodPressure` | `VitalSignsProfile`        |

----------------------

#### :octicons-law-24: Rule 2 <br> Complete FHIRPaths

FHIRPaths can be the complete paths starting from the base resource (e.g., Patient.id)

!!! example

    ``` yaml
    schemas:
        MyPatient:
            type: object
            x-fhir-resource:
                profile: http://domain.org/CustomClientProfile
                resourceType: Patient
            properties:
                birthday:
                    type: string
                    x-fhirpath: Patient.birthDate
    ```

    Which adds the mapping between the JSON path `MyPatient.gender` and the FHIR path `Patient.gender`:  
    
    | JSON Path          | FHIR Path             | 
    | -----------------  | --------------------- |
    | `MyPatient`        | `CustomClientProfile` |
    | `MyPatient.birthday` | `Patient.birthDate`   |                      


## Validation 

To ensure the proper use of these extensions, fhircraft provides a comprehensive set of validation tools. In addition to a full suite of Pydantic models representing standard OpenAPI components, the package includes custom validation tools within the [`Schema`](/reference/fhircraft/openapi/models/schema/) model. This model extends the standard JSON schema model to incorporate the `x-fhirpath` and `x-fhir-resource` attributes. It validates both the properties and structure of these extensions and checks the validity of the FHIRPath expressions in `x-fhirpath` using the built-in FHIRPath parser.