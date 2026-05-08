"""Environment for Nova-Language2 - handles variable scoping"""
from typing import Dict, Optional, Any


class Environment:
    def __init__(self, enclosing: Optional['Environment'] = None):
        self.values: Dict[str, Any] = {}
        self.constants: set = set()  # Track constant variables
        self.enclosing = enclosing

    def define(self, name: str, value: Any, is_const: bool = False):
        """Define a variable in current scope"""
        self.values[name] = value
        if is_const:
            self.constants.add(name)

    def get(self, name: str) -> Any:
        """Get variable value by name"""
        if name in self.values:
            return self.values[name]
        elif self.enclosing is not None:
            return self.enclosing.get(name)
        else:
            raise NovaRuntimeError(f"Undefined variable '{name}'")

    def assign(self, name: str, value: Any):
        """Assign new value to existing variable"""
        if name in self.values:
            if name in self.constants:
                raise NovaRuntimeError(f"Cannot reassign constant '{name}'")
            self.values[name] = value
        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
        else:
            raise NovaRuntimeError(f"Undefined variable '{name}'")

    def is_defined(self, name: str) -> bool:
        """Check if variable is defined in any scope"""
        if name in self.values:
            return True
        elif self.enclosing is not None:
            return self.enclosing.is_defined(name)
        return False


# =================== CUSTOM EXCEPTIONS ===================
class NovaRuntimeError(Exception):
    """Runtime error in Nova-Language2"""
    pass


class ReturnSignal(Exception):
    """Signal to return from function"""
    def __init__(self, value: Any = None):
        self.value = value


class BreakSignal(Exception):
    """Signal for break statement"""
    pass


class ContinueSignal(Exception):
    """Signal for continue statement"""
    pass


class NovaException(Exception):
    """User-thrown exception"""
    def __init__(self, thrown: Any):
        self.thrown = thrown