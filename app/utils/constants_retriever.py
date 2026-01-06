import yaml 
from typing import Any
from .singleton_handler import SingletonClass
from pathlib import Path


class ConstantsRetriever:

    path = Path(__file__).parent.parent.parent / "app" /"config" / "constants.yaml"

    with open(path, 'r') as file:
        constants = yaml.safe_load(file)


    @classmethod
    def getConstants(cls, name: str) -> Any:
        return cls.constants[name]
    


