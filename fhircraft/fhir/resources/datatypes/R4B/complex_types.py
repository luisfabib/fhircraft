from pydantic import Field, field_validator, BaseModel
from fhircraft.fhir.resources.datatypes.primitives import *
import fhircraft.fhir.resources.validators as fhir_validators
import typing  

 
 
class Element(BaseModel):
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List['Extension']] = Field(
        description="Additional content defined by implementations",
        default=None,
    )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class BackboneElement(Element):
    modifierExtension: typing.Optional[typing.List['Extension']] = Field(
        description="Extensions that cannot be ignored even if unrecognized",
        default=None,
    )

    @field_validator(*('modifierExtension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('modifierExtension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class xhtml(Element):
    value: String = Field(
        description="Actual xhtml",
        default=None,
    )
    value_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Address(Element):
    use: typing.Optional[Code] = Field(
        description="home | work | temp | old | billing - purpose of this address",
        default=None,
    )
    use_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    type: typing.Optional[Code] = Field(
        description="postal | physical | both",
        default=None,
    )
    type_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    text: typing.Optional[String] = Field(
        description="Text representation of the address",
        default=None,
    )
    text_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
    line: typing.Optional[typing.List[String]] = Field(
        description="Street name, number, direction \u0026 P.O. Box etc.",
        default=None,
    )
    line_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for line extensions",
        default=None,
        alias="_line",
    )
    city: typing.Optional[String] = Field(
        description="Name of city, town etc.",
        default=None,
    )
    city_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for city extensions",
        default=None,
        alias="_city",
    )
    district: typing.Optional[String] = Field(
        description="District name (aka county)",
        default=None,
    )
    district_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for district extensions",
        default=None,
        alias="_district",
    )
    state: typing.Optional[String] = Field(
        description="Sub-unit of country (abbreviations ok)",
        default=None,
    )
    state_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for state extensions",
        default=None,
        alias="_state",
    )
    postalCode: typing.Optional[String] = Field(
        description="Postal code for area",
        default=None,
    )
    postalCode_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for postalCode extensions",
        default=None,
        alias="_postalCode",
    )
    country: typing.Optional[String] = Field(
        description="Country (e.g. can be ISO 3166 2 or 3 letter code)",
        default=None,
    )
    country_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for country extensions",
        default=None,
        alias="_country",
    )
    period: typing.Optional['Period'] = Field(
        description="Time period when address was/is in use",
        default=None,
    )

    @field_validator(*['use', 'type', 'text', 'line', 'city', 'district', 'state', 'postalCode', 'country', 'period'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Age(BaseModel):
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List['Extension']] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    value: typing.Optional[Decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    value_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    comparator: typing.Optional[Code] = Field(
        description="\u003c | \u003c= | \u003e= | \u003e - how to understand the value",
        default=None,
    )
    comparator_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for comparator extensions",
        default=None,
        alias="_comparator",
    )
    unit: typing.Optional[String] = Field(
        description="Unit representation",
        default=None,
    )
    unit_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for unit extensions",
        default=None,
        alias="_unit",
    )
    system: typing.Optional[Uri] = Field(
        description="System that defines coded unit form",
        default=None,
    )
    system_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    code: typing.Optional[Code] = Field(
        description="Coded form of the unit",
        default=None,
    )
    code_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )

    @field_validator(*['extension', 'value', 'comparator', 'unit', 'system', 'code'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Annotation(Element):
    authorReference: typing.Optional['Reference'] = Field(
        description="Individual responsible for the annotation",
        default=None,
    )
    authorString: typing.Optional[String] = Field(
        description="Individual responsible for the annotation",
        default=None,
    )
    author: typing.Optional[String] = Field(
        description="Individual responsible for the annotation",
        default=None,
    )
    author_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for author extensions",
        default=None,
        alias="_author",
    )
    time: typing.Optional[DateTime] = Field(
        description="When the annotation was made",
        default=None,
    )
    time_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for time extensions",
        default=None,
        alias="_time",
    )
    text: Markdown = Field(
        description="The annotation  - text content (as markdown)",
        default=None,
    )
    text_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )

    @field_validator(*['author', 'time', 'text'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


    @property 
    def author(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="author",
        )
 
 
class Attachment(Element):
    contentType: typing.Optional[Code] = Field(
        description="Mime type of the content, with charset etc.",
        default=None,
    )
    contentType_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for contentType extensions",
        default=None,
        alias="_contentType",
    )
    language: typing.Optional[Code] = Field(
        description="Human language of the content (BCP-47)",
        default=None,
    )
    language_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    data: typing.Optional[Base64Binary] = Field(
        description="Data inline, base64ed",
        default=None,
    )
    data_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )
    url: typing.Optional[Url] = Field(
        description="Uri where the data can be found",
        default=None,
    )
    url_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    size: typing.Optional[UnsignedInt] = Field(
        description="Number of bytes of content (if url provided)",
        default=None,
    )
    size_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for size extensions",
        default=None,
        alias="_size",
    )
    hash: typing.Optional[Base64Binary] = Field(
        description="Hash of the data (sha-1, base64ed)",
        default=None,
    )
    hash_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for hash extensions",
        default=None,
        alias="_hash",
    )
    title: typing.Optional[String] = Field(
        description="Label to display in place of the data",
        default=None,
    )
    title_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    creation: typing.Optional[DateTime] = Field(
        description="Date attachment was first created",
        default=None,
    )
    creation_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for creation extensions",
        default=None,
        alias="_creation",
    )

    @field_validator(*['contentType', 'language', 'data', 'url', 'size', 'hash', 'title', 'creation'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class CodeableConcept(Element):
    coding: typing.Optional[typing.List['Coding']] = Field(
        description="Code defined by a terminology system",
        default=None,
    )
    text: typing.Optional[String] = Field(
        description="Plain text representation of the concept",
        default=None,
    )
    text_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )

    @field_validator(*['coding', 'text'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class CodeableReference(Element):
    concept: typing.Optional['CodeableConcept'] = Field(
        description="Reference to a concept (by class)",
        default=None,
    )
    reference: typing.Optional['Reference'] = Field(
        description="Reference to a resource (by instance)",
        default=None,
    )

    @field_validator(*['concept', 'reference'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Coding(Element):
    system: typing.Optional[Uri] = Field(
        description="Identity of the terminology system",
        default=None,
    )
    system_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    version: typing.Optional[String] = Field(
        description="Version of the system - if relevant",
        default=None,
    )
    version_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for version extensions",
        default=None,
        alias="_version",
    )
    code: typing.Optional[Code] = Field(
        description="Symbol in syntax defined by the system",
        default=None,
    )
    code_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )
    display: typing.Optional[String] = Field(
        description="Representation defined by the system",
        default=None,
    )
    display_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for display extensions",
        default=None,
        alias="_display",
    )
    userSelected: typing.Optional[Boolean] = Field(
        description="If this coding was chosen directly by the user",
        default=None,
    )
    userSelected_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for userSelected extensions",
        default=None,
        alias="_userSelected",
    )

    @field_validator(*['system', 'version', 'code', 'display', 'userSelected'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class ContactDetail(Element):
    name: typing.Optional[String] = Field(
        description="Name of an individual to contact",
        default=None,
    )
    name_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    telecom: typing.Optional[typing.List['ContactPoint']] = Field(
        description="Contact details for individual or organization",
        default=None,
    )

    @field_validator(*['name', 'telecom'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class ContactPoint(Element):
    system: typing.Optional[Code] = Field(
        description="phone | fax | email | pager | url | sms | other",
        default=None,
    )
    system_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    value: typing.Optional[String] = Field(
        description="The actual contact point details",
        default=None,
    )
    value_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    use: typing.Optional[Code] = Field(
        description="home | work | temp | old | mobile - purpose of this contact point",
        default=None,
    )
    use_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    rank: typing.Optional[PositiveInt] = Field(
        description="Specify preferred order of use (1 = highest)",
        default=None,
    )
    rank_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for rank extensions",
        default=None,
        alias="_rank",
    )
    period: typing.Optional['Period'] = Field(
        description="Time period when the contact point was/is in use",
        default=None,
    )

    @field_validator(*['system', 'value', 'use', 'rank', 'period'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Contributor(Element):
    type: Code = Field(
        description="author | editor | reviewer | endorser",
        default=None,
    )
    type_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    name: String = Field(
        description="Who contributed the content",
        default=None,
    )
    name_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    contact: typing.Optional[typing.List['ContactDetail']] = Field(
        description="Contact details of the contributor",
        default=None,
    )

    @field_validator(*['type', 'name', 'contact'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Count(BaseModel):
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List['Extension']] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    value: typing.Optional[Decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    value_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    comparator: typing.Optional[Code] = Field(
        description="\u003c | \u003c= | \u003e= | \u003e - how to understand the value",
        default=None,
    )
    comparator_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for comparator extensions",
        default=None,
        alias="_comparator",
    )
    unit: typing.Optional[String] = Field(
        description="Unit representation",
        default=None,
    )
    unit_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for unit extensions",
        default=None,
        alias="_unit",
    )
    system: typing.Optional[Uri] = Field(
        description="System that defines coded unit form",
        default=None,
    )
    system_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    code: typing.Optional[Code] = Field(
        description="Coded form of the unit",
        default=None,
    )
    code_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )

    @field_validator(*['extension', 'value', 'comparator', 'unit', 'system', 'code'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class DataRequirement(Element):
    type: Code = Field(
        description="The type of the required data",
        default=None,
    )
    type_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    profile: typing.Optional[typing.List[Canonical]] = Field(
        description="The profile of the required data",
        default=None,
    )
    profile_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )
    subjectCodeableConcept: typing.Optional['CodeableConcept'] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
    )
    subjectReference: typing.Optional['Reference'] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
    )
    subject: typing.Optional['Reference'] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
    )
    mustSupport: typing.Optional[typing.List[String]] = Field(
        description="Indicates specific structure elements that are referenced by the knowledge module",
        default=None,
    )
    mustSupport_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for mustSupport extensions",
        default=None,
        alias="_mustSupport",
    )
    codeFilter: typing.Optional[typing.List['Element']] = Field(
        description="What codes are expected",
        default=None,
    )
    dateFilter: typing.Optional[typing.List['Element']] = Field(
        description="What dates/date ranges are expected",
        default=None,
    )
    limit: typing.Optional[PositiveInt] = Field(
        description="Number of results",
        default=None,
    )
    limit_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for limit extensions",
        default=None,
        alias="_limit",
    )
    sort: typing.Optional[typing.List['Element']] = Field(
        description="Order of the results",
        default=None,
    )

    @field_validator(*['type', 'profile', 'subject', 'mustSupport', 'codeFilter', 'dateFilter', 'limit', 'sort'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )

    @field_validator(*('codeFilter',), mode="after", check_fields=None)
    @classmethod
    def FHIR_drq_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="path.exists() xor searchParam.exists()",
            human="Either a path or a searchParam must be provided, but not both",
            key="drq-1",
        )

    @field_validator(*('dateFilter',), mode="after", check_fields=None)
    @classmethod
    def FHIR_drq_2_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="path.exists() xor searchParam.exists()",
            human="Either a path or a searchParam must be provided, but not both",
            key="drq-2",
        )


    @property 
    def subject(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="subject",
        )
 
 
