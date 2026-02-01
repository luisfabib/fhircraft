import pytest
from unittest.mock import Mock, patch
from pydantic import BaseModel
from typing import List, Optional

from fhircraft.fhir.resources.validators import (
    validate_element_constraint,
    _validate_FHIR_element_constraint,
    validate_model_constraint,
    validate_type_choice_element,
    validate_slicing_cardinalities,
    get_type_choice_value_by_base,
)


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


class TestValidateElementConstraint:
    """Test cases for the validate_element_constraint function."""

    def setup_method(self):
        """Set up test data."""
        self.patient = MockPatient(
            name="John Doe",
            address=MockAddress(city="Springfield", state="IL", postalCode="62701"),
            telecom=[
                MockTelecom(value="555-1234", system="phone", use="home"),
                MockTelecom(value="john@email.com", system="email", use="work"),
            ],
            active=True,
        )

    @patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
    def test_simple_element_path(self, mock_validate):
        """Test validation with a simple element path."""
        mock_validate.return_value = "John Doe"

        result = validate_element_constraint(
            self.patient,
            ["name"],
            "name.exists()",
            "Name must exist",
            "test-1",
            "error",
        )

        assert result == self.patient
        mock_validate.assert_called_once()
        # Check that the correct value was passed
        args, kwargs = mock_validate.call_args
        assert args[0] == "John Doe"  # The value
        assert args[1] == self.patient  # The instance
        assert kwargs["element"] == "name"

    @patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
    def test_nested_element_path(self, mock_validate):
        """Test validation with a nested element path."""
        mock_validate.return_value = "Springfield"

        result = validate_element_constraint(
            self.patient,
            ["address.city"],
            "address.city.exists()",
            "City must exist",
            "test-2",
            "error",
        )

        assert result == self.patient
        mock_validate.assert_called_once()
        # Check that the correct value was passed
        args, kwargs = mock_validate.call_args
        assert args[0] == "Springfield"  # The value
        assert args[1] == self.patient  # The instance
        assert kwargs["element"] == "address.city"

    @patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
    def test_list_element_path(self, mock_validate):
        """Test validation with a list element path."""
        mock_validate.side_effect = lambda v, *args, **kwargs: v

        result = validate_element_constraint(
            self.patient,
            ["telecom"],
            "telecom.exists()",
            "Telecom must exist",
            "test-3",
            "error",
        )

        assert result == self.patient
        mock_validate.assert_called_once()
        # Check that the correct value was passed (the list)
        args, kwargs = mock_validate.call_args
        assert args[0] == self.patient.telecom
        assert args[1] == self.patient
        assert kwargs["element"] == "telecom"

    @patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
    def test_nested_list_element_path(self, mock_validate):
        """Test validation with a nested element inside a list."""
        mock_validate.side_effect = lambda v, *args, **kwargs: v

        result = validate_element_constraint(
            self.patient,
            ["telecom.value"],
            "telecom.value.exists()",
            "Telecom value must exist",
            "test-4",
            "error",
        )

        assert result == self.patient
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
    def test_multiple_element_paths(self, mock_validate):
        """Test validation with multiple element paths."""
        mock_validate.side_effect = lambda v, *args, **kwargs: v

        result = validate_element_constraint(
            self.patient,
            ["name", "address.city", "active"],
            "exists()",
            "Elements must exist",
            "test-5",
            "error",
        )

        assert result == self.patient
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
    def test_missing_element_path(self, mock_validate):
        """Test validation with a missing element path."""
        mock_validate.side_effect = lambda v, *args, **kwargs: v

        result = validate_element_constraint(
            self.patient,
            ["nonexistent"],
            "nonexistent.exists()",
            "Nonexistent must exist",
            "test-6",
            "error",
        )

        assert result == self.patient
        # Should still be called once with None value
        mock_validate.assert_called_once()
        args, kwargs = mock_validate.call_args
        assert args[0] is None
        assert kwargs["element"] == "nonexistent"

    @patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
    def test_missing_nested_element_path(self, mock_validate):
        """Test validation with a missing nested element path."""
        mock_validate.side_effect = lambda v, *args, **kwargs: v

        result = validate_element_constraint(
            self.patient,
            ["address.nonexistent"],
            "address.nonexistent.exists()",
            "Nonexistent nested must exist",
            "test-7",
            "error",
        )

        assert result == self.patient
        # Should be called once with None value
        mock_validate.assert_called_once()
        args, kwargs = mock_validate.call_args
        assert args[0] is None
        assert kwargs["element"] == "address.nonexistent"

    def test_empty_patient_with_nested_paths(self):
        """Test with empty patient object and nested paths."""
        empty_patient = MockPatient()

        with patch(
            "fhircraft.fhir.resources.validators._validate_FHIR_element_constraint"
        ) as mock_validate:
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


