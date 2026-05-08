from typing import List, Dict, Tuple, Any, Optional, Callable
from ..lexer.token import Token
from ..lexer.token_types import TokenType
from ..ast.nodes import (
    ProgramNode, BlockNode, PrintNode, VarDeclNode, FunctionDeclNode,
    ClassDeclNode, InterfaceDeclNode, EnumDeclNode, StructDeclNode,
    IfNode, WhileNode, DoWhileNode, ForNode, ReturnNode,
    TryCatchNode, ThrowNode, ExprStmtNode,
    LiteralExpr, VariableExpr, BinaryExpr, UnaryExpr,
    CallExpr, GetExpr, SetExpr, ThisExpr, SuperExpr, ArrayExpr
)


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.errors: List[str] = []
        self.pos = 0

    def parse(self) -> ProgramNode:
        statements = []
        while not self._is_at_end():
            try:
                stmt = self._statement()
                statements.append(stmt)
            except ParseError as e:
                self.errors.append(str(e))
                self._synchronize()
        return ProgramNode(statements)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def get_errors(self) -> List[str]:
        return self.errors.copy()

    def _statement(self) -> Any:
        peek_type = self._peek().type
        if peek_type == TokenType.KW_PRINT:
            return self._print_stmt()
        elif peek_type == TokenType.KW_VAR:
            return self._var_decl("public", False)
        elif peek_type == TokenType.KW_CONST:
            return self._var_decl("public", True)
        elif peek_type == TokenType.KW_FUNC:
            return self._func_decl("public")
        elif peek_type == TokenType.KW_CLASS:
            return self._class_decl(False)
        elif peek_type == TokenType.KW_IF:
            return self._if_stmt()
        elif peek_type == TokenType.KW_WHILE:
            return self._while_stmt()
        elif peek_type == TokenType.KW_DO:
            return self._do_while_stmt()
        elif peek_type == TokenType.KW_TRY:
            return self._try_catch_stmt()
        elif peek_type == TokenType.LBRACE:
            return self._block()
        elif peek_type == TokenType.KW_RETURN:
            return self._return_stmt()
        elif peek_type in (TokenType.KW_PUBLIC, TokenType.KW_PRIVATE, TokenType.KW_PROTECTED):
            vis = self._advance().lexeme
            if self._check(TokenType.KW_FUNC):
                return self._func_decl(vis)
            elif self._check(TokenType.KW_VAR):
                return self._var_decl(vis, False)
            elif self._check(TokenType.KW_CONST):
                return self._var_decl(vis, True)
            else:
                raise self._error(f"Expected 'func', 'var' or 'const' after '{vis}'")
        else:
            return self._expr_stmt()

    def _print_stmt(self) -> PrintNode:
        self._consume(TokenType.KW_PRINT, "Expected 'print'")
        expr = None
        if self._check(TokenType.LPAREN):
            self._advance()
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')'")
        else:
            expr = self._expression()
        self._consume_opt_semi()
        return PrintNode(expr)

    def _var_decl(self, visibility: str, is_const: bool) -> VarDeclNode:
        self._advance()
        name = self._consume_ident("Expected variable name")
        type_annot = None
        if self._match(TokenType.COLON):
            type_annot = self._parse_type_name()
        init = None
        if self._match(TokenType.EQ):
            init = self._expression()
        self._consume_opt_semi()
        return VarDeclNode(visibility, name, is_const, type_annot, init)

    def _func_decl(self, visibility: str) -> FunctionDeclNode:
        self._consume(TokenType.KW_FUNC, "Expected 'func'")
        return self._parse_func_decl(visibility, False)

    def _parse_func_decl(self, visibility: str, is_abstract: bool) -> FunctionDeclNode:
        name = self._consume_ident("Expected function name")
        self._consume(TokenType.LPAREN, "Expected '(' after function name")
        params = []
        param_types = []
        if not self._check(TokenType.RPAREN):
            while True:
                params.append(self._consume_ident("Expected parameter name"))
                pt = None
                if self._match(TokenType.COLON):
                    pt = self._parse_type_name()
                param_types.append(pt)
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RPAREN, "Expected ')'")
        return_type = None
        if self._match(TokenType.ARROW) or self._check(TokenType.COLON):
            if self._peek().type == TokenType.COLON:
                self._advance()
            return_type = self._parse_type_name()
        body = None
        if not is_abstract:
            body = self._block()
        return FunctionDeclNode(visibility, is_abstract, name, params, param_types, return_type, body)

    def _if_stmt(self) -> IfNode:
        self._consume(TokenType.KW_IF, "Expected 'if'")
        condition = self._expression()
        then_branch = self._block()
        else_branch = None
        if self._match(TokenType.KW_ELSE):
            if self._check(TokenType.KW_IF):
                else_branch = self._if_stmt()
            else:
                else_branch = self._block()
        return IfNode(condition, then_branch, else_branch)

    def _while_stmt(self) -> WhileNode:
        self._consume(TokenType.KW_WHILE, "Expected 'while'")
        condition = self._expression()
        body = self._block()
        return WhileNode(condition, body)

    def _do_while_stmt(self) -> DoWhileNode:
        self._consume(TokenType.KW_DO, "Expected 'do'")
        body = self._block()
        self._consume(TokenType.KW_WHILE, "Expected 'while'")
        condition = self._expression()
        self._consume_opt_semi()
        return DoWhileNode(body, condition)

    def _try_catch_stmt(self) -> TryCatchNode:
        """Parse: try { ... } catch (Type var) { ... } finally { ... }"""
        self._consume(TokenType.KW_TRY, "Expected 'try'")
        try_block = self._block()
        
        catch_blocks = []
        while self._match(TokenType.KW_CATCH):
            self._consume(TokenType.LPAREN, "Expected '(' after 'catch'")
            exc_type = self._consume_ident("Expected exception type")
            var_name = self._consume_ident("Expected variable name")
            self._consume(TokenType.RPAREN, "Expected ')'")
            handler_block = self._block()
            catch_blocks.append((exc_type, var_name, handler_block))
        
        finally_block = None
        if self._match(TokenType.KW_FINALLY):
            finally_block = self._block()
        
        return TryCatchNode(try_block, catch_blocks, finally_block)

    def _return_stmt(self) -> ReturnNode:
        self._consume(TokenType.KW_RETURN, "Expected 'return'")
        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self._expression()
        self._consume_opt_semi()
        return ReturnNode(value)

    def _expr_stmt(self) -> ExprStmtNode:
        expr = self._expression()
        self._consume_opt_semi()
        return ExprStmtNode(expr)

    def _block(self) -> BlockNode:
        self._consume(TokenType.LBRACE, "Expected '{'")
        statements = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            statements.append(self._statement())
        self._consume(TokenType.RBRACE, "Expected '}'")
        return BlockNode(statements)

    def _expression(self) -> Any:
        return self._assignment()

    def _assignment(self) -> Any:
        expr = self._logic_or()
        if self._match(TokenType.EQ, TokenType.PLUS_EQ, TokenType.MINUS_EQ,
                       TokenType.STAR_EQ, TokenType.SLASH_EQ, TokenType.PERCENT_EQ):
            operator = self._previous().lexeme
            value = self._assignment()
            if isinstance(expr, VariableExpr):
                return BinaryExpr(expr, operator, value)
            else:
                raise self._error("Invalid assignment target")
        return expr

    def _logic_or(self) -> Any:
        left = self._logic_and()
        while self._match(TokenType.PIPE_PIPE):
            operator = self._previous().lexeme
            right = self._logic_and()
            left = BinaryExpr(left, operator, right)
        return left

    def _logic_and(self) -> Any:
        left = self._equality()
        while self._match(TokenType.AMP_AMP):
            operator = self._previous().lexeme
            right = self._equality()
            left = BinaryExpr(left, operator, right)
        return left

    def _equality(self) -> Any:
        left = self._comparison()
        while self._match(TokenType.EQ_EQ, TokenType.BANG_EQ):
            operator = self._previous().lexeme
            right = self._comparison()
            left = BinaryExpr(left, operator, right)
        return left

    def _comparison(self) -> Any:
        left = self._term()
        while self._match(TokenType.LESS, TokenType.LESS_EQ,
                          TokenType.GREATER, TokenType.GREATER_EQ):
            operator = self._previous().lexeme
            right = self._term()
            left = BinaryExpr(left, operator, right)
        return left

    def _term(self) -> Any:
        left = self._factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().lexeme
            right = self._factor()
            left = BinaryExpr(left, operator, right)
        return left

    def _factor(self) -> Any:
        left = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT, TokenType.STAR_STAR):
            operator = self._previous().lexeme
            right = self._unary()
            left = BinaryExpr(left, operator, right)
        return left

    def _unary(self) -> Any:
        if self._match(TokenType.BANG, TokenType.MINUS, TokenType.PLUS):
            operator = self._previous().lexeme
            operand = self._unary()
            return UnaryExpr(operator, operand)
        return self._call()

    def _call(self) -> Any:
        expr = self._primary()
        while True:
            if self._match(TokenType.LPAREN):
                args = []
                if not self._check(TokenType.RPAREN):
                    while True:
                        args.append(self._expression())
                        if not self._match(TokenType.COMMA):
                            break
                self._consume(TokenType.RPAREN, "Expected ')'")
                expr = CallExpr(expr, args)
            elif self._match(TokenType.DOT):
                name = self._consume_ident("Expected property name")
                expr = GetExpr(expr, name)
            else:
                break
        return expr

    def _primary(self) -> Any:
        if self._match(TokenType.NUMBER):
            return LiteralExpr(self._previous().literal)
        elif self._match(TokenType.STRING):
            return LiteralExpr(self._previous().literal)
        elif self._match(TokenType.TRUE):
            return LiteralExpr(True)
        elif self._match(TokenType.FALSE):
            return LiteralExpr(False)
        elif self._match(TokenType.NULL):
            return LiteralExpr(None)
        elif self._match(TokenType.IDENTIFIER):
            return VariableExpr(self._previous().lexeme)
        elif self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')'")
            return expr
        elif self._match(TokenType.KW_THIS):
            return ThisExpr()
        elif self._match(TokenType.LBRACKET):
            elements = []
            if not self._check(TokenType.RBRACKET):
                while True:
                    elements.append(self._expression())
                    if not self._match(TokenType.COMMA):
                        break
            self._consume(TokenType.RBRACKET, "Expected ']'")
            return ArrayExpr(elements)
        else:
            raise self._error(f"Expected expression, got {self._peek().type}")

    def _parse_type_name(self) -> str:
        return self._consume_ident("Expected type name")

    def _consume_opt_semi(self):
        if self._check(TokenType.SEMICOLON):
            self._advance()

    def _consume_ident(self, error_msg: str) -> str:
        if self._check(TokenType.IDENTIFIER):
            return self._advance().lexeme
        raise self._error(error_msg)

    def _consume(self, token_type: TokenType, error_msg: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise self._error(error_msg)

    def _match(self, *token_types) -> bool:
        for tt in token_types:
            if self._check(tt):
                self._advance()
                return True
        return False

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            tok = self.tokens[self.pos]
            self.pos += 1
            return tok
        return self.tokens[-1]

    def _peek(self) -> Token:
        if self._is_at_end():
            return self.tokens[-1]
        return self.tokens[self.pos]

    def _previous(self) -> Token:
        return self.tokens[self.pos - 1]

    def _is_at_end(self) -> bool:
        if self.pos >= len(self.tokens):
            return True
        return self.tokens[self.pos].type == TokenType.EOF

    def _synchronize(self):
        self._advance()
        while not self._is_at_end():
            if self.tokens[self.pos - 1].type == TokenType.SEMICOLON:
                return
            if self._peek().type in (TokenType.KW_VAR, TokenType.KW_CONST, TokenType.KW_FUNC,
                                     TokenType.KW_CLASS, TokenType.KW_IF, TokenType.KW_WHILE,
                                     TokenType.KW_FOR, TokenType.KW_RETURN, TokenType.KW_PRINT):
                return
            self._advance()

    def _error(self, message: str) -> ParseError:
        token = self._peek()
        full_msg = f"Line {token.line}: {message}"
        return ParseError(full_msg)
