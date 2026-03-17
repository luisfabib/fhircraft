import pytest
from fhircraft.fhir.resources.factory import FHIRModelFactory
from fhircraft.fhir.resources.generator import CodeGenerator


def _normalize(s):
    import re

    return re.sub(r"\s+", " ", s.strip())


def assertBlockInCode(code, expected_block):
    # Generate source code
    # Assert code block (normalized)
    norm_expected = _normalize(expected_block)
    norm_code = _normalize(code)
    assert (
        norm_expected in norm_code
    ), f"Expected block not found in generated code.\n\nExpected:\n{expected_block}\n\nGot:\n{code}"


@pytest.fixture
def generator():

    generator = CodeGenerator()
    yield generator


@pytest.fixture
def factory():

    factory = FHIRModelFactory(fhir_release="R5")
    yield factory
    factory.reset_cache()


def test_regression_issue_255(factory):
    """Regression test for issue #255: nested slice with fixed values on a backbone element.

    Verifies the assembled model structure directly without relying on the
    generated source-code string, which is fragile to cosmetic changes.
    """
    from typing import get_args, get_origin, Union
    import pydantic

    from fhircraft.fhir.resources.base import FHIRSliceModel

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "issue-255",
        "url": "http://example.org/fhir/StructureDefinition/issue-255",
        "version": "5.0.0",
        "name": "ProfileExample",
        "title": "Example Profile",
        "status": "draft",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Observation",
        "derivation": "constraint",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
        "differential": {
            "element": [
                {
                    "id": "Observation",
                    "path": "Observation",
                    "min": 0,
                    "max": "*",
                },
                {
                    "id": "Observation.code",
                    "path": "Observation.code",
                },
                {
                    "id": "Observation.code.coding",
                    "path": "Observation.code.coding",
                    "slicing": {
                        "discriminator": [
                            {"type": "value", "path": "code"},
                            {"type": "value", "path": "system"},
                        ],
                        "ordered": False,
                        "rules": "open",
                    },
                },
                {
                    "id": "Observation.code.coding:slicedCoding",
                    "path": "Observation.code.coding",
                    "sliceName": "slicedCoding",
                    "min": 1,
                    "max": "1",
                },
                {
                    "id": "Observation.code.coding:slicedCoding.system",
                    "path": "Observation.code.coding.system",
                    "min": 1,
                    "max": "1",
                    "type": [{"code": "uri"}],
                    "fixedUri": "http://example.org",
                },
                {
                    "id": "Observation.code.coding:slicedCoding.code",
                    "path": "Observation.code.coding.code",
                    "min": 1,
                    "max": "1",
                    "type": [{"code": "code"}],
                    "fixedCode": "12345-6",
                },
            ]
        },
    }

    model = factory.build(
        structure_definition=structure_definition, mode="differential"
    )

    # -----------------------------------------------------------------------
    # ProfileExample – root model
    # -----------------------------------------------------------------------
    from fhircraft.fhir.resources.datatypes.R5.core import Observation

    assert model.__name__ == "ProfileExample"
    assert issubclass(model, Observation)
    assert (
        model._canonical_url == "http://example.org/fhir/StructureDefinition/issue-255"
    )
    assert "code" in model.model_fields

    # -----------------------------------------------------------------------
    # ProfileExampleCode – backbone for Observation.code
    # -----------------------------------------------------------------------
    from fhircraft.fhir.resources.datatypes.R5.complex import CodeableConcept

    code_annotation = model.model_fields["code"].annotation
    # annotation is Optional[ProfileExampleCode] i.e. Union[ProfileExampleCode, None]
    code_model = next(a for a in get_args(code_annotation) if a is not type(None))

    assert code_model.__name__ == "ProfileExampleCode"
    assert issubclass(code_model, CodeableConcept)
    assert "coding" in code_model.model_fields

    # -----------------------------------------------------------------------
    # ProfileExampleSlicedCoding – FHIRSliceModel inside code.coding
    # -----------------------------------------------------------------------
    from fhircraft.fhir.resources.datatypes.R5.complex import Coding

    coding_annotation = code_model.model_fields["coding"].annotation
    # Optional[List[Annotated[Union[SlicedCoding, Coding], ...]]]
    list_type = next(a for a in get_args(coding_annotation) if a is not type(None))
    annotated_item = get_args(list_type)[0]  # List[X] -> X (Annotated[...])
    union_type = get_args(annotated_item)[0]  # Annotated[Union[...], ...] -> Union[...]
    union_members = get_args(union_type)  # Union[A, B] -> (A, B)

    sliced_coding_model: type = next(
        m
        for m in union_members
        if isinstance(m, type) and issubclass(m, FHIRSliceModel)
    )

    assert sliced_coding_model.__name__ == "ProfileExampleSlicedCoding"
    assert issubclass(sliced_coding_model, Coding)
    assert issubclass(sliced_coding_model, FHIRSliceModel)

    # cardinalities carried as class variables
    assert sliced_coding_model.min_cardinality == 1
    assert sliced_coding_model.max_cardinality == 1

    # -----------------------------------------------------------------------
    # Field defaults reflect the fixedUri / fixedCode constraints
    # -----------------------------------------------------------------------
    assert sliced_coding_model.model_fields["system"].default == "http://example.org"
    assert sliced_coding_model.model_fields["code"].default == "12345-6"

    # -----------------------------------------------------------------------
    # Fixed-value validators reject wrong values at runtime
    # -----------------------------------------------------------------------
    with pytest.raises(pydantic.ValidationError):
        sliced_coding_model(system="http://wrong.org", code="12345-6")

    with pytest.raises(pydantic.ValidationError):
        sliced_coding_model(system="http://example.org", code="WRONG")

    # -----------------------------------------------------------------------
    # Valid instance assembles without errors
    # -----------------------------------------------------------------------
    instance = sliced_coding_model(system="http://example.org", code="12345-6")
    assert instance.system == "http://example.org"
    assert instance.code == "12345-6"


