package com.example.pipeline.steps;

import com.example.pipeline.AbstractPipelineStep;
import com.example.pipeline.context.TextContext;

public class LowercaseStep extends AbstractPipelineStep<TextContext> {
    public LowercaseStep() { super("To lowercase"); }

    @Override
    public void execute(TextContext context) {
        String t = context.getText();
        if (t != null) {
            context.setText(t.toLowerCase());
            context.getAudit().addEvent("LowercaseStep: lowered");
        }
    }
}
