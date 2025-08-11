"""FHIR Package Registry client and models."""

from .client import (
    FHIRPackageRegistryClient,
    FHIRPackageRegistryError,
    PackageNotFoundError,
    download_latest_package,
    download_package,
    get_package_metadata,
)
from .models import (
    DistributionTags,
    Package,
    PackageDistribution,
    PackageMetadata,
    PackageVersion,
)

__all__ = [
    # Client classes
    "FHIRPackageRegistryClient",
    "FHIRPackageRegistryError",
    "PackageNotFoundError",
    # Convenience functions
    "get_package_metadata",
    "download_package",
    "download_latest_package",
    # Models
    "Package",
    "PackageVersion",
    "PackageMetadata",
    "PackageDistribution",
    "DistributionTags",
]