def test_regression_issue_258(factory):
    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "issue-258",
        "url": "http://example.org/fhir/StructureDefinition/issue-258",
        "version": "5.0.0",
        "name": "ProfileExample",
        "title": "Example Profile",
        "status": "draft",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Observation",
        "derivation": "constraint",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
        "differential": {
            "element": [
                {"id": "Observation", "path": "Observation", "min": 0, "max": "*"},
                {
                    "id": "Observation.category",
                    "path": "Observation.category",
                    "slicing": {"discriminator": [{"type": "value", "path": "coding"}]},
                },
                {
                    "id": "Observation.category:slice",
                    "path": "Observation.category",
                    "max": "2",
                    "sliceName": "slice",
                    "patternCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://example.org",
                                "code": "12345-6",
                                "display": "Fixed Category",
                            }
                        ]
                    },
                },
            ]
        },
    }

    model = factory.build(
        structure_definition=structure_definition, mode="differential"
    )

    from typing import get_args
    import pydantic
    from fhircraft.fhir.resources.base import FHIRSliceModel
    from fhircraft.fhir.resources.datatypes.R5.core import Observation
    from fhircraft.fhir.resources.datatypes.R5.complex import CodeableConcept, Coding

    # -----------------------------------------------------------------------
    # ProfileExample – root model
    # -----------------------------------------------------------------------
    assert model.__name__ == "ProfileExample"
    assert issubclass(model, Observation)
    assert (
        model._canonical_url == "http://example.org/fhir/StructureDefinition/issue-258"
    )
    assert "category" in model.model_fields

    # -----------------------------------------------------------------------
    # ProfileExampleSlice – FHIRSliceModel inside category
    # -----------------------------------------------------------------------
    category_annotation = model.model_fields["category"].annotation
    list_type = next(a for a in get_args(category_annotation) if a is not type(None))
    annotated_item = get_args(list_type)[0]
    union_type = get_args(annotated_item)[0]
    union_members = get_args(union_type)

    slice_model = next(
        m
        for m in union_members
        if isinstance(m, type) and issubclass(m, FHIRSliceModel)
    )

    assert slice_model.__name__ == "ProfileExampleSlice"
    assert issubclass(slice_model, CodeableConcept)
    assert slice_model.min_cardinality == 0
    assert slice_model.max_cardinality == 2

    # -----------------------------------------------------------------------
    # Pattern default on the coding field
    # -----------------------------------------------------------------------
    assert slice_model.model_fields["coding"].default is not None

    # -----------------------------------------------------------------------
    # Pattern validator rejects non-matching instances at runtime
    # -----------------------------------------------------------------------
    with pytest.raises(pydantic.ValidationError):
        slice_model(coding=[{"system": "http://wrong.org", "code": "WRONG"}])

    # -----------------------------------------------------------------------
    # Valid instance assembles without errors
    # -----------------------------------------------------------------------
    instance = slice_model(
        coding=[
            Coding(
                system="http://example.org", code="12345-6", display="Fixed Category"
            )
        ]
    )
    assert instance is not None


