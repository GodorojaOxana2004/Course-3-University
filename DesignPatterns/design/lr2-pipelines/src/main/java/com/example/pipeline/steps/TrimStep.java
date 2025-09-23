package com.example.pipeline.steps;

import com.example.pipeline.AbstractPipelineStep;
import com.example.pipeline.context.TextContext;

public class TrimStep extends AbstractPipelineStep<TextContext> {
    public TrimStep() { super("Trim whitespace"); }

    @Override
    public void execute(TextContext context) {
        String t = context.getText();
        if (t != null) {
            context.setText(t.trim());
            context.getAudit().addEvent("TrimStep: trimmed");
        }
    }
}
