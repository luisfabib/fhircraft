---
title: 'fhircraft: A Python toolkit for FHIR-based healthcare data modelling and interoperability'
tags:
  - Python
  - FHIR
  - healthcare
  - interoperability
  - Pydantic
  - HL7
  - FHIRPath
authors:
  - name: Luis Fábregas-Ibáñez
    corresponding: true
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 19 July 2026
bibliography: paper.bib
---

# Summary

The Fast Healthcare Interoperability Resources (FHIR) standard, published and maintained by Health
Level Seven International (HL7), defines a comprehensive data model for representing and exchanging
healthcare information [@hl7fhir:2019]. FHIR resources — discrete, structured units of healthcare
data such as patients, observations, medications, and clinical documents — are serialised as JSON or
XML documents and validated against formally specified structural definitions called
`StructureDefinition` resources. Clinical implementation guides (IGs) layer additional constraints
atop the base FHIR specification through a profiling mechanism that restricts cardinalities, fixes
element values, and defines slices on repeating elements.

Working with FHIR data programmatically requires developers to navigate a complex web of
specification documents, structural constraints, and query languages. `fhircraft` provides a
comprehensive Python toolkit that translates this complexity into idiomatic Python objects: it
generates type-safe Pydantic [@pydantic:2024] models from FHIR `StructureDefinition` resources,
implements the FHIRPath [@fhirpath:2023] query language as a native Python engine, and executes
FHIR Mapping Language [@fhirmapping:2023] scripts for data transformation — all without requiring
external FHIR server infrastructure.

# Statement of need

Clinical software developers and health informatics researchers working in Python need tools that
allow them to construct, validate, query, and transform FHIR resources in a way that integrates
naturally with the modern Python ecosystem. The predominant pattern in production clinical systems is
to delegate FHIR validation and transformation to a running FHIR server (such as HAPI FHIR
[@hapifhir:2014]) over HTTP, which introduces infrastructure dependencies, round-trip latency, and
operational complexity that are undesirable in many contexts: lightweight microservices, offline
processing pipelines, unit testing, and research data extraction workflows.

`fhircraft` was developed to address a specific and underserved set of requirements:

1. Pydantic v2-based Python models for all FHIR R4, R4B, and R5 resource types, enabling full IDE
   type-checking, autocompletion, and automatic JSON (de)serialisation without any external tooling.
2. Dynamic generation of validated Python model classes from any `StructureDefinition`, including
   profiled resources from third-party implementation guides loaded from the FHIR package registry
   [@fhirregistry:2019], without requiring a running FHIR server.
3. A native Python FHIRPath engine that evaluates expressions directly on Python model instances,
   enabling in-process FHIR constraint evaluation and resource querying.
4. A FHIR Mapping Language engine for authoring and executing data transformation scripts that
   convert legacy or non-FHIR data into fully validated FHIR resources.

# State of the field

Several Python packages exist for working with FHIR data. `fhir.resources`
[@fhirresources:2021] provides pre-generated Pydantic models for the FHIR base specification and is
the most widely used Python FHIR modelling library. However, it does not support dynamic model
generation from arbitrary `StructureDefinition` resources or profiled implementation guides, does
not include a FHIRPath engine, and does not implement the FHIR Mapping Language. `fhirclient`
[@fhirclient:2014], developed by SMART Health IT, offers a Python FHIR client with its own model
classes but focuses on client-server communication and does not use Pydantic. Standalone FHIRPath
implementations such as `fhirpath.py` [@fhirpathpy:2020] provide expression evaluation but operate
on raw Python dictionaries and are not integrated with typed Pydantic model objects.
`google-fhir-py` [@googlefhir:2021] supports R4 and STU3 resources with Google-specific validation
extensions but does not cover R4B or R5, does not implement the FHIR Mapping Language, and is not
Pydantic-based.

`fhircraft` was built as a unified toolkit rather than contributing piecemeal to existing projects
for several reasons. First, the core requirement of generating Pydantic v2 models from arbitrary
`StructureDefinition` resources — including differential-only profiles — demands an integrated
pipeline from schema resolution to class construction that does not exist in any single existing
package. Second, tight integration between the model layer and the FHIRPath engine (via the
`FHIRPathMixin` incorporated into every model) enables a more natural API than a standalone
FHIRPath evaluator operating on raw dictionaries. Third, implementing the FHIR Mapping Language
within the same package and using the same typed model objects as both source and target allows
transformation pipelines to benefit from full Pydantic validation at every stage. Fourth, support
for all three active FHIR releases (R4, R4B, and R5) in a single package reduces fragmentation for
projects that must interoperate across release boundaries.

# Software design

`fhircraft` is structured around three major subsystems: the **resource modelling pipeline**, the
**FHIRPath engine**, and the **FHIR Mapping Language engine**.

