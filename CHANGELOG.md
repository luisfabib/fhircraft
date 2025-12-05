
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

----------------- 

## [0.4.2] - 2025-12-05

### Changed

* Added thread-local stacks to track recursion during polymorphic serialization and deserialization, preventing infinite recursion in nested FHIR resource structures. This replaces the previous global flag approach for recursion protection. ([#142](https://github.com/luisfabib/fhircraft/pull/142))

### Fixed 

* Removed the `generic_FHIR_resource_validator` methods for the outcome, resource, and issues fields in the Bundle resource for R4, R4B, and R5. Since these were calling the previously removed `validate_contained_resource` an error was raised whenever evaluating a `Bundle` ([#140](https://github.com/luisfabib/fhircraft/pull/140))
* Modified `FHIRBaseModel._serialize_fhir_field_polymorphically` and `FHIRBaseModel._deserialize_polymorphically` to remove temporary disabling of polymorphic flags, relying instead on stack-based recursion protection. This ensures that nested resources are handled correctly and safely. ([#142](https://github.com/luisfabib/fhircraft/pull/142), fixes [#141](https://github.com/luisfabib/fhircraft/pull/141))


## [0.4.1] - 2025-12-03

### Added

- Added internal `_fhir_release` attribute to `FHIRBaseModel` and initialized it to correct values in base resources across R4, R4B, and R5 for proper version tracking and context awareness ([#132](https://github.com/luisfabib/fhircraft/pull/132))
- Implemented new automated FHIRPath environment variable `%fhirRelease` that tracks the resource context's FHIR release version ([#132](https://github.com/luisfabib/fhircraft/pull/132))

### Changed

- Updated `TypeSpecifier` to support multiple FHIR releases with enhanced error handling and version-specific type resolution ([#132](https://github.com/luisfabib/fhircraft/pull/132))
- Enhanced FHIRPath mixin to automatically set `%fhirRelease` for better context-aware evaluation ([#132](https://github.com/luisfabib/fhircraft/pull/132))


### Fixed

- Fixed `DomainResource` invariant `dom-3` for all FHIR releases prior to R5 by replacing incorrect FHIRPath fragments `descendants().as()` with `descendants().ofType()` throughout ([#130](https://github.com/luisfabib/fhircraft/pull/130), fixes [#128](https://github.com/luisfabib/fhircraft/issues/128))
- Fixed polymorphic serialization check in `FHIRBaseModel` by adding type check to ensure polymorphic serialization is only attempted on instances of `FHIRBaseModel` ([#131](https://github.com/luisfabib/fhircraft/pull/131), fixes [#129](https://github.com/luisfabib/fhircraft/issues/129))
- Fixed FHIR `Reference` resource `ref-1` invariant validator to only evaluate its FHIRPath expression if the instance is assigned to a resource, allowing `Reference` objects with local references to be built outside of a root resource context ([#132](https://github.com/luisfabib/fhircraft/pull/132), [#136](https://github.com/luisfabib/fhircraft/pull/136))
- Fixed recursion errors when checking own type in FHIRPath invariant expressions by adding circular reference protection (e.g. a `Coding` with an invariant evaluating `is(Coding)`) ([#132](https://github.com/luisfabib/fhircraft/pull/132))
- Added missing environment variable support in `TypeSpecifier.evaluate()` ([#132](https://github.com/luisfabib/fhircraft/pull/132))
- Fixed exponential string escaping in FHIRPath expression `__repr__` methods that caused CPU crashes with deeply nested expressions ([#134](https://github.com/luisfabib/fhircraft/pull/134), fixes [#133](https://github.com/luisfabib/fhircraft/issues/133))
- Fixed missing resource context setup during `model_validate()` and `model_validate_json()` operations with dictionaries as input values ([#135](https://github.com/luisfabib/fhircraft/pull/135))
- Ensured proper type preservation during dictionary-based resource loading ([#135](https://github.com/luisfabib/fhircraft/pull/135))
- Enhanced polymorphic validation for nested FHIR resources from dictionary inputs ([#136](https://github.com/luisfabib/fhircraft/pull/136))
- Corrected certain inheritance patterns across resource classes to ensure proper class hierarchies in all FHIR versions ([#132](https://github.com/luisfabib/fhircraft/pull/132))
  
----------------- 

## [0.4.0] - 2025-11-30

### Added

- Implement polymorphic serialization and deserialization support in `FHIRBaseModel` to preserve runtime type information for FHIR resources, ensuring specialized fields are not lost during serialization ([#123](https://github.com/luisfabib/fhircraft/pull/123))
- Add new FHIRPath `TypeSpecifier` class for handling type identifiers with namespace support including qualified type names like `FHIR.Patient` and `System.String` ([#124](https://github.com/luisfabib/fhircraft/pull/124))
- Implement unit conversion and handling for FHIRPath `Quantity` using the Pint library with UCUM unit definitions support, enabling robust unit-aware arithmetic and comparison FHIRPath operations ([#126](https://github.com/luisfabib/fhircraft/pull/126))

### Changed

- Update FHIRPath `is`, `as`, `ofType()`, and legacy type functions to use `TypeSpecifier` objects instead of plain strings for improved type handling ([#124](https://github.com/luisfabib/fhircraft/pull/124))
- Improve import consolidation in generated code to reduce verbosity by grouping multiple individual import lines into single grouped imports ([#125](https://github.com/luisfabib/fhircraft/pull/125))

### Fixed

- Fix contained resource serialization to preserve specialized model schemas instead of being reduced to generic base models ([#123](https://github.com/luisfabib/fhircraft/pull/123), fixes [#120](https://github.com/luisfabib/fhircraft/issues/120))
- Fix Jinja2 template to properly handle models with multiple base classes by iterating over `model.__bases__` instead of using only `model.__base__` ([#125](https://github.com/luisfabib/fhircraft/pull/125), fixes [#121](https://github.com/luisfabib/fhircraft/issues/121))
- Fix FHIRPath arithmetic and comparison operations between `Quantity` instances with different but convertible units ([#126](https://github.com/luisfabib/fhircraft/pull/126), fixes [#36](https://github.com/luisfabib/fhircraft/issues/36))

### Removed

- Remove obsolete `contained_FHIR_resource_validator` method and its assignments, superseded by polymorphic functionality ([#123](https://github.com/luisfabib/fhircraft/pull/123))

----------------- 

## [0.3.7] - 2025-11-26

### Added

- Add comprehensive parent and resource tracking to `FHIRBaseModel` with FHIRPath integration to enable richer context-aware evaluation and navigation of model trees ([#114](https://github.com/luisfabib/fhircraft/pull/114))

### Changed

- Enhance `hasValue` and `getValue` functions to check for FHIR primitive values, improving correctness when inspecting primitive-valued elements ([#106](https://github.com/luisfabib/fhircraft/pull/106))
- Improve performance of FHIR primitive type checking to reduce overhead in hot paths of FHIRPath evaluation and validation ([#112](https://github.com/luisfabib/fhircraft/pull/112))
- Improve inheritance from core resources and remove the `meta.versionId` default value to avoid unintended defaults and ensure cleaner model inheritance behavior ([#118](https://github.com/luisfabib/fhircraft/pull/118))

### Fixed

- Change `ValidationError` to `TypeError` in `validate_contained_resource` to provide a more appropriate exception type for invalid contained resources ([#109](https://github.com/luisfabib/fhircraft/pull/109))
- Fix contained resource validation logic so contained resources are validated and coerced into appropriate resource models without losing data ([#113](https://github.com/luisfabib/fhircraft/pull/113))
- Add missing primitive extension fields for type choice elements across all FHIR versions ensuring primitive extensions are preserved for choice-typed elements ([#116](https://github.com/luisfabib/fhircraft/pull/116))
- Enhance string handling in `CodeGenerator` for multiline and escaped characters to prevent incorrect escaping or truncation in autogenerated model source code ([#115](https://github.com/luisfabib/fhircraft/pull/115))

----------------- 

## [0.3.6] - 2025-11-19

### Changed

- Update return type of `model_construct` to `Self` to fix type hinting of return value for all `FHIRBaseModel` classes ([#99](https://github.com/luisfabib/fhircraft/pull/99))

 ### Fixed

- Improved handling of empty collections in FHIRPath `Is` and `As` operators to avoid errors on runtime ([#98](https://github.com/luisfabib/fhircraft/pull/98))
- Fixed the FHIRPath `replace()` fucntion to allowing empty strings `''` to be used for the substitution instead of returning an empty collection ([#100](https://github.com/luisfabib/fhircraft/pull/100))
- Improved the FHIRPath engine better handle cases where the primitive extension/id elements are requested ([#102](https://github.com/luisfabib/fhircraft/pull/102))

----------------- 

## [0.3.5] - 2025-11-19

### Changed

- Updated `FHIRBaseModel` to use `ConfigDict(defer_build=True)` for deferred building, largely improving import times of Pydantic-heavy modules such as `fhircraft.resources.datatypes` ([#95](https://github.com/luisfabib/fhircraft/pull/95))
- Changed the import path for complex types from `complex_types` to `complex` and for core resources from `resources` to `core` ([#95](https://github.com/luisfabib/fhircraft/pull/95))

### Fixed

- Updated the Jinja resource template to add the missing `min_cardinality` and `max_cardinality` class variables for models inheriting from `FHIRSliceModel` ([#85](https://github.com/luisfabib/fhircraft/pull/85))
- Fixed a bug in `validate_slicing_cardinalities` raising an error when no slices are provided and the value is `None` ([#86](https://github.com/luisfabib/fhircraft/pull/86))
- Fixed the FHIRPath concatenation operation (`&`) to ensure the complete strings are concatenated and not just the initial characters ([#90](https://github.com/luisfabib/fhircraft/pull/90))
- Fixed a bug in the FHIRPath `Is`, `As`, `LegacyIs`, and `LegacyAs` classes when providing core FHIR resources as target types ([#92](https://github.com/luisfabib/fhircraft/pull/92))
- Added a validator to the `Bundle` resource models to ensure that `Bundle.entry.resource` entries are properly resolved and validated with the appropriate resource model without loosing any data ([#94](https://github.com/luisfabib/fhircraft/pull/94))
- Reorganized the complex type models for all releases to fix many of the `{model.__name__} is not fully defined` errors caused by recursive relations between complex datatype models when importing datatypes or resources ([#95](https://github.com/luisfabib/fhircraft/pull/95))

----------------- 

## [0.3.4] - 2025-11-11

### Fixed
- Fixed processing of pattern and fixed values for both primitive and complex FHIR types ([#82](https://github.com/luisfabib/fhircraft/pull/82))
- Resolved bugs in type choice field construction, ensuring all possible types are supported and correctly named ([#82](https://github.com/luisfabib/fhircraft/pull/82))
- Corrected slice model construction, ensuring that slice names do not conflict within a model or with other models by prepending the parent model's name to the slice name ([#82](https://github.com/luisfabib/fhircraft/pull/82))
- Fixed linting errors in autogenerated code when defining model fields with default factories calling FHIR models ([#82](https://github.com/luisfabib/fhircraft/pull/82))
- Resolved a bug leading to some FHIR models with backbone elements having its name overriden with the backbone model's name ([#82](https://github.com/luisfabib/fhircraft/pull/82))
- Expanded the `validate_FHIR_element_pattern` validator to avoid an error when assigning patterns to primitive-valued fields ([#82](https://github.com/luisfabib/fhircraft/pull/82))
- Expand the code generator to import models used in default or pattern values in autogenerated code ([#82](https://github.com/luisfabib/fhircraft/pull/82))
- Refactor certain imports to avoid circular import errors when loading individual modules ([#83](https://github.com/luisfabib/fhircraft/pull/83))
- Reduce the overall import time of Fhircraft modeules by implementing lazy loading of the complex FHIR type models ([#83](https://github.com/luisfabib/fhircraft/pull/83))
- Fixed an error in the `List` FHIR resource model definitions ([#83](https://github.com/luisfabib/fhircraft/pull/83)).

----------------- 

## [0.3.3] - 2025-10-13

### Changed

- Update `Date`, `DateTime`, and `Time` FHIR type aliases to support native Python date and time types. ([#77](https://github.com/luisfabib/fhircraft/pull/77))
- Remove large number of empty lines between code blocks in autogenerated model class definition source code. ([#78](https://github.com/luisfabib/fhircraft/pull/78))
- Update the internal `resolve_structure_definition` method to accept an optional `version` parameter, enabling version-specific resolution of StructureDefinitions. ([#79](https://github.com/luisfabib/fhircraft/pull/79))
- Add internal functionality to load local FHIR definitions in `CompositeStructureDefinitionRepository` ([#79](https://github.com/luisfabib/fhircraft/pull/79))
- Add an internal `FHIR_version` attribute to the `FactoryConfig` class for more precise version tracking during model construction ([#79](https://github.com/luisfabib/fhircraft/pull/79))
- Improve test cases for content reference resolution to include valid URL references ([#79](https://github.com/luisfabib/fhircraft/pull/79))

## Fixed

- Enhance the `_resolve_content_reference` method to support cross-resource references by splitting the `contentReference` into resource URL and path ([#79](https://github.com/luisfabib/fhircraft/pull/79), fixes [#65](https://github.com/luisfabib/fhircraft/pull/65))
- Resolve an obscure bug in the `ResourceFactory._build_element_tree_structure` method that lead to repeated calls to return erroneous results ([#79](https://github.com/luisfabib/fhircraft/pull/79))
- Refine the import and add lazy module loading to fix circular import errors raised when importing certain modules or components ([#80](https://github.com/luisfabib/fhircraft/pull/80))
- Remove unnecessary print/debug statements and redundant imports ([#80](https://github.com/luisfabib/fhircraft/pull/80))
- Suppress (expected) warnings raised during the test suite ([#80](https://github.com/luisfabib/fhircraft/pull/80))


----------------- 

## [0.3.2] - 2025-10-09

### Changed

- Add an option `install_dependencies` to the `load_package` method ([#73](https://github.com/luisfabib/fhircraft/pull/73))

### Fixed

- Change the `pyyaml` dependency to allow newer versions ([#74](https://github.com/luisfabib/fhircraft/pull/72))
- Update the `load_package` method to skip loading a dependency if it has already been loaded ([#73](https://github.com/luisfabib/fhircraft/pull/73))

----------------- 

## [0.3.1] - 2025-10-09

### Fixed

- Fix extraction of `package.json` while processing FHIR package dependencies ([#72](https://github.com/luisfabib/fhircraft/pull/72), fixes [#71](https://github.com/luisfabib/fhircraft/pull/71))

----------------- 

## [0.3.0] - 2025-10-07

### Added
- Implement complete FHIR Mapping Language support with lexer, parser, and execution engine ([#30](https://github.com/luisfabib/fhircraft/pull/30))


- Implement missing FHIRPath math functions ([#47](https://github.com/luisfabib/fhircraft/pull/47))

- Add a complete set of autogenerated Pydantic models for all FHIR canonical core resources across R4, R4B, and R5 releases ([#55](https://github.com/luisfabib/fhircraft/pull/55))

- Implement new utility functions to dynamically import FHIR types (primitive, complex, and resource types) and enable type checking against canonical FHIR resources and generated profiles for improved (FHIRPath) type checking.
([#55](https://github.com/luisfabib/fhircraft/pull/55))


- Implement missing logic for resolving `ElementDefinition.contentReference` references in FHIR structure definitions at model build-time  ([#55](https://github.com/luisfabib/fhircraft/pull/55), fixes [#52](https://github.com/luisfabib/fhircraft/pull/52))

- Ensure correct interpretation of FHIR cardinality and requiredness. Now all Fhircraft model fields are optional, but not nullable, and presence of data elements is delegated to FHIRPath invariants as intended by the specification. ([#60](https://github.com/luisfabib/fhircraft/pull/60))

- Implement missing FHIRPath function `aggregate` ([#62](https://github.com/luisfabib/fhircraft/pull/62), closes [#61](https://github.com/luisfabib/fhircraft/pull/61))

- Implement missing FHIRPath functions added in the FHIR specification ([#62](https://github.com/luisfabib/fhircraft/pull/62), closes [#28](https://github.com/luisfabib/fhircraft/pull/28))

- Implement proper behavior of FHIRPath contextual variables `$this`, `$index`, and `$total` ([#62](https://github.com/luisfabib/fhircraft/pull/62))

- Implement FHIRPath environmental variables and add default variables `%resource`, `%context`, and `%rootResource` to the public API evaluation methods ([#62](https://github.com/luisfabib/fhircraft/pull/62))

- Improve robustness of `ResourceFactory` methods and other minor fixes ([#64](https://github.com/luisfabib/fhircraft/pull/64))
- Correctly validate constrained values in `ResourceFactory` ([#66](https://github.com/luisfabib/fhircraft/pull/66))
- Implement loading of package dependencies ([#68](https://github.com/luisfabib/fhircraft/pull/68))
- Add unit tests and fix issues in code generator ([#69](https://github.com/luisfabib/fhircraft/pull/69))

### Changed

- Implement logic to download FHIR package dependencies when downloading/loading a package ([#68](https://github.com/luisfabib/fhircraft/pull/68)) 

- Update documentation ([#23](https://github.com/luisfabib/fhircraft/pull/23))

- Update the FHIRPath `Element` access operation to return the primitive extension of a primitive FHRI element if its primitive value is not set ([#60](https://github.com/luisfabib/fhircraft/pull/60)).

- Modified the string representation of the FHIRPath classes to represent the shorthand appropriate FHIRPath notation  ([#32](https://github.com/luisfabib/fhircraft/pull/32))

- Enhance FHIR type validation and FHIRPath type operators ([#25](https://github.com/luisfabib/fhircraft/pull/25))

- Only show explicitly set values on `FHIRBaseModel.__repr__` ([#58](https://github.com/luisfabib/fhircraft/pull/58))

- Add docstrings to autogenerated model source code classes ([#55](https://github.com/luisfabib/fhircraft/pull/55)).

- Override the `model_construct` method in all `FHIRBaseModel` subclasses to include default values upon construction ([#55](https://github.com/luisfabib/fhircraft/pull/55)).

- Add Fhircraft metadata to generated source code including timestamp and release version ([#24](https://github.com/luisfabib/fhircraft/pull/24))

- Improve factory logic to avoid duplicated model names and use of class decorator keywords ([#35](https://github.com/luisfabib/fhircraft/pull/35))

- Updated behavior of the FHIRPath equivalence `~` operator to conform to additional FHIR specification constraints  ([#62](https://github.com/luisfabib/fhircraft/pull/62), closes [#29](https://github.com/luisfabib/fhircraft/pull/29))


### Fixed

- Ensure the FHIRPath `HtmlChecks` function validates for valid HTML content  ([#62](https://github.com/luisfabib/fhircraft/pull/62), closes [#44](https://github.com/luisfabib/fhircraft/pull/44))

- Improve factory logic to avoid duplicated model names and use of class decorator keywords ([#35](https://github.com/luisfabib/fhircraft/pull/35))

- Properly handle FHIR structure elements matching Python keywords ([#22](https://github.com/luisfabib/fhircraft/pull/22))

- Avoid setting subclass properties on base classes during resource construction ([#48](https://github.com/luisfabib/fhircraft/pull/48), fixes [#48](https://github.com/luisfabib/fhircraft/pull/48))

- Ensure proper validation of contained FHIR resources into appropriate resource models ([#55](https://github.com/luisfabib/fhircraft/pull/55), fixes [#53](https://github.com/luisfabib/fhircraft/pull/53)).

- Field defaults (other than `None`) are now properly added to generated source code ([#54](https://github.com/luisfabib/fhircraft/pull/54))

- Import-time behavior issues across package modules leading to circular import errors ([#54](https://github.com/luisfabib/fhircraft/pull/54) and [#69](https://github.com/luisfabib/fhircraft/pull/54)).

- Ensure correct FHIR type resolution for the FHIRPath `ofType`, `Is` and `As` functions ([#62](https://github.com/luisfabib/fhircraft/pull/62), fixes [#31](https://github.com/luisfabib/fhircraft/pull/31))

- Update the resource factory to use the correct method (`load_from_files`) for loading `StructureDefinition` from file paths, fixing issues with resource model construction ([#64](https://github.com/luisfabib/fhircraft/pull/64)) 

- Fix validation of constrained values by ensuring proper handling of `BaseModel` instances when structure definition is of a different version than the resource's ([#66](https://github.com/luisfabib/fhircraft/pull/66)) 

**Full Changelog**: https://github.com/luisfabib/fhircraft/compare/0.2.0...0.3.0

----------------- 

## [0.2.0] - 2025-08-12

### Added
- FHIR StructureDefinition repository system for managing FHIR Structure Definitions from local, package, or online sources ([#19](https://github.com/luisfabib/fhircraft/pull/19))
- Client for the FHIR Package Registry and integration with the new repository system ([#20](https://github.com/luisfabib/fhircraft/pull/20))

### Changed
- Improved and expanded the documentation structure and content ([#18](https://github.com/luisfabib/fhircraft/pull/18), [#16](https://github.com/luisfabib/fhircraft/pull/16), [#15](https://github.com/luisfabib/fhircraft/pull/15))
- Comprehensive type safety and code quality improvements across the package ([#17](https://github.com/luisfabib/fhircraft/pull/17))

### Fixed
- Several bug fixes ([#17](https://github.com/luisfabib/fhircraft/pull/17))

**Full Changelog**: https://github.com/luisfabib/fhircraft/compare/0.1.1...0.2.0

----------------- 

## [0.1.1] - 2025-08-07

### Added
- Logic to load a JSON `StructureDefinition` from a file if a string path is provided to the factory method.
- New custom warning class, `FhirPathWarning`, to distinguish (and silence) FHIRPath-related warnings.

### Fixed
- Corrected the search path of Jinja template leading to error when trying to generate code ([#10](https://github.com/luisfabib/fhircraft/pull/11))

### Changed
- Quality of life improvements ([#12](https://github.com/luisfabib/fhircraft/pull/12))
- Prepare patch 0.1.1 ([#13](https://github.com/luisfabib/fhircraft/pull/13))

**Full Changelog**: https://github.com/luisfabib/fhircraft/compare/0.1.0...0.1.1

----------------- 

## [0.1.0] - 2024-08-20

### Added
- Initial release 🎉

[0.4.2]: https://github.com/luisfabib/fhircraft/releases/tag/0.4.2
[0.4.1]: https://github.com/luisfabib/fhircraft/releases/tag/0.4.1
[0.4.0]: https://github.com/luisfabib/fhircraft/releases/tag/0.4.0
[0.3.7]: https://github.com/luisfabib/fhircraft/releases/tag/0.3.7
[0.3.6]: https://github.com/luisfabib/fhircraft/releases/tag/0.3.6
[0.3.5]: https://github.com/luisfabib/fhircraft/releases/tag/0.3.5
[0.3.4]: https://github.com/luisfabib/fhircraft/releases/tag/0.3.4
[0.3.3]: https://github.com/luisfabib/fhircraft/releases/tag/0.3.3
[0.3.2]: https://github.com/luisfabib/fhircraft/releases/tag/0.3.2
[0.3.1]: https://github.com/luisfabib/fhircraft/releases/tag/0.3.1
[0.3.0]: https://github.com/luisfabib/fhircraft/releases/tag/0.3.0
[0.2.0]: https://github.com/luisfabib/fhircraft/releases/tag/0.2.0
[0.1.1]: https://github.com/luisfabib/fhircraft/releases/tag/0.1.1
[0.1.0]: https://github.com/luisfabib/fhircraft/releases/tag/0.1.0
