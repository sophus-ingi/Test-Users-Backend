"""
Test suite for the Test-Users-Backend application.

Tests cover:
- Info configuration class
- Database connection (if database available)
- FakeInfo person generation
- Flask API endpoints
"""
import pytest
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app import app
from src.fake_info import FakeInfo
from src.info import Info


class TestInfo:
    """Tests for the Info configuration class."""
    
    def test_info_host(self):
        """Test getting database host."""
        host = Info.host()
        assert isinstance(host, str)
        assert len(host) > 0
    
    def test_info_db_name(self):
        """Test getting database name."""
        db_name = Info.db_name()
        assert isinstance(db_name, str)
        assert db_name == 'addresses'
    
    def test_info_user(self):
        """Test getting database user."""
        user = Info.user()
        assert isinstance(user, str)
        assert len(user) > 0
    
    def test_info_password(self):
        """Test getting database password."""
        password = Info.password()
        assert isinstance(password, str)


class TestFakeInfo:
    """Tests for the FakeInfo person generation class."""
    
    @pytest.fixture(autouse=True)
    def mock_town(self):
        """Mock the Town class to avoid database connection."""
        with patch('src.fake_info.Town') as mock_town_class:
            mock_town_instance = MagicMock()
            mock_town_instance.get_random_town.return_value = {
                'postal_code': '1000',
                'town_name': 'Copenhagen'
            }
            mock_town_class.return_value = mock_town_instance
            yield
    
    def test_fake_info_initialization(self):
        """Test that FakeInfo initializes with all required fields."""
        fake = FakeInfo()
        assert fake.cpr is not None
        assert fake.first_name is not None
        assert fake.last_name is not None
        assert fake.gender is not None
        assert fake.birth_date is not None
        assert fake.phone is not None
        assert isinstance(fake.address, dict)
    
    def test_get_cpr(self):
        """Test CPR generation."""
        fake = FakeInfo()
        cpr = fake.get_cpr()
        assert isinstance(cpr, str)
        assert len(cpr) == 10
        assert cpr.isdigit()
    
    def test_get_full_name_and_gender(self):
        """Test getting full name and gender."""
        fake = FakeInfo()
        result = fake.get_full_name_and_gender()
        assert isinstance(result, dict)
        assert 'firstName' in result
        assert 'lastName' in result
        assert 'gender' in result
        assert result['gender'] in [FakeInfo.GENDER_FEMININE, FakeInfo.GENDER_MASCULINE]
    
    def test_get_full_name_gender_and_birth_date(self):
        """Test getting full name, gender, and birth date."""
        fake = FakeInfo()
        result = fake.get_full_name_gender_and_birth_date()
        assert isinstance(result, dict)
        assert 'firstName' in result
        assert 'lastName' in result
        assert 'gender' in result
        assert 'birthDate' in result
        # Birth date should be in YYYY-MM-DD format
        assert len(result['birthDate']) == 10
        assert result['birthDate'].count('-') == 2
    
    def test_get_cpr_full_name_and_gender(self):
        """Test getting CPR, full name, and gender."""
        fake = FakeInfo()
        result = fake.get_cpr_full_name_and_gender()
        assert isinstance(result, dict)
        assert 'CPR' in result
        assert 'firstName' in result
        assert 'lastName' in result
        assert 'gender' in result
    
    def test_get_cpr_full_name_gender_and_birth_date(self):
        """Test getting CPR, full name, gender, and birth date."""
        fake = FakeInfo()
        result = fake.get_cpr_full_name_gender_and_birth_date()
        assert isinstance(result, dict)
        assert 'CPR' in result
        assert 'firstName' in result
        assert 'lastName' in result
        assert 'gender' in result
        assert 'birthDate' in result
    
    def test_get_address(self):
        """Test getting address."""
        fake = FakeInfo()
        result = fake.get_address()
        assert isinstance(result, dict)
        # Address is returned as flat dictionary, not nested
        assert 'street' in result
        assert 'number' in result
        assert 'floor' in result
        assert 'door' in result
        assert 'postal_code' in result
        assert 'town_name' in result
    
    def test_get_phone_number(self):
        """Test getting phone number."""
        fake = FakeInfo()
        phone = fake.get_phone_number()
        assert isinstance(phone, str)
        assert len(phone) == 8
        assert phone.isdigit()
    
    def test_get_fake_person(self):
        """Test getting complete fake person information."""
        fake = FakeInfo()
        person = fake.get_fake_person()
        assert isinstance(person, dict)
        assert 'CPR' in person
        assert 'firstName' in person
        assert 'lastName' in person
        assert 'gender' in person
        assert 'birthDate' in person
        assert 'address' in person
        assert 'phoneNumber' in person
    
    def test_get_fake_persons_default(self):
        """Test getting multiple fake persons with default amount."""
        fake = FakeInfo()
        persons = fake.get_fake_persons()
        assert isinstance(persons, list)
        assert len(persons) == FakeInfo.MIN_BULK_PERSONS
    
    def test_get_fake_persons_single(self):
        """Test getting a single fake person."""
        fake = FakeInfo()
        persons = fake.get_fake_persons(1)
        assert isinstance(persons, list)
        assert len(persons) == FakeInfo.MIN_BULK_PERSONS  # Should be clamped to MIN
    
    def test_get_fake_persons_multiple(self):
        """Test getting multiple fake persons."""
        fake = FakeInfo()
        persons = fake.get_fake_persons(5)
        assert isinstance(persons, list)
        assert len(persons) == 5
        for person in persons:
            assert 'CPR' in person
            assert 'firstName' in person
    
    def test_get_fake_persons_max_limit(self):
        """Test that max persons limit is enforced."""
        fake = FakeInfo()
        persons = fake.get_fake_persons(200)
        assert len(persons) == FakeInfo.MAX_BULK_PERSONS
    
    def test_cpr_gender_parity(self):
        """Test that CPR last digit matches gender parity."""
        for _ in range(10):
            fake = FakeInfo()
            cpr = fake.get_cpr()
            last_digit = int(cpr[-1])
            if fake.gender == FakeInfo.GENDER_FEMININE:
                assert last_digit % 2 == 0, "Female CPR must end in even number"
            else:
                assert last_digit % 2 == 1, "Male CPR must end in odd number"


