from abc import ABC, abstractmethod


class BaseValidator(ABC):
    @abstractmethod
    def validate(self, value):
        """
        Checking the value. Must be implemented in the child class.
        """
        pass
