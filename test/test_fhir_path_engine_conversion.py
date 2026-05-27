import pytest

from fhircraft.fhir.path.engine.conversion import (
    Iif,
    ToString,
    ConvertsToString,
    ToBoolean,
    ConvertsToBoolean,
    ToInteger,
    ConvertsToInteger,
    ToDecimal,
    ConvertsToDecimal,
    ToDate,
    ConvertsToDate,
    ToDateTime,
    ConvertsToDateTime,
    ToQuantity,
    ConvertsToQuantity,
    ToTime,
    ConvertsToTime,
)
from fhircraft.fhir.path.engine.conversion import FhirPathRuntimeError
from fhircraft.fhir.path.engine.core import (
    Element,
    FHIRPathCollectionItem,
)
from fhircraft.fhir.path.engine.existence import Empty, Exists
from fhircraft.fhir.path.engine.literals import Date, DateTime, Quantity, Time
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Quantity as R4_Quantity,
    Age as R4_Age,
)
from fhircraft.fhir.resources.datatypes.R4.primitive import (
    String as FHIRString,
    Integer as FHIRInteger,
    Boolean as FHIRBoolean,
    Decimal as FHIRDecimal,
    Date as FHIRDate,
    DateTime as FHIRDateTime,
    Time as FHIRTime,
)
from datetime import datetime, date, time

env = dict()

# ---------------------------
# Iif()
# ---------------------------


def test_iif_returns_empty_if_empty():
    collection = []
    result = Iif(Exists(), [FHIRPathCollectionItem.wrap(1)]).evaluate(collection, env)
    assert result == []


def test_iif_returns_value_if_criterion_is_true():
    collection = [FHIRPathCollectionItem(value=True)]
    result = Iif(Exists(), [FHIRPathCollectionItem.wrap("return_value")]).evaluate(
        collection, env, create=False
    )
    assert result == [FHIRPathCollectionItem.wrap("return_value")]


def test_iif_returns_value_if_criterion_is_false():
    collection = []
    result = Iif(
        Exists(),
        [FHIRPathCollectionItem.wrap("return_value")],
        [FHIRPathCollectionItem.wrap("other_value")],
    ).evaluate(collection, env, create=False)
    assert result == [FHIRPathCollectionItem.wrap("other_value")]


def test_iif_returns_true_if_criterion_is_empty():
    collection = []
    result = Iif(Empty(), [FHIRPathCollectionItem.wrap(True)]).evaluate(
        collection, env, create=False
    )
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_iif_returns_value_if_criterion_is_false_and_no_otherwise():
    collection = []
    result = Iif(Exists(), [FHIRPathCollectionItem.wrap("return_value")]).evaluate(
        collection, env, create=False
    )
    assert result == []


def test_iif_returns_evaluated_value_if_criterion_is_true():
    collection = [FHIRPathCollectionItem(value=True)]
    result = Iif(Exists(), Empty(), Exists()).evaluate(collection, env, create=False)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_iif_returns_evaluated_value_if_criterion_is_false():
    collection = []
    result = Iif(Exists(), Empty(), Exists()).evaluate(collection, env, create=False)
    assert result == [FHIRPathCollectionItem.wrap(False)]


def test_iif_returns_evaluated_value_if_criterion_is_false_and_no_otherwise():
    collection = []
    result = Iif(Exists(), Exists()).evaluate(collection, env, create=False)
    assert result == []


def test_iif_string_representation():
    expression = Iif(Element("left"), Element("right"), Element("other"))
    assert str(expression) == "iif(left, right, other)"


# ---------------------------
# ToBoolean()
# ---------------------------


def test_toBoolean_returns_empty_if_empty():
    collection = []
    result = ToBoolean().evaluate(collection, env)
    assert result == []


def test_toBoolean_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ToBoolean().evaluate(collection, env)
    assert result == []