def test_regression_issue_111(factory):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "example-procedure",
        "url": "http://example.org/StructureDefinition/example-procedure",
        "version": "0.1.0",
        "name": "ExampleProcedure",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Procedure",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Procedure",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Procedure",
                    "path": "Procedure",
                },
                {
                    "id": "Procedure.code",
                    "path": "Procedure.code",
                    "patternCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
                                "code": "C93304",
                                "display": "Tumor Board Review",
                            }
                        ]
                    },
                },
                {
                    "id": "Procedure.code.text",
                    "path": "Procedure.code.text",
                    "fixedString": "Tumor Board Review",
                    "min": 0,
                },
            ]
        },
    }

    model = factory.build(
        structure_definition=structure_definition, mode="differential"
    )

    from typing import get_args
    import pydantic
    from fhircraft.fhir.resources.datatypes.R5.complex import CodeableConcept, Coding

    # -----------------------------------------------------------------------
    # ExampleProcedure – root model
    # -----------------------------------------------------------------------
    assert model.__name__ == "ExampleProcedure"
    assert (
        model._canonical_url
        == "http://example.org/StructureDefinition/example-procedure"
    )
    assert "code" in model.model_fields

    # -----------------------------------------------------------------------
    # ExampleProcedureCode – backbone for Procedure.code
    # -----------------------------------------------------------------------
    code_annotation = model.model_fields["code"].annotation
    code_model = next(a for a in get_args(code_annotation) if a is not type(None))

    assert code_model.__name__ == "ExampleProcedureCode"
    assert issubclass(code_model, CodeableConcept)

    # -----------------------------------------------------------------------
    # Fixed value on the text field
    # -----------------------------------------------------------------------
    assert code_model.model_fields["text"].default == "Tumor Board Review"

    # -----------------------------------------------------------------------
    # Fixed-value validator rejects wrong text at runtime
    # -----------------------------------------------------------------------
    with pytest.raises(pydantic.ValidationError):
        code_model(text="Wrong Text")

    # -----------------------------------------------------------------------
    # Pattern default on the root code field
    # -----------------------------------------------------------------------
    code_field = model.model_fields["code"]
    assert code_field.default is not None
    default_code = code_field.default
    assert isinstance(default_code, CodeableConcept)
    assert default_code.coding is not None
    assert default_code.coding[0].code == "C93304"

    # -----------------------------------------------------------------------
    # Pattern validator rejects wrong code at runtime
    # -----------------------------------------------------------------------
    with pytest.raises(pydantic.ValidationError):
        model(code=code_model(coding=[Coding(system="http://wrong.org", code="WRONG")]))

    # -----------------------------------------------------------------------
    # Valid instance assembles without errors
    # -----------------------------------------------------------------------
    instance = model()
    assert isinstance(instance, model)


