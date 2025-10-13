from copy import copy
from typing import ClassVar

from pydantic import BaseModel, ValidationError
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from fhircraft.fhir.path.mixin import FHIRPathMixin
from fhircraft.utils import get_all_models_from_field


class FHIRBaseModel(BaseModel, FHIRPathMixin):
    """
    Base class for representation of FHIR resources as Pydantic objects.

    Expands the Pydantic [BaseModel](https://docs.pydantic.dev/latest/api/base_model/) class with FHIR-specific methods.
    """

    def model_dump(self, *args, **kwargs):
        kwargs.update({"by_alias": True, "exclude_none": True})
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        kwargs.update({"by_alias": True, "exclude_none": True})
        return super().model_dump_json(*args, **kwargs)

    @classmethod
    def model_construct(cls, set_defaults=True, *args, **kwargs) -> object:
        """
        Constructs a model without running validation, with an option to set default values for fields that have them defined.

        Args:
            set_defaults (bool): Optional, if `True`, sets default values for fields that have them defined (default is `True`).

        Returns:
            instance (Self): An instance of the model.
        """
        instance = super().model_construct(*args, **kwargs)
        if not set_defaults:
            return instance
        # Set default values for fields that have them defined
        for field_name, field in cls.model_fields.items():
            if getattr(instance, field_name, None) is not None:
                continue
            if field.default not in (PydanticUndefined, None):
                setattr(instance, field_name, copy(field.default))
            elif field.default_factory not in (PydanticUndefined, None):
                setattr(instance, field_name, field.default_factory)
        return instance

    @classmethod
    def model_construct_with_slices(cls, slice_copies: int = 9) -> object:
        """
        Constructs a model with sliced elements by creating empty slice instances based on the specified number of slice copies.
        The method iterates over the sliced elements of the class, generates slice resources, and sets them in the resource collection.

        Args:
            slice_copies (int): Optional, an integer specifying the number of copies for each slice (default is 9).

        Returns:
            instance (Self): An instance of the model with the sliced elements constructed.
        """
        from fhircraft.fhir.path import fhirpath

        instance = super().model_construct()
        for element, slices in cls.get_sliced_elements().items():
            slice_resources = []
            for slice in slices:
                # Add empty slice instances
                slice_resources.extend(
                    [
                        slice.model_construct_with_slices()
                        for _ in range(min(slice.max_cardinality, slice_copies))
                    ]
                )
            # Set the whole list of slices in the resource
            collection = fhirpath.parse(element).__evaluate_wrapped(
                instance, create=True
            )
            [item.set_literal(slice_resources) for item in collection]
        return instance

    @classmethod
    def get_sliced_elements(cls) -> dict[str, list[type["FHIRSliceModel"]]]:
        """
        Get the sliced elements from the model fields and their extension fields.
        Sliced elements are filtered based on being instances of `FHIRSliceModel`.

        Returns:
            slices (dict): A dictionary with field names as keys and corresponding sliced elements as values.
        """
        # Get model elements' extension fields
        extensions = {
            f"{field_name}.extension": next(
                (
                    arg.model_fields.get("extension")
                    for arg in get_all_models_from_field(field)
                    if arg.model_fields.get("extension")
                ),
                None,
            )
            for field_name, field in cls.model_fields.items()
            if field_name != "extension"
        }
        fields = {
            **cls.model_fields,
            **extensions,
        }
        # Compile the sliced elements in the model
        return {
            field_name: slices
            for field_name, field in fields.items()
            if field
            and bool(
                slices := list(
                    get_all_models_from_field(field, issubclass_of=FHIRSliceModel)
                )
            )
        }

    @classmethod
    def clean_unusued_slice_instances(cls, resource):
        """
        Cleans up unused or incomplete slice instances within the given FHIR resource by iterating through the
        sliced elements of the class, identifying valid elements, and updating the resource with only the valid slices.
        """
        from fhircraft.fhir.path import fhirpath

        # Remove unused/incomplete slices
        for element, slices in cls.get_sliced_elements().items():
            valid_elements = [
                col.value
                for col in fhirpath.parse(element).__evaluate_wrapped(
                    resource, create=True
                )
                if col.value is not None
            ]
            new_valid_elements = []
            if not valid_elements:
                continue
            for slice in slices:
                # Get all the elements that conform to this slice's definition
                sliced_entries = [
                    entry for entry in valid_elements if isinstance(entry, slice)
                ]
                for entry in sliced_entries:
                    if slice.get_sliced_elements():
                        entry = slice.clean_unusued_slice_instances(entry)
                    if (entry.is_FHIR_complete and entry.has_been_modified) or (
                        entry.is_FHIR_complete
                        and not entry.has_been_modified
                        and slice.min_cardinality > 0
                    ):
                        if entry not in new_valid_elements:
                            new_valid_elements.append(entry)
            # Set the new list with only the valid slices
            collection = fhirpath.parse(element).__evaluate_wrapped(
                resource, create=True
            )
            [col.set_literal(new_valid_elements) for col in collection]
        return resource

    def __repr__(self) -> str:
        repr_args = []
        for fieldname in self.model_fields_set or self.__class__.model_fields:
            value = getattr(self, fieldname)
            repr_args.append(f"{fieldname}={value}")
        return f"{self.__class__.__name__}({', '.join(repr_args)})"


class FHIRSliceModel(FHIRBaseModel):
    """
    Base class for representation of FHIR profiled slices as Pydantic objects.

    Expands the `FHIRBaseModel` class with slice-specific methods.
    """

    min_cardinality: ClassVar[int] = 0
    max_cardinality: ClassVar[int] = 1

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
