package com.luminar.nova.parser;

import com.luminar.nova.lexer.Token;
import com.luminar.nova.lexer.TokenType;
import com.luminar.nova.parser.ast.*;

import java.util.*;

public final class Parser {
    private final List<Token> tokens;
    private final List<String> errors = new ArrayList<>();
    private int pos = 0;

    public Parser(List<Token> tokens) { this.tokens = tokens; }

    public ProgramNode parse() {
        var stmts = new ArrayList<Node>();
        while (!isAtEnd()) {
            try   { stmts.add(statement()); }
            catch (ParseError e) { errors.add(e.getMessage()); synchronize(); }
        }
        return new ProgramNode(stmts);
    }

    public boolean hasErrors()      { return !errors.isEmpty(); }
    public List<String> getErrors() { return List.copyOf(errors); }

    private Node statement() {
        return switch (peek().type()) {
            case KW_PRINT    -> printStmt();
            case KW_VAR      -> varDecl("public", false);
            case KW_CONST    -> varDecl("public", true);
            case KW_FUNC     -> funcDecl("public");
            case KW_ABSTRACT -> abstractDecl();
            case KW_CLASS    -> classDecl(false);
            case KW_INTERFACE-> interfaceDecl();
            case KW_ENUM     -> enumDecl();
            case KW_STRUCT   -> structDecl();
            case KW_RETURN   -> returnStmt();
            case KW_IF       -> ifStmt();
            case KW_WHILE    -> whileStmt();
            case KW_DO       -> doWhileStmt();
            case KW_FOR      -> forStmt();
            case KW_TRY      -> tryStmt();
            case KW_THROW    -> throwStmt();
            case KW_BREAK    -> { advance(); consumeOptSemi(); yield new BreakNode(); }
            case KW_CONTINUE -> { advance(); consumeOptSemi(); yield new ContinueNode(); }
            case KW_PUBLIC, KW_PRIVATE, KW_PROTECTED -> {
                String vis = advance().lexeme();
                if (check(TokenType.KW_ABSTRACT)) { advance(); yield parseFuncDecl(vis, true); }
                if (check(TokenType.KW_FUNC))     yield funcDecl(vis);
                if (check(TokenType.KW_VAR))      yield varDecl(vis, false);
                if (check(TokenType.KW_CONST))     yield varDecl(vis, true);
                throw error("Expected 'func', 'var' or 'const' after '" + vis + "'");
            }
            default -> exprStmt();
        };
    }

    private PrintNode printStmt() {
        consume(TokenType.KW_PRINT, "Expected 'print'");
        ExprNode expr;
        if (check(TokenType.LPAREN)) {
            advance(); expr = expression(); consume(TokenType.RPAREN, "Expected ')'");
        } else {
            expr = expression();
        }
        consumeOptSemi();
        return new PrintNode(expr);
    }

    private VarDeclNode varDecl(String vis, boolean isConst) {
        advance();
        String name = consumeIdent("Expected variable name");
        String typeAnnot = null;
        if (match(TokenType.COLON)) typeAnnot = parseTypeName();
        ExprNode init = null;
        if (match(TokenType.EQ)) init = expression();
        consumeOptSemi();
        return new VarDeclNode(vis, name, isConst, typeAnnot, init);
    }

    private FunctionDeclNode funcDecl(String visibility) {
        consume(TokenType.KW_FUNC, "Expected 'func'");
        return parseFuncDecl(visibility, false);
    }

    private FunctionDeclNode parseFuncDecl(String visibility, boolean isAbstract) {
        String name = consumeIdent("Expected function name");
        var parts  = parseFuncParts(isAbstract);
        if (isAbstract) {
            consumeOptSemi();
            return new FunctionDeclNode(visibility, true, name, parts.params, parts.paramTypes, parts.ret, null);
        }
        return new FunctionDeclNode(visibility, false, name, parts.params, parts.paramTypes, parts.ret, parts.body);
    }

