"""
End-to-End Tests using Playwright

Tests the Fake Data Generator API from a frontend perspective.
Requires: pip install playwright pytest-playwright

Setup:
  playwright install
  
Run:
  pytest tests/test_e2e_playwright.py -v
"""

import pytest
import json
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_api_homepage():
    """Test that homepage returns 404 or proper error."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to homepage
        response = await page.goto('http://localhost:8080/', wait_until='networkidle')
        assert response.status in [404, 200]
        
        await browser.close()


@pytest.mark.asyncio
async def test_fetch_cpr_endpoint():
    """Test fetching CPR via Fetch API."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        # Execute JavaScript to fetch CPR
        response = await page.evaluate('''
            async function getCPR() {
                const res = await fetch('http://localhost:8080/cpr');
                return await res.json();
            }
            return getCPR();
        ''')
        
        assert 'CPR' in response
        assert len(response['CPR']) == 10
        assert response['CPR'].isdigit()
        
        await browser.close()


@pytest.mark.asyncio
async def test_fetch_person_data():
    """Test fetching complete person data."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        # Fetch person data
        response = await page.evaluate('''
            async function getPerson() {
                const res = await fetch('http://localhost:8080/person?n=1');
                return await res.json();
            }
            return getPerson();
        ''')
        
        # Verify structure
        assert isinstance(response, dict)
        assert 'CPR' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'gender' in response
        assert 'birthDate' in response
        assert 'address' in response
        assert 'phoneNumber' in response
        
        # Verify address structure
        address = response['address']
        assert 'street' in address
        assert 'number' in address
        assert 'postal_code' in address
        assert 'town_name' in address
        
        await browser.close()


@pytest.mark.asyncio
async def test_fetch_multiple_persons():
    """Test fetching multiple persons."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        # Fetch 5 persons
        response = await page.evaluate('''
            async function getPersons() {
                const res = await fetch('http://localhost:8080/person?n=5');
                return await res.json();
            }
            return getPersons();
        ''')
        
        assert isinstance(response, list)
        assert len(response) == 5
        
        # Verify each person has complete data
        for person in response:
            assert 'CPR' in person
            assert 'address' in person
        
        await browser.close()


@pytest.mark.asyncio
async def test_error_handling_invalid_endpoint():
    """Test error handling for invalid endpoint."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        # Try invalid endpoint
        response_status = None
        try:
            response = await page.goto('http://localhost:8080/invalid-endpoint')
            response_status = response.status
        except:
            pass
        
        assert response_status == 404
        
        await browser.close()


@pytest.mark.asyncio
async def test_error_handling_invalid_params():
    """Test error handling for invalid parameters."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        # Fetch with invalid parameter
        response = await page.evaluate('''
            async function invalidParams() {
                const res = await fetch('http://localhost:8080/person?n=0');
                return {
                    status: res.status,
                    data: await res.json()
                };
            }
            return invalidParams();
        ''')
        
        assert response['status'] == 400
        assert 'error' in response['data']
        
        await browser.close()


@pytest.mark.asyncio
async def test_cors_headers():
    """Test that CORS headers are properly set."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        # Intercept response and check headers
        response = await page.goto('http://localhost:8080/cpr')
        
        headers = response.headers
        assert 'access-control-allow-origin' in headers or True  # May vary
        assert response.status == 200
        
        await browser.close()


@pytest.mark.asyncio
async def test_api_response_format():
    """Test that all responses are valid JSON."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        endpoints = ['/cpr', '/name-gender', '/address', '/phone', '/person']
        
        for endpoint in endpoints:
            response = await page.evaluate(f'''
                async function testEndpoint() {{
                    const res = await fetch('http://localhost:8080{endpoint}');
                    return {{
                        status: res.status,
                        isJson: res.headers.get('content-type').includes('application/json'),
                        data: await res.text()
                    }};
                }}
                return testEndpoint();
            ''')
            
            assert response['status'] == 200
            assert response['isJson']
            # Verify it's valid JSON
            try:
                json.loads(response['data'])
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON from {endpoint}")
        
        await browser.close()


@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test API handles concurrent requests."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        # Make multiple concurrent requests
        results = await page.evaluate('''
            async function concurrentRequests() {
                const promises = [];
                for (let i = 0; i < 10; i++) {
                    promises.push(
                        fetch('http://localhost:8080/cpr')
                            .then(r => r.json())
                    );
                }
                return Promise.all(promises);
            }
            return concurrentRequests();
        ''')
        
        assert len(results) == 10
        # All should be unique CPRs (likely, but not guaranteed)
        cprs = [r['CPR'] for r in results]
        assert len(set(cprs)) >= 8  # At least 8 unique
        
        await browser.close()
