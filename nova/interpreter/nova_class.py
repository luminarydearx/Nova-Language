"""NovaClass and NovaInstance for Nova-Language2"""
from typing import Dict, List, Optional, Any
from .nova_callable import NovaCallable, NovaFunction


class NovaInstance:
    """Instance of a Nova class"""
    def __init__(self, klass: 'NovaClass'):
        self.klass = klass
        self.fields: Dict[str, Any] = {}

    def get(self, name: str, interpreter=None) -> Any:
        """Get a property or method"""
        if name in self.fields:
            return self.fields[name]

        # Look in class methods
        if name in self.klass.methods:
            method = self.klass.methods[name]
            return method

        raise Exception(f"Undefined property '{name}' on instance of '{self.klass.name}'")

    def set(self, name: str, value: Any):
        """Set a field value"""
        self.fields[name] = value

    def __str__(self):
        # Call toString if available
        if "toString" in self.klass.methods:
            # This would need interpreter context to call properly
            return f"<{self.klass.name} instance>"
        return f"<{self.klass.name} instance>"


class NovaClass(NovaCallable):
    """Represents a Nova class"""
    def __init__(self, name: str, methods: Dict[str, NovaCallable],
                 superclass: Optional['NovaClass'] = None,
                 is_abstract: bool = False,
                 interface_names: List[str] = None,
                 fields: list = None):
        self.name = name
        self.methods = methods
        self.superclass = superclass
        self.is_abstract = is_abstract
        self.interface_names = interface_names or []
        self.field_declarations = fields or []

    def call(self, interpreter, args: List[Any]) -> NovaInstance:
        """Instantiate the class (called when class is called like a function)"""
        instance = NovaInstance(self)

        # Call init if exists
        if "init" in self.methods:
            init_method = self.methods["init"]
            # Push this instance to stack
            interpreter.this_stack.append(instance)
            try:
                init_method.call(interpreter, args)
            finally:
                interpreter.this_stack.pop()

        return instance

    def get_method(self, name: str) -> Optional[NovaCallable]:
        """Get method by name, checking superclass if needed"""
        if name in self.methods:
            return self.methods[name]
        if self.superclass:
            return self.superclass.get_method(name)
        return None

    def arity(self) -> int:
        """Return arity of init method, or 0 if no init"""
        if "init" in self.methods:
            return self.methods["init"].arity()
        return 0

    def __str__(self):
        return f"<class {self.name}>"