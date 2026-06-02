"""
The functions in this section operate on collections with a single item. If there is more than one item, or an item that is not a String, the evaluation of the expression will end and signal an error to the calling environment.

To use these functions over a collection with multiple items, one may use filters like `where()` and `select()`:

    Patient.name.given.select(substring(0))
"""

__all__ = [
    "IndexOf",
    "Substring",
    "StartsWith",
    "EndsWith",
    "Contains",
    "Upper",
    "Lower",
    "Replace",
    "Matches",
    "ReplaceMatches",
    "ToChars",
    "Length",
    "Concatenation",

]

import re
from typing import Any, List, Optional

from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathFunction,
    Literal,
)
from fhircraft.exceptions import FhirPathException
from fhircraft.fhir.path.utils import (
    evaluate_and_prepare_collection_values,
    get_expression_context,
)


class StringManipulationFunction(FHIRPathFunction):
    """
    Abstract class definition for category of string manipulation FHIRPath functions.
    """

    def validate_collection(self, collection: FHIRPathCollection) -> str:
        """
        Validates the input collection of a FHIRPath string manipulation function.

        Args:
            collection (FHIRPathCollection): Collection to be validated.

        Returns:
            str: The validated string from the collection.

        Raises:
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.
        """
        from fhircraft.fhir.resources.datatypes.R4.primitive import String as R4_String
        from fhircraft.fhir.resources.datatypes.R4B.primitive import (
            String as R4B_String,
        )
        from fhircraft.fhir.resources.datatypes.R5.primitive import String as R5_String

        if len(collection) > 1:
            raise FhirPathException(
                f"FHIRPath function {self.__str__()} expected a single-item collection, instead got a {len(collection)}-items collection."
            )
        value = collection[0].value
        if (
            isinstance(value, (R4_String, R4B_String, R5_String))
            and value.value is not None
        ):
            return value.value
        elif isinstance(value, str):
            return value
        else:
            raise FhirPathException(
                f"FHIRPath function {self.__str__()} expected a string, instead got a {type(collection[0].value)}"
            )


