#!/usr/bin/env python3
"""
Nova Language v2.0 - Main Entry Point
Usage:
    nova <file.nova>        # Run file
    nova -i                 # Interactive REPL
    nova --version          # Show version
    nova --help             # Show help
"""

import sys
import os
import readline  # Untuk input history di REPL

__version__ = "2.0.0"

def show_logo():
    from nova.cli.nova_console import NovaConsole
    NovaConsole.print_logo()

def show_help():
    print(f"""Nova Language v{__version__}

Usage:
    nova <file.nova>        Run a .nova file
    nova -i, --interactive  Start interactive REPL
    nova -v, --version      Show version
    nova -h, --help         Show this help

Examples:
    nova examples/hello.nova
    nova -i
    """)

def run_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' tidak ditemukan.")
        sys.exit(1)
    
    try:
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

def start_repl():
    from nova.interpreter.interpreter import Interpreter
    from nova.lexer.lexer import Lexer
    from nova.parser.parser import Parser
    
    show_logo()
    print("Tipe 'exit()' atau Ctrl+D untuk keluar.\n")
    
    interpreter = Interpreter()
    
    while True:
        try:
            line = input(">>> " if not hasattr(start_repl, 'multiline') else "... ")
            if line.strip() == "":
                continue
            if line.strip() in ('exit()', 'quit()'):
                break
            
            # Lexing & Parsing
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            
            if parser.has_errors():
                for error in parser.get_errors():
                    print(f"  {error}")
                continue
            
            # Interpret
            output = interpreter.interpret(ast)
            for out in output:
                print(out)
                
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar dari Nova REPL.")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    args = sys.argv[1:]
    
    if not args or args[0] in ('-h', '--help'):
        show_help()
        sys.exit(0)
    
    if args[0] in ('-v', '--version'):
        print(f"Nova Language v{__version__}")
        sys.exit(0)
    
    if args[0] in ('-i', '--interactive'):
        start_repl()
        sys.exit(0)
    
    # Asumsi argumen pertama adalah file .nova
    run_file(args[0])

if __name__ == "__main__":
    main()
