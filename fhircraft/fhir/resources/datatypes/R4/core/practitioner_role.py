import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Boolean,
    Time,
)

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Period,
    Reference,
    CodeableConcept,
    BackboneElement,
    ContactPoint,
)
from .resource import Resource
from .domain_resource import DomainResource


class PractitionerRoleAvailableTime(BackboneElement):
    """
    A collection of times the practitioner is available or performing this role at the location and/or healthcareservice.
    """

    daysOfWeek: Optional[ListType[Code]] = Field(
        description="mon | tue | wed | thu | fri | sat | sun",
        default=None,
    )
    daysOfWeek_ext: Optional[Element] = Field(
        description="Placeholder element for daysOfWeek extensions",
        default=None,
        alias="_daysOfWeek",
    )
    allDay: Optional[Boolean] = Field(
        description="Always available? e.g. 24 hour service",
        default=None,
    )
    allDay_ext: Optional[Element] = Field(
        description="Placeholder element for allDay extensions",
        default=None,
        alias="_allDay",
    )
    availableStartTime: Optional[Time] = Field(
        description="Opening time of day (ignored if allDay = true)",
        default=None,
    )
    availableStartTime_ext: Optional[Element] = Field(
        description="Placeholder element for availableStartTime extensions",
        default=None,
        alias="_availableStartTime",
    )
    availableEndTime: Optional[Time] = Field(
        description="Closing time of day (ignored if allDay = true)",
        default=None,
    )
    availableEndTime_ext: Optional[Element] = Field(
        description="Placeholder element for availableEndTime extensions",
        default=None,
        alias="_availableEndTime",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "availableEndTime",
                "availableStartTime",
                "allDay",
                "daysOfWeek",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class PractitionerRoleNotAvailable(BackboneElement):
    """
    The practitioner is not available or performing this role during this period of time due to the provided reason.
    """

    description: Optional[String] = Field(
        description="Reason presented to the user explaining why time not available",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    during: Optional[Period] = Field(
        description="Service not available from this date",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "during",
                "description",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class PractitionerRole(DomainResource):
    """
    A specific set of Roles/Locations/specialties/services that a practitioner may perform at an organization for a period of time.
    """

    _abstract = False
    _type = "PractitionerRole"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/PractitionerRole"

    id: Optional[String] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    id_ext: Optional[Element] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    meta: Optional[Meta] = Field(
        description="Metadata about the resource.",
        default_factory=lambda: Meta(
            profile=["http://hl7.org/fhir/StructureDefinition/PractitionerRole"]
        ),
    )
    implicitRules: Optional[Uri] = Field(
        description="A set of rules under which this content was created",
        default=None,
    )
    implicitRules_ext: Optional[Element] = Field(
        description="Placeholder element for implicitRules extensions",
        default=None,
        alias="_implicitRules",
    )
    language: Optional[Code] = Field(
        description="Language of the resource content",
        default=None,
    )
    language_ext: Optional[Element] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    text: Optional[Narrative] = Field(
        description="Text summary of the resource, for human interpretation",
        default=None,
    )
    contained: Optional[ListType[Resource]] = Field(
        description="Contained, inline Resources",
        default=None,
    )
    extension: Optional[ListType[Extension]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: Optional[ListType[Extension]] = Field(
        description="Extensions that cannot be ignored",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifiers that are specific to a role/location",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this practitioner role record is in active use",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
    )
    period: Optional[Period] = Field(
        description="The period during which the practitioner is authorized to perform in these role(s)",
        default=None,
    )
    practitioner: Optional[Reference] = Field(
        description="Practitioner that is able to provide the defined services for the organization",
        default=None,
    )
    organization: Optional[Reference] = Field(
        description="Organization where the roles are available",
        default=None,
    )
    code: Optional[ListType[CodeableConcept]] = Field(
        description="Roles which this practitioner may perform",
        default=None,
    )
    specialty: Optional[ListType[CodeableConcept]] = Field(
        description="Specific specialty of the practitioner",
        default=None,
    )
    location: Optional[ListType[Reference]] = Field(
        description="The location(s) at which this practitioner provides care",
        default=None,
    )
    healthcareService: Optional[ListType[Reference]] = Field(
        description="The list of healthcare services that this worker provides for this role\u0027s Organization/Location(s)",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="Contact details that are specific to the role/location/service",
        default=None,
    )
    availableTime: Optional[ListType[PractitionerRoleAvailableTime]] = Field(
        description="Times the Service Site is available",
        default=None,
    )
    notAvailable: Optional[ListType[PractitionerRoleNotAvailable]] = Field(
        description="Not available during this time due to provided reason",
        default=None,
    )
    availabilityExceptions: Optional[String] = Field(
        description="Description of availability exceptions",
        default=None,
    )
    availabilityExceptions_ext: Optional[Element] = Field(
        description="Placeholder element for availabilityExceptions extensions",
        default=None,
        alias="_availabilityExceptions",
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Technical endpoints providing access to services operated for the practitioner with this role",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "endpoint",
                "availabilityExceptions",
                "notAvailable",
                "availableTime",
                "telecom",
                "healthcareService",
                "location",
                "specialty",
                "code",
                "organization",
                "practitioner",
                "period",
                "active",
                "identifier",
                "modifierExtension",
                "extension",
                "text",
                "language",
                "implicitRules",
                "meta",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "modifierExtension",
                "extension",
            ),
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
            expression="contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url))) or descendants().where(reference = '#').exists() or descendants().where(as(canonical) = '#').exists() or descendants().where(as(canonical) = '#').exists()).not()).trace('unmatched', id).empty()",
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
