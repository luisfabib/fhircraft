import re
from typing import TYPE_CHECKING, Any, Union

from fhircraft.utils import ensure_list

if TYPE_CHECKING:
    from fhircraft.fhir.path.engine.core import FHIRPath, FHIRPathCollection

from fhircraft.fhir.path.engine.literals import Quantity
from fhircraft.fhir.path.exceptions import FHIRPathRuntimeError


def split_fhirpath(fhir_path: str) -> list[str]:
    """
    Split a FHIR path string at non-quoted dots.

    Args:
        fhir_path (str): The FHIR path string to split.

    Returns:
        List[str]: A list of strings resulting from splitting the FHIR path at non-quoted dots.

    Example:
        This shows how to safely split a FHIRPath string into segments:

        ``` python
        >>> from fhircraft.fhir.path.utils import join_fhirpath
        >>> split_fhirpath("Observation.components.where(code.coding.code='123')"])
        ["Observation","components","where(code.coding.code='123')"]
        ```
    """
    FHIRPATH_SEPARATORS = re.compile(r"\.(?=(?:[^\)]*\([^\(]*\))*[^\(\)]*$)")
    # Split FHIR path only at non-quoted dots
    return FHIRPATH_SEPARATORS.split(fhir_path)


def join_fhirpath(*segments: str) -> str:
    """
    Join multiple FHIR path segments into a single FHIR path string.

    Args:
        segments (str): Variable number of FHIR path segments to join.

    Returns:
        str: A single FHIR path string created by joining the input segments with dots.

    Example:
        This shows how to join a list of FHIRPath segments irrespectively of the separators:

        ``` python
        >>> from fhircraft.fhir.path.utils import join_fhirpath
        >>> join_fhirpath(['Patient','.name','given.'])
        Patient.name.given
        ```
    """
    return ".".join((str(segment).strip(".") for segment in segments if segment != ""))


def _underline_error_in_fhir_path(fhir_path, error, error_position):
    return f'{fhir_path[:error_position+len(str(error))+15]}...\n{" "*error_position}{"—"*len(str(error))}'


def import_fhirpath_engine():
    from fhircraft.fhir.path import fhirpath

    return fhirpath


def evaluate_fhirpath_collection(
    fhir_path: Union["FHIRPath", "FHIRPathCollection"],
    collection: "FHIRPathCollection",
    create: bool = False,
) -> "FHIRPathCollection":
    from fhircraft.fhir.path.engine.core import FHIRPath, FHIRPathCollectionItem

    return (
        [item for item in fhir_path.evaluate(collection, create)]
        if isinstance(fhir_path, FHIRPath)
        else [FHIRPathCollectionItem.wrap(item) for item in ensure_list(fhir_path)]
    )


def evaluate_left_right_expressions(
    left: Union["FHIRPath", "FHIRPathCollection"],
    right: Union["FHIRPath", "FHIRPathCollection"],
    collection: "FHIRPathCollection",
    create: "bool",
) -> tuple["FHIRPathCollection", "FHIRPathCollection"]:
    """
    Evaluates the given left and right FHIRPath expressions or collections against the provided collection,
    optionally creating new elements, and returns the resulting collections of values.

    Args:
        left (FHIRPath | FHIRPathCollection): The left operand, which can be a FHIRPath expression or a collection of values.
        right (FHIRPath | FHIRPathCollection): The right operand, which can be a FHIRPath expression or a collection of values.
        collection (FHIRPathCollection): The collection to evaluate the expressions against.
        create (bool): Whether to create new elements during evaluation if necessary.

    Returns:
        tuple[FHIRPathCollection, FHIRPathCollection]: A tuple containing the evaluated left and right collections of values.
    """
    left_collection = evaluate_fhirpath_collection(left, collection, create)
    right_collection = evaluate_fhirpath_collection(right, collection, create)
    return left_collection, right_collection


def evaluate_and_prepare_collection_values(
    operator: "FHIRPath",
    left: Union["FHIRPath", "FHIRPathCollection"],
    right: Union["FHIRPath", "FHIRPathCollection"],
    collection: "FHIRPathCollection",
    create=False,
    prevent_all_empty: bool = True,
) -> tuple[Any | None, Any | None]:

    def _get_collection_values(collection: "FHIRPathCollection") -> list[Any]:
        return [
            (
                Quantity(item.value.value, item.value.unit)
                if "Quantity" in type(item.value).__name__
                else item.value
            )
            for item in collection
        ]

    left_collection, right_collection = evaluate_left_right_expressions(
        left, right, collection, create
    )
    left_collection = _get_collection_values(left_collection)
    right_collection = _get_collection_values(right_collection)

    if len(left_collection) > 1:
        raise FHIRPathRuntimeError(
            f"FHIRPath operator {operator.__str__()} expected a single-item collection for the left expression, instead got a {len(collection)}-items collection."
        )
    if len(right_collection) > 1:
        raise FHIRPathRuntimeError(
            f"FHIRPath operator {operator.__str__()} expected a single-item collection for the right expression, instead got a {len(collection)}-items collection."
        )
    if prevent_all_empty and (len(left_collection) == 0 or len(right_collection) == 0):
        return None, None
    else:
        if len(left_collection) == 0:
            left_collection = [None]
        if len(right_collection) == 0:
            right_collection = [None]
    return left_collection[0], right_collection[0]