toBoolean_cases = (
    ("true", True),
    ("t", True),
    ("yes", True),
    ("y", True),
    ("True", True),
    ("T", True),
    ("Yes", True),
    ("Y", True),
    ("1", True),
    ("1.0", True),
    (1, True),
    (1.0, True),
    ("false", False),
    ("f", False),
    ("no", False),
    ("n", False),
    ("False", False),
    ("F", False),
    ("No", False),
    ("N", False),
    ("0", False),
    ("0.0", False),
    (0, False),
    (0.0, False),
    # FHIR primitive class instances
    (FHIRString(value="true"), True),
    (FHIRString(value="false"), False),
    (FHIRBoolean(value=True), True),
    (FHIRBoolean(value=False), False),
    (FHIRInteger(value=1), True),
    (FHIRInteger(value=0), False),
)


@pytest.mark.parametrize("value, expected", toBoolean_cases)
def test_toBoolean_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToBoolean().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(expected)]


def test_toBoolean_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ToBoolean().evaluate(collection, env)


def test_toBoolean_string_representation():
    expression = ToBoolean()
    assert str(expression) == "toBoolean()"


# ---------------------------
# ConvertsToBoolean()
# ---------------------------


def test_convertstoboolean_returns_empty_if_empty():
    collection = []
    result = ConvertsToBoolean().evaluate(collection, env)
    assert result == []


def test_convertstoboolean_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ConvertsToBoolean().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


convertsToBoolean_cases = (
    ("true"),
    ("t"),
    ("True"),
    ("T"),
    ("yes"),
    ("y"),
    ("Yes"),
    ("Y"),
    ("1"),
    ("1.0"),
    (1),
    (1.0),
    ("false"),
    ("f"),
    ("no"),
    ("n"),
    ("False"),
    ("F"),
    ("No"),
    ("N"),
    ("0"),
    ("0.0"),
    (0),
    (0.0),
    # FHIR primitive class instances
    (FHIRString(value="true")),
    (FHIRString(value="false")),
    (FHIRBoolean(value=True)),
    (FHIRInteger(value=1)),
)


@pytest.mark.parametrize("value", convertsToBoolean_cases)
def test_convertstoboolean_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToBoolean().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_convertsToBoolean_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ConvertsToBoolean().evaluate(collection, env)


def test_convertsToBoolean_string_representation():
    expression = ConvertsToBoolean()
    assert str(expression) == "convertsToBoolean()"


# ---------------------------
# ToInteger()
# ---------------------------


def test_tointeger_returns_empty_if_empty():
    collection = []
    result = ToInteger().evaluate(collection, env)
    assert result == []


def test_tointeger_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ToInteger().evaluate(collection, env)
    assert result == []


tointeger_cases = (
    ("+14", 14),
    ("14", 14),
    (14, 14),
    ("-14", -14),
    (-14, -14),
    (True, 1),
    (False, 0),
    # FHIR primitive class instances
    (FHIRString(value="14"), 14),
    (FHIRString(value="-14"), -14),
    (FHIRInteger(value=14), 14),
    (FHIRBoolean(value=True), 1),
    (FHIRBoolean(value=False), 0),
)


@pytest.mark.parametrize("value, expected", tointeger_cases)
def test_tointeger_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToInteger().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(expected)]


def test_toInteger_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ToInteger().evaluate(collection, env)


def test_toInteger_string_representation():
    expression = ToInteger()
    assert str(expression) == "toInteger()"


# ---------------------------
# ConvertsToInteger()
# ---------------------------


def test_convertstointeger_returns_empty_if_empty():
    collection = []
    result = ConvertsToInteger().evaluate(collection, env)
    assert result == []


def test_convertstointeger_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ConvertsToInteger().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


convertstointeger_cases = (
    ("+14"),
    ("14"),
    (14),
    ("-14"),
    (-14),
    (True),
    (False),
    # FHIR primitive class instances
    (FHIRString(value="14")),
    (FHIRInteger(value=14)),
    (FHIRBoolean(value=True)),
)


@pytest.mark.parametrize("value", convertstointeger_cases)
def test_convertstointeger_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToInteger().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_convertstoInteger_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ConvertsToInteger().evaluate(collection, env)


def test_convertsToInteger_string_representation():
    expression = ConvertsToInteger()
    assert str(expression) == "convertsToInteger()"


# ---------------------------
# ToDecimal()
# ---------------------------


