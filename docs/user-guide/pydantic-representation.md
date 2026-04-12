# Pydantic Representation of FHIR

This guide explains how Fhircraft transforms FHIR (Fast Healthcare Interoperability Resources) concepts into Python objects using Pydantic models. You'll learn about the technical foundations that make Fhircraft's type-safe, validated FHIR implementation possible, and how to work effectively with the resulting object representations.

This is the foundational guide in the FHIR Resources section. Understanding these concepts will help you work more effectively with [Resource Models](resources-models.md) and [Resource Factory](resources-construction.md).

### Foundation

Fhircraft uses Pydantic v2 to create strongly-typed Python representations of FHIR resources. Each FHIR resource becomes a Python class that inherits from `FHIRBaseModel`, which extends Pydantic's `BaseModel` with healthcare-specific capabilities, which provide

- **FHIR validation** using embedded invariant rules
- **Parent tracking** for maintaining object relationships  
- **FHIRPath integration** for querying and manipulation
- **Polymorphic serialization** for handling inheritance
- **XML/JSON serialization** with FHIR-compliant formatting

```python
from pydantic import Field, model_validator
from typing import Optional, List
from fhircraft.fhir.resources.base import FHIRBaseModel
from fhircraft.fhir.resources.datatypes.R5.primitive import boolean, code  # (1)!
from fhircraft.fhir.resources.datatypes.R5.complex import HumanName, Identifier

class Patient(FHIRBaseModel):

    active: Optional[boolean] = Field(...)  # (2)!
    name: Optional[List[HumanName]] = Field(...)
    gender: Optional[code] = Field(...)
    ...

    # FHIR invariant validation
    @model_validator(mode="after")
    def validate_patient_constraints(self):
        ...
```

1. Primitive **type aliases** (`boolean`, `code`) are the recommended annotation for resource fields — they accept both native Python values and FHIR primitive model instances.
2. Field values are stored as FHIR primitive model instances that behave transparently as their underlying Python types.

## Data Type System

Fhircraft implements FHIR's complete type hierarchy using Python objects. This ensures that every piece of healthcare data maintains its semantic meaning while being fully accessible in Python.

### Primitive Types  