    private record FuncParts(List<String> params, List<String> paramTypes, String ret, BlockNode body) {}

    private FuncParts parseFuncParts(boolean isAbstract) {
        consume(TokenType.LPAREN, "Expected '(' after function name");
        var params     = new ArrayList<String>();
        var paramTypes = new ArrayList<String>();
        if (!check(TokenType.RPAREN)) {
            do {
                params.add(consumeIdent("Expected parameter name"));
                String pt = null;
                if (match(TokenType.COLON)) pt = parseTypeName();
                paramTypes.add(pt);
            } while (match(TokenType.COMMA));
        }
        consume(TokenType.RPAREN, "Expected ')'");
        String returnType = null;
        if (match(TokenType.ARROW) || (check(TokenType.COLON) && !isAbstract)) {
            if (peek().type() == TokenType.COLON) advance();
            returnType = parseTypeName();
        }
        BlockNode body = isAbstract ? null : block();
        return new FuncParts(params, paramTypes, returnType, body);
    }

    private Node abstractDecl() {
        consume(TokenType.KW_ABSTRACT, "Expected 'abstract'");
        if (check(TokenType.KW_CLASS)) return classDecl(true);
        if (check(TokenType.KW_FUNC))  { advance(); return parseFuncDecl("public", true); }
        throw error("Expected 'class' or 'func' after 'abstract'");
    }

    private ClassDeclNode classDecl(boolean isAbstract) {
        consume(TokenType.KW_CLASS, "Expected 'class'");
        String name = consumeIdent("Expected class name");
        String superName = null;
        if (match(TokenType.KW_EXTENDS)) superName = consumeIdent("Expected superclass name");
        var ifaceNames = new ArrayList<String>();
        if (match(TokenType.KW_IMPLEMENTS)) {
            do { ifaceNames.add(consumeIdent("Expected interface name")); } while (match(TokenType.COMMA));
        }
        consume(TokenType.LBRACE, "Expected '{'");
        var methods = new ArrayList<FunctionDeclNode>();
        var fields  = new ArrayList<VarDeclNode>();
        while (!check(TokenType.RBRACE) && !isAtEnd()) {
            try {
                Object member = parseClassMember();
                if (member instanceof FunctionDeclNode f) methods.add(f);
                else if (member instanceof VarDeclNode v) fields.add(v);
            }
            catch (ParseError e) { errors.add(e.getMessage()); synchronize(); }
        }
        consume(TokenType.RBRACE, "Expected '}'");
        return new ClassDeclNode(name, superName, ifaceNames, isAbstract, fields, methods);
    }

    private Object parseClassMember() {
        String vis = "public";
        boolean abs = false;
        if (check(TokenType.KW_PUBLIC) || check(TokenType.KW_PRIVATE) || check(TokenType.KW_PROTECTED))
            vis = advance().lexeme();
        if (match(TokenType.KW_ABSTRACT)) abs = true;
        match(TokenType.KW_STATIC);

        if (check(TokenType.KW_FUNC)) {
            advance();
            return parseFuncDecl(vis, abs);
        }
        if (check(TokenType.KW_VAR))   return varDecl(vis, false);
        if (check(TokenType.KW_CONST)) return varDecl(vis, true);

        throw error("Expected function or variable declaration in class");
    }