def test_todecimal_returns_empty_if_empty():
    collection = []
    result = ToDecimal().evaluate(collection, env)
    assert result == []


def test_todecimal_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ToDecimal().evaluate(collection, env)
    assert result == []


todecimal_cases = (
    ("-14.5", -14.5),
    ("+14.5", 14.5),
    ("14.5", 14.5),
    ("14", 14.0),
    (14.5, 14.5),
    (14, 14.0),
    (True, 1.0),
    (False, 0.0),
    # FHIR primitive class instances
    (FHIRString(value="14.5"), 14.5),
    (FHIRString(value="14"), 14.0),
    (FHIRDecimal(value=14.5), 14.5),
    (FHIRInteger(value=14), 14.0),
    (FHIRBoolean(value=True), 1.0),
    (FHIRBoolean(value=False), 0.0),
)


@pytest.mark.parametrize("value, expected", todecimal_cases)
def test_todecimal_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToDecimal().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(expected)]


def test_toDecimal_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ToDecimal().evaluate(collection, env)


def test_toDecimal_string_representation():
    expression = ToDecimal()
    assert str(expression) == "toDecimal()"


# ---------------------------
# ConvertsToDecimal()
# ---------------------------


def test_convertstodecimal_returns_empty_if_empty():
    collection = []
    result = ConvertsToDecimal().evaluate(collection, env)
    assert result == []


def test_convertstodecimal_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ConvertsToDecimal().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


convertstodecimal_cases = (
    ("-14.5"),
    ("+14.5"),
    ("14.5"),
    ("14"),
    (14.5),
    (14),
    (True),
    (False),
    # FHIR primitive class instances
    (FHIRString(value="14.5")),
    (FHIRDecimal(value=14.5)),
    (FHIRInteger(value=14)),
    (FHIRBoolean(value=True)),
)


@pytest.mark.parametrize("value", convertstodecimal_cases)
def test_convertstodecimal_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToDecimal().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_convertsToDecimal_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ConvertsToDecimal().evaluate(collection, env)


def test_convertsToDecimal_string_representation():
    expression = ConvertsToDecimal()
    assert str(expression) == "convertsToDecimal()"


# ---------------------------
# ToDate()
# ---------------------------


def test_todate_returns_empty_if_empty():
    collection = []
    result = ToDate().evaluate(collection, env)
    assert result == []


def test_todate_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ToDate().evaluate(collection, env)
    assert result == []


todate_cases = (
    ("2014", "2014"),
    ("2014-02", "2014-02"),
    ("2014-02-01", "2014-02-01"),
    ("2014-02-01T:12:25", "2014-02-01"),
    ("2014-02-01T00:00:00.000Z", "2014-02-01"),
    (date(2014, 2, 1), "2014-02-01"),
    (datetime(2014, 2, 1, 0, 0), "2014-02-01"),
    (Date("@2014-02-01"), "2014-02-01"),
    (DateTime("@2014-02-01T00:00:00.000Z"), "2014-02-01"),
    # FHIR primitive class instances
    (FHIRString(value="2014-02-01"), "2014-02-01"),
    (FHIRDate(value="2014-02-01"), "2014-02-01"),
    (FHIRDateTime(value="2014-02-01T00:00:00.000Z"), "2014-02-01"),
)


@pytest.mark.parametrize("value, expected", todate_cases)
def test_todate_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToDate().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(expected)]


def test_toDate_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ToDate().evaluate(collection, env)


def test_toDate_string_representation():
    expression = ToDate()
    assert str(expression) == "toDate()"


# ---------------------------
# ConvertsToDate()
# ---------------------------


def test_convertstodate_returns_empty_if_empty():
    collection = []
    result = ConvertsToDate().evaluate(collection, env)
    assert result == []


def test_convertstodate_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ConvertsToDate().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


convertstodate_cases = (
    ("2014"),
    ("2014-02"),
    ("2014-02-01"),
    ("2014-02-01T:12:25"),
    ("2014-02-01T00:00:00.000Z"),
    (date(2000, 1, 1)),
    (datetime(2000, 1, 1)),
    (Date("@2014-02-01")),
    (DateTime("@2014-02-01T00:00:00.000Z")),
    # FHIR primitive class instances
    (FHIRString(value="2014-02-01")),
    (FHIRDate(value="2014-02-01")),
    (FHIRDateTime(value="2014-02-01T00:00:00.000Z")),
)


