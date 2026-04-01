#!/usr/bin/env python3
"""Initialize database for CI/CD pipeline."""

import time
import sys
import os
import mysql.connector
from mysql.connector import Error as MySQLError

def wait_for_mysql(max_attempts=30):
    """Wait for MySQL to be ready."""
    print("Waiting for MySQL to be ready...")
    for attempt in range(max_attempts):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                connection_timeout=5
            )
            print("✓ MySQL is ready!")
            conn.close()
            return True
        except MySQLError as e:
            print(f"  Attempt {attempt+1}/{max_attempts}: Connecting...", end="\r")
            time.sleep(1)
    
    return False

def create_database():
    """Ensure database exists."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS addresses")
        conn.commit()
        print("✓ Database 'addresses' exists")
        conn.close()
        return True
    except MySQLError as e:
        print(f"✗ Error creating database: {e}")
        return False

def initialize_database():
    """Load database schema."""
    print("Loading database schema...")
    
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='addresses'
        )
        cursor = conn.cursor()
        
        # Read and execute SQL file
        sql_file = 'db/addresses.sql'
        if not os.path.exists(sql_file):
            print(f"✗ Error: {sql_file} not found")
            return False
            
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split by statements and execute
        statements = sql_content.split(';')
        successful = 0
        for statement in statements:
            stmt = statement.strip()
            if stmt:
                try:
                    cursor.execute(stmt)
                    successful += 1
                except MySQLError as e:
                    # Some errors are expected (like recreating tables)
                    error_msg = str(e).lower()
                    if 'already exists' in error_msg or 'duplicate' in error_msg:
                        print(f"  ℹ Table already exists (expected)")
                    else:
                        print(f"  ✗ Error executing statement: {e}")
        
        conn.commit()
        conn.close()
        print(f"✓ Database initialized successfully! ({successful} statements executed)")
        return True
        
    except MySQLError as e:
        print(f"✗ Error initializing database: {e}")
        return False

if __name__ == '__main__':
    print("=== Database Initialization Script ===")
    print()
    
    # Wait for MySQL
    if not wait_for_mysql():
        print("✗ MySQL did not become ready after 30 seconds")
        sys.exit(1)
    
    print()
    
    # Create database
    if not create_database():
        print("✗ Failed to create/verify database")
        sys.exit(1)
    
    print()
    
    # Initialize database
    if not initialize_database():
        print("✗ Failed to initialize database")
        sys.exit(1)
    
    print()
    print("✓ Database initialization complete!")
    sys.exit(0)
