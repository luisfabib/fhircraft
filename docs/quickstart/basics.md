# Basics 

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

Fhircraft provides a robust FHIRPath engine with an enhanced interface, allowing you to query and modify FHIR resources using standard FHIRPath expressions directly in Python. This enables expressive, standards-compliant access to deeply nested data and supports both retrieval and update operations.

**Example: Accessing Values with FHIRPath**

The enhanced interface provides multiple methods for retrieving values based on your specific needs:

```python
from fhircraft.fhir.path import fhirpath

# Parse the FHIRPath expression
name_path = fhirpath.parse('Patient.name.family')

# Get all matching values as a list (always returns a list)
all_family_names = name_path.values(my_patient)
# Returns: ['Doe', 'Smith'] if patient has multiple names

# Get a single value (raises error if multiple values found)
family_name = name_path.single(my_patient)
# Returns: 'Doe' or raises FHIRPathRuntimeError if multiple names exist

# Get the first value (safe for multiple values)
first_family_name = name_path.first(my_patient)
# Returns: 'Doe' (first family name) or None if no names

# Get the last value
last_family_name = name_path.last(my_patient)
# Returns: 'Smith' (last family name) or None if no names

# Check if values exist
has_family_name = name_path.exists(my_patient)
# Returns: True if patient has any family names

# Count matching values
name_count = name_path.count(my_patient)
# Returns: 2 if patient has 2 family names

# Check if path is empty
is_empty = name_path.is_empty(my_patient)
# Returns: True if patient has no family names
```

**Example: Updating Values with FHIRPath**

```python
# Update all matching values
name_path.update_values(my_patient, 'NewFamilyName')
# Sets all family names to 'NewFamilyName'

# Update a single value (safer for single-value fields)
gender_path = fhirpath.parse('Patient.gender')
gender_path.update_single(my_patient, 'female')
# Sets gender to 'female', raises error if multiple gender values exist
```

**Example: Using Default Values**

```python
# Get values with fallback defaults
birth_date = fhirpath.parse('Patient.birthDate').first(my_patient, default='1900-01-01')
# Returns actual birth date or '1900-01-01' if not set

phone = fhirpath.parse('Patient.telecom.where(system="phone").value').single(
    my_patient, 
    default='No phone number'
)
# Returns phone number or default message if not found
```

With these methods, you can efficiently navigate and manipulate FHIR resources, making complex data operations straightforward and Pythonic.

------------------

### Complete Example: End-to-End Workflow

Here's a complete example that demonstrates the entire workflow from constructing a model to validating and manipulating FHIR data:

```python
from fhircraft.fhir.resources.factory import construct_resource_model
from fhircraft.fhir.path import fhirpath
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
family_name_path = fhirpath.parse('Patient.name.family')

# Get the family name
family_name = family_name_path.first(my_patient)
print(f"Family name: {family_name}")

# Update the family name
family_name_path.update_values(my_patient, 'Smith')
updated_name = family_name_path.first(my_patient)
print(f"Updated family name: {updated_name}")

# Check other information
gender_path = fhirpath.parse('Patient.gender')
if gender_path.exists(my_patient):
    gender = gender_path.single(my_patient)
    print(f"Patient gender: {gender}")

# Count given names
given_names_path = fhirpath.parse('Patient.name.given')
given_count = given_names_path.count(my_patient)
print(f"Number of given names: {given_count}")
```

--------------------

## Getting Help

**📚 Documentation**

- [:material-link-variant: User Guide](../user-guide/fhir-models.md) - Complete documentation of all Fhircraft features

- [:material-book-open-variant: Pydantic Documentation](https://docs.pydantic.dev/latest/) - Learn more about Pydantic's powerful features

- [:material-fire-circle: FHIRPath Documentation](https://hl7.org/fhirpath/N1/) - Official FHIRPath specification

**💬 Community & Support**

- [:material-github: GitHub Issues](https://github.com/luisfabib/fhircraft/issues) - Report bugs or request features

- [:material-github: GitHub Discussions](https://github.com/luisfabib/fhircraft/discussions) - Ask questions and share ideas

**🚀 Next Steps**

Ready to dive deeper? Explore these advanced topics:

1. [Pydantic representation of FHIR](../user-guide/pydantic-representation.md) - Detailed description of how Fhircraft represents FHIR within Pydantic

2. [Working with Fhircraft Models](../user-guide/fhir-models.md) - Advanced model construction and validation

3. [FHIRPath Guide](../user-guide/fhirpath.md) - Master the FHIRPath expression language

