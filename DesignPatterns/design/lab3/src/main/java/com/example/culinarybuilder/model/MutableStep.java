package com.example.culinarybuilder.model;

import java.util.UUID;

public class MutableStep {
    private String id = UUID.randomUUID().toString();
    private String description;
    private int line;

    public MutableStep(String description, int line) {
        this.description = description;
        this.line = line;
    }

    public MutableStep() {

    }

    public String getDescription() { return description; }
    public int getLine() { return line; }

    public Step toImmutable() {
        return new Step(id, description);
    }

    public void setDescription(String description) {
        this.description = description;
    }
}