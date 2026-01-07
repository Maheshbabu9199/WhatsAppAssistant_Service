from pathlib import Path
from typing import Any

import yaml


class ConstantsRetriever:
    path = Path(__file__).parent.parent.parent / "app" / "config" / "constants.yaml"

    with open(path, "r") as file:
        constants = yaml.safe_load(file)

    @classmethod
    def get_constants(cls, name: str) -> Any:
        return cls.constants[name]
