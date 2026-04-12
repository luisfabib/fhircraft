import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    CodeableConcept,
    BackboneElement,
    Attachment,
    SubstanceAmount,
)
from .resource import Resource
from .domain_resource import DomainResource

class SubstancePolymerMonomerSetStartingMaterial(BackboneElement):
    """
    Todo.
    """

    material: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    isDefining: Optional[fhir.boolean] = Field(
        description="Todo",
        default=None,
    )
    amount: Optional[SubstanceAmount] = Field(
        description="Todo",
        default=None,
    )

class SubstancePolymerMonomerSet(BackboneElement):
    """
    Todo.
    """

    ratioType: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    startingMaterial: Optional[ListType[SubstancePolymerMonomerSetStartingMaterial]] = (
        Field(
            description="Todo",
            default=None,
        )
    )

class SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation(BackboneElement):
    """
    Todo.
    """

    degree: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    amount: Optional[SubstanceAmount] = Field(
        description="Todo",
        default=None,
    )

class SubstancePolymerRepeatRepeatUnitStructuralRepresentation(BackboneElement):
    """
    Todo.
    """

    type: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    representation: Optional[fhir.string] = Field(
        description="Todo",
        default=None,
    )
    attachment: Optional[Attachment] = Field(
        description="Todo",
        default=None,
    )

class SubstancePolymerRepeatRepeatUnit(BackboneElement):
    """
    Todo.
    """

    orientationOfPolymerisation: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    repeatUnit: Optional[fhir.string] = Field(
        description="Todo",
        default=None,
    )
    amount: Optional[SubstanceAmount] = Field(
        description="Todo",
        default=None,
    )
    degreeOfPolymerisation: Optional[
        ListType[SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation]
    ] = Field(
        description="Todo",
        default=None,
    )
    structuralRepresentation: Optional[
        ListType[SubstancePolymerRepeatRepeatUnitStructuralRepresentation]
    ] = Field(
        description="Todo",
        default=None,
    )

class SubstancePolymerRepeat(BackboneElement):
    """
    Todo.
    """

    numberOfUnits: Optional[fhir.integer] = Field(
        description="Todo",
        default=None,
    )
    averageMolecularFormula: Optional[fhir.string] = Field(
        description="Todo",
        default=None,
    )
    repeatUnitAmountType: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    repeatUnit: Optional[ListType[SubstancePolymerRepeatRepeatUnit]] = Field(
        description="Todo",
        default=None,
    )

class SubstancePolymer(DomainResource):
    """
    Todo.
    """

    _abstract = False
    _type = "SubstancePolymer"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SubstancePolymer"

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
    class_: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
        alias="class",
    )
    geometry: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    copolymerConnectivity: Optional[ListType[CodeableConcept]] = Field(
        description="Todo",
        default=None,
    )
    modification: Optional[ListType[fhir.string]] = Field(
        description="Todo",
        default=None,
    )
    monomerSet: Optional[ListType[SubstancePolymerMonomerSet]] = Field(
        description="Todo",
        default=None,
    )
    repeat: Optional[ListType[SubstancePolymerRepeat]] = Field(
        description="Todo",
        default=None,
    )
