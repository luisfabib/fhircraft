"""
Indexer for FHIR StructureDefinition bundles.

Provides efficient splitting and indexing of large bundle files,
creating individual StructureDefinition files and a lightweight manifest index.
"""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union, overload

import requests
from pydantic import BaseModel

from pydantic_core import ValidationError
from fhircraft.fhir.packages.client import FHIRPackageRegistryClient
from fhircraft.fhir.resources.datatypes.R4.core import (
    StructureDefinition as StructureDefinitionR4,
)
from fhircraft.fhir.resources.datatypes.R4B.core import (
    StructureDefinition as StructureDefinitionR4B,
)
from fhircraft.fhir.resources.datatypes.R5.core import (
    StructureDefinition as StructureDefinitionR5,
)
from fhircraft.fhir.resources.datatypes.registry import get_fhir_type
from fhircraft.utils import load_env_variables


DEFINITIONS_DIR = Path(__file__).resolve().parent

StructureDefinitionUnion = Union[
    StructureDefinitionR4, StructureDefinitionR4B, StructureDefinitionR5
]


class StructureDefinitionNotFoundError(FileNotFoundError):
    """Raised when a required structure definition cannot be resolved."""

    pass


@dataclass
class ManifestEntry:
    """Metadata entry for a single StructureDefinition in the manifest."""

    url: str
    """ Canonical URL (primary key) """

    name: str
    """ StructureDefinition name """

    fhir_version: str
    """ FHIR version (e.g., "4.0.1", "4.3.0", "5.0.0") """

    kind: str
    """ Kind (resource, complex-type, primitive-type, etc.) """

    filename: str
    """ Filename where this definition is stored (e.g., "Patient.json") """

    has_snapshot: bool = False
    """ Whether snapshot is present """

    has_differential: bool = False
    """ Whether differential is present """


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

    def __contains__(self, item):
        """Check if a URL or a name is in the manifest."""
        return item in self.by_url or item in self.by_name


