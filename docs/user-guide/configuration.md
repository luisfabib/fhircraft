# FHIRcraft Configuration System

## Overview

The FHIRcraft configuration system allows you to customize validation behavior globally or temporarily within specific code blocks. This is useful when you need to:

- Disable validation warnings in production
- Work with FHIR resources that may not be fully compliant
- Test error handling without triggering validations
- Selectively disable specific constraints

## Quick Start

### Disabling All Validation Warnings

```python
from fhircraft import configure

# Disable all validation warnings globally
configure(disable_validation_warnings=True)

# Now create FHIR resources without validation warnings
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type
Patient = get_fhir_resource_type("Patient", "R5")
patient = Patient(name=[{"given": ["Alice"]}])
```

### Temporary Configuration with Context Manager

```python
from fhircraft import with_config

# Temporarily disable warnings for a specific operation
with with_config(disable_validation_warnings=True):
    patient = Patient(name=[{"given": ["Alice"]}])  # Warnings disabled here
# Warnings re-enabled automatically after the block
```

### Disabling Specific Constraints

```python
from fhircraft import disable_constraint

# Disable the 'dom-6' constraint (narrative warning)
disable_constraint('dom-6')

# Disable multiple constraints
disable_constraint('dom-6', 'sdf-0', 'ele-1')

# Re-enable a constraint
from fhircraft import enable_constraint
enable_constraint('dom-6')
```

## Validation Modes

### Strict Mode (Default)

All validations are enabled. Errors raise exceptions, warnings emit Python warnings.

```python
from fhircraft import configure

configure(validation_mode='strict')
```

### Lenient Mode

Converts all validation errors to warnings. Useful when working with potentially invalid data.

```python
configure(validation_mode='lenient')

# This would normally raise an error, but now emits a warning
patient = Patient(name=[{"given": ["Alice"]}])
```

### Skip Mode

Disables all validations completely. Use with caution!

```python
configure(validation_mode='skip')

# No validations will be performed
patient = Patient(name=[{"given": ["Alice"]}])
```

## Environment Variables

Configure FHIRcraft using environment variables:

```bash
export FHIRCRAFT_DISABLE_WARNINGS=true
export FHIRCRAFT_VALIDATION_MODE=lenient
export FHIRCRAFT_DISABLED_CONSTRAINTS=dom-6,sdf-0
```

Then in your code:

```python
from fhircraft import load_config_from_env

load_config_from_env()
```

## Advanced Usage

### Working with the Config Object

```python
from fhircraft import get_config, FhircraftConfig, ValidationConfig

# Get current configuration
config = get_config()
print(f"Warnings disabled: {config.validation.disable_warnings}")
print(f"Mode: {config.validation.mode}")

# Create custom configuration
custom_config = FhircraftConfig(
    validation=ValidationConfig(
        disable_warnings=True,
        disabled_constraints={'dom-6'},
        mode='lenient'
    )
)

from fhircraft import set_config
set_config(custom_config)
```

### Resetting Configuration

```python
from fhircraft import reset_config

# Reset to default configuration
reset_config()
```

### Multiple Configuration Changes

```python
from fhircraft import configure

# Configure multiple options at once
configure(
    disable_validation_warnings=True,
    validation_mode='lenient',
    disabled_constraints={'dom-6', 'sdf-0'}
)
```

## Configuration Options

### `FhircraftConfig`

Main configuration class that can be extended for future features.

**Attributes:**
- `validation`: `ValidationConfig` - Validation-specific settings

### `ValidationConfig`

Validation behavior configuration.

**Attributes:**
- `disable_warnings` (bool): Disable all validation warnings
- `disabled_constraints` (Set[str]): Set of constraint keys to disable
- `disable_warning_severity` (bool): Disable only warning-level constraints
- `disable_errors` (bool): Disable error-level constraints (dangerous!)
- `mode` (str): Validation mode - 'strict', 'lenient', or 'skip'

## Best Practices

1. **Use context managers for temporary changes**: This ensures configuration is properly restored and doesn't affect other parts of your code.

2. **Be cautious with `mode='skip'`**: Disabling all validations can lead to invalid FHIR resources. Only use in controlled scenarios.

3. **Document your configuration**: If you disable validations globally, document why in your code.

4. **Test with validations enabled**: Even if you disable warnings in production, test with validations enabled to catch issues early.

5. **Use specific constraint disabling**: Instead of disabling all warnings, disable specific constraints you know are problematic.

## Examples

### Example 1: Production Configuration

```python
from fhircraft import configure

# In production, disable warnings but keep errors
configure(
    disable_validation_warnings=True,
    validation_mode='strict'
)
```

### Example 2: Working with External Data

```python
from fhircraft import with_config

# When parsing external FHIR data that may not be fully compliant
def parse_external_fhir_data(data):
    with with_config(validation_mode='lenient'):
        return parse_fhir_resource(data)
```

### Example 3: Testing Error Handling

```python
from fhircraft import with_config

def test_error_handling():
    # Temporarily disable validations to test error handling
    with with_config(validation_mode='skip'):
        invalid_resource = create_invalid_resource()
        # Test your error handling logic
```

### Example 4: Selective Validation

```python
from fhircraft import disable_constraint

# Disable narrative warning if you're generating resources programmatically
# and don't need human-readable text
disable_constraint('dom-6')  # "A resource should have narrative"
```

## Thread Safety

The configuration system uses Python's `contextvars` for thread-safe configuration management. Each async context or thread can have its own configuration without affecting others.

```python
import asyncio
from fhircraft import with_config

async def process_with_config():
    with with_config(disable_validation_warnings=True):
        # This configuration is isolated to this async context
        await process_resources()
```