@pytest.mark.parametrize("value", convertstodate_cases)
def test_convertstodate_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToDate().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_convertsToDate_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ConvertsToDate().evaluate(collection, env)


def test_convertsToDate_string_representation():
    expression = ConvertsToDate()
    assert str(expression) == "convertsToDate()"


# ---------------------------
# ToDateTime()
# ---------------------------


def test_todatetime_returns_empty_if_empty():
    collection = []
    result = ToDateTime().evaluate(collection, env)
    assert result == []


def test_todatetime_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ToDateTime().evaluate(collection, env)
    assert result == []


todatetime_cases = (
    ("2014", "2014"),
    ("2014-02", "2014-02"),
    ("2014-02-01", "2014-02-01"),
    ("2014-02-01T:12:25", "2014-02-01T:12:25"),
    ("2014-02-01T00:00:00.000Z", "2014-02-01T00:00:00.000Z"),
    (date(2014, 2, 1), "2014-02-01"),
    (datetime(2014, 2, 1), "2014-02-01T00:00:00"),
    (Date("@2014-02-01"), "2014-02-01"),
    (DateTime("@2012-02-01T00:00:00.000Z"), "2012-02-01T00:00:00Z"),
    # FHIR primitive class instances
    (FHIRString(value="2014-02-01T00:00:00.000Z"), "2014-02-01T00:00:00.000Z"),
    (FHIRDate(value="2014-02-01"), "2014-02-01"),
    (FHIRDateTime(value="2014-02-01T00:00:00.000Z"), "2014-02-01T00:00:00.000Z"),
)


@pytest.mark.parametrize("value, expected", todatetime_cases)
def test_todatetime_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToDateTime().evaluate(collection, env)
    print(result[0].value, expected)
    assert result == [FHIRPathCollectionItem.wrap(expected)]


def test_toDateTime_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ToDateTime().evaluate(collection, env)


def test_toDateTime_string_representation():
    expression = ToDateTime()
    assert str(expression) == "toDateTime()"


# ---------------------------
# ConvertsToDateTime()
# ---------------------------


def test_convertstodatetime_returns_empty_if_empty():
    collection = []
    result = ConvertsToDateTime().evaluate(collection, env)
    assert result == []


def test_convertstodatetime_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ConvertsToDateTime().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


convertstodatetime_cases = (
    ("2014"),
    ("2014-02"),
    ("2014-02-01"),
    ("2014-02-01T:12:25"),
    ("2014-02-01T00:00:00.000Z"),
    (date(2014, 2, 1)),
    (datetime(2014, 2, 1)),
    (Date("@2014-02-01")),
    (DateTime("@2014-02-01T00:00:00.000Z")),
    # FHIR primitive class instances
    (FHIRString(value="2014-02-01")),
    (FHIRDate(value="2014-02-01")),
    (FHIRDateTime(value="2014-02-01T00:00:00.000Z")),
)


@pytest.mark.parametrize("value", convertstodatetime_cases)
def test_convertstodatetime_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToDateTime().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_convertsToDateTime_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ConvertsToDateTime().evaluate(collection, env)


def test_convertsToDateTime_string_representation():
    expression = ConvertsToDateTime()
    assert str(expression) == "convertsToDateTime()"


# ---------------------------
# ToQuantity()
# ---------------------------


def test_toquantity_returns_empty_if_empty():
    collection = []
    result = ToQuantity().evaluate(collection, env)
    assert result == []


def test_toquantity_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ToQuantity().evaluate(collection, env)
    assert result == []


