import operator
from pathlib import Path
import re
import warnings
from abc import ABC
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional, Union
from pint import UnitRegistry, Quantity as PintQuantity

# Load the Pint unit registry with UCUM definitions
ureg = UnitRegistry()
ureg.load_definitions(Path(__file__).resolve().parent / "ucum_to_pint.txt")


class FHIRPathLiteralType(ABC):
    pass


@dataclass
class Quantity(FHIRPathLiteralType):
    value: Union[int, float]
    unit: Optional[str]

    def __comparison__(self, other, op) -> bool:
        if isinstance(other, Quantity):
            return op(
                self.value * ureg(self.unit or ""), other.value * ureg(other.unit or "")
            )
        elif isinstance(other, (int, float)) and self.unit in (None, "1"):
            return op(self.value, other)
        else:
            raise TypeError(f"Comparisons with {type(other)} not supported")

    def __math__(self, other, op) -> PintQuantity:
        if isinstance(other, Quantity):
            return op(
                self.value * ureg(self.unit or ""), other.value * ureg(other.unit or "")
            )
        elif isinstance(other, (int, float)):
            return op(self.value, other)
        else:
            raise TypeError(f"Operations with {type(other)} not supported")

    def __abs__(self):
        return Quantity(abs(self.value), self.unit)

    def __eq__(self, other):
        return self.__comparison__(other, operator.eq)

    def __lt__(self, other):
        return self.__comparison__(other, operator.lt)

    def __le__(self, other):
        return self.__comparison__(other, operator.le)

    def __gt__(self, other):
        return self.__comparison__(other, operator.gt)

    def __ge__(self, other):
        return self.__comparison__(other, operator.ge)

    def __add__(self, other):
        result = self.__math__(other, operator.add)
        return Quantity(
            value=result.to(self.unit).magnitude,
            unit=self.unit,
        )

    def __sub__(self, other):
        result = self.__math__(other, operator.sub)
        return Quantity(
            value=result.to(self.unit).magnitude,
            unit=self.unit,
        )

    def __mul__(self, other):
        result = self.__math__(other, operator.mul)
        return Quantity(
            value=result.magnitude,
            unit=f"{self.unit}*{other.unit}",
        )

    def __floordiv__(self, other):
        result = self.__math__(other, operator.floordiv)
        return Quantity(
            value=result.magnitude,
            unit=f"{self.unit}/{other.unit}" if self.unit != other.unit else "1",
        )

    def __truediv__(self, other):
        result = self.__math__(other, operator.truediv)
        return Quantity(
            value=result.magnitude,
            unit=f"{self.unit}/{other.unit}" if self.unit != other.unit else "1",
        )


@dataclass
class Date(FHIRPathLiteralType):
    year: int
    month: Optional[int]
    day: Optional[int]

    def __init__(self, valuestring=None, value_date=None):
        if valuestring:
            match = re.match(r"\@(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?", valuestring)
            if match:
                groups = match.groups()
                self.year, self.month, self.day = [  # type: ignore
                    int(group) if group else None
                    for group in list(groups) + [None for _ in range(3 - len(groups))]
                ]
            else:
                raise ValueError(f'Invalid string format "{valuestring}" for Date type')
        elif value_date:
            self.year = value_date.year
            self.month = value_date.month
            self.day = value_date.day

    def to_date(self):
        return date(self.year, self.month or 1, self.day or 1)

    def __comparison__(self, other, op):
        if isinstance(other, Date):
            if all(
                [
                    (getattr(self, part) is not None)
                    == (getattr(other, part) is not None)
                    for part in ["day", "month", "year"]
                ]
            ):
                return op(self.to_date(), other.to_date())
            else:
                return []
        elif isinstance(other, date):
            return op(self.to_date(), other)
        else:
            raise TypeError("Comparisons only supported between Date objects")

    def __lt__(self, other):
        return self.__comparison__(other, operator.lt)

    def __le__(self, other):
        return self.__comparison__(other, operator.le)

    def __gt__(self, other):
        return self.__comparison__(other, operator.gt)

    def __ge__(self, other):
        return self.__comparison__(other, operator.ge)

    def __eq__(self, other):
        return self.__comparison__(other, operator.eq)

    def __ne__(self, other):
        return self.__comparison__(other, operator.ne)


