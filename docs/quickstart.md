
Welcome to the Fhircraft Quickstart Guide! Here, you'll learn how to easily install Fhircraft, construct dynamic Pydantic FHIR models, validate FHIR payloads, and more. 

## Requirements

- Python 3.8 or newer
- `pip` package manager

Optional (for advanced features):

- Internet access (to fetch FHIR StructureDefinitions by canonical URL)
- Local FHIR StructureDefinition files (for offline model construction)
- Familiarity with [:simple-pydantic: Pydantic](https://docs.pydantic.dev/latest/) is helpful but not required

## Installation

To get started with Fhircraft, ensure you have Python 3.8 or newer and `pip` installed on your system.

Install Fhircraft using pip:

```bash
pip install fhircraft
```

This command will automatically download and install Fhircraft along with its required dependencies.

For advanced installation options or further information, refer to the [:material-download: Installation instructions](installation.md).

### Development Installation

If you want to contribute to Fhircraft or work with the latest development version:

```bash
# Clone the repository
git clone https://github.com/luisfabib/fhircraft.git
cd fhircraft

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Dependencies

Fhircraft has the following core dependencies:

- **Pydantic** (≥2.7) - For data validation and serialization
- **requests** - For fetching FHIR structure definitions via HTTP
- **ply** (≥3.11) - For FHIRPath parsing
- **jsonschema** (>4) - For JSON schema validation
- **pyyaml** (6.0.1) - For YAML file support
- **jsonpath-ng** (>1) - For JSON path operations
- **jinja2** (≥3.1) - For code generation templates

All dependencies are automatically installed when you install Fhircraft.

## Features

Explore some of the key features of Fhircraft and learn how to access them quickly.

---------------

### Constructing Dynamic Pydantic FHIR Models

Fhircraft makes it simple to generate Pydantic models for any FHIR resource or profile using the `construct_resource_model` function. This function dynamically builds a model based on the provided FHIR StructureDefinition, supporting both canonical URLs and local files as input sources.

**Example: Creating a Pydantic Model for the FHIR `Patient` Resource**

You can construct a model for the core FHIR `Patient` resource in two ways:

=== "Canonical URL"

    ```python
    from fhircraft.fhir.resources.factory import construct_resource_model
    patient_model = construct_resource_model(
        canonical_url='http://hl7.org/fhir/StructureDefinition/Patient'
    )
    ```

    !!! warning "Internet Access Required"
        When using a canonical URL, Fhircraft fetches the StructureDefinition via HTTP. Ensure your environment has internet access, as the definition will be downloaded from an external FHIR server.

=== "Local File"

    ```python
    from fhircraft.fhir.resources.factory import construct_resource_model
    from fhircraft.utils import load_file
    patient_model = construct_resource_model(
        structure_definition=load_file('FHIR_StructureDefinition_Patient.json')
    )
    ```

Once constructed, the resulting model fully leverages [:simple-pydantic: Pydantic's features](https://docs.pydantic.dev/latest/) while enforcing all FHIR structural and validation rules through Pydantic validators. This enables robust, standards-compliant data validation and manipulation for your FHIR resources.

--------------

### Generating Source Code for Pydantic FHIR Models

Fhircraft enables you to generate reusable Python source code for any dynamically constructed Pydantic FHIR model. This is accomplished using the `generate_resource_model_code` function, which returns the model's class definition as a string. This feature is ideal for integrating FHIR models into other projects, sharing models with collaborators, or version-controlling your model definitions.

**Example: Exporting the Source Code for a FHIR `Patient` Model**

```python
from fhircraft.fhir.resources.generator import generate_resource_model_code

# Assume patient_model was created using construct_resource_model
source_code = generate_resource_model_code(patient_model)

# Optionally, save the code to a file for reuse
with open("patient.py", "w") as f:
    f.write(source_code)
```

The generated code is ready to use in any Python project, provided that Fhircraft and its dependencies are installed. This approach streamlines collaboration and deployment by allowing you to distribute static model definitions without requiring dynamic model construction at runtime.

-----------

### Validating FHIR Payloads

Once you've constructed a Pydantic FHIR model, you can use it to validate real-world FHIR payloads. This ensures your data strictly adheres to the structure and constraints defined by the FHIR specification or your chosen profile.

**Example: Validating a FHIR `Patient` Resource**

```python
from fhircraft.utils import load_file

# Load your FHIR resource data (as a dict) from a JSON file
data = load_file('my_fhir_patient.json')

# Validate and parse the data using the generated model
my_patient = patient_model.model_validate(data)
```

If the input data does not match the expected FHIR structure or contains invalid values, Pydantic will raise a `ValidationError` detailing the issues. If no error is raised, your payload is valid and ready for further processing.

This validation step helps catch errors early, enforce FHIR compliance, and maintain data quality throughout your workflow.

---------------
### Manipulating Models with FHIRPath

Fhircraft provides a robust FHIRPath engine, allowing you to query and modify FHIR resources using standard FHIRPath expressions directly in Python. This enables expressive, standards-compliant access to deeply nested data and supports both retrieval and update operations.

**Example: Accessing Values with FHIRPath**

```python
# Retrieve the patient's family name using a FHIRPath expression
patient_surname = my_patient.get_fhirpath('Patient.name.family')
```

**Example: Updating Values with FHIRPath**

```python
# Update the patient's family name using a FHIRPath expression
my_patient.replace_fhirpath('Patient.name.family', 'Smith')
```

With these methods, you can efficiently navigate and manipulate FHIR resources, making complex data operations straightforward and Pythonic.

------------------

### Complete Example: End-to-End Workflow

Here's a complete example that demonstrates the entire workflow from constructing a model to validating and manipulating FHIR data:

```python
from fhircraft.fhir.resources.factory import construct_resource_model
from fhircraft.utils import load_file

# Step 1: Construct the Patient model
patient_model = construct_resource_model(
    canonical_url='http://hl7.org/fhir/StructureDefinition/Patient'
)

# Step 2: Create and validate a patient resource
patient_data = {
    "resourceType": "Patient",
    "id": "example-patient",
    "active": True,
    "name": [{
        "use": "official",
        "family": "Doe",
        "given": ["John", "William"]
    }],
    "gender": "male",
    "birthDate": "1990-01-01"
}

# Step 3: Validate the data
try:
    my_patient = patient_model.model_validate(patient_data)
    print("✅ Patient data is valid!")
except Exception as e:
    print(f"❌ Validation error: {e}")

# Step 4: Use FHIRPath to query and modify
family_name = my_patient.get_fhirpath('Patient.name.family')
print(f"Family name: {family_name}")

# Update the family name
my_patient.replace_fhirpath('Patient.name.family', 'Smith')
print(f"Updated family name: {my_patient.get_fhirpath('Patient.name.family')}")
```

------------------

### Error Handling and Common Issues

When working with Fhircraft, you may encounter several types of errors. Here's how to handle them:

**Validation Errors**
```python
from pydantic import ValidationError

try:
    invalid_patient = patient_model.model_validate({
        "resourceType": "Patient",
        "gender": "invalid_gender"  # Invalid value
    })
except ValidationError as e:
    print("Validation failed:")
    for error in e.errors():
        print(f"- {error['msg']} at {error['loc']}")
```

**FHIRPath Parsing Errors**
```python
from fhircraft.fhir.path import FhirPathParserError

try:
    result = my_patient.get_fhirpath('Patient.invalid..path')
except FhirPathParserError as e:
    print(f"FHIRPath syntax error: {e}")
```

**Network Issues with Canonical URLs**
```python
import requests

try:
    model = construct_resource_model(
        canonical_url='http://hl7.org/fhir/StructureDefinition/Patient'
    )
except requests.RequestException as e:
    print(f"Failed to fetch structure definition: {e}")
    # Fallback to local file
    model = construct_resource_model(
        structure_definition=load_file('local_patient_definition.json')
    )
```

------------------

### Performance Tips

**Model Caching**
Fhircraft automatically caches constructed models. Subsequent calls with the same structure definition return the cached model instantly:

```python
# First call constructs and caches the model
patient_model_1 = construct_resource_model(canonical_url='...')

# Second call returns cached model (very fast)
patient_model_2 = construct_resource_model(canonical_url='...')

# Clear cache if needed
from fhircraft.fhir.resources.factory import clear_cache
clear_cache()
```

**Local Files vs Canonical URLs**
- **Use local files** for production environments and when you need specific versions
- **Use canonical URLs** for quick prototyping and testing
- **Local files** are faster and don't require internet connectivity

------------------

### Common Pitfalls and Troubleshooting

**Structure Definition Requirements**
```python
# ❌ This will fail - missing snapshot
incomplete_definition = {
    "resourceType": "StructureDefinition",
    "differential": {...}  # Only differential, no snapshot
}

# ✅ This works - includes snapshot
complete_definition = {
    "resourceType": "StructureDefinition", 
    "snapshot": {...},  # Required for Fhircraft
    "differential": {...}  # Optional
}
```

**Choice Element Naming**
```python
# ❌ Wrong - using generic name
observation_data = {
    "value": "some_value"  # This won't work
}

# ✅ Correct - using specific choice element
observation_data = {
    "valueString": "some_value",  # or valueQuantity, valueBoolean, etc.
}
```

**FHIRPath Expression Syntax**
```python
# ❌ Common mistakes
my_patient.get_fhirpath('Patient.name[0].family')  # Arrays use different syntax
my_patient.get_fhirpath('Patient.name.Family')     # Case-sensitive

# ✅ Correct syntax  
my_patient.get_fhirpath('Patient.name.first().family')  # Use first() function
my_patient.get_fhirpath('Patient.name.family')          # Correct case
```

------------------

### Working with FHIR Profiles and Extensions

**Working with FHIR Profiles**
FHIR profiles extend or constrain base resources. Fhircraft can construct models from any valid FHIR profile:

```python
# Example: US Core Patient profile
us_core_patient_model = construct_resource_model(
    canonical_url='http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient'
)

# Validate data against the profile
patient_data = {
    "resourceType": "Patient",
    "identifier": [{
        "system": "http://example.org/patient-ids",
        "value": "12345"
    }],
    "name": [{
        "family": "Doe",
        "given": ["John"]
    }],
    # Additional constraints from US Core profile will be enforced
}

validated_patient = us_core_patient_model.model_validate(patient_data)
```

**Working with Extensions**
Extensions allow additional data elements beyond the base FHIR specification:

```python
# Example: Patient with extension
patient_with_extension = {
    "resourceType": "Patient",
    "id": "example",
    "extension": [{
        "url": "http://example.org/fhir/extensions/patient-importance",
        "valueString": "VIP"
    }],
    "name": [{
        "family": "Smith",
        "given": ["Jane"]
    }]
}

# Access extensions via FHIRPath
importance = my_patient.get_fhirpath(
    "Patient.extension.where(url='http://example.org/fhir/extensions/patient-importance').valueString"
)
```

------------------

### Working with FHIR Data Types

Fhircraft handles FHIR's complex data type system automatically:

**Primitive Types**
```python
# FHIR primitive types are validated according to FHIR rules
patient_data = {
    "resourceType": "Patient",
    "active": True,  # boolean
    "birthDate": "1990-01-01",  # date (YYYY-MM-DD format required)
    "id": "patient123"  # string with specific constraints
}
```

**Choice Elements (value[x])**
```python
# FHIR choice elements allow different data types
observation_data = {
    "resourceType": "Observation",
    "status": "final",
    "code": {"coding": [{"code": "weight"}]},
    # Either valueQuantity, valueString, valueBoolean, etc.
    "valueQuantity": {
        "value": 70.5,
        "unit": "kg"
    }
}
```

------------------

## Getting Help

**📚 Documentation**

- [:material-link-variant: User Guide](user-guide/fhir-resources.md) - Complete documentation of all Fhircraft features

- [:material-book-open-variant: Pydantic Documentation](https://docs.pydantic.dev/latest/) - Learn more about Pydantic's powerful features

- [:material-fire-circle: FHIRPath Documentation](https://hl7.org/fhirpath/N1/) - Official FHIRPath specification

**💬 Community & Support**

- [:material-github: GitHub Issues](https://github.com/luisfabib/fhircraft/issues) - Report bugs or request features

- [:material-github: GitHub Discussions](https://github.com/luisfabib/fhircraft/discussions) - Ask questions and share ideas

**🚀 Next Steps**

Ready to dive deeper? Explore these advanced topics:

1. [Working with FHIR Resources](user-guide/fhir-resources.md) - Advanced model construction and validation

2. [FHIRPath Guide](user-guide/fhirpath.md) - Master the FHIRPath expression language

3. [Code Generation](user-guide/fhir-resources.md#generating-source-code) - Generate reusable Python code from your models