def test_regression_issue_263(factory):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "vitalspanel",
        "url": "http://hl7.org/fhir/StructureDefinition/vitalspanel",
        "version": "5.0.0",
        "name": "Vitalspanel",
        "title": "Observation Vital Signs Panel Profile",
        "status": "draft",
        "experimental": False,
        "date": "2018-08-11",
        "description": "FHIR Vital Signs Panel Profile",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Observation",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Observation.code",
                    "path": "Observation.code",
                },
                {
                    "id": "Observation.code.coding",
                    "path": "Observation.code.coding",
                    "slicing": {
                        "discriminator": [
                            {"type": "value", "path": "code"},
                            {"type": "value", "path": "system"},
                        ],
                        "ordered": False,
                        "rules": "open",
                    },
                },
                {
                    "id": "Observation.code.coding:VitalsPanelCode",
                    "path": "Observation.code.coding",
                    "sliceName": "VitalsPanelCode",
                    "max": "1",
                },
                {
                    "id": "Observation.code.coding:VitalsPanelCode.system",
                    "path": "Observation.code.coding.system",
                    "type": [{"code": "uri"}],
                    "fixedUri": "http://loinc.org",
                },
                {
                    "id": "Observation.code.coding:VitalsPanelCode.code",
                    "path": "Observation.code.coding.code",
                    "type": [{"code": "code"}],
                    "fixedCode": "85353-1",
                },
            ]
        },
    }

    model = factory.build(
        structure_definition=structure_definition, mode="differential"
    )

    print(CodeGenerator().generate_resource_model_code(model))

    from typing import get_args
    import pydantic
    from fhircraft.fhir.resources.base import FHIRSliceModel
    from fhircraft.fhir.resources.datatypes.R5.core import Observation
    from fhircraft.fhir.resources.datatypes.R5.complex import CodeableConcept, Coding

    # -----------------------------------------------------------------------
    # Vitalspanel – root model
    # -----------------------------------------------------------------------
    assert model.__name__ == "Vitalspanel"
    assert issubclass(model, Observation)
    assert "code" in model.model_fields

    # -----------------------------------------------------------------------
    # VitalspanelCode – backbone for Observation.code
    # -----------------------------------------------------------------------
    code_annotation = model.model_fields["code"].annotation
    code_model = next(a for a in get_args(code_annotation) if a is not type(None))
    assert issubclass(code_model, CodeableConcept)
    assert "coding" in code_model.model_fields

    # -----------------------------------------------------------------------
    # VitalspanelVitalsPanelCode – FHIRSliceModel inside code.coding
    # -----------------------------------------------------------------------
    coding_annotation = code_model.model_fields["coding"].annotation
    list_type = next(a for a in get_args(coding_annotation) if a is not type(None))
    print(coding_annotation)
    annotated_item = get_args(list_type)[0]
    union_type = get_args(annotated_item)[0]
    union_members = get_args(union_type)

    slice_model = next(
        m
        for m in union_members
        if isinstance(m, type) and issubclass(m, FHIRSliceModel)
    )

    assert slice_model.__name__ == "VitalspanelVitalsPanelCode"
    assert issubclass(slice_model, Coding)
    assert slice_model.min_cardinality == 0
    assert slice_model.max_cardinality == 1

    # -----------------------------------------------------------------------
    # Fixed-value defaults
    # -----------------------------------------------------------------------
    assert slice_model.model_fields["system"].default == "http://loinc.org"
    assert slice_model.model_fields["code"].default == "85353-1"

    # -----------------------------------------------------------------------
    # Fixed-value validators reject wrong values at runtime
    # -----------------------------------------------------------------------
    with pytest.raises(pydantic.ValidationError):
        slice_model(system="http://wrong.org", code="85353-1")

    with pytest.raises(pydantic.ValidationError):
        slice_model(system="http://loinc.org", code="WRONG")

    # -----------------------------------------------------------------------
    # Valid instance assembles without errors
    # -----------------------------------------------------------------------
    instance = slice_model(system="http://loinc.org", code="85353-1")
    assert instance.system == "http://loinc.org"
    assert instance.code == "85353-1"


def test_regression_issue_262():
    from pydantic import Field, model_validator
    from typing import Optional, List
    from fhircraft.fhir.resources.datatypes.R5.core import Patient
    from typing import List, Optional
    from fhircraft.fhir.resources.datatypes.R5.complex import HumanName, Meta
    from fhircraft.fhir.resources.datatypes.primitives import String
    from fhircraft.fhir.resources.validators import validate_element_constraint

    class ExamplePatientName(HumanName):
        family: Optional[String] = Field(
            description="(USCDI) Family name (often called \u0027Surname\u0027)",
            default=None,
        )

    class ExamplePatient(Patient):

        _canonical_url = "http://example.org/fhir/StructureDefinition/example"

        meta: Optional[Meta] = Field(
            title="Meta",
            description="Metadata about the resource.",
            default_factory=lambda: Meta(
                profile=["http://example.org/fhir/StructureDefinition/example"]
            ),
        )
        name: Optional[List[ExamplePatientName]] = Field(
            description="(USCDI) A name associated with the patient",
            default=None,
        )

        @model_validator(mode="after")
        def FHIR_us_core_6_constraint_validator(self):
            return validate_element_constraint(
                self,
                elements=["name"],
                expression="(family.exists() or given.exists()) xor extension.where(url='http://hl7.org/fhir/StructureDefinition/data-absent-reason').exists()",
                human="At least name.given and/or name.family are present or, if neither is available, the Data Absent Reason Extension is present.",
                key="us-core-6",
                severity="error",
            )

    instance = ExamplePatient(
        name=[HumanName(given=["John"], family="Doe")]  # type: ignore
    )

    assert isinstance(instance, ExamplePatient)
    assert instance.name
    assert instance.name[0].given == ["John"]


