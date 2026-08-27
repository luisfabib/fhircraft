from collections import namedtuple
from unittest import result
import pytest
import sys

from fhircraft.exceptions import FHIRPathWarning, FHIRPathException
from fhircraft.fhir.path.engine.additional import *
from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.terminology import TerminologyService
from fhircraft.fhir.path.engine.environment import EnvironmentVariable
from fhircraft.fhir.path.engine.literals import Date, DateTime, Quantity
from fhircraft.fhir.resources.base import FHIRPrimitiveModel
from fhircraft.fhir.resources.datatypes import get_fhir_type
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Coding as R4_Coding,
    CodeableConcept as R4_CodeableConcept,
    Quantity as R4_Quantity,
    Age as R4_Age,
    Extension as R4_Extension,
)
from fhircraft.fhir.resources.datatypes.R4.primitive import Boolean
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Quantity as R4B_Quantity,
    Reference as R4B_Reference,
)
from fhircraft.fhir.resources.datatypes.R4B.primitive import String
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Quantity as R5_Quantity,
    Reference as R5_Reference,
)
from fhircraft.fhir.resources.datatypes.R5.primitive import Integer

env = dict()


@pytest.fixture
def terminology_service():
    """Fixture that provides a mock terminology service implementation for testing."""

    class MockTerminologyService(TerminologyService):

        @staticmethod
        def _code_value(code):
            return getattr(code, "code", code)

        def validate_valueset_code(self, *, url=None, code=None, **kwargs):
            if url == "http://example.org/ValueSet/ExampleVS":
                if code == "valid-code":
                    return True
                else:
                    return False
            raise ValueError()

        def validate_codesystem_code(self, **kwargs):
            raise NotImplementedError()

        def codesystem_lookup(self, **kwargs):
            raise NotImplementedError()

        def codesystem_subsumes(self, codeA, codeB, system=None, version=None):
            code_a = self._code_value(codeA)
            code_b = self._code_value(codeB)
            if system is None:
                raise ValueError("system is required")
            if code_a == "parent" and code_b == "child":
                return True
            if code_a == "child" and code_b == "parent":
                return False
            if code_a == "unknown" or code_b == "unknown":
                return None
            if code_a == "error":
                raise RuntimeError("terminology backend error")
            return False

    return MockTerminologyService()


# -------------
# Extension
# -------------


def test_extension_returns_empty_for_empty_collection():
    collection = []
    result = Extension("").evaluate(collection, env)
    assert result == []


def test_extension_selects_correct_extension_by_url():
    resource = namedtuple("Resource", "extension")(
        extension=[
            R4_Extension(url="http://domain.org/extension1", valueInteger=1),
            R4_Extension(url="http://domain.org/extension2", valueInteger=2),
            R4_Extension(url="http://domain.org/extension3", valueInteger=3),
        ]
    )
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Extension("http://domain.org/extension2").evaluate(collection, env)
    assert result[0].value == resource.extension[1]


# -------------
# HasValue
# -------------

has_value_cases = (
    "ABC",
    123,
    1.23,
    True,
    False,
    Date("@2012"),
    Date("@2012-01"),
    DateTime("@2012-01-01T10:30"),
    DateTime("@2012-01-01T10:30:12.312"),
    "1 year",
)


def test_hasvalue_returns_false_for_empty_collection():
    collection = []
    result = HasValue().evaluate(collection, env)
    assert result[0].value == False


