"""
    QuaO Project base_enum.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from enum import Enum


class BaseEnum(Enum):
    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

    @staticmethod
    def resolve(provider_type: str):
        for element in BaseEnum:
            if element.value.__eq__(provider_type):
                return element

        raise Exception("Enum type is not supported!")
