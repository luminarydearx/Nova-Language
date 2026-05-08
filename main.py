#!/usr/bin/env python3
"""
Nova Language v2.0 - Main Entry Point
Jalankan file .nova dari command line
"""

import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.nova>")
        print("       python main.py examples/hello.nova")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' tidak ditemukan.")
        sys.exit(1)
    
    try:
        # Baca file
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Lexing
        from nova.lexer.lexer import Lexer
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Parsing
        from nova.parser.parser import Parser
        parser = Parser(tokens)
        ast = parser.parse()
        
        if parser.has_errors():
            print("Parser errors:")
            for error in parser.get_errors():
                print(f"  {error}")
            sys.exit(1)
        
        # Interpretation
        from nova.interpreter.interpreter import Interpreter
        interpreter = Interpreter()
        output = interpreter.interpret(ast)
        
        # Tampilkan output
        for line in output:
            print(line)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
