# Configuring Validation Behavior

This guide shows you how to control validation rules when working with FHIR resources. You will learn to adjust validation settings globally or for specific operations, allowing you to work with data that does not meet all FHIR constraints while maintaining appropriate safeguards for your use case.

## Understanding Validation Configuration

When you create FHIR resources with Fhircraft, the library automatically validates them according to FHIR [:material-fire: Conformance rules and Constraints](https://www.hl7.org/fhir/validation.html). These validations ensure data quality and interoperability. However, real-world scenarios sometimes require flexibility. You might receive data from external systems that violate minor constraints, or you might generate resources programmatically where certain warnings do not apply to your workflow.

Fhircraft provides configuration controls that let you adjust validation behavior without modifying your resource construction code. You can disable all warnings, switch between strict and lenient modes, or selectively turn off specific constraint checks. The configuration system uses thread-safe context variables, meaning each part of your application can have different validation settings without interfering with other operations running simultaneously.

Understanding when and how to adjust validation settings helps you balance data quality requirements with practical constraints. Production systems often need different validation configurations than development environments, and batch processing pipelines might use different settings than interactive user interfaces.

## Disabling Validation Warnings

Validation warnings alert you to FHIR data quality issues that do not prevent resource use but indicate potential problems. For example, the dom-6 constraint warns when a resource lacks human-readable narrative text. In production systems processing thousands of resources, these warnings can create excessive log noise without providing actionable information.

Disabling warnings globally affects all FHIR resource operations in your application from that point forward. This setting persists until you change it or restart your application. Validation errors that indicate serious data problems continue to raise exceptions even when warnings are disabled:

```python
# Import the configuration function
from fhircraft import configure

# Disable all validation warnings for the entire application
configure(disable_validation_warnings=True)

# Create FHIR resources without validation warnings appearing
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type
Patient = get_fhir_resource_type("Patient", "R5")

# This patient creation will not show warnings about missing narrative
patient = Patient(name=[{"given": ["Alice"]}])
```

This approach works well for production deployments where you want clean logs and have already validated your data creation logic during development and testing.

## Using Temporary Configuration

Sometimes you need different validation settings for specific operations while keeping your global configuration unchanged. Context managers provide temporary configuration that automatically restores previous settings when the operation completes. This pattern is useful when processing external data, running specific tests, or performing operations that you know will trigger benign warnings.

The context manager creates an isolated configuration scope. Any validation setting changes within the context block only affect operations inside that block. Once execution leaves the block, either normally or through an exception, the previous configuration restores automatically:

```python
from fhircraft import with_config
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

Patient = get_fhir_resource_type("Patient", "R5")

# Temporarily disable warnings for importing external data
with with_config(disable_validation_warnings=True):
    # Warnings are disabled only within this block
    external_patient = Patient(name=[{"given": ["Alice"]}])
    
# Warnings automatically re-enabled after the block ends
local_patient = Patient(name=[{"given": ["Bob"]}])
```

This pattern is particularly valuable in data processing pipelines where some operations work with untrusted external data while others work with your own validated data structures.

## Controlling Specific Constraints

FHIR defines numerous [:material-fire: Invariants and Constraints](https://www.hl7.org/fhir/conformance-rules.html#constraints) that validate resource correctness. Each constraint has a unique key like dom-6, ele-1, or sdf-0. Sometimes you need to disable specific constraints that do not apply to your use case while keeping other validations active. For example, resources generated programmatically might not need narrative text, making the dom-6 constraint inappropriate.

Disabling constraints by key provides surgical precision. You turn off only the validations that cause problems while maintaining all other data quality checks. This approach is safer than disabling all warnings because it preserves most of the validation safety net:

```python
from fhircraft import disable_constraint, enable_constraint
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Disable the dom-6 constraint that requires narrative text
disable_constraint('dom-6')

Patient = get_fhir_resource_type("Patient", "R5")

# Now creating patients without narrative will not trigger dom-6 warnings
patient = Patient(name=[{"given": ["Alice"]}])

# Disable multiple constraints at once
disable_constraint('dom-6', 'sdf-0', 'ele-1')

# Re-enable a specific constraint when you need it again
enable_constraint('dom-6')
```

Constraint keys are documented in the FHIR specification for each resource type. You can find them in the [:material-fire: StructureDefinition snapshots](https://www.hl7.org/fhir/structuredefinition.html) or in validation error messages when they occur.

## Choosing Validation Modes

Fhircraft supports three validation modes that control how the library responds to validation failures. The mode setting affects both warnings and errors, providing coarse-grained control over validation behavior. Each mode serves different use cases in the development and deployment lifecycle.

Strict mode is the default and recommended for most development work. It enforces all FHIR constraints, raising exceptions for errors and emitting Python warnings for minor issues. Lenient mode converts validation errors into warnings, allowing you to process data that technically violates FHIR rules while still seeing what problems exist. Skip mode disables all validation, which is dangerous but occasionally necessary for specific performance-critical scenarios or when working with severely non-compliant data.

### Strict Mode

Strict mode enforces the complete FHIR specification. Validation errors raise exceptions that stop execution, while validation warnings emit Python warnings that appear in logs. This mode catches data quality problems early and enforces compliance with FHIR standards:

```python
from fhircraft import configure
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

# Explicitly set strict mode (this is the default)
configure(validation_mode='strict')

Patient = get_fhir_resource_type("Patient", "R5")

# Validation errors will raise exceptions
# Validation warnings will emit Python warnings
patient = Patient(name=[{"given": ["Alice"]}])
```

### Lenient Mode

Lenient mode converts all validation errors into warnings. Operations that would normally fail due to validation errors instead complete successfully while logging the problems. This mode helps when you need to process FHIR data from external systems that do not fully comply with the specification:

```python
from fhircraft import configure

# Switch to lenient mode for processing external data
configure(validation_mode='lenient')

# Operations that would normally raise validation errors now emit warnings
# This allows processing to continue even with non-compliant data
patient = Patient(name=[{"given": ["Alice"]}])
```

Use lenient mode during data migration, when importing legacy systems, or when you need visibility into validation problems but cannot fix them immediately.

### Skip Mode

Skip mode disables all validation completely. No checks occur, no warnings appear, and no exceptions raise for invalid data. This mode provides maximum performance but removes all data quality safeguards. Use skip mode only in controlled scenarios where you have verified data validity through other means:

```python
from fhircraft import configure

# Disable all validation for maximum performance
configure(validation_mode='skip')

# No validations will be performed at all
# Use only when you have validated data through other means
patient = Patient(name=[{"given": ["Alice"]}])
```

Skip mode is appropriate for high-performance batch processing of pre-validated data or when re-processing resources you have already validated and stored.

## Loading Configuration from Environment Variables

Environment variables provide configuration without modifying code, which helps when deploying applications across different environments. You can set validation behavior through environment variables that Fhircraft reads during initialization. This approach keeps configuration separate from code and makes it easy to adjust settings in production, staging, and development environments.

Fhircraft recognizes specific environment variable names for each configuration option. Set these variables in your shell, container configuration, or deployment scripts before running your application:

```bash
# Set environment variables in your shell or deployment configuration
export FHIRCRAFT_DISABLE_WARNINGS=true
export FHIRCRAFT_VALIDATION_MODE=lenient
export FHIRCRAFT_DISABLED_CONSTRAINTS=dom-6,sdf-0
```

Then load these settings in your application code:

```python
from fhircraft import load_config_from_env

# Load configuration from environment variables
load_config_from_env()

# Configuration now reflects environment variable settings
# No need to call configure() explicitly
```

This pattern works well with container orchestration systems like Docker and Kubernetes where environment variables are the standard configuration mechanism.

## Working with Configuration Objects

The configuration system uses structured objects that you can inspect, modify, and manage programmatically. This provides flexibility for advanced scenarios where you need to query current settings, create custom configurations, or implement configuration management logic:

```python
from fhircraft import get_config, FhircraftConfig, ValidationConfig, set_config

# Get the current active configuration
config = get_config()

# Inspect current validation settings
print(f"Warnings disabled: {config.validation.disable_warnings}")
print(f"Validation mode: {config.validation.mode}")
print(f"Disabled constraints: {config.validation.disabled_constraints}")

# Create a custom configuration object
custom_config = FhircraftConfig(
    validation=ValidationConfig(
        disable_warnings=True,
        disabled_constraints={'dom-6'},
        mode='lenient'
    )
)

# Apply the custom configuration
set_config(custom_config)
```

Configuration objects are immutable after creation, ensuring thread safety and preventing accidental modifications that could affect concurrent operations.

## Resetting to Default Configuration

After experimenting with different validation settings or processing special data, you might want to return to the default configuration. The reset function clears all custom settings and restores Fhircraft to its initial strict validation mode:

```python
from fhircraft import reset_config, configure

# Make some configuration changes
configure(disable_validation_warnings=True, validation_mode='lenient')

# Later, reset everything to defaults
reset_config()

# Now back to strict mode with all warnings enabled
```

Resetting proves useful in test suites where each test should start with clean configuration, or in long-running applications that process different types of data requiring different validation approaches.

## Configuring Multiple Settings Simultaneously

When you need to adjust several validation settings at once, the configure function accepts multiple parameters in a single call. This ensures all changes take effect atomically and makes your configuration code more concise:

```python
from fhircraft import configure

# Configure multiple validation options in one call
configure(
    disable_validation_warnings=True,  # Turn off warnings
    validation_mode='lenient',          # Convert errors to warnings
    disabled_constraints={'dom-6', 'sdf-0'}  # Disable specific constraints
)

# All settings now active together
```

This approach prevents intermediate states where some settings have changed but others have not yet been applied.

## Common Configuration Scenarios

Real-world applications typically need validation configuration in specific patterns. Understanding these common scenarios helps you choose the right configuration strategy for your situation.

### Production Environment Configuration

Production systems usually want clean logs without excessive warning noise, but they still need to catch serious errors. Disable warnings while maintaining strict error checking:

```python
from fhircraft import configure

# Production configuration: disable warnings, keep strict error checking
configure(
    disable_validation_warnings=True,
    validation_mode='strict'
)
```

This configuration reduces log volume while maintaining data quality safeguards.

### Processing External Data

When importing FHIR resources from external systems that might not fully comply with specifications, use lenient mode within a context manager to isolate the relaxed validation:

```python
from fhircraft import with_config

# Function to parse FHIR data from external sources
def parse_external_fhir_data(data):
    # Use lenient mode only for this operation
    with with_config(validation_mode='lenient'):
        # Validation errors become warnings
        return parse_fhir_resource(data)
    # Strict validation resumes after function returns
```

The context manager ensures that your own data creation continues to use strict validation.

### Testing Error Handling

Test suites sometimes need to create intentionally invalid resources to verify error handling code. Skip mode allows creating these resources without triggering validation:

```python
from fhircraft import with_config

def test_error_handling():
    # Disable all validations to create invalid test resources
    with with_config(validation_mode='skip'):
        # Create resource that would normally fail validation
        invalid_resource = create_invalid_resource()
        
        # Test that your error handling code works correctly
        result = your_error_handler(invalid_resource)
        assert result.handled_correctly
```

This pattern isolates validation disabling to just the test scenario without affecting other tests.

### Selective Constraint Disabling

When you generate resources programmatically and know certain constraints do not apply to your workflow, disable those specific constraints while keeping other validations:

```python
from fhircraft import disable_constraint
from fhircraft.fhir.resources.datatypes.R5.core import Observation 

# Disable dom-6 constraint for programmatically generated resources
# This constraint requires human-readable narrative text
disable_constraint('dom-6')

# Now create resources without narrative text triggering warnings
patient = Patient(name=[{"given": ["Alice"], "family": "Smith"}])
observation = Observation(status="final", code={"text": "Temperature"})
```

This surgical approach maintains maximum validation coverage while removing specific unhelpful warnings.


This isolation prevents configuration conflicts in concurrent and parallel processing scenarios.

## Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| Warnings still appear after disabling them | Check that you called configure before creating resources. Configuration does not affect resources already created. Restart your application if using environment variables. |
| Configuration changes do not persist | Use configure() for global changes, not with_config(). Context managers reset configuration after the block ends. |
| Different validation behavior in tests versus production | Ensure test suites call reset_config() before each test. Check that environment variables match between environments. |
| Concurrent operations have wrong validation settings | Verify you are using with_config() context managers to isolate configuration. Avoid modifying global configuration in concurrent code. |
| Cannot find constraint key to disable | Check validation error messages for constraint keys. Refer to [:material-fire: FHIR StructureDefinition snapshots](https://www.hl7.org/fhir/structuredefinition.html) for resource-specific constraints. |

