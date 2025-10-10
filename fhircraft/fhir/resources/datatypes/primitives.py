from datetime import date, datetime, time
from typing import Callable, Union

from pydantic import AfterValidator, Field
from typing_extensions import Annotated, TypeAliasType

Boolean = TypeAliasType(
    "Boolean",
    Union[
        bool,
        Annotated[
            str, Field(pattern=r"true|false"), AfterValidator(lambda x: x == "true")
        ],
    ],
)

Integer = TypeAliasType(
    "Integer",
    Union[
        int, Annotated[str, Field(pattern=r"[0]|[-+]?[1-9][0-9]*"), AfterValidator(int)]
    ],
)


Integer64 = TypeAliasType(
    "Integer64",
    Union[
        int, Annotated[str, Field(pattern=r"[0]|[-+]?[1-9][0-9]*"), AfterValidator(int)]
    ],
)

String = TypeAliasType("String", str)


Decimal = TypeAliasType(
    "Decimal",
    Union[
        float,
        Annotated[
            str,
            Field(pattern=r"-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?"),
            AfterValidator(float),
        ],
    ],
)


Uri = TypeAliasType(
    "Uri",
    Annotated[
        str,
        Field(pattern=r"\S*"),
    ],
)


Url = TypeAliasType("Url", str)


Canonical = TypeAliasType("Canonical", str)


Base64Binary = TypeAliasType(
    "Base64Binary", Annotated[str, Field(pattern=r"(\s*([0-9a-zA-Z\+\=]){4}\s*)+")]
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
                pattern=rf"{YEAR_REGEX}-{MONTH_REGEX}-{DAY_REGEX}T{HOUR_REGEX}:{MINUTES_REGEX}:{SECONDS_REGEX}({TIMEZONE_REGEX})?"
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
            Field(pattern=rf"{YEAR_REGEX}(-{MONTH_REGEX}(-{DAY_REGEX})?)?"),
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
                pattern=rf"{YEAR_REGEX}(-{MONTH_REGEX}(-{DAY_REGEX})?)?(T{HOUR_REGEX}(:{MINUTES_REGEX}(:{SECONDS_REGEX}({TIMEZONE_REGEX})?)?)?)?"
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
                pattern=rf"{HOUR_REGEX}(:{MINUTES_REGEX}(:{SECONDS_REGEX}({TIMEZONE_REGEX})?)?)?"
            ),
        ],
    ],
)

Code = TypeAliasType(
    "Code",
    Annotated[
        str,
        Field(pattern=r"[^\s]+(\s[^\s]+)*"),
    ],
)

Oid = TypeAliasType(
    "Oid",
    Annotated[
        str,
        Field(pattern=r"urn:oid:[0-2](\.(0|[1-9][0-9]*))+"),
    ],
)

Id = TypeAliasType(
    "Id",
    Annotated[
        str,
        Field(pattern=r"[A-Za-z0-9\-\.]{1,64}"),
    ],
)

Markdown = TypeAliasType(
    "Markdown",
    Annotated[
        str,
        Field(pattern=r"\s*(\S|\s)*"),
    ],
)


def __integer_validator(criterion: Callable) -> Callable:
    def _validate(value: str):
        integer = int(value)
        if not criterion(integer):
            raise ValueError(f"Value {value} does not satisfy the comparison.")
        return integer

    return _validate


UnsignedInt = TypeAliasType(
    "UnsignedInt",
    Union[
        Annotated[int, Field(ge=0)],
        Annotated[
            str,
            Field(pattern=r"[0]|([1-9][0-9]*)"),
            AfterValidator(__integer_validator(lambda x: x >= 0)),
        ],
    ],
)

PositiveInt = TypeAliasType(
    "PositiveInt",
    Union[
        Annotated[int, Field(gt=0)],
        Annotated[
            str,
            Field(pattern=r"\+?[1-9][0-9]*"),
            AfterValidator(__integer_validator(lambda x: x > 0)),
        ],
    ],
)

Uuid = TypeAliasType("Uuid", str)
