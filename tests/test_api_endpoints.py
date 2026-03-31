"""
Integration tests for Flask API endpoints.

Tests cover:
- All API routes and HTTP methods
- Request/response format validation
- Status code validation
- Error handling
- Edge cases (invalid parameters, boundary conditions)
"""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestCPREndpoint:
    """Test /cpr endpoint."""
    
    def test_cpr_endpoint_get_success(self, client):
        """GET /cpr should return 200 with valid CPR."""
        response = client.get('/cpr')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'CPR' in data
        assert isinstance(data['CPR'], str)
        assert len(data['CPR']) == 10
        assert data['CPR'].isdigit()
    
    def test_cpr_endpoint_returns_json(self, client):
        """Response should be valid JSON."""
        response = client.get('/cpr')
        assert response.content_type == 'application/json; charset=utf-8'
    
    def test_cpr_endpoint_post_not_allowed(self, client):
        """POST /cpr should not be allowed."""
        response = client.post('/cpr')
        assert response.status_code == 405
    
    def test_cpr_endpoint_put_not_allowed(self, client):
        """PUT /cpr should not be allowed."""
        response = client.put('/cpr')
        assert response.status_code == 405
    
    def test_cpr_endpoint_delete_not_allowed(self, client):
        """DELETE /cpr should not be allowed."""
        response = client.delete('/cpr')
        assert response.status_code == 405
    
    def test_cpr_endpoint_multiple_calls_different(self, client):
        """Multiple calls should generate different CPRs."""
        cprs = [json.loads(client.get('/cpr').data)['CPR'] for _ in range(10)]
        assert len(set(cprs)) > 1


class TestNameGenderEndpoint:
    """Test /name-gender endpoint."""
    
    def test_name_gender_endpoint_success(self, client):
        """GET /name-gender should return valid name and gender."""
        response = client.get('/name-gender')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'firstName' in data
        assert 'lastName' in data
        assert 'gender' in data
        assert data['gender'] in ['male', 'female']
    
    def test_name_gender_endpoint_names_not_empty(self, client):
        """Names should be non-empty strings."""
        response = client.get('/name-gender')
        data = json.loads(response.data)
        assert len(data['firstName']) > 0
        assert len(data['lastName']) > 0
    
    def test_name_gender_endpoint_cors_headers(self, client):
        """Response should include CORS headers."""
        response = client.get('/name-gender')
        assert response.headers.get('Access-Control-Allow-Origin') == '*'


class TestNameGenderDobEndpoint:
    """Test /name-gender-dob endpoint."""
    
    def test_name_gender_dob_endpoint_success(self, client):
        """GET /name-gender-dob should return name, gender, and birth date."""
        response = client.get('/name-gender-dob')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'firstName' in data
        assert 'lastName' in data
        assert 'gender' in data
        assert 'birthDate' in data
    
    def test_birth_date_format_valid(self, client):
        """Birth date should be in YYYY-MM-DD format."""
        response = client.get('/name-gender-dob')
        data = json.loads(response.data)
        birth_date = data['birthDate']
        # Should be 10 characters (YYYY-MM-DD)
        assert len(birth_date) == 10
        # Should contain dashes at positions 4 and 7
        assert birth_date[4] == '-' and birth_date[7] == '-'


class TestCPRNameGenderEndpoint:
    """Test /cpr-name-gender endpoint."""
    
    def test_cpr_name_gender_endpoint_success(self, client):
        """GET /cpr-name-gender should return CPR, name, and gender."""
        response = client.get('/cpr-name-gender')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'CPR' in data
        assert 'firstName' in data
        assert 'lastName' in data
        assert 'gender' in data


class TestCPRNameGenderDobEndpoint:
    """Test /cpr-name-gender-dob endpoint."""
    
    def test_cpr_name_gender_dob_endpoint_success(self, client):
        """GET /cpr-name-gender-dob should return all fields."""
        response = client.get('/cpr-name-gender-dob')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'CPR' in data
        assert 'firstName' in data
        assert 'lastName' in data
        assert 'gender' in data
        assert 'birthDate' in data


