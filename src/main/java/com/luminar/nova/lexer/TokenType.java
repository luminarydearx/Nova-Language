package com.luminar.nova.lexer;
import java.util.Map;

public enum TokenType {
    // Literals & identifiers
    NUMBER, STRING, IDENTIFIER, TRUE, FALSE, NULL,

    // Arithmetic
    PLUS, MINUS, STAR, SLASH, PERCENT, STAR_STAR,
    PLUS_PLUS, MINUS_MINUS,

    // Comparison
    EQ_EQ, BANG_EQ, LESS, LESS_EQ, GREATER, GREATER_EQ,

    // Logical
    AMP_AMP, PIPE_PIPE, BANG,

    // Assignment
    EQ, PLUS_EQ, MINUS_EQ, STAR_EQ, SLASH_EQ, PERCENT_EQ,

    // Delimiters
    LPAREN, RPAREN, LBRACE, RBRACE, LBRACKET, RBRACKET,
    COMMA, SEMICOLON, COLON, QUESTION, DOT, DOT_DOT, ARROW,

    // Keywords — control flow
    KW_VAR, KW_CONST, KW_FUNC, KW_RETURN,
    KW_IF, KW_ELSE, KW_WHILE, KW_DO, KW_FOR, KW_IN,
    KW_BREAK, KW_CONTINUE,

    // Keywords — exception handling
    KW_TRY, KW_CATCH, KW_FINALLY, KW_THROW,

    // Keywords — OOP
    KW_CLASS, KW_NEW, KW_THIS, KW_SUPER, KW_EXTENDS,
    KW_ABSTRACT, KW_INTERFACE, KW_IMPLEMENTS, KW_STATIC,

    // Keywords — visibility
    KW_PUBLIC, KW_PRIVATE, KW_PROTECTED,

    // Keywords — data types
    KW_ENUM, KW_STRUCT,

    // Keywords — other
    KW_IMPORT, KW_FROM, KW_EXPORT, KW_MATCH, KW_PRINT,
    KW_ASYNC, KW_AWAIT,

    EOF;

    private static final Map<String, TokenType> KW = Map.ofEntries(
        Map.entry("var",       KW_VAR),
        Map.entry("const",     KW_CONST),
        Map.entry("func",      KW_FUNC),
        Map.entry("return",    KW_RETURN),
        Map.entry("if",        KW_IF),
        Map.entry("else",      KW_ELSE),
        Map.entry("while",     KW_WHILE),
        Map.entry("do",        KW_DO),
        Map.entry("for",       KW_FOR),
        Map.entry("in",        KW_IN),
        Map.entry("break",     KW_BREAK),
        Map.entry("continue",  KW_CONTINUE),
        Map.entry("try",       KW_TRY),
        Map.entry("catch",     KW_CATCH),
        Map.entry("finally",   KW_FINALLY),
        Map.entry("throw",     KW_THROW),
        Map.entry("true",      TRUE),
        Map.entry("false",     FALSE),
        Map.entry("null",      NULL),
        Map.entry("class",     KW_CLASS),
        Map.entry("new",       KW_NEW),
        Map.entry("this",      KW_THIS),
        Map.entry("super",     KW_SUPER),
        Map.entry("extends",   KW_EXTENDS),
        Map.entry("abstract",  KW_ABSTRACT),
        Map.entry("interface", KW_INTERFACE),
        Map.entry("implements",KW_IMPLEMENTS),
        Map.entry("static",    KW_STATIC),
        Map.entry("public",    KW_PUBLIC),
        Map.entry("private",   KW_PRIVATE),
        Map.entry("protected", KW_PROTECTED),
        Map.entry("enum",      KW_ENUM),
        Map.entry("struct",    KW_STRUCT),
        Map.entry("import",    KW_IMPORT),
        Map.entry("from",      KW_FROM),
        Map.entry("export",    KW_EXPORT),
        Map.entry("match",     KW_MATCH),
        Map.entry("print",     KW_PRINT),
        Map.entry("async",     KW_ASYNC),
        Map.entry("await",     KW_AWAIT)
    );

    public static TokenType fromKeyword(String w) {
        return KW.getOrDefault(w, IDENTIFIER);
    }
}