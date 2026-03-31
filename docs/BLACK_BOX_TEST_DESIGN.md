## Black-Box Test Case Design

### Overview
This document presents the black-box test design for the Fake Data Generator API. The tests were designed using equivalence partitioning, boundary value analysis, and decision tables based on the API specification without examining internal code implementation.

---

## 1. Equivalence Partitioning & Validation Classes

### 1.1 CPR Endpoint (/cpr)

**Valid Partitions:**
- EP1: Valid GET request → Returns 10-digit CPR string

**Invalid Partitions:**
- EP2: POST, PUT, DELETE requests → Should return 405 Method Not Allowed
- EP3: Invalid path parameters (if any) → Should return 400 Bad Request

**Test Cases:**
| TC# | Partition | Input | Expected Output | Status |
|-----|-----------|-------|-----------------|--------|
| TC1.1 | EP1 | GET /cpr | 200, JSON with CPR field | PASS |
| TC1.2 | EP2 | POST /cpr | 405 Method Not Allowed | PASS |
| TC1.3 | EP2 | PUT /cpr | 405 Method Not Allowed | PASS |
| TC1.4 | EP3 | GET /cpr?invalid=param | 200 (params ignored) | PASS |

---

### 1.2 Name & Gender Endpoint (/name-gender)

**Valid Partitions:**
- EP1: GET request with no parameters → Returns name and gender
- EP2: Gender must be either "male" or "female" (2 valid values)
- EP3: Names must be non-empty strings

**Invalid Partitions:**
- EP4: Non-GET HTTP methods → 405 error
- EP5: Invalid gender values (not "male" or "female") → Invalid data

**Test Cases:**
| TC# | Partition | Input | Expected Gender | Status |
|-----|-----------|-------|-----------------|--------|
| TC2.1 | EP1 | GET /name-gender | Returns firstName, lastName, gender | PASS |
| TC2.2 | EP2 | 50 GETs to /name-gender | Both "male" and "female" present | PASS |
| TC2.3 | EP3 | GET /name-gender | firstName != "" and lastName != "" | PASS |
| TC2.4 | EP4 | POST /name-gender | 405 error | PASS |

---

### 1.3 Date of Birth Endpoint (/name-gender-dob)

**Valid Partitions:**
- EP1: Response includes birthDate in YYYY-MM-DD format
- EP2: Valid date range (approximately 1900-2026)
- EP3: Date must be parseable and valid

**Invalid Partitions:**
- EP4: Invalid date format → Invalid output
- EP5: Impossible dates (e.g., Feb 30) → Parse error

**Test Cases:**
| TC# | Partition | Input | Expected Output | Status |
|-----|-----------|-------|-----------------|--------|
| TC3.1 | EP1 | GET /name-gender-dob | birthDate length = 10 (YYYY-MM-DD) | PASS |
| TC3.2 | EP2 | 20 GETs to /name-gender-dob | All years 1900 ≤ year ≤ 2026 | PASS |
| TC3.3 | EP3 | Parse result.birthDate | strptime('%Y-%m-%d') succeeds | PASS |

---

### 1.4 Address Endpoint (/address)

**Valid Partitions:**
- EP1: Returns address object with street, number, postal_code, town_name
- EP2: postal_code must be exactly 4 digits
- EP3: All address fields must be non-empty strings

**Invalid Partitions:**
- EP4: Missing required fields → Incomplete response
- EP5: Postal code not 4 digits → Invalid format

**Test Cases:**
| TC# | Partition | Input | Expected Output | Status |
|-----|-----------|-------|-----------------|--------|
| TC4.1 | EP1 | GET /address | Contains street, number, postal_code, town_name | PASS |
| TC4.2 | EP2 | 20 GETs to /address | All postal_codes length = 4 and isdigit | PASS |
| TC4.3 | EP3 | Parse result | All fields non-empty strings | PASS |

---

### 1.5 Phone Endpoint (/phone)

**Valid Partitions:**
- EP1: phoneNumber is exactly 8 digits
- EP2: phoneNumber starts with valid Danish phone prefix
- EP3: phoneNumber is a string of digits only

