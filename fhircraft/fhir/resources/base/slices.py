from typing import ClassVar
from pydantic import ValidationError

from fhircraft.fhir.resources.base import FHIRBaseModel


class FHIRSliceModel(FHIRBaseModel):
    """
    Base class for representation of FHIR profiled slices as Pydantic objects.

    Expands the `FHIRBaseModel` class with slice-specific methods.
    """

    min_cardinality: ClassVar[int] = 0
    max_cardinality: ClassVar[int | None] = None

    @property
    def is_FHIR_complete(self):
        """
        Validates if the FHIR model is complete by attempting to validate the model dump.
        Returns `True` if the model is complete, `False` otherwise.
        """
        model = self.__class__
        try:
            model.model_validate(self.model_dump())
            return True
        except ValidationError:
            return False

    @property
    def has_been_modified(self):
        """
        Checks if the FHIRSliceModel instance has been modified by comparing it with a new instance constructed with slices.
        Returns `True` if the instance has been modified, `False` otherwise.
        """
        return self != self.__class__.model_construct_with_slices()
