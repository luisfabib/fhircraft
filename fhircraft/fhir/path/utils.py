"""
FHIRPath utility functions for parsing, evaluating, and handling FHIRPath 
expressions and collections.
"""
import re
import threading
from typing import Any, Dict, Union, TYPE_CHECKING

from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, FHIRPath, Literal
from fhircraft.utils import ensure_list
from fhircraft.exceptions import FHIRPathRuntimeError

if TYPE_CHECKING:
    from fhircraft.fhir.path.parser import FHIRPathParser

FHIRPATH_SEPARATORS = re.compile(r"\.(?=(?:[^\)]*\([^\(]*\))*[^\(\)]*$)")
    
# Singleton parser instance with thread-safe initialization
_parser_instance: "FHIRPathParser | None" = None
_parser_lock = threading.Lock()

__all__ = [
    "parse_fhirpath",
]

def parse_fhirpath(expression: str) -> "FHIRPath":
    """
    Parses a FHIRPath expression string into a FHIRPath object.

    Uses a thread-safe singleton instance of FHIRPathParser for efficiency.

    Args:
        expression (str): The FHIRPath expression string to parse.

    Returns:
        FHIRPath: The parsed FHIRPath object representing the expression.
    
    Example:
        This shows how to parse a FHIRPath expression string into a FHIRPath object:
        ``` python
        >>> from fhircraft.fhir.path.utils import parse_fhirpath
        >>> parse_fhirpath("Observation.components.where(code.coding.code='123')")
        FHIRPath(Observation.components.where(code.coding.code='123'))
        ```
    """
    return _get_parser().parse(expression)

def _get_parser():
    """Get or create the singleton FHIRPathParser instance in a thread-safe manner."""
    global _parser_instance
    if _parser_instance is None:
        with _parser_lock:
            if _parser_instance is None:
                from fhircraft.fhir.path.parser import FHIRPathParser

                _parser_instance = FHIRPathParser()
    return _parser_instance


def _underline_error_in_fhir_path(text, error, error_position, line_number=None):
    """
    Underlines the error in a FHIR path string, supporting multiline strings and optional line number.

    Args:
        text (str): The FHIR path string (may be multiline).
        error (Any): The error object or message.
        error_position (int): The position (character index) of the error in the string.
        line_number (int, optional): The line number where the error occurred (1-based).

    Returns:
        str: A string with the error underlined, optionally prefixed with the line number.
    """
    lines = text.splitlines()
    if line_number is not None and 1 <= line_number <= len(lines):
        line = lines[line_number - 1]
        error_pos_in_line = error_position - 1
        underline = " " * error_pos_in_line + "—" * len(str(error))
        return f'\nLine {line_number}: {line}\n{" " * (len(f"Line {line_number}: "))}{underline}'
    else:
        underline = " " * error_position + "—" * len(str(error))
        return f"{text[:error_position+len(str(error))+15]}...\n{underline}"




def _evaluate_fhirpath_collection(
    fhir_path: Union["FHIRPath", "FHIRPathCollection"],
    collection: "FHIRPathCollection",
    environment: dict,
    create: bool = False,
) -> "FHIRPathCollection":
    """
    Evaluates a FHIRPath expression or collection against a given collection and environment, optionally creating new elements.

    Args:
        fhir_path (FHIRPath | FHIRPathCollection): The FHIRPath expression or collection to evaluate.
        collection (FHIRPathCollection): The collection to evaluate the expression against.
        environment (dict): The evaluation environment containing variable bindings.
        create (bool): Whether to create new elements during evaluation if necessary.

    Returns:
        FHIRPathCollection: The resulting collection after evaluation.
    """
    return (
        [item for item in fhir_path.evaluate(collection, environment, create)]
        if isinstance(fhir_path, FHIRPath)
        else [FHIRPathCollectionItem.wrap(item) for item in ensure_list(fhir_path)]
    )


