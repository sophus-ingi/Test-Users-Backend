# PHP to Python Migration Guide

This document outlines the conversion from PHP to Python for the Test-Users-Backend project.

## File Mappings

| PHP File | Python File | Description |
|----------|------------|-------------|
| `info/Info.php` | `info.py` | Configuration and database credentials from environment variables |
| `src/DB.php` | `db.py` | Database connection class using MySQL connector |
| `src/Town.php` | `town.py` | Generates random postal codes and town names |
| `src/FakeInfo.php` | `fake_info.py` | Generates fake person information |
| `index.php` | `app.py` | REST API server using Flask |

## Key Changes

### 1. **Framework Change: PHP → Flask**
   - The PHP REST API has been converted to a Flask application
   - All HTTP routing and request handling is now managed by Flask

### 2. **Database Connection: PDO → MySQL Connector**
   - Replaced PHP PDO with Python's `mysql-connector-python`
   - Connection error handling updated accordingly

### 3. **Class Structure**
   - Class naming: `CamelCase` (PHP) → `snake_case` (Python)
   - Method naming: `camelCase` (PHP) → `snake_case` (Python)
   - Constants remain `UPPER_CASE`

### 4. **Type Hints**
   - Added Python type hints for better code clarity
   - Return types documented for all methods

### 5. **String Formatting**
   - PHP string concatenation (`.`) → Python f-strings and `.format()`
   - JSON handling: `json_encode()` → `jsonify()` and `json.dumps()`

## Installation & Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables
Set these environment variables for database configuration:
```bash
export DB_HOST=localhost
export DB_NAME=addresses
export DB_USER=root
export DB_PASSWORD=yourpassword
```

### Run the Application
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

All endpoints remain the same as the original PHP implementation:

- `GET /cpr` - Get a fake CPR number
- `GET /name-gender` - Get fake name and gender
- `GET /name-gender-dob` - Get fake name, gender, and date of birth
- `GET /cpr-name-gender` - Get CPR, name, and gender
- `GET /cpr-name-gender-dob` - Get CPR, name, gender, and birth date
- `GET /address` - Get fake address
- `GET /phone` - Get fake phone number
- `GET /person?n=1` - Get one or more complete fake persons (n parameter: 1-100)

## Differences from PHP

### Error Handling
- Python uses exceptions instead of exit/die statements
- All database errors are caught and logged

### Random Number Generation
- PHP `mt_rand()` → Python `random.randint()`
- PHP `mt_rand(0, 9)` → Python `random.randint(0, 9)`

### Array/Dictionary Handling
- PHP arrays `['key' => 'value']` → Python dictionaries `{'key': 'value'}`

### File Reading
- PHP `file_get_contents()` → Python `open()` with context manager

### Static Properties
- PHP static properties → Python class variables

## Testing

You can test the endpoints using curl:
```bash
curl http://localhost:5000/cpr
curl http://localhost:5000/name-gender
curl http://localhost:5000/person?n=5
```

Or using Python requests:
```python
import requests

response = requests.get('http://localhost:5000/cpr')
print(response.json())
```

## Docker Integration

If using Docker, update your Dockerfile to run the Flask application:
```dockerfile
CMD ["python", "app.py"]
```

Or use gunicorn for production:
```dockerfile
RUN pip install gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## Notes

- The `person-names.json` and `addresses.sql` data files remain unchanged
- Database schema requirements are identical to the PHP version
- All business logic has been preserved from the original implementation
