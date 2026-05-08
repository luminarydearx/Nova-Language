"""
Module System untuk Nova Language
Memungkinkan import file .nova lain
"""

import os
from typing import Optional


def load_module(module_name: str, current_dir: str, interpreter) -> None:
    """
    Load dan eksekusi module Nova.
    
    Args:
        module_name: Nama file (misal: 'utils.nova' atau 'utils')
        current_dir: Direktori file yang sedang dieksekusi (untuk relatif path)
        interpreter: Instance Interpreter utama (untuk share scope)
    """
    # Cari file .nova
    if not module_name.endswith('.nova'):
        module_name += '.nova'
    
    # Cek di direktori saat ini atau path absolut
    paths_to_try = [
        os.path.join(current_dir, module_name),
        module_name  # absolute path
    ]
    
    module_path = None
    for path in paths_to_try:
        if os.path.exists(path):
            module_path = path
            break
    
    if not module_path:
        raise Exception(f"Module '{module_name}' tidak ditemukan")
    
    # Baca file
    with open(module_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Lexing & Parsing
    from ..lexer.lexer import Lexer
    from ..parser.parser import Parser
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    if parser.has_errors():
        raise Exception(f"Module load error: {parser.get_errors()}")
    
    # Eksekusi dalam interpreter yang sama (share scope)
    interpreter._visit(ast)
