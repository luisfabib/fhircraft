# OpenAPI FHIR Extensions

The `fhircraft` package allows the conversion of API payloads to FHIR responses (and vice versa) by introducing a series of OpenAPI Specification (OAS) extensions in the schemas. These extensions enable mapping of schema properties to FHIRPaths, allowing for flexible and accurate transformation of data.

## `x-fhir-path`

Specifies the FHIRPath to which the schema property/item should be mapped. The FHIRPath must conform to one of the following categories:


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
The `%context` variable will be replace on runtime by the FHIRPath of the closest ancestor with a valid `x-fhir-path` attribute. 

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

