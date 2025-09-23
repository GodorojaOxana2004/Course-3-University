package com.example.pipeline.context;

public class TextContext {
    private String text;
    private boolean done = false;
    private final AuditContext audit;

    public TextContext(String text, AuditContext audit) {
        this.text = text;
        this.audit = audit;
    }

    public String getText() { return text; }
    public void setText(String text) { this.text = text; }

    public boolean isDone() { return done; }
    public void setDone(boolean done) { this.done = done; }

    public AuditContext getAudit() { return audit; }
}
