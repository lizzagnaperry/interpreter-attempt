from python.compiler import Bytecode, BytecodeType, Compiler
from python.parser import BinOp, Int

def test_compile_addition():
    tree = BinOp(
        "+",
        Int(3),
        Int(5),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 3),
        Bytecode(BytecodeType.PUSH, 5),
        Bytecode(BytecodeType.BINOP, "+"),
    ]

def test_compile_subtraction():
    tree = BinOp(
        "-",
        Int(5),
        Int(2),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 5),
        Bytecode(BytecodeType.PUSH, 2),
        Bytecode(BytecodeType.BINOP, "-"),
    ]

def test_compile_multiplication():
    tree = BinOp("*", Int(4), Int(6))
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 4),
        Bytecode(BytecodeType.PUSH, 6),
        Bytecode(BytecodeType.BINOP, "*"),
    ]
 
def test_compile_division():
    tree = BinOp("/", Int(10), Int(2))
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 10),
        Bytecode(BytecodeType.PUSH, 2),
        Bytecode(BytecodeType.BINOP, "/"),
    ]

def test_compile_nested_binop_on_the_right():
    tree = BinOp(
        "+",
        Int(1),
        BinOp("*", Int(2), Int(3)),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 1),
        Bytecode(BytecodeType.PUSH, 2),
        Bytecode(BytecodeType.PUSH, 3),
        Bytecode(BytecodeType.BINOP, "*"),
        Bytecode(BytecodeType.BINOP, "+"),
    ]

def test_compile_nested_binop_on_the_left():
    tree = BinOp(
        "+",
        BinOp("-", Int(1), Int(2)),
        Int(3),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 1),
        Bytecode(BytecodeType.PUSH, 2),
        Bytecode(BytecodeType.BINOP, "-"),
        Bytecode(BytecodeType.PUSH, 3),
        Bytecode(BytecodeType.BINOP, "+"),
    ]

def test_compile_nested_binop_on_both_sides():
    tree = BinOp(
        "*",
        BinOp("+", Int(1), Int(2)),
        BinOp("-", Int(3), Int(4)),
    )
    bytecode = list(Compiler(tree).compile())
    assert bytecode == [
        Bytecode(BytecodeType.PUSH, 1),
        Bytecode(BytecodeType.PUSH, 2),
        Bytecode(BytecodeType.BINOP, "+"),
        Bytecode(BytecodeType.PUSH, 3),
        Bytecode(BytecodeType.PUSH, 4),
        Bytecode(BytecodeType.BINOP, "-"),
        Bytecode(BytecodeType.BINOP, "*"),
    ]