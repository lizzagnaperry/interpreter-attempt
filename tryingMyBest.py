from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Any

class TokenType(StrEnum):
    INT = auto()
    PLUS = auto()