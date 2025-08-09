"""
Test cases for the enhanced FHIRPathMixin class.

This test suite thoroughly tests all methods of the FHIRPathMixin,
including value retrieval, existence checking, counting, updates,
and convenience methods.
"""

import unittest
from dataclasses import dataclass
from typing import List, Optional
from unittest.mock import Mock, patch

from fhircraft.fhir.path.exceptions import FHIRPathError, FHIRPathRuntimeError
from fhircraft.fhir.path.mixin import FHIRPathMixin


@dataclass
class MockHumanName:
    use: Optional[str] = None
    family: Optional[str] = None
    given: Optional[List[str]] = None
    prefix: Optional[List[str]] = None


@dataclass
class MockTelecom:
    system: Optional[str] = None
    value: Optional[str] = None
    use: Optional[str] = None


@dataclass
class MockAddress:
    use: Optional[str] = None
    line: Optional[List[str]] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None


@dataclass
class MockPatient(FHIRPathMixin):
    """Mock FHIR Patient resource for testing."""

    resourceType: str = "Patient"
    id: Optional[str] = None
    active: Optional[bool] = None
    name: Optional[List[MockHumanName]] = None
    gender: Optional[str] = None
    birthDate: Optional[str] = None
    telecom: Optional[List[MockTelecom]] = None
    address: Optional[List[MockAddress]] = None


