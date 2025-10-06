from typing import Optional, List

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.base import FHIRBaseModel
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.utils import model_rebuild_all


class Element(FHIRBaseModel):
    """
    Base for all elements
    """

    id: Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: Optional[List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )

    @field_validator(*("extension",), mode="after", check_fields=None)
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class BackboneElement(Element):
    """
    Base for elements defined inside a resource
    """

    modifierExtension: Optional[List["Extension"]] = Field(
        description="Extensions that cannot be ignored even if unrecognized",
        default=None,
    )

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
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

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class xhtml(Element):
    """
    Primitive Type xhtml
    """

    value: Optional[String] = Field(
        description="Actual xhtml",
        default=None,
    )
    value_ext: Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )

    @field_validator(*("extension",), mode="after", check_fields=None)
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


class Address(Element):
    """
    An address expressed using postal conventions (as opposed to GPS or other location definition formats)
    """

    use: Optional[Code] = Field(
        description="home | work | temp | old | billing - purpose of this address",
        default=None,
    )
    use_ext: Optional["Element"] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    type: Optional[Code] = Field(
        description="postal | physical | both",
        default=None,
    )
    type_ext: Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    text: Optional[String] = Field(
        description="Text representation of the address",
        default=None,
    )
    text_ext: Optional["Element"] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
    line: Optional[List[String]] = Field(
        description="Street name, number, direction \u0026 P.O. Box etc.",
        default=None,
    )
    line_ext: Optional["Element"] = Field(
        description="Placeholder element for line extensions",
        default=None,
        alias="_line",
    )
    city: Optional[String] = Field(
        description="Name of city, town etc.",
        default=None,
    )
    city_ext: Optional["Element"] = Field(
        description="Placeholder element for city extensions",
        default=None,
        alias="_city",
    )
    district: Optional[String] = Field(
        description="District name (aka county)",
        default=None,
    )
    district_ext: Optional["Element"] = Field(
        description="Placeholder element for district extensions",
        default=None,
        alias="_district",
    )
    state: Optional[String] = Field(
        description="Sub-unit of country (abbreviations ok)",
        default=None,
    )
    state_ext: Optional["Element"] = Field(
        description="Placeholder element for state extensions",
        default=None,
        alias="_state",
    )
    postalCode: Optional[String] = Field(
        description="Postal code for area",
        default=None,
    )
    postalCode_ext: Optional["Element"] = Field(
        description="Placeholder element for postalCode extensions",
        default=None,
        alias="_postalCode",
    )
    country: Optional[String] = Field(
        description="Country (e.g. can be ISO 3166 2 or 3 letter code)",
        default=None,
    )
    country_ext: Optional["Element"] = Field(
        description="Placeholder element for country extensions",
        default=None,
        alias="_country",
    )
    period: Optional["Period"] = Field(
        description="Time period when address was/is in use",
        default=None,
    )

    @field_validator(
        *(
            "period",
            "country",
            "postalCode",
            "state",
            "district",
            "city",
            "line",
            "text",
            "type",
            "use",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class Annotation(Element):
    """
    Text node with attribution
    """

    authorReference: Optional["Reference"] = Field(
        description="Individual responsible for the annotation",
        default=None,
    )
    authorString: Optional[String] = Field(
        description="Individual responsible for the annotation",
        default=None,
    )
    time: Optional[DateTime] = Field(
        description="When the annotation was made",
        default=None,
    )
    time_ext: Optional["Element"] = Field(
        description="Placeholder element for time extensions",
        default=None,
        alias="_time",
    )
    text: Optional[Markdown] = Field(
        description="The annotation  - text content (as markdown)",
        default=None,
    )
    text_ext: Optional["Element"] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )

    @field_validator(
        *("text", "time", "extension", "extension"), mode="after", check_fields=None
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def author_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Reference", String],
            field_name_base="author",
        )

    @property
    def author(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="author",
        )


class Attachment(Element):
    """
    Content in a format defined elsewhere
    """

    contentType: Optional[Code] = Field(
        description="Mime type of the content, with charset etc.",
        default=None,
    )
    contentType_ext: Optional["Element"] = Field(
        description="Placeholder element for contentType extensions",
        default=None,
        alias="_contentType",
    )
    language: Optional[Code] = Field(
        description="Human language of the content (BCP-47)",
        default=None,
    )
    language_ext: Optional["Element"] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    data: Optional[Base64Binary] = Field(
        description="Data inline, base64ed",
        default=None,
    )
    data_ext: Optional["Element"] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )
    url: Optional[Url] = Field(
        description="Uri where the data can be found",
        default=None,
    )
    url_ext: Optional["Element"] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    size: Optional[UnsignedInt] = Field(
        description="Number of bytes of content (if url provided)",
        default=None,
    )
    size_ext: Optional["Element"] = Field(
        description="Placeholder element for size extensions",
        default=None,
        alias="_size",
    )
    hash: Optional[Base64Binary] = Field(
        description="Hash of the data (sha-1, base64ed)",
        default=None,
    )
    hash_ext: Optional["Element"] = Field(
        description="Placeholder element for hash extensions",
        default=None,
        alias="_hash",
    )
    title: Optional[String] = Field(
        description="Label to display in place of the data",
        default=None,
    )
    title_ext: Optional["Element"] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    creation: Optional[DateTime] = Field(
        description="Date attachment was first created",
        default=None,
    )
    creation_ext: Optional["Element"] = Field(
        description="Placeholder element for creation extensions",
        default=None,
        alias="_creation",
    )

    @field_validator(
        *(
            "creation",
            "title",
            "hash",
            "size",
            "url",
            "data",
            "language",
            "contentType",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_att_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="data.empty() or contentType.exists()",
            human="If the Attachment has data, it SHALL have a contentType",
            key="att-1",
            severity="error",
        )


class CodeableConcept(Element):
    """
    Concept - reference to a terminology or just  text
    """

    coding: Optional[List["Coding"]] = Field(
        description="Code defined by a terminology system",
        default=None,
    )
    text: Optional[String] = Field(
        description="Plain text representation of the concept",
        default=None,
    )
    text_ext: Optional["Element"] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )

    @field_validator(
        *("text", "coding", "extension", "extension"), mode="after", check_fields=None
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class CodeableReference(Element):
    """
    Reference to a resource or a concept
    """

    concept: Optional["CodeableConcept"] = Field(
        description="Reference to a concept (by class)",
        default=None,
    )
    reference: Optional["Reference"] = Field(
        description="Reference to a resource (by instance)",
        default=None,
    )

    @field_validator(
        *("reference", "concept", "extension", "extension"),
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class Coding(Element):
    """
    A reference to a code defined by a terminology system
    """

    system: Optional[Uri] = Field(
        description="Identity of the terminology system",
        default=None,
    )
    system_ext: Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    version: Optional[String] = Field(
        description="Version of the system - if relevant",
        default=None,
    )
    version_ext: Optional["Element"] = Field(
        description="Placeholder element for version extensions",
        default=None,
        alias="_version",
    )
    code: Optional[Code] = Field(
        description="Symbol in syntax defined by the system",
        default=None,
    )
    code_ext: Optional["Element"] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )
    display: Optional[String] = Field(
        description="Representation defined by the system",
        default=None,
    )
    display_ext: Optional["Element"] = Field(
        description="Placeholder element for display extensions",
        default=None,
        alias="_display",
    )
    userSelected: Optional[Boolean] = Field(
        description="If this coding was chosen directly by the user",
        default=None,
    )
    userSelected_ext: Optional["Element"] = Field(
        description="Placeholder element for userSelected extensions",
        default=None,
        alias="_userSelected",
    )

    @field_validator(
        *(
            "userSelected",
            "display",
            "code",
            "version",
            "system",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class ContactDetail(Element):
    """
    Contact information
    """

    name: Optional[String] = Field(
        description="Name of an individual to contact",
        default=None,
    )
    name_ext: Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    telecom: Optional[List["ContactPoint"]] = Field(
        description="Contact details for individual or organization",
        default=None,
    )

    @field_validator(
        *("telecom", "name", "extension", "extension"), mode="after", check_fields=None
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class ContactPoint(Element):
    """
    Details of a Technology mediated contact point (phone, fax, email, etc.)
    """

    system: Optional[Code] = Field(
        description="phone | fax | email | pager | url | sms | other",
        default=None,
    )
    system_ext: Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    value: Optional[String] = Field(
        description="The actual contact point details",
        default=None,
    )
    value_ext: Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    use: Optional[Code] = Field(
        description="home | work | temp | old | mobile - purpose of this contact point",
        default=None,
    )
    use_ext: Optional["Element"] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    rank: Optional[PositiveInt] = Field(
        description="Specify preferred order of use (1 = highest)",
        default=None,
    )
    rank_ext: Optional["Element"] = Field(
        description="Placeholder element for rank extensions",
        default=None,
        alias="_rank",
    )
    period: Optional["Period"] = Field(
        description="Time period when the contact point was/is in use",
        default=None,
    )

    @field_validator(
        *(
            "period",
            "rank",
            "use",
            "value",
            "system",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cpt_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="value.empty() or system.exists()",
            human="A system is required if a value is provided.",
            key="cpt-2",
            severity="error",
        )


class Contributor(Element):
    """
    Contributor information
    """

    type: Optional[Code] = Field(
        description="author | editor | reviewer | endorser",
        default=None,
    )
    type_ext: Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    name: Optional[String] = Field(
        description="Who contributed the content",
        default=None,
    )
    name_ext: Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    contact: Optional[List["ContactDetail"]] = Field(
        description="Contact details of the contributor",
        default=None,
    )

    @field_validator(
        *("contact", "name", "type", "extension", "extension", "extension"),
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


class DataRequirement(Element):
    """
    Describes a required data item
    """

    type: Optional[Code] = Field(
        description="The type of the required data",
        default=None,
    )
    type_ext: Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    profile: Optional[List[Canonical]] = Field(
        description="The profile of the required data",
        default=None,
    )
    profile_ext: Optional["Element"] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )
    subjectCodeableConcept: Optional["CodeableConcept"] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
    )
    subjectReference: Optional["Reference"] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
    )
    mustSupport: Optional[List[String]] = Field(
        description="Indicates specific structure elements that are referenced by the knowledge module",
        default=None,
    )
    mustSupport_ext: Optional["Element"] = Field(
        description="Placeholder element for mustSupport extensions",
        default=None,
        alias="_mustSupport",
    )
    codeFilter: Optional[List["Element"]] = Field(
        description="What codes are expected",
        default=None,
    )
    dateFilter: Optional[List["Element"]] = Field(
        description="What dates/date ranges are expected",
        default=None,
    )
    limit: Optional[PositiveInt] = Field(
        description="Number of results",
        default=None,
    )
    limit_ext: Optional["Element"] = Field(
        description="Placeholder element for limit extensions",
        default=None,
        alias="_limit",
    )
    sort: Optional[List["Element"]] = Field(
        description="Order of the results",
        default=None,
    )

    @field_validator(
        *(
            "sort",
            "limit",
            "dateFilter",
            "codeFilter",
            "mustSupport",
            "profile",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
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

    @field_validator(*("codeFilter",), mode="after", check_fields=None)
    @classmethod
    def FHIR_drq_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="path.exists() xor searchParam.exists()",
            human="Either a path or a searchParam must be provided, but not both",
            key="drq-1",
            severity="error",
        )

    @field_validator(*("dateFilter",), mode="after", check_fields=None)
    @classmethod
    def FHIR_drq_2_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="path.exists() xor searchParam.exists()",
            human="Either a path or a searchParam must be provided, but not both",
            key="drq-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def subject_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["CodeableConcept", "Reference"],
            field_name_base="subject",
        )

    @property
    def subject(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="subject",
        )


class Dosage(BackboneElement):
    """
    How the medication is/was taken or should be taken
    """

    sequence: Optional[Integer] = Field(
        description="The order of the dosage instructions",
        default=None,
    )
    sequence_ext: Optional["Element"] = Field(
        description="Placeholder element for sequence extensions",
        default=None,
        alias="_sequence",
    )
    text: Optional[String] = Field(
        description="Free text dosage instructions e.g. SIG",
        default=None,
    )
    text_ext: Optional["Element"] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
    additionalInstruction: Optional[List["CodeableConcept"]] = Field(
        description='Supplemental instruction or warnings to the patient - e.g. "with meals", "may cause drowsiness"',
        default=None,
    )
    patientInstruction: Optional[String] = Field(
        description="Patient or consumer oriented instructions",
        default=None,
    )
    patientInstruction_ext: Optional["Element"] = Field(
        description="Placeholder element for patientInstruction extensions",
        default=None,
        alias="_patientInstruction",
    )
    timing: Optional["Timing"] = Field(
        description="When medication should be administered",
        default=None,
    )
    asNeededBoolean: Optional[Boolean] = Field(
        description='Take "as needed" (for x)',
        default=None,
    )
    asNeededCodeableConcept: Optional["CodeableConcept"] = Field(
        description='Take "as needed" (for x)',
        default=None,
    )
    site: Optional["CodeableConcept"] = Field(
        description="Body site to administer to",
        default=None,
    )
    route: Optional["CodeableConcept"] = Field(
        description="How drug should enter body",
        default=None,
    )
    method: Optional["CodeableConcept"] = Field(
        description="Technique for administering medication",
        default=None,
    )
    doseAndRate: Optional[List["Element"]] = Field(
        description="Amount of medication administered",
        default=None,
    )
    maxDosePerPeriod: Optional["Ratio"] = Field(
        description="Upper limit on medication per unit of time",
        default=None,
    )
    maxDosePerAdministration: Optional["Quantity"] = Field(
        description="Upper limit on medication per administration",
        default=None,
    )
    maxDosePerLifetime: Optional["Quantity"] = Field(
        description="Upper limit on medication per lifetime of the patient",
        default=None,
    )

    @field_validator(
        *(
            "maxDosePerLifetime",
            "maxDosePerAdministration",
            "maxDosePerPeriod",
            "doseAndRate",
            "method",
            "route",
            "site",
            "timing",
            "patientInstruction",
            "additionalInstruction",
            "text",
            "sequence",
            "modifierExtension",
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

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
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

    @model_validator(mode="after")
    def asNeeded_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Boolean, "CodeableConcept"],
            field_name_base="asNeeded",
        )

    @property
    def asNeeded(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="asNeeded",
        )


class ElementDefinition(BackboneElement):
    """
    Definition of an element in a resource or extension
    """

    path: Optional[String] = Field(
        description="Path of the element in the hierarchy of elements",
        default=None,
    )
    path_ext: Optional["Element"] = Field(
        description="Placeholder element for path extensions",
        default=None,
        alias="_path",
    )
    representation: Optional[List[Code]] = Field(
        description="xmlAttr | xmlText | typeAttr | cdaText | xhtml",
        default=None,
    )
    representation_ext: Optional["Element"] = Field(
        description="Placeholder element for representation extensions",
        default=None,
        alias="_representation",
    )
    sliceName: Optional[String] = Field(
        description="Name for this particular element (in a set of slices)",
        default=None,
    )
    sliceName_ext: Optional["Element"] = Field(
        description="Placeholder element for sliceName extensions",
        default=None,
        alias="_sliceName",
    )
    sliceIsConstraining: Optional[Boolean] = Field(
        description="If this slice definition constrains an inherited slice definition (or not)",
        default=None,
    )
    sliceIsConstraining_ext: Optional["Element"] = Field(
        description="Placeholder element for sliceIsConstraining extensions",
        default=None,
        alias="_sliceIsConstraining",
    )
    label: Optional[String] = Field(
        description="Name for element to display with or prompt for element",
        default=None,
    )
    label_ext: Optional["Element"] = Field(
        description="Placeholder element for label extensions",
        default=None,
        alias="_label",
    )
    code: Optional[List["Coding"]] = Field(
        description="Corresponding codes in terminologies",
        default=None,
    )
    slicing: Optional["Element"] = Field(
        description="This element is sliced - slices follow",
        default=None,
    )
    short: Optional[String] = Field(
        description="Concise definition for space-constrained presentation",
        default=None,
    )
    short_ext: Optional["Element"] = Field(
        description="Placeholder element for short extensions",
        default=None,
        alias="_short",
    )
    definition: Optional[Markdown] = Field(
        description="Full formal definition as narrative text",
        default=None,
    )
    definition_ext: Optional["Element"] = Field(
        description="Placeholder element for definition extensions",
        default=None,
        alias="_definition",
    )
    comment: Optional[Markdown] = Field(
        description="Comments about the use of this element",
        default=None,
    )
    comment_ext: Optional["Element"] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )
    requirements: Optional[Markdown] = Field(
        description="Why this resource has been created",
        default=None,
    )
    requirements_ext: Optional["Element"] = Field(
        description="Placeholder element for requirements extensions",
        default=None,
        alias="_requirements",
    )
    alias: Optional[List[String]] = Field(
        description="Other names",
        default=None,
    )
    alias_ext: Optional["Element"] = Field(
        description="Placeholder element for alias extensions",
        default=None,
        alias="_alias",
    )
    min: Optional[UnsignedInt] = Field(
        description="Minimum Cardinality",
        default=None,
    )
    min_ext: Optional["Element"] = Field(
        description="Placeholder element for min extensions",
        default=None,
        alias="_min",
    )
    max: Optional[String] = Field(
        description="Maximum Cardinality (a number or *)",
        default=None,
    )
    max_ext: Optional["Element"] = Field(
        description="Placeholder element for max extensions",
        default=None,
        alias="_max",
    )
    base: Optional["Element"] = Field(
        description="Base definition information for tools",
        default=None,
    )
    contentReference: Optional[Uri] = Field(
        description="Reference to definition of content for the element",
        default=None,
    )
    contentReference_ext: Optional["Element"] = Field(
        description="Placeholder element for contentReference extensions",
        default=None,
        alias="_contentReference",
    )
    type: Optional[List["Element"]] = Field(
        description="Data type and Profile for this element",
        default=None,
    )
    defaultValueBase64Binary: Optional[Base64Binary] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueBoolean: Optional[Boolean] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCanonical: Optional[Canonical] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCode: Optional[Code] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDate: Optional[Date] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDateTime: Optional[DateTime] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDecimal: Optional[Decimal] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueId: Optional[Id] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueInstant: Optional[Instant] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueInteger: Optional[Integer] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMarkdown: Optional[Markdown] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueOid: Optional[Oid] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValuePositiveInt: Optional[PositiveInt] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueString: Optional[String] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTime: Optional[Time] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUri: Optional[Uri] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUrl: Optional[Url] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUuid: Optional[Uuid] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAddress: Optional["Address"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAge: Optional["Age"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAnnotation: Optional["Annotation"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAttachment: Optional["Attachment"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCodeableConcept: Optional["CodeableConcept"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCodeableReference: Optional["CodeableReference"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCoding: Optional["Coding"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContactPoint: Optional["ContactPoint"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCount: Optional["Count"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDistance: Optional["Distance"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDuration: Optional["Duration"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueHumanName: Optional["HumanName"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueIdentifier: Optional["Identifier"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMoney: Optional["Money"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValuePeriod: Optional["Period"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueQuantity: Optional["Quantity"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRange: Optional["Range"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRatio: Optional["Ratio"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRatioRange: Optional["RatioRange"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueReference: Optional["Reference"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueSampledData: Optional["SampledData"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueSignature: Optional["Signature"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTiming: Optional["Timing"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContactDetail: Optional["ContactDetail"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContributor: Optional["Contributor"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDataRequirement: Optional["DataRequirement"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueExpression: Optional["Expression"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueParameterDefinition: Optional["ParameterDefinition"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRelatedArtifact: Optional["RelatedArtifact"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTriggerDefinition: Optional["TriggerDefinition"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUsageContext: Optional["UsageContext"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDosage: Optional["Dosage"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    meaningWhenMissing: Optional[Markdown] = Field(
        description="Implicit meaning when this element is missing",
        default=None,
    )
    meaningWhenMissing_ext: Optional["Element"] = Field(
        description="Placeholder element for meaningWhenMissing extensions",
        default=None,
        alias="_meaningWhenMissing",
    )
    orderMeaning: Optional[String] = Field(
        description="What the order of the elements means",
        default=None,
    )
    orderMeaning_ext: Optional["Element"] = Field(
        description="Placeholder element for orderMeaning extensions",
        default=None,
        alias="_orderMeaning",
    )
    fixedBase64Binary: Optional[Base64Binary] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedBoolean: Optional[Boolean] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCanonical: Optional[Canonical] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCode: Optional[Code] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDate: Optional[Date] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDateTime: Optional[DateTime] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDecimal: Optional[Decimal] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedId: Optional[Id] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedInstant: Optional[Instant] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedInteger: Optional[Integer] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMarkdown: Optional[Markdown] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedOid: Optional[Oid] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedPositiveInt: Optional[PositiveInt] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedString: Optional[String] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTime: Optional[Time] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUnsignedInt: Optional[UnsignedInt] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUri: Optional[Uri] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUrl: Optional[Url] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUuid: Optional[Uuid] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAddress: Optional["Address"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAge: Optional["Age"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAnnotation: Optional["Annotation"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAttachment: Optional["Attachment"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCodeableConcept: Optional["CodeableConcept"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCodeableReference: Optional["CodeableReference"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCoding: Optional["Coding"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContactPoint: Optional["ContactPoint"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCount: Optional["Count"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDistance: Optional["Distance"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDuration: Optional["Duration"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedHumanName: Optional["HumanName"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedIdentifier: Optional["Identifier"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMoney: Optional["Money"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedPeriod: Optional["Period"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedQuantity: Optional["Quantity"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRange: Optional["Range"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRatio: Optional["Ratio"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRatioRange: Optional["RatioRange"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedReference: Optional["Reference"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedSampledData: Optional["SampledData"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedSignature: Optional["Signature"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTiming: Optional["Timing"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContactDetail: Optional["ContactDetail"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContributor: Optional["Contributor"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDataRequirement: Optional["DataRequirement"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedExpression: Optional["Expression"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedParameterDefinition: Optional["ParameterDefinition"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRelatedArtifact: Optional["RelatedArtifact"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTriggerDefinition: Optional["TriggerDefinition"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUsageContext: Optional["UsageContext"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDosage: Optional["Dosage"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    patternBase64Binary: Optional[Base64Binary] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternBoolean: Optional[Boolean] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCanonical: Optional[Canonical] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCode: Optional[Code] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDate: Optional[Date] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDateTime: Optional[DateTime] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDecimal: Optional[Decimal] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternId: Optional[Id] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternInstant: Optional[Instant] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternInteger: Optional[Integer] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMarkdown: Optional[Markdown] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternOid: Optional[Oid] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternPositiveInt: Optional[PositiveInt] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternString: Optional[String] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTime: Optional[Time] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUnsignedInt: Optional[UnsignedInt] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUri: Optional[Uri] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUrl: Optional[Url] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUuid: Optional[Uuid] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAddress: Optional["Address"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAge: Optional["Age"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAnnotation: Optional["Annotation"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAttachment: Optional["Attachment"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCodeableConcept: Optional["CodeableConcept"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCodeableReference: Optional["CodeableReference"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCoding: Optional["Coding"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContactPoint: Optional["ContactPoint"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCount: Optional["Count"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDistance: Optional["Distance"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDuration: Optional["Duration"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternHumanName: Optional["HumanName"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternIdentifier: Optional["Identifier"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMoney: Optional["Money"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternPeriod: Optional["Period"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternQuantity: Optional["Quantity"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRange: Optional["Range"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRatio: Optional["Ratio"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRatioRange: Optional["RatioRange"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternReference: Optional["Reference"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternSampledData: Optional["SampledData"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternSignature: Optional["Signature"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTiming: Optional["Timing"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContactDetail: Optional["ContactDetail"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContributor: Optional["Contributor"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDataRequirement: Optional["DataRequirement"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternExpression: Optional["Expression"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternParameterDefinition: Optional["ParameterDefinition"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRelatedArtifact: Optional["RelatedArtifact"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTriggerDefinition: Optional["TriggerDefinition"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUsageContext: Optional["UsageContext"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDosage: Optional["Dosage"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    example: Optional[List["Element"]] = Field(
        description="Example value (as defined for type)",
        default=None,
    )
    minValueDate: Optional[Date] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueDateTime: Optional[DateTime] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueInstant: Optional[Instant] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueTime: Optional[Time] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueDecimal: Optional[Decimal] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueInteger: Optional[Integer] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValuePositiveInt: Optional[PositiveInt] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueQuantity: Optional["Quantity"] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    maxValueDate: Optional[Date] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueDateTime: Optional[DateTime] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueInstant: Optional[Instant] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueTime: Optional[Time] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueDecimal: Optional[Decimal] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueInteger: Optional[Integer] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValuePositiveInt: Optional[PositiveInt] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueQuantity: Optional["Quantity"] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxLength: Optional[Integer] = Field(
        description="Max length for strings",
        default=None,
    )
    maxLength_ext: Optional["Element"] = Field(
        description="Placeholder element for maxLength extensions",
        default=None,
        alias="_maxLength",
    )
    condition: Optional[List[Id]] = Field(
        description="Reference to invariant about presence",
        default=None,
    )
    condition_ext: Optional["Element"] = Field(
        description="Placeholder element for condition extensions",
        default=None,
        alias="_condition",
    )
    constraint: Optional[List["Element"]] = Field(
        description="Condition that must evaluate to true",
        default=None,
    )
    mustSupport: Optional[Boolean] = Field(
        description="If the element must be supported",
        default=None,
    )
    mustSupport_ext: Optional["Element"] = Field(
        description="Placeholder element for mustSupport extensions",
        default=None,
        alias="_mustSupport",
    )
    isModifier: Optional[Boolean] = Field(
        description="If this modifies the meaning of other elements",
        default=None,
    )
    isModifier_ext: Optional["Element"] = Field(
        description="Placeholder element for isModifier extensions",
        default=None,
        alias="_isModifier",
    )
    isModifierReason: Optional[String] = Field(
        description="Reason that this element is marked as a modifier",
        default=None,
    )
    isModifierReason_ext: Optional["Element"] = Field(
        description="Placeholder element for isModifierReason extensions",
        default=None,
        alias="_isModifierReason",
    )
    isSummary: Optional[Boolean] = Field(
        description="Include when _summary = true?",
        default=None,
    )
    isSummary_ext: Optional["Element"] = Field(
        description="Placeholder element for isSummary extensions",
        default=None,
        alias="_isSummary",
    )
    binding: Optional["Element"] = Field(
        description="ValueSet details if this is coded",
        default=None,
    )
    mapping: Optional[List["Element"]] = Field(
        description="Map element to another set of definitions",
        default=None,
    )

    @field_validator(
        *(
            "mapping",
            "binding",
            "isSummary",
            "isModifierReason",
            "isModifier",
            "mustSupport",
            "constraint",
            "condition",
            "maxLength",
            "example",
            "orderMeaning",
            "meaningWhenMissing",
            "type",
            "contentReference",
            "base",
            "max",
            "min",
            "alias",
            "requirements",
            "comment",
            "definition",
            "short",
            "slicing",
            "code",
            "label",
            "sliceIsConstraining",
            "sliceName",
            "representation",
            "path",
            "modifierExtension",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
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

    @field_validator(*("slicing",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="discriminator.exists() or description.exists()",
            human="If there are no discriminators, there must be a definition",
            key="eld-1",
            severity="error",
        )

    @field_validator(*("max",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_3_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="empty() or ($this = '*') or (toInteger() >= 0)",
            human='Max SHALL be a number or "*"',
            key="eld-3",
            severity="error",
        )

    @field_validator(*("type",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_4_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="aggregation.empty() or (code = 'Reference') or (code = 'canonical')",
            human="Aggregation may only be specified if one of the allowed types for the element is a reference",
            key="eld-4",
            severity="error",
        )

    @field_validator(*("type",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_17_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="(code='Reference' or code = 'canonical' or code = 'CodeableReference') or targetProfile.empty()",
            human="targetProfile is only allowed if the type is Reference or canonical",
            key="eld-17",
            severity="error",
        )

    @field_validator(*("constraint",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_21_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="expression.exists()",
            human="Constraints should have an expression or else validators will not be able to enforce them",
            key="eld-21",
            severity="warning",
        )

    @field_validator(*("binding",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_12_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="valueSet.exists() implies (valueSet.startsWith('http:') or valueSet.startsWith('https') or valueSet.startsWith('urn:') or valueSet.startsWith('#'))",
            human="ValueSet SHALL start with http:// or https:// or urn:",
            key="eld-12",
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

    @model_validator(mode="after")
    def defaultValue_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Base64Binary,
                Boolean,
                Canonical,
                Code,
                Date,
                DateTime,
                Decimal,
                Id,
                Instant,
                Integer,
                Markdown,
                Oid,
                PositiveInt,
                String,
                Time,
                UnsignedInt,
                Uri,
                Url,
                Uuid,
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
                "CodeableReference",
                "Coding",
                "ContactPoint",
                "Count",
                "Distance",
                "Duration",
                "HumanName",
                "Identifier",
                "Money",
                "Period",
                "Quantity",
                "Range",
                "Ratio",
                "RatioRange",
                "Reference",
                "SampledData",
                "Signature",
                "Timing",
                "ContactDetail",
                "Contributor",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Dosage",
            ],
            field_name_base="defaultValue",
        )

    @model_validator(mode="after")
    def fixed_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Base64Binary,
                Boolean,
                Canonical,
                Code,
                Date,
                DateTime,
                Decimal,
                Id,
                Instant,
                Integer,
                Markdown,
                Oid,
                PositiveInt,
                String,
                Time,
                UnsignedInt,
                Uri,
                Url,
                Uuid,
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
                "CodeableReference",
                "Coding",
                "ContactPoint",
                "Count",
                "Distance",
                "Duration",
                "HumanName",
                "Identifier",
                "Money",
                "Period",
                "Quantity",
                "Range",
                "Ratio",
                "RatioRange",
                "Reference",
                "SampledData",
                "Signature",
                "Timing",
                "ContactDetail",
                "Contributor",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Dosage",
            ],
            field_name_base="fixed",
        )

    @model_validator(mode="after")
    def pattern_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Base64Binary,
                Boolean,
                Canonical,
                Code,
                Date,
                DateTime,
                Decimal,
                Id,
                Instant,
                Integer,
                Markdown,
                Oid,
                PositiveInt,
                String,
                Time,
                UnsignedInt,
                Uri,
                Url,
                Uuid,
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
                "CodeableReference",
                "Coding",
                "ContactPoint",
                "Count",
                "Distance",
                "Duration",
                "HumanName",
                "Identifier",
                "Money",
                "Period",
                "Quantity",
                "Range",
                "Ratio",
                "RatioRange",
                "Reference",
                "SampledData",
                "Signature",
                "Timing",
                "ContactDetail",
                "Contributor",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Dosage",
            ],
            field_name_base="pattern",
        )

    @model_validator(mode="after")
    def minValue_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Date,
                DateTime,
                Instant,
                Time,
                Decimal,
                Integer,
                PositiveInt,
                UnsignedInt,
                "Quantity",
            ],
            field_name_base="minValue",
        )

    @model_validator(mode="after")
    def maxValue_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Date,
                DateTime,
                Instant,
                Time,
                Decimal,
                Integer,
                PositiveInt,
                UnsignedInt,
                "Quantity",
            ],
            field_name_base="maxValue",
        )

    @model_validator(mode="after")
    def FHIR_eld_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="min.empty() or max.empty() or (max = '*') or iif(max != '*', min <= max.toInteger())",
            human="Min <= Max",
            key="eld-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_5_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contentReference.empty() or (type.empty() and defaultValue.empty() and fixed.empty() and pattern.empty() and example.empty() and minValue.empty() and maxValue.empty() and maxLength.empty() and binding.empty())",
            human="if the element definition has a contentReference, it cannot have type, defaultValue, fixed, pattern, example, minValue, maxValue, maxLength, or binding",
            key="eld-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_6_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="fixed.empty() or (type.count()  <= 1)",
            human="Fixed value may only be specified if there is one type",
            key="eld-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_7_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="pattern.empty() or (type.count() <= 1)",
            human="Pattern may only be specified if there is one type",
            key="eld-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_8_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="pattern.empty() or fixed.empty()",
            human="Pattern and fixed are mutually exclusive",
            key="eld-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_11_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="binding.empty() or type.code.empty() or type.select((code = 'code') or (code = 'Coding') or (code='CodeableConcept') or (code = 'Quantity') or (code = 'string') or (code = 'uri') or (code = 'Duration')).exists()",
            human="Binding can only be present for coded elements, string, and uri",
            key="eld-11",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_13_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type.select(code).isDistinct()",
            human="Types must be unique by code",
            key="eld-13",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_14_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="constraint.select(key).isDistinct()",
            human="Constraints must be unique by key",
            key="eld-14",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_15_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="defaultValue.empty() or meaningWhenMissing.empty()",
            human="default value and meaningWhenMissing are mutually exclusive",
            key="eld-15",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_16_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="sliceName.empty() or sliceName.matches('^[a-zA-Z0-9\\/\\-_\\[\\]\\@]+$')",
            human='sliceName must be composed of proper tokens separated by"/"',
            key="eld-16",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_18_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(isModifier.exists() and isModifier) implies isModifierReason.exists()",
            human="Must have a modifier reason if isModifier = true",
            key="eld-18",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_19_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="path.matches('^[^\\s\\.,:;\\'\"\\/|?!@#$%&*()\\[\\]{}]{1,64}(\\.[^\\s\\.,:;\\'\"\\/|?!@#$%&*()\\[\\]{}]{1,64}(\\[x\\])?(\\:[^\\s\\.]+)?)*$')",
            human="Element names cannot include some special characters",
            key="eld-19",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_20_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="path.matches('^[A-Za-z][A-Za-z0-9]*(\\.[a-z][A-Za-z0-9]*(\\[x])?)*$')",
            human="Element names should be simple alphanumerics with a max of 64 characters, or code generation tools may be broken",
            key="eld-20",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_eld_22_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="sliceIsConstraining.exists() implies sliceName.exists()",
            human="sliceIsConstraining can only appear if slicename is present",
            key="eld-22",
            severity="error",
        )

    @property
    def defaultValue(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="defaultValue",
        )

    @property
    def fixed(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="fixed",
        )

    @property
    def pattern(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="pattern",
        )

    @property
    def minValue(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="minValue",
        )

    @property
    def maxValue(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="maxValue",
        )


class Expression(Element):
    """
    An expression that can be used to generate a value
    """

    description: Optional[String] = Field(
        description="Natural language description of the condition",
        default=None,
    )
    description_ext: Optional["Element"] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    name: Optional[Id] = Field(
        description="Short name assigned to expression for reuse",
        default=None,
    )
    name_ext: Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    language: Optional[Code] = Field(
        description="text/cql | text/fhirpath | application/x-fhir-query | text/cql-identifier | text/cql-expression | etc.",
        default=None,
    )
    language_ext: Optional["Element"] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    expression: Optional[String] = Field(
        description="Expression in specified language",
        default=None,
    )
    expression_ext: Optional["Element"] = Field(
        description="Placeholder element for expression extensions",
        default=None,
        alias="_expression",
    )
    reference: Optional[Uri] = Field(
        description="Where the expression is found",
        default=None,
    )
    reference_ext: Optional["Element"] = Field(
        description="Placeholder element for reference extensions",
        default=None,
        alias="_reference",
    )

    @field_validator(
        *(
            "reference",
            "expression",
            "language",
            "name",
            "description",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exp_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="expression.exists() or reference.exists()",
            human="An expression or a reference must be provided",
            key="exp-1",
            severity="error",
        )


class Extension(Element):
    """
    Optional Extensions Element
    """

    url: Optional[String] = Field(
        description="identifies the meaning of the extension",
        default=None,
    )
    url_ext: Optional["Element"] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    valueBase64Binary: Optional[Base64Binary] = Field(
        description="Value of extension",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="Value of extension",
        default=None,
    )
    valueCanonical: Optional[Canonical] = Field(
        description="Value of extension",
        default=None,
    )
    valueCode: Optional[Code] = Field(
        description="Value of extension",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="Value of extension",
        default=None,
    )
    valueDateTime: Optional[DateTime] = Field(
        description="Value of extension",
        default=None,
    )
    valueDecimal: Optional[Decimal] = Field(
        description="Value of extension",
        default=None,
    )
    valueId: Optional[Id] = Field(
        description="Value of extension",
        default=None,
    )
    valueInstant: Optional[Instant] = Field(
        description="Value of extension",
        default=None,
    )
    valueInteger: Optional[Integer] = Field(
        description="Value of extension",
        default=None,
    )
    valueMarkdown: Optional[Markdown] = Field(
        description="Value of extension",
        default=None,
    )
    valueOid: Optional[Oid] = Field(
        description="Value of extension",
        default=None,
    )
    valuePositiveInt: Optional[PositiveInt] = Field(
        description="Value of extension",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="Value of extension",
        default=None,
    )
    valueTime: Optional[Time] = Field(
        description="Value of extension",
        default=None,
    )
    valueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Value of extension",
        default=None,
    )
    valueUri: Optional[Uri] = Field(
        description="Value of extension",
        default=None,
    )
    valueUrl: Optional[Url] = Field(
        description="Value of extension",
        default=None,
    )
    valueUuid: Optional[Uuid] = Field(
        description="Value of extension",
        default=None,
    )
    valueAddress: Optional["Address"] = Field(
        description="Value of extension",
        default=None,
    )
    valueAge: Optional["Age"] = Field(
        description="Value of extension",
        default=None,
    )
    valueAnnotation: Optional["Annotation"] = Field(
        description="Value of extension",
        default=None,
    )
    valueAttachment: Optional["Attachment"] = Field(
        description="Value of extension",
        default=None,
    )
    valueCodeableConcept: Optional["CodeableConcept"] = Field(
        description="Value of extension",
        default=None,
    )
    valueCodeableReference: Optional["CodeableReference"] = Field(
        description="Value of extension",
        default=None,
    )
    valueCoding: Optional["Coding"] = Field(
        description="Value of extension",
        default=None,
    )
    valueContactPoint: Optional["ContactPoint"] = Field(
        description="Value of extension",
        default=None,
    )
    valueCount: Optional["Count"] = Field(
        description="Value of extension",
        default=None,
    )
    valueDistance: Optional["Distance"] = Field(
        description="Value of extension",
        default=None,
    )
    valueDuration: Optional["Duration"] = Field(
        description="Value of extension",
        default=None,
    )
    valueHumanName: Optional["HumanName"] = Field(
        description="Value of extension",
        default=None,
    )
    valueIdentifier: Optional["Identifier"] = Field(
        description="Value of extension",
        default=None,
    )
    valueMoney: Optional["Money"] = Field(
        description="Value of extension",
        default=None,
    )
    valuePeriod: Optional["Period"] = Field(
        description="Value of extension",
        default=None,
    )
    valueQuantity: Optional["Quantity"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRange: Optional["Range"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRatio: Optional["Ratio"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRatioRange: Optional["RatioRange"] = Field(
        description="Value of extension",
        default=None,
    )
    valueReference: Optional["Reference"] = Field(
        description="Value of extension",
        default=None,
    )
    valueSampledData: Optional["SampledData"] = Field(
        description="Value of extension",
        default=None,
    )
    valueSignature: Optional["Signature"] = Field(
        description="Value of extension",
        default=None,
    )
    valueTiming: Optional["Timing"] = Field(
        description="Value of extension",
        default=None,
    )
    valueContactDetail: Optional["ContactDetail"] = Field(
        description="Value of extension",
        default=None,
    )
    valueContributor: Optional["Contributor"] = Field(
        description="Value of extension",
        default=None,
    )
    valueDataRequirement: Optional["DataRequirement"] = Field(
        description="Value of extension",
        default=None,
    )
    valueExpression: Optional["Expression"] = Field(
        description="Value of extension",
        default=None,
    )
    valueParameterDefinition: Optional["ParameterDefinition"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRelatedArtifact: Optional["RelatedArtifact"] = Field(
        description="Value of extension",
        default=None,
    )
    valueTriggerDefinition: Optional["TriggerDefinition"] = Field(
        description="Value of extension",
        default=None,
    )
    valueUsageContext: Optional["UsageContext"] = Field(
        description="Value of extension",
        default=None,
    )
    valueDosage: Optional["Dosage"] = Field(
        description="Value of extension",
        default=None,
    )

    @field_validator(*("extension",), mode="after", check_fields=None)
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Base64Binary,
                Boolean,
                Canonical,
                Code,
                Date,
                DateTime,
                Decimal,
                Id,
                Instant,
                Integer,
                Markdown,
                Oid,
                PositiveInt,
                String,
                Time,
                UnsignedInt,
                Uri,
                Url,
                Uuid,
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
                "CodeableReference",
                "Coding",
                "ContactPoint",
                "Count",
                "Distance",
                "Duration",
                "HumanName",
                "Identifier",
                "Money",
                "Period",
                "Quantity",
                "Range",
                "Ratio",
                "RatioRange",
                "Reference",
                "SampledData",
                "Signature",
                "Timing",
                "ContactDetail",
                "Contributor",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Dosage",
            ],
            field_name_base="value",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )


class HumanName(Element):
    """
    Name of a human - parts and usage
    """

    use: Optional[Code] = Field(
        description="usual | official | temp | nickname | anonymous | old | maiden",
        default=None,
    )
    use_ext: Optional["Element"] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    text: Optional[String] = Field(
        description="Text representation of the full name",
        default=None,
    )
    text_ext: Optional["Element"] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
    family: Optional[String] = Field(
        description="Family name (often called \u0027Surname\u0027)",
        default=None,
    )
    family_ext: Optional["Element"] = Field(
        description="Placeholder element for family extensions",
        default=None,
        alias="_family",
    )
    given: Optional[List[String]] = Field(
        description="Given names (not always \u0027first\u0027). Includes middle names",
        default=None,
    )
    given_ext: Optional["Element"] = Field(
        description="Placeholder element for given extensions",
        default=None,
        alias="_given",
    )
    prefix: Optional[List[String]] = Field(
        description="Parts that come before the name",
        default=None,
    )
    prefix_ext: Optional["Element"] = Field(
        description="Placeholder element for prefix extensions",
        default=None,
        alias="_prefix",
    )
    suffix: Optional[List[String]] = Field(
        description="Parts that come after the name",
        default=None,
    )
    suffix_ext: Optional["Element"] = Field(
        description="Placeholder element for suffix extensions",
        default=None,
        alias="_suffix",
    )
    period: Optional["Period"] = Field(
        description="Time period when name was/is in use",
        default=None,
    )

    @field_validator(
        *(
            "period",
            "suffix",
            "prefix",
            "given",
            "family",
            "text",
            "use",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class Identifier(Element):
    """
    An identifier intended for computation
    """

    use: Optional[Code] = Field(
        description="usual | official | temp | secondary | old (If known)",
        default=None,
    )
    use_ext: Optional["Element"] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    type: Optional["CodeableConcept"] = Field(
        description="Description of identifier",
        default=None,
    )
    system: Optional[Uri] = Field(
        description="The namespace for the identifier value",
        default=None,
    )
    system_ext: Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    value: Optional[String] = Field(
        description="The value that is unique",
        default=None,
    )
    value_ext: Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    period: Optional["Period"] = Field(
        description="Time period when id is/was valid for use",
        default=None,
    )
    assigner: Optional["Reference"] = Field(
        description="Organization that issued id (may be just text)",
        default=None,
    )

    @field_validator(
        *(
            "assigner",
            "period",
            "value",
            "system",
            "type",
            "use",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class MarketingStatus(BackboneElement):
    """
    The marketing status describes the date when a medicinal product is actually put on the market or the date as of which it is no longer available
    """

    country: Optional["CodeableConcept"] = Field(
        description="The country in which the marketing authorisation has been granted shall be specified It should be specified using the ISO 3166 \u2011 1 alpha-2 code elements",
        default=None,
    )
    jurisdiction: Optional["CodeableConcept"] = Field(
        description="Where a Medicines Regulatory Agency has granted a marketing authorisation for which specific provisions within a jurisdiction apply, the jurisdiction can be specified using an appropriate controlled terminology The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
    status: Optional["CodeableConcept"] = Field(
        description="This attribute provides information on the status of the marketing of the medicinal product See ISO/TS 20443 for more information and examples",
        default=None,
    )
    dateRange: Optional["Period"] = Field(
        description="The date when the Medicinal Product is placed on the market by the Marketing Authorisation Holder (or where applicable, the manufacturer/distributor) in a country and/or jurisdiction shall be provided A complete date consisting of day, month and year shall be specified using the ISO 8601 date format NOTE \u201cPlaced on the market\u201d refers to the release of the Medicinal Product into the distribution chain",
        default=None,
    )
    restoreDate: Optional[DateTime] = Field(
        description="The date when the Medicinal Product is placed on the market by the Marketing Authorisation Holder (or where applicable, the manufacturer/distributor) in a country and/or jurisdiction shall be provided A complete date consisting of day, month and year shall be specified using the ISO 8601 date format NOTE \u201cPlaced on the market\u201d refers to the release of the Medicinal Product into the distribution chain",
        default=None,
    )
    restoreDate_ext: Optional["Element"] = Field(
        description="Placeholder element for restoreDate extensions",
        default=None,
        alias="_restoreDate",
    )

    @field_validator(
        *(
            "restoreDate",
            "dateRange",
            "status",
            "jurisdiction",
            "country",
            "modifierExtension",
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

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
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


class Meta(Element):
    """
    Metadata about a resource
    """

    versionId: Optional[Id] = Field(
        description="Version specific identifier",
        default=None,
    )
    versionId_ext: Optional["Element"] = Field(
        description="Placeholder element for versionId extensions",
        default=None,
        alias="_versionId",
    )
    lastUpdated: Optional[Instant] = Field(
        description="When the resource version last changed",
        default=None,
    )
    lastUpdated_ext: Optional["Element"] = Field(
        description="Placeholder element for lastUpdated extensions",
        default=None,
        alias="_lastUpdated",
    )
    source: Optional[Uri] = Field(
        description="Identifies where the resource comes from",
        default=None,
    )
    source_ext: Optional["Element"] = Field(
        description="Placeholder element for source extensions",
        default=None,
        alias="_source",
    )
    profile: Optional[List[Canonical]] = Field(
        description="Profiles this resource claims to conform to",
        default=None,
    )
    profile_ext: Optional["Element"] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )
    security: Optional[List["Coding"]] = Field(
        description="Security Labels applied to this resource",
        default=None,
    )
    tag: Optional[List["Coding"]] = Field(
        description="Tags applied to this resource",
        default=None,
    )

    @field_validator(
        *(
            "tag",
            "security",
            "profile",
            "source",
            "lastUpdated",
            "versionId",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class Money(Element):
    """
    An amount of economic utility in some recognized currency
    """

    value: Optional[Decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    value_ext: Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    currency: Optional[Code] = Field(
        description="ISO 4217 Currency Code",
        default=None,
    )
    currency_ext: Optional["Element"] = Field(
        description="Placeholder element for currency extensions",
        default=None,
        alias="_currency",
    )

    @field_validator(
        *("currency", "value", "extension", "extension"),
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class Narrative(Element):
    """
    Human-readable summary of the resource (essential clinical and business information)
    """

    status: Optional[Code] = Field(
        description="generated | extensions | additional | empty",
        default=None,
    )
    status_ext: Optional["Element"] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    div: Optional[str] = Field(
        description="Limited xhtml content",
        default=None,
    )

    @field_validator(
        *("div", "status", "extension", "extension"), mode="after", check_fields=None
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

    @field_validator(*("div",), mode="after", check_fields=None)
    @classmethod
    def FHIR_txt_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="htmlChecks()",
            human="The narrative SHALL contain only the basic html formatting elements and attributes described in chapters 7-11 (except section 4 of chapter 9) and 15 of the HTML 4.0 standard, <a> elements (either name or href), images and internally contained style attributes",
            key="txt-1",
            severity="error",
        )

    @field_validator(*("div",), mode="after", check_fields=None)
    @classmethod
    def FHIR_txt_2_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="htmlChecks()",
            human="The narrative SHALL have some non-whitespace content",
            key="txt-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class ParameterDefinition(Element):
    """
    Definition of a parameter to a module
    """

    name: Optional[Code] = Field(
        description="Name used to access the parameter value",
        default=None,
    )
    name_ext: Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    use: Optional[Code] = Field(
        description="in | out",
        default=None,
    )
    use_ext: Optional["Element"] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    min: Optional[Integer] = Field(
        description="Minimum cardinality",
        default=None,
    )
    min_ext: Optional["Element"] = Field(
        description="Placeholder element for min extensions",
        default=None,
        alias="_min",
    )
    max: Optional[String] = Field(
        description="Maximum cardinality (a number of *)",
        default=None,
    )
    max_ext: Optional["Element"] = Field(
        description="Placeholder element for max extensions",
        default=None,
        alias="_max",
    )
    documentation: Optional[String] = Field(
        description="A brief description of the parameter",
        default=None,
    )
    documentation_ext: Optional["Element"] = Field(
        description="Placeholder element for documentation extensions",
        default=None,
        alias="_documentation",
    )
    type: Optional[Code] = Field(
        description="What type of value",
        default=None,
    )
    type_ext: Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    profile: Optional[Canonical] = Field(
        description="What profile the value is expected to be",
        default=None,
    )
    profile_ext: Optional["Element"] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )

    @field_validator(
        *(
            "profile",
            "type",
            "documentation",
            "max",
            "min",
            "use",
            "name",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class Period(Element):
    """
    Time range defined by start and end date/time
    """

    start: Optional[DateTime] = Field(
        description="Starting time with inclusive boundary",
        default=None,
    )
    start_ext: Optional["Element"] = Field(
        description="Placeholder element for start extensions",
        default=None,
        alias="_start",
    )
    end: Optional[DateTime] = Field(
        description="End time with inclusive boundary, if not ongoing",
        default=None,
    )
    end_ext: Optional["Element"] = Field(
        description="Placeholder element for end extensions",
        default=None,
        alias="_end",
    )

    @field_validator(
        *("end", "start", "extension", "extension"), mode="after", check_fields=None
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_per_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="start.hasValue().not() or end.hasValue().not() or (start <= end)",
            human="If present, start SHALL have a lower value than end",
            key="per-1",
            severity="error",
        )


class Population(BackboneElement):
    """
    A definition of a set of people that apply to some clinically related context, for example people contraindicated for a certain medication
    """

    ageRange: Optional["Range"] = Field(
        description="The age of the specific population",
        default=None,
    )
    ageCodeableConcept: Optional["CodeableConcept"] = Field(
        description="The age of the specific population",
        default=None,
    )
    gender: Optional["CodeableConcept"] = Field(
        description="The gender of the specific population",
        default=None,
    )
    race: Optional["CodeableConcept"] = Field(
        description="Race of the specific population",
        default=None,
    )
    physiologicalCondition: Optional["CodeableConcept"] = Field(
        description="The existing physiological conditions of the specific population to which this applies",
        default=None,
    )

    @field_validator(
        *(
            "physiologicalCondition",
            "race",
            "gender",
            "modifierExtension",
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

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
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

    @model_validator(mode="after")
    def age_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Range", "CodeableConcept"],
            field_name_base="age",
        )

    @property
    def age(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="age",
        )


class ProdCharacteristic(BackboneElement):
    """
    The marketing status describes the date when a medicinal product is actually put on the market or the date as of which it is no longer available
    """

    height: Optional["Quantity"] = Field(
        description="Where applicable, the height can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    width: Optional["Quantity"] = Field(
        description="Where applicable, the width can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    depth: Optional["Quantity"] = Field(
        description="Where applicable, the depth can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    weight: Optional["Quantity"] = Field(
        description="Where applicable, the weight can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    nominalVolume: Optional["Quantity"] = Field(
        description="Where applicable, the nominal volume can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    externalDiameter: Optional["Quantity"] = Field(
        description="Where applicable, the external diameter can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    shape: Optional[String] = Field(
        description="Where applicable, the shape can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used",
        default=None,
    )
    shape_ext: Optional["Element"] = Field(
        description="Placeholder element for shape extensions",
        default=None,
        alias="_shape",
    )
    color: Optional[List[String]] = Field(
        description="Where applicable, the color can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used",
        default=None,
    )
    color_ext: Optional["Element"] = Field(
        description="Placeholder element for color extensions",
        default=None,
        alias="_color",
    )
    imprint: Optional[List[String]] = Field(
        description="Where applicable, the imprint can be specified as text",
        default=None,
    )
    imprint_ext: Optional["Element"] = Field(
        description="Placeholder element for imprint extensions",
        default=None,
        alias="_imprint",
    )
    image: Optional[List["Attachment"]] = Field(
        description="Where applicable, the image can be provided The format of the image attachment shall be specified by regional implementations",
        default=None,
    )
    scoring: Optional["CodeableConcept"] = Field(
        description="Where applicable, the scoring can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used",
        default=None,
    )

    @field_validator(
        *(
            "scoring",
            "image",
            "imprint",
            "color",
            "shape",
            "externalDiameter",
            "nominalVolume",
            "weight",
            "depth",
            "width",
            "height",
            "modifierExtension",
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

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
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


class ProductShelfLife(BackboneElement):
    """
    The shelf-life and storage information for a medicinal product item or container can be described using this class
    """

    identifier: Optional["Identifier"] = Field(
        description="Unique identifier for the packaged Medicinal Product",
        default=None,
    )
    type: Optional["CodeableConcept"] = Field(
        description="This describes the shelf life, taking into account various scenarios such as shelf life of the packaged Medicinal Product itself, shelf life after transformation where necessary and shelf life after the first opening of a bottle, etc. The shelf life type shall be specified using an appropriate controlled vocabulary The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
    period: Optional["Quantity"] = Field(
        description="The shelf life time period can be specified using a numerical value for the period of time and its unit of time measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    specialPrecautionsForStorage: Optional[List["CodeableConcept"]] = (
        Field(
            description="Special precautions for storage, if any, can be specified using an appropriate controlled vocabulary The controlled term and the controlled term identifier shall be specified",
            default=None,
        )
    )

    @field_validator(
        *(
            "specialPrecautionsForStorage",
            "period",
            "type",
            "identifier",
            "modifierExtension",
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

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
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


class Quantity(Element):
    """
    A measured or measurable amount
    """

    value: Optional[Decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    value_ext: Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    comparator: Optional[Code] = Field(
        description="\u003c | \u003c= | \u003e= | \u003e - how to understand the value",
        default=None,
    )
    comparator_ext: Optional["Element"] = Field(
        description="Placeholder element for comparator extensions",
        default=None,
        alias="_comparator",
    )
    unit: Optional[String] = Field(
        description="Unit representation",
        default=None,
    )
    unit_ext: Optional["Element"] = Field(
        description="Placeholder element for unit extensions",
        default=None,
        alias="_unit",
    )
    system: Optional[Uri] = Field(
        description="System that defines coded unit form",
        default=None,
    )
    system_ext: Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    code: Optional[Code] = Field(
        description="Coded form of the unit",
        default=None,
    )
    code_ext: Optional["Element"] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )

    @field_validator(
        *(
            "code",
            "system",
            "unit",
            "comparator",
            "value",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_qty_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="code.empty() or system.exists()",
            human="If a code for the unit is present, the system SHALL also be present",
            key="qty-3",
            severity="error",
        )


class Count(Quantity):
    """
    A measured or measurable amount
    """

    @field_validator(
        *("code", "system", "unit", "comparator", "value", "extension"),
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
    def FHIR_cnt_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(code.exists() or value.empty()) and (system.empty() or system = %ucum) and (code.empty() or code = '1') and (value.empty() or value.hasValue().not() or value.toString().contains('.').not())",
            human='There SHALL be a code with a value of "1" if there is a value. If system is present, it SHALL be UCUM.  If present, the value SHALL be a whole number.',
            key="cnt-3",
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

    @model_validator(mode="after")
    def FHIR_qty_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="code.empty() or system.exists()",
            human="If a code for the unit is present, the system SHALL also be present",
            key="qty-3",
            severity="error",
        )


class Age(Quantity):
    """
    A duration of time during which an organism (or a process) has existed
    """

    @field_validator(
        *("code", "system", "unit", "comparator", "value", "extension"),
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
    def FHIR_age_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(code.exists() or value.empty()) and (system.empty() or system = %ucum) and (value.empty() or value.hasValue().not() or value > 0)",
            human="There SHALL be a code if there is a value and it SHALL be an expression of time.  If system is present, it SHALL be UCUM.  If value is present, it SHALL be positive.",
            key="age-1",
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

    @model_validator(mode="after")
    def FHIR_qty_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="code.empty() or system.exists()",
            human="If a code for the unit is present, the system SHALL also be present",
            key="qty-3",
            severity="error",
        )


class Distance(Quantity):
    """
    A length - a value with a unit that is a physical distance
    """

    @field_validator(
        *("code", "system", "unit", "comparator", "value", "extension"),
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
    def FHIR_dis_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(code.exists() or value.empty()) and (system.empty() or system = %ucum)",
            human="There SHALL be a code if there is a value and it SHALL be an expression of length.  If system is present, it SHALL be UCUM.",
            key="dis-1",
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

    @model_validator(mode="after")
    def FHIR_qty_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="code.empty() or system.exists()",
            human="If a code for the unit is present, the system SHALL also be present",
            key="qty-3",
            severity="error",
        )


class Duration(Quantity):
    """
    A length of time
    """

    @field_validator(
        *("code", "system", "unit", "comparator", "value", "extension"),
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
    def FHIR_drt_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="value.exists() implies ((system = %ucum) and code.exists())",
            human="There SHALL be a code if there is a value and it SHALL be an expression of time.  If system is present, it SHALL be UCUM.",
            key="drt-1",
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

    @model_validator(mode="after")
    def FHIR_qty_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="code.empty() or system.exists()",
            human="If a code for the unit is present, the system SHALL also be present",
            key="qty-3",
            severity="error",
        )


class Range(Element):
    """
    Set of values bounded by low and high
    """

    low: Optional["Quantity"] = Field(
        description="Low limit",
        default=None,
    )
    high: Optional["Quantity"] = Field(
        description="High limit",
        default=None,
    )

    @field_validator(
        *("high", "low", "extension", "extension"), mode="after", check_fields=None
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_rng_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="low.empty() or high.empty() or (low <= high)",
            human="If present, low SHALL have a lower value than high",
            key="rng-2",
            severity="error",
        )


class Ratio(Element):
    """
    A ratio of two Quantity values - a numerator and a denominator
    """

    numerator: Optional["Quantity"] = Field(
        description="Numerator value",
        default=None,
    )
    denominator: Optional["Quantity"] = Field(
        description="Denominator value",
        default=None,
    )

    @field_validator(
        *("denominator", "numerator", "extension", "extension"),
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_rat_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(numerator.exists() and denominator.exists()) or (numerator.empty() and denominator.empty() and extension.exists())",
            human="Numerator and denominator SHALL both be present, or both are absent. If both are absent, there SHALL be some extension present",
            key="rat-1",
            severity="error",
        )


class RatioRange(Element):
    """
    Range of ratio values
    """

    lowNumerator: Optional["Quantity"] = Field(
        description="Low Numerator limit",
        default=None,
    )
    highNumerator: Optional["Quantity"] = Field(
        description="High Numerator limit",
        default=None,
    )
    denominator: Optional["Quantity"] = Field(
        description="Denominator value",
        default=None,
    )

    @field_validator(
        *(
            "denominator",
            "highNumerator",
            "lowNumerator",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_inv_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="((lowNumerator.exists() or highNumerator.exists()) and denominator.exists()) or (lowNumerator.empty() and highNumerator.empty() and denominator.empty() and extension.exists())",
            human="One of lowNumerator or highNumerator and denominator SHALL be present, or all are absent. If all are absent, there SHALL be some extension present",
            key="inv-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_inv_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="lowNumerator.empty() or highNumerator.empty() or (lowNumerator <= highNumerator)",
            human="If present, lowNumerator SHALL have a lower value than highNumerator",
            key="inv-2",
            severity="error",
        )


class Reference(Element):
    """
    A reference from one resource to another
    """

    reference: Optional[String] = Field(
        description="Literal reference, Relative, internal or absolute URL",
        default=None,
    )
    reference_ext: Optional["Element"] = Field(
        description="Placeholder element for reference extensions",
        default=None,
        alias="_reference",
    )
    type: Optional[Uri] = Field(
        description='Type the reference refers to (e.g. "Patient")',
        default=None,
    )
    type_ext: Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    identifier: Optional["Identifier"] = Field(
        description="Logical reference, when literal reference is not known",
        default=None,
    )
    display: Optional[String] = Field(
        description="Text alternative for the resource",
        default=None,
    )
    display_ext: Optional["Element"] = Field(
        description="Placeholder element for display extensions",
        default=None,
        alias="_display",
    )

    @field_validator(
        *(
            "display",
            "identifier",
            "type",
            "reference",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ref_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="reference.startsWith('#').not() or (reference.substring(1).trace('url') in %rootResource.contained.id.trace('ids')) or (reference='#' and %rootResource!=%resource)",
            human="SHALL have a contained resource if a local reference is provided",
            key="ref-1",
            severity="error",
        )


class RelatedArtifact(Element):
    """
    Related artifacts for a knowledge resource
    """

    type: Optional[Code] = Field(
        description="documentation | justification | citation | predecessor | successor | derived-from | depends-on | composed-of",
        default=None,
    )
    type_ext: Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    label: Optional[String] = Field(
        description="Short label",
        default=None,
    )
    label_ext: Optional["Element"] = Field(
        description="Placeholder element for label extensions",
        default=None,
        alias="_label",
    )
    display: Optional[String] = Field(
        description="Brief description of the related artifact",
        default=None,
    )
    display_ext: Optional["Element"] = Field(
        description="Placeholder element for display extensions",
        default=None,
        alias="_display",
    )
    citation: Optional[Markdown] = Field(
        description="Bibliographic citation for the artifact",
        default=None,
    )
    citation_ext: Optional["Element"] = Field(
        description="Placeholder element for citation extensions",
        default=None,
        alias="_citation",
    )
    url: Optional[Url] = Field(
        description="Where the artifact can be accessed",
        default=None,
    )
    url_ext: Optional["Element"] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    document: Optional["Attachment"] = Field(
        description="What document is being referenced",
        default=None,
    )
    resource: Optional[Canonical] = Field(
        description="What resource is being referenced",
        default=None,
    )
    resource_ext: Optional["Element"] = Field(
        description="Placeholder element for resource extensions",
        default=None,
        alias="_resource",
    )

    @field_validator(
        *(
            "resource",
            "document",
            "url",
            "citation",
            "display",
            "label",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class SampledData(Element):
    """
    A series of measurements taken by a device
    """

    origin: Optional["Quantity"] = Field(
        description="Zero value and units",
        default=None,
    )
    period: Optional[Decimal] = Field(
        description="Number of milliseconds between samples",
        default=None,
    )
    period_ext: Optional["Element"] = Field(
        description="Placeholder element for period extensions",
        default=None,
        alias="_period",
    )
    factor: Optional[Decimal] = Field(
        description="Multiply data by this before adding to origin",
        default=None,
    )
    factor_ext: Optional["Element"] = Field(
        description="Placeholder element for factor extensions",
        default=None,
        alias="_factor",
    )
    lowerLimit: Optional[Decimal] = Field(
        description="Lower limit of detection",
        default=None,
    )
    lowerLimit_ext: Optional["Element"] = Field(
        description="Placeholder element for lowerLimit extensions",
        default=None,
        alias="_lowerLimit",
    )
    upperLimit: Optional[Decimal] = Field(
        description="Upper limit of detection",
        default=None,
    )
    upperLimit_ext: Optional["Element"] = Field(
        description="Placeholder element for upperLimit extensions",
        default=None,
        alias="_upperLimit",
    )
    dimensions: Optional[PositiveInt] = Field(
        description="Number of sample points at each time point",
        default=None,
    )
    dimensions_ext: Optional["Element"] = Field(
        description="Placeholder element for dimensions extensions",
        default=None,
        alias="_dimensions",
    )
    data: Optional[String] = Field(
        description='Decimal values with spaces, or "E" | "U" | "L"',
        default=None,
    )
    data_ext: Optional["Element"] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )

    @field_validator(
        *(
            "data",
            "dimensions",
            "upperLimit",
            "lowerLimit",
            "factor",
            "period",
            "origin",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class Signature(Element):
    """
    A Signature - XML DigSig, JWS, Graphical image of signature, etc.
    """

    type: Optional[List["Coding"]] = Field(
        description="Indication of the reason the entity signed the object(s)",
        default=None,
    )
    when: Optional[Instant] = Field(
        description="When the signature was created",
        default=None,
    )
    when_ext: Optional["Element"] = Field(
        description="Placeholder element for when extensions",
        default=None,
        alias="_when",
    )
    who: Optional["Reference"] = Field(
        description="Who signed",
        default=None,
    )
    onBehalfOf: Optional["Reference"] = Field(
        description="The party represented",
        default=None,
    )
    targetFormat: Optional[Code] = Field(
        description="The technical format of the signed resources",
        default=None,
    )
    targetFormat_ext: Optional["Element"] = Field(
        description="Placeholder element for targetFormat extensions",
        default=None,
        alias="_targetFormat",
    )
    sigFormat: Optional[Code] = Field(
        description="The technical format of the signature",
        default=None,
    )
    sigFormat_ext: Optional["Element"] = Field(
        description="Placeholder element for sigFormat extensions",
        default=None,
        alias="_sigFormat",
    )
    data: Optional[Base64Binary] = Field(
        description="The actual signature content (XML DigSig. JWS, picture, etc.)",
        default=None,
    )
    data_ext: Optional["Element"] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )

    @field_validator(
        *(
            "data",
            "sigFormat",
            "targetFormat",
            "onBehalfOf",
            "who",
            "when",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class Timing(BackboneElement):
    """
    A timing schedule that specifies an event that may occur multiple times
    """

    event: Optional[List[DateTime]] = Field(
        description="When the event occurs",
        default=None,
    )
    event_ext: Optional["Element"] = Field(
        description="Placeholder element for event extensions",
        default=None,
        alias="_event",
    )
    repeat: Optional["Element"] = Field(
        description="When the event is to occur",
        default=None,
    )
    code: Optional["CodeableConcept"] = Field(
        description="BID | TID | QID | AM | PM | QD | QOD | +",
        default=None,
    )

    @field_validator(
        *(
            "code",
            "repeat",
            "event",
            "modifierExtension",
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

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
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

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="duration.empty() or durationUnit.exists()",
            human="if there's a duration, there needs to be duration units",
            key="tim-1",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_2_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="period.empty() or periodUnit.exists()",
            human="if there's a period, there needs to be period units",
            key="tim-2",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_4_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="duration.exists() implies duration >= 0",
            human="duration SHALL be a non-negative value",
            key="tim-4",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_5_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="period.exists() implies period >= 0",
            human="period SHALL be a non-negative value",
            key="tim-5",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_6_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="periodMax.empty() or period.exists()",
            human="If there's a periodMax, there must be a period",
            key="tim-6",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_7_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="durationMax.empty() or duration.exists()",
            human="If there's a durationMax, there must be a duration",
            key="tim-7",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_8_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="countMax.empty() or count.exists()",
            human="If there's a countMax, there must be a count",
            key="tim-8",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_9_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="offset.empty() or (when.exists() and ((when in ('C' | 'CM' | 'CD' | 'CV')).not()))",
            human="If there's an offset, there must be a when (and not C, CM, CD, CV)",
            key="tim-9",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_10_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="timeOfDay.empty() or when.empty()",
            human="If there's a timeOfDay, there cannot be a when, or vice versa",
            key="tim-10",
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


class TriggerDefinition(Element):
    """
    Defines an expected trigger for a module
    """

    type: Optional[Code] = Field(
        description="named-event | periodic | data-changed | data-added | data-modified | data-removed | data-accessed | data-access-ended",
        default=None,
    )
    type_ext: Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    name: Optional[String] = Field(
        description="Name or URI that identifies the event",
        default=None,
    )
    name_ext: Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    timingTiming: Optional["Timing"] = Field(
        description="Timing of the event",
        default=None,
    )
    timingReference: Optional["Reference"] = Field(
        description="Timing of the event",
        default=None,
    )
    timingDate: Optional[Date] = Field(
        description="Timing of the event",
        default=None,
    )
    timingDateTime: Optional[DateTime] = Field(
        description="Timing of the event",
        default=None,
    )
    data: Optional[List["DataRequirement"]] = Field(
        description="Triggering data of the event (multiple = \u0027and\u0027)",
        default=None,
    )
    condition: Optional["Expression"] = Field(
        description="Whether the event triggers (boolean expression)",
        default=None,
    )

    @field_validator(
        *(
            "condition",
            "data",
            "name",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def timing_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Timing", "Reference", Date, DateTime],
            field_name_base="timing",
        )

    @model_validator(mode="after")
    def FHIR_trd_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="data.empty() or timing.empty()",
            human="Either timing, or a data requirement, but not both",
            key="trd-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_trd_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="condition.exists() implies data.exists()",
            human="A condition only if there is a data requirement",
            key="trd-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_trd_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(type = 'named-event' implies name.exists()) and (type = 'periodic' implies timing.exists()) and (type.startsWith('data-') implies data.exists())",
            human="A named event requires a name, a periodic event requires timing, and a data event requires data",
            key="trd-3",
            severity="error",
        )

    @property
    def timing(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="timing",
        )


class UsageContext(Element):
    """
    Describes the context of use for a conformance or knowledge resource
    """

    code: Optional["Coding"] = Field(
        description="Type of context being specified",
        default=None,
    )
    valueCodeableConcept: Optional["CodeableConcept"] = Field(
        description="Value that defines the context",
        default=None,
    )
    valueQuantity: Optional["Quantity"] = Field(
        description="Value that defines the context",
        default=None,
    )
    valueRange: Optional["Range"] = Field(
        description="Value that defines the context",
        default=None,
    )
    valueReference: Optional["Reference"] = Field(
        description="Value that defines the context",
        default=None,
    )

    @field_validator(*("code", "extension"), mode="after", check_fields=None)
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["CodeableConcept", "Quantity", "Range", "Reference"],
            field_name_base="value",
        )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )


class MoneyQuantity(Quantity):
    """
    An amount of money.
    """

    @field_validator(
        *(
            "code",
            "system",
            "unit",
            "comparator",
            "value",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_qty_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="code.empty() or system.exists()",
            human="If a code for the unit is present, the system SHALL also be present",
            key="qty-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_mqty_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(code.exists() or value.empty()) and (system.empty() or system = 'urn:iso:std:iso:4217')",
            human='There SHALL be a code if there is a value and it SHALL be an expression of currency.  If system is present, it SHALL be ISO 4217 (system = "urn:iso:std:iso:4217" - currency).',
            key="mqty-1",
            severity="error",
        )


class SimpleQuantity(Quantity):
    """
    A fixed quantity (no comparator)
    """

    @field_validator(
        *(
            "code",
            "system",
            "unit",
            "comparator",
            "value",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_qty_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="code.empty() or system.exists()",
            human="If a code for the unit is present, the system SHALL also be present",
            key="qty-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sqty_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="comparator.empty()",
            human="The comparator is not used on a SimpleQuantity",
            key="sqty-1",
            severity="error",
        )


class Resource(FHIRBaseModel):
    """
    Base Resource
    """

    id: Optional[String] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    id_ext: Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    meta: Optional["Meta"] = Field(
        description="Metadata about the resource",
        default=None,
    )
    implicitRules: Optional[Uri] = Field(
        description="A set of rules under which this content was created",
        default=None,
    )
    implicitRules_ext: Optional["Element"] = Field(
        description="Placeholder element for implicitRules extensions",
        default=None,
        alias="_implicitRules",
    )
    language: Optional[Code] = Field(
        description="Language of the resource content",
        default=None,
    )
    language_ext: Optional["Element"] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )

    @field_validator(
        *("language", "implicitRules", "meta"), mode="after", check_fields=None
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


class DomainResource(Resource):
    """
    A resource with narrative, extensions, and contained resources
    """

    text: Optional["Narrative"] = Field(
        description="Text summary of the resource, for human interpretation",
        default=None,
    )
    contained: Optional[List["Resource"]] = Field(
        description="Contained, inline Resources",
        default=None,
    )
    extension: Optional[List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: Optional[List["Extension"]] = Field(
        description="Extensions that cannot be ignored",
        default=None,
    )

    @field_validator(
        *(
            "modifierExtension",
            "extension",
            "text",
            "language",
            "implicitRules",
            "meta",
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

    @field_validator(*("contained",), mode="after", check_fields=None)
    @classmethod
    def FHIR_dom_r4b_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="($this is Citation or $this is Evidence or $this is EvidenceReport or $this is EvidenceVariable or $this is MedicinalProductDefinition or $this is PackagedProductDefinition or $this is AdministrableProductDefinition or $this is Ingredient or $this is ClinicalUseDefinition or $this is RegulatedAuthorization or $this is SubstanceDefinition or $this is SubscriptionStatus or $this is SubscriptionTopic) implies (%resource is Citation or %resource is Evidence or %resource is EvidenceReport or %resource is EvidenceVariable or %resource is MedicinalProductDefinition or %resource is PackagedProductDefinition or %resource is AdministrableProductDefinition or %resource is Ingredient or %resource is ClinicalUseDefinition or %resource is RegulatedAuthorization or %resource is SubstanceDefinition or %resource is SubscriptionStatus or %resource is SubscriptionTopic)",
            human="Containing new R4B resources within R4 resources may cause interoperability issues if instances are shared with R4 systems",
            key="dom-r4b",
            severity="warning",
        )

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
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
    def FHIR_dom_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.contained.empty()",
            human="If the resource is contained in another resource, it SHALL NOT contain nested Resources",
            key="dom-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.where(((id.exists() and ('#'+id in (%resource.descendants().reference | %resource.descendants().as(canonical) | %resource.descendants().as(uri) | %resource.descendants().as(url)))) or descendants().where(reference = '#').exists() or descendants().where(as(canonical) = '#').exists() or descendants().where(as(uri) = '#').exists()).not()).trace('unmatched', id).empty()",
            human="If the resource is contained in another resource, it SHALL be referred to from elsewhere in the resource or SHALL refer to the containing resource",
            key="dom-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_4_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.versionId.empty() and contained.meta.lastUpdated.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a meta.versionId or a meta.lastUpdated",
            key="dom-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_5_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.security.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a security label",
            key="dom-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_6_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="text.`div`.exists()",
            human="A resource should have narrative for robust management",
            key="dom-6",
            severity="warning",
        )


model_rebuild_all()