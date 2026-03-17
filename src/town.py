"""
Town class - Generates random postal codes and town names.

@author  Arturo Mora-Rioja
@version 1.0.0 March 2023
"""
import random
from src.db import DB


class Town(DB):
    """Class to get random towns and postal codes from database."""
    
    _town_count = 0
    
    def __init__(self):
        """
        Constructor initializes database connection.
        The total number of towns is saved as a class variable.
        By making it a class variable, the calculation is made only once.
        """
        super().__init__()
        if Town._town_count == 0:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT COUNT(*) AS total FROM postal_code"
            cursor.execute(sql)
            result = cursor.fetchone()
            Town._town_count = result['total']
            cursor.close()
    
    def get_random_town(self) -> dict:
        """
        Generates a random postal code and town
        based on the values in the addresses database.
        
        @return dict with keys 'postal_code' and 'town_name'
        """
        random_town = random.randint(0, Town._town_count - 1)
        cursor = self.connection.cursor(dictionary=True)
        sql = f"""
            SELECT cPostalCode AS postal_code, cTownName AS town_name
            FROM postal_code
            LIMIT {random_town}, 1
        """
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result
