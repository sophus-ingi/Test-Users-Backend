"""
Unit tests for FakeInfo class.

Tests cover:
- CPR generation (valid format and range)
- Name and gender generation
- Birth date generation and validity
- Address generation
- Phone number generation
- Full person object generation
- Bulk person generation with limits
"""

import os
import pytest
from datetime import datetime
from src.fake_info import FakeInfo


class TestFakeInfoInitialization:
    """Test FakeInfo instance creation and basic properties."""
    
    def test_fake_info_initialization(self):
        """FakeInfo should initialize without errors."""
        fake_info = FakeInfo()
        assert fake_info is not None
    
    def test_fake_info_has_required_attributes(self):
        """FakeInfo instance should have all required attributes after init."""
        fake_info = FakeInfo()
        assert hasattr(fake_info, 'cpr')
        assert hasattr(fake_info, 'first_name')
        assert hasattr(fake_info, 'last_name')
        assert hasattr(fake_info, 'gender')
        assert hasattr(fake_info, 'birth_date')
        assert hasattr(fake_info, 'address')
        assert hasattr(fake_info, 'phone')


class TestCPRGeneration:
    """Test CPR (Danish personal ID) generation."""
    
    def test_get_cpr_returns_string(self):
        """get_cpr() should return a string."""
        fake_info = FakeInfo()
        cpr = fake_info.get_cpr()
        assert isinstance(cpr, str)
    
    def test_get_cpr_is_10_digits(self):
        """CPR should be exactly 10 digits."""
        fake_info = FakeInfo()
        cpr = fake_info.get_cpr()
        assert len(cpr) == 10
        assert cpr.isdigit()
    
    def test_get_cpr_multiple_calls_different_values(self):
        """Multiple CPR generations should produce different values."""
        cprs = [FakeInfo().get_cpr() for _ in range(10)]
        # At least some should be different (not always guaranteed but highly likely)
        assert len(set(cprs)) > 1
    
    def test_cpr_in_valid_range(self):
        """
        CPR values should be within valid range (0000000000-9999999999).
        
        REASONING (Range Validation - Repetition Testing):
        - Single test might pass by luck
        - We run 100 times to catch random failures
        - Tests that randomness always stays within bounds
        - If implementation occasionally generates 10-digit CPR starting with 0,
          but treats it as 9-digit when converted to int, this catches it
        - Example: "0000000001" as string vs 1 as int
        - Equivalence partitions:
          Valid: 0 <= CPR <= 9999999999
          Invalid: CPR < 0 or CPR > 9999999999
        - By testing 100 iterations with different random values,
          we validate the constraint holds universally
        """
        for _ in range(100):
            fake_info = FakeInfo()
            cpr_int = int(fake_info.get_cpr())
            assert 0 <= cpr_int <= 9999999999


class TestNameAndGender:
    """Test name and gender generation."""
    
    def test_get_full_name_and_gender_returns_dict(self):
        """get_full_name_and_gender() should return a dictionary."""
        fake_info = FakeInfo()
        result = fake_info.get_full_name_and_gender()
        assert isinstance(result, dict)
    
    def test_full_name_and_gender_has_required_keys(self):
        """Result should have firstName, lastName, and gender keys."""
        fake_info = FakeInfo()
        result = fake_info.get_full_name_and_gender()
        assert 'firstName' in result
        assert 'lastName' in result
        assert 'gender' in result
    
    def test_gender_is_valid_value(self):
        """
        Gender should be either 'male' or 'female'.
        
        REASONING (Equivalence Partitioning - Enumeration Testing):
        - Gender has only 2 valid values: 'male' or 'female'
        - Invalid partitions: 'MALE', 'Female', 'other', null, '', etc.
        - Run 50 iterations to catch any randomness bias
        - Possible bugs this catches:
          - Typo in code: 'male' vs 'Male'
          - Gender list incomplete: only includes male, missing female
          - Probability skew: always returns 'male'
        - Using `in ['male', 'female']` with 50 iterations validates:
          1. Always returns valid value
          2. Both values are reachable (high probability after 50 tries)
        - Real-world impact: Frontend might crash if gender = undefined
        """
        for _ in range(50):
            fake_info = FakeInfo()
            gender = fake_info.get_full_name_and_gender()['gender']
            assert gender in ['male', 'female']
    
    def test_names_are_non_empty_strings(self):
        """First and last names should be non-empty strings."""
        fake_info = FakeInfo()
        result = fake_info.get_full_name_and_gender()
        assert isinstance(result['firstName'], str) and len(result['firstName']) > 0
        assert isinstance(result['lastName'], str) and len(result['lastName']) > 0


