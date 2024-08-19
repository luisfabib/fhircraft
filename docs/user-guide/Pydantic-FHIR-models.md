
## Constructing FHIR Pydantic models 

To generate a Pydantic model representation for a FHIR resource, use the `construct_resource_model` function. This function automatically creates a model based on the structure definition of the specified resource or profile.

!!! important "Snapshot required"

    Fhircraft requires the resource's structure definition to be in `snapshot` form. Models cannot be constructed from definitions that only include a `differential`. If the `snapshot` attribute is missing, Fhircraft will raise an error.

!!! important "FHIR versions"

    Fhircraft automatically handles differences between official FHIR releases. It uses the appropriate complex types based on the FHIR version specified in the resource's structure definition, ensuring that the constructed model conforms to the correct release.

#### Via local files (recommended)

For optimal control and security, it is recommended to manage FHIR structure definitions as local files. These files should be loaded into Python and parsed into dictionary objects.

!!! note "Loading utilities"

    Fhircraft provides utility functions to load JSON or YAML files (XML currently not supported) into Python dictionaries. 
    
    ``` python 
        from fhircraft.utils import load_file
        structure_definition = load_file('fhir/patient_r4b_structuredefinition.json') 
    ``` 

The `construct_resource_model` function takes this dictionary containing the FHIR structure definition and constructs the corresponding model.

```python
from fhircraft.fhir.resources.factory import construct_resource_model
resource_model = construct_resource_model(structure_definition=structure_definition)
```

#### Via canonical URL 

A canonical URL is a globally unique identifier for FHIR conformance resources. Fhircraft includes a limited canonical URL resolver that can locate and download a FHIR resource's structure definition via HTTP.

```python
from fhircraft.fhir.resources.factory import construct_resource_model
resource_model = construct_resource_model(canonical_url=url)
```

!!! note "Release version" 

    Most canonical URLs will resolve to the latest normative release of the FHIR resource.

#### Cached models

Fhircraft caches the model created based on the structure definition of FHIR resource. Subsequent calls to `construct_resource_model` will not trigger any model constructer and will instead return the cached model. 
The cache can be reset by simply calling:
```python
from fhircraft.fhir.resources.factory import clear_cache
clear_cache()
```


## Pydantic representation

### Data types 

Fhircraft introduces a set of data types that align with the FHIR data type classification. These types serve as foundational elements for constructing Pydantic models that accurately reflect FHIR specifications. While rooted in primitive Python types, these Fhircraft data types maintain the FHIR flavor, ensuring that models are both Pythonic and compatible with other Pydantic models. The classification of data types into primitive and complex categories mirrors FHIR’s own structure, representing the fundamental components used to define FHIR resources.

#### Primitive Types

