import pytest
import uuid
from unittest import TestCase
from unittest.mock import MagicMock
from fhircraft.fhir.mapping.engine import (
    MappingScope, RuleProcessingError, MappingError
)
from pydantic import BaseModel
from dataclasses import dataclass
from fhircraft.fhir.mapping.engine import FHIRMappingEngine
from fhircraft.fhir.mapping.StructureMap import StructureMapParameter
from fhircraft.fhir.path.engine import Element, Invocation
from fhircraft.fhir.resources.datatypes.R4B.complex_types import (
    CodeableConcept, 
    Coding, 
    Quantity, 
    Identifier, 
    ContactPoint,
)

class MockResource(BaseModel):
    resourceType: str = "MockResource"
    id: str = "1234"
    baz: str | None = None
    foo: int | None = None


class MockConceptMap(MagicMock):
    class Group:
        class Element:
            code = "abc"
            class Target:
                code = "def"
            target = [Target()]
        element = [Element()]
    group = [Group()]

class MappingTargetTransformsTests(TestCase):
    
    def setUp(self):
        self.scope = MappingScope(
            name='test', 
            types={'MockResource': MockResource},
            variables={
                "vstr": Invocation(Element('src'),Element('baz')),
                "vint": Invocation(Element('src'),Element('foo')),
                "vfull": Element('src'),
            },
            concept_maps={
                "map": MockConceptMap(),
            }, 
            source_instances={'src': MockResource(baz="abc", foo=123)},
        )

    #=========================
    # copy
    #=========================

    def test_copy_transform_literal_string(self):
        param = [StructureMapParameter(valueString="foo")]
        assert FHIRMappingEngine._copy_transform(self.scope, param) == "foo"

    def test_copy_transform_literal_number(self):
        param = [StructureMapParameter(valueInteger=42)]
        assert FHIRMappingEngine._copy_transform(self.scope, param) == 42

    def test_copy_transform_id(self):
        param = [StructureMapParameter(valueId="vstr")]
        assert FHIRMappingEngine._copy_transform(self.scope, param) == "abc"

    #=========================
    # create
    #=========================

    def test_create_transform(self):
        param = [StructureMapParameter(valueString="MockResource")]
        assert isinstance(FHIRMappingEngine._create_transform(self.scope, param), MockResource)

    #=========================
    # truncate
    #=========================

    def test_truncate_transform(self):
        param = [StructureMapParameter(valueId="vstr"), StructureMapParameter(valueInteger=2)]
        assert FHIRMappingEngine._truncate_transform(self.scope, param) == "ab"

    #=========================
    # cast
    #=========================

    def test_cast_transform_explicit(self):
        param = [StructureMapParameter(valueId="vint"), StructureMapParameter(valueString="String")]
        assert FHIRMappingEngine._cast_transform(self.scope, param) == "123"

    #=========================
    # append
    #=========================

    def test_append_transform_literals(self):
        param = [StructureMapParameter(valueString="abc"), StructureMapParameter(valueString="def")]
        assert FHIRMappingEngine._append_transform(self.scope, param) == "abcdef"

    def test_append_transform_ids(self):
        param = [StructureMapParameter(valueId="vstr"), StructureMapParameter(valueId="vstr")]
        assert FHIRMappingEngine._append_transform(self.scope, param) == "abcabc"

    def test_append_transform_literals(self):
        param = [StructureMapParameter(valueString="abc"), StructureMapParameter(valueString="def")]
        assert FHIRMappingEngine._append_transform(self.scope, param) == "abcdef"

    #=========================
    # reference
    #=========================

    def test_reference_transform(self):
        param = [StructureMapParameter(valueId="vfull")]
        assert FHIRMappingEngine._reference_transform(self.scope, param) == "MockResource/1234"

    #=========================
    # uuid
    #=========================
        
    def test_uuid_transform(self):
        assert uuid.UUID(FHIRMappingEngine._uuid_transform(self.scope, []))

    #=========================
    # translate
    #=========================
    
    def test_translate_transform(self):
        param = [StructureMapParameter(valueId="vstr"), StructureMapParameter(valueString="map"), StructureMapParameter(valueString="code")]
        assert FHIRMappingEngine._translate_transform(self.scope, param) == "def"

    #=========================
    # evaluate
    #=========================

    def test_evaluate_transform_implicit_context(self):
        param = [StructureMapParameter(valueId="vint"), StructureMapParameter(valueString="$this + 1")]
        assert FHIRMappingEngine._evaluate_transform(self.scope, param) == 124

    def test_evaluate_transform_explicit_context(self):
        param = [StructureMapParameter(valueId="vfull"), StructureMapParameter(valueString="foo + 1")]
        assert FHIRMappingEngine._evaluate_transform(self.scope, param) == 124

    def test_evaluate_transform_no_context(self):
        param = [StructureMapParameter(valueString="123 + 1")]
        with pytest.raises(NotImplementedError):
            FHIRMappingEngine._evaluate_transform(self.scope, param)

    #=========================
    # cc
    #=========================

    def test_cc_transform_text(self):
        param = [StructureMapParameter(valueString="text-representation")]
        cc = FHIRMappingEngine._cc_transform(self.scope, param)
        assert isinstance(cc, CodeableConcept)
        assert cc.text == "text-representation"
        assert cc.coding == None

    def test_cc_transform_coding(self):
        param = [StructureMapParameter(valueString="code"), StructureMapParameter(valueString="system"), StructureMapParameter(valueString="display")]
        cc = FHIRMappingEngine._cc_transform(self.scope, param)
        assert isinstance(cc, CodeableConcept)
        assert cc.coding[0].code == "code"
        assert cc.coding[0].system == "system"
        assert cc.coding[0].display == "display"

    #=========================
    # c
    #=========================

    def test_c_transform(self):
        param = [StructureMapParameter(valueString="code"), StructureMapParameter(valueString="system"), StructureMapParameter(valueString="display")]
        c = FHIRMappingEngine._c_transform(self.scope, param)
        assert isinstance(c, Coding)
        assert c.code == "code"
        assert c.system == "system"
        assert c.display == "display"

    #=========================
    # qty
    #=========================

    def test_qty_transform_text_with_comparator(self):
        param = [StructureMapParameter(valueString=">=5 mg")]
        q = FHIRMappingEngine._qty_transform(self.scope, param)
        assert isinstance(q, Quantity)
        assert q.comparator == ">="
        assert q.value == 5.0
        assert q.unit == "mg"

    def test_qty_transform_text_without_comparator(self):
        param = [StructureMapParameter(valueString="122.5 mg/kg")]
        q = FHIRMappingEngine._qty_transform(self.scope, param)
        assert isinstance(q, Quantity)
        assert q.comparator == None
        assert q.value == 122.5
        assert q.unit == "mg/kg"

    def test_qty_transform_multi(self):
        param = [StructureMapParameter(valueString="5"), StructureMapParameter(valueString="mg"), StructureMapParameter(valueString="system"), StructureMapParameter(valueString="code")]
        q = FHIRMappingEngine._qty_transform(self.scope, param)
        assert isinstance(q, Quantity)
        assert q.value == 5.0
        assert q.unit == "mg"
        assert q.system == "system"
        assert q.code == "code"

    #=========================
    # id
    #=========================

    def test_id_transform(self):
        param = [StructureMapParameter(valueString="sys"), StructureMapParameter(valueString="val"), StructureMapParameter(valueString="code")]
        id_ = FHIRMappingEngine._id_transform(self.scope, param)
        assert isinstance(id_, Identifier)
        assert id_.system == "sys"
        assert id_.value == "val"
        assert id_.type.coding[0].code == "code"

    #=========================
    # id
    #=========================

    def test_cp_transform(self):
        param = [StructureMapParameter(valueString="phone"), StructureMapParameter(valueString="12345")]
        cp = FHIRMappingEngine._cp_transform(self.scope, param)
        assert isinstance(cp, ContactPoint)
        assert cp.system == "phone"
        assert cp.value == "12345"

    def test_cp_transform_implicit(self):
        param = [StructureMapParameter(valueString="mail@test.org")]
        with pytest.raises(NotImplementedError):
            FHIRMappingEngine._cp_transform(self.scope, param)