def test_regression_issue_265(factory):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "example-profile",
        "text": {
            "status": "generated",
            "div": '<div xmlns="http://www.w3.org/1999/xhtml">to do</div>',
        },
        "url": "http://hl7.org/fhir/StructureDefinition/example-profile",
        "version": "5.0.0",
        "name": "ExampleProfile",
        "title": "Example Profile",
        "status": "draft",
        "experimental": False,
        "date": "2018-08-11",
        "description": "Example Profile Description",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Observation",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Observation",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Observation",
                    "path": "Observation",
                    "short": "assessment observation",
                },
                {
                    "id": "Observation.category",
                    "path": "Observation.category",
                    "min": 1,
                    "mustSupport": True,
                },
                {
                    "id": "Observation.category:slice",
                    "path": "Observation.category",
                    "sliceName": "slice",
                    "short": "Classification of type of observation",
                    "min": 0,
                    "mustSupport": False,
                    "binding": {
                        "strength": "required",
                        "valueSet": "http://hl7.org/fhir/ValueSet/observation-category",
                    },
                },
            ]
        },
    }

    model = factory.build(
        structure_definition=structure_definition, mode="differential"
    )

    from typing import get_args
    from fhircraft.fhir.resources.base import FHIRSliceModel
    from fhircraft.fhir.resources.datatypes.R5.core import Observation
    from fhircraft.fhir.resources.datatypes.R5.complex import CodeableConcept

    # -----------------------------------------------------------------------
    # ExampleProfile – root model (only one class should be generated;
    # the slice has no discriminating fixed values, so no FHIRSliceModel subclass
    # is created – the category field stays a plain List[CodeableConcept]).
    # -----------------------------------------------------------------------
    assert model.__name__ == "ExampleProfile"
    assert issubclass(model, Observation)
    assert (
        model._canonical_url
        == "http://hl7.org/fhir/StructureDefinition/example-profile"
    )
    assert "category" in model.model_fields

    # -----------------------------------------------------------------------
    # category field is Optional[List[CodeableConcept]] – no slice model
    # -----------------------------------------------------------------------
    category_annotation = model.model_fields["category"].annotation
    list_type = next(a for a in get_args(category_annotation) if a is not type(None))
    item_type = get_args(list_type)[0]
    assert item_type is CodeableConcept

    # No FHIRSliceModel subclasses should appear anywhere in the field annotation
    all_args = get_args(list_type)
    for arg in all_args:
        if isinstance(arg, type):
            assert not issubclass(
                arg, FHIRSliceModel
            ), f"Unexpected FHIRSliceModel subclass {arg} in category annotation"


def test_regression_issue_266(factory):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "example-profile",
        "url": "http://hl7.org/fhir/StructureDefinition/example-profile",
        "version": "5.0.0",
        "name": "ExampleProfile",
        "title": "Example Profile",
        "status": "draft",
        "experimental": False,
        "date": "2018-08-11",
        "description": "Example Profile Description",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "AdverseEvent",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/AdverseEvent",
        "derivation": "constraint",
        "differential": {
            "element": [
                {"id": "AdverseEvent", "path": "AdverseEvent"},
                {
                    "id": "AdverseEvent.extension",
                    "path": "AdverseEvent.extension",
                    "slicing": {
                        "discriminator": [{"type": "value", "path": "url"}],
                        "ordered": False,
                        "rules": "open",
                    },
                    "min": 1,
                },
                {
                    "id": "AdverseEvent.extension:grade",
                    "path": "AdverseEvent.extension",
                    "sliceName": "grade",
                    "short": "grade",
                    "min": 1,
                    "max": "1",
                    "type": [
                        {
                            "code": "Extension",
                            "profile": [
                                "http://example.org/fhir/StructureDefinition/grade-extension"
                            ],
                        }
                    ],
                    "mustSupport": True,
                },
            ]
        },
    }

    extension_structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "grade-extension",
        "url": "http://example.org/fhir/StructureDefinition/grade-extension",
        "version": "0.1.0",
        "name": "GradeExtension",
        "title": "Grade Extension",
        "status": "active",
        "date": "2025-12-04T10:59:28+00:00",
        "description": "The grade of the adverse event",
        "fhirVersion": "5.0.0",
        "kind": "complex-type",
        "abstract": False,
        "context": [{"type": "element", "expression": "AdverseEvent.extension"}],
        "type": "Extension",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Extension",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Extension",
                    "path": "Extension",
                },
                {
                    "id": "Extension.url",
                    "path": "Extension.url",
                    "fixedUri": "http://example.org/fhir/StructureDefinition/grade-extension",
                },
                {
                    "id": "Extension.value[x]",
                    "path": "Extension.value[x]",
                    "short": "Grade",
                    "definition": "The grade of the adverse event",
                    "type": [{"code": "integer"}],
                    "min": 1,
                    "max": "1",
                },
            ]
        },
    }

    factory.definition_registry.from_dict(structure_definition)
    factory.definition_registry.from_dict(extension_structure_definition)

    model = factory.build(
        structure_definition=structure_definition, mode="differential"
    )

    from typing import get_args
    from fhircraft.fhir.resources.base import FHIRSliceModel
    from fhircraft.fhir.resources.datatypes.R5.complex import Extension

    # -----------------------------------------------------------------------
    # ExampleProfile – root model
    # -----------------------------------------------------------------------
    assert model.__name__ == "ExampleProfile"
    assert "extension" in model.model_fields

    # -----------------------------------------------------------------------
    # GradeExtension – FHIRSliceModel inside extension
    # -----------------------------------------------------------------------
    ext_annotation = model.model_fields["extension"].annotation
    list_type = next(a for a in get_args(ext_annotation) if a is not type(None))
    annotated_item = get_args(list_type)[0]
    union_type = get_args(annotated_item)[0]
    union_members = get_args(union_type)

    grade_ext_model = next(
        m
        for m in union_members
        if isinstance(m, type) and issubclass(m, FHIRSliceModel)
    )

    assert grade_ext_model.__name__ == "ExampleProfileGrade"
    assert issubclass(grade_ext_model, Extension)
    assert (
        grade_ext_model._canonical_url
        == "http://example.org/fhir/StructureDefinition/grade-extension"
    )
    assert grade_ext_model.min_cardinality == 1
    assert grade_ext_model.max_cardinality == 1

    # -----------------------------------------------------------------------
    # Fixed URL default and type-choice field
    # -----------------------------------------------------------------------
    assert (
        grade_ext_model.model_fields["url"].default
        == "http://example.org/fhir/StructureDefinition/grade-extension"
    )
    assert "valueInteger" in grade_ext_model.model_fields


