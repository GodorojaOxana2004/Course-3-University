package com.example.pipeline;

import java.util.*;
import java.util.function.Function;

public class Pipeline<TContext> {
    private final List<IPipelineStep<TContext>> steps = new ArrayList<>();

    public Pipeline() {}

    public Pipeline<TContext> add(IPipelineStep<TContext> step) {
        steps.add(step);
        return this;
    }

    public void execute(TContext context) {
        for (IPipelineStep<TContext> step : new ArrayList<>(steps)) {
            if (ContextUtils.isDone(context)) break;
            step.execute(context);
            if (ContextUtils.isDone(context)) break;
        }
    }

    public String introspect() {
        StringBuilder sb = new StringBuilder();
        com.example.pipeline.introspect.Introspection.appendHeader(sb, this);
        for (IPipelineStep<TContext> step : steps) {
            step.describe(sb);
        }
        return sb.toString();
    }

    public void replaceFirstInstance(Class<?> typeToReplace, IPipelineStep<TContext> newStep) {
        for (int i = 0; i < steps.size(); i++) {
            if (typeToReplace.isInstance(steps.get(i))) { steps.set(i, newStep); return; }
        }
    }

    public void replaceAll(Class<?> typeToReplace, IPipelineStep<TContext> newStep) {
        for (int i = 0; i < steps.size(); i++) {
            if (typeToReplace.isInstance(steps.get(i))) { steps.set(i, newStep); }
        }
    }

    public void wrapAll(Function<IPipelineStep<TContext>, IPipelineStep<TContext>> wrapFunc) {
        for (int i = 0; i < steps.size(); i++) {
            steps.set(i, wrapFunc.apply(steps.get(i)));
        }
    }

    public void moveTo(Class<?> typeToMove, int index) {
        IPipelineStep<TContext> found = null;
        int foundIdx = -1;
        for (int i = 0; i < steps.size(); i++) {
            if (typeToMove.isInstance(steps.get(i))) { found = steps.get(i); foundIdx = i; break; }
        }
        if (found == null) return;
        steps.remove(foundIdx);
        if (index < 0) index = 0;
        if (index > steps.size()) index = steps.size();
        steps.add(index, found);
    }

    public List<IPipelineStep<TContext>> getSteps() { return Collections.unmodifiableList(steps); }
}