@pytest.mark.parametrize("value", has_value_cases)
def test_hasvalue_returns_true_for_singleton_collection_with_primitive_value(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = HasValue().evaluate(collection, env)
    assert result[0].value == True


def test_hasvalue_returns_false_for_singleton_collection_without_primitive_value():
    collection = [
        FHIRPathCollectionItem(
            value=R4_Extension(url="http://domain.org/extension1", valueInteger=1)
        )
    ]
    result = HasValue().evaluate(collection, env)
    assert result[0].value == False


def test_hasvalue_returns_true_for_singleton_collection_without_value():
    collection = [FHIRPathCollectionItem(value=None)]
    result = HasValue().evaluate(collection, env)
    assert result[0].value == False


def test_hasvalue_returns_false_for_collection_with_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = HasValue().evaluate(collection, env)
    assert result[0].value == False


# -------------
# GetValue
# -------------

get_value_cases = (
    "ABC",
    String(value="ABC"),
    123,
    Integer(value=123),
    1.23,
    True,
    Boolean(value=True),
    False,
    Boolean(value=False),
    Date("@2012"),
    Date("@2012-01"),
    DateTime("@2012-01-01T10:30"),
    DateTime("@2012-01-01T10:30:12.312"),
    "1 year",
)


def test_getvalue_returns_empty_for_empty_collection():
    collection = []
    result = GetValue().evaluate(collection, env)
    assert result == []


@pytest.mark.parametrize("value", get_value_cases)
def test_getvalue_returns_value_for_singleton_collection_with_primitive_value(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = GetValue().evaluate(collection, env)
    if isinstance(value, FHIRPrimitiveModel):
        value = value.value
    assert result[0].value == value


def test_getvalue_returns_empty_for_singleton_collection_without_primitive_value():
    collection = [
        FHIRPathCollectionItem(
            value=R4_Extension(url="http://domain.org/extension1", valueInteger=1)
        )
    ]
    result = GetValue().evaluate(collection, env)
    assert result == []


def test_getvalue_returns_empty_for_collection_with_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = GetValue().evaluate(collection, env)
    assert result == []


# -------------
# HtmlChecks
# -------------


def test_htmlchecks_returns_empty_for_empty_collection():
    collection = []
    result = HtmlChecks().evaluate(collection, env)
    assert result == []


def test_htmlchecks_invalid_xhtml():
    html_snippet = """
    <html>
        <head>
            <link rel="stylesheet" href="styles.css">
            <title>Test</title>
        </head>
        <body>
            <p>Hello, World!</p>
        </body>
    </html>
    """
    collection = [FHIRPathCollectionItem(value=html_snippet)]
    result = HtmlChecks().evaluate(collection, env)
    assert result[0].value == False


def test_htmlchecks_invalid_empty_div():
    html_snippet = """
    <div xmlns=\"http://www.w3.org/1999/xhtml\"></div>
    """
    collection = [FHIRPathCollectionItem(value=html_snippet)]
    result = HtmlChecks().evaluate(collection, env)
    assert result[0].value == False


def test_htmlchecks_valid_xhtml():
    html_snippet = """
    <div xmlns=\"http://www.w3.org/1999/xhtml\">text</div>
    """
    collection = [FHIRPathCollectionItem(value=html_snippet)]
    result = HtmlChecks().evaluate(collection, env)
    assert result[0].value == True


# -------------
# LowBoundary
# -------------


def test_lowboundary_returns_empty_for_empty_collection():
    collection = []
    result = LowBoundary().evaluate(collection, env)
    assert result == []


def test_lowboundary_integer_precision():
    """Test low boundary for integer values"""
    collection = [FHIRPathCollectionItem(value=10)]
    result = LowBoundary().evaluate(collection, env)
    assert result[0].value == 10


def test_lowboundary_float_precision():
    """Test low boundary for decimal values with different precisions"""
    # Single decimal place
    collection = [FHIRPathCollectionItem(value=1.5)]
    result = LowBoundary().evaluate(collection, env)
    assert result[0].value == 1.5 - sys.float_info.epsilon

    # Two decimal places
    collection = [FHIRPathCollectionItem(value=1.25)]
    result = LowBoundary().evaluate(collection, env)
    assert result[0].value == 1.25 - sys.float_info.epsilon


def test_lowboundary_year_only():
    """Test low boundary for year-only date strings"""
    collection = [FHIRPathCollectionItem(value="2018")]
    result = LowBoundary().evaluate(collection, env)
    assert result[0].value == "2018-01-01T00:00:00.000"


def test_lowboundary_year_month():
    """Test low boundary for year-month date strings"""
    collection = [FHIRPathCollectionItem(value="2018-03")]
    result = LowBoundary().evaluate(collection, env)
    assert result[0].value == "2018-03-01T00:00:00.000"


def test_lowboundary_full_date():
    """Test low boundary for full date strings"""
    collection = [FHIRPathCollectionItem(value="2018-03-15")]
    result = LowBoundary().evaluate(collection, env)
    assert result[0].value == "2018-03-15T00:00:00.000"


def test_lowboundary_complete_datetime():
    """Test low boundary for complete datetime strings (should return as-is)"""
    collection = [FHIRPathCollectionItem(value="2018-03-15T14:30:45.123Z")]
    result = LowBoundary().evaluate(collection, env)
    assert result[0].value == "2018-03-15T14:30:45.123Z"


def test_lowboundary_non_datetime_string():
    """Test low boundary for non-datetime strings (should return as-is)"""
    collection = [FHIRPathCollectionItem(value="not-a-date")]
    result = LowBoundary().evaluate(collection, env)
    assert result[0].value == "not-a-date"


def test_lowboundary_fhirpath_quantity():
    """Test low boundary for Quantity objects"""

    quantity = Quantity(value=10.5, unit="kg")
    collection = [FHIRPathCollectionItem(value=quantity)]
    result = LowBoundary().evaluate(collection, env)

    assert result[0].value.value == 10.5 - sys.float_info.epsilon
    assert result[0].value.unit == "kg"


def test_lowboundary_r4_quantity():
    """Test low boundary for Quantity objects"""

    quantity = R4_Quantity(
        value=10.5, unit="kg", system="http://unitsofmeasure.org", code="kg"
    )
    collection = [FHIRPathCollectionItem(value=quantity)]
    result = LowBoundary().evaluate(collection, env)

    assert result[0].value.value == 10.5 - sys.float_info.epsilon
    assert result[0].value.unit == "kg"


def test_lowboundary_r4_age():
    """Test low boundary for Quantity objects"""
    from test.test_fhir_path_engine_conversion import Quantity

    quantity = R4_Age(value=42, unit="a", system="http://unitsofmeasure.org", code="a")
    collection = [FHIRPathCollectionItem(value=quantity)]
    result = LowBoundary().evaluate(collection, env)

    assert result[0].value.value == 42 - sys.float_info.epsilon
    assert result[0].value.unit == "a"


# -------------
# HighBoundary
# -------------


def test_highboundary_returns_empty_for_empty_collection():
    collection = []
    result = HighBoundary().evaluate(collection, env)
    assert result == []


def test_highboundary_integer_precision():
    """Test high boundary for integer values"""
    collection = [FHIRPathCollectionItem(value=10)]
    result = HighBoundary().evaluate(collection, env)
    assert result[0].value == 10


def test_highboundary_float_precision():
    """Test high boundary for decimal values with different precisions"""
    # Single decimal place
    collection = [FHIRPathCollectionItem(value=1.5)]
    result = HighBoundary().evaluate(collection, env)
    assert result[0].value == 1.5 + sys.float_info.epsilon

    # Two decimal places
    collection = [FHIRPathCollectionItem(value=1.25)]
    result = HighBoundary().evaluate(collection, env)
    assert result[0].value == 1.25 + sys.float_info.epsilon


def test_highboundary_year_only():
    """Test high boundary for year-only date strings"""
    collection = [FHIRPathCollectionItem(value="2018")]
    result = HighBoundary().evaluate(collection, env)
    assert result[0].value == "2018-12-31T23:59:59.999"


def test_highboundary_year_month():
    """Test high boundary for year-month date strings"""
    # Regular month
    collection = [FHIRPathCollectionItem(value="2018-03")]
    result = HighBoundary().evaluate(collection, env)
    assert result[0].value == "2018-03-31T23:59:59.999"

    # February in non-leap year
    collection = [FHIRPathCollectionItem(value="2018-02")]
    result = HighBoundary().evaluate(collection, env)
    assert result[0].value == "2018-02-28T23:59:59.999"

    # February in leap year
    collection = [FHIRPathCollectionItem(value="2020-02")]
    result = HighBoundary().evaluate(collection, env)
    assert result[0].value == "2020-02-29T23:59:59.999"


def test_highboundary_full_date():
    """Test high boundary for full date strings"""
    collection = [FHIRPathCollectionItem(value="2018-03-15")]
    result = HighBoundary().evaluate(collection, env)
    assert result[0].value == "2018-03-15T23:59:59.999"


def test_highboundary_complete_datetime():
    """Test high boundary for complete datetime strings (should return as-is)"""
    collection = [FHIRPathCollectionItem(value="2018-03-15T14:30:45.123Z")]
    result = HighBoundary().evaluate(collection, env)
    assert result[0].value == "2018-03-15T14:30:45.123Z"


def test_highboundary_non_datetime_string():
    """Test high boundary for non-datetime strings (should return as-is)"""
    collection = [FHIRPathCollectionItem(value="not-a-date")]
    result = HighBoundary().evaluate(collection, env)
    assert result[0].value == "not-a-date"


def test_highboundary_fhirpath_quantity():
    """Test high boundary for Quantity objects"""

    quantity = Quantity(value=10.5, unit="kg")
    collection = [FHIRPathCollectionItem(value=quantity)]
    result = HighBoundary().evaluate(collection, env)

    assert result[0].value.value == 10.5 + sys.float_info.epsilon
    assert result[0].value.unit == "kg"


def test_highboundary_r4_quantity():
    """Test high boundary for Quantity objects"""

    quantity = R4_Quantity(
        value=10.5, unit="kg", system="http://unitsofmeasure.org", code="kg"
    )
    collection = [FHIRPathCollectionItem(value=quantity)]
    result = HighBoundary().evaluate(collection, env)

    assert result[0].value.value == 10.5 + sys.float_info.epsilon
    assert result[0].value.unit == "kg"


def test_highboundary_r4_age():
    """Test high boundary for Quantity objects"""
    from test.test_fhir_path_engine_conversion import Quantity

    quantity = R4_Age(value=42, unit="a", system="http://unitsofmeasure.org", code="a")
    collection = [FHIRPathCollectionItem(value=quantity)]
    result = HighBoundary().evaluate(collection, env)

    assert result[0].value.value == 42 + sys.float_info.epsilon
    assert result[0].value.unit == "a"


# -------------
# Comparable
# -------------


def test_comparable_same_units():
    collection = [FHIRPathCollectionItem(value=Quantity(value=10, unit="mg"))]
    quantity = Quantity(
        value=12,
        unit="mg",
    )
    assert Comparable(quantity).single(collection, env) == True


def test_comparable_different_units():
    collection = [FHIRPathCollectionItem(value=Quantity(value=10, unit="l"))]
    quantity = Quantity(
        value=12,
        unit="mg",
    )
    assert Comparable(quantity).single(collection, env) == False


def test_comparable_returns_empty_for_empty_collection():
    collection = []
    quantity = Quantity(
        value=12,
        unit="mg",
    )
    result = Comparable(quantity).evaluate(collection, env)
    assert result == []


def test_comparable_same_units_with_fhirpath():
    collection = [FHIRPathCollectionItem(value=Quantity(value=10, unit="mg"))]
    result = Comparable(EnvironmentVariable("%quantity")).evaluate(
        collection, {"%quantity": Quantity(value=12, unit="mg")}
    )
    assert result[0].value == True


def test_comparable_r4_fhir_quantity():
    collection = [FHIRPathCollectionItem(value=R4_Quantity(value=10, unit="mg"))]
    quantity = Quantity(
        value=12,
        unit="mg",
    )
    assert Comparable(quantity).single(collection, env) == True


def test_comparable_r4_fhir_quantity_subclass():
    collection = [
        FHIRPathCollectionItem(
            value=R4_Age(value=10, system="http://unitsofmeasure.org", code="a")
        )
    ]
    quantity = Quantity(
        value=12,
        unit="s",
    )
    assert Comparable(quantity).single(collection, env) == True


def test_comparable_r4b_fhir_quantity():
    collection = [
        FHIRPathCollectionItem(
            value=R4B_Quantity(value=10, system="http://unitsofmeasure.org", code="mg")
        )
    ]
    quantity = Quantity(
        value=12,
        unit="mg",
    )
    assert Comparable(quantity).single(collection, env) == True


def test_comparable_r5_fhir_quantity():
    collection = [
        FHIRPathCollectionItem(
            value=R5_Quantity(value=10, system="http://unitsofmeasure.org", code="mg")
        )
    ]
    quantity = Quantity(
        value=12,
        unit="mg",
    )
    assert Comparable(quantity).single(collection, env) == True


# -------------
# Resolve
# -------------


def test_resolve_returns_empty_for_empty_collection():
    collection = []
    result = Resolve().evaluate(collection, env)
    assert result == []


def test_resolve_with_non_url_value():
    collection = [FHIRPathCollectionItem(value="not-a-url")]
    result = Resolve().evaluate(collection, env)
    assert result == []


def test_resolve_with_r4b_reference():
    collection = [
        FHIRPathCollectionItem(
            value=R4B_Reference(reference="http://example.org/resource")
        )
    ]
    with pytest.warns(FHIRPathWarning, match="not supported"):
        result = Resolve().evaluate(collection, env)
    assert result == []


def test_resolve_with_r5_reference():
    collection = [
        FHIRPathCollectionItem(
            value=R5_Reference(reference="http://example.org/resource")
        )
    ]
    with pytest.warns(FHIRPathWarning, match="not supported"):
        result = Resolve().evaluate(collection, env)
    assert result == []


def test_resolve_with_internal_reference():
    contained_resource = {"id": "123", "resourceType": "Patient"}
    resource = {"contained": [contained_resource]}
    collection = [FHIRPathCollectionItem(value="#123")]
    result = Resolve().evaluate(collection, {"%resource": resource})
    assert result[0].value == contained_resource


def test_resolve_with_unresolvable_internal_reference():
    contained_resource = {"id": "123", "resourceType": "Patient"}
    resource = {"contained": [contained_resource]}
    collection = [FHIRPathCollectionItem(value="#1234")]
    result = Resolve().evaluate(collection, {"%resource": resource})
    assert result == []


def test_resolve_ignores_non_reference_items():
    contained_resource = {"id": "123", "resourceType": "Patient"}
    resource = {"contained": [contained_resource]}
    collection = [
        FHIRPathCollectionItem(value="#123"),
        FHIRPathCollectionItem(value=123),
    ]
    result = Resolve().evaluate(collection, {"%resource": resource})
    assert result[0].value == contained_resource


# -------------
# ConformsTo
# -------------


def test_conformsto_returns_empty_for_empty_collection():
    collection = []
    result = ConformsTo("http://hl7.org/fhir/StructureDefinition/Patient").evaluate(
        collection, env
    )
    assert result == []


def test_conformsto_returns_empty_for_non_singleton_collection():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = ConformsTo("http://hl7.org/fhir/StructureDefinition/Patient").evaluate(
        collection, env
    )
    assert result == []


def test_conformsto_raises_error_when_fhir_release_not_in_environment():
    collection = [FHIRPathCollectionItem(value={"resourceType": "Patient"})]
    with pytest.raises(FHIRPathException, match="required for evaluating conformsTo"):
        ConformsTo("http://hl7.org/fhir/StructureDefinition/Patient").evaluate(
            collection, {}
        )


def test_conformsto_returns_true_for_conforming_resource():
    collection = [
        FHIRPathCollectionItem(value={"resourceType": "Patient", "gender": "female"})
    ]
    result = ConformsTo("http://hl7.org/fhir/StructureDefinition/Patient").evaluate(
        collection, {"%fhirRelease": "R4"}
    )
    assert result[0].value == True


def test_conformsto_returns_false_for_non_conforming_resource():
    collection = [
        FHIRPathCollectionItem(
            value={"resourceType": "Observation", "valueCode": "female"}
        )
    ]
    result = ConformsTo("http://hl7.org/fhir/StructureDefinition/Patient").evaluate(
        collection, {"%fhirRelease": "R4"}
    )
    assert result[0].value == False


def test_conformsto_returns_empty_for_unresolvable_structure_definition():
    collection = [
        FHIRPathCollectionItem(value={"resourceType": "Patient", "gender": "female"})
    ]
    with pytest.warns(FHIRPathWarning, match="Could not resolve structure definition"):
        result = ConformsTo("http://example.org/StructureDefinition/Unknown").evaluate(
            collection, {"%fhirRelease": "R4"}
        )
    assert result == []


# -------------
# MemberOf
# -------------


def test_memberof_returns_empty_for_empty_collection():
    collection = []
    result = MemberOf("http://example.org/ValueSet/ExampleVS").evaluate(collection, env)
    assert result == []


def test_memberof_returns_false_for_invalid_code(terminology_service):
    collection = [FHIRPathCollectionItem(value="invalid-code")]
    result = MemberOf("http://example.org/ValueSet/ExampleVS").evaluate(
        collection,
        {"%fhirRelease": "R4", "%terminologyService": terminology_service},
    )
    assert result[0].value == False


def test_memberof_returns_false_for_invalid_coding(terminology_service):
    collection = [FHIRPathCollectionItem(value=R4_Coding(code="invalid-code"))]
    result = MemberOf("http://example.org/ValueSet/ExampleVS").evaluate(
        collection,
        {"%fhirRelease": "R4", "%terminologyService": terminology_service},
    )
    assert result[0].value == False


def test_memberof_returns_false_for_invalid_codeableconcept(terminology_service):
    collection = [
        FHIRPathCollectionItem(
            value=R4_CodeableConcept(coding=[R4_Coding(code="invalid-code")])
        )
    ]
    result = MemberOf("http://example.org/ValueSet/ExampleVS").evaluate(
        collection,
        {"%fhirRelease": "R4", "%terminologyService": terminology_service},
    )
    assert result[0].value == False


def test_memberof_returns_true_for_valid_code(terminology_service):
    collection = [FHIRPathCollectionItem(value="valid-code")]

    result = MemberOf("http://example.org/ValueSet/ExampleVS").evaluate(
        collection,
        {"%fhirRelease": "R4", "%terminologyService": terminology_service},
    )
    assert result[0].value == True


def test_memberof_returns_true_for_valid_coding(terminology_service):
    collection = [FHIRPathCollectionItem(value=R4_Coding(code="valid-code"))]
    result = MemberOf("http://example.org/ValueSet/ExampleVS").evaluate(
        collection,
        {"%fhirRelease": "R4", "%terminologyService": terminology_service},
    )
    assert result[0].value == True


def test_memberof_returns_true_for_valid_codeableconcept(terminology_service):
    collection = [
        FHIRPathCollectionItem(
            value=R4_CodeableConcept(coding=[R4_Coding(code="valid-code")])
        )
    ]
    result = MemberOf("http://example.org/ValueSet/ExampleVS").evaluate(
        collection,
        {"%fhirRelease": "R4", "%terminologyService": terminology_service},
    )
    assert result[0].value == True


def test_memberof_returns_empty_for_unresolvable_valueset(terminology_service):
    collection = [FHIRPathCollectionItem(value="valid-code")]
    with pytest.warns(
        FHIRPathWarning, match="Error during terminology service call in memberOf()"
    ):
        result = MemberOf("http://example.org/ValueSet/Unknown").evaluate(
            collection,
            {"%fhirRelease": "R4", "%terminologyService": terminology_service},
        )
    assert result == []


def test_memberof_raises_error_when_fhir_release_not_in_environment(
    terminology_service,
):
    collection = [FHIRPathCollectionItem(value="example-code")]
    with pytest.raises(FHIRPathException, match="required for evaluating memberOf"):
        MemberOf("http://example.org/ValueSet/ExampleVS").evaluate(
            collection, {"%terminologyService": terminology_service}
        )


# -------------
# Subsumes
# -------------


def test_subsumes_returns_empty_for_empty_collection():
    collection = []
    result = Subsumes(Element("example-code")).evaluate(collection, env)
    assert result == []


def test_subsumes_returns_true_for_subsuming_code(terminology_service):
    collection = [
        FHIRPathCollectionItem(
            value=R4_Coding(system="http://loinc.org", code="parent")
        )
    ]
    result = Subsumes(EnvironmentVariable("%otherCoding")).evaluate(
        collection,
        {
            "%fhirRelease": "R4",
            "%terminologyService": terminology_service,
            "%otherCoding": R4_Coding(system="http://loinc.org", code="child"),
        },
    )
    assert result[0].value == True


def test_subsumes_returns_false_for_non_subsuming_code(terminology_service):
    collection = [
        FHIRPathCollectionItem(value=R4_Coding(system="http://loinc.org", code="child"))
    ]
    result = Subsumes(EnvironmentVariable("%otherCoding")).evaluate(
        collection,
        {
            "%fhirRelease": "R4",
            "%terminologyService": terminology_service,
            "%otherCoding": R4_Coding(system="http://loinc.org", code="parent"),
        },
    )
    assert result[0].value == False


def test_subsumes_returns_empty_when_service_returns_none(terminology_service):
    collection = [
        FHIRPathCollectionItem(
            value=R4_Coding(system="http://loinc.org", code="unknown")
        )
    ]
    result = Subsumes(EnvironmentVariable("%otherCoding")).evaluate(
        collection,
        {
            "%fhirRelease": "R4",
            "%terminologyService": terminology_service,
            "%otherCoding": R4_Coding(system="http://loinc.org", code="child"),
        },
    )
    assert result == []


def test_subsumes_warns_and_returns_empty_when_service_raises(terminology_service):
    collection = [
        FHIRPathCollectionItem(value=R4_Coding(system="http://loinc.org", code="error"))
    ]
    with pytest.warns(
        FHIRPathWarning, match="Error during terminology service call in subsumes()"
    ):
        result = Subsumes(EnvironmentVariable("%otherCoding")).evaluate(
            collection,
            {
                "%fhirRelease": "R4",
                "%terminologyService": terminology_service,
                "%otherCoding": R4_Coding(system="http://loinc.org", code="child"),
            },
        )
    assert result == []


def test_subsumes_raises_error_when_fhir_release_not_in_environment(
    terminology_service,
):
    collection = [
        FHIRPathCollectionItem(
            value=R4_Coding(system="http://loinc.org", code="parent")
        )
    ]
    with pytest.raises(FHIRPathException, match="required for evaluating subsumes"):
        Subsumes(EnvironmentVariable("%otherCoding")).evaluate(
            collection,
            {
                "%terminologyService": terminology_service,
                "%otherCoding": R4_Coding(system="http://loinc.org", code="child"),
            },
        )


def test_subsumes_raises_error_for_different_code_systems(terminology_service):
    collection = [
        FHIRPathCollectionItem(
            value=R4_Coding(system="http://loinc.org", code="parent")
        )
    ]
    with pytest.raises(
        FHIRPathException, match="Subsumption across different code systems"
    ):
        Subsumes(EnvironmentVariable("%otherCoding")).evaluate(
            collection,
            {
                "%fhirRelease": "R4",
                "%terminologyService": terminology_service,
                "%otherCoding": R4_Coding(
                    system="http://snomed.info/sct", code="child"
                ),
            },
        )


# -------------
# SubsumedBy
# -------------


def test_subsumedby_returns_empty_for_empty_collection():
    collection = []
    result = SubsumedBy(Element("example-code")).evaluate(collection, env)
    assert result == []


def test_subsumedby_returns_true_for_subsumed_code(terminology_service):
    collection = [
        FHIRPathCollectionItem(value=R4_Coding(system="http://loinc.org", code="child"))
    ]
    result = SubsumedBy(EnvironmentVariable("%otherCoding")).evaluate(
        collection,
        {
            "%fhirRelease": "R4",
            "%terminologyService": terminology_service,
            "%otherCoding": R4_Coding(system="http://loinc.org", code="parent"),
        },
    )
    assert result[0].value == True


def test_subsumedby_returns_false_for_non_subsumed_code(terminology_service):
    collection = [
        FHIRPathCollectionItem(
            value=R4_Coding(system="http://loinc.org", code="parent")
        )
    ]
    result = SubsumedBy(EnvironmentVariable("%otherCoding")).evaluate(
        collection,
        {
            "%fhirRelease": "R4",
            "%terminologyService": terminology_service,
            "%otherCoding": R4_Coding(system="http://loinc.org", code="child"),
        },
    )
    assert result[0].value == False


def test_subsumedby_returns_empty_when_service_returns_none(terminology_service):
    collection = [
        FHIRPathCollectionItem(
            value=R4_Coding(system="http://loinc.org", code="unknown")
        )
    ]
    result = SubsumedBy(EnvironmentVariable("%otherCoding")).evaluate(
        collection,
        {
            "%fhirRelease": "R4",
            "%terminologyService": terminology_service,
            "%otherCoding": R4_Coding(system="http://loinc.org", code="child"),
        },
    )
    assert result == []


def test_subsumedby_raises_error_when_fhir_release_not_in_environment(
    terminology_service,
):
    collection = [
        FHIRPathCollectionItem(value=R4_Coding(system="http://loinc.org", code="child"))
    ]
    with pytest.raises(FHIRPathException, match="required for evaluating"):
        SubsumedBy(EnvironmentVariable("%otherCoding")).evaluate(
            collection,
            {
                "%terminologyService": terminology_service,
                "%otherCoding": R4_Coding(system="http://loinc.org", code="parent"),
            },
        )


def test_subsumedby_raises_error_for_different_code_systems(terminology_service):
    collection = [
        FHIRPathCollectionItem(value=R4_Coding(system="http://loinc.org", code="child"))
    ]
    with pytest.raises(
        FHIRPathException,
        match="Subsumption across different code systems",
    ):
        SubsumedBy(EnvironmentVariable("%otherCoding")).evaluate(
            collection,
            {
                "%fhirRelease": "R4",
                "%terminologyService": terminology_service,
                "%otherCoding": R4_Coding(
                    system="http://snomed.info/sct", code="parent"
                ),
            },
        )
