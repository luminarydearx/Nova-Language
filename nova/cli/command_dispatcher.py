"""CommandDispatcher for Nova-Language2 - equivalent to Java CommandDispatcher"""
import sys
import os
from typing import List, Dict, Callable
from ..lexer.lexer import Lexer
from ..lexer.token import Token
from ..parser.parser import Parser
from ..interpreter.interpreter import Interpreter
from ..interpreter.environment import NovaRuntimeError
from .nova_console import NovaConsole


class CommandDispatcher:
    """Dispatch CLI commands for Nova-Language2"""
    
    COMMANDS = {
        "help": "Show this help message",
        "version": "Show Nova-Language version",
        "run": "Run a Nova source file",
        "repl": "Start interactive REPL mode",
        "tokenize": "Tokenize a source file (debug)",
        "parse": "Parse a source file and show AST (debug)",
    }

    @classmethod
    def dispatch(cls, command: str, args: List[str]) -> int:
        """Dispatch command to appropriate handler"""
        command = command.lower()
        
        if command == "help" or command == "--help" or command == "-h":
            return cls._help()
        elif command == "version" or command == "--version" or command == "-v":
            return cls._version()
        elif command == "run":
            return cls._run(args)
        elif command == "repl":
            return cls._repl()
        elif command == "tokenize":
            return cls._tokenize(args)
        elif command == "parse":
            return cls._parse(args)
        else:
            NovaConsole.error(f"Unknown command: {command}")
            NovaConsole.info("Run 'nova help' to see available commands.")
            return 1

    @classmethod
    def _help(cls) -> int:
        """Show help message"""
        NovaConsole.print_logo()
        print()
        print(NovaConsole.bold("Available Commands:"))
        print()
        for cmd, desc in cls.COMMANDS.items():
            print(f"  {NovaConsole.cyan(cmd):<15} {desc}")
        print()
        print(f"Usage: nova <command> [arguments]")
        print(f"Example: nova {NovaConsole.cyan('run')} hello.nova")
        return 0

    @classmethod
    def _version(cls) -> int:
        """Show version info"""
        NovaConsole.print_logo()
        print()
        print(f"Nova-Language2 {NovaConsole.cyan('0.5.7')} (Python Port)")
        print("Original Java version by LuminaryVoid (luminarydearx)")
        print("Python port by Hermes Agent")
        return 0

    @classmethod
    def _run(cls, args: List[str]) -> int:
        """Run a Nova source file"""
        if not args:
            NovaConsole.error("No file specified.")
            print(f"Usage: nova {NovaConsole.cyan('run')} <file.nova>")
            return 1
        
        filepath = args[0]
        if not os.path.exists(filepath):
            NovaConsole.error(f"File not found: {filepath}")
            return 1
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Tokenize
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            if lexer.has_errors():
                NovaConsole.error("Lexer errors:")
                for err in lexer.get_errors():
                    print(f"  {err}")
                return 1
            
            # Parse
            parser = Parser(tokens)
            program = parser.parse()
            
            if parser.has_errors():
                NovaConsole.error("Parser errors:")
                for err in parser.get_errors():
                    print(f"  {err}")
                return 1
            
            # Interpret
            interpreter = Interpreter()
            interpreter.execute(program)
            
            return 0
            
        except FileNotFoundError:
            NovaConsole.error(f"File not found: {filepath}")
            return 1
        except Exception as e:
            NovaConsole.error(f"Runtime error: {str(e)}")
            return 1

    @classmethod
    def _repl(cls) -> int:
        """Start interactive REPL mode"""
        NovaConsole.print_logo()
        print(NovaConsole.bold("\nInteractive Nova REPL (Python Port)"))
        print("Type 'exit' or press Ctrl+C to quit.\n")
        
        interpreter = Interpreter()
        
        while True:
            try:
                line = input(NovaConsole.cyan("nova> "))
                if line.strip() in ('exit', 'quit'):
                    print("Goodbye!")
                    break
                
                if not line.strip():
                    continue
                
                # Tokenize
                lexer = Lexer(line)
                tokens = lexer.tokenize()
                
                if lexer.has_errors():
                    for err in lexer.get_errors():
                        print(f"Error: {err}")
                    continue
                
                # Parse
                parser = Parser(tokens)
                program = parser.parse()
                
                if parser.has_errors():
                    for err in parser.get_errors():
                        print(f"Error: {err}")
                    continue
                
                # Interpret
                interpreter.execute(program)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
        
        return 0

    @classmethod
    def _tokenize(cls, args: List[str]) -> int:
        """Tokenize a source file (debug mode)"""
        if not args:
            NovaConsole.error("No file specified.")
            return 1
        
        filepath = args[0]
        if not os.path.exists(filepath):
            NovaConsole.error(f"File not found: {filepath}")
            return 1
        
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        print(NovaConsole.bold(f"Tokens ({len(tokens)} total):"))
        print()
        for i, token in enumerate(tokens):
            print(f"{i:3d}. {token}")
        
        if lexer.has_errors():
            print()
            NovaConsole.error("Errors:")
            for err in lexer.get_errors():
                print(f"  {err}")
            return 1
        
        return 0

    @classmethod
    def _parse(cls, args: List[str]) -> int:
        """Parse a source file and show AST (debug mode)"""
        if not args:
            NovaConsole.error("No file specified.")
            return 1
        
        filepath = args[0]
        if not os.path.exists(filepath):
            NovaConsole.error(f"File not found: {filepath}")
            return 1
        
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        if lexer.has_errors():
            NovaConsole.error("Lexer errors:")
            for err in lexer.get_errors():
                print(f"  {err}")
            return 1
        
        parser = Parser(tokens)
        program = parser.parse()
        
        print(NovaConsole.bold("AST (Abstract Syntax Tree):"))
        print()
        print(program)
        
        if parser.has_errors():
            print()
            NovaConsole.error("Parser errors:")
            for err in parser.get_errors():
                print(f"  {err}")
            return 1
        
        return 0