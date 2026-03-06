package com.luminar.nova.lexer;

import java.util.ArrayList;
import java.util.List;

public final class Lexer {
    private final String source;
    private final List<Token> tokens = new ArrayList<>();
    private final List<String> errors = new ArrayList<>();
    private int start = 0, current = 0, line = 1;

    public Lexer(String source) { this.source = source; }

    public List<Token> tokenize() {
        while (!isAtEnd()) { start = current; scanToken(); }
        tokens.add(new Token(TokenType.EOF, "", null, line));
        return tokens;
    }

    public boolean hasErrors()       { return !errors.isEmpty(); }
    public List<String> getErrors()  { return List.copyOf(errors); }

    private void scanToken() {
        char c = advance();
        switch (c) {
            case '(' -> emit(TokenType.LPAREN);
            case ')' -> emit(TokenType.RPAREN);
            case '{' -> emit(TokenType.LBRACE);
            case '}' -> emit(TokenType.RBRACE);
            case '[' -> emit(TokenType.LBRACKET);
            case ']' -> emit(TokenType.RBRACKET);
            case ',' -> emit(TokenType.COMMA);
            case ';' -> emit(TokenType.SEMICOLON);
            case ':' -> emit(TokenType.COLON);
            case '?' -> emit(TokenType.QUESTION);
            case '.' -> { if (match('.')) emit(TokenType.DOT_DOT); else emit(TokenType.DOT); }
            case '+' -> { if (match('+')) emit(TokenType.PLUS_PLUS); else if (match('=')) emit(TokenType.PLUS_EQ);   else emit(TokenType.PLUS);  }
            case '-' -> { if (match('-')) emit(TokenType.MINUS_MINUS); else if (match('>')) emit(TokenType.ARROW); else if (match('=')) emit(TokenType.MINUS_EQ);  else emit(TokenType.MINUS); }
            case '*' -> { if (match('*')) emit(TokenType.STAR_STAR); else if (match('=')) emit(TokenType.STAR_EQ);   else emit(TokenType.STAR);  }
            case '/' -> {
                if      (match('/')) { while (!isAtEnd() && peek() != '\n') advance(); }
                else if (match('*')) blockComment();
                else if (match('=')) emit(TokenType.SLASH_EQ);
                else                 emit(TokenType.SLASH);
            }
            case '%' -> { if (match('=')) emit(TokenType.PERCENT_EQ); else emit(TokenType.PERCENT); }
            case '!' -> { if (match('=')) emit(TokenType.BANG_EQ);    else emit(TokenType.BANG);    }
            case '=' -> { if (match('=')) emit(TokenType.EQ_EQ);      else emit(TokenType.EQ);      }
            case '<' -> { if (match('=')) emit(TokenType.LESS_EQ);    else emit(TokenType.LESS);    }
            case '>' -> { if (match('=')) emit(TokenType.GREATER_EQ); else emit(TokenType.GREATER); }
            case '&' -> { if (match('&')) emit(TokenType.AMP_AMP);    else errors.add("Line " + line + ": Expected '&&'"); }
            case '|' -> { if (match('|')) emit(TokenType.PIPE_PIPE);   else errors.add("Line " + line + ": Expected '||'"); }
            case ' ', '\r', '\t' -> {}
            case '\n' -> line++;
            case '"'  -> scanString('"');
            case '\'' -> scanString('\'');
            default -> {
                if (Character.isDigit(c))     scanNumber();
                else if (isIdentStart(c))     scanIdent();
                else errors.add("Line " + line + ": Unexpected character '" + c + "'");
            }
        }
    }

    private void scanString(char quote) {
        var sb = new StringBuilder();
        while (!isAtEnd() && peek() != quote) {
            char ch = advance();
            if (ch == '\n') { line++; sb.append('\n'); continue; }
            if (ch == '\\') {
                char esc = advance();
                sb.append(switch (esc) {
                    case 'n'  -> '\n'; case 't' -> '\t'; case 'r' -> '\r';
                    case '\\' -> '\\'; case '"' -> '"'; case '\'' -> '\'';
                    default   -> esc;
                });
            } else sb.append(ch);
        }
        if (isAtEnd()) { errors.add("Line " + line + ": Unterminated string"); return; }
        advance();
        emitLit(TokenType.STRING, sb.toString());
    }

    private void scanNumber() {
        boolean isFloat = false;
        while (!isAtEnd() && (Character.isDigit(peek()) || peek() == '_')) advance();
        if (!isAtEnd() && peek() == '.' && current + 1 < source.length()
                && Character.isDigit(source.charAt(current + 1))) {
            isFloat = true; advance();
            while (!isAtEnd() && Character.isDigit(peek())) advance();
        }
        String raw = source.substring(start, current).replace("_", "");
        emitLit(TokenType.NUMBER, isFloat ? Double.parseDouble(raw) : Long.parseLong(raw));
    }

    private void scanIdent() {
        while (!isAtEnd() && isIdentPart(peek())) advance();
        String word = source.substring(start, current);
        TokenType type = TokenType.fromKeyword(word);
        Object lit = switch (type) { case TRUE -> Boolean.TRUE; case FALSE -> Boolean.FALSE; case NULL -> null; default -> null; };
        emitLit(type, lit);
    }

    private void blockComment() {
        int depth = 1;
        while (!isAtEnd() && depth > 0) {
            if (peek() == '\n')                            { line++; }
            if (peek() == '/' && peekNext() == '*')        { depth++; advance(); }
            else if (peek() == '*' && peekNext() == '/')   { depth--; advance(); }
            advance();
        }
    }

    private void emit(TokenType t)             { tokens.add(new Token(t, source.substring(start, current), null, line)); }
    private void emitLit(TokenType t, Object v){ tokens.add(new Token(t, source.substring(start, current), v, line)); }
    private char advance()                     { return source.charAt(current++); }
    private boolean match(char e)              { if (isAtEnd() || source.charAt(current) != e) return false; current++; return true; }
    private char peek()                        { return isAtEnd() ? '\0' : source.charAt(current); }
    private char peekNext()                    { return current + 1 >= source.length() ? '\0' : source.charAt(current + 1); }
    private boolean isAtEnd()                  { return current >= source.length(); }
    private boolean isIdentStart(char c)       { return Character.isLetter(c) || c == '_'; }
    private boolean isIdentPart(char c)        { return Character.isLetterOrDigit(c) || c == '_'; }
}