from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    DataType,
    CodeableConcept,
    Element,
    Attachment,
    Reference,
)


class RelatedArtifact(DataType):
    """
    Related artifacts for a knowledge resource
    """

    _type = "RelatedArtifact"

    type: Optional[fhir.code] = Field(
        description="documentation | justification | citation | predecessor | successor | derived-from | depends-on | composed-of | part-of | amends | amended-with | appends | appended-with | cites | cited-by | comments-on | comment-in | contains | contained-in | corrects | correction-in | replaces | replaced-with | retracts | retracted-by | signs | similar-to | supports | supported-with | transforms | transformed-into | transformed-with | documents | specification-of | created-with | cite-as",
        default=None,
    )
    classifier: Optional[List[CodeableConcept]] = Field(
        description="Additional classifiers",
        default=None,
    )
    label: Optional[fhir.string] = Field(
        description="Short label",
        default=None,
    )
    display: Optional[fhir.string] = Field(
        description="Brief description of the related artifact",
        default=None,
    )
    citation: Optional[fhir.markdown] = Field(
        description="Bibliographic citation for the artifact",
        default=None,
    )
    document: Optional[Attachment] = Field(
        description="What document is being referenced",
        default=None,
    )
    resource: Optional[fhir.canonical] = Field(
        description="What artifact is being referenced",
        default=None,
    )
    resourceReference: Optional[Reference] = Field(
        description="What artifact, if not a conformance resource",
        default=None,
    )
    publicationStatus: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    publicationDate: Optional[fhir.date_] = Field(
        description="Date of publication of the artifact being referred to",
        default=None,
    )