toquantity_cases = (
    ("12.5 mm[Hg]", Quantity(value=12.5, unit="mm[Hg]")),
    ("12.5 mg", Quantity(value=12.5, unit="mg")),
    ("12.5", Quantity(value=12.5, unit="")),
    (12.5, Quantity(value=12.5, unit="")),
    (5, Quantity(value=5, unit="")),
    (True, Quantity(value=1.0, unit="")),
    (False, Quantity(value=0.0, unit="")),
    (Quantity(value=12.5, unit="mg"), Quantity(value=12.5, unit="mg")),
    (R4_Quantity(value=12.5, unit="mg"), Quantity(value=12.5, unit="mg")),
    (
        R4_Age(value=12.5, code="a", system="http://unitsofmeasure.org"),
        Quantity(value=12.5, unit="a"),
    ),
    # FHIR primitive class instances
    (FHIRString(value="12.5 mg"), Quantity(value=12.5, unit="mg")),
    (FHIRDecimal(value=12.5), Quantity(value=12.5, unit="")),
    (FHIRInteger(value=5), Quantity(value=5, unit="")),
    (FHIRBoolean(value=True), Quantity(value=1.0, unit="")),
)


@pytest.mark.parametrize("value, expected", toquantity_cases)
def test_toquantity_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToQuantity().evaluate(collection, env)
    assert result[0].value == expected


@pytest.mark.parametrize(
    "value, expected",
    (
        ("120.5 g", Quantity(value=0.1205, unit="kg")),
        ("12.5", Quantity(value=12.5, unit="kg")),
    ),
)
def test_toquantity_converts_to_input_unit(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToQuantity("kg").evaluate(collection, env)
    assert result[0].value == expected


def test_toQuantity_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ToQuantity().evaluate(collection, env)


def test_toQuantity_string_representation():
    expression = ToQuantity()
    assert str(expression) == "toQuantity()"


# ---------------------------
# ConvertsToQuantity()
# ---------------------------


def test_convertstoquantity_returns_empty_if_empty():
    collection = []
    result = ConvertsToQuantity().evaluate(collection, env)
    assert result == []


def test_convertstoquantity_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ConvertsToQuantity().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


convertstoquantity_cases = (
    ("12.5 mm[Hg]"),
    ("12.5 mg"),
    (12.5),
    (5),
    (True),
    (False),
    (Quantity(value=0.0, unit="")),
    (Quantity(value=12.5, unit="mg")),
    (R4_Quantity(value=12.5, unit="mg")),
    (R4_Age(value=12.5, code="a", system="http://unitsofmeasure.org")),
    # FHIR primitive class instances
    (FHIRString(value="12.5 mg")),
    (FHIRDecimal(value=12.5)),
    (FHIRInteger(value=5)),
    (FHIRBoolean(value=True)),
)


@pytest.mark.parametrize("value", convertstoquantity_cases)
def test_convertstoquantity_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToQuantity().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


@pytest.mark.parametrize(
    "value, expected",
    (
        ("120.5 g", True),
        ("12.5", True),
        ("12.5 mL", False),
        ("12.5 mm[Hg]", False),
    ),
)
def test_convertstoquantity_returns_correct_conversion(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToQuantity("kg").evaluate(collection, env)
    assert result[0].value == expected


def test_convertsToQuantity_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ConvertsToQuantity().evaluate(collection, env)


def test_convertsToQuantity_string_representation():
    expression = ConvertsToQuantity()
    assert str(expression) == "convertsToQuantity()"


# ---------------------------
# ToString()
# ---------------------------


def test_toString_returns_empty_if_empty():
    collection = []
    result = ToString().evaluate(collection, env)
    assert result == []


def test_toString_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value=BaseException)]
    result = ToString().evaluate(collection, env)
    assert result == []


toString_cases = (
    ("abc", "abc"),
    (2014, "2014"),
    (12.345, "12.345"),
    ("2014-02-01T:12:25", "2014-02-01T:12:25"),
    ("2014-02-01", "2014-02-01"),
    (True, "true"),
    (False, "false"),
    (Quantity(value=12.5, unit="mg"), "12.5 mg"),
    (R4_Quantity(value=12.5, unit="mg"), "12.5 mg"),
    (R4_Age(value=12.5, code="a", system="http://unitsofmeasure.org"), "12.5 a"),
    ("2014-02-01T00:00:00.000Z", "2014-02-01T00:00:00.000Z"),
    # FHIR primitive class instances
    (FHIRString(value="abc"), "abc"),
    (FHIRInteger(value=2014), "2014"),
    (FHIRDecimal(value=12.345), "12.345"),
    (FHIRBoolean(value=True), "true"),
    (FHIRBoolean(value=False), "false"),
)


