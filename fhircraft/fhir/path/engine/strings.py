
"""
The functions in this section operate on collections with a single item. If there is more than one item, or an item that is not a String, the evaluation of the expression will end and signal an error to the calling environment.

To use these functions over a collection with multiple items, one may use filters like `where()` and `select()`:
    
    Patient.name.given.select(substring(0))
"""

from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, FHIRPathFunction, FHIRPathError, FHIRPath
from fhircraft.utils import ensure_list
from typing import List, Any, Optional
import re 

class StringManipulationFunction(FHIRPathFunction):    
    """
    Abstract class definition for category of string manipulation FHIRPath functions. 
    """
    def validate_collection(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> List[FHIRPathCollectionItem]:
        """
        Validates the input collection of a FHIRPath string manipulation function. 

        Args: 
            collection (List[FHIRPathCollectionItem]): Collection to be validated.

        Returns: 
            collection (List[FHIRPathCollectionItem]): Validated collection.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """
        collection = ensure_list(collection)
        if len(collection)>1:
            raise FHIRPathError(f'FHIRPath function {self.__str__()} expected a single-item collection, instead got a {len(collection)}-items collection.')
        if len(collection) == 1 and not isinstance(collection[0].value, str):
            raise FHIRPathError(f'FHIRPath function {self.__str__()} expected a string, instead got a {type(collection[0])}')
        return collection 
    

class IndexOf(StringManipulationFunction):
    """
    A representation of the FHIRPath [`indexOf()`](https://hl7.org/fhirpath/N1/#indexofsubstring-string-integer) function.

    Attributes:
        substring (str): Subtring query.
    """
    def __init__(self, substring: str):
        self.substring =substring

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> int:
        """
        Returns the 0-based index of the first position substring is found in the input string, 
        or `-1` if it is not found.
        If substring is an empty string (`''`), the function returns `0`.
        If the input or substring is empty (`[]`), the result is empty (`[]`).

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            index (int): Index of the first position of `substring`.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
            
        """ 
        collection = super().validate_collection(collection)
        if len(collection)==0:
            return []
        return collection[0].value.find(self.substring)


class Substring(StringManipulationFunction):
    """
    A representation of the FHIRPath [`substring()`](https://hl7.org/fhirpath/N1/#substringstart-integer-length-integer-string) function.

    Attributes:
        start (int): Start index of the substring.
        end (Optional[int]): End index of the substring.
    """
    def __init__(self, start: int, end: Optional[int]=None):
        self.start = start
        self.end = end

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> str:
        """
        Returns the part of the string starting at position start (zero-based). If length is given, will
        return at most length number of characters from the input string.
        If start lies outside the length of the string, the function returns empty (`[]`). If there are
        less remaining characters in the string than indicated by length, the function returns just the 
        remaining characters.
        If the input or start is empty, the result is empty.
        If an empty length is provided, the behavior is the same as if length had not been provided.


        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            substring (str): The substring indexed by the `start` and `end` indices.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
            
        """ 
        collection = super().validate_collection(collection)
        if not collection or not self.start:
            return []
        if not self.end:
            return collection[0].value[self.start:]
        return collection[0].value[self.start:self.end]



class StartsWith(StringManipulationFunction):
    """
    A representation of the FHIRPath [`startsWith()`](https://hl7.org/fhirpath/N1/#startswithprefix-string-boolean) function.

    Attributes:
        prefix (str): String prefix to query.
    """
    def __init__(self, prefix: str):
        self.prefix = prefix

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Returns true when the input string starts with the given prefix.
        If prefix is the empty string (`''`), the result is `True`.
        If the input collection is empty, the result is empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            (bool): Whether the string starts with `prefix`.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
            
        """ 
        collection = super().validate_collection(collection)
        if not collection or not self.prefix:
            return []
        return collection[0].value.startswith(self.prefix)



class EndsWith(StringManipulationFunction):
    """
    A representation of the FHIRPath [`endsWith()`](https://hl7.org/fhirpath/N1/#endswithsuffix-string-boolean) function.

    Attributes:
        suffix (str): String suffix to query.
    """
    def __init__(self, suffix: str):
        self.suffix = suffix

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Returns true when the input string ends with the given suffix.
        If suffix is the empty string (`''`), the result is `True`.
        If the input collection is empty, the result is empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            (bool): Whether the string ends with `suffix`.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
            
        """ 
        collection = super().validate_collection(collection)
        if not collection or not self.suffix:
            return []
        return collection[0].value.endswith(self.suffix)




class Contains(StringManipulationFunction):
    """
    A representation of the FHIRPath [`contains()`](https://hl7.org/fhirpath/N1/#containssubstring-string-boolean) function.

    Attributes:
        substring (str): Substring to query.
    """
    def __init__(self, substring: str):
        self.substring = substring

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Returns true when the given substring is a substring of the input string.
        If substring is the empty string (`''`), the result is `True`.
        If the input collection is empty, the result is empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            (bool): Whether the string contains `substring`.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.

        Note:
            Note: The FHIRPath `.contains()` function described here is a string function that looks
            for a substring in a string. This is different than the `contains` FHIRPath operator, which
            is a list operator that looks for an element in a list.   

        """ 
        collection = super().validate_collection(collection)
        if not collection or not self.substring:
            return []
        return self.substring in collection[0].value 


class Upper(StringManipulationFunction):
    """
    A representation of the FHIRPath [`upper()`](https://hl7.org/fhirpath/N1/#upper-string) function.
    """
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> str:
        """
        Returns the input string with all characters converted to upper case.
        If the input collection is empty, the result is empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            string (str): Upper case string.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """ 
        collection = super().validate_collection(collection)
        if not collection:
            return []
        return collection[0].value.upper()


class Lower(StringManipulationFunction):
    """
    A representation of the FHIRPath [`lower()`](https://hl7.org/fhirpath/N1/#lower-string) function.
    """
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> str:
        """
        Returns the input string with all characters converted to lower case.
        If the input collection is empty, the result is empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            string (str): Lower case string.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """ 
        collection = super().validate_collection(collection)
        if not collection:
            return []
        return collection[0].value.lower()



class Replace(StringManipulationFunction):
    """
    A representation of the FHIRPath [`replace()`](https://hl7.org/fhirpath/N1/#replacepattern-string-substitution-string-string) function.

    Attributes:
        pattern (str): Substring to substitute. 
        substitution (str): String to substitute `pattern` with.
    """
    def __init__(self, pattern: str, substitution: str):
        self.pattern = pattern
        self.substitution = substitution
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> str:
        """
        Returns the input string with all instances of `pattern` replaced with `substitution`. 
        If the substitution is the empty string (`''`), instances of pattern are removed from the result.
        If pattern is the empty string (`''`), every character in the input string is surrounded by 
        the substitution, e.g. `'abc'.replace('','x')` becomes `'xaxbxcx'`.
        If the input collection, pattern, or substitution are empty, the result is empty ({ }).

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            string (str): Substituted string

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """ 
        collection = super().validate_collection(collection)
        if not collection or not self.substitution:
            return []
        return collection[0].value.replace(self.pattern, self.substitution)


class Matches(StringManipulationFunction):
    """
    A representation of the FHIRPath [`matches()`](https://hl7.org/fhirpath/N1/#matchesregex-string-boolean) function.

    Attributes:
        regex (str): Regular expression to match. 
    """
    def __init__(self, regex: str):
        self.regex = regex

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        Returns `True` when the value matches the given regular expression. Regular expressions
        should function consistently, regardless of any culture- and locale-specific settings
        in the environment, should be case-sensitive, use 'single line' mode and allow Unicode characters.
        If the input collection or regex are empty, the result is empty (`[]`).

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            (bool): Whether string matches the regular expression `regex`.

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """ 
        collection = super().validate_collection(collection)
        if not collection or not self.regex:
            return []
        return bool(re.match(self.regex, collection[0].value))


class ReplaceMatches(StringManipulationFunction):
    """
    A representation of the FHIRPath [`replaceMatches()`](https://hl7.org/fhirpath/N1/#replacematchesregex-string-substitution-string-string) function.

    Attributes:
        regex (str): Regular expression to substitute. 
        substitution (str): String to substitute `regex` with.
    """
    def __init__(self, regex: str, substitution: str):
        self.regex = regex
        self.substitution = substitution
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> str:
        """
        Matches the input using the regular expression in regex and replaces each match with the 
        substitution string. The substitution may refer to identified match groups in the regular expression.
        If the input collection, regex, or substitution are empty, the result is empty (`[]`).

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            string (str): Substituted string

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """ 
        collection = super().validate_collection(collection)
        if not collection or not self.regex or not self.substitution:
            return []
        return re.sub(self.regex, self.substitution, collection[0].value)
    
    
class Length(StringManipulationFunction):
    """
    A representation of the FHIRPath [`length()`](https://hl7.org/fhirpath/N1/#length-integer) function.
    """
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> int:
        """
        Returns the length of the input string. If the input collection is empty (`[]`), the result is empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            length (int): Length of the string

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """ 
        collection = super().validate_collection(collection)
        if not collection:
            return []
        return len(collection[0].value)


class ToChars(StringManipulationFunction):
    """
    A representation of the FHIRPath [`toChars()`](https://hl7.org/fhirpath/N1/#length-integer) function.
    """
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> int:
        """
        Returns the list of characters in the input string. If the input collection is empty (`[]`), the result is empty.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            characters (List[FHIRPathCollectionItem])): Collection of characters in the string

        Raises:
            FHIRPathError: If input collection has more than one item.
            FHIRPathError: If the item in the input collection is not a string.
        """ 
        collection = super().validate_collection(collection)
        if not collection:
            return []
        return [FHIRPathCollectionItem(character, parent=collection[0]) for character in collection[0].value]


class Concatenation(FHIRPath):
    """
    A representation of the FHIRPath [`&`](https://hl7.org/fhirpath/N1/#and) operator.

    Attributes:
        left (FHIRPath): Left operand.
        right (FHIRPath): Right operand.
    """
    def __init__(self, left: FHIRPath, right:FHIRPath):
        self.left = left
        self.right = right
        
    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> bool:
        """
        For strings, will concatenate the strings, where an empty operand is taken to be the empty string.
        This differs from + on two strings, which will result in an empty collection when one of the operands
        is empty. This operator is specifically included to simplify treating an empty collection as an empty
        string, a common use case in string manipulation.


        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            result (str): Concatenated string

        Raises:
            FHIRPathError: If either expression evaluates to a non-singleton collection.
        """
        create = kwargs.get('create')
        left_collection = [
            item.value if isinstance(item, FHIRPathCollectionItem) else item 
                for item in ensure_list(self.left.evaluate(collection, create))
        ]  if isinstance(self.left, FHIRPath) else ensure_list(self.left)

        right_collection = [ 
            item.value if isinstance(item, FHIRPathCollectionItem) else item  
                for item in ensure_list(self.right.evaluate(collection, create))
        ] if isinstance(self.right, FHIRPath) else ensure_list(self.right)

        if len(left_collection)>1:
            raise FHIRPathError(f'FHIRPath operator {self.__str__()} expected a single-item collection for the left expression, instead got a {len(collection)}-items collection.')
        if len(left_collection)>1:
            raise FHIRPathError(f'FHIRPath operator {self.__str__()} expected a single-item collection for the right expression, instead got a {len(collection)}-items collection.')
        
        left =  left_collection[0] if len(left_collection) > 0 else '' 
        right =  right_collection[0] if len(right_collection) > 0 else ''

        return f'{left}{right}'

    def __str__(self):
        return f'{self.__class__.__name__.lower()}({self.left.__str__(), self.right.__str__()})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left.__repr__(), self.right.__repr__()})'
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((self.left, self.right))
