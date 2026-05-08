from typing import Any, Optional
from ..symbol_table import ScopeStack, SymbolInfo
from ..native_bridge import NativeFunction
from ..ast.nodes import (
    ProgramNode, BlockNode, PrintNode, VarDeclNode, FunctionDeclNode,
    IfNode, WhileNode, DoWhileNode, ReturnNode, ExprStmtNode,
    LiteralExpr, VariableExpr, BinaryExpr, UnaryExpr,
    CallExpr, GetExpr, SetExpr, ThisExpr, ArrayExpr, TryCatchNode, ThrowNode
)
from ..parser.parser import ParseError

class ReturnException(Exception):
    def __init__(self, value: Any):
        self.value = value

class NovaRuntimeException(Exception):
    pass

class Interpreter:
    """Interpreter Nova dengan Visitor Pattern"""

    def __init__(self):
        self.scope = ScopeStack()
        self.output = []  # Menampung output print
        self._register_natives()

    def _register_natives(self):
        """Daftarkan fungsi native Python agar bisa dipanggil dari Nova"""
        import time
        import math
        
        # Fungsi waktu
        clock_fn = NativeFunction("clock", 0, lambda: time.time())
        self.scope.define("clock", "native", clock_fn, True, "public")
        
        # Fungsi matematika
        sqrt_fn = NativeFunction("sqrt", 1, math.sqrt)
        self.scope.define("sqrt", "native", sqrt_fn, True, "public")
        
        # Fungsi string/utility bisa ditambah di sini
        # Contoh: len_fn = NativeFunction("len", 1, len)
        # self.scope.define("len", "native", len_fn, True, "public")

    def interpret(self, ast: ProgramNode) -> list:
        """Jalankan program Nova dari AST"""
        try:
            self._visit(ast)
        except NovaRuntimeException as e:
            self.output.append(f"Runtime Error: {e}")
        return self.output

    def _visit(self, node: Any) -> Any:
        """Visitor pattern dispatcher"""
        method_name = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self._visit_generic)
        return visitor(node)

    def _visit_generic(self, node):
        raise NovaRuntimeException(f"Tidak ada visitor untuk node: {type(node).__name__}")

    # ===== Program & Block =====
    def _visit_ProgramNode(self, node: ProgramNode):
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_BlockNode(self, node: BlockNode):
        self.scope.push()  # Masuk lingkup baru
        try:
            for stmt in node.statements:
                self._visit(stmt)
        finally:
            self.scope.pop()  # Keluar lingkup

    # ===== Statements =====
    def _visit_PrintNode(self, node: PrintNode):
        value = self._visit(node.expression) if node.expression else "nil"
        self.output.append(str(value))

    def _visit_VarDeclNode(self, node: VarDeclNode):
        value = self._visit(node.initializer) if node.initializer else None
        var_type = node.type_annotation if node.type_annotation else self._infer_type(value)
        self.scope.define(node.name, var_type, value, node.is_const, node.visibility)

    def _visit_ExprStmtNode(self, node: ExprStmtNode):
        self._visit(node.expression)

    def _visit_ReturnNode(self, node: ReturnNode):
        value = self._visit(node.value) if node.value else None
        raise ReturnException(value)

    # ===== Control Flow =====
    def _visit_IfNode(self, node: IfNode):
        if self._is_truthy(self._visit(node.condition)):
            self._visit(node.then_branch)
        elif node.else_branch:
            self._visit(node.else_branch)

    def _visit_WhileNode(self, node: WhileNode):
        while self._is_truthy(self._visit(node.condition)):
            self._visit(node.body)

    def _visit_DoWhileNode(self, node: DoWhileNode):
        while True:
            self._visit(node.body)
            if not self._is_truthy(self._visit(node.condition)):
                break

    # ===== Exception Handling =====
    def _visit_TryCatchNode(self, node: TryCatchNode):
        """Handle try-catch-finally"""
        try:
            self._visit(node.try_block)
        except Exception as e:
            # Cek apakah ada catch block yang cocok
            caught = False
            for exc_type, var_name, handler_block in node.catch_blocks:
                # Simplifikasi: tangkap semua exception (bisa dikembangkan dengan cek tipe)
                self.scope.push()
                try:
                    # Define variabel exception di scope handler
                    self.scope.define(var_name, "exception", str(e), True, "public")
                    self._visit(handler_block)
                finally:
                    self.scope.pop()
                caught = True
                break
            if not caught:
                raise  # Re-raise jika tidak ada yang menangkap
        finally:
            if node.finally_block:
                self._visit(node.finally_block)

    def _visit_ThrowNode(self, node: ThrowNode):
        """Throw an exception"""
        value = self._visit(node.expression)
        raise NovaRuntimeException(f"Exception: {value}")

    # ===== Expressions =====
    def _visit_LiteralExpr(self, node: LiteralExpr):
        return node.value

    def _visit_VariableExpr(self, node: VariableExpr):
        info = self.scope.resolve(node.name)
        if not info:
            raise NovaRuntimeException(f"Variabel '{node.name}' tidak ditemukan")
        return info.value

    def _visit_BinaryExpr(self, node: BinaryExpr):
        left = self._visit(node.left)
        right = self._visit(node.right)
        op = node.operator

        # Constant folding sederhana
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': return left / right if right != 0 else 0
            if op == '%': return left % right
            if op == '==': return left == right
            if op == '!=': return left != right
            if op == '<': return left < right
            if op == '>': return left > right
            if op == '<=': return left <= right
            if op == '>=': return left >= right

        # String concatenation
        if op == '+':
            return str(left) + str(right)

        raise NovaRuntimeException(f"Operator '{op}' tidak didukung untuk {type(left)} dan {type(right)}")

    def _visit_UnaryExpr(self, node: UnaryExpr):
        operand = self._visit(node.operand)
        if node.operator == '-':
            return -operand if isinstance(operand, (int, float)) else 0
        if node.operator == '!':
            return not self._is_truthy(operand)
        return operand

    def _visit_CallExpr(self, node: CallExpr):
        """Panggil fungsi (native atau user-defined)"""
        callee = self._visit(node.callee)  # Harusnya VariableExpr -> dapet NativeFunction
        args = [self._visit(arg) for arg in node.arguments]

        if isinstance(callee, NativeFunction):
            return callee.call(args)
        else:
            raise NovaRuntimeException(f"Tidak bisa memanggil {type(callee)} sebagai fungsi")

    # ===== Helpers =====
    def _is_truthy(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        return bool(value)

    def _infer_type(self, value: Any) -> str:
        """Type inference sederhana"""
        if isinstance(value, bool):
            return "bool"
        if isinstance(value, int):
            return "int"
        if isinstance(value, float):
            return "float"
        if isinstance(value, str):
            return "string"
        if isinstance(value, list):
            return "array"
        if isinstance(value, NativeFunction):
            return "native"
        return "any"
