from python.tokenizer import Tokenizer
from python.parser import Parser
from python.compiler import Compiler
from python.interpreter import Interpreter

import pytest

@pytest.mark.parametrize(
    ["code", "result"],
    [
        ("3 + 5", 8),
        ("5 - 2", 3),
        ("1 + 2", 3),
        ("1 - 9", -8),
        ("4 * 6", 24),
        ("10 / 2", 5),
        ("7 / 2", 3),
        ("100 + 23", 123),
        ("999 - 1", 998),
        ("1 + 2 + 3 + 4", 10),
        ("20 - 5 - 3", 12),
        ("2 + 3 * 4", 14),
        ("2 * 3 + 4", 10),
        ("(2 + 3) * 4", 20),
        ("2 * (3 + 4)", 14),
        ("100 + 23 * 2 - (10 / 2)", 141),
    ],
)
def test_simple_arithmetic(code: str, result: int):
    tokens = list(Tokenizer(code))
    tree = Parser(tokens).parse()
    bytecode = list(Compiler(tree).compile())
    interpreter = Interpreter(bytecode)
    interpreter.interpret()
    assert interpreter.stack.pop() == result

def test_division_by_zero_raises():
    tokens = list(Tokenizer("5 / 0"))
    tree = Parser(tokens).parse()
    bytecode = list(Compiler(tree).compile())
    interpreter = Interpreter(bytecode)
    with pytest.raises(ZeroDivisionError):
        interpreter.interpret()