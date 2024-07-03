

from pydantic import Field, AfterValidator
from typing import Union
from typing_extensions import Annotated
import datetime as python_datetime
import re 

# VERSION: R4B
# SOURCE: https://hl7.org/fhir/R4B/datatypes.html#string

Boolean = Union[
    bool,
    Annotated[
        str,
        Field(pattern=r'true|false'),
        AfterValidator(lambda x: x=='true')
    ]
]

Integer = Union[
    int,
    Annotated[
        str,
        Field(pattern=r'[0]|[-+]?[1-9][0-9]*'),
        AfterValidator(int)
    ]
]

String = Annotated[
    str,
    Field(pattern=r'[\r\n\t\S]+')
]


Decimal = Union[
    float,
    Annotated[
        str,
        Field(pattern=r'-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?'),
        AfterValidator(float)
    ]
]


Uri = Annotated[
    str,
    Field(pattern=r'\S*'),
]


Url = str


Canonical = str


Base64Binary = Annotated[
    str,
    Field(pattern=r'(\s*([0-9a-zA-Z\+\=]){4}\s*)+')
]


YEAR_REGEX = r'([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)'
MONTH_REGEX = r'(0[1-9]|1[0-2])'
DAY_REGEX = r'(0[1-9]|[1-2][0-9]|3[0-1])'
HOUR_REGEX = r'([01][0-9]|2[0-3])'
MINUTES_REGEX = r'[0-5][0-9]'
SECONDS_REGEX = r'([0-5][0-9]|60)(\.[0-9]+)'
TIMEZONE_REGEX = r'(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))'

Instant = Union[
    python_datetime.datetime,
    Annotated[
        str,
        Field(pattern=fr'{YEAR_REGEX}-{MONTH_REGEX}-{DAY_REGEX}T{HOUR_REGEX}:{MINUTES_REGEX}:{SECONDS_REGEX}?{TIMEZONE_REGEX}'),
        AfterValidator(lambda d: python_datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ'))
    ]
]

Date = Union[
    python_datetime.date,
    Annotated[
        str,
        Field(pattern=fr'{YEAR_REGEX}(-{MONTH_REGEX}(-{DAY_REGEX})?)?'),
        AfterValidator(
            lambda d: python_datetime.datetime.strptime(d, 
                '%Y' if re.match(fr'^{YEAR_REGEX}$',d)
                else 
                '%Y-%m' if re.match(fr'^{YEAR_REGEX}-{MONTH_REGEX}$',d)
                else 
                '%Y-%m-%d'
            ).date()
        )
    ]
]


DateTime = Union[
    python_datetime.datetime,
    Annotated[
        str,
        Field(pattern=fr'{YEAR_REGEX}((-{MONTH_REGEX}(-{DAY_REGEX})?)?T{HOUR_REGEX}:{MINUTES_REGEX}:{SECONDS_REGEX}?{TIMEZONE_REGEX})?'),
        AfterValidator(lambda d: python_datetime.datetime.strptime(d, 
                '%Y' if re.match(fr'^{YEAR_REGEX}$',d)
                else 
                '%Y-%m' if re.match(fr'^{YEAR_REGEX}-{MONTH_REGEX}$',d)
                else 
                '%Y-%m-%d' if re.match(fr'^{YEAR_REGEX}-{MONTH_REGEX}-{DAY_REGEX}$',d)
                else
                '%Y-%m-%dT%H:%M:%SZ'
            )
        )
    ]
]


Time = Union[
    python_datetime.time,
    Annotated[
        str,
        Field(pattern=fr'{HOUR_REGEX}:{MINUTES_REGEX}:{SECONDS_REGEX}?'),
        AfterValidator(lambda d: python_datetime.datetime.strptime(d, '%H:%M:%S').time())
    ]
]


Code = Annotated[
    str,
    Field(pattern=r'[^\s]+(\s[^\s]+)*'),
]

Oid = Annotated[
    str,
    Field(pattern=r'urn:oid:[0-2](\.(0|[1-9][0-9]*))+'),
]

Id = Annotated[
    str,
    Field(pattern=r'[A-Za-z0-9\-\.]{1,64}'),
]

Markdown = Annotated[
    str,
    Field(pattern=r'\s*(\S|\s)*'),
]

UnsignedInt = Union[
    int, 
    Annotated[
        str,
        Field(pattern=r'[0]|([1-9][0-9]*)'),
        AfterValidator(int)
    ]
]

PositiveInt = Union[
    int, 
    Annotated[
        str,
        Field(pattern=r'\+?[1-9][0-9]*'),
        AfterValidator(int)
    ]
]

Uuid = str