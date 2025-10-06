from fhircraft.fhir.path.engine.literals import *


def test_fhirpath_type_quantity_init():
    value = Quantity(value=1, unit="m")
    assert isinstance(value, Quantity)


def test_fhirpath_type_quantity_eq():
    assert Quantity(value=1, unit="m") == Quantity(value=1, unit="m")


def test_fhirpath_type_quantity_gt():
    assert Quantity(value=2, unit="m") > Quantity(value=1, unit="m")


def test_fhirpath_type_quantity_lt():
    assert Quantity(value=1, unit="m") < Quantity(value=2, unit="m")


def test_fhirpath_type_quantity_ge():
    assert Quantity(value=2, unit="m") >= Quantity(value=1, unit="m")


def test_fhirpath_type_quantity_le():
    assert Quantity(value=1, unit="m") <= Quantity(value=2, unit="m")


def test_fhirpath_type_quantity_add():
    assert Quantity(value=2, unit="m") + Quantity(value=2, unit="m") == Quantity(
        value=4, unit="m"
    )


def test_fhirpath_type_quantity_sub():
    assert Quantity(value=2, unit="m") - Quantity(value=2, unit="m") == Quantity(
        value=0, unit="m"
    )


def test_fhirpath_type_quantity_prod():
    assert Quantity(value=3, unit="m") * Quantity(value=2, unit="s") == Quantity(
        value=6, unit="m*s"
    )


def test_fhirpath_type_quantity_div():
    assert Quantity(value=6, unit="m") / Quantity(value=2, unit="s") == Quantity(
        value=3, unit="m/s"
    )


def test_fhirpath_type_quantity_div_same_unit():
    assert Quantity(value=6, unit="m") / Quantity(value=2, unit="m") == Quantity(
        value=3, unit="1"
    )


def test_fhirpath_type_quantity_abs():
    assert abs(Quantity(value=-3, unit="m")) == Quantity(value=3, unit="m")


def test_fhirpath_type_quantity_different_units():
    assert (Quantity(value=1, unit="cm") <= Quantity(value=2, unit="m")) == []


def test_fhirpath_type_date_init():
    value = Date("@2015-05-01")
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


def test_fhirpath_type_time_init():
    value = Time("@T12:15:20.345+02:30")
    assert isinstance(value, Time)
    assert value.hour == 12
    assert value.minute == 15
    assert value.second == 20
    assert value.millisecond == 345
    assert value.hour_shift == 2
    assert value.minute_shift == 30


def test_fhirpath_type_time_eq():
    assert Time("@T12:15:20.345+02:30") == Time("@T12:15:20.345+02:30")
    assert Time("@T12:15:20.345") == Time("@T12:15:20.345")
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
    assert (Time("@T12:15:20") >= Time("@T12:15:20.345")) == []
    assert (Time("@T12:15") >= Time("@T12:15:20")) == []
    assert (Time("@T12") >= Time("@T12:15")) == []


def test_fhirpath_type_datetime_init():
    value = DateTime("@2015-04-01T12:15:20.345+02:30")
    assert isinstance(value, DateTime)
    assert value.year == 2015
    assert value.month == 4
    assert value.day == 1
    assert value.hour == 12
    assert value.minute == 15
    assert value.second == 20
    assert value.millisecond == 345
    assert value.hour_shift == 2
    assert value.minute_shift == 30


def test_fhirpath_type_datetime_eq():
    assert DateTime("@2015-04-01T12:15:20.345+02:30") == DateTime(
        "@2015-04-01T12:15:20.345+02:30"
    )
    assert DateTime("@2015-04-01T12:15:20.345") == DateTime("@2015-04-01T12:15:20.345")
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
    ) == []
    assert (DateTime("@2015-04-01T12:15") >= DateTime("@2015-04-01T12:15:20")) == []
    assert (DateTime("@2015-04-01T12") >= DateTime("@2015-04-01T12:15")) == []
