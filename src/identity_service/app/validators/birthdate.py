from datetime import date
from .base_validator import BaseValidator


class BirthdateValidator(BaseValidator):
    """
    Validator for birthdate. User must be over 18 years old.
    """
    def validate(self, birthdate: date) -> date:
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if age < 18:
            raise ValueError("User must be over 18 years old.")
        return birthdate
