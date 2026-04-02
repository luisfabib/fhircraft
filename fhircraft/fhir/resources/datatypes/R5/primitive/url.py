from .uri import Uri


class Url(Uri):
    """A Uniform Resource Locator."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/url"
    _type = "url"