def test_regression_issue_279(factory):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "my-condition",
        "url": "http://example.org/fhir/StructureDefinition/condition",
        "name": "MyCondition",
        "title": "Condition Profile",
        "status": "active",
        "description": "A description",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "Condition",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Condition",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Condition.clinicalStatus.extension",
                    "path": "Condition.clinicalStatus.extension",
                    "slicing": {
                        "discriminator": [{"type": "value", "path": "url"}],
                        "ordered": False,
                        "rules": "open",
                    },
                },
                {
                    "id": "Condition.clinicalStatus.extension:slice1",
                    "path": "Condition.clinicalStatus.extension",
                    "sliceName": "slice1",
                    "min": 0,
                    "max": "1",
                    "type": [
                        {
                            "code": "Extension",
                            "profile": [
                                "http://example.org/fhir/StructureDefinition/my-extension-1"
                            ],
                        }
                    ],
                },
                {
                    "id": "Condition.clinicalStatus.extension:slice2",
                    "path": "Condition.clinicalStatus.extension",
                    "sliceName": "slice2",
                    "min": 0,
                    "max": "1",
                    "type": [
                        {
                            "code": "Extension",
                            "profile": [
                                "http://example.org/fhir/StructureDefinition/my-extension-2"
                            ],
                        }
                    ],
                },
            ]
        },
    }

    extension_1_structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "my-extension-1",
        "url": "http://example.org/fhir/StructureDefinition/my-extension-1",
        "name": "MyExtension1",
        "title": "My Extension 1",
        "status": "active",
        "description": "A description of my extension 1.",
        "fhirVersion": "5.0.0",
        "kind": "complex-type",
        "abstract": False,
        "context": [
            {"expression": "Condition.clinicalStatus.extension", "type": "element"}
        ],
        "type": "Extension",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Extension",
        "derivation": "constraint",
        "differential": {
            "element": [
                {"id": "Extension", "path": "Extension"},
                {
                    "id": "Extension.url",
                    "path": "Extension.url",
                    "fixedUri": "http://example.org/fhir/StructureDefinition/my-extension-1",
                },
                {
                    "id": "Extension.value[x]",
                    "path": "Extension.value[x]",
                    "type": [{"code": "CodeableConcept"}],
                    "binding": {
                        "strength": "required",
                        "valueSet": "http://example.org/fhir/ValueSet/my-value-set-1",
                    },
                },
            ]
        },
    }

    extension_2_structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "my-extension-2",
        "url": "http://example.org/fhir/StructureDefinition/my-extension-2",
        "name": "MyExtension2",
        "title": "My Extension 2",
        "status": "active",
        "description": "A description of my extension 2.",
        "fhirVersion": "5.0.0",
        "kind": "complex-type",
        "abstract": False,
        "context": [
            {"expression": "Condition.clinicalStatus.extension", "type": "element"}
        ],
        "type": "Extension",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Extension",
        "derivation": "constraint",
        "differential": {
            "element": [
                {"id": "Extension", "path": "Extension"},
                {
                    "id": "Extension.url",
                    "path": "Extension.url",
                    "fixedUri": "http://example.org/fhir/StructureDefinition/my-extension-2",
                },
                {
                    "id": "Extension.value[x]",
                    "path": "Extension.value[x]",
                    "type": [{"code": "Reference"}],
                },
            ]
        },
    }

    factory.definition_registry.from_dict(structure_definition)
    factory.definition_registry.from_dict(extension_1_structure_definition)
    factory.definition_registry.from_dict(extension_2_structure_definition)

    model = factory.build(
        structure_definition=structure_definition, mode="differential"
    )

    from typing import get_args
    from fhircraft.fhir.resources.base import FHIRSliceModel
    from fhircraft.fhir.resources.datatypes.R5.complex import CodeableConcept, Extension

    # -----------------------------------------------------------------------
    # MyCondition – root model
    # -----------------------------------------------------------------------
    assert model.__name__ == "MyCondition"
    assert "clinicalStatus" in model.model_fields

    # -----------------------------------------------------------------------
    # MyConditionClinicalStatus – backbone for Condition.clinicalStatus
    # -----------------------------------------------------------------------
    cs_annotation = model.model_fields["clinicalStatus"].annotation
    cs_model = next(a for a in get_args(cs_annotation) if a is not type(None))

    assert cs_model.__name__ == "MyConditionClinicalStatus"
    print(cs_model.__bases__)
    assert issubclass(cs_model, CodeableConcept)
    assert "extension" in cs_model.model_fields

    # -----------------------------------------------------------------------
    # MyExtension1 and MyExtension2 – FHIRSliceModels inside clinicalStatus.extension
    # -----------------------------------------------------------------------
    ext_annotation = cs_model.model_fields["extension"].annotation
    list_type = next(a for a in get_args(ext_annotation) if a is not type(None))
    annotated_item = get_args(list_type)[0]
    union_type = get_args(annotated_item)[0]
    union_members = get_args(union_type)

    slice_models = [
        m
        for m in union_members
        if isinstance(m, type) and issubclass(m, FHIRSliceModel)
    ]
    slice_names = {m.__name__ for m in slice_models}

    assert "MyConditionSlice1" in slice_names
    assert "MyConditionSlice2" in slice_names

    for sm in slice_models:
        assert issubclass(sm, Extension)

    ext1 = next(m for m in slice_models if m.__name__ == "MyConditionSlice1")
    ext2 = next(m for m in slice_models if m.__name__ == "MyConditionSlice2")

    assert (
        ext1._canonical_url
        == "http://example.org/fhir/StructureDefinition/my-extension-1"
    )
    assert (
        ext2._canonical_url
        == "http://example.org/fhir/StructureDefinition/my-extension-2"
    )
    assert (
        ext1.model_fields["url"].default
        == "http://example.org/fhir/StructureDefinition/my-extension-1"
    )
    assert (
        ext2.model_fields["url"].default
        == "http://example.org/fhir/StructureDefinition/my-extension-2"
    )


