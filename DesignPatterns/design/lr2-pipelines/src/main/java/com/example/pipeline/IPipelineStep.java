package com.example.pipeline;

public interface IPipelineStep<TContext> {
    void execute(TContext context);
    void describe(StringBuilder sb);
    default void accept(com.example.pipeline.visitor.IPipelineVisitor visitor) {
        visitor.visit(this);
    }
}
