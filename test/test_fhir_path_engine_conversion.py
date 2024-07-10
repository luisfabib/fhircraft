from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, FHIRPathError, Invocation, Root, Element, This
from fhircraft.fhir.path.engine.existence import Exists, Empty
from fhircraft.fhir.path.engine.conversion import *
from fhircraft.fhir.resources.datatypes import get_FHIR_type
import pytest
Quantity = get_FHIR_type('Quantity')
        

#---------------------------
# Iif()
#---------------------------

def test_iif_returns_empty_if_empty():
    collection = []
    result = Iif(Exists(), 1).evaluate(collection)
    assert result == []

def test_iif_returns_value_if_criterion_is_true():
    collection = [FHIRPathCollectionItem(value=True)]
    result = Iif(Exists(), 'return_value').evaluate(collection, create=False)
    assert result == 'return_value'

def test_iif_returns_value_if_criterion_is_false():
    collection = []
    result = Iif(Exists(), 'return_value', 'other_value').evaluate(collection, create=False)
    assert result == 'other_value'
    
def test_iif_returns_value_if_criterion_is_false_and_no_otherwise():
    collection = []
    result = Iif(Exists(), 'return_value').evaluate(collection, create=False)
    assert result == []

def test_iif_returns_evaluated_value_if_criterion_is_true():
    collection = [FHIRPathCollectionItem(value=True)]
    result = Iif(Exists(),  Empty(), Exists()).evaluate(collection, create=False)
    assert result == False

def test_iif_returns_evaluated_value_if_criterion_is_false():
    collection = []
    result = Iif(Exists(), Empty(), Exists()).evaluate(collection, create=False)
    assert result == False
    
def test_iif_returns_evaluated_value_if_criterion_is_false_and_no_otherwise():
    collection = []
    result = Iif(Exists(), Exists()).evaluate(collection, create=False)
    assert result == []
    
    
#---------------------------
# FHIRTypeConversionFunction
#---------------------------

def test_type_conversion_function_checks_singleton_collection():
    collection = [FHIRPathCollectionItem(value='mySubstringValue'), FHIRPathCollectionItem(value='mySubstringValue2')]
    with pytest.raises(FHIRPathError):
        FHIRTypeConversionFunction().validate_collection(collection)

#---------------------------
# ToBoolean()
#---------------------------

def test_toBoolean_returns_empty_if_empty():
    collection = []
    result = ToBoolean().evaluate(collection)
    assert result == []

def test_toBoolean_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ToBoolean().evaluate(collection)
    assert result == []

toBoolean_cases = (
    ('true', True),
    ('t', True),
    ('yes', True),
    ('y', True),
    ('1', True),
    ('1.0', True),
    (1, True),
    (1.0, True),
    ('false', False),
    ('f', False),
    ('no', False),
    ('n', False),
    ('0', False),
    ('0.0', False),
    (0, False),
    (0.0, False),
)
@pytest.mark.parametrize("value, expected", toBoolean_cases)
def test_toBoolean_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToBoolean().evaluate(collection)
    assert result == expected


#---------------------------
# ConvertsToBoolean()
#---------------------------

def test_convertstoboolean_returns_empty_if_empty():
    collection = []
    result = ConvertsToBoolean().evaluate(collection)
    assert result == []

def test_convertstoboolean_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ConvertsToBoolean().evaluate(collection)
    assert result == False

convertsToBoolean_cases = (
    ('true'),
    ('t'),
    ('yes'),
    ('y'),
    ('1'),
    ('1.0'),
    (1),
    (1.0),
    ('false'),
    ('f'),
    ('no'),
    ('n'),
    ('0'),
    ('0.0'),
    (0),
    (0.0),
)
@pytest.mark.parametrize("value", convertsToBoolean_cases)
def test_convertstoboolean_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToBoolean().evaluate(collection)
    assert result == True


#---------------------------
# ToInteger()
#---------------------------

def test_tointeger_returns_empty_if_empty():
    collection = []
    result = ToInteger().evaluate(collection)
    assert result == []

def test_tointeger_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ToInteger().evaluate(collection)
    assert result == []

