"""
Indexer for FHIR StructureDefinition bundles.

Provides efficient splitting and indexing of large bundle files,
creating individual StructureDefinition files and a lightweight manifest index.
"""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ManifestEntry:
    """Metadata entry for a single StructureDefinition in the manifest."""

    url: str  # Canonical URL (primary key)
    name: str  # StructureDefinition name
    fhir_version: str  # FHIR version (e.g., "4.0.1", "4.3.0", "5.0.0")
    kind: str  # Kind (resource, complex-type, primitive-type, etc.)
    filename: str  # Filename where this definition is stored (e.g., "Patient.json")
    has_snapshot: bool = False  # Whether snapshot is present
    has_differential: bool = False  # Whether differential is present


@dataclass
class Manifest:
    """Manifest index for StructureDefinitions in a FHIR version."""

    definitions: Dict[str, ManifestEntry] = field(
        default_factory=dict
    )  # filename -> entry
    by_url: Dict[str, str] = field(default_factory=dict)  # url -> filename
    by_name: Dict[str, List[str]] = field(default_factory=dict)  # name -> list of urls

    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to dictionary for JSON serialization."""
        return {
            "definitions": {
                filename: asdict(entry) for filename, entry in self.definitions.items()
            },
            "by_url": self.by_url,
            "by_name": self.by_name,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Manifest":
        """Create manifest from dictionary."""
        manifest = cls()

        # Reconstruct definitions
        for filename, entry_dict in data.get("definitions", {}).items():
            entry = ManifestEntry(**entry_dict)
            manifest.definitions[filename] = entry

        # Reconstruct indexes
        manifest.by_url = data.get("by_url", {})
        manifest.by_name = data.get("by_name", {})

        return manifest

    def save(self, path: Path) -> None:
        """Save manifest to JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "Manifest":
        """Load manifest from JSON file."""
        if not path.exists():
            return cls()
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