class TestGetPathValueHelper:
    """Direct tests for the _get_path_value helper function in validate_element_constraint."""

    def test_path_value_extraction_directly(self):
        """Test the path value extraction logic directly by examining behavior."""
        patient = MockPatient(
            name="John Doe",
            address=MockAddress(city="Springfield"),
            telecom=[
                MockTelecom(value="555-1234"),
                MockTelecom(value="john@email.com"),
            ],
        )

        # Use a mock to capture what values are actually passed to _validate_FHIR_element_constraint
        captured_calls = []

        def capture_calls(
            value, instance, expression, human, key, severity, element=None
        ):
            captured_calls.append({"value": value, "element": element})
            return value

        with patch(
            "fhircraft.fhir.resources.validators._validate_FHIR_element_constraint",
            side_effect=capture_calls,
        ):
            validate_element_constraint(
                patient, ["telecom.value"], "exists()", "Must exist", "test", "error"
            )

        # Verify the captured calls
        assert len(captured_calls) == 2

        # Check values and paths
        values = [call["value"] for call in captured_calls]
        elements = [call["element"] for call in captured_calls]

        assert "555-1234" in values
        assert "john@email.com" in values
        assert "telecom[0].value" in elements
        assert "telecom[1].value" in elements


class TestValidateModelConstraint:
    """Test cases for the validate_model_constraint function."""

    @patch("fhircraft.fhir.resources.validators._validate_FHIR_element_constraint")
    def test_validate_model_constraint(self, mock_validate):
        """Test model constraint validation."""
        patient = MockPatient(name="John")
        mock_validate.return_value = patient

        result = validate_model_constraint(
            patient, "name.exists()", "Name must exist", "test-constraint", "error"
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


class TestValidateTypeChoiceElement:
    """Test cases for the validate_type_choice_element function."""

    class MockChoiceElement(BaseModel):
        valuestr: Optional[str] = None
        valueint: Optional[int] = None
        valuebool: Optional[bool] = None

    def test_valid_single_choice(self):
        """Test with only one choice field set."""
        element = self.MockChoiceElement(valuestr="test")

        result = validate_type_choice_element(
            element, [str, int, bool], "value", required=False
        )

        assert result == element

    def test_valid_no_choice_optional(self):
        """Test with no choice fields set and optional."""
        element = self.MockChoiceElement()

        result = validate_type_choice_element(
            element, [str, int, bool], "value", required=False
        )

        assert result == element

    def test_invalid_multiple_choices(self):
        """Test with multiple choice fields set."""
        element = self.MockChoiceElement(valuestr="test", valueint=42)

        with pytest.raises(AssertionError, match="can only have one value set"):
            validate_type_choice_element(
                element, [str, int, bool], "value", required=False
            )

    def test_invalid_required_no_choice(self):
        """Test with no choice fields set but required."""
        element = self.MockChoiceElement()

        with pytest.raises(AssertionError, match="must have one value set"):
            validate_type_choice_element(
                element, [str, int, bool], "value", required=True
            )

    def test_non_allowed_types(self):
        """Test with non-allowed types."""
        element = self.MockChoiceElement(valuebool=True)

        with pytest.raises(AssertionError, match="cannot use non-allowed type"):
            validate_type_choice_element(
                element,
                [str, int],  # Boolean not in allowed types
                "value",
                required=False,
                non_allowed_types=[bool],
            )


class TestGetTypeChoiceValueByBase:
    """Test cases for the get_type_choice_value_by_base function."""

    class MockChoiceElement(BaseModel):
        valueString: Optional[str] = None
        valueInteger: Optional[int] = None
        someOtherField: Optional[str] = None

    def test_get_existing_value(self):
        """Test getting an existing value."""
        element = self.MockChoiceElement(valueString="test", someOtherField="other")

        result = get_type_choice_value_by_base(element, "value")
        assert result == "test"

    def test_get_none_when_no_match(self):
        """Test getting None when no field matches."""
        element = self.MockChoiceElement(someOtherField="other")

        result = get_type_choice_value_by_base(element, "value")
        assert result is None

    def test_get_none_when_field_none(self):
        """Test getting None when matching field is None."""
        element = self.MockChoiceElement(valueString=None, someOtherField="other")

        result = get_type_choice_value_by_base(element, "value")
        assert result is None

    def test_first_non_none_value(self):
        """Test that it returns the first non-None value."""
        element = self.MockChoiceElement(valueString="test", valueInteger=42)

        result = get_type_choice_value_by_base(element, "value")
        # Should return one of the values (implementation dependent on field order)
        assert result in ["test", 42]
