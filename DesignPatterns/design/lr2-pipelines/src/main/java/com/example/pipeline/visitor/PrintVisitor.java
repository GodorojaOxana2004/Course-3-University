package com.example.pipeline.visitor;

import com.example.pipeline.IPipelineStep;

public class PrintVisitor implements IPipelineVisitor {
    @Override
    public void visit(IPipelineStep<?> step) {
        System.out.println("Visitor visiting: " + step.getClass().getSimpleName());
    }
}