    private InterfaceDeclNode interfaceDecl() {
        consume(TokenType.KW_INTERFACE, "Expected 'interface'");
        String name = consumeIdent("Expected interface name");
        var parents = new ArrayList<String>();
        if (match(TokenType.KW_EXTENDS)) {
            do { parents.add(consumeIdent("Expected interface name")); } while (match(TokenType.COMMA));
        }
        consume(TokenType.LBRACE, "Expected '{'");
        var sigs = new ArrayList<InterfaceMethodSig>();
        while (!check(TokenType.RBRACE) && !isAtEnd()) {
            consume(TokenType.KW_FUNC, "Expected 'func'");
            String mname = consumeIdent("Expected method name");
            consume(TokenType.LPAREN, "Expected '('");
            var params = new ArrayList<String>();
            if (!check(TokenType.RPAREN)) do { params.add(consumeIdent("Expected param")); } while (match(TokenType.COMMA));
            consume(TokenType.RPAREN, "Expected ')'");
            String ret = null;
            if (match(TokenType.ARROW) || check(TokenType.COLON)) { if (peek().type() == TokenType.COLON) advance(); ret = parseTypeName(); }
            consumeOptSemi();
            sigs.add(new InterfaceMethodSig(mname, params, ret));
        }
        consume(TokenType.RBRACE, "Expected '}'");
        return new InterfaceDeclNode(name, parents, sigs);
    }

    private EnumDeclNode enumDecl() {
        consume(TokenType.KW_ENUM, "Expected 'enum'");
        String name = consumeIdent("Expected enum name");
        consume(TokenType.LBRACE, "Expected '{'");
        var values = new ArrayList<String>();
        if (!check(TokenType.RBRACE)) {
            do { values.add(consumeIdent("Expected enum value")); } while (match(TokenType.COMMA) && !check(TokenType.RBRACE));
        }
        consume(TokenType.RBRACE, "Expected '}'");
        return new EnumDeclNode(name, values);
    }

    private StructDeclNode structDecl() {
        consume(TokenType.KW_STRUCT, "Expected 'struct'");
        String name = consumeIdent("Expected struct name");
        consume(TokenType.LBRACE, "Expected '{'");
        var fields = new ArrayList<StructField>();
        while (!check(TokenType.RBRACE) && !isAtEnd()) {
            String fname = consumeIdent("Expected field name");
            consume(TokenType.COLON, "Expected ':'");
            String ftype = parseTypeName();
            consumeOptSemi();
            fields.add(new StructField(fname, ftype));
        }
        consume(TokenType.RBRACE, "Expected '}'");
        return new StructDeclNode(name, fields);
    }

    private ReturnNode returnStmt() {
        consume(TokenType.KW_RETURN, "Expected 'return'");
        ExprNode val = null;
        if (!check(TokenType.SEMICOLON) && !check(TokenType.RBRACE) && !isAtEnd())
            val = expression();
        consumeOptSemi();
        return new ReturnNode(val);
    }

    private IfNode ifStmt() {
        consume(TokenType.KW_IF, "Expected 'if'");
        boolean paren = match(TokenType.LPAREN);
        ExprNode cond = expression();
        if (paren) consume(TokenType.RPAREN, "Expected ')'");
        BlockNode then = block();
        Node elseBranch = null;
        if (match(TokenType.KW_ELSE))
            elseBranch = check(TokenType.KW_IF) ? ifStmt() : block();
        return new IfNode(cond, then, elseBranch);
    }

    private WhileNode whileStmt() {
        consume(TokenType.KW_WHILE, "Expected 'while'");
        boolean paren = match(TokenType.LPAREN);
        ExprNode cond = expression();
        if (paren) consume(TokenType.RPAREN, "Expected ')'");
        return new WhileNode(cond, block());
    }

    private DoWhileNode doWhileStmt() {
        consume(TokenType.KW_DO, "Expected 'do'");
        BlockNode body = block();
        consume(TokenType.KW_WHILE, "Expected 'while'");
        boolean paren = match(TokenType.LPAREN);
        ExprNode cond = expression();
        if (paren) consume(TokenType.RPAREN, "Expected ')'");
        consumeOptSemi();
        return new DoWhileNode(body, cond);
    }

    private ForNode forStmt() {
        consume(TokenType.KW_FOR, "Expected 'for'");
        String var = consumeIdent("Expected loop variable");
        consume(TokenType.KW_IN, "Expected 'in'");
        return new ForNode(var, expression(), block());
    }

