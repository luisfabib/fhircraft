
# Pydantic Representation of FHIR

Fhircraft provides a comprehensive Pydantic-based representation of FHIR (Fast Healthcare Interoperability Resources) that combines the flexibility and validation power of Pydantic with the rich data modeling capabilities of FHIR. This approach ensures type safety, automatic validation, and seamless integration with Python applications while maintaining full compatibility with FHIR specifications.

## Overview

This guide covers how Fhircraft represents FHIR concepts using Pydantic models, including:

- **Data Types**: Primitive and complex FHIR types as Python type aliases and Pydantic models
- **FHIR Resources**: Complete resource models with validation and constraints
- **FHIR Elements**: Detailed representation of cardinality, backbone elements, slicing, and choice types
- **Extensions**: Support for standard and custom FHIR extensions
- **Validation**: Invariant constraints, pattern matching, and fixed values
- **Profiling**: Custom resources and profiles for specialized use cases

## Data types 

Fhircraft introduces a set of data types that align with the FHIR data type classification. These types serve as foundational elements for constructing Pydantic models that accurately reflect FHIR specifications. While rooted in primitive Python types, these Fhircraft data types maintain the FHIR flavor, ensuring that models are both Pythonic and compatible with other Pydantic models. The classification of data types into primitive and complex categories mirrors FHIR’s own structure, representing the fundamental components used to define FHIR resources.

#### Primitive Types

