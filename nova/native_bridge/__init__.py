from typing import Callable, Any, List

class NativeFunction:
    """Representasi fungsi native Python yang bisa dipanggil dari Nova"""
    def __init__(self, name: str, arity: int, callable: Callable):
        self.name = name
        self.arity = arity  # jumlah parameter wajib (-1 berarti variadic)
        self.callable = callable
    
    def call(self, args: List[Any]) -> Any:
        """Panggil fungsi Python dengan argumen yang diberikan"""
        if self.arity != -1 and len(args) != self.arity:
            raise Exception(f"Native function '{self.name}' expects {self.arity} args, got {len(args)}")
        return self.callable(*args)
    
    def __repr__(self):
        return f"<native fn '{self.name}'>"
