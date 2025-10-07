"""
FHIRPath defines both implicit and explicit conversion. Implicit conversions occur automatically, as opposed to explicit conversions
that require a function in this section to be called explicitly.
"""

import re

import fhircraft.fhir.resources.datatypes.primitives as primitives
from fhircraft.fhir.path.engine.core import (
    FHIRPath,
    FHIRPathCollection,
    FHIRPathCollectionItem,
    FHIRPathFunction,
)
from fhircraft.fhir.path.exceptions import FHIRPathRuntimeError
from fhircraft.fhir.path.utils import get_expression_context


class Iif(FHIRPathFunction):
    """
    A representation of the FHIRPath [`iif()`](http://hl7.org/fhirpath/N1/#iifcriterion-expression-true-result-collection-otherwise-result-collection-collection) function.

    Args:
        criterion (FHIRPath): The criterion expression,  is expected to evaluate to a `Boolean`.
        true_result (Union[FHIRPath, Any]): Value to be returned if `criterion` evaluates to `True`
        otherwise_result (Optional[Union[FHIRPath, Any]]): Value to be returned if `criterion` evaluates to `False`. Defaults to an empty collection.
    """

    def __init__(
        self,
        criterion: FHIRPath,
        true_result: FHIRPath | FHIRPathCollection,
        otherwise_result: FHIRPath | FHIRPathCollection = list(),
    ):
        self.criterion = criterion
        self.true_result = true_result
        self.otherwise_result = otherwise_result

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        This function acts as an immediate if, also known as a conditional operator.

        If `criterion` evaluates to `True`, the function returns the value of the `true_result` argument.
        If `true_result` is a FHIRPath expression it is evaluated.

        If `criterion` is `False` or an empty collection, the function returns the `otherwise_result` argument,
        unless the optional `otherwise_result` is not given, in which case the function returns an empty collection.
        If `otherwise_result` is a FHIRPath expression it is evaluated.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.

        """
        criterion_collection = []
        for index, item in enumerate(collection):
            criterion_collection.extend(
                self.criterion.evaluate(
                    [item], get_expression_context(environment, item, index), create
                )
            )

        if not criterion_collection:
            criterion = False
        else:
            criterion = criterion_collection[0].value

        if criterion:
            if isinstance(self.true_result, FHIRPath):
                return self.true_result.evaluate(collection, environment, create)
            else:
                return self.true_result
        else:
            if self.otherwise_result:
                if isinstance(self.otherwise_result, FHIRPath):
                    return self.otherwise_result.evaluate(
                        collection, environment, create
                    )
                else:
                    return self.otherwise_result
            else:
                return []


class FHIRTypeConversionFunction(FHIRPathFunction):
    """
    Abstract class definition for the category of type conversion FHIRPath functions.
    """

    def validate_collection(self, collection: FHIRPathCollection):
        """
        Validates the input collection of a FHIRPath type conversion function.

        Args:
            collection (FHIRPathCollection): Collection to be validated.

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        if len(collection) > 1:
            raise FHIRPathRuntimeError(
                f"FHIRPath function {self.__str__()} expected a single-item collection, instead got a {len(collection)}-items collection."
            )


