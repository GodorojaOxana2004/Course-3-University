package com.example.dynamiclib;

public final class TypedKey<T> {
    private final int id;
    private final String name;
    private final Class<T> type;

    TypedKey(int id, String name, Class<T> type) {
        this.id = id;
        this.name = name;
        this.type = type;
    }

    public int id() { return id; }
    public String name() { return name; }
    public Class<T> type() { return type; }

    @Override
    public String toString() {
        return "TypedKey{" + name + "#" + id + " -> " + type.getSimpleName() + "}";
    }
}
