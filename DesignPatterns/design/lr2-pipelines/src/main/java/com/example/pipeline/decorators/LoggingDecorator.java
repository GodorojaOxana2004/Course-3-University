package com.example.pipeline.decorators;

import com.example.pipeline.IPipelineStep;

public class LoggingDecorator<TContext> implements IPipelineStep<TContext> {
    private final IPipelineStep<TContext> inner;

    public LoggingDecorator(IPipelineStep<TContext> inner) { this.inner = inner; }

    @Override
    public void execute(TContext context) {
        System.out.println("[LOG] Starting step: " + inner);
        inner.execute(context);
        System.out.println("[LOG] Finished step: " + inner);
    }

    @Override
    public void describe(StringBuilder sb) {
        sb.append("LoggingDecorator(").append(inner.getClass().getSimpleName()).append(")\n");
        inner.describe(sb);
    }

    @Override
    public void accept(com.example.pipeline.visitor.IPipelineVisitor visitor) { visitor.visit(this); }
}
