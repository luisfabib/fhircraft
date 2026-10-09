from datetime import date
from unittest import TestCase

from pydantic import AliasChoices, BaseModel, Field
import pytest

from fhircraft.fhir.path.engine.core import (
    Element,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    Invocation,
    Literal,
    FHIRPathException,
    This,
)
from fhircraft.fhir.path.engine.strings import Upper

from typing import Any, List, Optional
from unittest import TestCase

import pytest

from fhircraft.fhir.path.engine.core import (
    Element,
    Invocation,
    RootElement,
    TypeSpecifier,
)

from fhircraft.fhir.resources.datatypes.R5 import core, complex, primitive

env = {"%fhirRelease": "R5"}


class MockName(BaseModel):
    _type = "HumanName"
    family: Optional[str] = None
    given: Optional[List[str]] = None


class MockPatient(BaseModel):
    _type = "Patient"
    name: Optional[List[MockName]] = None
    gender: Optional[primitive.string] = None
    birthDate: Optional[primitive.date_] = None
    age: Optional[primitive.integer] = None
    active: Optional[primitive.boolean] = None


@pytest.fixture
def collection() -> FHIRPathCollection:
    return FHIRPathCollection(
        [
            FHIRPathCollectionItem(value=MockPatient()),
            FHIRPathCollectionItem(value=MockPatient()),
        ]
    )


# --------------------------------------------------
# TypeSpecifier
# --------------------------------------------------


@pytest.mark.parametrize(
    "type_specifier,expected_value",
    [
        # Primitive types
        ("string", primitive.String),
        ("canonical", primitive.Canonical),
        ("url", primitive.Url),
        ("dateTime", primitive.DateTime),
        ("markdown", primitive.Markdown),
        # DomainResource types
        ("Patient", core.Patient),
        ("Observation", core.Observation),
        # Complex Types
        ("Quantity", complex.Quantity),
        ("CodeableConcept", complex.CodeableConcept),
    ],
)
def test_type_specifier__evaluate(type_specifier, expected_value):
    type_spec = TypeSpecifier(type_specifier)
    result = type_spec.evaluate(FHIRPathCollection([]), env)
    assert len(result) == 1
    assert result[0] == expected_value


# --------------------------------------------------
# RootElement
# --------------------------------------------------


def test_root_element__evaluate_returns_collection_unchanged(collection):
    # Root().evaluate should return the collection unchanged
    result = RootElement("Patient").evaluate(collection, env)
    assert result == collection
    assert all(isinstance(item, FHIRPathCollectionItem) for item in result._items)


def test_root_element__evaluate_empty_collection_returns_empty_list():
    # Root().evaluate([]) should return []
    result = RootElement("Patient").evaluate(FHIRPathCollection([]), env)
    assert result == []


def test_root_element__raises_error_for_wrong_type(collection):
    with pytest.raises(FHIRPathException):
        RootElement("Condition").evaluate(collection, env)


def test_root_element__string_representation():
    expression = RootElement("Patient")
    assert str(expression) == "Patient"


# --------------------------------------------------
# This
# --------------------------------------------------


def test_this__evaluate_returns_same_collection(collection):
    result = This().evaluate(collection, env)
    assert result == collection
    assert all(isinstance(item, FHIRPathCollectionItem) for item in result._items)


def test_this__evaluate_with_single_item(collection):
    item = collection[0]
    result = This().evaluate(FHIRPathCollection([item]), env)
    assert result == [item]


def test_this__evaluate_empty_collection_returns_empty_list():
    result = This().evaluate(FHIRPathCollection([]), env)
    assert result == []


def test_this__evaluate_with_none_value():
    item = FHIRPathCollectionItem(value=None)
    result = This().evaluate(FHIRPathCollection([item]), env)
    assert result == [item]
    assert result[0] is None


def test_this__string_representation():
    expression = This()
    assert str(expression) == ""


# --------------------------------------------------
# Invocation
# --------------------------------------------------


class TestInvocation(TestCase):

    def setUp(self):
        class DummyResource:
            def __init__(self):
                self.status = "active"

        self.resource = DummyResource()
        self.collection = [FHIRPathCollectionItem(self.resource)]

    def test_evaluate_invokes_method_on_each_item(self):
        result = Invocation(Element("status"), Upper()).evaluate(FHIRPathCollection(self.collection), env)
        assert result[0] == "ACTIVE"

    def test_evaluate_empty_collection_returns_empty_list(self):
        result = Invocation(Element("status"), Upper()).evaluate(FHIRPathCollection([]), env)
        assert result == []

    def test_invocation_string_representation(self):
        expression = Invocation(Element("left"), Element("right"))
        assert str(expression) == "left.right"


