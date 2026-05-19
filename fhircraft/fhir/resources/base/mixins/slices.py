"""
FHIR profile-slice construction and introspection mixin for FHIRBaseModel.
"""

from typing import TYPE_CHECKING

from fhircraft.utils import get_all_models_from_field

if TYPE_CHECKING:
    from fhircraft.fhir.resources.base.model import FHIRBaseModel


class FHIRSliceMixin:
    """
    Mixin providing FHIR profile-slice construction and introspection.

    Adds ``model_construct_with_slices`` for building skeleton instances that
    include empty slice entries, and ``get_sliced_elements`` for reflecting on
    which fields contain profiled slices.
    """

    @classmethod
    def model_construct_with_slices(cls, slice_copies: int = 9) -> "FHIRBaseModel":
        """
        Construct a model instance pre-populated with empty slice placeholders.

        Iterates over all sliced elements in the model, creates the appropriate
        number of empty slice instances (bounded by each slice's max cardinality
        and *slice_copies*), and injects them via FHIRPath.

        Args:
            slice_copies: Maximum number of copies per slice to generate
                (default 9, capped further by the slice's own max cardinality).

        Returns:
            A model instance with slice placeholders in place.
        """
        from fhircraft.fhir.path.parser import fhirpath

        instance = super().model_construct()  # type: ignore[misc]
        for element, slices in cls.get_sliced_elements().items():
            slice_resources: list = []
            for slc in slices:
                slice_resources.extend(
                    slc.model_construct_with_slices()
                    for _ in range(min(slc.max_cardinality or 9999, slice_copies))
                )
            collection = fhirpath.parse(element).__evaluate_wrapped(
                instance, create=True
            )
            for item in collection:
                item.set_literal(slice_resources)
        return instance  # type: ignore[return-value]

    @classmethod
    def get_sliced_elements(cls) -> "dict[str, list]":
        """
        Discover all profiled slices defined on this model's fields.

        Inspects both top-level fields and the extension sub-fields of complex
        elements.  Only fields whose type is a subclass of ``FHIRSliceModel``
        are included.

        Returns:
            A dict mapping FHIRPath-style element expressions (e.g.
            ``"extension"`` or ``"component.extension"``) to a list of the
            concrete ``FHIRSliceModel`` subclasses present on that element.
        """
        from fhircraft.fhir.resources.base.slices import FHIRSliceModel

        # Collect extension sub-fields from complex-type fields.
        extension_fields: dict = {
            f"{field_name}.extension": next(
                (
                    arg.model_fields.get("extension")
                    for arg in get_all_models_from_field(field)
                    if arg.model_fields.get("extension")
                ),
                None,
            )
            for field_name, field in cls.model_fields.items()  # type: ignore[attr-defined]
            if field_name != "extension"
        }
        all_fields = {**cls.model_fields, **extension_fields}  # type: ignore[attr-defined]

        return {
            field_name: slices
            for field_name, field in all_fields.items()
            if field
            and bool(
                slices := list(
                    get_all_models_from_field(field, issubclass_of=FHIRSliceModel)
                )
            )
        }
