from typing import List
from .base_validator import BaseValidator


class PasswordValidator(BaseValidator):
    """
    Password validator.
     Password must be at least 8 characters long,
     contain at least one digit,
     one uppercase letter.
    """

    def __init__(self):
        self.rules = [
            self._validate_length,
            self._validate_digit,
            self._validate_uppercase
        ]

    def validate(self, password: str) -> str:
        """
        Function for validation password for each rule.

        :param password:
        :return: str
        """

        # Eist for errors in password.
        errors: List[str] = []

        # Check password for every rule. If found error add it to error list.
        for rule in self.rules:
            try:
                rule(password)
            except ValueError as e:
                errors.append(str(e))
        if errors:
            raise ValueError("Password errors: " + "; ".join(errors))

        return password

    @staticmethod
    def _validate_length(password: str) -> None:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

    @staticmethod
    def _validate_digit(password: str) -> None:
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit.")

    @staticmethod
    def _validate_uppercase(password: str) -> None:
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter.")
