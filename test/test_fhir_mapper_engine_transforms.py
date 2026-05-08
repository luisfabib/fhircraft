import uuid
from unittest import TestCase
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from fhircraft.fhir.mapper.engine import transforms as tf
from fhircraft.fhir.path import engine as fp
from fhircraft.fhir.mapper.engine.scope import MappingScope
from fhircraft.fhir.resources.datatypes.R5.core.structure_map import (
    StructureMapGroupRuleTargetParameter as StructureMapParameter,
)
from fhircraft.fhir.path.engine import Element, Invocation
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    CodeableConcept,
    Coding,
    ContactPoint,
    Identifier,
    Quantity,
)


class MockResource(BaseModel):
    _type = "MockResource"
    id: str = "1234"
    baz: str | None = None
    foo: int | None = None


class MockConceptMap(MagicMock):
    class Group1:
        class Element:
            code = "abc"

            class Target:
                code = "def"

            target = [Target()]

        element = [Element()]

    class Group2:
        class Element:
            code = "1234"

            class Target:
                code = "4567"

            target = [Target()]

        element = [Element()]

    group = [Group1(), Group2()]


@pytest.fixture
def scope():
    return MappingScope(
        name="test",
        types={"MockResource": MockResource},
        variables={
            "vstr": Invocation(Element("src"), Element("baz")),
            "vint": Invocation(Element("src"), Element("foo")),
            "vfull": Element("src"),
            "id": Invocation(Element("src"), Element("id")),
        },
        concept_maps={
            "map": MockConceptMap(),
        },
        source_instances={"src": MockResource(baz="abc", foo=123, id="1234")},
    )


# =========================
# copy() Tests
# =========================


@pytest.mark.parametrize(
    "valueType,value,expected",
    [
        ("valueId", "vstr", "abc"),
        ("valueId", "vint", 123),
        ("valueString", "some-string", "some-string"),
        ("valueInteger", 123, 123),
        ("valueBoolean", True, True),
        ("valueDate", "2024-01-01", "2024-01-01"),
        ("valueDecimal", 12.34, 12.34),
        ("valueDateTime", "2024-01-01T12:00:00Z", "2024-01-01T12:00:00Z"),
    ],
)
def test_copy_transform(scope, valueType, value, expected):
    params = [StructureMapParameter(**{valueType: value})]
    assert tf.Copy(params).process(scope) == expected


def test_copy_transform_too_many_parameters():
    params = [
        StructureMapParameter(valueId="vstr"),
        StructureMapParameter(valueId="vstr2"),
    ]
    with pytest.raises(ValueError):
        tf.Copy(params)


# =========================
# create() Tests
# =========================


def test_create_transform(scope):
    params = [StructureMapParameter(valueString="MockResource")]
    assert isinstance(tf.Create(params).process(scope), MockResource)


def test_create_transform_too_many_parameters():
    params = [
        StructureMapParameter(valueString="vstr1"),
        StructureMapParameter(valueString="vstr2"),
    ]
    with pytest.raises(ValueError):
        tf.Create(params)


# =========================
# truncate() Tests
# =========================


@pytest.mark.parametrize(
    "variable,length,expected",
    [
        ("vstr", 1, "a"),
        ("vstr", 2, "ab"),
        ("vstr", 3, "abc"),
    ],
)
def test_truncate_transform(scope, variable, length, expected):
    params = [
        StructureMapParameter(valueId=variable),
        StructureMapParameter(valueInteger=length),
    ]
    assert tf.Truncate(params).process(scope) == expected


def test_truncate_transform_too_many_parameters():
    params = [
        StructureMapParameter(valueString="vstr1"),
        StructureMapParameter(valueString="vstr2"),
        StructureMapParameter(valueString="vstr3"),
    ]
    with pytest.raises(ValueError):
        tf.Truncate(params)


# =========================
# cast() Tests
# =========================


