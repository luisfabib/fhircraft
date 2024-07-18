

from pydantic import Field, AfterValidator, PlainSerializer, BaseModel
from typing import Union
from typing_extensions import Annotated, TypeAliasType
import datetime as python_datetime
import re 

# VERSION: R4B
# SOURCE: https://hl7.org/fhir/R4B/datatypes.html#string

Boolean = TypeAliasType('Boolean', Union[
    bool,
    Annotated[
        str,
        Field(pattern=r'true|false'),
        AfterValidator(lambda x: x=='true')
    ]
])

Integer = TypeAliasType('Integer', Union[
    int,
    Annotated[
        str,
        Field(pattern=r'[0]|[-+]?[1-9][0-9]*'),
        AfterValidator(int)
    ]
])


Integer64 = TypeAliasType('Integer64', Union[
    int,
    Annotated[
        str,
        Field(pattern=r'[0]|[-+]?[1-9][0-9]*'),
        AfterValidator(int)
    ]
])

String = TypeAliasType('String', str)


Decimal = TypeAliasType('Decimal', Union[
    float,
    Annotated[
        str,
        Field(pattern=r'-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?'),
        AfterValidator(float)
    ]
])


Uri = TypeAliasType('Uri', Annotated[
    str,
    Field(pattern=r'\S*'),
])


Url = TypeAliasType('Url', str)


Canonical = TypeAliasType('Canonical', str)


Base64Binary = TypeAliasType('Base64Binary', Annotated[
    str,
    Field(pattern=r'(\s*([0-9a-zA-Z\+\=]){4}\s*)+')
])


YEAR_REGEX = r'([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)'
MONTH_REGEX = r'(0[1-9]|1[0-2])'
DAY_REGEX = r'(0[1-9]|[1-2][0-9]|3[0-1])'
HOUR_REGEX = r'([01][0-9]|2[0-3])'
MINUTES_REGEX = r'[0-5][0-9]'
SECONDS_REGEX = r'([0-5][0-9]|60)(\.[0-9]+)?'
TIMEZONE_REGEX = r'Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)'    
   
Instant = TypeAliasType('Instant', Annotated[
    str,
    Field(pattern=fr'{YEAR_REGEX}-{MONTH_REGEX}-{DAY_REGEX}T{HOUR_REGEX}:{MINUTES_REGEX}:{SECONDS_REGEX}({TIMEZONE_REGEX})?'),
])

Date = TypeAliasType('Date',
    Annotated[
        str,
        Field(pattern=fr'{YEAR_REGEX}(-{MONTH_REGEX}(-{DAY_REGEX})?)?'),
    ]
)

DateTime = TypeAliasType('DateTime',
    Annotated[
        str,
        Field(pattern=fr'{YEAR_REGEX}(-{MONTH_REGEX}(-{DAY_REGEX})?)?(T{HOUR_REGEX}(:{MINUTES_REGEX}(:{SECONDS_REGEX}({TIMEZONE_REGEX})?)?)?)?'),
    ]
)

Time = TypeAliasType('Time',
    Annotated[
        str,
        Field(pattern=fr'{HOUR_REGEX}(:{MINUTES_REGEX}(:{SECONDS_REGEX}({TIMEZONE_REGEX})?)?)?'),
    ]
)

Code = TypeAliasType('Code', Annotated[
    str,
    Field(pattern=r'[^\s]+(\s[^\s]+)*'),
])

Oid = TypeAliasType('Oid', Annotated[
    str,
    Field(pattern=r'urn:oid:[0-2](\.(0|[1-9][0-9]*))+'),
])

Id = TypeAliasType('Id', Annotated[
    str,
    Field(pattern=r'[A-Za-z0-9\-\.]{1,64}'),
])

Markdown = TypeAliasType('Markdown', Annotated[
    str,
    Field(pattern=r'\s*(\S|\s)*'),
])

UnsignedInt = TypeAliasType('UnsignedInt', Union[
    int, 
    Annotated[
        str,
        Field(pattern=r'[0]|([1-9][0-9]*)'),
        AfterValidator(int)
    ]
])

PositiveInt = TypeAliasType('PositiveInt', Union[
    int, 
    Annotated[
        str,
        Field(pattern=r'\+?[1-9][0-9]*'),
        AfterValidator(int)
    ]
])

Uuid = TypeAliasType('Uuid', str)