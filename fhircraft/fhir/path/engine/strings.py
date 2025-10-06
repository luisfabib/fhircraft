"""
The functions in this section operate on collections with a single item. If there is more than one item, or an item that is not a String, the evaluation of the expression will end and signal an error to the calling environment.

To use these functions over a collection with multiple items, one may use filters like `where()` and `select()`:

    Patient.name.given.select(substring(0))
"""

import re
from typing import Any, List, Optional

from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathFunction,
    Literal,
)
from fhircraft.fhir.path.exceptions import FHIRPathError
from fhircraft.fhir.path.utils import evaluate_and_prepare_collection_values


class StringManipulationFunction(FHIRPathFunction):
    """
    Abstract class definition for category of string manipulation FHIRPath functions.
    """

    def validate_collection(self, collection: FHIRPathCollection):
        """
        Validates the input collection of a FHIRPath string manipulation function.

        Args:
            collection (FHIRPathCollection): Collection to be validated.

        Returns:
            (FHIRPathCollection): The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """
        if len(collection) > 1:
            raise FHIRPathError(
                f"FHIRPath function {self.__str__()} expected a single-item collection, instead got a {len(collection)}-items collection."
            )
        if len(collection) == 1 and not isinstance(collection[0].value, str):
            raise FHIRPathError(
                f"FHIRPath function {self.__str__()} expected a string, instead got a {type(collection[0])}"
            )


