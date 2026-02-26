# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

----------------- 

## v0.6.5 - 2026-02-26

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.6.5) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.6.5...0.6.4)

### Added

- Added an "AI Tools and Human Attribution" info box to the contributing guidelines, outlining acceptable and unacceptable types of AI-assisted contributions, and emphasizing the requirement for human review and responsibility ([286](https://github.com/luisfabib/fhircraft/pull/286))
- Implemented a manifest-based FHIR resource `StructureDefinition` lookup system for factory model construction based on canonical URL and name for performance and stability ([281](https://github.com/luisfabib/fhircraft/pull/281))

### Changed

- Splited the `definitions/R{x}/profiles-resources.json` and `definitions/R{x}/profiles-types.json` files into individual files containing just the bundled `StructureDefinition` resources, largely decreasing the overall package size ([281](https://github.com/luisfabib/fhircraft/pull/281))

### Fixed

- Added support for the logic that allows correctly creating models for slices of primitive types with extension placeholders, improving compatibility with FHIR extension patterns ([#276](https://github.com/luisfabib/fhircraft/pull/276))
- Fixed errors in factory methods when trying to load structure definitions of complex-type resources ([#281](https://github.com/luisfabib/fhircraft/pull/281))
- Fixed the differential element merging to recursively merge parent elements in the element path hierarchy. This ensures all intervening elements are created and properly merged with base definitions ([#278](https://github.com/luisfabib/fhircraft/pull/278), fixes [#279](https://github.com/luisfabib/fhircraft/pull/279))
- Fixed an issue with the differential merging to ensure that it succeeds even if the base definition has a different base name as the derived resource ([#278](https://github.com/luisfabib/fhircraft/pull/278))
- Ensured that when constructing differential mode profiles, specialized BackboneElement subclasses from the base model are used as bases instead of generic BackboneElement, allowing proper inheritance of backbone element structure ([#283](https://github.com/luisfabib/fhircraft/pull/283), fixes [#277](https://github.com/luisfabib/fhircraft/pull/277))
- Prevented identical inherited properties from being in generated source code of derived classes, while still generating properties that are new or have different implementations ([#285](https://github.com/luisfabib/fhircraft/pull/285))

----------------- 

## v0.6.4 - 2026-02-20

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.6.4) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.6.4...0.6.3)

### Fixed


- Ensured that profiled complex types with pattern or fixed values result in the correct default type when set ([#269](https://github.com/luisfabib/fhircraft/pull/269), fixes [#111](https://github.com/luisfabib/fhircraft/pull/111)) 
- Sanitized StructureDefinition.name values to ensure valid Python class identifiers ([#269](https://github.com/luisfabib/fhircraft/pull/269), fixes [#264](https://github.com/luisfabib/fhircraft/pull/264)) 
- Fixed cardinality resolution to fall back to base model when not resolved in structure definition ([#269](https://github.com/luisfabib/fhircraft/pull/269))
- Fixed the construction of slice models by passing the correct base class for constructing its element fields ([#269](https://github.com/luisfabib/fhircraft/pull/269))
- Changed the representation of fixed-value constraints from `Enum` and `Literal` to proper Pydantic field validators to ensure correct functionality even for complex values ([#269](https://github.com/luisfabib/fhircraft/pull/269), fixes [#263](https://github.com/luisfabib/fhircraft/pull/263)) 
-  Enabled polymorphic deserialization for profile models to accept instances of their parent classes, matching the behavior of dictionary deserialization. Profile fields now properly validate and adopt parent class instances while preserving all data ([#270](https://github.com/luisfabib/fhircraft/pull/270), fixes [#262](https://github.com/luisfabib/fhircraft/pull/262))
-  Ensured FHIR Pydantic fields are always nullable independently of default value ([#269](https://github.com/luisfabib/fhircraft/pull/269))
- Updated the model source code generation logic and template ([#272](https://github.com/luisfabib/fhircraft/pull/272), [#271](https://github.com/luisfabib/fhircraft/pull/271))
   * Removed hardcoded import statements in favor of dynamically generated imports, ensuring that only the required modules and objects are imported for each generated resource ([#272](https://github.com/luisfabib/fhircraft/pull/272), fixes [#261](https://github.com/luisfabib/fhircraft/pull/261))
   * Removed the `model_rebuild()` calls to avoid unnecessary model rebuilds ([#271](https://github.com/luisfabib/fhircraft/pull/271), fixes [#261](https://github.com/luisfabib/fhircraft/pull/267))
   * Avoided setting field descriptions when explicitly set as `None` or empty strings ([#269](https://github.com/luisfabib/fhircraft/pull/269))
- Prevented the resource factory of creating empty slice models if there are no fields and no validators specified for the slice ([#273](https://github.com/luisfabib/fhircraft/pull/273), fixes [#265](https://github.com/luisfabib/fhircraft/pull/265))

----------------- 

## v0.6.3 - 2026-02-13

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.6.3) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.6.3...0.6.2)

### Fixed

- Improve code generator to reduce boilerplate and repetitive code in auto-generated model definitions source code ([#256](https://github.com/luisfabib/fhircraft/pull/256))
  * Updated the code generator to serialize and include non-built-in bases in generated code, enabling proper handling of custom base classes
  * Fixed the factory method for differential elements resolution to ensure properties such as constraints are not reintroduced if not specified by the differential definition
  * Fixed the code generator to also check in ancestor bases of the requested models for inherited validators
  * Prevented unnecessary class variable definitions from being inherited from parent classes to avoid duplicate
- Resolve bug in factory when dealing with differentials that slice an element within a complex or backbone type. When profiling `Observation.code.coding:slice`, the slice cannot be resolved against the base because `Observation.code.coding` is implicitly derived from `Observation.code`'s type rather than explicitly defined in the snapshot. This causes the sliced element to lose type information and be omitted from code generation ([#257](https://github.com/luisfabib/fhircraft/pull/257), fixes [#255](https://github.com/luisfabib/fhircraft/pull/255))
- Ensured that when merging the differential element definitions, if the sliced element's ID is present in the base snapshot, then it is resolved against it with fallback to resolution against the path ([#257](https://github.com/luisfabib/fhircraft/pull/257))
- Pattern and fixed-value constraints on slices are now enforced. When a slice definition includes pattern values such as `patternCodeableConcept`, the generated model will validate  slice instances against the specified pattern and include appropriate default values. ([#259](https://github.com/luisfabib/fhircraft/pull/259), fixes [#258](https://github.com/luisfabib/fhircraft/pull/258))
- Limited polymorphic deserialization to abstract FHIR resource classes (`_abstract=True`) to avoid pollution of deserialization of other classes after creating new resource models ([#258](https://github.com/luisfabib/fhircraft/pull/258))

----------------- 

## v0.6.2 - 2026-02-09

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.6.2) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.6.2...0.6.1)

### Added

- Added support to the FHIRPath `resolve()` function for resolution of internal references when the `%resource` environment variable is available ([#252](https://github.com/luisfabib/fhircraft/pull/252))
- Added support for implicit FHIRPath evaluation context to the `evaluate` transform during mapping ([#246](https://github.com/luisfabib/fhircraft/pull/246), fixes [#39](https://github.com/luisfabib/fhircraft/pull/39) and [#217](https://github.com/luisfabib/fhircraft/pull/217))
- Added support for implicit type casting to the `cast` transform during mapping ([#246](https://github.com/luisfabib/fhircraft/pull/246), fixes [#38](https://github.com/luisfabib/fhircraft/pull/38))
- Added support for implicit system detection to the `cp` transform during mapping ([#246](https://github.com/luisfabib/fhircraft/pull/246), fixes [#40](https://github.com/luisfabib/fhircraft/pull/40))



### Changed 

- Updated the FHIR Mapping Language parser to no longer strip quotes from FHIRPath expressions, ensuring that string FHIRPaths within the mappings (e.g. constants) retain their quotes during parsing ([#251](https://github.com/luisfabib/fhircraft/pull/251), fixes [#213](https://github.com/luisfabib/fhircraft/pull/213) and [#216](https://github.com/luisfabib/fhircraft/pull/216))
- Removed support to the FHIRPath `resolve()` function for attempting resolution of URL references using the reference as absolute URL for security reasons, now warning instead ([#252](https://github.com/luisfabib/fhircraft/pull/252))



### Fixed

- Fixed resolution of FHIRPaths within source context scopes for the `where` and `check` statements ([#246](https://github.com/luisfabib/fhircraft/pull/246), fixes [#215](https://github.com/luisfabib/fhircraft/pull/215))
- Fixed documentation mapping examples not returning the correct results ([#246](https://github.com/luisfabib/fhircraft/pull/246), fixes [#220](https://github.com/luisfabib/fhircraft/pull/220))
- Fixed transforms to allow variables to be passed as arguments ([#246](https://github.com/luisfabib/fhircraft/pull/246), fixes [#218](https://github.com/luisfabib/fhircraft/pull/218))
- Expanded the FHIR Mapper parser grammar to allow reserved words (e.g. `group`, `import`, `source`, etc.) to be used as identifiers both in mapping rules and its FHIRPath expressions ([#250](https://github.com/luisfabib/fhircraft/pull/250), fixes [#214](https://github.com/luisfabib/fhircraft/pull/214))
- Modified the FHIRPath `Literal` class so that the string represenations of date, datetime, and time values are represented with an `@` prefix (e.g., `@2014-01-01`), aligning with FHIRPath conventions ([#249](https://github.com/luisfabib/fhircraft/pull/249), fixes [#247](https://github.com/luisfabib/fhircraft/pull/247))
- Fixed the string representation of FHIRPath index invocations (e.g., `a[2]`), which was previously represented with a dot ([#249](https://github.com/luisfabib/fhircraft/pull/249), fixes [#248](https://github.com/luisfabib/fhircraft/pull/248))
- Ensured that `resource_url` cannot be evaluated to `None` within the FHIRPath `resolve()` function, which was leading to `AttributeError` ([#252](https://github.com/luisfabib/fhircraft/pull/252), fixes [#240](https://github.com/luisfabib/fhircraft/pull/240))
- Fixed XML serialization to wrap contained/nested resources in their respective resource type tags during XML serialization ([#253](https://github.com/luisfabib/fhircraft/pull/253), fixes [#219](https://github.com/luisfabib/fhircraft/pull/219))


----------------- 

## v0.6.1 - 2026-02-03

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.6.1) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.6.1...0.6.0)

### Added

- Implemented one official FHIR example file for each core FHIR resource and a corresponding unit test to validate core resource model compliance across R4, R4B, and R5 releases ([#244](https://github.com/luisfabib/fhircraft/pull/244))

### Changed 

- Removed redundant validator methods and duplicate field definitions that unnecessarily overrode their inherited counterparts from the base class ([#236](https://github.com/luisfabib/fhircraft/pull/236))


### Fixed

- Added missing aliases for fields containing reserved keywords (e.g. `class_`, `import_`,  etc.) in 15+ resources across R4, R4B, R5 ensuring correct (de)serialization ([#227](https://github.com/luisfabib/fhircraft/pull/227)) and ensured they are properly evaluated in FHIRPath ([#233](https://github.com/luisfabib/fhircraft/pull/233))
- Added missing `_type` metadata attribute to the R4 `CommunicationRequest` class ([#229](https://github.com/luisfabib/fhircraft/pull/229))
- Added validation to ensure the FHIRPath `iif()` function only operates on singleton collections, fixed criterion evaluation for empty input collections instead of iterating over collection items, and added type checking to ensure criterion evaluates to a boolean value ([#231](https://github.com/luisfabib/fhircraft/pull/231), fixes [#230](https://github.com/luisfabib/fhircraft/pull/230)) 
- Fixed FHIRPath comparison operators when comparing `Quantity` subclasses such as `Age`, `Duration`, etc. ([#232](https://github.com/luisfabib/fhircraft/pull/232), fixes [#226](https://github.com/luisfabib/fhircraft/pull/226)) 
- Updated the `ref-1` constraint validation logic to skip evaluation when `_root_resource` or `_resource` attributes are not set, preventing FHIRPath evaluation errors ([#234](https://github.com/luisfabib/fhircraft/pull/234))
- Changed the FHIRBaseModel context setup for complex types by ensuring `_resource` and `_root_resource` are only set for actual FHIR resources and children objects, not root complex datatypes ([#234](https://github.com/luisfabib/fhircraft/pull/234))
- Added the missing backbone elements for the elements of the R5 `Availability` class ([#236](https://github.com/luisfabib/fhircraft/pull/236))
Ensured that the `List` exposed in the `fhircraft.fhir.resourcres.datatypes.R5.core` module is the FHIR model and not `typing.List` ([#236](https://github.com/luisfabib/fhircraft/pull/236))
- Improved the FHIRPath `comparable()`, `lowBoundary()`, `highBoundary()`, `toQuantity()`, and `toString()` functions to work with `FHIR.Quantity` types and subclasses ([#238](https://github.com/luisfabib/fhircraft/pull/238))
- Fixed issue in FHIRPath `comparable()` function to return `False` when one of the input values evaluates to `None`, conforming with the FHIRPath specification for this function ([#239](https://github.com/luisfabib/fhircraft/pull/239))
- Fixed errors during validation due to `%resource` not being defined by moving all FHIR invariant constraint validators in classes inheriting from `BackboneElement` to their core resource parent class to ensure they evaluate within the context of the full resource ([#236](https://github.com/luisfabib/fhircraft/pull/236))
- ixed FHIRPath math operators (addition, subtraction, multiplication, division) to work with mixed FHIRPath and FHIR `Quantity` types and with quantities of different (compatible) units ([#238](https://github.com/luisfabib/fhircraft/pull/238))
- Fixed `toString()` conversion to properly extract unit from `FHIR.Quantity` objects ([#238](https://github.com/luisfabib/fhircraft/pull/238))
- Fixed handling of UCUM unit codes with special characters (square brackets, quotes, curly braces) to ensure that UCUM unit codes such as, e.g. `mm[Hg]`, `{fractions}`, or `[arb'Unit]` are properly processed by FHIRPath `Quantity` objects ([#238](https://github.com/luisfabib/fhircraft/pull/238))
- Added missing `manufactured_item_definition` and `nutrition_product` imports to the R4B core module ([#241](https://github.com/luisfabib/fhircraft/pull/241))
- Added missing `resourceType` field to the R4B `ExampleScenarioInstance` class ([#241](https://github.com/luisfabib/fhircraft/pull/241))
- Updated the initialization of `UnitRegistry` in FHIRPath `Quantity` literals to set `autoconvert_offset_to_baseunit=True`, ensuring offset units are automatically converted to their base units ([#243](https://github.com/luisfabib/fhircraft/pull/243), fixes [#242](https://github.com/luisfabib/fhircraft/pull/242))


----------------- 

## v0.6.0 - 2026-01-30

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.6.0) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.6.0...0.5.0)

### Added

- Added support for differential-based FHIR model construction allowing more efficient resource creation and modification ([#156](https://github.com/luisfabib/fhircraft/pull/156))
    * Established using the `StructureDefinition.differential` as default behavior for contructing FHIR resource models. 
    * Introduced `construction_mode` configuration to the resource factory with `SNAPSHOT`, `DIFFERENTIAL`, and `AUTO` modes to control how to build resource models from structure definitions
- Added support for XML (de)serialization of FHIR resources through the new methods `model_dump_xml` and `model_validate_xml` ([#154](https://github.com/luisfabib/fhircraft/pull/154))
- Added support for mapping arbitrary structures as sources in FHIR Mapping Language enabling more flexible data transformations without requiring a strict structure definition ([#153](https://github.com/luisfabib/fhircraft/pull/153))
- Added support for nested target elements in FHIR Mapping Language parser to detect nested target paths and recursively expand them into intermediate targets with generated variables and nested rules, following the FHIR specification ([#160](https://github.com/luisfabib/fhircraft/pull/160))
- Added suuport for identity transforms and default group mappings in the FHIR Mapping Language engine ([#165](https://github.com/luisfabib/fhircraft/pull/165), fixes [#164](https://github.com/luisfabib/fhircraft/issues/164))
  - Enhanced the mapping engine to track groups with `StructureMap.group.typeMode` of `types` or `type-and-types` and makes them available for automatic invocation when using default mapping rules.
  - Introduced an internal `_DefaultMappingGroup_` symbol both for the FML parser and mapping engine to denote a dynamic mapping group that resolves into an appropriate default mapping group based on type context, with fallback to a simple copy group.
- Overhauled the  documentation ([#184](https://github.com/luisfabib/fhircraft/pull/184))
  - Added new user guides with better storylines, clearer explanation, better examples and with references to external resources   
  - Restructured the technical API reference for better navigation and removed internal (private) API documentation
  - Added a new suite of tests that ensure that all documentation examples are error-free.
- Added `ElementDefinition` models missing for all FHIR releases (R4, R4B, R5) ([#189](https://github.com/luisfabib/fhircraft/pull/189))
- Missing nested backbone elements in `Dosage`, `Timing` and `DataRequirements` complex types across R4, R4B and R5 ([#224](https://github.com/luisfabib/fhircraft/pull/224))
- Added multi-release FHIR Support for mapping parser and engine ([#221](https://github.com/luisfabib/fhircraft/pull/221))
- Added new class variables to all `FHIRBaseModel` subclasses to contain FHIR metadata ([#212](https://github.com/luisfabib/fhircraft/pull/212))
  - Added `_abstract` to indicate concrete resource implementations
  - Added `_type` field containing the FHIR resource type name to replace the now removed Pydantic field `resourceType`
  - Added `_canonical_url` containing the official HL7 FHIR structure definition URL

### Changed

- All Pydantic FHIR models now forbid extra fields for enhanced validation and strict FHIR conformance ([#223](https://github.com/luisfabib/fhircraft/pull/223))
- Updated the FHIRPath and FHIR Mapping Language parsers and lexers to reduce overhead and wasteful instantiation greatly improving overall performance ([#155](https://github.com/luisfabib/fhircraft/pull/155))
- Updated the type choice validator `validate_type_choice_element` to also check for the absence of types not permitted by the structure definition ([#156](https://github.com/luisfabib/fhircraft/pull/156))
- Updated the FHIRPath mixin methods now include optional `environment` argument for custom environment variables ([#169](https://github.com/luisfabib/fhircraft/pull/169), fixes [#166](https://github.com/luisfabib/fhircraft/issues/166))
- Changed FHIR model fields validation to support both name (`validate_by_name`) and alias (`validate_by_alias`) validation ([#175](https://github.com/luisfabib/fhircraft/pull/175))
- Changed the FHIR Mapping Language comment handling to ignore comments rather than attempting to parse them as `StructureMap` documentation elements ([#182](https://github.com/luisfabib/fhircraft/pull/182))
  
- FHIR constraint validators refactored from field-level to model-level validation for proper environment access ([#201](https://github.com/luisfabib/fhircraft/pull/201))
- Added multiple checks to raise errors in the mapping engine if critical elements are not set in the `StructureMap` resource ([#188](https://github.com/luisfabib/fhircraft/pull/188))
- Refactored all FHIR element constraint validators from Pydantic's `@field_validator` decorator to `@model_validator(mode="after")` to ensure FHIRPath invariant constraint evaluated on fully built instances with access to environment variables ([#201](https://github.com/luisfabib/fhircraft/pull/201), fixes [#190](https://github.com/luisfabib/fhircraft/issues/190))
- Updated the repository and factory methods to now use version-specific models instead of a bootstrapped `StructureDefinition` and `ElementDefinition` model. Avoids lost version-specific data when version-specific fields that were ignored during validation or during round-trip validation ([#210](https://github.com/luisfabib/fhircraft/pull/210))


### Fixed

- Improved the behavior of the code generator for factory-generated models, nested annotations, and type alias serialization ([#156](https://github.com/luisfabib/fhircraft/pull/156), fixes [#138](https://github.com/luisfabib/fhircraft/issues/138))
- Updated the `GreaterThan`, `LessThan`, `LessEqualThan` and `GreaterEqualThan` FHIRPath operators to treat zero (`0`) as a valid value, preventing it from being skipped in comparisons ([#158](https://github.com/luisfabib/fhircraft/pull/158), fixes [#157](https://github.com/luisfabib/fhircraft/issues/157))
- Fixed the evaluation of the FHIRPath `All` operator to properly evaluate the boolean values returned by the criteria expressions ([#158](https://github.com/luisfabib/fhircraft/pull/158))
- Fixed `Extension` field types to use forward references to avoid import errors on runtime ([#159](https://github.com/luisfabib/fhircraft/pull/159))
- Fixed the FHIRPath equality operator string representation to use single equals sign (`=`) to fix errors encountered during mapping ([#163](https://github.com/luisfabib/fhircraft/pull/163), fixes [#161](https://github.com/luisfabib/fhircraft/issues/161) and [#162](https://github.com/luisfabib/fhircraft/issues/162))
- Updated the FHIRPath parser to support type specifiers containing resource names like `FHIR.Patient` ([#170](https://github.com/luisfabib/fhircraft/pull/170), fixes [#170](https://github.com/luisfabib/fhircraft/issues/170))
- Updated the FHIRPath engine to support arguments of type `FHIRPath` in functions already taking `Literal` type values allowing runtime evaluation of dynamic input arguments ([#172](https://github.com/luisfabib/fhircraft/pull/172), fixes [#171](https://github.com/luisfabib/fhircraft/issues/171))
- Fixed the FHIRPath lexer to correctly handle escaped quotes (`\'` and `\"`) in strings supporting escape sequences usch as regexes ([#181](https://github.com/luisfabib/fhircraft/pull/181), fixes [#181](https://github.com/luisfabib/fhircraft/issues/181))
- Improved the code generator's handling of `default_factory` values containing lambda-functions or `BaseModel` instances ([#183](https://github.com/luisfabib/fhircraft/pull/183), fixes [#180](https://github.com/luisfabib/fhircraft/issues/180))
- Fixed multiple bugs in the FHIR Mapping Language engine ([#188](https://github.com/luisfabib/fhircraft/pull/188))
  - Fixed a bug leading to resolvable structure types not being recognized and treating all targets as `ArbitraryModel` instances and returning dictionaries (Fixes [#187](https://github.com/luisfabib/fhircraft/issues/187))
  - Fixed structure definition resolution logic in mapping engine to use `StructureDefinition.name` as default alias when not specified
  - Fixed HTML validation issues in FHIR Mapping Language parser when setting `StructureMap.text` with HTML-escaping mapping content
- Fixed a `TypeError` in FHIRPath `Union` operation by removing unnecessary sorting that failed when collections contained incomparable types ([#196](https://github.com/luisfabib/fhircraft/pull/1196), fixes [#194](https://github.com/luisfabib/fhircraft/issues/194))
- Fixed the environment variable precedence issue where default FHIRPath variables (`%context`, `%resource`, `%rootResource`, `%fhirRelease`) were overriding user-provided environment variables in nested evaluations. Custom environment variables now properly take precedence over system defaults when both are present ([#197](https://github.com/luisfabib/fhircraft/pull/197), fixes [#193](https://github.com/luisfabib/fhircraft/issues/193))
- Resolved FHIRPath ambiguity issues where negative numbers conflicted with subtraction operators ([#198](https://github.com/luisfabib/fhircraft/pull/198), fixes [#198](https://github.com/luisfabib/fhircraft/issues/198))
- Replaced `type.code.contains(':')` with `type.select(code.contains(':')).exists()` for the official FHIR `eld-11` constraint validation expression in `ElementDefinition` class for R5 release to properly handle collections with multiple `type.code` values ([#199](https://github.com/luisfabib/fhircraft/pull/199), fixes [#195](https://github.com/luisfabib/fhircraft/issues/195))
- Fixed the incorrect resolution of the $this variable in FHIRPath expressions when used within nested function calls. Previously, $this would maintain the outer collection item context instead of updating to reflect the current evaluation context for certain FHIRPath functions ([#203](https://github.com/luisfabib/fhircraft/pull/203), fixes [#202](https://github.com/luisfabib/fhircraft/issues/202))
- Added missing placeholder `*_ext` fields for all primitive `Extension.value[x]` choices ([#206](https://github.com/luisfabib/fhircraft/pull/206), fixes [#205](https://github.com/luisfabib/fhircraft/issues/205))
- Fixed the model factory to now create placeholder elements for list-type elements with correct typing and update all model fields so primitive extension fields for list-type elements use `Optional[List[Optional[Element]]]` for FHIR compliance ([#207](https://github.com/luisfabib/fhircraft/pull/207), fixes [#204](https://github.com/luisfabib/fhircraft/issues/204))
- Ensured that the `%fhirRelease` FHIRPath environment variable is available when evaluating FHIR invariant constraints ([#212](https://github.com/luisfabib/fhircraft/pull/212))
- Enforced stronger validation and regex-patterns for string-representation of FHIR primitive types ([#222](https://github.com/luisfabib/fhircraft/pull/222))
  - Fixed primitive type string representations to avoid partial matches leading to wrong type assignments or checks
  - Fixed integer primitive types to reject out-of-range values for 32-bit signed integers (`Integer`, `PositiveInt`, `UnsignedInt`)
  - Fixed integer primitive types to reject out-of-range values for 64-bit signed integers (`Integer64`)
  - Enhanced the `Base64Binary` primitive type to validate proper base64 encoding and padding rule 
- Added missing nested backbone elements in `Dosage`, `Timing` and `DataRequirements` complex types accross R4, R4B and R5 leading to errors when evaluating their invariant constraints ([#224](https://github.com/luisfabib/fhircraft/pull/224))

### Removed  

- Bootstrapped  `StructureDefinition` and `ElementDefinition` models containing only fields common to all releases and without validation ([#210](https://github.com/luisfabib/fhircraft/pull/210))
- All resourceType fields from resource models that were redundant with new metadata system [#212](https://github.com/luisfabib/fhircraft/pull/212)
- Duplicate `domain_resource.py` and `resource.py` modules in the R4, R4B, and R5 complex-type modules [#212](https://github.com/luisfabib/fhircraft/pull/212)
  

----------------- 

## v0.5.0 - 2025-12-19

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.5.0) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.5.0...0.4.2)

### Added

* Added a new configuration module that provides thread-safe global and context-local configuration management, and exposes functions for configuring, resetting, and modifying validation settings. This includes context manager support and environment variable loading ([#150](https://github.com/luisfabib/fhircraft/pull/150)) 

* Added configuration parameters to control how validation of FHIR resource invariants is executed, including their severity, type of feedback, or completely skipping their validation. ([#150](https://github.com/luisfabib/fhircraft/pull/150)) 

### Changed 

* Changed the logging level from `info` to `debug` for log entries created by the FHIRPath `trace` function. ([#147](https://github.com/luisfabib/fhircraft/pull/147))  

### Fixed 

* Added the `packaging` module as a core dependency to avoid import errors if `pytest` is not installed in the executing environment. ([#149](https://github.com/luisfabib/fhircraft/pull/149), fixes [#148](https://github.com/luisfabib/fhircraft/pull/148)) 

* Updated import statements in core FHIR resource modules to alias `typing.List` as `ListType` where necessary to avoid overshadowing the FHIR `List` model. ([#151](https://github.com/luisfabib/fhircraft/pull/151), fixes [#139](https://github.com/luisfabib/fhircraft/pull/139)) 

## v0.4.2 - 2025-12-05

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.4.2) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.4.2...0.4.1)

### Changed

* Added thread-local stacks to track recursion during polymorphic serialization and deserialization, preventing infinite recursion in nested FHIR resource structures. This replaces the previous global flag approach for recursion protection. ([#142](https://github.com/luisfabib/fhircraft/pull/142))

### Fixed 

* Removed the `generic_FHIR_resource_validator` methods for the outcome, resource, and issues fields in the Bundle resource for R4, R4B, and R5. Since these were calling the previously removed `validate_contained_resource` an error was raised whenever evaluating a `Bundle` ([#140](https://github.com/luisfabib/fhircraft/pull/140))
* Modified `FHIRBaseModel._serialize_fhir_field_polymorphically` and `FHIRBaseModel._deserialize_polymorphically` to remove temporary disabling of polymorphic flags, relying instead on stack-based recursion protection. This ensures that nested resources are handled correctly and safely. ([#142](https://github.com/luisfabib/fhircraft/pull/142), fixes [#141](https://github.com/luisfabib/fhircraft/pull/141))


## v0.4.1 - 2025-12-03

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.4.1) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.4.1...0.4.0)

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

## v0.4.0 - 2025-11-30

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.4.0) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.4.0...0.3.7)

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

## v0.3.7 - 2025-11-26

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.3.7) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.3.7...0.3.6)

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

## v0.3.6 - 2025-11-19

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.3.6) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.3.6...0.3.5)

### Changed

- Update return type of `model_construct` to `Self` to fix type hinting of return value for all `FHIRBaseModel` classes ([#99](https://github.com/luisfabib/fhircraft/pull/99))

### Fixed

- Improved handling of empty collections in FHIRPath `Is` and `As` operators to avoid errors on runtime ([#98](https://github.com/luisfabib/fhircraft/pull/98))
- Fixed the FHIRPath `replace()` fucntion to allowing empty strings `''` to be used for the substitution instead of returning an empty collection ([#100](https://github.com/luisfabib/fhircraft/pull/100))
- Improved the FHIRPath engine better handle cases where the primitive extension/id elements are requested ([#102](https://github.com/luisfabib/fhircraft/pull/102))

----------------- 

## v0.3.5 - 2025-11-19

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.3.5) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.3.5...0.3.4)

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

## v0.3.4 - 2025-11-11

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.3.4) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.3.4...0.3.3)

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

## v0.3.3 - 2025-10-13

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.3.3) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.3.3...0.3.2)

### Changed

- Update `Date`, `DateTime`, and `Time` FHIR type aliases to support native Python date and time types. ([#77](https://github.com/luisfabib/fhircraft/pull/77))
- Remove large number of empty lines between code blocks in autogenerated model class definition source code. ([#78](https://github.com/luisfabib/fhircraft/pull/78))
- Update the internal `resolve_structure_definition` method to accept an optional `version` parameter, enabling version-specific resolution of StructureDefinitions. ([#79](https://github.com/luisfabib/fhircraft/pull/79))
- Add internal functionality to load local FHIR definitions in `CompositeStructureDefinitionRepository` ([#79](https://github.com/luisfabib/fhircraft/pull/79))
- Add an internal `FHIR_version` attribute to the `FactoryConfig` class for more precise version tracking during model construction ([#79](https://github.com/luisfabib/fhircraft/pull/79))
- Improve test cases for content reference resolution to include valid URL references ([#79](https://github.com/luisfabib/fhircraft/pull/79))

### Fixed

- Enhance the `_resolve_content_reference` method to support cross-resource references by splitting the `contentReference` into resource URL and path ([#79](https://github.com/luisfabib/fhircraft/pull/79), fixes [#65](https://github.com/luisfabib/fhircraft/pull/65))
- Resolve an obscure bug in the `ResourceFactory._build_element_tree_structure` method that lead to repeated calls to return erroneous results ([#79](https://github.com/luisfabib/fhircraft/pull/79))
- Refine the import and add lazy module loading to fix circular import errors raised when importing certain modules or components ([#80](https://github.com/luisfabib/fhircraft/pull/80))
- Remove unnecessary print/debug statements and redundant imports ([#80](https://github.com/luisfabib/fhircraft/pull/80))
- Suppress (expected) warnings raised during the test suite ([#80](https://github.com/luisfabib/fhircraft/pull/80))


----------------- 

## v0.3.2 - 2025-10-09

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.3.2) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.3.2...0.3.1)

### Changed

- Add an option `install_dependencies` to the `load_package` method ([#73](https://github.com/luisfabib/fhircraft/pull/73))

### Fixed

- Change the `pyyaml` dependency to allow newer versions ([#74](https://github.com/luisfabib/fhircraft/pull/72))
- Update the `load_package` method to skip loading a dependency if it has already been loaded ([#73](https://github.com/luisfabib/fhircraft/pull/73))

----------------- 

## v0.3.1 - 2025-10-09

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.3.1) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.3.1...0.3.0)

### Fixed

- Fix extraction of `package.json` while processing FHIR package dependencies ([#72](https://github.com/luisfabib/fhircraft/pull/72), fixes [#71](https://github.com/luisfabib/fhircraft/pull/71))

----------------- 

## v0.3.0 - 2025-10-07

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.3.0) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.3.0...0.2.0)

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



----------------- 

## v0.2.0 - 2025-08-12

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.2.0) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.2.0...0.1.1)

### Added
- FHIR StructureDefinition repository system for managing FHIR Structure Definitions from local, package, or online sources ([#19](https://github.com/luisfabib/fhircraft/pull/19))
- Client for the FHIR Package Registry and integration with the new repository system ([#20](https://github.com/luisfabib/fhircraft/pull/20))

### Changed
- Improved and expanded the documentation structure and content ([#18](https://github.com/luisfabib/fhircraft/pull/18), [#16](https://github.com/luisfabib/fhircraft/pull/16), [#15](https://github.com/luisfabib/fhircraft/pull/15))
- Comprehensive type safety and code quality improvements across the package ([#17](https://github.com/luisfabib/fhircraft/pull/17))

### Fixed
- Several bug fixes ([#17](https://github.com/luisfabib/fhircraft/pull/17))



----------------- 

## v0.1.1 - 2025-08-07

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.1.1) | [Full Changelog](https://github.com/luisfabib/fhircraft/compare/0.1.1...0.1.0)

### Added
- Logic to load a JSON `StructureDefinition` from a file if a string path is provided to the factory method.
- New custom warning class, `FhirPathWarning`, to distinguish (and silence) FHIRPath-related warnings.

### Fixed
- Corrected the search path of Jinja template leading to error when trying to generate code ([#10](https://github.com/luisfabib/fhircraft/pull/11))

### Changed
- Quality of life improvements ([#12](https://github.com/luisfabib/fhircraft/pull/12))
- Prepare patch 0.1.1 ([#13](https://github.com/luisfabib/fhircraft/pull/13))



----------------- 

## v0.1.0 - 2024-08-20

[GitHub Release](https://github.com/luisfabib/fhircraft/releases/tag/0.1.0)

### Added
- Initial release 🎉
