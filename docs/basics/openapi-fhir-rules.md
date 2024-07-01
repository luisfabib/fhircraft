# OpenAPI FHIR Extensions

The `fhircraft` package allows the conversion of API payloads to FHIR responses (and vice versa) by introducing a series of OpenAPI Specification (OAS) extensions in the schemas. These extensions enable mapping of schema properties to FHIRPaths, allowing for flexible and accurate transformation of data.

!!! warning

    This framework is in an experimental phase and is bound to heavily change in the short-term future. 

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

The `x-fhirpath` extension specifies the FHIRPath to which the schema property/item should be mapped. 
See the [reference guidelines](#reference) for detailed usage rules and examples.

!!! info "FHIRPath Requirements"

    In addition to these rules, to enable the bidirectional conversion between an API payload and its FHIR resource counterpart,
     the FHIRPaths provided by `x-fhirpath` must fulfill the following requirements:

    - It must be a valid path in conformance with the [FHIRPath Normative Release v2](http://hl7.org/fhirpath/N1/).
    - Must finish in an element or function invocation that returns a FHIRPath collection.  
 
### Basics

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

The root of the FHIRPath and the `resourceType` of the `x-fhir-resource` must match, otherwise an error will be raised.  

### Context inheritance

FHIRPaths can start with the `%context` variable, referring to the schema's parent element's FHIRPath. The `%context` variable will be replaced on runtime by the FHIRPath of the closest ancestor with a valid `x-fhirpath` attribute. 

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

This is particularly useful for setting up the inheritance of repetitive schema blocks. For example, in a case where multiple ranges of values are used and represented by a `MyRange` schema. We will want to map this schema to the `Range` type of FHIR. To keep the mapping DRY we can use the `%context` variable to define the FHIR mapping of this sub-schema without having to bother knowing the larger structure within which the `MyRange` schema will be used:

``` yaml
schemas: 
    MyRange:
        type: object
        properties:
            upperBound: 
                type: number
                x-fhirpath: '%context.high.value'
            lowerBound: 
                type: number
                x-fhirpath: '%context.low.value'
```

We can now use the `MyRange` schema repetetively to map to FHIR elements of the type `Range`. For example, a case where we want to map two value ranges `bloodPressure` and `hearRate` to two `Observation.component` slices:

``` yaml
schemas: 
    MyRange:
        ...
    MyObservation:
        x-fhir-resource:
            profile: http://domain.org/profile
            resourceType: Observation
        type: object
        properties:
            bloodPressure: 
                $ref: '#/schemas/MyRange'
                x-fhirpath: 'Observation.component[0].valueRange'
            heartRate: 
                $ref: '#/schemas/MyRange'
                x-fhirpath: 'Observation.component[1].valueRange'
```

While the `x-fhirpath` definitions of the `MyRange` schema are the same, due the their parent `x-fhirpath` attributes in the `bloodPressure` and `hearRate` properties being different, the use of the `%context` variable will result in the following mapping:

| JSON Path                                | FHIR Path                                         |
| ---------------------------------------- | ------------------------------------------------- |
| `bloodPressure.upperBound` | `Observation.component[0].valueRange.upper.value` | 
| `bloodPressure.lowerBound` | `Observation.component[0].valueRange.lower.value` |
| `heartRate.upperBound`     | `Observation.component[1].valueRange.upper.value` |
| `heartRate.lowerBound`     | `Observation.component[1].valueRange.lower.value` |

!!! tip
    This approach can help reduce the complexity of the FHIRPaths used in the mapping definitions and can be used to enforce mapping structure in parent schemas. 



## Validation 

To ensure the proper use of these extensions, `fhircraft` provides a comprehensive set of validation tools. In addition to a full suite of Pydantic models representing standard OpenAPI components, the package includes custom validation tools within the [`Schema`](/reference/fhircraft/openapi/models/schema/) model. This model extends the standard JSON schema model to incorporate the `x-fhirpath` and `x-fhir-resource` attributes. It validates both the properties and structure of these extensions and checks the validity of the FHIRPath expressions in `x-fhirpath` using the built-in FHIRPath parser.

## Reference 

### 1. General Rules

----------------------
#### :octicons-law-24: 1.1 FHIR Resource Scopes

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

#### :octicons-law-24: 1.2 FHIRPath specification

FHIRPaths can be the complete paths starting from the base resource (e.g., `Patient.id`)

!!! example
    The most straightforward way to introdue a mapping of a schema property to a FHIR resource element is by using the full path:  

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
    
    | JSON Path            | FHIR Path             | 
    | -------------------  | --------------------- |
    | `MyPatient`          | `CustomClientProfile` |
    | `MyPatient.birthday` | `Patient.birthDate`   |                      


----------------------

#### :octicons-law-24: 1.3 Context substitution

FHIRPaths can start with the `%context` variable, in which 
case the schema's parent element's FHIRPath is used to 
substitute the `%context` variable.

!!! example

    The `%context` variable always referes to the closest ancestors FHIRPath:  

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
                    x-fhirpath: '%context.birthDate'
    ```

    Which adds the mapping between the JSON path `MyPatient.gender` and the FHIR path `Patient.gender`:  
    
    | JSON Path            | FHIR Path             | 
    | -------------------  | --------------------- |
    | `MyPatient`          | `CustomClientProfile` |
    | `MyPatient.birthday` | `Patient.birthDate`   |                      


!!! example
    
    The `%context` variable always referes to the closest ancestors FHIRPath:  

    ``` yaml
    schemas:
        MyPatient:
            type: object
            x-fhir-resource:
                profile: http://domain.org/CustomClientProfile
                resourceType: Patient
            properties:
                name:
                    type: object
                    x-fhirpath: '%context.name'
                    properties:
                        surname:
                            type: string
                            x-fhirpath: '%context.family'
    ```

    Which adds the mapping between the JSON path `MyPatient.name.surname` and the FHIR path `Patient.name.family`:  
    
    | JSON Path                | FHIR Path               | 
    | -------------------      | ---------------------   |
    | `MyPatient`              | `CustomClientProfile`   |
    | `MyPatient.name.surname` | `Patient.name.family`   |                      



----------------------

#### :octicons-law-24: 1.4  Aliasing resources

FHIRPaths can start with an `%<alias>` variable, where `<alias>` is one
of the aliases defined in an ancestor's `x-fhir-resource`. The 
corresponding `resourceType` is substituted for the `%<alias>` variable.
Aliases must be unique and differentiate FHIR resource scopes within the same schema.

!!! example
    
    We can alias the `CustomClientProfile` as `%patient` to directly refer to this resource in its child properties.

    ``` yaml
    schemas:
        MyPatient:
            type: object
            x-fhir-resource:
                profile: http://domain.org/CustomClientProfile
                resourceType: Patient
                alias: '%patient'
            properties:
                birthday:
                    type: string
                    x-fhirpath: '%patient.birthDate'
    ```

    Which adds the mapping between the JSON path `MyPatient.gender` and the FHIR path `Patient.gender`:  
    
    | JSON Path            | FHIR Path             | 
    | -------------------  | --------------------- |
    | `MyPatient`          | `CustomClientProfile` |
    | `MyPatient.birthday` | `Patient.birthDate`   |                     



### 2. Inheritance Rules

----------------------
#### :octicons-law-24: 2.1 Scope inheritance

When a schema inherits from another schema using `allOf`, the `x-fhir-resource`
and `x-fhir-path` extensions from the parent schema are inherited by the child
schema unless explicitly overridden.

!!! example
    
    A simple schema inheritance example using `allOf`:

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
                    x-fhirpath: Patient.birthDate'
        MyOtherPatient:
            allOf:
                - $ref: '#/schemas/MyPatient'
                - properties:
                    status:
                        type: string
                        x-fhirpath: Patient.status'

    ```

    This results in the `MyPatient` and `MyOtherPatient` schemas being mapped to the same FHIR profile `CustomClientProfile`, but with different mapped properties:  
    
    | JSON Path                 | FHIR Path             | 
    | ------------------------- | --------------------- |
    | `MyPatient`               | `CustomClientProfile` |
    | `MyPatient.birthday`      | `Patient.birthDate`   | 
    | `MyOtherPatient`          | `CustomClientProfile` |
    | `MyOtherPatient.birthday` | `Patient.birthDate`   | 
    | `MyOtherPatient.status`   | `Patient.status`      |                       



----------------------
#### :octicons-law-24: 2.2 Overriding inherited FHIRPaths

If a property in the child schema has an `x-fhir-path` that conflicts
with the parent schema, the child schema's `x-fhir-path` takes precedence.  
An inherited `x-fhir-path` can be removed by setting the attribute in the inherited schema's property to `null`.

!!! example
    
    In this example, we have a `MyOtherPatient` schema that only has the birth year of a patient, so
    we need to remove the `x-fhirpath` attribute from the inherited `birthDay` property and set it to the new `birthYear` property:

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
                    x-fhirpath: Patient.birthDate'
        MyOtherPatient:
            allOf:
                - $ref: '#/schemas/MyPatient'
                - properties:
                    birthDay:
                        x-fhirpath: null
                    birthYear:
                        type: string
                        x-fhirpath: Patient.birthDate'

    ```

    This results in the following mapping:  
    
    | JSON Path                  | FHIR Path             | 
    | -------------------------  | --------------------- |
    | `MyPatient`                | `CustomClientProfile` |
    | `MyPatient.birthday`       | `Patient.birthDate`   | 
    | `MyOtherPatient`           | `CustomClientProfile` |
    | `MyOtherPatient.birthYear` | `Patient.birthDate`  |                 


----------------------
#### :octicons-law-24: 2.3 Overriding inherited resource scopes

A child schema can override the `x-fhir-resource` extension to change
the `resourceType` or `profile` attributes (for `alias` see below).

!!! example
    
    This example shows how `x-fhir-resource` attributes can be overriden:

    ``` yaml
    schemas:
        MyPatient:
            type: object
            x-fhir-resource:
                profile: http://domain.org/CustomClientProfile
                resourceType: Patient
                alias: '%baseAlias'
            properties:
                birthday:
                    type: string
                    x-fhirpath: '%baseAlias.birthDate'
        MyOtherPatient:
            allOf:
                - $ref: '#/schemas/MyPatient'
                - x-fhir-resource:
                    profile:  http://domain.org/NewCustomClientProfile
    ```

    This results in the mapping of the `MyOtherPatient` schema to a new profile `NewCustomClientProfile`:  
    
    | JSON Path                  | FHIR Path                | 
    | -------------------------  | ---------------------    |
    | `MyPatient`                | `CustomClientProfile`    |
    | `MyPatient.birthday`       | `Patient.birthDate`      |   
    | `MyOtherPatient`           | `NewCustomClientProfile` |
    | `MyOtherPatient.birthday`  | `Patient.birthDate`      |                  


----------------------
#### :octicons-law-24: 2.4 Alias inheritance

A child schema inherits the aliases of the parent schema even if new
aliases are introduced by the child. The parent aliases can still be used to refer the the resource within its scope.

!!! example
    
    This example shows how `x-fhir-resource` aliases are inherited and used when overriden:

    ``` yaml
    schemas:
        MyPatient:
            type: object
            x-fhir-resource:
                profile: http://domain.org/CustomClientProfile
                resourceType: Patient
                alias: '%baseAlias'
            properties:
                birthday:
                    type: string
                    x-fhirpath: '%baseAlias.birthDate'
        MyOtherPatient:
            allOf:
                - $ref: '#/schemas/MyPatient'
                - x-fhir-resource:
                    alias: '%newAlias'
                - properties:
                    name:
                        type: object
                        x-fhirpath: '%baseAlias.name'
                    status:
                        type: string
                        x-fhirpath: '%newAlias.status'
    ```

    This results in the following mapping for the `MyOtherPatient` schema:  
    
    | JSON Path                  | FHIR Path             | 
    | -------------------------  | --------------------- |
    | `MyOtherPatient`           | `CustomClientProfile` |
    | `MyOtherPatient.birthday`  | `Patient.birthDate`   |   
    | `MyOtherPatient.name`      | `Patient.name`        |          
    | `MyOtherPatient.status`    | `Patient.status`      |                  
