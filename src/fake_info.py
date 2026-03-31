"""
FakeInfo class - Generates information about fake persons.

@author  Arturo Mora-Rioja
@version 1.0.0 March 2023
@converted by Asger Bergøe to Python from the original PHP implementation by Arturo Mora-Rioja
@version 2.0.0 March 2026 Adaptation to Docker

"""
import json
import random
from datetime import datetime
from src.town import Town


class FakeInfo:
    """Class to generate fake person information."""
    
    GENDER_FEMININE = 'female'
    GENDER_MASCULINE = 'male'
    FILE_PERSON_NAMES = 'data/person-names.json'
    PHONE_PREFIXES = [
        '2', '30', '31', '40', '41', '42', '50', '51', '52', '53', '60', '61', '71', '81', '91', '92', '93', '342',
        '344', '345', '346', '347', '348', '349', '356', '357', '359', '362', '365', '366', '389', '398', '431',
        '441', '462', '466', '468', '472', '474', '476', '478', '485', '486', '488', '489', '493', '494', '495',
        '496', '498', '499', '542', '543', '545', '551', '552', '556', '571', '572', '573', '574', '577', '579',
        '584', '586', '587', '589', '597', '598', '627', '629', '641', '649', '658', '662', '663', '664', '665',
        '667', '692', '693', '694', '697', '771', '772', '782', '783', '785', '786', '788', '789', '826', '827', '829'
    ]
    MIN_BULK_PERSONS = 2
    MAX_BULK_PERSONS = 100

    def __init__(self):
        """Initialize FakeInfo with generated fake person data."""
        self.cpr = None
        self.first_name = None
        self.last_name = None
        self.gender = None
        self.birth_date = None
        self.address = {}
        self.phone = None
        
        self._set_full_name_and_gender()
        self._set_birth_date()
        self._set_cpr()
        self._set_address()
        self._set_phone()
    
    def _set_cpr(self) -> None:
        """
        Generates a fake CPR based on the existing birth date and gender.
        - If no birth date exists, it generates it.
        - If no first name, last name or gender exists, it generates them.
        """
        if self.birth_date is None:
            self._set_birth_date()
        if self.first_name is None or self.last_name is None or self.gender is None:
            self._set_full_name_and_gender()
        
        # The CPR must end in an even number for females, odd for males
        final_digit = random.randint(0, 9)
        if self.gender == self.GENDER_FEMININE:
            # Ensure even for females
            if final_digit % 2 == 1:
                final_digit -= 1
        else:
            # Ensure odd for males
            if final_digit % 2 == 0:
                final_digit += 1
        
        self.cpr = (
            self.birth_date[8:10] +
            self.birth_date[5:7] +
            self.birth_date[2:4] +
            str(self._get_random_digit()) +
            str(self._get_random_digit()) +
            str(self._get_random_digit()) +
            str(final_digit)
        )
    
    def _set_birth_date(self) -> None:
        """Generates a fake date of birth from 1900 to the present year."""
        year = random.randint(1900, datetime.now().year)
        month = random.randint(1, 12)
        
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:
            # Leap years are not taken into account to avoid complexity
            day = random.randint(1, 28)
        
        self.birth_date = f"{year:04d}-{month:02d}-{day:02d}"
    
    def _set_full_name_and_gender(self) -> None:
        """
        Generates a fake full name and gender.
        The generation consists in extracting them randomly from the person's JSON file.
        """
        with open(self.FILE_PERSON_NAMES, 'r', encoding='utf-8') as f:
            names = json.load(f)
        
        person = random.choice(names['persons'])
        self.first_name = person['firstName']
        self.last_name = person['lastName']
        self.gender = person['gender']
    
    def _set_address(self) -> None:
        """Generates a fake Danish address."""
        self.address['street'] = self._get_random_text(40)
        
        self.address['number'] = str(random.randint(1, 999))
        # Approx. 20% of Danish addresses includes a letter
        if random.randint(1, 10) < 3:
            self.address['number'] += self._get_random_text(1, False).upper()
        
        # Approx. 30% of Danish addresses are on the ground floor
        if random.randint(1, 10) < 4:
            self.address['floor'] = 'st'
        else:
            self.address['floor'] = random.randint(1, 99)
        
        # The door will be randomly generated based on the following distribution:
        # 1-7     35% th
        # 8-14    35% tv
        # 15-16   10% mf
        # 17-18   10% 1-50
        # 19      5% lowercase_letter + 1-999
        # 20      5% lowercase letter + '-' + 1-999
        door_type = random.randint(1, 20)
        if door_type < 8:
            self.address['door'] = 'th'
        elif door_type < 15:
            self.address['door'] = 'tv'
        elif door_type < 17:
            self.address['door'] = 'mf'
        elif door_type < 19:
            self.address['door'] = random.randint(1, 50)
        else:
            lower_case_letters = [
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ø', 'æ', 'å'
            ]
            self.address['door'] = random.choice(lower_case_letters)
            if door_type == 20:
                self.address['door'] += '-'
            self.address['door'] += str(random.randint(1, 999))
        
        # Postal code and town
        town = Town()
        town_data = town.get_random_town()
        self.address['postal_code'] = town_data['postal_code']
        self.address['town_name'] = town_data['town_name']
    
    @staticmethod
    def _get_random_text(length: int = 1, include_danish_characters: bool = True) -> str:
        """
        Returns a random text.
        Only alphabetic characters and the space are allowed.
        
        @param length: Length of the text to return (1 by default)
        @param include_danish_characters: Whether to include Danish characters
        @return str: The random text
        """
        valid_characters = [
            ' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z'
        ]
        if include_danish_characters:
            valid_characters.extend(['æ', 'ø', 'å', 'Æ', 'Ø', 'Å'])
        
        # The first character is chosen from position 1 to avoid the space
        text = random.choice(valid_characters[1:])
        for _ in range(1, length):
            text += random.choice(valid_characters)
        return text
    
    def _set_phone(self) -> None:
        """
        Generates a fake Danish phone number.
        The phone number must start with a prefix in PHONE_PREFIXES.
        """
        phone = random.choice(self.PHONE_PREFIXES)
        prefix_length = len(phone)
        for _ in range(8 - prefix_length):
            phone += str(self._get_random_digit())
        
        self.phone = phone
    
    def get_cpr(self) -> str:
        """
        Returns a fake CPR.
        @return str: The fake CPR
        """
        return self.cpr
    
    def get_full_name_and_gender(self) -> dict:
        """
        Returns a fake full name and gender.
        @return dict: ['firstName' => value, 'lastName' => value, 'gender' => 'female' | 'male']
        """
        return {
            'firstName': self.first_name,
            'lastName': self.last_name,
            'gender': self.gender
        }
    
    def get_full_name_gender_and_birth_date(self) -> dict:
        """
        Returns a fake full name, gender, and birth date.
        @return dict: ['firstName' => value, 'lastName' => value, 'gender' => 'female' | 'male', 'birthDate' => value]
        """
        return {
            'firstName': self.first_name,
            'lastName': self.last_name,
            'gender': self.gender,
            'birthDate': self.birth_date
        }
    
    def get_cpr_full_name_and_gender(self) -> dict:
        """
        Returns a fake CPR, full name, and gender.
        @return dict: ['CPR' => value, 'firstName' => value, 'lastName' => value, 'gender' => 'female' | 'male']
        """
        return {
            'CPR': self.cpr,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'gender': self.gender
        }
    
    def get_cpr_full_name_gender_and_birth_date(self) -> dict:
        """
        Returns a fake CPR, full name, gender, and birth date.
        @return dict: ['CPR' => value, 'firstName' => value, 'lastName' => value, 'gender' => 'female' | 'male', 'birthDate' => value]
        """
        return {
            'CPR': self.cpr,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'gender': self.gender,
            'birthDate': self.birth_date
        }
    
    def get_address(self) -> dict:
        """
        Returns a fake Danish address.
        @return dict: ['address' => dict with address details]
        """
        return {'address': self.address}
    
    def get_phone_number(self) -> str:
        """
        Returns a fake Danish phone number.
        @return str: The fake phone number
        """
        return self.phone
    
    def get_fake_person(self) -> dict:
        """
        Returns fake person information.
        @return dict: ['CPR' => value, 'firstName' => value, 'lastName' => value, 
                       'gender' => 'female'|'male', 'birthDate' => value, 'phoneNumber' => value]
        """
        return {
            'CPR': self.cpr,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'gender': self.gender,
            'birthDate': self.birth_date,
            'address': self.address,
            'phoneNumber': self.phone
        }
    
    def get_fake_persons(self, amount: int = None) -> list:
        """
        Returns information about several fake persons.
        @param amount: The number of fake persons to generate, between 2 and 100 inclusive
        @return list: List of fake person information
        """
        if amount is None:
            amount = self.MIN_BULK_PERSONS
        if amount < self.MIN_BULK_PERSONS:
            amount = self.MIN_BULK_PERSONS
        if amount > self.MAX_BULK_PERSONS:
            amount = self.MAX_BULK_PERSONS
        
        bulk_info = []
        for _ in range(amount):
            fake_info = FakeInfo()
            bulk_info.append(fake_info.get_fake_person())
        return bulk_info
    
    @staticmethod
    def _get_random_digit() -> int:
        """
        Generates a random digit.
        @return int: The randomly generated digit
        """
        return random.randint(0, 9)
