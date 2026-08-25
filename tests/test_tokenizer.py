from tokenizer import Token, Tokenizer, TokenType
import pytest

#test addition
def test_tokenizer_addition(): 
    tokens = list(Tokenizer("3 + 5"))
    assert tokens == [
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 5),
        Token(TokenType.EOF),
    ]

#test subtraction
def test_tokenizer_subtraction(): 
    tokens = list(Tokenizer("3 - 6"))
    assert tokens == [
        Token(TokenType.INT, 3),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 6),
        Token(TokenType.EOF),
    ]

#testing both same time
def test_tokenizer_additions_and_subtractions():
    tokens = list(Tokenizer("1 + 2 + 3 + 4 - 5 - 6 + 7 - 8"))
    assert tokens == [
        Token(TokenType.INT, 1),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 2),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 4),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 5),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 6),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 7),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 8),
        Token(TokenType.EOF),
    ]

#testing both addition and subtraction along woth withspace
def test_tokenizer_additions_and_subtractions_with_whitespace():
    tokens = list(Tokenizer("     1+       2   +3+4-5  -   6 + 7  - 8        "))
    assert tokens == [
        Token(TokenType.INT, 1),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 2),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 3),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 4),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 5),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 6),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 7),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 8),
        Token(TokenType.EOF),
    ]

#testing on some bullshittttt so the tokenizer will raise an error if theres somehting it doesnt know how to toeknize
def test_tokenizer_raises_error_on_garbage():
    with pytest.raises(RuntimeError):
        list(Tokenizer("$"))

#so tokenizer can recognise each token type seperately
def tokenizer_recognises_each_token(code: str, token: Token):
    tokens = list(Tokenizer(code))
    assert tokens == [token, Token(TokenType.EOF)]

def test_tokenizer_knows_plus():
    tokenizer_recognises_each_token("+", Token(TokenType.PLUS))

def test_tokenizer_knows_minus():
    tokenizer_recognises_each_token("-", Token(TokenType.MINUS))

def test_tokenizer_knows_integer():
    tokenizer_recognises_each_token("3", Token(TokenType.INT, 3))