# --------------------------------------------------
# Literal
# --------------------------------------------------


class TestLiteral(TestCase):

    def test_evaluate_returns_single_value_for_multiple_collection_items(self):
        items = [
            FHIRPathCollectionItem(value="a"),
            FHIRPathCollectionItem(value="b"),
        ]
        literal = Literal(42)
        result = literal.evaluate(FHIRPathCollection(items), env)
        assert len(result) == 1
        assert list(result) == [42]

    def test_evaluate_with_empty_collection_returns_nonempty_list(self):
        literal = Literal("test")
        result = literal.evaluate(FHIRPathCollection([]), env)
        assert list(result) == ["test"]

    def test_evaluate_with_single_item(self):
        item = FHIRPathCollectionItem(value="x")
        literal = Literal(True)
        result = literal.evaluate(FHIRPathCollection([item]), env)
        assert len(result) == 1
        assert result[0] is True

    def test_evaluate_with_none_literal(self):
        items = [FHIRPathCollectionItem(value="a")]
        literal = Literal(None)
        result = literal.evaluate(FHIRPathCollection(items), env)
        assert len(result) == 1
        assert result[0] is None

    def test_debug_info_evaluates_collection(self):
        result = Literal(42).debug_info({})

        assert result["evaluation_success"] is True
        assert result["result_values"] == ["42"]

    def test_literal_string_representation(self):
        assert str(Literal("foo")) == "'foo'"
        assert str(Literal("123")) == "'123'"
        assert str(Literal(120)) == "120"
        assert str(Literal(True)) == "true"
        assert str(Literal(date(2014, 1, 1))) == "@2014-01-01"


# --------------------------------------------------
# Element
# --------------------------------------------------


def _collection_with_value(**kwargs) -> FHIRPathCollection:
    class DummyResource:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    return FHIRPathCollection([FHIRPathCollectionItem.wrap(DummyResource(**kwargs))])


def test_element__repr_representation():
    expression = Element("elementName")
    assert repr(expression) == "Element(elementName)"


def test_element__string_representation():
    expression = Element("elementName")
    assert str(expression) == "elementName"


def test_element__init_accepts_fhir_string_primitive_as_name():
    # A FHIR `string` primitive is unwrapped to its raw text.
    expression = Element(primitive.String(value="gender"))
    assert expression.name == "gender"


def test_element__init_accepts_literal_as_name():
    # `str(Literal(...))` renders as FHIRPath source, quotes included -- this
    # only ever matches an equally-quoted name, not the bare field name.
    expression = Element(Literal("gender"))
    assert expression.name == "'gender'"


def test_element__init_raises_for_non_string_name():
    with pytest.raises(FHIRPathException):
        Element(123)  # type: ignore


def test_element__equality_compares_by_name():
    assert Element("status") == Element("status")
    assert Element("status") != Element("gender")
    assert Element("status") != "status"


def test_element__hash_is_consistent_with_equality():
    assert hash(Element("status")) == hash(Element("status"))
    assert len({Element("status"), Element("status"), Element("gender")}) == 2


def test_element__evaluate_returns_empty_for_empty_collection():
    assert Element("status").evaluate(FHIRPathCollection([]), env) == []


def test_element__evaluate_returns_empty_when_field_missing():
    collection = _collection_with_value(status="active")
    result = Element("missingField").evaluate(collection, env)
    assert result == []


@pytest.mark.parametrize(
    "element_name, element_value",
    [
        ("valueString", primitive.String(value="male")),
        ("valueInteger", primitive.Integer(value=30)),
        ("valueBoolean", primitive.Boolean(value=True)),
        ("valueDate", primitive.Date(value="2014-01-01")),
    ],
)
def test_element__evaluate_returns_primitive_value(element_name, element_value):
    collection = _collection_with_value(**{element_name: element_value})
    result = Element(element_name).evaluate(collection, env)
    assert len(result) == 1
    assert result[0] == element_value


@pytest.mark.parametrize(
    "element_name, element_value",
    [
        ("valueCoding", complex.Coding(code="code1", system="system1")),
        ("valueReference", complex.Reference(reference="ref1")),
    ],
)
def test_element__evaluate_returns_complex_value(element_name, element_value):
    collection = _collection_with_value(**{element_name: element_value})
    result = Element(element_name).evaluate(collection, env)
    assert len(result) == 1
    assert result[0] == element_value