    private TryCatchNode tryStmt() {
        consume(TokenType.KW_TRY, "Expected 'try'");
        BlockNode tryBlock = block();
        String catchVar = null;
        BlockNode catchBlock = null;
        BlockNode finallyBlock = null;
        if (check(TokenType.KW_CATCH)) {
            advance();
            consume(TokenType.LPAREN, "Expected '('");
            catchVar = consumeIdent("Expected catch variable");
            if (match(TokenType.COLON)) parseTypeName();
            consume(TokenType.RPAREN, "Expected ')'");
            catchBlock = block();
        }
        if (check(TokenType.KW_FINALLY)) {
            advance();
            finallyBlock = block();
        }
        return new TryCatchNode(tryBlock, catchVar, catchBlock, finallyBlock);
    }

    private ThrowNode throwStmt() {
        consume(TokenType.KW_THROW, "Expected 'throw'");
        ExprNode val = expression();
        consumeOptSemi();
        return new ThrowNode(val);
    }

    private BlockNode block() {
        consume(TokenType.LBRACE, "Expected '{'");
        var stmts = new ArrayList<Node>();
        while (!check(TokenType.RBRACE) && !isAtEnd()) {
            try   { stmts.add(statement()); }
            catch (ParseError e) { errors.add(e.getMessage()); synchronize(); }
        }
        consume(TokenType.RBRACE, "Expected '}'");
        return new BlockNode(stmts);
    }

    private Node exprStmt() {
        ExprNode expr = expression();
        consumeOptSemi();
        return new ExprStmtNode(expr);
    }

    private ExprNode expression() { return assignment(); }

    private ExprNode assignment() {
        ExprNode expr = ternary();
        if (match(TokenType.EQ)) {
            ExprNode val = assignment();
            if (expr instanceof ExprNode.Id id) return new ExprNode.CmpIdSet(id.name(), "=", val);
            if (expr instanceof ExprNode.MemberGet mg) return new ExprNode.MemberSet(mg.obj(), mg.member(), val);
            if (expr instanceof ExprNode.IndexGet ig) return new ExprNode.IndexSet(ig.obj(), ig.index(), val);
            throw error("Invalid assignment target");
        }
        String op = compoundOp();
        if (op != null) {
            ExprNode val = assignment();
            if (expr instanceof ExprNode.Id id) return new ExprNode.CmpIdSet(id.name(), op, val);
            if (expr instanceof ExprNode.MemberGet mg) return new ExprNode.CmpMemberSet(mg.obj(), mg.member(), op, val);
            if (expr instanceof ExprNode.IndexGet ig) return new ExprNode.CmpIndexSet(ig.obj(), ig.index(), op, val);
            throw error("Invalid compound assignment target");
        }
        return expr;
    }

    private String compoundOp() {
        return switch (peek().type()) {
            case PLUS_EQ    -> { advance(); yield "+"; }
            case MINUS_EQ   -> { advance(); yield "-"; }
            case STAR_EQ    -> { advance(); yield "*"; }
            case SLASH_EQ   -> { advance(); yield "/"; }
            case PERCENT_EQ -> { advance(); yield "%"; }
            default -> null;
        };
    }

    private ExprNode ternary() {
        ExprNode expr = or();
        if (match(TokenType.QUESTION)) {
            ExprNode then = expression();
            consume(TokenType.COLON, "Expected ':' in ternary expression");
            ExprNode els = ternary();
            return new ExprNode.Ternary(expr, then, els);
        }
        return expr;
    }

    private ExprNode or() {
        ExprNode l = and();
        while (match(TokenType.PIPE_PIPE)) l = new ExprNode.Binary(l, "||", and());
        return l;
    }

    private ExprNode and() {
        ExprNode l = equality();
        while (match(TokenType.AMP_AMP)) l = new ExprNode.Binary(l, "&&", equality());
        return l;
    }

