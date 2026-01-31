from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Canonical,
    Markdown,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    CodeableReference,
    Annotation,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class GenomicStudyAnalysisInput(BackboneElement):
    """
    Inputs for the analysis event.
    """

    file: Optional[Reference] = Field(
        description="File containing input data",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of input data (e.g., BAM, CRAM, or FASTA)",
        default=None,
    )
    generatedByIdentifier: Optional[Identifier] = Field(
        description="The analysis event or other GenomicStudy that generated this input file",
        default=None,
    )
    generatedByReference: Optional[Reference] = Field(
        description="The analysis event or other GenomicStudy that generated this input file",
        default=None,
    )

    @property
    def generatedBy(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="generatedBy",
        )

    @model_validator(mode="after")
    def generatedBy_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Identifier, Reference],
            field_name_base="generatedBy",
            required=False,
        )


class GenomicStudyAnalysisOutput(BackboneElement):
    """
    Outputs for the analysis event.
    """

    file: Optional[Reference] = Field(
        description="File containing output data",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of output data (e.g., VCF, MAF, or BAM)",
        default=None,
    )


class GenomicStudyAnalysisPerformer(BackboneElement):
    """
    Performer for the analysis event.
    """

    actor: Optional[Reference] = Field(
        description="The organization, healthcare professional, or others who participated in performing this analysis",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="Role of the actor for this analysis",
        default=None,
    )


class GenomicStudyAnalysisDevice(BackboneElement):
    """
    Devices used for the analysis (e.g., instruments, software), with settings and parameters.
    """

    device: Optional[Reference] = Field(
        description="Device used for the analysis",
        default=None,
    )
    function: Optional[CodeableConcept] = Field(
        description="Specific function for the device used for the analysis",
        default=None,
    )


class GenomicStudyAnalysis(BackboneElement):
    """
    The details about a specific analysis that was performed in this GenomicStudy.
    """

    identifier: Optional[List[Identifier]] = Field(
        description="Identifiers for the analysis event",
        default=None,
    )
    methodType: Optional[List[CodeableConcept]] = Field(
        description="Type of the methods used in the analysis (e.g., FISH, Karyotyping, MSI)",
        default=None,
    )
    changeType: Optional[List[CodeableConcept]] = Field(
        description="Type of the genomic changes studied in the analysis (e.g., DNA, RNA, or AA change)",
        default=None,
    )
    genomeBuild: Optional[CodeableConcept] = Field(
        description="Genome build that is used in this analysis",
        default=None,
    )
    instantiatesCanonical: Optional[Canonical] = Field(
        description="The defined protocol that describes the analysis",
        default=None,
    )
    instantiatesCanonical_ext: Optional[Element] = Field(
        description="Placeholder element for instantiatesCanonical extensions",
        default=None,
        alias="_instantiatesCanonical",
    )
    instantiatesUri: Optional[Uri] = Field(
        description="The URL pointing to an externally maintained protocol that describes the analysis",
        default=None,
    )
    instantiatesUri_ext: Optional[Element] = Field(
        description="Placeholder element for instantiatesUri extensions",
        default=None,
        alias="_instantiatesUri",
    )
    title: Optional[String] = Field(
        description="Name of the analysis event (human friendly)",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    focus: Optional[List[Reference]] = Field(
        description="What the genomic analysis is about, when it is not about the subject of record",
        default=None,
    )
    specimen: Optional[List[Reference]] = Field(
        description="The specimen used in the analysis event",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="The date of the analysis event",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    note: Optional[List[Annotation]] = Field(
        description="Any notes capture with the analysis event",
        default=None,
    )
    protocolPerformed: Optional[Reference] = Field(
        description="The protocol that was performed for the analysis event",
        default=None,
    )
    regionsStudied: Optional[List[Reference]] = Field(
        description="The genomic regions to be studied in the analysis (BED file)",
        default=None,
    )
    regionsCalled: Optional[List[Reference]] = Field(
        description="Genomic regions actually called in the analysis event (BED file)",
        default=None,
    )
    input: Optional[List[GenomicStudyAnalysisInput]] = Field(
        description="Inputs for the analysis event",
        default=None,
    )
    output: Optional[List[GenomicStudyAnalysisOutput]] = Field(
        description="Outputs for the analysis event",
        default=None,
    )
    performer: Optional[List[GenomicStudyAnalysisPerformer]] = Field(
        description="Performer for the analysis event",
        default=None,
    )
    device: Optional[List[GenomicStudyAnalysisDevice]] = Field(
        description="Devices used for the analysis (e.g., instruments, software), with settings and parameters",
        default=None,
    )


class GenomicStudy(DomainResource):
    """
    A set of analyses performed to analyze and generate genomic data.
    """

    _abstract = False
    _type = "GenomicStudy"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/GenomicStudy"

    identifier: Optional[List[Identifier]] = Field(
        description="Identifiers for this genomic study",
        default=None,
    )
    status: Optional[Code] = Field(
        description="registered | available | cancelled | entered-in-error | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    type: Optional[List[CodeableConcept]] = Field(
        description="The type of the study (e.g., Familial variant segregation, Functional variation detection, or Gene expression profiling)",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="The primary subject of the genomic study",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="The healthcare event with which this genomics study is associated",
        default=None,
    )
    startDate: Optional[DateTime] = Field(
        description="When the genomic study was started",
        default=None,
    )
    startDate_ext: Optional[Element] = Field(
        description="Placeholder element for startDate extensions",
        default=None,
        alias="_startDate",
    )
    basedOn: Optional[List[Reference]] = Field(
        description="Event resources that the genomic study is based on",
        default=None,
    )
    referrer: Optional[Reference] = Field(
        description="Healthcare professional who requested or referred the genomic study",
        default=None,
    )
    interpreter: Optional[List[Reference]] = Field(
        description="Healthcare professionals who interpreted the genomic study",
        default=None,
    )
    reason: Optional[List[CodeableReference]] = Field(
        description="Why the genomic study was performed",
        default=None,
    )
    instantiatesCanonical: Optional[Canonical] = Field(
        description="The defined protocol that describes the study",
        default=None,
    )
    instantiatesCanonical_ext: Optional[Element] = Field(
        description="Placeholder element for instantiatesCanonical extensions",
        default=None,
        alias="_instantiatesCanonical",
    )
    instantiatesUri: Optional[Uri] = Field(
        description="The URL pointing to an externally maintained protocol that describes the study",
        default=None,
    )
    instantiatesUri_ext: Optional[Element] = Field(
        description="Placeholder element for instantiatesUri extensions",
        default=None,
        alias="_instantiatesUri",
    )
    note: Optional[List[Annotation]] = Field(
        description="Comments related to the genomic study",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Description of the genomic study",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    analysis: Optional[List[GenomicStudyAnalysis]] = Field(
        description="Genomic Analysis Event",
        default=None,
    )
