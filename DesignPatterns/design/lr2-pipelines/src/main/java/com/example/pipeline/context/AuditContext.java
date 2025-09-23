package com.example.pipeline.context;

import java.util.ArrayList;
import java.util.List;

public class AuditContext {
    private final List<String> events = new ArrayList<>();

    public void addEvent(String ev) { events.add(ev); }
    public List<String> getEvents() { return events; }
}
