"""Generate the code reference pages organized by logical sections."""

import importlib
import inspect
import re
import sys
from pathlib import Path
from typing import List, Union
import logging

import mkdocs_gen_files

logger = logging.getLogger(__name__)

root = Path(__file__).parent.parent.parent
src = root / "fhircraft"

# Define documentation sections with their patterns
# Each section can specify:
# - 'files': list of specific module paths (relative to src)
# - 'patterns': list of regex patterns to match module paths
CONFIGS = [
    {
        "output": "reference/fhir-resources-base.md",
        "title": "Base FHIR Models",
        "description": "These classes provide base for constructing Fhircraft-compatible Pydantic FHIR models.",
        "patterns": [r"^fhir/resources/base/.*"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-factory.md",
        "title": "FHIR Model Factory",
        "description": "Main class and utilities for dynamically constructing FHIR resource models.",
        "patterns": [r"^fhir/resources/factory/.*"],
        "files": ["fhir/resources/validators.py"],
    },
    {
        "output": "reference/fhir-resources-definitions.md",
        "title": "Structure Definitions Registry",
        "description": "Main class and utilities for managing FHIR structure definitions.",
        "patterns": [r"^fhir/resources/definitions/.*"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-code-generator.md",
        "title": "Code Generator",
        "description": "FHIR resource code generation utilities.",
        "patterns": [],
        "files": ["fhir/resources/generator.py"],
    },
    {
        "output": "reference/fhir-resources-primitives.md",
        "title": "FHIR Primitive Types",
        "description": "Primitive data types.",
        "patterns": [r"^fhir/resources/datatypes/primitives.py"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-type-registries.md",
        "title": "FHIR Types Registries",
        "description": "Registry classes and functions for managing FHIR types.",
        "patterns": [r"^fhir/resources/datatypes/registry.py"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-type-utils.md",
        "title": "FHIR Types Utilities",
        "description": "Utility classes and functions for getting and validating FHIR types.",
        "patterns": [r"^fhir/resources/datatypes/utils.py"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-r4-primitive.md",
        "title": "FHIR R4 Primitive Types",
        "description": "Classes representing FHIR R4 primitive types.",
        "patterns": [r"^fhir/resources/datatypes/R4/primitive/.*"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-r4-complex.md",
        "title": "FHIR R4 Complex Types",
        "description": "Classes representing FHIR R4 complex data types.",
        "patterns": [r"^fhir/resources/datatypes/R4/complex/.*"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-r4-core.md",
        "title": "FHIR R4 Core Resources",
        "description": "Classes representing FHIR R4 core resources.",
        "patterns": [r"^fhir/resources/datatypes/R4/core/.*"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-r4b-primitive.md",
        "title": "FHIR R4B Primitive Types",
        "description": "Classes representing FHIR R4B primitive types.",
        "patterns": [r"^fhir/resources/datatypes/R4B/primitive/.*"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-r4b-complex.md",
        "title": "FHIR R4B Complex Types",
        "description": "Classes representing FHIR R4B complex data types.",
        "patterns": [r"^fhir/resources/datatypes/R4B/complex/.*"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-r4b-core.md",
        "title": "FHIR R4B Core Resources",
        "description": "Classes representing FHIR R4B core resources.",
        "patterns": [r"^fhir/resources/datatypes/R4B/core/.*"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-r5-primitive.md",
        "title": "FHIR R5 Primitive Types",
        "description": "Classes representing FHIR R5 primitive types.",
        "patterns": [r"^fhir/resources/datatypes/R5/primitive/.*"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-r5-complex.md",
        "title": "FHIR R5 Complex Types",
        "description": "Classes representing FHIR R5 complex data types.",
        "patterns": [r"^fhir/resources/datatypes/R5/complex/.*"],
        "files": [],
    },
    {
        "output": "reference/fhir-resources-r5-core.md",
        "title": "FHIR R5 Core Resources",
        "description": "Classes representing FHIR R5 core resources.",
        "patterns": [r"^fhir/resources/datatypes/R5/core/.*"],
        "files": [],
    },
    {
        "output": "reference/fhir-path-engine.md",
        "title": "FHIRPath Engine",
        "description": "FHIRPath evaluation engine components",
        "patterns": [
            r"^fhir/path/engine/.*",
        ],
        "files": [],
    },
    {
        "output": "reference/fhir-path-parser.md",
        "title": "FHIRPath Parser & Lexer",
        "description": "FHIRPath lexer and parser components",
        "patterns": [],
        "files": [
            "fhir/path/lexer.py",
            "fhir/path/parser.py",
        ],
    },
    {
        "output": "reference/fhir-path-mixin.md",
        "title": "FHIRPath Mixin",
        "description": "FHIRPath mixin components",
        "patterns": [],
        "files": [
            "fhir/path/mixin.py",
        ],
    },
    {
        "output": "reference/fhir-mapping-engine.md",
        "title": "FHIR Mapping Language",
        "description": "FHIR Mapping Language parser and transformation utilities.",
        "patterns": [
            r"^fhir/mapper/engine/.*",
        ],
        "files": [],
    },
    {
        "output": "reference/fhir-mapping-parser.md",
        "title": "FHIR Mapping Language Parser",
        "description": "FHIR Mapping Language parser and lexer utilities.",
        "patterns": [],
        "files": [
            "fhir/mapper/lexer.py",
            "fhir/mapper/parser.py",
        ],
    },
    {
        "output": "reference/core-utilities.md",
        "title": "Core Utilities",
        "description": "Configuration, utilities, and helper functions.",
        "patterns": [
            r"^(config|utils)\.py$",
        ],
        "files": [
            "config.py",
            "utils.py",
        ],
    },
    {
        "output": "reference/fhir-packages-models.md",
        "title": "FHIR Packages Models",
        "description": "FHIR Package Registry data models.",
        "patterns": [],
        "files": [
            "fhir/packages/models.py",
        ],
    },
    {
        "output": "reference/fhir-packages-client.md",
        "title": "FHIR Packages Client",
        "description": "FHIR Package Registry client utilities.",
        "patterns": [],
        "files": [
            "fhir/packages/client.py",
        ],
    },
    {
        "output": "reference/exceptions.md",
        "title": "Exceptions",
        "description": "All public exceptions raised by Fhircraft, organized by component.",
        "patterns": [],
        "files": [
            "exceptions.py",
        ],
    },
]

# Excluded files/modules (basename matching)
EXCLUDE = ["__init__", "__main__", "__pycache__"]


def matches_pattern(module_path: str, patterns: List[str]) -> bool:
    """Check if module path matches any of the regex patterns."""
    for pattern in patterns:
        if re.match(pattern, module_path):
            return True
    return False


def get_module_objects(identifier: str) -> List[str]:
    """Get all public objects defined in a module (not imported).

    Returns:
        List of fully qualified object names
    """
    objects = []
    try:
        # Add the root directory to Python path if not already there
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))

        module = importlib.import_module(identifier)

        # Get all members and filter for those defined in this module
        for name, obj in inspect.getmembers(module):
            if not name.startswith("_"):  # Only public objects
                # Check if the object is defined in this module
                obj_module = getattr(obj, "__module__", None)
                if obj_module == identifier:
                    # Include classes, functions, and other objects defined in this module
                    if (
                        inspect.isclass(obj)
                        or inspect.isfunction(obj)
                        or inspect.ismethod(obj)
                        or not inspect.ismodule(obj)
                    ):
                        objects.append(f"{identifier}.{name}")
    except Exception as e:
        print(f"Warning: Could not import {identifier}: {e}")
        # Fallback to module-level import if individual object inspection fails
        objects = [identifier]

    return objects if objects else [identifier]


def collect_modules_for_section(section_config: dict) -> List[tuple[Path, str]]:
    """Collect all modules that belong to a section.

    Returns:
        List of (file_path, module_identifier) tuples
    """
    modules = []
    patterns = section_config.get("patterns", [])
    files = section_config.get("files", [])

    # Collect all Python files in the source directory
    for path in sorted(src.rglob("*.py")):
        try:
            # Skip excluded files
            if any(
                excluded in path.parts or path.stem == excluded for excluded in EXCLUDE
            ):
                continue

            module_path = path.relative_to(root).with_suffix("")
            parts = tuple(module_path.parts)

            # Skip if not in fhircraft package
            if parts[0] != "fhircraft":
                continue

            # Convert to relative path from src for pattern matching
            relative_path = str(path.relative_to(src))

            # Check if matches explicit files
            if relative_path in files:
                identifier = ".".join(parts)
                modules.append((path, identifier))
                continue

            # Check if matches any pattern
            if patterns and matches_pattern(relative_path, patterns):
                identifier = ".".join(parts)
                modules.append((path, identifier))

        except Exception:
            continue

    return modules


# Generate documentation pages for each section
for config in CONFIGS:
    modules = collect_modules_for_section(config)

    if not modules:
        continue

    output_path = Path(config["output"])

    with mkdocs_gen_files.open(output_path, "w") as fd:
        # Write section header
        print(f"# {config['title']}\n", file=fd)
        print(f"{config['description']}\n", file=fd)

        # Write each module's documentation
        for path, identifier in modules:
            # Get all objects from the module
            objects = get_module_objects(identifier)

            # Write documentation for each object
            for obj_name in objects:
                print(f"::: {obj_name}", file=fd)
                print("", file=fd)  # Add empty line between objects
        # Set edit path to the first module (or could be omitted)
        if modules:
            mkdocs_gen_files.set_edit_path(output_path, modules[0][0].relative_to(root))
