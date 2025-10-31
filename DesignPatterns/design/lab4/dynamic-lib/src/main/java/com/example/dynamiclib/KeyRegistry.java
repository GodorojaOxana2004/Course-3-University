package com.example.dynamiclib;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public final class KeyRegistry {
    private final AtomicInteger counter = new AtomicInteger(1);
    private final ConcurrentHashMap<String, Integer> nameToId = new ConcurrentHashMap<>();
    private final ConcurrentHashMap<Integer, Class<?>> idToType = new ConcurrentHashMap<>();

    public <T> TypedKey<T> register(String namespacedName, Class<T> type) {
        Integer existing = nameToId.putIfAbsent(namespacedName, -1);
        if (existing != null) {
            Integer id = nameToId.get(namespacedName);
            Class<?> registeredType = idToType.get(id);
            if (!registeredType.equals(type)) {
                throw new KeyAlreadyRegisteredException("Key '" + namespacedName + "' already registered with different type: " + registeredType);
            }
            return new TypedKey<>(id, namespacedName, type);
        }

        int id = counter.getAndIncrement();
        nameToId.put(namespacedName, id);
        idToType.put(id, type);
        return new TypedKey<>(id, namespacedName, type);
    }

    public boolean isRegistered(String namespacedName) {
        return nameToId.containsKey(namespacedName);
    }
}
