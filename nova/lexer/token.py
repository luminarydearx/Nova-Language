"""Token class for Nova-Language2 (equivalent to Java Token record)"""
from dataclasses import dataclass
from .token_types import TokenType

@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: object  # Can be int, float, str, bool, None
    line: int

    def __repr__(self):
        return f"Token({self.type}, '{self.lexeme}', {self.literal}, line {self.line})"