    private ExprNode equality() {
        ExprNode l = comparison();
        while (check(TokenType.EQ_EQ) || check(TokenType.BANG_EQ))
            l = new ExprNode.Binary(l, advance().lexeme(), comparison());
        return l;
    }

    private ExprNode comparison() {
        ExprNode l = range();
        while (check(TokenType.LESS) || check(TokenType.LESS_EQ) ||
               check(TokenType.GREATER) || check(TokenType.GREATER_EQ))
            l = new ExprNode.Binary(l, advance().lexeme(), range());
        return l;
    }

    private ExprNode range() {
        ExprNode l = term();
        while (match(TokenType.DOT_DOT)) l = new ExprNode.Binary(l, "..", term());
        return l;
    }

    private ExprNode term() {
        ExprNode l = factor();
        while (check(TokenType.PLUS) || check(TokenType.MINUS))
            l = new ExprNode.Binary(l, advance().lexeme(), factor());
        return l;
    }

    private ExprNode factor() {
        ExprNode l = unary();
        while (check(TokenType.STAR) || check(TokenType.SLASH) ||
               check(TokenType.PERCENT) || check(TokenType.STAR_STAR))
            l = new ExprNode.Binary(l, advance().lexeme(), unary());
        return l;
    }

    private ExprNode unary() {
        if (check(TokenType.PLUS_PLUS) || check(TokenType.MINUS_MINUS))
            return new ExprNode.Prefix(advance().lexeme(), unary());
        if (check(TokenType.BANG) || check(TokenType.MINUS))
            return new ExprNode.Unary(advance().lexeme(), unary());
        if (match(TokenType.KW_AWAIT))
            return new ExprNode.Await(unary());
        return postfix();
    }

    private ExprNode postfix() {
        ExprNode expr = primary();
        while (true) {
            if (check(TokenType.PLUS_PLUS)) {
                advance(); expr = new ExprNode.Postfix(expr, "++");
            } else if (check(TokenType.MINUS_MINUS)) {
                advance(); expr = new ExprNode.Postfix(expr, "--");
            } else if (match(TokenType.LPAREN)) {
                var args = new ArrayList<ExprNode>();
                if (!check(TokenType.RPAREN)) do { args.add(expression()); } while (match(TokenType.COMMA));
                consume(TokenType.RPAREN, "Expected ')'");
                expr = new ExprNode.Call(expr, args);
            } else if (match(TokenType.LBRACKET)) {
                ExprNode idx = expression();
                consume(TokenType.RBRACKET, "Expected ']'");
                expr = new ExprNode.IndexGet(expr, idx);
            } else if (match(TokenType.DOT)) {
                String member = consumeIdent("Expected property name");
                expr = new ExprNode.MemberGet(expr, member);
            } else break;
        }
        return expr;
    }

    private ExprNode primary() {
        Token t = peek();
        return switch (t.type()) {
            case NUMBER, STRING -> { advance(); yield new ExprNode.Lit(t.literal()); }
            case TRUE           -> { advance(); yield new ExprNode.Lit(Boolean.TRUE);  }
            case FALSE          -> { advance(); yield new ExprNode.Lit(Boolean.FALSE); }
            case NULL           -> { advance(); yield new ExprNode.Lit(null); }
            case IDENTIFIER     -> { advance(); yield new ExprNode.Id(t.lexeme()); }
            case KW_THIS        -> { advance(); yield new ExprNode.ThisExpr(); }
            case KW_SUPER       -> parseSuper();
            case KW_NEW         -> parseNew();
            case LPAREN         -> { advance(); ExprNode e = expression(); consume(TokenType.RPAREN, "Expected ')'"); yield new ExprNode.Grouping(e); }
            case LBRACKET       -> parseArray();
            case LBRACE         -> parseObject();
            case KW_FUNC        -> { advance(); var p = parseFuncParts(false); yield new ExprNode.FuncExpr(p.params, p.paramTypes, p.ret, p.body); }
            default -> throw error("Unexpected token '" + t.lexeme() + "'");
        };
    }