## Resource modelling pipeline

The modelling pipeline transforms a FHIR `StructureDefinition` JSON document into a Pydantic
`BaseModel` subclass. The pipeline consists of four stages orchestrated by `FHIRModelFactory`. The
`SnapshotResolver` first synthesises a complete element snapshot from a differential-only profile by
traversing the `baseDefinition` chain and merging element definitions, resolving inherited fields for
cardinalities, type constraints, slicing definitions, and documentation. The resulting
`DefinitionIndex` — a path-queryable tree of `ElementNode` objects — is passed to the
`ModelAssembler`, which dispatches each element to a prioritised builder chain:
`TypeChoiceFieldBuilder` handles polymorphic `value[x]` elements; `SlicedFieldBuilder` handles
constrained repeating elements with named slices; `BackboneFieldBuilder` handles nested
backbone sub-resource structures; and `SimpleFieldBuilder` handles all remaining scalar and list
fields. The assembled Pydantic field definitions are collected by `FHIRModelFactory`, which invokes
Pydantic's metaclass machinery to construct the final model class and caches the result by canonical
URL to avoid redundant recompilation across repeated instantiations.

For the built-in FHIR R4, R4B, and R5 resource types, `fhircraft` ships pre-generated static Python
modules produced by the `CodeGenerator` class using Jinja2 [@jinja2:2008] templates. A
manifest-backed `TypeRegistry` lazily imports these modules on first access, keeping package startup
time low despite the several hundred FHIR type definitions bundled per release.

## FHIRPath engine

`fhircraft` implements FHIRPath [@fhirpath:2023] as a complete native Python engine using PLY
(Python Lex-Yacc) [@ply:2001] for LALR(1) lexing and parsing. FHIRPath expressions are parsed into
an abstract syntax tree composed of composable `FHIRPath` node objects covering the full FHIRPath
function library: navigation (`children`, `descendants`, `parent`), filtering (`where`, `select`,
`ofType`), existence (`exists`, `empty`, `all`, `allTrue`, `allFalse`, `anyTrue`, `anyFalse`),
aggregation (`aggregate`, `sum`, `count`), type operations (`is`, `as`, `ofType`), type conversion
(`toInteger`, `toDecimal`, `toString`, `toDate`, `toDateTime`, `toBoolean`), string manipulation,
arithmetic operators, and comparison and equality operators. Quantity arithmetic is handled via the
Pint [@pint:2014] library using a bundled UCUM [@ucum:1998]-to-Pint unit mapping, enabling
dimensionally-correct arithmetic on FHIR `Quantity` values (e.g., $10\,\text{mg} \times 2 = 20\,\text{mg}$).

Parsed FHIRPath expressions are cached per expression string for the lifetime of the process,
eliminating redundant LALR parse passes when the same expression is evaluated repeatedly. This is a
critical optimisation given that FHIR invariant constraint expressions embedded in
`StructureDefinition` resources are re-evaluated on every model instantiation. The
`FHIRPathMixin` incorporated into `FHIRBaseModel` exposes `fhirpath_values()`, `fhirpath_single()`,
`fhirpath_exists()`, `fhirpath_update_single()`, and `fhirpath_update_values()` as first-class
methods on every FHIR model instance.

## FHIR Mapping Language engine

The FHIR Mapping Language [@fhirmapping:2023] is a formal specification language for expressing
transformations between data structures, encoded as a `StructureMap` resource. `fhircraft`
implements a complete parser and execution engine for this language. The `FHIRStructureMapper` class
provides a high-level interface: a mapping script is parsed by a dedicated PLY LALR(1) parser into a
`StructureMapUnion` abstract syntax tree, registered in a `StructureMapRegistry` by canonical URL,
and executed by `FHIRMappingEngine` against source data to produce typed FHIR target instances. The
engine supports group inheritance (`extends`), map imports, and all standard transform functions
defined in the specification: `copy`, `create`, `cast`, `truncate`, `append`, `translate`,
`reference`, `dateOp`, `uuid`, `pointer`, and others.

## Validation

`fhircraft` enforces FHIR constraint validation at model instantiation time through Pydantic
validators that evaluate FHIRPath invariant expressions (e.g., `fhir:ele-1`, profile-specific
constraints), fixed-value and pattern constraints, type-choice element restrictions, and slicing
cardinality rules. A configurable `FhircraftConfig` dataclass allows per-deployment adjustment of
validation strictness — strict, lenient, or skip modes — and selective disabling of individual
constraint types, supporting both development and production deployment patterns. A pluggable
`TerminologyService` protocol interface allows integration of external terminology services for
`CodeSystem` and `ValueSet` validation when required.

# Acknowledgements

The author thanks the HL7 FHIR community for the open publication of the FHIR, FHIRPath, and FHIR
Mapping Language specifications, which made this work possible.

# References
