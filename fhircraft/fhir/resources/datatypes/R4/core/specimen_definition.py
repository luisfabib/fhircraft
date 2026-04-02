import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

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
    additive: Optional[ListType[SpecimenDefinitionTypeTestedContainerAdditive]] = Field(
        description="Additive associated with container",
        default=None,
    )
    preparation: Optional[String] = Field(
        description="Specimen container preparation",
        default=None,
    )

    @property
    def minimumVolume(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="minimumVolume",
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

class SpecimenDefinitionTypeTested(BackboneElement):
    """
    Specimen conditioned in a container as expected by the testing laboratory.
    """

    isDerived: Optional[Boolean] = Field(
        description="Primary or secondary specimen",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of intended specimen",
        default=None,
    )
    preference: Optional[Code] = Field(
        description="preferred | alternate",
        default=None,
    )
    container: Optional[SpecimenDefinitionTypeTestedContainer] = Field(
        description="The specimen\u0027s container",
        default=None,
    )
    requirement: Optional[String] = Field(
        description="Specimen requirements",
        default=None,
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

class SpecimenDefinition(DomainResource):
    """
    A kind of specimen with associated set of requirements.
    """

    _abstract = False
    _type = "SpecimenDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SpecimenDefinition"

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
    collection: Optional[ListType[CodeableConcept]] = Field(
        description="Specimen collection procedure",
        default=None,
    )
    typeTested: Optional[ListType[SpecimenDefinitionTypeTested]] = Field(
        description="Specimen in container intended for testing by lab",
        default=None,
    )
