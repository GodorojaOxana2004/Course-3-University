package com.example.dynamiclib;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

public final class DynamicContext {
    private final Map<Integer, Object> map = new ConcurrentHashMap<>();

    public <T> void put(TypedKey<T> key, T value) {
        if (value != null && !key.type().isInstance(value)) {
            throw new ClassCastException("Value for key " + key.name() + " is not of type " + key.type());
        }
        map.put(key.id(), value);
    }

    public <T> Optional<T> get(TypedKey<T> key) {
        Object v = map.get(key.id());
        if (v == null) return Optional.empty();
        return Optional.of(key.type().cast(v));
    }

    public <T> T getOrDefault(TypedKey<T> key, T defaultValue) {
        return get(key).orElse(defaultValue);
    }

    public boolean contains(TypedKey<?> key) {
        return map.containsKey(key.id());
    }

    public void remove(TypedKey<?> key) {
        map.remove(key.id());
    }
}
