package com.luminar.nova.interpreter;

import java.util.HashMap;
import java.util.Map;
import java.util.StringJoiner;

public final class NovaInstance {
    public final NovaClass klass;
    final Map<String, Object> fields = new HashMap<>();

    public NovaInstance(NovaClass klass) { this.klass = klass; }

    /** Get a property. Checks fields first, then methods (binding this). */
    public Object get(String name, Interpreter interp) {
        if (fields.containsKey(name)) return fields.get(name);
        NovaCallable method = klass.findMethod(name);
        if (method != null) return method.bind(this);
        throw new NovaRuntimeError("Undefined property '" + name + "' on " + klass.name);
    }

    public void set(String name, Object value) { fields.put(name, value); }

    @Override public String toString() {
        if (fields.isEmpty()) return klass.name + " {}";
        StringJoiner sj = new StringJoiner(", ", klass.name + " { ", " }");
        for (var e : fields.entrySet()) sj.add(e.getKey() + ": " + e.getValue());
        return sj.toString();
    }
}