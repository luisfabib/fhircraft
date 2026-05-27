"""Tests for FHIR Package Registry client."""

import io
import json
import tarfile
from unittest.mock import Mock, patch

import pytest

from fhircraft.fhir.packages import (
    PackageMetadata,
    FHIRPackageRegistryClient
)
from fhircraft.exceptions import (
   PackageResolutionError,
   PackageNotFoundError,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_tar(files: dict) -> tarfile.TarFile:
    """Build an in-memory TarFile from a dict of {filename: bytes_or_str}."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for name, content in files.items():
            if isinstance(content, str):
                content = content.encode("utf-8")
            info = tarfile.TarInfo(name=name)
            info.size = len(content)
            tf.addfile(info, io.BytesIO(content))
    buf.seek(0)
    return tarfile.open(fileobj=buf, mode="r:gz")


def _sd(url: str, resource_type: str = "StructureDefinition") -> str:
    return json.dumps({"resourceType": resource_type, "url": url})


class TestFHIRPackageRegistryClient:
    """Test cases for FHIRPackageRegistryClient."""

    def test_client_initialization(self):
        """Test client initialization with default and custom parameters."""
        # Default initialization
        client = FHIRPackageRegistryClient()
        assert client.base_url == FHIRPackageRegistryClient.FHIR_ORG_BASE_URL
        assert client.timeout == 30.0

        # Custom initialization
        custom_url = "https://custom.registry.com"
        client = FHIRPackageRegistryClient(base_url=custom_url, timeout=60.0)
        assert client.base_url == custom_url
        assert client.timeout == 60.0

    @patch("requests.Session.get")
    def test_list_package_versions_success(self, mock_get):
        """Test successful package version listing."""
        # Mock response data
        mock_response_data = {
            "_id": "hl7.fhir.us.core",
            "name": "hl7.fhir.us.core",
            "dist-tags": {"latest": "3.1.1"},
            "versions": {
                "3.1.1": {
                    "name": "hl7.fhir.us.core",
                    "version": "3.1.1",
                    "description": "US Core Implementation Guide",
                    "fhirVersion": "R4",
                }
            },
        }

        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        result = client.list_package_versions("hl7.fhir.us.core")

        # Assertions
        assert isinstance(result, PackageMetadata)
        assert result.id == "hl7.fhir.us.core"
        assert result.name == "hl7.fhir.us.core"
        assert result.dist_tags is not None
        assert result.dist_tags.latest == "3.1.1"
        assert result.versions is not None
        assert "3.1.1" in result.versions

    @patch("requests.Session.get")
    def test_list_package_versions_not_found(self, mock_get):
        """Test package not found error."""
        # Setup mock for 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        with pytest.raises(PackageNotFoundError) as exc_info:
            client.list_package_versions("nonexistent.package")

        assert "not found" in str(exc_info.value)

    @patch("requests.Session.get")
    def test_download_package_success(self, mock_get):
        """Test successful package download."""
        # Mock binary response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake-tar-gz-content"
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        result = client.download_package("hl7.fhir.us.core", "3.1.1")

        # Assertions
        assert isinstance(result, bytes)
        assert result == b"fake-tar-gz-content"

    @patch("requests.Session.get")
    def test_download_package_not_found(self, mock_get):
        """Test package download not found error."""
        # Setup mock for 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        with pytest.raises(PackageNotFoundError) as exc_info:
            client.download_package("nonexistent.package", "1.0.0")

        assert "not found" in str(exc_info.value)

    @patch("requests.Session.get")
    def test_get_latest_version(self, mock_get):
        """Test getting latest version."""
        # Mock response data
        mock_response_data = {
            "_id": "hl7.fhir.us.core",
            "name": "hl7.fhir.us.core",
            "dist-tags": {"latest": "3.1.1"},
        }

        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        latest = client.get_latest_version("hl7.fhir.us.core")

        # Assertions
        assert latest == "3.1.1"

    @patch("requests.Session.get")
    def test_get_latest_version_no_tags(self, mock_get):
        """Test getting latest version when no dist-tags exist."""
        # Mock response data without dist-tags
        mock_response_data = {"_id": "hl7.fhir.us.core", "name": "hl7.fhir.us.core"}

        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        # Test
        client = FHIRPackageRegistryClient()
        latest = client.get_latest_version("hl7.fhir.us.core")

        # Assertions
        assert latest is None


class TestPackageMetadata:
    """Test cases for PackageMetadata model."""

    def test_package_metadata_validation(self):
        """Test PackageMetadata validation with valid data."""
        data = {
            "_id": "hl7.fhir.us.core",
            "name": "hl7.fhir.us.core",
            "dist-tags": {"latest": "3.1.1"},
            "versions": {
                "3.1.1": {
                    "name": "hl7.fhir.us.core",
                    "version": "3.1.1",
                    "description": "US Core Implementation Guide",
                    "fhirVersion": "R4",
                }
            },
        }

        metadata = PackageMetadata.model_validate(data)
        assert metadata.id == "hl7.fhir.us.core"
        assert metadata.name == "hl7.fhir.us.core"
        assert metadata.dist_tags is not None
        assert metadata.dist_tags.latest == "3.1.1"
        assert metadata.versions is not None
        assert "3.1.1" in metadata.versions

    def test_package_metadata_minimal(self):
        """Test PackageMetadata with minimal data."""
        data = {}
        metadata = PackageMetadata.model_validate(data)

        # All fields should be optional
        assert metadata.id is None
        assert metadata.name is None
        assert metadata.dist_tags is None
        assert metadata.versions is None
        assert metadata.versions is None


# ===========================================================================
# TestProcessPackageTar
# ===========================================================================


class TestProcessPackageTar:
    """Tests for FHIRPackageRegistryClient._process_package_tar."""

    def test_returns_sds_from_package(self):
        """SDs in the tar file are extracted and returned."""
        sd_url = "http://example.org/StructureDefinition/MyProfile"
        tar = _make_tar(
            {
                "package/StructureDefinition-MyProfile.json": _sd(sd_url),
            }
        )
        client = FHIRPackageRegistryClient()
        results, errors = client._process_package_tar("StructureDefinition", tar)
        assert errors == []
        assert len(results) == 1
        assert results[0]["url"] == sd_url

    def test_no_dependencies_when_package_json_absent(self):
        """When there is no package.json the dependency loop is skipped."""
        sd_url = "http://example.org/StructureDefinition/MyProfile"
        tar = _make_tar(
            {
                "package/StructureDefinition-MyProfile.json": _sd(sd_url),
            }
        )
        client = FHIRPackageRegistryClient()
        with patch.object(client, "load_resources_from_package") as mock_load:
            results, errors = client._process_package_tar("StructureDefinition", tar)
        mock_load.assert_not_called()
        assert len(results) == 1

    def test_dependency_sds_included_in_results(self):
        """SDs from dependencies are merged into the result list."""
        dep_url = "http://example.org/StructureDefinition/DepProfile"
        dep_sd = {"resourceType": "StructureDefinition", "url": dep_url}

        package_json = json.dumps(
            {"name": "my.pkg", "version": "1.0.0", "dependencies": {"dep.pkg": "1.0.0"}}
        )
        tar = _make_tar({"package/package.json": package_json})

        client = FHIRPackageRegistryClient()
        with patch.object(
            client,
            "load_resources_from_package",
            return_value=[dep_sd],
        ) as mock_load:
            results, errors = client._process_package_tar("StructureDefinition", tar)

        mock_load.assert_called_once_with(
            "StructureDefinition", "dep.pkg", "1.0.0", fail_if_exists=False
        )
        assert errors == []
        assert dep_sd in results

    def test_multiple_dependency_sds_all_included(self):
        """SDs from multiple dependencies are all present in results."""
        dep_a = {"resourceType": "StructureDefinition", "url": "http://example.org/A"}
        dep_b = {"resourceType": "StructureDefinition", "url": "http://example.org/B"}

        package_json = json.dumps(
            {
                "name": "my.pkg",
                "version": "1.0.0",
                "dependencies": {"dep.a": "1.0.0", "dep.b": "2.0.0"},
            }
        )
        tar = _make_tar({"package/package.json": package_json})

        client = FHIRPackageRegistryClient()
        with patch.object(
            client,
            "load_resources_from_package",
            side_effect=[[dep_a], [dep_b]],
        ):
            results, errors = client._process_package_tar("StructureDefinition", tar)

        assert errors == []
        assert dep_a in results
        assert dep_b in results

    def test_already_loaded_dependency_is_skipped(self):
        """A dependency already in history is not re-downloaded."""
        package_json = json.dumps(
            {"name": "my.pkg", "version": "1.0.0", "dependencies": {"dep.pkg": "1.0.0"}}
        )
        tar = _make_tar({"package/package.json": package_json})

        client = FHIRPackageRegistryClient()
        client.history.add("dep.pkg@1.0.0")  # mark as already loaded

        with patch.object(client, "load_resources_from_package") as mock_load:
            results, errors = client._process_package_tar("StructureDefinition", tar)

        mock_load.assert_not_called()
        assert errors == []

    def test_dependency_failure_recorded_as_error_not_raised(self):
        """A failing dependency download is recorded in errors, not raised."""
        package_json = json.dumps(
            {"name": "my.pkg", "version": "1.0.0", "dependencies": {"bad.dep": "9.9.9"}}
        )
        tar = _make_tar({"package/package.json": package_json})

        client = FHIRPackageRegistryClient()
        with patch.object(
            client,
            "load_resources_from_package",
            side_effect=PackageNotFoundError("not found"),
        ):
            results, errors = client._process_package_tar("StructureDefinition", tar)

        assert len(errors) == 1
        assert "bad.dep" in errors[0]
        assert results == []

    def test_install_dependencies_false_skips_dependency_processing(self):
        """When install_dependencies=False the dependency block is never entered."""
        package_json = json.dumps(
            {"name": "my.pkg", "version": "1.0.0", "dependencies": {"dep.pkg": "1.0.0"}}
        )
        tar = _make_tar({"package/package.json": package_json})

        client = FHIRPackageRegistryClient()
        with patch.object(client, "load_resources_from_package") as mock_load:
            results, errors = client._process_package_tar(
                "StructureDefinition", tar, install_dependencies=False
            )

        mock_load.assert_not_called()


# ===========================================================================
# TestLoadResourcesFromPackage – dependency propagation (regression)
# ===========================================================================


class TestLoadResourcesFromPackageDependencies:
    """Regression tests for the bug where dependency SDs were not returned."""

    def _make_download_mock(self, pkg_sd_url: str, dep_sd_url: str):
        """
        Return a side_effect callable that serves two packages:
          - "my.pkg/1.0.0"  → tar with package.json declaring dep.pkg + one SD
          - "dep.pkg/1.0.0" → tar with one SD
        """
        pkg_sd = _sd(pkg_sd_url)
        dep_sd = _sd(dep_sd_url)
        pkg_package_json = json.dumps(
            {"name": "my.pkg", "version": "1.0.0", "dependencies": {"dep.pkg": "1.0.0"}}
        )
        dep_package_json = json.dumps(
            {"name": "dep.pkg", "version": "1.0.0", "dependencies": {}}
        )

        pkg_tar = _make_tar(
            {
                "package/package.json": pkg_package_json,
                "package/StructureDefinition-PkgProfile.json": pkg_sd,
            }
        )
        dep_tar = _make_tar(
            {
                "package/package.json": dep_package_json,
                "package/StructureDefinition-DepProfile.json": dep_sd,
            }
        )

        tars = {"my.pkg": pkg_tar, "dep.pkg": dep_tar}

        def _download(name, version, extract=False):
            tf = tars[name]
            assert tf.fileobj is not None, "TarFile must have fileobj for mock to work"
            # Re-open the same buffer for each download call
            tf.fileobj.seek(0)
            return tarfile.open(fileobj=tf.fileobj, mode="r:gz")

        return _download

    @patch("requests.Session.get")
    def test_register_package_also_returns_dependency_sds(self, mock_get):
        """
        Regression test: load_resources_from_package must include SDs from
        transitive dependencies in its return value, not only the top-level package.
        """
        pkg_sd_url = "http://example.org/StructureDefinition/PkgProfile"
        dep_sd_url = "http://example.org/StructureDefinition/DepProfile"

        # Mock the HTTP layer so download_package calls get real tar content
        def _http_side_effect(url, **kwargs):
            resp = Mock()
            resp.status_code = 200
            if "my.pkg" in url:
                pkg_package_json = json.dumps(
                    {
                        "name": "my.pkg",
                        "version": "1.0.0",
                        "dependencies": {"dep.pkg": "1.0.0"},
                    }
                )
                buf = io.BytesIO()
                with tarfile.open(fileobj=buf, mode="w:gz") as tf:
                    for name, content in {
                        "package/package.json": pkg_package_json,
                        "package/StructureDefinition-PkgProfile.json": _sd(pkg_sd_url),
                    }.items():
                        b = content.encode("utf-8")
                        info = tarfile.TarInfo(name=name)
                        info.size = len(b)
                        tf.addfile(info, io.BytesIO(b))
                resp.content = buf.getvalue()
            else:
                dep_package_json = json.dumps(
                    {"name": "dep.pkg", "version": "1.0.0", "dependencies": {}}
                )
                buf = io.BytesIO()
                with tarfile.open(fileobj=buf, mode="w:gz") as tf:
                    for name, content in {
                        "package/package.json": dep_package_json,
                        "package/StructureDefinition-DepProfile.json": _sd(dep_sd_url),
                    }.items():
                        b = content.encode("utf-8")
                        info = tarfile.TarInfo(name=name)
                        info.size = len(b)
                        tf.addfile(info, io.BytesIO(b))
                resp.content = buf.getvalue()
            return resp

        mock_get.side_effect = _http_side_effect

        client = FHIRPackageRegistryClient()
        results = client.load_resources_from_package(
            "StructureDefinition", "my.pkg", "1.0.0"
        )
        urls = [r["url"] for r in results]

        assert pkg_sd_url in urls, "Top-level package SD must be in results"
        assert (
            dep_sd_url in urls
        ), "Dependency SD must also be in results (regression: was silently dropped)"
