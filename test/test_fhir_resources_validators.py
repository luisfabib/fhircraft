import warnings
import pytest
from unittest.mock import Mock, patch
from pydantic import BaseModel
from pydantic_core import PydanticCustomError
from typing import List, Optional

from fhircraft.config import override_config
from fhircraft.fhir.resources.datatypes.R4.primitive import (
    boolean,
    integer,
    string,
    String,
    Integer,
    Boolean,
)
from fhircraft.fhir.resources.validators import (
    _validate_FHIR_element_constraint,
    validate_element_constraint,
    validate_model_constraint,
    validate_FHIR_element_pattern,
    validate_FHIR_model_pattern,
    validate_FHIR_element_fixed_value,
    validate_FHIR_model_fixed_value,
    validate_type_choice_element,
    validate_slicing_cardinalities,
    get_type_choice_value_by_base,
)

# ===========================================================
# Fixtures & Helpers
# ===========================================================


class MockAddress(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None


class MockTelecom(BaseModel):
    value: Optional[str] = None
    system: Optional[str] = None
    use: Optional[str] = None


class MockPatient(BaseModel):
    name: Optional[str] = None
    address: Optional[MockAddress] = None
    telecom: Optional[List[MockTelecom]] = None
    active: Optional[bool] = None


class MockTypeChoiceModel(BaseModel):
    valueString: Optional[string] = None
    valueInteger: Optional[integer] = None
    valueBoolean: Optional[boolean] = None


@pytest.fixture
def mock_patient():
    return MockPatient(
        name="John Doe",
        address=MockAddress(city="Springfield", state="IL", postalCode="62701"),
        telecom=[
            MockTelecom(value="555-1234", system="phone", use="home"),
            MockTelecom(value="john@email.com", system="email", use="work"),
        ],
        active=True,
    )


# ===========================================================
# validate_element_constraint()
# ===========================================================


@patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
def test_validate_element_constraint__simple_element_path(mock_validate, mock_patient):
    mock_validate.return_value = "John Doe"

    result = validate_element_constraint(
        mock_patient,
        elements=["name"],
        expression="name.exists()",
        human="Name must exist",
        key="test-1",
        severity="error",
    )

    assert result == mock_patient
    mock_validate.assert_called_once()
    # Check that the correct value was passed
    args, kwargs = mock_validate.call_args
    assert args[0] == "John Doe"  # The value
    assert args[1] == mock_patient  # The instance
    assert kwargs["element"] == "name"


@patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
def test_validate_element_constraint__nested_element_path(mock_validate, mock_patient):
    mock_validate.return_value = "Springfield"

    result = validate_element_constraint(
        mock_patient,
        elements=["address.city"],
        expression="address.city.exists()",
        human="City must exist",
        key="test-2",
        severity="error",
    )

    assert result == mock_patient
    mock_validate.assert_called_once()
    # Check that the correct value was passed
    args, kwargs = mock_validate.call_args
    assert args[0] == "Springfield"  # The value
    assert args[1] == mock_patient  # The instance
    assert kwargs["element"] == "address.city"


@patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
def test_validate_element_constraint__list_element_path(mock_validate, mock_patient):
    mock_validate.side_effect = lambda v, *args, **kwargs: v

    result = validate_element_constraint(
        mock_patient,
        elements=["telecom"],
        expression="telecom.exists()",
        human="Telecom must exist",
        key="test-3",
        severity="error",
    )

    assert result == mock_patient
    mock_validate.assert_called_once()
    # Check that the correct value was passed (the list)
    args, kwargs = mock_validate.call_args
    assert args[0] == mock_patient.telecom
    assert args[1] == mock_patient
    assert kwargs["element"] == "telecom"


@patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
def test_validate_element_constraint__nested_element_inside_list(
    mock_validate, mock_patient
):
    mock_validate.side_effect = lambda v, *args, **kwargs: v

    result = validate_element_constraint(
        mock_patient,
        elements=["telecom.value"],
        expression="telecom.value.exists()",
        human="Telecom value must exist",
        key="test-4",
        severity="error",
    )

    assert result == mock_patient
    # Should be called twice (once for each telecom item)
    assert mock_validate.call_count == 2

    # Check the calls were made with correct values
    calls = mock_validate.call_args_list

    # First call should be for "555-1234"
    assert calls[0][0][0] == "555-1234"
    assert calls[0][1]["element"] == "telecom[0].value"

    # Second call should be for "john@email.com"
    assert calls[1][0][0] == "john@email.com"
    assert calls[1][1]["element"] == "telecom[1].value"


@patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
def test_validate_element_constraint__multiple_element_paths(
    mock_validate, mock_patient
):
    mock_validate.side_effect = lambda v, *args, **kwargs: v

    result = validate_element_constraint(
        mock_patient,
        elements=["name", "address.city", "active"],
        expression="exists()",
        human="Elements must exist",
        key="test-5",
        severity="error",
    )

    assert result == mock_patient
    # Should be called 3 times
    assert mock_validate.call_count == 3

    # Verify all calls were made with correct values
    calls = mock_validate.call_args_list
    values = [call[0][0] for call in calls]
    elements = [call[1]["element"] for call in calls]

    assert "John Doe" in values
    assert "Springfield" in values
    assert True in values
    assert "name" in elements
    assert "address.city" in elements
    assert "active" in elements


@patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
def test_validate_element_constraint__missing_element_path(mock_validate, mock_patient):
    mock_validate.side_effect = lambda v, *args, **kwargs: v

    result = validate_element_constraint(
        mock_patient,
        ["nonexistent"],
        "nonexistent.exists()",
        "Nonexistent must exist",
        "test-6",
        "error",
    )

    assert result == mock_patient
    # Should still be called once with None value
    mock_validate.assert_called_once()
    args, kwargs = mock_validate.call_args
    assert args[0] is None
    assert kwargs["element"] == "nonexistent"


@patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
def test_validate_element_constraint__missing_nested_element_path(
    mock_validate, mock_patient
):
    mock_validate.side_effect = lambda v, *args, **kwargs: v

    result = validate_element_constraint(
        mock_patient,
        ["address.nonexistent"],
        "address.nonexistent.exists()",
        "Nonexistent nested must exist",
        "test-7",
        "error",
    )

    assert result == mock_patient
    # Should be called once with None value
    mock_validate.assert_called_once()
    args, kwargs = mock_validate.call_args
    assert args[0] is None

    assert kwargs["element"] == "address.nonexistent"


@patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
def test_validate_element_constraint__empty_object(mock_validate):
    empty_patient = MockPatient()

    mock_validate.side_effect = lambda v, *args, **kwargs: v

    result = validate_element_constraint(
        empty_patient,
        ["address.city", "telecom.value"],
        "exists()",
        "Must exist",
        "test-8",
        "error",
    )

    assert result == empty_patient
    # Should be called twice with None values
    assert mock_validate.call_count == 2

    calls = mock_validate.call_args_list
    assert calls[0][0][0] is None  # address.city -> None
    assert calls[1][0][0] is None  # telecom.value -> None


# ===========================================================
# validate_model_constraint()
# ===========================================================


@patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
def test_validate_model_constraint__basic(mock_validate):
    patient = MockPatient(name="John")
    mock_validate.return_value = patient

    result = validate_model_constraint(
        patient,
        expression="name.exists()",
        human="Name must exist",
        key="test-constraint",
        severity="error",
    )

    assert result == patient
    mock_validate.assert_called_once_with(
        patient,
        patient,
        "name.exists()",
        "Name must exist",
        "test-constraint",
        "error",
    )


# ===========================================================
# _validate_FHIR_element_constraint()
# ===========================================================


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__skip_mode_returns_value(mock_fhirpath):
    with override_config(validation_mode="skip"):
        result = _validate_FHIR_element_constraint(
            "value", Mock(), "expr", "Human", "key-1", "error"
        )
    assert result == "value"
    mock_fhirpath.assert_not_called()


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__disabled_constraint_returns_value(
    mock_fhirpath,
):
    with override_config(disabled_fhir_constraints=frozenset({"key-1"})):
        result = _validate_FHIR_element_constraint(
            "value", Mock(), "expr", "Human", "key-1", "error"
        )
    assert result == "value"
    mock_fhirpath.assert_not_called()


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__disable_validation_warnings_skips_warning(
    mock_fhirpath,
):
    with override_config(disable_validation_warnings=True):
        result = _validate_FHIR_element_constraint(
            "value", Mock(), "expr", "Human", "key-1", "warning"
        )
    assert result == "value"
    mock_fhirpath.assert_not_called()


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__disable_fhir_warnings_skips_warning(
    mock_fhirpath,
):
    with override_config(disable_fhir_warnings=True):
        result = _validate_FHIR_element_constraint(
            "value", Mock(), "expr", "Human", "key-1", "warning"
        )
    assert result == "value"
    mock_fhirpath.assert_not_called()


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__disable_fhir_errors_skips_error(
    mock_fhirpath,
):
    with override_config(disable_fhir_errors=True):
        result = _validate_FHIR_element_constraint(
            "value", Mock(), "expr", "Human", "key-1", "error"
        )
    assert result == "value"
    mock_fhirpath.assert_not_called()


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__none_value_returns_none(mock_fhirpath):
    result = _validate_FHIR_element_constraint(
        None, Mock(), "expr", "Human", "key-1", "error"
    )
    assert result is None
    mock_fhirpath.assert_not_called()


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__valid_expression_returns_value(
    mock_fhirpath,
):
    mock_fhirpath.return_value.single.return_value = True

    result = _validate_FHIR_element_constraint(
        "test_value", Mock(), "some.expr", "Human", "key-1", "error"
    )

    assert result == "test_value"
    mock_fhirpath.assert_called_once_with("some.expr")


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__invalid_expression_raises_on_error(
    mock_fhirpath,
):
    mock_fhirpath.return_value.single.return_value = False

    with pytest.raises(PydanticCustomError, match=r"\[key-1\]"):
        _validate_FHIR_element_constraint(
            "test_value", Mock(), "some.expr", "Human must hold", "key-1", "error"
        )


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__invalid_expression_warns_on_warning(
    mock_fhirpath,
):
    mock_fhirpath.return_value.single.return_value = False

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = _validate_FHIR_element_constraint(
            "test_value", Mock(), "some.expr", "Human must hold", "key-1", "warning"
        )

    assert result == "test_value"
    assert len(caught) == 1
    assert "key-1" in str(caught[0].message)


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__lenient_mode_converts_error_to_warning(
    mock_fhirpath,
):
    mock_fhirpath.return_value.single.return_value = False

    with override_config(validation_mode="lenient"):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = _validate_FHIR_element_constraint(
                "test_value", Mock(), "some.expr", "Human must hold", "key-1", "error"
            )

    assert result == "test_value"
    assert len(caught) == 1


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__fhirpath_exception_emits_warning(
    mock_fhirpath,
):
    mock_fhirpath.side_effect = ValueError("bad expression")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = _validate_FHIR_element_constraint(
            "test_value", Mock(), "bad.expr", "Human", "key-1", "error"
        )

    assert result == "test_value"
    assert len(caught) == 1
    assert "ValueError" in str(caught[0].message)


@patch("fhircraft.fhir.path.parse_fhirpath")
def test__validate_FHIR_element_constraint__element_prefix_in_error_message(
    mock_fhirpath,
):
    mock_fhirpath.return_value.single.return_value = False

    with pytest.raises(PydanticCustomError) as exc_info:
        _validate_FHIR_element_constraint(
            "val",
            Mock(),
            "expr",
            "Must hold",
            "key-1",
            "error",
            element="Patient.name",
        )

    assert "Patient.name" in str(exc_info.value)


# ===========================================================
# validate_FHIR_element_pattern()
# ===========================================================


def test_validate_FHIR_element_pattern__skip_mode_returns_element():
    with override_config(validation_mode="skip"):
        result = validate_FHIR_element_pattern(None, "some_value", "other_value")
    assert result == "some_value"


def test_validate_FHIR_element_pattern__matching_scalar_returns_element():
    result = validate_FHIR_element_pattern(None, "John", "John")
    assert result == "John"


def test_validate_FHIR_element_pattern__non_matching_scalar_raises():
    with pytest.raises(PydanticCustomError, match="does not fulfill pattern"):
        validate_FHIR_element_pattern(None, "John", "Jane")


def test_validate_FHIR_element_pattern__lenient_mode_warns_instead_of_raising():
    with override_config(validation_mode="lenient"):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = validate_FHIR_element_pattern(None, "John", "Jane")
    assert result == "John"
    assert len(caught) == 1
    assert "does not fulfill pattern" in str(caught[0].message)


def test_validate_FHIR_element_pattern__list_element_uses_first_item():
    result = validate_FHIR_element_pattern(None, ["John", "Jane"], "John")
    assert result == ["John", "Jane"]


def test_validate_FHIR_element_pattern__list_pattern_uses_first_item():
    result = validate_FHIR_element_pattern(None, "John", ["John", "Jane"])
    assert result == "John"


def test_validate_FHIR_element_pattern__passes_for_matching_pattern():
    element = {"codes": ["A"]}
    pattern = {"codes": ["A"]}
    result = validate_FHIR_element_pattern(None, element, pattern)
    assert result == element


def test_validate_FHIR_element_pattern__passes_for_superset_of_pattern():
    element = {"codes": ["A"], "extra": "value"}
    pattern = {"codes": ["A"]}
    result = validate_FHIR_element_pattern(None, element, pattern)
    assert result == element


def test_validate_FHIR_element_pattern__raises_error_for_subset_of_pattern():
    element = {"codes": ["A"]}
    pattern = {"codes": ["A"], "system": "B"}
    with pytest.raises(PydanticCustomError, match="does not fulfill pattern"):
        validate_FHIR_element_pattern(None, element, pattern)


def test_validate_FHIR_element_pattern__raises_error_for_missing_pattern():
    element = {"extra": "value"}
    pattern = {"codes": ["A"]}
    with pytest.raises(PydanticCustomError, match="does not fulfill pattern"):
        validate_FHIR_element_pattern(None, element, pattern)


def test_validate_FHIR_element_pattern__raises_error_for_conflicting_scalar_pattern():
    element = {"codes": "A"}
    pattern = {"codes": "B"}
    with pytest.raises(PydanticCustomError, match="does not fulfill pattern"):
        validate_FHIR_element_pattern(None, element, pattern)


def test_validate_FHIR_element_pattern__raises_error_for_conflicting_pattern():
    element = {"codes": ["A"]}
    pattern = {"codes": ["B"]}
    with pytest.raises(PydanticCustomError, match="does not fulfill pattern"):
        validate_FHIR_element_pattern(None, element, pattern)


def test_validate_FHIR_element_pattern__raises_error_for_conflicting_nested_pattern():
    element = {"codes": [{"code": "A", "system": "C"}]}
    pattern = {"codes": [{"code": "A", "system": "B"}]}
    with pytest.raises(PydanticCustomError, match="does not fulfill pattern"):
        validate_FHIR_element_pattern(None, element, pattern)


def test_validate_FHIR_element_pattern__passes_for_nested_superset_of_pattern():
    element = {"codes": [{"code": "A", "system": "B"}, {"code": "C", "system": "D"}]}
    pattern = {"codes": [{"code": "A", "system": "B"}]}
    result = validate_FHIR_element_pattern(None, element, pattern)
    assert result == element


# ===========================================================
# validate_FHIR_model_pattern()
# ===========================================================


@patch("fhircraft.fhir.resources.validators.validate_FHIR_element_pattern")
def test_validate_FHIR_model_pattern__delegates_to_element_pattern(mock_element):
    model = {"name": "John"}
    pattern = {"name": "John"}
    mock_element.return_value = model

    result = validate_FHIR_model_pattern(model, pattern)

    mock_element.assert_called_once_with(cls=None, element=model, pattern=pattern)
    assert result == model


# ===========================================================
# validate_FHIR_element_fixed_value()
# ===========================================================


def test_validate_FHIR_element_fixed_value__skip_mode_returns_element():
    with override_config(validation_mode="skip"):
        result = validate_FHIR_element_fixed_value(None, "some_value", "other_value")
    assert result == "some_value"


def test_validate_FHIR_element_fixed_value__matching_values_returns_element():
    result = validate_FHIR_element_fixed_value(None, "exact", "exact")
    assert result == "exact"


def test_validate_FHIR_element_fixed_value__matching_int_returns_element():
    result = validate_FHIR_element_fixed_value(None, 42, 42)
    assert result == 42


def test_validate_FHIR_element_fixed_value__non_matching_values_raises():
    with pytest.raises(PydanticCustomError, match="does not fulfill constant"):
        validate_FHIR_element_fixed_value(None, "actual", "expected")


def test_validate_FHIR_element_fixed_value__lenient_mode_warns_instead_of_raising():
    with override_config(validation_mode="lenient"):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = validate_FHIR_element_fixed_value(None, "actual", "expected")
    assert result == "actual"
    assert len(caught) == 1
    assert "does not fulfill constant" in str(caught[0].message)


def test_validate_FHIR_element_fixed_value__list_element_uses_first_item():
    result = validate_FHIR_element_fixed_value(None, ["exact", "other"], "exact")
    assert result == ["exact", "other"]


def test_validate_FHIR_element_fixed_value__list_constant_uses_first_item():
    result = validate_FHIR_element_fixed_value(None, "exact", ["exact", "other"])
    assert result == "exact"


def test_validate_FHIR_element_fixed_value__non_matching_list_element_raises():
    with pytest.raises(PydanticCustomError, match="does not fulfill constant"):
        validate_FHIR_element_fixed_value(None, ["wrong", "other"], "exact")


# ===========================================================
# validate_FHIR_model_fixed_value()
# ===========================================================


@patch("fhircraft.fhir.resources.validators.validate_FHIR_element_fixed_value")
def test_validate_FHIR_model_fixed_value__delegates_to_element_fixed_value(
    mock_element,
):
    model = "exact"
    constant = "exact"
    mock_element.return_value = model

    result = validate_FHIR_model_fixed_value(model, constant)

    mock_element.assert_called_once_with(cls=None, element=model, constant=constant)
    assert result == model


# ===========================================================
# validate_type_choice_element()
# ===========================================================


def test_validate_type_choice_element__skip_mode_returns_instance():
    instance = MockTypeChoiceModel(valueString=String(value="hello"))
    with override_config(validation_mode="skip"):
        result = validate_type_choice_element(instance, ["String"], "value")
    assert result is instance


def test_validate_type_choice_element__single_value_set_is_valid():
    instance = MockTypeChoiceModel(valueString=String(value="hello"))
    result = validate_type_choice_element(
        instance, ["String", "Integer", "Boolean"], "value"
    )
    assert result is instance


def test_validate_type_choice_element__no_value_set_not_required_is_valid():
    instance = MockTypeChoiceModel()
    result = validate_type_choice_element(
        instance, ["String", "Integer", "Boolean"], "value", required=False
    )
    assert result is instance


def test_validate_type_choice_element__multiple_values_set_raises():
    instance = MockTypeChoiceModel(
        valueString=String(value="hello"), valueInteger=Integer(value=42)
    )
    with pytest.raises(PydanticCustomError, match="can only have one value set"):
        validate_type_choice_element(
            instance, ["String", "Integer", "Boolean"], "value"
        )


def test_validate_type_choice_element__required_and_no_value_raises():
    instance = MockTypeChoiceModel()
    with pytest.raises(PydanticCustomError, match="must have one value set"):
        validate_type_choice_element(
            instance, ["String", "Integer", "Boolean"], "value", required=True
        )


def test_validate_type_choice_element__required_and_value_set_is_valid():
    instance = MockTypeChoiceModel(valueInteger=Integer(value=7))
    result = validate_type_choice_element(
        instance, ["String", "Integer", "Boolean"], "value", required=True
    )
    assert result is instance


def test_validate_type_choice_element__non_allowed_type_raises():
    # valueBoolean is set but only String and Integer are allowed
    instance = MockTypeChoiceModel(valueBoolean=Boolean(value=True))
    with pytest.raises(PydanticCustomError, match="cannot use non-allowed type"):
        validate_type_choice_element(instance, ["String", "Integer"], "value")


def test_validate_type_choice_element__explicit_non_allowed_type_raises():
    instance = MockTypeChoiceModel(valueBoolean=Boolean(value=True))
    with pytest.raises(PydanticCustomError, match="cannot use non-allowed type"):
        validate_type_choice_element(
            instance,
            ["String", "Integer", "Boolean"],
            "value",
            non_allowed_types=["Boolean"],
        )


def test_validate_type_choice_element__lenient_mode_warns_on_multiple_values():
    instance = MockTypeChoiceModel(
        valueString=String(value="a"), valueInteger=Integer(value=1)
    )
    with override_config(validation_mode="lenient"):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = validate_type_choice_element(
                instance, ["String", "Integer", "Boolean"], "value"
            )
    assert result is instance
    assert any("can only have one value set" in str(w.message) for w in caught)


def test_validate_type_choice_element__lenient_mode_warns_on_non_allowed_type():
    instance = MockTypeChoiceModel(valueBoolean=True)
    with override_config(validation_mode="lenient"):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = validate_type_choice_element(
                instance, ["String", "Integer"], "value"
            )
    assert result is instance
    assert any("cannot use non-allowed type" in str(w.message) for w in caught)


# ===========================================================
# validate_slicing_cardinalities()
# ===========================================================


@patch("fhircraft.fhir.resources.validators.get_all_models_from_field")
def test_validate_slicing_cardinalities__skip_mode_returns_values(mock_get_models):
    mock_cls = Mock()
    mock_cls.model_fields = {"items": Mock()}
    values = [Mock(), Mock()]

    with override_config(validation_mode="skip"):
        result = validate_slicing_cardinalities(mock_cls, values, "items")

    assert result is values
    mock_get_models.assert_not_called()


@patch("fhircraft.fhir.resources.validators.get_all_models_from_field")
def test_validate_slicing_cardinalities__none_values_returns_none(mock_get_models):
    mock_cls = Mock()
    mock_cls.model_fields = {"items": Mock()}

    result = validate_slicing_cardinalities(mock_cls, None, "items")

    assert result is None
    mock_get_models.assert_not_called()


@patch("fhircraft.fhir.resources.validators.get_all_models_from_field")
def test_validate_slicing_cardinalities__valid_cardinalities_returns_values(
    mock_get_models,
):
    class MockSlice:
        min_cardinality = 1
        max_cardinality = 3
        __name__ = "MockSlice"

    class MockSliceInstance(MockSlice):
        pass

    mock_get_models.return_value = iter([MockSlice])
    mock_cls = Mock()
    mock_cls.model_fields = {"items": Mock()}
    values = [MockSliceInstance(), MockSliceInstance()]

    result = validate_slicing_cardinalities(mock_cls, values, "items")

    assert result is values


@patch("fhircraft.fhir.resources.validators.get_all_models_from_field")
def test_validate_slicing_cardinalities__violates_min_cardinality_raises(
    mock_get_models,
):
    class MockSlice:
        min_cardinality = 3
        max_cardinality = None
        __name__ = "MockSlice"

    class MockSliceInstance(MockSlice):
        pass

    mock_get_models.return_value = iter([MockSlice])
    mock_cls = Mock()
    mock_cls.model_fields = {"items": Mock()}
    values = [MockSliceInstance()]  # only 1, but min is 3

    with pytest.raises(PydanticCustomError, match="min. cardinality"):
        validate_slicing_cardinalities(mock_cls, values, "items")


@patch("fhircraft.fhir.resources.validators.get_all_models_from_field")
def test_validate_slicing_cardinalities__violates_max_cardinality_raises(
    mock_get_models,
):
    class MockSlice:
        min_cardinality = 1
        max_cardinality = 2
        __name__ = "MockSlice"

    class MockSliceInstance(MockSlice):
        pass

    mock_get_models.return_value = iter([MockSlice])
    mock_cls = Mock()
    mock_cls.model_fields = {"items": Mock()}
    values = [
        MockSliceInstance(),
        MockSliceInstance(),
        MockSliceInstance(),
    ]  # 3 > max 2

    with pytest.raises(PydanticCustomError, match="max. cardinality"):
        validate_slicing_cardinalities(mock_cls, values, "items")


@patch("fhircraft.fhir.resources.validators.get_all_models_from_field")
def test_validate_slicing_cardinalities__lenient_mode_warns_on_violation(
    mock_get_models,
):
    class MockSlice:
        min_cardinality = 3
        max_cardinality = None
        __name__ = "MockSlice"

    class MockSliceInstance(MockSlice):
        pass

    mock_get_models.return_value = iter([MockSlice])
    mock_cls = Mock()
    mock_cls.model_fields = {"items": Mock()}
    values = [MockSliceInstance()]

    with override_config(validation_mode="lenient"):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = validate_slicing_cardinalities(mock_cls, values, "items")

    assert result is values
    assert any("min. cardinality" in str(w.message) for w in caught)


@patch("fhircraft.fhir.resources.validators.get_all_models_from_field")
def test_validate_slicing_cardinalities__no_slice_instances_skips_check(
    mock_get_models,
):
    class MockSlice:
        min_cardinality = 5
        max_cardinality = 5
        __name__ = "MockSlice"

    mock_get_models.return_value = iter([MockSlice])
    mock_cls = Mock()
    mock_cls.model_fields = {"items": Mock()}
    values = [Mock(), Mock()]  # no MockSlice instances

    # Should not raise even though cardinality would be violated if checked
    result = validate_slicing_cardinalities(mock_cls, values, "items")
    assert result is values


# ===========================================================
# get_type_choice_value_by_base()
# ===========================================================


def test_get_type_choice_value_by_base__returns_correct_value():
    instance = MockTypeChoiceModel(valueString="hello")
    result = get_type_choice_value_by_base(instance, "value")
    assert result == "hello"


def test_get_type_choice_value_by_base__returns_none_when_no_matching_field():
    instance = MockPatient(name="John")
    result = get_type_choice_value_by_base(instance, "nonexistent")
    assert result is None


def test_get_type_choice_value_by_base__returns_none_when_all_matching_fields_are_none():
    instance = MockTypeChoiceModel()
    result = get_type_choice_value_by_base(instance, "value")
    assert result is None


def test_get_type_choice_value_by_base__returns_first_non_none_value():
    # valueBoolean is set; function should return the first non-None field starting with "value"
    instance = MockTypeChoiceModel(valueBoolean=Boolean(value=True))
    result = get_type_choice_value_by_base(instance, "value")
    assert result.value is True


def test_get_type_choice_value_by_base__integer_value():
    instance = MockTypeChoiceModel(valueInteger=Integer(value=99))
    result = get_type_choice_value_by_base(instance, "value")
    assert result.value == 99
