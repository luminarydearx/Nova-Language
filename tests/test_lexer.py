"""Test suite untuk Nova Lexer"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nova.lexer.lexer import Lexer
from nova.lexer.token_types import TokenType


def test_basic_tokens():
    """Test tokenisasi dasar"""
    code = "var x = 10"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Filter token penting (bukan EOF/NEWLINE)
    important_tokens = [t for t in tokens if t.type not in (TokenType.EOF, TokenType.NEWLINE)]
    
    assert len(important_tokens) >= 3
    assert important_tokens[0].type == TokenType.KW_VAR
    assert important_tokens[1].type == TokenType.IDENTIFIER
    assert important_tokens[1].lexeme == "x"
    print("✓ test_basic_tokens passed")


def test_string_literal():
    """Test string literal"""
    code = 'print("Hello Nova")'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    string_tokens = [t for t in tokens if t.type == TokenType.STRING]
    assert len(string_tokens) == 1
    assert string_tokens[0].literal == "Hello Nova"
    print("✓ test_string_literal passed")


def test_number_literal():
    """Test number literal"""
    code = "var num = 42"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    number_tokens = [t for t in tokens if t.type == TokenType.NUMBER]
    assert len(number_tokens) == 1
    assert number_tokens[0].literal == 42
    print("✓ test_number_literal passed")


def test_operators():
    """Test operator tokens"""
    code = "a + b - c * d / e"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    operators = [t for t in tokens if t.type in (TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH)]
    assert len(operators) == 4
    print("✓ test_operators passed")


if __name__ == "__main__":
    test_basic_tokens()
    test_string_literal()
    test_number_literal()
    test_operators()
    print("\n✅ All Lexer tests passed!")
