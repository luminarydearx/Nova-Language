package com.luminar.nova.interpreter;

import java.util.List;
import java.util.Set;

/**
 * Runtime representation of a Nova interface.
 * Stores the set of required method names.
 */
public final class NovaInterface {
    public final String      name;
    public final Set<String> requiredMethods;
    public final List<String> parents;

    public NovaInterface(String name, Set<String> requiredMethods, List<String> parents) {
        this.name            = name;
        this.requiredMethods = requiredMethods;
        this.parents         = parents;
    }

    /** Check whether a NovaClass satisfies this interface. */
    public void checkImplementedBy(NovaClass klass) {
        for (String m : requiredMethods) {
            if (klass.findMethod(m) == null)
                throw new NovaRuntimeError(
                    "Class '" + klass.name + "' does not implement required method '" + m +
                    "' from interface '" + name + "'");
        }
    }

    @Override public String toString() { return "<interface " + name + ">"; }
}