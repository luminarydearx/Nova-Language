"""NovaCallable and NovaFunction for Nova-Language2"""
from typing import List, Optional, Callable, Any
from ..parser.ast.nodes import FunctionDeclNode, BlockNode


class NovaCallable:
    """Base class for callable objects (functions, methods, classes)"""
    def call(self, interpreter, args: List[Any]) -> Any:
        raise NotImplementedError

    def arity(self) -> int:
        raise NotImplementedError

    def __str__(self):
        return "<callable>"


class NovaFunction(NovaCallable):
    """Represents a Nova-Language2 function"""
    def __init__(self, name: Optional[str], params: List[str],
                 param_types: List[Optional[str]], return_type: Optional[str],
                 body: Optional[BlockNode], closure: Any, is_abstract: bool = False,
                 native_fn: Optional[Callable] = None):
        self.name = name or "<anonymous>"
        self.params = params
        self.param_types = param_types
        self.return_type = return_type
        self.body = body
        self.closure = closure
        self.is_abstract = is_abstract
        self.native_fn = native_fn  # For built-in/native functions

    def call(self, interpreter, args: List[Any]) -> Any:
        if self.is_abstract:
            raise Exception(f"Abstract method '{self.name}' not implemented")

        if self.native_fn:
            # Native/built-in function
            return self.native_fn(interpreter, args)

        # User-defined function
        if len(args) != len(self.params):
            raise Exception(f"Function '{self.name}' expects {len(self.params)} arguments, got {len(args)}")

        # Create new environment with closure as parent
        env = interpreter.env.__class__(self.closure)

        # Bind parameters
        for i, param in enumerate(self.params):
            env.define(param, args[i])

        # Execute function body
        previous_env = interpreter.env
        interpreter.env = env

        try:
            interpreter.execute_block(self.body, env)
        except ReturnSignal as ret:
            return ret.value
        finally:
            interpreter.env = previous_env

        return None

    def arity(self) -> int:
        return len(self.params)

    def __str__(self):
        return f"<function {self.name}>"