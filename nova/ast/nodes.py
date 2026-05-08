from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Any


@dataclass(frozen=True)
class Node(ABC):
    """Base class for all AST nodes"""
    # line info removed for simplicity - not provided by current parser
    
    @abstractmethod
    def __repr__(self):
        pass


# --- Statement Nodes ---
@dataclass(frozen=True)
class ProgramNode(Node):
    statements: List[Node]

    def __repr__(self):
        return f"ProgramNode({len(self.statements)} stmts)"


@dataclass(frozen=True)
class BlockNode(Node):
    statements: List[Node]

    def __repr__(self):
        return f"BlockNode({len(self.statements)} stmts)"


@dataclass(frozen=True)
class PrintNode(Node):
    expression: 'ExprNode'

    def __repr__(self):
        return f"PrintNode({self.expression})"


@dataclass(frozen=True)
class VarDeclNode(Node):
    visibility: str  # public, private, protected
    name: str
    is_const: bool
    type_annotation: Optional[str]
    initializer: Optional['ExprNode']

    def __repr__(self):
        return f"VarDeclNode({self.visibility} {self.name}: {self.type_annotation} = {self.initializer})"


@dataclass(frozen=True)
class FunctionDeclNode(Node):
    visibility: str
    is_abstract: bool
    name: str
    params: List[str]
    param_types: List[Optional[str]]
    return_type: Optional[str]
    body: Optional[BlockNode]

    def __repr__(self):
        return f"FunctionDeclNode({self.visibility} {self.name}({len(self.params)} params))"


@dataclass(frozen=True)
class ClassDeclNode(Node):
    name: str
    super_name: Optional[str]
    interface_names: List[str]
    is_abstract: bool
    fields: List[VarDeclNode]
    methods: List[FunctionDeclNode]

    def __repr__(self):
        return f"ClassDeclNode(class {self.name})"


@dataclass(frozen=True)
class InterfaceDeclNode(Node):
    name: str
    parent_interfaces: List[str]
    method_signatures: List['InterfaceMethodSig']

    def __repr__(self):
        return f"InterfaceDeclNode(interface {self.name})"


@dataclass(frozen=True)
class InterfaceMethodSig(Node):
    name: str
    params: List[str]
    return_type: Optional[str]

    def __repr__(self):
        return f"InterfaceMethodSig({self.name}({len(self.params)} params))"


@dataclass(frozen=True)
class EnumDeclNode(Node):
    name: str
    values: List[str]

    def __repr__(self):
        return f"EnumDeclNode(enum {self.name})"


@dataclass(frozen=True)
class StructDeclNode(Node):
    name: str
    fields: List['StructField']

    def __repr__(self):
        return f"StructDeclNode(struct {self.name})"


@dataclass(frozen=True)
class StructField(Node):
    name: str
    type_annotation: Optional[str]

    def __repr__(self):
        return f"StructField({self.name}: {self.type_annotation})"


# --- Control Flow Nodes ---
@dataclass(frozen=True)
class IfNode(Node):
    condition: 'ExprNode'
    then_branch: BlockNode
    else_branch: Optional[BlockNode]

    def __repr__(self):
        return f"IfNode({self.condition})"


@dataclass(frozen=True)
class WhileNode(Node):
    condition: 'ExprNode'
    body: BlockNode

    def __repr__(self):
        return f"WhileNode({self.condition})"


@dataclass(frozen=True)
class DoWhileNode(Node):
    body: BlockNode
    condition: 'ExprNode'

    def __repr__(self):
        return f"DoWhileNode({self.condition})"


@dataclass(frozen=True)
class ForNode(Node):
    initializer: Optional[Node]
    condition: Optional['ExprNode']
    increment: Optional['ExprNode']
    body: BlockNode

    def __repr__(self):
        return f"ForNode({self.condition})"


@dataclass(frozen=True)
class ReturnNode(Node):
    value: Optional['ExprNode']

    def __repr__(self):
        return f"ReturnNode({self.value})"


@dataclass(frozen=True)
class BreakNode(Node):
    def __repr__(self):
        return "BreakNode()"


@dataclass(frozen=True)
class ContinueNode(Node):
    def __repr__(self):
        return "ContinueNode()"


# --- Try-Catch Nodes ---
@dataclass(frozen=True)
class TryCatchNode(Node):
    try_block: BlockNode
    catch_blocks: List[tuple]  # (exception_type, variable, block)
    finally_block: Optional[BlockNode]

    def __repr__(self):
        return f"TryCatchNode({len(self.catch_blocks)} catches)"


@dataclass(frozen=True)
class ThrowNode(Node):
    expression: 'ExprNode'

    def __repr__(self):
        return f"ThrowNode({self.expression})"


# --- Expression Nodes ---
@dataclass(frozen=True)
class ExprNode(Node):
    """Base class for expression nodes"""
    pass


@dataclass(frozen=True)
class LiteralExpr(ExprNode):
    value: Any  # int, float, str, bool, None

    def __repr__(self):
        return f"LiteralExpr({self.value})"


@dataclass(frozen=True)
class VariableExpr(ExprNode):
    name: str

    def __repr__(self):
        return f"VariableExpr({self.name})"


@dataclass(frozen=True)
class BinaryExpr(ExprNode):
    left: ExprNode
    operator: str  # Token lexeme
    right: ExprNode

    def __repr__(self):
        return f"BinaryExpr({self.left} {self.operator} {self.right})"


@dataclass(frozen=True)
class UnaryExpr(ExprNode):
    operator: str
    operand: ExprNode

    def __repr__(self):
        return f"UnaryExpr({self.operator}{self.operand})"


@dataclass(frozen=True)
class CallExpr(ExprNode):
    callee: ExprNode
    arguments: List[ExprNode]

    def __repr__(self):
        return f"CallExpr({self.callee}({len(self.arguments)} args))"


@dataclass(frozen=True)
class GetExpr(ExprNode):
    object: ExprNode
    property: str

    def __repr__(self):
        return f"GetExpr({self.object}.{self.property})"


@dataclass(frozen=True)
class SetExpr(ExprNode):
    object: ExprNode
    property: str
    value: ExprNode

    def __repr__(self):
        return f"SetExpr({self.object}.{self.property} = {self.value})"


@dataclass(frozen=True)
class ThisExpr(ExprNode):
    def __repr__(self):
        return "ThisExpr()"


@dataclass(frozen=True)
class SuperExpr(ExprNode):
    method: str

    def __repr__(self):
        return f"SuperExpr(super.{self.method})"


@dataclass(frozen=True)
class ArrayExpr(ExprNode):
    elements: List[ExprNode]

    def __repr__(self):
        return f"ArrayExpr({len(self.elements)} elements)"


@dataclass(frozen=True)
class ExprStmtNode(Node):
    expression: ExprNode

    def __repr__(self):
        return f"ExprStmtNode({self.expression})"