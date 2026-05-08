"""NovaInterface for Nova-Language2"""
from typing import Set, List


class NovaInterface:
    """Represents a Nova interface"""
    def __init__(self, name: str, required_methods: Set[str], parent_interfaces: List[str]):
        self.name = name
        self.required_methods = required_methods
        self.parent_interfaces = parent_interfaces

    def check_implemented_by(self, nova_class):
        """Check if a class properly implements this interface"""
        missing = []
        for method_name in self.required_methods:
            if method_name not in nova_class.methods:
                missing.append(method_name)
        
        if missing:
            raise Exception(f"Class '{nova_class.name}' does not implement interface '{self.name}'. "
                          f"Missing methods: {', '.join(missing)}")
        
        # Check parent interfaces recursively
        for parent_name in self.parent_interfaces:
            # This would need access to the interpreter's environment
            # For now, just pass
            pass

    def __str__(self):
        return f"<interface {self.name}>"