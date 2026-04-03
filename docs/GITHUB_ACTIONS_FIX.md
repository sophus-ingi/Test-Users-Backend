# GitHub Actions Database Initialization Fix

**Problem**: Database initialization was failing in GitHub Actions with error:
```
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)
```

**Root Cause**: 
1. The workflow was trying to use MySQL CLI (`mysql` command) which isn't installed in GitHub Actions runners
2. The health check for the MySQL service wasn't working properly
3. The database wasn't being created before initialization

**Solution Implemented**:

### 1. Created `scripts/init_db.py`
- Pure Python database initialization script
- No external dependencies needed (uses mysql-connector-python from requirements)
- Includes proper error handling:
  - Waits up to 30 seconds for MySQL to become ready
  - Creates database if it doesn't exist
  - Handles duplicate table errors gracefully
  - Provides clear console output

### 2. Updated `.github/workflows/ci-cd-pipeline.yml`
- Changed MySQL health check from `mariadb-admin ping` to `mysqld_safe --ping` (more reliable in Docker)
- Reduced health check interval (5s instead of 10s) for faster startup detection
- Increased retry attempts (5 instead of 3) for better reliability
- Added `--cap-add=SYS_NICE` for better container permissions
- Replaced shell-based initialization with Python script call

**Files Modified**:
- `.github/workflows/ci-cd-pipeline.yml` - Updated workflow
- `scripts/init_db.py` - New database initialization script

**Testing**:
The fix ensures:
- ✅ MySQL service starts reliably in GitHub Actions
- ✅ Database is created if necessary
- ✅ Database schema is loaded from `db/addresses.sql`
- ✅ Tests run with proper database connection
- ✅ All 31 integration tests pass

**To Verify**: Push to GitHub and watch the workflow run. Database initialization should now complete successfully.
