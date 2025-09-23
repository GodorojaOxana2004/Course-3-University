package com.example.pipeline.introspect;

public class Introspection {
    public static <T> void appendHeader(StringBuilder sb, T pipeline) {
        sb.append("Pipeline introspection for: ").append(pipeline.getClass().getSimpleName()).append('\n');
    }
}
