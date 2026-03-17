"""
Configuration class for database connection settings.
Reads from environment variables with fallback to defaults.
"""
import os


class Info:
    HOST = 'localhost'
    DB_NAME = 'addresses'
    USER = 'root'
    PASSWORD = ''

    @staticmethod
    def host() -> str:
        return os.getenv('DB_HOST', Info.HOST)

    @staticmethod
    def db_name() -> str:
        return os.getenv('DB_NAME', Info.DB_NAME)

    @staticmethod
    def user() -> str:
        return os.getenv('DB_USER', Info.USER)

    @staticmethod
    def password() -> str:
        value = os.getenv('DB_PASSWORD')
        return value if value is not None else Info.PASSWORD
