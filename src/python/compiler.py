from dataclasses import dataclass
from typing import Any
from enum import auto, StrEnum


class BytecodeType(StrEnum):
    BINOP = auto() #type for binary ops
    PUSH = auto() # type to push values on stack

#class for bytecode operations
@dataclass
class Bytecode:
    type: BytecodeType
    value: Any = None
