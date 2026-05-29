# Error Handling

This guide shows you how to handle errors raised by Fhircraft. You will learn about the exception hierarchy, understand which exceptions each component raises and why, and write effective error-handling code that makes your FHIR application robust and easy to debug.

## Exception Hierarchy

Fhircraft organizes its exceptions into a clear tree rooted at `FhircraftException`. Every exception the library raises — whether from the FHIRPath engine, the model factory, the FHIR Mapper, or the package registry — lives somewhere in this tree. Because each of these components has its own intermediate base class that inherits from `FhircraftException`, you can tune the granularity of your `except` clauses: catch the root for a coarse safety net, or catch only the specific leaf class you care about. All classes are importable from the single public module `fhircraft.exceptions`.

```
FhircraftException
├── MapperException            # FHIR Mapping Language engine
│   ├── MapperParsingError
│   ├── MapperValidationError
│   ├── MapperScopeError
│   ├── MapperDigestionError
│   ├── MapperGroupProcessingError
│   ├── MapperRuleProcessingError
│   ├── MapperSourceProcessingError
│   ├── MapperTargetProcessingError
│   ├── MapperExecutionError
│   └── MapperRegistryNotFoundError
├── FhirPathException          # FHIRPath evaluation engine
│   ├── FhirPathParsingError
│   ├── FhirPathLexingError
│   ├── FhirPathRuntimeError
│   ├── FhirPathTypeError
│   └── FhirPathOperationError
├── FactoryException           # FHIR model factory and builders
│   ├── FactoryDefinitionIndexError
│   ├── FactoryDefinitionResolutionError
│   ├── FactoryBuilderError
│   │   └── FactoryBuildError
│   ├── FactoryTypeResolutionError
│   └── FactoryAssemblerError
├── DefinitionNotFoundError    # Structure definition registry
└── PackageException           # FHIR package registry
    ├── PackageNotFoundError
    ├── PackageResolutionError
    └── PackageValidationError
```

There is one deliberate exception to this rule: FHIR **resource validation errors** (constraint and invariant failures on `Patient`, `Observation`, etc.) surface as Pydantic's `ValidationError`, not as a `FhircraftException` subclass. This is intentional — resource models are standard Pydantic models, so they use the standard Pydantic error mechanism. See [FHIR Validation Errors](#fhir-validation-errors) for details.

??? abstract "Technical Documentation"

    [`fhircraft.exceptions`](../reference/exceptions.md)


## Importing Exceptions

All exceptions live in `fhircraft.exceptions`. Import exactly what you need — using the intermediate base class (e.g. `FhirPathException`) keeps your `except` clauses readable without catching too broadly:

```python
from fhircraft.exceptions import (
    FhircraftException,              # catch-all for any Fhircraft error
    FhirPathException,               # catch-all for any FHIRPath error
    FhirPathRuntimeError,            # runtime evaluation failures
)
```

!!! tip "Catch specific before broad"

    When chaining multiple `except` clauses, always list the most specific exception first. Python checks clauses in order, so a broad `except FhircraftException` placed before `except DefinitionNotFoundError` would shadow the specific branch and prevent it from ever matching.


## Exception Attributes

Every `FhircraftException` provides two structured attributes beyond the standard string message. These attributes let you write clean logging and alerting code without parsing the exception string yourself:

| Attribute | Type | Description |
|---|---|---|
| `message` | `str` | The raw error description, without the component prefix |
| `component` | `str` | None` | Which library component raised the error (`"factory"`, `"fhirpath"`, `"mapper"`, `"packages"`, `"registry"`) |

```python
from fhircraft.exceptions import FhircraftException, DefinitionNotFoundError
from fhircraft.fhir.resources import FHIRModelFactory

factory = FHIRModelFactory(fhir_release="R4")

try:
    model = factory.build("http://example.org/StructureDefinition/Unknown")
except FhircraftException as e:
    print(e.message)    # the raw description
    #> Definition 'http://example.org/StructureDefinition/Unknown' not found in registry
    print(e.component)  # which subsystem raised it
    #> registry
    print(str(e))       # formatted "[component] message"
    #> [registry] Definition 'http://example.org/...' not found in registry
