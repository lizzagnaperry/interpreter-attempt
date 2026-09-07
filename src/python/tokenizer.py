from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Any, Generator
from string import digits

#class to make tokentype to represent whether its an integer, + operator, - operator
class TokenType(StrEnum):
    INT = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()

@dataclass #to represent all tokens
class Token:
    type : TokenType
    value: Any=None

#class called Tokenizer to accept code strings
class Tokenizer:
    def __init__(self, code:str) -> None:
        self.code = code
        self.ptr: int = 0  #remember girly the ptr tracks current location in source code

    #method to tokenize
    def next_token(self) -> Token:
        #skips whitespace
        while self.ptr < len(self.code) and self.code[self.ptr]==" ":
            self.ptr+=1

        if self.ptr ==len(self.code):
            return Token(TokenType.EOF)

        #registers and logs which tokentype is for each character
        char = self.code[self.ptr]

        #for multi digit numbers aka will keep consuming digits while they last
        if char in digits:
            start = self.ptr
            while self.ptr < len(self.code) and self.code[self.ptr] in digits:
                self.ptr += 1
            number_str = self.code[start:self.ptr]
            return Token(TokenType.INT, int(number_str))

        self.ptr += 1
        if char == "+":
            return Token(TokenType.PLUS)
        elif char == "-":
            return Token(TokenType.MINUS)
        elif char == "*":
            return Token(TokenType.STAR)
        elif char == "/":
            return Token(TokenType.SLASH)
        elif char == "(":
            return Token(TokenType.LPAREN)
        elif char == ")":
            return Token(TokenType.RPAREN)
        else:
            raise RuntimeError(f"Can't tokenize {char!r}.")

    #makes it iterable so we can loop through tokens directly
    def __iter__(self) -> Generator[Token, None, None]:
        while (token := self.next_token()).type != TokenType.EOF:
            yield token
        yield token #yield the eof token too



if __name__ == "__main__":
    code= "12 + 345 - (6 * 7) / 2"
    tokenizer = Tokenizer(code)
    print(code)
    for tok in tokenizer:
        print(f"\t{tok.type}, {tok.value}")