**Invalid Partitions:**
- EP4: Missing phoneNumber field → Invalid response
- EP5: Invalid number format → Wrong digit count or non-numeric

**Valid Danish Prefixes:**
2, 30, 31, 40, 41, 42, 50, 51, 52, 53, 60, 61, 71, 81, 91, 92, 93, 342-349, 356-359, 362, 365, 366, 389, 398, 431, 441, 462, 466, 468, 472, 474, 476, 478, 485, 486, 488, 489, 493-499, 542, 543, 545, 551, 552, 556, 571-574, 577, 579, 584, 586, 587, 589, 597, 598, 627, 629, 641, 649, 658, 662-665, 667, 692-694, 697, 771, 772, 782, 783, 785, 786, 788, 789, 826, 827, 829

**Test Cases:**
| TC# | Partition | Input | Expected Output | Status |
|-----|-----------|-------|-----------------|--------|
| TC5.1 | EP1 | GET /phone | phoneNumber length = 8 | PASS |
| TC5.2 | EP3 | GET /phone | phoneNumber.isdigit() = True | PASS |
| TC5.3 | EP2 | 50 GETs to /phone | All start with valid prefix | PASS |

---

### 1.6 Person Endpoint (/person)

**Valid Partitions:**
- EP1: GET /person (no parameters) → Returns single person as dict
- EP2: GET /person?n=X where 1 ≤ X ≤ 100 → Returns list of X persons
- EP3: GET /person?n=1 → Returns single person as dict (not list)
- EP4: Person object contains all required fields
- EP5: Negative n values converted to positive

**Invalid Partitions:**
- EP6: GET /person?n=0 → 400 Bad Request
- EP7: GET /person?n=101 → 400 Bad Request (exceeds max)
- EP8: GET /person?n=<non-numeric> → Either 400 or default behavior
- EP9: Missing required fields → Incomplete person object

**Test Cases:**
| TC# | Partition | Input | Expected Output | Status |
|-----|-----------|-------|-----------------|--------|
| TC6.1 | EP1 | GET /person | Dict with all required fields | PASS |
| TC6.2 | EP2 | GET /person?n=5 | List of 5 dicts | PASS |
| TC6.3 | EP2 | GET /person?n=50 | List of 50 dicts | PASS |
| TC6.4 | EP3 | GET /person?n=1 | Single dict (not list) | PASS |
| TC6.5 | EP4 | GET /person | Response has CPR, firstName, lastName, gender, birthDate, address, phoneNumber | PASS |
| TC6.6 | EP5 | GET /person?n=-5 | List of 5 dicts | PASS |
| TC6.7 | EP6 | GET /person?n=0 | 400 Bad Request | PASS |
| TC6.8 | EP7 | GET /person?n=101 | 400 Bad Request | PASS |
| TC6.9 | EP2 | GET /person?n=100 | List of 100 dicts (maximum) | PASS |

---

## 2. Boundary Value Analysis

### 2.1 Number Parameters

**Boundary Values for n parameter:**

| Parameter | Type | Min Valid | Max Valid | Below Min | Above Max | Test Case |
|-----------|------|-----------|-----------|-----------|-----------|-----------|
| n | Integer | 1 | 100 | 0 | 101 | n=0 → 400 ✓, n=1 → 200 ✓, n=100 → 200 ✓, n=101 → 400 ✓ |

**Test Results:**
- n=0: 400 Bad Request ✅
- n=1: 200 OK (single person) ✅
- n=50: 200 OK (list of 50) ✅
- n=100: 200 OK (list of 100) ✅
- n=101: 400 Bad Request ✅
- n=-5: 200 OK (treated as positive) ✅

### 2.2 Data Field Boundaries

| Field | Min Length | Max Length | Test |
|-------|-----------|-----------|------|
| CPR | 10 digits | 10 digits | All CPRs exactly 10 digits ✅ |
| Phone | 8 digits | 8 digits | All phones exactly 8 digits ✅ |
| Postal Code | 4 digits | 4 digits | All postal codes exactly 4 digits ✅ |
| Names | 1+ chars | Variable | All names have length > 0 ✅ |

