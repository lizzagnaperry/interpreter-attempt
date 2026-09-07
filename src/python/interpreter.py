from .compiler import Bytecode, BytecodeType



#make stack to keep track of our calculations
class Stack:
    def __init__(self) -> None:
        self.stack: list[int] = []

    def push(self, item: int) -> None:
        self.stack.append(item)

    def pop(self) -> int:
        return self.stack.pop()

    def peek(self) -> int:
        return self.stack[-1]

    def __repr__(self) -> str:
        return f"Stack({self.stack})"

#accepts a list of bytecode operations 
#and will go through list of bytecodes 
#to interpret one at a timne
class Interpreter:
    def __init__(self, bytecode: list[Bytecode]) -> None:
        self.stack = Stack()
        self.bytecode = bytecode
        self.ptr: int = 0

    #will check which bytecode its looking at and then perform the op it implements
    def interpret(self) -> None:
        for bc in self.bytecode:
            if bc.type == BytecodeType.PUSH:
                self.stack.push(bc.value)
            elif bc.type == BytecodeType.BINOP:
                right = self.stack.pop()
                left = self.stack.pop()
                if bc.value == "+":
                    result = left + right
                elif bc.value == "-":
                    result = left - right
                elif bc.value == "*":
                    result = left * right
                elif bc.value == "/":
                    #integer division, since our language only has ints
                    result = left // right
                else:
                    raise RuntimeError(f"Unknown operator {bc.value}.")
                self.stack.push(result)

        print("Done!")
        print(self.stack)


#testing again
if __name__ == "__main__":
    import sys

    from .tokenizer import Tokenizer
    from .parser import Parser
    from .compiler import Compiler

    code = sys.argv[1]
    tokens = list(Tokenizer(code))
    tree = Parser(tokens).parse()
    bytecode = list(Compiler(tree).compile())
    Interpreter(bytecode).interpret()