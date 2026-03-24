from datetime import timedelta, timezone

import pytest

from fhircraft.fhir.path.engine.literals import *

from fhircraft.fhir.resources.datatypes.R4.complex.quantity import (
    Quantity as R4_Quantity,
)
from fhircraft.fhir.resources.datatypes.R4B.complex.quantity import (
    Quantity as R4B_Quantity,
)
from fhircraft.fhir.resources.datatypes.R5.complex.quantity import (
    Quantity as R5_Quantity,
)


def test_fhirpath_type_quantity_init():
    value = Quantity(value=1, unit="m")
    assert isinstance(value, Quantity)


def test_fhirpath_type_quantity_parse_quantity():
    value = Quantity.parse_quantity(Quantity(value=1, unit="m"))
    assert isinstance(value, Quantity)
    value_r4 = Quantity.parse_quantity(R4_Quantity(value=1, unit="m"))
    assert isinstance(value_r4, Quantity)
    value_r4b = Quantity.parse_quantity(R4B_Quantity(value=1, unit="m"))
    assert isinstance(value_r4b, Quantity)
    value_r5 = Quantity.parse_quantity(R5_Quantity(value=1, unit="m"))
    assert isinstance(value_r5, Quantity)
    value_int = Quantity.parse_quantity(1)
    assert isinstance(value_int, Quantity)
    value_float = Quantity.parse_quantity(1.0)
    assert isinstance(value_float, Quantity)


def test_fhirpath_type_quantity_is_compatible_with():
    assert Quantity(value=1, unit="m").is_compatible_with(Quantity(value=1, unit="m"))
    assert not Quantity(value=1, unit="m").is_compatible_with(
        Quantity(value=1, unit="s")
    )


def test_fhirpath_type_quantity_eq():
    assert Quantity(value=1, unit="m") == Quantity(value=1, unit="m")
    assert Quantity(value=1, unit="m") == Quantity(value=100, unit="cm")
    assert Quantity(value=1, unit="km") == Quantity(value=100000, unit="cm")
    assert Quantity(value=10, unit="{mutations}") == Quantity(
        value=1, unit="da{mutations}"
    )
    assert Quantity(value=10, unit="mm[Hg]") == Quantity(value=10, unit="mm[Hg]")
    assert Quantity(value=10, unit="[arb'U]") == Quantity(value=10, unit="[arb'U]")


def test_fhirpath_type_quantity_gt():
    assert Quantity(value=2, unit="m") > Quantity(value=1, unit="m")
    assert Quantity(value=2, unit="m") > Quantity(value=100, unit="cm")
    assert Quantity(value=1, unit="km") > Quantity(value=1, unit="m")


def test_fhirpath_type_quantity_lt():
    assert Quantity(value=1, unit="m") < Quantity(value=2, unit="m")
    assert Quantity(value=1, unit="m") < Quantity(value=200, unit="cm")
    assert Quantity(value=1, unit="m") < Quantity(value=1, unit="km")


def test_fhirpath_type_quantity_ge():
    assert Quantity(value=2, unit="m") >= Quantity(value=1, unit="m")
    assert Quantity(value=1, unit="km") >= Quantity(value=1, unit="m")


def test_fhirpath_type_quantity_le():
    assert Quantity(value=1, unit="m") <= Quantity(value=2, unit="m")
    assert Quantity(value=1, unit="m") <= Quantity(value=200, unit="cm")
    assert Quantity(value=1, unit="m") <= Quantity(value=1, unit="km")


def test_fhirpath_type_quantity_add():
    assert Quantity(value=2, unit="m") + Quantity(value=2, unit="m") == Quantity(
        value=4, unit="m"
    )
    assert Quantity(value=2, unit="m") + Quantity(value=2, unit="cm") == Quantity(
        value=2.02, unit="m"
    )
    assert Quantity(value=1, unit="g") + Quantity(value=1, unit="kg") == Quantity(
        value=1001, unit="g"
    )
    assert Quantity(value=1, unit="{mutations}") + Quantity(
        value=1, unit="k{mutations}"
    ) == Quantity(value=1001, unit="{mutations}")


def test_fhirpath_type_quantity_sub():
    assert Quantity(value=2, unit="m") - Quantity(value=2, unit="m") == Quantity(
        value=0, unit="m"
    )
    assert Quantity(value=2, unit="m") - Quantity(value=20, unit="cm") == Quantity(
        value=1.8, unit="m"
    )
    assert Quantity(value=1, unit="kg") - Quantity(value=500, unit="g") == Quantity(
        value=0.5, unit="kg"
    )
    assert Quantity(value=10, unit="k{mutations}") - Quantity(
        value=100, unit="da{mutations}"
    ) == Quantity(value=9, unit="k{mutations}")


