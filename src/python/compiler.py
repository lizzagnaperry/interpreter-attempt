from dataclasses import dataclass
from typing import Any
from typing import Generator
from enum import auto, StrEnum
from .parser import BinOp


class BytecodeType(StrEnum):
    BINOP = auto() #type for binary ops
    PUSH = auto() # type to push values on stack

#class for bytecode operations
@dataclass
class Bytecode:
    type: BytecodeType
    value: Any = None

#will produce bytecode ops
class Compiler:
    def __init__(self, tree: BinOp) -> None:
        self.tree = tree

    #uses treenodes and makes the bytecode ops
    def compile(self) -> Generator[Bytecode, None, None]:
        left = self.tree.left
        yield Bytecode(BytecodeType.PUSH, left.value)

        right = self.tree.right
        yield Bytecode(BytecodeType.PUSH, right.value)

        yield Bytecode(BytecodeType.BINOP, self.tree.op)

#testiinnggggggg
if __name__ == "__main__":
    from .tokenizer import Tokenizer
    from .parser import Parser

    compiler = Compiler(Parser(list(Tokenizer("3 + 5"))).parse())
    for bc in compiler.compile():
        print(bc)