Fhircraft implements all [:material-fire: FHIR Primitive Types](https://hl7.org/fhir/datatypes.html#primitive) through a **dual-type design**: each primitive type has both a **model class** and a **type alias**.

**Model classes** (uppercase, e.g. `String`, `Boolean`) are the full FHIR representation of a primitive. Each one wraps the raw value in a `.value` attribute and carries the rest of the FHIR element payload—`id`, `extension`, and other metadata—right alongside it. The value is also validated against the FHIR-specified regex for that type, so invalid data is caught early.

**Type aliases** (lowercase, e.g. `string`, `boolean`) are what you'll use day-to-day when annotating fields in your resource models. Behind the scenes they're `Annotated` types that automatically coerce whatever you pass in—a plain Python value *or* a full model instance—into the corresponding model class. You get the convenience of working with native Python types without losing any FHIR fidelity.

```python
from fhircraft.fhir.resources.datatypes.R5.primitive import (
    String, string,    # model class + type alias
    Boolean, boolean,
    Date, date_,
)
```

| FHIR Primitive | Type Alias    | Model Class    | Accepted native types  |
| -------------- | ------------- | -------------- | ---------------------- |
| `boolean`      | `boolean`     | `Boolean`      | `bool`, `str`          |
| `integer`      | `integer`     | `Integer`      | `int`, `str`           |
| `integer64`    | `integer64`   | `Integer64`    | `int`, `str`           |
| `string`       | `string`      | `String`       | `str`                  |
| `decimal`      | `decimal`     | `Decimal`      | `float`, `str`         |
| `uri`          | `uri`         | `Uri`          | `str`                  |
| `url`          | `url`         | `Url`          | `str`                  |
| `canonical`    | `canonical`   | `Canonical`    | `str`                  |
| `base64Binary` | `base64Binary`| `Base64Binary` | `str`                  |
| `instant`      | `instant`     | `Instant`      | `str`                  |
| `date`         | `date_`       | `Date`         | `str`                  |
| `time`         | `time_`       | `Time`         | `str`                  |
| `dateTime`     | `dateTime`    | `DateTime`     | `str`                  |
| `code`         | `code`        | `Code`         | `str`                  |
| `oid`          | `oid`         | `Oid`          | `str`                  |
| `id`           | `id_`         | `Id`           | `str`                  |
| `markdown`     | `markdown`    | `Markdown`     | `str`                  |
| `unsignedInt`  | `unsignedInt` | `UnsignedInt`  | `int`, `str`           |
| `positiveInt`  | `positiveInt` | `PositiveInt`  | `int`, `str`           |
| `uuid`         | `uuid`        | `Uuid`         | `str`                  |
| `xhtml`        | `xhtml`       | `Xhtml`        | `str`                  |

!!! note "Why the trailing underscore?"
    A handful of alias names (`date_`, `time_`, `id_`) use a trailing underscore to avoid shadowing Python built-ins (`date`, `time`) or commonly-used names (`id`).

#### Transparent value access

Fields annotated with a type alias store their values as the corresponding model class instance, not as a plain Python value. The model classes are designed to be **transparent**: they delegate all comparison, arithmetic, and string operations to the underlying `.value`, so they behave like the native type in most contexts.

!!! example "Primitive Types"

    ```python
    from fhircraft.fhir.resources.datatypes.R5.core import Patient

    patient = Patient(birthDate="1990-05-15")  # (1)!

    # The field stores a model instance...
    print(type(patient.birthDate))
    #> <class 'fhircraft.fhir.resources.datatypes.R5.primitive.date.Date'>

    # ...but it compares and prints like the underlying value:
    print(patient.birthDate)
    #> 1990-05-15

    print(patient.birthDate == "1990-05-15")
    #> True

    # Access the raw Python value directly:
    print(patient.birthDate.value)
    #> 1990-05-15
    print(type(patient.birthDate.value))
    #> <class 'str'>
    ```

    1. Any compatible native Python value is automatically coerced into the model class by the type alias's `BeforeValidator`.


??? abstract "Technical Documentation"

    [`fhircraft.fhir.path.mixin`](/fhircraft/reference/fhir-resources-types-primitives.md/)

### Complex Types
FHIR complex types represent structured data with multiple fields—such as addresses, names, and codeable concepts. Unlike primitive types that represent single values, complex types bundle related fields into cohesive data structures. Fhircraft provides Pydantic models for all [:material-fire: FHIR complex types](https://hl7.org/fhir/datatypes.html#complex), ensuring built-in validation, type safety, and seamless integration with the rest of the FHIR ecosystem.

Each complex type is a reusable component that can appear in multiple resources. For example, `HumanName` can be used in `Patient`, `Practitioner`, and `RelatedPerson` resources, while `Address` appears across numerous resource types. These types maintain consistent structure and validation rules regardless of where they're used, making it easy to work with healthcare data in a standardized way.

```python
from fhircraft.fhir.resources.datatypes.R5.complex import (
    HumanName, Address, CodeableConcept, Quantity
)

# Create complex structured data
name = HumanName(
    family="Johnson",
    given=["Alice", "Marie"],
    use="official"
) 

address = Address(
    line=["123 Main Street", "Apt 4B"],
    city="Springfield", 
    state="IL",
    postalCode="62704",
    country="US"
) 

# Complex types can contain other complex types
concept = CodeableConcept(
    coding=[{
        "system": "http://loinc.org",
        "code": "29463-7", 
        "display": "Body weight"
    }]
) 

print(name.family)  
#> Johnson

print(address.line[0])  
#> '123 Main Street'
```

## FHIR Resource Structure

FHIR resources map to Pydantic models that reflect the complete FHIR specification, including cardinality, constraints, and relationships.

### Field Cardinality

FHIR's cardinality rules (min..max) translate to Python type annotations:

| Max | Python Type              | Description    |
| --- | ------------------------ | -------------- |
| 1   | `Optional[<type>]`       | A single value |
| *   | `Optional[List[<type>]]` | A list value   |

For list-type elements, the length of the list is constrained by the minimal and maximal cardinality of the element using the Pydantic  `Field(max_length=..., min_length=...)` constraints.

```python

class MyPatient(FHIRBaseModel):    
    
    # Cardinality 0..1 
    active: Optional[boolean] = Field(default=None)
    
    # Cardinality 1..2
    name: Optional[List[HumanName]] = Field(default=None, max_length=3)
    
    # Cardinality 1..*
    identifier: Optional[List[Identifier]] = Field(default=None)
```

!!! info "Cardinality and requiredness in FHIR"
    
    In FHIR, a minimal cardinality of `1` does not necessarily mean the element is required; it only restricts the element to a single value if present. As a result, all resource fields in Fhircraft Pydantic models are optional by default, and requiredness is enforced through FHIR invariants when applicable.


### Type Choice Elements

In FHIR, type choice elements (those ending with `[x]`) allow multiple possible data types but only one can be used at a time. For example, an `Observation`'s effective time can be expressed as a `DateTime`, `Period`, `Instant`, or `Timing`. Fhircraft handles this by creating separate fields for each allowed type variant. So instead of a single `effective[x]` field, you get `effectiveDateTime`, `effectivePeriod`, `effectiveInstant`, and so on. Each variant field corresponds to one of the allowed types for that choice element. 

Fhircraft validates that exactly one type variant is set at a time—attempting to set multiple variants raises a validation error. For convenient access when the specific type variant is unknown (such as when working with deserialized resources), each choice element provides a generic property named after the element's base name. For instance, `Observation.effective` automatically returns the value of whichever type variant (`effectiveDateTime`, `effectivePeriod`, etc.) is currently set.

!!! example "Working with type choice elements"

    ```python
    from fhircraft.fhir.resources.datatypes.R5.core import Observation

    # The effective[x] element can be Date, DateTime, Period, etc.
    observation = Observation(
        status="final",
        code={"text": "Time of Birth"},
        valueDateTime="2023-12-25T10:30:00Z"  # (1)!
    )

    assert observation.valueDateTime == observation.value # (3)!

    # Setting a different type does not clear the previous one
    observation.valueTime = "10:30:00"  # (4)!
    observation.valueDateTime = None # (5)!
    assert observation.valueTime == observation.value # (6)!
    ```

    1. Set the `valueDateTime` variant of the choice element.
    3. The generic `value` property returns whichever variant is set.
    4. Setting a different variant does not automatically clear the previous one; both will be set simultaneously, which violates the single-variant constraint.
    5. The previous variant (`valueDateTime`) must be explicitly cleared to avoid a validation error.
    6. The generic property now returns the remaining active variant.

### Backbone Elements

Backbone elements are nested structures within FHIR resources that define complex, resource-specific data patterns. Unlike reusable complex types (such as `HumanName` or `Address`), backbone elements are unique to their parent resource and represent specialized sub-structures with their own fields, cardinality rules, and validation constraints.

Fhircraft generates dedicated Pydantic models for each backbone element. They inherit the `BackboneElement` class and maintain full type safety and validation throughout the hierarchy. These models follow a clear naming convention: the backbone element class name combines the parent resource name with the element name. For example, `Observation.component` becomes `ObservationComponent`, and `MedicationRequest.dosageInstruction` becomes `MedicationRequestDosageInstruction`. This naming pattern makes it easy to identify the origin and purpose of each backbone element class.

!!! example "Working with backbone elements"

    ```python
    # Observation.component is a backbone element
    component_data = {
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "8480-6",
                "display": "Systolic blood pressure"
            }]
        },
        "valueQuantity": {
            "value": 120,
            "unit": "mmHg",
            "system": "http://unitsofmeasure.org",
            "code": "mm[Hg]"
        }
    }

    observation = Observation(
        status="final",
        code={"text": "Blood pressure"},
        component=[component_data]  # (1)!
    )

    # Access backbone element data
    component = observation.component[0]  # (2)!
    print(type(component))  # (3)!
    #> <class 'fhircraft.fhir.resources.datatypes.R5.core.observation.ObservationComponent'>

    print(component.valueQuantity.value)  # (4)!
    #> 120.0
    ```

    1. Backbone elements can be provided as dictionaries during construction.
    2. They become properly typed Python objects.
    3. Each backbone element has its own generated class.
    4. Navigate nested structures naturally using dot notation.


### Context Awareness

Fhircraft automatically maintains bidirectional relationships between nested `FHIRBaseModel` objects, enabling seamless context-aware navigation throughout the resource hierarchy. When you access any nested element—whether a complex type, backbone element, or item in a list—it retains references to both its immediate parent and the root resource. This parent tracking is essential for FHIRPath evaluation, constraint validation, and resource manipulation, as it allows any element to understand its position and context within the broader resource structure without requiring manual reference management.

Additionally, Fhircraft replaces standard Python lists with context-aware `FHIRList` objects. These specialized lists automatically propagate context information to their items, ensuring that every element added to or modified within the list maintains proper parent and resource references. This happens transparently—you work with `FHIRList` just like a regular Python list, but with the added benefit of automatic context tracking.

!!! example "Working with context-aware structures"

    ```python
    from fhircraft.fhir.resources.datatypes.R5.core import Patient
    from fhircraft.fhir.resources.datatypes.R5.complex import HumanName

    patient = Patient(name=[])

    # List fields use FHIRList instead of standard Python lists
    print(type(patient.name))  # (1)!
    #> <class 'fhircraft.fhir.resources.base.FHIRList'>

    # Add items and context is automatically maintained
    patient.name.append(HumanName(family="Smith", given=["John"]))  # (2)!
    patient.name.append(HumanName(family="Smith", given=["Johnny"], use="nickname"))

    # Access nested elements with maintained context
    name = patient.name[0]  # (3)!
    
    print(hasattr(name, '_parent'))  # (4)!
    #> True
    
    print(name._parent == patient)  # (5)!
    #> True
    
    print(name._resource == patient)  # (7)!
    #> True
    ```

    1. List fields automatically use context-aware `FHIRList` containers.
    2. Adding items to the list automatically establishes parent relationships.
    3. Retrieved elements maintain full context information.
    4. Each element knows its immediate parent container.
    5. The parent reference points to the containing `FHIRList`.
    6. Each element also maintains a reference to the root resource.
    7. Navigate back to the root resource from any nested element.

### Polymorphic (De)serialization

Fhircraft automatically handles inheritance and polymorphism during serialization and deserialization, ensuring that resource types are preserved accurately throughout the data lifecycle. When a FHIR resource contains nested elements that can be any resource type )such as `Bundle.entry.resource`, `Parameters.parameter.resource`, or `DomainResource.contained`) Fhircraft ensures the exact concrete type is maintained rather than being reduced to a generic base class.

