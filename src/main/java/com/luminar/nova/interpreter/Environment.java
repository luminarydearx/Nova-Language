package com.luminar.nova.interpreter;

import java.util.HashMap;
import java.util.Map;

public final class Environment {
    private final Environment parent;
    private final Map<String, Object>  values    = new HashMap<>();
    private final Map<String, Boolean> constants = new HashMap<>();

    public Environment()              { this.parent = null; }
    public Environment(Environment p) { this.parent = p;    }

    public void define(String name, Object value)                { define(name, value, false); }

    public void define(String name, Object value, boolean isConst) {
        values.put(name, value);
        constants.put(name, isConst);
    }

    public Object get(String name) {
        if (values.containsKey(name)) return values.get(name);
        if (parent != null) return parent.get(name);
        throw new NovaRuntimeError("Undefined variable: '" + name + "'");
    }

    public void assign(String name, Object value) {
        if (values.containsKey(name)) {
            if (Boolean.TRUE.equals(constants.get(name)))
                throw new NovaRuntimeError("Cannot reassign constant: '" + name + "'");
            values.put(name, value);
            return;
        }
        if (parent != null) { parent.assign(name, value); return; }
        throw new NovaRuntimeError("Undefined variable: '" + name + "'");
    }

    public boolean isDefined(String name) {
        return values.containsKey(name) || (parent != null && parent.isDefined(name));
    }
}