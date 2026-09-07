from dataclasses import dataclass
from .tokenizer import TokenType, Token


#class for the nodes of the trees
@dataclass
class TreeNode:
    pass

#subclass for addition and subtraction akak the binary operations
#left and right are treenodes cuz either side of a binop could be another binop
@dataclass
class BinOp(TreeNode):
    op: str
    left: "TreeNode"
    right: "TreeNode"

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

    #parses the whole program
    def parse(self) -> TreeNode:
        tree = self.parse_expression()
        self.eat(TokenType.EOF)
        return tree

    #lowest precedence: + and -
    #parses one term, then keeps folding in more +/- terms as long as
    #they appear, building left chain of the binosp
    def parse_expression(self) -> TreeNode:
        left = self.parse_term()
 
        while self.peek() in (TokenType.PLUS, TokenType.MINUS):
            if self.peek() == TokenType.PLUS:
                op = "+"
                self.eat(TokenType.PLUS)
            else:
                op = "-"
                self.eat(TokenType.MINUS)
 
            right = self.parse_term()
            left = BinOp(op, left, right)
 
        return left

    #higher precedence: * and /
    #works on factors instead of terms
    #"2 + 3 * 4" makes binds the * tighter than the +
    def parse_term(self) -> TreeNode:
        left = self.parse_factor()
 
        while self.peek() in (TokenType.STAR, TokenType.SLASH):
            if self.peek() == TokenType.STAR:
                op = "*"
                self.eat(TokenType.STAR)
            else:
                op = "/"
                self.eat(TokenType.SLASH)
 
            right = self.parse_factor()
            left = BinOp(op, left, right)
 
        return left

    #highest precedence: a single number, or a parenthesized expression
    #the parens let you "reset" back to the top of the precedence chain,
    #lets "(2 + 3) * 4" overrides normal precedence
    def parse_factor(self) -> TreeNode:
        if self.peek() == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
 
        token = self.eat(TokenType.INT)
        return Int(token.value)


#testinggggg
if __name__ == "__main__":
    from src.python.tokenizer import Tokenizer

    code = "3 + 5 - 2 * (4 - 1)"
    parser = Parser(list(Tokenizer(code)))
    print(parser.parse())