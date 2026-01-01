# Frequently Asked Questions

Common questions about Fhircraft and their answers.

## General

### What is Fhircraft?

Fhircraft is a Python library that transforms FHIR (Fast Healthcare Interoperability Resources) specifications into type-safe Pydantic models. It enables you to work with FHIR resources using familiar Python patterns with automatic validation and serialization.

### What FHIR versions are supported?

Fhircraft currently supports:

- FHIR R4 (4.0.1)
- FHIR R4B (4.3.0)
- FHIR R5 (5.0.0)

You can specify the version when getting resource types or loading packages.

### Do I need a FHIR server to use Fhircraft?

No! Fhircraft works entirely with local Python objects. You don't need a FHIR server for validation, querying, or transforming FHIR data. However, you can use Fhircraft alongside FHIR servers if your application requires one.

### Is Fhircraft production-ready?

Fhircraft is under active development and considered alpha software. While it's functional and tested, expect breaking changes in future releases. Use caution in production environments and pin your version dependencies.


### Can I use Fhircraft with virtual environments?

Yes! Fhircraft works with all standard Python virtual environment tools including venv, virtualenv, conda, and Poetry.

## Working with Resources

### How do I get a FHIR resource model?

For core resources:

```python
from fhircraft.fhir.resources.datatypes import get_fhir_resource_type

Patient = get_fhir_resource_type("Patient", "R5")
```

For profiles from implementation guides:

```python
from fhircraft.fhir.resources.factory import factory

factory.load_package('hl7.fhir.us.core')
USCorePatient = factory.construct_resource_model(
    canonical_url='http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient'
)
```

### Can I create resources without all required fields?

No. Fhircraft validates resources against FHIR specifications. All required fields must be present and correctly typed. This catches errors early rather than at runtime or when interacting with FHIR servers.

### How do I handle validation errors?

Validation errors are Pydantic `ValidationError` exceptions:

```python
from pydantic import ValidationError

try:
    patient = Patient(gender=1)
except ValidationError as e:
    print(e.errors())
    # [{'loc': ('gender',), 'msg': 'Input should be...', ...}]
```

### What is the FHIR Mapping Language?

The FHIR Mapping Language is an official HL7 specification for transforming data between different structures. Fhircraft implements this language to enable declarative data transformations.

### Is the Mapper production-ready?

The FHIR Mapping Language is specified as Maturity Level 0 (Draft) by HL7, meaning both the specification and implementations are subject to change. Use carefully and test thoroughly.

### Can I use the Mapper for non-FHIR data?

Yes! You can transform legacy system data, CSV files, or any JSON structure to FHIR resources using mapping scripts.

## Performance

### Is Fhircraft fast?

Fhircraft uses Pydantic v2, which is highly optimized. For most use cases, performance is excellent. Large-scale processing may require optimization strategies.

### How can I improve performance?

1. **Reuse models** - Don't generate models repeatedly
2. **Batch operations** - Process multiple resources together
3. **Lazy loading** - Only load packages when needed
4. **Cache parsed FHIRPath** - Parse expressions once, evaluate many times

### Can I use Fhircraft with large datasets?

Yes, but consider:

- Streaming large files instead of loading everything into memory
- Using generators for batch processing
- Database storage for persistence
- Profiling your specific use case

## Development

### How do I contribute?

See our [Contributing Guide](contributing.md) for detailed instructions on:

- Setting up your development environment
- Running tests
- Submitting pull requests
- Code style guidelines

### How do I report a bug?

[Open an issue](https://github.com/luisfabib/fhircraft/issues) on GitHub with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and Fhircraft version
- Minimal code example if possible

### How do I request a feature?

[Open an issue](https://github.com/luisfabib/fhircraft/issues) with the `enhancement` label, describing:

- The feature you'd like
- Your use case
- How it would benefit the community
- Any implementation ideas (optional)

### Can I help improve documentation?

Absolutely! Documentation improvements are highly valued. You can:

- Fix typos or unclear explanations
- Add examples
- Improve navigation
- Translate content

Submit a pull request with your changes.