def test_regression_issue_278(factory):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "my-adverse-event",
        "url": "http://example.org/fhir/StructureDefinition/adverse-event",
        "name": "MyAdverseEvent",
        "title": "Adverse Event Profile",
        "status": "active",
        "description": "A description",
        "fhirVersion": "5.0.0",
        "kind": "resource",
        "abstract": False,
        "type": "AdverseEvent",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/AdverseEvent",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "AdverseEvent",
                    "path": "AdverseEvent",
                    "short": "Adverse Event Profile",
                    "definition": "A description",
                    "min": 0,
                    "max": "*",
                },
                {
                    "id": "AdverseEvent.extension",
                    "path": "AdverseEvent.extension",
                    "slicing": {
                        "discriminator": [{"type": "value", "path": "url"}],
                        "ordered": False,
                        "rules": "open",
                    },
                    "min": 1,
                },
                {
                    "id": "AdverseEvent.extension:my-extension",
                    "path": "AdverseEvent.extension",
                    "sliceName": "myExtension",
                    "short": "My Extension",
                    "type": [
                        {
                            "code": "Extension",
                            "profile": [
                                "http://example.org/fhir/StructureDefinition/my-extension"
                            ],
                        }
                    ],
                },
            ]
        },
    }

    extension_structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "my-extension",
        "url": "http://example.org/fhir/StructureDefinition/my-extension",
        "name": "MyExtension",
        "title": "My Extension",
        "status": "active",
        "description": "A description of my extension.",
        "fhirVersion": "5.0.0",
        "kind": "complex-type",
        "abstract": False,
        "context": [{"expression": "AdverseEvent.extension", "type": "element"}],
        "type": "Extension",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Extension",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Extension",
                    "path": "Extension",
                },
                {
                    "id": "Extension.extension",
                    "path": "Extension.extension",
                    "max": "0",
                },
                {
                    "id": "Extension.url",
                    "path": "Extension.url",
                    "fixedUri": "http://example.org/fhir/StructureDefinition/my-extension",
                },
                {
                    "id": "Extension.value[x]",
                    "path": "Extension.value[x]",
                    "short": "Custom value",
                    "definition": "The custom value of the extension",
                    "type": [{"code": "integer"}],
                },
            ]
        },
    }

    factory.definition_registry.from_dict(structure_definition)
    factory.definition_registry.from_dict(extension_structure_definition)

    model = factory.build(
        structure_definition=structure_definition, mode="differential"
    )

    from typing import get_args
    from fhircraft.fhir.resources.base import FHIRSliceModel
    from fhircraft.fhir.resources.datatypes.R5.complex import Extension

    # -----------------------------------------------------------------------
    # MyAdverseEvent – root model
    # -----------------------------------------------------------------------
    assert model.__name__ == "MyAdverseEvent"
    assert (
        model._canonical_url
        == "http://example.org/fhir/StructureDefinition/adverse-event"
    )
    assert "extension" in model.model_fields

    # -----------------------------------------------------------------------
    # MyExtension – FHIRSliceModel inside extension
    # -----------------------------------------------------------------------
    ext_annotation = model.model_fields["extension"].annotation
    list_type = next(a for a in get_args(ext_annotation) if a is not type(None))
    annotated_item = get_args(list_type)[0]
    union_type = get_args(annotated_item)[0]
    union_members = get_args(union_type)

    ext_model = next(
        m
        for m in union_members
        if isinstance(m, type) and issubclass(m, FHIRSliceModel)
    )

    assert ext_model.__name__ == "MyAdverseEventMyExtension"
    assert issubclass(ext_model, Extension)
    assert (
        ext_model.model_fields["url"].default
        == "http://example.org/fhir/StructureDefinition/my-extension"
    )

    # -----------------------------------------------------------------------
    # Type-choice field valueInteger is present
    # -----------------------------------------------------------------------
    assert "valueInteger" in ext_model.model_fields