    private ExprNode parseNew() {
        consume(TokenType.KW_NEW, "Expected 'new'");
        String name = consumeIdent("Expected class name");
        consume(TokenType.LPAREN, "Expected '('");
        var args = new ArrayList<ExprNode>();
        if (!check(TokenType.RPAREN)) do { args.add(expression()); } while (match(TokenType.COMMA));
        consume(TokenType.RPAREN, "Expected ')'");
        return new ExprNode.NewExpr(name, args);
    }

    private ExprNode parseSuper() {
        consume(TokenType.KW_SUPER, "Expected 'super'");
        consume(TokenType.DOT, "Expected '.'");
        String method = consumeIdent("Expected method name");
        consume(TokenType.LPAREN, "Expected '('");
        var args = new ArrayList<ExprNode>();
        if (!check(TokenType.RPAREN)) do { args.add(expression()); } while (match(TokenType.COMMA));
        consume(TokenType.RPAREN, "Expected ')'");
        return new ExprNode.SuperCall(method, args);
    }

    private ExprNode parseArray() {
        consume(TokenType.LBRACKET, "Expected '['");
        var elems = new ArrayList<ExprNode>();
        if (!check(TokenType.RBRACKET))
            do { elems.add(expression()); } while (match(TokenType.COMMA) && !check(TokenType.RBRACKET));
        consume(TokenType.RBRACKET, "Expected ']'");
        return new ExprNode.ArrayLit(elems);
    }

    private ExprNode parseObject() {
        consume(TokenType.LBRACE, "Expected '{'");
        var entries = new ArrayList<Map.Entry<String, ExprNode>>();
        if (!check(TokenType.RBRACE)) {
            do {
                String key = check(TokenType.STRING) ? (String) advance().literal() : consumeIdent("Expected key");
                consume(TokenType.COLON, "Expected ':'");
                entries.add(Map.entry(key, expression()));
            } while (match(TokenType.COMMA) && !check(TokenType.RBRACE));
        }
        consume(TokenType.RBRACE, "Expected '}'");
        return new ExprNode.ObjLit(entries);
    }

    private String parseTypeName() {
        Token t = peek();
        if (t.type() == TokenType.IDENTIFIER || t.lexeme().matches("string|int|float|boolean|bool|void|any|number")) {
            advance(); return t.lexeme();
        }
        throw error("Expected type name");
    }

    private Token peek()               { return tokens.get(pos); }
    private boolean isAtEnd()          { return peek().type() == TokenType.EOF; }
    private Token advance()            { Token t = tokens.get(pos); if (!isAtEnd()) pos++; return t; }
    private boolean check(TokenType t) { return peek().type() == t; }
    private boolean match(TokenType t) { if (check(t)) { advance(); return true; } return false; }
    private Token consume(TokenType type, String msg) { if (!check(type)) throw error(msg); return advance(); }
    private String consumeIdent(String msg) { if (!check(TokenType.IDENTIFIER)) throw error(msg); return advance().lexeme(); }
    private void consumeOptSemi() { match(TokenType.SEMICOLON); }
    private ParseError error(String msg) { return new ParseError("Line " + peek().line() + ": " + msg); }
    private void synchronize() {
        advance();
        while (!isAtEnd()) {
            if (tokens.get(pos - 1).type() == TokenType.SEMICOLON) return;
            switch (peek().type()) {
                case KW_FUNC, KW_VAR, KW_CONST, KW_CLASS, KW_INTERFACE, KW_ENUM, KW_STRUCT,
                     KW_IF, KW_WHILE, KW_DO, KW_FOR, KW_RETURN, KW_PRINT, KW_TRY, KW_THROW -> { return; }
                default -> advance();
            }
        }
    }
    static class ParseError extends RuntimeException { ParseError(String m) { super(m); } }
}