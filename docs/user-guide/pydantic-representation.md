
# Pydantic Representation of FHIR

This guide explains how Fhircraft represents FHIR (Fast Healthcare Interoperability Resources) concepts using Pydantic models. You'll learn about the technical foundations that make Fhircraft's type-safe, validated FHIR implementation possible.

This is the foundational guide in the FHIR Resources section. Understanding these concepts will help you work more effectively with [Resource Models](resources-models.md) and [Resource Factory](resources-construction.md).

## Prerequisites

This guide assumes familiarity with:

- **[Basic Python](https://docs.python.org/3/tutorial/index.html)** and object-oriented programming
- **[Pydantic fundamentals](https://docs.pydantic.dev/latest/)** - Validation and data models  
- **[FHIR basics](https://hl7.org/fhir/R4/index.html)** - Understanding of FHIR as a healthcare interoperability standard

If you're new to Fhircraft, consider starting with the [FHIR Resources Overview](resources-overview.md) first.

## Technical Overview

Fhircraft provides a comprehensive Pydantic-based representation of FHIR that combines the flexibility and validation power of Pydantic with the rich data modeling capabilities of FHIR. This approach ensures type safety, automatic validation, and seamless integration with Python applications while maintaining full compatibility with FHIR specifications.

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

Primitive types represent simple values like strings, numbers, and dates. Fhircraft implements all [FHIR primitive types](https://hl7.org/fhir/datatypes.html#primitive) as Python type aliases that accept both their native Python types and string representations. The types are validated using regex patterns to ensure FHIR compliance.

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

### Complex Types

Complex types represent structured data with multiple fields, such as addresses, names, and codeable concepts. FHIRCraft provides Pydantic models for all [FHIR complex types](https://hl7.org/fhir/datatypes.html#complex) with built-in validation and type checking.

Import complex types directly from a specific FHIR release:

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

For dynamic imports across FHIR releases, use the utility function:

```python 
from fhircraft.fhir.resources.datatypes import get_complex_FHIR_type

# Import CodeableConcept from R4B release
CodeableConcept = get_complex_FHIR_type('CodeableConcept', release='R4B')
```


## FHIR Resources 

All FHIR resources inherit from `FHIRBaseModel`, providing consistent validation and behavior across all resource types:

```python
class <ResourceName>(FHIRBaseModel):

    <FhirElementName>: <FhirType> = Field(<defaultValue>)

    def <validationName>(self):
        <FhirValidationFcn>
```

Here's how Fhircraft transforms a FHIR structure definition into a Pydantic model. Given this simplified resource definition:

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

Fhircraft generates this Pydantic model:

```python
from fhircraft.fhir.resources.factory import construct_resource_model
from fhircraft.fhir.utils import load_file

# Construct the model from the structure definition
MyResource = construct_resource_model(
    structure_definition=load_file('mycustomresource.json')
)

# The generated model is equivalent to:
from fhircraft.fhir.resources.base import FHIRBaseModel 
from fhircraft.fhir.resources.datatypes.primitives import String 

class MyResource(FHIRBaseModel):
    exampleElement: String = Field(description="An example element")

# Use the model
instance = MyResource(exampleElement="Hello, FHIR!")
```

## FHIR Elements

Fhircraft handles several key FHIR concepts automatically when generating models. Understanding these concepts helps you work more effectively with the generated code.

### Cardinality

Maximal element cardinality determines whether fields are required, optional, or accept multiple values:

| Max | Python Type | Description |
|-----|-------------|-------------|
| 1   | `Optional[<type>]` | A single value |
| *   | `Optional[List[<type>]]` | A list value |

For list-type elements, the length of the list is constrained by the minimal and maximal cardinality of the element using the Pydantic  `Field(max_length=..., min_length=...)` constraints.

!!! tip "Cardinality and requiredness in FHIR"
    
    In FHIR, a minimal cardinality of `1` does not necessarily mean the element is required; it only restricts the element to a single value if present. As a result, all resource fields in Fhircraft Pydantic models are optional by default, and requiredness is enforced through FHIR invariants when applicable.


### Backbone Elements

Backbone elements are nested structures within FHIR resources. Fhircraft creates separate Pydantic models for these, maintaining the hierarchical relationships.

The [`Observation.component`](https://www.hl7.org/fhir/observation-definitions.html#Observation.component) element demonstrates this pattern:

```python
class ObservationComponent(BackboneElement):
    ...

class Observation(FHIRBaseModel):
    ...
    component = Optional[List[ObservationComponent]] = Field(...)
```

### Slicing

[Slicing](https://hl7.org/fhir/R4/profiling.html#slicing) allows FHIR profiles to define specialized variations of repeating elements. Fhircraft represents each slice as a separate model (based on `FHIRSliceModel`, with its own fields and constraints) and uses type unions to accept any valid slice.

Consider an `Observation.component` element sliced into string and integer variants:

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

Pydantic tries each slice model in order until one matches:

```python
myobs = ProfiledObservation(
    component=[
        {"valueInteger": 5},
        {"valueString": "value"}
    ],
    # ... other required fields
)

# Check assigned types
print(type(myobs.component[0]))  # <class 'IntegerComponent'>
print(type(myobs.component[1]))  # <class 'StringComponent'>

# View available slices
print(ProfiledObservation.get_sliced_elements())
# {'component': [StringComponent, IntegerComponent]}
```


### Choice Elements

Choice elements (marked with `[x]` in FHIR) can accept multiple types but only one at a time. Fhircraft creates separate fields for each allowed type.

The [`Observation.effective[x]`](https://build.fhir.org/observation-definitions.html#Observation.effective_x_) element accepts Date, DateTime, Instant, or Timing:

```python
class Observation(FHIRBaseModel):
    # Multiple type-specific fields
    effectiveDateTime: Optional[DateTime] = Field(...)
    effectiveDate: Optional[Date] = Field(...)
    effectiveInstant: Optional[Instant] = Field(...)
    effectiveTiming: Optional[Timing] = Field(...)

# Use any one type
obs = Observation(
    status="final",
    code={"text": "Blood Pressure"},
    effectiveDateTime="2023-12-25T10:30:00Z"
)

# Access through generic property
print(obs.effective)  # "2023-12-25T10:30:00Z"

# Setting another type clears the previous
obs.effectiveDate = "2023-12-25"
print(obs.effective)  # "2023-12-25"
print(obs.effectiveDateTime)  # None
```


### Primitive Extensions

FHIR allows extensions on primitive values. Fhircraft creates companion `_ext` fields for this purpose:

```python
class Observation(FHIRBaseModel):
    status: Code = Field(...)
    status_ext: Element = Field(...)  # Extensions for status

# Add extensions to primitive values
obs = Observation(
    status="final",
    status_ext={
        "extension": [{
            "url": "http://example.org/data-source",
            "valueString": "manual-entry"
        }]
    }
)
``` 

### Invariant Constraints

Fhircraft automatically validates FHIR invariants using its built-in FHIRPath engine. Violations raise clear `ValidationError` messages:

```python
from fhircraft.fhir.resources.datatypes.R5.complex_types import Quantity

# This violates FHIR invariant qty-3
try:
    weight = Quantity(value=10, unit='milligrams', code='mg')
except ValidationError as e:
    print(e)
    # ValidationError: If a code for the unit is present, 
    # the system SHALL also be present. [qty-3]

# Correct version includes system
weight = Quantity(
    value=10, 
    unit='milligrams', 
    code='mg',
    system='http://unitsofmeasure.org'
)
```

### Fixed Values and Pattern Constraints

Fhircraft enforces FHIR constraints automatically:

**Fixed Values** create enumerations with single values:
```python
# Element with fixed value "active"
instance = MyResource()  # status automatically set to "active"
print(instance.status)  # "active"
```

**Pattern Constraints** validate that values conform to required patterns:
```python
# CodeableConcept requiring specific system
concept = CodeableConcept(
    coding=[{
        "system": "http://required-system.org",
        "code": "example-code"
    }]
)  # Passes validation

# Wrong system raises ValidationError
```

## Extensions

FHIR extensions allow you to add custom data not in the base specification. Fhircraft supports all extension types through the `Extension` model.

### Standard Extensions

All FHIR elements include an `extension` field:

```python
from fhircraft.fhir.resources.datatypes.R5.complex_types import Extension, Patient

# Create extensions with different value types
nickname_ext = Extension(
    url="http://example.org/extension/nickname",
    valueString="Johnny"
)

priority_ext = Extension(
    url="http://example.org/extension/priority",
    valueCoding={
        "system": "http://example.org/priority",
        "code": "high"
    }
)

# Add to a patient
patient = Patient(
    name=[{"given": ["John"], "family": "Doe"}],
    extension=[nickname_ext, priority_ext]
)
```


## What's Next?

Now that you understand how Fhircraft represents FHIR concepts in Python, continue with:

- **[Resource Models](resources-models.md)** - Learn to create and work with FHIR resource instances
- **[Resource Factory](resources-construction.md)** - Master model construction from FHIR specifications and packages
- **[FHIR Path](fhirpath.md)** - Query and manipulate resources with FHIRPath expressions
- **[FHIR Mapper](mapper.md)** - Transform external data into validated FHIR resources

For a broader overview of all Fhircraft features, see the [User Guide overview](overview.md).

---

**Continue learning:** [Resource Models →](resources-models.md)