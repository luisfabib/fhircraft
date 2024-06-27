from typing import Dict, Optional

from pydantic import BaseModel

from fhircraft.openapi.models.compat import PYDANTIC_V2, ConfigDict, Extra

_examples = [
    {
        "profile": "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-patient",
        "resourceType": "Patient"
    },
]


class FhirResourceExtension(BaseModel):
    """An object representing a Server."""

    profile: str
    """
    **REQUIRED**. A canonical URL to the resource profile StructureDefinition.
    """

    resourceType: str
    """
    The type of core FHIR resource
    """

    alias: Optional[str] = None
    """
    Alias used for the resource. Must be a FHIRPath environmental variable '%<alias>'
    """

    if PYDANTIC_V2:
        model_config = ConfigDict(
            json_schema_extra={"examples": _examples},
        )

    else:

        class Config:
            schema_extra = {"examples": _examples}