Primitive types are the most fundamental data types in FHIR, representing simple values that cannot be subdivided further. In Fhircraft, all [FHIR primitive types](https://hl7.org/fhir/datatypes.html#primitive) are represented as parametrized type aliases (`TypeAliasType`) in Python. This representation is consistent across all FHIR releases. 

All primitive types can be handled as strings and are parsed using appropriate regular expressions to ensure accurate formatting and conversion to more Pythonic types. This approach ensures that data adheres to FHIR specifications while remaining integrated with Python's type system.

| FHIR Primitive | Fhircraft Primitive  | Python types     | Regex |
|----------------|----------------------|------------------|-------|
| boolean | `Boolean` | `bool`, `str`  | `true|false` |
| integer | `Integer` | `int`, `str`  | `[0]|[-+]?[1-9][0-9]*` |
| integer64 | `Integer64` | `int`, `str`  | `[0]|[-+]?[1-9][0-9]*` |
| string | `String` | `str`  | `.*` |
| decimal | `Decimal` | `float`, `str`  | `-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?` |
| uri | `Uri` | `str`  | `\S*` |
| url | `Url` | `str`  | `\S*` |
| canonical | `Canonical` | `str`  | `\S*` |
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
| uuid | `Uuid` | `str`  | `[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}` |

#### Complex Types

Complex types, are composed of multiple elements, each of which can be either primitive or other complex types. They are used to represent more sophisticated data structures. In Fhircraft all [FHIR complex types](https://hl7.org/fhir/datatypes.html#complex) are represented as built-in Pydantic models, which are auto-generated from their respective FHIR structure definitions. Each complex type includes all fields specified in the release-specific FHIR definitions and incorporates validators to enforce FHIR constraints.

You can import complex types directly for a specific FHIR release:

```python
# Direct import for R5
from fhircraft.fhir.resources.datatypes.R5.complex_types import CodeableConcept, Quantity, Period

# Create instances with validation
concept = CodeableConcept(
    coding=[{
        "system": "http://loinc.org",
        "code": "29463-7",
        "display": "Body weight"
    }],
    text="Body weight"
)
```

Alternatively, to import a complex type for a specific FHIR release dynamically, use the `get_complex_FHIR_type` utility function. For example, to import the `CodeableConcept` complex type from the FHIR R4B release:

```python 
from fhircraft.fhir.resources.datatypes import get_complex_FHIR_type
CodeableConcept = get_complex_FHIR_type('CodeableConcept', release='R4B')
```

For a comprehensive list of Fhircraft's complex data types and additional details, please refer to the Fhircraft FHIR-release-specific documentation:

- [FHIR Release R4 complex types](../reference/fhircraft/fhir/resources/datatypes/R4/complex_types.md)
- [FHIR Release R4B complex types](../reference/fhircraft/fhir/resources/datatypes/R4B/complex_types.md)
- [FHIR Release R5 complex types](../reference/fhircraft/fhir/resources/datatypes/R5/complex_types.md)


## FHIR resources 

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

## FHIR elements

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

For example, for an `Observation.component` element in the profile `ProfiledObservation` that has been sliced into the slices:

- `'string-component'`: An `Observation.component` where `Observation.component.value[x]` only accepts `string` values
- `'integer-component'`: An `Observation.component` where `Observation.component.value[x]` only accepts `integer` values    

Fhircraft will automatically generate the following model structure:

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
    # ... other required fields
)

# Check the actual types assigned
print(type(myobs.component[0]))  # <class 'IntegerComponent'>
print(type(myobs.component[1]))  # <class 'StringComponent'>
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
# Create an observation with effective date
obs = Observation(
    status="final",
    code={"text": "Blood Pressure"},
    effectiveDateTime="2023-12-25T10:30:00Z"
)

# Access the value through the base property
print(obs.effective)  # "2023-12-25T10:30:00Z"

# Only one type can be set at a time
obs.effectiveDate = "2023-12-25"  # This will clear effectiveDateTime
print(obs.effective)  # "2023-12-25"
print(obs.effectiveDateTime)  # None
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

If a resource violates an invariant constraint, the Fhircraft model will raise a [`ValidationError`](https://docs.pydantic.dev/latest/api/pydantic_core/#pydantic_core.ValidationError), indicating that the resource does not conform to the FHIR specification. The [`ValidationError`](https://docs.pydantic.dev/latest/api/pydantic_core/#pydantic_core.ValidationError) will reference invariant's identifier as well as the evaluated FHIRPath expression, for reference.

For example, if a `Quantity` resource is specified with unit `code` but without its coding `system`, the invariant `[qty-3]` will violated and the validation fails:

```python
from fhircraft.fhir.resources.datatypes.R5.complex_types import Quantity
weight = Quantity(value=10, unit='miligrams', code='mg')
# ValidationError: 1 validation error for Quantity
#    If a code for the unit is present, the system SHALL also be present. 
#    [qty-3] -> "code.empty() or system.exists()"
```

#### Fixed values & Pattern constraints 

In FHIR, elements can be constrained using fixed values or pattern constraints to enforce specific requirements on the data:

- **Fixed values** specify that an element must have exactly the specified value
- **Pattern constraints** specify that an element must conform to a specific pattern or structure

Fhircraft automatically processes both types of constraints when constructing Pydantic models from FHIR structure definitions.

##### Fixed Values

When a FHIR element has a fixed value constraint, Fhircraft creates an enumeration with a single value and sets it as both the field type and default value. This ensures that the field can only accept the predefined value.

```python
# Example: Element with fixed string value
from fhircraft.fhir.resources.factory import construct_resource_model

# Assuming a structure definition with fixedString: "active"
MyResource = construct_resource_model(structure_definition=structure_def)

# The resulting model will have:
# status: StatusFixedValue = StatusFixedValue.fixedValue
# where StatusFixedValue is an Enum with only one value: "active"

instance = MyResource()
print(instance.status)  # "active" - automatically set
```

##### Pattern Constraints

Pattern constraints require that an element's value conforms to a specified pattern while allowing additional properties or values. Fhircraft implements pattern validation using field validators that check whether the provided value fulfills the pattern requirements.

```python
# Example: CodeableConcept with pattern constraint
from fhircraft.fhir.resources.datatypes.R5.complex_types import CodeableConcept

# If a profile requires a CodeableConcept to have a specific coding system
# The generated model will include a pattern validator
instance = CodeableConcept(
    coding=[{
        "system": "http://required-system.org",
        "code": "example-code"
    }]
)
# This will pass validation if it matches the pattern

# Attempting to use a different system may fail validation
# depending on the specific pattern requirements
```

The pattern validation works by:

1. **Extracting the pattern** from the FHIR structure definition during model construction
2. **Creating a field validator** that compares the element value against the pattern
3. **Merging dictionaries** to ensure the provided value contains all required pattern properties
4. **Raising validation errors** if the pattern is not satisfied

For complex types, pattern validation ensures that all specified fields in the pattern are present with the correct values, while allowing additional fields that are not part of the pattern constraint.

```python
# Pattern validation error example
try:
    instance = CodeableConcept(
        coding=[{
            "system": "http://wrong-system.org",  # Doesn't match pattern
            "code": "example-code"
        }]
    )
except ValidationError as e:
    print(f"Pattern validation failed: {e}")
    # Output shows which pattern was expected
```

Both fixed values and pattern constraints are processed automatically by Fhircraft's `ResourceFactory` during model construction, ensuring that your Pydantic models enforce the same constraints defined in the original FHIR specification or profile.

#### Extensions

Extensions in FHIR provide a mechanism to add additional data elements that are not part of the base resource definition. Fhircraft fully supports FHIR extensions through its `Extension` complex type and the `Element` base model.

##### Standard Extensions

Every FHIR element in Fhircraft inherits from the `Element` base model, which includes an `extension` field that can contain a list of `Extension` objects:

```python
from fhircraft.fhir.resources.datatypes.R5.complex_types import Extension, Patient

# Create an extension
my_extension = Extension(
    url="http://example.org/fhir/StructureDefinition/patient-nickname",
    valueString="Johnny"
)

# Add it to a patient
patient = Patient(
    name=[{
        "given": ["John"],
        "family": "Doe"
    }],
    extension=[my_extension]
)
```

##### Modifier Extensions

Some elements also support modifier extensions, which can change the meaning or interpretation of the element. These are represented through the `modifierExtension` field in backbone elements:

```python
from fhircraft.fhir.resources.datatypes.R5.complex_types import Extension

# Modifier extension (changes the meaning of the parent element)
modifier_ext = Extension(
    url="http://example.org/fhir/StructureDefinition/data-absent-reason",
    valueCode="unknown"
)

# Add to a backbone element that supports modifier extensions
observation_component = ObservationComponent(
    code={"text": "Blood Pressure"},
    modifierExtension=[modifier_ext]
)
```

##### Extension Value Types

Extensions use a choice-type element `value[x]` that can accept various data types. Fhircraft represents this through multiple `value{Type}` fields:

```python
# Different value types for extensions
string_ext = Extension(
    url="http://example.org/extension/note",
    valueString="Patient prefers morning appointments"
)

boolean_ext = Extension(
    url="http://example.org/extension/high-risk",
    valueBoolean=True
)

coding_ext = Extension(
    url="http://example.org/extension/priority",
    valueCoding={
        "system": "http://example.org/priority",
        "code": "high",
        "display": "High Priority"
    }
)
```

##### Extension Validation

Fhircraft automatically validates extensions according to FHIR rules:

- An extension must have either a value or nested extensions, but not both
- The URL field is required and identifies the meaning of the extension
- Only one value type can be specified per extension

```python
# This will raise a validation error - both value and nested extension
try:
    invalid_ext = Extension(
        url="http://example.org/extension/invalid",
        valueString="some value",
        extension=[Extension(url="http://nested", valueString="nested")]
    )
except ValidationError as e:
    print("Extension validation failed:", e)
```

The extension mechanism allows FHIR resources to be extended while maintaining type safety and validation through Fhircraft's Pydantic-based approach.

#### Profiling and Custom Resources

Fhircraft supports the creation of custom FHIR resources and profiles through its flexible resource factory system. This allows you to define specialized versions of standard FHIR resources or create entirely new resource types.

##### Creating Custom Profiles

You can create custom profiles by providing a FHIR structure definition that constrains or extends an existing resource:

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# Load a custom profile structure definition
profile_structure = {
    "resourceType": "StructureDefinition",
    "url": "http://example.org/fhir/StructureDefinition/MyPatientProfile",
    "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
    "derivation": "constraint",
    # ... additional constraints
}

# Construct the profiled model
MyPatientProfile = construct_resource_model(structure_definition=profile_structure)

# Use the profiled model with enhanced validation
patient = MyPatientProfile(
    # Patient data that must conform to the profile constraints
)
```

##### Working with Multiple FHIR Releases

Fhircraft supports multiple FHIR releases (R4, R4B, R5) simultaneously. You can specify which release to use when constructing models:

```python
from fhircraft.fhir.resources.factory import construct_resource_model

# Construct a model for a specific FHIR release
PatientR4 = construct_resource_model(
    structure_definition=structure_def,
    fhir_release="R4"
)

PatientR5 = construct_resource_model(
    structure_definition=structure_def,
    fhir_release="R5"
)
```

This flexibility ensures that your applications can work with different FHIR versions and gradually migrate between releases as needed.



