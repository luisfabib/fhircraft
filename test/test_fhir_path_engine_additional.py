from collections import namedtuple

from fhircraft.fhir.path.engine.additional import *
from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.resources.datatypes import get_complex_FHIR_type

# -------------
# Extension
# -------------


def test_extension_returns_empty_for_empty_collection():
    collection = []
    result = Extension("").evaluate(collection)
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
    result = Extension("http://domain.org/extension2").evaluate(collection)
    assert result[0].value == resource.extension[1]


# -------------
# HasValue
# -------------


def test_hasvalue_returns_false_for_empty_collection():
    collection = []
    result = HasValue().evaluate(collection)
    assert result[0].value == False


def test_hasvaslue_returns_true_for_singleton_collection_with_value():
    collection = [FHIRPathCollectionItem(value=1)]
    result = HasValue().evaluate(collection)
    assert result[0].value == True


def test_hasvaslue_returns_true_for_singleton_collection_without_value():
    collection = [FHIRPathCollectionItem(value=None)]
    result = HasValue().evaluate(collection)
    assert result[0].value == False


def test_hasvaslue_returns_false_for_collection_with_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = HasValue().evaluate(collection)
    assert result[0].value == False


# -------------
# GetValue
# -------------


def test_getvalue_returns_empty_for_empty_collection():
    collection = []
    result = GetValue().evaluate(collection)
    assert result == []


def test_getvalue_returns_true_for_singleton_collection_with_value():
    collection = [FHIRPathCollectionItem(value=1)]
    result = GetValue().evaluate(collection)
    assert result[0].value == 1


def test_getvalue_returns_empty_for_collection_with_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    result = GetValue().evaluate(collection)
    assert result == []


# -------------
# HtmlChecks
# -------------


def test_htmlchecks_returns_empty_for_empty_collection():
    collection = []
    result = HtmlChecks().evaluate(collection)
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
    result = HtmlChecks().evaluate(collection)
    assert result[0].value == False


def test_htmlchecks_invalid_empty_div():
    html_snippet = """
    <div xmlns=\"http://www.w3.org/1999/xhtml\"></div>
    """
    collection = [FHIRPathCollectionItem(value=html_snippet)]
    result = HtmlChecks().evaluate(collection)
    assert result[0].value == False


def test_htmlchecks_valid_xhtml():
    html_snippet = """
    <div xmlns=\"http://www.w3.org/1999/xhtml\">text</div>
    """
    collection = [FHIRPathCollectionItem(value=html_snippet)]
    result = HtmlChecks().evaluate(collection)
    assert result[0].value == True
