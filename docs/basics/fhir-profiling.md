# Working with FHIR resources

Working with Fast Healthcare Interoperability Resources (FHIR) offers many benefits in terms of interoperability and data exchange in healthcare, but it also comes with certain disadvantages and caveats:

- FHIR includes a broad and intricate set of validation rules that cover syntax, structure, and content. Understanding and implementing these rules can be complex and time-consuming.
- FHIR resources often reference each other. Validating these interdependencies can be complex, particularly when dealing with incomplete or partial data.
- Different validation tools and libraries might have varying levels of support for the full range of FHIR validation rules, leading to inconsistent validation results.
- Many organizations use custom extensions and profiles to tailor FHIR resources to their specific needs. Validating these custom elements requires additional configuration and can be challenging.

This package provides a series of tools that aim to tackle these issues in a pythonic manner.
This section will discuss the different tools available for working with FHIR resources purely with Python. 

## Profiled FHIR Resources

Profiling in FHIR is needed to customize and extend standard resources to fit specific organizational or domain requirements without modifying the core FHIR specification. It allows healthcare systems to capture and exchange data in ways that are more meaningful and relevant to their specific workflows and contexts.

Profile modify a core resource by imposing a series of structural definitions and constraints upon a core resource. These constraints can introduce fixed values or additional validation conditions in addition to the existing conditions present in a core resource. All the changes imposed by a profile are give by its `StructureDefinition` which in turn has a unique canonical URL.

Fhircraft provides the tools to parse such a canonical URL and its corresponding `StructureDefinition` to generate a new Pydantic model that introduces the new constraints and validation conditions to ensure that any payload parsed by this model conforms to the provided FHIR profile. This is achieved as follows:

1. The profile `StructureDefinition` is downloaded from its canonical URL (or provided locally as a file) and parsed by the package. 

2. Based on the type of base resource, the appropriate core resource is selected from the `fhir.resources` package. This way, the explicit type definitions and validation tools of the core resource are maintained in the profiled resource.

3. A factory method then introduces the new constraints and validation functions to create a new derived Pydantic model that represents the profiled resource. 

### Constructing profile models

The generation of a new profiled FHIR resource Pydantic model is as easy as using the `construct_profiled_resource_model` function with the canonical URL of the desired profile. The factory method will return a Pydantic model with the same functionality as any other resource model in the `fhir.resources` package. 

```python
from fhircraft.fhir.profiling import construct_profiled_resource_model

# Construct the FHIR profile Pydantic model
canonical_url = 'http://domain.org/StructureDefinition-my-profile'
myProfile = construct_profiled_resource_model(canonical_url)

# Load and validate a FHIR payload against the profiled FHIR resource 
filename = pathlib.Path("data/clinicalObservation.json")
myProfile.parse_file(filename)

# Will raise ValidationError if payload does not conform to the profile
```


### Initializing profiled resources

!!! warning
    Under construction, TBA