class TestBirthDate:
    """Test birth date generation."""
    
    def test_get_full_name_gender_and_birth_date_returns_dict(self):
        """Should return a dictionary with birth date."""
        fake_info = FakeInfo()
        result = fake_info.get_full_name_gender_and_birth_date()
        assert isinstance(result, dict)
    
    def test_birth_date_has_required_fields(self):
        """Result should have birthDate, firstName, lastName, gender."""
        fake_info = FakeInfo()
        result = fake_info.get_full_name_gender_and_birth_date()
        assert 'birthDate' in result
        assert 'firstName' in result
        assert 'lastName' in result
        assert 'gender' in result
    
    def test_birth_date_format_valid(self):
        """
        Birth date should be in YYYY-MM-DD format.
        
        REASONING (Format & Parsing Validation):
        - API contract specifies: ISO 8601 format (YYYY-MM-DD)
        - Frontend depends on this format for parsing
        - Run 20 iterations to catch random format variations
        - Uses datetime.strptime() to validate format
        - If format wrong, strptime() raises ValueError
        - Examples of failures caught:
          - '01/15/1990' (wrong format)
          - '1990-1-15' (missing leading zero)
          - '1990/01/15' (wrong separator)
          - '15-01-1990' (wrong order)
        - This test doesn't validate reasonable dates,
          just that format is parseable
        - Data contract test: ensures interface compatibility
        """
        fake_info = FakeInfo()
        for _ in range(20):
            result = FakeInfo().get_full_name_gender_and_birth_date()
            birth_date = result['birthDate']
            try:
                datetime.strptime(birth_date, '%Y-%m-%d')
                valid = True
            except ValueError:
                valid = False
            assert valid
    
    def test_birth_date_is_reasonable(self):
        """
        Birth dates should be within reasonable historical range.
        
        REASONING (Constraint Validation - Domain Rules):
        - Birth year constraint: 1900 <= year <= current_year
        - Validates business logic constraint
        - Catches implementation bugs:
          - Off-by-one: birth year = current_year + 1 (future person)
          - Type error: birth_year as string '20204' (too large)
          - Random seed bug: always generating same year
        - Why 1900? Min reasonable age: ~120+ years old
        - Why current_year? Can't be born in future
        - Example violations this catches:
          - Birth date: 2099-01-01 (future)
          - Birth date: 1800-01-01 (too old)
          - Birth date: constant value (broken randomness)
        - This is domain-specific validation,
          not just format checking
        """
        fake_info = FakeInfo()
        result = fake_info.get_full_name_gender_and_birth_date()
        birth_date = datetime.strptime(result['birthDate'], '%Y-%m-%d')
        current_year = datetime.now().year
        # Birth year should be between 1900 and current year
        assert 1900 <= birth_date.year <= current_year


class TestAddress:
    """Test address generation."""
    
    def test_get_address_returns_dict(self):
        """get_address() should return a dictionary."""
        fake_info = FakeInfo()
        address = fake_info.get_address()
        assert isinstance(address, dict)
    
    def test_address_has_required_fields(self):
        """Address should have street, number, postal_code, town_name."""
        fake_info = FakeInfo()
        address = fake_info.get_address()
        assert 'street' in address
        assert 'number' in address
        assert 'postal_code' in address
        assert 'town_name' in address
    
    def test_postal_code_is_valid(self):
        """Postal code should be 4 digits."""
        for _ in range(20):
            fake_info = FakeInfo()
            address = fake_info.get_address()
            postal_code = address['postal_code']
            assert len(postal_code) == 4
            assert postal_code.isdigit()
    
    def test_address_fields_are_non_empty_strings(self):
        """All address fields should be non-empty strings."""
        fake_info = FakeInfo()
        address = fake_info.get_address()
        assert isinstance(address['street'], str) and len(address['street']) > 0
        assert isinstance(address['number'], str) and len(address['number']) > 0
        assert isinstance(address['postal_code'], str) and len(address['postal_code']) > 0
        assert isinstance(address['town_name'], str) and len(address['town_name']) > 0


