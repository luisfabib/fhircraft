---
icon: lucide/bolt
--- 

# Configuring Validation Behavior

This guide shows you how to control validation rules when working with FHIR resources. You will learn to adjust validation settings globally or for specific operations, allowing you to work with data that does not meet all FHIR constraints while maintaining appropriate safeguards for your use case.

## Understanding Validation Configuration

When you create FHIR resources with Fhircraft, the library automatically validates them according to FHIR [:lucide-flame: Conformance rules and Constraints](https://www.hl7.org/fhir/validation.html). These validations ensure data quality and interoperability. However, real-world scenarios sometimes require flexibility. You might receive data from external systems that violate minor constraints that do not affect your application's logic, or you might generate resources programmatically where certain warnings do not apply to your workflow. Furthermore, validation of large and heavily constrained resources can lead to significant overhead.

Fhircraft provides configuration controls that let you adjust validation behavior without modifying your resource construction code. You can disable all warnings, switch between strict and lenient modes, or selectively turn off specific constraint checks. The configuration system uses thread-safe context variables, meaning each part of your application can have different validation settings without interfering with other operations running simultaneously.

Understanding when and how to adjust validation settings helps you balance data quality requirements with practical constraints such as performance. Production systems often need different validation configurations than development environments, and batch processing pipelines might use different settings than interactive user interfaces.

!!! info "See also"

    For details on catching and handling the exceptions that validation raises, see [Error Handling](error-handling.md).

## Disabling Validation Warnings

Validation warnings alert you to FHIR data quality issues that do not prevent resource use but indicate potential problems or best-practice recommendations. For example, the `dom-6` constraint warns when a resource lacks human-readable narrative text. In production systems processing thousands of resources, these warnings can create excessive log noise without providing actionable information.

Disabling warnings globally affects all FHIR resource operations in your application from that point forward. This setting persists until you change it or restart your application. Validation errors that indicate serious data problems continue to raise `ValidationError` even when warnings are disabled:

```python
# Import the configuration function
from fhircraft import configure

# Disable all validation warnings for the entire application
configure(disable_validation_warnings=True)

# Create FHIR resources without validation warnings appearing
from fhircraft import R5 as fhir
# This patient creation will not show warnings about missing narrative
patient = fhir.Patient(name=[{"given": ["Alice"]}])
```

This approach works well for production deployments where you want clean logs and have already validated your data creation logic during development and testing.

## Using Temporary Configuration

Sometimes you need different validation settings for specific operations while keeping your global configuration unchanged. Context managers provide temporary configuration that automatically restores previous settings when the operation completes. This pattern is useful when processing external data, running specific tests, or performing operations that you know will trigger benign warnings.

The context manager `override_config` creates an isolated configuration scope. Any validation setting changes within the context block only affect operations inside that block. Once execution leaves the block, either normally or through an exception, the previous configuration restores automatically:

```python
from fhircraft import override_config
# Temporarily disable warnings for importing external data
with override_config(disable_validation_warnings=True):
    # Warnings are disabled only within this block
    external_patient = fhir.Patient(name=[{"given": ["Alice"]}])
    
# Warnings automatically re-enabled after the block ends
local_patient = fhir.Patient(name=[{"given": ["Bob"]}])
```

This pattern is particularly valuable in data processing pipelines where some operations work with untrusted external data while others work with your own validated data structures.

## Controlling Specific Constraints

FHIR defines numerous [:lucide-flame: Invariants and Constraints](https://www.hl7.org/fhir/conformance-rules.html#constraints) that validate resource correctness. Each constraint has a unique key like `dom-6`, `ele-1`, or `sdf-0`. Sometimes you need to disable specific constraints that do not apply to your use case while keeping other validations active. For example, resources generated programmatically might not need narrative text, making the `dom-6` constraint inappropriate.

Disabling constraints by key provides surgical precision. You turn off only the validations that cause problems while maintaining all other data quality checks. This approach is safer than disabling all warnings because it preserves most of the validation safety net:

```python
from fhircraft import disable_constraint, enable_constraint

# Disable the dom-6 constraint that requires narrative text
disable_constraint('dom-6')

# Now creating patients without narrative will not trigger dom-6 warnings
patient = fhir.Patient(name=[{"given": ["Alice"]}])

# Disable multiple constraints at once
disable_constraint('dom-6', 'sdf-0', 'ele-1')

# Re-enable a specific constraint when you need it again
enable_constraint('dom-6')
```

Constraint keys are documented in the FHIR specification for each resource type. You can find them in the [:lucide-flame: StructureDefinition snapshots](https://www.hl7.org/fhir/structuredefinition.html) or in validation error messages when they occur.

## Choosing Validation Modes

Fhircraft supports three validation modes that control how the library responds to validation failures. The mode setting affects both warnings and errors, providing coarse-grained control over validation behavior. Each mode serves different use cases in the development and deployment lifecycle.

### Strict Mode

Strict mode enforces the complete set of FHIR constraints. FHIR constraint violations raise Pydantic's `ValidationError` (wrapping a `PydanticCustomError` per constraint) that stops execution, while validation warnings emit Python warnings that appear in logs. This mode catches data quality problems early and enforces compliance with FHIR standards:

```python hl_lines="5"
from fhircraft import configure

# Explicitly set strict mode (this is the default)
configure(validation_mode='strict')

# Validation errors will raise ValidationError
# Validation warnings will emit Python warnings
patient = fhir.Patient(name=[{"given": ["Alice"]}])
```

### Lenient Mode

Lenient mode converts all validation errors into warnings. Operations that would normally fail due to validation errors instead complete successfully while logging the problems. This mode helps when you need to process FHIR data from external systems that do not fully comply with the specification:

```python hl_lines="4"
from fhircraft import configure

# Switch to lenient mode for processing external data
configure(validation_mode='lenient')

# Operations that would normally raise validation errors now emit warnings
patient = fhir.Patient(name=[{"given": ["Alice"]}]) #(1)!
```
1. This allows processing to continue even with non-compliant data

Use lenient mode during data migration, when importing legacy systems, or when you need visibility into validation problems but cannot fix them immediately.

### Skip Mode

Skip mode disables all validation completely. No checks occur, no warnings appear, and no exceptions raise for invalid data. This mode provides maximum performance but removes all data quality safeguards. Use skip mode only in controlled scenarios where you have verified data validity through other means:

```python hl_lines="4"
from fhircraft import configure

# Disable all validation for maximum performance
configure(validation_mode='skip')

# No validations will be performed at all 
patient = fhir.Patient(name=[{"given": ["Alice"]}]) #(1)!
```

1. Use only when you have validated data through other means

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
load_config_from_env() # (1)!
```
1. Configuration now reflects environment variable settings. No need to call configure() explicitly

This pattern works well with container orchestration systems like Docker and Kubernetes where environment variables are the standard configuration mechanism.

## Working with Configuration Objects

The configuration system uses structured `FhircraftConfig` objects that you can inspect, modify, and manage programmatically. This provides flexibility for advanced scenarios where you need to query current settings, create custom configurations, or implement configuration management logic:

```python
from fhircraft import get_config

# Get the current active configuration
config = get_config()

# Inspect current validation settings
print(f"Warnings disabled: {config.disable_validation_warnings}")
print(f"Validation mode: {config.validation_mode}")
print(f"Disabled constraints: {config.disabled_fhir_constraints}")
```

Configuration objects are immutable after creation, ensuring thread safety and preventing accidental modifications that could affect concurrent operations.

## Resetting to Default Configuration

After experimenting with different validation settings or processing special data, you might want to return to the default configuration. The `reset_config` function clears all custom settings and restores Fhircraft to its initial strict validation mode:

```python
from fhircraft import reset_config, configure

# Make some configuration changes
configure(disable_validation_warnings=True, validation_mode='lenient')

# Later, reset everything to defaults
reset_config()

# Now back to strict mode with all warnings enabled
```

Resetting proves useful in test suites where each test should start with clean configuration, or in long-running applications that process different types of data requiring different validation approaches.

## Configuring the Terminology Service

Fhircraft's FHIRPath terminology functions — `memberOf()`, `subsumes()`, and `subsumedBy()` — require a terminology service to produce results. You provide one by registering an object that implements the `TerminologyService` protocol from `fhircraft.fhir.terminology`.

### The `TerminologyService` Protocol

The protocol uses Python structural subtyping, so your class does not need to inherit from anything. It just needs to implement the relevant methods:

```python
from fhircraft.fhir.terminology import TerminologyService

class MyTerminologyService:
    """Delegates terminology operations to a remote FHIR server."""

    def validate_valueset_code(self, *, url=None, code=None, system=None,
                               version=None, display=None) -> bool:
        # ValueSet/$validate-code
        ...

    def validate_codesystem_code(self, *, url=None, code=None,
                                 version=None, display=None) -> bool:
        # CodeSystem/$validate-code
        ...

    def codesystem_lookup(self, *, code, system=None, version=None):
        # CodeSystem/$lookup
        ...

    def codesystem_subsumes(self, codeA, codeB, system=None, version=None):
        # CodeSystem/$subsumes
        ...

# Verify structural compatibility at runtime
assert isinstance(MyTerminologyService(), TerminologyService)
```

You only need to implement the methods that your application actually calls. Unimplemented methods that raise `NotImplementedError` are handled gracefully by the FHIRPath engine — they cause the function to return an empty collection rather than crashing.

### Registering Globally

Use `configure()` to set a default terminology service for the entire application. The service is then used automatically by all `memberOf()`, `subsumes()`, and `subsumedBy()` FHIRPath evaluations:

```python
from fhircraft import configure

configure(terminology_service=MyTerminologyService())
```

### Clearing the Service

Pass `None` explicitly to remove a previously registered service:

```python
from fhircraft import configure

configure(terminology_service=None)  # (1)!
```

1. Omitting the argument entirely leaves the existing service unchanged. Only `None` clears it.

### Scoped Service with `override_config`

Use `override_config` when you need a different terminology service for a specific block of code without affecting the global configuration:

```python
from fhircraft import override_config

with override_config(terminology_service=MyTerminologyService()):
    # All FHIRPath evaluations in this block use the staging service
    result = fhir.Observation(status="final", code={"coding":[{"code":"LP-12292"}]}).fhirpath_single(
        "Observation.code.memberOf('http://example.org/ValueSet/LabCodes')"
    )

# Global service (or no service) is automatically restored after the block
```

## Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| Warnings still appear after disabling them | Check that you called configure before creating resources. Configuration does not affect resources already created. Restart your application if using environment variables. |
| Configuration changes do not persist | Use configure() for global changes, not override_config(). Context managers reset configuration after the block ends. |
| Different validation behavior in tests versus production | Ensure test suites call reset_config() before each test. Check that environment variables match between environments. |
| Concurrent operations have wrong validation settings | Verify you are using override_config() context managers to isolate configuration. Avoid modifying global configuration in concurrent code. |
| Cannot find constraint key to disable | Check validation error messages for constraint keys. Refer to [:lucide-flame: FHIR StructureDefinition snapshots](https://www.hl7.org/fhir/structuredefinition.html) for resource-specific constraints. |