```

The `str()` representation always produces `[component] message`, making it easy to read in log output without needing a log formatter to add context.


## Catching Exceptions by Component

### FHIRPath Errors

FHIRPath evaluation can fail at two distinct stages: when parsing the expression text, and when evaluating it against data. Separating these cases lets you report helpful messages to users — a parsing failure means the expression string is wrong (a developer mistake or bad input), while a runtime failure means the expression is valid but the data does not match what the expression expects.

```python
from fhircraft.exceptions import (
    FhirPathParsingError,
    FhirPathLexingError,
    FhirPathRuntimeError,
)
from fhircraft.fhir.resources import get_fhir_type

Patient = get_fhir_type("Patient", "R5")
patient = Patient(
    name=[
        {"given": ["Alice"], "family": "Johnson"},
        {"given": ["Aly"],   "family": "Johnson", "use": "nickname"},
    ]
)

# A malformed expression fails at parse time
try:
    patient.fhirpath_single("Patient.name.where(use = ")  # (1)!
except FhirPathParsingError as e:
    print(f"Fix the expression: {e.message}")

# A valid expression that returns multiple values fails at runtime
try:
    patient.fhirpath_single("Patient.name")  # (2)!
except FhirPathRuntimeError as e:
    print(f"Adjust the query: {e.message}")
```

1. The `where(` clause is never closed — this fails during lexing/parsing before any data is touched.
2. The expression is syntactically valid, but `single()` expects exactly one result and the patient has two names.

| Exception | When it is raised |
|---|---|
| `FhirPathParsingError` | Expression cannot be parsed — invalid syntax such as unclosed parentheses or unknown keywords |
| `FhirPathLexingError` | Expression contains tokens the lexer does not recognize |
| `FhirPathRuntimeError` | Evaluation fails at runtime — wrong cardinality, failed navigation, invalid `single()` or `update_single()` call |
| `FhirPathTypeError` | Incompatible types used together (e.g. comparing a string to a date without conversion) |
| `FhirPathOperationError` | A function or operator is called with incompatible or unsupported arguments |

!!! note "FhirPathWarning"

    `FhirPathWarning` is not part of the `FhircraftException` tree — it inherits from Python's built-in `Warning` class. It is issued via Python's `warnings` module for non-fatal FHIRPath situations (such as using a deprecated function). Use the standard `warnings.catch_warnings()` context manager to capture or suppress it:

    ```python
    import warnings
    from fhircraft.exceptions import FhirPathWarning

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", FhirPathWarning)
        result = patient.fhirpath_values("Patient.name")

    for w in caught:
        print(f"FHIRPath warning: {w.message}")
    ```


### FHIR Validation Errors

When Fhircraft constructs or modifies a FHIR resource, Pydantic validates every field automatically. Failures raise `pydantic.ValidationError`, which bundles all constraint violations into a single exception. Each entry in the `errors()` list describes one violation.

```python
from pydantic import ValidationError
from fhircraft.fhir.resources import get_fhir_type

Observation = get_fhir_type("Observation", "R4")

try:
    patient = Observation.model_validate({"valueReference": {"type": "only-type"}}})  # (1)!
except ValidationError as e:
    for error in e.errors():
        print(f"  field : {error['loc']}")
        print(f"  type  : {error['type']}")
        print(f"  detail: {error['msg']}")
        print() 
```

To distinguish between validation errorrs (e.g to determine FHIR-invariant errors), inspect the `type` key.

### Resource factory Errors

The factory raises specific errors depending at which stage the model build fails. In a healthy workflow, `DefinitionNotFoundError` is the only factory exception you routinely need to catch — the others indicate either a corrupt structure definition or an internal library issue worth logging and escalating.

```python
from pydantic import ValidationError
from fhircraft.exceptions import (
    DefinitionNotFoundError,
    FactoryBuilderError,
    FactoryDefinitionResolutionError,
    FactoryTypeResolutionError,
)
from fhircraft.fhir.resources import FHIRModelFactory

factory = FHIRModelFactory(fhir_release="R4")

try:
    MyPatient = factory.build("http://example.org/StructureDefinition/MyPatient")  # (1)!
except DefinitionNotFoundError as e:
    # The most common case: the definition was never loaded into the registry
    print(f"Load the definition first: {e.message}")
except FactoryDefinitionResolutionError as e:
    # The definition was found, but snapshot/differential resolution failed
    print(f"Definition may be malformed: {e.message}")
except FactoryTypeResolutionError as e:
    # A FHIR type referenced inside the definition could not be resolved
    print(f"Unsupported or missing type: {e.message}")
