"""Type inference implementation for Nova-Language."""
from nova.ast.nodes import NumberNode, StringNode, BooleanNode, VariableNode, BinaryOpNode

class TypeInferer:
    """Infer types of expressions in Nova-Language."""
    
    def infer(self, node):
        """Return the inferred type of an AST node."""
        method_name = f'infer_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_infer)
        return method(node)
    
    def generic_infer(self, node):
        return 'unknown'
    
    def infer_NumberNode(self, node):
        return 'int' if isinstance(node.value, int) else 'float'
    
    def infer_StringNode(self, node):
        return 'string'
    
    def infer_BooleanNode(self, node):
        return 'boolean'
    
    def infer_VariableNode(self, node):
        # In real implementation, this would look up the symbol table
        return 'unknown'  # Placeholder
    
    def infer_BinaryOpNode(self, node):
        left_type = self.infer(node.left)
        right_type = self.infer(node.right)
        
        # Simple type promotion rules
        if left_type == 'float' or right_type == 'float':
            return 'float'
        elif left_type == 'int' and right_type == 'int':
            return 'int'
        else:
            return 'unknown'