tointeger_cases = (
    ('14', 14),
    (14, 14),
    ('-14', -14),
    (-14, -14),
    (True, 1),
    (False, 0),
)
@pytest.mark.parametrize("value, expected", tointeger_cases)
def test_tointeger_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToInteger().evaluate(collection)
    assert result == expected


#---------------------------
# ConvertsToInteger()
#---------------------------

def test_convertstointeger_returns_empty_if_empty():
    collection = []
    result = ConvertsToInteger().evaluate(collection)
    assert result == []

def test_convertstointeger_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ConvertsToInteger().evaluate(collection)
    assert result == False

convertstointeger_cases = (
    ('4'),
    (4),
    ('-4'),
    (-4),
    (True),
    (False),
)
@pytest.mark.parametrize("value", convertstointeger_cases)
def test_convertstointeger_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToInteger().evaluate(collection)
    assert result == True



#---------------------------
# ToDecimal()
#---------------------------

def test_todecimal_returns_empty_if_empty():
    collection = []
    result = ToDecimal().evaluate(collection)
    assert result == []

def test_todecimal_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ToDecimal().evaluate(collection)
    assert result == []

todecimal_cases = (
    ('14.0',14.0),
    ('14', 14.0),
    (14, 14.0),
    (True, 1.0),
    (False, 0.0),
)
@pytest.mark.parametrize("value, expected", todecimal_cases)
def test_todecimal_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToDecimal().evaluate(collection)
    assert result == expected


#---------------------------
# ConvertsToDecimal()
#---------------------------

def test_convertstodecimal_returns_empty_if_empty():
    collection = []
    result = ConvertsToDecimal().evaluate(collection)
    assert result == []

def test_convertstodecimal_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ConvertsToDecimal().evaluate(collection)
    assert result == False

convertstodecimal_cases = (
    ('14.0'),
    ('14'),
    (14),
    (True),
    (False),
)
@pytest.mark.parametrize("value", convertstodecimal_cases)
def test_convertstodecimal_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToDecimal().evaluate(collection)
    assert result == True



#---------------------------
# ToDate()
#---------------------------

def test_todate_returns_empty_if_empty():
    collection = []
    result = ToDate().evaluate(collection)
    assert result == []

def test_todate_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ToDate().evaluate(collection)
    assert result == []

todate_cases = (
    ('2014', '2014'),
    ('2014-02', '2014-02'),
    ('2014-02-01', '2014-02-01'),
    ('2014-02-01T:12:25', '2014-02-01'),
    ('2014-02-01T00:00:00.000Z', '2014-02-01'),
)
@pytest.mark.parametrize("value, expected", todate_cases)
def test_todate_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToDate().evaluate(collection)
    assert result == expected


#---------------------------
# ConvertsToDate()
#---------------------------

def test_convertstodate_returns_empty_if_empty():
    collection = []
    result = ConvertsToDate().evaluate(collection)
    assert result == []

def test_convertstodate_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ConvertsToDate().evaluate(collection)
    assert result == False

convertstodate_cases = (
    ('2014'),
    ('2014-02'),
    ('2014-02-01'),
    ('2014-02-01T:12:25'),
    ('2014-02-01T00:00:00.000Z'),
)
@pytest.mark.parametrize("value", convertstodate_cases)
def test_convertstodate_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToDate().evaluate(collection)
    assert result == True



#---------------------------
# ToDateTime()
#---------------------------

def test_todatetime_returns_empty_if_empty():
    collection = []
    result = ToDateTime().evaluate(collection)
    assert result == []

def test_todatetime_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ToDateTime().evaluate(collection)
    assert result == []

todatetime_cases = (
    ('2014', '2014'),
    ('2014-02', '2014-02'),
    ('2014-02-01', '2014-02-01'),
    ('2014-02-01T:12:25', '2014-02-01T:12:25'),
    ('2014-02-01T00:00:00.000Z', '2014-02-01T00:00:00.000Z'),
)
@pytest.mark.parametrize("value, expected", todatetime_cases)
def test_todatetime_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToDateTime().evaluate(collection)
    assert result == expected


#---------------------------
# ConvertsToDateTime()
#---------------------------

def test_convertstodatetime_returns_empty_if_empty():
    collection = []
    result = ConvertsToDateTime().evaluate(collection)
    assert result == []

