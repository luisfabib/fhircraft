from datetime import date, datetime, time
from typing import Callable, Union

from pydantic import AfterValidator, Field
from typing_extensions import Annotated, TypeAliasType


MAX_SIGNED_32BIT_INT = 2147483647
MIN_SIGNED_32BIT_INT = -2147483648
MAX_SIGNED_64BIT_INT = 9223372036854775807
MIN_SIGNED_64BIT_INT = -9223372036854775808
MAX_UNSIGNED_32BIT_INT = 4294967295
MIN_UNSIGNED_32BIT_INT = 0

def __integer_validator(criterion: Callable) -> Callable:
    def _validate(value: str):
        integer = int(value)
        if not criterion(integer):
            raise ValueError(f"Value {value} does not satisfy the comparison.")
        return integer

    return _validate

String = TypeAliasType("String", str)

Boolean = TypeAliasType(
    "Boolean",
    Union[
        bool,
        Annotated[
            str, Field(pattern=r"^(true|false)$"), AfterValidator(lambda x: x == "true")
        ],
    ],
)

Integer = TypeAliasType(
    "Integer",
    Union[
        Annotated[
            int, 
            Annotated[
                str, 
                Field(pattern=r"^[0]|[-+]?[1-9][0-9]*$"), 
            ],
            AfterValidator(__integer_validator(lambda x: (x >= MIN_SIGNED_32BIT_INT) and (x <= MAX_SIGNED_32BIT_INT)))
        ],
    ],
)


Integer64 = TypeAliasType(
    "Integer64",
    Union[
        Annotated[
            int, 
            Annotated[
                str, 
                Field(pattern=r"^[0]|[-+]?[1-9][0-9]*$"), 
            ],
            AfterValidator(__integer_validator(lambda x: x >= MIN_SIGNED_64BIT_INT and x <= MAX_SIGNED_64BIT_INT))
        ],
    ],
)


UnsignedInt = TypeAliasType(
    "UnsignedInt",
    Union[
        Annotated[
            int,
            Annotated[
                str,
                Field(pattern=r"[0]|([1-9][0-9]*)"),
            ],
            AfterValidator(__integer_validator(lambda x: x >= MIN_UNSIGNED_32BIT_INT and x <= MAX_UNSIGNED_32BIT_INT)),
        ],
    ],
)

PositiveInt = TypeAliasType(
    "PositiveInt",
    Union[
        Annotated[
            int,
            Annotated[
                str,
                Field(pattern=r"\+?[1-9][0-9]*"),
            ],
            AfterValidator(__integer_validator(lambda x: x >= 1 and x <= MAX_SIGNED_32BIT_INT)),
        ],
    ],
)



Decimal = TypeAliasType(
    "Decimal",
    Union[
        float,
        Annotated[
            str,
            Field(pattern=r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$"),
            AfterValidator(float),
        ],
    ],
)


Uri = TypeAliasType(
    "Uri",
    Annotated[
        str,
        # Regex according to RFC 3986 (https://datatracker.ietf.org/doc/html/rfc3986#page-50)
        Field(pattern=r"^(([^:\/?#\s]+):)(\/\/([^\/?#\s]*))?([^\s?#]+)(\?([^#]*))?(#(.*))?$"),
    ],
)


Url = TypeAliasType(
    "Url",
    Annotated[
        str,
        # Regex according to RFC 1738 (https://datatracker.ietf.org/doc/html/rfc1738)
        Field(pattern=r"^(?i)\b((?:[a-z][\w-]+:(?:\/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?]))$",),
    ],
)


Canonical = TypeAliasType(
    "Canonical",
    Annotated[
        str,
        # Regex according to RFC 3986 (https://datatracker.ietf.org/doc/html/rfc3986#page-50)
        Field(pattern=r"^(([^:\/?#\s]+):)(\/\/([^\/?#\s]*))?([^\s?#]+)(\?([^#]*))?(#(.*))?$"),
    ],
)


Base64Binary = TypeAliasType(
    "Base64Binary", Annotated[str, Field(pattern=r"^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$")]
)


YEAR_REGEX = r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)"
MONTH_REGEX = r"(0[1-9]|1[0-2])"
DAY_REGEX = r"(0[1-9]|[1-2][0-9]|3[0-1])"
HOUR_REGEX = r"([01][0-9]|2[0-3])"
MINUTES_REGEX = r"[0-5][0-9]"
SECONDS_REGEX = r"([0-5][0-9]|60)(\.[0-9]+)?"
TIMEZONE_REGEX = r"Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)"

Instant = TypeAliasType(
    "Instant",
    Union[
        Annotated[datetime, Field(), AfterValidator(lambda d: d.isoformat())],
        Annotated[
            str,
            Field(
                pattern=rf"^{YEAR_REGEX}-{MONTH_REGEX}-{DAY_REGEX}T{HOUR_REGEX}:{MINUTES_REGEX}:{SECONDS_REGEX}({TIMEZONE_REGEX})?$"
            ),
        ],
    ],
)

Date = TypeAliasType(
    "Date",
    Union[
        Annotated[date, Field(), AfterValidator(lambda d: d.isoformat())],
        Annotated[
            str,
            Field(pattern=rf"^{YEAR_REGEX}(-{MONTH_REGEX}(-{DAY_REGEX})?)?$"),
        ],
    ],
)


DateTime = TypeAliasType(
    "DateTime",
    Union[
        Annotated[datetime, Field(), AfterValidator(lambda d: d.isoformat())],
        Annotated[
            str,
            Field(
                pattern=rf"^{YEAR_REGEX}(-{MONTH_REGEX}(-{DAY_REGEX})?)?(T{HOUR_REGEX}(:{MINUTES_REGEX}(:{SECONDS_REGEX}({TIMEZONE_REGEX})?)?)?)?$"
            ),
        ],
    ],
)

Time = TypeAliasType(
    "Time",
    Union[
        Annotated[time, Field(), AfterValidator(lambda t: t.isoformat())],
        Annotated[
            str,
            Field(
                pattern=rf"^{HOUR_REGEX}(:{MINUTES_REGEX}(:{SECONDS_REGEX}({TIMEZONE_REGEX})?)?)?$"
            ),
        ],
    ],
)

Code = TypeAliasType(
    "Code",
    Annotated[
        str,
        Field(pattern=r"^[^\s]+(\s[^\s]+)*$"),
    ],
)

Oid = TypeAliasType(
    "Oid",
    Annotated[
        str,
        Field(pattern=r"^urn:oid:[0-2](\.(0|[1-9][0-9]*))+$"),
    ],
)


Uuid = TypeAliasType(
    "Uuid",
    Annotated[
        str,
        Field(pattern=r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"),
    ],
)

Id = TypeAliasType(
    "Id",
    Annotated[
        str,
        Field(pattern=r"^[A-Za-z0-9\-\.]{1,64}$"),
    ],
)

Markdown = TypeAliasType(
    "Markdown",
    Annotated[
        str,
        Field(pattern=r"^\s*(\S|\s)*$"),
    ],
)

