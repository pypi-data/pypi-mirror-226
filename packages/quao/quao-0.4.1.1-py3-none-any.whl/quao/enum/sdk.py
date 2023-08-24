"""
    QuaO Project sdk.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from enum import Enum


class Sdk(Enum):
    QISKIT = 'qiskit'
    BRAKET = 'braket'
    TYTAN = 'tytan'

    @staticmethod
    def resolve_sdk(sdk_type: str):
        for element in Sdk:
            if element.value.__eq__(sdk_type):
                return element

        raise Exception("sdk not supported!")