class TestAddressEndpoint:
    """Test /address endpoint."""
    
    def test_address_endpoint_success(self, client):
        """GET /address should return valid address."""
        response = client.get('/address')
        assert response.status_code == 200
        data = json.loads(response.data)
        # Address is nested in the response
        assert 'address' in data
        address = data['address']
        assert 'street' in address
        assert 'number' in address
        assert 'postal_code' in address
        assert 'town_name' in address
    
    def test_address_postal_code_valid(self, client):
        """Postal code should be 4 digits."""
        response = client.get('/address')
        data = json.loads(response.data)
        address = data['address']
        postal_code = address['postal_code']
        assert len(postal_code) == 4
        assert postal_code.isdigit()


class TestPhoneEndpoint:
    """Test /phone endpoint."""
    
    def test_phone_endpoint_success(self, client):
        """GET /phone should return valid phone number."""
        response = client.get('/phone')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'phoneNumber' in data
        phone = data['phoneNumber']
        assert len(phone) == 8
        assert phone.isdigit()


class TestPersonEndpoint:
    """Test /person endpoint."""
    
    def test_person_endpoint_default_success(self, client):
        """GET /person should return one person by default."""
        response = client.get('/person')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
        assert 'CPR' in data
        assert 'firstName' in data
        assert 'address' in data
    
    def test_person_endpoint_with_n_parameter(self, client):
        """GET /person?n=5 should return 5 persons."""
        response = client.get('/person?n=5')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 5
    
    def test_person_endpoint_with_n_1(self, client):
        """GET /person?n=1 should return single person as dict."""
        response = client.get('/person?n=1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_person_endpoint_with_large_n(self, client):
        """GET /person?n=100 should return 100 persons."""
        response = client.get('/person?n=100')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 100
    
    def test_person_endpoint_n_zero_error(self, client):
        """GET /person?n=0 should return 400 error."""
        response = client.get('/person?n=0')
        assert response.status_code == 400
    
    def test_person_endpoint_n_exceeds_max_error(self, client):
        """GET /person?n=101 should return 400 error (exceeds max 100)."""
        response = client.get('/person?n=101')
        assert response.status_code == 400
    
    def test_person_endpoint_n_negative_converts_to_positive(self, client):
        """GET /person?n=-5 should be treated as n=5."""
        response = client.get('/person?n=-5')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 5
    
    def test_person_endpoint_n_invalid_string(self, client):
        """GET /person?n=abc should handle gracefully."""
        response = client.get('/person?n=abc')
        # Should either return 400 or treat as default
        assert response.status_code in [200, 400]
    
    def test_person_has_all_required_fields(self, client):
        """Person object should have all required fields."""
        response = client.get('/person')
        data = json.loads(response.data)
        required_fields = ['CPR', 'firstName', 'lastName', 'gender', 'birthDate', 'address', 'phoneNumber']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
    
    def test_person_address_has_all_fields(self, client):
        """Person's address should have all required fields."""
        response = client.get('/person')
        data = json.loads(response.data)
        address = data['address']
        address_fields = ['street', 'number', 'postal_code', 'town_name']
        for field in address_fields:
            assert field in address, f"Missing address field: {field}"


class TestInvalidEndpoints:
    """Test error handling for invalid endpoints."""
    
    def test_invalid_endpoint_404(self, client):
        """GET /invalid-endpoint should return 404."""
        response = client.get('/invalid-endpoint')
        assert response.status_code == 404
    
    def test_root_endpoint_404(self, client):
        """GET / should return 404."""
        response = client.get('/')
        assert response.status_code == 404
    
    def test_api_version_header_present(self, client):
        """Response should include API version header."""
        response = client.get('/cpr')
        assert 'Accept-version' in response.headers


class TestDataConsistency:
    """Test consistency of generated data across endpoints."""
    
    def test_always_valid_json_responses(self, client):
        """All endpoints should return valid JSON."""
        endpoints = ['/cpr', '/name-gender', '/address', '/phone', '/person']
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code in [200, 400, 404, 405]
            if response.status_code == 200:
                try:
                    json.loads(response.data)
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON from {endpoint}")
    
    def test_cors_headers_on_all_endpoints(self, client):
        """All successful responses should have CORS headers."""
        endpoints = ['/cpr', '/name-gender', '/address', '/phone']
        for endpoint in endpoints:
            response = client.get(endpoint)
            if response.status_code == 200:
                assert response.headers.get('Access-Control-Allow-Origin') == '*'