class TestFlaskAPI:
    """Tests for the Flask REST API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create Flask test client with mocked database."""
        app.config['TESTING'] = True
        with patch('src.fake_info.Town') as mock_town_class:
            mock_town_instance = MagicMock()
            mock_town_instance.get_random_town.return_value = {
                'postal_code': '1000',
                'town_name': 'Copenhagen'
            }
            mock_town_class.return_value = mock_town_instance
            
            with app.test_client() as client:
                yield client
    
    def test_cpr_endpoint(self, client):
        """Test /cpr endpoint."""
        response = client.get('/cpr')
        assert response.status_code == 200
        data = response.get_json()
        assert 'CPR' in data
        assert isinstance(data['CPR'], str)
        assert len(data['CPR']) == 10
    
    def test_name_gender_endpoint(self, client):
        """Test /name-gender endpoint."""
        response = client.get('/name-gender')
        assert response.status_code == 200
        data = response.get_json()
        assert 'firstName' in data
        assert 'lastName' in data
        assert 'gender' in data
        assert data['gender'] in ['female', 'male']
    
    def test_name_gender_dob_endpoint(self, client):
        """Test /name-gender-dob endpoint."""
        response = client.get('/name-gender-dob')
        assert response.status_code == 200
        data = response.get_json()
        assert 'firstName' in data
        assert 'lastName' in data
        assert 'gender' in data
        assert 'birthDate' in data
    
    def test_cpr_name_gender_endpoint(self, client):
        """Test /cpr-name-gender endpoint."""
        response = client.get('/cpr-name-gender')
        assert response.status_code == 200
        data = response.get_json()
        assert 'CPR' in data
        assert 'firstName' in data
        assert 'lastName' in data
        assert 'gender' in data
    
    def test_cpr_name_gender_dob_endpoint(self, client):
        """Test /cpr-name-gender-dob endpoint."""
        response = client.get('/cpr-name-gender-dob')
        assert response.status_code == 200
        data = response.get_json()
        assert 'CPR' in data
        assert 'firstName' in data
        assert 'lastName' in data
        assert 'gender' in data
        assert 'birthDate' in data
    
    def test_address_endpoint(self, client):
        """Test /address endpoint."""
        response = client.get('/address')
        assert response.status_code == 200
        data = response.get_json()
        # Address is returned as flat dictionary, not nested
        assert 'street' in data
        assert 'number' in data
        assert 'floor' in data
        assert 'door' in data
        assert 'postal_code' in data
        assert 'town_name' in data
    
    def test_phone_endpoint(self, client):
        """Test /phone endpoint."""
        response = client.get('/phone')
        assert response.status_code == 200
        data = response.get_json()
        assert 'phoneNumber' in data
        assert len(data['phoneNumber']) == 8
    
    def test_person_endpoint_default(self, client):
        """Test /person endpoint with default parameter."""
        response = client.get('/person')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'CPR' in data
        assert 'firstName' in data
    
    def test_person_endpoint_single(self, client):
        """Test /person endpoint with n=1."""
        response = client.get('/person?n=1')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'CPR' in data
    
    def test_person_endpoint_multiple(self, client):
        """Test /person endpoint with n=5."""
        response = client.get('/person?n=5')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 5
    
    def test_person_endpoint_max(self, client):
        """Test /person endpoint with n=100."""
        response = client.get('/person?n=100')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 100
    
    def test_person_endpoint_zero(self, client):
        """Test /person endpoint with n=0 (invalid)."""
        response = client.get('/person?n=0')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_person_endpoint_exceed_max(self, client):
        """Test /person endpoint with n > 100 (invalid)."""
        response = client.get('/person?n=150')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_invalid_endpoint(self, client):
        """Test invalid endpoint."""
        response = client.get('/invalid-endpoint')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'Incorrect API endpoint' in data['error']
    
    def test_post_method_not_allowed(self, client):
        """Test that POST method is not allowed."""
        response = client.post('/cpr')
        assert response.status_code == 405
        data = response.get_json()
        assert 'error' in data
    
    def test_cors_headers(self, client):
        """Test that CORS headers are present."""
        response = client.get('/cpr')
        assert 'Access-Control-Allow-Origin' in response.headers
        assert response.headers['Access-Control-Allow-Origin'] == '*'
    
    def test_content_type_header(self, client):
        """Test that Content-Type header is set correctly."""
        response = client.get('/cpr')
        assert 'Content-Type' in response.headers
        assert 'application/json' in response.headers['Content-Type']
    
    def test_api_version_header(self, client):
        """Test that API version header is present."""
        response = client.get('/cpr')
        assert 'Accept-version' in response.headers
        assert response.headers['Accept-version'] == 'v1'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
