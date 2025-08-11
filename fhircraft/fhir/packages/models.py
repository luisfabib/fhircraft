"""Pydantic models for FHIR Package Registry API."""

from typing import Dict, Optional

from pydantic import BaseModel, Field


class Package(BaseModel):
    """An object describing a package."""

    name: Optional[str] = Field(
        None, description="Package name", examples=["hl7.fhir.us.core"]
    )
    description: Optional[str] = Field(
        None,
        description="Package description",
        examples=[
            "The US Core Implementation Guide is based on FHIR Version R4 and defines "
            "the minimum conformance requirements for accessing patient data."
        ],
    )
    fhir_version: Optional[str] = Field(
        None, alias="fhirVersion", description="Package FHIR version", examples=["R4"]
    )


class PackageDistribution(BaseModel):
    """Distribution information for a package version."""

    shasum: Optional[str] = Field(
        None, examples=["8dd6ac852c1d2cb4ac7312188d8d6ef7ccb65da6"]
    )
    tarball: Optional[str] = Field(
        None, examples=["https://packages.simplifier.net/hl7.fhir.us.core/1.0.0"]
    )


class PackageVersion(Package):
    """An object describing a specific version of a package."""

    version: Optional[str] = Field(
        None, description="Package version", examples=["1.0.0"]
    )
    dist: Optional[PackageDistribution] = None
    url: Optional[str] = Field(
        None,
        description="Url for downloading this package",
        examples=["https://packages.simplifier.net/hl7.fhir.us.core/1.0.0"],
    )


class DistributionTags(BaseModel):
    """Tags describing specific package versions."""

    latest: Optional[str] = Field(
        None, description="A pointer to the latest package version", examples=["1.0.0"]
    )


class PackageMetadata(BaseModel):
    """An object listing package metadata and all individual versions."""

    id: Optional[str] = Field(
        None, alias="_id", description="Package Id", examples=["hl7.fhir.us.core"]
    )
    name: Optional[str] = Field(
        None, description="Package name", examples=["hl7.fhir.us.core"]
    )
    dist_tags: Optional[DistributionTags] = Field(
        None, alias="dist-tags", description="Tags describing specific package versions"
    )
    versions: Optional[Dict[str, PackageVersion]] = Field(
        None, description="Dictionary object of package versions"
    )