class StructureDefinitionRegistry:
    """Registry for managing indexed StructureDefinitions."""

    fhir_release: str
    """ FHIR release version (e.g., "4.0.1", "4.3.0", "5.0.0"). """

    structure_definitions_by_url: "Dict[str, StructureDefinitionR4 | StructureDefinitionR4B | StructureDefinitionR5]"
    """ Mapping of base URL to version to StructureDefinition instance. """

    local_manifest: Manifest
    """ Manifest of local definitions"""

    def __init__(self, fhir_release: str):
        self.fhir_release = fhir_release
        self._internet_access_enabled = False
        self.structure_definitions_by_url = {}
        self._package_client = FHIRPackageRegistryClient()
        self._load_local_definitions_manifest()

    def _load_local_definitions_manifest(self):
        manifest_path = DEFINITIONS_DIR / self.fhir_release / ".manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(
                f"Manifest file not found for FHIR release {self.fhir_release} at {manifest_path}"
            )
        self.local_manifest = Manifest.load(manifest_path)

    def add(
        self,
        struct_def: "StructureDefinitionR4 | StructureDefinitionR4B | StructureDefinitionR5",
        fail_if_exists: bool = False,
    ) -> None:
        if not struct_def.url:
            raise ValueError(
                "StructureDefinition must have a 'url' field to be added to the repository."
            )

        base_url, _ = self.parse_canonical_url(struct_def.url)
        # Check for duplicates
        if base_url in self and fail_if_exists:
            raise ValueError(
                f"Attempted to load structure definition failed. Canonical URL '{base_url}' already exists in the repository."
            )

        # Store the definition
        self.structure_definitions_by_url[base_url] = struct_def

    def from_dict(
        self,
        struct_def: dict,
        fail_if_exists: bool = False,
    ) -> "StructureDefinitionR4 | StructureDefinitionR4B | StructureDefinitionR5":
        structure_definition = self._validate_structure_definition(struct_def)
        self.add(structure_definition, fail_if_exists=fail_if_exists)
        return structure_definition

    def get(
        self,
        canonical_url: str,
    ) -> "StructureDefinitionR4 | StructureDefinitionR4B | StructureDefinitionR5":

        # ------------------------------
        # Registry index lookup
        # ------------------------------
        if canonical_url in self.structure_definitions_by_url:
            return self.structure_definitions_by_url[canonical_url]

        # ------------------------------
        # Local definition files lookup
        # ------------------------------
        elif canonical_url in self.local_manifest:
            # Try to find by URL first
            if canonical_url in self.local_manifest.by_url:
                # Get the file path from the manifest and load the structure definition
                file_path = (
                    DEFINITIONS_DIR
                    / self.fhir_release
                    / "entries"
                    / self.local_manifest.by_url[canonical_url]
                )
                if not file_path.exists():
                    raise FileNotFoundError(
                        f"Manifest entry found for URL '{canonical_url}' but file '{file_path}' does not exist."
                    )
                # Load and validate the structure definition
                with open(file_path, "r", encoding="utf-8") as f:
                    return self.from_dict(json.load(f))

        # ------------------------------
        # Internet access lookup
        # ------------------------------
        elif self._internet_access_enabled:
            # Fall back to internet if enabled
            return self.from_dict(self.download_url(canonical_url))

        raise StructureDefinitionNotFoundError(
            f"Structure definition not found for {canonical_url}. Either load it locally, load the appropriate package, or enable internet access to download it."
        )

    # ------------------------------
    # Configuration methods
    # ------------------------------

    def enable_internet_access(self):
        """Enable internet access for downloading structure definitions."""
        self._internet_access_enabled = True

    def disable_internet_access(self):
        """Disable internet access for downloading structure definitions."""
        self._internet_access_enabled = False

    # ------------------------------
    # Helper methods
    # ------------------------------

    def _validate_structure_definition(
        self, data: Dict[str, Any]
    ) -> "StructureDefinitionR4 | StructureDefinitionR4B | StructureDefinitionR5":
        StructureDefinition = get_fhir_type("StructureDefinition", self.fhir_release)
        try:
            if isinstance(data, BaseModel):
                data = data.model_dump()
            return StructureDefinition.model_validate(data)
        except ValidationError as e:
            raise ValueError(
                f"Data does not conform to expected structure definition for FHIR release {self.fhir_release}: \n\n{str(e)}"
            ) from e

    @staticmethod
    def download_url(url: str) -> Dict[str, Any]:
        """Download JSON content from a URL."""
        # Configure proxy if needed
        settings = load_env_variables()
        proxies = (
            {
                k: v
                for k, v in {
                    "https": settings.get("PROXY_URL_HTTPS"),
                    "http": settings.get("PROXY_URL_HTTP"),
                }.items()
                if v is not None
            }
            if settings.get("PROXY_URL_HTTPS") or settings.get("PROXY_URL_HTTP")
            else None
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, application/json+fhir, text/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        }
        # Download the StructureDefinition JSON
        response = requests.get(
            url,
            proxies=proxies,
            verify=settings.get("CERTIFICATE_BUNDLE_PATH"),
            headers=headers,
            allow_redirects=True,
        )
        response.raise_for_status()
        return response.json()

    def download_package(self, package_name: str, version: str) -> None:
        """Download a package from the registry and add its structure definitions to the registry."""
        for sd in self._package_client.load_resources_from_package(
            "StructureDefinition", package_name, version
        ):
            structure_definition = self._validate_structure_definition(sd)
            self.add(structure_definition)

    def set_registry_base_url(self, base_url: str) -> None:
        """Change the package registry base URL."""
        self._package_client.base_url = base_url

    @staticmethod
    def parse_canonical_url(canonical_url: str) -> Tuple[str, Optional[str]]:
        """Parse a canonical URL to extract base URL and version."""
        if "|" in canonical_url:
            base_url, version = canonical_url.split("|", 1)
            return base_url.strip(), version.strip()
        return canonical_url.strip(), None

    def __contains__(self, item):
        """Check if a URL or a name is in the manifest."""
        return (
            item in self.structure_definitions_by_url
            or item in self.local_manifest.by_url
        )
