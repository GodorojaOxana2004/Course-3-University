package com.example.pipeline.steps;

import com.example.pipeline.AbstractPipelineStep;
import com.example.pipeline.context.TextContext;

import java.util.Set;

public class StopOnProfanityStep extends AbstractPipelineStep<TextContext> {
    private final Set<String> blocked;

    public StopOnProfanityStep(Set<String> blocked) {
        super("Profanity stopper");
        this.blocked = blocked;
    }

    @Override
    public void execute(TextContext context) {
        String t = context.getText();
        if (t == null) return;
        for (String b : blocked) {
            if (t.toLowerCase().contains(b.toLowerCase())) {
                context.getAudit().addEvent("StopOnProfanityStep: found profanity " + b + ", stopping pipeline");
                context.setDone(true);
                return;
            }
        }
    }
}
