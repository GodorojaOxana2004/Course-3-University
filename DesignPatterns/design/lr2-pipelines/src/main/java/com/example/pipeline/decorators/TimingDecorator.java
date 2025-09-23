package com.example.pipeline.decorators;

import com.example.pipeline.IPipelineStep;

public class TimingDecorator<TContext> implements IPipelineStep<TContext> {
    private final IPipelineStep<TContext> inner;

    public TimingDecorator(IPipelineStep<TContext> inner) { this.inner = inner; }

    @Override
    public void execute(TContext context) {
        long start = System.nanoTime();
        inner.execute(context);
        long end = System.nanoTime();
        System.out.println("[TIME] " + inner.getClass().getSimpleName() + " took " + (end - start) / 1_000_000.0 + " ms");
    }

    @Override
    public void describe(StringBuilder sb) {
        sb.append("TimingDecorator(").append(inner.getClass().getSimpleName()).append(")\n");
        inner.describe(sb);
    }

    @Override
    public void accept(com.example.pipeline.visitor.IPipelineVisitor visitor) { visitor.visit(this); }
}
