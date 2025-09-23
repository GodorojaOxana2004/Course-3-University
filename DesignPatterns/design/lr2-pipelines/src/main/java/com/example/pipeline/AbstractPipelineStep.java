package com.example.pipeline;

public abstract class AbstractPipelineStep<TContext> implements IPipelineStep<TContext> {
    protected final String name;

    protected AbstractPipelineStep(String name) {
        this.name = name;
    }

    @Override
    public void describe(StringBuilder sb) {
        sb.append(getClass().getSimpleName()).append(" - ").append(name).append('\n');
    }

    @Override
    public String toString() {
        return getClass().getSimpleName() + "(" + name + ")";
    }
}