During serialization, each resource automatically includes a `resourceType` field, which identifies the specific FHIR resource class. This discriminator field allows deserializers to reconstruct the exact Python class when reading the data back.


!!! example "Serializing a Bundle"
    
    For example, when a `Bundle` contains both `Patient` and `Observation` resources in its entries, serialization preserves each resource's specific type information.

    During deserialization, Fhircraft reads the `resourceType` discriminator and dynamically instantiates the correct Python class for each resource. This means that accessing `bundle.entry[0].resource` returns an actual `Patient` instance with all its specific methods and fields, not a generic `Resource` object. This polymorphic deserialization works recursively through the entire resource tree, ensuring that every nested resource maintains its precise type identity.

    ```python
    from fhircraft.fhir.resources import get_fhir_type

    # Different resource types
    Patient = get_fhir_type("Patient", "R5") 
    Practitioner = get_fhir_type("Practitioner", "R5")
    Bundle = get_fhir_type("Bundle", "R5")

    # Create a bundle containing different resource types
    bundle = Bundle(
        type="collection",
        entry=[
            {"resource": Patient(name=[{"family": "Johnson"}]), "fullUrl": 'http:example.org/patient1'},
            {"resource": Practitioner(name=[{"family": "Smith"}]), "fullUrl": 'http:example.org/patient2'}
        ]
    ) # (1)!

    # Serialization preserves exact types
    bundle_dict = bundle.model_dump()
    print(bundle_dict["entry"][0]["resource"]["resourceType"])  # (2)!
    #> Patient

    print(bundle_dict["entry"][1]["resource"]["resourceType"])  # (3)!
    #> Practitioner

    # Deserialization reconstructs exact types
    bundle_copy = Bundle.model_validate(bundle_dict)
    print(type(bundle_copy.entry[0].resource))  # (4)!
    #> <class 'fhircraft.fhir.resources.datatypes.R5.core.patient.Patient'>
    ```

    1. Bundle entries can contain any FHIR resource type.
    2. Patient resource maintains its type during serialization.
    3. Practitioner resource maintains its type during serialization.
    4. Deserialization recreates the original specific types, not generic resources.


