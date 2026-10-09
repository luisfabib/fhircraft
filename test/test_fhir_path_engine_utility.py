from fhircraft.fhir.path.collection import FHIRPathCollection
from fhircraft.fhir.path.engine.core import Element, FHIRPathCollectionItem
from fhircraft.fhir.path.engine.environment import EnvironmentVariable
from fhircraft.fhir.path.engine.literals import Date, Time, DateTime
from fhircraft.fhir.path.engine.utility import *
import datetime 
import logging

env = dict()

# -------------
# Trace
# -------------


def test_trace_logs_collection_and_returns_input(caplog):
    caplog.set_level(logging.INFO)
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
    ]
    result = Trace("TestTrace").evaluate(FHIRPathCollection(collection), env)
    assert result == collection


def test_trace_string_representation():
    expression = Trace("TestTrace", Element("field"))
    assert str(expression) == "trace('TestTrace', field)"


def test_trace_logs_collection_with_fhirpath(caplog):
    caplog.set_level(logging.INFO)
    collection = [
        FHIRPathCollectionItem(value="item1"),
        FHIRPathCollectionItem(value="item2"),
    ]
    result = Trace(EnvironmentVariable("%name")).evaluate(
        FHIRPathCollection(collection), {"%name": "DynamicTrace"}
    )
    assert result == collection


# -------------
# Today
# -------------


def test_today_returns_current_date():
    result = Today().evaluate(FHIRPathCollection([]), env)
    assert isinstance(result[0], Date)
    assert result[0] == Date(value_date=datetime.datetime.now().date())


def test_today_string_representation():
    expression = Today()
    assert str(expression) == "today()"


# -------------
# Now
# -------------


def test_now_returns_datetime_with_timezone_offset():
    result = Now().evaluate(FHIRPathCollection([]), env)
    assert isinstance(result[0], DateTime)
    assert result[0].hour_shift is not None
    assert result[0].minute_shift is not None


def test_now_string_representation():
    expression = Now()
    assert str(expression) == "now()"


# -------------
# TimeOfDay
# -------------


def test_timeofday_returns_current_time():
    result = TimeOfDay().evaluate(FHIRPathCollection([]), env)
    assert isinstance(result[0], Time)


def test_timeofday_string_representation():
    expression = TimeOfDay()
    assert str(expression) == "timeOfDay()"
