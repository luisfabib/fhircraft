import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, Boolean

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Reference,
    Duration,
    Range,
)
from .resource import Resource
from .domain_resource import DomainResource


class SpecimenDefinitionTypeTestedContainerAdditive(BackboneElement):
    """
    Substance introduced in the kind of container to preserve, maintain or enhance the specimen. Examples: Formalin, Citrate, EDTA.
    """

    additiveCodeableConcept: Optional[CodeableConcept] = Field(
        description="Additive associated with container",
        default=None,
    )
    additiveReference: Optional[Reference] = Field(
        description="Additive associated with container",
        default=None,
    )

    @property
    def additive(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="additive",
        )

    @model_validator(mode="after")
    def additive_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="additive",
            required=True,
        )


class SpecimenDefinitionTypeTestedContainer(BackboneElement):
    """
    The specimen's container.
    """

    material: Optional[CodeableConcept] = Field(
        description="Container material",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Kind of container associated with the kind of specimen",
        default=None,
    )
    cap: Optional[CodeableConcept] = Field(
        description="Color of container cap",
        default=None,
    )
    description: Optional[String] = Field(
        description="Container description",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    capacity: Optional[Quantity] = Field(
        description="Container capacity",
        default=None,
    )
    minimumVolumeQuantity: Optional[Quantity] = Field(
        description="Minimum volume",
        default=None,
    )
    minimumVolumeString: Optional[String] = Field(
        description="Minimum volume",
        default=None,
    )
    minimumVolumeString_ext: Optional[Element] = Field(
        description="Placeholder element for minimumVolumeString extensions",
        default=None,
        alias="_minimumVolumeString",
    )
    additive: Optional[ListType[SpecimenDefinitionTypeTestedContainerAdditive]] = Field(
        description="Additive associated with container",
        default=None,
    )
    preparation: Optional[String] = Field(
        description="Specimen container preparation",
        default=None,
    )
    preparation_ext: Optional[Element] = Field(
        description="Placeholder element for preparation extensions",
        default=None,
        alias="_preparation",
    )

    @property
    def minimumVolume(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="minimumVolume",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "preparation",
                "additive",
                "capacity",
                "description",
                "cap",
                "type",
                "material",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def minimumVolume_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, String],
            field_name_base="minimumVolume",
            required=False,
        )


class SpecimenDefinitionTypeTestedHandling(BackboneElement):
    """
    Set of instructions for preservation/transport of the specimen at a defined temperature interval, prior the testing process.
    """

    temperatureQualifier: Optional[CodeableConcept] = Field(
        description="Temperature qualifier",
        default=None,
    )
    temperatureRange: Optional[Range] = Field(
        description="Temperature range",
        default=None,
    )
    maxDuration: Optional[Duration] = Field(
        description="Maximum preservation time",
        default=None,
    )
    instruction: Optional[String] = Field(
        description="Preservation instruction",
        default=None,
    )
    instruction_ext: Optional[Element] = Field(
        description="Placeholder element for instruction extensions",
        default=None,
        alias="_instruction",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "instruction",
                "maxDuration",
                "temperatureRange",
                "temperatureQualifier",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class SpecimenDefinitionTypeTested(BackboneElement):
    """
    Specimen conditioned in a container as expected by the testing laboratory.
    """

    isDerived: Optional[Boolean] = Field(
        description="Primary or secondary specimen",
        default=None,
    )
    isDerived_ext: Optional[Element] = Field(
        description="Placeholder element for isDerived extensions",
        default=None,
        alias="_isDerived",
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of intended specimen",
        default=None,
    )
    preference: Optional[Code] = Field(
        description="preferred | alternate",
        default=None,
    )
    preference_ext: Optional[Element] = Field(
        description="Placeholder element for preference extensions",
        default=None,
        alias="_preference",
    )
    container: Optional[SpecimenDefinitionTypeTestedContainer] = Field(
        description="The specimen\u0027s container",
        default=None,
    )
    requirement: Optional[String] = Field(
        description="Specimen requirements",
        default=None,
    )
    requirement_ext: Optional[Element] = Field(
        description="Placeholder element for requirement extensions",
        default=None,
        alias="_requirement",
    )
    retentionTime: Optional[Duration] = Field(
        description="Specimen retention time",
        default=None,
    )
    rejectionCriterion: Optional[ListType[CodeableConcept]] = Field(
        description="Rejection criterion",
        default=None,
    )
    handling: Optional[ListType[SpecimenDefinitionTypeTestedHandling]] = Field(
        description="Specimen handling before testing",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "handling",
                "rejectionCriterion",
                "retentionTime",
                "requirement",
                "container",
                "preference",
                "type",
                "isDerived",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class SpecimenDefinition(DomainResource):
    """
    A kind of specimen with associated set of requirements.
    """

    _abstract = False
    _type = "SpecimenDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SpecimenDefinition"

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
            profile=["http://hl7.org/fhir/StructureDefinition/SpecimenDefinition"]
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
    identifier: Optional[Identifier] = Field(
        description="Business identifier of a kind of specimen",
        default=None,
    )
    typeCollected: Optional[CodeableConcept] = Field(
        description="Kind of material to collect",
        default=None,
    )
    patientPreparation: Optional[ListType[CodeableConcept]] = Field(
        description="Patient preparation for collection",
        default=None,
    )
    timeAspect: Optional[String] = Field(
        description="Time aspect for collection",
        default=None,
    )
    timeAspect_ext: Optional[Element] = Field(
        description="Placeholder element for timeAspect extensions",
        default=None,
        alias="_timeAspect",
    )
    collection: Optional[ListType[CodeableConcept]] = Field(
        description="Specimen collection procedure",
        default=None,
    )
    typeTested: Optional[ListType[SpecimenDefinitionTypeTested]] = Field(
        description="Specimen in container intended for testing by lab",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "typeTested",
                "collection",
                "timeAspect",
                "patientPreparation",
                "typeCollected",
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