This polymorphic behavior extends to all models derived from `FHIRBaseModel` throughout the FHIR specification. Whether you're working with `Bundle` entries, contained resources, `Parameters` with resource values, or provenance targets, Fhircraft preserves the concrete types automatically. You can serialize complex resource hierarchies to JSON or XML and deserialize them back with complete type fidelity, enabling type-safe resource processing without manual type checking or casting.


### Fixed and Pattern Constraints

FHIR profiles and implementation guides often define additional constraints beyond basic type validation. These constraints can specify fixed values (elements that must always have a specific value) or pattern requirements (elements that must conform to particular patterns or contain specific sub-elements). Fhircraft automatically enforces these constraints during model validation, ensuring that resources conform to their intended profiles.

Fixed and pattern value constraints are treated as follows: if the field is not provided during construction, the pattern value is used as the default. However, if a value is explicitly provided, Fhircraft uses Pydantic validators to ensure the supplied value matches either the exact constrained value (for fixed-value constraints) or partially matches with the full required pattern value (for pattern-value constraints). This allows for flexibility while maintaining conformance requirements.


### Extensions

FHIR extensions allow you to add custom data to any element in a resource, enabling implementation-specific requirements while maintaining FHIR conformance. Fhircraft supports extensions on all element types.

For complex types and resources, add extensions via the `extension` field, which accepts a list of `Extension` objects. Each extension has a `url` identifying its definition and a type-choice value field (`valueString`, `valueCodeableConcept`, `valueQuantity`, etc.).

