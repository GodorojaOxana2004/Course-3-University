package com.example.pipeline.visitor;

import com.example.pipeline.IPipelineStep;

public interface IPipelineVisitor {
    void visit(IPipelineStep<?> step);
}
