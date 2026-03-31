"""
DB class - Encapsulates a connection to the database.

@author  Arturo Mora-Rioja
@version 1.0.0 August 2020
@version 2.0.0 March 2026 Adaptation to Docker
@converted by Asger Bergøe to Python from the original PHP implementation by Arturo Mora-Rioja
@version 2.0.0 March 2026 Adaptation to Docker
"""
import mysql.connector
from mysql.connector import Error
from src.info import Info


class DB:
    """Database connection class using MySQL connector."""
    
    def __init__(self):
        """Opens a connection to the database."""
        try:
            self.connection = mysql.connector.connect(
                host=Info.host(),
                database=Info.db_name(),
                user=Info.user(),
                password=Info.password(),
                charset='utf8'
            )
        except Error as e:
            print('Connection unsuccessful')
            raise Exception(f'Connection unsuccessful: {e}')
    
    def __del__(self):
        """Closes a connection to the database."""
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
    
    def get_connection(self):
        """Returns the database connection."""
        return self.connection
