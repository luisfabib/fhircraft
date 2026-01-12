# Transforming Data with FHIR Mapper

This guide shows you how to convert data between different structures using FHIR mapping rules. Building on the resource models and validation concepts covered earlier, you will learn to transform legacy system data into FHIR resources, convert between different FHIR profiles, and handle complex data transformations with automatic validation.

## What Is FHIR Mapping

Healthcare data exists in countless formats across different systems, databases, and file structures. Converting this data into standardized FHIR resources manually would require writing custom transformation code for each source format, leading to maintenance challenges and inconsistent implementations. FHIR Mapping Language provides a standardized, declarative way to describe these transformations.

Fhircraft implements the [:material-fire: FHIR Mapping Language](https://hl7.org/fhir/mapping-language.html) specification, which lets you write transformation rules that describe what the end result should look like rather than step-by-step instructions on how to build it. The mapper executes these rules, handles data type conversions, manages nested structures, and automatically validates output against FHIR specifications. This approach separates transformation logic from application code, making it easier to maintain, audit, and share mapping rules.

The mapping language is particularly valuable in healthcare integration scenarios where you need repeatable, auditable transformations. Every mapped resource is automatically validated using the resource models discussed in earlier sections, ensuring that transformed data complies with FHIR constraints before it reaches your application. However, note that the FHIR Mapping Language is specified as [:material-fire: Maturity Level 0 (Draft)](https://hl7.org/fhir/versions.html#maturity), meaning both the specification and implementations may change as the standard evolves.

## Basic Data Transformation

The simplest way to understand FHIR mapping is through a complete example that transforms legacy patient data into a standard FHIR Patient resource. This example demonstrates the core concepts: defining the mapping, writing transformation rules, and executing the transformation.

Legacy systems often use different field names and value formats than FHIR expects. The mapping script below shows how to convert a simple patient record with fields like firstName and sex into a FHIR-compliant Patient resource with the proper structure:

```python
# Import the FHIR mapper
from fhircraft.fhir.mapper import FHIRMapper

# Legacy system data with non-FHIR field names
legacy_patient = {
    "firstName": "Alice",
    "lastName": "Johnson",
    "dob": "1985-03-15",  # Date of birth
    "sex": "F"             # Single character gender code
}

# Mapping script defines transformation rules
mapping_script = """
map 'http://example.org/legacy-to-fhir' = 'LegacyPatient'

group main(source legacy, target patient: Patient) {
    // Map name fields to FHIR name structure
    legacy -> patient.name as name then {
        legacy.firstName -> name.given;
        legacy.lastName -> name.family;
    };
    // Copy birth date directly
    legacy.dob -> patient.birthDate;
    // Convert sex code to FHIR gender values
    legacy.sex where($this = 'F') -> patient.gender = 'female';
    legacy.sex where($this = 'M') -> patient.gender = 'male';
}
"""

# Create mapper and execute the transformation
mapper = FHIRMapper()
targets = mapper.execute_mapping(mapping_script, legacy_patient)
patient = targets[0]  # Get the transformed Patient resource

print(f"Transformed: {patient}")
```

## Understanding Mapping Benefits and Use Cases

FHIR Mapping Language provides advantages over writing custom transformation code in several important ways. The declarative approach means you describe what data should look like in the target format rather than writing step-by-step instructions. This makes mapping rules more readable and easier for non-programmers to understand and review. Healthcare domain experts can often read and verify mapping logic without deep programming knowledge.

Automatic validation is built into every transformation. The mapper validates output against [:material-fire: FHIR Constraints and Invariants](https://www.hl7.org/fhir/conformance-rules.html#constraints) as resources are constructed, catching structural errors and data quality issues before they propagate through your system. This validation uses the same resource models covered in earlier sections, ensuring consistency across your application.

Mapping rules are also portable and reusable. Because they follow the standard FHIR specification, you can share mapping definitions between systems and organizations. A mapping you create can work in other FHIR implementations, and mappings created by others can work in Fhircraft. This interoperability reduces duplication and promotes consistent transformation logic across the healthcare ecosystem.

### Choosing When to Use Mapping

Mapping works best for standardized, repeatable transformations where you need validation and auditability. Converting legacy EHR data to FHIR resources, transforming between FHIR profiles like [:material-fire: US Core](https://www.hl7.org/fhir/us/core/) and [:material-fire: International Patient Summary](https://hl7.org/fhir/uv/ips/), and normalizing data from multiple sources with different schemas are all ideal mapping scenarios. Complex nested structures and consistent business rules also benefit from the declarative approach.

However, some situations work better with direct Python code. Simple one-to-one field copying without validation needs, one-time data migrations where you will not reuse the mapping logic, or performance-critical paths where microseconds matter might be better served by custom code. When source and target structures are identical or when you need complex procedural logic that does not fit the declarative model, direct coding may be more appropriate.

## Writing Mapping Rules

Every FHIR mapping follows a consistent structure defined by the [:material-fire: FHIR Mapping Language specification](https://hl7.org/fhir/mapping-language.html). Understanding these components helps you read existing mappings and create your own transformation rules.

The map declaration identifies the mapping with a unique URL and human-readable name. Uses statements declare the [:material-fire:  Structure Definitions](https://www.hl7.org/fhir/structuredefinition.html) for source and target data, telling the mapper what data types to expect. Groups contain the actual transformation rules that describe how to move and transform data from source to target structures. Each group can call other groups, allowing you to organize complex mappings into manageable pieces.

### Direct Field Mapping

The simplest transformation type copies values directly from source fields to target fields without modification. This approach works when source and target use compatible data types and the values need no transformation. The mapping syntax uses arrows to indicate data flow from left to right:

```python
from fhircraft.fhir.mapper import FHIRMapper

# Define simple field-to-field mappings
script = """
map 'http://example.org/simple-mapping' = 'SimpleMapping'

group main(source src, target tgt) {
    // Copy fields directly without transformation
    src.name -> tgt.fullName;     
    src.age -> tgt.yearsOld;       
    src.email -> tgt.contactEmail;
}
"""

# Source data to transform
source_data = {"name": "John Doe", "age": 30, "email": "john@example.com"}

# Execute the mapping
mapper = FHIRMapper()
targets = mapper.execute_mapping(script, source_data)

print(f"Result: {targets[0]}")
```

### Mapping to FHIR Resources

When your target is a FHIR resource rather than a simple data structure, you specify the structure definition in the uses statement. This tells the mapper to validate the output against FHIR rules and create properly typed resource objects. The mapper uses the same model construction system covered in earlier sections, ensuring consistent validation across your application.

FHIR resources have specific required fields, data types, and constraints. By declaring the target type as a FHIR resource, the mapper enforces these rules automatically. If your transformation produces invalid data, you receive clear error messages indicating which constraints failed:

```python
# Transform to a validated FHIR Patient resource
script = """
map 'http://example.org/patient-mapping' = 'PatientMapping'

uses "http://hl7.org/fhir/StructureDefinition/Patient" alias Patient as target

group main(source legacy, target patient: Patient) {
    // Create nested name structure in FHIR format
    legacy -> patient.name as name then {
        legacy.firstName -> name.given;
        legacy.lastName -> name.family;
    };
    // Copy birth date to FHIR date field
    legacy.dob -> patient.birthDate;
    // Transform gender codes using conditional rules
    legacy.sex where($this = 'F') -> patient.gender = 'female';
    legacy.sex where($this = 'M') -> patient.gender = 'male';
}
"""

# Legacy system data
legacy_data = {
    "firstName": "Alice", 
    "lastName": "Johnson",
    "dob": "1985-03-15",
    "sex": "F"
}

# Execute mapping and get validated FHIR resource
targets = mapper.execute_mapping(script, legacy_data)
patient = targets[0]  # This is a validated FHIR Patient resource

print(f"Patient ID: {patient.id}")
```

## Handling Complex Transformations

Real-world data transformations often involve nested structures, collections, and conditional logic. FHIR resources themselves are hierarchical, with objects containing other objects and arrays of repeating elements. The mapping language provides constructs to handle these complex scenarios while maintaining readability.

### Working with Nested Structures

FHIR resources organize data hierarchically. A Patient has name objects, which contain given and family elements. Addresses have line arrays, city, state, and postal code fields. The mapping language uses the then keyword to navigate into these nested structures, creating intermediate objects as needed.

When you map into a nested structure, the mapper creates the parent objects automatically. You do not need to explicitly construct each level of the hierarchy. The transformation rules describe the desired final structure, and the mapper builds it appropriately:

```python
script = """
map 'http://example.org/nested' = 'NestedMapping'

group main(source src, target patient: Patient) {
    // Navigate into nested name structure
    src -> patient.name as name then {
        src.fullName -> name.text;      // Human-readable full name
        src.firstName -> name.given;    // Given name element
        src.lastName -> name.family;    // Family name element
    };
    
    // Transform array of phone numbers to telecom array
    src.phoneNumbers as phones -> patient.telecom as telecom then {
        phones.number -> telecom.value;   // Contact value
        phones.type -> telecom.system;    // Contact type (phone/email)
    };
    
    // Conditionally map emergency contact if it exists
    src.emergencyContact where(exists()) as contact -> patient.contact as contact then {
        // Map contact name into nested structure
        contact.name -> contact.name.text;
        // Map relationship into nested structure
        contact.relationship -> contact.relationship.text;
    };
}
"""

# Source data with nested and array structures
source_data = {
    "fullName": "Alice Johnson",
    "firstName": "Alice",
    "lastName": "Johnson",
    "phoneNumbers": [
        {"number": "555-0123", "type": "phone"},
    ],
    "emergencyContact": {
        "name": "Bob Johnson",
        "relationship": "spouse"
    }
}

targets = mapper.execute_mapping(script, source_data)
```

### Organizing with Multiple Groups

Complex transformations benefit from organization into logical sections. The mapping language allows you to define multiple groups that handle different aspects of the transformation. This modularity makes mappings easier to understand, test, and maintain. You can focus on one transformation concern at a time rather than managing all rules in a single large group.

Groups can call other groups, creating a hierarchy of transformation logic. The main group typically orchestrates the overall transformation, calling specialized groups for specific data domains. This pattern mirrors good programming practice by separating concerns and promoting reusability:

```python
script = """
map 'http://example.org/multi-group' = 'MultiGroup'

// Main group orchestrates the transformation
group main(source src, target patient: Patient) {
    src -> patient then demographics(src, patient);  // Handle demographics data
    src -> patient then contacts(src, patient);      // Handle contact information
    src -> patient then identifiers(src, patient);   // Handle identifiers
}

// Group focused on demographic fields
group demographics(source src, target patient: Patient) {
    src.name -> patient.name as name then {
        src.name -> name.text;
    };
    src.birthDate -> patient.birthDate;
    src.gender -> patient.gender;
}

// Group focused on contact information
group contacts(source src, target patient: Patient) {
    src.phone as phone -> patient.telecom as tel then {
        phone -> tel.value, tel.system='phone';
    };
    src.email as email -> patient.telecom as email then {
        email -> email.value, email.system='email';
    };
}

// Group focused on identifier mappings
group identifiers(source src, target patient: Patient) {
    src.ssn -> patient.identifier as id then {
        ssn -> id.value, id.system='http://hl7.org/fhir/sid/us-ssn';
    };
}
"""

# Execute the entire mapping (all groups)
targets = mapper.execute_mapping(script, source_data)

# Or execute only a specific group for testing
targets = mapper.execute_mapping(script, source_data, group="demographics")
```

## Combining Multiple Data Sources

Real-world scenarios often require merging data from multiple systems or databases into a single FHIR resource. Patient demographics might come from one system while insurance information comes from another. Lab results might reference patient and provider data stored separately. The mapping language supports multiple source parameters, allowing you to pull data from different sources in a single transformation.

When you define multiple source parameters in a group, you pass the source data as a tuple when executing the mapping. The mapper correlates each source parameter with the corresponding data object. This approach maintains clear separation between different data sources while allowing them to contribute to the same target resource:

```python
script = """
map 'http://example.org/multi-source' = 'MultiSource'

// Define two separate source parameters
group main(source demographics, source insurance, target patient: Patient) {
    // Pull demographic fields from first source
    demographics.name -> patient.name as name then {
        demographics.name -> name.text;
    };
    demographics.birthDate -> patient.birthDate;
    demographics.gender -> patient.gender;
    
    // Pull insurance data from second source
    insurance -> patient.identifier as id then {
        insurance.policyNumber -> id.value;       // Policy number as identifier
        insurance.carrier -> id.system;           // Insurance carrier as system
        insurance.memberSince -> id.period as period then {
            insurance.memberSince -> period.start;  // Coverage start date
        };
    };
}
"""

# Demographics from one system
demo_data = {
    "name": "Alice Johnson",
    "birthDate": "1985-03-15",
    "gender": "female"
}

# Insurance from another system
insurance_data = {
    "policyNumber": "POL-12345",
    "carrier": "ACME Insurance",
    "memberSince": "2020-01-01"
}

# Pass both sources as a tuple
targets = mapper.execute_mapping(
    script,
    (demo_data, insurance_data)
)

patient = targets[0]  # Single Patient resource combining both sources
```

## Managing Mapping Definitions

While inline mapping scripts work well for examples and simple transformations, production systems benefit from storing mapping definitions separately from application code. FHIR defines the [:material-fire: StructureMap Resource](https://www.hl7.org/fhir/structuremap.html) to represent mapping definitions in a standardized format. These definitions can live in files, databases, or FHIR servers, making them easy to version, share, and manage.

### Loading from Files and URLs

Storing mappings in files separates transformation logic from application code, making it easier for healthcare informaticists to maintain mapping rules without changing Python code. Loading from URLs enables organizations to publish and share mapping definitions through FHIR servers or web endpoints:

```python
from fhircraft.fhir.mapper import FHIRMapper

mapper = FHIRMapper()

# Load mapping definition from a local JSON file
structure_map = mapper.load_structure_map("patient-mapping.json")

# Execute the loaded mapping
targets = mapper.execute_mapping(structure_map, source_data)

# Load mapping from a FHIR server or web URL
structure_map = mapper.load_structure_map(
    "https://example.org/fhir/StructureMap/PatientMapping"
)

# Execute mapping loaded from URL
targets = mapper.execute_mapping(structure_map, source_data)
```

## Handling Mapping Errors

Mapping failures can occur for several reasons: invalid mapping syntax, missing source fields, data type mismatches, or FHIR validation failures. Understanding these error types helps you diagnose and fix transformation problems quickly. The mapper provides detailed error information including which rule failed and what data was being processed.

Mapping errors occur when transformation rules cannot execute, such as when source data lacks required fields or when conditional expressions evaluate incorrectly. Validation errors occur when the transformed output violates FHIR constraints. Both error types provide context to help you identify and resolve the problem:

```python
from fhircraft.fhir.mapper import FHIRMapper
from fhircraft.fhir.mapper.engine.exceptions import MappingError
from pydantic import ValidationError

mapper = FHIRMapper()

try:
    # Attempt the mapping transformation
    targets = mapper.execute_mapping(structure_map, source_data)
    patient = targets[0]
    
except MappingError as e:
    # Mapping execution failed
    print(f"Mapping failed: {e}")
    print(f"Failed rule: {e.rule_path}")  # Which rule caused the error
    print(f"Data context: {e.context}")   # What data was being processed
    
except ValidationError as e:
    # Output failed FHIR validation
    print(f"FHIR validation failed: {e}")
    print(f"Invalid fields: {e.errors()}")  # Which fields are invalid
```

When debugging mapping failures, examine the error message and context carefully. The rule path shows which transformation rule failed, while the context shows the actual data being processed. This information helps you identify whether the problem is incorrect mapping logic or unexpected source data.

## Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| Mapping syntax errors | Check the [:material-fire: FHIR Mapping Language syntax](https://hl7.org/fhir/mapping-language.html). Ensure proper use of semicolons, parentheses, and keywords. Validate mapping scripts using FHIR validation tools. |
| Source field not found | Verify source data contains expected fields. Check field name spelling and case sensitivity. Use conditional expressions with where(exists()) to handle optional fields. |
| Target validation failures | Review [:material-fire: FHIR Resource Validation Rules](https://www.hl7.org/fhir/validation.html). Ensure required fields are populated. Check that values match expected data types and value sets. |
| Type conversion errors | Verify source and target data types are compatible. Add explicit conversion logic for incompatible types. Use transformation functions to convert between formats. |
| Nested structure issues | Use then clauses to navigate into nested structures. Ensure intermediate objects are created with as clauses. Check that nested field paths are correct. |
| Performance with large datasets | Load mappings once and reuse the mapper instance. Consider batch processing for very large datasets. Profile mapping execution to identify slow rules. |
| Multiple target resources | Specify multiple target parameters in group definitions. The execute_mapping result contains all target resources in order. |