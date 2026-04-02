from .uri import Uri


class Canonical(Uri):
    """A URI that refers to a resource by its canonical URL."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/canonical"
    _type = "canonical"