@pytest.mark.parametrize("value, expected", toString_cases)
def test_toString_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToString().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(expected)]


def test_toString_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ToString().evaluate(collection, env)


def test_toString_string_representation():
    expression = ToString()
    assert str(expression) == "toString()"


# ---------------------------
# ConvertsToString()
# ---------------------------


def test_convertstostring_returns_empty_if_empty():
    collection = []
    result = ConvertsToString().evaluate(collection, env)
    assert result == []


def test_convertstostring_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value=BaseException)]
    result = ConvertsToString().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


convertstostring_cases = (
    ("string"),
    (123),
    (14.54),
    ("2014-02-01T:12:25"),
    ("2014-02-01"),
    (True),
    (False),
    (Quantity(value=12.5, unit="mg")),
    (Quantity(value=12.5, unit="mg")),
    (R4_Quantity(value=12.5, unit="mg")),
    (R4_Age(value=12.5, code="a", system="http://unitsofmeasure.org")),
    # FHIR primitive class instances
    (FHIRString(value="abc")),
    (FHIRInteger(value=42)),
    (FHIRDecimal(value=14.54)),
    (FHIRBoolean(value=True)),
)


@pytest.mark.parametrize("value", convertstostring_cases)
def test_convertstostring_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToString().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_convertsToString_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ConvertsToString().evaluate(collection, env)


def test_convertsToString_string_representation():
    expression = ConvertsToString()
    assert str(expression) == "convertsToString()"


# ---------------------------
# ToTime()
# ---------------------------


def test_totime_returns_empty_if_empty():
    collection = []
    result = ToTime().evaluate(collection, env)
    assert result == []


def test_totime_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ToTime().evaluate(collection, env)
    assert result == []


totime_cases = (
    ("2014", "2014"),
    ("2014-02", "2014-02"),
    ("2014-02-01", "2014-02-01"),
    ("2014-02-01T:12:25", "2014-02-01T:12:25"),
    ("2014-02-01T00:00:00.000Z", "2014-02-01T00:00:00.000Z"),
    (time(12, 25), "12:25:00"),
    (Time("@T12:25"), "12:25:00"),
    # FHIR primitive class instances
    (FHIRString(value="10:30:00"), "10:30:00"),
    (FHIRTime(value="10:30:00"), "10:30:00"),
)


@pytest.mark.parametrize("value, expected", totime_cases)
def test_totime_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToTime().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(expected)]


def test_toTime_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ToTime().evaluate(collection, env)


def test_toTime_string_representation():
    expression = ToTime()
    assert str(expression) == "toTime()"


# ---------------------------
# ConvertsToTime()
# ---------------------------


def test_convertstotime_returns_empty_if_empty():
    collection = []
    result = ConvertsToDateTime().evaluate(collection, env)
    assert result == []


def test_convertstotime_returns_empty_for_invalid_type():
    collection = [FHIRPathCollectionItem(value="invalid")]
    result = ConvertsToDateTime().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(False)]


convertstotime_cases = (
    ("2014"),
    ("2014-02"),
    ("2014-02-01"),
    ("2014-02-01T:12:25"),
    ("2014-02-01T00:00:00.000Z"),
    (time(12, 25)),
    (Time("@T12:25")),
    # FHIR primitive class instances
    (FHIRString(value="10:30:00")),
    (FHIRTime(value="10:30:00")),
)


@pytest.mark.parametrize("value", convertstotime_cases)
def test_convertstotime_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToTime().evaluate(collection, env)
    assert result == [FHIRPathCollectionItem.wrap(True)]


def test_convertsToTime_raises_error_for_multiple_items():
    collection = [FHIRPathCollectionItem(value=1), FHIRPathCollectionItem(value=2)]
    with pytest.raises(FhirPathRuntimeError):
        ConvertsToTime().evaluate(collection, env)


def test_convertsToTime_string_representation():
    expression = ConvertsToTime()
    assert str(expression) == "convertsToTime()"
