package com.luminar.nova.lexer;

public record Token(TokenType type, String lexeme, Object literal, int line) {}