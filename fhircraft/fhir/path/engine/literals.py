from decimal import Decimal as PythonDecimal
from dataclasses import dataclass 
from typing import Union, Optional
import operator
from abc import ABC 
import re 
from datetime import date, time, datetime

class FHIRPathLiteralType(ABC):
    pass


@dataclass
class Quantity(FHIRPathLiteralType):
    value: Union[int, float]
    unit: Optional[str]

    def __comparison__(self, other, op):
        if self.unit == other.unit:
            return op(self.value, other.value)
        else: 
            return []
        
    def __math__(self, other, op):
        if self.unit == other.unit:
            return Quantity(op(self.value, other.value), self.unit)
        else:
            return []
        
    def __abs__(self):
        return Quantity(abs(self.value), self.unit)

    def __lt__(self, other):
        return self.__comparison__(other, operator.lt)

    def __le__(self, other):
        return self.__comparison__(other, operator.le)
        
    def __gt__(self, other):
        return self.__comparison__(other, operator.gt)

    def __ge__(self, other):
        return self.__comparison__(other, operator.ge)

    def __add__(self, other):
        return self.__math__(other, operator.add)

    def __sub__(self, other):
        return self.__math__(other, operator.sub)

    def __mul__(self, other):
        return self.__math__(other, operator.mul)

    def __truediv__(self, other):
        return self.__math__(other, operator.truediv)


@dataclass
class Date(FHIRPathLiteralType):
    year: int
    month: Optional[int]
    day: Optional[int]
     
    def __init__(self, valuestring):
        match = re.match(r'\@(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?', valuestring)
        if match:
            groups = match.groups()
            self.year, self.month, self.day  = [int(group) if group else None for group in list(groups) + [None for _ in range(3 - len(groups))] ]
        else: 
            raise ValueError(f'Invalid string format "{valuestring}" for Date type') 

    def to_date(self):
        return date(self.year, self.month or 1, self.day or 1)

    def __comparison__(self, other, op):
        if isinstance(other, Date):
            if all([
                (getattr(self, part) is not None) == (getattr(other, part) is not None) 
                    for part in ['day', 'month', 'year']
            ]):
                return op(self.to_date(), other.to_date())
            else: 
                return []
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
     
    def __init__(self, valuestring):
        match = re.match(r'\@T(\d{2})(?:\:(\d{2})(?:\:(\d{2})(?:\.(\d{3})(?:([+|-]\d{2})(?:\:(\d{2}))?)?)?)?)?', valuestring)
        if match:
            groups = match.groups()
            self.hour, self.minute, self.second, self.millisecond, self.hour_shift, self.minute_shift = [
                int(group) if group else None for group in list(groups) + [None for _ in range(6 - len(groups))] 
            ]
        else: 
            raise ValueError(f'Invalid string format "{valuestring}" for Time type') 

    def to_time(self):
        return time(self.hour, self.minute or 0, self.second or 0, self.millisecond or 0)

    def __comparison__(self, other, op):
        if isinstance(other, Time):
            if all([
                (getattr(self, part) is not None) == (getattr(other, part) is not None) 
                    for part in ['hour', 'minute', 'second', 'millisecond', 'hour_shift', 'minute_shift']
            ]):
                return op(self.to_time(), other.to_time())
            else: 
                return []
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

    def __init__(self, valuestring):
        match = re.match(r'\@([0-9]{4})(?:-([0-9]{2})(?:-?([0-9]{2})T(?:(\d{2})(?:\:(\d{2})(?:\:(\d{2})(?:\.(\d{3})(?:([+|-]\d{2})(?:\:(\d{2}))?)?)?)?)?)?)?)?', valuestring)
        if match:
            groups = match.groups()
            self.year, self.month, self.day, self.hour, self.minute, self.second, self.millisecond, self.hour_shift, self.minute_shift = [
                int(group) if group else None for group in list(groups) + [None for _ in range(9 - len(groups))] 
            ]
        else: 
            raise ValueError(f'Invalid string format "{valuestring}" for DateTime type') 

    def to_datetime(self):
        return datetime(self.year, self.month or 1, self.day or 1, self.hour or 0, self.minute or 0, self.second or 0, self.millisecond or 0)

    def __comparison__(self, other, op):
        if isinstance(other, DateTime):
            if all([
                (getattr(self, part) is not None) == (getattr(other, part) is not None) 
                    for part in ['year', 'month', 'day', 'hour', 'minute', 'second', 'millisecond', 'hour_shift', 'minute_shift']
            ]):
                return op(self.to_datetime(), other.to_datetime())
            else: 
                return []
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