class TestFHIRPathMixin(unittest.TestCase):
    """Test cases for FHIRPathMixin."""

    def setUp(self):
        """Set up test fixtures with sample patient data."""
        self.patient = MockPatient(
            id="test-patient-123",
            active=True,
            name=[
                MockHumanName(
                    use="official",
                    family="Johnson",
                    given=["Alice", "Marie"],
                    prefix=["Dr."],
                ),
                MockHumanName(
                    use="maiden",
                    family="Smith",
                    given=["Alice"],
                ),
            ],
            gender="female",
            birthDate="1985-07-15",
            telecom=[
                MockTelecom(system="phone", value="+1-555-123-4567", use="home"),
                MockTelecom(system="phone", value="+1-555-987-6543", use="work"),
                MockTelecom(system="email", value="alice@example.com", use="work"),
            ],
            address=[
                MockAddress(
                    use="home",
                    line=["123 Main Street", "Apt 4B"],
                    city="Springfield",
                    state="IL",
                    postalCode="62701",
                    country="US",
                )
            ],
        )

        self.empty_patient = MockPatient(id="empty-patient")

    def test_fhirpath_property(self):
        """Test that the fhirpath property returns a parser instance."""
        parser = self.patient.fhirpath
        self.assertIsNotNone(parser)
        # Verify it has a parse method
        self.assertTrue(hasattr(parser, "parse"))

    # Test value retrieval methods
    def test_fhirpath_values(self):
        """Test fhirpath_values() method."""
        # Test with multiple values
        family_names = self.patient.fhirpath_values("Patient.name.family")
        self.assertIsInstance(family_names, list)
        self.assertEqual(len(family_names), 2)
        self.assertIn("Johnson", family_names)
        self.assertIn("Smith", family_names)

        # Test with single value
        gender_values = self.patient.fhirpath_values("Patient.gender")
        self.assertIsInstance(gender_values, list)
        self.assertEqual(len(gender_values), 1)
        self.assertEqual(gender_values[0], "female")

        # Test with no values
        empty_values = self.patient.fhirpath_values("Patient.nonexistent")
        self.assertIsInstance(empty_values, list)
        self.assertEqual(len(empty_values), 0)

    def test_fhirpath_single(self):
        """Test fhirpath_single() method."""
        # Test with single value
        gender = self.patient.fhirpath_single("Patient.gender")
        self.assertEqual(gender, "female")

        # Test with default value for missing field
        missing = self.patient.fhirpath_single(
            "Patient.nonexistent", default="default_value"
        )
        self.assertEqual(missing, "default_value")

        # Test with no default for missing field
        missing_no_default = self.patient.fhirpath_single("Patient.nonexistent")
        self.assertIsNone(missing_no_default)

        # Test error when multiple values exist
        with self.assertRaises(FHIRPathRuntimeError):
            self.patient.fhirpath_single("Patient.name.family")

    def test_fhirpath_first(self):
        """Test fhirpath_first() method."""
        # Test with multiple values
        first_family = self.patient.fhirpath_first("Patient.name.family")
        self.assertEqual(first_family, "Johnson")

        # Test with single value
        gender = self.patient.fhirpath_first("Patient.gender")
        self.assertEqual(gender, "female")

        # Test with no values and default
        missing = self.patient.fhirpath_first(
            "Patient.nonexistent", default="default_value"
        )
        self.assertEqual(missing, "default_value")

        # Test with no values and no default
        missing_no_default = self.patient.fhirpath_first("Patient.nonexistent")
        self.assertIsNone(missing_no_default)

    def test_fhirpath_last(self):
        """Test fhirpath_last() method."""
        # Test with multiple values
        last_family = self.patient.fhirpath_last("Patient.name.family")
        self.assertEqual(last_family, "Smith")

        # Test with single value
        gender = self.patient.fhirpath_last("Patient.gender")
        self.assertEqual(gender, "female")

        # Test with no values and default
        missing = self.patient.fhirpath_last(
            "Patient.nonexistent", default="default_value"
        )
        self.assertEqual(missing, "default_value")

        # Test with no values and no default
        missing_no_default = self.patient.fhirpath_last("Patient.nonexistent")
        self.assertIsNone(missing_no_default)

    # Test existence and counting methods
    def test_fhirpath_exists(self):
        """Test fhirpath_exists() method."""
        # Test existing field
        self.assertTrue(self.patient.fhirpath_exists("Patient.gender"))
        self.assertTrue(self.patient.fhirpath_exists("Patient.name.family"))

        # Test non-existing field
        self.assertFalse(self.patient.fhirpath_exists("Patient.nonexistent"))
        self.assertFalse(self.empty_patient.fhirpath_exists("Patient.name"))

    def test_fhirpath_is_empty(self):
        """Test fhirpath_is_empty() method."""
        # Test existing field
        self.assertFalse(self.patient.fhirpath_is_empty("Patient.gender"))
        self.assertFalse(self.patient.fhirpath_is_empty("Patient.name.family"))

        # Test non-existing field
        self.assertTrue(self.patient.fhirpath_is_empty("Patient.nonexistent"))
        self.assertTrue(self.empty_patient.fhirpath_is_empty("Patient.name"))

    def test_fhirpath_count(self):
        """Test fhirpath_count() method."""
        # Test multiple values
        family_count = self.patient.fhirpath_count("Patient.name.family")
        self.assertEqual(family_count, 2)

        # Test single value
        gender_count = self.patient.fhirpath_count("Patient.gender")
        self.assertEqual(gender_count, 1)

        # Test no values
        empty_count = self.patient.fhirpath_count("Patient.nonexistent")
        self.assertEqual(empty_count, 0)

        # Test complex expression
        phone_count = self.patient.fhirpath_count(
            "Patient.telecom.where(system='phone')"
        )
        self.assertEqual(phone_count, 2)

    # Test update methods
    def test_fhirpath_update_single(self):
        """Test fhirpath_update_single() method."""
        # Test updating single value
        original_gender = self.patient.fhirpath_single("Patient.gender")
        self.assertEqual(original_gender, "female")

        self.patient.fhirpath_update_single("Patient.gender", "other")
        updated_gender = self.patient.fhirpath_single("Patient.gender")
        self.assertEqual(updated_gender, "other")

        # Test error when multiple values exist
        with self.assertRaises(FHIRPathError):
            self.patient.fhirpath_update_single("Patient.name.family", "NewName")

    def test_fhirpath_update_values(self):
        """Test fhirpath_update_values() method."""
        # Test updating multiple values
        original_families = self.patient.fhirpath_values("Patient.name.family")
        self.assertEqual(len(original_families), 2)

        self.patient.fhirpath_update_values("Patient.name.family", "UpdatedFamily")
        updated_families = self.patient.fhirpath_values("Patient.name.family")

        self.assertEqual(len(updated_families), 2)
        self.assertTrue(all(name == "UpdatedFamily" for name in updated_families))

        # Test updating single value
        self.patient.fhirpath_update_values("Patient.gender", "male")
        updated_gender = self.patient.fhirpath_single("Patient.gender")
        self.assertEqual(updated_gender, "male")

    # Test convenience methods (these would be available if added to the mixin)
    def test_convenience_method_concepts(self):
        """Test concepts that could be implemented as convenience methods."""
        # Test getting first value with default (using existing methods)
        gender = self.patient.fhirpath_first("Patient.gender", default="unknown")
        self.assertEqual(gender, "female")

        missing = self.patient.fhirpath_first(
            "Patient.nonexistent", default="default_value"
        )
        self.assertEqual(missing, "default_value")

        # Test checking for specific values (using existing methods)
        family_names = self.patient.fhirpath_values("Patient.name.family")
        self.assertIn("Johnson", family_names)
        self.assertIn("Smith", family_names)
        self.assertNotIn("Doe", family_names)

        # Test safe update pattern (using existing methods with try/catch)
        def safe_update_single(patient, expression, value):
            try:
                patient.fhirpath_update_single(expression, value)
                return True
            except (FHIRPathError, RuntimeError):
                return False

        # Test successful single update
        success = safe_update_single(self.patient, "Patient.gender", "other")
        self.assertTrue(success)
        self.assertEqual(self.patient.fhirpath_single("Patient.gender"), "other")

        # Test failed single update (multiple values)
        success = safe_update_single(self.patient, "Patient.name.family", "NewName")
        self.assertFalse(success)

    def test_batch_evaluation_concept(self):
        """Test batch evaluation concept using existing methods."""
        expressions = [
            "Patient.id",
            "Patient.name.family",
            "Patient.gender",
            "Patient.nonexistent",
        ]

        results = {}
        for expr in expressions:
            try:
                values = self.patient.fhirpath_values(expr)
                results[expr] = {
                    "success": True,
                    "count": len(values),
                    "values": values,
                    "exists": len(values) > 0,
                }
            except Exception as e:
                results[expr] = {
                    "success": False,
                    "error": str(e),
                    "error_type": type(e).__name__,
                }

        # Check results
        self.assertTrue(results["Patient.id"]["success"])
        self.assertEqual(results["Patient.id"]["count"], 1)

        self.assertTrue(results["Patient.name.family"]["success"])
        self.assertEqual(results["Patient.name.family"]["count"], 2)

        self.assertTrue(results["Patient.nonexistent"]["success"])
        self.assertEqual(results["Patient.nonexistent"]["count"], 0)
        self.assertFalse(results["Patient.nonexistent"]["exists"])

    # Test complex FHIRPath expressions
    def test_complex_fhirpath_expressions(self):
        """Test complex FHIRPath expressions with filtering."""
        # Test filtering by system
        phone_values = self.patient.fhirpath_values(
            "Patient.telecom.where(system='phone').value"
        )
        self.assertEqual(len(phone_values), 2)
        self.assertIn("+1-555-123-4567", phone_values)
        self.assertIn("+1-555-987-6543", phone_values)

        # Test filtering by use
        home_phone = self.patient.fhirpath_first(
            "Patient.telecom.where(system='phone' and use='home').value"
        )
        self.assertEqual(home_phone, "+1-555-123-4567")

        # Test nested navigation
        official_given = self.patient.fhirpath_values(
            "Patient.name.where(use='official').given"
        )
        self.assertEqual(len(official_given), 2)
        self.assertIn("Alice", official_given)
        self.assertIn("Marie", official_given)

    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        # Test with empty patient
        empty_values = self.empty_patient.fhirpath_values("Patient.name.family")
        self.assertEqual(len(empty_values), 0)

        empty_exists = self.empty_patient.fhirpath_exists("Patient.name")
        self.assertFalse(empty_exists)

        empty_count = self.empty_patient.fhirpath_count("Patient.name")
        self.assertEqual(empty_count, 0)

        # Test with None values in data
        patient_with_none = MockPatient(id="test", name=None)
        none_values = patient_with_none.fhirpath_values("Patient.name.family")
        self.assertEqual(len(none_values), 0)

    def test_method_consistency(self):
        """Test that different methods return consistent results."""
        expression = "Patient.name.family"

        # Values from different methods should be consistent
        all_values = self.patient.fhirpath_values(expression)
        first_value = self.patient.fhirpath_first(expression)
        last_value = self.patient.fhirpath_last(expression)
        count = self.patient.fhirpath_count(expression)
        exists = self.patient.fhirpath_exists(expression)

        self.assertEqual(len(all_values), count)
        self.assertEqual(first_value, all_values[0] if all_values else None)
        self.assertEqual(last_value, all_values[-1] if all_values else None)
        self.assertEqual(exists, count > 0)

    @patch("fhircraft.fhir.path.mixin.import_fhirpath_engine")
    def test_fhirpath_engine_import(self, mock_import):
        """Test that the FHIRPath engine is properly imported."""
        mock_engine = Mock()
        mock_import.return_value = mock_engine

        # Create new patient to trigger import
        patient = MockPatient()
        engine = patient.fhirpath

        mock_import.assert_called_once()
        self.assertEqual(engine, mock_engine)

    def test_real_world_scenarios(self):
        """Test real-world usage scenarios."""

        # Scenario 1: Get patient display name
        def get_display_name(patient):
            first_name = patient.fhirpath_first("Patient.name.given")
            last_name = patient.fhirpath_first("Patient.name.family")
            if first_name and last_name:
                return f"{first_name} {last_name}"
            return patient.fhirpath_first("Patient.id", default="Unknown Patient")

        display_name = get_display_name(self.patient)
        self.assertEqual(display_name, "Alice Johnson")

        # Scenario 2: Validate required fields
        def validate_patient(patient):
            issues = []
            if patient.fhirpath_is_empty("Patient.id"):
                issues.append("Missing ID")
            if patient.fhirpath_is_empty("Patient.name"):
                issues.append("Missing name")
            return issues

        issues = validate_patient(self.patient)
        self.assertEqual(len(issues), 0)

        issues = validate_patient(self.empty_patient)
        self.assertEqual(len(issues), 1)  # Should have missing name

        # Scenario 3: Safe contact information update
        def update_primary_phone(patient, new_phone):
            phone_expr = "Patient.telecom.where(system='phone' and use='home').value"
            if patient.fhirpath_exists(phone_expr):
                try:
                    patient.fhirpath_update_single(phone_expr, new_phone)
                    return True
                except (FHIRPathError, RuntimeError):
                    return False
            return False

        success = update_primary_phone(self.patient, "+1-555-999-8888")
        self.assertTrue(success)

        updated_phone = self.patient.fhirpath_first(
            "Patient.telecom.where(system='phone' and use='home').value"
        )
        self.assertEqual(updated_phone, "+1-555-999-8888")