Primitive types are the most fundamental data types in FHIR, representing simple values that cannot be subdivided further. In Fhircraft, all [FHIR primitive types](https://hl7.org/fhir/datatypes.html#primitive) are represented as parametrized type aliases (`TypeAliasType`) in Python. This representation is consistent across all FHIR releases. 

All primitive types can be handled as strings and are parsed using appropriate regular expressions to ensure accurate formatting and conversion to more Pythonic types. This approach ensures that data adheres to FHIR specifications while remaining integrated with Python's type system.

| FHIR Primitive | Fhircraft Primitive  | Python types     | Regex |
|----------------|----------------------|------------------|-------|
| boolean | `Boolean` | `bool`, `str`  | `true|false` |
| integer | `Integer` | `int`, `str`  | `[0]|[-+]?[1-9][0-9]*` |
| integer64 | `Integer64` | `int`, `str`  | `[0]|[-+]?[1-9][0-9]*` |
| string | `String` | `str`  |  |
| decimal | `Decimal` | `float`, `str`  | `-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?` |
| uri | `Uri` | `str`  | `\S*` |
| url | `Url` | `str`  | |
| canonical | `Canonical` | `str`  | |
| base64Binary | `Base64Binary` | `str`  | `(\s*([0-9a-zA-Z\+\=]){4}\s*)+` |
| instant | `Instant` | `str`  | `([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\\.[0-9]+)?(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?` |
| date | `Date` | `str`  | `([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1]))?)?` |
| time | `Time` | `str`  | `([01][0-9]|2[0-3])(:[0-5][0-9](:([0-5][0-9]|60)(\\.[0-9]+)?(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?)?)?` |
| datetime | `DateTime` | `str`  | `([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1]))?)?(T([01][0-9]|2[0-3])(:[0-5][0-9](:([0-5][0-9]|60)(\\.[0-9]+)?(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?)?)?)?` |
| code | `Code` | `str`  | `[^\s]+(\s[^\s]+)*` |
| oid | `Oid` | `str`  | `urn:oid:[0-2](\.(0|[1-9][0-9]*))+` |
| id | `Id` | `str`  | `[A-Za-z0-9\-\.]{1,64}` |
| markdown | `Markdown` | `str`  | `\s*(\S|\s)*` |
| unsignedInt | `UnsignedInt` | `int`,`str`  | `[0]|([1-9][0-9]*)` |
| positiveInt | `PositiveInt` | `int`,`str`  | `\+?[1-9][0-9]*` |
| uuid | `Uuid` | `str`  | `` |

#### Complex Types

Complex types, are composed of multiple elements, each of which can be either primitive or other complex types. They are used to represent more sophisticated data structures. In Fhircraft all [FHIR complex types](https://hl7.org/fhir/datatypes.html#complex) are represented as built-in Pydantic models, which are auto-generated from their respective FHIR structure definitions. Each complex type includes all fields specified in the release-specific FHIR definitions and incorporates validators to enforce FHIR constraints.


To import a complex type for a specific FHIR release, use the `get_complex_FHIR_type` utility function. For example, to import the `CodeableConcept` complex type from the FHIR R4B release:

```python 
from fhircraft.fhir.resources.datatypes import get_complex_FHIR_type
CodeableConcept = get_complex_FHIR_type('CodeableConcept', release='R4B')
```

For a comprehensive list of Fhircraft's complex data types and additional details, please refer to the Fhircraft FHIR-release-specific documentation:

- [FHIR Release R4 complex types](/docs/reference/fhircraft/fhir/resources/datatypes/R4/complex_types/)
- [FHIR Release R4B complex types](/docs/reference/fhircraft/fhir/resources/datatypes/R4B/complex_types/)
- [FHIR Release R5 complex types](/docs/reference/fhircraft/fhir/resources/datatypes/R5/complex_types/)


### FHIR resources 

Each FHIR resource (be it a core resource, complex type, or profiled resource) is represented as a Pydantic `FHIRBaseModel` with the following structure:

```python
class <ResourceName>(FHIRBaseModel):

    <FhirElementName>: <FhirType> = Field(<defaultValue>)

    def <validationName>(self):
        <FhirValidationFcn>
```

For example, for a fictional simplified FHIR resource `mycustomresource.json`

```json title="mycustomresource.json"
{
  "resourceType": "StructureDefinition",
  "id": "myresource",
  "url": "http://example.org/fhir/StructureDefinition/mycustomresource",
  "name": "MyResource",
  "status": "draft",
  "kind": "resource",
  "abstract": false,
  "type": "DomainResource",
  "baseDefinition": "http://hl7.org/fhir/StructureDefinition/DomainResource",
  "derivation": "constraint",
  "snapshot": {
    "element": [
      {
        "id": "MyResource",
        "path": "MyResource",
        "short": "A custom resource for demonstration",
        "definition": "A custom resource with a single example element.",
        "min": 0,
        "max": "*"
      },
      {
        "id": "MyResource.exampleElement",
        "path": "MyResource.exampleElement",
        "short": "An example element",
        "definition": "An example element of type string.",
        "min": 1,
        "max": "1",
        "type": [
          {
            "code": "string"
          }
        ]
      }
    ]
  }
}
```

constructing a Pydantic FHIR model via 

```python
from fhircraft.fhir.resources.factory import construct_resource_model
from fhircraft.fhir.utils import load_file
mycustomresource_model = construct_resource_model(structure_definition=load_file('mycustomresource.json'))
```

will result in a model that could be manually specified using the following code: 

```python
from fhircraft.fhir.resources.base import FHIRBaseModel 
from fhircraft.fhir.resources.datatypes.primitives import String 

class MyResource(FHIRBaseModel):

    exampleElement: String = Field(description="An example element")
```

### FHIR elements

The following section will describe how Fhircraft represents certain aspects of FHIR resource elements. This is purely informative, as Fhircraft automatically accounts for all rules and representation described here when constructing models. 

#### Cardinality

The cardinality of an element determines the field's characteristics in the Pydantic model, such as whether it should be optional, required, or a list. Specifically:
- A minimal cardinality of 0 indicates that the field is optional.
- A maximal cardinality greater than 1 signifies that the field should be represented as a list.

The following table demonstrates how cardinality affects type annotations for an element of type `Coding`: 

| FHIR type  | Min. cardinality | Max. cardinality | Field type     |
|------------|------------------|------------------|----------------|
| `Coding`   | `1`              | `1`              | `Coding`            |
| `Coding`   | `0`              | `1`              | `Optional[Coding]`  |
| `Coding`   | `1`              | `*`              | `List[Coding]`      |
| `Coding`   | `0`              | `*`              | `Optional[List[Coding]]` |


#### Backbone elements

Backbone elements represent reusable groups of elements that can be shared across different resources or used multiple times within a resource to provide hierarchical structure. These elements are modeled using the FHIR complex type `BackboneElement`. 

In Fhircraft, backbone elements are represented as individual Pydantic models. These models include the structure and fields defined by the `BackboneElement` type. The model is then referenced by the original resource, preserving the hierarchical structure in the Pydantic model.

For example, the [`Observation.component`](https://www.hl7.org/fhir/observation-definitions.html#Observation.component) element of the `Observation` FHIR resource is a `BackboneElement`. In Fhircraft, this would be represented as follows:

```python
class ObservationComponent(BackboneElement):
    ...

class Observation(FHIRBaseModel):
    ...
    component = Optional[List[ObservationComponent]] = Field(...)
```

#### Slicing

Slicing in FHIR is a mechanism that allows for the differentiation and specialization of repeated elements within a resource. It's used when a single element or field in a resource can have multiple subtypes or variations that need to be distinguished from one another based on certain criteria. Slicing is often applied in profiles and extensions to enforce specific constraints and rules on these repeated elements.

!!! note Slicing

    Slicing is only applicable to elements that are allowed to repeat.

Each "slice" represents a distinct subset or variation of the repeated element that meets specific criteria defined by the discriminators. Slices allow the same element to be used in different ways within the same resource. 
Fhircraft represents each slice as an independent model, based on `FHIRSliceModel`, with its own fields and constraints, and representing the profiled structure of the slice. 

The sliced element can accept any value that matches any of the slices or the original element. This is achieved via an ordered `Union` of the slices and the original element type. 

For example, for an `Observation.component` element in the profile `ProfiledObservation` that has been sliced into the slices
- `'string-component'`: An `Observation.component` where `Observation.component.value` only accepts `str`
- `'integer-component'`: An `Observation.component` where `Observation.component.value` only accepts `int`    
from which Fhircraft will automatically generate the following model structure:

```python
class ObservationComponent(BackboneElement):
    ...
    valueString: str = Field(...)
    valueInteger: int = Field(...)

class StringComponent(FHIRSliceModel):
    ...
    valueString: str = Field(...)
    
class IntegerComponent(FHIRSliceModel):
    ...    
    valueInteger: str = Field(...)

class ProfiledObservation(FHIRBaseModel):
    ...
    component = Optional[List[
        Annotated[
            Union[StringComponent, IntegerComponent, ObservationComponent],
            Field(union_mode='left_to_right')
        ]
    ]] = Field(...)
```

Thanks to the use of `union_mode='left_to_right'`, when a value is assigned to a sliced element (`component`), the model will first try to instanciate the individual slice models (based on their individual validation criteria) and otherwise use the original model to store the data. For example

```python
myobs = ProfiledObservation(component=[
        {
            ...
            valueInteger=5,
        }, {
            ...
            valueString='value,
        }
    ],
    ...
)
type(myobs.component[0])
# IntegerComponent
type(myobs.component[1])
# StringComponent
```

FHIR profiles can also enforce individual cardinality rules on the slices. Fhircraft accounts for these via model validators that ensure that the correct number of slices of each type are present in the model. 

The elements in the model that contain slices can be examined by calling the `get_sliced_elements` class method on the model.

```python
>>>ProfiledObservation.get_sliced_elements()
{'component': [StringComponent, IntegerComponent]}
```


#### Type-choice elements

In FHIR, choice-type elements are named using the pattern `<elementName>[x]`, where `[x]` indicates that the element can be of multiple types. Fhircraft represents each allowed type by creating a separate field, replacing `[x]` with the specific type name. 
For example, a FHIR element `value[x]` that allows either `str` or `int` values would be represented by two Pydantic fields:  `valueString` and `valueInteger`.

Only one type can be chosen at a time for a choice-type element, meaning that you cannot assign multiple types to the same element in a single instance of a resource. Fhircraft enforces this constraint through validation, ensuring that only one of the fields representing the different types has a value.

For example, the [`Observation.effective[x]`](https://build.fhir.org/observation-definitions.html#Observation.effective_x_) element of the `Observation` FHIR resource is a type choice value that accepts a value of the one of the types `Date`, `DateTime`, `Instant`, or `Timing`. In Fhircraft, this would be represented as follows:

```python
class Observation(FHIRBaseModel):
    ...
    effectiveDateTime = Optional[DateTime] = Field(...)
    effectiveDate = Optional[Date] = Field(...)
    effectiveInstant = Optional[Instant] = Field(...)
    effectiveTiming = Optional[Timing] = Field(...)

   @model_validator(mode="after")
    def effective_type_choice_validator(self):
        ...
```

Additionally, if the chosen type for an instance is not known, you can access the value via a property  `<elementName>` (without the `[x]`) that returns the value of the type that has been set.

```python
>>> obs = Observation(effectiveDate='01/01/2000')
>>> obs.effective
'01/01/2000'
```


#### Primitive extensions

FHIR allows for extensions and IDs to be added even to primitive data types to enable the representation of additional information or to capture data that isn't part of the core specification.

When a primitive data type in FHIR has an extension (or ID), these are not applied directly to the primitive value itself. Instead, the primitive type is wrapped in a structure that allows for the inclusion of both the original value and any associated extensions or IDs. 

To account for this extensibility of primitive values, for each primitive-type field `<fieldName>` in a model , Fhircraft creates an additional field `<fieldName>_ext` of type `Element` that containts the `id` and `extension` fields for that primitive value. 

For example, for the `Observation.status` field of the `Observation` resource, Fhircraft generates a model that can be represented as
```python
class Observation(FHIRBaseModel):
    ...
    status: Code = Field(...)
    status_ext: Element = Field(...)
```
where any extensions for `status` can be added to `status_ext.extension`. 

#### Invariant constraints 

Invariant constraints are logical expressions that specify conditions that must be met for the data to be considered valid. These constraints often involve relationships between different elements within a resource and are crucial for maintaining the integrity of FHIR data, ensuring that resources adhere to expected standards.

In Fhircraft, invariant constraints are typically expressed using FHIRPath, a specialized expression language for querying and validating FHIR data. Fhircraft processes these constraints into Pydantic field or model validators that leverage its built-in FHIRPath engine to perform the necessary validation.

If a resource violates an invariant constraint, the Fhircraft model will raise a `ValidationError`, indicating that the resource does not conform to the FHIR specification. The `ValidationError` will reference invariant's identifier as well as the evaluated FHIRPath expression, for reference.

For example, if a `Quantity` resource is specified with unit `code` but without its coding `system`, the invariant `[qty-3]` will violated and the validation fails:

```python
from fhircraft.fhir.resources.datatypes.R5.complex_types import Quantity
weight = Quantity(value=10, unit='miligrams', code='mg')
# ValidationError: 1 validation error for Quantity
#    If a code for the unit is present, the system SHALL also be present. 
#    [qty-3] -> "code.empty() or system.exists()"
```

#### Fixed values & Pattern constraints 

!!! warning
    Under construction, TBA


