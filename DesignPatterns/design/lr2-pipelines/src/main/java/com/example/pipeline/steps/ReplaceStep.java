package com.example.pipeline.steps;

import com.example.pipeline.AbstractPipelineStep;
import com.example.pipeline.context.TextContext;

public class ReplaceStep extends AbstractPipelineStep<TextContext> {
    private final String target;
    private final String replacement;

    public ReplaceStep(String target, String replacement) {
        super("Replace '" + target + "' -> '" + replacement + "'");
        this.target = target;
        this.replacement = replacement;
    }

    @Override
    public void execute(TextContext context) {
        String t = context.getText();
        if (t != null && t.contains(target)) {
            context.setText(t.replace(target, replacement));
            context.getAudit().addEvent("ReplaceStep: replaced " + target);
        }
    }
}
