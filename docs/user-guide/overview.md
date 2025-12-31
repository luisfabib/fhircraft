# Overview

Welcome to the comprehensive Fhircraft User Guide. This guide is designed for developers who want to leverage FHIR (Fast Healthcare Interoperability Resources) in Python applications using type-safe, validated Pydantic models.

## What You'll Learn

Fhircraft enables you to:

- **Build Type-Safe FHIR Models** from specifications and implementation guides
- **Query and Navigate** FHIR resources using the standard FHIRPath language
- **Transform Data** between different structures using FHIR Mapping Language
- **Validate Healthcare Data** with automatic FHIR compliance checking
- **Integrate FHIR** seamlessly into modern Python applications

## Choose Your Learning Path

### New to Fhircraft?
**Start here if you're beginning your Fhircraft journey:**

1. **[Installation](../quickstart/installation.md)** - Get Fhircraft running in your environment
2. **[Basics Tutorial](../quickstart/basics.md)** - Your first FHIR models and resources
3. **[FHIR Resources Overview](resources-overview.md)** - Understanding Fhircraft's approach to FHIR

### Building FHIR Applications?
**Follow this path for application development:**

1. **[FHIR Resources Overview](resources-overview.md)** - Core concepts and architecture
2. **[Pydantic FHIR](pydantic-representation.md)** - How FHIR maps to Python types
3. **[Resource Models](resources-models.md)** - Working with FHIR resource instances
4. **[Resource Factory](resources-construction.md)** - Advanced model construction patterns

### Working with FHIR Data?
**Focus on querying and data manipulation:**

1. **[Resource Models](resources-models.md)** - Creating and validating FHIR resources
2. **[FHIR Path](fhirpath.md)** - Querying resources with FHIRPath expressions
3. **[FHIR Mapper](mapper.md)** - Transforming data between structures

### Integrating Legacy Systems?
**Emphasize data transformation and validation:**

1. **[FHIR Mapper](mapper.md)** - Convert legacy data to FHIR resources
2. **[Resource Factory](resources-construction.md)** - Loading custom profiles and packages
3. **[Resource Models](resources-models.md)** - Validation and error handling patterns

## Feature Overview

### FHIR Resources
Transform FHIR specifications into working Python code with full type safety and validation.

| Feature | Description | Learn More |
|---------|-------------|------------|
| **Pydantic Models** | FHIR resources as validated Python classes | [Pydantic FHIR](pydantic-representation.md) |
| **Resource Construction** | Build models from specifications and packages | [Resource Factory](resources-construction.md) |
| **Data Validation** | Automatic FHIR compliance and constraint checking | [Resource Models](resources-models.md) |

### FHIR Path
Query and navigate FHIR resources using the standard FHIRPath expression language.

| Feature | Description | Learn More |
|---------|-------------|------------|
| **Path Expressions** | Extract data using familiar path-based syntax | [FHIR Path](fhirpath.md) |
| **Resource Integration** | Built-in FHIRPath methods on all Fhircraft models | [FHIR Path](fhirpath.md) |
| **Complex Queries** | Support for filtering, aggregation, and transformation | [FHIR Path](fhirpath.md) |

### FHIR Mapper
Transform data between different structures using declarative mapping rules.

| Feature | Description | Learn More |
|---------|-------------|------------|
| **Mapping Language** | Official FHIR Mapping Language implementation | [FHIR Mapper](mapper.md) |
| **Legacy Integration** | Convert existing data formats to FHIR resources | [FHIR Mapper](mapper.md) |
| **Validation** | Automatic validation of transformed data | [FHIR Mapper](mapper.md) |

## Getting Help

### Documentation
- **This User Guide** - Comprehensive feature documentation
- **[API Reference](../reference/)** - Detailed method and class documentation
- **[Pydantic Docs](https://docs.pydantic.dev/latest/)** - Learn about the underlying validation framework

### Troubleshooting
- **[Resource Models](resources-models.md#error-handling)** - Common validation errors and solutions
- **[FHIR Path](fhirpath.md#debugging-and-troubleshooting)** - FHIRPath debugging techniques
- **[Resource Factory](resources-construction.md#troubleshooting)** - Package loading and construction issues

### Community
- **[GitHub Issues](https://github.com/luisfabib/fhircraft/issues)** - Report bugs and request features
- **[GitHub Discussions](https://github.com/luisfabib/fhircraft/discussions)** - Ask questions and share ideas

---

**Ready to start?** Choose your learning path above or jump directly to [FHIR Resources Overview](resources-overview.md) to begin building with Fhircraft.