class IndexOf(StringManipulationFunction):
    """
    A representation of the FHIRPath [`indexOf()`](https://hl7.org/fhirpath/N1/#indexofsubstring-string-integer) function.

    Attributes:
        substring (str | FHIRPath): Subtring query or FHIRPath that resolves to a string..
    """

    def __init__(self, substring: str | FHIRPath):
        if isinstance(substring, str):
            substring = Literal(substring)
        if not isinstance(substring, FHIRPath):
            raise FhirPathException(
                "IndexOf() argument must be a literal string or a valid FHIRPath."
            )
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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.

        """
        from fhircraft.fhir.resources.base import StringBase

        if not collection:
            return []
        string_item = self.validate_collection(collection)
        # Get string value
        string_item = collection[0].value
        # Update the evaluation context
        environment = get_expression_context(environment, item=string_item, index=0)
        if not isinstance(
            substring := self.substring.single(collection, environment=environment),
            (str, StringBase),
        ) or (
            isinstance(substring, StringBase) and (substring := substring.value) is None
        ):
            raise FhirPathException(
                "IndexOf() argument must resolve in a non-empty string."
            )
        return [FHIRPathCollectionItem.wrap(collection[0].value.find(substring))]


class Substring(StringManipulationFunction):
    """
    A representation of the FHIRPath [`substring()`](https://hl7.org/fhirpath/N1/#substringstart-integer-length-integer-string) function.

    Attributes:
        start (int | FHIRPath): Start index of the substring  or FHIRPath that resolves to an integer.
        end (Optional[int | FHIRPath]): Optional, end index of the substring  or FHIRPath that resolves to an integer.
    """

    def __init__(self, start: int | FHIRPath, end: int | FHIRPath | None = None):
        self.start: FHIRPath = Literal(start) if isinstance(start, int) else start
        self.end: FHIRPath | None = Literal(end) if isinstance(end, int) else end

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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.

        """
        from fhircraft.fhir.resources.base import IntegerBase

        if not collection:
            return []
        string_item = self.validate_collection(collection)
        # Update the evaluation context
        environment = get_expression_context(
            environment, item=FHIRPathCollectionItem.wrap(string_item), index=0
        )
        # Get start and end positions
        if not isinstance(
            (start := self.start.single(collection, environment=environment)),
            (int, IntegerBase),
        ) or (isinstance(start, IntegerBase) and (start := start.value) is None):
            raise FhirPathException(
                "Substring() start argument must resolve to an integer."
            )
        end = self.end.single(collection, environment=environment) if self.end else None
        if (
            (
                end := (
                    self.end.single(collection, environment=environment)
                    if self.end
                    else None
                )
            )
            and not isinstance(end, (int, IntegerBase))
            or (isinstance(end, IntegerBase) and (end := end.value) is None)
        ):
            raise FhirPathException("Substring() end argument must resolve to an integer.")

        if start > len(string_item) - 1:
            return []
        # Apply substring extraction
        if end is None:
            return [FHIRPathCollectionItem.wrap(string_item[start:])]
        else:
            return [FHIRPathCollectionItem.wrap(string_item[start:end])]


class StartsWith(StringManipulationFunction):
    """
    A representation of the FHIRPath [`startsWith()`](https://hl7.org/fhirpath/N1/#startswithprefix-string-boolean) function.

    Attributes:
        prefix (str | FHIRPath): String prefix to query or FHIRPath that resolves to a string..
    """

    def __init__(self, prefix: str | FHIRPath):
        if isinstance(prefix, str):
            prefix = Literal(prefix)
        if not isinstance(prefix, FHIRPath):
            raise FhirPathException(
                "StartsWith() argument must be a string literal or a valid FHIRPath."
            )
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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.

        """
        from fhircraft.fhir.resources.base import StringBase

        if not collection:
            return []
        string_item = self.validate_collection(collection)
        # Update the evaluation context
        environment = get_expression_context(
            environment, item=FHIRPathCollectionItem.wrap(string_item), index=0
        )
        # Get prefix value
        if not isinstance(
            prefix := self.prefix.single(collection, environment=environment),
            (str, StringBase),
        ) or (isinstance(prefix, StringBase) and (prefix := prefix.value) is None):
            raise FhirPathException("StartsWith() argument must resolve to a string.")
        if not prefix:
            return [FHIRPathCollectionItem.wrap(True)]
        # Check for prefix presence
        return [FHIRPathCollectionItem.wrap(string_item.startswith(prefix))]


class EndsWith(StringManipulationFunction):
    """
    A representation of the FHIRPath [`endsWith()`](https://hl7.org/fhirpath/N1/#endswithsuffix-string-boolean) function.

    Attributes:
        suffix (str | FHIRPath): String suffix to query  or FHIRPath that resolves to a string.
    """

    def __init__(self, suffix: str | FHIRPath):
        if isinstance(suffix, str):
            suffix = Literal(suffix)
        if not isinstance(suffix, FHIRPath):
            raise FhirPathException(
                "EndsWith() argument must be a string literal or a valid FHIRPath."
            )
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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.

        """
        from fhircraft.fhir.resources.base import StringBase

        if not collection:
            return []
        string_item = self.validate_collection(collection)
        # Update the evaluation context
        environment = get_expression_context(
            environment, item=FHIRPathCollectionItem.wrap(string_item), index=0
        )
        # Get suffix value
        if not isinstance(
            suffix := self.suffix.single(collection, environment=environment),
            (str, StringBase),
        ) or (isinstance(suffix, StringBase) and (suffix := suffix.value) is None):
            raise FhirPathException("EndsWith() argument must resolve to a string.")
        if not suffix:
            return [FHIRPathCollectionItem.wrap(True)]
        # Check for suffix presence
        return [FHIRPathCollectionItem.wrap(string_item.endswith(suffix))]


class Contains(StringManipulationFunction):
    """
    A representation of the FHIRPath [`contains()`](https://hl7.org/fhirpath/N1/#containssubstring-string-boolean) function.

    Attributes:
        substring (str | FHIRPath): Substring to query or FHIRPath that resolves to a string.
    """

    def __init__(self, substring: str | FHIRPath):
        if isinstance(substring, str):
            substring = Literal(substring)
        if not isinstance(substring, FHIRPath):
            raise FhirPathException(
                "Contains() argument must be a string literal or a valid FHIRPath."
            )
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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.

        Note:
            Note: The FHIRPath `.contains()` function described here is a string function that looks
            for a substring in a string. This is different than the `contains` FHIRPath operator, which
            is a list operator that looks for an element in a list.

        """
        from fhircraft.fhir.resources.base import StringBase

        if not collection:
            return []
        string_item = self.validate_collection(collection)
        # Update the evaluation context
        environment = get_expression_context(
            environment, item=FHIRPathCollectionItem.wrap(string_item), index=0
        )
        # Get substring value
        if not isinstance(
            substring := self.substring.single(collection, environment=environment),
            (str, StringBase),
        ) or (
            isinstance(substring, StringBase) and (substring := substring.value) is None
        ):
            raise FhirPathException("Contains() argument must resolve to a string.")
        if not substring:
            return [FHIRPathCollectionItem.wrap(True)]
        # Check for substring presence
        return [FHIRPathCollectionItem.wrap(substring in string_item)]


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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.
        """
        if not collection:
            return []
        string_item = self.validate_collection(collection)
        # Apply upper case transformation
        return [FHIRPathCollectionItem.wrap(string_item.upper())]


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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.
        """
        if not collection:
            return []
        string_item = self.validate_collection(collection)
        # Apply lower case transformation
        return [FHIRPathCollectionItem.wrap(string_item.lower())]


class Replace(StringManipulationFunction):
    """
    A representation of the FHIRPath [`replace()`](https://hl7.org/fhirpath/N1/#replacepattern-string-substitution-string-string) function.

    Attributes:
        pattern (str | FHIRPath): Substring to substitute or FHIRPath that resolves to a string.
        substitution (str | FHIRPath): String to substitute `pattern` with or FHIRPath that resolves to a string.
    """

    def __init__(
        self,
        pattern: str | FHIRPath | FHIRPathCollection,
        substitution: str | FHIRPath | FHIRPathCollection,
    ):
        if isinstance(pattern, str):
            self.pattern = Literal(pattern)
        elif isinstance(pattern, list):
            if len(pattern) > 0 and isinstance(pattern[0], FHIRPathCollectionItem):
                self.pattern = (
                    Literal(pattern[0])
                    if not isinstance(pattern[0], Literal)
                    else pattern[0]
                )
            else:
                self.pattern = Literal(None)
        elif isinstance(pattern, FHIRPath):
            self.pattern = pattern
        else:
            raise FhirPathException(
                "Replace() pattern argument must be a string literal or valid FHIRPath."
            )

        if isinstance(substitution, str):
            self.substitution = Literal(substitution)
        elif isinstance(substitution, list):
            if len(substitution) > 0 and isinstance(
                substitution[0], FHIRPathCollectionItem
            ):
                self.substitution = (
                    Literal(substitution[0])
                    if not isinstance(substitution[0], Literal)
                    else substitution[0]
                )
            else:
                self.substitution = Literal(None)
        elif isinstance(substitution, FHIRPath):
            self.substitution = substitution
        else:
            raise FhirPathException(
                "Replace() substitution argument must be a string literal or valid FHIRPath."
            )

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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.
        """
        from fhircraft.fhir.resources.base import StringBase

        if not collection:
            return []
        string_item = self.validate_collection(collection)
        # Update the evaluation context
        environment = get_expression_context(
            environment, item=FHIRPathCollectionItem.wrap(string_item), index=0
        )
        # Validate pattern and substitution
        if self.substitution.is_empty(
            collection, environment=environment
        ) or self.pattern.is_empty(collection, environment=environment):
            return []
        # Get pattern and substitution values
        if not isinstance(
            pattern := self.pattern.single(collection, environment=environment),
            (str, StringBase),
        ) or (isinstance(pattern, StringBase) and (pattern := pattern.value) is None):
            raise FhirPathException("Replace() pattern argument must resolve to a string.")
        if not isinstance(
            substitution := self.substitution.single(
                collection, environment=environment
            ),
            (str, StringBase),
        ) or (
            isinstance(substitution, StringBase)
            and (substitution := substitution.value) is None
        ):
            raise FhirPathException(
                "Replace() substitution argument must resolve to a string."
            )
        # Apply replacement
        return [FHIRPathCollectionItem.wrap(string_item.replace(pattern, substitution))]


class Matches(StringManipulationFunction):
    """
    A representation of the FHIRPath [`matches()`](https://hl7.org/fhirpath/N1/#matchesregex-string-boolean) function.

    Attributes:
        regex (str | FHIRPath): Regular expression to match or FHIRPath that resolves to a string.
    """

    def __init__(self, regex: str | FHIRPath):
        if isinstance(regex, str):
            regex = Literal(regex)
        if not isinstance(regex, FHIRPath):
            raise FhirPathException(
                "Matches() argument must be a string literal or valid FHIRPath."
            )
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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.
        """
        from fhircraft.fhir.resources.base import StringBase

        if not collection:
            return []
        string_item = self.validate_collection(collection)
        # Update the evaluation context
        environment = get_expression_context(
            environment, item=FHIRPathCollectionItem.wrap(string_item), index=0
        )
        # Get regex value
        if self.regex.is_empty(collection, environment=environment):
            return []
        if not isinstance(
            regex := self.regex.single(collection, environment=environment),
            (str, StringBase),
        ) or (isinstance(regex, StringBase) and (regex := regex.value) is None):
            raise FhirPathException("Matches() argument must resolve to a string.")
        # Apply regex match
        return [FHIRPathCollectionItem.wrap(bool(re.match(regex, string_item)))]


class ReplaceMatches(StringManipulationFunction):
    """
    A representation of the FHIRPath [`replaceMatches()`](https://hl7.org/fhirpath/N1/#replacematchesregex-string-substitution-string-string) function.

    Attributes:
        regex (str | FHIRPath): Regular expression to substitute or FHIRPath that resolves to a string.
        substitution (str | FHIRPath): String to substitute `regex` with or FHIRPath that resolves to a string.
    """

    def __init__(self, regex: str | FHIRPath, substitution: str | FHIRPath):
        if isinstance(regex, str):
            regex = Literal(regex)
        if not isinstance(regex, FHIRPath):
            raise FhirPathException(
                "ReplaceMatches() regex argument must be a string literal or valid FHIRPath."
            )
        if isinstance(substitution, str):
            substitution = Literal(substitution)
        if not isinstance(substitution, FHIRPath):
            raise FhirPathException(
                "ReplaceMatches() substitution argument must be a string literal or valid FHIRPath."
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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.
        """
        from fhircraft.fhir.resources.base import StringBase

        if not collection:
            return []
        string_item = self.validate_collection(collection)
        # Update the evaluation context
        environment = get_expression_context(
            environment, item=FHIRPathCollectionItem.wrap(string_item), index=0
        )
        # Validate pattern and substitution
        if self.regex.is_empty(
            collection, environment=environment
        ) or self.substitution.is_empty(collection, environment=environment):
            return []
        if not isinstance(
            regex := self.regex.single(collection, environment=environment),
            (str, StringBase),
        ) or (isinstance(regex, StringBase) and (regex := regex.value) is None):
            raise FhirPathException(
                "ReplaceMatches() regex argument must resolve to a string."
            )
        if not isinstance(
            substitution := self.substitution.single(
                collection, environment=environment
            ),
            (str, StringBase),
        ) or (
            isinstance(substitution, StringBase)
            and (substitution := substitution.value) is None
        ):
            raise FhirPathException(
                "ReplaceMatches() substitution argument must resolve to a string."
            )
        return [FHIRPathCollectionItem.wrap(re.sub(regex, substitution, string_item))]


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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.
        """
        if not collection:
            return []
        string_item = self.validate_collection(collection)
        return [FHIRPathCollectionItem.wrap(len(string_item))]


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
            FhirPathException: If input collection has more than one item.
            FhirPathException: If the item in the input collection is not a string.
        """
        if not collection:
            return []
        string_item = self.validate_collection(collection)
        return [FHIRPathCollectionItem.wrap(character) for character in string_item]


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
            FhirPathException: If either expression evaluates to a non-singleton collection.
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
        left_value = left_value or ""
        right_value = right_value or ""
        return [FHIRPathCollectionItem.wrap(f"{left_value}{right_value}")]

    def __str__(self):
        return f"{self.left} & {self.right}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left!s}, {self.right!s})"

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and other.left == self.left
            and other.right == self.right
        )

    def __hash__(self):
        return hash((self.left, self.right))
