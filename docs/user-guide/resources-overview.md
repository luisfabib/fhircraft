# Overview

This section covers everything you need to work with FHIR resources in Fhircraft. You'll learn how FHIR specifications translate to Python code, how to construct and use resource models, and how to build robust healthcare applications with type safety and validation.

## Overview

Fhircraft transforms FHIR (Fast Healthcare Interoperability Resources) specifications into working Python code using Pydantic models. This approach gives you:

- **Type Safety** - Catch errors at development time with proper Python typing
- **Automatic Validation** - Ensure FHIR compliance with built-in constraint checking  
- **Seamless Integration** - Use FHIR resources like any other Python objects
- **Standards Compliance** - Support for FHIR R4, R4B, and R5 specifications

## Learning Path

This section is organized into three progressive guides:

### 1. [Pydantic FHIR](pydantic-representation.md)
**Foundation: Understanding FHIR in Python**

Learn how Fhircraft represents FHIR concepts using Pydantic models. This guide covers the technical foundation you need to understand how FHIR data types, resources, and constraints map to Python code.

**Topics covered:**

- FHIR primitive and complex data types as Python types
- FHIR resources as Pydantic models
- FHIR elements: cardinality, backbone elements, slicing, choice types
- Extensions and custom profiles
- Validation constraints and invariants

**Start here if:** You're new to FHIR or want to understand the technical foundations of Fhircraft's approach.

### 2. [Resource Models](resources-models.md)
**Practice: Working with FHIR Resource Instances**

Learn to create, validate, query, and serialize FHIR resource instances in your applications. This guide focuses on the practical aspects of working with FHIR data in Python.

**Topics covered:**

- Creating resource instances with validation
- Handling validation errors and debugging
- JSON serialization and deserialization  
- Working with resource references and relationships
- Performance considerations and best practices

**Start here if:** You have FHIR resource models and want to use them effectively in your application.

### 3. [Resource Factory](resources-construction.md)
**Advanced: Building Models from Specifications**

Master the construction of Pydantic models from FHIR structure definitions, implementation guides, and packages. This guide covers advanced patterns for loading and managing FHIR specifications.

**Topics covered:**

- Constructing models from structure definitions
- Loading FHIR packages and implementation guides
- Repository system for managing multiple specifications
- Multi-version FHIR support
- Package loading strategies and caching

**Start here if:** You need to work with custom FHIR profiles, implementation guides, or multiple FHIR versions.

## What's Next?

Choose your next step based on your goals:

- **New to FHIR?** Start with [Pydantic FHIR](pydantic-representation.md) to understand the fundamentals
- **Ready to build?** Jump to [Resource Models](resources-models.md) for practical usage patterns
- **Working with profiles?** Go to [Resource Factory](resources-construction.md) for advanced construction techniques
- **Need to query data?** Check out [FHIR Path](fhirpath.md) for powerful data access patterns
- **Transforming data?** Explore [FHIR Mapper](mapper.md) for data conversion workflows

---

**Continue learning:** [Pydantic FHIR →](pydantic-representation.md)