@dataclass
class Time(FHIRPathLiteralType):
    hour: int
    minute: Optional[int]
    second: Optional[int]
    millisecond: Optional[int]
    hour_shift: Optional[int]
    minute_shift: Optional[int]

    def __init__(
        self, valuestring: str | None = None, value_time: datetime | None = None
    ):
        if valuestring:
            match = re.match(
                r"\@T(\d{2})(?:\:(\d{2})(?:\:(\d{2})(?:\.(\d{3})(?:([+|-]\d{2})(?:\:(\d{2}))?)?)?)?)?",
                valuestring,
            )
            if match:
                groups = match.groups()
                (
                    self.hour,  # type: ignore
                    self.minute,
                    self.second,
                    self.millisecond,
                    self.hour_shift,
                    self.minute_shift,
                ) = [
                    int(group) if group else None
                    for group in list(groups) + [None for _ in range(6 - len(groups))]
                ]
            else:
                raise ValueError(f'Invalid string format "{valuestring}" for Time type')
        elif value_time:
            self.hour = value_time.hour
            self.minute = value_time.minute
            self.second = value_time.second
            self.millisecond = value_time.microsecond // 1000
            self.hour_shift = None
            self.minute_shift = None

    def to_time(self):
        return time(
            self.hour, self.minute or 0, self.second or 0, self.millisecond or 0
        )

    def __comparison__(self, other, op):
        if isinstance(other, Time):
            if all(
                [
                    (getattr(self, part) is not None)
                    == (getattr(other, part) is not None)
                    for part in [
                        "hour",
                        "minute",
                        "second",
                        "millisecond",
                        "hour_shift",
                        "minute_shift",
                    ]
                ]
            ):
                return op(self.to_time(), other.to_time())
            else:
                return []
        elif isinstance(other, time):
            return op(self.to_time(), other)
        else:
            raise TypeError("Comparisons only supported between Date objects")

    def __lt__(self, other):
        return self.__comparison__(other, operator.lt)

    def __le__(self, other):
        return self.__comparison__(other, operator.le)

    def __gt__(self, other):
        return self.__comparison__(other, operator.gt)

    def __ge__(self, other):
        return self.__comparison__(other, operator.ge)

    def __eq__(self, other):
        return self.__comparison__(other, operator.eq)

    def __ne__(self, other):
        return self.__comparison__(other, operator.ne)


@dataclass
class DateTime(FHIRPathLiteralType):
    year: int
    month: Optional[int]
    day: Optional[int]
    hour: Optional[int]
    minute: Optional[int]
    second: Optional[int]
    millisecond: Optional[int]
    hour_shift: Optional[int]
    minute_shift: Optional[int]

    def __init__(
        self, valuestring: str | None = None, value_datetime: datetime | None = None
    ):
        if valuestring:
            match = re.match(
                r"\@([0-9]{4})(?:-([0-9]{2})(?:-?([0-9]{2})T(?:(\d{2})(?:\:(\d{2})(?:\:(\d{2})(?:\.(\d{3})(?:([+|-]\d{2})(?:\:(\d{2}))?)?)?)?)?)?)?)?",
                valuestring,
            )
            if match:
                groups = match.groups()
                (
                    self.year,  # type: ignore
                    self.month,
                    self.day,
                    self.hour,
                    self.minute,
                    self.second,
                    self.millisecond,
                    self.hour_shift,
                    self.minute_shift,
                ) = [
                    int(group) if group else None
                    for group in list(groups) + [None for _ in range(9 - len(groups))]
                ]
            else:
                raise ValueError(
                    f'Invalid string format "{valuestring}" for DateTime type'
                )
        elif value_datetime:
            self.year = value_datetime.year
            self.month = value_datetime.month
            self.day = value_datetime.day
            self.hour = value_datetime.hour
            self.minute = value_datetime.minute
            self.second = value_datetime.second
            self.millisecond = value_datetime.microsecond // 1000
            self.hour_shift = None
            self.minute_shift = None

    def to_datetime(self):
        return datetime(
            self.year,
            self.month or 1,
            self.day or 1,
            self.hour or 0,
            self.minute or 0,
            self.second or 0,
            self.millisecond or 0,
        )

    def __comparison__(self, other, op):
        if isinstance(other, DateTime):
            if all(
                [
                    (getattr(self, part) is not None)
                    == (getattr(other, part) is not None)
                    for part in [
                        "year",
                        "month",
                        "day",
                        "hour",
                        "minute",
                        "second",
                        "millisecond",
                        "hour_shift",
                        "minute_shift",
                    ]
                ]
            ):
                return op(self.to_datetime(), other.to_datetime())
            else:
                return []
        elif isinstance(other, datetime):
            return op(self.to_datetime(), other)
        else:
            raise TypeError("Comparisons only supported between Date objects")

    def __lt__(self, other):
        return self.__comparison__(other, operator.lt)

    def __le__(self, other):
        return self.__comparison__(other, operator.le)

    def __gt__(self, other):
        return self.__comparison__(other, operator.gt)

    def __ge__(self, other):
        return self.__comparison__(other, operator.ge)

    def __eq__(self, other):
        return self.__comparison__(other, operator.eq)

    def __ne__(self, other):
        return self.__comparison__(other, operator.ne)
