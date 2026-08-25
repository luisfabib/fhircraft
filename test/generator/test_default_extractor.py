import pytest

from fhircraft.fhir.resources.generator._defaults import DefaultExtractor


@pytest.fixture
def extractor():
    return DefaultExtractor()


class TestExtractDefaultFactory:
    def test_list_builtin(self, extractor):
        assert extractor.extract_default_factory(list) == "list"

    def test_dict_builtin(self, extractor):
        assert extractor.extract_default_factory(dict) == "dict"

    def test_set_builtin(self, extractor):
        assert extractor.extract_default_factory(set) == "set"

    def test_tuple_builtin(self, extractor):
        assert extractor.extract_default_factory(tuple) == "tuple"

    def test_frozenset_builtin(self, extractor):
        assert extractor.extract_default_factory(frozenset) == "frozenset"

    def test_lambda_returning_literal(self, extractor):
        fn = lambda: []  # noqa: E731
        result = extractor.extract_default_factory(fn)
        assert result.startswith("lambda:")

    def test_fallback_for_uninspectable(self, extractor):
        # A C-extension callable has no inspectable source
        result = extractor.extract_default_factory(len)
        assert result.startswith("lambda:")

    def test_returns_string(self, extractor):
        result = extractor.extract_default_factory(list)
        assert isinstance(result, str)
