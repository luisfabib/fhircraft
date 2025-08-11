
FHIRPath is a path-based navigation and extraction language, similar to XPath. It is designed to operate on hierarchical data models, enabling operations such as traversal, selection, and filtering of data. FHIRPath is particularly suited to the healthcare domain, where it is used extensively with HL7 Fast Healthcare Interoperability Resources (FHIR). The language's design was heavily influenced by the need to navigate paths, select specific data points, and formulate invariants within FHIR data models.

Fhircraft provides a fully compliant FHIRPath engine that adheres to the FHIRPath Normative Release v2.0.0 (ANSI/HL7 NMN R1-2020). This engine allows users to parse and evaluate FHIRPath expressions against FHIR data structures.

## Basics

### FHIRPath expressions

The Fhircraft FHIRPath engine can be accessed through the `fhircraft.fhir.path` module, where an initialized instance is available as `fhirpath`. This engine provides a `parse` method, which is used to convert string-based FHIRPath expressions into their corresponding Python representations.

```python
from fhircraft.fhir.path import fhirpath 
expression = fhirpath.parse('Observation.value.unit')
``` 

The `expression` object represents the parsed FHIRPath expression in Python, which can then be used to evaluate the expression against FHIR-compliant Python objects.

!!! info "FHIRPath Expressions"
    For a comprehensive guide on constructing FHIRPath expressions, refer to the official [FHIRPath documentation](https://hl7.org/fhirpath/N1/). 

## Using FHIRPath with Resource Objects

### FHIRPathMixin Interface

For convenience when working with FHIR resource objects, Fhircraft provides a `FHIRPathMixin` class that adds FHIRPath methods directly to your resource instances. This is the recommended approach for most use cases as it provides a cleaner, more intuitive interface.

When your resource classes inherit from `FHIRPathMixin`, you can call FHIRPath methods directly on resource instances:

```python
# Assuming your Patient class inherits from FHIRPathMixin
my_patient = Patient(...)

# Get all family names
family_names = my_patient.fhirpath_values("Patient.name.family")

# Get a single gender value
gender = my_patient.fhirpath_single("Patient.gender", default="unknown")

# Get the first family name
first_name = my_patient.fhirpath_first("Patient.name.family")

# Check if patient has any phone numbers
has_phone = my_patient.fhirpath_exists("Patient.telecom.where(system='phone')")

# Update gender
my_patient.fhirpath_update_single("Patient.gender", "other")
```

The mixin provides all the same methods as the engine interface, but with a more convenient syntax. All examples in this guide can be adapted to use the mixin by replacing:

```python
# Engine interface
expression = fhirpath.parse('Patient.name.family')
result = expression.values(my_patient)

# Mixin interface (more convenient)
result = my_patient.fhirpath_values("Patient.name.family")
```

### Engine Interface (Advanced)

For advanced use cases, performance optimization, or when you need more control over expression parsing, you can use the engine interface directly:

### Evaluating expressions

FHIRPath expressions operate on [collections](https://hl7.org/fhirpath/#collections), meaning that the result of every expression is a collection—even when the expression yields a single element. Fhircraft provides an enhanced interface with multiple methods to handle different scenarios when working with these collections.

#### Value Retrieval Methods

**Getting All Values**

Returns all matching values as a list. This is the most basic method and always returns a list, even for single or no matches:

```python
# Mixin interface (recommended)
family_names = my_patient.fhirpath_values("Patient.name.family")

# Engine interface (advanced)
family_names = fhirpath.parse('Patient.name.family').values(my_patient)

# Result: ['Doe', 'Smith'] or [] if no matches
```

**Getting a Single Value**

Returns exactly one value. Raises `FHIRPathRuntimeError` if multiple values are found:

```python
# Mixin interface (recommended)
gender = my_patient.fhirpath_single("Patient.gender", default="unknown")

# Engine interface (advanced)
gender = fhirpath.parse('Patient.gender').single(my_patient, default="unknown")

# Result: 'male' or 'unknown' if no gender specified
```

**Getting the First Value**

Returns the first matching value, safe for multiple values:

```python
# Mixin interface (recommended)
first_name = my_patient.fhirpath_first("Patient.name.family", default="Unknown")

# Engine interface (advanced)
first_name = fhirpath.parse('Patient.name.family').first(my_patient, default="Unknown")

# Result: 'Doe' (first family name) or 'Unknown' if no names
```

**Getting the Last Value**

Returns the last matching value:

```python
# Mixin interface (recommended)
last_name = my_patient.fhirpath_last("Patient.name.family")

# Engine interface (advanced)
last_name = fhirpath.parse('Patient.name.family').last(my_patient)

# Result: 'Smith' (last family name) or None if no names
```

#### Existence and Count Methods

**Checking if Values Exist**

Checks if any values match the FHIRPath expression:

```python
# Mixin interface (recommended)
has_family_name = my_patient.fhirpath_exists("Patient.name.family")

# Engine interface (advanced)
has_family_name = fhirpath.parse('Patient.name.family').exists(my_patient)

# Result: True if at least one family name exists
```

**Checking if No Values Exist**

Checks if no values match the FHIRPath expression:

```python
# Mixin interface (recommended)
no_phone = my_patient.fhirpath_is_empty("Patient.telecom.where(system='phone')")

# Engine interface (advanced)
no_phone = fhirpath.parse('Patient.telecom.where(system="phone")').is_empty(my_patient)

# Result: True if no phone numbers found
```

**Counting Values**

Returns the number of matching values:

```python
# Count the number of given names
given_count = fhirpath.parse('Patient.name.given').count(my_patient)
# Result: 2 if patient has 2 given names
```

#### Value Modification Methods

**`update_values(data, value) -> None`**

Sets all matching locations to the given value:

```python
# Update all family names to 'NewName'
fhirpath.parse('Patient.name.family').update_values(my_patient, 'NewName')
```

**`update_single(data, value) -> None`**

Sets exactly one matching location to the given value. Raises `FHIRPathError` if multiple locations match:

```python
# Update gender (expects single value)
fhirpath.parse('Patient.gender').update_single(my_patient, 'female')
# Raises error if multiple gender values exist
```

## Advanced Usage

### Error Handling

The enhanced interface provides specific error handling for different scenarios:

```python
try:
    # This will raise FHIRPathRuntimeError if multiple values found
    single_name = fhirpath.parse('Patient.name.family').single(my_patient)
except FHIRPathRuntimeError as e:
    print(f"Multiple family names found: {e}")
    # Fallback to getting the first one
    single_name = fhirpath.parse('Patient.name.family').first(my_patient)

try:
    # This will raise FHIRPathError if multiple locations to update
    fhirpath.parse('Patient.name.family').update_single(my_patient, 'NewName')
except FHIRPathError as e:
    print(f"Cannot update single value: {e}")
    # Use update_values to update all locations
    fhirpath.parse('Patient.name.family').update_values(my_patient, 'NewName')
```

### Working with Complex FHIRPath Expressions

The enhanced interface works seamlessly with complex FHIRPath expressions:

```python
# Complex expression with filtering
phone_expr = fhirpath.parse('Patient.telecom.where(system="phone").value')

# Check if patient has a phone number
if phone_expr.exists(my_patient):
    phone = phone_expr.first(my_patient)
    print(f"Phone: {phone}")

# Get all email addresses
emails = fhirpath.parse('Patient.telecom.where(system="email").value').values(my_patient)

# Update primary phone number
primary_phone_expr = fhirpath.parse('Patient.telecom.where(system="phone" and use="home").value')
if primary_phone_expr.exists(my_patient):
    primary_phone_expr.update_single(my_patient, '+1-555-123-4567')
```

### Best Practices

**1. Choose the Right Method for Your Use Case**

```python
# For single-value fields (like gender), use single()
gender = fhirpath.parse('Patient.gender').single(my_patient, default='unknown')

# For potentially multi-value fields, use first() or values()
primary_name = fhirpath.parse('Patient.name.family').first(my_patient)
all_names = fhirpath.parse('Patient.name.family').values(my_patient)

# Always check existence before assuming values exist
if fhirpath.parse('Patient.birthDate').exists(my_patient):
    birth_date = fhirpath.parse('Patient.birthDate').single(my_patient)
```

**2. Use Default Values Appropriately**

```python
# Provide meaningful defaults
birth_year = fhirpath.parse('Patient.birthDate.substring(0,4)').first(
    my_patient, 
    default='1900'
)

# Use None when absence is meaningful
phone = fhirpath.parse('Patient.telecom.where(system="phone").value').first(
    my_patient, 
    default=None
)
if phone is None:
    print("No phone number provided")
```

**3. Handle Updates Safely**

```python
# For single-value updates, prefer update_single() for safety
try:
    fhirpath.parse('Patient.gender').update_single(my_patient, 'other')
except FHIRPathError:
    # Handle case where field unexpectedly has multiple values
    print("Warning: Multiple gender values found")

# For multi-value fields, be explicit about updating all
name_expr = fhirpath.parse('Patient.name.family')
if name_expr.count(my_patient) > 0:
    name_expr.update_values(my_patient, 'UpdatedName')
```

### Debugging and Troubleshooting

Fhircraft provides built-in debugging methods to help you understand how FHIRPath expressions are evaluated and troubleshoot issues.

**`trace(data, verbose=False) -> List[str]`**

Returns a trace of evaluation steps:

```python
# Basic trace
expression = fhirpath.parse('Patient.name.family')
trace_lines = expression.trace(my_patient)
for line in trace_lines:
    print(line)

# Verbose trace with detailed information
verbose_trace = expression.trace(my_patient, verbose=True)
for line in verbose_trace:
    print(line)
```

**`debug_info(data) -> dict`**

Returns comprehensive debugging information:

```python
debug_data = expression.debug_info(my_patient)
print(f"Expression: {debug_data['expression']}")
print(f"Success: {debug_data['evaluation_success']}")
print(f"Result count: {debug_data['result_count']}")
print(f"Result types: {debug_data['result_types']}")

# Check for errors
if not debug_data['evaluation_success']:
    print(f"Error: {debug_data['error']}")
```

These debugging methods are particularly useful when:
- Expressions don't return expected results
- You need to understand the evaluation flow
- Debugging complex nested expressions
- Validating expression behavior during development

## Quick Reference

### Method Summary

| Method | Purpose | Returns | Raises Error |
|--------|---------|---------|-------------|
| `values(data)` | Get all matching values | `List[Any]` | Never |
| `single(data, default=None)` | Get exactly one value | `Any` | If multiple values found |
| `first(data, default=None)` | Get first value | `Any` | Never |
| `last(data, default=None)` | Get last value | `Any` | Never |
| `exists(data)` | Check if any values exist | `bool` | Never |
| `is_empty(data)` | Check if no values exist | `bool` | Never |
| `count(data)` | Count matching values | `int` | Never |
| `update_values(data, value)` | Update all matching locations | `None` | If no locations found |
| `update_single(data, value)` | Update single location | `None` | If 0 or >1 locations found |

### Common Patterns

```python
from fhircraft.fhir.path import fhirpath

# Parse expression once, use multiple times
name_expr = fhirpath.parse('Patient.name.family')

# Safe single value retrieval
gender = fhirpath.parse('Patient.gender').single(my_patient, default='unknown')

# Safe multi-value handling
all_phones = fhirpath.parse('Patient.telecom.where(system="phone").value').values(my_patient)
primary_phone = fhirpath.parse('Patient.telecom.where(use="home").value').first(my_patient)

# Existence checking before operations
birth_date_expr = fhirpath.parse('Patient.birthDate')
if birth_date_expr.exists(my_patient):
    birth_date = birth_date_expr.single(my_patient)
    print(f"Birth date: {birth_date}")

# Safe updates
try:
    fhirpath.parse('Patient.gender').update_single(my_patient, 'other')
except FHIRPathError:
    print("Multiple gender values found - using update_values instead")
    fhirpath.parse('Patient.gender').update_values(my_patient, 'other')

# Debugging
debug_info = name_expr.debug_info(my_patient)
if not debug_info['evaluation_success']:
    print(f"Evaluation failed: {debug_info['error']}")
```


