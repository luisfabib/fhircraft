
FHIRPath is a path-based navigation and extraction language, similar to XPath. It is designed to operate on hierarchical data models, enabling operations such as traversal, selection, and filtering of data. FHIRPath is particularly suited to the healthcare domain, where it is used extensively with HL7 Fast Healthcare Interoperability Resources (FHIR). The language's design was heavily influenced by the need to navigate paths, select specific data points, and formulate invariants within FHIR data models.

Fhircraft provides a fully compliant FHIRPath engine that adheres to the FHIRPath Normative Release v2.0.0 (ANSI/HL7 NMN R1-2020). This engine allows users to parse and evaluate FHIRPath expressions against FHIR data structures.

## Basics

### FHIRPath expressions

The Fhircraft FHIRPath engine can be accessed through the `fhircraft.fhir.path module`, where an initialized instance is available as `fhirpath`. This engine provides a `parse` method, which is used to convert string-based FHIRPath expressions into their corresponding Python representations.

```python
from fhircraft.fhir.path import fhirpath 
expression = fhirpath.parse('Observation.value.unit')
``` 

The `expression` object represents the parsed FHIRPath expression in Python, which can then be used to evaluate the expression against FHIR-compliant Python objects.

!!! info FHIRPath Expressions
    For a comprehensive guide on constructing FHIRPath expressions, refer to the official [FHIRPath documentation](https://hl7.org/fhirpath/N1/). 


FHIRPath expressions operate on [collections](https://hl7.org/fhirpath/#collections), meaning that the result of every expression is a collection—even when the expression yields a single element. This design simplifies path specification by abstracting away the need to consider the cardinality of individual elements, making it particularly well-suited for traversing graph-like structures. To evaluate a parsed expression and retrieve the value(s) from a FHIR object, you can use the  `get_value` method.

```
value_unit = expression.get_value(my_observation)
```

This method will execute the FHIRPath expression against the provided FHIR object and return the corresponding collection of values.

## Advanced Usage

!!! warning
    Under construction, TBA


