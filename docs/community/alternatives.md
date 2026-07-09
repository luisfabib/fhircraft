---
icon: lucide/shapes
---

# Alternative FHIR Python Packages

The FHIR Python ecosystem has several excellent projects, each with its own strengths and focus areas. Fhircraft is one option among many, and we're grateful to be part of this community. If fhircraft doesn't quite fit your needs or you're exploring different approaches, here are some other great projects worth checking out:

---

## fhir.resources (nazrulworld)

[:material-github: Repository](https://github.com/nazrulworld/fhir.resources)

fhir.resources is a comprehensive Pydantic-based library that provides complete type-safe Python representations of all FHIR resources for STU3, R4, R4B, and R5. It focuses on validation and serialization of FHIR data. The library includes pre-generated Pydantic models for all FHIR resources across multiple versions with automatic validation, type hints, and constraints enforcement. It offers XML and YAML serialization support alongside JSON, includes FHIR summary mode for selective field serialization, provides extensibility support for FHIR primitive data types, and offers configurable constraints such as ID length and string requirements.

**Shared Functionality**

- Pydantic-based model validation
- JSON serialization/deserialization
- Support for multiple FHIR versions (R4, R4B, R5)
- Type-safe resource manipulation
- FHIR specification compliance

---

## fhirpath (nazrulworld)

[:material-github: Repository](https://github.com/nazrulworld/fhirpath)

fhirpath is an implementation of the FHIRPath query language specification (v2.0.0 normative spec) with support for querying FHIR resources and integration with database backends like Elasticsearch. The library provides database engine support with an extensible dialect system, implements the FHIR Search API, offers a query builder with fluent interface, supports multiple FHIR versions (STU3, R4), and features an abstract design that allows custom backend providers for various database systems.

**Shared Functionality** 

- FHIRPath expression evaluation
- Support for multiple FHIR versions
- Query construction and execution
- Resource path navigation

---

## fhirpath-py (beda-software)

[:material-github: Repository](https://github.com/beda-software/fhirpath-py)

fhirpath-py is a Python implementation of the FHIRPath specification (N1 normative release) with support for FHIR data models and user-defined functions. The library fully implements the FHIRPath N1 specification using an ANTLR4-based parser for FHIRPath expressions. It includes FHIR data models for DSTU2, STU3, R4, and R5, provides support for user-defined functions, features type checking with the FHIRPath type system, and includes trace callback functionality for debugging FHIRPath expression evaluation.

**Shared Functionality**

- FHIRPath expression evaluation
- Support for multiple FHIR versions
- Integration with FHIR resources
- Navigation and filtering capabilities

---

## fhir-py (beda-software)

[:material-github: Repository](https://github.com/beda-software/fhir-py)

beda-software's fhir-py is an async/sync FHIR client library providing CRUD operations and search functionality for interacting with FHIR servers. The library offers both async and sync implementations using aiohttp and requests respectively, supports comprehensive CRUD operations (create, read, update, patch, delete), implements FHIR Search with chaining, includes, and modifiers, provides reference handling and resource relationships management, includes pagination support for large result sets, offers conditional operations (conditional create, update, patch, delete), and supports custom data models via protocol for flexible resource handling.

**Shared Functionality**

- FHIR resource operations
- JSON serialization
- Resource validation
- Support for FHIR R4

---

## Comparison Summary

| Feature | fhircraft | fhir.resources | fhirpath | fhirpath-py | fhir-py (beda) |
|---------|-----------|----------------|----------|-------------|----------------|
| **Pydantic Models** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **FHIRPath** | ✅ | ❌ | ✅ | ✅ | ❌ |
| **FHIR Mapper** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Profile Construction** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **FHIR Client** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **FHIR Versions** | R4, R4B, R5 | STU3, R4, R4B, R5 | STU3, R4 | DSTU2-R5 | R4 |
