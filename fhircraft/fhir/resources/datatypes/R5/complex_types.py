from pydantic import Field, field_validator, model_validator, BaseModel
from fhircraft.fhir.resources.datatypes.primitives import *
import fhircraft.fhir.resources.validators as fhir_validators
import typing  
 
 
class Element(BaseModel):
    """
    Base for all elements
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
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
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class BackboneElement(Element):
    """
    Base for elements defined inside a resource
    """
    modifierExtension: typing.Optional[typing.List["Extension"]] = Field(
        description="Extensions that cannot be ignored even if unrecognized",
        default=None,
    )
    @field_validator(*('modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class xhtml(Element):
    """
    Primitive Type xhtml
    """
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
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Address(BaseModel):
    """
    An address expressed using postal conventions (as opposed to GPS or other location definition formats)
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
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
        description="Country (e.g. may be ISO 3166 2 or 3 letter code)",
        default=None,
    )
    country_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for country extensions",
        default=None,
        alias="_country",
    )
    period: typing.Optional["Period"] = Field(
        description="Time period when address was/is in use",
        default=None,
    )
    @field_validator(*('period', 'country', 'postalCode', 'state', 'district', 'city', 'line', 'text', 'type', 'use', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Age(BaseModel):
    """
    A duration of time during which an organism (or a process) has existed
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
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
        description="\u003c | \u003c= | \u003e= | \u003e | ad - how to understand the value",
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
    @field_validator(*('code', 'system', 'unit', 'comparator', 'value', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Annotation(BaseModel):
    """
    Text node with attribution
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    authorReference: typing.Optional["Reference"] = Field(
        description="Individual responsible for the annotation",
        default=None,
    )
    authorString: typing.Optional[String] = Field(
        description="Individual responsible for the annotation",
        default=None,
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
    @field_validator(*('text', 'time', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def author_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element( 
            self,
            field_types=[Reference, String],
            field_name_base="author",
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

    @property 
    def author(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="author",
        )

 
 
class Attachment(BaseModel):
    """
    Content in a format defined elsewhere
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
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
    size: typing.Optional[Integer64] = Field(
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
    height: typing.Optional[PositiveInt] = Field(
        description="Height of the image in pixels (photo/video)",
        default=None,
    )
    height_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for height extensions",
        default=None,
        alias="_height",
    )
    width: typing.Optional[PositiveInt] = Field(
        description="Width of the image in pixels (photo/video)",
        default=None,
    )
    width_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for width extensions",
        default=None,
        alias="_width",
    )
    frames: typing.Optional[PositiveInt] = Field(
        description="Number of frames if \u003e 1 (photo)",
        default=None,
    )
    frames_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for frames extensions",
        default=None,
        alias="_frames",
    )
    duration: typing.Optional[Decimal] = Field(
        description="Length in seconds (audio / video)",
        default=None,
    )
    duration_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for duration extensions",
        default=None,
        alias="_duration",
    )
    pages: typing.Optional[PositiveInt] = Field(
        description="Number of printed pages",
        default=None,
    )
    pages_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for pages extensions",
        default=None,
        alias="_pages",
    )
    @field_validator(*('pages', 'duration', 'frames', 'width', 'height', 'creation', 'title', 'hash', 'size', 'url', 'data', 'language', 'contentType', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


 
 
class Availability(BaseModel):
    """
    Availability data for an {item}
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    availableTime: typing.Optional[typing.List["Element"]] = Field(
        description="Times the {item} is available",
        default=None,
    )
    notAvailableTime: typing.Optional[typing.List["Element"]] = Field(
        description="Not available during this time due to provided reason",
        default=None,
    )
    @field_validator(*('notAvailableTime', 'availableTime', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @field_validator(*('availableTime',), mode="after", check_fields=None)
    @classmethod
    def FHIR_av_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="allDay.exists().not() or (allDay implies availableStartTime.exists().not() and availableEndTime.exists().not())",
            human="Cannot include start/end times when selecting all day availability.",
            key="av-1",
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


 
 
class BackboneType(BaseModel):
    """
    Base for datatypes that can carry modifier extensions
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: typing.Optional[typing.List["Extension"]] = Field(
        description="Extensions that cannot be ignored even if unrecognized",
        default=None,
    )
    @field_validator(*('modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Base(BaseModel):
    """
    Base for all types and resources
    """
    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


 
 
class CodeableConcept(BaseModel):
    """
    Concept - reference to a terminology or just  text
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    coding: typing.Optional[typing.List["Coding"]] = Field(
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
    @field_validator(*('text', 'coding', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class CodeableReference(BaseModel):
    """
    Reference to a resource or a concept
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    concept: typing.Optional[CodeableConcept] = Field(
        description="Reference to a concept (by class)",
        default=None,
    )
    reference: typing.Optional["Reference"] = Field(
        description="Reference to a resource (by instance)",
        default=None,
    )
    @field_validator(*('reference', 'concept', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Coding(BaseModel):
    """
    A reference to a code defined by a terminology system
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
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
    @field_validator(*('userSelected', 'display', 'code', 'version', 'system', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cod_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="code.exists().not() implies display.exists().not()",
            human="A Coding SHOULD NOT have a display unless a code is also present.  Computation on Coding.display alone is generally unsafe.  Consider using CodeableConcept.text",
            key="cod-1",
            severity="warning",
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


 
 
class ContactDetail(BaseModel):
    """
    Contact information
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    name: typing.Optional[String] = Field(
        description="Name of an individual to contact",
        default=None,
    )
    name_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    telecom: typing.Optional[typing.List["ContactPoint"]] = Field(
        description="Contact details for individual or organization",
        default=None,
    )
    @field_validator(*('telecom', 'name', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class ContactPoint(BaseModel):
    """
    Details of a Technology mediated contact point (phone, fax, email, etc.)
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
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
    period: typing.Optional["Period"] = Field(
        description="Time period when the contact point was/is in use",
        default=None,
    )
    @field_validator(*('period', 'rank', 'use', 'value', 'system', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


 
 
class Contributor(BaseModel):
    """
    Contributor information
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
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
    contact: typing.Optional[typing.List[ContactDetail]] = Field(
        description="Contact details of the contributor",
        default=None,
    )
    @field_validator(*('contact', 'name', 'type', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Count(BaseModel):
    """
    A measured or measurable amount
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
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
        description="\u003c | \u003c= | \u003e= | \u003e | ad - how to understand the value",
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
    @field_validator(*('code', 'system', 'unit', 'comparator', 'value', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
            human="There SHALL be a code with a value of \"1\" if there is a value. If system is present, it SHALL be UCUM.  If present, the value SHALL be a whole number.",
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


 
 
class DataRequirement(BaseModel):
    """
    Describes a required data item
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
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
    subjectCodeableConcept: typing.Optional[CodeableConcept] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
    )
    subjectReference: typing.Optional["Reference"] = Field(
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
    codeFilter: typing.Optional[typing.List["Element"]] = Field(
        description="What codes are expected",
        default=None,
    )
    dateFilter: typing.Optional[typing.List["Element"]] = Field(
        description="What dates/date ranges are expected",
        default=None,
    )
    valueFilter: typing.Optional[typing.List["Element"]] = Field(
        description="What values are expected",
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
    sort: typing.Optional[typing.List["Element"]] = Field(
        description="Order of the results",
        default=None,
    )
    @field_validator(*('sort', 'limit', 'valueFilter', 'dateFilter', 'codeFilter', 'mustSupport', 'profile', 'type', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @field_validator(*('codeFilter',), mode="after", check_fields=None)
    @classmethod
    def FHIR_drq_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="path.exists() xor searchParam.exists()",
            human="Either a path or a searchParam must be provided, but not both",
            key="drq-1",
            severity="error",
        )

    @field_validator(*('dateFilter',), mode="after", check_fields=None)
    @classmethod
    def FHIR_drq_2_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="path.exists() xor searchParam.exists()",
            human="Either a path or a searchParam must be provided, but not both",
            key="drq-2",
            severity="error",
        )

    @model_validator(mode="after")
    def subject_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element( 
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="subject",
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

    @property 
    def subject(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="subject",
        )

 
 
class DataType(Element):
    """
    Reuseable Types
    """
    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Distance(BaseModel):
    """
    A length - a value with a unit that is a physical distance
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
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
        description="\u003c | \u003c= | \u003e= | \u003e | ad - how to understand the value",
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
    @field_validator(*('code', 'system', 'unit', 'comparator', 'value', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Dosage(BackboneType):
    """
    How the medication is/was taken or should be taken
    """
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
    additionalInstruction: typing.Optional[typing.List[CodeableConcept]] = Field(
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
    timing: typing.Optional["Timing"] = Field(
        description="When medication should be administered",
        default=None,
    )
    asNeeded: typing.Optional[Boolean] = Field(
        description="Take \"as needed\"",
        default=None,
    )
    asNeeded_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for asNeeded extensions",
        default=None,
        alias="_asNeeded",
    )
    asNeededFor: typing.Optional[typing.List[CodeableConcept]] = Field(
        description="Take \"as needed\" (for x)",
        default=None,
    )
    site: typing.Optional[CodeableConcept] = Field(
        description="Body site to administer to",
        default=None,
    )
    route: typing.Optional[CodeableConcept] = Field(
        description="How drug should enter body",
        default=None,
    )
    method: typing.Optional[CodeableConcept] = Field(
        description="Technique for administering medication",
        default=None,
    )
    doseAndRate: typing.Optional[typing.List["Element"]] = Field(
        description="Amount of medication administered, to be administered or typical amount to be administered",
        default=None,
    )
    maxDosePerPeriod: typing.Optional[typing.List["Ratio"]] = Field(
        description="Upper limit on medication per unit of time",
        default=None,
    )
    maxDosePerAdministration: typing.Optional["Quantity"] = Field(
        description="Upper limit on medication per administration",
        default=None,
    )
    maxDosePerLifetime: typing.Optional["Quantity"] = Field(
        description="Upper limit on medication per lifetime of the patient",
        default=None,
    )
    @field_validator(*('maxDosePerLifetime', 'maxDosePerAdministration', 'maxDosePerPeriod', 'doseAndRate', 'method', 'route', 'site', 'asNeededFor', 'asNeeded', 'timing', 'patientInstruction', 'additionalInstruction', 'text', 'sequence', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def FHIR_dos_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="asNeededFor.empty() or asNeeded.empty() or asNeeded",
            human="AsNeededFor can only be set if AsNeeded is empty or true",
            key="dos-1",
            severity="error",
        )


 
 
class Duration(BaseModel):
    """
    A length of time
    """
    id: typing.Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
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
        description="\u003c | \u003c= | \u003e= | \u003e | ad - how to understand the value",
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
    @field_validator(*('code', 'system', 'unit', 'comparator', 'value', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_drt_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="code.exists() implies ((system = %ucum) and value.exists())",
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


 
 
class ElementDefinition(BackboneType):
    """
    Definition of an element in a resource or extension
    """
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
    code: typing.Optional[typing.List[Coding]] = Field(
        description="Corresponding codes in terminologies",
        default=None,
    )
    slicing: typing.Optional["Element"] = Field(
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
    base: typing.Optional["Element"] = Field(
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
    type: typing.Optional[typing.List["Element"]] = Field(
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
    defaultValueInteger64: typing.Optional[Integer64] = Field(
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
    defaultValueAddress: typing.Optional[Address] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAge: typing.Optional[Age] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAnnotation: typing.Optional[Annotation] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAttachment: typing.Optional[Attachment] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCodeableConcept: typing.Optional[CodeableConcept] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCodeableReference: typing.Optional[CodeableReference] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCoding: typing.Optional[Coding] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContactPoint: typing.Optional[ContactPoint] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCount: typing.Optional[Count] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDistance: typing.Optional[Distance] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDuration: typing.Optional[Duration] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueHumanName: typing.Optional["HumanName"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueIdentifier: typing.Optional["Identifier"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMoney: typing.Optional["Money"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValuePeriod: typing.Optional["Period"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueQuantity: typing.Optional["Quantity"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRange: typing.Optional["Range"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRatio: typing.Optional["Ratio"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRatioRange: typing.Optional["RatioRange"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueReference: typing.Optional["Reference"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueSampledData: typing.Optional["SampledData"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueSignature: typing.Optional["Signature"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTiming: typing.Optional["Timing"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContactDetail: typing.Optional[ContactDetail] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDataRequirement: typing.Optional[DataRequirement] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueExpression: typing.Optional["Expression"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueParameterDefinition: typing.Optional["ParameterDefinition"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRelatedArtifact: typing.Optional["RelatedArtifact"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTriggerDefinition: typing.Optional["TriggerDefinition"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUsageContext: typing.Optional["UsageContext"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAvailability: typing.Optional['Availability'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueExtendedContactDetail: typing.Optional['ExtendedContactDetail'] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDosage: typing.Optional[Dosage] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMeta: typing.Optional["Meta"] = Field(
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
    fixedInteger64: typing.Optional[Integer64] = Field(
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
    fixedAddress: typing.Optional[Address] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAge: typing.Optional[Age] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAnnotation: typing.Optional[Annotation] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAttachment: typing.Optional[Attachment] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCodeableConcept: typing.Optional[CodeableConcept] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCodeableReference: typing.Optional[CodeableReference] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCoding: typing.Optional[Coding] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContactPoint: typing.Optional[ContactPoint] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCount: typing.Optional[Count] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDistance: typing.Optional[Distance] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDuration: typing.Optional[Duration] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedHumanName: typing.Optional["HumanName"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedIdentifier: typing.Optional["Identifier"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMoney: typing.Optional["Money"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedPeriod: typing.Optional["Period"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedQuantity: typing.Optional["Quantity"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRange: typing.Optional["Range"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRatio: typing.Optional["Ratio"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRatioRange: typing.Optional["RatioRange"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedReference: typing.Optional["Reference"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedSampledData: typing.Optional["SampledData"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedSignature: typing.Optional["Signature"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTiming: typing.Optional["Timing"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContactDetail: typing.Optional[ContactDetail] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDataRequirement: typing.Optional[DataRequirement] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedExpression: typing.Optional["Expression"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedParameterDefinition: typing.Optional["ParameterDefinition"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRelatedArtifact: typing.Optional["RelatedArtifact"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTriggerDefinition: typing.Optional["TriggerDefinition"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUsageContext: typing.Optional["UsageContext"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAvailability: typing.Optional['Availability'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedExtendedContactDetail: typing.Optional['ExtendedContactDetail'] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDosage: typing.Optional[Dosage] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMeta: typing.Optional["Meta"] = Field(
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
    patternInteger64: typing.Optional[Integer64] = Field(
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
    patternAddress: typing.Optional[Address] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAge: typing.Optional[Age] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAnnotation: typing.Optional[Annotation] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAttachment: typing.Optional[Attachment] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCodeableConcept: typing.Optional[CodeableConcept] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCodeableReference: typing.Optional[CodeableReference] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCoding: typing.Optional[Coding] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContactPoint: typing.Optional[ContactPoint] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCount: typing.Optional[Count] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDistance: typing.Optional[Distance] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDuration: typing.Optional[Duration] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternHumanName: typing.Optional["HumanName"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternIdentifier: typing.Optional["Identifier"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMoney: typing.Optional["Money"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternPeriod: typing.Optional["Period"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternQuantity: typing.Optional["Quantity"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRange: typing.Optional["Range"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRatio: typing.Optional["Ratio"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRatioRange: typing.Optional["RatioRange"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternReference: typing.Optional["Reference"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternSampledData: typing.Optional["SampledData"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternSignature: typing.Optional["Signature"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTiming: typing.Optional["Timing"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContactDetail: typing.Optional[ContactDetail] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDataRequirement: typing.Optional[DataRequirement] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternExpression: typing.Optional["Expression"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternParameterDefinition: typing.Optional["ParameterDefinition"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRelatedArtifact: typing.Optional["RelatedArtifact"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTriggerDefinition: typing.Optional["TriggerDefinition"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUsageContext: typing.Optional["UsageContext"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAvailability: typing.Optional['Availability'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternExtendedContactDetail: typing.Optional['ExtendedContactDetail'] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDosage: typing.Optional[Dosage] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMeta: typing.Optional["Meta"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    example: typing.Optional[typing.List["Element"]] = Field(
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
    minValueInteger64: typing.Optional[Integer64] = Field(
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
    minValueQuantity: typing.Optional["Quantity"] = Field(
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
    maxValueInteger64: typing.Optional[Integer64] = Field(
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
    maxValueQuantity: typing.Optional["Quantity"] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxLength: typing.Optional[Integer] = Field(
        description="Max length for string type data",
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
    constraint: typing.Optional[typing.List["Element"]] = Field(
        description="Condition that must evaluate to true",
        default=None,
    )
    mustHaveValue: typing.Optional[Boolean] = Field(
        description="For primitives, that a value must be present - not replaced by an extension",
        default=None,
    )
    mustHaveValue_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for mustHaveValue extensions",
        default=None,
        alias="_mustHaveValue",
    )
    valueAlternatives: typing.Optional[typing.List[Canonical]] = Field(
        description="Extensions that are allowed to replace a primitive value",
        default=None,
    )
    valueAlternatives_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for valueAlternatives extensions",
        default=None,
        alias="_valueAlternatives",
    )
    mustSupport: typing.Optional[Boolean] = Field(
        description="If the element must be supported (discouraged - see obligations)",
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
    binding: typing.Optional["Element"] = Field(
        description="ValueSet details if this is coded",
        default=None,
    )
    mapping: typing.Optional[typing.List["Element"]] = Field(
        description="Map element to another set of definitions",
        default=None,
    )
    @field_validator(*('mapping', 'binding', 'isSummary', 'isModifierReason', 'isModifier', 'mustSupport', 'valueAlternatives', 'mustHaveValue', 'constraint', 'condition', 'maxLength', 'example', 'orderMeaning', 'meaningWhenMissing', 'type', 'contentReference', 'base', 'max', 'min', 'alias', 'requirements', 'comment', 'definition', 'short', 'slicing', 'code', 'label', 'sliceIsConstraining', 'sliceName', 'representation', 'path', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @field_validator(*('max',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_3_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="empty() or ($this = '*') or (toInteger() >= 0)",
            human="Max SHALL be a number or \"*\"",
            key="eld-3",
            severity="error",
        )

    @field_validator(*('type',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_4_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="aggregation.empty() or (code = 'Reference') or (code = 'canonical') or (code = 'CodeableReference')",
            human="Aggregation may only be specified if one of the allowed types for the element is a reference",
            key="eld-4",
            severity="error",
        )

    @field_validator(*('type',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_17_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="(code='Reference' or code = 'canonical' or code = 'CodeableReference') or targetProfile.empty()",
            human="targetProfile is only allowed if the type is Reference or canonical",
            key="eld-17",
            severity="error",
        )

    @field_validator(*('constraint',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_21_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="expression.exists()",
            human="Constraints should have an expression or else validators will not be able to enforce them",
            key="eld-21",
            severity="warning",
        )

    @field_validator(*('constraint',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_26_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="(severity = 'error') implies suppress.empty()",
            human="Errors cannot be suppressed",
            key="eld-26",
            severity="error",
        )

    @field_validator(*('binding',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_12_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="valueSet.exists() implies (valueSet.startsWith('http:') or valueSet.startsWith('https') or valueSet.startsWith('urn:') or valueSet.startsWith('#'))",
            human="ValueSet SHALL start with http:// or https:// or urn: or #",
            key="eld-12",
            severity="error",
        )

    @field_validator(*('binding',), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_23_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="description.exists() or valueSet.exists()",
            human="binding SHALL have either description or valueSet",
            key="eld-23",
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
            field_types=[Base64Binary, Boolean, Canonical, Code, Date, DateTime, Decimal, Id, Instant, Integer, Integer64, Markdown, Oid, PositiveInt, String, Time, UnsignedInt, Uri, Url, Uuid, Address, Age, Annotation, Attachment, CodeableConcept, CodeableReference, Coding, ContactPoint, Count, Distance, Duration, HumanName, Identifier, Money, Period, Quantity, Range, Ratio, RatioRange, Reference, SampledData, Signature, Timing, ContactDetail, DataRequirement, Expression, ParameterDefinition, RelatedArtifact, TriggerDefinition, UsageContext, 'Availability', 'ExtendedContactDetail', Dosage, Meta],
            field_name_base="defaultValue",
        )

    @model_validator(mode="after")
    def fixed_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element( 
            self,
            field_types=[Base64Binary, Boolean, Canonical, Code, Date, DateTime, Decimal, Id, Instant, Integer, Integer64, Markdown, Oid, PositiveInt, String, Time, UnsignedInt, Uri, Url, Uuid, Address, Age, Annotation, Attachment, CodeableConcept, CodeableReference, Coding, ContactPoint, Count, Distance, Duration, HumanName, Identifier, Money, Period, Quantity, Range, Ratio, RatioRange, Reference, SampledData, Signature, Timing, ContactDetail, DataRequirement, Expression, ParameterDefinition, RelatedArtifact, TriggerDefinition, UsageContext, 'Availability', 'ExtendedContactDetail', Dosage, Meta],
            field_name_base="fixed",
        )

    @model_validator(mode="after")
    def pattern_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element( 
            self,
            field_types=[Base64Binary, Boolean, Canonical, Code, Date, DateTime, Decimal, Id, Instant, Integer, Integer64, Markdown, Oid, PositiveInt, String, Time, UnsignedInt, Uri, Url, Uuid, Address, Age, Annotation, Attachment, CodeableConcept, CodeableReference, Coding, ContactPoint, Count, Distance, Duration, HumanName, Identifier, Money, Period, Quantity, Range, Ratio, RatioRange, Reference, SampledData, Signature, Timing, ContactDetail, DataRequirement, Expression, ParameterDefinition, RelatedArtifact, TriggerDefinition, UsageContext, 'Availability', 'ExtendedContactDetail', Dosage, Meta],
            field_name_base="pattern",
        )

    @model_validator(mode="after")
    def minValue_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element( 
            self,
            field_types=[Date, DateTime, Instant, Time, Decimal, Integer, Integer64, PositiveInt, UnsignedInt, Quantity],
            field_name_base="minValue",
        )

    @model_validator(mode="after")
    def maxValue_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element( 
            self,
            field_types=[Date, DateTime, Instant, Time, Decimal, Integer, Integer64, PositiveInt, UnsignedInt, Quantity],
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
            expression="binding.empty() or type.code.empty() or type.code.contains(\":\") or type.select((code = 'code') or (code = 'Coding') or (code='CodeableConcept') or (code = 'Quantity') or (code = 'string') or (code = 'uri') or (code = 'Duration')).exists()",
            human="Binding can only be present for coded elements, string, and uri if using FHIR-defined types",
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
            human="sliceName must be composed of proper tokens separated by \"/\"",
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
            expression="path.matches('^[^\\s\\.,:;\\\'\"\\/|?!@#$%&*()\\[\\]{}]{1,64}(\\.[^\\s\\.,:;\\\'\"\\/|?!@#$%&*()\\[\\]{}]{1,64}(\\[x\\])?(\\:[^\\s\\.]+)?)*$')",
            human="Element path SHALL be expressed as a set of '.'-separated components with each component restricted to a maximum of 64 characters and with some limits on the allowed choice of characters",
            key="eld-19",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_20_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="path.matches('^[A-Za-z][A-Za-z0-9]{0,63}(\\.[a-z][A-Za-z0-9]{0,63}(\\[x])?)*$')",
            human="The first component of the path should be UpperCamelCase.  Additional components (following a '.') should be lowerCamelCase.  If this syntax is not adhered to, code generation tools may be broken. Logical models may be less concerned about this implication.",
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

    @model_validator(mode="after")
    def FHIR_eld_24_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="fixed.exists().not()",
            human="pattern[x] should be used rather than fixed[x]",
            key="eld-24",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_eld_25_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="orderMeaning.empty() implies slicing.where(rules='openAtEnd' or ordered).exists().not()",
            human="Order has no meaning (and cannot be asserted to have meaning), so enforcing rules on order is improper",
            key="eld-25",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_eld_27_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="mapping.select(identity).isDistinct()",
            human="Mappings SHOULD be unique by key",
            key="eld-27",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_eld_28_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="mustHaveValue.value implies valueAlternatives.empty()",
            human="Can't have valueAlternatives if mustHaveValue is true",
            key="eld-28",
            severity="error",
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

 
 
class Expression(DataType):
    """
    An expression that can be used to generate a value
    """
    description: typing.Optional[String] = Field(
        description="Natural language description of the condition",
        default=None,
    )
    description_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    name: typing.Optional[Code] = Field(
        description="Short name assigned to expression for reuse",
        default=None,
    )
    name_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    language: typing.Optional[Code] = Field(
        description="text/cql | text/fhirpath | application/x-fhir-query | etc.",
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
    @field_validator(*('reference', 'expression', 'language', 'name', 'description', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def FHIR_exp_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="expression.exists() or reference.exists()",
            human="An expression or a reference must be provided",
            key="exp-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exp_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="name.hasValue() implies name.matches('[A-Za-z][A-Za-z0-9\\_]{0,63}')",
            human="The name must be a valid variable name in most computer languages",
            key="exp-2",
            severity="error",
        )


 
 
class ExtendedContactDetail(DataType):
    """
    Contact information
    """
    purpose: typing.Optional[CodeableConcept] = Field(
        description="The type of contact",
        default=None,
    )
    name: typing.Optional[typing.List["HumanName"]] = Field(
        description="Name of an individual to contact",
        default=None,
    )
    telecom: typing.Optional[typing.List[ContactPoint]] = Field(
        description="Contact details (e.g.phone/fax/url)",
        default=None,
    )
    address: typing.Optional[Address] = Field(
        description="Address for the contact",
        default=None,
    )
    organization: typing.Optional["Reference"] = Field(
        description="This contact detail is handled/monitored by a specific organization",
        default=None,
    )
    period: typing.Optional["Period"] = Field(
        description="Period that this contact was valid for usage",
        default=None,
    )
    @field_validator(*('period', 'organization', 'address', 'telecom', 'name', 'purpose', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Extension(DataType):
    """
    Optional Extensions Element
    """
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
    valueInteger64: typing.Optional[Integer64] = Field(
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
    valueAddress: typing.Optional[Address] = Field(
        description="Value of extension",
        default=None,
    )
    valueAge: typing.Optional[Age] = Field(
        description="Value of extension",
        default=None,
    )
    valueAnnotation: typing.Optional[Annotation] = Field(
        description="Value of extension",
        default=None,
    )
    valueAttachment: typing.Optional[Attachment] = Field(
        description="Value of extension",
        default=None,
    )
    valueCodeableConcept: typing.Optional[CodeableConcept] = Field(
        description="Value of extension",
        default=None,
    )
    valueCodeableReference: typing.Optional[CodeableReference] = Field(
        description="Value of extension",
        default=None,
    )
    valueCoding: typing.Optional[Coding] = Field(
        description="Value of extension",
        default=None,
    )
    valueContactPoint: typing.Optional[ContactPoint] = Field(
        description="Value of extension",
        default=None,
    )
    valueCount: typing.Optional[Count] = Field(
        description="Value of extension",
        default=None,
    )
    valueDistance: typing.Optional[Distance] = Field(
        description="Value of extension",
        default=None,
    )
    valueDuration: typing.Optional[Duration] = Field(
        description="Value of extension",
        default=None,
    )
    valueHumanName: typing.Optional["HumanName"] = Field(
        description="Value of extension",
        default=None,
    )
    valueIdentifier: typing.Optional["Identifier"] = Field(
        description="Value of extension",
        default=None,
    )
    valueMoney: typing.Optional["Money"] = Field(
        description="Value of extension",
        default=None,
    )
    valuePeriod: typing.Optional["Period"] = Field(
        description="Value of extension",
        default=None,
    )
    valueQuantity: typing.Optional["Quantity"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRange: typing.Optional["Range"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRatio: typing.Optional["Ratio"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRatioRange: typing.Optional["RatioRange"] = Field(
        description="Value of extension",
        default=None,
    )
    valueReference: typing.Optional["Reference"] = Field(
        description="Value of extension",
        default=None,
    )
    valueSampledData: typing.Optional["SampledData"] = Field(
        description="Value of extension",
        default=None,
    )
    valueSignature: typing.Optional["Signature"] = Field(
        description="Value of extension",
        default=None,
    )
    valueTiming: typing.Optional["Timing"] = Field(
        description="Value of extension",
        default=None,
    )
    valueContactDetail: typing.Optional[ContactDetail] = Field(
        description="Value of extension",
        default=None,
    )
    valueDataRequirement: typing.Optional[DataRequirement] = Field(
        description="Value of extension",
        default=None,
    )
    valueExpression: typing.Optional[Expression] = Field(
        description="Value of extension",
        default=None,
    )
    valueParameterDefinition: typing.Optional["ParameterDefinition"] = Field(
        description="Value of extension",
        default=None,
    )
    valueRelatedArtifact: typing.Optional["RelatedArtifact"] = Field(
        description="Value of extension",
        default=None,
    )
    valueTriggerDefinition: typing.Optional["TriggerDefinition"] = Field(
        description="Value of extension",
        default=None,
    )
    valueUsageContext: typing.Optional["UsageContext"] = Field(
        description="Value of extension",
        default=None,
    )
    valueAvailability: typing.Optional['Availability'] = Field(
        description="Value of extension",
        default=None,
    )
    valueExtendedContactDetail: typing.Optional['ExtendedContactDetail'] = Field(
        description="Value of extension",
        default=None,
    )
    valueDosage: typing.Optional[Dosage] = Field(
        description="Value of extension",
        default=None,
    )
    valueMeta: typing.Optional["Meta"] = Field(
        description="Value of extension",
        default=None,
    )
    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element( 
            self,
            field_types=[Base64Binary, Boolean, Canonical, Code, Date, DateTime, Decimal, Id, Instant, Integer, Integer64, Markdown, Oid, PositiveInt, String, Time, UnsignedInt, Uri, Url, Uuid, Address, Age, Annotation, Attachment, CodeableConcept, CodeableReference, Coding, ContactPoint, Count, Distance, Duration, HumanName, Identifier, Money, Period, Quantity, Range, Ratio, RatioRange, Reference, SampledData, Signature, Timing, ContactDetail, DataRequirement, Expression, ParameterDefinition, RelatedArtifact, TriggerDefinition, UsageContext, 'Availability', 'ExtendedContactDetail', Dosage, Meta],
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
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="value",
        )

 
 
class HumanName(DataType):
    """
    Name of a human or other living entity - parts and usage
    """
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
    period: typing.Optional["Period"] = Field(
        description="Time period when name was/is in use",
        default=None,
    )
    @field_validator(*('period', 'suffix', 'prefix', 'given', 'family', 'text', 'use', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Identifier(DataType):
    """
    An identifier intended for computation
    """
    use: typing.Optional[Code] = Field(
        description="usual | official | temp | secondary | old (If known)",
        default=None,
    )
    use_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    type: typing.Optional[CodeableConcept] = Field(
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
    period: typing.Optional["Period"] = Field(
        description="Time period when id is/was valid for use",
        default=None,
    )
    assigner: typing.Optional["Reference"] = Field(
        description="Organization that issued id (may be just text)",
        default=None,
    )
    @field_validator(*('assigner', 'period', 'value', 'system', 'type', 'use', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def FHIR_ident_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="value.exists()",
            human="Identifier with no value has limited utility.  If communicating that an identifier value has been suppressed or missing, the value element SHOULD be present with an extension indicating the missing semantic - e.g. data-absent-reason",
            key="ident-1",
            severity="warning",
        )


 
 
class MarketingStatus(BackboneType):
    """
    The marketing status describes the date when a medicinal product is actually put on the market or the date as of which it is no longer available
    """
    country: typing.Optional[CodeableConcept] = Field(
        description="The country in which the marketing authorization has been granted shall be specified It should be specified using the ISO 3166 \u2011 1 alpha-2 code elements",
        default=None,
    )
    jurisdiction: typing.Optional[CodeableConcept] = Field(
        description="Where a Medicines Regulatory Agency has granted a marketing authorization for which specific provisions within a jurisdiction apply, the jurisdiction can be specified using an appropriate controlled terminology The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
    status: CodeableConcept = Field(
        description="This attribute provides information on the status of the marketing of the medicinal product See ISO/TS 20443 for more information and examples",
        default=None,
    )
    dateRange: typing.Optional["Period"] = Field(
        description="The date when the Medicinal Product is placed on the market by the Marketing Authorization Holder (or where applicable, the manufacturer/distributor) in a country and/or jurisdiction shall be provided A complete date consisting of day, month and year shall be specified using the ISO 8601 date format NOTE \u201cPlaced on the market\u201d refers to the release of the Medicinal Product into the distribution chain",
        default=None,
    )
    restoreDate: typing.Optional[DateTime] = Field(
        description="The date when the Medicinal Product is placed on the market by the Marketing Authorization Holder (or where applicable, the manufacturer/distributor) in a country and/or jurisdiction shall be provided A complete date consisting of day, month and year shall be specified using the ISO 8601 date format NOTE \u201cPlaced on the market\u201d refers to the release of the Medicinal Product into the distribution chain",
        default=None,
    )
    restoreDate_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for restoreDate extensions",
        default=None,
        alias="_restoreDate",
    )
    @field_validator(*('restoreDate', 'dateRange', 'status', 'jurisdiction', 'country', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Meta(DataType):
    """
    Metadata about a resource
    """
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
    security: typing.Optional[typing.List[Coding]] = Field(
        description="Security Labels applied to this resource",
        default=None,
    )
    tag: typing.Optional[typing.List[Coding]] = Field(
        description="Tags applied to this resource",
        default=None,
    )
    @field_validator(*('tag', 'security', 'profile', 'source', 'lastUpdated', 'versionId', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class MonetaryComponent(DataType):
    """
    Availability data for an {item}
    """
    type: Code = Field(
        description="base | surcharge | deduction | discount | tax | informational",
        default=None,
    )
    type_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    code: typing.Optional[CodeableConcept] = Field(
        description="Codes may be used to differentiate between kinds of taxes, surcharges, discounts etc.",
        default=None,
    )
    factor: typing.Optional[Decimal] = Field(
        description="Factor used for calculating this component",
        default=None,
    )
    factor_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for factor extensions",
        default=None,
        alias="_factor",
    )
    amount: typing.Optional["Money"] = Field(
        description="Explicit value amount to be used",
        default=None,
    )
    @field_validator(*('amount', 'factor', 'code', 'type', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Money(DataType):
    """
    An amount of economic utility in some recognized currency
    """
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
    @field_validator(*('currency', 'value', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Narrative(DataType):
    """
    Human-readable summary of the resource (essential clinical and business information)
    """
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
    @field_validator(*('div', 'status', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @field_validator(*('div',), mode="after", check_fields=None)
    @classmethod
    def FHIR_txt_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="htmlChecks()",
            human="The narrative SHALL contain only the basic html formatting elements and attributes described in chapters 7-11 (except section 4 of chapter 9) and 15 of the HTML 4.0 standard, <a> elements (either name or href), images and internally contained style attributes",
            key="txt-1",
            severity="error",
        )

    @field_validator(*('div',), mode="after", check_fields=None)
    @classmethod
    def FHIR_txt_2_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="htmlChecks()",
            human="The narrative SHALL have some non-whitespace content",
            key="txt-2",
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


 
 
class ParameterDefinition(DataType):
    """
    Definition of a parameter to a module
    """
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
    @field_validator(*('profile', 'type', 'documentation', 'max', 'min', 'use', 'name', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Period(DataType):
    """
    Time range defined by start and end date/time
    """
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
    @field_validator(*('end', 'start', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def FHIR_per_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="start.hasValue().not() or end.hasValue().not() or (start.lowBoundary() <= end.highBoundary())",
            human="If present, start SHALL have a lower or equal value than end",
            key="per-1",
            severity="error",
        )


 
 
class PrimitiveType(DataType):
    """
    Parent type for DataTypes with a simple value
    """
    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class ProductShelfLife(BackboneType):
    """
    The shelf-life and storage information for a medicinal product item or container can be described using this class
    """
    type: typing.Optional[CodeableConcept] = Field(
        description="This describes the shelf life, taking into account various scenarios such as shelf life of the packaged Medicinal Product itself, shelf life after transformation where necessary and shelf life after the first opening of a bottle, etc. The shelf life type shall be specified using an appropriate controlled vocabulary The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
    periodDuration: typing.Optional[Duration] = Field(
        description="The shelf life time period can be specified using a numerical value for the period of time and its unit of time measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    periodString: typing.Optional[String] = Field(
        description="The shelf life time period can be specified using a numerical value for the period of time and its unit of time measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    specialPrecautionsForStorage: typing.Optional[typing.List[CodeableConcept]] = Field(
        description="Special precautions for storage, if any, can be specified using an appropriate controlled vocabulary The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
    @field_validator(*('specialPrecautionsForStorage', 'type', 'modifierExtension', 'extension', 'modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def period_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element( 
            self,
            field_types=[Duration, String],
            field_name_base="period",
        )

    @property 
    def period(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="period",
        )

 
 
class Quantity(DataType):
    """
    A measured or measurable amount
    """
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
        description="\u003c | \u003c= | \u003e= | \u003e | ad - how to understand the value",
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
    @field_validator(*('code', 'system', 'unit', 'comparator', 'value', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def FHIR_qty_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="code.empty() or system.exists()",
            human="If a code for the unit is present, the system SHALL also be present",
            key="qty-3",
            severity="error",
        )


 
 
class Range(DataType):
    """
    Set of values bounded by low and high
    """
    low: typing.Optional[Quantity] = Field(
        description="Low limit",
        default=None,
    )
    high: typing.Optional[Quantity] = Field(
        description="High limit",
        default=None,
    )
    @field_validator(*('high', 'low', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def FHIR_rng_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="low.value.empty() or high.value.empty() or low.lowBoundary().comparable(high.highBoundary()).not() or (low.lowBoundary() <= high.highBoundary())",
            human="If present, low SHALL have a lower value than high",
            key="rng-2",
            severity="error",
        )


 
 
class Ratio(DataType):
    """
    A ratio of two Quantity values - a numerator and a denominator
    """
    numerator: typing.Optional[Quantity] = Field(
        description="Numerator value",
        default=None,
    )
    denominator: typing.Optional[Quantity] = Field(
        description="Denominator value",
        default=None,
    )
    @field_validator(*('denominator', 'numerator', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def FHIR_rat_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="(numerator.exists() and denominator.exists()) or (numerator.empty() and denominator.empty() and extension.exists())",
            human="Numerator and denominator SHALL both be present, or both are absent. If both are absent, there SHALL be some extension present",
            key="rat-1",
            severity="error",
        )


 
 
class RatioRange(DataType):
    """
    Range of ratio values
    """
    lowNumerator: typing.Optional[Quantity] = Field(
        description="Low Numerator limit",
        default=None,
    )
    highNumerator: typing.Optional[Quantity] = Field(
        description="High Numerator limit",
        default=None,
    )
    denominator: typing.Optional[Quantity] = Field(
        description="Denominator value",
        default=None,
    )
    @field_validator(*('denominator', 'highNumerator', 'lowNumerator', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def FHIR_ratrng_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="((lowNumerator.exists() or highNumerator.exists()) and denominator.exists()) or (lowNumerator.empty() and highNumerator.empty() and denominator.empty() and extension.exists())",
            human="One of lowNumerator or highNumerator and denominator SHALL be present, or all are absent. If all are absent, there SHALL be some extension present",
            key="ratrng-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ratrng_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="lowNumerator.hasValue().not() or highNumerator.hasValue().not()  or (lowNumerator.lowBoundary() <= highNumerator.highBoundary())",
            human="If present, lowNumerator SHALL have a lower value than highNumerator",
            key="ratrng-2",
            severity="error",
        )


 
 
class Reference(DataType):
    """
    A reference from one resource to another
    """
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
        description="Type the reference refers to (e.g. \"Patient\") - must be a resource in resources",
        default=None,
    )
    type_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    identifier: typing.Optional[Identifier] = Field(
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
    @field_validator(*('display', 'identifier', 'type', 'reference', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def FHIR_ref_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="reference.exists()  implies (reference.startsWith('#').not() or (reference.substring(1).trace('url') in %rootResource.contained.id.trace('ids')) or (reference='#' and %rootResource!=%resource))",
            human="SHALL have a contained resource if a local reference is provided",
            key="ref-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ref_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="reference.exists() or identifier.exists() or display.exists() or extension.exists()",
            human="At least one of reference, identifier and display SHALL be present (unless an extension is provided).",
            key="ref-2",
            severity="error",
        )


 
 
class RelatedArtifact(DataType):
    """
    Related artifacts for a knowledge resource
    """
    type: Code = Field(
        description="documentation | justification | citation | predecessor | successor | derived-from | depends-on | composed-of | part-of | amends | amended-with | appends | appended-with | cites | cited-by | comments-on | comment-in | contains | contained-in | corrects | correction-in | replaces | replaced-with | retracts | retracted-by | signs | similar-to | supports | supported-with | transforms | transformed-into | transformed-with | documents | specification-of | created-with | cite-as",
        default=None,
    )
    type_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    classifier: typing.Optional[typing.List[CodeableConcept]] = Field(
        description="Additional classifiers",
        default=None,
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
    document: typing.Optional[Attachment] = Field(
        description="What document is being referenced",
        default=None,
    )
    resource: typing.Optional[Canonical] = Field(
        description="What artifact is being referenced",
        default=None,
    )
    resource_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for resource extensions",
        default=None,
        alias="_resource",
    )
    resourceReference: typing.Optional[Reference] = Field(
        description="What artifact, if not a conformance resource",
        default=None,
    )
    publicationStatus: typing.Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    publicationStatus_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for publicationStatus extensions",
        default=None,
        alias="_publicationStatus",
    )
    publicationDate: typing.Optional[Date] = Field(
        description="Date of publication of the artifact being referred to",
        default=None,
    )
    publicationDate_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for publicationDate extensions",
        default=None,
        alias="_publicationDate",
    )
    @field_validator(*('publicationDate', 'publicationStatus', 'resourceReference', 'resource', 'document', 'citation', 'display', 'label', 'classifier', 'type', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class SampledData(DataType):
    """
    A series of measurements taken by a device
    """
    origin: Quantity = Field(
        description="Zero value and units",
        default=None,
    )
    interval: typing.Optional[Decimal] = Field(
        description="Number of intervalUnits between samples",
        default=None,
    )
    interval_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for interval extensions",
        default=None,
        alias="_interval",
    )
    intervalUnit: Code = Field(
        description="The measurement unit of the interval between samples",
        default=None,
    )
    intervalUnit_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for intervalUnit extensions",
        default=None,
        alias="_intervalUnit",
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
    codeMap: typing.Optional[Canonical] = Field(
        description="Defines the codes used in the data",
        default=None,
    )
    codeMap_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for codeMap extensions",
        default=None,
        alias="_codeMap",
    )
    offsets: typing.Optional[String] = Field(
        description="Offsets, typically in time, at which data values were taken",
        default=None,
    )
    offsets_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for offsets extensions",
        default=None,
        alias="_offsets",
    )
    data: typing.Optional[String] = Field(
        description="Decimal values with spaces, or \"E\" | \"U\" | \"L\", or another code",
        default=None,
    )
    data_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )
    @field_validator(*('data', 'offsets', 'codeMap', 'dimensions', 'upperLimit', 'lowerLimit', 'factor', 'intervalUnit', 'interval', 'origin', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def FHIR_sdd_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="interval.exists().not() xor offsets.exists().not()",
            human="A SampledData SAHLL have either an interval and offsets but not both",
            key="sdd-1",
            severity="error",
        )


 
 
class Signature(DataType):
    """
    A Signature - XML DigSig, JWS, Graphical image of signature, etc.
    """
    type: typing.Optional[typing.List[Coding]] = Field(
        description="Indication of the reason the entity signed the object(s)",
        default=None,
    )
    when: typing.Optional[Instant] = Field(
        description="When the signature was created",
        default=None,
    )
    when_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for when extensions",
        default=None,
        alias="_when",
    )
    who: typing.Optional[Reference] = Field(
        description="Who signed",
        default=None,
    )
    onBehalfOf: typing.Optional[Reference] = Field(
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
    @field_validator(*('data', 'sigFormat', 'targetFormat', 'onBehalfOf', 'who', 'when', 'type', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Timing(BackboneType):
    """
    A timing schedule that specifies an event that may occur multiple times
    """
    event: typing.Optional[typing.List[DateTime]] = Field(
        description="When the event occurs",
        default=None,
    )
    event_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for event extensions",
        default=None,
        alias="_event",
    )
    repeat: typing.Optional["Element"] = Field(
        description="When the event is to occur",
        default=None,
    )
    code: typing.Optional[CodeableConcept] = Field(
        description="C | BID | TID | QID | AM | PM | QD | QOD | +",
        default=None,
    )
    @field_validator(*('code', 'repeat', 'event', 'modifierExtension', 'extension', 'modifierExtension', 'extension', 'modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="duration.empty() or durationUnit.exists()",
            human="if there's a duration, there needs to be duration units",
            key="tim-1",
            severity="error",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_2_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="period.empty() or periodUnit.exists()",
            human="if there's a period, there needs to be period units",
            key="tim-2",
            severity="error",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_4_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="duration.exists() implies duration >= 0",
            human="duration SHALL be a non-negative value",
            key="tim-4",
            severity="error",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_5_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="period.exists() implies period >= 0",
            human="period SHALL be a non-negative value",
            key="tim-5",
            severity="error",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_6_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="periodMax.empty() or period.exists()",
            human="If there's a periodMax, there must be a period",
            key="tim-6",
            severity="error",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_7_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="durationMax.empty() or duration.exists()",
            human="If there's a durationMax, there must be a duration",
            key="tim-7",
            severity="error",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_8_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="countMax.empty() or count.exists()",
            human="If there's a countMax, there must be a count",
            key="tim-8",
            severity="error",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_9_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="offset.empty() or (when.exists() and when.select($this in ('C' | 'CM' | 'CD' | 'CV')).allFalse())",
            human="If there's an offset, there must be a when (and not C, CM, CD, CV)",
            key="tim-9",
            severity="error",
        )

    @field_validator(*('repeat',), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_10_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class TriggerDefinition(DataType):
    """
    Defines an expected trigger for a module
    """
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
    code: typing.Optional[CodeableConcept] = Field(
        description="Coded definition of the event",
        default=None,
    )
    subscriptionTopic: typing.Optional[Canonical] = Field(
        description="What event",
        default=None,
    )
    subscriptionTopic_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for subscriptionTopic extensions",
        default=None,
        alias="_subscriptionTopic",
    )
    timingTiming: typing.Optional[Timing] = Field(
        description="Timing of the event",
        default=None,
    )
    timingReference: typing.Optional[Reference] = Field(
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
    data: typing.Optional[typing.List[DataRequirement]] = Field(
        description="Triggering data of the event (multiple = \u0027and\u0027)",
        default=None,
    )
    condition: typing.Optional[Expression] = Field(
        description="Whether the event triggers (boolean expression)",
        default=None,
    )
    @field_validator(*('condition', 'data', 'subscriptionTopic', 'code', 'name', 'type', 'extension', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def timing_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element( 
            self,
            field_types=[Timing, Reference, Date, DateTime],
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
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="timing",
        )

 
 
class UsageContext(DataType):
    """
    Describes the context of use for a conformance or knowledge resource
    """
    code: Coding = Field(
        description="Type of context being specified",
        default=None,
    )
    valueCodeableConcept: CodeableConcept = Field(
        description="Value that defines the context",
        default=None,
    )
    valueQuantity: Quantity = Field(
        description="Value that defines the context",
        default=None,
    )
    valueRange: Range = Field(
        description="Value that defines the context",
        default=None,
    )
    valueReference: Reference = Field(
        description="Value that defines the context",
        default=None,
    )
    @field_validator(*('code', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element( 
            self,
            field_types=[CodeableConcept, Quantity, Range, Reference],
            field_name_base="value",
        )

    @property 
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="value",
        )

 
 
class VirtualServiceDetail(DataType):
    """
    Virtual Service Contact Details
    """
    channelType: typing.Optional[Coding] = Field(
        description="Channel Type",
        default=None,
    )
    addressUrl: typing.Optional[Url] = Field(
        description="Contact address/number",
        default=None,
    )
    addressString: typing.Optional[String] = Field(
        description="Contact address/number",
        default=None,
    )
    addressContactPoint: typing.Optional[ContactPoint] = Field(
        description="Contact address/number",
        default=None,
    )
    addressExtendedContactDetail: typing.Optional['ExtendedContactDetail'] = Field(
        description="Contact address/number",
        default=None,
    )
    additionalInfo: typing.Optional[typing.List[Url]] = Field(
        description="Address to see alternative connection details",
        default=None,
    )
    additionalInfo_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for additionalInfo extensions",
        default=None,
        alias="_additionalInfo",
    )
    maxParticipants: typing.Optional[PositiveInt] = Field(
        description="Maximum number of participants supported by the virtual service",
        default=None,
    )
    maxParticipants_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for maxParticipants extensions",
        default=None,
        alias="_maxParticipants",
    )
    sessionKey: typing.Optional[String] = Field(
        description="Session Key required by the virtual service",
        default=None,
    )
    sessionKey_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for sessionKey extensions",
        default=None,
        alias="_sessionKey",
    )
    @field_validator(*('sessionKey', 'maxParticipants', 'additionalInfo', 'channelType', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def address_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element( 
            self,
            field_types=[Url, String, ContactPoint, 'ExtendedContactDetail'],
            field_name_base="address",
        )

    @property 
    def address(self):
        return fhir_validators.get_type_choice_value_by_base(self, 
            base="address",
        )

 
 
class MoneyQuantity(Quantity):
    """
    An amount of money. With regard to precision, see [Decimal Precision](datatypes.html#precision)
    """
    @field_validator(*('code', 'system', 'unit', 'comparator', 'value', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
    def FHIR_qty_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="code.empty() or system.exists()",
            human="If a code for the unit is present, the system SHALL also be present",
            key="qty-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_mtqy_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint( 
            self,
            expression="(code.exists() or value.empty()) and (system.empty() or system = 'urn:iso:std:iso:4217')",
            human="There SHALL be a code if there is a value and it SHALL be an expression of currency.  If system is present, it SHALL be ISO 4217 (system = \"urn:iso:std:iso:4217\" - currency).",
            key="mtqy-1",
            severity="error",
        )


 
 
class SimpleQuantity(Quantity):
    """
    A fixed quantity (no comparator)
    """
    @field_validator(*('code', 'system', 'unit', 'comparator', 'value', 'extension', 'extension', 'extension', 'extension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('extension',), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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


 
 
class Resource(Base):
    """
    Base Resource
    """
    id: typing.Optional[String] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    id_ext: typing.Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    meta: typing.Optional[Meta] = Field(
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
    @field_validator(*('language', 'implicitRules', 'meta'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
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


 
 
class DomainResource(Resource):
    """
    A resource with narrative, extensions, and contained resources
    """
    text: typing.Optional[Narrative] = Field(
        description="Text summary of the resource, for human interpretation",
        default=None,
    )
    contained: typing.Optional[typing.List[Resource]] = Field(
        description="Contained, inline Resources",
        default=None,
    )
    extension: typing.Optional[typing.List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: typing.Optional[typing.List["Extension"]] = Field(
        description="Extensions that cannot be ignored",
        default=None,
    )
    @field_validator(*('modifierExtension', 'extension', 'text', 'language', 'implicitRules', 'meta', 'language', 'implicitRules', 'meta', 'language', 'implicitRules', 'meta'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*('modifierExtension', 'extension'), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(cls, value, 
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
            expression="contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url))) or descendants().where(reference = '#').exists() or descendants().where(ofType(canonical) = '#').exists() or descendants().where(ofType(canonical) = '#').exists()).not()).trace('unmatched', id).empty()",
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




 
ElementDefinition.model_rebuild()
 
Extension.model_rebuild()
 
Narrative.model_rebuild()
 
VirtualServiceDetail.model_rebuild()