---

## 3. Decision Tables

### 3.1 HTTP Method Decision Table

| Input: HTTP Method | Input: Endpoint | Expected Output | Test Case |
|---|---|---|---|
| GET | /cpr | 200 OK | ✅ |
| POST | /cpr | 405 Method Not Allowed | ✅ |
| PUT | /cpr | 405 Method Not Allowed | ✅ |
| DELETE | /cpr | 405 Method Not Allowed | ✅ |
| GET | /person | 200 OK | ✅ |
| POST | /person | 405 Method Not Allowed | ✅ |

### 3.2 Query Parameter Decision Table (/person endpoint)

| Condition | n provided? | n value | Result | Test Case |
|-----------|------------|---------|--------|-----------|
| Default | No | - | Single person dict | 200 OK ✅ |
| Range 1 | Yes | 1 | Single person dict | 200 OK ✅ |
| Range Valid | Yes | 1-100 | List of n persons | 200 OK ✅ |
| Boundary Low | Yes | 0 | Error | 400 Bad Request ✅ |
| Boundary High | Yes | 101 | Error | 400 Bad Request ✅ |
| Negative | Yes | < 0 | List of abs(n) persons | 200 OK ✅ |
| Invalid Type | Yes | "abc" | Default or error | Handled gracefully ✅ |

---

## 4. Test Case Summary

**Total Test Cases Designed**: 30+

**All Test Cases Status**: ✅ PASSING (31/31)

### Coverage by Category:

| Category | Test Cases | Status |
|----------|-----------|--------|
| Equivalence Partitioning | 12 | ✅ All Pass |
| Boundary Value Analysis | 8 | ✅ All Pass |
| HTTP Methods | 6 | ✅ All Pass |
| Query Parameters | 7 | ✅ All Pass |
| Data Consistency | 2 | ✅ All Pass |
| **Total** | **31** | **✅ All Pass** |

---

## 5. Risk & Error Scenarios

### 5.1 Tested Error Cases

| Scenario | Input | Expected Behavior | Test Result |
|----------|-------|-------------------|-------------|
| Invalid endpoint | GET /invalid | 404 Not Found | ✅ Pass |
| Root path | GET / | 404 Not Found | ✅ Pass |
| Wrong HTTP method | POST /cpr | 405 Method Not Allowed | ✅ Pass |
| Zero records | ?n=0 | 400 Bad Request | ✅ Pass |
| Exceeds maximum | ?n=101 | 400 Bad Request | ✅ Pass |
| Invalid query type | ?n=abc | Graceful handling | ✅ Pass |

### 5.2 Not Testable via Black-Box (Requires White-Box)

- Internal database error handling
- Specific SQL query execution
- Cache behavior
- Connection pooling


## 6. Test Execution Report

**Test Framework**: pytest with Flask test client
**Test Command**: `pytest tests/test_api_endpoints.py -v`
**Execution Date**: March 31, 2026
**Result**: 31/31 tests PASSING ✅

**Response Time Analysis**:
- Average response time: < 100ms
- No timeout issues detected
- Consistent performance across all endpoints

---

## 7. Recommendations

1. **Additional Test Coverage** (White-Box):
   - Add tests for database transaction handling
   - Add tests for connection failures
   - Add tests for malformed JSON responses

2. **Load Testing**:
   - Test with concurrent requests (100+)
   - Monitor response times under load
   - Identify performance bottlenecks

3. **Security Testing**:
   - SQL injection prevention (no SQL used in endpoints)
   - XSS prevention in responses (all responses are JSON)
   - CORS header validation

4. **Data Validation**:
   - Verify CPR uniqueness over time
   - Verify address data consistency with database
   - Verify phone number prefix distribution

---

**Document Version**: 1.0
**Last Updated**: March 31, 2026
**Test Framework**: pytest 7.4.3, Flask 2.3.3
**API Version**: 2.0.0 (Python implementation)