def _evaluate_left_right_expressions(
    left: Union["FHIRPath", "FHIRPathCollection"],
    right: Union["FHIRPath", "FHIRPathCollection"],
    collection: "FHIRPathCollection",
    environment: dict,
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
    left_collection = _evaluate_fhirpath_collection(
        left, collection, environment, create
    )
    right_collection = _evaluate_fhirpath_collection(
        right, collection, environment, create
    )
    return left_collection, right_collection


def _evaluate_and_prepare_collection_values(
    operator: "FHIRPath",
    left: Union["FHIRPath", "FHIRPathCollection"],
    right: Union["FHIRPath", "FHIRPathCollection"],
    collection: "FHIRPathCollection",
    environment: dict,
    create=False,
    prevent_all_empty: bool = True,
) -> tuple[Any | None, Any | None]:
    """
    Evaluates the left and right FHIRPath expressions or collections, prepares their values for comparison, and returns them.

    Args:
        operator (FHIRPath): The FHIRPath operator being evaluated, used for error messages.
        left (FHIRPath | FHIRPathCollection): The left operand, which can be a FHIRPath expression or a collection of values.
        right (FHIRPath | FHIRPathCollection): The right operand, which can be a FHIRPath expression or a collection of values.
        collection (FHIRPathCollection): The collection to evaluate the expressions against.
        environment (dict): The evaluation environment containing variable bindings.
        create (bool): Whether to create new elements during evaluation if necessary.
        prevent_all_empty (bool): If True, returns None for both values if either collection is empty; otherwise treats empty collections as [None].

    Returns:
        tuple[Any | None, Any | None]: A tuple containing the prepared left and right values for comparison, or None if prevented by empty collections.
    """

    def _get_collection_values(collection: "FHIRPathCollection") -> list[Any]:
        from fhircraft.fhir.path.engine.literals import Quantity

        return [
            (
                Quantity.parse_quantity(data)
                if Quantity.is_quantity(data := item.value) and data.value is not None
                else data
            )
            for item in collection
        ]

    left_collection, right_collection = _evaluate_left_right_expressions(
        left, right, collection, environment, create
    )
    left_collection = _get_collection_values(left_collection)
    right_collection = _get_collection_values(right_collection)

    if len(left_collection) > 1:
        raise FHIRPathRuntimeError(
            f"FHIRPath operator {operator} expected a single-item collection for the left expression, instead got a {len(left_collection)}-items collection."
        )
    if len(right_collection) > 1:
        raise FHIRPathRuntimeError(
            f"FHIRPath operator {operator} expected a single-item collection for the right expression, instead got a {len(right_collection)}-items collection."
        )
    if prevent_all_empty and (len(left_collection) == 0 or len(right_collection) == 0):
        return None, None
    else:
        if len(left_collection) == 0:
            left_collection = [None]
        if len(right_collection) == 0:
            right_collection = [None]
    left_value = left_collection[0]
    right_value = right_collection[0]
    if isinstance(left_value, Literal):
        left_value = left_value.value
    if isinstance(right_value, Literal):
        right_value = right_value.value
    return left_value, right_value


def _get_expression_context(
    environment: Dict[str, FHIRPathCollectionItem],
    item: FHIRPathCollectionItem,
    index: int,
) -> dict:
    """ 
    Creates a new evaluation context for a FHIRPath expression by copying the existing environment
    and adding the current item and index.

    Args:
        environment (Dict[str, FHIRPathCollectionItem]): The existing evaluation environment containing variable bindings.
        item (FHIRPathCollectionItem): The current item being evaluated, to be added to the context as $this.
        index (int): The index of the current item in the collection, to be added to the context as $index.
    
    Returns:
        dict: A new evaluation context dictionary containing the existing environment plus $this and $index.
    """
    context = environment.copy()
    context["$this"] = item
    context["$index"] = FHIRPathCollectionItem.wrap(index)
    return context
