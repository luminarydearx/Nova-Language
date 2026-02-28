package com.luminar.nova.interpreter;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Runtime representation of a Nova enum.
 *
 *   enum Direction { NORTH, SOUTH, EAST, WEST }
 *   var d = Direction.NORTH;
 *   print(d);           // "Direction.NORTH"
 *   print(d.name);      // "NORTH"
 *   print(d.ordinal);   // 0
 *   print(d == Direction.NORTH);  // true
 */
public final class NovaEnum {
    public final String name;
    private final Map<String, NovaEnumValue> values = new LinkedHashMap<>();

    public NovaEnum(String name, List<String> valueNames) {
        this.name = name;
        int ordinal = 0;
        for (String vn : valueNames)
            values.put(vn, new NovaEnumValue(name, vn, ordinal++));
    }

    public Object get(String valueName) {
        if (values.containsKey(valueName)) return values.get(valueName);
        if ("values".equals(valueName))    return values.values().stream().toList();
        if ("name".equals(valueName))      return name;
        throw new NovaRuntimeError("Enum '" + name + "' has no value '" + valueName + "'");
    }

    @Override public String toString() { return "<enum " + name + ">"; }
}

// ── A single enum value ───────────────────────────────────────────────────────
final class NovaEnumValue {
    public final String enumName;
    public final String name;
    public final int    ordinal;

    NovaEnumValue(String enumName, String name, int ordinal) {
        this.enumName = enumName; this.name = name; this.ordinal = ordinal;
    }

    public Object get(String prop) {
        return switch (prop) {
            case "name"    -> name;
            case "ordinal" -> (long) ordinal;
            default -> throw new NovaRuntimeError("Enum value has no property '" + prop + "'");
        };
    }

    @Override public String toString() { return enumName + "." + name; }
    @Override public boolean equals(Object o) { return this == o; }
    @Override public int hashCode()           { return System.identityHashCode(this); }
}