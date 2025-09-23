package com.example.pipeline.steps;

import com.example.pipeline.AbstractPipelineStep;
import com.example.pipeline.context.TextContext;

public class WordCountStep extends AbstractPipelineStep<TextContext> {
    private int lastCount = 0;

    public WordCountStep() { super("Word count"); }

    @Override
    public void execute(TextContext context) {
        String t = context.getText();
        if (t == null || t.isBlank()) {
            lastCount = 0;
        } else {
            lastCount = t.split("\\s+").length;
        }
        context.getAudit().addEvent("WordCountStep: " + lastCount);
    }

    public int getLastCount() { return lastCount; }
}