except FactoryBuilderError as e:
    # General model assembly failure
    print(f"Build failed: {e.message}")
```

1. `factory.register(...)` or `factory.load_package(...)` must be called before `build()` for any non-base FHIR definition.

| Exception | When it is raised |
|---|---|
| `DefinitionNotFoundError` | The requested canonical URL is not present in the definition registry |
| `FactoryDefinitionResolutionError` | Snapshot or differential resolution fails (e.g. broken inheritance chain) |
| `FactoryDefinitionIndexError` | Navigation of the element index inside the definition fails |
| `FactoryBuilderError` | A builder step fails during model construction |
| `FactoryTypeResolutionError` | A FHIR type referenced in the definition cannot be mapped to a Python type |
| `FactoryAssemblerError` | The final model assembly step fails when combining builder outputs |

!!! tip "DefinitionNotFoundError is also a FileNotFoundError"

    `DefinitionNotFoundError` inherits from both `FhircraftException` and Python's built-in `FileNotFoundError`. Libraries or frameworks that catch `FileNotFoundError` at a high level will therefore also catch missing-definition errors without requiring any Fhircraft-specific handling.


### Mapper Errors

The FHIR Mapper engine processes StructureMap scripts through several sequential stages: lexing and parsing the mapping script, digesting the group and rule definitions, and executing the transformation. Each stage has its own exception class so you can tell immediately where in the pipeline a failure occurred.

```python
from fhircraft.exceptions import (
    MapperParsingError,
    MapperDigestionError,
    MapperRuleProcessingError,
    MapperExecutionError,
    MapperRegistryNotFoundError,
)
from fhircraft.fhir.mapper import FHIRStructureMapper

mapper = FHIRStructureMapper()

mapping_script = """
map 'http://example.org/mapping' = 'MyMapping'
uses "http://hl7.org/fhir/StructureDefinition/Patient" as target
group main(source src, target patient: Patient) {
    src.name -> patient.name;
}
"""

source_data = {"name": [{"given": ["Alice"], "family": "Johnson"}]}

try:
    results = mapper.map(mapping_script, source_data)  # (1)!
except MapperParsingError as e:
    # Syntax error in the mapping script itself
    print(f"Mapping script syntax error: {e.message}")
except MapperDigestionError as e:
    # Valid syntax but structurally inconsistent group or rule definitions
    print(f"Mapping definition error: {e.message}")
except MapperRegistryNotFoundError as e:
    # A referenced StructureMap or StructureDefinition could not be resolved
    print(f"Missing dependency: {e.message}")
except MapperExecutionError as e:
    # The script parsed fine but failed during the actual data transformation
    print(f"Transformation failed: {e.message}")
```

1. `mapper.map()` runs the full pipeline: parse → digest → execute. Any stage may raise its exception type.

| Exception | When it is raised |
|---|---|
| `MapperParsingError` | The mapping script has invalid FHIR Mapping Language syntax |
| `MapperValidationError` | Input data fails pre-transformation validation |
| `MapperScopeError` | A variable or scope reference cannot be resolved during execution |
| `MapperDigestionError` | Group or rule definitions are structurally invalid after parsing |
| `MapperGroupProcessingError` | A specific group within the mapping fails to process |
| `MapperRuleProcessingError` | A single mapping rule fails to process |
| `MapperSourceProcessingError` | Reading or resolving a source value fails |
| `MapperTargetProcessingError` | Writing or resolving a target value fails |
| `MapperExecutionError` | Top-level execution failure not covered by a more specific class |
| `MapperRegistryNotFoundError` | A required StructureMap or StructureDefinition cannot be found |


### Package Registry Errors

When loading FHIR packages from the registry — either the default FHIR NPM registry or a custom endpoint — network issues, missing packages, or malformed archives raise package-specific exceptions.

```python
from fhircraft.exceptions import (
    PackageNotFoundError,
    PackageResolutionError,
    PackageValidationError,
)
from fhircraft.fhir.resources import FHIRModelFactory

factory = FHIRModelFactory(fhir_release="R4")

try:
    factory.load_package("hl7.fhir.us.core", "6.1.0")  # (1)!
except PackageNotFoundError as e:
    # Package name or version does not exist in the registry
    print(f"Package not published: {e.message}")
