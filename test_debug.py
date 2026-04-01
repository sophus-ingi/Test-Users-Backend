#!/usr/bin/env python
"""Debug script to test FakeInfo class initialization."""

import os
import sys

# Set environment variables
os.environ['DB_HOST'] = 'mysql'
os.environ['DB_NAME'] = 'addresses'
os.environ['DB_USER'] = 'root'
os.environ['DB_PASSWORD'] = 'root'

try:
    from src.fake_info import FakeInfo
    print("✓ Successfully imported FakeInfo")
    
    print("Attempting to create FakeInfo instance...")
    fake_info = FakeInfo()
    print("✓ Successfully created FakeInfo instance")
    
    print("\nTesting methods:")
    print(f"CPR: {fake_info.get_cpr()}")
    print("✓ get_cpr() works")
    
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All tests passed!")