class IndexOf(StringManipulationFunction):
    """
    A representation of the FHIRPath [`indexOf()`](https://hl7.org/fhirpath/N1/#indexofsubstring-string-integer) function.

    Attributes:
        substring (str): Subtring query.
    """

    def __init__(self, substring: str | Literal):
        if isinstance(substring, str):
            substring = Literal(substring)
        if not isinstance(substring, Literal):
            raise FHIRPathError("IndexOf() argument must be a literal string.")
        self.substring = substring

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the 0-based index of the first position substring is found in the input string,
        or `-1` if it is not found.
        If substring is an empty string (`''`), the function returns `0`.
        If the input or substring is empty (`[]`), the result is empty (`[]`).

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.

        """
        self.validate_collection(collection)
        if len(collection) == 0:
            return []
        return [
            FHIRPathCollectionItem.wrap(collection[0].value.find(self.substring.value))
        ]


class Substring(StringManipulationFunction):
    """
    A representation of the FHIRPath [`substring()`](https://hl7.org/fhirpath/N1/#substringstart-integer-length-integer-string) function.

    Attributes:
        start (int): Start index of the substring.
        end (Optional[int]): End index of the substring.
    """

    def __init__(self, start: int | Literal, end: int | Literal | None = None):
        self.start: int = start.value if isinstance(start, Literal) else start
        self.end: int | None = end.value if isinstance(end, Literal) else end

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the part of the string starting at position start (zero-based). If length is given, will
        return at most length number of characters from the input string.
        If start lies outside the length of the string, the function returns empty (`[]`). If there are
        less remaining characters in the string than indicated by length, the function returns just the
        remaining characters.
        If the input or start is empty, the result is empty.
        If an empty length is provided, the behavior is the same as if length had not been provided.


        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.

        """
        self.validate_collection(collection)
        if not collection or self.start > len(collection[0].value) - 1:
            return []
        if self.end is None:
            return [FHIRPathCollectionItem.wrap(collection[0].value[self.start :])]
        return [FHIRPathCollectionItem.wrap(collection[0].value[self.start : self.end])]


class StartsWith(StringManipulationFunction):
    """
    A representation of the FHIRPath [`startsWith()`](https://hl7.org/fhirpath/N1/#startswithprefix-string-boolean) function.

    Attributes:
        prefix (str): String prefix to query.
    """

    def __init__(self, prefix: str | Literal):
        if isinstance(prefix, str):
            prefix = Literal(prefix)
        if not isinstance(prefix, Literal):
            raise FHIRPathError("StartsWith() argument must be a string literal.")
        self.prefix = prefix

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns true when the input string starts with the given prefix.
        If prefix is the empty string (`''`), the result is `True`.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.

        """
        self.validate_collection(collection)
        if not collection or not self.prefix.value:
            return []
        prefix_collection = self.prefix.evaluate(collection, environment, create)
        if not prefix_collection:
            return []
        prefix = prefix_collection[0].value
        return [FHIRPathCollectionItem.wrap(collection[0].value.startswith(prefix))]


class EndsWith(StringManipulationFunction):
    """
    A representation of the FHIRPath [`endsWith()`](https://hl7.org/fhirpath/N1/#endswithsuffix-string-boolean) function.

    Attributes:
        suffix (str): String suffix to query.
    """

    def __init__(self, suffix: str | Literal):
        if isinstance(suffix, str):
            suffix = Literal(suffix)
        if not isinstance(suffix, Literal):
            raise FHIRPathError("EndsWith() argument must be a string literal.")
        self.suffix = suffix

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns true when the input string ends with the given suffix.
        If suffix is the empty string (`''`), the result is `True`.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.

        """
        self.validate_collection(collection)
        if not collection or not self.suffix.value:
            return []
        return [
            FHIRPathCollectionItem.wrap(collection[0].value.endswith(self.suffix.value))
        ]


class Contains(StringManipulationFunction):
    """
    A representation of the FHIRPath [`contains()`](https://hl7.org/fhirpath/N1/#containssubstring-string-boolean) function.

    Attributes:
        substring (str): Substring to query.
    """

    def __init__(self, substring: str | Literal):
        if isinstance(substring, str):
            substring = Literal(substring)
        if not isinstance(substring, Literal):
            raise FHIRPathError("Contains() argument must be a string literal.")
        self.substring = substring

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns true when the given substring is a substring of the input string.
        If substring is the empty string (`''`), the result is `True`.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.

        Note:
            Note: The FHIRPath `.contains()` function described here is a string function that looks
            for a substring in a string. This is different than the `contains` FHIRPath operator, which
            is a list operator that looks for an element in a list.

        """
        self.validate_collection(collection)
        if not collection or not self.substring.value:
            return []
        return [
            FHIRPathCollectionItem.wrap(self.substring.value in collection[0].value)
        ]


class Upper(StringManipulationFunction):
    """
    A representation of the FHIRPath [`upper()`](https://hl7.org/fhirpath/N1/#upper-string) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the input string with all characters converted to upper case.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [FHIRPathCollectionItem.wrap(collection[0].value.upper())]


class Lower(StringManipulationFunction):
    """
    A representation of the FHIRPath [`lower()`](https://hl7.org/fhirpath/N1/#lower-string) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the input string with all characters converted to lower case.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [FHIRPathCollectionItem.wrap(collection[0].value.lower())]


class Replace(StringManipulationFunction):
    """
    A representation of the FHIRPath [`replace()`](https://hl7.org/fhirpath/N1/#replacepattern-string-substitution-string-string) function.

    Attributes:
        pattern (str): Substring to substitute.
        substitution (str): String to substitute `pattern` with.
    """

    def __init__(self, pattern: str | Literal, substitution: str | Literal):
        if isinstance(pattern, str):
            pattern = Literal(pattern)
        if not isinstance(pattern, Literal):
            raise FHIRPathError("Replace() pattern argument must be a string literal.")
        if isinstance(substitution, str):
            substitution = Literal(substitution)
        if not isinstance(substitution, Literal):
            raise FHIRPathError(
                "Replace() substitution argument must be a string literal."
            )
        self.pattern = pattern
        self.substitution = substitution

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the input string with all instances of `pattern` replaced with `substitution`.
        If the substitution is the empty string (`''`), instances of pattern are removed from the result.
        If pattern is the empty string (`''`), every character in the input string is surrounded by
        the substitution, e.g. `'abc'.replace('','x')` becomes `'xaxbxcx'`.
        If the input collection, pattern, or substitution are empty, the result is empty ({ }).

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """
        self.validate_collection(collection)
        if not collection or not self.substitution.value:
            return []
        return [
            FHIRPathCollectionItem.wrap(
                collection[0].value.replace(self.pattern.value, self.substitution.value)
            )
        ]


class Matches(StringManipulationFunction):
    """
    A representation of the FHIRPath [`matches()`](https://hl7.org/fhirpath/N1/#matchesregex-string-boolean) function.

    Attributes:
        regex (str): Regular expression to match.
    """

    def __init__(self, regex: str | Literal):
        if isinstance(regex, str):
            regex = Literal(regex)
        if not isinstance(regex, Literal):
            raise FHIRPathError("Matches() argument must be a string literal.")
        self.regex = regex

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns `True` when the value matches the given regular expression. Regular expressions
        should function consistently, regardless of any culture- and locale-specific settings
        in the environment, should be case-sensitive, use 'single line' mode and allow Unicode characters.
        If the input collection or regex are empty, the result is empty (`[]`).

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """
        self.validate_collection(collection)
        if not collection or not self.regex.value:
            return []
        return [
            FHIRPathCollectionItem.wrap(
                bool(re.match(self.regex.value, collection[0].value))
            )
        ]


class ReplaceMatches(StringManipulationFunction):
    """
    A representation of the FHIRPath [`replaceMatches()`](https://hl7.org/fhirpath/N1/#replacematchesregex-string-substitution-string-string) function.

    Attributes:
        regex (str): Regular expression to substitute.
        substitution (str): String to substitute `regex` with.
    """

    def __init__(self, regex: str | Literal, substitution: str | Literal):
        if isinstance(regex, str):
            regex = Literal(regex)
        if not isinstance(regex, Literal):
            raise FHIRPathError(
                "ReplaceMatches() regex argument must be a string literal."
            )
        if isinstance(substitution, str):
            substitution = Literal(substitution)
        if not isinstance(substitution, Literal):
            raise FHIRPathError(
                "ReplaceMatches() substitution argument must be a string literal."
            )
        self.regex = regex
        self.substitution = substitution

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Matches the input using the regular expression in regex and replaces each match with the
        substitution string. The substitution may refer to identified match groups in the regular expression.
        If the input collection, regex, or substitution are empty, the result is empty (`[]`).

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """
        self.validate_collection(collection)
        if not collection or not self.regex or not self.substitution:
            return []
        return [
            FHIRPathCollectionItem.wrap(
                re.sub(self.regex.value, self.substitution.value, collection[0].value)
            )
        ]


class Length(StringManipulationFunction):
    """
    A representation of the FHIRPath [`length()`](https://hl7.org/fhirpath/N1/#length-integer) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the length of the input string. If the input collection is empty (`[]`), the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [FHIRPathCollectionItem.wrap(len(collection[0].value))]


class ToChars(StringManipulationFunction):
    """
    A representation of the FHIRPath [`toChars()`](https://hl7.org/fhirpath/N1/#length-integer) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        Returns the list of characters in the input string. If the input collection is empty (`[]`), the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [
            FHIRPathCollectionItem(character, parent=collection[0])
            for character in collection[0].value
        ]


class Concatenation(FHIRPath):
    """
    A representation of the FHIRPath [`&`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath | FHIRPathCollection): Left operand.
        right (FHIRPath | FHIRPathCollection): Right operand.
    """

    def __init__(
        self, left: FHIRPath | FHIRPathCollection, right: FHIRPath | FHIRPathCollection
    ):
        self.left = left
        self.right = right

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        For strings, will concatenate the strings, where an empty operand is taken to be the empty string.
        This differs from + on two strings, which will result in an empty collection when one of the operands
        is empty. This operator is specifically included to simplify treating an empty collection as an empty
        string, a common use case in string manipulation.


        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection.

        Raises:
            FHIRPathError: If either expression evaluates to a non-singleton collection.
        """
        left_value, right_value = evaluate_and_prepare_collection_values(
            self,
            self.left,
            self.right,
            collection,
            environment,
            create,
            prevent_all_empty=False,
        )
        left_value = left_value or [""]
        right_value = right_value or [""]
        left = left_value[0]
        right = right_value[0]
        return [FHIRPathCollectionItem.wrap(f"{left}{right}")]

    def __str__(self):
        return f"{self.left} & {self.right}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))
