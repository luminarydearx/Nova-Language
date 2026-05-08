"""Constant folding implementation for Nova-Language."""
from nova.ast.nodes import NumberNode, BinaryOpNode, UnaryOpNode
from nova.type_inference.inference import TypeInferer

class ConstantFolder:
    """Fold constant expressions into single values."""
    
    def __init__(self):
        self.inferer = TypeInferer()
    
    def fold(self, node):
        """Return folded node if possible, otherwise original node."""
        method_name = f'fold_{type(node).__name__}'
        method = getattr(self, method_name, lambda n: n)
        return method(node)
    
    def fold_BinaryOpNode(self, node):
        # Fold left and right first
        left = self.fold(node.left)
        right = self.fold(node.right)
        
        # If both are numbers, fold them
        if isinstance(left, NumberNode) and isinstance(right, NumberNode):
            if node.op == '+':
                return NumberNode(left.value + right.value)
            elif node.op == '-':
                return NumberNode(left.value - right.value)
            elif node.op == '*':
                return NumberNode(left.value * right.value)
            elif node.op == '/':
                return NumberNode(left.value / right.value)
        
        # Return new node with folded children
        return BinaryOpNode(node.op, left, right)
    
    def fold_UnaryOpNode(self, node):
        operand = self.fold(node.operand)
        if isinstance(operand, NumberNode):
            if node.op == '-':
                return NumberNode(-operand.value)
        return UnaryOpNode(node.op, operand)
