from dataclasses import dataclass
from typing import Any
from typing import Generator
from enum import auto, StrEnum
from .parser import BinOp
from .parser import TreeNode
from .parser import Int


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

    #uses treenodes and makes the bytecode ops recursively
    #a node can be just an int or a binop whose left or rigjt are trees
    #that need compiling first since the VM needs both operands pushed before it sees operator
    def compile(self) -> Generator[Bytecode, None, None]:
        yield from self._compile_node(self.tree)
 
    def _compile_node(self, node: TreeNode) -> Generator[Bytecode, None, None]:
        if isinstance(node, Int):
            yield Bytecode(BytecodeType.PUSH, node.value)
            return
 
        if isinstance(node, BinOp):
            # compile the left first -- if it's itself a binop,
            # recurses and emits ITS pushes/binop before
            # continuing, so by the time we get back here the left
            # result is sitting on top of the stack
            yield from self._compile_node(node.left)
            yield from self._compile_node(node.right)
            yield Bytecode(BytecodeType.BINOP, node.op)
            return
 
        raise RuntimeError(f"Don't know how to compile {node!r}.")


#testiinnggggggg
if __name__ == "__main__":
    from .tokenizer import Tokenizer
    from .parser import Parser

    compiler = Compiler(Parser(list(Tokenizer("3 + 5 - 2 * (4 - 1)"))).parse())
    for bc in compiler.compile():
        print(bc)