except PackageResolutionError as e:
    # Package was found but downloading or extracting it failed
    # (network error, corrupted archive, file system permission, etc.)
    print(f"Could not load package: {e.message}")
except PackageValidationError as e:
    # Package was loaded but its contents failed structural validation
    print(f"Package contents are invalid: {e.message}")
```

1. `load_package` contacts the FHIR package registry, downloads the specified version, extracts the `.tgz` archive, and registers all contained StructureDefinitions.

| Exception | When it is raised |
|---|---|
| `PackageNotFoundError` | The package name and/or version does not exist in the registry |
| `PackageResolutionError` | Download or archive extraction failed (network, I/O, or format error) |
| `PackageValidationError` | Package metadata or contained resource files failed validation |


## Integrating with Standard Exception Types

Several Fhircraft exceptions also inherit from standard Python built-ins. This dual inheritance means code that catches standard built-in types (e.g. a generic HTTP framework handler catching `FileNotFoundError`) will also catch the corresponding Fhircraft exceptions without requiring Fhircraft-specific imports:

| Fhircraft Exception | Also a subclass of | Practical effect |
|---|---|---|
| `DefinitionNotFoundError` | `FileNotFoundError` | Caught by filesystem / resource-not-found handlers |
| `MapperRegistryNotFoundError` | `FileNotFoundError` | Caught by the same generic not-found handlers |
| `FhirPathRuntimeError` | `RuntimeError` | Caught by generic runtime error handlers |
| `FactoryTypeResolutionError` | `LookupError` | Caught by generic lookup/key-error handlers |
| `FactoryAssemblerError` | `LookupError` | Caught by generic lookup/key-error handlers |

```python
# A framework handler that catches FileNotFoundError will also catch this
from fhircraft.exceptions import DefinitionNotFoundError

try:
    raise DefinitionNotFoundError("No definition for 'MyPatient'")
except FileNotFoundError as e:
    print(str(e))  # caught without any Fhircraft import needed
    #> [registry] No definition for 'MyPatient'
```


## Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| `FhircraftException` catch-all hides the root cause | Narrow the `except` clause to the component's base class (e.g. `FactoryException`, `FhirPathException`) or to the specific leaf exception. Log `e.component` and `e.message` separately so the subsystem is always visible in output. |
| `DefinitionNotFoundError` raised at build time | The required structure definition was not loaded before calling `factory.build()`. Call `factory.register()`, `factory.load_directory()`, or `factory.load_package()` first, then retry the build. |
| `ValidationError` raised but unclear which field failed | Iterate `e.errors()` and print each entry's `loc`, `type`, and `msg` keys. Types prefixed with `fhir_` identify FHIR invariant violations (e.g. `fhir_dom-6`); all others are Pydantic field-type errors. |
| FHIR constraint violations appear even on valid-looking data | The resource may be missing optional-but-constrained elements such as narrative text (`dom-6`). Use `disable_constraint('dom-6')` or switch to `validation_mode='lenient'` for that operation. See [Configuring Validation Behavior](configuration.md). |
| `FhirPathParsingError` on a seemingly correct expression | Check for unclosed parentheses, mismatched quotes, or unsupported syntax. Validate the expression against the [:material-fire: FHIRPath specification](https://hl7.org/fhirpath/N1/). |
| `FhirPathRuntimeError` from `fhirpath_single()` | The expression matched more than one value. Use `fhirpath_values()` to retrieve all matches, or tighten the expression with a `where()` filter so only one result is returned. |
| Mapper raises `MapperRegistryNotFoundError` | A `uses` declaration in the mapping script references a StructureDefinition that is not loaded. Register the definition or load the relevant package before running the mapper. |
| `MapperExecutionError` with no clear cause | Enable verbose logging and inspect intermediate scope state. Break the mapping script into smaller groups to isolate the failing rule. |
| `PackageNotFoundError` for a package that exists on the registry | Verify the package name and version string exactly match the registry entry (names are case-sensitive). Check that the configured registry URL is reachable. |
| `PackageResolutionError` despite the package being found | A network timeout, proxy restriction, or disk permission issue prevented download or extraction. Confirm internet access, check available disk space, and verify write permissions on the package cache directory. |
| Uncertain whether two exceptions overlap in an `except` chain | Use `issubclass(SpecificError, BroadError)` to verify the relationship before writing code that depends on it. Place the most specific clause first to avoid it being shadowed. |