@pytest.mark.parametrize(
    "value,type_specifier,expected",
    [
        ("123", "Integer", 123),
        ("12.34", "Decimal", 12.34),
        ("12.34", "Decimal", 12.34),
        ("2014", "DateTime", "2014"),
        ("2014-02", "DateTime", "2014-02"),
        ("2014-02-01", "DateTime", "2014-02-01"),
        ("12.5 mm[Hg]", "Quantity", fp.Quantity(value=12.5, unit="mm[Hg]")),
        ("12.5 mg", "Quantity", fp.Quantity(value=12.5, unit="mg")),
    ],
)
def test_cast_transform_explicit(scope, value, type_specifier, expected):

    scope.source_instances = {"src": MockResource(baz=value)}
    params = [
        StructureMapParameter(valueId="vstr"),
        StructureMapParameter(valueString=type_specifier),
    ]
    assert tf.Cast(params).process(scope) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("2014-02", "2014-02"),
        ("12.5", 12.5),
    ],
)
def test_cast_transform_implicit(scope, value, expected):

    scope.source_instances = {"src": MockResource(baz=value)}
    params = [
        StructureMapParameter(valueId="vstr"),
    ]
    assert tf.Cast(params).process(scope) == expected


# =========================
# append() Tests
# =========================


@pytest.mark.parametrize(
    "value_type,value,expected",
    [
        ("valueString", "efg", "prefix-efg"),
        ("valueString", "EFG", "prefix-EFG"),
        ("valueId", "vstr", "prefix-abc"),
    ],
)
def test_append_transform(scope, value_type, value, expected):
    param = [
        StructureMapParameter(valueString="prefix-"),
        StructureMapParameter(**{value_type: value}),
    ]
    assert tf.Append(param).process(scope) == expected


# =========================
# reference() Tests
# =========================


def test_reference_transform(scope):
    params = [StructureMapParameter(valueId="vfull")]
    assert tf.Reference(params).process(scope) == "MockResource/1234"


# =========================
# uuid() Tests
# =========================


def test_uuid_transform(scope):
    assert uuid.UUID(tf.UUID([]).process(scope)).version == 4


# =========================
# translate() Tests
# =========================


def test_translate_transform(scope):
    param = [
        StructureMapParameter(valueId="vstr"),
        StructureMapParameter(valueString="map"),
        StructureMapParameter(valueString="code"),
    ]
    assert tf.Translate(param).process(scope) == "def"


def test_translate_transform_multiple_groups(scope):
    param = [
        StructureMapParameter(valueId="id"),
        StructureMapParameter(valueString="map"),
        StructureMapParameter(valueString="code"),
    ]
    assert tf.Translate(param).process(scope) == "4567"


# =========================
# evaluate() Tests
# =========================


def test_evaluate_transform_implicit_context(scope):
    param = [
        StructureMapParameter(valueId="vint"),
        StructureMapParameter(valueString="$this + 1"),
    ]
    assert tf.Evaluate(param).process(scope) == 124


def test_evaluate_transform_explicit_context(scope):
    param = [
        StructureMapParameter(valueId="vfull"),
        StructureMapParameter(valueString="foo + 1"),
    ]
    assert tf.Evaluate(param).process(scope) == 124


def test_evaluate_transform_no_context(scope):
    param = [StructureMapParameter(valueString="123 + 1")]
    assert tf.Evaluate(param).process(scope) == 124


# =========================
# cc() Tests
# =========================


def test_codeable_concept_transform_text(scope):
    param = [StructureMapParameter(valueString="text-representation")]
    cc = tf.CodeableConcept(param).process(scope)
    cc = CodeableConcept.model_validate(cc)
    assert cc.text == "text-representation"
    assert cc.coding == None


def test_codeable_concept_transform_coding(scope):
    param = [
        StructureMapParameter(valueString="code"),
        StructureMapParameter(valueString="system"),
        StructureMapParameter(valueString="display"),
    ]
    cc = tf.CodeableConcept(param).process(scope)
    cc = CodeableConcept.model_validate(cc)
    assert cc.coding is not None
    assert cc.coding[0].code == "code"
    assert cc.coding[0].system == "system"
    assert cc.coding[0].display == "display"


