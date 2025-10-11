package com.example.pipeline;

import com.example.pipeline.context.AuditContext;
import com.example.pipeline.context.TextContext;
import com.example.pipeline.decorators.LoggingDecorator;
import com.example.pipeline.decorators.TimingDecorator;
import com.example.pipeline.singleton.CommonSteps;
import com.example.pipeline.steps.*;

import java.util.Set;

public class Main {
    public static void main(String[] args) {
        AuditContext audit = new AuditContext();
        TextContext ctx = new TextContext("   Hello WORLD! sosati   ", audit);

        Pipeline<TextContext> pipeline = new Pipeline<>();
        pipeline.add(CommonSteps.TRIM)
                .add(new ReplaceStep("WORLD", "Java"))
                .add(CommonSteps.LOWER)
                .add(new ReplaceStep("sosati", "***"))
                .add(new WordCountStep());

    pipeline.wrapAll(s -> new LoggingDecorator<>(s));

        pipeline.execute(ctx);

        System.out.println("Final text: '" + ctx.getText() + "'");
        System.out.println("--- Audit events: ---");
        ctx.getAudit().getEvents().forEach(System.out::println);

        System.out.println("--- Introspection ---");
        System.out.println(pipeline.introspect());
    }
}