def test_convertstodatetime_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ConvertsToDateTime().evaluate(collection)
    assert result == False

convertstodatetime_cases = (
    ('2014'),
    ('2014-02'),
    ('2014-02-01'),
    ('2014-02-01T:12:25'),
    ('2014-02-01T00:00:00.000Z'),
)
@pytest.mark.parametrize("value", convertstodatetime_cases)
def test_convertstodatetime_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToDateTime().evaluate(collection)
    assert result == True



#---------------------------
# ToQuantity()
#---------------------------

def test_toquantity_returns_empty_if_empty():
    collection = []
    result = ToQuantity().evaluate(collection)
    assert result == []

def test_toquantity_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ToQuantity().evaluate(collection)
    assert result == []

toquantity_cases = (
    ('12.5 mg', Quantity(value=12.5, unit='mg')),
    (12.5, Quantity(value=12.5, unit='1')),
    (5, Quantity(value=5, unit='1')),
    (True, Quantity(value=1.0, unit='1')),
    (False, Quantity(value=0.0, unit='1')),
)
@pytest.mark.parametrize("value, expected", toquantity_cases)
def test_toquantity_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToQuantity().evaluate(collection)
    assert result == expected




#---------------------------
# ConvertsToQuantity()
#---------------------------

def test_convertstoquantity_returns_empty_if_empty():
    collection = []
    result = ConvertsToQuantity().evaluate(collection)
    assert result == []

def test_convertstoquantity_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ConvertsToQuantity().evaluate(collection)
    assert result == False

convertstoquantity_cases = (
    ('12.5 mg'),
    (12.5),
    (5),
    (True),
    (False), 
    (Quantity(value=0.0, unit='1')),
)
@pytest.mark.parametrize("value", convertstoquantity_cases)
def test_convertstoquantity_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToQuantity().evaluate(collection)
    assert result == True

#---------------------------
# ConvertsToString()
#---------------------------

def test_convertstostring_returns_empty_if_empty():
    collection = []
    result = ConvertsToString().evaluate(collection)
    assert result == []

def test_convertstostring_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value=BaseException)]
    result = ConvertsToString().evaluate(collection)
    assert result == False

convertstostring_cases = (
    ('string'),
    (123),
    (14.54),
    ('2014-02-01T:12:25'),
    ('2014-02-01'),
    (True),
    (False),
    (Quantity(value=12.5, unit='mg')),
)
@pytest.mark.parametrize("value", convertstostring_cases)
def test_convertstostring_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToString().evaluate(collection)
    assert result == True


#---------------------------
# ToTime()
#---------------------------

def test_totime_returns_empty_if_empty():
    collection = []
    result = ToTime().evaluate(collection)
    assert result == []

def test_totime_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ToTime().evaluate(collection)
    assert result == []

totime_cases = (
    ('2014', '2014'),
    ('2014-02', '2014-02'),
    ('2014-02-01', '2014-02-01'),
    ('2014-02-01T:12:25', '2014-02-01T:12:25'),
    ('2014-02-01T00:00:00.000Z', '2014-02-01T00:00:00.000Z'),
)
@pytest.mark.parametrize("value, expected", totime_cases)
def test_totime_converts_correctly_for_valid_type(value, expected):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ToTime().evaluate(collection)
    assert result == expected


#---------------------------
# ConvertsToTime()
#---------------------------

def test_convertstotime_returns_empty_if_empty():
    collection = []
    result = ConvertsToDateTime().evaluate(collection)
    assert result == []

def test_convertstotime_returns_emtpy_for_invalid_type():
    collection = [FHIRPathCollectionItem(value='invalid')]
    result = ConvertsToDateTime().evaluate(collection)
    assert result == False

convertstotime_cases = (
    ('2014'),
    ('2014-02'),
    ('2014-02-01'),
    ('2014-02-01T:12:25'),
    ('2014-02-01T00:00:00.000Z'),
)
@pytest.mark.parametrize("value", convertstotime_cases)
def test_convertstotime_returns_true_for_valid_type(value):
    collection = [FHIRPathCollectionItem(value=value)]
    result = ConvertsToTime().evaluate(collection)
    assert result == True