For **primitive fields**, because field values are now stored as model class instances (e.g. `Boolean`, `Date`) that already inherit from `Element`, you can attach extensions directly to the primitive value by constructing the model class explicitly:

```python
from fhircraft.fhir.resources.datatypes.R5.core import Patient
from fhircraft.fhir.resources.datatypes.R5.primitive import Date, Boolean
from fhircraft.fhir.resources.datatypes.R5.complex import Extension

# Extensions directly on a primitive value
patient = Patient(
    birthDate=Date(
        value="1990-05-15",
        extension=[
            Extension(
                url="http://example.org/data-quality",
                valueCode="estimated"
            )
        ]
    )  # (1)!
)

# The value still behaves transparently:
print(patient.birthDate)
#> 1990-05-15
print(patient.birthDate == "1990-05-15")
#> True

# But the extension metadata is preserved:
print(patient.birthDate.extension[0].url)  # (2)!
#> http://example.org/data-quality

# Extensions on complex elements
patient.extension = [
    Extension(
        url="http://example.org/patient-category",
        valueCodeableConcept={
            "coding": [{
                "system": "http://example.org/categories",
                "code": "VIP"
            }]
        }
    )
]  # (3)!

print(patient.extension[0].valueCodeableConcept.coding[0].code)
#> VIP
```

1. Construct the model class directly to attach extensions to a primitive value. A plain Python value (e.g. `"1990-05-15"`) is also accepted and coerced automatically — the model class form is only needed when you want to include extensions or other element metadata.
2. The extension is accessible directly on the primitive model instance.
3. All elements support the standard `extension` array.

### FHIR Invariant Constraints

FHIR invariants are formal constraints defined in the FHIR specificatio or in implementation guides that enforce business rules and data integrity requirements beyond basic type validation. These constraints, identified by codes like `ele-1`, `qty-3`, or `pat-1`, express complex validation logic such as "if element X is present, then element Y must also be present" or "the value must satisfy condition Z." 

Fhircraft automatically validates these invariants by embedding them directly into the Pydantic models as field validators (using `@field_validator` for element-level constraints) or model validators (using `@model_validator` for constraints that span multiple fields). The validation logic leverages Fhircraft's embedded FHIRPath engine to evaluate the constraint expressions, ensuring that every resource instance conforms to both its structural definition and the semantic rules defined in the FHIR specification.

```python
from pydantic import ValidationError
from fhircraft.fhir.resources.datatypes.R5.complex import Quantity

# This violates FHIR invariant qty-3: "If a code for the unit is present, the system SHALL also be present"
try:
    invalid_quantity = Quantity(
        value=10,
        unit="mg", 
        code="mg"  # (1)!
        # Missing required 'system' field
    )
except ValidationError as e:
    print("Validation failed:")
    print(e)  # (2)!
```

1. Providing a `code` without a `system` violates a FHIR constraint.
2. Fhircraft raises clear validation errors with FHIR constraint information.


### Slicing

