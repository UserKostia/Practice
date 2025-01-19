from typing import List

from .base_validator import BaseValidator


class UsernameValidator(BaseValidator):
    """
    Validator for username. User username must be at least 3 characters long and less than 40 characters long.
    """

    def __init__(self):
        self.rules = [
            self._validate_length,
        ]

    def validate(self, username: str) -> str:
        """
        Function for validation username for each rule.

        :param username:
        :return: str
        """

        # Eist for errors in username.
        errors: List[str] = []

        # Check username for every rule. If found error add it to error list.
        for rule in self.rules:
            try:
                rule(username)
            except ValueError as e:
                errors.append(str(e))
        if errors:
            raise ValueError("Username errors: " + "; ".join(errors))

        return username

    @staticmethod
    def _validate_length(username: str) -> None:
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        if len(username) > 40:
            raise ValueError("Username must be less than 40 characters long.")