def test_fhirpath_type_quantity_prod():
    assert Quantity(value=3, unit="m") * Quantity(value=2, unit="s") == Quantity(
        value=6, unit="m*s"
    )
    assert Quantity(value=3, unit="m") * Quantity(value=2, unit="m") == Quantity(
        value=6, unit="m*m"
    )
    assert Quantity(value=2, unit="{mutations}") * Quantity(
        value=10, unit="{mutations}"
    ) == Quantity(value=20, unit="{mutations}")


def test_fhirpath_type_quantity_div():
    assert Quantity(value=6, unit="m") / Quantity(value=2, unit="s") == Quantity(
        value=3, unit="m/s"
    )
    assert Quantity(value=2, unit="{mutations}") / Quantity(
        value=10, unit="k{mutations}"
    ) == Quantity(value=0.2, unit="{mutations}/k{mutations}")


def test_fhirpath_type_quantity_div_same_unit():
    assert Quantity(value=6, unit="m") / Quantity(value=2, unit="m") == Quantity(
        value=3, unit="1"
    )


def test_fhirpath_type_quantity_abs():
    assert abs(Quantity(value=-3, unit="m")) == Quantity(value=3, unit="m")


def test_fhirpath_type_date_string_init():
    value = Date(valuestring="@2015-05-01")
    assert isinstance(value, Date)
    assert value.year == 2015
    assert value.month == 5
    assert value.day == 1


def test_fhirpath_type_date_date_init():
    value = Date(value_date=date(2015, 5, 1))
    assert isinstance(value, Date)
    assert value.year == 2015
    assert value.month == 5
    assert value.day == 1


def test_fhirpath_type_date_datetime_init():
    value = Date(value_date=datetime(2015, 5, 1))
    assert isinstance(value, Date)
    assert value.year == 2015
    assert value.month == 5
    assert value.day == 1


def test_fhirpath_type_date_eq():
    assert Date("@2015-05-01") == Date("@2015-05-01")
    assert Date("@2015-05") == Date("@2015-05")
    assert Date("@2015") == Date("@2015")


def test_fhirpath_type_date_gt():
    assert Date("@2015-06-01") > Date("@2015-05-01")
    assert Date("@2015-06") > Date("@2015-05")
    assert Date("@2016") > Date("@2015")


def test_fhirpath_type_date_lt():
    assert Date("@2015-04-01") < Date("@2015-05-01")
    assert Date("@2015-04") < Date("@2015-05")
    assert Date("@2014") < Date("@2015")


def test_fhirpath_type_date_ge():
    assert Date("@2015-05-01") >= Date("@2015-05-01")


def test_fhirpath_type_date_le():
    assert Date("@2015-05-01") <= Date("@2015-05-01")


def test_fhirpath_type_date_different_precision():
    assert (Date("@2015-05") <= Date("@2015-05-01")) == []
    assert (Date("@2015") <= Date("@2015-05")) == []
    assert (Date("@2015-05") <= Date("@2015")) == []


def test_fhirpath_type_time_string_init():
    value = Time(valuestring="@T12:15:20.345+02:30")
    assert isinstance(value, Time)
    assert value.hour == 12
    assert value.minute == 15
    assert value.second == 20.345
    assert value.hour_shift == 2
    assert value.minute_shift == 30


def test_fhirpath_type_time_native_init():
    value = Time(
        value_time=time(
            12, 15, 20, 345000, tzinfo=timezone(timedelta(hours=2, minutes=30))
        )
    )
    assert isinstance(value, Time)
    assert value.hour == 12
    assert value.minute == 15
    assert value.second == 20.345
    assert value.hour_shift == 2
    assert value.minute_shift == 30


def test_fhirpath_type_time_utc_init():
    value = Time(value_time=time(12, 15, 20, 345000, tzinfo=timezone.utc))
    assert isinstance(value, Time)
    assert value.hour == 12
    assert value.minute == 15
    assert value.second == 20.345
    assert value.hour_shift == 0
    assert value.minute_shift == 0


