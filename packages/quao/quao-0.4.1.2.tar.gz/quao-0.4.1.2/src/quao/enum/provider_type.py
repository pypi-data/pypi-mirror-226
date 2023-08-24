"""
    QuaO Project ProviderType.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from enum import Enum


class ProviderType(Enum):
    QUAO_QUANTUM_SIMULATOR = 'QUAO_QUANTUM_SIMULATOR'
    IBM_QUANTUM = 'IBM_QUANTUM'
    IBM_CLOUD = 'IBM_CLOUD'
    AWS_BRAKET = 'AWS_BRAKET'

    @staticmethod
    def resolve_provider_type(provider_type: str):
        for element in ProviderType:
            if element.value.__eq__(provider_type):
                return element

        raise Exception("provider not supported!")
