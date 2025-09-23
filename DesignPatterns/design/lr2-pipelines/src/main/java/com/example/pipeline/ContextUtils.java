package com.example.pipeline;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class ContextUtils {
    public static boolean isDone(Object context) {
        if (context == null) return false;
        try {
            Method m = context.getClass().getMethod("isDone");
            Object res = m.invoke(context);
            if (res instanceof Boolean) return (Boolean) res;
        } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException ignored) {}
        try {
            java.lang.reflect.Field f = context.getClass().getDeclaredField("done");
            f.setAccessible(true);
            Object val = f.get(context);
            if (val instanceof Boolean) return (Boolean) val;
        } catch (Exception ignored) {}
        return false;
    }
}
