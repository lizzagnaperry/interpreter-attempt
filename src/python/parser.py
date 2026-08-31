from dataclasses import dataclass
from .tokenizer import TokenType, Token


#class for the nodes of the trees
@dataclass
class TreeNode:
    pass

#subclass for addition and subtraction akak the binary operations
@dataclass
class BinOp(TreeNode):
    op: str
    left: "Int"
    right: "Int"

#nodetype for the integers
@dataclass
class Int(TreeNode):
    value: int

#deifning parser
class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.next_token_index: int = 0
        #it points to the next token to be consumed C:

    #returns next token if expected type, if not then error raised
    def eat(self, expected_token_type: TokenType) -> Token:
        next_token = self.tokens[self.next_token_index]
        self.next_token_index += 1
        if next_token.type != expected_token_type:
            raise RuntimeError(f"Expected {expected_token_type}, ate {next_token!r}.")
        return next_token

    #checks type of next token without consuming it
    def peek(self, skip: int = 0) -> TokenType | None:
        peek_at = self.next_token_index + skip
        return self.tokens[peek_at].type if peek_at < len(self.tokens) else None

    #parses the program
    def parse(self) -> BinOp:
        #if parsing + and - then need to have integers
        left_op = self.eat(TokenType.INT)

        #if we have + or -
        if self.peek() == TokenType.PLUS:
            op = "+"
            self.eat(TokenType.PLUS)
        else:
            op = "-"
            self.eat(TokenType.MINUS)

        #after eating op token we can expect a new int
        right_op = self.eat(TokenType.INT)

        self.eat(TokenType.EOF)

        #return and build tree node
        return BinOp(op, Int(left_op.value), Int(right_op.value))

#testinggggg
if __name__ == "__main__":
    from src.python.tokenizer import Tokenizer

    code = "3 + 5"
    parser = Parser(list(Tokenizer(code)))
    print(parser.parse())

    # BinOp(op='+', left=Int(value=3), right=Int(value=5))