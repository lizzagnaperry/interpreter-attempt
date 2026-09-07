from python.parser import Parser
from python.parser import BinOp, Int
from python.tokenizer import Token, TokenType, Tokenizer

def test_parsing_addition():
    tokens = [
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 5),
        Token(TokenType.EOF),
    ]
    tree = Parser(tokens).parse()
    assert tree == BinOp(
        "+",
        Int(3),
        Int(5),
    )

def test_parsing_subtraction():
    tokens = [
        Token(TokenType.INT, 5),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 2),
        Token(TokenType.EOF),
    ]
    tree = Parser(tokens).parse()
    assert tree == BinOp(
        "-",
        Int(5),
        Int(2),
    )

def test_parsing_chained_addition_and_subtraction_is_left_associative():
    tree = Parser(list(Tokenizer("1 + 2 - 3"))).parse()
    assert tree == BinOp(
        "-",
        BinOp("+", Int(1), Int(2)),
        Int(3),
    )
 
def test_parsing_multiplication_binds_tighter_than_addition():
    tree = Parser(list(Tokenizer("2 + 3 * 4"))).parse()
    assert tree == BinOp(
        "+",
        Int(2),
        BinOp("*", Int(3), Int(4)),
    )
 
def test_parsing_multiplication_binds_tighter_on_the_left():
    tree = Parser(list(Tokenizer("2 * 3 + 4"))).parse()
    assert tree == BinOp(
        "+",
        BinOp("*", Int(2), Int(3)),
        Int(4),
    )
 

def test_parsing_chained_multiplication_and_division():
    tree = Parser(list(Tokenizer("8 / 4 * 2"))).parse()
    assert tree == BinOp(
        "*",
        BinOp("/", Int(8), Int(4)),
        Int(2),
    )
 

def test_parsing_parens_override_precedence():
    tree = Parser(list(Tokenizer("(2 + 3) * 4"))).parse()
    assert tree == BinOp(
        "*",
        BinOp("+", Int(2), Int(3)),
        Int(4),
    )
 
def test_parsing_nested_parens():
    tree = Parser(list(Tokenizer("((1 + 2))"))).parse()
    assert tree == BinOp("+", Int(1), Int(2))
 

def test_parsing_multi_digit_numbers():
    tree = Parser(list(Tokenizer("123 + 45"))).parse()
    assert tree == BinOp("+", Int(123), Int(45))