[Slicing](https://hl7.org/fhir/R4/profiling.html#slicing) is a powerful FHIR profiling mechanism that allows profiles to define specialized variations of repeating elements. When a profile needs to constrain different instances of the same element in different ways, slicing provides a way to create distinct "slices" with their own specific constraints, discriminators, and validation rules.

Fhircraft represents each slice as a separate Pydantic model that inherits from `FHIRSliceModel` and the original sliced type model. Each slice model contains only the fields and constraints relevant to that specific slice variant. At runtime, Pydantic uses type unions with `union_mode='left_to_right'` to attempt matching input data against each slice model in the defined order until one successfully validates.

This approach ensures type safety while maintaining the flexibility that slicing provides. Each slice becomes a distinct Python class with its own validation logic, making it easy to work with strongly-typed slice instances while preserving the polymorphic nature of sliced elements.

!!! example "Working with sliced elements"

    ```python
    from fhircraft.fhir.resources.base import FHIRBaseModel, FHIRSliceModel
    from fhircraft.fhir.resources.datatypes.R5.complex import CodeableConcept, BackboneElement
    from pydantic import Field
    from typing import Optional, List, Union, Annotated

    # Base backbone element with all possible fields
    class ObservationComponent(BackboneElement):
        code: Optional[CodeableConcept] = Field(...)
        valueString: Optional[str] = Field(...)
        valueInteger: Optional[int] = Field(...)

    # Slice for string-based components (e.g., text observations)
    class StringComponent(FHIRSliceModel):  # (1)!
        code: CodeableConcept = Field(...)
        valueString: str = Field(...)
        
    # Slice for integer-based components (e.g., numeric measurements)
    class IntegerComponent(FHIRSliceModel):  # (2)!
        code: CodeableConcept = Field(...)
        valueInteger: int = Field(...)

    # Profiled observation using sliced components
    class VitalSignsObservation(FHIRBaseModel):  # (3)!
        status: str = Field(default="final")
        code: CodeableConcept = Field(...)
        component: Optional[List[
            Annotated[
                Union[StringComponent, IntegerComponent, ObservationComponent],  # (4)!
                Field(union_mode='left_to_right')
            ]
        ]] = Field(default=None)

    # Create observation with mixed component types
    observation = VitalSignsObservation(
        code={"text": "Vital Signs Panel"},
        component=[
            {  # (5)!
                "code": {"text": "Blood Pressure Status"},
                "valueString": "Normal"
            },
            {  # (6)!
                "code": {"text": "Heart Rate"},
                "valueInteger": 72
            }
        ]
    )

    # Verify slice assignments
    print(type(observation.component[0]))  # (7)!
    #> <class '__main__.StringComponent'>
    
    print(type(observation.component[1]))  # (8)!
    #> <class '__main__.IntegerComponent'>
    
    print(observation.component[0].valueString)  # (9)!
    #> Normal
    
    print(observation.component[1].valueInteger)  # (10)!
    #> 72

    # Check available slices programmatically
    if hasattr(VitalSignsObservation, 'get_sliced_elements'):  # (11)!
        slices = VitalSignsObservation.get_sliced_elements()
        print(slices)
        #> {'component': [StringComponent, IntegerComponent]}
    ```

    1. String slice model with constraints specific to text-based components.
    2. Integer slice model with constraints specific to numeric measurements.
    3. The main profiled resource that uses sliced components.
    4. Union type with left-to-right matching - Pydantic tries each slice in order.
    5. This input matches StringComponent (has valueString field).
    6. This input matches IntegerComponent (has valueInteger field).
    7. First component was assigned to the StringComponent slice.
    8. Second component was assigned to the IntegerComponent slice.
    9. Access slice-specific fields directly with full type safety.
    10. Each slice provides its own validated data structure.
    11. Introspection methods help understand the slice structure at runtime.

## What's Next?

Now that you understand how Fhircraft represents FHIR concepts in Python, continue with:

- **[Resource Models](resources-models.md)** - Learn to create and work with FHIR resource instances
- **[Resource Factory](resources-construction.md)** - Master model construction from FHIR specifications and packages  
- **[FHIRPath Querying](fhirpath.md)** - Query and manipulate resources with FHIRPath expressions
- **[FHIR Mapper](mapper.md)** - Transform external data into validated FHIR resources

For a broader overview of all Fhircraft features, see the [User Guide overview](overview.md).

---

**Continue learning:** [Resource Models →](resources-models.md)