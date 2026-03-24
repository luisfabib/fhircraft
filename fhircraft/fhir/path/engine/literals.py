import operator
from pathlib import Path
import re
import warnings
from abc import ABC
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Optional, Union, Any, TYPE_CHECKING
from pint import UnitRegistry, Quantity as PintQuantity
from fhircraft.fhir.path.exceptions import FhirPathWarning

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4.complex.quantity import (
        Quantity as R4_Quantity,
    )
    from fhircraft.fhir.resources.datatypes.R4B.complex.quantity import (
        Quantity as R4B_Quantity,
    )
    from fhircraft.fhir.resources.datatypes.R5.complex.quantity import (
        Quantity as R5_Quantity,
    )

# Load the Pint unit registry with UCUM definitions
ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)
ureg.load_definitions(Path(__file__).resolve().parent / "ucum_to_pint.txt")


class TypePrecisionError(TypeError):
    pass


class FHIRPathLiteralType(ABC):
    pass


@dataclass
class Quantity(FHIRPathLiteralType):
    value: Union[int, float]
    unit: Optional[str]

    @classmethod
    def is_quantity(cls, instance: Any) -> bool:
        from fhircraft.fhir.resources.datatypes.R4.complex.quantity import (
            Quantity as R4_Quantity,
        )
        from fhircraft.fhir.resources.datatypes.R4B.complex.quantity import (
            Quantity as R4B_Quantity,
        )
        from fhircraft.fhir.resources.datatypes.R5.complex.quantity import (
            Quantity as R5_Quantity,
        )

        return isinstance(instance, (cls, R4_Quantity, R4B_Quantity, R5_Quantity))

    @classmethod
    def parse_quantity(
        cls,
        instance: Union[
            "Quantity", "R4_Quantity", "R4B_Quantity", "R5_Quantity", int, float
        ],
    ) -> "Quantity":
        from fhircraft.fhir.resources.datatypes.R4.complex.quantity import (
            Quantity as R4_Quantity,
        )
        from fhircraft.fhir.resources.datatypes.R4B.complex.quantity import (
            Quantity as R4B_Quantity,
        )
        from fhircraft.fhir.resources.datatypes.R5.complex.quantity import (
            Quantity as R5_Quantity,
        )

        if isinstance(instance, Quantity):
            return instance
        elif isinstance(instance, (R4_Quantity, R4B_Quantity, R5_Quantity)):
            if instance.system not in (None, "http://unitsofmeasure.org"):
                warnings.warn(
                    f"Quantity with non-UCUM system '{instance.system}' may not be parsed correctly.",
                    FhirPathWarning,
                )
            if not instance.value:
                raise ValueError("Quantity value is required")
            return cls(value=float(instance.value), unit=instance.code or instance.unit)
        elif isinstance(instance, (int, float)):
            return cls(value=instance, unit="")
        else:
            raise TypeError("Input must be a FHIRPath Quantity or FHIR Quantity type.")

    @property
    def registry_unit(self) -> PintQuantity:
        _unit = self.unit or ""
        # UCUM square brackets not supported by Pint; replace with nothing
        _unit = _unit.replace("[", "").replace("]", "")
        # UCUM single-quotes not supported by Pint; replace with underscores
        _unit = _unit.replace("'", "_")
        # UCUM curly braces not supported by Pint; replace with nothing
        _unit = re.sub(r"\{.*?\}", "_1", _unit)
        return ureg(_unit)

    def is_compatible_with(self, unit: "Quantity") -> bool:
        return self.registry_unit.is_compatible_with(unit.registry_unit)

    def __comparison__(self, other, op) -> bool:
        if isinstance(other, Quantity):
            if not self.is_compatible_with(other):
                raise ValueError(
                    f"Cannot perform logical comparisons between incompatible units: {self.unit} and {other.unit}"
                )
            return op(
                self.value * self.registry_unit, other.value * other.registry_unit
            )
        elif isinstance(other, (int, float)) and not self.unit:
            return op(self.value, other)
        else:
            raise TypeError("Comparisons only supported between Quantity objects")

    def __math__(self, other, op) -> PintQuantity:
        if isinstance(other, Quantity):
            return op(
                self.value * self.registry_unit, other.value * other.registry_unit
            )
        elif isinstance(other, (int, float)) and not self.unit:
            return op(self.value, other)
        else:
            raise TypeError(f"Operations with {type(other)} not supported")

    def __abs__(self):
        return Quantity(abs(self.value), self.unit)

    def __eq__(self, other):
        if isinstance(other, Quantity):
            return self.__comparison__(other, operator.eq)
        else:
            return False

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
        if not self.is_compatible_with(other):
            raise ValueError(
                f"Cannot perform additions between incompatible units: {self.unit} and {other.unit}"
            )
        return Quantity(
            value=result.to(self.registry_unit).magnitude,
            unit=self.unit,
        )

    def __sub__(self, other):
        result = self.__math__(other, operator.sub)
        if not self.is_compatible_with(other):
            raise ValueError(
                f"Cannot perform subtractions between incompatible units: {self.unit} and {other.unit}"
            )
        return Quantity(
            value=result.to(self.registry_unit).magnitude,
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
            unit=f"{self.unit}/{other.unit}" if self.unit != other.unit else "",
        )

    def __truediv__(self, other):
        result = self.__math__(other, operator.truediv)
        return Quantity(
            value=result.magnitude,
            unit=f"{self.unit}/{other.unit}" if self.unit != other.unit else "",
        )

    def __repr__(self):
        return f"Quantity({self.value}, '{self.unit}')"


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

    def __comparison__(self, other, op) -> bool:
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
                raise TypePrecisionError(
                    "Comparison cannot be performed between Date values with different levels of precision"
                )
        elif isinstance(other, date):
            return op(self.to_date(), other)
        else:
            raise TypeError("Comparisons only supported between Date or date objects")

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
    second: Optional[float]
    hour_shift: Optional[int]
    minute_shift: Optional[int]

    def __init__(self, valuestring: str | None = None, value_time: time | None = None):
        if valuestring:
            match = re.match(
                r"\@T(\d{2})(?:\:(\d{2})(?:\:(\d{2})(?:\.(\d{1,3})(?:([+|-]\d{2})(?:\:(\d{2}))?)?)?)?)?",
                valuestring,
            )
            if match:
                groups = match.groups()
                self.hour = int(groups[0]) if groups[0] else None  # type: ignore
                self.minute = int(groups[1]) if groups[1] else None
                second_int = int(groups[2]) if groups[2] is not None else None
                millisecond_int = int(groups[3]) if groups[3] is not None else None
                self.second = (
                    (
                        second_int
                        + (
                            millisecond_int / (10 ** len(str(millisecond_int)))
                            if millisecond_int is not None
                            else 0.0
                        )
                    )
                    if second_int is not None
                    else None
                )
                self.hour_shift = int(groups[4]) if groups[4] else None
                self.minute_shift = int(groups[5]) if groups[5] else None
                if valuestring.endswith("Z"):
                    self.hour_shift = 0
                    self.minute_shift = 0
            else:
                raise ValueError(f'Invalid string format "{valuestring}" for Time type')
        elif value_time:
            self.hour = value_time.hour
            self.minute = value_time.minute
            self.second = value_time.second + value_time.microsecond / 1_000_000
            self.hour_shift = None
            self.minute_shift = None
            if value_time.tzinfo:
                offset = value_time.utcoffset()
                if offset is not None:
                    total_minutes = int(offset.total_seconds() // 60)
                    self.hour_shift = total_minutes // 60
                    self.minute_shift = total_minutes % 60

    def to_time(self):
        second_int = int(self.second) if self.second is not None else 0
        microsecond = round(((self.second or 0.0) % 1) * 1_000_000)
        return time(
            self.hour,
            self.minute or 0,
            second_int,
            microsecond,
            tzinfo=(
                timezone(
                    timedelta(
                        hours=self.hour_shift or 0, minutes=self.minute_shift or 0
                    )
                )
                if self.hour_shift is not None and self.minute_shift is not None
                else None
            ),
        )

    def __comparison__(self, other, op) -> bool:
        if isinstance(other, Time):
            if all(
                [
                    (getattr(self, part) is not None)
                    == (getattr(other, part) is not None)
                    for part in [
                        "hour",
                        "minute",
                        "second",
                        "hour_shift",
                        "minute_shift",
                    ]
                ]
            ):
                return op(self.to_time(), other.to_time())
            else:
                raise TypePrecisionError(
                    "Comparison cannot be performed between Time values with different levels of precision"
                )
        elif isinstance(other, time):
            return op(self.to_time(), other)
        else:
            raise TypeError(
                "Comparison can only be performed between Time objects or time instances"
            )

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
    second: Optional[float]
    hour_shift: Optional[int]
    minute_shift: Optional[int]

    def __init__(
        self, valuestring: str | None = None, value_datetime: datetime | None = None
    ):
        if valuestring:
            match = re.match(
                r"\@([0-9]{4})(?:-([0-9]{2})(?:-?([0-9]{2})T(?:(\d{2})(?:\:(\d{2})(?:\:(\d{2})(?:\.(\d{1,3})(?:([+|-]\d{2})(?:\:(\d{2}))?)?)?)?)?)?)?)?",
                valuestring,
            )
            if match:
                groups = match.groups()
                padded = list(groups) + [None] * (9 - len(groups))
                self.year = int(padded[0]) if padded[0] else None  # type: ignore
                self.month = int(padded[1]) if padded[1] else None
                self.day = int(padded[2]) if padded[2] else None
                self.hour = int(padded[3]) if padded[3] else None
                self.minute = int(padded[4]) if padded[4] else None
                second_int = int(padded[5]) if padded[5] is not None else None
                millisecond_int = int(padded[6]) if padded[6] is not None else None
                self.second = (
                    (
                        second_int
                        + (
                            millisecond_int / (10 ** len(str(millisecond_int)))
                            if millisecond_int is not None
                            else 0.0
                        )
                    )
                    if second_int is not None
                    else None
                )
                self.hour_shift = int(padded[7]) if padded[7] else None
                self.minute_shift = int(padded[8]) if padded[8] else None
                if valuestring.endswith("Z"):
                    self.hour_shift = 0
                    self.minute_shift = 0
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
            self.second = value_datetime.second + value_datetime.microsecond / 1_000_000
            self.hour_shift = None
            self.minute_shift = None
            if value_datetime.tzinfo:
                offset = value_datetime.utcoffset()
                if offset is not None:
                    total_minutes = int(offset.total_seconds() // 60)
                    self.hour_shift = total_minutes // 60
                    self.minute_shift = total_minutes % 60

    def to_datetime(self):
        second_int = int(self.second) if self.second is not None else 0
        microsecond = round(((self.second or 0.0) % 1) * 1_000_000)
        return datetime(
            self.year,
            self.month or 1,
            self.day or 1,
            self.hour or 0,
            self.minute or 0,
            second_int,
            microsecond,
            tzinfo=(
                timezone(
                    timedelta(
                        hours=self.hour_shift or 0, minutes=self.minute_shift or 0
                    )
                )
                if self.hour_shift is not None and self.minute_shift is not None
                else None
            ),
        )

    def __comparison__(self, other, op) -> bool:
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
                        "hour_shift",
                        "minute_shift",
                    ]
                ]
            ):
                return op(self.to_datetime(), other.to_datetime())
            else:
                raise TypePrecisionError(
                    "Comparison cannot be performed between DateTime values with different levels of precision"
                )
        elif isinstance(other, datetime):
            return op(self.to_datetime(), other)
        else:
            raise TypeError(
                "Comparison can only be performed between DateTime objects or datetime instances"
            )

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