class ToBoolean(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`toBoolean()`](http://hl7.org/fhirpath/N1/#boolean-conversion-functions) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return a single `Boolean` if:
            - the item is a `Boolean`
            - the item is an `Integer` that is equal to one of the possible integer representations of `Boolean` values
            - the item is a `Decimal` that is equal to one of the possible decimal representations of `Boolean` values
            - the item is a `String` that is equal to one of the possible string representations of `Boolean` values

        If the item is not one of the above types, or the item is a `String`, `Integer`, or `Decimal`, but is not equal to one of the possible values convertible to a `Boolean`, the result is false.
        If the input collection is empty, the result is empty ('[]').

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.

        """
        self.validate_collection(collection)
        if not collection:
            return []

        # Use type_utils for conversion
        from fhircraft.fhir.resources.datatypes.utils import to_boolean

        value = collection[0].value
        result = to_boolean(value)

        if result is not None:
            return [FHIRPathCollectionItem.wrap(result)]
        else:
            return []


class ConvertsToBoolean(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`convertsToBoolean()`](http://hl7.org/fhirpath/N1/#convertstoboolean-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return `True` if the item can be converted to a Boolean, `False` otherwise.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [
            FHIRPathCollectionItem.wrap(
                ToBoolean().evaluate(collection, environment, create) != []
            )
        ]


class ToInteger(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`toInteger()`](http://hl7.org/fhirpath/N1/#tointeger-integer) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return a single `Integer` if:
            - the item is an `Integer`
            - the item is a `String` and is convertible to an integer
            - the item is a `Boolean`, where `True` results in a 1 and `False` results in a 0.
        If the item is not one the above types, the result is empty (`[]`).

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []

        # Use type_utils for conversion
        from fhircraft.fhir.resources.datatypes.utils import to_integer

        value = collection[0].value
        result = to_integer(value)

        if result is not None:
            return [FHIRPathCollectionItem.wrap(result)]
        else:
            return []


class ConvertsToInteger(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`convertsToInteger()`](http://hl7.org/fhirpath/N1/#convertstointeger-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return `True` if the item can be converted to an Integer, `False` otherwise.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.

        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [
            FHIRPathCollectionItem.wrap(
                ToInteger().evaluate(collection, environment, create) != []
            )
        ]


class ToDate(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`toDate()`](http://hl7.org/fhirpath/N1/#todate-date) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return a single date if:
            - the item is a `Date`
            - the item is a `DateTime`
            - the item is a `String` and is convertible to a `Date`
        If the item is not one of the above types, or is not convertible to a `Date` (using the format `YYYY-MM-DD`), the result is empty.
        If the item contains a partial date (e.g. `'2012-01'`), the result is a partial date.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        value = collection[0].value
        if isinstance(value, str):
            date_match = re.match(
                rf"^{primitives.YEAR_REGEX}(-{primitives.MONTH_REGEX}(-{primitives.DAY_REGEX})?)?$",
                value,
            )
            datetime_match = re.match(
                rf"^({primitives.YEAR_REGEX}(-{primitives.MONTH_REGEX}(-{primitives.DAY_REGEX})?)?)(T{primitives.HOUR_REGEX}(:{primitives.MINUTES_REGEX}(:{primitives.SECONDS_REGEX}({primitives.TIMEZONE_REGEX})?)?)?)?",
                value,
            )
            if date_match:
                return [FHIRPathCollectionItem.wrap(value)]
            elif datetime_match:
                return [FHIRPathCollectionItem.wrap(datetime_match.group(1))]
            else:
                return []
        else:
            return []


class ConvertsToDate(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`convertsToDate()`](http://hl7.org/fhirpath/N1/#convertstodate-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return `True` if:
            - the item is a `Date`
            - the item is a `DateTime`
            - the item is a `String` and is convertible to a `Date`
        If the item is not one of the above types, or is not convertible to a `Date` (using the format `YYYY-MM-DD`), the result is `False`.
        If the item contains a partial date (e.g. `'2012-01'`), the result is a partial date.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [
            FHIRPathCollectionItem.wrap(
                ToDate().evaluate(collection, environment, create) != []
            )
        ]


class ToDateTime(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`toDateTime()`](http://hl7.org/fhirpath/N1/#todatetime-datetime) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return a single datetime if:
            - the item is a `DateTime`
            - the item is a `Date`, in which case the result is a `DateTime` with the year, month, and day of the `Date`, and the time components empty (not set to zero)
            - the item is a `String` and is convertible to a `DateTime`
        If the item is a `String`, but the string is not convertible to a `DateTime` (using the format `YYYY-MM-DDThh:mm:ss.fff(+|-)hh:mm`), the result is empty.
        If the item contains a partial datetime (e.g. `'2012-01-01T10:00'`), the result is a partial datetime.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        value = collection[0].value
        if isinstance(value, str):
            date_match = re.match(
                rf"^{primitives.YEAR_REGEX}(-{primitives.MONTH_REGEX}(-{primitives.DAY_REGEX})?)?$",
                value,
            )
            datetime_match = re.match(
                rf"^({primitives.YEAR_REGEX}(-{primitives.MONTH_REGEX}(-{primitives.DAY_REGEX})?)?)(T{primitives.HOUR_REGEX}(:{primitives.MINUTES_REGEX}(:{primitives.SECONDS_REGEX}({primitives.TIMEZONE_REGEX})?)?)?)?",
                value,
            )
            if date_match or datetime_match:
                return [FHIRPathCollectionItem.wrap(value)]
            else:
                return []
        else:
            return []


class ConvertsToDateTime(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`convertsToDateTime()`](http://hl7.org/fhirpath/N1/#convertstodatetime-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return `True` if:
            - the item is a `DateTime`
            - the item is a `Date`, in which case the result is a `DateTime` with the year, month, and day of the `Date`, and the time components empty (not set to zero)
            - the item is a `String` and is convertible to a `DateTime`
        If the item is a `String`, but the string is not convertible to a `DateTime` (using the format `YYYY-MM-DDThh:mm:ss.fff(+|-)hh:mm`), the result is `False`.
        If the item contains a partial datetime (e.g. `'2012-01-01T10:00'`), the result is 'True'.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [
            FHIRPathCollectionItem.wrap(
                ToDateTime().evaluate(collection, environment, create) != []
            )
        ]


class ToDecimal(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`toDecimal()`](http://hl7.org/fhirpath/N1/#todecimal-decimal) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return a single decimal if:
            - the item is an `Integer` or `Decimal`
            - the item is a `String` and is convertible to a `Decimal`
            - the item is a `Boolean`, where `True` results in a `1.0` and `False` results in a `0.0`.
        If the item is not one of the above types, the result is empty (`[]`).
        If the item is a `String`, but the string is not convertible to a `Decimal`, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        value = collection[0].value
        if isinstance(value, (int, float, bool)):
            return [FHIRPathCollectionItem.wrap(float(value))]
        elif isinstance(value, str):
            if re.match(r"(\\+|-)?\d+(\.\d+)?", value):
                return [FHIRPathCollectionItem.wrap(float(value))]
            else:
                return []
        else:
            return []


class ConvertsToDecimal(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`convertsToDecimal()`](http://hl7.org/fhirpath/N1/#convertstodecimal-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return `True` if:
            - the item is an `Integer` or `Decimal`
            - the item is a `String` and is convertible to a `Decimal`
            - the item is a `Boolean`, where `True` results in a `1.0` and `False` results in a `0.0`.
        If the item is not one of the above types, or is not convertible to a `Decimal`, the result is `False`.
        If the input collection is empty, the result is empty ('[]').

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [
            FHIRPathCollectionItem.wrap(
                ToDecimal().evaluate(collection, environment, create) != []
            )
        ]


class ToQuantity(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`toQuantity()`](http://hl7.org/fhirpath/N1/#toquantity-string) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return a single quantity if:
            - the item is an `Integer`, or `Decimal`, where the resulting quantity will have the default unit (`'1'`)
            - the item is a `Quantity`
            - the item is a `String` and is convertible to a `Quantity`
            - the item is a `Boolean`, where true results in the quantity `1.0 '1'`, and false results in the quantity `0.0 '1'`
        If the item is not one of the above types, the result is empty.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        from fhircraft.fhir.resources.datatypes.utils import get_complex_FHIR_type

        self.validate_collection(collection)
        Quantity = get_complex_FHIR_type("Quantity")
        if not collection:
            return []
        value = collection[0].value
        if isinstance(value, (bool, int, float)):
            return [FHIRPathCollectionItem.wrap(Quantity(value=float(value), unit="1"))]
        elif isinstance(value, str):
            quantity_match = re.match(
                r"((\+|-)?\d+(\.\d+)?)\s*(('([^']+)'|([a-zA-Z]+))?)", value
            )
            if quantity_match:
                return [
                    FHIRPathCollectionItem.wrap(
                        Quantity(
                            value=quantity_match.group(1), unit=quantity_match.group(4)
                        )
                    )
                ]
            else:
                return []
        elif isinstance(value, Quantity):
            return [FHIRPathCollectionItem.wrap(value)]
        else:
            return []


class ConvertsToQuantity(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`convertsToQuantity()`](http://hl7.org/fhirpath/N1/#convertstoquantity-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return `True` if:
            - the item is an `Integer`, or `Decimal`, where the resulting quantity will have the default unit (`'1'`)
            - the item is a `Quantity`
            - the item is a `String` and is convertible to a `Quantity`
            - the item is a `Boolean`, where true results in the quantity `1.0 '1'`, and false results in the quantity `0.0 '1'`
        If the item is not one of the above types, the result is `False`.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [
            FHIRPathCollectionItem.wrap(
                ToQuantity().evaluate(collection, environment, create) != []
            )
        ]


class ToString(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`toString()`](http://hl7.org/fhirpath/N1/#tostring-string) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return a single string if:
            - the item in the input collection is a `String`
            - the item in the input collection is an `Integer`, `Decimal`, `Date`, `Time`, `DateTime`, or `Quantity` the output will contain its `String` representation
            - the item is a `Boolean`, where true results in `'true'` and false in `'false'`.
        If the item is not one of the above types, the result is empty.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        from fhircraft.fhir.resources.datatypes.utils import get_complex_FHIR_type

        self.validate_collection(collection)
        if not collection:
            return []
        value = collection[0].value
        if isinstance(value, bool):
            return [FHIRPathCollectionItem.wrap("true" if value else "false")]
        elif isinstance(value, (str, int, float)):
            return [FHIRPathCollectionItem.wrap(str(value))]
        elif isinstance(value, get_complex_FHIR_type("Quantity")):
            return [FHIRPathCollectionItem.wrap(f"{value.value} {value.unit}")]
        else:
            return []


class ConvertsToString(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`convertsToString()`](http://hl7.org/fhirpath/N1/#convertstostring-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return `True` if:
            - the item in the input collection is a `String`
            - the item in the input collection is an `Integer`, `Decimal`, `Date`, `Time`, `DateTime`, or `Quantity` the output will contain its `String` representation
            - the item is a `Boolean`, where true results in `'true'` and false in `'false'`.
        If the item is not one of the above types, the result is `False`.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [
            FHIRPathCollectionItem.wrap(
                ToString().evaluate(collection, environment, create) != []
            )
        ]


class ToTime(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`toTime()`](http://hl7.org/fhirpath/N1/#totime-time) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return a single time if:
            - the item is a `Time`
            - the item is a `String` and is convertible to a `Time`
        If the item is a `String`, but the string is not convertible to a `Time` (using the format `hh:mm:ss.fff(+|-)hh:mm`), the result is empty.
        If the item contains a partial datetime (e.g. `'10:00'`), the result is a partial datetime.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        value = collection[0].value
        if isinstance(value, str):
            time_match = re.match(
                rf"^{primitives.HOUR_REGEX}(:{primitives.MINUTES_REGEX}(:{primitives.SECONDS_REGEX}({primitives.TIMEZONE_REGEX})?)?)?",
                value,
            )
            if time_match:
                return [FHIRPathCollectionItem.wrap(value)]
            else:
                return []
        else:
            return []


class ConvertsToTime(FHIRTypeConversionFunction):
    """
    A representation of the FHIRPath [`convertsToTime()`](http://hl7.org/fhirpath/N1/#convertstotime-boolean) function.
    """

    def evaluate(
        self, collection: FHIRPathCollection, environment: dict, create: bool = False
    ) -> FHIRPathCollection:
        """
        If the input collection contains a single item, this function will return `True` if:
            - the item is a `Time`
            - the item is a `String` and is convertible to a `Time`
        If the item is a `String`, but the string is not convertible to a `DateTime` (using the format `hh:mm:ss.fff(+|-)hh:mm`), the result is `False`.
        If the item contains a partial datetime (e.g. `'10:00'`), the result is 'True'.
        If the input collection is empty, the result is empty.

        Args:
            collection (FHIRPathCollection): The input collection.
            environment (dict): The environment context for the evaluation.
            create (bool): Whether to create new elements during evaluation if necessary.

        Returns:
            FHIRPathCollection: The output collection

        Raises:
            FHIRPathRuntimeError: If input collection has more than one item.
        """
        self.validate_collection(collection)
        if not collection:
            return []
        return [
            FHIRPathCollectionItem.wrap(
                ToTime().evaluate(collection, environment, create) != []
            )
        ]
