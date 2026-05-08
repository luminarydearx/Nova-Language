"""Test suite untuk Nova Parser"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nova.lexer.lexer import Lexer
from nova.parser.parser import Parser


def test_parse_var_declaration():
    """Test parsing var declaration"""
    code = "var x = 10"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert not parser.has_errors(), f"Parser errors: {parser.get_errors()}"
    assert len(ast.statements) == 1
    print("✓ test_parse_var_declaration passed")


def test_parse_print():
    """Test parsing print statement"""
    code = 'print("Hello")'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert not parser.has_errors(), f"Parser errors: {parser.get_errors()}"
    assert len(ast.statements) == 1
    print("✓ test_parse_print passed")


def test_parse_if_statement():
    """Test parsing if statement"""
    code = """
    if (true) {
        print("yes")
    }
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert not parser.has_errors(), f"Parser errors: {parser.get_errors()}"
    print("✓ test_parse_if_statement passed")


def test_parse_function():
    """Test parsing function declaration"""
    code = """
    func add(a, b) {
        return a + b
    }
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert not parser.has_errors(), f"Parser errors: {parser.get_errors()}"
    print("✓ test_parse_function passed")


if __name__ == "__main__":
    test_parse_var_declaration()
    test_parse_print()
    test_parse_if_statement()
    test_parse_function()
    print("\n✅ All Parser tests passed!")
