"""Test suite untuk Nova Interpreter - Updated untuk struktur baru"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nova.lexer.lexer import Lexer
from nova.parser.parser import Parser
from nova.interpreter.interpreter import Interpreter, ReturnException, NovaRuntimeException


def run_nova_code(code: str) -> list:
    """Helper: Jalankan kode Nova dan kembalikan output"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    if parser.has_errors():
        raise Exception(f"Parser errors: {parser.get_errors()}")
    
    interpreter = Interpreter()
    return interpreter.interpret(ast)


def test_print_literal():
    """Test print literal string"""
    code = 'print("Hello Nova")'
    output = run_nova_code(code)
    assert output == ["Hello Nova"], f"Expected ['Hello Nova'], got {output}"
    print("✓ test_print_literal passed")


def test_var_and_print():
    """Test var declaration dan print"""
    code = """
    var x = 42
    print(x)
    """
    output = run_nova_code(code)
    assert any("42" in str(o) for o in output), f"Expected 42 in output, got {output}"
    print("✓ test_var_and_print passed")


def test_arithmetic():
    """Test operasi aritmatika"""
    code = """
    var a = 10
    var b = 5
    print(a + b)
    print(a - b)
    """
    output = run_nova_code(code)
    assert any("15" in str(o) for o in output), f"Expected 15 in output, got {output}"
    assert any("5" in str(o) for o in output), f"Expected 5 in output, got {output}"
    print("✓ test_arithmetic passed")


def test_scope():
    """Test lingkup variabel (scope)"""
    code = """
    var x = "global"
    {
        var x = "local"
        print(x)
    }
    print(x)
    """
    output = run_nova_code(code)
    assert any("local" in str(o) for o in output), f"Expected 'local' in output, got {output}"
    assert any("global" in str(o) for o in output), f"Expected 'global' in output, got {output}"
    print("✓ test_scope passed")


def test_symbol_table():
    """Test symbol table functionality"""
    from nova.symbol_table import SymbolTable, ScopeStack
    
    scope = ScopeStack()
    scope.define("x", "int", 10, False, "public")
    
    info = scope.resolve("x")
    assert info is not None, "Symbol 'x' harus ditemukan"
    assert info.value == 10, f"Expected 10, got {info.value}"
    assert info.var_type == "int", f"Expected 'int', got {info.var_type}"
    print("✓ test_symbol_table passed")


def test_const_folding():
    """Test constant folding (2 + 3 langsung jadi 5)"""
    code = """
    var x = 2 + 3
    print(x)
    """
    output = run_nova_code(code)
    assert any("5" in str(o) for o in output), f"Expected 5 in output, got {output}"
    print("✓ test_const_folding passed")


if __name__ == "__main__":
    print("=" * 50)
    print("Running Nova Language v2.0 Tests")
    print("=" * 50)
    
    test_print_literal()
    test_var_and_print()
    test_arithmetic()
    test_scope()
    test_symbol_table()
    test_const_folding()
    
    print("\n" + "=" * 50)
    print("✅ All Interpreter tests passed!")
    print("=" * 50)