class Distance(BaseModel):
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List['Extension']] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    value: typing.Optional[Decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    value_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    comparator: typing.Optional[Code] = Field(
        description="\u003c | \u003c= | \u003e= | \u003e - how to understand the value",
        default=None,
    )
    comparator_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for comparator extensions",
        default=None,
        alias="_comparator",
    )
    unit: typing.Optional[String] = Field(
        description="Unit representation",
        default=None,
    )
    unit_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for unit extensions",
        default=None,
        alias="_unit",
    )
    system: typing.Optional[Uri] = Field(
        description="System that defines coded unit form",
        default=None,
    )
    system_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    code: typing.Optional[Code] = Field(
        description="Coded form of the unit",
        default=None,
    )
    code_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )

    @field_validator(*['extension', 'value', 'comparator', 'unit', 'system', 'code'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Dosage(BackboneElement):
    sequence: typing.Optional[Integer] = Field(
        description="The order of the dosage instructions",
        default=None,
    )
    sequence_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for sequence extensions",
        default=None,
        alias="_sequence",
    )
    text: typing.Optional[String] = Field(
        description="Free text dosage instructions e.g. SIG",
        default=None,
    )
    text_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
    additionalInstruction: typing.Optional[typing.List['CodeableConcept']] = Field(
        description="Supplemental instruction or warnings to the patient - e.g. \"with meals\", \"may cause drowsiness\"",
        default=None,
    )
    patientInstruction: typing.Optional[String] = Field(
        description="Patient or consumer oriented instructions",
        default=None,
    )
    patientInstruction_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for patientInstruction extensions",
        default=None,
        alias="_patientInstruction",
    )
    timing: typing.Optional['Timing'] = Field(
        description="When medication should be administered",
        default=None,
    )
    asNeededBoolean: typing.Optional[Boolean] = Field(
        description="Take \"as needed\" (for x)",
        default=None,
    )
    asNeededCodeableConcept: typing.Optional['CodeableConcept'] = Field(
        description="Take \"as needed\" (for x)",
        default=None,
    )
    asNeeded: typing.Optional['CodeableConcept'] = Field(
        description="Take \"as needed\" (for x)",
        default=None,
    )
    site: typing.Optional['CodeableConcept'] = Field(
        description="Body site to administer to",
        default=None,
    )
    route: typing.Optional['CodeableConcept'] = Field(
        description="How drug should enter body",
        default=None,
    )
    method: typing.Optional['CodeableConcept'] = Field(
        description="Technique for administering medication",
        default=None,
    )
    doseAndRate: typing.Optional[typing.List['Element']] = Field(
        description="Amount of medication administered",
        default=None,
    )
    maxDosePerPeriod: typing.Optional['Ratio'] = Field(
        description="Upper limit on medication per unit of time",
        default=None,
    )
    maxDosePerAdministration: typing.Optional['Quantity'] = Field(
        description="Upper limit on medication per administration",
        default=None,
    )
    maxDosePerLifetime: typing.Optional['Quantity'] = Field(
        description="Upper limit on medication per lifetime of the patient",
        default=None,
    )

    @field_validator(*['sequence', 'text', 'additionalInstruction', 'patientInstruction', 'timing', 'asNeeded', 'site', 'route', 'method', 'doseAndRate', 'maxDosePerPeriod', 'maxDosePerAdministration', 'maxDosePerLifetime'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('modifierExtension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


    @property 
    def asNeeded(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="asNeeded",
        )
 
 
class Duration(BaseModel):
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List['Extension']] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    value: typing.Optional[Decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    value_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    comparator: typing.Optional[Code] = Field(
        description="\u003c | \u003c= | \u003e= | \u003e - how to understand the value",
        default=None,
    )
    comparator_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for comparator extensions",
        default=None,
        alias="_comparator",
    )
    unit: typing.Optional[String] = Field(
        description="Unit representation",
        default=None,
    )
    unit_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for unit extensions",
        default=None,
        alias="_unit",
    )
    system: typing.Optional[Uri] = Field(
        description="System that defines coded unit form",
        default=None,
    )
    system_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    code: typing.Optional[Code] = Field(
        description="Coded form of the unit",
        default=None,
    )
    code_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )

    @field_validator(*['extension', 'value', 'comparator', 'unit', 'system', 'code'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class ElementDefinition(BackboneElement):
    path: String = Field(
        description="Path of the element in the hierarchy of elements",
        default=None,
    )
    path_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for path extensions",
        default=None,
        alias="_path",
    )
    representation: typing.Optional[typing.List[Code]] = Field(
        description="xmlAttr | xmlText | typeAttr | cdaText | xhtml",
        default=None,
    )
    representation_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for representation extensions",
        default=None,
        alias="_representation",
    )
    sliceName: typing.Optional[String] = Field(
        description="Name for this particular element (in a set of slices)",
        default=None,
    )
    sliceName_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for sliceName extensions",
        default=None,
        alias="_sliceName",
    )
    sliceIsConstraining: typing.Optional[Boolean] = Field(
        description="If this slice definition constrains an inherited slice definition (or not)",
        default=None,
    )
    sliceIsConstraining_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for sliceIsConstraining extensions",
        default=None,
        alias="_sliceIsConstraining",
    )
    label: typing.Optional[String] = Field(
        description="Name for element to display with or prompt for element",
        default=None,
    )
    label_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for label extensions",
        default=None,
        alias="_label",
    )
    code: typing.Optional[typing.List['Coding']] = Field(
        description="Corresponding codes in terminologies",
        default=None,
    )
    slicing: typing.Optional['Element'] = Field(
        description="This element is sliced - slices follow",
        default=None,
    )
    short: typing.Optional[String] = Field(
        description="Concise definition for space-constrained presentation",
        default=None,
    )
    short_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for short extensions",
        default=None,
        alias="_short",
    )
    definition: typing.Optional[Markdown] = Field(
        description="Full formal definition as narrative text",
        default=None,
    )
    definition_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for definition extensions",
        default=None,
        alias="_definition",
    )
    comment: typing.Optional[Markdown] = Field(
        description="Comments about the use of this element",
        default=None,
    )
    comment_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )
    requirements: typing.Optional[Markdown] = Field(
        description="Why this resource has been created",
        default=None,
    )
    requirements_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for requirements extensions",
        default=None,
        alias="_requirements",
    )
    alias: typing.Optional[typing.List[String]] = Field(
        description="Other names",
        default=None,
    )
    alias_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for alias extensions",
        default=None,
        alias="_alias",
    )
    min: typing.Optional[UnsignedInt] = Field(
        description="Minimum Cardinality",
        default=None,
    )
    min_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for min extensions",
        default=None,
        alias="_min",
    )
    max: typing.Optional[String] = Field(
        description="Maximum Cardinality (a number or *)",
        default=None,
    )
    max_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for max extensions",
        default=None,
        alias="_max",
    )
    base: typing.Optional['Element'] = Field(
        description="Base definition information for tools",
        default=None,
    )
    contentReference: typing.Optional[Uri] = Field(
        description="Reference to definition of content for the element",
        default=None,
    )
    contentReference_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for contentReference extensions",
        default=None,
        alias="_contentReference",
    )
    type: typing.Optional[typing.List['Element']] = Field(
        description="Data type and Profile for this element",
        default=None,
    )
    defaultValueBase64Binary: typing.Optional[Base64Binary] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueBoolean: typing.Optional[Boolean] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCanonical: typing.Optional[Canonical] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCode: typing.Optional[Code] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDate: typing.Optional[Date] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDateTime: typing.Optional[DateTime] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDecimal: typing.Optional[Decimal] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueId: typing.Optional[Id] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueInstant: typing.Optional[Instant] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueInteger: typing.Optional[Integer] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMarkdown: typing.Optional[Markdown] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueOid: typing.Optional[Oid] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValuePositiveInt: typing.Optional[PositiveInt] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueString: typing.Optional[String] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTime: typing.Optional[Time] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUnsignedInt: typing.Optional[UnsignedInt] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUri: typing.Optional[Uri] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUrl: typing.Optional[Url] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUuid: typing.Optional[Uuid] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAddress: typing.Optional['Address'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAge: typing.Optional['Age'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAnnotation: typing.Optional['Annotation'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAttachment: typing.Optional['Attachment'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCodeableConcept: typing.Optional['CodeableConcept'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCodeableReference: typing.Optional['CodeableReference'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCoding: typing.Optional['Coding'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContactPoint: typing.Optional['ContactPoint'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCount: typing.Optional['Count'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDistance: typing.Optional['Distance'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDuration: typing.Optional['Duration'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueHumanName: typing.Optional['HumanName'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueIdentifier: typing.Optional['Identifier'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMoney: typing.Optional['Money'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValuePeriod: typing.Optional['Period'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueQuantity: typing.Optional['Quantity'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRange: typing.Optional['Range'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRatio: typing.Optional['Ratio'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRatioRange: typing.Optional['RatioRange'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueReference: typing.Optional['Reference'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueSampledData: typing.Optional['SampledData'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueSignature: typing.Optional['Signature'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTiming: typing.Optional['Timing'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContactDetail: typing.Optional['ContactDetail'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContributor: typing.Optional['Contributor'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDataRequirement: typing.Optional['DataRequirement'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueExpression: typing.Optional['Expression'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueParameterDefinition: typing.Optional['ParameterDefinition'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRelatedArtifact: typing.Optional['RelatedArtifact'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTriggerDefinition: typing.Optional['TriggerDefinition'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUsageContext: typing.Optional['UsageContext'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDosage: typing.Optional['Dosage'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValue: typing.Optional['Dosage'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    meaningWhenMissing: typing.Optional[Markdown] = Field(
        description="Implicit meaning when this element is missing",
        default=None,
    )
    meaningWhenMissing_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for meaningWhenMissing extensions",
        default=None,
        alias="_meaningWhenMissing",
    )
    orderMeaning: typing.Optional[String] = Field(
        description="What the order of the elements means",
        default=None,
    )
    orderMeaning_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for orderMeaning extensions",
        default=None,
        alias="_orderMeaning",
    )
    fixedBase64Binary: typing.Optional[Base64Binary] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedBoolean: typing.Optional[Boolean] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCanonical: typing.Optional[Canonical] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCode: typing.Optional[Code] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDate: typing.Optional[Date] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDateTime: typing.Optional[DateTime] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDecimal: typing.Optional[Decimal] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedId: typing.Optional[Id] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedInstant: typing.Optional[Instant] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedInteger: typing.Optional[Integer] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMarkdown: typing.Optional[Markdown] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedOid: typing.Optional[Oid] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedPositiveInt: typing.Optional[PositiveInt] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedString: typing.Optional[String] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTime: typing.Optional[Time] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUnsignedInt: typing.Optional[UnsignedInt] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUri: typing.Optional[Uri] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUrl: typing.Optional[Url] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUuid: typing.Optional[Uuid] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAddress: typing.Optional['Address'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAge: typing.Optional['Age'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAnnotation: typing.Optional['Annotation'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAttachment: typing.Optional['Attachment'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCodeableConcept: typing.Optional['CodeableConcept'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCodeableReference: typing.Optional['CodeableReference'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCoding: typing.Optional['Coding'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContactPoint: typing.Optional['ContactPoint'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCount: typing.Optional['Count'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDistance: typing.Optional['Distance'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDuration: typing.Optional['Duration'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedHumanName: typing.Optional['HumanName'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedIdentifier: typing.Optional['Identifier'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMoney: typing.Optional['Money'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedPeriod: typing.Optional['Period'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedQuantity: typing.Optional['Quantity'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRange: typing.Optional['Range'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRatio: typing.Optional['Ratio'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRatioRange: typing.Optional['RatioRange'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedReference: typing.Optional['Reference'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedSampledData: typing.Optional['SampledData'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedSignature: typing.Optional['Signature'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTiming: typing.Optional['Timing'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContactDetail: typing.Optional['ContactDetail'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContributor: typing.Optional['Contributor'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDataRequirement: typing.Optional['DataRequirement'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedExpression: typing.Optional['Expression'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedParameterDefinition: typing.Optional['ParameterDefinition'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRelatedArtifact: typing.Optional['RelatedArtifact'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTriggerDefinition: typing.Optional['TriggerDefinition'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUsageContext: typing.Optional['UsageContext'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDosage: typing.Optional['Dosage'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixed: typing.Optional['Dosage'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    patternBase64Binary: typing.Optional[Base64Binary] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternBoolean: typing.Optional[Boolean] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCanonical: typing.Optional[Canonical] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCode: typing.Optional[Code] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDate: typing.Optional[Date] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDateTime: typing.Optional[DateTime] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDecimal: typing.Optional[Decimal] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternId: typing.Optional[Id] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternInstant: typing.Optional[Instant] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternInteger: typing.Optional[Integer] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMarkdown: typing.Optional[Markdown] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternOid: typing.Optional[Oid] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternPositiveInt: typing.Optional[PositiveInt] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternString: typing.Optional[String] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTime: typing.Optional[Time] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUnsignedInt: typing.Optional[UnsignedInt] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUri: typing.Optional[Uri] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUrl: typing.Optional[Url] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUuid: typing.Optional[Uuid] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAddress: typing.Optional['Address'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAge: typing.Optional['Age'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAnnotation: typing.Optional['Annotation'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAttachment: typing.Optional['Attachment'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCodeableConcept: typing.Optional['CodeableConcept'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCodeableReference: typing.Optional['CodeableReference'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCoding: typing.Optional['Coding'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContactPoint: typing.Optional['ContactPoint'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCount: typing.Optional['Count'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDistance: typing.Optional['Distance'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDuration: typing.Optional['Duration'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternHumanName: typing.Optional['HumanName'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternIdentifier: typing.Optional['Identifier'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMoney: typing.Optional['Money'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternPeriod: typing.Optional['Period'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternQuantity: typing.Optional['Quantity'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRange: typing.Optional['Range'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRatio: typing.Optional['Ratio'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRatioRange: typing.Optional['RatioRange'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternReference: typing.Optional['Reference'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternSampledData: typing.Optional['SampledData'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternSignature: typing.Optional['Signature'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTiming: typing.Optional['Timing'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContactDetail: typing.Optional['ContactDetail'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContributor: typing.Optional['Contributor'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDataRequirement: typing.Optional['DataRequirement'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternExpression: typing.Optional['Expression'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternParameterDefinition: typing.Optional['ParameterDefinition'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRelatedArtifact: typing.Optional['RelatedArtifact'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTriggerDefinition: typing.Optional['TriggerDefinition'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUsageContext: typing.Optional['UsageContext'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDosage: typing.Optional['Dosage'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    pattern: typing.Optional['Dosage'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    example: typing.Optional[typing.List['Element']] = Field(
        description="Example value (as defined for type)",
        default=None,
    )
    minValueDate: typing.Optional[Date] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueDateTime: typing.Optional[DateTime] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueInstant: typing.Optional[Instant] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueTime: typing.Optional[Time] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueDecimal: typing.Optional[Decimal] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueInteger: typing.Optional[Integer] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValuePositiveInt: typing.Optional[PositiveInt] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueUnsignedInt: typing.Optional[UnsignedInt] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueQuantity: typing.Optional['Quantity'] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValue: typing.Optional['Quantity'] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    maxValueDate: typing.Optional[Date] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueDateTime: typing.Optional[DateTime] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueInstant: typing.Optional[Instant] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueTime: typing.Optional[Time] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueDecimal: typing.Optional[Decimal] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueInteger: typing.Optional[Integer] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValuePositiveInt: typing.Optional[PositiveInt] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueUnsignedInt: typing.Optional[UnsignedInt] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueQuantity: typing.Optional['Quantity'] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValue: typing.Optional['Quantity'] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxLength: typing.Optional[Integer] = Field(
        description="Max length for strings",
        default=None,
    )
    maxLength_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for maxLength extensions",
        default=None,
        alias="_maxLength",
    )
    condition: typing.Optional[typing.List[Id]] = Field(
        description="Reference to invariant about presence",
        default=None,
    )
    condition_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for condition extensions",
        default=None,
        alias="_condition",
    )
    constraint: typing.Optional[typing.List['Element']] = Field(
        description="Condition that must evaluate to true",
        default=None,
    )
    mustSupport: typing.Optional[Boolean] = Field(
        description="If the element must be supported",
        default=None,
    )
    mustSupport_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for mustSupport extensions",
        default=None,
        alias="_mustSupport",
    )
    isModifier: typing.Optional[Boolean] = Field(
        description="If this modifies the meaning of other elements",
        default=None,
    )
    isModifier_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for isModifier extensions",
        default=None,
        alias="_isModifier",
    )
    isModifierReason: typing.Optional[String] = Field(
        description="Reason that this element is marked as a modifier",
        default=None,
    )
    isModifierReason_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for isModifierReason extensions",
        default=None,
        alias="_isModifierReason",
    )
    isSummary: typing.Optional[Boolean] = Field(
        description="Include when _summary = true?",
        default=None,
    )
    isSummary_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for isSummary extensions",
        default=None,
        alias="_isSummary",
    )
    binding: typing.Optional['Element'] = Field(
        description="ValueSet details if this is coded",
        default=None,
    )
    mapping: typing.Optional[typing.List['Element']] = Field(
        description="Map element to another set of definitions",
        default=None,
    )

    @field_validator(*['path', 'representation', 'sliceName', 'sliceIsConstraining', 'label', 'code', 'slicing', 'short', 'definition', 'comment', 'requirements', 'alias', 'min', 'max', 'base', 'contentReference', 'type', 'defaultValue', 'meaningWhenMissing', 'orderMeaning', 'fixed', 'pattern', 'example', 'minValue', 'maxValue', 'maxLength', 'condition', 'constraint', 'mustSupport', 'isModifier', 'isModifierReason', 'isSummary', 'binding', 'mapping'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('modifierExtension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )

    @field_validator(*('slicing',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="discriminator.exists() or description.exists()",
            human="If there are no discriminators, there must be a definition",
            key="eld-1",
        )

    @field_validator(*('max',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_3_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="empty() or ($this = '*') or (toInteger() >= 0)",
            human="Max SHALL be a number or "*"",
            key="eld-3",
        )

    @field_validator(*('type',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_4_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="aggregation.empty() or (code = 'Reference') or (code = 'canonical')",
            human="Aggregation may only be specified if one of the allowed types for the element is a reference",
            key="eld-4",
        )

    @field_validator(*('type',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_17_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="(code='Reference' or code = 'canonical' or code = 'CodeableReference') or targetProfile.empty()",
            human="targetProfile is only allowed if the type is Reference or canonical",
            key="eld-17",
        )

    @field_validator(*('constraint',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_21_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="expression.exists()",
            human="Constraints should have an expression or else validators will not be able to enforce them",
            key="eld-21",
        )

    @field_validator(*('binding',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_12_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="valueSet.exists() implies (valueSet.startsWith('http:') or valueSet.startsWith('https') or valueSet.startsWith('urn:') or valueSet.startsWith('#'))",
            human="ValueSet SHALL start with http:// or https:// or urn:",
            key="eld-12",
        )


    @property 
    def defaultValue(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="defaultValue",
        )
    @property 
    def fixed(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="fixed",
        )
    @property 
    def pattern(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="pattern",
        )
    @property 
    def minValue(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="minValue",
        )
    @property 
    def maxValue(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="maxValue",
        )
 
 
class Expression(Element):
    description: typing.Optional[String] = Field(
        description="Natural language description of the condition",
        default=None,
    )
    description_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    name: typing.Optional[Id] = Field(
        description="Short name assigned to expression for reuse",
        default=None,
    )
    name_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    language: Code = Field(
        description="text/cql | text/fhirpath | application/x-fhir-query | text/cql-identifier | text/cql-expression | etc.",
        default=None,
    )
    language_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    expression: typing.Optional[String] = Field(
        description="Expression in specified language",
        default=None,
    )
    expression_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for expression extensions",
        default=None,
        alias="_expression",
    )
    reference: typing.Optional[Uri] = Field(
        description="Where the expression is found",
        default=None,
    )
    reference_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for reference extensions",
        default=None,
        alias="_reference",
    )

    @field_validator(*['description', 'name', 'language', 'expression', 'reference'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Extension(Element):
    url: String = Field(
        description="identifies the meaning of the extension",
        default=None,
    )
    url_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    valueBase64Binary: typing.Optional[Base64Binary] = Field(
        description="Value of extension",
        default=None,
    )
    valueBoolean: typing.Optional[Boolean] = Field(
        description="Value of extension",
        default=None,
    )
    valueCanonical: typing.Optional[Canonical] = Field(
        description="Value of extension",
        default=None,
    )
    valueCode: typing.Optional[Code] = Field(
        description="Value of extension",
        default=None,
    )
    valueDate: typing.Optional[Date] = Field(
        description="Value of extension",
        default=None,
    )
    valueDateTime: typing.Optional[DateTime] = Field(
        description="Value of extension",
        default=None,
    )
    valueDecimal: typing.Optional[Decimal] = Field(
        description="Value of extension",
        default=None,
    )
    valueId: typing.Optional[Id] = Field(
        description="Value of extension",
        default=None,
    )
    valueInstant: typing.Optional[Instant] = Field(
        description="Value of extension",
        default=None,
    )
    valueInteger: typing.Optional[Integer] = Field(
        description="Value of extension",
        default=None,
    )
    valueMarkdown: typing.Optional[Markdown] = Field(
        description="Value of extension",
        default=None,
    )
    valueOid: typing.Optional[Oid] = Field(
        description="Value of extension",
        default=None,
    )
    valuePositiveInt: typing.Optional[PositiveInt] = Field(
        description="Value of extension",
        default=None,
    )
    valueString: typing.Optional[String] = Field(
        description="Value of extension",
        default=None,
    )
    valueTime: typing.Optional[Time] = Field(
        description="Value of extension",
        default=None,
    )
    valueUnsignedInt: typing.Optional[UnsignedInt] = Field(
        description="Value of extension",
        default=None,
    )
    valueUri: typing.Optional[Uri] = Field(
        description="Value of extension",
        default=None,
    )
    valueUrl: typing.Optional[Url] = Field(
        description="Value of extension",
        default=None,
    )
    valueUuid: typing.Optional[Uuid] = Field(
        description="Value of extension",
        default=None,
    )
    valueAddress: typing.Optional['Address'] = Field(
        description="Value of extension",
        default=None,
    )
    valueAge: typing.Optional['Age'] = Field(
        description="Value of extension",
        default=None,
    )
    valueAnnotation: typing.Optional['Annotation'] = Field(
        description="Value of extension",
        default=None,
    )
    valueAttachment: typing.Optional['Attachment'] = Field(
        description="Value of extension",
        default=None,
    )
    valueCodeableConcept: typing.Optional['CodeableConcept'] = Field(
        description="Value of extension",
        default=None,
    )
    valueCodeableReference: typing.Optional['CodeableReference'] = Field(
        description="Value of extension",
        default=None,
    )
    valueCoding: typing.Optional['Coding'] = Field(
        description="Value of extension",
        default=None,
    )
    valueContactPoint: typing.Optional['ContactPoint'] = Field(
        description="Value of extension",
        default=None,
    )
    valueCount: typing.Optional['Count'] = Field(
        description="Value of extension",
        default=None,
    )
    valueDistance: typing.Optional['Distance'] = Field(
        description="Value of extension",
        default=None,
    )
    valueDuration: typing.Optional['Duration'] = Field(
        description="Value of extension",
        default=None,
    )
    valueHumanName: typing.Optional['HumanName'] = Field(
        description="Value of extension",
        default=None,
    )
    valueIdentifier: typing.Optional['Identifier'] = Field(
        description="Value of extension",
        default=None,
    )
    valueMoney: typing.Optional['Money'] = Field(
        description="Value of extension",
        default=None,
    )
    valuePeriod: typing.Optional['Period'] = Field(
        description="Value of extension",
        default=None,
    )
    valueQuantity: typing.Optional['Quantity'] = Field(
        description="Value of extension",
        default=None,
    )
    valueRange: typing.Optional['Range'] = Field(
        description="Value of extension",
        default=None,
    )
    valueRatio: typing.Optional['Ratio'] = Field(
        description="Value of extension",
        default=None,
    )
    valueRatioRange: typing.Optional['RatioRange'] = Field(
        description="Value of extension",
        default=None,
    )
    valueReference: typing.Optional['Reference'] = Field(
        description="Value of extension",
        default=None,
    )
    valueSampledData: typing.Optional['SampledData'] = Field(
        description="Value of extension",
        default=None,
    )
    valueSignature: typing.Optional['Signature'] = Field(
        description="Value of extension",
        default=None,
    )
    valueTiming: typing.Optional['Timing'] = Field(
        description="Value of extension",
        default=None,
    )
    valueContactDetail: typing.Optional['ContactDetail'] = Field(
        description="Value of extension",
        default=None,
    )
    valueContributor: typing.Optional['Contributor'] = Field(
        description="Value of extension",
        default=None,
    )
    valueDataRequirement: typing.Optional['DataRequirement'] = Field(
        description="Value of extension",
        default=None,
    )
    valueExpression: typing.Optional['Expression'] = Field(
        description="Value of extension",
        default=None,
    )
    valueParameterDefinition: typing.Optional['ParameterDefinition'] = Field(
        description="Value of extension",
        default=None,
    )
    valueRelatedArtifact: typing.Optional['RelatedArtifact'] = Field(
        description="Value of extension",
        default=None,
    )
    valueTriggerDefinition: typing.Optional['TriggerDefinition'] = Field(
        description="Value of extension",
        default=None,
    )
    valueUsageContext: typing.Optional['UsageContext'] = Field(
        description="Value of extension",
        default=None,
    )
    valueDosage: typing.Optional['Dosage'] = Field(
        description="Value of extension",
        default=None,
    )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


    @property 
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="value",
        )
 
 
class HumanName(Element):
    use: typing.Optional[Code] = Field(
        description="usual | official | temp | nickname | anonymous | old | maiden",
        default=None,
    )
    use_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    text: typing.Optional[String] = Field(
        description="Text representation of the full name",
        default=None,
    )
    text_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
    family: typing.Optional[String] = Field(
        description="Family name (often called \u0027Surname\u0027)",
        default=None,
    )
    family_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for family extensions",
        default=None,
        alias="_family",
    )
    given: typing.Optional[typing.List[String]] = Field(
        description="Given names (not always \u0027first\u0027). Includes middle names",
        default=None,
    )
    given_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for given extensions",
        default=None,
        alias="_given",
    )
    prefix: typing.Optional[typing.List[String]] = Field(
        description="Parts that come before the name",
        default=None,
    )
    prefix_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for prefix extensions",
        default=None,
        alias="_prefix",
    )
    suffix: typing.Optional[typing.List[String]] = Field(
        description="Parts that come after the name",
        default=None,
    )
    suffix_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for suffix extensions",
        default=None,
        alias="_suffix",
    )
    period: typing.Optional['Period'] = Field(
        description="Time period when name was/is in use",
        default=None,
    )

    @field_validator(*['use', 'text', 'family', 'given', 'prefix', 'suffix', 'period'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Identifier(Element):
    use: typing.Optional[Code] = Field(
        description="usual | official | temp | secondary | old (If known)",
        default=None,
    )
    use_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    type: typing.Optional['CodeableConcept'] = Field(
        description="Description of identifier",
        default=None,
    )
    system: typing.Optional[Uri] = Field(
        description="The namespace for the identifier value",
        default=None,
    )
    system_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    value: typing.Optional[String] = Field(
        description="The value that is unique",
        default=None,
    )
    value_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    period: typing.Optional['Period'] = Field(
        description="Time period when id is/was valid for use",
        default=None,
    )
    assigner: typing.Optional['Reference'] = Field(
        description="Organization that issued id (may be just text)",
        default=None,
    )

    @field_validator(*['use', 'type', 'system', 'value', 'period', 'assigner'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class MarketingStatus(BackboneElement):
    country: typing.Optional['CodeableConcept'] = Field(
        description="The country in which the marketing authorisation has been granted shall be specified It should be specified using the ISO 3166 \u2011 1 alpha-2 code elements",
        default=None,
    )
    jurisdiction: typing.Optional['CodeableConcept'] = Field(
        description="Where a Medicines Regulatory Agency has granted a marketing authorisation for which specific provisions within a jurisdiction apply, the jurisdiction can be specified using an appropriate controlled terminology The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
    status: 'CodeableConcept' = Field(
        description="This attribute provides information on the status of the marketing of the medicinal product See ISO/TS 20443 for more information and examples",
        default=None,
    )
    dateRange: typing.Optional['Period'] = Field(
        description="The date when the Medicinal Product is placed on the market by the Marketing Authorisation Holder (or where applicable, the manufacturer/distributor) in a country and/or jurisdiction shall be provided A complete date consisting of day, month and year shall be specified using the ISO 8601 date format NOTE \u201cPlaced on the market\u201d refers to the release of the Medicinal Product into the distribution chain",
        default=None,
    )
    restoreDate: typing.Optional[DateTime] = Field(
        description="The date when the Medicinal Product is placed on the market by the Marketing Authorisation Holder (or where applicable, the manufacturer/distributor) in a country and/or jurisdiction shall be provided A complete date consisting of day, month and year shall be specified using the ISO 8601 date format NOTE \u201cPlaced on the market\u201d refers to the release of the Medicinal Product into the distribution chain",
        default=None,
    )
    restoreDate_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for restoreDate extensions",
        default=None,
        alias="_restoreDate",
    )

    @field_validator(*['country', 'jurisdiction', 'status', 'dateRange', 'restoreDate'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('modifierExtension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Meta(Element):
    versionId: typing.Optional[Id] = Field(
        description="Version specific identifier",
        default=None,
    )
    versionId_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for versionId extensions",
        default=None,
        alias="_versionId",
    )
    lastUpdated: typing.Optional[Instant] = Field(
        description="When the resource version last changed",
        default=None,
    )
    lastUpdated_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for lastUpdated extensions",
        default=None,
        alias="_lastUpdated",
    )
    source: typing.Optional[Uri] = Field(
        description="Identifies where the resource comes from",
        default=None,
    )
    source_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for source extensions",
        default=None,
        alias="_source",
    )
    profile: typing.Optional[typing.List[Canonical]] = Field(
        description="Profiles this resource claims to conform to",
        default=None,
    )
    profile_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )
    security: typing.Optional[typing.List['Coding']] = Field(
        description="Security Labels applied to this resource",
        default=None,
    )
    tag: typing.Optional[typing.List['Coding']] = Field(
        description="Tags applied to this resource",
        default=None,
    )

    @field_validator(*['versionId', 'lastUpdated', 'source', 'profile', 'security', 'tag'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Money(Element):
    value: typing.Optional[Decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    value_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    currency: typing.Optional[Code] = Field(
        description="ISO 4217 Currency Code",
        default=None,
    )
    currency_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for currency extensions",
        default=None,
        alias="_currency",
    )

    @field_validator(*['value', 'currency'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Narrative(Element):
    status: Code = Field(
        description="generated | extensions | additional | empty",
        default=None,
    )
    status_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    div: str = Field(
        description="Limited xhtml content",
        default=None,
    )

    @field_validator(*['status', 'div'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )

    @field_validator(*('div',), mode="after", check_fields=None)
    @classmethod
    def FHIR_txt_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="htmlChecks()",
            human="The narrative SHALL contain only the basic html formatting elements and attributes described in chapters 7-11 (except section 4 of chapter 9) and 15 of the HTML 4.0 standard, <a> elements (either name or href), images and internally contained style attributes",
            key="txt-1",
        )

    @field_validator(*('div',), mode="after", check_fields=None)
    @classmethod
    def FHIR_txt_2_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="htmlChecks()",
            human="The narrative SHALL have some non-whitespace content",
            key="txt-2",
        )


 
 
class ParameterDefinition(Element):
    name: typing.Optional[Code] = Field(
        description="Name used to access the parameter value",
        default=None,
    )
    name_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    use: Code = Field(
        description="in | out",
        default=None,
    )
    use_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    min: typing.Optional[Integer] = Field(
        description="Minimum cardinality",
        default=None,
    )
    min_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for min extensions",
        default=None,
        alias="_min",
    )
    max: typing.Optional[String] = Field(
        description="Maximum cardinality (a number of *)",
        default=None,
    )
    max_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for max extensions",
        default=None,
        alias="_max",
    )
    documentation: typing.Optional[String] = Field(
        description="A brief description of the parameter",
        default=None,
    )
    documentation_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for documentation extensions",
        default=None,
        alias="_documentation",
    )
    type: Code = Field(
        description="What type of value",
        default=None,
    )
    type_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    profile: typing.Optional[Canonical] = Field(
        description="What profile the value is expected to be",
        default=None,
    )
    profile_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )

    @field_validator(*['name', 'use', 'min', 'max', 'documentation', 'type', 'profile'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Period(Element):
    start: typing.Optional[DateTime] = Field(
        description="Starting time with inclusive boundary",
        default=None,
    )
    start_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for start extensions",
        default=None,
        alias="_start",
    )
    end: typing.Optional[DateTime] = Field(
        description="End time with inclusive boundary, if not ongoing",
        default=None,
    )
    end_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for end extensions",
        default=None,
        alias="_end",
    )

    @field_validator(*['start', 'end'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Population(BackboneElement):
    ageRange: typing.Optional['Range'] = Field(
        description="The age of the specific population",
        default=None,
    )
    ageCodeableConcept: typing.Optional['CodeableConcept'] = Field(
        description="The age of the specific population",
        default=None,
    )
    age: typing.Optional['CodeableConcept'] = Field(
        description="The age of the specific population",
        default=None,
    )
    gender: typing.Optional['CodeableConcept'] = Field(
        description="The gender of the specific population",
        default=None,
    )
    race: typing.Optional['CodeableConcept'] = Field(
        description="Race of the specific population",
        default=None,
    )
    physiologicalCondition: typing.Optional['CodeableConcept'] = Field(
        description="The existing physiological conditions of the specific population to which this applies",
        default=None,
    )

    @field_validator(*['age', 'gender', 'race', 'physiologicalCondition'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('modifierExtension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


    @property 
    def age(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="age",
        )
 
 
class ProdCharacteristic(BackboneElement):
    height: typing.Optional['Quantity'] = Field(
        description="Where applicable, the height can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    width: typing.Optional['Quantity'] = Field(
        description="Where applicable, the width can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    depth: typing.Optional['Quantity'] = Field(
        description="Where applicable, the depth can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    weight: typing.Optional['Quantity'] = Field(
        description="Where applicable, the weight can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    nominalVolume: typing.Optional['Quantity'] = Field(
        description="Where applicable, the nominal volume can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    externalDiameter: typing.Optional['Quantity'] = Field(
        description="Where applicable, the external diameter can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    shape: typing.Optional[String] = Field(
        description="Where applicable, the shape can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used",
        default=None,
    )
    shape_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for shape extensions",
        default=None,
        alias="_shape",
    )
    color: typing.Optional[typing.List[String]] = Field(
        description="Where applicable, the color can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used",
        default=None,
    )
    color_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for color extensions",
        default=None,
        alias="_color",
    )
    imprint: typing.Optional[typing.List[String]] = Field(
        description="Where applicable, the imprint can be specified as text",
        default=None,
    )
    imprint_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for imprint extensions",
        default=None,
        alias="_imprint",
    )
    image: typing.Optional[typing.List['Attachment']] = Field(
        description="Where applicable, the image can be provided The format of the image attachment shall be specified by regional implementations",
        default=None,
    )
    scoring: typing.Optional['CodeableConcept'] = Field(
        description="Where applicable, the scoring can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used",
        default=None,
    )

    @field_validator(*['height', 'width', 'depth', 'weight', 'nominalVolume', 'externalDiameter', 'shape', 'color', 'imprint', 'image', 'scoring'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('modifierExtension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class ProductShelfLife(BackboneElement):
    identifier: typing.Optional['Identifier'] = Field(
        description="Unique identifier for the packaged Medicinal Product",
        default=None,
    )
    type: 'CodeableConcept' = Field(
        description="This describes the shelf life, taking into account various scenarios such as shelf life of the packaged Medicinal Product itself, shelf life after transformation where necessary and shelf life after the first opening of a bottle, etc. The shelf life type shall be specified using an appropriate controlled vocabulary The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
    period: 'Quantity' = Field(
        description="The shelf life time period can be specified using a numerical value for the period of time and its unit of time measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    specialPrecautionsForStorage: typing.Optional[typing.List['CodeableConcept']] = Field(
        description="Special precautions for storage, if any, can be specified using an appropriate controlled vocabulary The controlled term and the controlled term identifier shall be specified",
        default=None,
    )

    @field_validator(*['identifier', 'type', 'period', 'specialPrecautionsForStorage'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('modifierExtension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Quantity(Element):
    value: typing.Optional[Decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    value_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    comparator: typing.Optional[Code] = Field(
        description="\u003c | \u003c= | \u003e= | \u003e - how to understand the value",
        default=None,
    )
    comparator_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for comparator extensions",
        default=None,
        alias="_comparator",
    )
    unit: typing.Optional[String] = Field(
        description="Unit representation",
        default=None,
    )
    unit_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for unit extensions",
        default=None,
        alias="_unit",
    )
    system: typing.Optional[Uri] = Field(
        description="System that defines coded unit form",
        default=None,
    )
    system_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    code: typing.Optional[Code] = Field(
        description="Coded form of the unit",
        default=None,
    )
    code_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )

    @field_validator(*['value', 'comparator', 'unit', 'system', 'code'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Range(Element):
    low: typing.Optional['Quantity'] = Field(
        description="Low limit",
        default=None,
    )
    high: typing.Optional['Quantity'] = Field(
        description="High limit",
        default=None,
    )

    @field_validator(*['low', 'high'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Ratio(Element):
    numerator: typing.Optional['Quantity'] = Field(
        description="Numerator value",
        default=None,
    )
    denominator: typing.Optional['Quantity'] = Field(
        description="Denominator value",
        default=None,
    )

    @field_validator(*['numerator', 'denominator'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class RatioRange(Element):
    lowNumerator: typing.Optional['Quantity'] = Field(
        description="Low Numerator limit",
        default=None,
    )
    highNumerator: typing.Optional['Quantity'] = Field(
        description="High Numerator limit",
        default=None,
    )
    denominator: typing.Optional['Quantity'] = Field(
        description="Denominator value",
        default=None,
    )

    @field_validator(*['lowNumerator', 'highNumerator', 'denominator'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Reference(Element):
    reference: typing.Optional[String] = Field(
        description="Literal reference, Relative, internal or absolute URL",
        default=None,
    )
    reference_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for reference extensions",
        default=None,
        alias="_reference",
    )
    type: typing.Optional[Uri] = Field(
        description="Type the reference refers to (e.g. \"Patient\")",
        default=None,
    )
    type_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    identifier: typing.Optional['Identifier'] = Field(
        description="Logical reference, when literal reference is not known",
        default=None,
    )
    display: typing.Optional[String] = Field(
        description="Text alternative for the resource",
        default=None,
    )
    display_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for display extensions",
        default=None,
        alias="_display",
    )

    @field_validator(*['reference', 'type', 'identifier', 'display'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class RelatedArtifact(Element):
    type: Code = Field(
        description="documentation | justification | citation | predecessor | successor | derived-from | depends-on | composed-of",
        default=None,
    )
    type_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    label: typing.Optional[String] = Field(
        description="Short label",
        default=None,
    )
    label_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for label extensions",
        default=None,
        alias="_label",
    )
    display: typing.Optional[String] = Field(
        description="Brief description of the related artifact",
        default=None,
    )
    display_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for display extensions",
        default=None,
        alias="_display",
    )
    citation: typing.Optional[Markdown] = Field(
        description="Bibliographic citation for the artifact",
        default=None,
    )
    citation_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for citation extensions",
        default=None,
        alias="_citation",
    )
    url: typing.Optional[Url] = Field(
        description="Where the artifact can be accessed",
        default=None,
    )
    url_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    document: typing.Optional['Attachment'] = Field(
        description="What document is being referenced",
        default=None,
    )
    resource: typing.Optional[Canonical] = Field(
        description="What resource is being referenced",
        default=None,
    )
    resource_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for resource extensions",
        default=None,
        alias="_resource",
    )

    @field_validator(*['type', 'label', 'display', 'citation', 'url', 'document', 'resource'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class SampledData(Element):
    origin: 'Quantity' = Field(
        description="Zero value and units",
        default=None,
    )
    period: Decimal = Field(
        description="Number of milliseconds between samples",
        default=None,
    )
    period_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for period extensions",
        default=None,
        alias="_period",
    )
    factor: typing.Optional[Decimal] = Field(
        description="Multiply data by this before adding to origin",
        default=None,
    )
    factor_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for factor extensions",
        default=None,
        alias="_factor",
    )
    lowerLimit: typing.Optional[Decimal] = Field(
        description="Lower limit of detection",
        default=None,
    )
    lowerLimit_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for lowerLimit extensions",
        default=None,
        alias="_lowerLimit",
    )
    upperLimit: typing.Optional[Decimal] = Field(
        description="Upper limit of detection",
        default=None,
    )
    upperLimit_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for upperLimit extensions",
        default=None,
        alias="_upperLimit",
    )
    dimensions: PositiveInt = Field(
        description="Number of sample points at each time point",
        default=None,
    )
    dimensions_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for dimensions extensions",
        default=None,
        alias="_dimensions",
    )
    data: typing.Optional[String] = Field(
        description="Decimal values with spaces, or \"E\" | \"U\" | \"L\"",
        default=None,
    )
    data_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )

    @field_validator(*['origin', 'period', 'factor', 'lowerLimit', 'upperLimit', 'dimensions', 'data'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Signature(Element):
    type: typing.List['Coding'] = Field(
        description="Indication of the reason the entity signed the object(s)",
        default=None,
    )
    when: Instant = Field(
        description="When the signature was created",
        default=None,
    )
    when_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for when extensions",
        default=None,
        alias="_when",
    )
    who: 'Reference' = Field(
        description="Who signed",
        default=None,
    )
    onBehalfOf: typing.Optional['Reference'] = Field(
        description="The party represented",
        default=None,
    )
    targetFormat: typing.Optional[Code] = Field(
        description="The technical format of the signed resources",
        default=None,
    )
    targetFormat_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for targetFormat extensions",
        default=None,
        alias="_targetFormat",
    )
    sigFormat: typing.Optional[Code] = Field(
        description="The technical format of the signature",
        default=None,
    )
    sigFormat_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for sigFormat extensions",
        default=None,
        alias="_sigFormat",
    )
    data: typing.Optional[Base64Binary] = Field(
        description="The actual signature content (XML DigSig. JWS, picture, etc.)",
        default=None,
    )
    data_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )

    @field_validator(*['type', 'when', 'who', 'onBehalfOf', 'targetFormat', 'sigFormat', 'data'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Timing(BackboneElement):
    event: typing.Optional[typing.List[DateTime]] = Field(
        description="When the event occurs",
        default=None,
    )
    event_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for event extensions",
        default=None,
        alias="_event",
    )
    repeat: typing.Optional['Element'] = Field(
        description="When the event is to occur",
        default=None,
    )
    code: typing.Optional['CodeableConcept'] = Field(
        description="BID | TID | QID | AM | PM | QD | QOD | +",
        default=None,
    )

    @field_validator(*['event', 'repeat', 'code'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('modifierExtension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="duration.empty() or durationUnit.exists()",
            human="if there's a duration, there needs to be duration units",
            key="tim-1",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_2_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="period.empty() or periodUnit.exists()",
            human="if there's a period, there needs to be period units",
            key="tim-2",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_4_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="duration.exists() implies duration >= 0",
            human="duration SHALL be a non-negative value",
            key="tim-4",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_5_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="period.exists() implies period >= 0",
            human="period SHALL be a non-negative value",
            key="tim-5",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_6_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="periodMax.empty() or period.exists()",
            human="If there's a periodMax, there must be a period",
            key="tim-6",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_7_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="durationMax.empty() or duration.exists()",
            human="If there's a durationMax, there must be a duration",
            key="tim-7",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_8_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="countMax.empty() or count.exists()",
            human="If there's a countMax, there must be a count",
            key="tim-8",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_9_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="offset.empty() or (when.exists() and ((when in ('C' | 'CM' | 'CD' | 'CV')).not()))",
            human="If there's an offset, there must be a when (and not C, CM, CD, CV)",
            key="tim-9",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_10_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="timeOfDay.empty() or when.empty()",
            human="If there's a timeOfDay, there cannot be a when, or vice versa",
            key="tim-10",
        )


 
 
class TriggerDefinition(Element):
    type: Code = Field(
        description="named-event | periodic | data-changed | data-added | data-modified | data-removed | data-accessed | data-access-ended",
        default=None,
    )
    type_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    name: typing.Optional[String] = Field(
        description="Name or URI that identifies the event",
        default=None,
    )
    name_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    timingTiming: typing.Optional['Timing'] = Field(
        description="Timing of the event",
        default=None,
    )
    timingReference: typing.Optional['Reference'] = Field(
        description="Timing of the event",
        default=None,
    )
    timingDate: typing.Optional[Date] = Field(
        description="Timing of the event",
        default=None,
    )
    timingDateTime: typing.Optional[DateTime] = Field(
        description="Timing of the event",
        default=None,
    )
    timing: typing.Optional[DateTime] = Field(
        description="Timing of the event",
        default=None,
    )
    timing_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for timing extensions",
        default=None,
        alias="_timing",
    )
    data: typing.Optional[typing.List['DataRequirement']] = Field(
        description="Triggering data of the event (multiple = \u0027and\u0027)",
        default=None,
    )
    condition: typing.Optional['Expression'] = Field(
        description="Whether the event triggers (boolean expression)",
        default=None,
    )

    @field_validator(*['type', 'name', 'timing', 'data', 'condition'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


    @property 
    def timing(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="timing",
        )
 
 
class UsageContext(Element):
    code: 'Coding' = Field(
        description="Type of context being specified",
        default=None,
    )
    valueCodeableConcept: 'CodeableConcept' = Field(
        description="Value that defines the context",
        default=None,
    )
    valueQuantity: 'Quantity' = Field(
        description="Value that defines the context",
        default=None,
    )
    valueRange: 'Range' = Field(
        description="Value that defines the context",
        default=None,
    )
    valueReference: 'Reference' = Field(
        description="Value that defines the context",
        default=None,
    )
    value: 'Reference' = Field(
        description="Value that defines the context",
        default=None,
    )

    @field_validator(*['code', 'value'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


    @property 
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="value",
        )
 
 
class MoneyQuantity(Quantity):

    @field_validator(*['value', 'comparator', 'unit', 'system', 'code'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class SimpleQuantity(Quantity):

    @field_validator(*['value', 'comparator', 'unit', 'system', 'code'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )


 
 
class Resource(BaseModel):
    id: typing.Optional[String] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    meta: typing.Optional['Meta'] = Field(
        description="Metadata about the resource",
        default=None,
    )
    implicitRules: typing.Optional[Uri] = Field(
        description="A set of rules under which this content was created",
        default=None,
    )
    implicitRules_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for implicitRules extensions",
        default=None,
        alias="_implicitRules",
    )
    language: typing.Optional[Code] = Field(
        description="Language of the resource content",
        default=None,
    )
    language_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )

    @field_validator(*['meta', 'implicitRules', 'language'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )


 
 
class DomainResource(Resource):
    text: typing.Optional['Narrative'] = Field(
        description="Text summary of the resource, for human interpretation",
        default=None,
    )
    contained: typing.Optional[typing.List['Resource']] = Field(
        description="Contained, inline Resources",
        default=None,
    )
    extension: typing.Optional[typing.List['Extension']] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: typing.Optional[typing.List['Extension']] = Field(
        description="Extensions that cannot be ignored",
        default=None,
    )

    @field_validator(*['text', 'extension', 'modifierExtension'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
        )

    @field_validator(*('contained',), mode="after", check_fields=None)
    @classmethod
    def FHIR_dom_r4b_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="($this is Citation or $this is Evidence or $this is EvidenceReport or $this is EvidenceVariable or $this is MedicinalProductDefinition or $this is PackagedProductDefinition or $this is AdministrableProductDefinition or $this is Ingredient or $this is ClinicalUseDefinition or $this is RegulatedAuthorization or $this is SubstanceDefinition or $this is SubscriptionStatus or $this is SubscriptionTopic) implies (%resource is Citation or %resource is Evidence or %resource is EvidenceReport or %resource is EvidenceVariable or %resource is MedicinalProductDefinition or %resource is PackagedProductDefinition or %resource is AdministrableProductDefinition or %resource is Ingredient or %resource is ClinicalUseDefinition or %resource is RegulatedAuthorization or %resource is SubstanceDefinition or %resource is SubscriptionStatus or %resource is SubscriptionTopic)",
            human="Containing new R4B resources within R4 resources may cause interoperability issues if instances are shared with R4 systems",
            key="dom-r4b",
        )

    @field_validator(*['extension', 'modifierExtension'], mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
        )




 
Element.model_rebuild()
 
BackboneElement.model_rebuild()
 
Address.model_rebuild()
 
Age.model_rebuild()
 
Annotation.model_rebuild()
 
CodeableConcept.model_rebuild()
 
CodeableReference.model_rebuild()
 
ContactDetail.model_rebuild()
 
ContactPoint.model_rebuild()
 
Contributor.model_rebuild()
 
Count.model_rebuild()
 
DataRequirement.model_rebuild()
 
Distance.model_rebuild()
 
Dosage.model_rebuild()
 
Duration.model_rebuild()
 
ElementDefinition.model_rebuild()
 
Extension.model_rebuild()
 
HumanName.model_rebuild()
 
Identifier.model_rebuild()
 
MarketingStatus.model_rebuild()
 
Meta.model_rebuild()
 
Narrative.model_rebuild()
 
Population.model_rebuild()
 
ProdCharacteristic.model_rebuild()
 
ProductShelfLife.model_rebuild()
 
Range.model_rebuild()
 
Ratio.model_rebuild()
 
RatioRange.model_rebuild()
 
Reference.model_rebuild()
 
RelatedArtifact.model_rebuild()
 
SampledData.model_rebuild()
 
Signature.model_rebuild()
 
Timing.model_rebuild()
 
TriggerDefinition.model_rebuild()
 
UsageContext.model_rebuild()
 
Resource.model_rebuild()
 
DomainResource.model_rebuild()
