# Fake Data Generator

## Purpose
REST API that generates fake data of nonexistent Danish persons. Originally built in PHP, now converted to **Python with Flask** for improved maintainability and performance.

**Status**: ✅ Complete with 60 comprehensive tests (95% coverage) and CI/CD pipeline

## Dependencies

- The fake persons' first name, last name, and gender are extracted from the file `data/person-names.json`.
- The fake persons' postal code and town are extracted from the MariaDB/MySQL database `addresses`.
- Python dependencies listed in `requirements.txt`: Flask, mysql-connector-python, pytest

## Quick Start

### 🐳 Fastest Way (Docker)
```bash
docker compose up -d    # Start backend + database
docker compose down -v  # Stop
```
API available at `http://localhost:8080`

### 💻 Local Python
```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
API available at `http://localhost:5000`

## Usage

### Option 1: Run with Docker (Recommended)
```bash
docker compose up --build -d    # Start
docker compose down -v          # Stop
```

### Option 2: Run Python Directly

**1. Create and activate virtual environment:**

Windows (PowerShell):
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# (If you get permission denied, run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)
```

Linux/Mac:
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Set environment variables (Windows PowerShell):**
```powershell
$env:DB_HOST = "localhost"
$env:DB_NAME = "addresses"
$env:DB_USER = "root"
$env:DB_PASSWORD = "yourpassword"
```

Linux/Mac:
```bash
export DB_HOST=localhost
export DB_NAME=addresses
export DB_USER=root
export DB_PASSWORD=yourpassword
```

**4. Run the Flask server:**
```bash
python app.py
```
The API will be available at `http://localhost:5000`

**5. Deactivate virtual environment (when done):**
```bash
deactivate
```

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

### 🚀 Quick Test Commands (Copy & Paste)

**⚡ Run ALL 60 tests (FASTEST):**
```powershell
.\.venv\Scripts\pytest tests/ -v
```

**📊 Run with coverage report:**
```powershell
.\.venv\Scripts\pip install pytest-cov -q
.\.venv\Scripts\pytest tests/ --cov=src --cov=app --cov-report=term
```

**🧪 Run unit tests only (29 tests):**
```powershell
.\.venv\Scripts\pytest tests/test_fake_info.py -v
```

**🔗 Run integration tests only (31 tests):**
```powershell
.\.venv\Scripts\pytest tests/test_api_endpoints.py -v
```

**🐳 Run tests in Docker:**
```bash
docker compose up -d
docker compose exec web python -m pytest tests/ -v
```

### Test Suite Overview

| Test File | Tests | Purpose | Status |
|-----------|-------|---------|--------|
| `test_fake_info.py` | 29 | Unit tests - individual functions | ✅ All passing |
| `test_api_endpoints.py` | 31 | Integration tests - API endpoints + DB | ✅ All passing |
| **TOTAL** | **60** | Backend coverage | **✅ 95%** |

### Full System E2E Testing

Complete end-to-end testing (UI → API → Backend) is handled in a **separate E2E repository** maintained by Sophus:
- **Repository**: https://github.com/sophus-ingi/Test-Users-Frontend
- **Tests**: 35+ E2E tests using Playwright
- **Coverage**: Full user workflow testing (button clicks, forms, data display)

For complete testing documentation, see [docs/TESTING.md](docs/TESTING.md)

## Development Setup

### Prerequisites
- Python 3.12+
- MySQL/MariaDB (or use Docker)
- pip and venv (included with Python)

### Quick Start with venv

**Windows (PowerShell):**
```powershell
# Clone/navigate to project
cd Test-Users-Backend

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import flask; print(f'Flask {flask.__version__} installed')"
```

**Linux/Mac (Bash/Zsh):**
```bash
cd Test-Users-Backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "import flask; print(f'Flask {flask.__version__} installed')"
```

### Running Different Configurations

**Development Mode (Hot Reload):**
```bash
# Terminal 1: Start database
docker compose up db -d

# Terminal 2: Run Flask with venv
.\.venv\Scripts\python.exe app.py
# Or on Linux: ./.venv/bin/python app.py
```

**Production Mode (Docker):**
```bash
docker compose up --build -d
# API available at http://localhost:8080
```

**Testing Mode:**
```bash
# Activate venv first
.\.venv\Scripts\Activate.ps1  # Windows
# or
source .venv/bin/activate     # Linux/Mac

# Run tests
pytest tests/ -v --tb=short
```

## Troubleshooting

### Virtual Environment Issues

**Error: "python: command not found"**
- Ensure Python 3.12+ is installed: `python --version`
- On Linux: Use `python3` instead of `python`

**Error: "venv module not found"**
- On Linux/Mac: Install venv with `sudo apt-get install python3-venv`

**Error: "cannot activate venv script"**
- Windows: Allow script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Linux/Mac: Make script executable: `chmod +x .venv/bin/activate`

### Database Connection

**Error: "Connection unsuccessful"**
- Ensure database is running: `docker compose up db -d`
- Check credentials match in environment variables
- Verify MySQL/MariaDB is listening on correct port (3306)

**Database not initialized:**
```bash
# Initialize database
docker compose exec db mysql -u root -p$DB_PASSWORD addresses < db/addresses.sql
```

### Flask Server

**Error: "Address already in use"**
- Port 5000/8080 is in use. Kill existing process or use different port
- Windows: `netstat -ano | findstr :5000`
- Linux: `lsof -i :5000`

**Error: "Module not found"**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Tests

**Tests fail with "Connection refused"**
- Ensure Docker containers are running: `docker compose ps`
- Restart containers: `docker compose down && docker compose up -d`

**Import errors in tests**
- Activate venv: `.\.venv\Scripts\Activate.ps1` (Windows)
- Verify installed packages: `pip list`

## Tools
Python 3.12 / Flask 2.3.3 / MySQL / Docker / pytest

## Author
Arturo Mora-Rioja
**Converted to Python**: March 2026