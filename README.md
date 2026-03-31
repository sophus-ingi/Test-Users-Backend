# Fake Data Generator

## Purpose
REST API that generates fake data of nonexistent Danish persons. Originally built in PHP, now converted to **Python with Flask** for improved maintainability and performance.

## Dependencies

- The fake persons' first name, last name, and gender are extracted from the file `data/person-names.json`.
- The fake persons' postal code and town are extracted from the MariaDB/MySQL database `addresses`.
- Python dependencies listed in `requirements.txt`: Flask, mysql-connector-python, pytest

## Usage

### Option 1: Run with Docker (Recommended)
```bash
docker compose up --build -d    # Start
docker compose down -v          # Stop
```

### Option 2: Run Python Directly

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Set environment variables (Windows PowerShell):**
```powershell
$env:DB_HOST = "localhost"
$env:DB_NAME = "addresses"
$env:DB_USER = "root"
$env:DB_PASSWORD = "yourpassword"
```

**Run the Flask server:**
```bash
python app.py
```
The API will be available at `http://localhost:5000`

## API Endpoints
|Method|Endpoint|
|------|--------|
|GET|/cpr|
|GET|/name-gender|
|GET|/name-gender-dob|
|GET|/cpr-name-gender|
|GET|/cpr-name-gender-dob|
|GET|/address|
|GET|/phone|
|GET|/person|
|GET|/person?n=<number_of_fake_persons>|

## API Sample Output
`GET /cpr`
```json
{
    "CPR": "0412489054"
}
```

`GET /person`
```json
{
    "CPR": "0107832911",
    "firstName": "Michelle W.",
    "lastName": "Henriksen",
    "gender": "female",
    "birthDate": "1983-07-01",
    "address": {
        "street": "GYØVCoØMeceOjøtÆgvYrøQQDascNFCHArnSNrxub",
        "number": "521",
        "floor": 74,
        "door": "tv",
        "postal_code": "8670",
        "town_name": "Låsby"
    },
    "phoneNumber": "58676658"
}
```

`GET /person&n=3`
```json
[
    {
        "CPR": "2411576095",
        "firstName": "Laurits S.",
        "lastName": "Kjeldsen",
        "gender": "male",
        "birthDate": "1957-11-24",
        "address": {
            "street": "aÅGgøhIbJXVsRÆøjLnåæFoXtsgU Ø NINFYwBnaø",
            "number": "413",
            "floor": 46,
            "door": "tv",
            "postal_code": "8700",
            "town_name": "Horsens"
        },
        "phoneNumber": "35753186"
    },
    {
        "CPR": "1008114708",
        "firstName": "Tristan M.",
        "lastName": "Christoffersen",
        "gender": "male",
        "birthDate": "2011-08-10",
        "address": {
            "street": "dÅJaKxnRqdRbtxaUyviQBxZÅu JozfbyonuCgNXA",
            "number": "77K",
            "floor": 82,
            "door": 44,
            "postal_code": "3210",
            "town_name": "Vejby"
        },
        "phoneNumber": "69712398"
    },
    {
        "CPR": "0507110046",
        "firstName": "Thomas E.",
        "lastName": "Olsen",
        "gender": "male",
        "birthDate": "1911-07-05",
        "address": {
            "street": "m tfYxXøBxmhadvtIHwWvTWEEIRjOÆglcHigsVjb",
            "number": "184",
            "floor": 3,
            "door": "th",
            "postal_code": "7950",
            "town_name": "Erslev"
        },
        "phoneNumber": "38907752"
    }
]
```

## Migration from PHP to Python

This project has been **successfully converted from PHP to Python 3** with Flask. For detailed information about the migration, see [PYTHON_MIGRATION.md](PYTHON_MIGRATION.md).

### Key Changes:
- **Framework**: PHP → Python Flask
- **Database Driver**: PDO → mysql-connector-python
- **File Structure**: `src/*.py` replaces `src/*.php`
- **Testing**: Added pytest for unit and integration tests
- **API Endpoints**: All endpoints remain compatible

## Class `FakeInfo` - Public methods

```python
- get_cpr() -> str
- get_full_name_and_gender() -> dict
- get_full_name_gender_and_birth_date() -> dict
- get_cpr_full_name_and_gender() -> dict
- get_cpr_full_name_gender_and_birth_date() -> dict
- get_address() -> dict
- get_phone_number() -> str
- get_fake_person() -> dict
- get_fake_persons(amount: int) -> list
```

## Sample Class Output

```python
from src.fake_info import FakeInfo

fake_info = FakeInfo()
fake_persons = fake_info.get_fake_persons(1)
print(fake_persons)
```

Output:
```json
[
    {
        "CPR": "1909743965",
        "firstName": "Anton D.",
        "lastName": "Jespersen",
        "gender": "male",
        "birthDate": "1974-09-19",
        "address": {
            "street": "WTquWUqMiHLBKXcEÆnMpqhdGæzlrødfAAAJuGGXø",
            "number": "456",
            "floor": 61,
            "door": "th",
            "postal_code": "3650",
            "town_name": "Ølstykke"
        },
        "phoneNumber": "55129415"
    }
]
```

## Testing

Run the test suite using pytest:
```bash
pytest test_backend.py -v
```

## Tools
Python 3 / Flask / MySQL

## Author
Arturo Mora-Rioja