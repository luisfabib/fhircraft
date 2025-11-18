from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
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

    type: Optional[Code] = Field(
        description="documentation | justification | citation | predecessor | successor | derived-from | depends-on | composed-of | part-of | amends | amended-with | appends | appended-with | cites | cited-by | comments-on | comment-in | contains | contained-in | corrects | correction-in | replaces | replaced-with | retracts | retracted-by | signs | similar-to | supports | supported-with | transforms | transformed-into | transformed-with | documents | specification-of | created-with | cite-as",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    classifier: Optional[List[CodeableConcept]] = Field(
        description="Additional classifiers",
        default=None,
    )
    label: Optional[String] = Field(
        description="Short label",
        default=None,
    )
    label_ext: Optional[Element] = Field(
        description="Placeholder element for label extensions",
        default=None,
        alias="_label",
    )
    display: Optional[String] = Field(
        description="Brief description of the related artifact",
        default=None,
    )
    display_ext: Optional[Element] = Field(
        description="Placeholder element for display extensions",
        default=None,
        alias="_display",
    )
    citation: Optional[Markdown] = Field(
        description="Bibliographic citation for the artifact",
        default=None,
    )
    citation_ext: Optional[Element] = Field(
        description="Placeholder element for citation extensions",
        default=None,
        alias="_citation",
    )
    document: Optional[Attachment] = Field(
        description="What document is being referenced",
        default=None,
    )
    resource: Optional[Canonical] = Field(
        description="What artifact is being referenced",
        default=None,
    )
    resource_ext: Optional[Element] = Field(
        description="Placeholder element for resource extensions",
        default=None,
        alias="_resource",
    )
    resourceReference: Optional[Reference] = Field(
        description="What artifact, if not a conformance resource",
        default=None,
    )
    publicationStatus: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    publicationStatus_ext: Optional[Element] = Field(
        description="Placeholder element for publicationStatus extensions",
        default=None,
        alias="_publicationStatus",
    )
    publicationDate: Optional[Date] = Field(
        description="Date of publication of the artifact being referred to",
        default=None,
    )
    publicationDate_ext: Optional[Element] = Field(
        description="Placeholder element for publicationDate extensions",
        default=None,
        alias="_publicationDate",
    )

    @field_validator(
        *(
            "publicationDate",
            "publicationStatus",
            "resourceReference",
            "resource",
            "document",
            "citation",
            "display",
            "label",
            "classifier",
            "type",
            "extension",
        ),
        mode="after",
        check_fields=None,
    )
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*("extension",), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
