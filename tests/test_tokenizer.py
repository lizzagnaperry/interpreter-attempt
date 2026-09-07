import pytest
from python.tokenizer import Token, Tokenizer, TokenType

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

#testing star and slash alongside plus/minus
def test_tokenizer_all_four_operators():
    tokens = list(Tokenizer("2 + 3 - 4 * 5 / 6"))
    assert tokens == [
        Token(TokenType.INT, 2),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 3),
        Token(TokenType.MINUS),
        Token(TokenType.INT, 4),
        Token(TokenType.STAR),
        Token(TokenType.INT, 5),
        Token(TokenType.SLASH),
        Token(TokenType.INT, 6),
        Token(TokenType.EOF),
    ]
 
#testing parens around an expression
def test_tokenizer_parens():
    tokens = list(Tokenizer("(1 + 2) * 3"))
    assert tokens == [
        Token(TokenType.LPAREN),
        Token(TokenType.INT, 1),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 2),
        Token(TokenType.RPAREN),
        Token(TokenType.STAR),
        Token(TokenType.INT, 3),
        Token(TokenType.EOF),
    ]
 
#testing nested parens
def test_tokenizer_nested_parens():
    tokens = list(Tokenizer("((1))"))
    assert tokens == [
        Token(TokenType.LPAREN),
        Token(TokenType.LPAREN),
        Token(TokenType.INT, 1),
        Token(TokenType.RPAREN),
        Token(TokenType.RPAREN),
        Token(TokenType.EOF),
    ]

#testing on some bullshittttt so the tokenizer will raise an error if theres somehting it doesnt know how to toeknize
def test_tokenizer_raises_error_on_garbage():
    with pytest.raises(RuntimeError):
        list(Tokenizer("$"))

#so tokenizer can recognise each token type seperately
@pytest.mark.parametrize(
    ["code", "token"],
    [
        ("+", Token(TokenType.PLUS)),
        ("-", Token(TokenType.MINUS)),
        ("*", Token(TokenType.STAR)),
        ("/", Token(TokenType.SLASH)),
        ("(", Token(TokenType.LPAREN)),
        (")", Token(TokenType.RPAREN)),
        ("3", Token(TokenType.INT, 3)),
    ],
)
def test_tokenizer_recognises_each_token(code: str, token: Token):
    tokens = list(Tokenizer(code))
    assert tokens == [token, Token(TokenType.EOF)]

#tesing multi-digit numbers should tokenize as a single INT, not
#one token per digit like i did before whoops
@pytest.mark.parametrize(
    ["code", "value"],
    [
        ("7", 7),
        ("42", 42),
        ("100", 100),
        ("123456", 123456),
    ],
)
def test_tokenizer_multi_digit_numbers(code: str, value: int):
    tokens = list(Tokenizer(code))
    assert tokens == [Token(TokenType.INT, value), Token(TokenType.EOF)]
 
#makes sure two multi-digit numbers next to an operator don't
#accidentally get merged or split wrong
def test_tokenizer_multi_digit_numbers_with_operator():
    tokens = list(Tokenizer("123 + 45"))
    assert tokens == [
        Token(TokenType.INT, 123),
        Token(TokenType.PLUS),
        Token(TokenType.INT, 45),
        Token(TokenType.EOF),
    ]