@pytest.mark.parametrize(
    "element_name, element_value",
    [
        (
            "valueString",
            # `model_construct` bypasses the (unrelated, currently broken)
            # Extension "value[x] xor extension" invariant validator.
            primitive.String.model_construct(
                extension=[complex.Extension.model_construct(url="url1", valueId="id1")]
            ),
        ),
        (
            "valueInteger",
            primitive.Integer.model_construct(
                extension=[complex.Extension.model_construct(url="url2", valueId="id2")]
            ),
        ),
    ],
)
def test_element__evaluate_returns_primitive_extensions(element_name, element_value):
    # FHIR primitives carry `extension` as a genuine field on their own model,
    # so chaining `Element("extension")` needs no special-casing in `Element`.
    collection = _collection_with_value(**{element_name: element_value})
    result = Invocation(Element(element_name), Element("extension")).evaluate(
        collection, env
    )
    assert len(result) == 1
    assert result[0] == element_value.extension[0]


def test_element__evaluate_identifies_aliased_fields():
    class DummyResource(BaseModel):
        class_: str = Field(
            alias="class", validation_alias=AliasChoices("class", "class_")
        )

    collection = [FHIRPathCollectionItem.wrap(DummyResource(class_="classValue"))]  # type: ignore
    # Should return the value of the field as a FHIRPathCollectionItem
    result = Element("class").evaluate(FHIRPathCollection(collection), env)
    assert len(result) == 1
    assert result[0] == "classValue"


def test_element__evaluate_resolves_leading_underscore_extension_sibling():
    # Raw FHIR JSON keeps a primitive's id/extension under a leading-underscore
    # sibling key (e.g. `_status`); it is only consulted when `status` itself
    # is absent.
    resource = {"_status": {"id": "ext1"}}
    result = Element("status").evaluate(
        FHIRPathCollection([FHIRPathCollectionItem(resource)]), env
    )
    assert len(result) == 1
    assert result[0] == {"id": "ext1"}
    assert result._items[0].accessor.element == "status"


def test_element__evaluate_handles_list_valued_fields_in_order():
    patient = MockPatient(name=[MockName(family="Doe"), MockName(family="Smith")])
    result = Element("name").evaluate(FHIRPathCollection([FHIRPathCollectionItem(patient)]), env)
    assert [item.family for item in result] == ["Doe", "Smith"]
    assert [item.accessor.index for item in result._items if item.accessor] == [0, 1]


def test_element__evaluate_sets_parent_and_element_on_children():
    collection = _collection_with_value(status="active")
    result = Element("status").evaluate(collection, env)
    assert result._items[0].accessor.parent.get() is collection[0]
    assert result._items[0].accessor.element == "status"
    assert result._items[0].canonical_path.endswith("status")


def test_element__evaluate_broadcasts_over_every_item_in_collection():
    collection = _collection_with_value(status="active") + _collection_with_value(
        status="cancelled"
    )
    result = Element("status").evaluate(FHIRPathCollection(collection), env)
    assert list(result) == ["active", "cancelled"]


def test_element__evaluate_skips_items_whose_value_is_none():
    collection = [FHIRPathCollectionItem(None)] + _collection_with_value(
        status="active"
    )
    result = Element("status").evaluate(FHIRPathCollection(collection), env)
    assert len(result) == 1
    assert result[0] == "active"


def test_element__evaluate_missing_dict_key_yields_writable_target():
    resource = {}
    result = Element("newField").evaluate(FHIRPathCollection([FHIRPathCollectionItem(resource)]), env)
    assert len(result) == 0
    assert resource == {}
    result.set("x")
    assert resource["newField"] == "x"


def test_element__evaluate_missing_model_field_yields_writable_target():
    patient = MockPatient()
    result = Element("name").evaluate(FHIRPathCollection([FHIRPathCollectionItem(patient)]), env)
    assert len(result) == 0
    assert patient.name in (None, [])
    name = MockName(family="Doe")
    result.add(name)
    assert patient.name == [name]


def test_element__evaluate_chains_through_missing_parents():
    patient = MockPatient()
    collection = Element("name").evaluate(FHIRPathCollection([FHIRPathCollectionItem(patient)]), env)
    result = Element("family").evaluate(collection, env)
    assert len(result) == 0
    assert not patient.name
    result.set("Doe")
    assert patient.name and patient.name[0].family == "Doe"


def test_element__evaluate_literal_has_no_writable_target():
    result = Element("x").evaluate(FHIRPathCollection([FHIRPathCollectionItem("abc")]), env)
    assert result == []
    assert result.targets == ()


def test_element__evaluate_does_not_mutate_container():
    resource = {}
    Element("newField").evaluate(FHIRPathCollection([FHIRPathCollectionItem(resource)]), env)
    assert resource == {}
