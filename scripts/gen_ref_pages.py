"""Generate the code reference pages organized by logical sections."""

import re
from pathlib import Path
from typing import List, Union

import mkdocs_gen_files

root = Path(__file__).parent.parent
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
        "patterns": [],
        "files": ["fhir/resources/base.py"],
    },
    {
        "output": "reference/fhir-resources-primitives.md",
        "title": "FHIR Primitive Types",
        "description": "Primitive data types.",
        "patterns": [r"^fhir/resources/datatypes/primitives.py"],
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
    # {
    #     "output": "reference/fhir-resources-r4b-complex.md",
    #     "title": "FHIR R4B Complex Types",
    #     "description": "Classes representing FHIR R4B complex data types.",
    #     "patterns": [r"^fhir/resources/datatypes/R4B/complex/.*"],
    #     "files": [],
    # },
    # {
    #     "output": "reference/fhir-resources-r4b-core.md",
    #     "title": "FHIR R4B Core Resources",
    #     "description": "Classes representing FHIR R4B core resources.",
    #     "patterns": [r"^fhir/resources/datatypes/R4B/core/.*"],
    #     "files": [],
    # },
    # {
    #     "output": "reference/fhir-resources-r5-complex.md",
    #     "title": "FHIR R5 Complex Types",
    #     "description": "Classes representing FHIR R5 complex data types.",
    #     "patterns": [r"^fhir/resources/datatypes/R5/complex/.*"],
    #     "files": [],
    # },
    # {
    #     "output": "reference/fhir-resources-r5-core.md",
    #     "title": "FHIR R5 Core Resources",
    #     "description": "Classes representing FHIR R5 core resources.",
    #     "patterns": [r"^fhir/resources/datatypes/R5/core/.*"],
    #     "files": [],
    # },
    {
        "output": "reference/fhir-path.md",
        "title": "FHIR Path",
        "description": "FHIRPath expression evaluation and utilities.",
        "patterns": [
            r"^fhir/path/.*",
        ],
        "files": [],
    },
    {
        "output": "reference/fhir-mapping.md",
        "title": "FHIR Mapping Language",
        "description": "FHIR Mapping Language parser and transformation utilities.",
        "patterns": [
            r"^fhir/mapping/.*",
        ],
        "files": [],
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
]

# Excluded files/modules (basename matching)
EXCLUDE = ["__init__", "__main__", "parser", "lexer", "__pycache__"]


def matches_pattern(module_path: str, patterns: List[str]) -> bool:
    """Check if module path matches any of the regex patterns."""
    for pattern in patterns:
        if re.match(pattern, module_path):
            return True
    return False


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
            if any(excluded in path.parts or path.stem == excluded for excluded in EXCLUDE):
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
            print(f"::: {identifier}", file=fd)
        
        # Set edit path to the first module (or could be omitted)
        if modules:
            mkdocs_gen_files.set_edit_path(output_path, modules[0][0].relative_to(root))