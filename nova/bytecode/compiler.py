"""
Bytecode Compiler untuk Nova Language
Mengubah AST menjadi daftar instruksi bytecode
"""

from dataclasses import dataclass
from typing import List, Any

from ..ast.nodes import (
    ProgramNode, BlockNode, PrintNode, VarDeclNode, FunctionDeclNode,
    IfNode, WhileNode, DoWhileNode, ReturnNode, ExprStmtNode,
    LiteralExpr, VariableExpr, BinaryExpr, UnaryExpr,
    CallExpr, GetExpr, SetExpr, ThisExpr, ArrayExpr, TryCatchNode, ThrowNode
)


@dataclass
class Instruction:
    """Satu instruksi bytecode"""
    op: str  # Nama opcode: LOAD_CONST, ADD, STORE_VAR, PRINT, dll.
    arg: Any = None  # Argumen opsional
    line: int = 0  # Untuk debugging

    def __repr__(self):
        if self.arg is not None:
            return f"{self.op} {repr(self.arg)}"
        return self.op


class Compiler:
    """Compiler dari AST ke Bytecode"""

    def __init__(self):
        self.instructions: List[Instruction] = []
        self.constants: List[Any] = []  # Pool konstanta

    def compile(self, node) -> List[Instruction]:
        """Compile AST menjadi bytecode"""
        self._visit(node)
        return self.instructions

    def _visit(self, node):
        """Visitor pattern dispatcher"""
        method_name = f"_compile_{type(node).__name__}"
        visitor = getattr(self, method_name, self._visit_generic)
        return visitor(node)

    def _visit_generic(self, node):
        raise Exception(f"Tidak ada compiler visitor untuk node: {type(node).__name__}")

    # ===== Program & Block =====
    def _compile_ProgramNode(self, node: ProgramNode):
        for stmt in node.statements:
            self._visit(stmt)

    def _compile_BlockNode(self, node: BlockNode):
        for stmt in node.statements:
            self._visit(stmt)

    # ===== Statements =====
    def _compile_PrintNode(self, node: PrintNode):
        if node.expression:
            self._visit(node.expression)
        self.instructions.append(Instruction('PRINT'))

    def _compile_VarDeclNode(self, node: VarDeclNode):
        if node.initializer:
            self._visit(node.initializer)
        self.instructions.append(Instruction('STORE_VAR', node.name))

    def _compile_ExprStmtNode(self, node: ExprStmtNode):
        self._visit(node.expression)

    def _compile_ReturnNode(self, node: ReturnNode):
        if node.value:
            self._visit(node.value)
        self.instructions.append(Instruction('RETURN'))

    # ===== Control Flow =====
    def _compile_IfNode(self, node: IfNode):
        self._visit(node.condition)
        # Jump ke else jika kondisi False
        jump_else = Instruction('JUMP_IF_FALSE', None)
        self.instructions.append(jump_else)

        self._visit(node.then_branch)

        if node.else_branch:
            jump_end = Instruction('JUMP', None)
            self.instructions.append(jump_end)
            # Patch alamat jump_else
            else_addr = len(self.instructions)
            jump_else.arg = else_addr
            self._visit(node.else_branch)
            end_addr = len(self.instructions)
            jump_end.arg = end_addr
        else:
            else_addr = len(self.instructions)
            jump_else.arg = else_addr

    def _compile_WhileNode(self, node: WhileNode):
        loop_start = len(self.instructions)
        self._visit(node.condition)
        jump_exit = Instruction('JUMP_IF_FALSE', None)
        self.instructions.append(jump_exit)

        self._visit(node.body)

        # Loop balik ke awal
        self.instructions.append(Instruction('JUMP', loop_start))
        exit_addr = len(self.instructions)
        jump_exit.arg = exit_addr

    # ===== Expressions =====
    def _compile_LiteralExpr(self, node: LiteralExpr):
        # Masukkan konstanta ke pool
        if node.value in self.constants:
            idx = self.constants.index(node.value)
        else:
            idx = len(self.constants)
            self.constants.append(node.value)
        self.instructions.append(Instruction('LOAD_CONST', idx))

    def _compile_VariableExpr(self, node: VariableExpr):
        self.instructions.append(Instruction('LOAD_VAR', node.name))

    def _compile_BinaryExpr(self, node: BinaryExpr):
        self._visit(node.left)
        self._visit(node.right)
        # Map operator ke opcode
        op_map = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            '%': 'MOD',
            '==': 'EQ',
            '!=': 'NEQ',
            '<': 'LT',
            '>': 'GT',
            '<=': 'LTE',
            '>=': 'GTE'
        }
        op_code = op_map.get(node.operator, 'ADD')  # Default ADD
        self.instructions.append(Instruction(op_code))

    def _compile_UnaryExpr(self, node: UnaryExpr):
        if node.operator == '-':
            # Negasi: push 0, tukar, kurangi
            self.instructions.append(Instruction('LOAD_CONST', 0))
            self._visit(node.operand)
            self.instructions.append(Instruction('SUB'))
        elif node.operator == '!':
            self._visit(node.operand)
            self.instructions.append(Instruction('NOT'))
        else:
            self._visit(node.operand)
