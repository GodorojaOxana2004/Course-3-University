package com.example.dynamiclib;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
        

public final class KeyRegistry {
    private final AtomicInteger counter = new AtomicInteger(1);
    private final ConcurrentHashMap<String, Integer> nameToId = new ConcurrentHashMap<>();
    private final ConcurrentHashMap<Integer, Class<?>> idToType = new ConcurrentHashMap<>();

    public <T> TypedKey<T> register(String name, Class<T> type) {
        Integer existing = nameToId.putIfAbsent(name, -1);
        if (existing != null) {
            Integer id = nameToId.get(name);
            Class<?> registeredType = idToType.get(id);
            if (!registeredType.equals(type)) {
                throw new KeyAlreadyRegisteredException("Key '" + name + "' already registered with different type: " + registeredType);
            }
            return new TypedKey<>(id, name, type);
        }

        int id = counter.getAndIncrement();
        nameToId.put(name, id);
        idToType.put(id, type);
        return new TypedKey<>(id, name, type);
    }

    public boolean isRegistered(String namespacedName) {
        return nameToId.containsKey(namespacedName);
    }
}
