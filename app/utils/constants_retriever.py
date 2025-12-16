import yaml 
from typing import Any
from .singleton_handler import SingletonClass


class ConstantsRetriever(metaclass=SingletonClass):

    with open("../config/constants.yaml", 'r') as file:
            constants = yaml.safe_load(file)


    @classmethod
    def get_constants(cls, name: str) -> Any:
        return cls.constants[name]