def test_codeable_concept_transform_scope_variables(scope):
    param = [
        StructureMapParameter(valueId="vstr"),
        StructureMapParameter(valueString="system"),
        StructureMapParameter(valueString="display"),
    ]
    cc = tf.CodeableConcept(param).process(scope)
    cc = CodeableConcept.model_validate(cc)
    assert cc.coding is not None
    assert cc.coding[0].code == "abc"
    assert cc.coding[0].system == "system"
    assert cc.coding[0].display == "display"


# =========================
# c() Tests
# =========================


def test_coding_transform(scope):
    param = [
        StructureMapParameter(valueString="code"),
        StructureMapParameter(valueString="system"),
        StructureMapParameter(valueString="display"),
    ]
    c = tf.Coding(param).process(scope)
    c = Coding.model_validate(c)
    assert c.code == "code"
    assert c.system == "system"
    assert c.display == "display"


def test_coding_transform_scope_variables(scope):
    param = [
        StructureMapParameter(valueId="vstr"),
        StructureMapParameter(valueString="system"),
        StructureMapParameter(valueString="display"),
    ]
    c = tf.Coding(param).process(scope)
    c = Coding.model_validate(c)
    assert c.code == "abc"
    assert c.system == "system"
    assert c.display == "display"


# =========================
# qty() Tests
# =========================


def test_quantity_transform_text_with_comparator(scope):
    params = [StructureMapParameter(valueString=">=5 mg")]
    q = tf.Quantity(params).process(scope)
    q = Quantity.model_validate(q)
    assert q.comparator == ">="
    assert q.value == 5.0
    assert q.unit == "mg"


def test_quantity_transform_text_without_comparator(scope):
    params = [StructureMapParameter(valueString="122.5 mg/kg")]
    q = tf.Quantity(params).process(scope)
    q = Quantity.model_validate(q)
    assert q.comparator == None
    assert q.value == 122.5
    assert q.unit == "mg/kg"


def test_quantity_transform_multi(scope):
    params = [
        StructureMapParameter(valueString="5"),
        StructureMapParameter(valueString="mg"),
        StructureMapParameter(valueString="system"),
        StructureMapParameter(valueString="code"),
    ]
    q = tf.Quantity(params).process(scope)
    q = Quantity.model_validate(q)
    assert q.value == 5.0
    assert q.unit == "mg"
    assert q.system == "system"
    assert q.code == "code"


def test_quantity_transform_scope_variables(scope):
    params = [
        StructureMapParameter(valueId="vint"),
        StructureMapParameter(valueId="vstr"),
        StructureMapParameter(valueString="system"),
        StructureMapParameter(valueString="code"),
    ]
    q = tf.Quantity(params).process(scope)
    q = Quantity.model_validate(q)
    assert q.value == 123
    assert q.unit == "abc"
    assert q.system == "system"
    assert q.code == "code"


# =========================
# id() Tests
# =========================


def test_id_transform(scope):
    param = [
        StructureMapParameter(valueString="sys"),
        StructureMapParameter(valueString="val"),
        StructureMapParameter(valueString="code"),
    ]
    id_ = tf.Identifier(param).process(scope)
    id_ = Identifier.model_validate(id_)
    assert id_.system == "sys"
    assert id_.value == "val"
    assert id_.type is not None
    assert id_.type.coding is not None
    assert id_.type.coding[0].code == "code"


# =========================
# cp() Tests
# =========================


def test_cp_transform(scope):
    param = [
        StructureMapParameter(valueString="phone"),
        StructureMapParameter(valueString="12345"),
    ]
    cp = tf.ContactPoint(param).process(scope)
    cp = ContactPoint.model_validate(cp)
    assert cp.system == "phone"
    assert cp.value == "12345"


def test_cp_transform_implicit(scope):
    param = [StructureMapParameter(valueString="mail@test.org")]
    cp = tf.ContactPoint(param).process(scope)
    cp = ContactPoint.model_validate(cp)
    assert cp.system == "email"
    assert cp.value == "mail@test.org"
