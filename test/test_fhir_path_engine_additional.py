from collections import namedtuple

from fhircraft.fhir.path.engine.additional import *
from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.resources.datatypes import get_complex_FHIR_type

env = dict()

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
            get_complex_FHIR_type("Extension")(
                url="http://domain.org/extension1", valueInteger=1
            ),
            get_complex_FHIR_type("Extension")(
                url="http://domain.org/extension2", valueInteger=2
            ),
            get_complex_FHIR_type("Extension")(
                url="http://domain.org/extension3", valueInteger=3
            ),
        ]
    )
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Extension("http://domain.org/extension2").evaluate(collection, env)
    assert result[0].value == resource.extension[1]


# -------------
# HasValue
# -------------


def test_hasvalue_returns_false_for_empty_collection():
    collection = []
    result = HasValue().evaluate(collection, env)
    assert result[0].value == False


def test_hasvaslue_returns_true_for_singleton_collection_with_value():
    collection = [FHIRPathCollectionItem(value=1)]
    result = HasValue().evaluate(collection, env)
    assert result[0].value == True


def test_hasvaslue_returns_true_for_singleton_collection_without_value():
    collection = [FHIRPathCollectionItem(value=None)]
    result = HasValue().evaluate(collection, env)
    assert result[0].value == False


def test_hasvaslue_returns_false_for_collection_with_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = HasValue().evaluate(collection, env)
    assert result[0].value == False


# -------------
# GetValue
# -------------


def test_getvalue_returns_empty_for_empty_collection():
    collection = []
    result = GetValue().evaluate(collection, env)
    assert result == []


def test_getvalue_returns_true_for_singleton_collection_with_value():
    collection = [FHIRPathCollectionItem(value=1)]
    result = GetValue().evaluate(collection, env)
    assert result[0].value == 1


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


def test_lowboundary_quantity():
    """Test low boundary for Quantity objects"""
    from test.test_fhir_path_engine_conversion import Quantity

    quantity = Quantity(
        value=10.5, unit="kg", system="http://unitsofmeasure.org", code="kg"
    )
    collection = [FHIRPathCollectionItem(value=quantity)]
    result = LowBoundary().evaluate(collection, env)

    assert result[0].value.value == 10.5 - sys.float_info.epsilon
    assert result[0].value.unit == "kg"
    assert result[0].value.system == "http://unitsofmeasure.org"
    assert result[0].value.code == "kg"


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


def test_highboundary_quantity():
    """Test high boundary for Quantity objects"""
    from test.test_fhir_path_engine_conversion import Quantity

    quantity = Quantity(
        value=10.5, unit="kg", system="http://unitsofmeasure.org", code="kg"
    )
    collection = [FHIRPathCollectionItem(value=quantity)]
    result = HighBoundary().evaluate(collection, env)

    assert result[0].value.value == 10.5 + sys.float_info.epsilon
    assert result[0].value.unit == "kg"
    assert result[0].value.system == "http://unitsofmeasure.org"
    assert result[0].value.code == "kg"


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
