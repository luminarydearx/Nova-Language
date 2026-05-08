from enum import Enum

class TokenType(Enum):
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"

    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    PERCENT = "PERCENT"
    STAR_STAR = "STAR_STAR"
    PLUS_PLUS = "PLUS_PLUS"
    MINUS_MINUS = "MINUS_MINUS"

    EQ_EQ = "EQ_EQ"
    BANG_EQ = "BANG_EQ"
    LESS = "LESS"
    LESS_EQ = "LESS_EQ"
    GREATER = "GREATER"
    GREATER_EQ = "GREATER_EQ"

    AMP_AMP = "AMP_AMP"
    PIPE_PIPE = "PIPE_PIPE"
    BANG = "BANG"

    EQ = "EQ"
    PLUS_EQ = "PLUS_EQ"
    MINUS_EQ = "MINUS_EQ"
    STAR_EQ = "STAR_EQ"
    SLASH_EQ = "SLASH_EQ"
    PERCENT_EQ = "PERCENT_EQ"

    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    COLON = "COLON"
    QUESTION = "QUESTION"
    DOT = "DOT"
    DOT_DOT = "DOT_DOT"
    ARROW = "ARROW"

    KW_VAR = "KW_VAR"
    KW_CONST = "KW_CONST"
    KW_FUNC = "KW_FUNC"
    KW_RETURN = "KW_RETURN"
    KW_IF = "KW_IF"
    KW_ELSE = "KW_ELSE"
    KW_WHILE = "KW_WHILE"
    KW_DO = "KW_DO"
    KW_FOR = "KW_FOR"
    KW_IN = "KW_IN"
    KW_BREAK = "KW_BREAK"
    KW_CONTINUE = "KW_CONTINUE"

    KW_TRY = "KW_TRY"
    KW_CATCH = "KW_CATCH"
    KW_FINALLY = "KW_FINALLY"
    KW_THROW = "KW_THROW"

    KW_CLASS = "KW_CLASS"
    KW_NEW = "KW_NEW"
    KW_THIS = "KW_THIS"
    KW_SUPER = "KW_SUPER"
    KW_EXTENDS = "KW_EXTENDS"
    KW_ABSTRACT = "KW_ABSTRACT"
    KW_INTERFACE = "KW_INTERFACE"
    KW_IMPLEMENTS = "KW_IMPLEMENTS"
    KW_STATIC = "KW_STATIC"

    KW_PUBLIC = "KW_PUBLIC"
    KW_PRIVATE = "KW_PRIVATE"
    KW_PROTECTED = "KW_PROTECTED"

    KW_ENUM = "KW_ENUM"
    KW_STRUCT = "KW_STRUCT"

    KW_IMPORT = "KW_IMPORT"
    KW_FROM = "KW_FROM"
    KW_EXPORT = "KW_EXPORT"
    KW_MATCH = "KW_MATCH"
    KW_PRINT = "KW_PRINT"
    KW_ASYNC = "KW_ASYNC"
    KW_AWAIT = "KW_AWAIT"

    EOF = "EOF"


KEYWORDS = {
    "var": TokenType.KW_VAR,
    "const": TokenType.KW_CONST,
    "func": TokenType.KW_FUNC,
    "return": TokenType.KW_RETURN,
    "if": TokenType.KW_IF,
    "else": TokenType.KW_ELSE,
    "while": TokenType.KW_WHILE,
    "do": TokenType.KW_DO,
    "for": TokenType.KW_FOR,
    "in": TokenType.KW_IN,
    "break": TokenType.KW_BREAK,
    "continue": TokenType.KW_CONTINUE,
    "try": TokenType.KW_TRY,
    "catch": TokenType.KW_CATCH,
    "finally": TokenType.KW_FINALLY,
    "throw": TokenType.KW_THROW,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL,
    "class": TokenType.KW_CLASS,
    "new": TokenType.KW_NEW,
    "this": TokenType.KW_THIS,
    "super": TokenType.KW_SUPER,
    "extends": TokenType.KW_EXTENDS,
    "abstract": TokenType.KW_ABSTRACT,
    "interface": TokenType.KW_INTERFACE,
    "implements": TokenType.KW_IMPLEMENTS,
    "static": TokenType.KW_STATIC,
    "public": TokenType.KW_PUBLIC,
    "private": TokenType.KW_PRIVATE,
    "protected": TokenType.KW_PROTECTED,
    "enum": TokenType.KW_ENUM,
    "struct": TokenType.KW_STRUCT,
    "import": TokenType.KW_IMPORT,
    "from": TokenType.KW_FROM,
    "export": TokenType.KW_EXPORT,
    "match": TokenType.KW_MATCH,
    "print": TokenType.KW_PRINT,
    "async": TokenType.KW_ASYNC,
    "await": TokenType.KW_AWAIT
}


def from_keyword(word: str):
    return KEYWORDS.get(word, TokenType.IDENTIFIER)
