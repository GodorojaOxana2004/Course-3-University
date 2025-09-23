package com.example.pipeline;

import com.example.pipeline.context.AuditContext;
import com.example.pipeline.context.TextContext;
import com.example.pipeline.steps.TrimStep;
import com.example.pipeline.steps.LowercaseStep;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PipelineTest {
    @Test
    public void testTrimAndLowercase() {
        AuditContext audit = new AuditContext();
        TextContext ctx = new TextContext("  AbC  ", audit);
        Pipeline<TextContext> pipeline = new Pipeline<>();
        pipeline.add(new TrimStep()).add(new LowercaseStep());
        pipeline.execute(ctx);
        assertEquals("abc", ctx.getText());
    }
}