def test_fhirpath_type_time_eq():
    assert Time("@T12:15:20.345Z") == Time("@T12:15:20.345+00:00")
    assert Time("@T12:15:20.345+02:30") == Time("@T12:15:20.345+02:30")
    assert Time("@T12:15:20.345+02:30") == Time("@T12:15:20.345+02:30")
    assert Time("@T12:15:20.345") == Time("@T12:15:20.345")
    assert Time("@T12:15:20.34") == Time("@T12:15:20.34")
    assert Time("@T12:15:20.3") == Time("@T12:15:20.3")
    assert Time("@T12:15:20.0") == Time("@T12:15:20")
    assert Time("@T12:15:20") == Time("@T12:15:20")
    assert Time("@T12:15") == Time("@T12:15")
    assert Time("@T12") == Time("@T12")


def test_fhirpath_type_time_gt():
    assert Time("@T12:15:20.545") > Time("@T12:15:20.345")
    assert Time("@T12:15:30") > Time("@T12:15:20")
    assert Time("@T12:25") > Time("@T12:15")
    assert Time("@T13") > Time("@T12")


def test_fhirpath_type_time_lt():
    assert Time("@T12:15:20.345") < Time("@T12:15:20.545")
    assert Time("@T12:15:20") < Time("@T12:15:50")
    assert Time("@T12:15") < Time("@T12:55")
    assert Time("@T12") < Time("@T13")


def test_fhirpath_type_time_ge():
    assert Time("@T12:15:20.345+02:30") >= Time("@T12:15:20.345+02:30")
    assert Time("@T12:15:20.345") >= Time("@T12:15:20.345")
    assert Time("@T12:15:20") >= Time("@T12:15:20")
    assert Time("@T12:15") >= Time("@T12:15")
    assert Time("@T12") >= Time("@T12")


def test_fhirpath_type_time_le():
    assert Time("@T12:15:20.345+02:30") <= Time("@T12:15:20.345+02:30")
    assert Time("@T12:15:20.345") <= Time("@T12:15:20.345")
    assert Time("@T12:15:20") <= Time("@T12:15:20")
    assert Time("@T12:15") <= Time("@T12:15")
    assert Time("@T12") <= Time("@T12")


def test_fhirpath_type_time_different_precision():
    assert (Time("@T12:15:20.345") >= Time("@T12:15:20.345+02:30")) == []
    assert (Time("@T12:15:20") >= Time("@T12:15:20.345")) == False
    assert (Time("@T12:15") >= Time("@T12:15:20")) == []
    assert (Time("@T12") >= Time("@T12:15")) == []


def test_fhirpath_type_datetime_string_init():
    value = DateTime("@2015-04-01T12:15:20.7+02:30")
    assert isinstance(value, DateTime)
    assert value.year == 2015
    assert value.month == 4
    assert value.day == 1
    assert value.hour == 12
    assert value.minute == 15
    assert value.second == 20.7
    assert value.hour_shift == 2
    assert value.minute_shift == 30


def test_fhirpath_type_datetime_native_init():
    value = DateTime(
        value_datetime=datetime(
            2015,
            4,
            1,
            12,
            15,
            20,
            345000,
            tzinfo=timezone(timedelta(hours=2, minutes=30)),
        )
    )
    assert isinstance(value, DateTime)
    assert value.year == 2015
    assert value.month == 4
    assert value.day == 1
    assert value.hour == 12
    assert value.minute == 15
    assert value.second == 20.345
    assert value.hour_shift == 2
    assert value.minute_shift == 30


def test_fhirpath_type_datetime_utc_init():
    value = DateTime(
        value_datetime=datetime(2015, 4, 1, 12, 15, 20, 345000, tzinfo=timezone.utc)
    )
    assert isinstance(value, DateTime)
    assert value.year == 2015
    assert value.month == 4
    assert value.day == 1
    assert value.hour == 12
    assert value.minute == 15
    assert value.second == 20.345
    assert value.hour_shift == 0
    assert value.minute_shift == 0