def test_regression_issue_277(factory: FHIRModelFactory):

    structure_definition = {
        "resourceType": "StructureDefinition",
        "id": "my-adverse-event",
        "url": "http://example.org/fhir/StructureDefinition/my-adverse-event",
        "name": "MyAdverseEvent",
        "title": "Adverse Event Profile",
        "status": "active",
        "description": "A description",
        "fhirVersion": "4.0.1",
        "kind": "resource",
        "abstract": False,
        "type": "AdverseEvent",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/AdverseEvent",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "AdverseEvent",
                    "path": "AdverseEvent",
                    "short": "Adverse Event Profile",
                    "definition": "A description",
                    "min": 0,
                    "max": "*",
                },
                {
                    "id": "AdverseEvent.suspectEntity",
                    "path": "AdverseEvent.suspectEntity",
                },
                {
                    "id": "AdverseEvent.suspectEntity.instance",
                    "path": "AdverseEvent.suspectEntity.instance",
                    "type": [
                        {
                            "code": "Reference",
                            "targetProfile": [
                                "http://example.org/fhir/StructureDefinition/example-medication",
                            ],
                        }
                    ],
                },
            ]
        },
    }
    factory = factory.__class__(fhir_release="R4")
    model = factory.build(
        structure_definition=structure_definition, mode="differential"
    )

    from typing import get_args

    # -----------------------------------------------------------------------
    # MyAdverseEvent – root model
    # -----------------------------------------------------------------------
    assert model.__name__ == "MyAdverseEvent"
    assert (
        model._canonical_url
        == "http://example.org/fhir/StructureDefinition/my-adverse-event"
    )
    assert "suspectEntity" in model.model_fields

    # -----------------------------------------------------------------------
    # MyAdverseEventSuspectEntity – backbone for AdverseEvent.suspectEntity
    # -----------------------------------------------------------------------
    se_annotation = model.model_fields["suspectEntity"].annotation
    list_type = next(a for a in get_args(se_annotation) if a is not type(None))
    se_model = get_args(list_type)[0]

    assert se_model.__name__ == "MyAdverseEventSuspectEntity"

    # The backbone must subclass the base AdverseEventSuspectEntity backbone
    from fhircraft.fhir.resources.datatypes.R4.core import AdverseEvent

    base_se = next(
        f.annotation
        for name, f in AdverseEvent.model_fields.items()
        if name == "suspectEntity"
    )
    base_se_item = get_args(next(a for a in get_args(base_se) if a is not type(None)))[
        0
    ]
    assert issubclass(se_model, base_se_item)
