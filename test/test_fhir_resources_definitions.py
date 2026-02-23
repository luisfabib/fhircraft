"""
Tests for the StructureDefinition indexer module.
"""

import tempfile
from pathlib import Path
from fhircraft.fhir.resources.indexer import (
    Manifest,
    ManifestEntry,
)


def test_manifest_entry_create():
    entry = ManifestEntry(
        url="http://hl7.org/fhir/StructureDefinition/Patient",
        name="Patient",
        fhir_version="4.0.1",
        kind="resource",
        filename="patient.json",
        has_snapshot=True,
        has_differential=False,
    )
    assert entry.url == "http://hl7.org/fhir/StructureDefinition/Patient"
    assert entry.name == "Patient"


def test_manifest_create_empty():
    manifest = Manifest()
    assert len(manifest.definitions) == 0
    assert len(manifest.by_url) == 0
    assert len(manifest.by_name) == 0


def test_manifest_to_dict():
    manifest = Manifest()
    entry = ManifestEntry(
        url="http://hl7.org/fhir/StructureDefinition/Patient",
        name="Patient",
        fhir_version="4.0.1",
        kind="resource",
        filename="patient.json",
    )
    manifest.definitions["patient.json"] = entry
    manifest.by_url["http://hl7.org/fhir/StructureDefinition/Patient"] = "patient.json"
    manifest.by_name["Patient"] = ["http://hl7.org/fhir/StructureDefinition/Patient"]

    data = manifest.to_dict()
    assert "definitions" in data
    assert "by_url" in data
    assert "by_name" in data


def test_manifest_save_and_load():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        manifest_path = tmpdir_path / ".manifest.json"

        # Create and save
        manifest = Manifest()
        entry = ManifestEntry(
            url="http://hl7.org/fhir/StructureDefinition/Patient",
            name="Patient",
            fhir_version="4.0.1",
            kind="resource",
            filename="patient.json",
            has_snapshot=True,
        )
        manifest.definitions["patient.json"] = entry
        manifest.by_url["http://hl7.org/fhir/StructureDefinition/Patient"] = (
            "patient.json"
        )
        manifest.by_name["Patient"] = [
            "http://hl7.org/fhir/StructureDefinition/Patient"
        ]

        manifest.save(manifest_path)

        # Load and verify
        loaded = Manifest.load(manifest_path)
        assert len(loaded.definitions) == 1
        assert "patient.json" in loaded.definitions
        assert (
            loaded.definitions["patient.json"].url
            == "http://hl7.org/fhir/StructureDefinition/Patient"
        )
        assert loaded.definitions["patient.json"].has_snapshot is True
