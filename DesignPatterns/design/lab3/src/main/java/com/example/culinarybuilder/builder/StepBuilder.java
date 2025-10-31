package com.example.culinarybuilder.builder;

import com.example.culinarybuilder.model.MutableStep;
import com.example.culinarybuilder.model.Step;

public class StepBuilder {
    private MutableStep step = new MutableStep();

    public StepBuilder setDescription(String description) {
        step.setDescription(description);
        return this;
    }

    public Step build() {
        return step.toImmutable();
    }
}