def test_fhirpath_type_datetime_eq():
    assert DateTime("@2015-04-01T12:15:20.345Z") == DateTime(
        "@2015-04-01T12:15:20.345+00:00"
    )
    assert DateTime("@2015-04-01T12:15:20.345+02:30") == DateTime(
        "@2015-04-01T12:15:20.345+02:30"
    )
    assert DateTime("@2015-04-01T12:15:20.345") == DateTime("@2015-04-01T12:15:20.345")
    assert DateTime("@2015-04-01T12:15:20.12") == DateTime("@2015-04-01T12:15:20.12")
    assert DateTime("@2015-04-01T12:15:20.1") == DateTime("@2015-04-01T12:15:20.1")
    assert DateTime("@2015-04-01T12:15:20.0") == DateTime("@2015-04-01T12:15:20")
    assert DateTime("@2015-04-01T12:15:20") == DateTime("@2015-04-01T12:15:20")
    assert DateTime("@2015-04-01T12:15") == DateTime("@2015-04-01T12:15")
    assert DateTime("@2015-04-01T12") == DateTime("@2015-04-01T12")
    assert DateTime("@2015-04-01T") == DateTime("@2015-04-01T")
    assert DateTime("@2015-04T") == DateTime("@2015-04T")
    assert DateTime("@2015T") == DateTime("@2015T")


def test_fhirpath_type_datetime_gt():
    assert DateTime("@2015-04-01T12:15:20.545") > DateTime("@2015-04-01T12:15:20.345")
    assert DateTime("@2015-04-01T12:15:30") > DateTime("@2015-04-01T12:15:20")
    assert DateTime("@2015-04-01T12:25") > DateTime("@2015-04-01T12:15")
    assert DateTime("@2015-04-01T13") > DateTime("@2015-04-01T12")
    assert DateTime("@2015-04-05T") > DateTime("@2015-04-01T")
    assert DateTime("@2015-05T") > DateTime("@2015-04T")
    assert DateTime("@2016T") > DateTime("@2015T")


def test_fhirpath_type_datetime_lt():
    assert DateTime("@2015-04-01T12:15:20.345") < DateTime("@2015-04-01T12:15:20.545")
    assert DateTime("@2015-04-01T12:15:20") < DateTime("@2015-04-01T12:15:50")
    assert DateTime("@2015-04-01T12:15") < DateTime("@2015-04-01T12:55")
    assert DateTime("@2015-04-01T12") < DateTime("@2015-04-01T13")
    assert DateTime("@2015-04-01T") < DateTime("@2015-04-10T")
    assert DateTime("@2015-03T") < DateTime("@2015-04T")
    assert DateTime("@2014T") < DateTime("@2015T")


def test_fhirpath_type_datetime_ge():
    assert DateTime("@2015-04-01T12:15:20.345+02:30") >= DateTime(
        "@2015-04-01T12:15:20.345+02:30"
    )
    assert DateTime("@2015-04-01T12:15:20.345") >= DateTime("@2015-04-01T12:15:20.345")
    assert DateTime("@2015-04-01T12:15:20") >= DateTime("@2015-04-01T12:15:20")
    assert DateTime("@2015-04-01T12:15") >= DateTime("@2015-04-01T12:15")
    assert DateTime("@2015-04-01T12") >= DateTime("@2015-04-01T12")
    assert DateTime("@2015-04-01T") >= DateTime("@2015-04-01T")
    assert DateTime("@2015-04T") >= DateTime("@2015-04T")
    assert DateTime("@2015T") >= DateTime("@2015T")


def test_fhirpath_type_datetime_le():
    assert DateTime("@2015-04-01T12:15:20.345+02:30") <= DateTime(
        "@2015-04-01T12:15:20.345+02:30"
    )
    assert DateTime("@2015-04-01T12:15:20.345") <= DateTime("@2015-04-01T12:15:20.345")
    assert DateTime("@2015-04-01T12:15:20") <= DateTime("@2015-04-01T12:15:20")
    assert DateTime("@2015-04-01T12:15") <= DateTime("@2015-04-01T12:15")
    assert DateTime("@2015-04-01T12") <= DateTime("@2015-04-01T12")
    assert DateTime("@2015-04-01T") <= DateTime("@2015-04-01T")
    assert DateTime("@2015-04T") <= DateTime("@2015-04T")
    assert DateTime("@2015T") <= DateTime("@2015T")


def test_fhirpath_type_datetime_different_precision():
    assert (
        DateTime("@2015-04-01T12:15:20.345")
        >= DateTime("@2015-04-01T12:15:20.345+02:30")
    ) == []
    assert (
        DateTime("@2015-04-01T12:15:20") >= DateTime("@2015-04-01T12:15:20.345")
    ) == False
    assert (DateTime("@2015-04-01T12:15") >= DateTime("@2015-04-01T12:15:20")) == []
    assert (DateTime("@2015-04-01T12") >= DateTime("@2015-04-01T12:15")) == []
