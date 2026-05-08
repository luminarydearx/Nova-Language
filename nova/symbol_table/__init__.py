from typing import Dict, Any, Optional, List

class SymbolInfo:
    def __init__(self, name: str, var_type: str, value: Any, is_const: bool, visibility: str):
        self.name = name
        self.var_type = var_type  # "int", "string", "bool", etc.
        self.value = value
        self.is_const = is_const
        self.visibility = visibility  # "public", "private", "protected"

    def __repr__(self):
        return f"SymbolInfo(name={self.name}, type={self.var_type}, value={self.value}, const={self.is_const}, vis={self.visibility})"


class SymbolTable:
    """Tabel simbol untuk satu lingkup (scope)"""
    def __init__(self, parent: Optional['SymbolTable'] = None):
        self.symbols: Dict[str, SymbolInfo] = {}
        self.parent = parent  # untuk nested scope

    def define(self, name: str, var_type: str, value: Any, is_const: bool, visibility: str):
        if name in self.symbols:
            raise Exception(f"Variabel '{name}' sudah didefinisikan di lingkup ini")
        self.symbols[name] = SymbolInfo(name, var_type, value, is_const, visibility)

    def resolve(self, name: str) -> Optional[SymbolInfo]:
        """Cari simbol dari lingkup terkini ke atas (global)"""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.resolve(name)
        return None

    def assign(self, name: str, value: Any):
        """Update nilai variabel"""
        info = self.resolve(name)
        if not info:
            raise Exception(f"Variabel '{name}' tidak ditemukan")
        if info.is_const:
            raise Exception(f"Cannot assign to constant '{name}'")
        # Type checking sederhana
        if info.var_type == "int" and not isinstance(value, (int, float)):
            raise Exception(f"Tipe salah: {name} bertipe int, diberi {type(value)}")
        info.value = value

    def __repr__(self):
        return f"SymbolTable({len(self.symbols)} symbols, parent={'yes' if self.parent else 'no'})"


class ScopeStack:
    """Manajemen tumpukan lingkup (scope)"""
    def __init__(self):
        self.stack: List[SymbolTable] = [SymbolTable()]  # global scope di dasar

    def push(self, table: Optional[SymbolTable] = None):
        """Masuk ke lingkup baru"""
        if table is None:
            table = SymbolTable(parent=self.current())
        self.stack.append(table)

    def pop(self) -> SymbolTable:
        """Keluar dari lingkup terkini"""
        if len(self.stack) <= 1:
            raise Exception("Tidak bisa pop global scope")
        return self.stack.pop()

    def current(self) -> SymbolTable:
        return self.stack[-1]

    def define(self, name: str, var_type: str, value: Any, is_const: bool, visibility: str):
        self.current().define(name, var_type, value, is_const, visibility)

    def resolve(self, name: str) -> Optional[SymbolInfo]:
        return self.current().resolve(name)

    def assign(self, name: str, value: Any):
        self.current().assign(name, value)

    def __repr__(self):
        return f"ScopeStack(depth={len(self.stack)})"
