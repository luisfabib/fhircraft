# FHIRPath Querying

This guide covers how to use [:material-fire: FHIRPath](https://hl7.org/fhirpath/N1/) expressions in Fhircraft to query and manipulate FHIR data. FHIRPath provides a standardized way to navigate through FHIR resource structures, similar to XPath for XML documents. Fhircraft implements the [:material-fire: FHIRPath Normative Release (v2.0.0)](https://hl7.org/fhirpath/N1/) as well as the [:material-fire: FHIR-specific add-on](https://www.hl7.org/fhir/fhirpath.html) variables and functions.  

??? abstract "Technical Documentation"

    [`fhircraft.fhir.path.engine`](/fhircraft/reference/fhir-path-engine/)

## FHIRPath Basics

FHIRPath is a query language designed specifically for healthcare data. If you've worked with [XPath](https://www.w3.org/TR/xpath/) for XML or [JSONPath](https://goessner.net/articles/JsonPath/) for JSON, FHIRPath serves a similar purpose for FHIR resources. It lets you navigate through complex nested healthcare data structures using simple path expressions.

| Tool | Purpose | Example Expression |
|------|---------|-------------------|
| **XPath** | Query XML documents | `//patient/name[@use='official']/family` |
| **JSONPath** | Query JSON structures | `$.patient.name[?(@.use=='official')].family` |
| **FHIRPath** | Query FHIR resources | `Patient.name.where(use='official').family` |

FHIR resources have complex, deeply nested structures that reflect real-world healthcare complexity. Consider a patient with multiple names, addresses, and contact points, or an observation with coded values, components, and references to other resources. FHIRPath expressions handle this complexity naturally:

```python
from fhircraft.fhir.resources.datatypes.R5.core import Patient

patient = Patient(
    name=[
        {"given": ["Alice"], "family": "Johnson", "use": "official"},
        {"given": ["Aly"], "family": "John", "use": "nickname"}
    ],
) 

# Without FHIRPath, you'd write loops and conditionals:
official_family_name = None
for name in patient.name:
    if name.use == "official":
        official_family_name = name.family
        break

# With FHIRPath, express your intent directly:
official_family_name = patient.fhirpath_single("Patient.name.where(use='official').family") # (1)!
```

1. This expresses the same logic as the loop above but more clearly and concisely.

FHIRPath also handles edge cases automatically - missing values, lists of values, multiple matches, and type conversions work consistently across all healthcare data scenarios.

!!! info "Further reading"

    Checkout these resources for additional information:

    - [:material-fire: FHIRPath Specification](https://hl7.org/fhirpath/N1/) - Official language specification
    - [:material-fire: FHIRPath Tutorial](https://hl7.org/fhirpath/N1/#tutorial) - Interactive examples
    - [:material-fire: FHIR Data Types](https://hl7.org/fhir/datatypes.html) - Understanding FHIR structures



## Querying FHIR Models

When working with Fhircraft FHIR resources, you can use FHIRPath expressions directly on the resource instances. This provides the most convenient way to query FHIR data since all Fhircraft models include built-in FHIRPath methods:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

Patient = get_fhir_resource_type("Patient", "R5")

patient = Patient(
    name=[{"given": ["Alice"], "family": "Johnson"}],
    gender="female",
    telecom=[{"system": "phone", "value": "555-0123"}]
) # (1)!

# Query directly on the resource using built-in methods
family_names = patient.fhirpath_values("Patient.name.family") # (2)!
gender = patient.fhirpath_single("Patient.gender") # (3)!
has_phone = patient.fhirpath_exists("Patient.telecom.where(system='phone')") # (4)!

assert family_names == ["Johnson"]
assert gender == "female" 
assert has_phone == True
```

1. This creates a patient with name, gender, and contact information.
2. This extracts all family names directly from the patient object.
3. This gets the gender value, expecting exactly one result.
4. This checks if the patient has any phone numbers.

The FHIR model methods automatically handle environment setup and provide the simplest interface for most use cases.


??? abstract "Technical Documentation"

    [`fhircraft.fhir.path.mixin`](/fhircraft/reference/fhir-path-mixin/)

## Querying Non-FHIR Data

When you need to query raw dictionaries, JSON data, or other data structures that aren't Fhircraft FHIR models, use the engine interface directly. This gives you control over expression parsing and evaluation:

```python
from fhircraft.fhir.path import fhirpath

# Raw dictionary data (e.g., from an API or JSON file)
patient_dict = {
    "name": [{"given": ["Alice"], "family": "Johnson"}],
    "gender": "female"
} # (1)!

# Parse an expression once for reuse
name_expr = fhirpath.parse("name.family") # (2)!

# Evaluate against the dictionary data
family_names = name_expr.values(patient_dict) # (3)!
assert family_names == ["Johnson"]
```

1. This works with raw dictionary data that matches FHIR structure.
2. This parses the FHIRPath expression once and creates a reusable expression object.
3. This evaluates the parsed expression against the dictionary data.
4. This reuses the same parsed expression for multiple data items, improving performance.

## Query Methods

Healthcare data often contains fields with variable cardinality - some fields may be empty, contain a single value, or hold multiple values. For example, a patient resource might have zero phone numbers, one primary contact number, or multiple phone numbers for home, work, and mobile.

Fhircraft provides safe and predictable query methods to handle these scenarios effectively. These methods ensure that your code handles the variability of FHIR data structures without unexpected errors or null reference exceptions.

Additionally, Fhircraft enables updating values through FHIRPath operations, allowing you to modify healthcare data in a consistent and type-safe manner using the same expressive FHIRPath syntax used for querying.

### Available Methods

| FHIR Model Method | Engine Method | Purpose | Returns | Error Behavior |
|-------------------|---------------|---------|---------|----------------|
| `fhirpath_values()` | `values()` | Get all matching values | `List[Any]` | Never raises errors, returns `[]` if empty |
| `fhirpath_single()` | `single()` | Get exactly one value | `Any` | Raises error if multiple values found |
| `fhirpath_first()` | `first()` | Get first value safely | `Any` | Never raises errors, returns default if empty |
| `fhirpath_last()` | `last()` | Get last value safely | `Any` | Never raises errors, returns default if empty |
| `fhirpath_exists()` | `exists()` | Check if any values exist | `bool` | Never raises errors |
| `fhirpath_is_empty()` | `is_empty()` | Check if no values exist | `bool` | Never raises errors |
| `fhirpath_count()` | `count()` | Count matching values | `int` | Never raises errors |
| `fhirpath_update_values()` | `update_values()` | Update all matching locations | `None` | Raises error if no locations found |
| `fhirpath_update_single()` | `update_single()` | Update exactly one location | `None` | Raises error if zero or multiple locations |
| N/A | `trace()` | Get evaluation step trace | `List[str]` | Never raises errors |
| N/A | `debug_info()` | Get comprehensive debug data | `dict` | Never raises errors |

!!! example "Working with Collections"

    ```python
    from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

    Patient = get_fhir_resource_type("Patient", "R5")

    patient = Patient(
        name=[
            {"given": ["John"], "family": "Smith"},
            {"given": ["Johnny"], "family": "Smith", "use": "nickname"}
        ],
        telecom=[
            {"system": "phone", "value": "555-0123", "use": "home"},
            {"system": "phone", "value": "555-0456", "use": "work"},
            {"system": "email", "value": "john@example.com"}
        ]
    ) # (1)!

    # Get all values - safe for any number of matches
    all_phones = patient.fhirpath_values("Patient.telecom.where(system='phone').value") # (2)!
    assert all_phones == ["555-0123", "555-0456"]

    # Get single value - strict about expecting exactly one
    gender = patient.fhirpath_single("Patient.gender", default="unknown") # (3)!
    assert gender == "unknown"

    # Get first/last safely - handles multiple values gracefully  
    first_name = patient.fhirpath_first("Patient.name.given") # (4)!
    last_phone = patient.fhirpath_last("Patient.telecom.where(system='phone').value") # (5)!

    assert first_name == "John"
    assert last_phone == "555-0456"
    ```

    1. This creates a patient with multiple names and contact methods.
    2. This gets all phone numbers as a list, regardless of how many exist.
    3. This gets the gender with a fallback since none was provided.
    4. This safely gets the first given name from any name entry.
    5. This gets the last phone number from the filtered list.

!!! example "Testing Data Presence"

    ```python
    # Check existence before processing
    if patient.fhirpath_exists("Patient.birthDate"): # (1)!
        birth_year = patient.fhirpath_single("Patient.birthDate.substring(0,4)")
        print(f"Born in {birth_year}")

    # Count items for validation
    phone_count = patient.fhirpath_count("Patient.telecom.where(system='phone')") # (2)!
    if phone_count > 1:
        print(f"Patient has {phone_count} phone numbers")

    # Verify required data is missing
    if patient.fhirpath_is_empty("Patient.address"): # (3)!
        print("No address on file")
    ```

    6. This checks if a birth date exists before trying to process it.
    7. This counts phone numbers to handle multiple values appropriately.
    8. This verifies that no address information exists.

!!! example "Updating Data"

    ```python
    # Update all matching values
    patient.fhirpath_update_values("Patient.name.family", "Johnson") # (1)!

    # Update single value with error checking
    try:
        patient.fhirpath_update_single("Patient.gender", "male") # (2)!
    except FHIRPathError:
        print("Expected single gender field but found multiple")

    # Safe conditional updates
    if patient.fhirpath_exists("Patient.birthDate"):
        patient.fhirpath_update_single("Patient.birthDate", "1990-05-15") # (3)!
    ```

    1. This changes all family names to "Johnson" across all name entries.
    2. This attempts to set gender but fails safely if multiple gender fields exist.
    3. This only updates birth date if one already exists.

## Environment Variables

FHIRPath supports [:material-fire: Environment Variables](https://hl7.org/fhirpath/N1/#environment-variables) that provide context during expression evaluation. Environment variables are prefixed with `%` and usually contain metadata or information from outside the evaluation context.

### Available Environment Variables

Fhircraft automatically provides several standard environment variables that give you access to contextual or external information during FHIRPath expression evaluation. These variables follow the FHIRPath specification and provide access to the current evaluation context, resource hierarchy, and system constants.

Fhircraft automatically provides these environment variables in all FHIRPath evaluations that involve Fhircraft models (i.e. no unstructured dictionaries):

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `%context` | The current node being evaluated in the expression | `CodeableConcept` |
| `%resource` | The current resource being evaluated | `Patient` |
| `%rootResource` | The root resource in the evaluation hierarchy (typically same as `%resource` for simple queries) | `Bundle` |
| `%ucum` | The URL for the Unified Code for Units of Measure system | `http://unitsofmeasure.org` |
| `%fhirRelease` | The FHIR release version of the node being evaluated in the expression | `R4B` |

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

Patient = get_fhir_resource_type("Patient", "R5")

patient = Patient(
    id="patient-123",
    name=[{"given": ["Alice"], "family": "Johnson"}]
)
name = patient.name[0]

print(type(name.fhirpath_single("%context"))) # (1)!
#> <class 'fhircraft.fhir.resources.datatypes.R5.complex.human_name.HumanName'>

print(type(patient.fhirpath_single("%resource"))) # (2)!  
#> <class 'fhircraft.fhir.resources.datatypes.R5.core.patient.Patient'>

print(type(patient.fhirpath_single("%rootResource"))) # (3)!
#> <class 'fhircraft.fhir.resources.datatypes.R5.core.patient.Patient'>

print(patient.fhirpath_single("%ucum")) # (4)!
#> http://unitsofmeasure.org

print(patient.fhirpath_single("%fhirRelease")) # (5)!
#> R5
```

1. This accesses the current evaluation context (the patient).
2. This accesses the current resource being evaluated.
3. This accesses the root resource in the evaluation hierarchy.
4. This accesses the official UCUM units system URL.
4. This accesses the FHIR Release label of the patient resource.

### Custom Environment Variables

You can define custom environment variables to pass additional context into your FHIRPath expressions. This is particularly useful when working with implementation guides that require specific variables for resource validation or when implementing packages with modular environment variables. Use the `environment` argument to pass custom variables or override built-in ones.

For example, if working with a US-specific profile that requires a `%usZip` variable 
```python
expr = patient.fhirpath_values(
    expression="Patient.address.where(postalCode.matches(%usZip))", # (1)!
    environment={
        "%usZip": "[0-9]{5}(-[0-9]{4}){0,1}"  # (2)!
    }  
) 
```

1. This uses the custom environment variable in the expression.
2. This defines custom environment variables with specific values.

## Contextual Variables

FHIRPath provides contextual variables that give you access to the current evaluation state during collection iteration. These variables start with `$` and are automatically managed by the FHIRPath engine as it processes collections and filters.They become particularly useful when working with collection functions like `where()`, `select()`, or `repeat()`.

!!! tip "Contextual Variables vs Environment Variables"

    Unlike environment variables (which start with `%` and contain external context), contextual variables reflect the current position and state within the FHIRPath evaluation itself. Contextual variables change automatically as the FHIRPath engine processes collections, while environment variables remain constant throughout the entire evaluation.

### Available Contextual Variables

| Variable | Description | Type | Example Use Case |
|----------|-------------|------|------------------|
| `$this` | The current item being evaluated in a collection | `Any` | Filtering or transforming collection items |
| `$index` | The zero-based index of the current item within the collection | `int` | Accessing position-specific logic |
| `$total` | Accumulator variable used within `aggregate()` function | `Any` | Storing intermediate results during aggregation |

!!! example "Using `$this` in Collection Filtering"

    The `$this` variable refers to the current item when iterating through collections:

    ```python
    from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

    Patient = get_fhir_resource_type("Patient", "R5")

    patient = Patient(
        name=[
            {"given": ["John"], "family": "Smith", "use": "official"},
            {"given": ["Johnny"], "family": "Smith", "use": "nickname"},
            {"given": ["J"], "family": "Smith", "use": "usual"}
        ]
    ) # (1)!

    # Filter names using $this to reference the current name object
    official_names = patient.fhirpath_values("Patient.name.where($this.use = 'official')") # (2)!

    # Use $this for complex conditions
    short_nicknames = patient.fhirpath_values("Patient.name.where($this.use = 'nickname' and $this.given.length() <= 2)") # (3)!
    ```

    1. This creates a patient with multiple name entries using different use codes.
    2. This filters names where the current name object has use='official'.
    3. This combines multiple conditions using $this to reference the current name being evaluated.

!!! example "Using `$index` for Position-Based Logic"

    The `$index` variable provides the zero-based position of the current item:

    ```python
    patient = Patient(
        telecom=[
            {"system": "phone", "value": "555-0123"},
            {"system": "email", "value": "john@example.com"},
            {"system": "phone", "value": "555-0456"}
        ]
    ) # (1)!

    # Get the first contact method using index
    first_contact = patient.fhirpath_values("Patient.telecom.where($index = 0)") # (2)!

    # Get even-positioned items (0, 2, 4, etc.)
    even_contacts = patient.fhirpath_values("Patient.telecom.where($index mod 2 = 0)") # (3)!
    ```

    1. This creates a patient with multiple contact methods.
    2. This selects only the first contact method using the index.
    3. This selects contact methods at even positions using modulo arithmetic.

!!! example "Using `$total` in Aggregate Functions"

    The `$total` variable is an accumulator used within the `aggregate()` function to build up results:

    ```python
    from fhircraft.fhir.path import fhirpath

    # Sum all values using $total as accumulator
    numbers = [1, 2, 3, 4, 5]
    total_sum = fhirpath.parse("aggregate($this + $total, 0)").single(numbers) # (1)!
    assert total_sum == 15

    # Find minimum value using $total for comparison
    min_value = fhirpath.parse("aggregate(iif($total.empty(), $this, iif($this < $total, $this, $total)))").single(numbers) # (2)!
    assert min_value == 1

    # Calculate average using $total accumulation
    avg_calc = fhirpath.parse("aggregate($total + $this, 0)").single(numbers)  # (3)!
    average = avg_calc / len(numbers)
    assert average == 3.0
    ```

    1. This accumulates a sum, starting $total at 0 and adding each $this value to it.
    2. This finds the minimum by comparing each $this with the accumulated $total minimum.
    3. This shows how $total accumulates the sum, which can then be used to calculate average.

## FHIRPath Type System

FHIRPath expressions operate with their own type system that is distinct from FHIR resource types. Understanding this distinction helps you work effectively with FHIRPath evaluation results and type checking operations.

Fhircraft implements FHIRPath's native type system using specialized literal classes in the engine. These types handle FHIRPath-specific operations like date arithmetic, quantity comparisons, and precision handling that go beyond what standard FHIR types provide.

FHIRPath defines its own literal types that are separate from FHIR resource types:

| FHIRPath Type | FHIR Type |
|---------------|-----------------|
| `System.Boolean` | `FHIR.boolean` |
| `System.Integer` | `FHIR.integer`, `FHIR.positiveInt`, `FHIR.unsignedInt` |
| `System.Decimal` | `FHIR.decimal` |
| `System.String` | `FHIR.string`, `FHIR.code`, `FHIR.uuid`, `FHIR.oid`, `FHIR.uri`,`FHIR.id`, `FHIR.markdown`, `FHIR.base64binary` | 
| `System.Date` | `FHIR.date` | 
| `System.Time` | `FHIR.time` | 
| `System.DateTime` | `FHIR.dateTime`, `FHIR.instant` |
| `System.Quantity` | `FHIR.Quantity` |

Some of these literal types support FHIRPath-specific aritmethical and comparison operations that aren't available in standard FHIR types, such as unit conversion between quantities with compatible UCUM units and partial dates/times.

!!! example "FHIRPath specific type operations"

    ```python
    from fhircraft.fhir.path.engine.literals import Quantity, Date, DateTime

    # FHIRPath Quantity with unit conversion
    bp_systolic = Quantity(120000, "Pa")
    bp_kpa = Quantity(120, "kPa") 

    # FHIRPath handles unit conversion automatically
    print(bp_systolic == bp_kpa)  # (1)!
    #> True

    # FHIRPath Date with partial precision
    partial_date = Date("@2023-03")  # (2)!
    print(f"Year: {partial_date.year}, Month: {partial_date.month}, Day: {partial_date.day}")
    #> Year: 2023, Month: 3, Day: None
    ```

    1. This demonstrates automatic unit conversion between mmHg and kPa.
    2. This creates a partial date with only year and month specified.


### Type Namespaces

FHIRPath type specifiers support namespaces to distinguish between different type systems. 
When no namespace is specified, FHIRPath defaults to the `FHIR` namespace. The namespace resolution uses the `%fhirRelease` environment variable to determine which FHIR version's types to use:

```python
# These are equivalent - FHIR is the default namespace
is_patient_explicit = patient.fhirpath_single("Patient is FHIR.Patient") # (1)!
is_patient_implicit = patient.fhirpath_single("Patient is Patient") # (2)!

print(f"Explicit namespace: {is_patient_explicit}")
#> Explicit namespace: True
print(f"Implicit namespace: {is_patient_implicit}")
#> Implicit namespace: True

# Check for complex types with explicit namespace
has_name = patient.fhirpath_single("Patient.name.first() is FHIR.HumanName") # (3)!
print(f"Has HumanName: {has_name}")

# Use namespace for primitive types
birth_is_date = patient.fhirpath_single("Patient.birthDate is FHIR.date") # (4)!
print(f"Birth date is FHIR.date: {birth_is_date}")
```

1. This explicitly uses the FHIR namespace to check for Patient type.
2. This implicitly uses the FHIR namespace (default behavior).
3. This checks if name is a FHIR HumanName type using explicit namespace.
4. This checks if birth date is a FHIR date type using explicit namespace.

!!! warning "Limited namespace support"

    Currently, Fhircraft only supports the `FHIR` namespace for FHIR data types.


### Type Checking in FHIRPath

FHIRPath provides `is` and `as` operators for type checking and casting. These operators work with type specifiers that can optionally include namespaces:

```python
from fhircraft.fhir.resources.datatypes.R5.core import Patient

patient = Patient(id="ID1234") # (1)!

print(patient.fhirpath_single("Patient.id is id"))
#> True

print(patient.fhirpath_single("Patient.id is FHIR.id"))
#> True

print(patient.fhirpath_single("Patient.id is FHIR.integer"))
#> False
```

