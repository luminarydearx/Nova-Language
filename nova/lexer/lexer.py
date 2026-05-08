from typing import List, Optional
from .token_types import TokenType, from_keyword
from .token import Token


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.errors: List[str] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def tokenize(self) -> List[Token]:
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def get_errors(self) -> List[str]:
        return self.errors.copy()

    def _scan_token(self):
        c = self._advance()
        if c == '(':
            self._emit(TokenType.LPAREN)
        elif c == ')':
            self._emit(TokenType.RPAREN)
        elif c == '{':
            self._emit(TokenType.LBRACE)
        elif c == '}':
            self._emit(TokenType.RBRACE)
        elif c == '[':
            self._emit(TokenType.LBRACKET)
        elif c == ']':
            self._emit(TokenType.RBRACKET)
        elif c == ',':
            self._emit(TokenType.COMMA)
        elif c == ';':
            self._emit(TokenType.SEMICOLON)
        elif c == ':':
            self._emit(TokenType.COLON)
        elif c == '?':
            self._emit(TokenType.QUESTION)
        elif c == '.':
            if self._match('.'):
                self._emit(TokenType.DOT_DOT)
            else:
                self._emit(TokenType.DOT)
        elif c == '+':
            if self._match('+'):
                self._emit(TokenType.PLUS_PLUS)
            elif self._match('='):
                self._emit(TokenType.PLUS_EQ)
            else:
                self._emit(TokenType.PLUS)
        elif c == '-':
            if self._match('-'):
                self._emit(TokenType.MINUS_MINUS)
            elif self._match('>'):
                self._emit(TokenType.ARROW)
            elif self._match('='):
                self._emit(TokenType.MINUS_EQ)
            else:
                self._emit(TokenType.MINUS)
        elif c == '*':
            if self._match('*'):
                self._emit(TokenType.STAR_STAR)
            elif self._match('='):
                self._emit(TokenType.STAR_EQ)
            else:
                self._emit(TokenType.STAR)
        elif c == '/':
            if self._match('/'):
                while not self._is_at_end() and self._peek() != '\n':
                    self._advance()
            elif self._match('*'):
                self._block_comment()
            elif self._match('='):
                self._emit(TokenType.SLASH_EQ)
            else:
                self._emit(TokenType.SLASH)
        elif c == '%':
            if self._match('='):
                self._emit(TokenType.PERCENT_EQ)
            else:
                self._emit(TokenType.PERCENT)
        elif c == '!':
            if self._match('='):
                self._emit(TokenType.BANG_EQ)
            else:
                self._emit(TokenType.BANG)
        elif c == '=':
            if self._match('='):
                self._emit(TokenType.EQ_EQ)
            else:
                self._emit(TokenType.EQ)
        elif c == '<':
            if self._match('='):
                self._emit(TokenType.LESS_EQ)
            else:
                self._emit(TokenType.LESS)
        elif c == '>':
            if self._match('='):
                self._emit(TokenType.GREATER_EQ)
            else:
                self._emit(TokenType.GREATER)
        elif c == '&':
            if self._match('&'):
                self._emit(TokenType.AMP_AMP)
            else:
                self.errors.append(f"Line {self.line}: Expected '&&'")
        elif c == '|':
            if self._match('|'):
                self._emit(TokenType.PIPE_PIPE)
            else:
                self.errors.append(f"Line {self.line}: Expected '||'")
        elif c in (' ', '\r', '\t'):
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"' or c == "'":
            self._scan_string(c)
        else:
            if c.isdigit():
                self._scan_number()
            elif self._is_ident_start(c):
                self._scan_ident()
            else:
                self.errors.append(f"Line {self.line}: Unexpected character '{c}'")

    def _scan_string(self, quote: str):
        sb = []
        while not self._is_at_end() and self._peek() != quote:
            ch = self._advance()
            if ch == '\n':
                self.line += 1
                sb.append('\n')
                continue
            if ch == '\\':
                esc = self._advance()
                if esc == 'n':
                    sb.append('\n')
                elif esc == 't':
                    sb.append('\t')
                elif esc == 'r':
                    sb.append('\r')
                elif esc == '\\':
                    sb.append('\\')
                elif esc == '"':
                    sb.append('"')
                elif esc == "'":
                    sb.append("'")
                else:
                    sb.append(esc)
            else:
                sb.append(ch)
        if self._is_at_end():
            self.errors.append(f"Line {self.line}: Unterminated string")
            return
        self._advance()
        self._emit_lit(TokenType.STRING, ''.join(sb))

    def _scan_number(self):
        is_float = False
        while not self._is_at_end() and (self._peek().isdigit() or self._peek() == '_'):
            self._advance()
        if (not self._is_at_end() and self._peek() == '.'
                and self.current + 1 < len(self.source)
                and self.source[self.current + 1].isdigit()):
            is_float = True
            self._advance()
            while not self._is_at_end() and self._peek().isdigit():
                self._advance()
        raw = self.source[self.start:self.current].replace('_', '')
        if is_float:
            value = float(raw)
        else:
            value = int(raw)
        self._emit_lit(TokenType.NUMBER, value)

    def _scan_ident(self):
        while not self._is_at_end() and self._is_ident_part(self._peek()):
            self._advance()
        word = self.source[self.start:self.current]
        token_type = from_keyword(word)
        literal = None
        if token_type == TokenType.TRUE:
            literal = True
        elif token_type == TokenType.FALSE:
            literal = False
        elif token_type == TokenType.NULL:
            literal = None
        self._emit_lit(token_type, literal)

    def _block_comment(self):
        depth = 1
        while not self._is_at_end() and depth > 0:
            if self._peek() == '\n':
                self.line += 1
            if self._peek() == '/' and self._peek_next() == '*':
                depth += 1
                self._advance()
            elif self._peek() == '*' and self._peek_next() == '/':
                depth -= 1
                self._advance()
            self._advance()

    def _emit(self, token_type: TokenType):
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, lexeme, None, self.line))

    def _emit_lit(self, token_type: TokenType, value: object):
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, lexeme, value, self.line))

    def _advance(self) -> str:
        ch = self.source[self.current]
        self.current += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return '\0'
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _is_ident_start(self, c: str) -> bool:
        return c.isalpha() or c == '_'

    def _is_ident_part(self, c: str) -> bool:
        return c.isalnum() or c == '_'