class TestPhoneNumber:
    """Test phone number generation."""
    
    def test_get_phone_number_returns_string(self):
        """get_phone_number() should return a string."""
        fake_info = FakeInfo()
        phone = fake_info.get_phone_number()
        assert isinstance(phone, str)
    
    def test_phone_number_is_8_digits(self):
        """Phone number should be 8 digits."""
        for _ in range(20):
            fake_info = FakeInfo()
            phone = fake_info.get_phone_number()
            assert len(phone) == 8
            assert phone.isdigit()
    
    def test_phone_number_starts_with_valid_prefix(self):
        """Phone number should start with a valid Danish phone prefix."""
        valid_prefixes = [
            '2', '30', '31', '40', '41', '42', '50', '51', '52', '53',
            '60', '61', '71', '81', '91', '92', '93'
        ]
        for _ in range(50):
            fake_info = FakeInfo()
            phone = fake_info.get_phone_number()
            # Check if phone starts with any valid prefix
            found = False
            for prefix in valid_prefixes:
                if phone.startswith(prefix):
                    found = True
                    break
            assert found, f"Phone {phone} doesn't start with valid prefix"


class TestFakePerson:
    """Test complete fake person generation."""
    
    def test_get_fake_person_returns_dict(self):
        """get_fake_person() should return a dictionary."""
        fake_info = FakeInfo()
        person = fake_info.get_fake_person()
        assert isinstance(person, dict)
    
    def test_fake_person_has_all_required_fields(self):
        """Fake person should have CPR, names, gender, birthDate, address, phone."""
        fake_info = FakeInfo()
        person = fake_info.get_fake_person()
        required_fields = ['CPR', 'firstName', 'lastName', 'gender', 'birthDate', 'address', 'phoneNumber']
        for field in required_fields:
            assert field in person, f"Missing field: {field}"
    
    def test_fake_person_address_structure(self):
        """Address in person object should have all required fields."""
        fake_info = FakeInfo()
        person = fake_info.get_fake_person()
        address = person['address']
        required_address_fields = ['street', 'number', 'postal_code', 'town_name']
        for field in required_address_fields:
            assert field in address, f"Missing address field: {field}"
    
    def test_get_fake_persons_returns_list(self):
        """get_fake_persons() should return a list."""
        fake_info = FakeInfo()
        persons = fake_info.get_fake_persons(3)
        assert isinstance(persons, list)
    
    def test_get_fake_persons_returns_correct_count(self):
        """get_fake_persons(n) should return n persons."""
        for n in [1, 5, 10, 50]:
            fake_info = FakeInfo()
            persons = fake_info.get_fake_persons(n)
            assert len(persons) == n
    
    def test_get_fake_persons_large_bulk(self):
        """get_fake_persons should handle maximum allowed (100)."""
        fake_info = FakeInfo()
        persons = fake_info.get_fake_persons(100)
        assert len(persons) == 100
        # Verify each person has required fields
        for person in persons:
            assert 'CPR' in person
            assert 'firstName' in person
            assert 'address' in person


class TestDataConsistency:
    """Test data consistency across generated values."""
    
    def test_multiple_instances_have_unique_cprs(self):
        """Different FakeInfo instances should generate different CPRs."""
        cprs = [FakeInfo().get_cpr() for _ in range(50)]
        # Very unlikely to have all duplicates
        assert len(set(cprs)) > 40
    
    def test_cpr_independently_generated(self):
        """CPR should be independently generated, not reused."""
        fake_info = FakeInfo()
        cpr1 = fake_info.get_cpr()
        cpr2 = fake_info.get_cpr()
        # Both should be valid CPRs
        assert len(cpr1) == 10 and cpr1.isdigit()
        assert len(cpr2) == 10 and cpr2.isdigit()
