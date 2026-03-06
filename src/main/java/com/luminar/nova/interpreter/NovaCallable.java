package com.luminar.nova.interpreter;

import com.luminar.nova.parser.ast.BlockNode;

import java.util.List;

// ── Callable interface ───────────────────────────────────────────────────────
interface NovaCallable {
    Object call(Interpreter interpreter, List<Object> args);
    int    arity();
    /** Bind a 'this' instance for method calls. Default: no-op (return self). */
    default NovaCallable bind(NovaInstance instance) { return this; }
}

// ── Functional interface for native lambdas ──────────────────────────────────
@FunctionalInterface
interface NativeBody {
    Object execute(Interpreter interp, List<Object> args);
}

// ── Native built-in function ─────────────────────────────────────────────────
final class NativeFunction implements NovaCallable {
    private final NativeBody body;
    NativeFunction(NativeBody body) { this.body = body; }
    @Override public int    arity()                                     { return -1; }
    @Override public Object call(Interpreter i, List<Object> args)      { return body.execute(i, args); }
    @Override public String toString()                                  { return "<native>"; }
}

// ── User-defined function (with closure + optional type annotations) ─────────
final class NovaFunction implements NovaCallable {
    final String       name;
    final List<String> params;
    final List<String> paramTypes;   // may be null or contain nulls for untyped params
    final String       returnType;   // null = untyped
    final BlockNode    body;
    final Environment  closure;

    NovaFunction(String name, List<String> params, List<String> paramTypes,
                 String returnType, BlockNode body, Environment closure) {
        this.name       = name;
        this.params     = params;
        this.paramTypes = paramTypes;
        this.returnType = returnType;
        this.body       = body;
        this.closure    = closure;
    }

    /** Returns a copy with 'this' bound in the closure environment. */
    @Override
    public NovaFunction bind(NovaInstance instance) {
        Environment env = new Environment(closure);
        env.define("this", instance);
        return new NovaFunction(name, params, paramTypes, returnType, body, env);
    }

    @Override public int arity() { return params.size(); }

    @Override
    public Object call(Interpreter interp, List<Object> args) {
        Environment funcEnv = new Environment(closure);
        for (int i = 0; i < params.size(); i++) {
            Object arg = i < args.size() ? args.get(i) : null;
            // Optional type check for each parameter
            if (paramTypes != null && i < paramTypes.size() && paramTypes.get(i) != null) {
                arg = interp.coerce(paramTypes.get(i), arg, "param '" + params.get(i) + "'");
            }
            funcEnv.define(params.get(i), arg);
        }
        try {
            interp.executeBlock(body, funcEnv);
        } catch (ReturnSignal r) {
            Object ret = r.value;
            if (returnType != null && !returnType.equals("void") && !returnType.equals("any")) {
                ret = interp.coerce(returnType, ret, "return value of '" + name + "'");
            }
            return ret;
        }
        return null;
    }

    @Override public String toString() { return "<func " + name + "/" + params.size() + ">"; }
}

// ── Control-flow signals ─────────────────────────────────────────────────────
final class ReturnSignal   extends RuntimeException { final Object value; ReturnSignal(Object v)   { super(null,null,true,false); value = v; } }
final class BreakSignal    extends RuntimeException { BreakSignal()    { super(null,null,true,false); } }
final class ContinueSignal extends RuntimeException { ContinueSignal() { super(null,null,true,false); } }

// ── Nova exception (created by 'throw') ──────────────────────────────────────
final class NovaException extends RuntimeException {
    final Object thrown;   // the value that was thrown
    NovaException(Object thrown) {
        super(thrown != null ? thrown.toString() : "null", null, true, false);
        this.thrown = thrown;
    }
}