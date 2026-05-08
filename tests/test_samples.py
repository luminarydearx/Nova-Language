"""
Test runner untuk file .nova di tests/samples/
Jalankan setiap file dan verifikasi output-nya
"""

import sys
import os
sys.path.insert(0, '.')

from nova.lexer.lexer import Lexer
from nova.parser.parser import Parser
from nova.interpreter.interpreter import Interpreter


def run_nova_file(path: str) -> list:
    """Jalankan file .nova dan kembalikan output"""
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Lexing
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parsing
    parser = Parser(tokens)
    ast = parser.parse()
    
    if parser.has_errors():
        raise Exception(f"Parser errors in {path}: {parser.get_errors()}")
    
    # Interpret
    interpreter = Interpreter()
    return interpreter.interpret(ast)


def test_hello():
    """Test hello.nova"""
    print("Testing hello.nova...")
    output = run_nova_file('tests/samples/hello.nova')
    expected = ["Hello from Nova Language v2.0!"]
    assert output == expected, f"Expected {expected}, got {output}"
    print("✓ hello.nova passed")


def test_arithmetic():
    """Test arithmetic.nova"""
    print("Testing arithmetic.nova...")
    output = run_nova_file('tests/samples/arithmetic.nova')
    # Output harusnya: ["30", "10", "200", "0.5"]
    assert len(output) == 4, f"Expected 4 outputs, got {len(output)}: {output}"
    assert "30" in str(output[0]), f"Expected 30, got {output[0]}"
    assert "10" in str(output[1]), f"Expected 10, got {output[1]}"
    print("✓ arithmetic.nova passed")


def test_scope():
    """Test scope_test.nova"""
    print("Testing scope_test.nova...")
    output = run_nova_file('tests/samples/scope_test.nova')
    # Output harusnya: ["local", "global"]
    assert len(output) == 2, f"Expected 2 outputs, got {len(output)}: {output}"
    assert output[0] == "local", f"Expected 'local', got {output[0]}"
    assert output[1] == "global", f"Expected 'global', got {output[1]}"
    print("✓ scope_test.nova passed")


if __name__ == "__main__":
    print("=" * 60)
    print("Running Nova Language v2.0 Sample Tests")
    print("=" * 60)
    
    try:
        test_hello()
        test_arithmetic()
        test_scope()
        
        print("\n" + "=" * 60)
        print("✅ All Sample Tests Passed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
